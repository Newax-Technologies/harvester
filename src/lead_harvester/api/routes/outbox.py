from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
)
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.outbox import OutboxStatus
from lead_harvester.schemas.outbox import EventOutboxResponse, ProcessOutboxResponse
from lead_harvester.services.outbox_service import (
    list_outbox_entries,
    process_pending_deliveries,
    requeue_dead_letter,
)

router = APIRouter(prefix="/outbox", tags=["Event Outbox"])


@router.get("", response_model=list[EventOutboxResponse])
async def list_outbox_entries_route(
    status: OutboxStatus | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    entries = await list_outbox_entries(session, status=status, limit=limit)
    return [EventOutboxResponse.model_validate(e) for e in entries]


@router.post("/process", response_model=ProcessOutboxResponse)
async def process_pending_deliveries_route(
    limit: int = Query(50, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    lead_sync_emitter: LeadSyncEmitter = Depends(get_lead_sync_emitter),
):
    """Retries every PENDING row whose next_attempt_at has passed."""
    processed = await process_pending_deliveries(session, lead_sync_emitter, limit=limit)
    await session.commit()
    return ProcessOutboxResponse(processed=processed)


@router.post("/{outbox_id}/requeue", response_model=EventOutboxResponse)
async def requeue_dead_letter_route(
    outbox_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Moves a DEAD_LETTER row back to PENDING for another attempt."""
    try:
        entry = await requeue_dead_letter(session, outbox_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return EventOutboxResponse.model_validate(entry)
