import datetime

from .config import Settings
from .database import get_session
from .models import RawSourceRecord, RunStatus, SourceRun
from .sources.base import SourceConnector
from .sources.google_places import GooglePlacesSourceConnector
from .sources.web import WebSourceConnector


class LeadPipeline:
    """
    Runs every SourceConnector applicable to the current job config and
    persists their NormalizedRecords as RawSourceRecords. Connectors are
    independent and additive, so a job config with both "seeds"/"queries"
    and a Google Places API key runs both sources in the same pass.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    def _build_connectors(self) -> list[SourceConnector]:
        connectors: list[SourceConnector] = []

        job_config = self.settings.job_config
        if job_config.get("seeds") or job_config.get("queries"):
            connectors.append(
                WebSourceConnector(self.settings, brave_search_api_key=self.settings.brave_search_api_key or None)
            )

        if self.settings.google_places_api_key:
            connectors.append(GooglePlacesSourceConnector(api_key=self.settings.google_places_api_key))

        return connectors

    async def run(self) -> None:
        connectors = self._build_connectors()
        if not connectors:
            print("No source connectors are configured for this job.")
            return

        for connector in connectors:
            await self._run_connector(connector)

    async def _run_connector(self, connector: SourceConnector) -> None:
        async with get_session() as session:
            run = SourceRun(
                source_type=connector.source_type,
                run_metadata={},
                status=RunStatus.STARTED,
            )
            session.add(run)
            await session.flush()

            try:
                records = await connector.fetch(self.settings.job_config)

                for record in records:
                    session.add(RawSourceRecord(
                        source_run_id=run.id,
                        source_type=connector.source_type,
                        source_id=record.source_id,
                        raw_payload=record.raw_payload,
                        normalized_name=record.normalized_name,
                        normalized_phone=record.normalized_phone,
                        normalized_domain=record.normalized_domain,
                        location=record.location_wkt,
                    ))

                run.run_metadata["records_found"] = len(records)
                run.status = RunStatus.COMPLETED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
                print(f"[{connector.source_type.value}] Found {len(records)} record(s).")
            except Exception as e:
                run.status = RunStatus.FAILED
                run.completed_at = datetime.datetime.now(datetime.timezone.utc)
                run.run_metadata["error"] = str(e)
                raise
            finally:
                await session.commit()
