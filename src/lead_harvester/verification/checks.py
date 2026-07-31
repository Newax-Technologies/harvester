"""
Pure(-ish) verification checks against a CanonicalInstitution's already-
loaded evidence -- see docs/ROADMAP.md module 12. Each check returns the
arguments for a DataQualityFlag if it finds a problem, or None if it
doesn't; services/verification_service.py is what actually queries the
database and creates/dedupes the flag rows.

Kept as plain functions over already-fetched data (not doing their own DB
queries) so they're unit-testable without a database, matching the split
already used in allocation/eligibility.py vs
services/daily_selection_service.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.verification import FlagType
from lead_harvester.resolution.normalize import normalize_name
from lead_harvester.verification.confidence import confidence_for_source_count

# field_name recorded by canonical/merger.py's own attach_record_to_institution
# for "this raw record attached to this institution" links -- the count of
# these (plus the initial creating record) is exactly the "source_count"
# confidence_for_source_count expects, and it's what determines
# is_new_evidence there too.
_BRANCH_MEMBERSHIP_FIELD = "branch_membership"


@dataclass(frozen=True)
class CheckResult:
    flag_type: FlagType
    field_name: str | None
    details: dict[str, Any]


def check_confidence_drift(
    institution: CanonicalInstitution, branch_membership_count: int
) -> CheckResult | None:
    """
    Flags when the stored confidence_score no longer matches what the
    formula would compute from the institution's actual current count of
    distinct attached sources (branch_membership FieldProvenance rows).
    Drift can happen if a merge/split ever changes the source count
    without going through attach_record_to_institution's own increment
    (e.g. a future bulk data-migration script, or a manual DB edit) --
    this check exists to catch exactly that, not to duplicate the
    increment itself.
    """
    expected = confidence_for_source_count(branch_membership_count)
    if institution.confidence_score != expected:
        return CheckResult(
            flag_type=FlagType.CONFIDENCE_DRIFT,
            field_name=None,
            details={
                "stored": institution.confidence_score,
                "expected": expected,
                "branch_membership_count": branch_membership_count,
            },
        )
    return None


def check_stale_evidence(
    institution: CanonicalInstitution,
    latest_evidence_at: datetime | None,
    *,
    now: datetime,
    freshness_days: int,
) -> CheckResult | None:
    """
    Flags an institution with no recorded evidence (FieldProvenance or
    ResearchFinding) at all, or none within the freshness window -- its
    canonical data could be stale (a school could have moved, closed, or
    changed contacts) with nothing in the pipeline having looked at it
    again since.
    """
    if latest_evidence_at is None:
        age_days = None
    else:
        age_days = (now - latest_evidence_at).days
        if age_days < freshness_days:
            return None

    return CheckResult(
        flag_type=FlagType.STALE_EVIDENCE,
        field_name=None,
        details={
            "latest_evidence_at": latest_evidence_at.isoformat() if latest_evidence_at else None,
            "age_days": age_days,
            "freshness_days": freshness_days,
        },
    )


def check_conflicting_canonical_name(
    institution: CanonicalInstitution, name_provenance: list[FieldProvenance]
) -> CheckResult | None:
    """
    Flags when two or more sources assert meaningfully different
    canonical_name values for the same institution -- e.g. an
    authorized-import row and a Google Places record disagreeing on the
    name in a way normalization doesn't reconcile, which could mean two
    genuinely different institutions were merged together without ever
    going through the resolution PENDING review flow that would normally
    catch that ambiguity.

    v1 scope: exact comparison after resolution/normalize.py's own
    normalize_name (the same normalization used for blocking/matching
    elsewhere) -- not a fuzzy/trigram similarity check. Two names that
    normalize identically are never flagged; anything that doesn't is,
    even a minor variant, so this can be noisy on legitimate near-
    duplicates (e.g. "The Riverside School" vs "Riverside School") --
    accepted for v1 since a false positive here is a human dismissing a
    flag, not a silent data-integrity problem.
    """
    distinct_normalized: dict[str, list[str]] = {}
    for fp in name_provenance:
        value = fp.asserted_value if isinstance(fp.asserted_value, str) else str(fp.asserted_value)
        key = normalize_name(value)
        distinct_normalized.setdefault(key, []).append(value)

    if len(distinct_normalized) <= 1:
        return None

    return CheckResult(
        flag_type=FlagType.CONFLICTING_FIELD,
        field_name="canonical_name",
        details={"values": [v for values in distinct_normalized.values() for v in values]},
    )
