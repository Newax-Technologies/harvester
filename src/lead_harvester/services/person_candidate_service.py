"""
Identity resolution for the person_candidate entity -- see
docs/ROADMAP.md module 1 ("Entity Registry"). Called from every live path
that writes a ContactPoint with a person_name (canonical/merger.py's
_add_contact_if_present, api/routes/manual_leads.py's create_manual_lead)
so the same real person named on two different contact points for one
institution converges onto one PersonCandidate row instead of silently
staying two unrelated bare strings.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.person import PersonCandidate
from lead_harvester.resolution.normalize import normalize_name


async def resolve_person_candidate(
    session: AsyncSession, institution_id: uuid.UUID, person_name: str | None
) -> PersonCandidate | None:
    """
    Find-or-create the PersonCandidate for `person_name` at this
    institution, bumping its evidence_count/last_seen_at either way.
    Returns None for a blank/whitespace-only name -- a bare office phone
    or generic "info@" email has no person to resolve.

    Matching is exact-after-normalize_name (the same normalizer
    verification/checks.py's conflicting-canonical-name check already
    uses for institution names), not fuzzy -- consistent with this
    codebase's v1 convention elsewhere of exact-after-normalization
    rather than trigram/fuzzy similarity for identity matching.

    SELECT ... FOR UPDATE on the lookup, backed by a unique constraint on
    (institution_id, normalized_name) as defense in depth (see the
    d7f9b1c3e5a7 migration) -- the same two-layer concurrency-safety
    pattern LeadReservation's claim query and partial unique index use,
    so two contact points for the same new person created in an
    overlapping transaction can't each mint their own PersonCandidate row.
    """
    if not person_name or not person_name.strip():
        return None
    normalized = normalize_name(person_name)
    if not normalized:
        return None

    now = datetime.now(UTC)
    existing = await session.scalar(
        select(PersonCandidate)
        .where(PersonCandidate.institution_id == institution_id)
        .where(PersonCandidate.normalized_name == normalized)
        .with_for_update()
    )
    if existing is not None:
        existing.evidence_count += 1
        existing.last_seen_at = now
        existing.display_name = person_name.strip()
        return existing

    candidate = PersonCandidate(
        institution_id=institution_id,
        display_name=person_name.strip(),
        normalized_name=normalized,
        evidence_count=1,
        first_seen_at=now,
        last_seen_at=now,
    )
    session.add(candidate)
    await session.flush()
    return candidate


async def list_person_candidates(
    session: AsyncSession, *, institution_id: uuid.UUID | None = None, limit: int = 100
) -> list[PersonCandidate]:
    stmt = select(PersonCandidate).order_by(PersonCandidate.last_seen_at.desc()).limit(limit)
    if institution_id is not None:
        stmt = stmt.where(PersonCandidate.institution_id == institution_id)
    return list(await session.scalars(stmt))
