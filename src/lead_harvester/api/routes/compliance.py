from __future__ import annotations

import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
)
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import ContactPoint
from lead_harvester.models.compliance import DeletionRequest, DeletionRequestStatus, DeletionSubjectType
from lead_harvester.schemas.compliance import (
    AddSuppressionRequest,
    CreateDeletionRequestRequest,
    DeletionRequestResponse,
    RejectDeletionRequest,
    SuppressionEntryResponse,
)
from lead_harvester.services.compliance_service import (
    add_suppression,
    fulfill_deletion,
    list_deletion_requests,
    list_suppressions,
    reject_deletion,
    remove_suppression,
    request_deletion,
)

router = APIRouter(prefix="/compliance", tags=["Compliance"])


async def _deliver_deletion_sync_event(
    lead_sync_emitter: LeadSyncEmitter,
    subject_type: DeletionSubjectType,
    institution_id: uuid.UUID,
    contact_point_id: uuid.UUID | None,
) -> None:
    # Mirrors api/routes/manual_leads.py::_deliver_lead_sync_event's
    # background-task scheduling: runs after the response is sent, and only
    # once fulfill_deletion_request's own session.commit() below has
    # actually succeeded -- notifying core-newax about a deletion that got
    # rolled back would be worse than not notifying at all. No DB session
    # needed here (unlike manual_leads.py's version) since the emitter's
    # deletion methods are a plain signed HTTP call, not a durable outbox
    # row -- see LeadSyncEmitter.emit_contact_point_deleted's docstring for
    # why that durability gap is a known, tracked limitation rather than
    # something bolted on here. See docs/ROADMAP.md's tracked follow-up #4
    # (deletion/reconciliation).
    try:
        if subject_type == DeletionSubjectType.CONTACT_POINT:
            await lead_sync_emitter.emit_contact_point_deleted(institution_id, contact_point_id)
        else:
            await lead_sync_emitter.emit_institution_deleted(institution_id)
    except Exception as e:
        print(
            f"lead_sync deletion notification raised unexpectedly "
            f"({subject_type.value} institution={institution_id}): {e}"
        )


@router.get("/suppressions", response_model=list[SuppressionEntryResponse])
async def list_suppression_entries(
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    entries = await list_suppressions(session, limit=limit)
    return [SuppressionEntryResponse.model_validate(e) for e in entries]


@router.post("/suppressions", response_model=SuppressionEntryResponse)
async def create_suppression_entry(
    payload: AddSuppressionRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    entry = await add_suppression(
        session,
        payload.contact_value,
        payload.reason,
        channel=payload.channel,
        note=payload.note,
        suppressed_by=payload.suppressed_by,
        default_region=payload.default_region,
    )
    await session.commit()
    return SuppressionEntryResponse.model_validate(entry)


@router.delete("/suppressions/{suppression_id}", status_code=204)
async def delete_suppression_entry(
    suppression_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    await remove_suppression(session, suppression_id)
    await session.commit()


@router.get("/deletion-requests", response_model=list[DeletionRequestResponse])
async def list_deletion_requests_route(
    status: DeletionRequestStatus | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    requests = await list_deletion_requests(session, status=status, limit=limit)
    return [DeletionRequestResponse.model_validate(r) for r in requests]


@router.post("/deletion-requests", response_model=DeletionRequestResponse)
async def create_deletion_request(
    payload: CreateDeletionRequestRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Records an erasure request. Does NOT delete anything -- see /fulfill."""
    request = await request_deletion(
        session, payload.subject_type, payload.subject_id, payload.note
    )
    await session.commit()
    return DeletionRequestResponse.model_validate(request)


@router.post("/deletion-requests/{request_id}/fulfill", response_model=DeletionRequestResponse)
async def fulfill_deletion_request(
    background_tasks: BackgroundTasks,
    request_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    lead_sync_emitter: LeadSyncEmitter = Depends(get_lead_sync_emitter),
):
    """Actually deletes the requested subject. Irreversible."""
    # Captured before fulfill_deletion actually removes the row -- a
    # ContactPoint's institution_id is otherwise unrecoverable once it's
    # gone, and it's what emit_contact_point_deleted needs to report which
    # institution's contact list changed.
    pending_request = await session.get(DeletionRequest, request_id)
    sync_institution_id: uuid.UUID | None = None
    sync_contact_point_id: uuid.UUID | None = None
    if pending_request is not None and pending_request.status == DeletionRequestStatus.PENDING:
        if pending_request.subject_type == DeletionSubjectType.CONTACT_POINT:
            contact = await session.get(ContactPoint, pending_request.subject_id)
            if contact is not None:
                sync_institution_id = contact.institution_id
                sync_contact_point_id = contact.id
        else:
            sync_institution_id = pending_request.subject_id

    try:
        request = await fulfill_deletion(session, request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()

    if sync_institution_id is not None:
        background_tasks.add_task(
            _deliver_deletion_sync_event,
            lead_sync_emitter,
            request.subject_type,
            sync_institution_id,
            sync_contact_point_id,
        )

    return DeletionRequestResponse.model_validate(request)


@router.post("/deletion-requests/{request_id}/reject", response_model=DeletionRequestResponse)
async def reject_deletion_request(
    payload: RejectDeletionRequest,
    request_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    try:
        request = await reject_deletion(session, request_id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return DeletionRequestResponse.model_validate(request)
