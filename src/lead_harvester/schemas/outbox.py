from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.outbox import OutboxStatus
from lead_harvester.schemas.common import BaseSchema


class EventOutboxResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    event_type: str
    payload: dict[str, Any]
    status: OutboxStatus
    attempt_count: int
    next_attempt_at: datetime
    last_error: str | None = None
    created_at: datetime
    delivered_at: datetime | None = None


class ProcessOutboxResponse(BaseSchema):
    processed: int
