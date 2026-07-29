from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import find_canonical_for_raw_record, merge_records
from lead_harvester.models.canonical import Branch
from lead_harvester.models.resolution import MatchAssessment, MatchDecision
from lead_harvester.resolution.orchestrator import resolve_incoming_record

from .factories import google_places_record


@pytest.mark.asyncio
async def test_no_candidates_creates_own_institution(db_session, source_run):
    record = google_places_record(
        source_run.id, name="Unique Standalone School", phone="+923009999999", lat=1.0, lng=1.0
    )
    db_session.add(record)
    await db_session.flush()

    institution = await resolve_incoming_record(db_session, record)

    assert institution is not None
    assert institution.canonical_name == "Unique Standalone School"
    canonical_id = await find_canonical_for_raw_record(db_session, record.id)
    assert canonical_id == institution.id


@pytest.mark.asyncio
async def test_merge_with_unresolved_target_creates_shared_institution(db_session, source_run):
    a = google_places_record(
        source_run.id, name="Twin School", phone="+923001112222", lat=24.86, lng=67.00
    )
    b = google_places_record(
        source_run.id, name="Twin School", phone="+923003334444", lat=24.86, lng=67.00
    )
    db_session.add(a)
    await db_session.flush()

    inst_a = await resolve_incoming_record(db_session, a)
    assert inst_a is not None

    db_session.add(b)
    await db_session.flush()
    inst_b = await resolve_incoming_record(db_session, b)

    # First record had no candidates and got its own institution; the second
    # record should MERGE into that same institution (same name, same
    # location), not create a second one.
    assert inst_b is not None
    assert inst_b.id == inst_a.id

    result = await db_session.execute(select(Branch).where(Branch.institution_id == inst_a.id))
    branches = result.scalars().all()
    assert len(branches) == 1  # same_location=True collapses to one branch


@pytest.mark.asyncio
async def test_merge_with_already_resolved_target_attaches_to_existing(db_session, source_run):
    a = google_places_record(
        source_run.id, name="Established School", phone="+923005556666", lat=31.5, lng=74.3
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    b = google_places_record(
        source_run.id, name="Established School", phone="+923007778888", lat=31.5, lng=74.3
    )
    db_session.add(b)
    await db_session.flush()

    result = await resolve_incoming_record(db_session, b)

    assert result is not None
    assert result.id == institution.id
    canonical_id = await find_canonical_for_raw_record(db_session, b.id)
    assert canonical_id == institution.id

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1
    assert b.source_id in branches[0].provider_ids.get("google_places", [])
    assert a.source_id in branches[0].provider_ids.get("google_places", [])


@pytest.mark.asyncio
async def test_pending_leaves_record_unresolved(db_session, source_run):
    a = google_places_record(source_run.id, name="Phone Sharing School A", phone="+923001010101")
    b = google_places_record(source_run.id, name="Phone Sharing School B", phone="+923001010101")
    db_session.add_all([a, b])
    await db_session.flush()

    pending_assessment = MatchAssessment(
        candidate_id=None,
        name_similarity=0.0,
        distance_meters=None,
        phone_match=True,
        domain_match=False,
        total_score=65.0,
        decision=MatchDecision.PENDING,
    )

    async def fake_score_candidate(session, candidate):
        pending_assessment.candidate_id = candidate.id
        session.add(pending_assessment)
        return pending_assessment

    with patch(
        "lead_harvester.resolution.orchestrator.score_candidate",
        new=AsyncMock(side_effect=fake_score_candidate),
    ):
        result = await resolve_incoming_record(db_session, b)

    assert result is None
    assert await find_canonical_for_raw_record(db_session, b.id) is None


@pytest.mark.asyncio
async def test_link_only_creates_own_institution(db_session, source_run):
    # Same phone number, but different names and far apart -- shared
    # contact detail, not the same physical entity (e.g. a franchise chain).
    a = google_places_record(
        source_run.id,
        name="Franchise Branch One",
        phone="+923002020202",
        lat=24.86,
        lng=67.00,
    )
    b = google_places_record(
        source_run.id,
        name="Completely Different Name",
        phone="+923002020202",
        lat=31.5,
        lng=74.3,
    )
    db_session.add(a)
    await db_session.flush()
    inst_a = await resolve_incoming_record(db_session, a)

    db_session.add(b)
    await db_session.flush()
    inst_b = await resolve_incoming_record(db_session, b)

    assert inst_b is not None
    assert inst_b.id != inst_a.id
