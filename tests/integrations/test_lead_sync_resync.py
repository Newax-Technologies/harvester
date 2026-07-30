import uuid
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from lead_harvester.config import Settings
from lead_harvester.database import engine as resync_engine
from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.integrations.lead_sync_resync import resync_institution
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)

# resync_institution (unlike the rest of the resolution codepaths, which
# always take an already-open AsyncSession as a parameter) opens its OWN
# session via database.get_session() -- this is deliberate, since it runs
# from a background task / after a run's own session has already closed
# (see the module docstring). That means it can't be exercised through the
# tests/conftest.py db_session fixture (bound to a separate, savepoint-only
# test database connection get_session() never touches) -- seed and clean
# up directly against the real configured database instead, the same way
# database.get_session() itself will be used at runtime.


def _enabled_settings() -> Settings:
    return Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_url="https://core-newax.test/api/integrations/lead-harvester/webhook",
        lead_sync_webhook_secret="test-secret-with-more-than-32-characters",
    )


@pytest_asyncio.fixture(autouse=True)
async def dispose_resync_engine():
    # database.engine is a module-level engine bound to whatever event loop
    # first uses it; pytest-asyncio (strict mode) gives each test its own
    # loop, so it must be disposed between tests here too -- same reasoning
    # as tests/api/test_manual_leads.py's dispose_manual_leads_engine.
    yield
    await resync_engine.dispose()


@pytest.mark.asyncio
async def test_resync_institution_emits_current_branches_and_contacts():
    async with get_session() as session:
        institution = CanonicalInstitution(
            canonical_name="Resync Test School",
            institution_type="school",
            status=OperatingStatus.OPERATIONAL,
            confidence_score=50.0,
        )
        session.add(institution)
        await session.flush()

        branch = Branch(
            institution_id=institution.id,
            branch_name="Main Campus",
            address="1 Test Street",
            city="Lahore",
            country_code="PK",
            provider_ids={},
        )
        contact = ContactPoint(
            institution_id=institution.id,
            contact_type="phone",
            contact_value="+923001112222",
            is_publicly_listed=False,
        )
        session.add_all([branch, contact])
        await session.flush()
        institution_id, branch_id, contact_id = institution.id, branch.id, contact.id

    try:
        emitter = LeadSyncEmitter(_enabled_settings())
        emitter.emit_institution_upserted = AsyncMock()

        await resync_institution(emitter, institution_id)

        emitter.emit_institution_upserted.assert_awaited_once()
        args, _ = emitter.emit_institution_upserted.call_args
        resynced_institution, branches, contacts = args
        assert resynced_institution.id == institution_id
        assert [b.id for b in branches] == [branch_id]
        assert [c.id for c in contacts] == [contact_id]
    finally:
        async with get_session() as session:
            await session.delete(await session.get(ContactPoint, contact_id))
            await session.delete(await session.get(Branch, branch_id))
            await session.delete(await session.get(CanonicalInstitution, institution_id))


@pytest.mark.asyncio
async def test_resync_institution_no_ops_for_missing_institution():
    emitter = LeadSyncEmitter(_enabled_settings())
    emitter.emit_institution_upserted = AsyncMock()

    await resync_institution(emitter, uuid.uuid4())

    emitter.emit_institution_upserted.assert_not_awaited()
