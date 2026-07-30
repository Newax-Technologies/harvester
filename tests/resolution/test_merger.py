import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    display_fields,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.models.canonical import Branch, ContactPoint, OperatingStatus
from lead_harvester.models.provenance import FieldProvenance

from .factories import google_places_record, website_record


@pytest.mark.asyncio
async def test_merge_records_creates_separate_branches_by_default(db_session, source_run):
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    b = google_places_record(source_run.id, name="Riverside Academy Annex", phone="+923002222222")
    db_session.add_all([a, b])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b])
    await db_session.flush()

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    branches = result.scalars().all()
    assert len(branches) == 2
    assert {b.branch_name for b in branches} == {"Main Campus", "Additional Campus"}


@pytest.mark.asyncio
async def test_merge_records_maps_google_places_closed_status(db_session, source_run):
    # A permanently closed Google Place must not be canonicalized as
    # OPERATIONAL -- otherwise it can silently proceed into qualification
    # or outreach despite the source data explicitly flagging it closed.
    a = google_places_record(source_run.id, business_status="CLOSED_PERMANENTLY")
    db_session.add(a)
    await db_session.flush()

    institution = await merge_records(db_session, [a])

    assert institution.status == OperatingStatus.CLOSED_PERMANENTLY


@pytest.mark.asyncio
async def test_merge_records_defaults_to_unknown_status_without_source_signal(
    db_session, source_run
):
    # A source with no operating-status signal at all (e.g. a web-crawled
    # record) shouldn't be guessed as OPERATIONAL either.
    a = website_record(source_run.id)
    db_session.add(a)
    await db_session.flush()

    institution = await merge_records(db_session, [a])

    assert institution.status == OperatingStatus.UNKNOWN


@pytest.mark.asyncio
async def test_merge_records_same_location_collapses_to_one_branch(db_session, source_run):
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    b = google_places_record(source_run.id, name="Riverside Academy", phone="+923002222222")
    db_session.add_all([a, b])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b], same_location=True)
    await db_session.flush()

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    branches = result.scalars().all()
    assert len(branches) == 1
    # Same source_type for both records -> provider_ids keeps BOTH source_ids
    # under the shared "google_places" key (a list), so a later run
    # rediscovering either original Place can still find this branch.
    assert branches[0].provider_ids == {"google_places": [a.source_id, b.source_id]}
    assert await find_branch_for_raw_record(db_session, institution.id, a) is not None
    assert await find_branch_for_raw_record(db_session, institution.id, b) is not None


@pytest.mark.asyncio
async def test_merge_records_writes_provenance_even_without_phone(db_session, source_run):
    # A non-primary record with no phone number used to get zero
    # FieldProvenance rows at all, breaking find_canonical_for_raw_record.
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    b = google_places_record(source_run.id, name="Riverside Academy Annex", phone=None)
    db_session.add_all([a, b])
    await db_session.flush()

    institution = await merge_records(db_session, [a, b])
    await db_session.flush()

    canonical_id = await find_canonical_for_raw_record(db_session, b.id)
    assert canonical_id == institution.id


@pytest.mark.asyncio
async def test_display_fields_handles_google_places_shape(source_run):
    record = google_places_record(source_run.id, name="Beacon School", website="https://beacon.edu")
    fields = display_fields(record)
    # The raw display name (original casing) is preferred for presentation;
    # normalized_name is reserved for blocking/scoring's exact-string matches.
    assert fields["name"] == "Beacon School"
    assert fields["address"] == "12 River Road, Lahore"
    assert fields["website"] == "https://beacon.edu"
    assert fields["institution_type"] == "school"


@pytest.mark.asyncio
async def test_display_fields_handles_website_shape(source_run):
    record = website_record(
        source_run.id,
        name="Jane Doe",
        organization="Beacon School",
        website="beacon.edu",
        location_text="Karachi, Pakistan",
    )
    fields = display_fields(record)
    # The raw "organization" value (original casing) is preferred over
    # "name" and over normalized_name for presentation.
    assert fields["name"] == "Beacon School"
    assert fields["address"] == "Karachi, Pakistan"
    assert fields["website"] == "beacon.edu"


