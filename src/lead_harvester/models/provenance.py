import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class FieldProvenance(Base):
    """
    Tracks exactly which RawSourceRecord asserted a specific value for a CanonicalInstitution.
    This provides a traceable audit log so we never guess where a phone number or domain came from.
    """

    __tablename__ = "field_provenance"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    canonical_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("raw_source_records.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # The name of the field on the canonical entity (e.g. "domain", "primary_phone", "canonical_name")
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # The value asserted by this source (stored as JSON for flexibility, e.g. strings, lists, dicts)
    asserted_value = mapped_column(JSONB, nullable=False)

    # Optional trust score applied to this specific assertion (e.g., Google Places website is high trust)
    assertion_trust: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    canonical_institution = relationship("CanonicalInstitution")
    raw_source_record = relationship("RawSourceRecord")
