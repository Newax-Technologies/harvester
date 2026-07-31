"""
Durable outbound event delivery -- see docs/ROADMAP.md module 13's
event_outbox/delivery_status pieces. integrations/lead_sync_emitter.py's
emit_institution_upserted is intentionally left unmodified (its public
signature/behavior is relied on by ~15 existing tests) and stays
fire-and-forget with no retry. This module is the durable path on top of
it: api/routes/manual_leads.py and integrations/lead_sync_resync.py now
call enqueue_and_attempt_delivery instead of the emitter directly, so a
failed delivery becomes a PENDING outbox row instead of a lost event.

_attempt_delivery deliberately does NOT call
emitter.emit_institution_upserted -- that method always swallows its own
result (no way to know success/failure to update outbox status) and
rebuilds a fresh payload with a new eventId on every call, which would
break the "every retry of the same logical event reuses the same eventId"
guarantee this module exists to provide. Instead it reuses the emitter's
private _build_payload/_sign helpers directly (see lead_sync_emitter.py's
own _filter_supported_contacts docstring for the same reuse reasoning)
and does its own HTTP call plus status/backoff bookkeeping.
"""

from __future__ import annotations

import json
import time
import uuid
from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.integrations.lead_sync_emitter import (
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    LeadSyncEmitter,
)
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.outbox import EventOutbox, OutboxStatus

# A row is retried up to this many times (i.e. this many failed attempts)
# before it moves to DEAD_LETTER and requires a human to requeue it via
# requeue_dead_letter -- never retried forever silently.
MAX_ATTEMPTS = 6
# Exponential backoff: attempt 1's failure schedules a retry
# BACKOFF_BASE_SECONDS out, attempt 2's schedules 2x that, etc, capped at
# MAX_BACKOFF_SECONDS so a long losing streak doesn't push next_attempt_at
# absurdly far into the future.
BACKOFF_BASE_SECONDS = 60
MAX_BACKOFF_SECONDS = 3600


def _backoff_seconds(attempt_count: int) -> float:
    return min(BACKOFF_BASE_SECONDS * (2 ** (attempt_count - 1)), MAX_BACKOFF_SECONDS)


async def enqueue_and_attempt_delivery(
    session: AsyncSession,
    emitter: LeadSyncEmitter,
    institution: CanonicalInstitution,
    branches: list[Branch],
    contact_points: list[ContactPoint],
) -> EventOutbox | None:
    """
    Builds the envelope once (via the emitter's own filtering/payload
    helpers), persists it as a PENDING row keyed by the envelope's own
    eventId, and attempts delivery immediately -- so the common case
    (Core reachable) still delivers synchronously like it always did, with
    the outbox row as a safety net rather than an added round trip.

    No-ops (returns None) when lead_sync is disabled/unconfigured, mirroring
    emit_institution_upserted's own no-op -- an outbox row for a sync that
    will never be attempted would just accumulate forever.
    """
    if not emitter.settings.lead_sync_enabled or not emitter.settings.lead_sync_webhook_url:
        return None

    supported_contacts = emitter._filter_supported_contacts(institution.id, contact_points)
    payload = emitter._build_payload(institution, branches, supported_contacts)

    row = EventOutbox(
        id=uuid.UUID(payload["eventId"]),
        institution_id=institution.id,
        event_type=payload["eventType"],
        payload=payload,
        status=OutboxStatus.PENDING,
        next_attempt_at=datetime.now(UTC),
    )
    session.add(row)
    await session.flush()

    await _attempt_delivery(session, emitter, row)
    return row


