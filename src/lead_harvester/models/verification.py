import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class FlagType(str, enum.Enum):
    # A CanonicalInstitution.confidence_score that no longer matches what
    # verification/confidence.py's formula would compute from its actual
    # current evidence count -- see docs/ROADMAP.md module 12.
    CONFIDENCE_DRIFT = "confidence_drift"
    # Two or more FieldProvenance rows assert meaningfully different values
    # for the same field on the same institution, without ever having gone
    # through the resolution PENDING review flow.
    CONFLICTING_FIELD = "conflicting_field"
    # No new evidence (FieldProvenance or ResearchFinding) recorded for this
    # institution within the configured freshness window.
    STALE_EVIDENCE = "stale_evidence"
    # A specific ContactPoint has been reported unreachable (bounced email,
    # disconnected number) -- currently only ever recorded manually; no
    # automated email/phone verification integration exists yet.
    UNREACHABLE_CONTACT = "unreachable_contact"


class FlagStatus(str, enum.Enum):
    OPEN = "open"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class DataQualityFlag(Base):
    """
    One detected (or manually reported) data-quality issue against a
    CanonicalInstitution -- the review_queue half of docs/ROADMAP.md
    module 12. Verification and Data Quality checks (confidence drift,
    conflicting field assertions, stale evidence, unreachable contacts)
    create these instead of silently correcting or ignoring what they
    find, so a human decides what to do about it.
    """

    __tablename__ = "data_quality_flags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False, index=True
    )

    flag_type: Mapped[FlagType] = mapped_column(Enum(FlagType), nullable=False, index=True)

    # The specific field/contact this flag is about, e.g. "canonical_name"
    # or a ContactPoint id (as a string) for UNREACHABLE_CONTACT -- null
    # for institution-wide flags (CONFIDENCE_DRIFT, STALE_EVIDENCE).
    field_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Structured context for the flag (e.g. {"stored": 10.0, "expected":
    # 30.0} for CONFIDENCE_DRIFT, or {"values": [...], "source_ids": [...]}
    # for CONFLICTING_FIELD) -- lets a reviewer see why this fired without
    # re-deriving it themselves.
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    status: Mapped[FlagStatus] = mapped_column(
        Enum(FlagStatus), default=FlagStatus.OPEN, nullable=False, index=True
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    institution = relationship("CanonicalInstitution")
