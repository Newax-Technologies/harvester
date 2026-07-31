import asyncio
import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.config import Settings
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.outbox import EventOutbox, OutboxStatus
from lead_harvester.services import outbox_service
from lead_harvester.services.outbox_service import (
    MAX_ATTEMPTS,
    _attempt_delivery,
    _backoff_seconds,
    enqueue_and_attempt_delivery,
    list_outbox_entries,
    process_pending_deliveries,
    requeue_dead_letter,
)


def _enabled_settings() -> Settings:
    return Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_url="https://core-newax.test/api/integrations/lead-harvester/webhook",
        lead_sync_webhook_secret="test-secret-with-more-than-32-characters",
    )


async def _seed_institution(
    db_session, name: str
) -> tuple[CanonicalInstitution, list[Branch], list[ContactPoint]]:
    # Returns the branch/contact objects directly rather than relying on
    # institution.branches/.contact_points -- those are lazy relationships,
    # and accessing them outside an already-awaited SQLAlchemy call chain
    # raises MissingGreenlet (the same class of bug documented in
    # docs/CODE_REVIEW_LESSONS.md for refresh_lead_profile).
    institution = CanonicalInstitution(
        canonical_name=name, status=OperatingStatus.OPERATIONAL, confidence_score=50.0
    )
    db_session.add(institution)
    await db_session.flush()
    branch = Branch(
        institution_id=institution.id,
        branch_name="Main",
        city="Lahore",
        country_code="PK",
        provider_ids={},
    )
    contact = ContactPoint(
        institution_id=institution.id,
        contact_type="phone",
        contact_value=f"+9230012{uuid.uuid4().int % 100000:05d}",
        is_publicly_listed=False,
    )
    db_session.add_all([branch, contact])
    await db_session.flush()
    return institution, [branch], [contact]


def _success_response(settings: Settings) -> httpx.Response:
    return httpx.Response(200, request=httpx.Request("POST", settings.lead_sync_webhook_url))


def test_backoff_seconds_grows_exponentially_and_caps():
    assert _backoff_seconds(1) == outbox_service.BACKOFF_BASE_SECONDS
    assert _backoff_seconds(2) == outbox_service.BACKOFF_BASE_SECONDS * 2
    assert _backoff_seconds(3) == outbox_service.BACKOFF_BASE_SECONDS * 4
    assert _backoff_seconds(20) == outbox_service.MAX_BACKOFF_SECONDS


@pytest.mark.asyncio
async def test_enqueue_and_attempt_delivery_noops_when_disabled(db_session):
    settings = Settings(lead_sync_enabled=False)
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Disabled Sync School"
    )

    result = await enqueue_and_attempt_delivery(
        db_session, emitter, institution, institution_branches, institution_contacts
    )

    assert result is None
    assert (await db_session.execute(select(EventOutbox))).scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_enqueue_and_attempt_delivery_marks_delivered_on_success(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Delivered School"
    )

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=_success_response(settings),
    ) as mock_post:
        row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            institution,
            institution_branches,
            institution_contacts,
        )

    mock_post.assert_awaited_once()
    assert row.status == OutboxStatus.DELIVERED
    assert row.attempt_count == 1
    assert row.delivered_at is not None
    assert row.last_error is None
    # The row's own id is the payload's eventId -- a retry of this row must
    # reuse this identical id, not mint a new one.
    assert str(row.id) == row.payload["eventId"]


@pytest.mark.asyncio
async def test_enqueue_and_attempt_delivery_schedules_retry_on_failure(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Failing School"
    )

    before = datetime.now(UTC)
    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            institution,
            institution_branches,
            institution_contacts,
        )

    assert row.status == OutboxStatus.PENDING
    assert row.attempt_count == 1
    assert row.last_error is not None
    assert row.next_attempt_at > before + timedelta(seconds=outbox_service.BACKOFF_BASE_SECONDS - 1)


@pytest.mark.asyncio
async def test_repeated_failures_move_row_to_dead_letter_after_max_attempts(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Dead Letter School"
    )

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            institution,
            institution_branches,
            institution_contacts,
        )
        # First attempt already happened inside enqueue -- drive the
        # remaining attempts directly via _attempt_delivery so this test
        # doesn't depend on real wall-clock time passing for backoff.
        for _ in range(MAX_ATTEMPTS - 1):
            await _attempt_delivery(db_session, emitter, row)

    assert row.attempt_count == MAX_ATTEMPTS
    assert row.status == OutboxStatus.DEAD_LETTER


