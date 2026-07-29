import pytest

from lead_harvester.models.resolution import MatchDecision, ResolutionCandidate
from lead_harvester.resolution.scoring import score_candidate

from .factories import google_places_record


@pytest.mark.asyncio
async def test_pending_is_reachable_for_moderate_ambiguous_match(db_session, source_run):
    # "greenwood international school" vs "greenwood international college"
    # has a real pg_trgm similarity of ~0.615 (in (0.5, 0.8], so +20, not the
    # MERGE-qualifying >0.8 bucket) and these are placed at the identical
    # point (distance=0, i.e. <50m, so +40) -- total_score lands at exactly
    # 60 with no phone/domain match. Before the `> 60` -> `>= 60` fix, this
    # combination could only ever reach REJECT, and PENDING (the review
    # queue's only feeder) was unreachable for any input.
    a = google_places_record(
        source_run.id,
        name="Greenwood International School",
        phone="+923001110000",
        website="https://greenwood-a.example.edu",
        lat=24.86,
        lng=67.00,
    )
    b = google_places_record(
        source_run.id,
        name="Greenwood International College",
        phone="+923002220000",
        website="https://greenwood-b.example.edu",
        lat=24.86,
        lng=67.00,
    )
    db_session.add_all([a, b])
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=a.id,
        target_raw_record_id=b.id,
        blocking_strategy="geo_name",
        version=1,
    )
    db_session.add(candidate)
    await db_session.flush()

    assessment = await score_candidate(db_session, candidate)

    assert assessment.total_score == 60.0
    assert assessment.decision == MatchDecision.PENDING


@pytest.mark.asyncio
async def test_exact_domain_and_strong_name_match_is_pending_not_link_only(db_session, source_run):
    # A web-crawled record has no coordinates at all (location is always
    # None), so it can never reach the MERGE branch (needs distance<100m).
    # Before this fix, an exact domain match plus a near-identical name would
    # still fall through to LINK_ONLY (the phone/domain branch), which the
    # orchestrator treats as "confidently distinct" and immediately
    # canonicalizes as a second, duplicate institution.
    a = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone=None,
        website="https://riverside.example.edu",
        lat=None,
        lng=None,
    )
    b = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone=None,
        website="https://riverside.example.edu",
        lat=None,
        lng=None,
    )
    db_session.add_all([a, b])
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=a.id,
        target_raw_record_id=b.id,
        blocking_strategy="domain",
        version=1,
    )
    db_session.add(candidate)
    await db_session.flush()

    assessment = await score_candidate(db_session, candidate)

    assert assessment.domain_match is True
    assert assessment.decision == MatchDecision.PENDING


@pytest.mark.asyncio
async def test_domain_match_alone_with_weak_name_stays_link_only(db_session, source_run):
    # Domain match without a strong name match is still LINK_ONLY -- e.g. a
    # shared website domain that doesn't otherwise look like the same
    # institution shouldn't jump to PENDING just because of the domain.
    a = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone=None,
        website="https://shared-portal.example.edu",
        lat=None,
        lng=None,
    )
    b = google_places_record(
        source_run.id,
        name="Totally Unrelated Name",
        phone=None,
        website="https://shared-portal.example.edu",
        lat=None,
        lng=None,
    )
    db_session.add_all([a, b])
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=a.id,
        target_raw_record_id=b.id,
        blocking_strategy="domain",
        version=1,
    )
    db_session.add(candidate)
    await db_session.flush()

    assessment = await score_candidate(db_session, candidate)

    assert assessment.domain_match is True
    assert assessment.decision == MatchDecision.LINK_ONLY
