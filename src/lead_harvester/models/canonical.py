import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class OperatingStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    CLOSED_TEMPORARILY = "closed_temporarily"
    CLOSED_PERMANENTLY = "closed_permanently"
    UNKNOWN = "unknown"


class CanonicalInstitution(Base):
    """
    The pristine, resolved entity representing a single educational institution.
    Constructed by merging one or more RawSourceRecords.
    """

    __tablename__ = "canonical_institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Core Fields
    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    institution_type: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[OperatingStatus] = mapped_column(
        Enum(OperatingStatus), default=OperatingStatus.OPERATIONAL, nullable=False
    )

    # Business vertical (education, healthcare, ...) -- see models/sector.py
    # and docs/ROADMAP.md module 16. Nullable: an institution whose
    # institution_type doesn't match any configured Sector's
    # institution_types stays unclassified rather than being forced into a
    # wrong bucket.
    sector_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("sectors.id"), nullable=True, index=True
    )

    # Trust score based on the number and quality of sources that confirm this entity
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Set the first time integrations/lead_sync_emitter.py's
    # emit_institution_upserted is attempted for this institution (currently
    # only from api/routes/manual_leads.py::create_manual_lead). Gates
    # whether a LATER resolution-driven update (automated pipeline
    # attach, or a reviewer's merge/branch decision) bothers re-emitting a
    # sync event -- without this, an institution that was already mirrored
    # into core-newax silently goes stale on every subsequent enrichment,
    # since only the original manual-lead creation ever synced it. Marking
    # this optimistically when delivery is *attempted* (not confirmed
    # delivered) matches the emitter's own fire-and-forget contract --
    # requiring confirmed delivery would need a callback from the
    # background task, which is disproportionate machinery for what this
    # flag is for (deciding whether a re-sync attempt is worth making at
    # all).
    lead_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    branches: Mapped[list["Branch"]] = relationship(
        "Branch", back_populates="institution", cascade="all, delete-orphan"
    )
    contact_points: Mapped[list["ContactPoint"]] = relationship(
        "ContactPoint", back_populates="institution", cascade="all, delete-orphan"
    )


class Branch(Base):
    """
    A specific physical location of a CanonicalInstitution.
    """

    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False
    )

    branch_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    address: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Structured fields alongside the free-text `address`, required so a synced
    # CoreAddress downstream always has a real city/country (CoreAddress.city is
    # NOT NULL and has no way to be derived from a flattened address string).
    city: Mapped[str] = mapped_column(String(128), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)

    location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=True)

    # Store provider-specific IDs mapping to this exact physical location (e.g. Google Place IDs)
    provider_ids: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    institution: Mapped["CanonicalInstitution"] = relationship(
        "CanonicalInstitution", back_populates="branches"
    )


class ContactPoint(Base):
    """
    A unified contact method (e.g., a phone number or email) associated with an institution.
    If multiple branches share a phone number, it is stored here once to link them.
    """

    __tablename__ = "contact_points"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False
    )

    contact_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g. "phone", "email", "whatsapp", "telegram"
    contact_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    person_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_publicly_listed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Which PersonCandidate (models/person.py) this contact's person_name
    # resolves to, if any -- set by services/person_candidate_service.py
    # whenever a contact with a non-blank person_name is written. Null for
    # contacts with no person_name (a bare office phone/email) or for rows
    # written before this column existed.
    person_candidate_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("person_candidates.id"), nullable=True, index=True
    )

    institution: Mapped["CanonicalInstitution"] = relationship(
        "CanonicalInstitution", back_populates="contact_points"
    )
