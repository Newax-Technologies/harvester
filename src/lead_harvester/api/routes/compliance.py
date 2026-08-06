from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    require_permission,
)
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


@router.get("/suppressions", response_model=list[SuppressionEntryResponse])
async def list_suppression_entries(
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    entries = await list_suppressions(session, limit=limit)
    return [SuppressionEntryResponse.model_validate(e) for e in entries]


@router.post(
    "/suppressions",
    response_model=SuppressionEntryResponse,
    dependencies=[Depends(require_permission("compliance.suppressions.manage"))],
)
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


@router.delete(
    "/suppressions/{suppression_id}",
    status_code=204,
    dependencies=[Depends(require_permission("compliance.suppressions.manage"))],
)
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


@router.post(
    "/deletion-requests",
    response_model=DeletionRequestResponse,
    dependencies=[Depends(require_permission("compliance.deletion_requests.create"))],
)
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


@router.post(
    "/deletion-requests/{request_id}/fulfill",
    response_model=DeletionRequestResponse,
    dependencies=[Depends(require_permission("compliance.deletion_requests.fulfill"))],
)
async def fulfill_deletion_request(
    request_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
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
    dependencies=[Depends(require_permission("compliance.deletion_requests.decide"))],
)
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
