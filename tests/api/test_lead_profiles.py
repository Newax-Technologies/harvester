import uuid

import pytest

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.services.lead_profile_service import refresh_lead_profile


async def _seed_profiled_institution(db_session, **overrides) -> CanonicalInstitution:
    defaults = {"canonical_name": "Riverside Academy", "institution_type": "school"}
    defaults.update(overrides)
    institution = CanonicalInstitution(**defaults)
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        ContactPoint(
            institution_id=institution.id, contact_type="phone", contact_value="+923001234567"
        )
    )
    await db_session.flush()
    await refresh_lead_profile(db_session, institution.id)
    await db_session.commit()
    return institution


@pytest.mark.asyncio
async def test_get_profile_returns_the_current_profile(client_a, db_session):
    institution = await _seed_profiled_institution(db_session)

    response = await client_a.get(f"/api/v1/lead-profiles/{institution.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["institution_id"] == str(institution.id)
    assert body["has_phone"] is True
    assert body["overall_score"] > 0


@pytest.mark.asyncio
async def test_get_profile_404s_for_an_institution_never_profiled(client_a, db_session):
    institution = CanonicalInstitution(canonical_name="Never Profiled School")
    db_session.add(institution)
    await db_session.commit()

    response = await client_a.get(f"/api/v1/lead-profiles/{institution.id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_profile_404s_for_a_nonexistent_institution(client_a):
    response = await client_a.get(f"/api/v1/lead-profiles/{uuid.uuid4()}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_profiles_orders_by_score_descending(client_a, db_session):
    weak = CanonicalInstitution(canonical_name="Weak Lead", institution_type="")
    db_session.add(weak)
    await db_session.flush()
    await refresh_lead_profile(db_session, weak.id)

    await _seed_profiled_institution(db_session, canonical_name="Strong Lead")
    await db_session.commit()

    response = await client_a.get("/api/v1/lead-profiles")

    assert response.status_code == 200
    body = response.json()
    names = [item["canonical_name"] for item in body["items"]]
    assert names.index("Strong Lead") < names.index("Weak Lead")


@pytest.mark.asyncio
async def test_score_history_returns_snapshots_most_recent_first(client_a, db_session):
    institution = await _seed_profiled_institution(db_session)
    await refresh_lead_profile(db_session, institution.id)
    await db_session.commit()

    response = await client_a.get(f"/api/v1/lead-profiles/{institution.id}/score-history")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["computed_at"] >= body[1]["computed_at"]
