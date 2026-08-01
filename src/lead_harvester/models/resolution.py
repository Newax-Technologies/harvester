import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class MatchDecision(str, enum.Enum):
    PENDING = "pending"
    MERGE = "merge"  # Strong match, combine into same canonical profile
    LINK_ONLY = "link_only"  # Shared phone/property, but distinct entities (e.g. franchises)
    REJECT = "reject"  # Distinct entities, no relationship


class ReviewOutcome(str, enum.Enum):
    """
    What a human reviewer actually decided for a ResolutionCandidate, as
    distinct from MatchDecision (the automated scorer's verdict). Null means
    "not yet reviewed" -- this is what the resolution-reviews queue filters
    on, rather than inferring "already decided" from AuditLog presence.
    """

    MERGED = "merged"  # Same branch -- enrich the existing Branch in place
    BRANCHED = "branched"  # Same institution, a distinct physical location
    SEPARATED = "separated"  # Confidently distinct entities


class ResolutionCandidate(Base):
    """
    Pairs a raw source record with a target CanonicalInstitution (or another raw record)
    to be evaluated by the scoring engine.
    """

    __tablename__ = "resolution_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # The new incoming record we are trying to resolve
    raw_record_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("raw_source_records.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # The existing canonical institution we think it might match
    target_canonical_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=True, index=True
    )

    # Or, matching against another raw record if no canonical exists yet
    target_raw_record_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("raw_source_records.id", ondelete="CASCADE"), nullable=True, index=True
    )

    # The mechanism that found this candidate (e.g. "blocking_geographic", "blocking_domain")
    blocking_strategy: Mapped[str] = mapped_column(String(50), nullable=False)

    # Optimistic locking version
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Null until a human reviewer acts on this candidate via the
    # resolution-reviews decision endpoint.
    review_outcome: Mapped[ReviewOutcome | None] = mapped_column(Enum(ReviewOutcome), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # Assessment details
    assessments: Mapped[list["MatchAssessment"]] = relationship(
        "MatchAssessment", back_populates="candidate", cascade="all, delete-orphan"
    )


class MatchAssessment(Base):
    """
    The result of scoring a ResolutionCandidate against various vectors (name, distance, phone, etc).
    """

    __tablename__ = "match_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resolution_candidates.id", ondelete="CASCADE"), nullable=False
    )

    # Granular scoring
    name_similarity: Mapped[float] = mapped_column(Float, default=0.0)  # pg_trgm similarity
    distance_meters: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # PostGIS ST_Distance
    phone_match: Mapped[bool] = mapped_column(Boolean, default=False)
    domain_match: Mapped[bool] = mapped_column(Boolean, default=False)

    # Overall score (0-100)
    total_score: Mapped[float] = mapped_column(Float, default=0.0)

    decision: Mapped[MatchDecision] = mapped_column(
        Enum(MatchDecision), default=MatchDecision.PENDING, nullable=False
    )

    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    candidate: Mapped["ResolutionCandidate"] = relationship(
        "ResolutionCandidate", back_populates="assessments"
    )
