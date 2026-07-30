from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from lead_harvester.intelligence.researcher import ResearchBrain
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType


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
