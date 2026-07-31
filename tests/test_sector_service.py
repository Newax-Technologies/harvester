import pytest
from sqlalchemy import select

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.sector import Sector
from lead_harvester.services.sector_service import (
    apply_sector_hint_fallback,
    classify_all_unclassified,
    classify_institution_sector,
    create_sector,
    get_sector,
    list_sectors,
    resolve_sector_for_institution_type,
    update_sector,
)


async def _seed_sector(db_session, *, code="education", institution_types=None) -> Sector:
    sector = Sector(
        code=code,
        display_name=code.title(),
        institution_types=institution_types or ["school", "college", "university"],
        icp_criteria={},
        qualification_rules={},
    )
    db_session.add(sector)
    await db_session.flush()
    return sector


@pytest.mark.asyncio
async def test_resolve_sector_for_institution_type_matches_case_insensitively(db_session):
    await _seed_sector(db_session, code="education", institution_types=["School", "College"])

    sector = await resolve_sector_for_institution_type(db_session, "school")

    assert sector is not None
    assert sector.code == "education"


@pytest.mark.asyncio
async def test_resolve_sector_for_institution_type_returns_none_for_blank_or_unmatched(
    db_session,
):
    await _seed_sector(db_session)

    assert await resolve_sector_for_institution_type(db_session, "") is None
    assert await resolve_sector_for_institution_type(db_session, "spaceship_dealer") is None


@pytest.mark.asyncio
async def test_classify_institution_sector_sets_sector_id_from_institution_type(db_session):
    sector = await _seed_sector(db_session, code="healthcare", institution_types=["clinic"])
    institution = CanonicalInstitution(canonical_name="Test Clinic", institution_type="clinic")
    db_session.add(institution)
    await db_session.flush()

    await classify_institution_sector(db_session, institution)

    assert institution.sector_id == sector.id


@pytest.mark.asyncio
async def test_classify_institution_sector_is_a_noop_without_a_match(db_session):
    await _seed_sector(db_session, institution_types=["school"])
    institution = CanonicalInstitution(canonical_name="Mystery Co", institution_type="unknown_biz")
    db_session.add(institution)
    await db_session.flush()

    await classify_institution_sector(db_session, institution)

    assert institution.sector_id is None


@pytest.mark.asyncio
async def test_classify_institution_sector_never_reclassifies_an_already_classified_institution(
    db_session,
):
    education = await _seed_sector(db_session, code="education", institution_types=["school"])
    await _seed_sector(db_session, code="healthcare", institution_types=["school"])
    institution = CanonicalInstitution(canonical_name="Ambiguous School", institution_type="school")
    institution.sector_id = education.id
    db_session.add(institution)
    await db_session.flush()

    await classify_institution_sector(db_session, institution)

    assert institution.sector_id == education.id


@pytest.mark.asyncio
async def test_apply_sector_hint_fallback_only_applies_when_unclassified(db_session):
    hinted = await _seed_sector(db_session, code="hospitality", institution_types=[])
    institution = CanonicalInstitution(canonical_name="Unmatched Venue", institution_type="")
    db_session.add(institution)
    await db_session.flush()

    await apply_sector_hint_fallback(db_session, institution, "hospitality")

    assert institution.sector_id == hinted.id


@pytest.mark.asyncio
async def test_apply_sector_hint_fallback_never_overrides_an_already_resolved_sector(db_session):
    education = await _seed_sector(db_session, code="education", institution_types=["school"])
    await _seed_sector(db_session, code="hospitality", institution_types=[])
    institution = CanonicalInstitution(canonical_name="A School", institution_type="school")
    await classify_institution_sector(db_session, institution)
    assert institution.sector_id == education.id

    await apply_sector_hint_fallback(db_session, institution, "hospitality")

    assert institution.sector_id == education.id


@pytest.mark.asyncio
async def test_apply_sector_hint_fallback_noop_for_unknown_hint_code(db_session):
    institution = CanonicalInstitution(canonical_name="Unmatched Venue", institution_type="")
    db_session.add(institution)
    await db_session.flush()

    await apply_sector_hint_fallback(db_session, institution, "not_a_real_sector")

    assert institution.sector_id is None


@pytest.mark.asyncio
async def test_classify_all_unclassified_classifies_matching_institutions_only(db_session):
    sector = await _seed_sector(db_session, code="education", institution_types=["school"])
    matching = CanonicalInstitution(canonical_name="A School", institution_type="school")
    non_matching = CanonicalInstitution(canonical_name="A Shop", institution_type="retail_store")
    db_session.add_all([matching, non_matching])
    await db_session.flush()

    count = await classify_all_unclassified(db_session)

    assert count == 1
    await db_session.refresh(matching)
    await db_session.refresh(non_matching)
    assert matching.sector_id == sector.id
    assert non_matching.sector_id is None


@pytest.mark.asyncio
async def test_list_sectors_returns_all_ordered_by_code(db_session):
    await _seed_sector(db_session, code="zzz_sector")
    await _seed_sector(db_session, code="aaa_sector")

    sectors = await list_sectors(db_session)

    assert [s.code for s in sectors] == ["aaa_sector", "zzz_sector"]


@pytest.mark.asyncio
async def test_get_sector_returns_none_for_unknown_id(db_session):
    import uuid

    assert await get_sector(db_session, uuid.uuid4()) is None


@pytest.mark.asyncio
async def test_create_sector_rejects_a_duplicate_code(db_session):
    await create_sector(db_session, code="finance", display_name="Finance")

    with pytest.raises(ValueError):
        await create_sector(db_session, code="finance", display_name="Finance Again")


@pytest.mark.asyncio
async def test_create_sector_persists_all_fields(db_session):
    sector = await create_sector(
        db_session,
        code="legal",
        display_name="Legal",
        institution_types=["law_firm"],
        icp_criteria={"min_branch_count": 2},
        qualification_rules={"requires_website": True},
    )

    fetched = (await db_session.scalars(select(Sector).where(Sector.id == sector.id))).one()
    assert fetched.institution_types == ["law_firm"]
    assert fetched.icp_criteria == {"min_branch_count": 2}
    assert fetched.qualification_rules == {"requires_website": True}


@pytest.mark.asyncio
async def test_update_sector_raises_not_found_for_unknown_id(db_session):
    import uuid

    with pytest.raises(ResourceNotFoundError):
        await update_sector(db_session, uuid.uuid4(), display_name="Whatever")


@pytest.mark.asyncio
async def test_update_sector_only_changes_provided_fields(db_session):
    sector = await create_sector(
        db_session, code="retail", display_name="Retail", institution_types=["retail_store"]
    )

    updated = await update_sector(db_session, sector.id, display_name="Retail & E-commerce")

    assert updated.display_name == "Retail & E-commerce"
    assert updated.institution_types == ["retail_store"]  # unchanged