@pytest.mark.asyncio
async def test_display_fields_handles_manual_shape(source_run):
    from lead_harvester.models.source import RawSourceRecord, SourceType
    from lead_harvester.resolution.normalize import normalize_name

    # normalized_name is always populated for manual entries too (matches
    # manual_leads.py::create_manual_lead) -- must not shadow the
    # user-entered casing in raw_payload["institution_name"].
    record = RawSourceRecord(
        source_run_id=source_run.id,
        source_type=SourceType.MANUAL,
        source_id="manual:test123",
        raw_payload={"institution_name": "Beacon School", "address": "1 Main St"},
        normalized_name=normalize_name("Beacon School"),
        normalized_phone=None,
        normalized_domain=None,
        location=None,
    )
    fields = display_fields(record)
    assert fields["name"] == "Beacon School"


@pytest.mark.asyncio
async def test_display_fields_prefers_full_website_url_over_bare_domain(source_run):
    # normalized_domain is a bare host ("beacon.edu"), used for blocking, and
    # is truthy whenever a website exists at all -- it must not shadow the
    # full origin ("https://www.beacon.edu") retained in raw_payload, or
    # every website-sourced institution's `website` field becomes a
    # non-usable bare domain instead of an absolute URL.
    record = website_record(source_run.id, name="Beacon School", website="https://www.beacon.edu")
    assert record.normalized_domain == "beacon.edu"  # sanity check on the factory

    fields = display_fields(record)
    assert fields["website"] == "https://www.beacon.edu"


@pytest.mark.asyncio
async def test_find_canonical_for_raw_record_returns_none_when_unresolved(db_session, source_run):
    record = google_places_record(source_run.id)
    db_session.add(record)
    await db_session.flush()

    assert await find_canonical_for_raw_record(db_session, record.id) is None


@pytest.mark.asyncio
async def test_attach_record_to_institution_enriches_existing_branch(db_session, source_run):
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    branch = await find_branch_for_raw_record(db_session, institution.id, a)
    assert branch is not None

    b = google_places_record(source_run.id, name="Riverside Academy", phone="+923002222222")
    db_session.add(b)
    await db_session.flush()

    result_branch = await attach_record_to_institution(
        db_session, b, institution, target_branch=branch
    )
    await db_session.flush()

    assert result_branch.id == branch.id
    assert result_branch.provider_ids["google_places"] == [a.source_id, b.source_id]

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    assert len(result.scalars().all()) == 1

    prov = await db_session.execute(
        select(FieldProvenance).where(FieldProvenance.raw_record_id == b.id)
    )
    assert len(prov.scalars().all()) >= 1


@pytest.mark.asyncio
async def test_attach_record_to_institution_does_not_boost_score_for_duplicate_source(
    db_session, source_run
):
    # Every ingestion run creates a brand new RawSourceRecord row even when
    # re-scraping the exact same Google Place (pipeline.py never dedupes by
    # source_id before inserting) -- so two distinct RawSourceRecord rows
    # sharing the same source_id is the realistic "repeated rediscovery"
    # shape, not a hypothetical. Re-attaching that duplicate evidence must
    # not inflate confidence_score, since it isn't independent evidence.
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()
    assert institution.confidence_score == 10.0

    branch = await find_branch_for_raw_record(db_session, institution.id, a)

    # A second RawSourceRecord row for the exact same Place (identical
    # source_id) from a later rerun.
    duplicate = google_places_record(
        source_run.id, name="Riverside Academy", phone="+923001111111", source_id=a.source_id
    )
    db_session.add(duplicate)
    await db_session.flush()

    await attach_record_to_institution(db_session, duplicate, institution, target_branch=branch)
    await db_session.flush()

    assert branch.provider_ids["google_places"] == [a.source_id]
    assert institution.confidence_score == 10.0


@pytest.mark.asyncio
async def test_attach_record_to_institution_caps_confidence_score_at_100(db_session, source_run):
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()
    institution.confidence_score = 95.0

    b = google_places_record(source_run.id, name="Riverside Academy", phone="+923002222222")
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    assert institution.confidence_score == 100.0


