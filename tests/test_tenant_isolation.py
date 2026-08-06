import pytest
from httpx import ASGITransport, AsyncClient

from lead_harvester.api.app import app
from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID, Tenant
from lead_harvester.services.institution_service import InstitutionService


@pytest.mark.asyncio
async def test_canonical_institution_defaults_to_the_default_tenant(db_session):
    inst = CanonicalInstitution(canonical_name="No Tenant Specified", confidence_score=50.0)
    db_session.add(inst)
    await db_session.flush()

    assert inst.tenant_id == DEFAULT_TENANT_ID


@pytest.mark.asyncio
async def test_get_institutions_only_returns_the_callers_tenant(db_session):
    other_tenant = Tenant(name="Other Tenant Co", slug="other-tenant-co")
    db_session.add(other_tenant)
    await db_session.flush()

    default_inst = CanonicalInstitution(
        canonical_name="Default Tenant School", confidence_score=50.0
    )
    other_inst = CanonicalInstitution(
        tenant_id=other_tenant.id, canonical_name="Other Tenant School", confidence_score=50.0
    )
    db_session.add_all([default_inst, other_inst])
    await db_session.flush()

    result = await InstitutionService.get_institutions(db_session, DEFAULT_TENANT_ID)

    names = {item.canonical_name for item in result.items}
    assert "Default Tenant School" in names
    assert "Other Tenant School" not in names


@pytest.mark.asyncio
async def test_get_institution_detail_returns_none_for_a_cross_tenant_id(db_session):
    other_tenant = Tenant(name="Cross Tenant Co", slug="cross-tenant-co")
    db_session.add(other_tenant)
    await db_session.flush()

    other_inst = CanonicalInstitution(
        tenant_id=other_tenant.id, canonical_name="Cross Tenant School", confidence_score=50.0
    )
    db_session.add(other_inst)
    await db_session.flush()

    # Cross-tenant lookup must return None, exactly like a genuinely
    # missing id -- it must never distinguish "exists in another tenant"
    # from "doesn't exist" to an unauthorized caller.
    result = await InstitutionService.get_institution_detail(
        db_session, str(other_inst.id), DEFAULT_TENANT_ID
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_institution_detail_returns_the_institution_for_the_owning_tenant(db_session):
    inst = CanonicalInstitution(canonical_name="Owned School", confidence_score=50.0)
    db_session.add(inst)
    await db_session.flush()

    result = await InstitutionService.get_institution_detail(
        db_session, str(inst.id), DEFAULT_TENANT_ID
    )

    assert result is not None
    assert result.id == inst.id


@pytest.mark.asyncio
async def test_api_institution_detail_is_invisible_across_tenants(db_session):
    other_tenant = Tenant(name="API Cross Tenant Co", slug="api-cross-tenant-co")
    db_session.add(other_tenant)
    await db_session.flush()

    other_inst = CanonicalInstitution(
        tenant_id=other_tenant.id,
        canonical_name="API Cross Tenant School",
        confidence_score=50.0,
    )
    db_session.add(other_inst)
    await db_session.commit()

    async def get_test_session():
        yield db_session

    async def override_user():
        return User(id="u1", username="tenant-a-user", role="admin", tenant_id=DEFAULT_TENANT_ID)

    app.dependency_overrides[get_db_session] = get_test_session
    app.dependency_overrides[get_current_user] = override_user
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get(f"/api/v1/institutions/{other_inst.id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_api_institution_list_excludes_other_tenants(db_session):
    other_tenant = Tenant(name="API List Cross Tenant Co", slug="api-list-cross-tenant-co")
    db_session.add(other_tenant)
    await db_session.flush()

    own_inst = CanonicalInstitution(canonical_name="Own Listed School", confidence_score=50.0)
    other_inst = CanonicalInstitution(
        tenant_id=other_tenant.id,
        canonical_name="Other Listed School",
        confidence_score=50.0,
    )
    db_session.add_all([own_inst, other_inst])
    await db_session.commit()

    async def get_test_session():
        yield db_session

    async def override_user():
        return User(id="u1", username="tenant-a-user", role="admin", tenant_id=DEFAULT_TENANT_ID)

    app.dependency_overrides[get_db_session] = get_test_session
    app.dependency_overrides[get_current_user] = override_user
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/v1/institutions")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    names = {item["canonical_name"] for item in response.json()["items"]}
    assert "Own Listed School" in names
    assert "Other Listed School" not in names
