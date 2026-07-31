"""
Runs verification/checks.py's checks against real data and manages the
resulting DataQualityFlag review queue -- see docs/ROADMAP.md module 12.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.research import ResearchFinding
from lead_harvester.models.verification import DataQualityFlag, FlagStatus, FlagType
from lead_harvester.verification.checks import (
    _BRANCH_MEMBERSHIP_FIELD,
    CheckResult,
    check_confidence_drift,
    check_conflicting_canonical_name,
    check_stale_evidence,
)

_DEFAULT_FRESHNESS_DAYS = 90


async def run_verification_checks(
    session: AsyncSession,
    institution_id: uuid.UUID,
    *,
    freshness_days: int = _DEFAULT_FRESHNESS_DAYS,
    now: datetime | None = None,
) -> list[DataQualityFlag]:
    """
    Runs every check against one institution's current evidence and
    creates a DataQualityFlag for each new problem found. Returns only
    the flags created THIS call -- a check whose problem is already
    covered by an existing OPEN flag of the same (flag_type, field_name)
    does not create a duplicate.
    """
    now = now or datetime.now(UTC)

    institution = await session.get(CanonicalInstitution, institution_id)
    if institution is None:
        raise ResourceNotFoundError(str(institution_id))

    provenance = list(
        (
            await session.scalars(
                select(FieldProvenance).where(FieldProvenance.canonical_id == institution_id)
            )
        ).all()
    )
    branch_membership_count = sum(
        1 for fp in provenance if fp.field_name == _BRANCH_MEMBERSHIP_FIELD
    )
    name_provenance = [fp for fp in provenance if fp.field_name == "canonical_name"]

    latest_provenance_at = max((fp.created_at for fp in provenance), default=None)
    latest_finding_at = await session.scalar(
        select(func.max(ResearchFinding.created_at)).where(
            ResearchFinding.institution_id == institution_id
        )
    )
    latest_evidence_at = max(
        (t for t in (latest_provenance_at, latest_finding_at) if t is not None), default=None
    )

    results: list[CheckResult] = []
    confidence_result = check_confidence_drift(institution, branch_membership_count)
    if confidence_result is not None:
        results.append(confidence_result)

    stale_result = check_stale_evidence(
        institution, latest_evidence_at, now=now, freshness_days=freshness_days
    )
    if stale_result is not None:
        results.append(stale_result)

    if name_provenance:
        conflict_result = check_conflicting_canonical_name(institution, name_provenance)
        if conflict_result is not None:
            results.append(conflict_result)

    created: list[DataQualityFlag] = []
    for result in results:
        already_open = await session.scalar(
            select(DataQualityFlag.id)
            .where(DataQualityFlag.institution_id == institution_id)
            .where(DataQualityFlag.flag_type == result.flag_type)
            .where(DataQualityFlag.field_name == result.field_name)
            .where(DataQualityFlag.status == FlagStatus.OPEN)
            .limit(1)
        )
        if already_open is not None:
            continue

        flag = DataQualityFlag(
            institution_id=institution_id,
            flag_type=result.flag_type,
            field_name=result.field_name,
            details=result.details,
        )
        session.add(flag)
        created.append(flag)

    if created:
        await session.flush()
    return created


async def run_verification_sweep(
    session: AsyncSession, *, limit: int = 200, freshness_days: int = _DEFAULT_FRESHNESS_DAYS
) -> int:
    """
    Runs run_verification_checks across a batch of institutions. Each
    institution is processed in its own SAVEPOINT (see
    docs/CODE_REVIEW_LESSONS.md pattern 3) so one institution's failure
    doesn't abort the whole sweep. Returns the total number of new flags
    created across the batch.
    """
    institution_ids = list(
        (await session.scalars(select(CanonicalInstitution.id).limit(limit))).all()
    )

    total_created = 0
    for institution_id in institution_ids:
        try:
            async with session.begin_nested():
                created = await run_verification_checks(
                    session, institution_id, freshness_days=freshness_days
                )
            total_created += len(created)
        except Exception as e:
            print(f"[Verification] check failed for institution {institution_id}: {e}")

    return total_created


async def resolve_flag(
    session: AsyncSession, flag_id: uuid.UUID, note: str = ""
) -> DataQualityFlag:
    flag = await session.get(DataQualityFlag, flag_id)
    if flag is None:
        raise ResourceNotFoundError(str(flag_id))
    if flag.status != FlagStatus.OPEN:
        raise ValueError(f"Flag {flag_id} is {flag.status.value}, not open -- nothing to resolve.")
    flag.status = FlagStatus.RESOLVED
    flag.resolved_at = datetime.now(UTC)
    flag.resolution_note = note
    await session.flush()
    return flag


async def dismiss_flag(
    session: AsyncSession, flag_id: uuid.UUID, note: str = ""
) -> DataQualityFlag:
    flag = await session.get(DataQualityFlag, flag_id)
    if flag is None:
        raise ResourceNotFoundError(str(flag_id))
    if flag.status != FlagStatus.OPEN:
        raise ValueError(f"Flag {flag_id} is {flag.status.value}, not open -- nothing to dismiss.")
    flag.status = FlagStatus.DISMISSED
    flag.resolved_at = datetime.now(UTC)
    flag.resolution_note = note
    await session.flush()
    return flag


async def flag_contact_unreachable(
    session: AsyncSession, contact_point_id: uuid.UUID, note: str = ""
) -> DataQualityFlag:
    """
    Manually records that a specific contact was found unreachable (a
    bounced email, a disconnected number). No automated email/phone
    verification integration exists yet -- see docs/ROADMAP.md module 12
    -- so this is the only way an UNREACHABLE_CONTACT flag is created in
    v1, whether triggered by a human or a future external check.
    """
    contact = await session.get(ContactPoint, contact_point_id)
    if contact is None:
        raise ResourceNotFoundError(str(contact_point_id))

    already_open = await session.scalar(
        select(DataQualityFlag.id)
        .where(DataQualityFlag.institution_id == contact.institution_id)
        .where(DataQualityFlag.flag_type == FlagType.UNREACHABLE_CONTACT)
        .where(DataQualityFlag.field_name == str(contact_point_id))
        .where(DataQualityFlag.status == FlagStatus.OPEN)
        .limit(1)
    )
    if already_open is not None:
        return await session.get(DataQualityFlag, already_open)

    flag = DataQualityFlag(
        institution_id=contact.institution_id,
        flag_type=FlagType.UNREACHABLE_CONTACT,
        field_name=str(contact_point_id),
        details={
            "contact_type": contact.contact_type,
            "contact_value": contact.contact_value,
            "note": note,
        },
    )
    session.add(flag)
    await session.flush()
    return flag


async def list_flags(
    session: AsyncSession,
    *,
    status: FlagStatus | None = None,
    flag_type: FlagType | None = None,
    limit: int = 100,
) -> list[DataQualityFlag]:
    stmt = select(DataQualityFlag).order_by(DataQualityFlag.detected_at.desc()).limit(limit)
    if status is not None:
        stmt = stmt.where(DataQualityFlag.status == status)
    if flag_type is not None:
        stmt = stmt.where(DataQualityFlag.flag_type == flag_type)
    return list(await session.scalars(stmt))
