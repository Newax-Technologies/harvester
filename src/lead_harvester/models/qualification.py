import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class QualificationStatus(str, enum.Enum):
    PENDING = "pending"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    NEEDS_REVIEW = "needs_review"


class QualificationAssessment(Base):
    """
    The result of an AI Subagent (or human) evaluating a CanonicalInstitution
    against a specific set of criteria to determine if it is a viable lead.
    """

    __tablename__ = "qualification_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Versioning allows us to track *which* set of criteria this assessment was based on.
    # If the user changes their ICP (Ideal Customer Profile), we increment the version
    # and re-assess the database.
    criteria_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    status: Mapped[QualificationStatus] = mapped_column(
        Enum(QualificationStatus), default=QualificationStatus.PENDING, nullable=False
    )

    # The agent's final boolean vote (True = Qualified, False = Disqualified, None = Pending)
    is_qualified: Mapped[bool | None] = mapped_column(nullable=True)

    # The detailed explanation for the vote
    rationale: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Optional: Detailed sub-scores or criteria checklists (e.g. {"has_website": True, "is_private_school": False})
    criteria_checklist = mapped_column(JSONB, default=dict, nullable=False)

    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    institution = relationship("CanonicalInstitution")
