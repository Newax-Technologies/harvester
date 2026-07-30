import contextlib
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.pipeline import LeadPipeline
from lead_harvester.sources.web import Lead

# _run_web_crawler/_run_google_places open their own session via
# database.get_session() (bound to settings.database_url, a real database
# CI never provisions) -- same reasoning as
# tests/integrations/test_lead_sync_resync.py. Patch get_session within the
# pipeline module to yield the isolated db_session fixture instead.


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


def _lead(website: str) -> Lead:
    return Lead(
        source="search",
        source_url="https://example.com/directory",
        name="Test Lead",
        organization="",
        title="",
        email="",
        phone="",
        website=website,
        location="",
        social_profiles=[],
        evidence="",
        raw={},
    )


def test_constructing_pipeline_without_places_api_key_does_not_raise():
    # job.yaml's documented seeds-only web-crawler mode never needs
    # GOOGLE_PLACES_API_KEY (cli.py's own run_command only requires it OR
    # seeds), but GooglePlacesConnector.__init__ raises ValueError without
    # one -- constructing it eagerly in LeadPipeline.__init__ broke that
    # mode for every caller that only configured seeds.
    pipeline = LeadPipeline(
        Settings(google_places_api_key="", job_config={"seeds": ["https://example.com"]})
    )
    assert pipeline is not None


def test_places_connector_still_raises_lazily_when_actually_used():
    pipeline = LeadPipeline(Settings(google_places_api_key=""))
    with pytest.raises(ValueError, match="GOOGLE_PLACES_API_KEY"):
        pipeline.places_connector  # noqa: B018 -- accessing the lazy property is the point


@pytest.mark.asyncio
async def test_run_web_crawler_emits_resync_events_even_when_run_fails(db_session):
    # A run that fails partway through (an exception outside
    # _resolve_or_log's own internal try/except, which already swallows
    # per-record resolution failures) still commits everything processed
    # before the failure via the inner finally -- including any
    # already-lead_synced institution enrichment. The resync emit for that
    # committed work must not be skipped just because the run as a whole
    # re-raises.
    pipeline = LeadPipeline(Settings(google_places_api_key="dummy-test-key"))
    pipeline.settings.job_config = {"seeds": ["https://example.com"]}

    fake_institution_id = uuid.uuid4()
    calls = {"n": 0}

    async def fake_resolve_or_log(session, run, record, resync_ids=None):
        calls["n"] += 1
        if calls["n"] == 1:
            if resync_ids is not None:
                resync_ids.add(fake_institution_id)
            return
        raise RuntimeError("boom")

    emit_mock = AsyncMock()
    pipeline._emit_resync_events = emit_mock

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=AsyncMock(
                return_value=[_lead("https://a.example.edu"), _lead("https://b.example.edu")]
            ),
        ),
        patch.object(LeadPipeline, "_resolve_or_log", new=staticmethod(fake_resolve_or_log)),
        pytest.raises(RuntimeError, match="boom"),
    ):
        await pipeline._run_web_crawler()

    emit_mock.assert_awaited_once_with({fake_institution_id})
