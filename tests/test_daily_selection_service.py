import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.allocation import LeadReservation, ReservationStatus
from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint, OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus
from lead_harvester.services.daily_selection_service import (
    list_reservations,
    mark_consumed,
    release_expired_reservations,
    release_reservation,
    select_daily_batch,
)


async def _seed_profiled_institution(
    db_session,
    *,
    canonical_name: str,
    overall_score: int = 50,
    has_phone: bool = True,
    has_email: bool = False,
    qualification_status: QualificationStatus | None = None,
    status: OperatingStatus = OperatingStatus.OPERATIONAL,
) -> CanonicalInstitution:
    institution = CanonicalInstitution(canonical_name=canonical_name, status=status)
    db_session.add(institution)
    await db_session.flush()
    if has_phone:
        db_session.add(
            ContactPoint(
                institution_id=institution.id, contact_type="phone", contact_value="+923001234567"
            )
        )
    if has_email:
        db_session.add(
            ContactPoint(
                institution_id=institution.id, contact_type="email", contact_value="a@b.com"
            )
        )
    db_session.add(
        LeadProfile(
            institution_id=institution.id,
            overall_score=overall_score,
            has_phone=has_phone,
            has_email=has_email,
            qualification_status=qualification_status,
        )
    )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_select_daily_batch_ranks_highest_score_first(db_session):
    weak = await _seed_profiled_institution(
        db_session, canonical_name="Weak Lead", overall_score=10
    )
    strong = await _seed_profiled_institution(
        db_session, canonical_name="Strong Lead", overall_score=90
    )

    reservations = await select_daily_batch(db_session, limit=10)

    assert [r.institution_id for r in reservations] == [strong.id, weak.id]


@pytest.mark.asyncio
async def test_select_daily_batch_excludes_ineligible_institutions(db_session):
    closed = await _seed_profiled_institution(
        db_session, canonical_name="Closed School", status=OperatingStatus.CLOSED_PERMANENTLY
    )
    disqualified = await _seed_profiled_institution(
        db_session,
        canonical_name="Disqualified School",
        qualification_status=QualificationStatus.DISQUALIFIED,
    )
    no_contact = await _seed_profiled_institution(
        db_session, canonical_name="Unreachable School", has_phone=False, has_email=False
    )
    eligible = await _seed_profiled_institution(db_session, canonical_name="Eligible School")

    reservations = await select_daily_batch(db_session, limit=10)

    selected_ids = {r.institution_id for r in reservations}
    assert selected_ids == {eligible.id}
    assert closed.id not in selected_ids
    assert disqualified.id not in selected_ids
    assert no_contact.id not in selected_ids


@pytest.mark.asyncio
async def test_select_daily_batch_respects_limit(db_session):
    for i in range(5):
        await _seed_profiled_institution(db_session, canonical_name=f"School {i}", overall_score=i)

    reservations = await select_daily_batch(db_session, limit=2)

    assert len(reservations) == 2


@pytest.mark.asyncio
async def test_select_daily_batch_respects_min_score(db_session):
    await _seed_profiled_institution(db_session, canonical_name="Low Score", overall_score=5)
    high = await _seed_profiled_institution(
        db_session, canonical_name="High Score", overall_score=50
    )

    reservations = await select_daily_batch(db_session, limit=10, min_score=20)

    assert [r.institution_id for r in reservations] == [high.id]


@pytest.mark.asyncio
async def test_select_daily_batch_never_reselects_an_actively_reserved_institution(db_session):
    institution = await _seed_profiled_institution(db_session, canonical_name="Once Only")

    first = await select_daily_batch(db_session, limit=10)
    assert len(first) == 1

    second = await select_daily_batch(db_session, limit=10)
    assert second == []

    # Sanity: the institution really is still reserved, not silently
    # dropped from eligibility for some other reason.
    active = (
        await db_session.scalars(
            select(LeadReservation).where(LeadReservation.institution_id == institution.id)
        )
    ).all()
    assert len(active) == 1
    assert active[0].status == ReservationStatus.RESERVED


@pytest.mark.asyncio
async def test_release_expired_reservations_frees_the_institution_for_reselection(db_session):
    institution = await _seed_profiled_institution(db_session, canonical_name="Expiring Lead")
    db_session.add(
        LeadReservation(
            institution_id=institution.id,
            status=ReservationStatus.RESERVED,
            score_at_reservation=50,
            batch_label="2026-01-01",
            reserved_at=datetime.now(UTC) - timedelta(hours=48),
            expires_at=datetime.now(UTC) - timedelta(hours=24),
        )
    )
    await db_session.flush()

    released_count = await release_expired_reservations(db_session)
    assert released_count == 1

    reservations = await select_daily_batch(db_session, limit=10)
    assert [r.institution_id for r in reservations] == [institution.id]


