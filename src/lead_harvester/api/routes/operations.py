import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import get_db_session
from lead_harvester.api.permissions import Permission, require_permission
from lead_harvester.models.source import RunStatus, SourceType
from lead_harvester.schemas.common import AuditEventSchema
from lead_harvester.schemas.operations import (
    HealthResponse,
    OperationalMetricsResponse,
    PageSnapshotResponse,
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
    list_page_snapshots,
    list_source_runs,
    list_stranded_records,
)

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get(
    "/source-runs",
    response_model=list[SourceRunResponse],
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def list_source_runs_route(
    source_type: SourceType | None = Query(None),
    status: RunStatus | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    runs = await list_source_runs(session, source_type=source_type, status=status, limit=limit)
    return [SourceRunResponse.model_validate(r) for r in runs]


@router.get(
    "/source-runs/{run_id}",
    response_model=SourceRunDetailResponse,
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def get_source_run_detail_route(
    run_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
):
    detail = await get_source_run_detail(session, run_id)
    return SourceRunDetailResponse(
        run=SourceRunResponse.model_validate(detail["run"]),
        record_count=detail["record_count"],
        unresolved_records=detail["unresolved_records"],
    )


@router.get(
    "/source-health",
    response_model=list[SourceHealthResponse],
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def get_source_health_route(
    session: AsyncSession = Depends(get_db_session),
):
    return await compute_source_health(session)


@router.get(
    "/stranded-records",
    response_model=list[StrandedRecordResponse],
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def list_stranded_records_route(
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    records = await list_stranded_records(session, limit=limit)
    return [StrandedRecordResponse.model_validate(r) for r in records]


@router.get(
    "/page-snapshots",
    response_model=list[PageSnapshotResponse],
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def list_page_snapshots_route(
    source_run_id: uuid.UUID | None = Query(None),
    only_errors: bool = Query(False),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    """
    docs/ROADMAP.md module 3's raw_snapshot data -- every page a WEBSITE
    crawl attempted, success or failure. Excludes the stored HTML body
    (can be large); query the database directly for that.
    """
    snapshots = await list_page_snapshots(
        session, source_run_id=source_run_id, only_errors=only_errors, limit=limit
    )
    return [PageSnapshotResponse.model_validate(s) for s in snapshots]


@router.get(
    "/audit-log",
    response_model=list[AuditEventSchema],
    dependencies=[Depends(require_permission(Permission.AUDIT_READ))],
)
async def list_audit_log_route(
    entity_type: str | None = Query(None),
    entity_id: uuid.UUID | None = Query(None),
    actor: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    entries = await list_audit_log(
        session, entity_type=entity_type, entity_id=entity_id, actor=actor, limit=limit
    )
    return [AuditEventSchema.model_validate(e) for e in entries]


@router.get(
    "/config",
    response_model=dict,
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def get_config_route():
    """Read-only, allowlisted subset of Settings -- see operations_service._SAFE_CONFIG_FIELDS."""
    return get_sanitized_config()


@router.get(
    "/metrics",
    response_model=OperationalMetricsResponse,
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def get_metrics_route(
    session: AsyncSession = Depends(get_db_session),
):
    return await compute_operational_metrics(session)


@router.get(
    "/health",
    response_model=HealthResponse,
    dependencies=[Depends(require_permission(Permission.OPERATIONS_READ))],
)
async def get_health_route(
    session: AsyncSession = Depends(get_db_session),
):
    return await check_health(session)
