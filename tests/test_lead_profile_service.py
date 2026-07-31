import uuid

import pytest
from sqlalchemy import select

from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus
from lead_harvester.services.lead_profile_service import (
    get_lead_profile,
    get_lead_score_history,
    list_lead_profiles,
    qualify_all_unassessed,
    qualify_and_refresh,
    refresh_lead_profile,
)


async def _seed_institution(db_session, **overrides) -> CanonicalInstitution:
    defaults = {
        "canonical_name": "Riverside Academy",
        "institution_type": "school",
        "website": "https://riverside.edu",
        "confidence_score": 90.0,  # 0-100 scale -- see verification/confidence.py
    }
    defaults.update(overrides)
    institution = CanonicalInstitution(**defaults)
    db_session.add(institution)
    await db_session.flush()
    return institution


@pytest.mark.asyncio
async def test_refresh_creates_a_new_profile_when_none_exists(db_session):
    institution = await _seed_institution(db_session)
    db_session.add(
        ContactPoint(
            institution_id=institution.id, contact_type="phone", contact_value="+923001234567"
        )
    )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.institution_id == institution.id
    assert profile.has_phone is True
    assert profile.overall_score > 0

    rows = (
        await db_session.scalars(
            select(LeadProfile).where(LeadProfile.institution_id == institution.id)
        )
    ).all()
    assert len(rows) == 1


@pytest.mark.asyncio
async def test_refresh_upserts_the_existing_profile_instead_of_duplicating(db_session):
    institution = await _seed_institution(db_session)

    await refresh_lead_profile(db_session, institution.id)

    db_session.add(
        ContactPoint(
            institution_id=institution.id, contact_type="email", contact_value="a@riverside.edu"
        )
    )
    await db_session.flush()

    await refresh_lead_profile(db_session, institution.id)

    rows = (
        await db_session.scalars(
            select(LeadProfile).where(LeadProfile.institution_id == institution.id)
        )
    ).all()
    assert len(rows) == 1
    assert rows[0].has_email is True


@pytest.mark.asyncio
async def test_refresh_appends_a_score_history_row_every_call(db_session):
    institution = await _seed_institution(db_session)

    await refresh_lead_profile(db_session, institution.id)
    await refresh_lead_profile(db_session, institution.id)
    await refresh_lead_profile(db_session, institution.id)

    rows = (
        await db_session.scalars(
            select(LeadScoreSnapshot).where(LeadScoreSnapshot.institution_id == institution.id)
        )
    ).all()
    assert len(rows) == 3


