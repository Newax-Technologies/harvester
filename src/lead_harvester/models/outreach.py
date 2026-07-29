import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class BriefStatus(str, enum.Enum):
    DRAFTING = "drafting"
    READY_FOR_REVIEW = "ready_for_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class DraftStatus(str, enum.Enum):
    PENDING_GENERATION = "pending_generation"
    GENERATED = "generated"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"
    SENT = "sent"


class AccountBrief(Base):
    """
    A comprehensive synthesis of all data, research, and hypotheses for a specific CanonicalInstitution.
    This acts as the 'dossier' that sales reps review before approving outreach.
    """

    __tablename__ = "account_briefs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False, index=True
    )

    status: Mapped[BriefStatus] = mapped_column(
        Enum(BriefStatus), default=BriefStatus.DRAFTING, nullable=False
    )

    # Generated hypotheses on why this institution needs our product
    value_hypotheses: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)

    # A ranked list of stakeholders (e.g. [{"role": "Principal", "name": "John Doe", "score": 95}])
    stakeholder_ranking = mapped_column(JSONB, default=list, nullable=False)

    # AI summary of the institution's background
    executive_summary: Mapped[str] = mapped_column(Text, default="", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    institution = relationship("CanonicalInstitution")
    drafts: Mapped[list["OutreachDraft"]] = relationship(
        "OutreachDraft", back_populates="brief", cascade="all, delete-orphan"
    )


class OutreachDraft(Base):
    """
    A specific message drafted by the AI for a specific stakeholder.
    Must pass through a Readiness Gate (human approval) before being marked SENT.
    """

    __tablename__ = "outreach_drafts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brief_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("account_briefs.id"), nullable=False, index=True
    )

    status: Mapped[DraftStatus] = mapped_column(
        Enum(DraftStatus), default=DraftStatus.PENDING_GENERATION, nullable=False
    )

    # The stakeholder this is targeted at
    target_name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_role: Mapped[str] = mapped_column(String(255), nullable=False)
    target_contact_value: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # e.g. email address

    subject_line: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Feedback from the human reviewer for the AI to incorporate in the next revision
    human_feedback: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Optimistic locking version
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    brief: Mapped["AccountBrief"] = relationship("AccountBrief", back_populates="drafts")
    outcomes: Mapped[list["OutreachOutcome"]] = relationship(
        "OutreachOutcome", back_populates="draft", cascade="all, delete-orphan"
    )


class OutreachOutcome(Base):
    """
    Tracks what happened after an OutreachDraft was sent.
    Provides the crucial feedback loop to improve future drafts.
    """

    __tablename__ = "outreach_outcomes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    draft_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("outreach_drafts.id"), nullable=False, index=True
    )

    opened: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    clicked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    replied: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # If they replied, was it positive?
    positive_reply: Mapped[bool | None] = mapped_column(nullable=True)
    reply_text: Mapped[str] = mapped_column(Text, default="", nullable=False)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    draft: Mapped["OutreachDraft"] = relationship("OutreachDraft", back_populates="outcomes")
