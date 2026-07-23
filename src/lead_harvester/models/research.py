import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Float, ForeignKey, String, Text, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class FindingType(str, enum.Enum):
    FACT = "fact"           # Explicitly stated on the website (e.g. "Phone: 555-1234")
    INFERENCE = "inference" # Deduced by AI (e.g. "Appears to be a Montessori school based on curriculum page")


class ResearchJob(Base):
    """
    Tracks a long-running AI research task against a CanonicalInstitution.
    For example, crawling their website to find decision makers.
    """
    __tablename__ = "research_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canonical_institutions.id"), nullable=False, index=True)
    
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    
    # What the agent is supposed to look for (e.g. ["decision_maker_emails", "curriculum_type"])
    objectives = mapped_column(JSONB, default=list, nullable=False)
    
    # Internal logs or steps taken by the agent
    execution_logs = mapped_column(JSONB, default=list, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    institution = relationship("CanonicalInstitution")
    findings: Mapped[list["ResearchFinding"]] = relationship("ResearchFinding", back_populates="job", cascade="all, delete-orphan")


class ResearchFinding(Base):
    """
    A specific piece of data extracted by a ResearchJob.
    """
    __tablename__ = "research_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canonical_institutions.id"), nullable=False, index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("research_jobs.id"), nullable=False, index=True)
    
    finding_type: Mapped[FindingType] = mapped_column(Enum(FindingType), nullable=False)
    
    # e.g. "decision_maker_email" or "curriculum_type"
    finding_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    # The actual extracted value (can be a string, dict, list)
    finding_value = mapped_column(JSONB, nullable=False)
    
    # E.g. Exact quote from the website or URL where it was found
    evidence: Mapped[str] = mapped_column(Text, default="", nullable=False)
    
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    institution = relationship("CanonicalInstitution")
    job: Mapped["ResearchJob"] = relationship("ResearchJob", back_populates="findings")
