from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from lead_harvester.api.dependencies import User, get_current_user, get_db_session, require_roles
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft
from lead_harvester.schemas.outreach import (
    DraftDecisionRequest,
    DraftEditRequest,
    OutreachDraftSchema,
)
from lead_harvester.services.draft_review_service import DraftReviewService

router = APIRouter(prefix="/drafts", tags=["Drafts"])


@router.get("", response_model=list[dict])
async def list_drafts(session: AsyncSession = Depends(get_db_session)):
    stmt = (
        select(OutreachDraft)
        .options(selectinload(OutreachDraft.brief).selectinload(AccountBrief.institution))
        .where(OutreachDraft.status == DraftStatus.GENERATED)
    )
    result = await session.execute(stmt)
    drafts = result.scalars().all()

    return [
        {
            "id": str(d.id),
            "targetName": d.target_name,
            "role": d.target_role,
            "institution": d.brief.institution.canonical_name
            if d.brief and d.brief.institution
            else "Unknown",
            "status": d.status.value,
            "generatedAt": d.created_at.isoformat(),
        }
        for d in drafts
    ]


@router.get("/{draft_id}", response_model=OutreachDraftSchema)
async def get_draft(draft_id: UUID = Path(...), session: AsyncSession = Depends(get_db_session)):
    draft = await DraftReviewService.get_draft(session, draft_id)
    return OutreachDraftSchema.model_validate(draft)


@router.patch(
    "/{draft_id}",
    response_model=OutreachDraftSchema,
    dependencies=[Depends(require_roles("reviewer", "admin"))],
)
async def edit_draft(
    req: DraftEditRequest,
    draft_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    draft = await DraftReviewService.edit_draft(session, draft_id, req, current_user.username)
    return OutreachDraftSchema.model_validate(draft)


@router.post(
    "/{draft_id}/decision",
    response_model=OutreachDraftSchema,
    dependencies=[Depends(require_roles("reviewer", "admin"))],
)
async def make_draft_decision(
    req: DraftDecisionRequest,
    draft_id: UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    draft = await DraftReviewService.make_decision(session, draft_id, req, current_user.id)
    return OutreachDraftSchema.model_validate(draft)