@pytest.mark.asyncio
async def test_refresh_raises_for_a_nonexistent_institution(db_session):
    with pytest.raises(ValueError, match="No CanonicalInstitution"):
        await refresh_lead_profile(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_refresh_uses_only_the_most_recent_qualification_assessment(db_session):
    institution = await _seed_institution(db_session)
    db_session.add(
        QualificationAssessment(
            institution_id=institution.id,
            status=QualificationStatus.DISQUALIFIED,
            criteria_version=1,
        )
    )
    await db_session.flush()
    db_session.add(
        QualificationAssessment(
            institution_id=institution.id,
            status=QualificationStatus.QUALIFIED,
            criteria_version=2,
        )
    )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.qualification_status == QualificationStatus.QUALIFIED
    assert profile.score_breakdown["qualification"] == 20


@pytest.mark.asyncio
async def test_qualify_and_refresh_runs_the_agent_and_updates_the_profile(db_session):
    institution = await _seed_institution(db_session, website="https://riverside.edu")

    profile = await qualify_and_refresh(db_session, institution.id)

    assessments = (
        await db_session.scalars(
            select(QualificationAssessment).where(
                QualificationAssessment.institution_id == institution.id
            )
        )
    ).all()
    assert len(assessments) == 1
    assert profile.qualification_status == assessments[0].status


@pytest.mark.asyncio
async def test_qualify_all_unassessed_skips_institutions_already_assessed(db_session):
    assessed = await _seed_institution(db_session, canonical_name="Already Assessed School")
    db_session.add(
        QualificationAssessment(
            institution_id=assessed.id, status=QualificationStatus.QUALIFIED, criteria_version=1
        )
    )
    unassessed = await _seed_institution(db_session, canonical_name="Never Assessed School")
    await db_session.flush()

    count = await qualify_all_unassessed(db_session)

    assert count == 1
    new_assessments = (
        await db_session.scalars(
            select(QualificationAssessment).where(
                QualificationAssessment.institution_id == unassessed.id
            )
        )
    ).all()
    assert len(new_assessments) == 1
    # The already-assessed institution must not get a second assessment.
    assessed_assessments = (
        await db_session.scalars(
            select(QualificationAssessment).where(
                QualificationAssessment.institution_id == assessed.id
            )
        )
    ).all()
    assert len(assessed_assessments) == 1


@pytest.mark.asyncio
async def test_qualify_all_unassessed_isolates_one_institutions_failure(db_session, monkeypatch):
    # Savepoint isolation (docs/CODE_REVIEW_LESSONS.md pattern 3) -- one
    # institution failing mid-batch must not stop the others from being
    # qualified.
    good_one = await _seed_institution(db_session, canonical_name="Good School One")
    bad_one = await _seed_institution(db_session, canonical_name="Bad School")
    good_two = await _seed_institution(db_session, canonical_name="Good School Two")
    await db_session.flush()

    from lead_harvester.services import lead_profile_service as service_module

    real_qualify_and_refresh = service_module.qualify_and_refresh

    async def flaky_qualify_and_refresh(session, institution_id, **kwargs):
        if institution_id == bad_one.id:
            raise RuntimeError("simulated qualification failure")
        return await real_qualify_and_refresh(session, institution_id, **kwargs)

    monkeypatch.setattr(service_module, "qualify_and_refresh", flaky_qualify_and_refresh)

    count = await qualify_all_unassessed(db_session)

    assert count == 2
    for inst in (good_one, good_two):
        assessments = (
            await db_session.scalars(
                select(QualificationAssessment).where(
                    QualificationAssessment.institution_id == inst.id
                )
            )
        ).all()
        assert len(assessments) == 1
    bad_assessments = (
        await db_session.scalars(
            select(QualificationAssessment).where(
                QualificationAssessment.institution_id == bad_one.id
            )
        )
    ).all()
    assert bad_assessments == []


@pytest.mark.asyncio
async def test_list_lead_profiles_ranks_highest_score_first(db_session):
    weak = await _seed_institution(
        db_session, canonical_name="Weak Lead", website=None, confidence_score=0.0
    )
    strong = await _seed_institution(db_session, canonical_name="Strong Lead")
    db_session.add(
        ContactPoint(institution_id=strong.id, contact_type="phone", contact_value="+923001234567")
    )
    db_session.add(Branch(institution_id=strong.id, city="Lahore", country_code="PK"))
    await db_session.flush()

    await refresh_lead_profile(db_session, weak.id)
    await refresh_lead_profile(db_session, strong.id)

    result = await list_lead_profiles(db_session)

    scores_by_name = {item.canonical_name: item.overall_score for item in result.items}
    assert scores_by_name["Strong Lead"] > scores_by_name["Weak Lead"]
    assert result.total == 2


@pytest.mark.asyncio
async def test_list_lead_profiles_filters_by_min_score(db_session):
    weak = await _seed_institution(
        db_session,
        canonical_name="Weak Lead",
        website=None,
        institution_type="",
        confidence_score=0.0,
    )
    strong = await _seed_institution(db_session, canonical_name="Strong Lead")
    db_session.add(
        ContactPoint(institution_id=strong.id, contact_type="phone", contact_value="+923001234567")
    )
    await db_session.flush()
    await refresh_lead_profile(db_session, weak.id)
    await refresh_lead_profile(db_session, strong.id)

    result = await list_lead_profiles(db_session, min_score=1)

    names = {item.canonical_name for item in result.items}
    assert "Strong Lead" in names
    assert "Weak Lead" not in names


@pytest.mark.asyncio
async def test_get_lead_profile_returns_none_when_never_refreshed(db_session):
    institution = await _seed_institution(db_session)

    profile = await get_lead_profile(db_session, institution.id)

    assert profile is None


@pytest.mark.asyncio
async def test_get_lead_score_history_returns_most_recent_first(db_session):
    institution = await _seed_institution(db_session)
    await refresh_lead_profile(db_session, institution.id)
    db_session.add(
        ContactPoint(
            institution_id=institution.id, contact_type="phone", contact_value="+923001234567"
        )
    )
    await db_session.flush()
    await refresh_lead_profile(db_session, institution.id)

    history = await get_lead_score_history(db_session, institution.id)

    assert len(history) == 2
    assert history[0].computed_at >= history[1].computed_at
