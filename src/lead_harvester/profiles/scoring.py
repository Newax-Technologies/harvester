"""
Lead scoring against LIVE data.

Computes an evidence-backed 0-100 score for a CanonicalInstitution from its
actual resolved data: branches, contact points, the latest qualification
assessment, and the latest AI research findings. Each contributing category
is kept in `breakdown` so a consumer can see *why* a lead scored the way it
did, not just the number (see docs/ROADMAP.md module 8's requirement that
scoring be evidence-backed, not an opaque single figure).

Deliberately NOT a reuse of intelligence/scoring.py -- that module scores the
dead Phase-1 `entities/` dataclasses (Institution/Branch/ContactPoint/
OpportunitySignal), which nothing in the live pipeline ever constructs (see
docs/CODE_REVIEW_LESSONS.md pattern 2 on divergent parallel implementations
of "the same" concept). This scores the real, live models instead:
models/canonical.py, models/qualification.py, models/research.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus
from lead_harvester.models.research import ResearchFinding

_FRESHNESS_WINDOW_DAYS = 30

# Category point caps -- must sum to 100 (compute_lead_score's overall_score
# is min(100, sum(breakdown.values())), so this is the effective ceiling).
_MAX_SCALE = 15
_MAX_CONTACTABILITY = 15
_MAX_CATEGORY_FIT = 15
_MAX_QUALIFICATION = 20
_MAX_RESEARCH_SIGNAL = 20
_MAX_FRESHNESS = 10
_MAX_CONFIDENCE = 5


@dataclass(frozen=True)
class ScoreResult:
    overall_score: int
    breakdown: dict[str, int]
    has_phone: bool
    has_email: bool
    has_named_contact: bool
    evidence_count: int


def compute_lead_score(
    institution: CanonicalInstitution,
    branches: list[Branch],
    contact_points: list[ContactPoint],
    qualification: QualificationAssessment | None,
    findings: list[ResearchFinding],
) -> ScoreResult:
    breakdown: dict[str, int] = {}

    # 1. Scale -- more physical branches means a bigger, more valuable account.
    branch_count = len(branches)
    if branch_count >= 5:
        breakdown["scale"] = _MAX_SCALE
    elif branch_count >= 3:
        breakdown["scale"] = 10
    elif branch_count >= 2:
        breakdown["scale"] = 5
    else:
        breakdown["scale"] = 0

    # 2. Contactability -- can we actually reach a real person here.
    has_phone = any(cp.contact_type == "phone" for cp in contact_points)
    has_email = any(cp.contact_type == "email" for cp in contact_points)
    has_named_contact = any(cp.person_name for cp in contact_points)
    contactability = 0
    if has_phone and institution.website:
        contactability += 8
    elif has_phone:
        contactability += 5
    if has_email:
        contactability += 2
    if has_named_contact:
        contactability += 5
    breakdown["contactability"] = min(_MAX_CONTACTABILITY, contactability)

    # 3. ICP/category fit -- do we even know what kind of institution this is.
    breakdown["category_fit"] = (
        _MAX_CATEGORY_FIT if institution.institution_type not in ("", "UNKNOWN") else 0
    )

    # 4. Qualification fit -- has anyone (human or QualificationAgent)
    # actually assessed this against an ICP, and did it pass. Only the
    # MOST RECENT assessment counts -- an institution's data (and thus its
    # fit) can change after an earlier assessment, so an old DISQUALIFIED
    # verdict shouldn't permanently suppress the score once new evidence
    # justifies re-assessment. Whether to actually re-assess is a separate
    # decision (see services/lead_profile_service.py::qualify_and_refresh);
    # this just reflects whatever the latest verdict says.
    qualification_points = 0
    if qualification is not None:
        if qualification.status == QualificationStatus.QUALIFIED:
            qualification_points = _MAX_QUALIFICATION
        elif qualification.status == QualificationStatus.NEEDS_REVIEW:
            qualification_points = _MAX_QUALIFICATION // 2
    breakdown["qualification"] = qualification_points

    # 5. Research signal -- pain points + buying signals an AI research pass
    # actually surfaced (currently only produced for LinkedIn profiles via
    # intelligence/researcher.py). Only the latest of each finding_key
    # counts, not a running total across every past research job, mirroring
    # how process_all_pending treats research as something that supersedes
    # a prior pass rather than accumulating with it.
    pain_points: list = []
    buying_signals: list = []
    latest_by_key: dict[str, ResearchFinding] = {}
    for f in findings:
        current = latest_by_key.get(f.finding_key)
        if current is None or f.created_at > current.created_at:
            latest_by_key[f.finding_key] = f
    pain_finding = latest_by_key.get("pain_points")
    if pain_finding is not None and isinstance(pain_finding.finding_value, list):
        pain_points = pain_finding.finding_value
    buying_finding = latest_by_key.get("buying_signals")
    if buying_finding is not None and isinstance(buying_finding.finding_value, list):
        buying_signals = buying_finding.finding_value
    research_points = min(10, len(pain_points) * 3) + min(10, len(buying_signals) * 3)
    breakdown["research_signal"] = min(_MAX_RESEARCH_SIGNAL, research_points)

    # 6. Freshness -- is there any recent evidence at all, or is everything
    # we know about this lead stale.
    cutoff = datetime.now(UTC) - timedelta(days=_FRESHNESS_WINDOW_DAYS)
    has_recent_finding = any(f.created_at >= cutoff for f in findings)
    breakdown["freshness"] = _MAX_FRESHNESS if has_recent_finding else 0

    # 7. Data confidence -- how corroborated is this institution's identity
    # itself (see resolution/scoring.py -- this is a different confidence
    # signal, about resolution match quality feeding into merger.py's
    # confidence_score, not about the research above).
    if institution.confidence_score > 0.8:
        breakdown["confidence"] = _MAX_CONFIDENCE
    elif institution.confidence_score > 0.5:
        breakdown["confidence"] = 2
    else:
        breakdown["confidence"] = 0

    overall_score = min(100, sum(breakdown.values()))

    return ScoreResult(
        overall_score=overall_score,
        breakdown=breakdown,
        has_phone=has_phone,
        has_email=has_email,
        has_named_contact=has_named_contact,
        evidence_count=len(findings),
    )
