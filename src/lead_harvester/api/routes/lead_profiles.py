import uuid

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.schemas.profiles import (
    LeadProfileResponse,
    LeadScoreHistoryPoint,
    PaginatedLeadProfiles,
)
from lead_harvester.services.lead_profile_service import (
    get_lead_profile,
    get_lead_score_history,
    list_lead_profiles,
)

router = APIRouter(prefix="/lead-profiles", tags=["Lead Profiles"])


@router.get("", response_model=PaginatedLeadProfiles)
async def list_profiles(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_score: int | None = Query(None, ge=0, le=100),
    sector_id: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """List lead profiles, highest-scoring first."""
    return await list_lead_profiles(session, limit, offset, min_score, sector_id)


@router.get("/{institution_id}", response_model=LeadProfileResponse)
async def get_profile(
    institution_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Get the current lead profile for a specific institution."""
    profile = await get_lead_profile(session, institution_id)
    if profile is None:
        raise ResourceNotFoundError("Lead profile not found")
    return LeadProfileResponse.model_validate(profile)


@router.get("/{institution_id}/score-history", response_model=list[LeadScoreHistoryPoint])
async def get_score_history(
    institution_id: str = Path(...),
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Historical score snapshots for a specific institution, most recent first."""
    return await get_lead_score_history(session, institution_id, limit)
