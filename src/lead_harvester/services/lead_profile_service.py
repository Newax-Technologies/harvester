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

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import settings as app_settings
from lead_harvester.intelligence.icp_matching import score_icp_fit
from lead_harvester.intelligence.operational_maturity import compute_operational_maturity
from lead_harvester.intelligence.research_summary import summarize_signals
from lead_harvester.intelligence.service_gap import compute_service_gap_score
from lead_harvester.intelligence.size_estimation import estimate_size_tier
from lead_harvester.intelligence.website_quality import compute_website_quality_tier
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.qualification import QualificationAssessment
from lead_harvester.models.research import ResearchFinding
from lead_harvester.models.sector import Sector
from lead_harvester.models.signal import Signal
from lead_harvester.models.source import RawPageSnapshot
from lead_harvester.profiles.scoring import compute_lead_score
from lead_harvester.qualification.agent import QualificationAgent
from lead_harvester.schemas.profiles import (
    LeadProfileListItem,
    LeadScoreHistoryPoint,
    PaginatedLeadProfiles,
)


async def refresh_lead_profile(
    session: AsyncSession, institution_id: uuid.UUID, *, record_history: bool = True
) -> LeadProfile:
    """
    record_history=False skips the LeadScoreSnapshot append (the
    LeadProfile upsert itself always happens) -- for a caller that already
    knows a second, more complete refresh is coming immediately after this
    one within the same per-record processing (e.g. pipeline.py's
    _resolve_or_log before its own snapshot-linkage step runs), writing
    history here would record an intermediate score that was never really
    "current" -- visible nowhere, superseded microseconds later -- as a
    phantom entry, doubling history growth for no benefit. Defaults True
    so every other caller keeps recording every call, unaffected.

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

    # docs/ROADMAP.md module 20: the crawled pages that belong to this
    # institution's own website specifically -- see _get_website_snapshots'
    # own docstring for why this is institution_id, not source_run_id.
    website_snapshots = await _get_website_snapshots(session, institution_id)
    website_quality_tier = compute_website_quality_tier(institution.website, website_snapshots)
    service_gap_score = compute_service_gap_score(website_quality_tier, signals, size_tier)

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
    profile.website_quality_tier = website_quality_tier
    profile.service_gap_score = service_gap_score
    profile.organization_summary = organization_summary
    profile.evidence_count = result.evidence_count
    profile.computed_at = datetime.now(UTC)
    # Clear any stale failed-attempt marker: recompute_all_lead_profiles'
    # COALESCE(last_recompute_attempted_at, computed_at) cursor would
    # otherwise keep pointing at an old failure timestamp forever, since a
    # non-null last_recompute_attempted_at always wins the COALESCE even
    # after this fresh, newer computed_at succeeds it.
    profile.last_recompute_attempted_at = None

    if record_history:
        session.add(
            LeadScoreSnapshot(
                institution_id=institution_id,
                overall_score=result.overall_score,
                score_breakdown=result.breakdown,
            )
        )

    await session.flush()
    return profile


async def _get_website_snapshots(
    session: AsyncSession, institution_id: uuid.UUID
) -> list[RawPageSnapshot]:
    """
    docs/ROADMAP.md module 20: the RawPageSnapshot rows that actually
    belong to this institution's own crawled website.

    Correction: a single WEBSITE SourceRun crawls every seed domain passed
    to WebCrawler.crawl() in one call, not just one -- filtering by
    "snapshots from a run that touched this institution" (source_run_id
    membership, this function's original approach) could silently pull in
    another institution's pages that happened to be fetched in the same
    run. RawPageSnapshot.institution_id (models/source.py, stamped by
    pipeline.py::_run_web_crawler once a page's domain has both produced a
    RawSourceRecord and been resolved) is the exact-grain link that fixes
    this -- filter on it directly, never on source_run_id alone. A row
    with institution_id still NULL (predates this column, or its domain's
    record never resolved) is correctly excluded, not guessed into scope.
    """
    return list(
        (
            await session.scalars(
                select(RawPageSnapshot).where(RawPageSnapshot.institution_id == institution_id)
            )
        ).all()
    )


async def link_page_snapshots_to_institution(
    session: AsyncSession, raw_record_id: uuid.UUID, institution_id: uuid.UUID
) -> None:
    """
    Correction: backfills RawPageSnapshot.institution_id for every page
    fetched under raw_record_id -- see models/source.py::RawPageSnapshot's
    "Correction" docstring and _get_website_snapshots above, which this
    directly feeds.

    pipeline.py::_run_web_crawler already does this inline for a record
    resolved within the SAME crawl run that fetched its pages. This is the
    shared path for every OTHER route that can canonicalize a WEBSITE
    record afterward, where the snapshots were already persisted (with
    raw_source_record_id set, institution_id still null) in an earlier,
    already-committed run:
      - pipeline.py::_retry_stranded_records, retrying a record that
        failed resolution in an earlier run;
      - services/resolution_service.py::_apply_decision, a human review
        decision canonicalizing a record that was left PENDING.
    Without this, either path leaves the record's pages permanently
    unlinked -- _get_website_snapshots excludes them forever, not just
    until some later recomputation, since nothing else ever revisits this
    link. A no-op for a non-WEBSITE record, since it has no RawPageSnapshot
    rows to begin with.
    """
    await session.execute(
        update(RawPageSnapshot)
        .where(RawPageSnapshot.raw_source_record_id == raw_record_id)
        .values(institution_id=institution_id)
    )


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


async def recompute_all_lead_profiles(session: AsyncSession, *, limit: int = 500) -> int:
    """
    Re-runs refresh_lead_profile for every institution that already has a
    LeadProfile row -- the direct remediation for the RawPageSnapshot
    institution-linkage correction (see migration e2a4c6f8b0d2 and
    _get_website_snapshots' docstring): every website_quality_tier/
    service_gap_score computed before that fix landed is treated as
    untrusted, since it may have been scored from another institution's
    crawled pages that happened to share a SourceRun. Calling this
    recomputes both fields (and every other refresh_lead_profile field)
    fresh, from the now-correctly-scoped institution_id-filtered snapshot
    query. Each institution is processed in its own savepoint (see
    docs/CODE_REVIEW_LESSONS.md pattern 3) so one failure doesn't abort
    the batch or the ones already recomputed in it. Returns the number
    successfully recomputed.

    Correction: ordered by COALESCE(last_recompute_attempted_at,
    computed_at) ascending (oldest first), not left unordered, so repeated
    bounded calls actually make progress across every profile instead of
    reprocessing the same first `limit` rows forever. A successful
    refresh_lead_profile sets computed_at to "now" as its last step, and a
    failed one bumps last_recompute_attempted_at instead (see below) --
    either way the profile naturally sinks to the back of this ordering,
    so the next call picks up the next oldest/never-attempted batch with
    no separate offset or cursor to track.
    """
    cursor = func.coalesce(LeadProfile.last_recompute_attempted_at, LeadProfile.computed_at)
    institution_ids = (
        await session.scalars(
            select(LeadProfile.institution_id).order_by(cursor.asc()).limit(limit)
        )
    ).all()

    recomputed_count = 0
    for institution_id in institution_ids:
        try:
            async with session.begin_nested():
                await refresh_lead_profile(session, institution_id)
            recomputed_count += 1
        except Exception as e:
            print(f"[LeadProfile] recompute failed for institution {institution_id}: {e}")
            # Correction: without this, a profile whose refresh keeps
            # failing (a genuinely bad row) stays at the front of the
            # cursor ordering forever -- every subsequent bounded call
            # re-selects the same failing profile(s) and never reaches
            # later untrusted-but-healthy profiles behind it. Bump
            # last_recompute_attempted_at alone (in a fresh savepoint,
            # since the failed one above already rolled back) so the
            # cursor advances past it; computed_at and every other field
            # are deliberately left untouched -- computed_at still means
            # "last successfully computed", so a consumer never sees a
            # failed, still-untrusted profile reported as freshly
            # computed, and it stays as untrusted as this function's own
            # remediation note describes, just no longer blocking the
            # queue for every other profile.
            try:
                async with session.begin_nested():
                    await session.execute(
                        update(LeadProfile)
                        .where(LeadProfile.institution_id == institution_id)
                        .values(last_recompute_attempted_at=datetime.now(UTC))
                    )
            except Exception as advance_error:
                print(
                    f"[LeadProfile] failed to advance cursor past institution "
                    f"{institution_id}: {advance_error}"
                )

    return recomputed_count


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
            website_quality_tier=profile.website_quality_tier,
            service_gap_score=profile.service_gap_score,
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
