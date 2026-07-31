import uuid

import pytest

from lead_harvester.models.canonical import Branch, CanonicalInstitution


@pytest.mark.asyncio
async def test_get_institution_exposes_branch_city_and_country_code(client_a, db_session):
    inst = CanonicalInstitution(
        id=uuid.uuid4(), canonical_name="Test School", domain="test.edu", confidence_score=90.0
    )
    branch = Branch(
        id=uuid.uuid4(),
        institution_id=inst.id,
        branch_name="Main Campus",
        address="1 Test Street",
        city="Lahore",
        country_code="PK",
        provider_ids={},
    )
    db_session.add(inst)
    db_session.add(branch)
    await db_session.commit()

    response = await client_a.get(f"/api/v1/institutions/{inst.id}")
    assert response.status_code == 200
    body = response.json()

    assert len(body["branches"]) == 1
    assert body["branches"][0]["city"] == "Lahore"
    assert body["branches"][0]["country_code"] == "PK"
