import uuid

import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    display_fields,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.models.canonical import Branch, ContactPoint, OperatingStatus, PersonCandidate
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
async def test_merge_records_multi_branch_status_is_not_first_record_wins(db_session, source_run):
    # These two records describe DISTINCT campuses (same_location=False,
    # the default -- each gets its own Branch). Picking whichever record's
    # non-UNKNOWN status happened to come first in the list previously let
    # one arbitrary campus's status represent the whole institution: a
    # closed incoming campus listed first would mark an otherwise-thriving
    # multi-branch institution closed, while an operational campus listed
    # first would conceal a closed sibling entirely. An institution with
    # at least one operational branch is still a live lead overall.
    closed_first = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923001111111",
        business_status="CLOSED_PERMANENTLY",
    )
    operational_second = google_places_record(
        source_run.id,
        name="Riverside Academy Annex",
        phone="+923002222222",
        business_status="OPERATIONAL",
    )
    db_session.add_all([closed_first, operational_second])
    await db_session.flush()

    institution = await merge_records(db_session, [closed_first, operational_second])

    assert institution.status == OperatingStatus.OPERATIONAL

    # Order flipped, and with no operational branch at all, every closed
    # branch must agree before the institution is marked closed.
    closed_a = google_places_record(
        source_run.id,
        name="Sunrise School",
        phone="+923003333333",
        business_status="CLOSED_PERMANENTLY",
    )
    closed_b = google_places_record(
        source_run.id,
        name="Sunrise School Annex",
        phone="+923004444444",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add_all([closed_a, closed_b])
    await db_session.flush()

    all_closed_institution = await merge_records(db_session, [closed_a, closed_b])
    assert all_closed_institution.status == OperatingStatus.CLOSED_PERMANENTLY


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
async def test_merge_records_synthesizes_fields_from_all_merged_records(db_session, source_run):
    # _apply_decision always passes the incoming record first -- if it's
    # sparse (no website/domain/status) while another record being merged
    # in the same group supplies them, that evidence must not be dropped
    # just because it wasn't first in the list.
    sparse = website_record(source_run.id, name="Sparse Site", website=None)
    rich = google_places_record(
        source_run.id,
        name="Sparse Site",
        website="https://sparsesite.example.edu",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add_all([sparse, rich])
    await db_session.flush()
    assert sparse.normalized_domain is None  # sanity check on the factory

    institution = await merge_records(db_session, [sparse, rich])

    assert institution.website == "https://sparsesite.example.edu"
    assert institution.domain == rich.normalized_domain
    assert institution.institution_type == "school"
    assert institution.status == OperatingStatus.CLOSED_PERMANENTLY


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
async def test_merge_records_same_location_synthesizes_branch_fields_from_all_records(
    db_session, source_run
):
    # Mirrors test_merge_records_synthesizes_fields_from_all_merged_records,
    # but for the collapsed Branch's own address/location -- these used to
    # come only from records[0] even when same_location=True collapses the
    # WHOLE group into one shared branch. If the first record in the list
    # is the sparse one (no address text, no location), a richer sibling
    # later in the same group must still supply the branch's address and
    # location instead of silently leaving them blank/null.
    sparse = website_record(source_run.id, name="Riverside Academy", location_text="")
    assert sparse.location is None  # sanity check on the factory
    rich = google_places_record(source_run.id, name="Riverside Academy", lat=24.8607, lng=67.0011)
    db_session.add_all([sparse, rich])
    await db_session.flush()

    institution = await merge_records(db_session, [sparse, rich], same_location=True)
    await db_session.flush()

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    branches = result.scalars().all()
    assert len(branches) == 1
    assert branches[0].address == "12 River Road, Lahore"
    assert branches[0].location is not None


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
async def test_display_fields_handles_authorized_import_shape(source_run):
    from lead_harvester.models.source import RawSourceRecord, SourceType
    from lead_harvester.resolution.normalize import normalize_name

    # Same reasoning as the MANUAL case above -- must not shadow the
    # spreadsheet's original casing in raw_payload["institution_name"].
    record = RawSourceRecord(
        source_run_id=source_run.id,
        source_type=SourceType.AUTHORIZED_IMPORT,
        source_id="license-2026:1",
        raw_payload={
            "institution_name": "Beacon School",
            "address": "1 Main St",
            "city": "Karachi",
            "country_code": "PK",
            "institution_type": "school",
            "contacts": [
                {
                    "contact_type": "email",
                    "contact_value": "admissions@beacon.edu",
                    "person_name": "",
                    "role": "",
                },
                {
                    "contact_type": "whatsapp",
                    "contact_value": "+923001234567",
                    "person_name": "Ali Khan",
                    "role": "Principal",
                },
            ],
        },
        normalized_name=normalize_name("Beacon School"),
        normalized_phone=None,
        normalized_domain=None,
        location=None,
    )
    fields = display_fields(record)
    assert fields["name"] == "Beacon School"
    assert fields["email"] == "admissions@beacon.edu"
    assert fields["institution_type"] == "school"
    assert fields["city"] == "Karachi"
    assert fields["country_code"] == "PK"
    assert len(fields["declared_contacts"]) == 2


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
async def test_attach_record_to_institution_backfills_institution_type(db_session, source_run):
    # A website-first institution has institution_type="" (WEBSITE's
    # display_fields never supplies one). A later Google Places record
    # confirmed to be the same institution DOES supply a primaryType, but
    # that evidence previously stayed stranded in the raw ledger --
    # institution.institution_type (and everything reading it downstream,
    # including sync) stayed permanently blank even after this attach.
    a = website_record(source_run.id, name="Riverside Academy", organization="Riverside Academy")
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()
    assert institution.institution_type == ""

    b = google_places_record(source_run.id, name="Riverside Academy")
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)

    assert institution.institution_type == "school"


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
async def test_attach_record_to_institution_refreshes_operating_status_for_same_branch(
    db_session, source_run
):
    # A rediscovered Google Place's businessStatus can change between scrapes
    # -- attach_record_to_institution previously only ever consulted
    # _operating_status when FIRST creating an institution, so a place that
    # later closed permanently kept showing OPERATIONAL indefinitely. Only
    # meaningful when the new evidence describes the SAME branch/location
    # (target_branch set) -- see the next test for why.
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

    branch = await find_branch_for_raw_record(db_session, institution.id, a)

    b = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923002222222",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=branch)
    await db_session.flush()

    assert institution.status == OperatingStatus.CLOSED_PERMANENTLY


@pytest.mark.asyncio
async def test_attach_record_to_institution_multi_branch_closure_does_not_overwrite_status(
    db_session, source_run
):
    # Branch has no per-branch status column, so once an institution has
    # more than one branch there's no way to re-derive the institution-wide
    # status from every branch's latest state the way
    # _aggregate_institution_status does at creation time. One campus
    # reporting closure (even on its OWN branch, via target_branch) must not
    # silently overwrite the whole institution's status while another
    # campus is still operational.
    a = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923001111111",
        business_status="OPERATIONAL",
    )
    b = google_places_record(
        source_run.id,
        name="Riverside Academy Annex",
        phone="+923002222222",
        business_status="OPERATIONAL",
    )
    db_session.add_all([a, b])
    await db_session.flush()
    institution = await merge_records(db_session, [a, b])
    await db_session.flush()
    assert institution.status == OperatingStatus.OPERATIONAL

    branch_a = await find_branch_for_raw_record(db_session, institution.id, a)

    a_rediscovered = google_places_record(
        source_run.id,
        name="Riverside Academy",
        phone="+923001111111",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add(a_rediscovered)
    await db_session.flush()

    await attach_record_to_institution(
        db_session, a_rediscovered, institution, target_branch=branch_a
    )
    await db_session.flush()

    # Branch A's own closure must not overwrite the institution while
    # Branch B is still (as far as this institution's evidence shows)
    # operational.
    assert institution.status == OperatingStatus.OPERATIONAL


@pytest.mark.asyncio
async def test_attach_record_to_institution_new_branch_does_not_change_institution_status(
    db_session, source_run
):
    # A newly-added DISTINCT branch (target_branch=None) of a multi-campus
    # institution must not overwrite the whole institution's status either
    # way -- one closed campus shouldn't mark an otherwise-active
    # institution closed, and a new active campus shouldn't "reopen" a
    # closed institution's status either.
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
        name="Riverside Academy Annex",
        phone="+923002222222",
        business_status="CLOSED_PERMANENTLY",
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    assert institution.status == OperatingStatus.OPERATIONAL


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


def _authorized_import_record(source_run_id, **payload_overrides):
    from lead_harvester.models.source import RawSourceRecord, SourceType
    from lead_harvester.resolution.normalize import normalize_name

    payload = {
        "institution_name": "Beacon House School",
        "institution_type": "school",
        "website": "",
        "address": "",
        "city": "",
        "country_code": "",
        "country": "",
        "notes": "",
        "source_reference": "license-2026",
        "contacts": [],
    }
    payload.update(payload_overrides)
    return RawSourceRecord(
        source_run_id=source_run_id,
        source_type=SourceType.AUTHORIZED_IMPORT,
        source_id="license-2026:test",
        raw_payload=payload,
        normalized_name=normalize_name(payload["institution_name"]),
        normalized_phone=None,
        normalized_domain=None,
        location=None,
    )


@pytest.mark.asyncio
async def test_merge_records_writes_every_declared_contact_for_authorized_import(
    db_session, source_run
):
    # merger.py's contact-writing path previously only ever wrote a single
    # phone (from normalized_phone) + a single email, discarding any other
    # contact_type (whatsapp/telegram/other) entirely and losing
    # person_name/role even for the phone/email contacts it did keep.
    record = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            },
            {
                "contact_type": "whatsapp",
                "contact_value": "+923009999999",
                "person_name": "",
                "role": "",
            },
        ],
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
    assert {c.contact_type for c in contacts} == {"phone", "whatsapp"}
    phone = next(c for c in contacts if c.contact_type == "phone")
    assert phone.person_name == "Ali Khan"
    assert phone.role == "Principal"


