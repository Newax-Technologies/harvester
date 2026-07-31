import csv
import io
import json

import pytest

from lead_harvester.exports import build_lead_export_rows, rows_to_csv, rows_to_json
from lead_harvester.exports.lead_export import LeadExportRow
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.compliance import SuppressionReason
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus
from lead_harvester.services.compliance_service import add_suppression


async def _seed_institution(
    db_session,
    *,
    name: str,
    status: OperatingStatus = OperatingStatus.OPERATIONAL,
    confidence_score: float = 50.0,
    overall_score: int | None = None,
    qualification_status: QualificationStatus | None = None,
    contact_count: int = 1,
) -> CanonicalInstitution:
    institution = CanonicalInstitution(
        canonical_name=name,
        institution_type="school",
        domain=f"{name.lower().replace(' ', '')}.edu",
        website=f"https://{name.lower().replace(' ', '')}.edu",
        status=status,
        confidence_score=confidence_score,
    )
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        Branch(
            institution_id=institution.id,
            branch_name="Main",
            city="Lahore",
            country_code="PK",
            provider_ids={},
        )
    )
    for i in range(contact_count):
        db_session.add(
            ContactPoint(
                institution_id=institution.id,
                contact_type="phone",
                contact_value=f"+9230011122{i:02d}",
                person_name=f"Contact {i}",
                role="Admin",
                is_publicly_listed=True,
            )
        )
    if overall_score is not None or qualification_status is not None:
        db_session.add(
            LeadProfile(
                institution_id=institution.id,
                overall_score=overall_score or 0,
                qualification_status=qualification_status,
            )
        )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_build_lead_export_rows_one_row_per_contact(db_session):
    institution = await _seed_institution(db_session, name="Multi Contact School", contact_count=3)

    rows = await build_lead_export_rows(db_session)

    assert len(rows) == 3
    assert {r.institution_id for r in rows} == {str(institution.id)}
    assert {r.contact_type for r in rows} == {"phone"}
    assert rows[0].branch_count == 1
    assert rows[0].primary_city == "Lahore"
    assert rows[0].primary_country_code == "PK"


@pytest.mark.asyncio
async def test_build_lead_export_rows_filters_by_status(db_session):
    operational = await _seed_institution(db_session, name="Open School")
    await _seed_institution(
        db_session, name="Closed School", status=OperatingStatus.CLOSED_PERMANENTLY
    )

    rows = await build_lead_export_rows(db_session, status=OperatingStatus.OPERATIONAL)

    assert {r.institution_id for r in rows} == {str(operational.id)}


@pytest.mark.asyncio
async def test_build_lead_export_rows_filters_by_min_score(db_session):
    strong = await _seed_institution(db_session, name="Strong Lead School", overall_score=80)
    await _seed_institution(db_session, name="Weak Lead School", overall_score=10)
    await _seed_institution(db_session, name="Unscored School")  # no LeadProfile at all

    rows = await build_lead_export_rows(db_session, min_score=50)

    assert {r.institution_id for r in rows} == {str(strong.id)}


@pytest.mark.asyncio
async def test_build_lead_export_rows_filters_by_qualification_status(db_session):
    qualified = await _seed_institution(
        db_session,
        name="Qualified School",
        overall_score=50,
        qualification_status=QualificationStatus.QUALIFIED,
    )
    await _seed_institution(
        db_session,
        name="Disqualified School",
        overall_score=50,
        qualification_status=QualificationStatus.DISQUALIFIED,
    )

    rows = await build_lead_export_rows(
        db_session, qualification_status=QualificationStatus.QUALIFIED
    )

    assert {r.institution_id for r in rows} == {str(qualified.id)}
    assert rows[0].qualification_status == "qualified"
    assert rows[0].overall_score == 50


@pytest.mark.asyncio
async def test_build_lead_export_rows_marks_suppressed_contacts(db_session):
    await _seed_institution(db_session, name="Suppressed Contact School")
    rows_before = await build_lead_export_rows(db_session)
    assert len(rows_before) == 1
    assert rows_before[0].is_suppressed is False

    await add_suppression(
        db_session, rows_before[0].contact_value, SuppressionReason.OPT_OUT, channel="phone"
    )
    await db_session.flush()

    rows_after = await build_lead_export_rows(db_session)

    assert len(rows_after) == 1
    assert rows_after[0].is_suppressed is True


def test_rows_to_csv_produces_header_and_all_rows():
    rows = [
        LeadExportRow(
            institution_id="inst-1",
            institution_name="Test School",
            institution_type="school",
            domain="test.edu",
            website="https://test.edu",
            operating_status="operational",
            confidence_score=50.0,
            overall_score=70,
            qualification_status="qualified",
            branch_count=1,
            primary_city="Lahore",
            primary_country_code="PK",
            contact_id="contact-1",
            contact_type="phone",
            contact_value="+923001234567",
            person_name="Jane Doe",
            role="Principal",
            is_publicly_listed=True,
            is_suppressed=False,
        )
    ]

    csv_text = rows_to_csv(rows)
    reader = csv.DictReader(io.StringIO(csv_text))
    parsed = list(reader)

    assert len(parsed) == 1
    assert parsed[0]["institution_name"] == "Test School"
    assert parsed[0]["contact_value"] == "+923001234567"
    assert parsed[0]["is_suppressed"] == "False"


def test_rows_to_csv_empty_list_still_has_header():
    csv_text = rows_to_csv([])
    reader = csv.reader(io.StringIO(csv_text))
    header = next(reader)

    assert "institution_id" in header
    assert "contact_value" in header
    with pytest.raises(StopIteration):
        next(reader)


def test_rows_to_json_round_trips():
    rows = [
        LeadExportRow(
            institution_id="inst-1",
            institution_name="Test School",
            institution_type="school",
            domain="test.edu",
            website="https://test.edu",
            operating_status="operational",
            confidence_score=50.0,
            overall_score=None,
            qualification_status=None,
            branch_count=0,
            primary_city="",
            primary_country_code="",
            contact_id="contact-1",
            contact_type="email",
            contact_value="jane@test.edu",
            person_name="",
            role="",
            is_publicly_listed=False,
            is_suppressed=False,
        )
    ]

    parsed = json.loads(rows_to_json(rows))

    assert len(parsed) == 1
    assert parsed[0]["institution_name"] == "Test School"
    assert parsed[0]["overall_score"] is None
    assert parsed[0]["contact_value"] == "jane@test.edu"