@pytest.mark.asyncio
async def test_process_pending_deliveries_only_claims_due_pending_rows(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    due_institution, due_institution_branches, due_institution_contacts = await _seed_institution(
        db_session, "Due School"
    )
    (
        future_institution,
        future_institution_branches,
        future_institution_contacts,
    ) = await _seed_institution(db_session, "Future School")

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        due_row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            due_institution,
            due_institution_branches,
            due_institution_contacts,
        )
        future_row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            future_institution,
            future_institution_branches,
            future_institution_contacts,
        )

    # Both rows just failed and got a future next_attempt_at from backoff --
    # pull one back into the past so only it is due for a retry.
    due_row.next_attempt_at = datetime.now(UTC) - timedelta(seconds=1)
    await db_session.flush()

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=_success_response(settings),
    ) as mock_post:
        processed = await process_pending_deliveries(db_session, emitter, limit=10)

    assert processed == 1
    mock_post.assert_awaited_once()
    await db_session.refresh(due_row)
    await db_session.refresh(future_row)
    assert due_row.status == OutboxStatus.DELIVERED
    assert future_row.status == OutboxStatus.PENDING
    assert future_row.attempt_count == 1


@pytest.mark.asyncio
async def test_process_pending_deliveries_isolates_one_rows_failure(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    ok_institution, _ok_branches, _ok_contacts = await _seed_institution(
        db_session, "Isolated OK School"
    )
    broken_institution, _broken_branches, _broken_contacts = await _seed_institution(
        db_session, "Isolated Broken School"
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock):
        ok_row = EventOutbox(
            institution_id=ok_institution.id,
            event_type="institution.upserted",
            payload=emitter._build_payload(ok_institution, [], []),
            status=OutboxStatus.PENDING,
            next_attempt_at=datetime.now(UTC) - timedelta(seconds=1),
        )
        broken_row = EventOutbox(
            institution_id=broken_institution.id,
            event_type="institution.upserted",
            payload=emitter._build_payload(broken_institution, [], []),
            status=OutboxStatus.PENDING,
            next_attempt_at=datetime.now(UTC) - timedelta(seconds=1),
        )
    db_session.add_all([ok_row, broken_row])
    await db_session.flush()

    original_attempt_delivery = outbox_service._attempt_delivery

    async def flaky_attempt_delivery(session, emitter_arg, row):
        if row.id == broken_row.id:
            raise RuntimeError("simulated unexpected DB-level failure")
        await original_attempt_delivery(session, emitter_arg, row)

    with (
        patch(
            "lead_harvester.services.outbox_service._attempt_delivery",
            new=flaky_attempt_delivery,
        ),
        patch(
            "httpx.AsyncClient.post",
            new_callable=AsyncMock,
            return_value=_success_response(settings),
        ),
    ):
        processed = await process_pending_deliveries(db_session, emitter, limit=10)

    # Only the row that didn't raise counts as processed -- the broken
    # row's failure must not corrupt the rest of the batch or leave the
    # session unusable for the row that succeeded.
    assert processed == 1
    await db_session.refresh(ok_row)
    assert ok_row.status == OutboxStatus.DELIVERED
    # The savepoint around the broken row's attempt rolled back cleanly --
    # confirm the session is still perfectly usable afterward.
    still_queryable = (
        await db_session.execute(select(EventOutbox).where(EventOutbox.id == broken_row.id))
    ).scalar_one()
    assert still_queryable.id == broken_row.id


@pytest.mark.asyncio
async def test_requeue_dead_letter_resets_row_to_pending(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Requeue School"
    )

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            institution,
            institution_branches,
            institution_contacts,
        )
        for _ in range(MAX_ATTEMPTS - 1):
            await _attempt_delivery(db_session, emitter, row)
    assert row.status == OutboxStatus.DEAD_LETTER

    requeued = await requeue_dead_letter(db_session, row.id)

    assert requeued.status == OutboxStatus.PENDING
    assert requeued.attempt_count == 0
    assert requeued.last_error is None


@pytest.mark.asyncio
async def test_requeue_dead_letter_raises_not_found_for_unknown_id(db_session):
    with pytest.raises(ResourceNotFoundError):
        await requeue_dead_letter(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_requeue_dead_letter_rejects_non_dead_letter_row(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    institution, institution_branches, institution_contacts = await _seed_institution(
        db_session, "Not Dead Yet School"
    )

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=_success_response(settings),
    ):
        row = await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            institution,
            institution_branches,
            institution_contacts,
        )
    assert row.status == OutboxStatus.DELIVERED

    with pytest.raises(ValueError, match="not dead_letter"):
        await requeue_dead_letter(db_session, row.id)