@pytest.mark.asyncio
async def test_add_contact_if_present_enriches_existing_contact_person_name_and_role(
    db_session, source_run
):
    # _add_contact_if_present previously only ever wrote person_name/role on
    # first creation -- a later record supplying (or correcting) that
    # metadata for an already-known contact_type+value left the existing
    # ContactPoint's person_name/role stale forever.
    a = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "",
                "role": "",
            }
        ],
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    contact = (await db_session.execute(select(ContactPoint))).scalar_one()
    assert contact.person_name is None

    b = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            }
        ],
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        )
    ).scalar_one()
    assert contact.person_name == "Ali Khan"
    assert contact.role == "Principal"


@pytest.mark.asyncio
async def test_merge_records_normalizes_declared_phone_contact_to_e164(db_session, source_run):
    # A phone entered in national/formatted form ("0300 1234567") must be
    # stored the same normalized E.164 way record.normalized_phone already
    # is for blocking -- otherwise a later Places/manual record for the
    # same institution storing "+923001234567" is treated as a distinct
    # contact_value by _find_contact_point's exact match, creating a
    # duplicate ContactPoint for the same physical number.
    record = _authorized_import_record(
        source_run.id,
        country_code="PK",
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "0300 1234567",
                "person_name": "",
                "role": "",
            },
        ],
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        )
    ).scalar_one()
    assert contact.contact_type == "phone"
    assert contact.contact_value == "+923001234567"


