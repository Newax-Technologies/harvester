from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import find_canonical_for_raw_record, merge_records
from lead_harvester.models.canonical import Branch
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.resolution import MatchAssessment, MatchDecision
from lead_harvester.models.sector import Sector
from lead_harvester.resolution.orchestrator import resolve_incoming_record

from .factories import google_places_record, website_record


@pytest.mark.asyncio
async def test_no_candidates_creates_own_institution(db_session, source_run):
    record = google_places_record(
        source_run.id, name="Unique Standalone School", phone="+923009999999", lat=1.0, lng=1.0
    )
    db_session.add(record)
    await db_session.flush()

    institution = await resolve_incoming_record(db_session, record)

    assert institution is not None
    assert institution.canonical_name == "Unique Standalone School"
    canonical_id = await find_canonical_for_raw_record(db_session, record.id)
    assert canonical_id == institution.id


@pytest.mark.asyncio
async def test_merge_with_unresolved_target_creates_shared_institution(db_session, source_run):
    a = google_places_record(
        source_run.id, name="Twin School", phone="+923001112222", lat=24.86, lng=67.00
    )
    b = google_places_record(
        source_run.id, name="Twin School", phone="+923003334444", lat=24.86, lng=67.00
    )
    db_session.add(a)
    await db_session.flush()

    inst_a = await resolve_incoming_record(db_session, a)
    assert inst_a is not None

    db_session.add(b)
    await db_session.flush()
    inst_b = await resolve_incoming_record(db_session, b)

    # First record had no candidates and got its own institution; the second
    # record should MERGE into that same institution (same name, same
    # location), not create a second one.
    assert inst_b is not None
    assert inst_b.id == inst_a.id

    result = await db_session.execute(select(Branch).where(Branch.institution_id == inst_a.id))
    branches = result.scalars().all()
    assert len(branches) == 1  # same_location=True collapses to one branch


@pytest.mark.asyncio
async def test_automated_merge_of_two_unresolved_records_links_both_records_snapshots(
    db_session, source_run
):
    # Correction regression test: when the incoming record merges with a
    # matched_record that is ITSELF still unresolved (neither has been
    # through resolve_incoming_record before), matched_record may already
    # carry its own persisted WEBSITE RawPageSnapshot rows from an earlier
    # run/attempt. pipeline.py's caller only ever backfills institution_id
    # for the record IT knows about (the incoming one); matched_record is
    # now canonicalized by this merge, so _retry_stranded_records would
    # never revisit it either -- its snapshots must be linked here.
    from lead_harvester.models.source import RawPageSnapshot

    incoming = website_record(
        source_run.id,
        name="Snapshot School",
        organization="Snapshot School",
        website="snapshot.edu",
        source_id="web:incoming",
    )
    matched = website_record(
        source_run.id,
        name="Snapshot School",
        organization="Snapshot School",
        website="snapshot.edu",
        source_id="web:matched",
    )
    db_session.add_all([incoming, matched])
    await db_session.flush()

    # matched's own snapshot, persisted in an earlier run/attempt, still
    # unlinked -- neither incoming nor matched has been resolved yet.
    snapshot = RawPageSnapshot(
        source_run_id=source_run.id,
        url="https://snapshot.edu/",
        final_url="https://snapshot.edu/",
        status_code=200,
        content_type="text/html",
        html="<html>hi</html>",
        fetch_error="",
        normalized_domain="snapshot.edu",
        raw_source_record_id=matched.id,
        institution_id=None,
    )
    db_session.add(snapshot)
    await db_session.flush()

    async def fake_score_candidate(session, candidate):
        assessment = MatchAssessment(
            candidate_id=candidate.id,
            name_similarity=0.95,
            distance_meters=None,
            phone_match=False,
            domain_match=True,
            total_score=95.0,
            decision=MatchDecision.MERGE,
        )
        session.add(assessment)
        return assessment

    with patch(
        "lead_harvester.resolution.orchestrator.score_candidate",
        new=AsyncMock(side_effect=fake_score_candidate),
    ):
        institution = await resolve_incoming_record(db_session, incoming)

    assert institution is not None
    assert await find_canonical_for_raw_record(db_session, matched.id) == institution.id
    await db_session.refresh(snapshot)
    assert snapshot.institution_id == institution.id


