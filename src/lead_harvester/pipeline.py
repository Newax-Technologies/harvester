import asyncio
import datetime
from typing import Any, Dict

from .config import Settings
from .database import get_session
from .models import RawSourceRecord, RunStatus, SourceRun, SourceType
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
        from .sources.web import WebCrawler
        import dataclasses
        
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
                status=RunStatus.STARTED
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
                        normalized_name=lead.organization or lead.name,
                        normalized_phone=lead.phone,
                        normalized_domain=lead.website,
                        location=None
                    )
                    session.add(record)
                    
                run.status = RunStatus.COMPLETED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
            except Exception as e:
                run.status = RunStatus.FAILED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
                run.run_metadata["error"] = str(e)
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
                status=RunStatus.STARTED
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
                            await self.process_place(session, run.id, place)
                            
                run.status = RunStatus.COMPLETED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
            except Exception as e:
                run.status = RunStatus.FAILED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
                run.run_metadata["error"] = str(e)
                raise
            finally:
                await session.commit()

    async def process_place(self, session, run_id, place: Dict[str, Any]) -> None:
        source_id = place.get("id")
        if not source_id:
            return
            
        from .resolution.normalize import normalize_name, normalize_phone, normalize_domain
        
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
            source_run_id=run_id,
            source_type=SourceType.GOOGLE_PLACES,
            source_id=source_id,
            raw_payload=place,
            normalized_name=normalize_name(name),
            normalized_phone=normalize_phone(phone),
            normalized_domain=normalize_domain(website),
            location=location_wkt
        )
        session.add(record)
