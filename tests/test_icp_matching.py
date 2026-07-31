from lead_harvester.config import Settings
from lead_harvester.intelligence.icp_matching import score_icp_fit
from lead_harvester.models.canonical import CanonicalInstitution


def _institution(institution_type: str = "school") -> CanonicalInstitution:
    return CanonicalInstitution(canonical_name="Example School", institution_type=institution_type)


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
