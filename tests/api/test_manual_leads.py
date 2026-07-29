from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
)
from lead_harvester.database import engine as manual_leads_engine
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import ContactPoint

# NOTE: create_manual_lead's DB access goes through database.get_session()
# directly rather than the get_db_session FastAPI dependency (unlike every
# other route in this app), so overriding get_db_session here has no effect
# on what this route actually writes to -- it always talks to the real
# configured database (settings.database_url), not an injectable test
# session. That's a pre-existing quirk of this route, not something this
# change introduces. Because of that, these tests verify persistence via the
# objects the route actually passed to the emitter (which are the same
# objects it just committed) rather than querying a session that never sees
# this route's writes.


VALID_PAYLOAD = {
    "institution_name": "Riverside Academy",
    "institution_type": "school",
    "website": "https://riverside.example.edu",
    "operating_status": "operational",
    "address": "12 River Road",
    "city": "Lahore",
    "country": "Pakistan",
    "country_code": "pk",
    "contacts": [
        {
            "contact_type": "phone",
            "contact_value": "+923001234567",
            "person_name": "Ayesha Malik",
            "role": "Admissions Officer",
        }
    ],
}


@pytest_asyncio.fixture(autouse=True)
async def dispose_manual_leads_engine():
    # database.engine is a module-level engine created once at import time and
    # bound to whatever event loop first used it. pytest-asyncio (strict mode)
    # gives each test its own event loop, and this route -- unlike every other
    # one in this app -- talks to that global engine directly rather than
    # through an injectable session (see the note above), so its pooled
    # connections must be disposed between tests or the next test's loop
    # can't reuse them ("Future attached to a different loop"). This is the
    # standard SQLAlchemy-recommended workaround for that exact error.
    yield
    await manual_leads_engine.dispose()


@pytest.fixture
def fake_emitter():
    emitter = AsyncMock(spec=LeadSyncEmitter)
    return emitter


@pytest.fixture
def override_manual_lead_dependencies(db_session, fake_emitter):
    async def get_test_session():
        yield db_session

    app.dependency_overrides[get_db_session] = get_test_session
    app.dependency_overrides[get_lead_sync_emitter] = lambda: fake_emitter
    app.dependency_overrides[get_current_user] = lambda: User(
        id="usr_test", username="test-user", role="admin"
    )
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def manual_leads_client(override_manual_lead_dependencies):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_manual_lead_persists_and_normalizes_country_code(
    manual_leads_client, fake_emitter
):
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["institution_name"] == "Riverside Academy"
    assert body["contacts_saved"] == 1

    args, _ = fake_emitter.emit_institution_upserted.call_args
    _, branches, _ = args
    assert branches[0].city == "Lahore"
    assert branches[0].country_code == "PK"  # normalized to uppercase


@pytest.mark.asyncio
async def test_create_manual_lead_rejects_missing_city(manual_leads_client):
    payload = {**VALID_PAYLOAD, "city": ""}
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_manual_lead_rejects_whitespace_only_city(manual_leads_client):
    payload = {**VALID_PAYLOAD, "city": "   "}
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_manual_lead_rejects_invalid_country_code(manual_leads_client):
    payload = {**VALID_PAYLOAD, "country_code": "PAK"}
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_manual_lead_invokes_emitter_after_commit(manual_leads_client, fake_emitter):
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201

    fake_emitter.emit_institution_upserted.assert_awaited_once()
    args, _ = fake_emitter.emit_institution_upserted.call_args
    institution, branches, contact_points = args

    assert institution.canonical_name == "Riverside Academy"
    assert len(branches) == 1
    assert branches[0].city == "Lahore"
    assert len(contact_points) == 1
    assert isinstance(contact_points[0], ContactPoint)
    assert contact_points[0].person_name == "Ayesha Malik"


@pytest.mark.asyncio
async def test_create_manual_lead_does_not_fail_when_emitter_raises(
    manual_leads_client, fake_emitter
):
    # The emitter's own contract is "never raise" (it swallows delivery
    # failures internally) -- but this endpoint's "a webhook problem never
    # fails a lead submission" guarantee shouldn't depend on trusting that.
    # Force a raise here (e.g. a bug in the emitter, or an unexpected error
    # like a signing failure) and confirm the route still succeeds.
    fake_emitter.emit_institution_upserted.side_effect = RuntimeError("boom")
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201
