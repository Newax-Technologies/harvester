import contextlib
import json
import uuid
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.integrations.lead_sync_resync import resync_institution
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.outbox import EventOutbox, OutboxStatus


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


# resync_institution opens its OWN session via database.get_session() in
# production (deliberately -- it runs from a background task / after a
# run's own session has already closed, see the module docstring). But
# database.get_session() is bound to settings.database_url, a separate,
# real database from the isolated settings.test_database_url the rest of
# this suite runs against (tests/conftest.py's db_session fixture) -- CI
# only ever provisions the test database (see setup_db.py), so exercising
# get_session() directly here would fail outside a local dev environment
# that happens to already have the dev database. Patch the module's
# get_session reference to yield the test's db_session instead, so this
# exercises resync_institution's actual query logic against the same
# isolated, already-provisioned database every other test uses.


def _enabled_settings() -> Settings:
    return Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_url="https://core-newax.test/api/integrations/lead-harvester/webhook",
        lead_sync_webhook_secret="test-secret-with-more-than-32-characters",
    )


@pytest.mark.asyncio
async def test_resync_institution_emits_current_branches_and_contacts(db_session):
    institution = CanonicalInstitution(
        canonical_name="Resync Test School",
        institution_type="school",
        status=OperatingStatus.OPERATIONAL,
        confidence_score=50.0,
    )
    db_session.add(institution)
    await db_session.flush()

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
    db_session.add_all([branch, contact])
    await db_session.flush()

    emitter = LeadSyncEmitter(_enabled_settings())
    mock_response = httpx.Response(
        200, request=httpx.Request("POST", emitter.settings.lead_sync_webhook_url)
    )

    with (
        patch(
            "lead_harvester.integrations.lead_sync_resync.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch(
            "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
        ) as mock_post,
    ):
        await resync_institution(emitter, institution.id)

    mock_post.assert_awaited_once()
    payload = json.loads(mock_post.call_args.kwargs["content"])
    assert payload["institution"]["id"] == str(institution.id)
    assert [b["id"] for b in payload["branches"]] == [str(branch.id)]
    assert [c["id"] for c in payload["contactPoints"]] == [str(contact.id)]

    outbox_row = (
        await db_session.execute(
            select(EventOutbox).where(EventOutbox.institution_id == institution.id)
        )
    ).scalar_one()
    assert outbox_row.status == OutboxStatus.DELIVERED


@pytest.mark.asyncio
async def test_resync_institution_no_ops_for_missing_institution(db_session):
    emitter = LeadSyncEmitter(_enabled_settings())

    with (
        patch(
            "lead_harvester.integrations.lead_sync_resync.get_session",
            new=lambda: _fake_get_session(db_session),
        ),
        patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
    ):
        await resync_institution(emitter, uuid.uuid4())

    mock_post.assert_not_awaited()
    assert (await db_session.execute(select(EventOutbox))).scalar_one_or_none() is None
