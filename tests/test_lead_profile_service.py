import uuid

import pytest
from sqlalchemy import select

from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.profile import (
    LeadProfile,
    LeadScoreSnapshot,
    SizeTier,
    WebsiteQualityTier,
)
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import RawPageSnapshot, RawSourceRecord, SourceRun, SourceType
from lead_harvester.services.lead_profile_service import (
    get_lead_profile,
    get_lead_score_history,
    list_lead_profiles,
    qualify_all_unassessed,
    qualify_and_refresh,
    recompute_all_lead_profiles,
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
async def test_refresh_computes_size_tier_from_branches(db_session):
    institution = await _seed_institution(db_session)
    for i in range(5):
        db_session.add(
            Branch(
                institution_id=institution.id,
                branch_name=f"Campus {i}",
                city="Lahore",
                country_code="PK",
            )
        )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.size_tier == SizeTier.LARGE


@pytest.mark.asyncio
async def test_refresh_computes_operational_maturity_from_signals(db_session):
    institution = await _seed_institution(db_session, website=None)
    db_session.add(
        Signal(institution_id=institution.id, signal_type=SignalType.PAIN_POINT, signal_text="x")
    )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    # baseline 50, no website bonus, one pain point penalty (-15) = 35
    assert profile.operational_maturity_score == 35


@pytest.mark.asyncio
async def test_refresh_website_quality_none_when_no_website(db_session):
    institution = await _seed_institution(db_session, website=None)

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.website_quality_tier == WebsiteQualityTier.NONE
    # Fully missing website (1.0) + no LMS signal (1.0), SMALL size multiplier.
    assert profile.service_gap_score == 2.0


@pytest.mark.asyncio
async def test_refresh_computes_website_quality_from_own_crawled_snapshots(db_session):
    institution = await _seed_institution(db_session)

    run = SourceRun(source_type=SourceType.WEBSITE)
    db_session.add(run)
    await db_session.flush()

    full_html = (
        '<html><head><meta name="viewport" content="width=device-width"></head>'
        "<body><form action='/contact'></form></body></html>"
    )
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id="https://riverside.edu",
        raw_payload={},
        normalized_domain="riverside.edu",
    )
    db_session.add(record)
    await db_session.flush()
    for _ in range(6):
        db_session.add(
            RawPageSnapshot(
                source_run_id=run.id,
                url="https://riverside.edu",
                final_url="https://riverside.edu",
                normalized_domain="riverside.edu",
                raw_source_record_id=record.id,
                institution_id=institution.id,
                html=full_html,
            )
        )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.website_quality_tier == WebsiteQualityTier.EXCEPTIONAL


@pytest.mark.asyncio
async def test_refresh_does_not_score_a_snapshot_with_no_institution_link(db_session):
    # Correction regression test: a RawPageSnapshot whose institution_id
    # is still NULL (predates the linkage fix, or its domain's record
    # never resolved) must be excluded, not guessed into scope via
    # source_run_id membership alone.
    institution = await _seed_institution(db_session)

    run = SourceRun(source_type=SourceType.WEBSITE)
    db_session.add(run)
    await db_session.flush()

    full_html = (
        '<html><head><meta name="viewport" content="width=device-width"></head>'
        "<body><form action='/contact'></form></body></html>"
    )
    for _ in range(6):
        db_session.add(
            RawPageSnapshot(
                source_run_id=run.id,
                url="https://riverside.edu",
                final_url="https://riverside.edu",
                normalized_domain="riverside.edu",
                # institution_id deliberately left unset.
                html=full_html,
            )
        )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    # Not NONE -- institution.website is still present, so NONE isn't
    # forced (that's only for an institution with no site at all, see
    # compute_website_quality_tier's own docstring); the unlinked
    # snapshots are simply invisible to the corrected query, same as if
    # zero pages had ever been crawled at all (https-only credit, no
    # depth/broken-link bonus since page_count is 0).
    assert profile.website_quality_tier == WebsiteQualityTier.POOR


