import datetime
from typing import Any

from .config import Settings
from .database import get_session
from .models import RawSourceRecord, RunStatus, SourceRun, SourceType
from .resolution.normalize import normalize_domain, normalize_name, normalize_phone
from .resolution.orchestrator import resolve_incoming_record
from .sources.geographic_tiling import build_queries_for_tile, generate_tiles
from .sources.google_places import GooglePlacesConnector


class LeadPipeline:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.places_connector = GooglePlacesConnector(api_key=settings.google_places_api_key)

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
                        normalized_phone=normalize_phone(lead.phone) if lead.phone else None,
                        normalized_domain=normalize_domain(lead.website) if lead.website else None,
                        location=None,
                    )
                    session.add(record)
                    await session.flush()
                    await self._resolve_or_log(session, run, record)

                run.status = RunStatus.COMPLETED
                run.completed_at = datetime.datetime.now(datetime.UTC)
            except Exception as e:
                run.status = RunStatus.FAILED
                run.completed_at = datetime.datetime.now(datetime.UTC)
                run.run_metadata = {**run.run_metadata, "error": str(e)}
                raise
            finally:
                await session.commit()
        print(f"WebCrawler finished. Found {len(leads)} leads.")

    async def _run_google_places(self) -> None:
        tiles = generate_tiles(self.settings.job_config)
        categories = self.settings.job_config.get("categories", ["FORMAL_EDUCATION"])

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
                            await self.process_place(session, run, place)

                run.status = RunStatus.COMPLETED
                run.completed_at = datetime.datetime.now(datetime.UTC)
            except Exception as e:
                run.status = RunStatus.FAILED
                run.completed_at = datetime.datetime.now(datetime.UTC)
                run.run_metadata = {**run.run_metadata, "error": str(e)}
                raise
            finally:
                await session.commit()

    async def process_place(self, session, run: SourceRun, place: dict[str, Any]) -> None:
        source_id = place.get("id")
        if not source_id:
            return

        name = place.get("displayName", {}).get("text", "")
        phone = place.get("nationalPhoneNumber", "")
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
            normalized_phone=normalize_phone(phone),
            normalized_domain=normalize_domain(website),
            location=location_wkt,
        )
        session.add(record)
        await session.flush()
        await self._resolve_or_log(session, run, record)

    @staticmethod
    async def _resolve_or_log(session, run: SourceRun, record: RawSourceRecord) -> None:
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
                await resolve_incoming_record(session, record)
        except Exception as e:
            unresolved = list(run.run_metadata.get("unresolved_records", []))
            unresolved.append({"raw_record_id": str(record.id), "error": str(e)})
            # run_metadata is a plain JSONB column (no MutableDict tracking),
            # so mutating the existing dict in place would never be detected
            # as a change -- reassign a new dict so the attribute-set event
            # actually marks `run` dirty.
            run.run_metadata = {**run.run_metadata, "unresolved_records": unresolved}
            print(f"Entity resolution failed for raw record {record.id}: {e}")