@pytest.mark.asyncio
async def test_merge_with_already_resolved_target_attaches_to_existing(db_session, source_run):
    a = google_places_record(
        source_run.id, name="Established School", phone="+923005556666", lat=31.5, lng=74.3
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    b = google_places_record(
        source_run.id, name="Established School", phone="+923007778888", lat=31.5, lng=74.3
    )
    db_session.add(b)
    await db_session.flush()

    result = await resolve_incoming_record(db_session, b)

    assert result is not None
    assert result.id == institution.id
    canonical_id = await find_canonical_for_raw_record(db_session, b.id)
    assert canonical_id == institution.id

    branches = (
        (await db_session.execute(select(Branch).where(Branch.institution_id == institution.id)))
        .scalars()
        .all()
    )
    assert len(branches) == 1
    assert b.source_id in branches[0].provider_ids.get("google_places", [])
    assert a.source_id in branches[0].provider_ids.get("google_places", [])


@pytest.mark.asyncio
async def test_attach_to_already_synced_institution_adds_resync_id(db_session, source_run):
    # An institution that went through the manual-lead route (and so has
    # lead_synced_at set -- see api/routes/manual_leads.py) must be flagged
    # for re-sync when a later automated resolution attaches new evidence to
    # it, or the core-newax mirror silently goes stale after the first sync.
    a = google_places_record(
        source_run.id, name="Synced School", phone="+923005551111", lat=31.5, lng=74.3
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    institution.lead_synced_at = datetime.now(UTC)
    await db_session.flush()

    b = google_places_record(
        source_run.id, name="Synced School", phone="+923005552222", lat=31.5, lng=74.3
    )
    db_session.add(b)
    await db_session.flush()

    resync_ids: set = set()
    result = await resolve_incoming_record(db_session, b, resync_ids=resync_ids)

    assert result is not None
    assert result.id == institution.id
    assert resync_ids == {institution.id}


@pytest.mark.asyncio
async def test_attach_to_never_synced_institution_does_not_add_resync_id(db_session, source_run):
    # The common case: an institution that originated from automated
    # ingestion (never offered to lead_sync at all, lead_synced_at is None)
    # shouldn't be introduced into core-newax for the first time just
    # because a later automated record attaches to it -- that's a separate,
    # bigger scope decision (see docs/ROADMAP.md), not this fix.
    a = google_places_record(
        source_run.id, name="Unsynced School", phone="+923005553333", lat=31.5, lng=74.3
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()
    assert institution.lead_synced_at is None

    b = google_places_record(
        source_run.id, name="Unsynced School", phone="+923005554444", lat=31.5, lng=74.3
    )
    db_session.add(b)
    await db_session.flush()

    resync_ids: set = set()
    result = await resolve_incoming_record(db_session, b, resync_ids=resync_ids)

    assert result is not None
    assert result.id == institution.id
    assert resync_ids == set()


@pytest.mark.asyncio
async def test_pending_leaves_record_unresolved(db_session, source_run):
    a = google_places_record(source_run.id, name="Phone Sharing School A", phone="+923001010101")
    b = google_places_record(source_run.id, name="Phone Sharing School B", phone="+923001010101")
    db_session.add_all([a, b])
    await db_session.flush()

    pending_assessment = MatchAssessment(
        candidate_id=None,
        name_similarity=0.0,
        distance_meters=None,
        phone_match=True,
        domain_match=False,
        total_score=65.0,
        decision=MatchDecision.PENDING,
    )

    async def fake_score_candidate(session, candidate):
        pending_assessment.candidate_id = candidate.id
        session.add(pending_assessment)
        return pending_assessment

    with patch(
        "lead_harvester.resolution.orchestrator.score_candidate",
        new=AsyncMock(side_effect=fake_score_candidate),
    ):
        result = await resolve_incoming_record(db_session, b)

    assert result is None
    assert await find_canonical_for_raw_record(db_session, b.id) is None


@pytest.mark.asyncio
async def test_merge_deferred_when_a_pending_candidate_also_exists(db_session, source_run):
    # incoming matches two unresolved targets sharing its phone: x scores a
    # confident MERGE, y scores PENDING (ambiguous). Auto-merging into x
    # while y's ambiguity is unresolved would hide that conflict -- once
    # merged, list_pending()'s already-canonicalized exclusion would drop
    # y's own candidate from the review queue too, even though nothing
    # about y was actually decided by a human.
    incoming = google_places_record(source_run.id, name="Ambiguous School", phone="+923006667777")
    x = google_places_record(source_run.id, name="Ambiguous School", phone="+923006667777")
    y = google_places_record(source_run.id, name="Ambiguous School Two", phone="+923006667777")
    db_session.add_all([incoming, x, y])
    await db_session.flush()

    async def fake_score_candidate(session, candidate):
        if candidate.target_raw_record_id == x.id:
            decision, score = MatchDecision.MERGE, 100.0
        else:
            decision, score = MatchDecision.PENDING, 65.0
        assessment = MatchAssessment(
            candidate_id=candidate.id,
            name_similarity=0.9,
            distance_meters=None,
            phone_match=True,
            domain_match=False,
            total_score=score,
            decision=decision,
        )
        session.add(assessment)
        return assessment

    with patch(
        "lead_harvester.resolution.orchestrator.score_candidate",
        new=AsyncMock(side_effect=fake_score_candidate),
    ):
        result = await resolve_incoming_record(db_session, incoming)

    assert result is None
    assert await find_canonical_for_raw_record(db_session, incoming.id) is None
    assert await find_canonical_for_raw_record(db_session, x.id) is None


@pytest.mark.asyncio
async def test_merge_blocked_when_target_has_its_own_pending_conflict(db_session, source_run):
    # b is a confident MERGE target for the incoming record, but b ITSELF
    # already has an unresolved conflict (b vs c, still PENDING, nobody has
    # reviewed it). Auto-merging incoming into b now would canonicalize b
    # for the first time, and list_pending's already-canonicalized
    # exclusion would then silently drop the b/c candidate from the review
    # queue -- hiding a genuine ambiguity nobody actually decided. Same
    # guard the human-decision path (ResolutionService._apply_decision)
    # already applies.
    from lead_harvester.api.errors import TargetHasPendingConflictError
    from lead_harvester.models.resolution import ResolutionCandidate

    b = google_places_record(
        source_run.id, name="Contested School", phone="+923008889999", lat=24.86, lng=67.00
    )
    c = google_places_record(source_run.id, name="Some Other School", phone="+923001234567")
    db_session.add_all([b, c])
    await db_session.flush()

    existing_candidate = ResolutionCandidate(
        raw_record_id=b.id,
        target_raw_record_id=c.id,
        blocking_strategy="phone",
        version=1,
    )
    db_session.add(existing_candidate)
    await db_session.flush()
    db_session.add(
        MatchAssessment(
            candidate_id=existing_candidate.id,
            name_similarity=0.5,
            distance_meters=None,
            phone_match=False,
            domain_match=False,
            total_score=60.0,
            decision=MatchDecision.PENDING,
        )
    )
    await db_session.flush()

    incoming = google_places_record(
        source_run.id, name="Contested School", phone="+923008889999", lat=24.86, lng=67.00
    )
    db_session.add(incoming)
    await db_session.flush()

    with pytest.raises(TargetHasPendingConflictError):
        await resolve_incoming_record(db_session, incoming)

    assert await find_canonical_for_raw_record(db_session, b.id) is None
    assert await find_canonical_for_raw_record(db_session, incoming.id) is None

    # b's own existing conflict must remain untouched -- still visible for
    # a human to actually decide.
    await db_session.refresh(existing_candidate)
    assert existing_candidate.review_outcome is None


@pytest.mark.asyncio
async def test_resolve_incoming_record_refreshes_the_lead_profile(db_session, source_run):
    # Every institution-producing branch of resolve_incoming_record must
    # call refresh_lead_profile so a new/attached record's contactability
    # is reflected immediately, not left stale until something else happens
    # to touch this institution.
    record = google_places_record(
        source_run.id, name="Profiled School", phone="+923004445555", lat=1.0, lng=1.0
    )
    db_session.add(record)
    await db_session.flush()

    institution = await resolve_incoming_record(db_session, record)

    profile = (
        await db_session.execute(
            select(LeadProfile).where(LeadProfile.institution_id == institution.id)
        )
    ).scalar_one_or_none()
    assert profile is not None
    assert profile.has_phone is True


@pytest.mark.asyncio
async def test_link_only_creates_own_institution(db_session, source_run):
    # Same phone number, but different names and far apart -- shared
    # contact detail, not the same physical entity (e.g. a franchise chain).
    a = google_places_record(
        source_run.id,
        name="Franchise Branch One",
        phone="+923002020202",
        lat=24.86,
        lng=67.00,
    )
    b = google_places_record(
        source_run.id,
        name="Completely Different Name",
        phone="+923002020202",
        lat=31.5,
        lng=74.3,
    )
    db_session.add(a)
    await db_session.flush()
    inst_a = await resolve_incoming_record(db_session, a)

    db_session.add(b)
    await db_session.flush()
    inst_b = await resolve_incoming_record(db_session, b)

    assert inst_b is not None
    assert inst_b.id != inst_a.id


@pytest.mark.asyncio
async def test_job_sector_hint_applies_only_when_institution_type_leaves_it_unclassified(
    db_session, source_run
):
    # docs/ROADMAP.md module 16: job.yaml's `sector` hint is a fallback,
    # never overriding institution_type-based classification.
    hospitality = Sector(code="hospitality", display_name="Hospitality", institution_types=[])
    db_session.add(hospitality)
    await db_session.flush()

    # No sector configured with institution_type "school" -- classification
    # inside merge_records leaves this institution unclassified, so the
    # hint should apply.
    record = google_places_record(source_run.id, name="Unclassified School", lat=5.0, lng=5.0)
    db_session.add(record)
    await db_session.flush()

    institution = await resolve_incoming_record(db_session, record, job_sector_hint="hospitality")

    assert institution is not None
    assert institution.sector_id == hospitality.id


@pytest.mark.asyncio
async def test_job_sector_hint_never_overrides_institution_type_classification(
    db_session, source_run
):
    education = Sector(code="education", display_name="Education", institution_types=["school"])
    hospitality = Sector(code="hospitality", display_name="Hospitality", institution_types=[])
    db_session.add_all([education, hospitality])
    await db_session.flush()

    record = google_places_record(source_run.id, name="Classified School", lat=6.0, lng=6.0)
    db_session.add(record)
    await db_session.flush()

    institution = await resolve_incoming_record(db_session, record, job_sector_hint="hospitality")

    assert institution is not None
    assert institution.sector_id == education.id
