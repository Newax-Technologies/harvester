import hashlib
import hmac
import json
import uuid
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from lead_harvester.config import Settings
from lead_harvester.integrations.lead_sync_emitter import (
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    LeadSyncEmitter,
)
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)


def _settings(**overrides) -> Settings:
    defaults = {
        "lead_sync_enabled": True,
        "lead_sync_webhook_url": "https://core-newax.test/api/integrations/lead-harvester/webhook",
        "lead_sync_webhook_secret": "test-secret-with-more-than-32-characters",
        "lead_sync_webhook_timeout_seconds": 5.0,
    }
    defaults.update(overrides)
    return Settings(**defaults)


def _institution() -> CanonicalInstitution:
    return CanonicalInstitution(
        id=uuid.uuid4(),
        canonical_name="Test School",
        institution_type="school",
        domain="test-school.edu",
        website="https://test-school.edu",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=0.9,
    )


def _branch(institution_id: uuid.UUID) -> Branch:
    return Branch(
        id=uuid.uuid4(),
        institution_id=institution_id,
        branch_name="Main Campus",
        address="123 Main St",
        city="Lahore",
        country_code="PK",
        provider_ids={},
    )


def _contact(institution_id: uuid.UUID) -> ContactPoint:
    return ContactPoint(
        id=uuid.uuid4(),
        institution_id=institution_id,
        contact_type="phone",
        contact_value="+923001234567",
        person_name="Ali Khan",
        role="Principal",
        is_publicly_listed=False,
    )


@pytest.mark.asyncio
async def test_noop_when_disabled():
    settings = _settings(lead_sync_enabled=False)
    emitter = LeadSyncEmitter(settings)
    institution = _institution()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await emitter.emit_institution_upserted(institution, [], [])

    mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_noop_when_url_not_configured():
    # Settings itself now refuses to construct with lead_sync_enabled=True
    # and an empty URL (see test_config.py), so this exercises the emitter's
    # own belt-and-suspenders check directly by mutating a validly-constructed
    # Settings instance after the fact (model_validator only runs at
    # construction time, not on attribute assignment).
    settings = _settings()
    settings.lead_sync_webhook_url = ""
    emitter = LeadSyncEmitter(settings)
    institution = _institution()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await emitter.emit_institution_upserted(institution, [], [])

    mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_sends_correctly_signed_payload():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution = _institution()
    branch = _branch(institution.id)
    contact = _contact(institution.id)

    mock_response = httpx.Response(
        200, request=httpx.Request("POST", settings.lead_sync_webhook_url)
    )
    with patch(
        "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
    ) as mock_post:
        await emitter.emit_institution_upserted(institution, [branch], [contact])

    mock_post.assert_awaited_once()
    args, kwargs = mock_post.call_args
    assert args[0] == settings.lead_sync_webhook_url

    body = kwargs["content"]
    payload = json.loads(body)
    assert payload["schemaVersion"] == 1
    assert payload["eventType"] == "institution.upserted"
    assert uuid.UUID(payload["eventId"])
    assert payload["institution"]["id"] == str(institution.id)
    assert payload["institution"]["status"] == "operational"
    assert payload["branches"] == [
        {
            "id": str(branch.id),
            "branchName": "Main Campus",
            "address": "123 Main St",
            "city": "Lahore",
            "countryCode": "PK",
        }
    ]
    assert payload["contactPoints"][0]["personName"] == "Ali Khan"

    timestamp = kwargs["headers"][TIMESTAMP_HEADER]
    signature = kwargs["headers"][SIGNATURE_HEADER]
    expected_signature = hmac.new(
        settings.lead_sync_webhook_secret.encode(),
        f"{timestamp}.{body}".encode(),
        hashlib.sha256,
    ).hexdigest()
    assert signature == expected_signature


@pytest.mark.asyncio
async def test_swallows_http_errors_without_raising():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution = _institution()

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        await emitter.emit_institution_upserted(institution, [], [])  # must not raise


