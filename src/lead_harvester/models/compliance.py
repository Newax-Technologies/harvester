import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class SuppressionReason(str, enum.Enum):
    OPT_OUT = "opt_out"
    BOUNCED = "bounced"
    EMAIL_COMPLAINT = "email_complaint"
    LEGAL_REQUEST = "legal_request"
    MANUAL = "manual"


class SuppressionEntry(Base):
    """
    A contact value (phone or email, normalized the same way
    resolution/normalize.py normalizes them everywhere else) that must
    never be contacted again -- see docs/ROADMAP.md module 11's
    suppression/channel_eligibility sub-concerns. Nothing in this
    codebase checked anything like this before -- OutreachAutomator sent
    to any APPROVED draft unconditionally.
    """

    __tablename__ = "suppression_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    normalized_contact_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Null means "every channel" -- a specific value like "email" scopes
    # the suppression to just that channel (e.g. someone unsubscribed from
    # email but is still fine to call).
    channel: Mapped[str | None] = mapped_column(String(50), nullable=True)

    reason: Mapped[SuppressionReason] = mapped_column(Enum(SuppressionReason), nullable=False)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)
    suppressed_by: Mapped[str] = mapped_column(String(255), default="system", nullable=False)

    suppressed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


class DeletionSubjectType(str, enum.Enum):
    INSTITUTION = "institution"
    CONTACT_POINT = "contact_point"


class DeletionRequestStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"


class DeletionRequest(Base):
    """
    A right-to-erasure request against a CanonicalInstitution or a single
    ContactPoint. Deliberately two-step (request, then a SEPARATE fulfill
    call) rather than deleting immediately -- see
    services/compliance_service.py -- so an actual deletion is always a
    distinct, auditable action a human (or an explicit automation)
    chooses to take, not a side effect of merely recording the request.
    """

    __tablename__ = "deletion_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    subject_type: Mapped[DeletionSubjectType] = mapped_column(
        Enum(DeletionSubjectType), nullable=False
    )
    # Not a foreign key -- once fulfilled, the referenced row may no longer
    # exist at all (that's the point), so this deliberately stays a bare
    # UUID reference rather than a real FK that a delete would need to
    # null out or cascade through.
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)

    status: Mapped[DeletionRequestStatus] = mapped_column(
        Enum(DeletionRequestStatus), default=DeletionRequestStatus.PENDING, nullable=False
    )

    requestor_note: Mapped[str] = mapped_column(Text, default="", nullable=False)
    rejection_reason: Mapped[str] = mapped_column(Text, default="", nullable=False)

    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    fulfilled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
