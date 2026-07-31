import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class ConsentBasis(str, enum.Enum):
    """The lawful basis for holding/using a given contact point, per the README's compliance guardrails."""
    PUBLIC_DIRECTORY = "public_directory"   # Public business listing (Google Places, website, etc.)
    LICENSED_EXPORT = "licensed_export"     # Authorized social/data export
    OWNED_DATA = "owned_data"               # First-party / manually entered by the operator
    UNKNOWN = "unknown"                     # Not yet established -- do not treat as cleared for outreach


class IdentifierType(str, enum.Enum):
    EMAIL = "email"
    PHONE = "phone"
    DOMAIN = "domain"


class SuppressionReason(str, enum.Enum):
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    COMPLAINT = "complaint"
    LEGAL_REQUEST = "legal_request"
    MANUAL = "manual"


class SuppressionEntry(Base):
    """
    A hard block list. Any identifier here must never be used as an outreach
    target, regardless of what CanonicalInstitution/ContactPoint it later
    shows up on (e.g. after a re-scrape).
    """
    __tablename__ = "suppression_entries"
    __table_args__ = (UniqueConstraint("identifier_type", "identifier_value", name="uq_suppression_identifier"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    identifier_type: Mapped[IdentifierType] = mapped_column(Enum(IdentifierType), nullable=False)
    identifier_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    reason: Mapped[SuppressionReason] = mapped_column(Enum(SuppressionReason), nullable=False)
    note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DeletionRequestStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class DeletionRequest(Base):
    """
    A right-to-be-forgotten / opt-out request against one identifier.
    Processing it deletes matching ContactPoints and OutreachDrafts, purges
    matching raw ledger records (phone/domain only -- see deletion.py for why
    email can't be purged from unstructured raw payloads), and adds a
    SuppressionEntry so the identifier can't silently re-enter the pipeline.
    """
    __tablename__ = "deletion_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    identifier_type: Mapped[IdentifierType] = mapped_column(Enum(IdentifierType), nullable=False)
    identifier_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    status: Mapped[DeletionRequestStatus] = mapped_column(Enum(DeletionRequestStatus), default=DeletionRequestStatus.PENDING, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)

    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