@pytest.mark.asyncio
async def test_list_outbox_entries_filters_by_status(db_session):
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)
    (
        delivered_institution,
        delivered_institution_branches,
        delivered_institution_contacts,
    ) = await _seed_institution(db_session, "Listed Delivered School")
    (
        failed_institution,
        failed_institution_branches,
        failed_institution_contacts,
    ) = await _seed_institution(db_session, "Listed Failed School")

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        return_value=_success_response(settings),
    ):
        await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            delivered_institution,
            delivered_institution_branches,
            delivered_institution_contacts,
        )
    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        await enqueue_and_attempt_delivery(
            db_session,
            emitter,
            failed_institution,
            failed_institution_branches,
            failed_institution_contacts,
        )

    delivered_only = await list_outbox_entries(db_session, status=OutboxStatus.DELIVERED)
    pending_only = await list_outbox_entries(db_session, status=OutboxStatus.PENDING)

    assert [r.institution_id for r in delivered_only] == [delivered_institution.id]
    assert [r.institution_id for r in pending_only] == [failed_institution.id]


@pytest.mark.asyncio
async def test_process_pending_deliveries_claim_query_never_double_delivers_across_connections(
    async_engine,
):
    # Two overlapping calls to process_pending_deliveries (e.g. an
    # overlapping cron schedule) must never both attempt the same row --
    # SELECT ... FOR UPDATE SKIP LOCKED claims rows as part of the SELECT
    # itself. See docs/CODE_REVIEW_LESSONS.md pattern 4 and
    # test_daily_selection_service.py's equivalent concurrency test.
    settings = _enabled_settings()
    emitter = LeadSyncEmitter(settings)

    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    row_ids = []
    institution_ids = []
    try:
        for i in range(6):
            institution = CanonicalInstitution(
                canonical_name=f"Outbox Concurrency School {i}",
                status=OperatingStatus.OPERATIONAL,
            )
            setup_session.add(institution)
            await setup_session.flush()
            row = EventOutbox(
                institution_id=institution.id,
                event_type="institution.upserted",
                payload=emitter._build_payload(institution, [], []),
                status=OutboxStatus.PENDING,
                next_attempt_at=datetime.now(UTC) - timedelta(seconds=1),
            )
            setup_session.add(row)
            await setup_session.flush()
            row_ids.append(row.id)
            institution_ids.append(institution.id)
        await setup_session.commit()
    finally:
        await setup_session.close()
        await setup_conn.close()

    first_claimed_event = asyncio.Event()
    second_claimed_event = asyncio.Event()

    async def claim(*, first: bool) -> int:
        conn = await async_engine.connect()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            if not first:
                await first_claimed_event.wait()
            with patch(
                "httpx.AsyncClient.post",
                new_callable=AsyncMock,
                return_value=_success_response(settings),
            ):
                async with session.begin():
                    processed = await process_pending_deliveries(session, emitter, limit=10)
                    if first:
                        first_claimed_event.set()
                        await second_claimed_event.wait()
                    else:
                        second_claimed_event.set()
            return processed
        finally:
            await session.close()
            await conn.close()

    processed_a, processed_b = await asyncio.gather(claim(first=True), claim(first=False))

    try:
        # Each row can only be delivered once -- the two runs' claimed
        # counts must sum to exactly the seeded row count, with no overlap
        # (a double-claim would sum to more than len(row_ids); a dropped
        # row would sum to less).
        assert processed_a + processed_b == len(row_ids)

        verify_conn = await async_engine.connect()
        verify_session = AsyncSession(bind=verify_conn, expire_on_commit=False)
        try:
            delivered = (
                await verify_session.scalars(select(EventOutbox).where(EventOutbox.id.in_(row_ids)))
            ).all()
            assert all(r.status == OutboxStatus.DELIVERED for r in delivered)
            assert all(r.attempt_count == 1 for r in delivered)
        finally:
            await verify_session.close()
            await verify_conn.close()
    finally:
        cleanup_conn = await async_engine.connect()
        cleanup_session = AsyncSession(bind=cleanup_conn, expire_on_commit=False)
        try:
            await cleanup_session.execute(
                delete(EventOutbox).where(EventOutbox.institution_id.in_(institution_ids))
            )
            await cleanup_session.execute(
                delete(CanonicalInstitution).where(CanonicalInstitution.id.in_(institution_ids))
            )
            await cleanup_session.commit()
        finally:
            await cleanup_session.close()
            await cleanup_conn.close()
