import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.source import RawPageSnapshot, RawSourceRecord, SourceType
from lead_harvester.pipeline import LeadPipeline
from lead_harvester.sources.web import Lead, PageSnapshot


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


def _fake_lead(*, organization: str, website: str) -> Lead:
    return Lead(
        source="website",
        source_url=website,
        name="",
        organization=organization,
        title="",
        email="",
        phone="",
        website=website,
        location="",
        social_profiles=[],
        evidence="",
        raw={},
    )


async def _fake_crawl_two_domains(self, seeds):
    self.snapshots.append(
        PageSnapshot(
            url="https://alpha.example.edu/",
            final_url="https://alpha.example.edu/",
            status_code=200,
            content_type="text/html",
            html="<html>alpha</html>",
            fetch_error="",
        )
    )
    self.snapshots.append(
        PageSnapshot(
            url="https://beta.example.edu/",
            final_url="https://beta.example.edu/",
            status_code=200,
            content_type="text/html",
            html="<html>beta</html>",
            fetch_error="",
        )
    )
    return [
        _fake_lead(organization="Alpha Academy", website="https://alpha.example.edu"),
        _fake_lead(organization="Beta College", website="https://beta.example.edu"),
    ]


@pytest.mark.asyncio
async def test_snapshots_are_linked_to_their_own_domains_record_and_institution(db_session):
    # Correction regression test at the real pipeline._run_web_crawler
    # level (not just a hand-constructed model test): one crawl() call
    # fetches TWO different seed domains in the same run, each producing
    # its own Lead/RawSourceRecord/institution -- every RawPageSnapshot
    # must link to the record/institution for ITS OWN domain, never the
    # other one's, even though both share source_run_id.
    pipeline = LeadPipeline(
        Settings(job_config={"seeds": ["https://alpha.example.edu", "https://beta.example.edu"]})
    )

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_two_domains,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    alpha_record = (
        await db_session.scalars(
            select(RawSourceRecord).where(RawSourceRecord.normalized_domain == "alpha.example.edu")
        )
    ).one()
    beta_record = (
        await db_session.scalars(
            select(RawSourceRecord).where(RawSourceRecord.normalized_domain == "beta.example.edu")
        )
    ).one()
    alpha_institution = (
        await db_session.scalars(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Alpha Academy"
            )
        )
    ).one()
    beta_institution = (
        await db_session.scalars(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Beta College"
            )
        )
    ).one()

    alpha_snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "alpha.example.edu")
        )
    ).one()
    beta_snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "beta.example.edu")
        )
    ).one()

    assert alpha_snapshot.raw_source_record_id == alpha_record.id
    assert alpha_snapshot.institution_id == alpha_institution.id
    assert beta_snapshot.raw_source_record_id == beta_record.id
    assert beta_snapshot.institution_id == beta_institution.id
    # The cross-contamination this correction fixes: neither snapshot may
    # link to the other domain's record/institution.
    assert alpha_snapshot.institution_id != beta_snapshot.institution_id
    assert alpha_snapshot.raw_source_record_id != beta_snapshot.raw_source_record_id


@pytest.mark.asyncio
async def test_post_link_refresh_failure_does_not_abort_the_run(db_session):
    # Correction regression test: a failure inside the post-resolution
    # refresh_lead_profile call (e.g. a transient scoring error) used to
    # run outside _resolve_or_log's own begin_nested() boundary -- it left
    # the whole run's transaction aborted, so a single institution's
    # refresh failure lost every later lead in the same crawl. It must now
    # be isolated in its own savepoint: the run completes, beta's
    # institution is still linked and scored, and the failure is recorded
    # instead of silently swallowed or fatal.
    from lead_harvester.models.source import RunStatus, SourceRun

    real_refresh_lead_profile = None
    calls = {"count": 0}

    async def _flaky_refresh(session, institution_id):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("transient scoring failure")
        return await real_refresh_lead_profile(session, institution_id)

    from lead_harvester.services import lead_profile_service

    real_refresh_lead_profile = lead_profile_service.refresh_lead_profile

    pipeline = LeadPipeline(
        Settings(job_config={"seeds": ["https://alpha.example.edu", "https://beta.example.edu"]})
    )

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_two_domains,
        ),
        patch("lead_harvester.pipeline.refresh_lead_profile", new=_flaky_refresh),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    run = (await db_session.scalars(select(SourceRun))).one()
    assert run.status == RunStatus.COMPLETED
    assert len(run.run_metadata["post_link_refresh_failures"]) == 1

    beta_institution = (
        await db_session.scalars(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Beta College"
            )
        )
    ).one()
    beta_snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "beta.example.edu")
        )
    ).one()
    assert beta_snapshot.institution_id == beta_institution.id
