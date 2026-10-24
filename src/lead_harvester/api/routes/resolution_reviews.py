from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
    require_permission,
)
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.schemas.resolution import (
    ResolutionCandidateSchema,
    ResolutionDecisionRequest,
    ResolutionSummarySchema,
)
from lead_harvester.services.resolution_service import ResolutionService

router = APIRouter(prefix="/resolution-reviews", tags=["Resolution Reviews"])


@router.get("", response_model=list[ResolutionSummarySchema])
async def list_reviews(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await ResolutionService.list_pending(session)


@router.get("/{review_id}", response_model=ResolutionCandidateSchema)
async def get_review(
    review_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await ResolutionService.get_review_detail(session, review_id)


@router.post(
    "/{review_id}/decision",
    response_model=ResolutionCandidateSchema,
    dependencies=[Depends(require_permission("resolution_reviews.decide"))],
)
async def make_review_decision(
    req: ResolutionDecisionRequest,
    background_tasks: BackgroundTasks,
    review_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    lead_sync_emitter: LeadSyncEmitter = Depends(get_lead_sync_emitter),
):
    return await ResolutionService.make_decision(
        session,
        review_id,
        req,
        current_user.id,
        background_tasks=background_tasks,
        lead_sync_emitter=lead_sync_emitter,
    )
