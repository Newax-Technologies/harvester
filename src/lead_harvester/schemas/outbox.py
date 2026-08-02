from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.outbox import OutboxStatus
from lead_harvester.schemas.common import BaseSchema


class EventOutboxResponse(BaseSchema):
    id: UUID
    # Nullable: the "institution.deleted" tombstone EventOutbox row
    # (services/compliance_service.py::_enqueue_deletion_event) deliberately
    # leaves this unset so it survives the institution's own CASCADE -- see
    # models/outbox.py's institution_id comment. The institution's id still
    # travels inside payload for that row.
    institution_id: UUID | None
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
