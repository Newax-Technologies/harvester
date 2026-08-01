import datetime
import hashlib
import uuid
from collections import defaultdict
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
from .models import RawPageSnapshot, RawSourceRecord, RunStatus, SourceRun, SourceType
from .models.canonical import CanonicalInstitution
from .models.provenance import FieldProvenance
from .models.resolution import ResolutionCandidate
from .models.signal import Signal, SignalType
from .resolution.normalize import normalize_domain, normalize_name, normalize_phone
from .resolution.orchestrator import resolve_incoming_record
from .services.lead_profile_service import link_page_snapshots_to_institution, refresh_lead_profile
from .sources.apple_maps import AppleMapsConnector
from .sources.authorized_imports import AuthorizedImportInstitution, parse_authorized_import_csv
from .sources.geographic_tiling import build_queries_for_tile, generate_tiles
from .sources.google_places import GooglePlacesConnector
from .sources.telegram_channels import TelegramChannelConnector
from .sources.yandex_maps import YandexMapsConnector


class LeadPipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        # Lazy: GooglePlacesConnector.__init__ raises ValueError without
        # GOOGLE_PLACES_API_KEY, but job.yaml's documented seeds-only
        # web-crawler mode never needs it -- constructing this eagerly here
        # broke that mode for any caller that only set up seeds.
        self._places_connector: GooglePlacesConnector | None = None
        self._yandex_connector: YandexMapsConnector | None = None
        self._apple_connector: AppleMapsConnector | None = None
        self.lead_sync_emitter = LeadSyncEmitter(settings)

    @property
    def places_connector(self) -> GooglePlacesConnector:
        if self._places_connector is None:
            self._places_connector = GooglePlacesConnector(
                api_key=self.settings.google_places_api_key
            )
        return self._places_connector

    @property
    def yandex_connector(self) -> YandexMapsConnector:
        if self._yandex_connector is None:
            self._yandex_connector = YandexMapsConnector(api_key=self.settings.yandex_maps_api_key)
        return self._yandex_connector

    @property
    def apple_connector(self) -> AppleMapsConnector:
        if self._apple_connector is None:
            self._apple_connector = AppleMapsConnector(
                team_id=self.settings.apple_maps_team_id,
                key_id=self.settings.apple_maps_key_id,
                private_key=self.settings.apple_maps_private_key,
            )
        return self._apple_connector

    async def run(self) -> bool:
        """
        Returns True on success, False for a structural authorized-import
        failure (see _run_authorized_import) -- the other paths either
        complete or raise, so they have no comparable "failed without
        raising" case and always return True.

        places_provider selects which tile-based maps connector runs
        (default "google" for backwards compatibility with every existing
        job.yaml that doesn't set it) -- "apple"/"yandex" reuse the exact
        same tile/query-generation machinery (geographic_tiling.py) as
        Google Places, just against a different connector and SourceType.
        """
        if "authorized_import_file" in self.settings.job_config:
            return await self._run_authorized_import()
        elif "seeds" in self.settings.job_config or "search_queries" in self.settings.job_config:
            await self._run_web_crawler()
        elif "telegram_channels" in self.settings.job_config:
            await self._run_telegram()
        elif self.settings.job_config.get("places_provider") == "apple":
            await self._run_apple_maps()
        elif self.settings.job_config.get("places_provider") == "yandex":
            await self._run_yandex_maps()
        else:
            await self._run_google_places()
        return True

    async def _run_web_crawler(self) -> None:
        import dataclasses

        from .sources.web import WebCrawler

        seeds = list(self.settings.job_config.get("seeds", []))

        # search_queries is an optional additional seed source: sources/
        # search.py's BraveSearchSource previously had zero callers anywhere
        # in this codebase (dead since it was written -- see
        # docs/CODE_REVIEW_LESSONS.md pattern 2 on not leaving an orphaned
        # implementation lying around). Wired in here rather than as a
        # separate pipeline mode, since its whole purpose is discovering
        # more seed URLs for the SAME web crawler that already exists, not
        # a distinct ingestion path with its own resolution logic.
        search_queries = self.settings.job_config.get("search_queries", [])
        if search_queries:
            if not self.settings.brave_search_api_key:
                print(
                    "search_queries configured but BRAVE_SEARCH_API_KEY is not set -- "
                    "skipping search-based seed discovery."
                )
            else:
                from .sources.search import BraveSearchSource

                search_source = BraveSearchSource(api_key=self.settings.brave_search_api_key)
                discovered: set[str] = set()
                for query in search_queries:
                    print(f"Discovering seeds via search: {query}")
                    results = await search_source.search(query)
                    discovered.update(result.url for result in results if result.url)
                new_seeds = sorted(discovered - set(seeds))
                if new_seeds:
                    print(f"Discovered {len(new_seeds)} new seed(s) via search.")
                seeds.extend(new_seeds)

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

                # docs/ROADMAP.md module 3's raw_snapshot sub-concern: one
                # row per page this crawl attempted (success or failure),
                # not just the domain-aggregated Leads above -- see
                # models/source.py::RawPageSnapshot's own docstring for why
                # this exists separately from RawSourceRecord.
                #
                # Correction: a single crawl() call (and so a single
                # SourceRun) fetches every seed domain in `seeds`, not just
                # one -- source_run_id alone can't distinguish which
                # institution's website a given snapshot belongs to.
                # normalized_domain is stamped on every snapshot up front
                # (always computable from final_url/url); raw_source_record_id/
                # institution_id are backfilled below, once each domain's
                # own RawSourceRecord exists and (for institution_id) has
                # been resolved -- snapshots_by_domain keeps the just-added,
                # still-uncommitted ORM objects addressable by domain for
                # that backfill.
                snapshots_by_domain: dict[str, list[RawPageSnapshot]] = defaultdict(list)
                for snapshot in crawler.snapshots:
                    domain = normalize_domain(snapshot.final_url or snapshot.url)
                    page_snapshot = RawPageSnapshot(
                        source_run_id=run.id,
                        url=snapshot.url,
                        final_url=snapshot.final_url,
                        normalized_domain=domain,
                        status_code=snapshot.status_code,
                        content_type=snapshot.content_type,
                        html=snapshot.html,
                        fetch_error=snapshot.fetch_error,
                    )
                    session.add(page_snapshot)
                    snapshots_by_domain[domain].append(page_snapshot)

                try:
                    await self._retry_stranded_records(session, run, resync_ids)

                    for lead in leads:
                        record_domain = normalize_domain(lead.website) if lead.website else None
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
                            normalized_domain=record_domain,
                            location=None,
                        )
                        session.add(record)
                        await session.flush()
                        institution = await self._resolve_or_log(
                            session, run, record, resync_ids, record_history=False
                        )

                        # Link every page fetched for this domain to the
                        # record it produced -- see the snapshots_by_domain
                        # comment above and models/source.py::RawPageSnapshot's
                        # docstring. A plain in-memory attribute set, never
                        # itself a failure point, so it stays outside the
                        # savepoint below.
                        record_snapshots = snapshots_by_domain.get(record_domain or "", [])
                        for page_snapshot in record_snapshots:
                            page_snapshot.raw_source_record_id = record.id

                        # Correction: _resolve_or_log's own refresh_lead_profile
                        # (called from inside resolve_incoming_record, before
                        # it returns `institution` above) runs before this
                        # record's detected-technology Signal rows
                        # (_persist_detected_signals, also inside
                        # _resolve_or_log) and before the snapshot linkage
                        # below ever exists -- so that first refresh always
                        # scores off ZERO of this crawl's own evidence.
                        # Refresh again now that both are actually attached,
                        # so website_quality_tier/service_gap_score/detection
                        # status reflect the crawl that just ran, not just
                        # whatever evidence predates it.
                        if institution is not None:
                            await self._link_snapshots_and_refresh(
                                session, run, institution, page_snapshots=record_snapshots
                            )

                    # Correction: a domain this crawl actually fetched
                    # pages for, but that never entered `leads` at all
                    # (_extract_lead found no identity/contact data, or
                    # every fetch for it failed) gets no RawSourceRecord,
                    # and so never gets a chance at the snapshot-linking
                    # loop above -- institution_id stays permanently null
                    # for a real, genuinely attempted crawl, reporting a
                    # misleading NOT_CRAWLED instead of CRAWL_FAILED/
                    # NOT_DETECTED for any institution whose domain
                    # happens to already be known (e.g. resolved via
                    # Google Places, not this crawl). Link those snapshots
                    # directly by domain match against an already-resolved
                    # institution -- there is no RawSourceRecord to link
                    # them through, since none was ever created.
                    leadless_domains = {domain for domain in snapshots_by_domain if domain} - {
                        normalize_domain(lead.website) for lead in leads if lead.website
                    }
                    if leadless_domains:
                        matched_institutions = (
                            await session.scalars(
                                select(CanonicalInstitution).where(
                                    CanonicalInstitution.domain.in_(leadless_domains)
                                )
                            )
                        ).all()
                        institutions_by_domain: dict[str, list[CanonicalInstitution]] = defaultdict(
                            list
                        )
                        for matched_institution in matched_institutions:
                            institutions_by_domain[matched_institution.domain].append(
                                matched_institution
                            )
                        for domain, institutions in institutions_by_domain.items():
                            if len(institutions) != 1:
                                # Correction: CanonicalInstitution.domain
                                # carries no uniqueness constraint -- linking
                                # this domain's snapshots to every institution
                                # that happens to share it would make the
                                # last one iterated the arbitrary persisted
                                # owner, while earlier ones already refreshed
                                # profiles from evidence they don't actually
                                # own. Skip ambiguous domains rather than
                                # guess; route them through entity resolution
                                # instead if this needs to be automatic.
                                print(
                                    f"Skipping leadless-domain snapshot link for {domain!r}: "
                                    f"{len(institutions)} institutions share this domain."
                                )
                                continue
                            matched_institution = institutions[0]
                            await self._link_snapshots_and_refresh(
                                session,
                                run,
                                matched_institution,
                                page_snapshots=snapshots_by_domain[domain],
                            )

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

    async def _run_yandex_maps(self) -> None:
        tiles = generate_tiles(self.settings.job_config)
        categories = self.settings.job_config.get("categories", ["FORMAL_EDUCATION"])
        resync_ids: set[uuid.UUID] = set()

        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.YANDEX,
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
                            print(f"Executing Yandex Maps query: {query}")
                            features = self.yandex_connector.search(query)
                            for feature in features:
                                await self.process_yandex_place(session, run, feature, resync_ids)

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

    async def process_yandex_place(
        self,
        session,
        run: SourceRun,
        feature: dict[str, Any],
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        properties = feature.get("properties", {})
        company = properties.get("CompanyMetaData", {})
        source_id = company.get("id")
        if not source_id:
            return

        name = company.get("name") or properties.get("name", "")
        phones = company.get("Phones", [])
        phone = phones[0].get("formatted", "") if phones else ""
        website = company.get("url", "")

        # GeoJSON coordinates are [longitude, latitude], the opposite order
        # from Google Places' {latitude, longitude} dict -- easy to
        # transpose by accident, so kept explicit rather than unpacked
        # positionally.
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        location_wkt = None
        if len(coordinates) == 2:
            lng, lat = coordinates
            location_wkt = f"SRID=4326;POINT({lng} {lat})"

        record = RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.YANDEX,
            source_id=source_id,
            raw_payload=feature,
            normalized_name=normalize_name(name),
            normalized_phone=normalize_phone(
                phone, default_region=self.settings.lead_sync_default_country_code
            )
            if phone
            else None,
            normalized_domain=normalize_domain(website) if website else None,
            location=location_wkt,
        )
        session.add(record)
        await session.flush()
        await self._resolve_or_log(session, run, record, resync_ids)

    async def _run_apple_maps(self) -> None:
        tiles = generate_tiles(self.settings.job_config)
        categories = self.settings.job_config.get("categories", ["FORMAL_EDUCATION"])
        resync_ids: set[uuid.UUID] = set()

        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.APPLE_MAPS,
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
                            print(f"Executing Apple Maps query: {query}")
                            results = self.apple_connector.search(query)
                            for result in results:
                                await self.process_apple_place(session, run, result, resync_ids)

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

    async def process_apple_place(
        self,
        session,
        run: SourceRun,
        result: dict[str, Any],
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        name = result.get("name", "")
        if not name:
            return

        address_lines = result.get("formattedAddressLines", [])
        address = ", ".join(address_lines)

        # Apple's /v1/search response carries no persistent POI id (unlike
        # Google Places' `id`/Yandex's CompanyMetaData.id) -- derive a
        # stable one from name+address the same way
        # sources/authorized_imports.py::AuthorizedImportInstitution.source_id
        # does for its own no-natural-id rows, so re-running the same query
        # against the same result doesn't fabricate a new identity for an
        # unchanged place every time.
        digest = hashlib.sha256(f"{normalize_name(name)}|{address}".encode()).hexdigest()[:16]
        source_id = f"apple:{digest}"

        coordinate = result.get("coordinate", {})
        lat = coordinate.get("latitude")
        lng = coordinate.get("longitude")
        location_wkt = None
        if lat is not None and lng is not None:
            location_wkt = f"SRID=4326;POINT({lng} {lat})"

        record = RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.APPLE_MAPS,
            source_id=source_id,
            raw_payload=result,
            normalized_name=normalize_name(name),
            normalized_phone=None,
            normalized_domain=None,
            location=location_wkt,
        )
        session.add(record)
        await session.flush()
        await self._resolve_or_log(session, run, record, resync_ids)

    async def _run_telegram(self) -> None:
        channels = self.settings.job_config.get("telegram_channels", [])
        if not channels:
            print("No telegram_channels provided.")
            return

        connector = TelegramChannelConnector(user_agent=self.settings.user_agent)
        resync_ids: set[uuid.UUID] = set()

        try:
            async with get_session() as session:
                run = SourceRun(
                    source_type=SourceType.TELEGRAM,
                    run_metadata={"channels_count": len(channels)},
                    status=RunStatus.STARTED,
                )
                session.add(run)
                await session.flush()

                try:
                    await self._retry_stranded_records(session, run, resync_ids)

                    for channel in channels:
                        print(f"Fetching Telegram channel: {channel}")
                        payload = connector.fetch_channel(channel)
                        if payload is None:
                            continue
                        await self.process_telegram_channel(session, run, payload, resync_ids)

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

    async def process_telegram_channel(
        self,
        session,
        run: SourceRun,
        payload: dict[str, Any],
        resync_ids: set[uuid.UUID] | None = None,
    ) -> None:
        name = payload.get("name", "")
        if not name:
            return

        phones = payload.get("all_phones", [])

        record = RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.TELEGRAM,
            source_id=f"telegram:{payload['channel']}",
            raw_payload=payload,
            normalized_name=normalize_name(name),
            normalized_phone=(
                normalize_phone(
                    phones[0], default_region=self.settings.lead_sync_default_country_code
                )
                if phones
                else None
            ),
            normalized_domain=None,
            location=None,
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
        SourceType.YANDEX,
        SourceType.APPLE_MAPS,
        SourceType.TELEGRAM,
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
            institution = await self._resolve_or_log(
                session, run, record, resync_ids, record_history=False
            )
            if institution is not None:
                # Correction: a stranded WEBSITE record's RawPageSnapshot
                # rows were already persisted (with raw_source_record_id
                # set) back when the record was first created, in an
                # earlier run that failed resolution -- unlike
                # _run_web_crawler's own per-lead loop, there's no
                # in-memory snapshots_by_domain here to backfill
                # institution_id onto, since those objects belong to a
                # different, already-committed session. Backfill by
                # raw_source_record_id instead (a no-op for a non-WEBSITE
                # record), then refresh so the profile reflects both the
                # signals _resolve_or_log just persisted and this linkage,
                # not just whatever refresh_lead_profile saw when it ran
                # from inside resolve_incoming_record before either
                # existed.
                await self._link_snapshots_and_refresh(
                    session, run, institution, raw_record_id=record.id
                )

        await self._retry_stranded_snapshot_links(session, run)

    async def _retry_stranded_snapshot_links(self, session, run: SourceRun) -> None:
        """
        A record can become canonicalized (FieldProvenance written) while
        its RawPageSnapshot rows still show institution_id IS NULL -- if
        _link_snapshots_and_refresh's own linkage step itself failed (a
        transient DB error, distinct from the fallible refresh that runs
        after it in its own separate savepoint), the record is now
        excluded from the stranded-resolution query above (which only
        retries records with NO FieldProvenance at all), so nothing else
        would ever attempt this linkage again -- self-healing the same
        way _retry_stranded_records self-heals a resolution failure.

        Claims the candidate RawPageSnapshot rows via SELECT ... FOR
        UPDATE SKIP LOCKED before processing them -- without it, two
        overlapping pipeline invocations could both select the same
        stranded snapshots and each perform the linkage + refresh,
        producing duplicate LeadScoreSnapshot history entries and
        redundant scoring work. Same claim pattern as the stranded-
        resolution query above and every other "atomically grab pending
        work" query in this codebase.
        """
        candidate_rows = list(
            (
                await session.execute(
                    select(RawPageSnapshot.id, RawPageSnapshot.raw_source_record_id)
                    .where(RawPageSnapshot.institution_id.is_(None))
                    .where(RawPageSnapshot.raw_source_record_id.is_not(None))
                    .with_for_update(skip_locked=True)
                )
            ).all()
        )
        raw_record_ids = {row.raw_source_record_id for row in candidate_rows}
        if not raw_record_ids:
            return

        stranded_links = list(
            (
                await session.execute(
                    select(FieldProvenance.raw_record_id, FieldProvenance.canonical_id)
                    .where(FieldProvenance.raw_record_id.in_(raw_record_ids))
                    .distinct()
                )
            ).all()
        )
        if stranded_links:
            print(f"Retrying snapshot linkage for {len(stranded_links)} stranded record(s)...")
        for raw_record_id, institution_id in stranded_links:
            institution = await session.get(CanonicalInstitution, institution_id)
            if institution is None:
                continue
            await self._link_snapshots_and_refresh(
                session, run, institution, raw_record_id=raw_record_id
            )

        # Second case: a leadless-domain snapshot (raw_source_record_id
        # IS NULL -- no RawSourceRecord was ever created for it, see
        # _run_web_crawler's own leadless_domains block) whose domain-match
        # linkage never landed, e.g. because refresh_lead_profile failed
        # before this run's own split-savepoint fix, or a transient DB
        # error hit the linkage savepoint itself. Same disambiguation rule
        # as the live block: only link when exactly one institution
        # currently owns that domain.
        leadless_domains_stmt = (
            select(RawPageSnapshot.normalized_domain)
            .where(RawPageSnapshot.institution_id.is_(None))
            .where(RawPageSnapshot.raw_source_record_id.is_(None))
            .where(RawPageSnapshot.normalized_domain.is_not(None))
            .distinct()
        )
        stranded_domains = {row[0] for row in (await session.execute(leadless_domains_stmt)).all()}
        if not stranded_domains:
            return

        matched_institutions = (
            await session.scalars(
                select(CanonicalInstitution).where(
                    CanonicalInstitution.domain.in_(stranded_domains)
                )
            )
        ).all()
        institutions_by_domain: dict[str, list[CanonicalInstitution]] = defaultdict(list)
        for matched_institution in matched_institutions:
            institutions_by_domain[matched_institution.domain].append(matched_institution)
        for domain, institutions in institutions_by_domain.items():
            if len(institutions) != 1:
                print(
                    f"Skipping stranded leadless-domain snapshot link for {domain!r}: "
                    f"{len(institutions)} institutions share this domain."
                )
                continue
            matched_institution = institutions[0]
            snapshots = list(
                (
                    await session.scalars(
                        select(RawPageSnapshot).where(
                            RawPageSnapshot.normalized_domain == domain,
                            RawPageSnapshot.institution_id.is_(None),
                            RawPageSnapshot.raw_source_record_id.is_(None),
                        )
                    )
                ).all()
            )
            print(f"Retrying leadless-domain snapshot linkage for {domain!r}...")
            await self._link_snapshots_and_refresh(
                session, run, matched_institution, page_snapshots=snapshots
            )

    async def _link_snapshots_and_refresh(
        self,
        session,
        run: SourceRun,
        institution: CanonicalInstitution,
        page_snapshots: list[RawPageSnapshot] | None = None,
        raw_record_id: uuid.UUID | None = None,
    ) -> None:
        """
        Correction: linkage and refresh used to share ONE savepoint -- when
        refresh_lead_profile raised, the whole savepoint rolled back and
        took the institution_id linkage down with it too, even though the
        record itself was already committed/canonicalized outside this
        savepoint's scope. Since _retry_stranded_records excludes
        already-canonicalized records, that linkage would then never be
        retried, permanently hiding those snapshots from website-quality
        scoring. Persist the linkage in its own successful savepoint FIRST,
        then attempt the refresh in a SEPARATE savepoint that can fail on
        its own without undoing it.
        """
        try:
            async with session.begin_nested():
                if page_snapshots is not None:
                    for page_snapshot in page_snapshots:
                        page_snapshot.institution_id = institution.id
                if raw_record_id is not None:
                    await link_page_snapshots_to_institution(session, raw_record_id, institution.id)
        except Exception as e:
            self._record_post_link_refresh_failure(run, institution, e, stage="link")
            return

        try:
            async with session.begin_nested():
                await refresh_lead_profile(session, institution.id)
        except Exception as e:
            self._record_post_link_refresh_failure(run, institution, e, stage="refresh")

    @staticmethod
    def _record_post_link_refresh_failure(
        run: SourceRun, institution: CanonicalInstitution, error: Exception, *, stage: str
    ) -> None:
        failed = list(run.run_metadata.get("post_link_refresh_failures", []))
        failed.append({"institution_id": str(institution.id), "error": str(error), "stage": stage})
        run.run_metadata = {**run.run_metadata, "post_link_refresh_failures": failed}
        print(f"Post-resolution snapshot {stage} failed for institution {institution.id}: {error}")

    async def _resolve_or_log(
        self,
        session,
        run: SourceRun,
        record: RawSourceRecord,
        resync_ids: set[uuid.UUID] | None = None,
        *,
        record_history: bool = True,
    ) -> CanonicalInstitution | None:
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
        #
        # Returns the resolved institution (or None) -- _run_web_crawler
        # uses this to stamp RawPageSnapshot.institution_id for the pages
        # that fed this record's domain (see models/source.py::RawPageSnapshot's
        # "Correction" docstring note). Every other caller ignores the
        # return value, unaffected by this addition.
        #
        # record_history=False: passed by callers (the web-crawler path)
        # that always immediately call _link_snapshots_and_refresh right
        # after this returns -- that second, more complete refresh is the
        # one that should land in LeadScoreSnapshot history, not this
        # pre-linkage one. See refresh_lead_profile's own docstring.
        try:
            async with session.begin_nested():
                # docs/ROADMAP.md module 16: job.yaml's optional `sector`
                # key, applied inside resolve_incoming_record only as a
                # fallback when institution_type-based classification left
                # the institution unclassified.
                institution = await resolve_incoming_record(
                    session,
                    record,
                    resync_ids=resync_ids,
                    job_sector_hint=self.settings.job_config.get("sector"),
                    record_history=record_history,
                )
                if institution is not None:
                    LeadPipeline._persist_detected_signals(session, institution.id, record)
                return institution
        except Exception as e:
            unresolved = list(run.run_metadata.get("unresolved_records", []))
            unresolved.append({"raw_record_id": str(record.id), "error": str(e)})
            # run_metadata is a plain JSONB column (no MutableDict tracking),
            # so mutating the existing dict in place would never be detected
            # as a change -- reassign a new dict so the attribute-set event
            # actually marks `run` dirty.
            run.run_metadata = {**run.run_metadata, "unresolved_records": unresolved}
            print(f"Entity resolution failed for raw record {record.id}: {e}")
            return None

    @staticmethod
    def _persist_detected_signals(
        session, institution_id: uuid.UUID, record: RawSourceRecord
    ) -> None:
        """
        Materializes sources/web.py::detect_technology_signals' output
        (carried through record.raw_payload["raw"]["detected_signals"] --
        see _extract_lead's own comment there) into real Signal rows, now
        that resolution has produced a real institution_id. Explicitly
        gated on SourceType.WEBSITE rather than relying on other source
        types simply never populating a "raw" key -- that's true today but
        would silently start persisting signals from an unrelated payload
        shape if it ever stopped being true.
        """
        if record.source_type != SourceType.WEBSITE:
            return
        detected = record.raw_payload.get("raw", {}).get("detected_signals", [])
        for item in detected:
            session.add(
                Signal(
                    institution_id=institution_id,
                    signal_type=SignalType(item["signal_type"]),
                    signal_text=item["text"],
                    source_url=record.source_id,
                    # Rule-based, not AI-derived -- lower confidence than
                    # researcher.py's 0.85 for its own Signal rows.
                    confidence_score=0.6,
                )
            )

    async def _emit_resync_events(self, resync_ids: set[uuid.UUID]) -> None:
        # Fire-and-forget, same as LeadSyncEmitter itself -- a delivery
        # failure here must never fail (or be allowed to look like it
        # failed) the ingestion run that already committed successfully.
        for institution_id in resync_ids:
            try:
                await resync_institution(self.lead_sync_emitter, institution_id)
            except Exception as e:
                print(f"lead_sync resync failed for institution {institution_id}: {e}")