@pytest.mark.asyncio
async def test_attach_record_to_institution_refreshes_operating_status(db_session, source_run):
    # A rediscovered Google Place's businessStatus can change between scrapes
    # -- attach_record_to_institution previously only ever consulted
    # _operating_status when FIRST creating an institution, so a place that
    # later closed permanently kept showing OPERATIONAL indefinitely.
    a = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923001111111",
        business_status="OPERATIONAL",
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()
    assert institution.status == OperatingStatus.OPERATIONAL

    b = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923002222222",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    assert institution.status == OperatingStatus.CLOSED_PERMANENTLY


@pytest.mark.asyncio
async def test_attach_record_to_institution_handles_legacy_scalar_provider_id(
    db_session, source_run
):
    # Branches written before provider_ids became list-valued stored a bare
    # source_id string under the source_type key. list("some-id-string")
    # would shatter that string into one list entry per character --
    # confirm enrichment instead treats the legacy scalar as a single-
    # element list, and that the original record stays findable afterward.
    a = google_places_record(source_run.id, name="Legacy School", phone="+923003333333")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    branch = await find_branch_for_raw_record(db_session, institution.id, a)
    assert branch is not None
    branch.provider_ids = {"google_places": a.source_id}  # simulate legacy scalar shape
    await db_session.flush()

    # The legacy scalar must still be findable by its original record.
    assert (await find_branch_for_raw_record(db_session, institution.id, a)) is not None

    b = google_places_record(source_run.id, name="Legacy School", phone="+923004444444")
    db_session.add(b)
    await db_session.flush()

    result_branch = await attach_record_to_institution(
        db_session, b, institution, target_branch=branch
    )
    await db_session.flush()

    assert result_branch.provider_ids["google_places"] == [a.source_id, b.source_id]
    assert await find_branch_for_raw_record(db_session, institution.id, a) is not None
    assert await find_branch_for_raw_record(db_session, institution.id, b) is not None


@pytest.mark.asyncio
async def test_attach_record_to_institution_creates_new_branch_when_no_target(
    db_session, source_run
):
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    b = google_places_record(
        source_run.id, name="Riverside Academy Branch 2", phone="+923002222222"
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    assert len(result.scalars().all()) == 2


@pytest.mark.asyncio
async def test_attach_record_reuses_existing_contact_point_for_same_phone(db_session, source_run):
    # Overlapping ingestion (e.g. the same place discovered by two
    # overlapping Google Places queries) must not accumulate a duplicate
    # ContactPoint row for the same phone number every time a record
    # attaches to an already-existing institution.
    a = google_places_record(source_run.id, name="Riverside Academy", phone="+923001111111")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    contacts_after_create = (
        (
            await db_session.execute(
                select(ContactPoint).where(ContactPoint.institution_id == institution.id)
            )
        )
        .scalars()
        .all()
    )
    assert len(contacts_after_create) == 1

    b = google_places_record(
        source_run.id, name="Riverside Academy Duplicate Hit", phone="+923001111111"
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    contacts_after_attach = (
        (
            await db_session.execute(
                select(ContactPoint).where(ContactPoint.institution_id == institution.id)
            )
        )
        .scalars()
        .all()
    )
    assert len(contacts_after_attach) == 1  # not 2 -- reused, not duplicated

    # But provenance for the second record's own contribution is still recorded.
    prov = (
        (
            await db_session.execute(
                select(FieldProvenance).where(
                    FieldProvenance.raw_record_id == b.id,
                    FieldProvenance.field_name == "contact_phone",
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(prov) == 1


@pytest.mark.asyncio
async def test_merge_records_creates_email_contact_for_email_only_website_lead(
    db_session, source_run
):
    # An email-only web-crawled lead (no phone) previously got zero
    # ContactPoints at all -- _add_contacts_and_provenance only ever looked
    # at normalized_phone -- making the institution appear uncontactable
    # despite a valid email being present in the raw payload.
    record = website_record(
        source_run.id,
        name="Beacon School",
        organization="Beacon School",
        phone=None,
        email="admissions@beacon.edu",
        website="https://beacon.edu",
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    contacts = (
        (
            await db_session.execute(
                select(ContactPoint).where(ContactPoint.institution_id == institution.id)
            )
        )
        .scalars()
        .all()
    )
    assert len(contacts) == 1
    assert contacts[0].contact_type == "email"
    assert contacts[0].contact_value == "admissions@beacon.edu"
