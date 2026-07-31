import uuid
from datetime import UTC, datetime, timedelta

import pytest

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.compliance import (
    DeletionRequestStatus,
    DeletionSubjectType,
    SuppressionReason,
)
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.services.compliance_service import (
    add_suppression,
    find_applicable_suppression,
    fulfill_deletion,
    is_eligible_to_contact,
    list_deletion_requests,
    list_suppressions,
    normalize_contact_value,
    purge_expired_raw_records,
    reject_deletion,
    remove_suppression,
    request_deletion,
)


def test_normalize_contact_value_handles_email_phone_and_linkedin_url():
    assert normalize_contact_value("Jane@Example.com") == "jane@example.com"
    assert normalize_contact_value("+92 300 1234567") == "+923001234567"
    assert (
        normalize_contact_value("HTTPS://linkedin.com/in/JaneDoe/")
        == "https://linkedin.com/in/janedoe"
    )


@pytest.mark.asyncio
async def test_add_and_find_suppression_blanket_channel(db_session):
    await add_suppression(
        db_session, "jane@example.com", SuppressionReason.OPT_OUT, note="unsubscribed"
    )

    found = await find_applicable_suppression(db_session, "Jane@Example.com", channel="email")
    assert found is not None
    assert found.reason == SuppressionReason.OPT_OUT


@pytest.mark.asyncio
async def test_find_suppression_returns_none_when_not_suppressed(db_session):
    found = await find_applicable_suppression(db_session, "nobody@example.com", channel="email")
    assert found is None


@pytest.mark.asyncio
async def test_is_eligible_to_contact_respects_channel_scoping(db_session):
    await add_suppression(
        db_session, "jane@example.com", SuppressionReason.BOUNCED, channel="email"
    )

    email_result = await is_eligible_to_contact(db_session, "jane@example.com", "email")
    linkedin_result = await is_eligible_to_contact(db_session, "jane@example.com", "linkedin")

    assert email_result.eligible is False
    assert linkedin_result.eligible is True


@pytest.mark.asyncio
async def test_remove_suppression_un_suppresses_the_contact(db_session):
    entry = await add_suppression(db_session, "jane@example.com", SuppressionReason.MANUAL)

    await remove_suppression(db_session, entry.id)

    found = await find_applicable_suppression(db_session, "jane@example.com", channel="email")
    assert found is None


@pytest.mark.asyncio
async def test_remove_suppression_raises_not_found(db_session):
    with pytest.raises(ResourceNotFoundError):
        await remove_suppression(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_list_suppressions_returns_most_recent_first(db_session):
    await add_suppression(db_session, "a@example.com", SuppressionReason.MANUAL)
    await add_suppression(db_session, "b@example.com", SuppressionReason.MANUAL)

    entries = await list_suppressions(db_session)

    assert len(entries) == 2
    assert entries[0].suppressed_at >= entries[1].suppressed_at


@pytest.mark.asyncio
async def test_fulfill_deletion_deletes_the_institution(db_session):
    institution = CanonicalInstitution(canonical_name="To Be Deleted School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id

    request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, institution_id, "GDPR request"
    )

    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.status == DeletionRequestStatus.COMPLETED
    assert fulfilled.fulfilled_at is not None
    remaining = await db_session.get(CanonicalInstitution, institution_id)
    assert remaining is None


@pytest.mark.asyncio
async def test_fulfill_deletion_deletes_a_single_contact_point(db_session):
    institution = CanonicalInstitution(canonical_name="Contact Deletion School")
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.flush()
    contact_id = contact.id

    request = await request_deletion(db_session, DeletionSubjectType.CONTACT_POINT, contact_id)
    await fulfill_deletion(db_session, request.id)

    remaining_contact = await db_session.get(ContactPoint, contact_id)
    assert remaining_contact is None
    # The institution itself is untouched -- only the one contact was deleted.
    remaining_institution = await db_session.get(CanonicalInstitution, institution.id)
    assert remaining_institution is not None


@pytest.mark.asyncio
async def test_fulfill_deletion_raises_not_found_for_unknown_request(db_session):
    with pytest.raises(ResourceNotFoundError):
        await fulfill_deletion(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_fulfill_deletion_raises_not_found_when_subject_already_gone(db_session):
    institution = CanonicalInstitution(canonical_name="Already Gone School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_id)
    await db_session.delete(institution)
    await db_session.flush()

    with pytest.raises(ResourceNotFoundError):
        await fulfill_deletion(db_session, request.id)


@pytest.mark.asyncio
async def test_fulfill_an_already_fulfilled_request_raises(db_session):
    institution = CanonicalInstitution(canonical_name="Double Fulfill School")
    db_session.add(institution)
    await db_session.flush()
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution.id)
    await fulfill_deletion(db_session, request.id)

    with pytest.raises(ValueError, match="not pending"):
        await fulfill_deletion(db_session, request.id)


@pytest.mark.asyncio
async def test_reject_deletion_marks_it_rejected_without_deleting_anything(db_session):
    institution = CanonicalInstitution(canonical_name="Rejected Deletion School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_id)

    rejected = await reject_deletion(db_session, request.id, "insufficient verification")

    assert rejected.status == DeletionRequestStatus.REJECTED
    assert rejected.rejection_reason == "insufficient verification"
    remaining = await db_session.get(CanonicalInstitution, institution_id)
    assert remaining is not None


@pytest.mark.asyncio
async def test_list_deletion_requests_filters_by_status(db_session):
    institution = CanonicalInstitution(canonical_name="Filter Test School")
    db_session.add(institution)
    await db_session.flush()
    pending_request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, uuid.uuid4()
    )
    completed_request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, institution.id
    )
    await fulfill_deletion(db_session, completed_request.id)

    pending = await list_deletion_requests(db_session, status=DeletionRequestStatus.PENDING)
    completed = await list_deletion_requests(db_session, status=DeletionRequestStatus.COMPLETED)

    assert {r.id for r in pending} == {pending_request.id}
    assert {r.id for r in completed} == {completed_request.id}


async def _seed_raw_record(db_session, *, extracted_at, with_provenance: bool) -> RawSourceRecord:
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
        extracted_at=extracted_at,
    )
    db_session.add(record)
    await db_session.flush()
    if with_provenance:
        institution = CanonicalInstitution(canonical_name="Referenced School")
        db_session.add(institution)
        await db_session.flush()
        db_session.add(
            FieldProvenance(
                canonical_id=institution.id,
                raw_record_id=record.id,
                field_name="branch_membership",
                asserted_value=record.source_id,
            )
        )
        await db_session.flush()
    return record


@pytest.mark.asyncio
async def test_purge_expired_raw_records_deletes_only_old_unreferenced_rows(db_session):
    old_unreferenced = await _seed_raw_record(
        db_session,
        extracted_at=datetime.now(UTC) - timedelta(days=400),
        with_provenance=False,
    )
    old_referenced = await _seed_raw_record(
        db_session,
        extracted_at=datetime.now(UTC) - timedelta(days=400),
        with_provenance=True,
    )
    recent_unreferenced = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC), with_provenance=False
    )

    deleted_count = await purge_expired_raw_records(db_session, retention_days=365)

    assert deleted_count == 1
    assert await db_session.get(RawSourceRecord, old_unreferenced.id) is None
    assert await db_session.get(RawSourceRecord, old_referenced.id) is not None
    assert await db_session.get(RawSourceRecord, recent_unreferenced.id) is not None
