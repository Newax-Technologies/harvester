"""
Eligibility and ranking rules for daily lead selection (see
docs/ROADMAP.md module 10). Pure functions, no DB access -- used by
api/routes/daily_selection.py's read-only ranked-preview endpoint.

services/daily_selection_service.py::select_daily_batch implements the
SAME eligibility/ranking logic again, but in SQL (so the actual claim
query can filter, order, and lock candidate rows in one atomic
statement). Keep the two in sync by hand if either changes -- the same
acknowledged tradeoff resolution/blocking.py's _predicted_decision
already documents for its own unavoidable duplication of scoring.py's
decision matrix.
"""

from __future__ import annotations

from lead_harvester.models.canonical import OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus


def is_eligible_for_selection(
    profile: LeadProfile, institution_status: OperatingStatus, *, min_score: int = 0
) -> bool:
    """
    A lead is eligible for today's selection if:
      - its institution is still OPERATIONAL (a closed institution is
        never worth reserving outreach capacity for);
      - it has never been explicitly DISQUALIFIED by QualificationAgent
        or a human reviewer (PENDING/NEEDS_REVIEW/never-assessed all still
        count -- only a confirmed DISQUALIFIED verdict excludes it);
      - its overall_score meets the caller's minimum bar;
      - it has at least one real contact method (has_phone or has_email)
        -- a lead with no way to actually reach anyone shouldn't consume a
        reservation slot at all, regardless of how it scored on the other
        components.
    """
    if institution_status != OperatingStatus.OPERATIONAL:
        return False
    if profile.qualification_status == QualificationStatus.DISQUALIFIED:
        return False
    if profile.overall_score < min_score:
        return False
    return profile.has_phone or profile.has_email


def ranking_sort_key(profile: LeadProfile) -> tuple[int, str]:
    """
    Deterministic ranking: highest overall_score first. Ties are broken by
    institution_id (an arbitrary but STABLE ordering) rather than left to
    whatever order the database happens to return rows in -- two
    selection runs against the same underlying data must always rank
    identically, which an unspecified tiebreak does not guarantee.
    """
    return (-profile.overall_score, str(profile.institution_id))
