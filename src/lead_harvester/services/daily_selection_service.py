"""
Ranking and Daily Selection (see docs/ROADMAP.md module 10). Claims a
bounded batch of the highest-scoring eligible leads for a round of
outreach work, so:
  - the same institution is never selected twice while its reservation is
    still active (duplicate_prevention);
  - two overlapping selection runs never claim the same institution
    (reservation, via SELECT ... FOR UPDATE SKIP LOCKED -- the same
    pattern used by outreach/automator.py's draft claiming and
    intelligence/researcher.py's process_all_pending);
  - a reservation nobody ever acts on eventually frees the institution
    back up instead of holding it forever (release_expired_reservations).

Known v1 limitation: nothing yet calls mark_consumed automatically --
outreach/automator.py works off OutreachDraft/AccountBrief, not
LeadProfile/LeadReservation, and wiring those two systems together is
separate, bigger integration work (see docs/ROADMAP.md's boundary-conflict
note on outreach/ itself). For now a reservation is consumed explicitly
(via the API/CLI) or simply expires: this module claims and tracks
capacity, it does not yet drive an outreach run.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.config import settings
from lead_harvester.models.allocation import LeadReservation, ReservationStatus
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus


async def release_expired_reservations(session: AsyncSession) -> int:
    """
    Transitions every RESERVED row past its expires_at to EXPIRED, freeing
    that institution up for a future selection. Always run before claiming
    a new batch (select_daily_batch calls this itself) so an expired
    reservation from an earlier run never blocks re-selection.
    """
    now = datetime.now(UTC)
    result = await session.execute(
        update(LeadReservation)
        .where(LeadReservation.status == ReservationStatus.RESERVED)
        .where(LeadReservation.expires_at < now)
        .values(status=ReservationStatus.EXPIRED, released_at=now)
    )
    await session.flush()
    return result.rowcount or 0


async def select_daily_batch(
    session: AsyncSession,
    *,
    limit: int | None = None,
    ttl_hours: float | None = None,
    min_score: int | None = None,
    batch_label: str | None = None,
) -> list[LeadReservation]:
    """
    Claims up to `limit` eligible LeadProfiles, highest-scoring first, and
    creates a LeadReservation for each -- atomically, so a concurrent call
    to this same function never claims an institution this call already
    claimed. See allocation/eligibility.py for the (kept-in-sync-by-hand)
    Python-side statement of the same filtering rules this query applies
    in SQL: institution must be OPERATIONAL, never DISQUALIFIED, meets
    min_score, and has at least one real contact method.

    The FOR UPDATE lock on LeadProfile is what actually prevents a double
    claim -- the "not already reserved" exclusion below only sees
    COMMITTED reservations, so two truly concurrent calls would otherwise
    both pass that check for the same row before either commits; SKIP
    LOCKED makes the second call's SELECT skip whatever the first has
    already locked, the same reasoning documented on every other claim
    query in this codebase.
    """
    limit = limit if limit is not None else settings.daily_selection_default_limit
    ttl_hours = (
        ttl_hours if ttl_hours is not None else settings.daily_selection_reservation_ttl_hours
    )
    min_score = min_score if min_score is not None else settings.daily_selection_min_score
    batch_label = batch_label or datetime.now(UTC).date().isoformat()

    await release_expired_reservations(session)

    actively_reserved = select(LeadReservation.institution_id).where(
        LeadReservation.status.in_([ReservationStatus.RESERVED, ReservationStatus.CONSUMED])
    )

    stmt = (
        select(LeadProfile)
        .join(CanonicalInstitution, CanonicalInstitution.id == LeadProfile.institution_id)
        .where(CanonicalInstitution.status == OperatingStatus.OPERATIONAL)
        .where(
            (LeadProfile.qualification_status != QualificationStatus.DISQUALIFIED)
            | (LeadProfile.qualification_status.is_(None))
        )
        .where(LeadProfile.overall_score >= min_score)
        .where((LeadProfile.has_phone.is_(True)) | (LeadProfile.has_email.is_(True)))
        .where(LeadProfile.institution_id.not_in(actively_reserved))
        .order_by(LeadProfile.overall_score.desc(), LeadProfile.institution_id.asc())
        .limit(limit)
        .with_for_update(of=LeadProfile, skip_locked=True)
    )

    candidates = list(await session.scalars(stmt))

    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=ttl_hours)
    reservations = []
    for profile in candidates:
        reservation = LeadReservation(
            institution_id=profile.institution_id,
            score_at_reservation=profile.overall_score,
            batch_label=batch_label,
            reserved_at=now,
            expires_at=expires_at,
        )
        session.add(reservation)
        reservations.append(reservation)

    await session.flush()
    return reservations


async def mark_consumed(session: AsyncSession, reservation_id: uuid.UUID) -> LeadReservation:
    """
    Marks a reservation as acted upon (e.g. outreach was actually sent),
    so it never re-enters selection and its capacity is accounted for as
    used rather than freed by expiry.
    """
    reservation = await session.get(LeadReservation, reservation_id)
    if reservation is None:
        raise ResourceNotFoundError(str(reservation_id))
    if reservation.status != ReservationStatus.RESERVED:
        raise ValueError(
            f"Reservation {reservation_id} is {reservation.status.value}, not reserved -- "
            "only an active reservation can be marked consumed."
        )
    reservation.status = ReservationStatus.CONSUMED
    reservation.consumed_at = datetime.now(UTC)
    await session.flush()
    return reservation


async def release_reservation(session: AsyncSession, reservation_id: uuid.UUID) -> LeadReservation:
    """
    Manually frees a reservation before its TTL expires (e.g. a reviewer
    decides this lead shouldn't be worked today after all) so it becomes
    selectable again on the very next call instead of waiting out the TTL.
    """
    reservation = await session.get(LeadReservation, reservation_id)
    if reservation is None:
        raise ResourceNotFoundError(str(reservation_id))
    if reservation.status != ReservationStatus.RESERVED:
        raise ValueError(
            f"Reservation {reservation_id} is {reservation.status.value}, not reserved -- "
            "only an active reservation can be released."
        )
    reservation.status = ReservationStatus.RELEASED
    reservation.released_at = datetime.now(UTC)
    await session.flush()
    return reservation


async def list_reservations(
    session: AsyncSession, *, status: ReservationStatus | None = None, limit: int = 100
) -> list[LeadReservation]:
    stmt = select(LeadReservation).order_by(LeadReservation.reserved_at.desc()).limit(limit)
    if status is not None:
        stmt = stmt.where(LeadReservation.status == status)
    return list(await session.scalars(stmt))
