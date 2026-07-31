"""
Recomputes and persists the LeadProfile "current state" view for a
CanonicalInstitution, plus an append-only LeadScoreSnapshot for history.

See docs/ROADMAP.md module 9. Every ingestion/research/qualification path
that changes data feeding a lead's score calls refresh_lead_profile
afterward, rather than leaving profiles to go stale until some separate
batch job recomputes them (see docs/CODE_REVIEW_LESSONS.md pattern 8 --
merges/updates must reflect current state, not just first-write state).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import settings as app_settings
from lead_harvester.intelligence.icp_matching import score_icp_fit
from lead_harvester.intelligence.operational_maturity import compute_operational_maturity
from lead_harvester.intelligence.research_summary import summarize_signals
from lead_harvester.intelligence.size_estimation import estimate_size_tier
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.qualification import QualificationAssessment
from lead_harvester.models.research import ResearchFinding
from lead_harvester.models.sector import Sector
from lead_harvester.models.signal import Signal
from lead_harvester.profiles.scoring import compute_lead_score
from lead_harvester.qualification.agent import QualificationAgent
from lead_harvester.schemas.profiles import (
    LeadProfileListItem,
    LeadScoreHistoryPoint,
    PaginatedLeadProfiles,
)


async def refresh_lead_profile(session: AsyncSession, institution_id: uuid.UUID) -> LeadProfile:
    """
    Idempotent -- safe to call repeatedly as new evidence arrives. Reads the
    institution's current branches/contact points, its latest
    QualificationAssessment (if any has ever run), every ResearchFinding,
    and every Signal (models/signal.py -- populated by both
    intelligence/researcher.py's AI analysis and
    enrichment/technology_detector.py's rule-based detection) recorded for
    it. Scores it via profiles/scoring.py, computes the docs/ROADMAP.md
    module 7 business-intelligence fields (size_tier, operational_maturity,
    icp_match) via intelligence/size_estimation.py,
    intelligence/operational_maturity.py, and intelligence/icp_matching.py,
    then upserts LeadProfile and appends a LeadScoreSnapshot row.
    """
    institution = await session.get(CanonicalInstitution, institution_id)
    if institution is None:
        raise ValueError(f"No CanonicalInstitution with id {institution_id}")

    # Queried explicitly rather than via institution.branches/.contact_points
    # -- if `institution` was already resident in the session's identity map
    # (the common case: every write path calls refresh_lead_profile right
    # after creating/flushing the institution in the SAME session),
    # session.get() returns that cached instance without re-applying any
    # eager-load options, and touching an unloaded relationship attribute
    # afterward raises MissingGreenlet (implicit lazy loading isn't legal
    # outside the ORM's own greenlet context on an AsyncSession). A plain
    # select() always executes for these, sidestepping the identity-map
    # cache issue entirely.
    branches = list(
        (await session.scalars(select(Branch).where(Branch.institution_id == institution_id))).all()
    )
    contact_points = list(
        (
            await session.scalars(
                select(ContactPoint).where(ContactPoint.institution_id == institution_id)
            )
        ).all()
    )

    qualification = (
        await session.scalars(
            select(QualificationAssessment)
            .where(QualificationAssessment.institution_id == institution_id)
            .order_by(QualificationAssessment.assessed_at.desc())
            .limit(1)
        )
    ).first()

    findings = list(
        (
            await session.scalars(
                select(ResearchFinding).where(ResearchFinding.institution_id == institution_id)
            )
        ).all()
    )

    signals = list(
        (await session.scalars(select(Signal).where(Signal.institution_id == institution_id))).all()
    )

    # docs/ROADMAP.md module 17: score_icp_fit reads this institution's
    # Sector-specific icp_criteria when it has one, falling back to global
    # Settings otherwise. sector_id is a plain scalar column, not a lazy
    # relationship, so reading it directly here is safe.
    sector = await session.get(Sector, institution.sector_id) if institution.sector_id else None

    result = compute_lead_score(
        institution,
        branches,
        contact_points,
        qualification,
        findings,
        signals,
    )

    organization_summary = (
        _latest_summary(findings)
        or summarize_signals(signals)
        or _default_summary(institution, len(branches))
    )

    size_tier = estimate_size_tier(branches, contact_points)
    operational_maturity_score = compute_operational_maturity(institution, signals)
    icp_match_score = score_icp_fit(institution, len(branches), app_settings, sector=sector)

    profile = (
        await session.scalars(
            select(LeadProfile).where(LeadProfile.institution_id == institution_id)
        )
    ).first()
    if profile is None:
        profile = LeadProfile(institution_id=institution_id)
        session.add(profile)

    profile.overall_score = result.overall_score
    profile.score_breakdown = result.breakdown
    profile.has_phone = result.has_phone
    profile.has_email = result.has_email
    profile.has_named_contact = result.has_named_contact
    profile.qualification_status = qualification.status if qualification else None
    profile.size_tier = size_tier
    profile.operational_maturity_score = operational_maturity_score
    profile.icp_match_score = icp_match_score
    profile.organization_summary = organization_summary
    profile.evidence_count = result.evidence_count
    profile.computed_at = datetime.now(UTC)

    session.add(
        LeadScoreSnapshot(
            institution_id=institution_id,
            overall_score=result.overall_score,
            score_breakdown=result.breakdown,
        )
    )

    await session.flush()
    return profile


def _latest_summary(findings: list[ResearchFinding]) -> str | None:
    summary_findings = [f for f in findings if f.finding_key == "summary"]
    if not summary_findings:
        return None
    latest = max(summary_findings, key=lambda f: f.created_at)
    return latest.finding_value if isinstance(latest.finding_value, str) else None


def _default_summary(institution: CanonicalInstitution, branch_count: int) -> str:
    # Only reached when there's neither an AI-generated summary (LinkedIn
    # research) nor any detected Signal evidence (summarize_signals above)
    # -- a genuinely bare institution, not merely "not yet researched".
    kind = institution.institution_type or "institution"
    location = f" across {branch_count} branches" if branch_count > 1 else ""
    return f"{institution.canonical_name} is a {kind}{location}. No research evidence yet."


async def qualify_and_refresh(
    session: AsyncSession, institution_id: uuid.UUID, *, criteria_version: int = 1
) -> LeadProfile:
    """
    Runs QualificationAgent (previously built but never called from any
    live path) against this institution, persists the resulting
    QualificationAssessment, then refreshes the LeadProfile so its
    qualification_status/score reflect the new verdict immediately.
    """
    institution = await session.get(CanonicalInstitution, institution_id)
    if institution is None:
        raise ValueError(f"No CanonicalInstitution with id {institution_id}")

    agent = QualificationAgent(criteria_version=criteria_version)
    await agent.evaluate_institution(session, institution)
    await session.flush()

    return await refresh_lead_profile(session, institution_id)


async def qualify_all_unassessed(
    session: AsyncSession, *, criteria_version: int = 1, limit: int = 200
) -> int:
    """
    Runs QualificationAgent for every CanonicalInstitution that has never
    been assessed (no QualificationAssessment row at all), then refreshes
    its LeadProfile. Each institution is processed in its own savepoint
    (see docs/CODE_REVIEW_LESSONS.md pattern 3) so one institution's
    failure doesn't abort the whole batch or the ones already qualified in
    it. Returns the number successfully qualified.
    """
    already_assessed = select(QualificationAssessment.institution_id).distinct()
    institution_ids = (
        await session.scalars(
            select(CanonicalInstitution.id)
            .where(CanonicalInstitution.id.not_in(already_assessed))
            .limit(limit)
        )
    ).all()

    qualified_count = 0
    for institution_id in institution_ids:
        try:
            async with session.begin_nested():
                await qualify_and_refresh(
                    session, institution_id, criteria_version=criteria_version
                )
            qualified_count += 1
        except Exception as e:
            print(f"[LeadProfile] qualification failed for institution {institution_id}: {e}")

    return qualified_count


async def list_lead_profiles(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
    min_score: int | None = None,
    sector_id: uuid.UUID | None = None,
) -> PaginatedLeadProfiles:
    """Lead profiles ranked by score, richest (highest-scoring) first."""
    query = (
        select(LeadProfile, CanonicalInstitution.canonical_name)
        .join(CanonicalInstitution, CanonicalInstitution.id == LeadProfile.institution_id)
        .order_by(LeadProfile.overall_score.desc())
    )
    if min_score is not None:
        query = query.where(LeadProfile.overall_score >= min_score)
    if sector_id is not None:
        query = query.where(CanonicalInstitution.sector_id == sector_id)

    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    query = query.offset(offset).limit(limit)
    result = await session.execute(query)

    items = [
        LeadProfileListItem(
            id=profile.id,
            institution_id=profile.institution_id,
            overall_score=profile.overall_score,
            score_breakdown=profile.score_breakdown,
            has_phone=profile.has_phone,
            has_email=profile.has_email,
            has_named_contact=profile.has_named_contact,
            qualification_status=profile.qualification_status,
            organization_summary=profile.organization_summary,
            evidence_count=profile.evidence_count,
            size_tier=profile.size_tier,
            operational_maturity_score=profile.operational_maturity_score,
            icp_match_score=profile.icp_match_score,
            computed_at=profile.computed_at,
            canonical_name=canonical_name,
        )
        for profile, canonical_name in result.all()
    ]

    return PaginatedLeadProfiles(
        items=items, total=total or 0, page=(offset // limit) + 1 if limit else 1, size=limit
    )


async def get_lead_profile(session: AsyncSession, institution_id: uuid.UUID) -> LeadProfile | None:
    return await session.scalar(
        select(LeadProfile).where(LeadProfile.institution_id == institution_id)
    )


async def get_lead_score_history(
    session: AsyncSession, institution_id: uuid.UUID, limit: int = 50
) -> list[LeadScoreHistoryPoint]:
    result = await session.scalars(
        select(LeadScoreSnapshot)
        .where(LeadScoreSnapshot.institution_id == institution_id)
        .order_by(LeadScoreSnapshot.computed_at.desc())
        .limit(limit)
    )
    return [LeadScoreHistoryPoint.model_validate(snapshot) for snapshot in result.all()]
