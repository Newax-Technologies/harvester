from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.verification import FlagStatus, FlagType
from lead_harvester.schemas.common import BaseSchema


class DataQualityFlagResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    flag_type: FlagType
    field_name: str | None = None
    details: dict[str, Any]
    status: FlagStatus
    detected_at: datetime
    resolved_at: datetime | None = None
    resolution_note: str


class ResolveFlagRequest(BaseSchema):
    note: str = ""


class RunSweepRequest(BaseSchema):
    limit: int | None = None
    freshness_days: int | None = None
