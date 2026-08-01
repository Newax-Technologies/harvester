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
    # instead of silently swallowed or fatal. Alpha's own snapshot linkage
    # must ALSO survive its refresh failure -- linkage and refresh run in
    # separate savepoints specifically so a refresh failure can't roll back
    # the (already independently successful) linkage alongside it.
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
    assert run.run_metadata["post_link_refresh_failures"][0]["stage"] == "refresh"

    alpha_institution = (
        await db_session.scalars(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Alpha Academy"
            )
        )
    ).one()
    alpha_snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "alpha.example.edu")
        )
    ).one()
    # Alpha's refresh failed, but its linkage ran in its own separate,
    # already-succeeded savepoint -- must NOT be rolled back by the later
    # refresh failure, or these snapshots would be permanently unreachable
    # (_retry_stranded_records skips already-canonicalized records).
    assert alpha_snapshot.institution_id == alpha_institution.id

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


@pytest.mark.asyncio
async def test_web_crawler_ingestion_writes_only_one_lead_score_snapshot(db_session):
    # Correction regression test: resolve_incoming_record's own
    # refresh_lead_profile call (inside _resolve_or_log, before snapshot
    # linkage exists) used to append a LeadScoreSnapshot history row, then
    # _link_snapshots_and_refresh's own refresh appended a SECOND one
    # immediately after -- a phantom pre-linkage entry that was never
    # really "current," doubling history growth for every ingested lead.
    # Only the final, fully-evidenced refresh should record history.
    from lead_harvester.models.profile import LeadScoreSnapshot

    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://eta.example.edu"]}))

    async def _fake_crawl_one_domain(self, seeds):
        self.snapshots.append(
            PageSnapshot(
                url="https://eta.example.edu/",
                final_url="https://eta.example.edu/",
                status_code=200,
                content_type="text/html",
                html="<html>hi</html>",
                fetch_error="",
            )
        )
        return [_fake_lead(organization="Eta Academy", website="https://eta.example.edu")]

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_one_domain,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    institution = (
        await db_session.scalars(
            select(CanonicalInstitution).where(CanonicalInstitution.canonical_name == "Eta Academy")
        )
    ).one()
    snapshots = (
        await db_session.scalars(
            select(LeadScoreSnapshot).where(LeadScoreSnapshot.institution_id == institution.id)
        )
    ).all()
    assert len(snapshots) == 1


@pytest.mark.asyncio
async def test_retry_stranded_snapshot_links_backfills_a_canonicalized_records_unlinked_snapshot(
    db_session,
):
    # Correction regression test: a record can become canonicalized
    # (FieldProvenance written) while its RawPageSnapshot rows still show
    # institution_id IS NULL -- e.g. if the linkage step inside
    # _link_snapshots_and_refresh itself failed on a transient error in an
    # earlier run. Since the record is now canonicalized,
    # _retry_stranded_records' own resolution-retry query would never
    # revisit it. _retry_stranded_snapshot_links must find and fix exactly
    # this case.
    from lead_harvester.models.provenance import FieldProvenance
    from lead_harvester.models.source import RunStatus, SourceRun

    run = SourceRun(source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.COMPLETED)
    db_session.add(run)
    await db_session.flush()

    institution = CanonicalInstitution(canonical_name="Stranded Link School")
    db_session.add(institution)
    await db_session.flush()

    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id="web:stranded",
        raw_payload={},
        normalized_domain="stranded.example.edu",
    )
    db_session.add(record)
    await db_session.flush()

    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=record.id,
            field_name="canonical_name",
            asserted_value="Stranded Link School",
        )
    )
    snapshot = RawPageSnapshot(
        source_run_id=run.id,
        url="https://stranded.example.edu/",
        final_url="https://stranded.example.edu/",
        status_code=200,
        content_type="text/html",
        html="<html>hi</html>",
        fetch_error="",
        normalized_domain="stranded.example.edu",
        raw_source_record_id=record.id,
        institution_id=None,
    )
    db_session.add(snapshot)
    await db_session.flush()

    pipeline = LeadPipeline(Settings(job_config={}))
    await pipeline._retry_stranded_snapshot_links(db_session, run)

    await db_session.refresh(snapshot)
    assert snapshot.institution_id == institution.id


@pytest.mark.asyncio
async def test_snapshots_for_a_leadless_domain_link_to_an_already_known_institution(db_session):
    # Correction: a domain the crawl actually fetched pages for, but that
    # produced no lead (extraction found no identity/contact data, or
    # every fetch for it failed) never gets a RawSourceRecord -- without
    # the domain-match fallback, its snapshots would stay permanently
    # unlinked even for an institution already known from another source
    # (e.g. Google Places), misreporting a real crawl attempt as
    # NOT_CRAWLED forever.
    existing_institution = CanonicalInstitution(
        canonical_name="Gamma School", domain="gamma.example.edu"
    )
    db_session.add(existing_institution)
    await db_session.flush()
    institution_id = existing_institution.id

    async def _fake_crawl_no_lead(self, seeds):
        self.snapshots.append(
            PageSnapshot(
                url="https://gamma.example.edu/",
                final_url="https://gamma.example.edu/",
                status_code=200,
                content_type="text/html",
                html="<html>hi</html>",
                fetch_error="",
            )
        )
        return []  # no lead extracted for this domain

    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://gamma.example.edu"]}))

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_no_lead,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "gamma.example.edu")
        )
    ).one()
    assert snapshot.raw_source_record_id is None
    assert snapshot.institution_id == institution_id


@pytest.mark.asyncio
async def test_snapshots_for_a_leadless_unknown_domain_stay_unlinked(db_session):
    # No CanonicalInstitution has this domain at all -- correctly stays
    # unlinked (institution_id null means "not yet linked", never guessed
    # into scope, per RawPageSnapshot's own docstring).
    async def _fake_crawl_no_lead_unknown(self, seeds):
        self.snapshots.append(
            PageSnapshot(
                url="https://delta.example.edu/",
                final_url="https://delta.example.edu/",
                status_code=200,
                content_type="text/html",
                html="<html>hi</html>",
                fetch_error="",
            )
        )
        return []

    pipeline = LeadPipeline(Settings(job_config={"seeds": ["https://delta.example.edu"]}))

    with (
        patch(
            "lead_harvester.pipeline.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "lead_harvester.sources.web.WebCrawler.crawl",
            new=_fake_crawl_no_lead_unknown,
        ),
        patch.object(LeadPipeline, "_emit_resync_events", new=AsyncMock()),
    ):
        await pipeline._run_web_crawler()

    snapshot = (
        await db_session.scalars(
            select(RawPageSnapshot).where(RawPageSnapshot.normalized_domain == "delta.example.edu")
        )
    ).one()
    assert snapshot.raw_source_record_id is None
    assert snapshot.institution_id is None
