import uuid

from lead_harvester.allocation.eligibility import is_eligible_for_selection, ranking_sort_key
from lead_harvester.models.canonical import OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus


def _profile(**overrides) -> LeadProfile:
    defaults = {
        "institution_id": uuid.uuid4(),
        "overall_score": 50,
        "has_phone": True,
        "has_email": False,
        "qualification_status": None,
    }
    defaults.update(overrides)
    return LeadProfile(**defaults)


def test_eligible_when_operational_with_contact_and_no_disqualification():
    profile = _profile()
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL) is True


def test_ineligible_when_institution_not_operational():
    profile = _profile()
    assert is_eligible_for_selection(profile, OperatingStatus.CLOSED_PERMANENTLY) is False


def test_ineligible_when_disqualified():
    profile = _profile(qualification_status=QualificationStatus.DISQUALIFIED)
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL) is False


def test_eligible_when_needs_review_or_pending_or_never_assessed():
    for status in (QualificationStatus.NEEDS_REVIEW, QualificationStatus.PENDING, None):
        profile = _profile(qualification_status=status)
        assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL) is True


def test_ineligible_below_min_score():
    profile = _profile(overall_score=10)
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL, min_score=20) is False
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL, min_score=10) is True


def test_ineligible_with_no_contact_method():
    profile = _profile(has_phone=False, has_email=False)
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL) is False


def test_eligible_with_only_email_no_phone():
    profile = _profile(has_phone=False, has_email=True)
    assert is_eligible_for_selection(profile, OperatingStatus.OPERATIONAL) is True


def test_ranking_sort_key_orders_by_score_descending():
    high = _profile(overall_score=90)
    low = _profile(overall_score=10)
    assert ranking_sort_key(high) < ranking_sort_key(low)


def test_ranking_sort_key_tiebreaks_deterministically_by_institution_id():
    id_a = uuid.UUID("00000000-0000-0000-0000-000000000001")
    id_b = uuid.UUID("00000000-0000-0000-0000-000000000002")
    a = _profile(institution_id=id_a, overall_score=50)
    b = _profile(institution_id=id_b, overall_score=50)
    assert ranking_sort_key(a) < ranking_sort_key(b)

    # Sorting a shuffled list by this key always produces the same order,
    # regardless of insertion order -- the defining property of a
    # "deterministic" ranking.
    ordered_forward = sorted([a, b], key=ranking_sort_key)
    ordered_backward = sorted([b, a], key=ranking_sort_key)
    assert [p.institution_id for p in ordered_forward] == [
        p.institution_id for p in ordered_backward
    ]
