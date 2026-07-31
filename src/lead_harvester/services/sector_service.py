"""
Sector (business vertical) registry -- see docs/ROADMAP.md module 16.

resolve_sector_for_institution_type/classify_institution_sector are the
auto-classification path wired into canonical/merger.py and
api/routes/manual_leads.py so every institution-producing write path
assigns a sector automatically. apply_sector_hint_fallback is the
separate, deliberately-secondary job.yaml `sector` hint, applied only
when institution_type-based classification comes up empty (see
pipeline.py's `_resolve_or_log`).
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.sector import Sector


async def list_sectors(session: AsyncSession) -> list[Sector]:
    return list((await session.scalars(select(Sector).order_by(Sector.code))).all())


async def get_sector(session: AsyncSession, sector_id: uuid.UUID) -> Sector | None:
    return await session.get(Sector, sector_id)


async def create_sector(
    session: AsyncSession,
    *,
    code: str,
    display_name: str,
    institution_types: list[str] | None = None,
    icp_criteria: dict | None = None,
    qualification_rules: dict | None = None,
) -> Sector:
    existing = await session.scalar(select(Sector).where(Sector.code == code))
    if existing is not None:
        raise ValueError(f"A sector with code {code!r} already exists.")

    sector = Sector(
        code=code,
        display_name=display_name,
        institution_types=institution_types or [],
        icp_criteria=icp_criteria or {},
        qualification_rules=qualification_rules or {},
    )
    session.add(sector)
    await session.flush()
    return sector


async def update_sector(
    session: AsyncSession,
    sector_id: uuid.UUID,
    *,
    display_name: str | None = None,
    institution_types: list[str] | None = None,
    icp_criteria: dict | None = None,
    qualification_rules: dict | None = None,
) -> Sector:
    sector = await session.get(Sector, sector_id)
    if sector is None:
        raise ResourceNotFoundError(str(sector_id))

    if display_name is not None:
        sector.display_name = display_name
    if institution_types is not None:
        sector.institution_types = institution_types
    if icp_criteria is not None:
        sector.icp_criteria = icp_criteria
    if qualification_rules is not None:
        sector.qualification_rules = qualification_rules

    await session.flush()
    return sector


async def resolve_sector_for_institution_type(
    session: AsyncSession, institution_type: str
) -> Sector | None:
    """
    Matches institution_type (case-insensitively) against every
    configured Sector's institution_types membership list. Returns None
    for a blank institution_type or one that doesn't match any configured
    sector -- callers must treat that as "leave unclassified", not guess.
    """
    if not institution_type:
        return None

    normalized = institution_type.strip().lower()
    sectors = await list_sectors(session)
    for sector in sectors:
        if normalized in (t.strip().lower() for t in sector.institution_types):
            return sector
    return None


async def classify_institution_sector(
    session: AsyncSession, institution: CanonicalInstitution
) -> None:
    """
    Sets institution.sector_id from institution.institution_type if it's
    currently unset and a sector now matches -- a no-op otherwise (never
    reclassifies an already-classified institution, and never clears a
    sector that was previously resolved even if institution_type later
    goes blank, matching this codebase's existing fill-if-missing
    convention for institution_type/website backfill in canonical/merger.py).
    """
    if institution.sector_id is not None:
        return

    sector = await resolve_sector_for_institution_type(session, institution.institution_type)
    if sector is not None:
        institution.sector_id = sector.id


async def apply_sector_hint_fallback(
    session: AsyncSession, institution: CanonicalInstitution, hint_code: str | None
) -> None:
    """
    job.yaml's optional `sector` key -- applied only when institution_type-
    based classification (classify_institution_sector, called earlier in
    the same write path via canonical/merger.py) left sector_id unset.
    institution_type stays the authoritative source: this never overrides
    a sector that classify_institution_sector already resolved.
    """
    if institution.sector_id is not None or not hint_code:
        return

    sector = await session.scalar(select(Sector).where(Sector.code == hint_code))
    if sector is not None:
        institution.sector_id = sector.id


async def classify_all_unclassified(session: AsyncSession, *, limit: int = 500) -> int:
    """
    One-time backfill for institutions that predate this module (or were
    created before their matching Sector existed). Each institution is
    processed in its own savepoint (docs/CODE_REVIEW_LESSONS.md pattern 3)
    so one failure doesn't abort the batch. Returns the number classified
    (institutions with no matching sector are skipped, not counted as a
    failure).
    """
    institution_ids = (
        await session.scalars(
            select(CanonicalInstitution.id)
            .where(CanonicalInstitution.sector_id.is_(None))
            .limit(limit)
        )
    ).all()

    classified_count = 0
    for institution_id in institution_ids:
        try:
            async with session.begin_nested():
                institution = await session.get(CanonicalInstitution, institution_id)
                if institution is None:
                    continue
                before = institution.sector_id
                await classify_institution_sector(session, institution)
                if institution.sector_id is not None and before is None:
                    classified_count += 1
        except Exception as e:
            print(f"[Sector] classification failed for institution {institution_id}: {e}")

    return classified_count