@pytest.mark.asyncio
async def test_merge_records_populates_branch_city_and_country_code_from_authorized_import(
    db_session, source_run
):
    # _build_branch previously always wrote the UNKNOWN sentinel for
    # city/country_code regardless of what the source actually supplied --
    # display_fields never exposed those fields for _synthesize_branch_fields
    # to pick up, so a valid spreadsheet location was stranded in the raw
    # payload only.
    record = _authorized_import_record(
        source_run.id,
        city="Karachi",
        country_code="PK",
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "",
                "role": "",
            }
        ],
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    branch = (
        await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    ).scalar_one()
    assert branch.city == "Karachi"
    assert branch.country_code == "PK"


@pytest.mark.asyncio
async def test_merge_records_creates_person_candidate_for_named_contact(db_session, source_run):
    record = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            }
        ],
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        )
    ).scalar_one()
    assert contact.person_candidate_id is not None

    candidate = (
        await db_session.execute(
            select(PersonCandidate).where(PersonCandidate.id == contact.person_candidate_id)
        )
    ).scalar_one()
    assert candidate.institution_id == institution.id
    assert candidate.display_name == "Ali Khan"
    assert candidate.normalized_name == "ali khan"
    assert candidate.role == "Principal"


@pytest.mark.asyncio
async def test_merge_records_groups_same_person_across_contact_points(db_session, source_run):
    # docs/ROADMAP.md tracked follow-up #5: the same person named on two
    # different ContactPoint rows for the same institution (their phone
    # from one contact, their email from another, with differing
    # casing/punctuation) previously had no link between them at all --
    # each became an entirely separate, unrelated ContactPoint.
    record = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            },
            {
                "contact_type": "email",
                "contact_value": "ali.khan@beacon.edu",
                "person_name": "ALI  khan.",  # different casing/punctuation, same person
                "role": "",
            },
        ],
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
    assert len(contacts) == 2
    candidate_ids = {c.person_candidate_id for c in contacts}
    assert len(candidate_ids) == 1
    assert None not in candidate_ids

    candidates = (
        (
            await db_session.execute(
                select(PersonCandidate).where(PersonCandidate.institution_id == institution.id)
            )
        )
        .scalars()
        .all()
    )
    assert len(candidates) == 1
    # Role from the first contact is preserved rather than cleared by the
    # second contact's blank role.
    assert candidates[0].role == "Principal"