@pytest.mark.asyncio
async def test_refresh_never_scores_a_different_institutions_snapshots_from_the_same_run(
    db_session,
):
    # Correction regression test: WebCrawler.crawl() fetches every seed
    # domain in one call, so one SourceRun's snapshots span multiple
    # institutions -- this institution's own snapshots are POOR (no
    # https/viewport/form/depth), while a same-run sibling institution's
    # snapshots are a fully-featured EXCEPTIONAL site. Scoping by
    # source_run_id alone (the bug this correction fixes) would leak the
    # sibling's high-quality pages into this institution's score.
    # http (not https) + a single bare page + no depth/broken-link penalty
    # scores POOR (0 https + 0 viewport + 0 form + 0 depth + 2 low-broken =
    # 2, below the ADEQUATE threshold of 3) -- see
    # intelligence/website_quality.py's point weights.
    institution = await _seed_institution(db_session, website="http://riverside.edu")
    other_institution = await _seed_institution(
        db_session, canonical_name="Lakeside Academy", website="https://lakeside.edu"
    )

    run = SourceRun(source_type=SourceType.WEBSITE)
    db_session.add(run)
    await db_session.flush()

    riverside_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id="https://riverside.edu",
        raw_payload={},
        normalized_domain="riverside.edu",
    )
    lakeside_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id="https://lakeside.edu",
        raw_payload={},
        normalized_domain="lakeside.edu",
    )
    db_session.add_all([riverside_record, lakeside_record])
    await db_session.flush()

    full_html = (
        '<html><head><meta name="viewport" content="width=device-width"></head>'
        "<body><form action='/contact'></form></body></html>"
    )
    db_session.add(
        RawPageSnapshot(
            source_run_id=run.id,
            url="https://riverside.edu",
            final_url="https://riverside.edu",
            normalized_domain="riverside.edu",
            raw_source_record_id=riverside_record.id,
            institution_id=institution.id,
            html="<html><body>bare page, no viewport/form</body></html>",
        )
    )
    for _ in range(6):
        db_session.add(
            RawPageSnapshot(
                source_run_id=run.id,
                url="https://lakeside.edu",
                final_url="https://lakeside.edu",
                normalized_domain="lakeside.edu",
                raw_source_record_id=lakeside_record.id,
                institution_id=other_institution.id,
                html=full_html,
            )
        )
    await db_session.flush()

    riverside_profile = await refresh_lead_profile(db_session, institution.id)
    lakeside_profile = await refresh_lead_profile(db_session, other_institution.id)

    assert riverside_profile.website_quality_tier == WebsiteQualityTier.POOR
    assert lakeside_profile.website_quality_tier == WebsiteQualityTier.EXCEPTIONAL


@pytest.mark.asyncio
async def test_refresh_computes_icp_match_score_from_settings(db_session, monkeypatch):
    from lead_harvester.services import lead_profile_service as service_module

    monkeypatch.setattr(service_module.app_settings, "icp_target_institution_types", ["school"])
    monkeypatch.setattr(service_module.app_settings, "icp_min_branch_count", 0)
    institution = await _seed_institution(db_session, institution_type="school")

    profile = await refresh_lead_profile(db_session, institution.id)

    assert profile.icp_match_score == 100


@pytest.mark.asyncio
async def test_refresh_summarizes_signals_when_no_ai_summary_exists(db_session):
    institution = await _seed_institution(db_session)
    db_session.add(
        Signal(
            institution_id=institution.id,
            signal_type=SignalType.PAIN_POINT,
            signal_text="uses whatsapp with no booking portal",
        )
    )
    await db_session.flush()

    profile = await refresh_lead_profile(db_session, institution.id)

    assert "pain point" in profile.organization_summary
    assert "uses whatsapp with no booking portal" in profile.organization_summary


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


@pytest.mark.asyncio
async def test_recompute_all_lead_profiles_only_touches_institutions_with_a_profile(db_session):
    profiled = await _seed_institution(db_session, canonical_name="Already Profiled School")
    await refresh_lead_profile(db_session, profiled.id)
    never_profiled = await _seed_institution(db_session, canonical_name="Never Profiled School")
    await db_session.flush()

    count = await recompute_all_lead_profiles(db_session)

    assert count == 1
    assert await get_lead_profile(db_session, never_profiled.id) is None


