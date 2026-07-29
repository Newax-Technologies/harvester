import pytest

from lead_harvester.canonical.merger import find_canonical_for_raw_record, merge_records
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
    # No location on any of these -- isolates this scenario to the phone
    # strategy only, since the shared default lat/lng would otherwise also
    # match via geo_name (a separate, higher-priority strategy tested on
    # its own below).
    a = google_places_record(
        source_run.id,
        name="Popular School",
        phone="+923001112222",
        website=None,
        lat=None,
        lng=None,
    )
    b = google_places_record(
        source_run.id,
        name="Popular School",
        phone="+923001112222",
        website=None,
        lat=None,
        lng=None,
    )
    c = google_places_record(
        source_run.id,
        name="Popular School",
        phone="+923001112222",
        website=None,
        lat=None,
        lng=None,
    )
    db_session.add_all([a, b, c])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b, c], same_location=True)
    await db_session.flush()

    d = google_places_record(
        source_run.id,
        name="Popular School",
        phone="+923001112222",
        website=None,
        lat=None,
        lng=None,
    )
    db_session.add(d)
    await db_session.flush()

    candidates = await generate_candidates(db_session, d)

    phone_candidates = [c for c in candidates if c.blocking_strategy == "phone"]
    assert len(phone_candidates) == 1
    assert phone_candidates[0].target_raw_record_id in {a.id, b.id, c.id}

    # The dedup must not break resolution -- whichever sibling survived
    # still correctly identifies the one existing institution.
    surviving_canonical_id = await find_canonical_for_raw_record(
        db_session, phone_candidates[0].target_raw_record_id
    )
    assert surviving_canonical_id == institution.id


@pytest.mark.asyncio
async def test_generate_candidates_keeps_strongest_match_not_first_encountered(
    db_session, source_run
):
    # Three siblings share a phone (a weak signal -- shared switchboards are
    # common across unrelated franchise branches), but only one of them (c)
    # also matches the incoming record's name AND location -- a much
    # stronger signal. If the dedup in generate_candidates just kept
    # whichever sibling the (unordered) phone query happened to return
    # first, it could easily discard c in favor of a or b, losing the one
    # match that would actually let score_candidate reach MERGE.
    a = google_places_record(
        source_run.id, name="Franchise Branch Alpha", phone="+923005556666", lat=1.0, lng=1.0
    )
    b = google_places_record(
        source_run.id, name="Franchise Branch Beta", phone="+923005556666", lat=2.0, lng=2.0
    )
    c = google_places_record(
        source_run.id,
        name="Downtown Academy",
        phone="+923005556666",
        lat=24.8607,
        lng=67.0011,
    )
    db_session.add_all([a, b, c])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b, c], same_location=True)
    await db_session.flush()

    d = google_places_record(
        source_run.id,
        name="Downtown Academy",
        phone="+923005556666",
        lat=24.8607,
        lng=67.0011,
    )
    db_session.add(d)
    await db_session.flush()

    candidates = await generate_candidates(db_session, d)

    assert len(candidates) == 1
    assert candidates[0].target_raw_record_id == c.id
    assert candidates[0].blocking_strategy == "geo_name"

    result = await resolve_incoming_record(db_session, d)
    assert result is not None
    assert result.id == institution.id


@pytest.mark.asyncio
async def test_generate_candidates_does_not_dedupe_unresolved_matches(db_session, source_run):
    # Two records sharing a phone that have NOT yet been canonicalized are
    # each a genuine, independent candidate (a human may need to review
    # both) -- the dedup only applies to matches that are already resolved.
    a = google_places_record(
        source_run.id,
        name="School Alpha",
        phone="+923003334444",
        website=None,
        lat=None,
        lng=None,
    )
    b = google_places_record(
        source_run.id,
        name="School Beta",
        phone="+923003334444",
        website=None,
        lat=None,
        lng=None,
    )
    db_session.add_all([a, b])
    await db_session.flush()

    c = google_places_record(
        source_run.id,
        name="School Gamma",
        phone="+923003334444",
        website=None,
        lat=None,
        lng=None,
    )
    db_session.add(c)
    await db_session.flush()

    candidates = await generate_candidates(db_session, c)

    phone_candidates = [cand for cand in candidates if cand.blocking_strategy == "phone"]
    assert {cand.target_raw_record_id for cand in phone_candidates} == {a.id, b.id}