async def _attempt_delivery(
    session: AsyncSession, emitter: LeadSyncEmitter, row: EventOutbox
) -> None:
    """
    POSTs row.payload exactly as it was originally built -- never rebuilt,
    so every retry of this row delivers the identical body/eventId the
    first attempt did. Catches any Exception (broader than the emitter's
    own httpx.HTTPError-only catch): a durable retry system's job is "any
    failure means retry later", whereas the emitter only needs to swallow
    enough to never break its caller's write path.
    """
    body = json.dumps(row.payload, separators=(",", ":"))
    timestamp = str(int(time.time()))
    signature = emitter._sign(timestamp, body)

    row.attempt_count += 1
    try:
        async with httpx.AsyncClient(
            timeout=emitter.settings.lead_sync_webhook_timeout_seconds
        ) as client:
            response = await client.post(
                emitter.settings.lead_sync_webhook_url,
                content=body,
                headers={
                    "Content-Type": "application/json",
                    TIMESTAMP_HEADER: timestamp,
                    SIGNATURE_HEADER: signature,
                },
            )
            response.raise_for_status()
    except Exception as e:
        row.last_error = str(e)[:2000]
        if row.attempt_count >= MAX_ATTEMPTS:
            row.status = OutboxStatus.DEAD_LETTER
        else:
            row.status = OutboxStatus.PENDING
            row.next_attempt_at = datetime.now(UTC) + timedelta(
                seconds=_backoff_seconds(row.attempt_count)
            )
        await session.flush()
        return

    row.status = OutboxStatus.DELIVERED
    row.delivered_at = datetime.now(UTC)
    row.last_error = None
    await session.flush()


async def process_pending_deliveries(
    session: AsyncSession, emitter: LeadSyncEmitter, *, limit: int = 50
) -> int:
    """
    Claims up to `limit` PENDING rows whose next_attempt_at has passed via
    SELECT ... FOR UPDATE SKIP LOCKED -- the same claiming pattern used by
    every other "atomically grab pending work" query in this codebase
    (services/daily_selection_service.py's select_daily_batch,
    pipeline.py's _retry_stranded_records), so two overlapping calls (e.g.
    a scheduled retry sweep overlapping a manual one) never both attempt
    the same row. Each row's attempt runs inside its own savepoint so one
    row's DB-level failure can't corrupt the whole batch (see
    docs/CODE_REVIEW_LESSONS.md pattern 3) -- _attempt_delivery itself
    already swallows HTTP-level failures, but this guards against any
    unexpected DB-level error while updating a row's status.
    """
    now = datetime.now(UTC)
    stmt = (
        select(EventOutbox)
        .where(EventOutbox.status == OutboxStatus.PENDING)
        .where(EventOutbox.next_attempt_at <= now)
        .order_by(EventOutbox.next_attempt_at.asc())
        .limit(limit)
        .with_for_update(skip_locked=True)
    )
    rows = list(await session.scalars(stmt))
    processed = 0
    for row in rows:
        try:
            async with session.begin_nested():
                await _attempt_delivery(session, emitter, row)
            processed += 1
        except Exception as e:
            print(f"outbox: delivery attempt for event {row.id} raised unexpectedly: {e}")
    return processed


async def list_outbox_entries(
    session: AsyncSession, *, status: OutboxStatus | None = None, limit: int = 100
) -> list[EventOutbox]:
    stmt = select(EventOutbox).order_by(EventOutbox.created_at.desc()).limit(limit)
    if status is not None:
        stmt = stmt.where(EventOutbox.status == status)
    return list(await session.scalars(stmt))


async def requeue_dead_letter(session: AsyncSession, outbox_id: uuid.UUID) -> EventOutbox:
    """
    Manually moves a DEAD_LETTER row back to PENDING for another attempt --
    e.g. once a human has confirmed the downstream outage that exhausted
    MAX_ATTEMPTS is resolved. Requires an explicit call (never automatic):
    DEAD_LETTER exists to surface "this needs a human", not to be retried
    forever silently.
    """
    row = await session.get(EventOutbox, outbox_id)
    if row is None:
        raise ResourceNotFoundError(str(outbox_id))
    if row.status != OutboxStatus.DEAD_LETTER:
        raise ValueError(f"Outbox entry {outbox_id} is {row.status.value}, not dead_letter.")
    row.status = OutboxStatus.PENDING
    row.attempt_count = 0
    row.next_attempt_at = datetime.now(UTC)
    row.last_error = None
    await session.flush()
    return row
