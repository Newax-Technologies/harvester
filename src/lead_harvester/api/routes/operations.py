import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.models.source import RunStatus, SourceType
from lead_harvester.schemas.common import AuditEventSchema
from lead_harvester.schemas.operations import (
    HealthResponse,
    OperationalMetricsResponse,
    SourceHealthResponse,
    SourceRunDetailResponse,
    SourceRunResponse,
    StrandedRecordResponse,
)
from lead_harvester.services.operations_service import (
    check_health,
    compute_operational_metrics,
    compute_source_health,
    get_sanitized_config,
    get_source_run_detail,
    list_audit_log,
    list_source_runs,
    list_stranded_records,
)

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/source-runs", response_model=list[SourceRunResponse])
async def list_source_runs_route(
    source_type: SourceType | None = Query(None),
    status: RunStatus | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    runs = await list_source_runs(session, source_type=source_type, status=status, limit=limit)
    return [SourceRunResponse.model_validate(r) for r in runs]


@router.get("/source-runs/{run_id}", response_model=SourceRunDetailResponse)
async def get_source_run_detail_route(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    detail = await get_source_run_detail(session, run_id)
    return SourceRunDetailResponse(
        run=SourceRunResponse.model_validate(detail["run"]),
        record_count=detail["record_count"],
        unresolved_records=detail["unresolved_records"],
    )


@router.get("/source-health", response_model=list[SourceHealthResponse])
async def get_source_health_route(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await compute_source_health(session)


@router.get("/stranded-records", response_model=list[StrandedRecordResponse])
async def list_stranded_records_route(
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    records = await list_stranded_records(session, limit=limit)
    return [StrandedRecordResponse.model_validate(r) for r in records]


@router.get("/audit-log", response_model=list[AuditEventSchema])
async def list_audit_log_route(
    entity_type: str | None = Query(None),
    entity_id: uuid.UUID | None = Query(None),
    actor: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    entries = await list_audit_log(
        session, entity_type=entity_type, entity_id=entity_id, actor=actor, limit=limit
    )
    return [AuditEventSchema.model_validate(e) for e in entries]


@router.get("/config", response_model=dict)
async def get_config_route(current_user: User = Depends(get_current_user)):
    """Read-only, allowlisted subset of Settings -- see operations_service._SAFE_CONFIG_FIELDS."""
    return get_sanitized_config()


@router.get("/metrics", response_model=OperationalMetricsResponse)
async def get_metrics_route(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await compute_operational_metrics(session)


@router.get("/health", response_model=HealthResponse)
async def get_health_route(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await check_health(session)
