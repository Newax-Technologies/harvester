import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class CRMSyncStatus(str, enum.Enum):
    PENDING = "pending"
    SYNCED = "synced"
    FAILED = "failed"


class CRMSyncRecord(Base):
    """
    Tracks whether a CanonicalInstitution has been pushed to an external CRM,
    and under what external ID -- so re-syncs update the same CRM record
    instead of creating duplicates. One row per (institution, provider).
    """
    __tablename__ = "crm_sync_records"
    __table_args__ = (UniqueConstraint("institution_id", "provider", name="uq_crm_sync_institution_provider"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canonical_institutions.id"), nullable=False, index=True)

    # e.g. "generic_crm", "hubspot", "salesforce"
    provider: Mapped[str] = mapped_column(String(100), nullable=False)

    # The CRM's own record ID for this institution, once created there
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[CRMSyncStatus] = mapped_column(Enum(CRMSyncStatus), default=CRMSyncStatus.PENDING, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    raw_response = mapped_column(JSONB, default=dict, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    institution = relationship("CanonicalInstitution")
