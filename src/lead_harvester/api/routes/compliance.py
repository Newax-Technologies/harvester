from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import get_db_session
from lead_harvester.api.permissions import Permission, require_permission
from lead_harvester.models.compliance import DeletionRequestStatus
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


@router.get(
    "/suppressions",
    response_model=list[SuppressionEntryResponse],
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_READ))],
)
async def list_suppression_entries(
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    entries = await list_suppressions(session, limit=limit)
    return [SuppressionEntryResponse.model_validate(e) for e in entries]


@router.post(
    "/suppressions",
    response_model=SuppressionEntryResponse,
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_MANAGE))],
)
async def create_suppression_entry(
    payload: AddSuppressionRequest,
    session: AsyncSession = Depends(get_db_session),
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


@router.delete(
    "/suppressions/{suppression_id}",
    status_code=204,
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_MANAGE))],
)
async def delete_suppression_entry(
    suppression_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
):
    await remove_suppression(session, suppression_id)
    await session.commit()


@router.get(
    "/deletion-requests",
    response_model=list[DeletionRequestResponse],
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_READ))],
)
async def list_deletion_requests_route(
    status: DeletionRequestStatus | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    requests = await list_deletion_requests(session, status=status, limit=limit)
    return [DeletionRequestResponse.model_validate(r) for r in requests]


@router.post(
    "/deletion-requests",
    response_model=DeletionRequestResponse,
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_MANAGE))],
)
async def create_deletion_request(
    payload: CreateDeletionRequestRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Records an erasure request. Does NOT delete anything -- see /fulfill."""
    request = await request_deletion(
        session, payload.subject_type, payload.subject_id, payload.note
    )
    await session.commit()
    return DeletionRequestResponse.model_validate(request)


@router.post(
    "/deletion-requests/{request_id}/fulfill",
    response_model=DeletionRequestResponse,
    dependencies=[Depends(require_permission(Permission.DELETIONS_FULFIL))],
)
async def fulfill_deletion_request(
    request_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
):
    """Actually deletes the requested subject. Irreversible."""
    try:
        request = await fulfill_deletion(session, request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return DeletionRequestResponse.model_validate(request)


@router.post(
    "/deletion-requests/{request_id}/reject",
    response_model=DeletionRequestResponse,
    dependencies=[Depends(require_permission(Permission.COMPLIANCE_MANAGE))],
)
async def reject_deletion_request(
    payload: RejectDeletionRequest,
    request_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        request = await reject_deletion(session, request_id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return DeletionRequestResponse.model_validate(request)
