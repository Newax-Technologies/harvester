"""
Estimates an institution's size tier -- see docs/ROADMAP.md module 7's
size_estimation sub-concern.

Known v1 limitation: no headcount/enrollment data exists anywhere in this
schema (no connector collects it), so this is a proxy from the only size
signals actually available -- how many physical branches/locations resolved
to this institution, and how many distinct contact points it has on
record -- not a real student/staff count.
"""

from __future__ import annotations

from lead_harvester.models.canonical import Branch, ContactPoint
from lead_harvester.models.profile import SizeTier

_LARGE_BRANCH_COUNT = 5
_MEDIUM_BRANCH_COUNT = 2
_LARGE_CONTACT_COUNT = 6
_MEDIUM_CONTACT_COUNT = 3


def estimate_size_tier(branches: list[Branch], contact_points: list[ContactPoint]) -> SizeTier:
    """
    LARGE: 5+ branches, or a single-branch institution with 6+ distinct
    contact points (a large single-campus institution often has many
    contacts rather than many locations).
    MEDIUM: 2+ branches, or 3+ contact points.
    SMALL: exactly one branch and fewer than 3 contact points.
    UNKNOWN: no branch data at all (an institution with zero resolved
    branches is a data gap, not evidence of being small).
    """
    branch_count = len(branches)
    contact_count = len(contact_points)

    if branch_count == 0:
        return SizeTier.UNKNOWN

    if branch_count >= _LARGE_BRANCH_COUNT or contact_count >= _LARGE_CONTACT_COUNT:
        return SizeTier.LARGE

    if branch_count >= _MEDIUM_BRANCH_COUNT or contact_count >= _MEDIUM_CONTACT_COUNT:
        return SizeTier.MEDIUM

    return SizeTier.SMALL
