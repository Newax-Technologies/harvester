from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.source import RunStatus, SourceType
from lead_harvester.schemas.common import BaseSchema


class SourceRunResponse(BaseSchema):
    id: UUID
    source_type: SourceType
    run_metadata: dict[str, Any]
    started_at: datetime
    completed_at: datetime | None = None
    status: RunStatus


class SourceRunDetailResponse(BaseSchema):
    run: SourceRunResponse
    record_count: int
    unresolved_records: list[dict[str, Any]]


class SourceHealthResponse(BaseSchema):
    source_type: str
    last_run_at: datetime
    last_run_status: str
    last_successful_run_at: datetime | None = None
    failed_run_count_last_7d: int


class StrandedRecordResponse(BaseSchema):
    id: UUID
    source_type: SourceType
    source_id: str
    extracted_at: datetime


class OperationalMetricsResponse(BaseSchema):
    total_canonical_institutions: int
    pending_resolution_candidates: int
    pending_outreach_drafts: int
    total_target_accounts: int
    recent_pipeline_activity: list[Any]
    outbox_pending: int
    outbox_dead_letter: int
    open_data_quality_flags: int
    suppressed_contacts: int


class HealthResponse(BaseSchema):
    database_ok: bool
    stuck_run_count: int
    stuck_run_ids: list[str]
    healthy: bool
