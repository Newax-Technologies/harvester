import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint


@pytest.mark.asyncio
async def test_create_and_list_suppression(client_a):
    response = await client_a.post(
        "/api/v1/compliance/suppressions",
        json={"contact_value": "Jane@Example.com", "reason": "opt_out", "note": "unsubscribed"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["normalized_contact_value"] == "jane@example.com"
    assert body["reason"] == "opt_out"

    listed = await client_a.get("/api/v1/compliance/suppressions")
    assert len(listed.json()) == 1


@pytest.mark.asyncio
async def test_delete_suppression_removes_it(client_a):
    created = await client_a.post(
        "/api/v1/compliance/suppressions",
        json={"contact_value": "jane@example.com", "reason": "manual"},
    )
    suppression_id = created.json()["id"]

    response = await client_a.delete(f"/api/v1/compliance/suppressions/{suppression_id}")

    assert response.status_code == 204
    listed = await client_a.get("/api/v1/compliance/suppressions")
    assert listed.json() == []


@pytest.mark.asyncio
async def test_create_deletion_request_does_not_delete_anything(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="API Deletion Test School")
    db_session.add(institution)
    await db_session.commit()

    response = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={
            "subject_type": "institution",
            "subject_id": str(institution.id),
            "note": "GDPR request",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    remaining = await db_session.get(CanonicalInstitution, institution.id)
    assert remaining is not None


@pytest.mark.asyncio
async def test_fulfill_deletion_request_deletes_the_institution(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="API Fulfill Test School")
    db_session.add(institution)
    await db_session.commit()

    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]

    response = await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    remaining = await db_session.get(CanonicalInstitution, institution.id)
    assert remaining is None


@pytest.mark.asyncio
async def test_reject_deletion_request(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="API Reject Test School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]

    response = await client_a.post(
        f"/api/v1/compliance/deletion-requests/{request_id}/reject",
        json={"reason": "insufficient verification"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"
    assert body["rejection_reason"] == "insufficient verification"


@pytest.mark.asyncio
async def test_fulfill_unknown_deletion_request_404s(client_a):
    response = await client_a.post(f"/api/v1/compliance/deletion-requests/{uuid.uuid4()}/fulfill")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_fulfill_already_fulfilled_request_returns_400(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="API Double Fulfill School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]
    await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    response = await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_deletion_requests_filters_by_status(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="API Filter Test School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]
    await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    pending = await client_a.get(
        "/api/v1/compliance/deletion-requests", params={"status": "pending"}
    )
    completed = await client_a.get(
        "/api/v1/compliance/deletion-requests", params={"status": "completed"}
    )

    assert pending.json() == []
    assert len(completed.json()) == 1


@pytest.mark.asyncio
async def test_fulfill_contact_deletion_schedules_resync_only_after_commit(
    client_a, db_session, monkeypatch
):
    # Correction regression test: compliance_service.py's
    # _resync_institution_id_if_eligible deliberately only determines
    # eligibility (no delivery attempt) inside fulfill_deletion's own
    # transaction -- this route is the one that must actually schedule
    # the resync, as a background task, AFTER session.commit() above it,
    # mirroring services/resolution_service.py::make_decision's identical
    # pattern for the same "don't let a downstream system observe this
    # change before it's durable, and don't deliver it on a
    # transaction that could still roll back" reason.
    from lead_harvester.config import settings as app_settings

    monkeypatch.setattr(app_settings, "lead_sync_enabled", True)
    monkeypatch.setattr(app_settings, "lead_sync_webhook_url", "https://core-newax.test/webhook")

    institution = CanonicalInstitution(
        canonical_name="API Resync Contact School", lead_synced_at=datetime.now(UTC)
    )
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="erase-me@example.com"
    )
    db_session.add(contact)
    await db_session.commit()
    contact_id = contact.id
    institution_id = institution.id

    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "contact_point", "subject_id": str(contact_id)},
    )
    request_id = created.json()["id"]

    with patch(
        "lead_harvester.api.routes.compliance.resync_institution",
        new=AsyncMock(),
    ) as mock_resync:
        response = await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 200
    assert response.json()["manifest"]["downstream_resync_enqueued"] is True
    mock_resync.assert_awaited_once()
    args, _ = mock_resync.call_args
    _emitter, resynced_institution_id = args
    assert resynced_institution_id == institution_id


@pytest.mark.asyncio
async def test_fulfill_contact_deletion_against_never_synced_institution_skips_resync(
    client_a, db_session
):
    institution = CanonicalInstitution(canonical_name="API Never Synced Contact School")
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.commit()
    contact_id = contact.id

    created = await client_a.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "contact_point", "subject_id": str(contact_id)},
    )
    request_id = created.json()["id"]

    with patch(
        "lead_harvester.api.routes.compliance.resync_institution",
        new=AsyncMock(),
    ) as mock_resync:
        response = await client_a.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 200
    assert response.json()["manifest"]["downstream_resync_enqueued"] is False
    mock_resync.assert_not_awaited()
