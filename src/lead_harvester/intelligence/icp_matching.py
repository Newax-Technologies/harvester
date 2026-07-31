"""
Scores how well an institution fits the configured Ideal Customer Profile
(ICP) -- see docs/ROADMAP.md module 7's icp_matching sub-concern, extended
by module 16/17 to be per-sector.

Distinct from profiles/scoring.py::compute_lead_score's "category_fit"
category, which only asks a binary question (is institution_type known at
all). This is a real, configurable, weighted match against operator-stated
target criteria -- the actual "does this lead match who we're targeting"
question a real ICP definition answers, not just "do we know what kind of
institution this is."

Criteria source, per-criterion (not all-or-nothing): each of
target_institution_types/min_branch_count is read from the institution's
Sector.icp_criteria dict when that KEY is present there, and only falls
back to the global Settings.icp_target_institution_types/icp_min_branch_count
for a key that's absent -- so a sector with only one criterion configured
still inherits the other from global settings, and every seeded sector's
initially-empty icp_criteria ({}) is a true no-op (100% today's global
behavior) until an operator actually fills one in.

Known v1 limitation: only two criteria exist (institution_type, minimum
branch count) -- geography/size-tier/other criteria are not yet
configurable dimensions here.
"""

from __future__ import annotations

from lead_harvester.config import Settings
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.sector import Sector

_MAX_SCORE = 100
_TYPE_MATCH_POINTS = 60
_TYPE_UNSTATED_POINTS = 30
_MIN_BRANCH_COUNT_POINTS = 40
_MIN_BRANCH_COUNT_UNSTATED_POINTS = 40


def score_icp_fit(
    institution: CanonicalInstitution,
    branch_count: int,
    settings: Settings,
    sector: Sector | None = None,
) -> int:
    icp_criteria = sector.icp_criteria if sector is not None else {}
    target_institution_types = icp_criteria.get(
        "target_institution_types", settings.icp_target_institution_types
    )
    min_branch_count = icp_criteria.get("min_branch_count", settings.icp_min_branch_count)

    score = 0

    # Institution-type criterion: full credit for a real match, partial
    # credit when the operator hasn't stated a preference at all (neither
    # a match nor a miss), zero when a real preference exists and this
    # institution's type isn't in it.
    if not target_institution_types:
        score += _TYPE_UNSTATED_POINTS
    elif institution.institution_type in target_institution_types:
        score += _TYPE_MATCH_POINTS

    # Minimum branch count criterion: same "unstated is neutral, not a
    # miss" treatment.
    if min_branch_count <= 0:
        score += _MIN_BRANCH_COUNT_UNSTATED_POINTS
    elif branch_count >= min_branch_count:
        score += _MIN_BRANCH_COUNT_POINTS

    return min(_MAX_SCORE, score)
