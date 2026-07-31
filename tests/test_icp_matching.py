from lead_harvester.config import Settings
from lead_harvester.intelligence.icp_matching import score_icp_fit
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.sector import Sector


def _institution(institution_type: str = "school") -> CanonicalInstitution:
    return CanonicalInstitution(canonical_name="Example School", institution_type=institution_type)


def _sector(**icp_criteria) -> Sector:
    return Sector(
        code="education",
        display_name="Education",
        institution_types=["school"],
        icp_criteria=icp_criteria,
        qualification_rules={},
    )


def test_no_criteria_configured_gives_neutral_credit_for_both():
    settings = Settings(icp_target_institution_types=[], icp_min_branch_count=0)
    score = score_icp_fit(_institution(), branch_count=1, settings=settings)
    assert score == 70  # 30 (type unstated) + 40 (branch count unstated)


def test_matching_institution_type_scores_full_type_credit():
    settings = Settings(icp_target_institution_types=["school"], icp_min_branch_count=0)
    score = score_icp_fit(_institution("school"), branch_count=1, settings=settings)
    assert score == 100  # 60 (type match) + 40 (branch count unstated)


def test_non_matching_institution_type_scores_zero_type_credit():
    settings = Settings(icp_target_institution_types=["university"], icp_min_branch_count=0)
    score = score_icp_fit(_institution("school"), branch_count=1, settings=settings)
    assert score == 40  # 0 (type mismatch) + 40 (branch count unstated)


def test_meeting_minimum_branch_count_scores_full_branch_credit():
    settings = Settings(icp_target_institution_types=[], icp_min_branch_count=3)
    score = score_icp_fit(_institution(), branch_count=5, settings=settings)
    assert score == 70  # 30 (type unstated) + 40 (branch count met)


def test_missing_minimum_branch_count_scores_zero_branch_credit():
    settings = Settings(icp_target_institution_types=[], icp_min_branch_count=3)
    score = score_icp_fit(_institution(), branch_count=1, settings=settings)
    assert score == 30  # 30 (type unstated) + 0 (branch count missed)


def test_full_match_on_both_criteria_scores_100():
    settings = Settings(icp_target_institution_types=["school"], icp_min_branch_count=2)
    score = score_icp_fit(_institution("school"), branch_count=3, settings=settings)
    assert score == 100


def test_sector_with_empty_icp_criteria_falls_back_to_global_settings():
    # Every seeded sector starts with icp_criteria={} -- this must be a
    # true no-op, not a switch to "unstated" for both criteria.
    settings = Settings(icp_target_institution_types=["university"], icp_min_branch_count=3)
    score = score_icp_fit(
        _institution("school"), branch_count=1, settings=settings, sector=_sector()
    )
    assert score == 0  # matches the global-only non-matching-type/missing-branch-count case


def test_sector_target_institution_types_overrides_global_setting():
    settings = Settings(icp_target_institution_types=["university"], icp_min_branch_count=0)
    sector = _sector(target_institution_types=["school"])

    score = score_icp_fit(_institution("school"), branch_count=1, settings=settings, sector=sector)

    assert score == 100  # sector's own list matches, overriding the non-matching global one


def test_sector_min_branch_count_overrides_global_setting_independently():
    # Only min_branch_count is configured on the sector -- target_institution_types
    # must still fall back to the global setting, not silently reset to unstated.
    settings = Settings(icp_target_institution_types=["school"], icp_min_branch_count=1)
    sector = _sector(min_branch_count=5)

    score = score_icp_fit(_institution("school"), branch_count=2, settings=settings, sector=sector)

    assert score == 60  # 60 (type match, from global) + 0 (branch count missed, from sector)
