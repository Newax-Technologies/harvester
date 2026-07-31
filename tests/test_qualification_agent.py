import pytest

from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.qualification import QualificationStatus
from lead_harvester.models.sector import Sector
from lead_harvester.qualification.agent import QualificationAgent


async def _institution_with_contact(db_session, **overrides) -> CanonicalInstitution:
    defaults = {"canonical_name": "Test Institution", "institution_type": "school"}
    defaults.update(overrides)
    institution = CanonicalInstitution(**defaults)
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        ContactPoint(institution_id=institution.id, contact_type="phone", contact_value="+92300")
    )
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_disqualifies_an_unreachable_institution(db_session):
    institution = CanonicalInstitution(
        canonical_name="No Contacts School", institution_type="school"
    )
    db_session.add(institution)
    await db_session.flush()

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.DISQUALIFIED
    assert "no contact information" in assessment.rationale.lower()


@pytest.mark.asyncio
async def test_disqualifies_a_permanently_closed_institution(db_session):
    institution = await _institution_with_contact(
        db_session, status=OperatingStatus.CLOSED_PERMANENTLY
    )

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.DISQUALIFIED
    assert "permanently closed" in assessment.rationale.lower()


@pytest.mark.asyncio
async def test_qualifies_a_reachable_operating_institution_with_no_website(db_session):
    institution = await _institution_with_contact(db_session, website=None)

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.QUALIFIED
    assert assessment.is_qualified is True
    assert "website-sale opportunity" in assessment.rationale.lower()
    assert assessment.criteria_checklist["has_website"] is False


@pytest.mark.asyncio
async def test_having_a_website_no_longer_disqualifies(db_session):
    # The whole point of the fix this module builds on: a website is an
    # opportunity signal, never a disqualifying trait.
    institution = await _institution_with_contact(db_session, website="https://example.edu")

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.QUALIFIED
    assert assessment.criteria_checklist["has_website"] is True


@pytest.mark.asyncio
async def test_sector_disqualifying_name_keyword_disqualifies(db_session):
    sector = Sector(
        code="real_estate",
        display_name="Real Estate",
        institution_types=["real_estate_agency"],
        qualification_rules={"disqualifying_name_keywords": ["solo agent"]},
    )
    db_session.add(sector)
    await db_session.flush()
    institution = await _institution_with_contact(
        db_session, canonical_name="Jane's Solo Agent Realty", sector_id=sector.id
    )

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.DISQUALIFIED
    assert "solo agent" in assessment.rationale.lower()
    assert assessment.criteria_checklist["matched_disqualifying_keyword"] == "solo agent"


@pytest.mark.asyncio
async def test_sector_disqualifying_keyword_does_not_affect_non_matching_names(db_session):
    sector = Sector(
        code="real_estate",
        display_name="Real Estate",
        institution_types=["real_estate_agency"],
        qualification_rules={"disqualifying_name_keywords": ["solo agent"]},
    )
    db_session.add(sector)
    await db_session.flush()
    institution = await _institution_with_contact(
        db_session, canonical_name="Big Realty Group", sector_id=sector.id
    )

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.QUALIFIED


@pytest.mark.asyncio
async def test_sector_min_branch_count_disqualifies_below_threshold(db_session):
    sector = Sector(
        code="retail",
        display_name="Retail",
        institution_types=["retail_store"],
        qualification_rules={"min_branch_count": 3},
    )
    db_session.add(sector)
    await db_session.flush()
    institution = await _institution_with_contact(db_session, sector_id=sector.id)
    db_session.add(
        Branch(
            institution_id=institution.id,
            branch_name="Only Branch",
            city="Karachi",
            country_code="PK",
        )
    )
    await db_session.flush()

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.DISQUALIFIED
    assert "minimum branch count" in assessment.rationale.lower()


@pytest.mark.asyncio
async def test_sector_min_branch_count_qualifies_when_met(db_session):
    sector = Sector(
        code="retail",
        display_name="Retail",
        institution_types=["retail_store"],
        qualification_rules={"min_branch_count": 2},
    )
    db_session.add(sector)
    await db_session.flush()
    institution = await _institution_with_contact(db_session, sector_id=sector.id)
    db_session.add_all(
        [
            Branch(
                institution_id=institution.id,
                branch_name="Branch A",
                city="Karachi",
                country_code="PK",
            ),
            Branch(
                institution_id=institution.id,
                branch_name="Branch B",
                city="Karachi",
                country_code="PK",
            ),
        ]
    )
    await db_session.flush()

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.QUALIFIED


@pytest.mark.asyncio
async def test_sector_with_empty_qualification_rules_skips_the_extra_layer(db_session):
    # Every seeded sector starts with qualification_rules={} -- this must
    # be a true no-op, not an implicit disqualifier.
    sector = Sector(code="education", display_name="Education", institution_types=["school"])
    db_session.add(sector)
    await db_session.flush()
    institution = await _institution_with_contact(db_session, sector_id=sector.id)

    assessment = await QualificationAgent().evaluate_institution(db_session, institution)

    assert assessment.status == QualificationStatus.QUALIFIED
    assert assessment.criteria_checklist["sector_code"] == "education"
