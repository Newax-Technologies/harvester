import asyncio
import uuid

import pytest
from cryptography.fernet import Fernet

from lead_harvester.config import settings
from lead_harvester.models.tenancy import DEFAULT_TENANT_ID
from lead_harvester.services.auth_service import TenantNotFoundError
from lead_harvester.services.credential_vault_service import (
    credential_metadata,
    get_credential_fingerprint,
    list_credentials,
    retrieve_plaintext_for_use,
    revoke_credential,
    store_credential,
)
from lead_harvester.vault_crypto import fingerprint_secret


@pytest.fixture(autouse=True)
def vault_key(monkeypatch):
    monkeypatch.setattr(settings, "vault_encryption_key", Fernet.generate_key().decode())


@pytest.mark.asyncio
async def test_store_then_retrieve_plaintext_round_trips(db_session):
    await store_credential(
        db_session, DEFAULT_TENANT_ID, "google_places_api_key", "AIza-real-value", created_by="op"
    )

    value = await retrieve_plaintext_for_use(db_session, DEFAULT_TENANT_ID, "google_places_api_key")
    assert value == "AIza-real-value"


@pytest.mark.asyncio
async def test_store_never_persists_plaintext_in_the_ciphertext_column(db_session):
    credential = await store_credential(
        db_session, DEFAULT_TENANT_ID, "yandex_maps_api_key", "yandex-secret", created_by="op"
    )
    assert "yandex-secret" not in credential.ciphertext
    assert credential.fingerprint == fingerprint_secret("yandex-secret")


@pytest.mark.asyncio
async def test_store_twice_rotates_and_deactivates_the_prior_version(db_session):
    first = await store_credential(
        db_session, DEFAULT_TENANT_ID, "rotating-key", "value-1", created_by="op"
    )
    second = await store_credential(
        db_session, DEFAULT_TENANT_ID, "rotating-key", "value-2", created_by="op"
    )

    await db_session.refresh(first)
    assert first.is_active is False
    assert first.revoked_at is None  # superseded, not revoked
    assert second.is_active is True
    assert second.version == first.version + 1

    value = await retrieve_plaintext_for_use(db_session, DEFAULT_TENANT_ID, "rotating-key")
    assert value == "value-2"


@pytest.mark.asyncio
async def test_store_raises_for_a_nonexistent_tenant(db_session):
    with pytest.raises(TenantNotFoundError):
        await store_credential(db_session, uuid.uuid4(), "some-key", "some-value", created_by="op")


@pytest.mark.asyncio
async def test_revoke_deactivates_and_leaves_no_active_credential(db_session):
    await store_credential(db_session, DEFAULT_TENANT_ID, "revoke-target", "value", created_by="op")

    revoked = await revoke_credential(db_session, DEFAULT_TENANT_ID, "revoke-target")

    assert revoked is not None
    assert revoked.revoked_at is not None
    assert await get_credential_fingerprint(db_session, DEFAULT_TENANT_ID, "revoke-target") is None


@pytest.mark.asyncio
async def test_revoke_returns_none_when_no_active_credential_exists(db_session):
    assert await revoke_credential(db_session, DEFAULT_TENANT_ID, "never-stored") is None


@pytest.mark.asyncio
async def test_get_credential_fingerprint_never_exposes_plaintext(db_session):
    await store_credential(
        db_session, DEFAULT_TENANT_ID, "fp-check", "the-real-secret", created_by="op"
    )

    fingerprint = await get_credential_fingerprint(db_session, DEFAULT_TENANT_ID, "fp-check")

    assert fingerprint == fingerprint_secret("the-real-secret")
    assert "the-real-secret" not in fingerprint


@pytest.mark.asyncio
async def test_list_credentials_only_returns_active_versions(db_session):
    await store_credential(db_session, DEFAULT_TENANT_ID, "list-a", "v1", created_by="op")
    await store_credential(db_session, DEFAULT_TENANT_ID, "list-b", "v1", created_by="op")
    await store_credential(db_session, DEFAULT_TENANT_ID, "list-b", "v2", created_by="op")

    credentials = await list_credentials(db_session, DEFAULT_TENANT_ID)
    names = {c.name for c in credentials}

    assert names == {"list-a", "list-b"}
    assert all(c.is_active for c in credentials)


@pytest.mark.asyncio
async def test_credential_metadata_never_includes_ciphertext_or_plaintext(db_session):
    credential = await store_credential(
        db_session, DEFAULT_TENANT_ID, "meta-check", "the-real-secret", created_by="op"
    )

    metadata = credential_metadata(credential)

    assert "ciphertext" not in metadata
    assert "the-real-secret" not in str(metadata)


@pytest.mark.asyncio
async def test_retrieve_plaintext_raises_for_unknown_name(db_session):
    with pytest.raises(ValueError, match="No active vaulted credential"):
        await retrieve_plaintext_for_use(db_session, DEFAULT_TENANT_ID, "never-stored")


@pytest.mark.asyncio
async def test_concurrent_first_stores_serialize_instead_of_racing_the_unique_index(async_engine):
    # Same reasoning/shape as tenant_config_service's identical test --
    # the never-stored-before case has no row for SELECT ... FOR UPDATE to
    # lock, so the advisory lock is what prevents two concurrent first
    # stores for the same (tenant_id, name) from racing
    # uq_vaulted_credentials_one_active_version.
    from sqlalchemy.ext.asyncio import AsyncSession

    conn_a = await async_engine.connect()
    conn_b = await async_engine.connect()
    session_a = AsyncSession(bind=conn_a, expire_on_commit=False)
    session_b = AsyncSession(bind=conn_b, expire_on_commit=False)

    async def _store_and_commit(session, value):
        result = await store_credential(
            session, DEFAULT_TENANT_ID, "race-key", value, created_by="op"
        )
        await session.commit()
        return result

    try:
        results = await asyncio.gather(
            _store_and_commit(session_a, "value-a"), _store_and_commit(session_b, "value-b")
        )
        assert sorted(r.version for r in results) == [1, 2]
    finally:
        # Both sessions commit for real against the shared test database --
        # delete the row(s) this test created so they don't outlive it and
        # affect unrelated tests (e.g. list_credentials for DEFAULT_TENANT_ID).
        from sqlalchemy import delete

        from lead_harvester.models.vault import VaultedCredential

        await session_a.execute(
            delete(VaultedCredential).where(VaultedCredential.name == "race-key")
        )
        await session_a.commit()
        await session_a.close()
        await session_b.close()
        await conn_a.close()
        await conn_b.close()
