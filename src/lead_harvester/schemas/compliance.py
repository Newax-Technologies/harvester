from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.compliance import (
    DeletionRequestStatus,
    DeletionSubjectType,
    SuppressionReason,
)
from lead_harvester.schemas.common import BaseSchema


class SuppressionEntryResponse(BaseSchema):
    id: UUID
    normalized_contact_value: str
    channel: str | None = None
    reason: SuppressionReason
    note: str
    suppressed_by: str
    suppressed_at: datetime


class AddSuppressionRequest(BaseSchema):
    contact_value: str
    reason: SuppressionReason
    channel: str | None = None
    note: str = ""
    suppressed_by: str = "system"
    default_region: str | None = None


class DeletionRequestResponse(BaseSchema):
    id: UUID
    subject_type: DeletionSubjectType
    subject_id: UUID
    status: DeletionRequestStatus
    requestor_note: str
    rejection_reason: str
    requested_at: datetime
    fulfilled_at: datetime | None = None
    manifest: dict[str, Any] = {}


class CreateDeletionRequestRequest(BaseSchema):
    subject_type: DeletionSubjectType
    subject_id: UUID
    note: str = ""


class RejectDeletionRequest(BaseSchema):
    reason: str
