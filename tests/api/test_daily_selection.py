import uuid

import pytest

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint, OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.sector import Sector


async def _seed_profiled_institution(
    db_session, *, canonical_name: str, overall_score: int = 50, sector_id: uuid.UUID | None = None
):
    institution = CanonicalInstitution(
        canonical_name=canonical_name, status=OperatingStatus.OPERATIONAL, sector_id=sector_id
    )
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        ContactPoint(
            institution_id=institution.id, contact_type="phone", contact_value="+923001234567"
        )
    )
    db_session.add(
        LeadProfile(institution_id=institution.id, overall_score=overall_score, has_phone=True)
    )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_trigger_selection_reserves_eligible_leads(client_a, db_session):
    institution = await _seed_profiled_institution(db_session, canonical_name="Riverside Academy")
    await db_session.commit()

    response = await client_a.post("/api/v1/daily-selection", json={})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["institution_id"] == str(institution.id)
    assert body[0]["status"] == "reserved"


@pytest.mark.asyncio
async def test_trigger_selection_never_reserves_the_same_lead_twice(client_a, db_session):
    await _seed_profiled_institution(db_session, canonical_name="Once Only")
    await db_session.commit()

    first = await client_a.post("/api/v1/daily-selection", json={})
    second = await client_a.post("/api/v1/daily-selection", json={})

    assert len(first.json()) == 1
    assert second.json() == []


@pytest.mark.asyncio
async def test_list_selection_returns_canonical_name(client_a, db_session):
    await _seed_profiled_institution(db_session, canonical_name="Listed School")
    await db_session.commit()
    await client_a.post("/api/v1/daily-selection", json={})

    response = await client_a.get("/api/v1/daily-selection")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["canonical_name"] == "Listed School"


@pytest.mark.asyncio
async def test_list_selection_filters_by_status(client_a, db_session):
    await _seed_profiled_institution(db_session, canonical_name="A")
    await db_session.commit()
    created = await client_a.post("/api/v1/daily-selection", json={})
    reservation_id = created.json()[0]["id"]
    await client_a.post(f"/api/v1/daily-selection/{reservation_id}/consume")

    reserved = await client_a.get("/api/v1/daily-selection", params={"status": "reserved"})
    consumed = await client_a.get("/api/v1/daily-selection", params={"status": "consumed"})

    assert reserved.json() == []
    assert len(consumed.json()) == 1


@pytest.mark.asyncio
async def test_consume_reservation_marks_it_consumed(client_a, db_session):
    await _seed_profiled_institution(db_session, canonical_name="To Consume")
    await db_session.commit()
    created = await client_a.post("/api/v1/daily-selection", json={})
    reservation_id = created.json()[0]["id"]

    response = await client_a.post(f"/api/v1/daily-selection/{reservation_id}/consume")

    assert response.status_code == 200
    assert response.json()["status"] == "consumed"


@pytest.mark.asyncio
async def test_consume_reservation_404s_for_unknown_id(client_a):
    response = await client_a.post(f"/api/v1/daily-selection/{uuid.uuid4()}/consume")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_consume_already_consumed_reservation_returns_400(client_a, db_session):
    await _seed_profiled_institution(db_session, canonical_name="Double Consume")
    await db_session.commit()
    created = await client_a.post("/api/v1/daily-selection", json={})
    reservation_id = created.json()[0]["id"]
    await client_a.post(f"/api/v1/daily-selection/{reservation_id}/consume")

    response = await client_a.post(f"/api/v1/daily-selection/{reservation_id}/consume")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_release_reservation_frees_it_for_reselection(client_a, db_session):
    institution = await _seed_profiled_institution(db_session, canonical_name="Release Me")
    await db_session.commit()
    created = await client_a.post("/api/v1/daily-selection", json={})
    reservation_id = created.json()[0]["id"]

    response = await client_a.post(f"/api/v1/daily-selection/{reservation_id}/release")
    assert response.status_code == 200
    assert response.json()["status"] == "released"

    reselected = await client_a.post("/api/v1/daily-selection", json={})
    assert reselected.json()[0]["institution_id"] == str(institution.id)


@pytest.mark.asyncio
async def test_trigger_selection_respects_request_overrides(client_a, db_session):
    for i in range(3):
        await _seed_profiled_institution(db_session, canonical_name=f"School {i}", overall_score=i)
    await db_session.commit()

    response = await client_a.post("/api/v1/daily-selection", json={"limit": 1})

    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "reserved"


@pytest.mark.asyncio
async def test_trigger_selection_filters_by_sector_id(client_a, db_session):
    education = Sector(code="education", display_name="Education", institution_types=["school"])
    retail = Sector(code="retail", display_name="Retail", institution_types=["retail_store"])
    db_session.add_all([education, retail])
    await db_session.flush()
    school = await _seed_profiled_institution(
        db_session, canonical_name="Sector School", sector_id=education.id
    )
    await _seed_profiled_institution(db_session, canonical_name="Sector Store", sector_id=retail.id)
    await db_session.commit()

    response = await client_a.post("/api/v1/daily-selection", json={"sector_id": str(education.id)})

    body = response.json()
    assert len(body) == 1
    assert body[0]["institution_id"] == str(school.id)
    assert body[0]["sector_id"] == str(education.id)


@pytest.mark.asyncio
async def test_list_selection_filters_by_sector_id(client_a, db_session):
    education = Sector(code="education", display_name="Education", institution_types=["school"])
    retail = Sector(code="retail", display_name="Retail", institution_types=["retail_store"])
    db_session.add_all([education, retail])
    await db_session.flush()
    await _seed_profiled_institution(
        db_session, canonical_name="List Sector School", sector_id=education.id
    )
    await _seed_profiled_institution(
        db_session, canonical_name="List Sector Store", sector_id=retail.id
    )
    await db_session.commit()
    await client_a.post("/api/v1/daily-selection", json={})

    response = await client_a.get(
        "/api/v1/daily-selection", params={"sector_id": str(education.id)}
    )

    body = response.json()
    assert len(body) == 1
    assert body[0]["canonical_name"] == "List Sector School"
