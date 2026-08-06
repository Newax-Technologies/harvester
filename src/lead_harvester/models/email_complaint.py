import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class EmailComplaintType(str, enum.Enum):
    RECIPIENT_SPAM = "recipient_spam"
    FEEDBACK_LOOP = "feedback_loop"
    DMARC_FORENSIC = "dmarc_forensic"
    AUTHENTICATION_FAILURE = "authentication_failure"
    OTHER = "other"


class EmailComplaintProjection(Base):
    """Harvester's idempotent projection of a complaint owned by another source system."""

    __tablename__ = "email_complaint_projections"
    __table_args__ = (
        UniqueConstraint("source_system", "source_complaint_id"),
        Index(
            "ix_email_complaint_projections_contact_occurred",
            "normalized_contact_value",
            "occurred_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_system: Mapped[str] = mapped_column(String(64), nullable=False)
    source_complaint_id: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_contact_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    complaint_type: Mapped[EmailComplaintType] = mapped_column(
        Enum(EmailComplaintType), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_message_id: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    evidence_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    suppression_entry_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppression_entries.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
