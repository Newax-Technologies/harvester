import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base
from lead_harvester.models.qualification import QualificationStatus


class SizeTier(str, enum.Enum):
    """
    See docs/ROADMAP.md module 7's size_estimation sub-concern --
    intelligence/size_estimation.py computes this from branch/contact
    counts (the only size proxy this schema has; no headcount data
    exists), not a guessed student/staff count.
    """

    UNKNOWN = "unknown"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class WebsiteQualityTier(str, enum.Enum):
    """
    See docs/ROADMAP.md module 20's website quality engine --
    intelligence/website_quality.py computes this from a weighted checklist
    over the institution's crawled RawPageSnapshot rows. NONE is forced
    whenever the institution has no website at all (no scoring needed).
    """

    NONE = "none"
    POOR = "poor"
    ADEQUATE = "adequate"
    GOOD = "good"
    EXCEPTIONAL = "exceptional"


class LeadProfile(Base):
    """
    The current, denormalized view of a CanonicalInstitution as a lead --
    one row per institution. Recomputed by
    services/lead_profile_service.py::refresh_lead_profile whenever the
    underlying data it summarizes changes (a new branch/contact attaches,
    LinkedIn research findings land, a qualification assessment runs), so
    downstream consumers (ranking, review UIs, exports) never need to
    re-derive score/contactability/qualification from scratch by joining
    across Branch/ContactPoint/ResearchFinding/QualificationAssessment
    themselves.
    """

    __tablename__ = "lead_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False, unique=True, index=True
    )

    overall_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Human-readable {category: points} breakdown backing overall_score --
    # evidence-backed per docs/ROADMAP.md module 8's requirement, not an
    # opaque single number.
    score_breakdown: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    has_phone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_named_contact: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Mirrors the latest QualificationAssessment for this institution, if
    # any has ever been run -- null means never assessed, distinct from any
    # real QualificationStatus value.
    qualification_status: Mapped[QualificationStatus | None] = mapped_column(
        Enum(QualificationStatus, name="qualificationstatus"), nullable=True
    )

    organization_summary: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Count of ResearchFinding rows this profile's score/summary drew on --
    # lets a consumer distinguish "confidently scored from real research"
    # from "scored on branch/contact data alone, nothing researched yet".
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # docs/ROADMAP.md module 7 (Business Intelligence) additions --
    # computed by intelligence/size_estimation.py,
    # intelligence/operational_maturity.py, and intelligence/icp_matching.py
    # respectively, refreshed alongside the score in the same
    # refresh_lead_profile call.
    size_tier: Mapped[SizeTier] = mapped_column(
        Enum(SizeTier, name="sizetier"), default=SizeTier.UNKNOWN, nullable=False
    )
    operational_maturity_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    icp_match_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # docs/ROADMAP.md module 20 additions -- computed by
    # intelligence/website_quality.py and intelligence/service_gap.py
    # respectively, refreshed alongside everything else above.
    website_quality_tier: Mapped[WebsiteQualityTier] = mapped_column(
        Enum(WebsiteQualityTier, name="websitequalitytier"),
        default=WebsiteQualityTier.NONE,
        nullable=False,
    )
    service_gap_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    # Correction: distinct from computed_at, which the lead-profile API
    # exposes as this profile's freshness/trust signal -- computed_at must
    # only ever mean "the score fields were last SUCCESSFULLY recomputed
    # as of this time". services/lead_profile_service.py::
    # recompute_all_lead_profiles bumps this column (not computed_at) when
    # a profile's refresh fails, purely so its own remediation cursor
    # (ordered by whichever of the two is more recent) advances past a
    # persistently-failing profile instead of re-selecting it forever --
    # without corrupting computed_at into claiming a failed, still-
    # untrusted profile was just freshly computed.
    last_recompute_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    institution = relationship("CanonicalInstitution")


class LeadScoreSnapshot(Base):
    """
    An append-only record of one score computation for an institution --
    lets score_history be queried/plotted over time, unlike LeadProfile
    (which only ever holds the latest computation). Written every time
    refresh_lead_profile runs, alongside upserting LeadProfile.
    """

    __tablename__ = "lead_score_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False, index=True
    )

    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    score_breakdown: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    institution = relationship("CanonicalInstitution")
