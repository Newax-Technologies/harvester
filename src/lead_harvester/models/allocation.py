import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class ReservationStatus(str, enum.Enum):
    RESERVED = "reserved"
    CONSUMED = "consumed"
    EXPIRED = "expired"
    RELEASED = "released"


class LeadReservation(Base):
    """
    Claims one institution for a batch of outreach work for a bounded
    window, so a lead selected for today's work isn't independently
    selected again by an overlapping/concurrent selection run, and isn't
    held forever if nothing ever acts on it.

    Only ever one active (RESERVED or CONSUMED) reservation may exist per
    institution at a time -- enforced both by
    services/daily_selection_service.py's SKIP LOCKED claim query (so two
    concurrent selection runs can never claim the same institution) and,
    as defense in depth, by a partial unique index on institution_id
    scoped to status='reserved' (see the f9c1a3e5b7d9 migration).
    """

    __tablename__ = "lead_reservations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )

    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus), default=ReservationStatus.RESERVED, nullable=False
    )

    # Snapshot of LeadProfile.overall_score at the moment of reservation --
    # the profile's live score can keep changing after this row is written
    # (new research, a later qualification), so this is what the ranking
    # actually selected on, kept for audit/explainability rather than
    # re-deriving it from score_history after the fact.
    score_at_reservation: Mapped[int] = mapped_column(Integer, nullable=False)

    # Groups reservations made by the same selection run -- defaults to an
    # ISO date (see daily_selection_service.py) but is a free-form label,
    # not a hard "one selection per calendar day" constraint.
    batch_label: Mapped[str] = mapped_column(String(64), nullable=False)

    # Snapshot of institution.sector_id at claim time (docs/ROADMAP.md
    # module 18) -- like score_at_reservation above, deliberately not a
    # live join to canonical_institutions.sector_id, which could change
    # after this batch was claimed. Nullable because an institution can be
    # unclassified (see models/sector.py).
    sector_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("sectors.id"), nullable=True, index=True
    )

    reserved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    institution = relationship("CanonicalInstitution")
