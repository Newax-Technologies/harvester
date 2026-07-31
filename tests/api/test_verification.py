import uuid

import pytest

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType


async def _seed_confidence_drift_institution(
    db_session, *, canonical_name: str = "Riverside Academy"
):
    institution = CanonicalInstitution(canonical_name=canonical_name, confidence_score=10.0)
    db_session.add(institution)
    await db_session.flush()

    for _ in range(2):
        run = SourceRun(
            source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED
        )
        db_session.add(run)
        await db_session.flush()
        record = RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.GOOGLE_PLACES,
            source_id=f"gp:{uuid.uuid4().hex[:8]}",
            raw_payload={},
        )
        db_session.add(record)
        await db_session.flush()
        db_session.add(
            FieldProvenance(
                canonical_id=institution.id,
                raw_record_id=record.id,
                field_name="branch_membership",
                asserted_value=record.source_id,
            )
        )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_trigger_sweep_creates_flags(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()

    response = await client_a.post("/api/v1/verification/sweep", json={})

    assert response.status_code == 200
    assert response.json()["flags_created"] == 1


@pytest.mark.asyncio
async def test_list_flags_returns_created_flags(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()
    await client_a.post("/api/v1/verification/sweep", json={})

    response = await client_a.get("/api/v1/verification/flags")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["flag_type"] == "confidence_drift"
    assert body[0]["status"] == "open"


@pytest.mark.asyncio
async def test_list_flags_filters_by_status(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()
    created = await client_a.post("/api/v1/verification/sweep", json={})
    flags = (await client_a.get("/api/v1/verification/flags")).json()
    flag_id = flags[0]["id"]
    await client_a.post(f"/api/v1/verification/flags/{flag_id}/resolve", json={})

    open_flags = await client_a.get("/api/v1/verification/flags", params={"status": "open"})
    resolved_flags = await client_a.get("/api/v1/verification/flags", params={"status": "resolved"})

    assert open_flags.json() == []
    assert len(resolved_flags.json()) == 1
    assert created.status_code == 200


@pytest.mark.asyncio
async def test_resolve_flag_marks_it_resolved(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()
    await client_a.post("/api/v1/verification/sweep", json={})
    flag_id = (await client_a.get("/api/v1/verification/flags")).json()[0]["id"]

    response = await client_a.post(
        f"/api/v1/verification/flags/{flag_id}/resolve", json={"note": "fixed it"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "resolved"
    assert body["resolution_note"] == "fixed it"


@pytest.mark.asyncio
async def test_dismiss_flag_marks_it_dismissed(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()
    await client_a.post("/api/v1/verification/sweep", json={})
    flag_id = (await client_a.get("/api/v1/verification/flags")).json()[0]["id"]

    response = await client_a.post(f"/api/v1/verification/flags/{flag_id}/dismiss", json={})

    assert response.status_code == 200
    assert response.json()["status"] == "dismissed"


@pytest.mark.asyncio
async def test_resolve_unknown_flag_404s(client_a):
    response = await client_a.post(f"/api/v1/verification/flags/{uuid.uuid4()}/resolve", json={})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_resolve_already_resolved_flag_returns_400(client_a, db_session):
    await _seed_confidence_drift_institution(db_session)
    await db_session.commit()
    await client_a.post("/api/v1/verification/sweep", json={})
    flag_id = (await client_a.get("/api/v1/verification/flags")).json()[0]["id"]
    await client_a.post(f"/api/v1/verification/flags/{flag_id}/resolve", json={})

    response = await client_a.post(f"/api/v1/verification/flags/{flag_id}/resolve", json={})

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_mark_contact_unreachable_creates_a_flag(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="Some School")
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.commit()

    response = await client_a.post(
        f"/api/v1/verification/contacts/{contact.id}/unreachable", json={"note": "bounced"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["flag_type"] == "unreachable_contact"
    assert body["institution_id"] == str(institution.id)


@pytest.mark.asyncio
async def test_mark_unknown_contact_unreachable_404s(client_a):
    response = await client_a.post(
        f"/api/v1/verification/contacts/{uuid.uuid4()}/unreachable", json={}
    )
    assert response.status_code == 404