@pytest.mark.asyncio
async def test_swallows_non_2xx_responses_without_raising():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution = _institution()

    request = httpx.Request("POST", settings.lead_sync_webhook_url)
    error_response = httpx.Response(500, request=request)
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=error_response):
        await emitter.emit_institution_upserted(institution, [], [])  # must not raise


@pytest.mark.asyncio
async def test_filters_unsupported_contact_types_before_delivery():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution = _institution()
    supported = _contact(institution.id)
    unsupported = ContactPoint(
        id=uuid.uuid4(),
        institution_id=institution.id,
        contact_type="linkedin",
        contact_value="https://linkedin.com/in/example",
        is_publicly_listed=True,
    )

    mock_response = httpx.Response(
        200, request=httpx.Request("POST", settings.lead_sync_webhook_url)
    )
    with patch(
        "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
    ) as mock_post:
        await emitter.emit_institution_upserted(institution, [], [supported, unsupported])

    body = mock_post.call_args.kwargs["content"]
    payload = json.loads(body)
    assert [c["id"] for c in payload["contactPoints"]] == [str(supported.id)]


@pytest.mark.asyncio
async def test_emit_contact_point_deleted_noops_when_disabled():
    settings = _settings(lead_sync_enabled=False)
    emitter = LeadSyncEmitter(settings)

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await emitter.emit_contact_point_deleted(uuid.uuid4(), uuid.uuid4())

    mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_emit_contact_point_deleted_sends_signed_payload():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution_id = uuid.uuid4()
    contact_point_id = uuid.uuid4()

    mock_response = httpx.Response(
        200, request=httpx.Request("POST", settings.lead_sync_webhook_url)
    )
    with patch(
        "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
    ) as mock_post:
        await emitter.emit_contact_point_deleted(institution_id, contact_point_id)

    mock_post.assert_awaited_once()
    args, kwargs = mock_post.call_args
    assert args[0] == settings.lead_sync_webhook_url

    body = kwargs["content"]
    payload = json.loads(body)
    assert payload["schemaVersion"] == 1
    assert payload["eventType"] == "contact_point.deleted"
    assert uuid.UUID(payload["eventId"])
    assert payload["institutionId"] == str(institution_id)
    assert payload["contactPointId"] == str(contact_point_id)

    timestamp = kwargs["headers"][TIMESTAMP_HEADER]
    signature = kwargs["headers"][SIGNATURE_HEADER]
    expected_signature = hmac.new(
        settings.lead_sync_webhook_secret.encode(),
        f"{timestamp}.{body}".encode(),
        hashlib.sha256,
    ).hexdigest()
    assert signature == expected_signature


@pytest.mark.asyncio
async def test_emit_contact_point_deleted_swallows_http_errors():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        await emitter.emit_contact_point_deleted(uuid.uuid4(), uuid.uuid4())  # must not raise


@pytest.mark.asyncio
async def test_emit_institution_deleted_noops_when_disabled():
    settings = _settings(lead_sync_enabled=False)
    emitter = LeadSyncEmitter(settings)

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await emitter.emit_institution_deleted(uuid.uuid4())

    mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_emit_institution_deleted_sends_signed_payload():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)
    institution_id = uuid.uuid4()

    mock_response = httpx.Response(
        200, request=httpx.Request("POST", settings.lead_sync_webhook_url)
    )
    with patch(
        "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
    ) as mock_post:
        await emitter.emit_institution_deleted(institution_id)

    body = mock_post.call_args.kwargs["content"]
    payload = json.loads(body)
    assert payload["eventType"] == "institution.deleted"
    assert payload["institutionId"] == str(institution_id)
    assert "contactPointId" not in payload


@pytest.mark.asyncio
async def test_emit_institution_deleted_swallows_http_errors():
    settings = _settings()
    emitter = LeadSyncEmitter(settings)

    with patch(
        "httpx.AsyncClient.post",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("connection refused"),
    ):
        await emitter.emit_institution_deleted(uuid.uuid4())  # must not raise
