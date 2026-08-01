import uuid

import pytest

from lead_harvester.models.canonical import CanonicalInstitution


@pytest.mark.asyncio
async def test_create_and_list_suppression(client_admin):
    response = await client_admin.post(
        "/api/v1/compliance/suppressions",
        json={"contact_value": "Jane@Example.com", "reason": "opt_out", "note": "unsubscribed"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["normalized_contact_value"] == "jane@example.com"
    assert body["reason"] == "opt_out"

    listed = await client_admin.get("/api/v1/compliance/suppressions")
    assert len(listed.json()) == 1


@pytest.mark.asyncio
async def test_delete_suppression_removes_it(client_admin):
    created = await client_admin.post(
        "/api/v1/compliance/suppressions",
        json={"contact_value": "jane@example.com", "reason": "manual"},
    )
    suppression_id = created.json()["id"]

    response = await client_admin.delete(f"/api/v1/compliance/suppressions/{suppression_id}")

    assert response.status_code == 204
    listed = await client_admin.get("/api/v1/compliance/suppressions")
    assert listed.json() == []


@pytest.mark.asyncio
async def test_create_deletion_request_does_not_delete_anything(client_admin, db_session):
    institution = CanonicalInstitution(canonical_name="API Deletion Test School")
    db_session.add(institution)
    await db_session.commit()

    response = await client_admin.post(
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
async def test_fulfill_deletion_request_deletes_the_institution(client_admin, db_session):
    institution = CanonicalInstitution(canonical_name="API Fulfill Test School")
    db_session.add(institution)
    await db_session.commit()

    created = await client_admin.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]

    response = await client_admin.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    remaining = await db_session.get(CanonicalInstitution, institution.id)
    assert remaining is None


@pytest.mark.asyncio
async def test_reject_deletion_request(client_admin, db_session):
    institution = CanonicalInstitution(canonical_name="API Reject Test School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_admin.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]

    response = await client_admin.post(
        f"/api/v1/compliance/deletion-requests/{request_id}/reject",
        json={"reason": "insufficient verification"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"
    assert body["rejection_reason"] == "insufficient verification"


@pytest.mark.asyncio
async def test_fulfill_unknown_deletion_request_404s(client_admin):
    response = await client_admin.post(
        f"/api/v1/compliance/deletion-requests/{uuid.uuid4()}/fulfill"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_fulfill_already_fulfilled_request_returns_400(client_admin, db_session):
    institution = CanonicalInstitution(canonical_name="API Double Fulfill School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_admin.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]
    await client_admin.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    response = await client_admin.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_deletion_requests_filters_by_status(client_admin, db_session):
    institution = CanonicalInstitution(canonical_name="API Filter Test School")
    db_session.add(institution)
    await db_session.commit()
    created = await client_admin.post(
        "/api/v1/compliance/deletion-requests",
        json={"subject_type": "institution", "subject_id": str(institution.id)},
    )
    request_id = created.json()["id"]
    await client_admin.post(f"/api/v1/compliance/deletion-requests/{request_id}/fulfill")

    pending = await client_admin.get(
        "/api/v1/compliance/deletion-requests", params={"status": "pending"}
    )
    completed = await client_admin.get(
        "/api/v1/compliance/deletion-requests", params={"status": "completed"}
    )

    assert pending.json() == []
    assert len(completed.json()) == 1


@pytest.mark.asyncio
async def test_list_suppressions_permitted_for_compliance_read_only_role(client_a):
    # client_a's "reviewer" role holds compliance.read (see
    # api/permissions.py's ROLE_PERMISSIONS) -- reads should succeed even
    # without compliance.manage/deletions.fulfil.
    response = await client_a.get("/api/v1/compliance/suppressions")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_suppression_requires_compliance_manage_permission(client_a):
    response = await client_a.post(
        "/api/v1/compliance/suppressions",
        json={"contact_value": "jane@example.com", "reason": "manual"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_fulfill_deletion_request_requires_deletions_fulfil_permission(client_a):
    # A reviewer holds compliance.read but not compliance.manage or
    # deletions.fulfil -- fulfilling (the one irreversible action) is
    # gated on the separate deletions.fulfil permission specifically.
    response = await client_a.post(f"/api/v1/compliance/deletion-requests/{uuid.uuid4()}/fulfill")
    assert response.status_code == 403
