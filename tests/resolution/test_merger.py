import pytest
from sqlalchemy import select

from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    display_fields,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.models.canonical import Branch, ContactPoint
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
    # Same source_type for both records -> provider_ids collapses to one key
    # (last record wins), a documented v1 fragility of the provider_ids dict.
    assert set(branches[0].provider_ids) == {"google_places"}


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
    # normalized_name (lowercased) is preferred over the raw displayName.text
    assert fields["name"] == "beacon school"
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
    # normalized_name is built from organization (preferred over name) and lowercased
    assert fields["name"] == "beacon school"
    assert fields["address"] == "Karachi, Pakistan"
    assert fields["website"] == "beacon.edu"


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
    assert result_branch.provider_ids["google_places"] == b.source_id

    result = await db_session.execute(select(Branch).where(Branch.institution_id == institution.id))
    assert len(result.scalars().all()) == 1

    prov = await db_session.execute(
        select(FieldProvenance).where(FieldProvenance.raw_record_id == b.id)
    )
    assert len(prov.scalars().all()) >= 1


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
