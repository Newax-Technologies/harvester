import pytest

from lead_harvester.models.sector import Sector


@pytest.mark.asyncio
async def test_list_sectors_returns_seeded_and_created_sectors(client_admin, db_session):
    db_session.add(Sector(code="education", display_name="Education", institution_types=["school"]))
    await db_session.commit()

    response = await client_admin.get("/api/v1/sectors")

    assert response.status_code == 200
    codes = [s["code"] for s in response.json()]
    assert "education" in codes


@pytest.mark.asyncio
async def test_get_sector_route_404s_for_unknown_id(client_admin):
    import uuid

    response = await client_admin.get(f"/api/v1/sectors/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_sector_route(client_admin):
    response = await client_admin.post(
        "/api/v1/sectors",
        json={
            "code": "legal",
            "display_name": "Legal",
            "institution_types": ["law_firm"],
            "icp_criteria": {},
            "qualification_rules": {},
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "legal"
    assert body["institution_types"] == ["law_firm"]


@pytest.mark.asyncio
async def test_create_sector_route_rejects_duplicate_code(client_admin):
    payload = {"code": "finance", "display_name": "Finance"}
    first = await client_admin.post("/api/v1/sectors", json=payload)
    assert first.status_code == 201

    second = await client_admin.post("/api/v1/sectors", json=payload)
    assert second.status_code == 400


@pytest.mark.asyncio
async def test_update_sector_route_changes_only_provided_fields(client_admin):
    created = await client_admin.post(
        "/api/v1/sectors",
        json={"code": "retail", "display_name": "Retail", "institution_types": ["retail_store"]},
    )
    sector_id = created.json()["id"]

    response = await client_admin.patch(
        f"/api/v1/sectors/{sector_id}", json={"display_name": "Retail & E-commerce"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["display_name"] == "Retail & E-commerce"
    assert body["institution_types"] == ["retail_store"]


@pytest.mark.asyncio
async def test_update_sector_route_404s_for_unknown_id(client_admin):
    import uuid

    response = await client_admin.patch(
        f"/api/v1/sectors/{uuid.uuid4()}", json={"display_name": "Whatever"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_sectors_requires_sectors_manage_permission(client_a):
    # client_a's "reviewer" role does not hold sectors.manage (see
    # api/permissions.py's ROLE_PERMISSIONS) -- every sectors route,
    # including reads, is gated on it.
    response = await client_a.get("/api/v1/sectors")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_sector_requires_sectors_manage_permission(client_viewer):
    response = await client_viewer.post(
        "/api/v1/sectors", json={"code": "hospitality", "display_name": "Hospitality"}
    )
    assert response.status_code == 403
