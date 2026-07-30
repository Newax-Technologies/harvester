import datetime
import uuid
from typing import Any

from .config import Settings
from .database import get_session
from .integrations.lead_sync_emitter import LeadSyncEmitter
from .integrations.lead_sync_resync import resync_institution
from .models import RawSourceRecord, RunStatus, SourceRun, SourceType
from .resolution.normalize import normalize_domain, normalize_name, normalize_phone
from .resolution.orchestrator import resolve_incoming_record
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

    async def run(self) -> None:
        if "seeds" in self.settings.job_config:
            await self._run_web_crawler()
        else:
            await self._run_google_places()

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
