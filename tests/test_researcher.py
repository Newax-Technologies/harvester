import contextlib
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.intelligence.researcher import ResearchBrain
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.mark.asyncio
async def test_research_record_constructs_valid_canonical_institution(db_session):
    # _research_record previously passed a nonexistent operating_status
    # kwarg and a nonexistent OperatingStatus.ACTIVE member -- both would
    # raise before this line even finished constructing the object, so
    # every linkedin-research run crashed before persisting anything.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="li:test123",
        raw_payload={"full_name": "Jane Doe"},
        normalized_name="jane doe",
    )
    db_session.add(record)
    await db_session.flush()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain.research_profile = AsyncMock(return_value=None)

    await brain._research_record(db_session, record)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(CanonicalInstitution.canonical_name == "Jane Doe")
        )
    ).scalar_one()
    assert institution.status == OperatingStatus.OPERATIONAL
    brain.research_profile.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_all_pending_excludes_already_researched_records(db_session):
    # Previously undocumented as a real gap ("full implementation would use
    # a processed flag") but harmless while linkedin-research was
    # unreachable dead code -- now that cli.py's shadowing duplicate main()
    # is gone, every invocation re-processed the same records forever.
    # Calling process_all_pending() twice must only research the record
    # once.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="li:test456",
        raw_payload={"full_name": "Already Processed"},
        normalized_name="already processed",
    )
    db_session.add(record)
    await db_session.commit()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain.research_profile = AsyncMock(return_value=None)

    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()
        await brain.process_all_pending()

    brain.research_profile.assert_awaited_once()
    count = await db_session.scalar(
        select(func.count())
        .select_from(CanonicalInstitution)
        .where(CanonicalInstitution.canonical_name == "Already Processed")
    )
    assert count == 1
