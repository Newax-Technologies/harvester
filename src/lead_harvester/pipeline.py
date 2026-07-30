import datetime
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy import select

from .canonical.merger import (
    attach_record_to_institution,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
)
from .config import Settings
from .database import get_session
from .integrations.lead_sync_emitter import LeadSyncEmitter
from .integrations.lead_sync_resync import resync_institution
from .models import RawSourceRecord, RunStatus, SourceRun, SourceType
from .models.canonical import CanonicalInstitution
from .models.provenance import FieldProvenance
from .models.resolution import ResolutionCandidate
from .resolution.normalize import normalize_domain, normalize_name, normalize_phone
from .resolution.orchestrator import resolve_incoming_record
from .sources.authorized_imports import AuthorizedImportInstitution, parse_authorized_import_csv
from .sources.geographic_tiling import build_queries_for_tile, generate_tiles
from .sources.google_places import GooglePlacesConnector


class LeadPipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        # Lazy: GooglePlacesConnector.__init__ raises ValueError without
        # GOOGLE_PLACES_API_KEY, but job.yaml's documented seeds-only
        # web-crawler mode never needs it -- constructing this eagerly here
        # broke that mode for any caller that only set up seeds.
        self._places_connector: GooglePlacesConnector | None = None
        self.lead_sync_emitter = LeadSyncEmitter(settings)

    @property
    def places_connector(self) -> GooglePlacesConnector:
        if self._places_connector is None:
            self._places_connector = GooglePlacesConnector(
                api_key=self.settings.google_places_api_key
            )
        return self._places_connector

    async def run(self) -> bool:
        """
        Returns True on success, False for a structural authorized-import
        failure (see _run_authorized_import) -- the other two paths either
        complete or raise, so they have no comparable "failed without
        raising" case and always return True.
        """
        if "authorized_import_file" in self.settings.job_config:
            return await self._run_authorized_import()
        elif "seeds" in self.settings.job_config:
            await self._run_web_crawler()
        else:
            await self._run_google_places()
        return True

    async def _run_web_crawler(self) -> None:
        import dataclasses

        from .sources.web import WebCrawler

        seeds = self.settings.job_config.get("seeds", [])
        if not seeds:
            print("No seeds provided.")
            return

        print(f"Starting WebCrawler with {len(seeds)} seeds...")
        crawler = WebCrawler(self.settings)
        leads = await crawler.crawl(seeds)

        # Populated by _resolve_or_log whenever a record in this run attaches
        # to an already lead_synced institution -- collected across the
        # whole run and re-emitted only after the transaction below commits
        # (see the comment at the bottom of this method), never mid-loop:
        # emitting before the outer commit could tell core-newax about data
        # that a later error in this same run rolls back.
        resync_ids: set[uuid.UUID] = set()

        # Wraps the whole session block (not just the try/except inside it)
        # so _emit_resync_events still runs even when the run fails and
        # re-raises: the inner finally's session.commit() durably persists
        # whatever records were processed before the failure (including any
        # already-lead_synced institution enrichment collected into
        # resync_ids so far) -- skipping the emit in that case would leave
        # the core-newax mirror silently stale for updates that DID land.
        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.WEBSITE,
                    run_metadata={"seeds_count": len(seeds), "leads_found": len(leads)},
                    status=RunStatus.STARTED,
                )
                session.add(run)
                await session.flush()

                try:
                    await self._retry_stranded_records(session, run, resync_ids)

                    for lead in leads:
                        record = RawSourceRecord(
                            source_run_id=run.id,
                            source_type=SourceType.WEBSITE,
                            source_id=lead.website,
                            raw_payload=dataclasses.asdict(lead),
                            # Normalized the same way as the Google Places path
                            # (process_place, below) -- otherwise domain-based
                            # blocking could never match a web-crawled record
                            # against a Google Places record for the same
                            # institution, since lead.website is a full origin
                            # like "https://www.example.edu" while Google
                            # Places' normalized_domain is "example.edu".
                            normalized_name=normalize_name(lead.organization or lead.name),
                            normalized_phone=(
                                normalize_phone(
                                    lead.phone,
                                    default_region=self.settings.lead_sync_default_country_code,
                                )
                                if lead.phone
                                else None
                            ),
                            normalized_domain=(
                                normalize_domain(lead.website) if lead.website else None
                            ),
                            location=None,
                        )
                        session.add(record)
                        await session.flush()
                        await self._resolve_or_log(session, run, record, resync_ids)

                    run.status = RunStatus.COMPLETED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                except Exception as e:
                    run.status = RunStatus.FAILED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                    run.run_metadata = {**run.run_metadata, "error": str(e)}
                    raise
                finally:
                    await session.commit()
        finally:
            await self._emit_resync_events(resync_ids)
        print(f"WebCrawler finished. Found {len(leads)} leads.")

    async def _run_authorized_import(self) -> bool:
        """
        Returns True on success (including "nothing to do"), False for a
        structural failure (missing config, unreadable/malformed CSV) --
        the caller (cli.py's import_authorized) uses this to decide its
        process exit code, since a scheduler or operator must not record a
        structurally invalid import as successful just because this
        method returned without raising.
        """
        import asyncio

        import_file = self.settings.job_config.get("authorized_import_file", "")
        source_reference = self.settings.job_config.get("authorized_import_source_reference", "")
        if not import_file:
            print("No authorized_import_file provided.")
            return False
        if not source_reference:
            print("authorized_import_source_reference is required for authorized imports.")
            return False

        try:
            csv_text = await asyncio.to_thread(Path(import_file).read_text, encoding="utf-8")
        except OSError as e:
            print(f"Could not read authorized import file {import_file}: {e}")
            return False

        try:
            parsed = parse_authorized_import_csv(
                csv_text,
                source_reference=source_reference,
                default_country_code=self.settings.lead_sync_default_country_code,
            )
        except ValueError as e:
            print(f"Authorized import file is malformed: {e}")
            return False

        for reason in parsed.skipped:
            print(f"[AuthorizedImport] Skipped {reason}")

        # See the matching comment in _run_web_crawler: this wraps the whole
        # session block (not just its inner try/except) so the emit still
        # runs even when the run fails and re-raises, since the inner
        # finally's commit durably persists whatever was processed before
        # the failure.
        resync_ids: set[uuid.UUID] = set()

        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.AUTHORIZED_IMPORT,
                    run_metadata={
                        "source_reference": source_reference,
                        "institutions_parsed": len(parsed.institutions),
                        "rows_skipped": len(parsed.skipped),
                        "skipped": parsed.skipped,
                    },
                    status=RunStatus.STARTED,
                )
                session.add(run)
                await session.flush()

                try:
                    await self._retry_stranded_records(session, run, resync_ids)

                    skipped_existing = 0
                    updated_existing = 0
                    for institution in parsed.institutions:
                        existing_record = await self._find_authorized_import_record(
                            session, institution.source_id
                        )
                        if (
                            existing_record is not None
                            and not self._authorized_import_has_new_evidence(
                                existing_record.raw_payload or {}, institution
                            )
                        ):
                            skipped_existing += 1
                            continue

                        record = self._build_authorized_import_record(run, institution)
                        session.add(record)
                        await session.flush()

                        if existing_record is None:
                            await self._resolve_or_log(session, run, record, resync_ids)
                            continue

                        updated_existing += 1
                        canonical_id = await find_canonical_for_raw_record(
                            session, existing_record.id
                        )
                        if canonical_id is None:
                            # Not yet resolved (still awaiting human review, or
                            # stranded and already retried this run via
                            # _retry_stranded_records above) -- route the
                            # updated snapshot through the normal resolution
                            # path like any fresh record, rather than silently
                            # discarding the new evidence it carries.
                            await self._resolve_or_log(session, run, record, resync_ids)
                            continue

                        target_institution = await session.get(CanonicalInstitution, canonical_id)
                        target_branch = await find_branch_for_raw_record(
                            session, target_institution.id, existing_record
                        )
                        await self._attach_or_log(
                            session, run, record, target_institution, target_branch, resync_ids
                        )

                    if skipped_existing:
                        run.run_metadata = {
                            **run.run_metadata,
                            "institutions_already_imported": skipped_existing,
                        }
                    if updated_existing:
                        run.run_metadata = {
                            **run.run_metadata,
                            "institutions_updated": updated_existing,
                        }

                    run.status = RunStatus.COMPLETED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                except Exception as e:
                    run.status = RunStatus.FAILED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                    run.run_metadata = {**run.run_metadata, "error": str(e)}
                    raise
                finally:
                    await session.commit()
        finally:
            await self._emit_resync_events(resync_ids)
        print(f"Authorized import finished. Processed {len(parsed.institutions)} institution(s).")
        return True

    @staticmethod
    async def _find_authorized_import_record(session, source_id: str) -> RawSourceRecord | None:
        """
        Finds the most recent previously-imported RawSourceRecord for this
        institution's stable source_id (see
        AuthorizedImportInstitution.source_id), if any. Returning the full
        record (not just an existence check) lets the caller diff its
        raw_payload against the freshly parsed institution to tell an
        unchanged rerun from one that supplies genuinely new evidence.
        """
        stmt = (
            select(RawSourceRecord)
            .where(
                RawSourceRecord.source_type == SourceType.AUTHORIZED_IMPORT,
                RawSourceRecord.source_id == source_id,
            )
            .order_by(RawSourceRecord.extracted_at.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def _authorized_import_has_new_evidence(
        existing_payload: dict, institution: AuthorizedImportInstitution
    ) -> bool:
        """
        source_id is derived only from institution_name + website/address
        (see AuthorizedImportInstitution.source_id) -- it intentionally
        ignores contacts and every other mutable field, so a matching
        source_id does not mean an identical row. Without this check,
        _run_authorized_import treated every matching identity as an
        unchanged rerun and skipped the whole institution, silently
        discarding a newly declared contact or a previously-blank field
        the spreadsheet has since filled in.

        Contacts are compared including person_name/role (not just
        contact_type + contact_value): a later CSV version that fills in
        or corrects the decision-maker metadata for an already-declared
        phone/email must count as new evidence too, not just a brand new
        contact_type+value pair -- see the matching update in
        canonical/merger.py's _add_contact_if_present, which now enriches
        an existing ContactPoint's person_name/role instead of only ever
        writing them on first creation.
        """
        existing_contacts = {
            (
                c.get("contact_type"),
                c.get("contact_value"),
                c.get("person_name") or "",
                c.get("role") or "",
            )
            for c in existing_payload.get("contacts") or []
        }
        new_contacts = {
            (c.contact_type, c.contact_value, c.person_name or "", c.role or "")
            for c in institution.contacts
        }
        if new_contacts - existing_contacts:
            return True

        for attr in (
            "institution_type",
            "website",
            "address",
            "city",
            "country",
            "country_code",
            "notes",
        ):
            if not existing_payload.get(attr) and getattr(institution, attr):
                return True
        return False

    @staticmethod
    async def _attach_or_log(
        session,
        run: SourceRun,
        record: RawSourceRecord,
        institution: CanonicalInstitution,
        target_branch,
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        # Same isolation reasoning as _resolve_or_log: one institution's
        # enrichment failing (e.g. a constraint violation) must not abort
        # the whole import run, and must run inside a SAVEPOINT so it
        # doesn't leave the surrounding transaction aborted for every
        # subsequent institution/commit.
        try:
            async with session.begin_nested():
                await attach_record_to_institution(
                    session, record, institution, target_branch=target_branch
                )
                if resync_ids is not None and institution.lead_synced_at is not None:
                    resync_ids.add(institution.id)
        except Exception as e:
            unresolved = list(run.run_metadata.get("unresolved_records", []))
            unresolved.append({"raw_record_id": str(record.id), "error": str(e)})
            run.run_metadata = {**run.run_metadata, "unresolved_records": unresolved}
            print(f"Applying new authorized-import evidence failed for raw record {record.id}: {e}")

    @staticmethod
    def _build_authorized_import_record(
        run: SourceRun, institution: AuthorizedImportInstitution
    ) -> RawSourceRecord:
        import dataclasses

        phone_contact = next(
            (c for c in institution.contacts if c.contact_type == "phone" and c.contact_value),
            None,
        )
        return RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.AUTHORIZED_IMPORT,
            source_id=institution.source_id,
            raw_payload=dataclasses.asdict(institution),
            normalized_name=normalize_name(institution.institution_name),
            normalized_phone=(
                normalize_phone(
                    phone_contact.contact_value, default_region=institution.country_code
                )
                if phone_contact
                else None
            ),
            normalized_domain=(
                normalize_domain(institution.website) if institution.website else None
            ),
            location=None,
        )

    async def _run_google_places(self) -> None:
        tiles = generate_tiles(self.settings.job_config)
        categories = self.settings.job_config.get("categories", ["FORMAL_EDUCATION"])

        # See the matching comment in _run_web_crawler: this wraps the whole
        # session block (not just its inner try/except) so the emit still
        # runs even when the run fails and re-raises, since the inner
        # finally's commit durably persists whatever was processed before
        # the failure.
        resync_ids: set[uuid.UUID] = set()

        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.GOOGLE_PLACES,
                    run_metadata={"categories": categories, "tiles": len(tiles)},
                    status=RunStatus.STARTED,
                )
                session.add(run)
                await session.flush()

                try:
                    await self._retry_stranded_records(session, run, resync_ids)

                    for tile in tiles:
                        queries = build_queries_for_tile(tile, categories)
                        for query in queries:
                            print(f"Executing Google Places query: {query}")
                            # In a real app this would be async, but keeping sync for now if connector is sync
                            places = self.places_connector.search(query)

                            for place in places:
                                await self.process_place(session, run, place, resync_ids)

                    run.status = RunStatus.COMPLETED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                except Exception as e:
                    run.status = RunStatus.FAILED
                    run.completed_at = datetime.datetime.now(datetime.UTC)
                    run.run_metadata = {**run.run_metadata, "error": str(e)}
                    raise
                finally:
                    await session.commit()
        finally:
            await self._emit_resync_events(resync_ids)

    async def process_place(
        self,
        session,
        run: SourceRun,
        place: dict[str, Any],
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        source_id = place.get("id")
        if not source_id:
            return

        name = place.get("displayName", {}).get("text", "")
        # internationalPhoneNumber is always "+"-prefixed (unambiguous on
        # its own); nationalPhoneNumber never is, so it needs a region hint
        # to normalize consistently -- prefer the international form when
        # Places supplies one (it's requested in the connector's field
        # mask) and only fall back to national+region-hint otherwise.
        phone = place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber", "")
        website = place.get("websiteUri", "")

        loc_dict = place.get("location", {})
        lat = loc_dict.get("latitude")
        lng = loc_dict.get("longitude")

        location_wkt = None
        if lat is not None and lng is not None:
            location_wkt = f"SRID=4326;POINT({lng} {lat})"

        record = RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.GOOGLE_PLACES,
            source_id=source_id,
            raw_payload=place,
            normalized_name=normalize_name(name),
            normalized_phone=normalize_phone(
                phone, default_region=self.settings.lead_sync_default_country_code
            ),
            normalized_domain=normalize_domain(website),
            location=location_wkt,
        )
        session.add(record)
        await session.flush()
        await self._resolve_or_log(session, run, record, resync_ids)

    # Source types resolve_incoming_record actually handles. LINKEDIN records
    # are never passed to it -- they're picked up by an entirely separate
    # mechanism (ResearchBrain.process_all_pending()) that's waiting for AI
    # analysis, not entity resolution. MANUAL records don't need retrying
    # either: manual_leads.py writes their canonical institution and
    # "branch_membership" FieldProvenance synchronously in the same request,
    # so a real MANUAL record is never left without provenance. Retrying an
    # unscoped set of "no provenance, no pending candidate" records
    # previously swept in every LinkedIn profile still waiting on
    # linkedin-research too: _resolve_or_log would resolve it into a bare
    # CanonicalInstitution with "branch_membership" provenance before any AI
    # analysis ever ran, and that same provenance link is exactly what
    # process_all_pending's own exclusion query treats as "already
    # researched" -- silently and permanently starving it of research.
    _RESOLUTION_ELIGIBLE_SOURCE_TYPES = (
        SourceType.WEBSITE,
        SourceType.GOOGLE_PLACES,
        SourceType.AUTHORIZED_IMPORT,
    )

    async def _retry_stranded_records(
        self,
        session,
        run: SourceRun,
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        """
        Retries resolution for every raw record a previous run's
        _resolve_or_log caught an exception for. That failure was
        previously only ever logged into that earlier run's own
        run_metadata['unresolved_records'] -- nothing outside that dict
        ever read it back, so the record stayed permanently stranded: no
        canonical institution, and (since the failure aborts
        resolve_incoming_record before any ResolutionCandidate row from
        this attempt survives the savepoint rollback) no entry in the
        resolution-reviews queue either, with no way for a human or any
        later process to ever notice or retry it.

        "Stranded" means: belongs to a source type resolve_incoming_record
        actually handles (see _RESOLUTION_ELIGIBLE_SOURCE_TYPES above);
        neither canonicalized (no FieldProvenance link at all, the same
        general check find_canonical_for_raw_record uses) nor already
        sitting in the pending human-review queue (a live
        ResolutionCandidate with review_outcome unset means a human, not
        this retry, owns resolving it -- re-running resolve_incoming_record
        against it would just create duplicate candidates for the same
        ambiguity). Runs at the start of every pipeline invocation so a
        transient failure (a DB hiccup, a since-fixed bug) self-heals on
        the next run instead of needing a dedicated backfill script.

        Claims stranded rows via SELECT ... FOR UPDATE SKIP LOCKED, the
        same pattern OutreachAutomator.run() and
        ResearchBrain.process_all_pending() already use for their own
        claim queries -- orchestrator.py's resolve_incoming_record
        docstring documents that two ingestion runs (e.g. an overlapping
        schedule, or google_places + web crawler running in parallel) can
        genuinely overlap. Without locking, two concurrent runs would both
        select the same stranded record here and both call
        resolve_incoming_record on it, producing two separate
        FieldProvenance/CanonicalInstitution rows for one raw record --
        a stronger duplicate than the documented "two different new
        records" limitation, since this is the SAME record resolved twice.
        The lock is held for the rest of this run's transaction (this
        method runs inside the same session the whole pipeline run
        commits at the end), which is intended: it keeps a concurrent
        run from claiming these rows until this run's outcome (success or
        rollback) is final.
        """
        canonicalized = select(FieldProvenance.raw_record_id)
        pending_review = select(ResolutionCandidate.raw_record_id).where(
            ResolutionCandidate.review_outcome.is_(None)
        )
        stmt = (
            select(RawSourceRecord)
            .where(RawSourceRecord.source_type.in_(self._RESOLUTION_ELIGIBLE_SOURCE_TYPES))
            .where(RawSourceRecord.id.not_in(canonicalized))
            .where(RawSourceRecord.id.not_in(pending_review))
            .with_for_update(skip_locked=True)
        )
        stranded = list(await session.scalars(stmt))
        if stranded:
            print(f"Retrying resolution for {len(stranded)} previously-stranded record(s)...")
        for record in stranded:
            await self._resolve_or_log(session, run, record, resync_ids)

    @staticmethod
    async def _resolve_or_log(
        session,
        run: SourceRun,
        record: RawSourceRecord,
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        # A resolution failure for one record must never abort the rest of
        # the run -- the outer per-run except/finally would otherwise mark
        # the whole run FAILED and stop processing every remaining
        # tile/place/lead. Logged into run_metadata so it's visible, not
        # silently dropped.
        #
        # Run inside a SAVEPOINT (begin_nested): a failed database operation
        # (e.g. a constraint violation) leaves the surrounding Postgres
        # transaction aborted -- every subsequent statement on it fails with
        # "current transaction is aborted" until something rolls back. Catching
        # the exception here without a savepoint would still leave every
        # later record's flush, and the run's own final commit, broken.
        try:
            async with session.begin_nested():
                await resolve_incoming_record(session, record, resync_ids=resync_ids)
        except Exception as e:
            unresolved = list(run.run_metadata.get("unresolved_records", []))
            unresolved.append({"raw_record_id": str(record.id), "error": str(e)})
            # run_metadata is a plain JSONB column (no MutableDict tracking),
            # so mutating the existing dict in place would never be detected
            # as a change -- reassign a new dict so the attribute-set event
            # actually marks `run` dirty.
            run.run_metadata = {**run.run_metadata, "unresolved_records": unresolved}
            print(f"Entity resolution failed for raw record {record.id}: {e}")

    async def _emit_resync_events(self, resync_ids: set[uuid.UUID]) -> None:
        # Fire-and-forget, same as LeadSyncEmitter itself -- a delivery
        # failure here must never fail (or be allowed to look like it
        # failed) the ingestion run that already committed successfully.
        for institution_id in resync_ids:
            try:
                await resync_institution(self.lead_sync_emitter, institution_id)
            except Exception as e:
                print(f"lead_sync resync failed for institution {institution_id}: {e}")
