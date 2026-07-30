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


@pytest.mark.asyncio
async def test_process_all_pending_excludes_by_stable_source_id_not_row_uuid(db_session):
    # A later crawler/farm run re-harvesting the same LinkedIn profile URL
    # creates a brand-new RawSourceRecord row (a new UUID) for the exact
    # same source_id -- excluding only by the OLD row's own UUID let that
    # new duplicate row sail through the filter and trigger another AI
    # call, ResearchJob, and CanonicalInstitution for the same person.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    original = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="https://linkedin.com/in/rescraped-profile",
        raw_payload={"full_name": "Rescraped Person"},
        normalized_name="rescraped person",
    )
    db_session.add(original)
    await db_session.commit()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain.research_profile = AsyncMock(return_value=None)

    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()

    brain.research_profile.assert_awaited_once()

    # A later run re-scrapes the exact same profile URL into a brand-new
    # row with its own UUID.
    rescraped = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="https://linkedin.com/in/rescraped-profile",
        raw_payload={"full_name": "Rescraped Person"},
        normalized_name="rescraped person",
    )
    db_session.add(rescraped)
    await db_session.commit()
    assert rescraped.id != original.id

    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()

    # Still only ever researched once.
    brain.research_profile.assert_awaited_once()
    count = await db_session.scalar(
        select(func.count())
        .select_from(CanonicalInstitution)
        .where(CanonicalInstitution.canonical_name == "Rescraped Person")
    )
    assert count == 1


@pytest.mark.asyncio
async def test_research_record_does_not_mark_processed_when_ai_call_fails(db_session):
    # A timed-out/rejected/malformed AI call previously got silently turned
    # into a fake zero-score analysis by _call_ai, so _research_record
    # persisted a COMPLETED job + READY_FOR_REVIEW brief containing the
    # failure text and marked the record processed -- permanently excluding
    # it from retry via process_all_pending's exclusion query. Later, once
    # the AI call was allowed to raise instead, the provisional institution
    # created before the try-block was left behind on every failure with no
    # FieldProvenance link back to it, so every failed retry minted another
    # orphan CanonicalInstitution forever. Neither must happen: the record
    # must stay retryable AND no orphan institution may survive the failure.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="li:test789",
        raw_payload={"full_name": "Failed Profile"},
        normalized_name="failed profile",
    )
    db_session.add(record)
    await db_session.flush()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain.research_profile = AsyncMock(side_effect=RuntimeError("AI call timed out"))

    await brain._research_record(db_session, record)

    institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Failed Profile"
            )
        )
    ).scalar_one_or_none()
    assert institution is None

    from lead_harvester.canonical.merger import find_canonical_for_raw_record

    assert await find_canonical_for_raw_record(db_session, record.id) is None

    # A second process_all_pending pass must still pick this record up.
    brain.research_profile = AsyncMock(return_value=None)
    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()

    brain.research_profile.assert_awaited_once()
    assert await find_canonical_for_raw_record(db_session, record.id) is not None
