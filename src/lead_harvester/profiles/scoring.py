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
from lead_harvester.models.signal import Signal, SignalType

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
    signals: list[Signal],
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

    # 5. Research signal -- pain points + buying signals detected for this
    # institution, from EITHER source: intelligence/researcher.py's AI
    # analysis (LinkedIn only) or enrichment/technology_detector.py's
    # rule-based website-text detection (see docs/ROADMAP.md module 6).
    # Reads models/signal.py's Signal rows directly rather than
    # ResearchFinding's "pain_points"/"buying_signals" list findings --
    # researcher.py's _persist_findings already writes a Signal row for
    # every item in those same lists (see models/signal.py's own
    # docstring), so Signal is a strict superset; reading both would
    # double-count a LinkedIn-researched institution's signals while still
    # giving a website-only institution's rule-based signals zero credit
    # (a real gap: those signals existed in the database but nothing that
    # computed a lead's score ever looked at them).
    pain_point_count = sum(1 for s in signals if s.signal_type == SignalType.PAIN_POINT)
    buying_signal_count = sum(1 for s in signals if s.signal_type == SignalType.BUYING_SIGNAL)
    research_points = min(10, pain_point_count * 3) + min(10, buying_signal_count * 3)
    breakdown["research_signal"] = min(_MAX_RESEARCH_SIGNAL, research_points)

    # 6. Freshness -- is there any recent evidence at all, or is everything
    # we know about this lead stale. Checks both findings (AI research
    # jobs) and signals (which can exist with zero ResearchFinding rows
    # for a website/maps-sourced institution that was never LinkedIn-
    # researched) -- checking findings alone previously scored a
    # freshly-crawled, signal-rich website institution as having stale
    # (zero) freshness just because no AI research job ever ran for it.
    cutoff = datetime.now(UTC) - timedelta(days=_FRESHNESS_WINDOW_DAYS)
    has_recent_finding = any(f.created_at >= cutoff for f in findings) or any(
        s.detected_at >= cutoff for s in signals
    )
    breakdown["freshness"] = _MAX_FRESHNESS if has_recent_finding else 0

    # 7. Data confidence -- how corroborated is this institution's identity
    # itself (see resolution/scoring.py -- this is a different confidence
    # signal, about resolution match quality feeding into merger.py's
    # confidence_score, not about the research above). confidence_score is
    # a 0-100 scale (verification/confidence.py, canonical/merger.py's own
    # +10-per-source/capped-at-100 convention) -- thresholds here were
    # previously 0.8/0.5, wrongly assuming a 0-1 fraction, which meant
    # every institution with even a single corroborating source (score
    # 10.0) always hit the top tier regardless of real corroboration.
    if institution.confidence_score > 80:
        breakdown["confidence"] = _MAX_CONFIDENCE
    elif institution.confidence_score > 50:
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