@pytest.mark.asyncio
async def test_recompute_all_lead_profiles_recomputes_website_quality(db_session):
    # The direct remediation this correction requires: a profile computed
    # before the RawPageSnapshot institution_id fix must pick up the
    # corrected (now-empty, since these snapshots predate the link) score
    # on recompute rather than keeping whatever it was scored as before.
    institution = await _seed_institution(db_session, website="https://riverside.edu")
    profile = await refresh_lead_profile(db_session, institution.id)
    # Simulate a stale/untrusted pre-correction score sitting in the DB.
    profile.website_quality_tier = WebsiteQualityTier.EXCEPTIONAL
    await db_session.flush()

    count = await recompute_all_lead_profiles(db_session)

    assert count == 1
    recomputed = await get_lead_profile(db_session, institution.id)
    assert recomputed.website_quality_tier == WebsiteQualityTier.POOR


@pytest.mark.asyncio
async def test_recompute_all_lead_profiles_isolates_one_institutions_failure(
    db_session, monkeypatch
):
    good_one = await _seed_institution(db_session, canonical_name="Good School One")
    await refresh_lead_profile(db_session, good_one.id)
    bad_one = await _seed_institution(db_session, canonical_name="Bad School")
    await refresh_lead_profile(db_session, bad_one.id)
    good_two = await _seed_institution(db_session, canonical_name="Good School Two")
    await refresh_lead_profile(db_session, good_two.id)

    from lead_harvester.services import lead_profile_service as service_module

    real_refresh_lead_profile = service_module.refresh_lead_profile

    async def flaky_refresh_lead_profile(session, institution_id, **kwargs):
        if institution_id == bad_one.id:
            raise RuntimeError("simulated recompute failure")
        return await real_refresh_lead_profile(session, institution_id, **kwargs)

    monkeypatch.setattr(service_module, "refresh_lead_profile", flaky_refresh_lead_profile)

    count = await recompute_all_lead_profiles(db_session)

    assert count == 2


@pytest.mark.asyncio
async def test_recompute_all_lead_profiles_advances_past_a_persistently_failing_profile(
    db_session, monkeypatch
):
    # Correction regression test: a profile whose refresh keeps failing
    # must not stay at the front of the computed_at-ascending ordering
    # forever -- otherwise every subsequent bounded call re-selects the
    # same failure and never reaches a later untrusted-but-healthy
    # profile behind it. computed_at should advance even on failure (the
    # score fields themselves stay untouched).
    bad_one = await _seed_institution(db_session, canonical_name="Persistently Bad School")
    await refresh_lead_profile(db_session, bad_one.id)
    healthy_two = await _seed_institution(db_session, canonical_name="Healthy School Two")
    await refresh_lead_profile(db_session, healthy_two.id)

    original_computed_at = (await get_lead_profile(db_session, bad_one.id)).computed_at

    from lead_harvester.services import lead_profile_service as service_module

    real_refresh_lead_profile = service_module.refresh_lead_profile

    async def flaky_refresh_lead_profile(session, institution_id, **kwargs):
        if institution_id == bad_one.id:
            raise RuntimeError("simulated persistent recompute failure")
        return await real_refresh_lead_profile(session, institution_id, **kwargs)

    monkeypatch.setattr(service_module, "refresh_lead_profile", flaky_refresh_lead_profile)

    # Bounded to 1 -- without the fix, this always re-selects bad_one
    # (oldest computed_at) and healthy_two is never reached across
    # repeated calls.
    first_call_count = await recompute_all_lead_profiles(db_session, limit=1)
    second_call_count = await recompute_all_lead_profiles(db_session, limit=1)

    assert first_call_count == 0
    assert second_call_count == 1

    bad_profile = await get_lead_profile(db_session, bad_one.id)
    assert bad_profile.computed_at > original_computed_at
