import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import get_lead_sync_emitter
from lead_harvester.config import Settings
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.outbox import EventOutbox, OutboxStatus


def _enabled_settings() -> Settings:
    return Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_url="https://core-newax.test/api/integrations/lead-harvester/webhook",
        lead_sync_webhook_secret="test-secret-with-more-than-32-characters",
    )


@pytest.fixture
def mock_webhook_post():
    # client_admin is ITSELF an httpx.AsyncClient (over ASGITransport) -- see
    # tests/api/test_manual_leads.py's identical fixture for why a blanket
    # AsyncClient.post patch would also break the test client's own request.
    original_post = httpx.AsyncClient.post
    mock_response = httpx.Response(
        200,
        request=httpx.Request(
            "POST", "https://core-newax.test/api/integrations/lead-harvester/webhook"
        ),
    )
    mock_post = AsyncMock(return_value=mock_response)

    async def dispatch(self, url, *args, **kwargs):
        if str(url).startswith("https://core-newax.test/"):
            return await mock_post(url, *args, **kwargs)
        return await original_post(self, url, *args, **kwargs)

    with patch.object(httpx.AsyncClient, "post", new=dispatch):
        yield mock_post


@pytest.fixture
def override_lead_sync_emitter():
    emitter = LeadSyncEmitter(_enabled_settings())
    app.dependency_overrides[get_lead_sync_emitter] = lambda: emitter
    yield emitter
    app.dependency_overrides.pop(get_lead_sync_emitter, None)


async def _seed_pending_row(db_session, *, due: bool = True) -> EventOutbox:
    institution = CanonicalInstitution(
        canonical_name=f"Outbox API School {uuid.uuid4().hex[:8]}",
        status=OperatingStatus.OPERATIONAL,
    )
    db_session.add(institution)
    await db_session.flush()
    row = EventOutbox(
        institution_id=institution.id,
        event_type="institution.upserted",
        payload={
            "schemaVersion": 1,
            "eventId": str(uuid.uuid4()),
            "eventType": "institution.upserted",
            "occurredAt": datetime.now(UTC).isoformat(),
            "institution": {"id": str(institution.id)},
            "branches": [],
            "contactPoints": [],
        },
        status=OutboxStatus.PENDING,
        next_attempt_at=(
            datetime.now(UTC) - timedelta(seconds=1)
            if due
            else datetime.now(UTC) + timedelta(hours=1)
        ),
    )
    db_session.add(row)
    await db_session.flush()
    return row


@pytest.mark.asyncio
async def test_list_outbox_entries_returns_seeded_rows(client_admin, db_session):
    row = await _seed_pending_row(db_session)
    await db_session.commit()

    response = await client_admin.get("/api/v1/outbox")

    assert response.status_code == 200
    body = response.json()
    assert [e["id"] for e in body] == [str(row.id)]
    assert body[0]["status"] == "pending"


@pytest.mark.asyncio
async def test_list_outbox_entries_filters_by_status(client_admin, db_session):
    await _seed_pending_row(db_session)
    await db_session.commit()

    delivered = await client_admin.get("/api/v1/outbox", params={"status": "delivered"})
    pending = await client_admin.get("/api/v1/outbox", params={"status": "pending"})

    assert delivered.json() == []
    assert len(pending.json()) == 1


@pytest.mark.asyncio
async def test_process_pending_deliveries_route_delivers_due_rows(
    client_admin, db_session, mock_webhook_post, override_lead_sync_emitter
):
    due_row = await _seed_pending_row(db_session, due=True)
    future_row = await _seed_pending_row(db_session, due=False)
    await db_session.commit()

    response = await client_admin.post("/api/v1/outbox/process")

    assert response.status_code == 200
    assert response.json()["processed"] == 1
    mock_webhook_post.assert_awaited_once()

    await db_session.refresh(due_row)
    await db_session.refresh(future_row)
    assert due_row.status == OutboxStatus.DELIVERED
    assert future_row.status == OutboxStatus.PENDING


@pytest.mark.asyncio
async def test_requeue_dead_letter_route_resets_row(client_admin, db_session):
    row = await _seed_pending_row(db_session)
    row.status = OutboxStatus.DEAD_LETTER
    row.attempt_count = 6
    row.last_error = "boom"
    await db_session.commit()

    response = await client_admin.post(f"/api/v1/outbox/{row.id}/requeue")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "pending"
    assert body["attempt_count"] == 0
    assert body["last_error"] is None


@pytest.mark.asyncio
async def test_requeue_dead_letter_route_404s_for_unknown_id(client_admin):
    response = await client_admin.post(f"/api/v1/outbox/{uuid.uuid4()}/requeue")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_requeue_dead_letter_route_400s_for_non_dead_letter_row(client_admin, db_session):
    row = await _seed_pending_row(db_session)
    await db_session.commit()

    response = await client_admin.post(f"/api/v1/outbox/{row.id}/requeue")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_outbox_entries_requires_outbox_manage_permission(client_a):
    # client_a's "reviewer" role does not hold outbox.manage (see
    # api/permissions.py's ROLE_PERMISSIONS).
    response = await client_a.get("/api/v1/outbox")
    assert response.status_code == 403
