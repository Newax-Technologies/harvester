from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import User, get_current_user, get_db_session, require_roles
from lead_harvester.schemas.resolution import (
    ResolutionCandidateSchema,
    ResolutionDecisionRequest,
    ResolutionSummarySchema,
)
from lead_harvester.services.resolution_service import ResolutionService

router = APIRouter(prefix="/resolution-reviews", tags=["Resolution Reviews"])


@router.get("", response_model=list[ResolutionSummarySchema])
async def list_reviews(session: AsyncSession = Depends(get_db_session)):
    return await ResolutionService.list_pending(session)


@router.get("/{review_id}", response_model=ResolutionCandidateSchema)
async def get_review(review_id: UUID = Path(...), session: AsyncSession = Depends(get_db_session)):
    return await ResolutionService.get_review_detail(session, review_id)


@router.post(
    "/{review_id}/decision",
    response_model=ResolutionCandidateSchema,
    dependencies=[Depends(require_roles("reviewer", "admin"))],
)
async def make_review_decision(
    req: ResolutionDecisionRequest,
    review_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await ResolutionService.make_decision(session, review_id, req, current_user.id)
