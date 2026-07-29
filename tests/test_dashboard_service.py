import uuid

import pytest

from lead_harvester.models.resolution import (
    MatchAssessment,
    MatchDecision,
    ResolutionCandidate,
    ReviewOutcome,
)
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.services.dashboard_service import DashboardService


def _record(run_id) -> RawSourceRecord:
    source_id = f"gp:{uuid.uuid4().hex[:8]}"
    return RawSourceRecord(
        source_run_id=run_id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=source_id,
        raw_payload={"id": source_id, "displayName": {"text": "Test School"}},
        normalized_name="test school",
        normalized_phone="+923001112222",
        normalized_domain=None,
        location=None,
    )


async def _candidate_with_decision(
    db_session, run_id, decision, *, review_outcome: ReviewOutcome | None = None
) -> ResolutionCandidate:
    record = _record(run_id)
    target = _record(run_id)
    db_session.add_all([record, target])
    await db_session.flush()

    candidate = ResolutionCandidate(
        raw_record_id=record.id,
        target_raw_record_id=target.id,
        blocking_strategy="phone",
        version=1,
        review_outcome=review_outcome,
    )
    db_session.add(candidate)
    await db_session.flush()

    db_session.add(
        MatchAssessment(
            candidate_id=candidate.id,
            name_similarity=0.5,
            distance_meters=None,
            phone_match=True,
            domain_match=False,
            total_score=60.0,
            decision=decision,
        )
    )
    await db_session.flush()
    return candidate


@pytest.mark.asyncio
async def test_pending_count_excludes_non_pending_and_already_reviewed(db_session):
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    # Should be counted: two genuinely pending, unreviewed candidates.
    await _candidate_with_decision(db_session, run.id, MatchDecision.PENDING)
    await _candidate_with_decision(db_session, run.id, MatchDecision.PENDING)

    # Should NOT be counted: automated decisions other than PENDING, and a
    # PENDING candidate a human has already reviewed.
    await _candidate_with_decision(db_session, run.id, MatchDecision.MERGE)
    await _candidate_with_decision(db_session, run.id, MatchDecision.LINK_ONLY)
    await _candidate_with_decision(db_session, run.id, MatchDecision.REJECT)
    await _candidate_with_decision(
        db_session, run.id, MatchDecision.PENDING, review_outcome=ReviewOutcome.SEPARATED
    )

    summary = await DashboardService.get_summary(db_session)

    assert summary["pending_resolution_candidates"] == 2
