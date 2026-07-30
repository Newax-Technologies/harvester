import contextlib
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.intelligence.researcher import ResearchBrain, _validate_analysis_schema
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType

_VALID_ANALYSIS = {
    "lead_score": 8,
    "decision_maker": True,
    "pain_points": ["scaling issues"],
    "buying_signals": ["hiring"],
    "best_angle": "Growth angle",
    "suggested_subject": "Quick question",
    "email_draft": "Hi there...",
    "linkedin_note": "Hi, connecting...",
    "summary": "Strong lead.",
}


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


def test_validate_analysis_schema_accepts_well_formed_analysis():
    _validate_analysis_schema(dict(_VALID_ANALYSIS))  # must not raise


@pytest.mark.parametrize(
    "overrides",
    [
        {},  # empty response -- every key missing
        {"lead_score": 11},  # out of range
        {"lead_score": 0},  # out of range
        {"lead_score": True},  # bool is technically an int subclass -- must be rejected
        {"lead_score": "8"},  # wrong type
        {"decision_maker": "yes"},  # wrong type
        {"pain_points": "not-a-list"},  # wrong type
        {"buying_signals": "not-a-list"},  # wrong type
        {"best_angle": ""},  # blank required string
        {"summary": 123},  # wrong type
    ],
)
def test_validate_analysis_schema_rejects_malformed_analysis(overrides):
    # response_format={"type": "json_object"} only guarantees syntactically
    # valid JSON -- an empty {} or a response with a missing/wrong-typed/
    # out-of-range key is still valid JSON and must still be rejected here.
    analysis = {**_VALID_ANALYSIS, **overrides}
    if overrides == {}:
        analysis = {}
    with pytest.raises((ValueError, TypeError)):
        _validate_analysis_schema(analysis)


@pytest.mark.asyncio
async def test_call_ai_rejects_response_missing_required_keys():
    brain = ResearchBrain(api_key="fake-key-for-test")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="{}"))]
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with (
        patch("openai.AsyncOpenAI", return_value=mock_client),
        pytest.raises(ValueError, match="lead_score"),
    ):
        await brain._call_ai({"full_name": "Jane Doe"})


@pytest.mark.asyncio
async def test_call_ai_accepts_well_formed_response():
    brain = ResearchBrain(api_key="fake-key-for-test")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps(_VALID_ANALYSIS)))]
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("openai.AsyncOpenAI", return_value=mock_client):
        result = await brain._call_ai({"full_name": "Jane Doe"})

    assert result == _VALID_ANALYSIS


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
async def test_process_all_pending_dedupes_same_source_id_within_one_call(db_session):
    # The exclusion query only sees source_ids committed by a PRIOR call --
    # if the same profile was scraped twice (e.g. two overlapping farm
    # runs) before either row was ever processed, both rows lack a
    # FieldProvenance link and both pass the exclusion filter, landing in
    # the same batch. Without an in-batch dedupe, both got processed here,
    # minting two AI calls/institutions for one person.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    for _ in range(2):
        db_session.add(
            RawSourceRecord(
                source_run_id=run.id,
                source_type=SourceType.LINKEDIN,
                source_id="https://linkedin.com/in/double-scraped",
                raw_payload={"full_name": "Double Scraped"},
                normalized_name="double scraped",
            )
        )
    await db_session.commit()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain.research_profile = AsyncMock(return_value=None)

    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()

    brain.research_profile.assert_awaited_once()
    count = await db_session.scalar(
        select(func.count())
        .select_from(CanonicalInstitution)
        .where(CanonicalInstitution.canonical_name == "Double Scraped")
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
