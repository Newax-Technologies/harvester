import pytest_asyncio

from lead_harvester.models.source import RunStatus, SourceRun, SourceType


@pytest_asyncio.fixture
async def source_run(db_session):
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    return run
