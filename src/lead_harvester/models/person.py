"""
A discovered *possible* person at an institution -- see docs/ROADMAP.md
module 1 ("Entity Registry"): "A person_candidate is a discovered
possible contact, not a verified person, until resolved."

Deliberately NOT the same thing as core-newax's CorePerson: this is
harvester's own pre-CRM identity-clustering layer over
ContactPoint.person_name, which was previously a bare string with no
resolution state at all -- the same real person named on two different
ContactPoint rows for one institution had no way to be recognized as one
person (see docs/ROADMAP.md's "cross-record person deduplication" tracked
follow-up, which named this exact entity as the missing piece).
"""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class PersonCandidateStatus(str, enum.Enum):
    ACTIVE = "active"
    MERGED = "merged"


class PersonCandidate(Base):
    __tablename__ = "person_candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # The name as most recently seen -- kept in its original casing/spacing
    # for display; matching itself always goes through
    # resolution/normalize.py's normalize_name (the same normalizer
    # verification/checks.py's conflicting-name check already uses), never
    # this raw value.
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    status: Mapped[PersonCandidateStatus] = mapped_column(
        Enum(PersonCandidateStatus), default=PersonCandidateStatus.ACTIVE, nullable=False
    )

    # How many ContactPoint rows currently link to this candidate --
    # denormalized so "how much evidence backs this identity" is a plain
    # column read, not a COUNT query, on every list/detail view.
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    institution = relationship("CanonicalInstitution")
