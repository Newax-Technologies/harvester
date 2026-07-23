from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from lead_harvester.api.dependencies import get_db_session, get_current_user, User, require_roles
from lead_harvester.services.resolution_service import ResolutionService
from lead_harvester.schemas.resolution import ResolutionCandidateSchema, ResolutionDecisionRequest
from sqlalchemy import select
from typing import List
from lead_harvester.models.resolution import ResolutionCandidate

router = APIRouter(prefix="/resolution-reviews", tags=["Resolution Reviews"])

@router.get("", response_model=List[dict])
async def list_reviews(session: AsyncSession = Depends(get_db_session)):
    stmt = select(ResolutionCandidate).where(ResolutionCandidate.decision == None)
    result = await session.execute(stmt)
    candidates = result.scalars().all()
    
    return [
        {
            "id": str(c.id),
            "targetName": "Unknown Target", # would join target institution in real
            "candidateName": c.incoming_data.get("name", "Unknown"),
            "score": c.confidence_score,
            "strategy": "matching_strategy",
            "date": c.created_at.isoformat()
        } for c in candidates
    ]

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
