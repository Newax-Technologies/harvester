import uuid
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
)
from lead_harvester.canonical.merger import (
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
)
from lead_harvester.database import engine as manual_leads_engine
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.source import RawSourceRecord
from lead_harvester.resolution.normalize import normalize_domain, normalize_phone

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
    # gives each test its own event loop, and importing lead_harvester.database
    # (even though this route no longer uses its engine directly) is enough to
    # create that binding, so it must be disposed between tests or the next
    # test's loop can't reuse it ("Future attached to a different loop"). This
    # is the standard SQLAlchemy-recommended workaround for that exact error.
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
async def test_create_manual_lead_rejects_non_alpha_country_code(manual_leads_client):
    payload = {**VALID_PAYLOAD, "country_code": "1!"}
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_manual_lead_rejects_country_code_that_expands_when_uppercased(
    manual_leads_client,
):
    # "ß".upper() == "SS", so a naive length check on the raw 2-char value
    # would let a 3-character result slip past validation.
    payload = {**VALID_PAYLOAD, "country_code": "ßa"}
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
async def test_create_manual_lead_preserves_country_code_in_raw_payload(
    manual_leads_client, db_session
):
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(
                RawSourceRecord.normalized_name == VALID_PAYLOAD["institution_name"].lower()
            )
        )
    ).scalar_one()
    assert record.raw_payload["country_code"] == "PK"


@pytest.mark.asyncio
async def test_create_manual_lead_normalizes_phone_and_domain_with_shared_helpers(
    manual_leads_client, db_session
):
    # Manual entries must use the same normalize_phone/normalize_domain
    # helpers as every other ingestion path -- otherwise the resolution
    # blocker's exact-string comparisons can never match a manual entry
    # against a later scraped record for the same institution, since a
    # formatted phone ("+92 300 1234567") or a "www."-prefixed domain won't
    # equal the stripped forms scraped records already use.
    payload = {
        **VALID_PAYLOAD,
        "institution_name": "Normalization Test School",
        "website": "https://www.normtest.example.edu/contact-us",
        "contacts": [
            {
                "contact_type": "phone",
                "contact_value": "+92 300 111 2222",
                "person_name": "Test Person",
                "role": "Admin",
            }
        ],
    }
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 201

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(
                RawSourceRecord.normalized_name == "normalization test school"
            )
        )
    ).scalar_one()

    assert record.normalized_phone == normalize_phone("+92 300 111 2222")
    assert record.normalized_domain == normalize_domain(payload["website"])
    # Sanity: the raw, unnormalized value must actually differ from the
    # normalized one, or this test wouldn't be exercising anything.
    assert record.normalized_phone != "+92 300 111 2222"
    assert record.normalized_domain != payload["website"]


@pytest.mark.asyncio
async def test_create_manual_lead_normalizes_national_format_phone_to_e164(
    manual_leads_client, db_session
):
    # A manual lead's phone entered in bare national format ("0300
    # 1234567", how Pakistani mobile numbers are commonly written)
    # previously normalized to "03001234567", while the same physical
    # number from a Google Places record (which supplies an
    # internationalPhoneNumber like "+92 300 1234567") normalized to
    # "+923001234567" -- two different strings for one real phone number,
    # silently breaking exact-match phone blocking between them. Using
    # payload.country_code as phonenumbers' region hint makes both forms
    # converge on the same E.164 value.
    payload = {
        **VALID_PAYLOAD,
        "institution_name": "National Format Test School",
        "country_code": "pk",
        "contacts": [
            {
                "contact_type": "phone",
                "contact_value": "0300 1234567",
                "person_name": "Test Person",
                "role": "Admin",
            }
        ],
    }
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 201

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(
                RawSourceRecord.normalized_name == "national format test school"
            )
        )
    ).scalar_one()

    assert record.normalized_phone == normalize_phone("+92 300 1234567")
    assert record.normalized_phone == "+923001234567"


@pytest.mark.asyncio
async def test_create_manual_lead_normalizes_contact_type_casing(
    manual_leads_client, db_session, fake_emitter
):
    # contact_type is compared exact-match against "phone" (this route's own
    # normalized_phone extraction, ContactPoint value normalization) and
    # against LeadSyncEmitter.SUPPORTED_CONTACT_TYPES -- a caller sending
    # "Phone" instead of "phone" must not silently fail every one of those
    # comparisons.
    payload = {
        **VALID_PAYLOAD,
        "institution_name": "Casing Test School",
        "contacts": [
            {
                "contact_type": "Phone",
                "contact_value": "+92 300 111 2222",
                "person_name": "Test Person",
                "role": "Admin",
            }
        ],
    }
    response = await manual_leads_client.post("/api/v1/leads/manual", json=payload)
    assert response.status_code == 201

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(RawSourceRecord.normalized_name == "casing test school")
        )
    ).scalar_one()
    assert record.normalized_phone == normalize_phone("+92 300 111 2222")

    args, _ = fake_emitter.emit_institution_upserted.call_args
    _, _, contact_points = args
    assert contact_points[0].contact_type == "phone"


@pytest.mark.asyncio
async def test_create_manual_lead_writes_branch_membership_provenance(
    manual_leads_client, db_session
):
    # Without this link, a later scraped record matching this manual entry
    # as a resolution candidate could never discover that it's already
    # canonicalized, and would create a duplicate institution instead of
    # attaching to this one.
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201
    institution_id = response.json()["id"]

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(
                RawSourceRecord.normalized_name == VALID_PAYLOAD["institution_name"].lower()
            )
        )
    ).scalar_one()

    canonical_id = await find_canonical_for_raw_record(db_session, record.id)
    assert str(canonical_id) == institution_id


@pytest.mark.asyncio
async def test_create_manual_lead_stores_provider_ids_in_resolver_canonical_shape(
    manual_leads_client, db_session
):
    # provider_ids must be keyed by source_type with a list of source_ids --
    # the shape canonical/merger.py's find_branch_for_raw_record actually
    # reads. A different key (e.g. "manual_record_id") or a bare scalar
    # would mean a later reviewer decision that targets this manual record
    # could never find this branch, creating an erroneous "Additional
    # Campus" instead of enriching it.
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201
    institution_id = response.json()["id"]

    record = (
        await db_session.execute(
            select(RawSourceRecord).where(
                RawSourceRecord.normalized_name == VALID_PAYLOAD["institution_name"].lower()
            )
        )
    ).scalar_one()

    branch = (
        await db_session.execute(
            select(Branch).where(Branch.institution_id == uuid.UUID(institution_id))
        )
    ).scalar_one()
    assert branch.provider_ids == {"manual": [record.source_id]}

    institution = await db_session.get(CanonicalInstitution, uuid.UUID(institution_id))
    found = await find_branch_for_raw_record(db_session, institution.id, record)
    assert found is not None
    assert found.id == branch.id


@pytest.mark.asyncio
async def test_create_manual_lead_creates_a_lead_profile(manual_leads_client, db_session):
    response = await manual_leads_client.post("/api/v1/leads/manual", json=VALID_PAYLOAD)
    assert response.status_code == 201
    institution_id = response.json()["id"]

    profile = (
        await db_session.execute(
            select(LeadProfile).where(LeadProfile.institution_id == uuid.UUID(institution_id))
        )
    ).scalar_one_or_none()
    assert profile is not None
    assert profile.has_phone is True


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