@pytest.mark.asyncio
async def test_mark_consumed_transitions_status(db_session):
    await _seed_profiled_institution(db_session, canonical_name="Consume Me")
    reservations = await select_daily_batch(db_session, limit=10)
    reservation_id = reservations[0].id

    consumed = await mark_consumed(db_session, reservation_id)

    assert consumed.status == ReservationStatus.CONSUMED
    assert consumed.consumed_at is not None


@pytest.mark.asyncio
async def test_mark_consumed_raises_not_found_for_unknown_id(db_session):
    with pytest.raises(ResourceNotFoundError):
        await mark_consumed(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_mark_consumed_rejects_an_already_consumed_reservation(db_session):
    await _seed_profiled_institution(db_session, canonical_name="Twice Consumed")
    reservations = await select_daily_batch(db_session, limit=10)
    reservation_id = reservations[0].id
    await mark_consumed(db_session, reservation_id)

    with pytest.raises(ValueError, match="not reserved"):
        await mark_consumed(db_session, reservation_id)


@pytest.mark.asyncio
async def test_release_reservation_frees_the_institution_immediately(db_session):
    institution = await _seed_profiled_institution(db_session, canonical_name="Early Release")
    reservations = await select_daily_batch(db_session, limit=10)
    reservation_id = reservations[0].id

    released = await release_reservation(db_session, reservation_id)
    assert released.status == ReservationStatus.RELEASED
    assert released.released_at is not None

    reselected = await select_daily_batch(db_session, limit=10)
    assert [r.institution_id for r in reselected] == [institution.id]


@pytest.mark.asyncio
async def test_list_reservations_filters_by_status(db_session):
    await _seed_profiled_institution(db_session, canonical_name="A")
    await _seed_profiled_institution(db_session, canonical_name="B")
    reservations = await select_daily_batch(db_session, limit=10)
    await mark_consumed(db_session, reservations[0].id)

    reserved_only = await list_reservations(db_session, status=ReservationStatus.RESERVED)
    consumed_only = await list_reservations(db_session, status=ReservationStatus.CONSUMED)

    assert len(reserved_only) == 1
    assert len(consumed_only) == 1


@pytest.mark.asyncio
async def test_select_daily_batch_claim_query_never_double_reserves_across_connections(
    async_engine,
):
    # Two overlapping calls to select_daily_batch (e.g. an overlapping
    # cron schedule) must never both reserve the same institution.
    # with_for_update(skip_locked=True) claims rows as part of the SELECT
    # itself -- this proves two real, concurrent connections running that
    # exact claim query against the same candidate set never claim the
    # same row. See docs/CODE_REVIEW_LESSONS.md pattern 4.
    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    institution_ids = []
    for i in range(6):
        institution = CanonicalInstitution(
            canonical_name=f"Concurrency School {i}", status=OperatingStatus.OPERATIONAL
        )
        setup_session.add(institution)
        await setup_session.flush()
        setup_session.add(
            ContactPoint(
                institution_id=institution.id, contact_type="phone", contact_value=f"+92300{i}"
            )
        )
        setup_session.add(
            LeadProfile(institution_id=institution.id, overall_score=i, has_phone=True)
        )
        institution_ids.append(institution.id)
    await setup_session.commit()
    await setup_session.close()
    await setup_conn.close()

    first_claimed_event = asyncio.Event()
    second_selected_event = asyncio.Event()

    async def claim(*, first: bool) -> set:
        conn = await async_engine.connect()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            if not first:
                await first_claimed_event.wait()
            async with session.begin():
                reservations = await select_daily_batch(session, limit=10)
                if first:
                    first_claimed_event.set()
                    await second_selected_event.wait()
                else:
                    second_selected_event.set()
            return {r.institution_id for r in reservations}
        finally:
            await session.close()
            await conn.close()

    results = await asyncio.gather(claim(first=True), claim(first=False))

    try:
        claimed_a, claimed_b = results
        assert claimed_a.isdisjoint(claimed_b), (claimed_a, claimed_b)
        assert claimed_a | claimed_b == set(institution_ids)
    finally:
        cleanup_conn = await async_engine.connect()
        cleanup_session = AsyncSession(bind=cleanup_conn, expire_on_commit=False)
        try:
            await cleanup_session.execute(
                delete(LeadReservation).where(LeadReservation.institution_id.in_(institution_ids))
            )
            await cleanup_session.execute(
                delete(LeadProfile).where(LeadProfile.institution_id.in_(institution_ids))
            )
            await cleanup_session.execute(
                delete(ContactPoint).where(ContactPoint.institution_id.in_(institution_ids))
            )
            await cleanup_session.execute(
                delete(CanonicalInstitution).where(CanonicalInstitution.id.in_(institution_ids))
            )
            await cleanup_session.commit()
        finally:
            await cleanup_session.close()
            await cleanup_conn.close()