@pytest.mark.asyncio
async def test_merge_records_creates_separate_person_candidates_for_different_names(
    db_session, source_run
):
    record = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            },
            {
                "contact_type": "whatsapp",
                "contact_value": "+923009999999",
                "person_name": "Sara Malik",
                "role": "Admissions Officer",
            },
        ],
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    candidates = (
        (
            await db_session.execute(
                select(PersonCandidate).where(PersonCandidate.institution_id == institution.id)
            )
        )
        .scalars()
        .all()
    )
    assert {c.display_name for c in candidates} == {"Ali Khan", "Sara Malik"}


@pytest.mark.asyncio
async def test_contact_with_no_person_name_has_no_person_candidate(db_session, source_run):
    record = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "email",
                "contact_value": "info@beacon.edu",
                "person_name": "",
                "role": "",
            }
        ],
    )
    db_session.add(record)
    await db_session.flush()

    institution = await merge_records(db_session, [record])
    await db_session.flush()

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        )
    ).scalar_one()
    assert contact.person_candidate_id is None
    assert (await db_session.execute(select(PersonCandidate))).first() is None


@pytest.mark.asyncio
async def test_backfilling_a_contacts_name_resolves_a_person_candidate(db_session, source_run):
    # A contact created without a person_name (e.g. a bare phone number)
    # later enriched with one by attach_record_to_institution should get
    # linked to a PersonCandidate at that point too, not only on initial
    # creation.
    a = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "",
                "role": "",
            }
        ],
    )
    db_session.add(a)
    await db_session.flush()
    institution = await merge_records(db_session, [a])
    await db_session.flush()

    contact = (await db_session.execute(select(ContactPoint))).scalar_one()
    assert contact.person_candidate_id is None

    b = _authorized_import_record(
        source_run.id,
        contacts=[
            {
                "contact_type": "phone",
                "contact_value": "+923001234567",
                "person_name": "Ali Khan",
                "role": "Principal",
            }
        ],
    )
    db_session.add(b)
    await db_session.flush()

    await attach_record_to_institution(db_session, b, institution, target_branch=None)
    await db_session.flush()

    contact = (
        await db_session.execute(
            select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        )
    ).scalar_one()
    assert contact.person_candidate_id is not None
    candidate = (
        await db_session.execute(
            select(PersonCandidate).where(PersonCandidate.id == contact.person_candidate_id)
        )
    ).scalar_one()
    assert candidate.display_name == "Ali Khan"


@pytest.mark.asyncio
async def test_merge_records_surfaces_crawled_social_profiles_as_contact_points(
    db_session, source_run
):
    # ingestion/web_crawler.py's Lead.social_profiles was extracted from the
    # page and stored in raw_payload, but _add_contacts_and_provenance
    # previously never read that key at all -- a crawled LinkedIn/Instagram
    # link was captured into the raw ledger and then silently dropped,
    # never becoming a ContactPoint.
    record = website_record(
        source_run.id,
        name="Riverside Academy",
        social_profiles=[
            "https://www.LinkedIn.com/company/Riverside/",
            "https://twitter.com/RiversideAcademy",
        ],
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
    by_type = {c.contact_type: c.contact_value for c in contacts}
    assert by_type["linkedin"] == "https://linkedin.com/company/riverside"
    # Folded to the current "x" platform/host, not left as "twitter".
    assert by_type["x"] == "https://x.com/riversideacademy"


def test_display_fields_defaults_social_profiles_to_empty_list():
    record = website_record(uuid.uuid4(), name="No Socials School")
    fields = display_fields(record)
    assert fields["social_profiles"] == []
