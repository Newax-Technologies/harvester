from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from lead_harvester.api.dependencies import get_db_session, get_current_user, User, require_roles
from lead_harvester.services.resolution_service import ResolutionService
from lead_harvester.schemas.resolution import ResolutionCandidateSchema, ResolutionDecisionRequest
from sqlalchemy import select
from typing import List
from lead_harvester.models.resolution import ResolutionCandidate, MatchAssessment, MatchDecision
from lead_harvester.models.source import RawSourceRecord
from lead_harvester.models.canonical import CanonicalInstitution

router = APIRouter(prefix="/resolution-reviews", tags=["Resolution Reviews"])


def _record_name(record: RawSourceRecord | None) -> str:
    if record is None:
        return "Unknown"
    if record.normalized_name:
        return record.normalized_name
    return record.raw_payload.get("displayName", {}).get("text", "Unknown")


@router.get("", response_model=List[dict])
async def list_reviews(session: AsyncSession = Depends(get_db_session)):
    # A "review" is a candidate whose most recent assessment is still PENDING.
    stmt = (
        select(ResolutionCandidate, MatchAssessment)
        .join(MatchAssessment, MatchAssessment.candidate_id == ResolutionCandidate.id)
        .where(MatchAssessment.decision == MatchDecision.PENDING)
        .order_by(MatchAssessment.assessed_at.desc())
    )
    rows = (await session.execute(stmt)).all()

    # Rows are ordered newest-assessment-first, so the first row seen per candidate is the latest.
    seen_candidate_ids = set()
    pairs = []
    for candidate, assessment in rows:
        if candidate.id in seen_candidate_ids:
            continue
        seen_candidate_ids.add(candidate.id)
        pairs.append((candidate, assessment))

    raw_record_ids = {c.raw_record_id for c, _ in pairs}
    raw_record_ids |= {c.target_raw_record_id for c, _ in pairs if c.target_raw_record_id}
    canonical_ids = {c.target_canonical_id for c, _ in pairs if c.target_canonical_id}

    raw_records = {}
    if raw_record_ids:
        result = await session.execute(select(RawSourceRecord).where(RawSourceRecord.id.in_(raw_record_ids)))
        raw_records = {r.id: r for r in result.scalars()}

    canonical_institutions = {}
    if canonical_ids:
        result = await session.execute(select(CanonicalInstitution).where(CanonicalInstitution.id.in_(canonical_ids)))
        canonical_institutions = {i.id: i for i in result.scalars()}

    reviews = []
    for candidate, assessment in pairs:
        if candidate.target_canonical_id:
            institution = canonical_institutions.get(candidate.target_canonical_id)
            target_name = institution.canonical_name if institution else "Unknown"
        else:
            target_name = _record_name(raw_records.get(candidate.target_raw_record_id))

        reviews.append({
            "id": str(candidate.id),
            "targetName": target_name,
            "candidateName": _record_name(raw_records.get(candidate.raw_record_id)),
            "score": assessment.total_score,
            "strategy": candidate.blocking_strategy,
            "date": candidate.created_at.isoformat()
        })

    return reviews

@router.get("/{review_id}", response_model=ResolutionCandidateSchema)
async def get_review(
    review_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session)
):
    candidate = await ResolutionService.get_candidate(session, review_id)
    return ResolutionCandidateSchema.model_validate(candidate)

@router.post("/{review_id}/decision", response_model=ResolutionCandidateSchema, dependencies=[Depends(require_roles("reviewer", "admin"))])
async def make_review_decision(
    req: ResolutionDecisionRequest,
    review_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    candidate = await ResolutionService.make_decision(session, review_id, req, current_user.id)
    return ResolutionCandidateSchema.model_validate(candidate)
