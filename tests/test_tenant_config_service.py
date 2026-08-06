import asyncio
import uuid

import pytest

from lead_harvester.config_registry import ConfigValueTypeError, UnknownConfigKeyError
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID
from lead_harvester.services.auth_service import TenantNotFoundError
from lead_harvester.services.tenant_config_service import (
    get_tenant_config,
    get_tenant_config_history,
    set_tenant_config,
)


@pytest.mark.asyncio
async def test_get_tenant_config_returns_registry_default_when_no_override_exists(db_session):
    value = await get_tenant_config(
        db_session, DEFAULT_TENANT_ID, "feature.restricted_sources_enabled"
    )
    assert value is False


@pytest.mark.asyncio
async def test_get_tenant_config_raises_for_an_unknown_key(db_session):
    with pytest.raises(UnknownConfigKeyError):
        await get_tenant_config(db_session, DEFAULT_TENANT_ID, "not.a.real.key")


@pytest.mark.asyncio
async def test_set_then_get_returns_the_override(db_session):
    await set_tenant_config(
        db_session,
        DEFAULT_TENANT_ID,
        "limit.export_max_rows",
        1000,
        created_by="test-operator",
    )

    value = await get_tenant_config(db_session, DEFAULT_TENANT_ID, "limit.export_max_rows")
    assert value == 1000


@pytest.mark.asyncio
async def test_set_tenant_config_rejects_an_unknown_key(db_session):
    with pytest.raises(UnknownConfigKeyError):
        await set_tenant_config(
            db_session, DEFAULT_TENANT_ID, "not.a.real.key", "x", created_by="test-operator"
        )


@pytest.mark.asyncio
async def test_set_tenant_config_rejects_a_value_of_the_wrong_type(db_session):
    with pytest.raises(ConfigValueTypeError):
        await set_tenant_config(
            db_session,
            DEFAULT_TENANT_ID,
            "limit.export_max_rows",
            "not-an-int",
            created_by="test-operator",
        )


@pytest.mark.asyncio
async def test_set_tenant_config_twice_creates_a_new_version_and_deactivates_the_old_one(
    db_session,
):
    first = await set_tenant_config(
        db_session,
        DEFAULT_TENANT_ID,
        "limit.export_max_rows",
        1000,
        created_by="test-operator",
    )
    second = await set_tenant_config(
        db_session,
        DEFAULT_TENANT_ID,
        "limit.export_max_rows",
        2000,
        created_by="test-operator",
    )

    await db_session.refresh(first)
    assert first.is_active is False
    assert second.is_active is True
    assert second.version == first.version + 1

    value = await get_tenant_config(db_session, DEFAULT_TENANT_ID, "limit.export_max_rows")
    assert value == 2000


@pytest.mark.asyncio
async def test_get_tenant_config_history_returns_every_version_oldest_first(db_session):
    await set_tenant_config(
        db_session, DEFAULT_TENANT_ID, "limit.export_max_rows", 1000, created_by="a"
    )
    await set_tenant_config(
        db_session, DEFAULT_TENANT_ID, "limit.export_max_rows", 2000, created_by="b"
    )
    await set_tenant_config(
        db_session, DEFAULT_TENANT_ID, "limit.export_max_rows", 3000, created_by="c"
    )

    history = await get_tenant_config_history(
        db_session, DEFAULT_TENANT_ID, "limit.export_max_rows"
    )

    assert [h.version for h in history] == [1, 2, 3]
    assert [h.value["v"] for h in history] == [1000, 2000, 3000]
    assert [h.is_active for h in history] == [False, False, True]
    assert [h.created_by for h in history] == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_get_tenant_config_history_raises_for_an_unknown_key(db_session):
    with pytest.raises(UnknownConfigKeyError):
        await get_tenant_config_history(db_session, DEFAULT_TENANT_ID, "not.a.real.key")


@pytest.mark.asyncio
async def test_set_tenant_config_raises_for_a_nonexistent_tenant(db_session):
    with pytest.raises(TenantNotFoundError):
        await set_tenant_config(
            db_session, uuid.uuid4(), "limit.export_max_rows", 1000, created_by="test-operator"
        )


@pytest.mark.asyncio
async def test_concurrent_first_writes_serialize_instead_of_racing_the_unique_index(async_engine):
    # db_session wraps every test in one shared connection/transaction, so
    # it can only prove sequential behavior. This opens two genuinely
    # independent connections and calls set_tenant_config for the SAME
    # (tenant, key) that has never been set before -- the "no existing row
    # to SELECT ... FOR UPDATE on" case -- truly concurrently. Without the
    # pg_advisory_xact_lock in set_tenant_config, both could read "no
    # active version", both compute version=1, and one would fail with a
    # raw IntegrityError against uq_tenant_config_one_active_version
    # instead of simply waiting its turn and landing on version 2.
    from sqlalchemy.ext.asyncio import AsyncSession

    from lead_harvester.models.tenancy import Tenant

    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    tenant = Tenant(name="Race Co", slug="race-co")
    setup_session.add(tenant)
    await setup_session.commit()
    tenant_id = tenant.id

    conn_a = await async_engine.connect()
    conn_b = await async_engine.connect()
    session_a = AsyncSession(bind=conn_a, expire_on_commit=False)
    session_b = AsyncSession(bind=conn_b, expire_on_commit=False)

    async def _set_and_commit(session, value, actor):
        # Commits inside the coroutine, not after gather() -- the
        # advisory lock is released on commit, and the other coroutine
        # is blocked waiting for exactly that release. Committing only
        # after both coroutines "finish" would deadlock: neither can
        # finish without the other's commit.
        result = await set_tenant_config(
            session, tenant_id, "limit.export_max_rows", value, created_by=actor
        )
        await session.commit()
        return result

    try:
        results = await asyncio.gather(
            _set_and_commit(session_a, 111, "a"),
            _set_and_commit(session_b, 222, "b"),
        )

        assert sorted(r.version for r in results) == [1, 2]
    finally:
        await session_a.close()
        await session_b.close()
        await setup_session.close()
        await conn_a.close()
        await conn_b.close()
        await setup_conn.close()


@pytest.mark.asyncio
async def test_tenant_config_overrides_do_not_leak_across_tenants(db_session):
    from lead_harvester.models.tenancy import Tenant

    other_tenant = Tenant(name="Config Isolation Co", slug="config-isolation-co")
    db_session.add(other_tenant)
    await db_session.flush()

    await set_tenant_config(
        db_session, DEFAULT_TENANT_ID, "limit.export_max_rows", 1000, created_by="test-operator"
    )

    other_value = await get_tenant_config(db_session, other_tenant.id, "limit.export_max_rows")

    # other_tenant never had an override set -- must see the registry
    # default, not the default tenant's override.
    assert other_value == 5000
