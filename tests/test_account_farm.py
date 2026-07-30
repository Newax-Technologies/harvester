import contextlib
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.sources.account_farm import AccountFarm, AccountResult


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.mark.asyncio
async def test_persist_profiles_writes_raw_source_records(db_session):
    # _run_account_worker previously returned only a bare profiles_scraped
    # count to the parent process -- the actual scraped profile data was
    # discarded, so a "successful" farm run left nothing in the database
    # for linkedin-research to process. _persist_profiles is what now
    # writes every worker's harvested profiles to RawSourceRecord.
    results = [
        AccountResult(
            account_id="burner_01",
            profiles_scraped=2,
            city="Karachi",
            warmup_phase=3,
            profiles=[
                {"profile_url": "https://linkedin.com/in/alice", "full_name": "Alice A"},
                {"profile_url": "https://linkedin.com/in/bob", "full_name": "Bob B"},
            ],
        ),
        AccountResult(
            account_id="burner_02",
            profiles_scraped=0,
            errors=["No session saved"],
            profiles=[],
        ),
    ]

    farm = AccountFarm(accounts=["burner_01", "burner_02"])

    with patch(
        "lead_harvester.sources.account_farm.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await farm._persist_profiles(results)

    records = (
        (
            await db_session.execute(
                select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
            )
        )
        .scalars()
        .all()
    )
    assert {r.source_id for r in records} == {
        "https://linkedin.com/in/alice",
        "https://linkedin.com/in/bob",
    }
    assert {r.normalized_name for r in records} == {"Alice A", "Bob B"}


@pytest.mark.asyncio
async def test_persist_profiles_no_ops_when_nothing_scraped(db_session):
    results = [AccountResult(account_id="burner_01", profiles_scraped=0, profiles=[])]
    farm = AccountFarm(accounts=["burner_01"])

    with patch(
        "lead_harvester.sources.account_farm.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await farm._persist_profiles(results)

    count = await db_session.scalar(
        select(RawSourceRecord).where(RawSourceRecord.source_type == SourceType.LINKEDIN)
    )
    assert count is None
