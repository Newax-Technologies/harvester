import uuid

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.models.allocation import LeadReservation, ReservationStatus
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.schemas.allocation import (
    LeadReservationListItem,
    LeadReservationResponse,
    SelectDailyBatchRequest,
)
from lead_harvester.services.daily_selection_service import (
    mark_consumed,
    release_reservation,
    select_daily_batch,
)

router = APIRouter(prefix="/daily-selection", tags=["Daily Selection"])


@router.post("", response_model=list[LeadReservationResponse])
async def trigger_daily_selection(
    payload: SelectDailyBatchRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Claim a batch of the highest-scoring eligible leads for outreach work."""
    reservations = await select_daily_batch(
        session,
        limit=payload.limit,
        ttl_hours=payload.ttl_hours,
        min_score=payload.min_score,
        batch_label=payload.batch_label,
        sector_id=payload.sector_id,
    )
    await session.commit()
    return [LeadReservationResponse.model_validate(r) for r in reservations]


@router.get("", response_model=list[LeadReservationListItem])
async def list_daily_selection(
    status: ReservationStatus | None = Query(None),
    sector_id: uuid.UUID | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """List reservations, most recent first, optionally filtered by status/sector."""
    stmt = (
        select(LeadReservation, CanonicalInstitution.canonical_name)
        .join(CanonicalInstitution, CanonicalInstitution.id == LeadReservation.institution_id)
        .order_by(LeadReservation.reserved_at.desc())
        .limit(limit)
    )
    if status is not None:
        stmt = stmt.where(LeadReservation.status == status)
    if sector_id is not None:
        stmt = stmt.where(LeadReservation.sector_id == sector_id)

    result = await session.execute(stmt)
    return [
        LeadReservationListItem(
            id=reservation.id,
            institution_id=reservation.institution_id,
            status=reservation.status,
            score_at_reservation=reservation.score_at_reservation,
            batch_label=reservation.batch_label,
            sector_id=reservation.sector_id,
            reserved_at=reservation.reserved_at,
            expires_at=reservation.expires_at,
            consumed_at=reservation.consumed_at,
            released_at=reservation.released_at,
            canonical_name=canonical_name,
        )
        for reservation, canonical_name in result.all()
    ]


@router.post("/{reservation_id}/consume", response_model=LeadReservationResponse)
async def consume_reservation(
    reservation_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    try:
        reservation = await mark_consumed(session, reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return LeadReservationResponse.model_validate(reservation)


@router.post("/{reservation_id}/release", response_model=LeadReservationResponse)
async def release_reservation_early(
    reservation_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    try:
        reservation = await release_reservation(session, reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return LeadReservationResponse.model_validate(reservation)
