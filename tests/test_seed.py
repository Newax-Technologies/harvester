import argparse
import contextlib
from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.resolution import MatchAssessment, ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord


@contextlib.asynccontextmanager
async def _fake_get_session(session: AsyncSession):
    yield session


@pytest.mark.asyncio
async def test_run_seed_creates_valid_resolution_candidate(db_session):
    # run_seed previously imported a nonexistent database.get_session_factory
    # (ImportError before anything ran) and constructed ResolutionCandidate
    # with fields the schema doesn't have (target_institution_id,
    # incoming_source_id, incoming_data, confidence_score) -- a TypeError
    # that rolled back the whole seed transaction. Confirms it now runs
    # end-to-end and produces a schema-valid candidate/assessment pair with
    # a real backing raw record.
    from lead_harvester.seed import run_seed

    args = argparse.Namespace(reset=False, scenario="full", seed=42)

    with patch("lead_harvester.seed.get_session", new=lambda: _fake_get_session(db_session)):
        result = await run_seed(args)

    assert result == 0

    institutions = (await db_session.execute(select(CanonicalInstitution))).scalars().all()
    assert len(institutions) == 5

    candidate = (await db_session.execute(select(ResolutionCandidate))).scalar_one()
    assert candidate.raw_record_id is not None
    assert candidate.target_canonical_id in {i.id for i in institutions}
    assert candidate.blocking_strategy

    raw_record = await db_session.get(RawSourceRecord, candidate.raw_record_id)
    assert raw_record is not None

    assessment = (
        await db_session.execute(
            select(MatchAssessment).where(MatchAssessment.candidate_id == candidate.id)
        )
    ).scalar_one()
    assert assessment.total_score == 75
