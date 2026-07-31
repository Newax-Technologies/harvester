import pytest
from sqlalchemy import select

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.person import PersonCandidate
from lead_harvester.services.person_candidate_service import (
    list_person_candidates,
    resolve_person_candidate,
)


async def _institution(db_session, name: str = "Test School") -> CanonicalInstitution:
    institution = CanonicalInstitution(canonical_name=name)
    db_session.add(institution)
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_resolve_person_candidate_creates_new_candidate(db_session):
    institution = await _institution(db_session)

    candidate = await resolve_person_candidate(db_session, institution.id, "Ali Khan")

    assert candidate is not None
    assert candidate.display_name == "Ali Khan"
    assert candidate.normalized_name == "ali khan"
    assert candidate.evidence_count == 1
    assert candidate.institution_id == institution.id


@pytest.mark.asyncio
async def test_resolve_person_candidate_returns_none_for_blank_name(db_session):
    institution = await _institution(db_session)

    assert await resolve_person_candidate(db_session, institution.id, None) is None
    assert await resolve_person_candidate(db_session, institution.id, "") is None
    assert await resolve_person_candidate(db_session, institution.id, "   ") is None

    count = await db_session.scalar(select(PersonCandidate.id))
    assert count is None


@pytest.mark.asyncio
async def test_resolve_person_candidate_dedupes_by_normalized_name(db_session):
    # "Ali Khan", "ali khan", and "Ali-Khan" all normalize to the same
    # value via resolution/normalize.py::normalize_name -- they must
    # converge on the SAME PersonCandidate row, not three separate ones.
    institution = await _institution(db_session)

    first = await resolve_person_candidate(db_session, institution.id, "Ali Khan")
    second = await resolve_person_candidate(db_session, institution.id, "ali khan")
    third = await resolve_person_candidate(db_session, institution.id, "Ali-Khan")

    assert first.id == second.id == third.id
    assert first.evidence_count == 3
    # display_name reflects the most recently seen spelling/casing.
    assert first.display_name == "Ali-Khan"


@pytest.mark.asyncio
async def test_resolve_person_candidate_scoped_per_institution(db_session):
    # The same real name at two DIFFERENT institutions must not collapse
    # onto one PersonCandidate -- these are almost certainly different
    # people (or at least should be reviewed as distinct until proven
    # otherwise), and the unique constraint is scoped by institution_id
    # precisely so this doesn't happen.
    institution_a = await _institution(db_session, "School A")
    institution_b = await _institution(db_session, "School B")

    candidate_a = await resolve_person_candidate(db_session, institution_a.id, "Ali Khan")
    candidate_b = await resolve_person_candidate(db_session, institution_b.id, "Ali Khan")

    assert candidate_a.id != candidate_b.id
    assert candidate_a.evidence_count == 1
    assert candidate_b.evidence_count == 1


@pytest.mark.asyncio
async def test_list_person_candidates_filters_by_institution(db_session):
    institution_a = await _institution(db_session, "School A")
    institution_b = await _institution(db_session, "School B")
    await resolve_person_candidate(db_session, institution_a.id, "Ali Khan")
    await resolve_person_candidate(db_session, institution_b.id, "Jane Doe")

    results = await list_person_candidates(db_session, institution_id=institution_a.id)

    assert len(results) == 1
    assert results[0].display_name == "Ali Khan"
