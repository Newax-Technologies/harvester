import pytest

from lead_harvester.canonical.merger import merge_records
from lead_harvester.resolution.blocking import generate_candidates
from lead_harvester.resolution.orchestrator import resolve_incoming_record

from .factories import google_places_record


@pytest.mark.asyncio
async def test_generate_candidates_keeps_one_match_per_already_canonicalized_institution(
    db_session, source_run
):
    # Three records that already collapsed into one institution (e.g. three
    # earlier Google Places rediscoveries of the same location) all share a
    # phone number. A fourth new record sharing that phone only needs ONE of
    # them to identify the existing institution -- scoring (and persisting a
    # permanent candidate/assessment row for) all three would grow without
    # bound as the same popular institution keeps getting rediscovered.
    a = google_places_record(source_run.id, name="Popular School", phone="+923001112222")
    b = google_places_record(source_run.id, name="Popular School", phone="+923001112222")
    c = google_places_record(source_run.id, name="Popular School", phone="+923001112222")
    db_session.add_all([a, b, c])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b, c], same_location=True)
    await db_session.flush()

    d = google_places_record(source_run.id, name="Popular School", phone="+923001112222")
    db_session.add(d)
    await db_session.flush()

    candidates = await generate_candidates(db_session, d)

    phone_candidates = [c for c in candidates if c.blocking_strategy == "phone"]
    assert len(phone_candidates) == 1
    assert phone_candidates[0].target_raw_record_id in {a.id, b.id, c.id}

    # The dedup must not break actual resolution -- d still correctly
    # attaches to the one existing institution via whichever sibling survived.
    result = await resolve_incoming_record(db_session, d)
    assert result is not None
    assert result.id == institution.id


@pytest.mark.asyncio
async def test_generate_candidates_does_not_dedupe_unresolved_matches(db_session, source_run):
    # Two records sharing a phone that have NOT yet been canonicalized are
    # each a genuine, independent candidate (a human may need to review
    # both) -- the dedup only applies to matches that are already resolved.
    a = google_places_record(source_run.id, name="School Alpha", phone="+923003334444")
    b = google_places_record(source_run.id, name="School Beta", phone="+923003334444")
    db_session.add_all([a, b])
    await db_session.flush()

    c = google_places_record(source_run.id, name="School Gamma", phone="+923003334444")
    db_session.add(c)
    await db_session.flush()

    candidates = await generate_candidates(db_session, c)

    phone_candidates = [cand for cand in candidates if cand.blocking_strategy == "phone"]
    assert {cand.target_raw_record_id for cand in phone_candidates} == {a.id, b.id}
