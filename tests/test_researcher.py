import asyncio
import contextlib
import json
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.intelligence.researcher import ResearchBrain, _validate_analysis_schema
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.profile import LeadProfile
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
async def test_research_record_savepoint_isolates_a_db_level_failure(db_session):
    # A failure partway through _persist_findings that's a genuine DB-level
    # error (not just a Python exception before any DB write) leaves the
    # surrounding Postgres transaction aborted -- every later statement on
    # it raises until a ROLLBACK. _research_record's own cleanup (deleting
    # the provisional institution, then flushing) used to be exactly such a
    # later statement, so it raised PendingRollbackError itself, escaping
    # this method and rolling back process_all_pending's whole shared
    # session -- discarding an EARLIER record in the same batch that had
    # already been researched successfully. Running each record inside its
    # own SAVEPOINT means only the failing record's work is undone.
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()

    now = datetime.now(UTC)
    good_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="li:good",
        raw_payload={"full_name": "Good Profile"},
        normalized_name="good profile",
        extracted_at=now - timedelta(seconds=5),
    )
    bad_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.LINKEDIN,
        source_id="li:bad",
        raw_payload={"full_name": "Bad Profile"},
        normalized_name="bad profile",
        extracted_at=now,
    )
    db_session.add_all([good_record, bad_record])
    await db_session.commit()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain._call_ai = AsyncMock(return_value=dict(_VALID_ANALYSIS))

    original_persist_findings = brain._persist_findings

    async def _persist_with_db_level_failure(session, institution_id, profile, analysis):
        if profile.get("full_name") == "Bad Profile":
            # A real DBAPI-level error (not a mocked Python exception) --
            # this is what actually poisons the surrounding transaction the
            # way a genuine flush/constraint failure would.
            await session.execute(text("SELECT 1/0"))
        await original_persist_findings(session, institution_id, profile, analysis)

    brain._persist_findings = _persist_with_db_level_failure

    with patch(
        "lead_harvester.intelligence.researcher.get_session",
        new=lambda: _fake_get_session(db_session),
    ):
        await brain.process_all_pending()

    good_institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(
                CanonicalInstitution.canonical_name == "Good Profile"
            )
        )
    ).scalar_one_or_none()
    assert good_institution is not None

    bad_institution = (
        await db_session.execute(
            select(CanonicalInstitution).where(CanonicalInstitution.canonical_name == "Bad Profile")
        )
    ).scalar_one_or_none()
    assert bad_institution is None


@pytest.mark.asyncio
async def test_research_profile_refreshes_the_lead_profile(db_session):
    # New research findings (lead_score, pain_points, buying_signals,
    # summary) change what an institution's LeadProfile should say --
    # research_profile must refresh it, not leave the profile reflecting
    # only whatever branch/contact data existed before this research ran.
    institution = CanonicalInstitution(
        canonical_name="Researched School", status=OperatingStatus.OPERATIONAL
    )
    db_session.add(institution)
    await db_session.flush()

    brain = ResearchBrain(api_key="fake-key-for-test")
    brain._call_ai = AsyncMock(return_value=dict(_VALID_ANALYSIS))

    await brain.research_profile(
        db_session,
        {"full_name": "Jane Doe", "profile_url": "https://linkedin.com/in/jane"},
        institution.id,
    )

    profile = (
        await db_session.execute(
            select(LeadProfile).where(LeadProfile.institution_id == institution.id)
        )
    ).scalar_one_or_none()
    assert profile is not None
    assert profile.organization_summary == _VALID_ANALYSIS["summary"]
    assert profile.evidence_count > 0


@pytest.mark.asyncio
async def test_process_all_pending_claim_query_never_double_claims_across_connections(
    async_engine,
):
    # already_researched_source_ids only excludes source_ids a PRIOR,
    # already-COMMITTED call already researched -- two overlapping
    # process_all_pending invocations (separate processes, each holding
    # this method's session open across a whole batch of slow AI calls)
    # previously both ran that query before either committed, both saw the
    # same "not yet researched" profiles, and both would perform the AI
    # call, mint a ResearchJob, and create a CanonicalInstitution for the
    # same person. with_for_update(skip_locked=True) claims rows as part
    # of the SELECT itself -- this proves two real, concurrent connections
    # running that exact claim query against the same candidate set never
    # claim the same row.
    setup_conn = await async_engine.connect()
    setup_session = AsyncSession(bind=setup_conn, expire_on_commit=False)
    run = SourceRun(source_type=SourceType.LINKEDIN, run_metadata={}, status=RunStatus.STARTED)
    setup_session.add(run)
    await setup_session.flush()

    records = [
        RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.LINKEDIN,
            source_id=f"https://linkedin.com/in/concurrency-{i}",
            raw_payload={"full_name": f"Person {i}"},
            normalized_name=f"person {i}",
        )
        for i in range(6)
    ]
    setup_session.add_all(records)
    await setup_session.commit()
    record_ids = {r.id for r in records}
    run_id = run.id
    await setup_session.close()
    await setup_conn.close()

    # A synchronization barrier forces genuine overlap between the two
    # transactions regardless of how fast the local test database responds
    # -- without it, one connection's SELECT-then-commit could race to
    # completion before the other's SELECT even starts, passing the
    # assertion below for the wrong reason (never actually exercising
    # SKIP LOCKED) rather than because claiming is truly race-safe.
    first_claimed_event = asyncio.Event()
    second_selected_event = asyncio.Event()

    async def claim(*, first: bool) -> set:
        conn = await async_engine.connect()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            if not first:
                await first_claimed_event.wait()
            async with session.begin():
                claimed = list(
                    await session.scalars(
                        select(RawSourceRecord)
                        .where(RawSourceRecord.source_type == SourceType.LINKEDIN)
                        .where(RawSourceRecord.id.in_(record_ids))
                        .with_for_update(skip_locked=True)
                    )
                )
                if first:
                    first_claimed_event.set()
                    await second_selected_event.wait()
                else:
                    second_selected_event.set()
            return {r.id for r in claimed}
        finally:
            await session.close()
            await conn.close()

    results = await asyncio.gather(claim(first=True), claim(first=False))

    try:
        claimed_a, claimed_b = results
        assert claimed_a.isdisjoint(claimed_b), (claimed_a, claimed_b)
        assert claimed_a | claimed_b == record_ids
    finally:
        cleanup_conn = await async_engine.connect()
        cleanup_session = AsyncSession(bind=cleanup_conn, expire_on_commit=False)
        try:
            await cleanup_session.execute(
                delete(RawSourceRecord).where(RawSourceRecord.id.in_(record_ids))
            )
            await cleanup_session.execute(delete(SourceRun).where(SourceRun.id == run_id))
            await cleanup_session.commit()
        finally:
            await cleanup_session.close()
            await cleanup_conn.close()


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
