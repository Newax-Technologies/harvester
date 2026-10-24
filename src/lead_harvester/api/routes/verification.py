from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    require_permission,
)
from lead_harvester.models.verification import FlagStatus, FlagType
from lead_harvester.schemas.verification import (
    DataQualityFlagResponse,
    ResolveFlagRequest,
    RunSweepRequest,
)
from lead_harvester.services.verification_service import (
    _DEFAULT_FRESHNESS_DAYS,
    dismiss_flag,
    flag_contact_unreachable,
    list_flags,
    resolve_flag,
    run_verification_sweep,
)

router = APIRouter(prefix="/verification", tags=["Verification"])


@router.get("/flags", response_model=list[DataQualityFlagResponse])
async def list_data_quality_flags(
    status: FlagStatus | None = Query(None),
    flag_type: FlagType | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """List data-quality flags, most recently detected first."""
    flags = await list_flags(session, status=status, flag_type=flag_type, limit=limit)
    return [DataQualityFlagResponse.model_validate(f) for f in flags]


@router.post(
    "/sweep",
    response_model=dict,
    dependencies=[Depends(require_permission("verification.manage"))],
)
async def trigger_verification_sweep(
    payload: RunSweepRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Run verification checks across a batch of institutions."""
    created_count = await run_verification_sweep(
        session,
        limit=payload.limit if payload.limit is not None else 200,
        freshness_days=(
            payload.freshness_days
            if payload.freshness_days is not None
            else _DEFAULT_FRESHNESS_DAYS
        ),
    )
    await session.commit()
    return {"flags_created": created_count}


@router.post(
    "/flags/{flag_id}/resolve",
    response_model=DataQualityFlagResponse,
    dependencies=[Depends(require_permission("verification.manage"))],
)
async def resolve_data_quality_flag(
    payload: ResolveFlagRequest,
    flag_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    try:
        flag = await resolve_flag(session, flag_id, payload.note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return DataQualityFlagResponse.model_validate(flag)


@router.post(
    "/flags/{flag_id}/dismiss",
    response_model=DataQualityFlagResponse,
    dependencies=[Depends(require_permission("verification.manage"))],
)
async def dismiss_data_quality_flag(
    payload: ResolveFlagRequest,
    flag_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    try:
        flag = await dismiss_flag(session, flag_id, payload.note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return DataQualityFlagResponse.model_validate(flag)


@router.post(
    "/contacts/{contact_point_id}/unreachable",
    response_model=DataQualityFlagResponse,
    dependencies=[Depends(require_permission("verification.manage"))],
)
async def mark_contact_unreachable(
    payload: ResolveFlagRequest,
    contact_point_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    Manually record that a contact was found unreachable (a bounced
    email, a disconnected number) -- no automated verification
    integration exists yet, see docs/ROADMAP.md module 12.
    """
    flag = await flag_contact_unreachable(session, contact_point_id, payload.note)
    await session.commit()
    return DataQualityFlagResponse.model_validate(flag)
