import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.source import RawPageSnapshot, SourceType
from lead_harvester.pipeline import LeadPipeline
from lead_harvester.sources.web import PageSnapshot


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


async def _fake_crawl_with_snapshots(self, seeds):
    self.snapshots.append(
        PageSnapshot(
            url="https://beaconhouse.example.edu/",
            final_url="https://beaconhouse.example.edu/",
            status_code=200,
            content_type="text/html",
            html="<html>hi</html>",
            fetch_error="",
        )
    )
    self.snapshots.append(
        PageSnapshot(
            url="https://beaconhouse.example.edu/private",
            final_url="",
            status_code=None,
            content_type="",
            html=None,
            fetch_error="robots_disallowed",
        )
    )
    return []


@pytest.mark.asyncio
async def test_run_web_crawler_persists_page_snapshots(db_session):
    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://beaconhouse.example.edu"]}))

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_with_snapshots,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    snapshots = (
        (await db_session.execute(select(RawPageSnapshot).order_by(RawPageSnapshot.url)))
        .scalars()
        .all()
    )
    assert len(snapshots) == 2
    assert snapshots[0].url == "https://beaconhouse.example.edu/"
    assert snapshots[0].html == "<html>hi</html>"
    assert snapshots[0].fetch_error == ""
    assert snapshots[1].fetch_error == "robots_disallowed"
    assert snapshots[1].html is None
    assert all(s.source_run_id is not None for s in snapshots)


@pytest.mark.asyncio
async def test_run_web_crawler_with_no_snapshots_persists_none(db_session):
    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://example.edu"]}))

    async def _empty_crawl(self, seeds):
        return []

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("lead_harvester.sources.web.WebCrawler.crawl", new=_empty_crawl),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    snapshots = (await db_session.execute(select(RawPageSnapshot))).scalars().all()
    assert snapshots == []


@pytest.mark.asyncio
async def test_page_snapshots_are_scoped_to_their_own_source_run(db_session):
    from lead_harvester.models.source import RunStatus, SourceRun

    other_run = SourceRun(source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(other_run)
    await db_session.flush()
    db_session.add(
        RawPageSnapshot(
            source_run_id=other_run.id,
            url="https://other.example.edu/",
            final_url="https://other.example.edu/",
            status_code=200,
            content_type="text/html",
            html="<html>other</html>",
            fetch_error="",
        )
    )
    await db_session.flush()

    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://beaconhouse.example.edu"]}))

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_with_snapshots,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    this_run_snapshots = (
        (
            await db_session.execute(
                select(RawPageSnapshot).where(RawPageSnapshot.source_run_id != other_run.id)
            )
        )
        .scalars()
        .all()
    )
    assert len(this_run_snapshots) == 2
