import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import find_canonical_for_raw_record
from lead_harvester.models.canonical import Branch
from lead_harvester.models.resolution import (
    MatchAssessment,
    MatchDecision,
    ResolutionCandidate,
    ReviewOutcome,
)
from lead_harvester.models.source import RunStatus, SourceRun, SourceType


async def _seed_pending_pair(db_session, *, name_a="School A", name_b="School B"):
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = _record(run.id, name_a, "+923001112222", "gp-record")
    target = _record(run.id, name_b, "+923001112222", "gp-target")
    db_session.add_all([record, target])
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=record.id,
        target_raw_record_id=target.id,
        blocking_strategy="phone",
        version=1,
    )
    db_session.add(candidate)
    await db_session.flush()

    assessment = MatchAssessment(
        candidate_id=candidate.id,
        name_similarity=0.5,
        distance_meters=None,
        phone_match=True,
        domain_match=False,
        total_score=65.0,
        decision=MatchDecision.PENDING,
    )
    db_session.add(assessment)
    await db_session.commit()

    return candidate, record, target


def _record(run_id, name, phone, source_id):
    from lead_harvester.models.source import RawSourceRecord
    from lead_harvester.resolution.normalize import normalize_name, normalize_phone

    return RawSourceRecord(
        source_run_id=run_id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=source_id,
        raw_payload={
            "id": source_id,
            "displayName": {"text": name},
            "formattedAddress": "1 Test Street",
            "websiteUri": f"https://{source_id}.example.edu",
            "primaryType": "school",
            "nationalPhoneNumber": phone,
        },
        normalized_name=normalize_name(name),
        normalized_phone=normalize_phone(phone),
        normalized_domain=f"{source_id}.example.edu",
        location=None,
    )


@pytest.mark.asyncio
async def test_list_reviews_shape(client_a, db_session):
    candidate, _record, _target = await _seed_pending_pair(db_session)

    response = await client_a.get("/api/v1/resolution-reviews")
    assert response.status_code == 200
    body = response.json()

    entry = next(r for r in body if r["id"] == str(candidate.id))
    assert entry["candidateName"] == "school a"
    assert entry["targetName"] == "school b"
    assert entry["strategy"] == "phone"
    assert entry["score"] == 65.0


@pytest.mark.asyncio
async def test_get_review_shape(client_a, db_session):
    candidate, _record, _target = await _seed_pending_pair(db_session)

    response = await client_a.get(f"/api/v1/resolution-reviews/{candidate.id}")
    assert response.status_code == 200
    body = response.json()

    assert body["version"] == 1
    assert body["confidence_score"] == 65.0
    assert body["incoming_data"]["name"] == "school a"
    assert body["incoming_data"]["phone"] == "+923001112222"


@pytest.mark.asyncio
async def test_merge_decision_attaches_records_to_one_institution(client_a, db_session):
    candidate, record, target = await _seed_pending_pair(db_session)

    response = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "merge", "feedback": "same branch", "expected_version": 1},
    )
    assert response.status_code == 200

    canonical_a = await find_canonical_for_raw_record(db_session, record.id)
    canonical_b = await find_canonical_for_raw_record(db_session, target.id)
    assert canonical_a is not None
    assert canonical_a == canonical_b

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == canonical_a)))
        .scalars()
        .all()
    )
    assert len(branches) == 1

    await db_session.refresh(candidate)
    assert candidate.review_outcome == ReviewOutcome.MERGED
    assert candidate.version == 2


@pytest.mark.asyncio
async def test_branch_decision_creates_two_branches_same_institution(client_a, db_session):
    candidate, record, target = await _seed_pending_pair(db_session)

    response = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "branch", "feedback": "different campus", "expected_version": 1},
    )
    assert response.status_code == 200

    canonical_a = await find_canonical_for_raw_record(db_session, record.id)
    canonical_b = await find_canonical_for_raw_record(db_session, target.id)
    assert canonical_a == canonical_b

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == canonical_a)))
        .scalars()
        .all()
    )
    assert len(branches) == 2

    await db_session.refresh(candidate)
    assert candidate.review_outcome == ReviewOutcome.BRANCHED


@pytest.mark.asyncio
async def test_separate_decision_creates_independent_institution(client_a, db_session):
    candidate, record, target = await _seed_pending_pair(db_session)

    response = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "separate", "feedback": "unrelated", "expected_version": 1},
    )
    assert response.status_code == 200

    canonical_a = await find_canonical_for_raw_record(db_session, record.id)
    canonical_b = await find_canonical_for_raw_record(db_session, target.id)
    assert canonical_a is not None
    assert canonical_b is None  # target untouched by this decision

    await db_session.refresh(candidate)
    assert candidate.review_outcome == ReviewOutcome.SEPARATED


@pytest.mark.asyncio
async def test_second_reviewer_receives_409_on_stale_version(client_a, client_b, db_session):
    candidate, _record, _target = await _seed_pending_pair(db_session)

    approved = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "separate", "feedback": "first reviewer", "expected_version": 1},
    )
    assert approved.status_code == 200

    stale = await client_b.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "merge", "feedback": "stale reviewer", "expected_version": 1},
    )
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "stale_resource"


@pytest.mark.asyncio
async def test_resolved_candidate_disappears_from_pending_list(client_a, db_session):
    candidate, _record, _target = await _seed_pending_pair(db_session)

    await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "separate", "feedback": "done", "expected_version": 1},
    )

    response = await client_a.get("/api/v1/resolution-reviews")
    ids = [r["id"] for r in response.json()]
    assert str(candidate.id) not in ids
