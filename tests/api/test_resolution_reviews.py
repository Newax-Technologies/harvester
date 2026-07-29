import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import find_canonical_for_raw_record
from lead_harvester.models.canonical import Branch, CanonicalInstitution, OperatingStatus
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
    # Target evidence must be populated too -- previously the frontend had to
    # hardcode the target side as "Unknown" since only incoming_data existed.
    assert body["target_data"]["name"] == "school b"
    assert body["target_data"]["phone"] == "+923001112222"


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
async def test_second_decision_with_correct_version_is_rejected(client_a, db_session):
    # A client that fetches the post-decision version (2) and resubmits a
    # new decision must still be rejected -- the candidate was already
    # reviewed, version-matching alone isn't enough.
    candidate, _record, target = await _seed_pending_pair(db_session)
    target_id = target.id

    first = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "separate", "feedback": "first decision", "expected_version": 1},
    )
    assert first.status_code == 200
    assert first.json()["version"] == 2

    second = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "merge", "feedback": "second decision", "expected_version": 2},
    )
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "already_reviewed"

    # And the second decision's side effects must not have happened. The
    # rejected request's internal rollback expires session-tracked objects,
    # so look up by the captured plain UUID rather than the (now possibly
    # expired) ORM object.
    canonical_b = await find_canonical_for_raw_record(db_session, target_id)
    assert canonical_b is None


@pytest.mark.asyncio
async def test_sibling_candidate_for_same_raw_record_is_rejected(client_a, db_session):
    # One incoming record can generate multiple candidates against different
    # targets (e.g. a phone-match candidate and a separate domain-match
    # candidate). Deciding one must prevent deciding the other -- otherwise
    # the same raw record gets canonicalized twice.
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = _record(run.id, "School A", "+923001112222", "gp-record")
    target_1 = _record(run.id, "School B", "+923001112222", "gp-target-1")
    target_2 = _record(run.id, "School C", "+923009998888", "gp-target-2")
    db_session.add_all([record, target_1, target_2])
    await db_session.flush()

    candidate_1 = ResolutionCandidate(
        raw_record_id=record.id,
        target_raw_record_id=target_1.id,
        blocking_strategy="phone",
        version=1,
    )
    candidate_2 = ResolutionCandidate(
        raw_record_id=record.id,
        target_raw_record_id=target_2.id,
        blocking_strategy="geo_name",
        version=1,
    )
    db_session.add_all([candidate_1, candidate_2])
    await db_session.flush()

    db_session.add_all(
        [
            MatchAssessment(
                candidate_id=candidate_1.id,
                name_similarity=0.5,
                distance_meters=None,
                phone_match=True,
                domain_match=False,
                total_score=65.0,
                decision=MatchDecision.PENDING,
            ),
            MatchAssessment(
                candidate_id=candidate_2.id,
                name_similarity=0.5,
                distance_meters=None,
                phone_match=False,
                domain_match=False,
                total_score=65.0,
                decision=MatchDecision.PENDING,
            ),
        ]
    )
    await db_session.commit()

    candidate_2_id = candidate_2.id

    first = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate_1.id}/decision",
        json={
            "decision": "separate",
            "feedback": "resolved via candidate 1",
            "expected_version": 1,
        },
    )
    assert first.status_code == 200

    second = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate_2_id}/decision",
        json={
            "decision": "separate",
            "feedback": "same record, different candidate",
            "expected_version": 1,
        },
    )
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "already_canonicalized"

    # The now-moot sibling must not linger in the pending queue either.
    listing = await client_a.get("/api/v1/resolution-reviews")
    ids = [r["id"] for r in listing.json()]
    assert str(candidate_2_id) not in ids


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


@pytest.mark.asyncio
async def test_invalid_decision_value_returns_422(client_a, db_session):
    candidate, _record, _target = await _seed_pending_pair(db_session)

    response = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={"decision": "obsolete_typo_value", "feedback": "oops", "expected_version": 1},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_decision_against_canonical_target_attaches_record(client_a, db_session):
    # ResolutionCandidate/the schema explicitly support target_canonical_id
    # (a candidate matched directly against an existing institution, not a
    # specific prior raw record) even though blocking.py never generates
    # this shape today -- must not 500 if it's ever encountered.
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = _record(run.id, "Canonical Target School", "+923004445555", "gp-canon-record")
    db_session.add(record)
    await db_session.flush()

    institution = CanonicalInstitution(
        canonical_name="Canonical Target School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=50.0,
    )
    db_session.add(institution)
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=record.id,
        target_canonical_id=institution.id,
        blocking_strategy="manual_review",
        version=1,
    )
    db_session.add(candidate)
    await db_session.flush()

    db_session.add(
        MatchAssessment(
            candidate_id=candidate.id,
            name_similarity=0.7,
            distance_meters=None,
            phone_match=False,
            domain_match=False,
            total_score=65.0,
            decision=MatchDecision.PENDING,
        )
    )
    await db_session.commit()

    response = await client_a.post(
        f"/api/v1/resolution-reviews/{candidate.id}/decision",
        json={
            "decision": "branch",
            "feedback": "confirmed same institution",
            "expected_version": 1,
        },
    )
    assert response.status_code == 200

    canonical_id = await find_canonical_for_raw_record(db_session, record.id)
    assert canonical_id == institution.id

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1
