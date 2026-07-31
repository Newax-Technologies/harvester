from lead_harvester.intelligence.size_estimation import estimate_size_tier
from lead_harvester.models.canonical import Branch, ContactPoint
from lead_harvester.models.profile import SizeTier


def _branches(n: int) -> list[Branch]:
    return [Branch(branch_name=f"Campus {i}") for i in range(n)]


def _contacts(n: int) -> list[ContactPoint]:
    return [ContactPoint(contact_type="email", contact_value=f"{i}@example.edu") for i in range(n)]


def test_no_branches_is_unknown():
    assert estimate_size_tier([], []) == SizeTier.UNKNOWN


def test_one_branch_and_few_contacts_is_small():
    assert estimate_size_tier(_branches(1), _contacts(1)) == SizeTier.SMALL


def test_five_or_more_branches_is_large():
    assert estimate_size_tier(_branches(5), []) == SizeTier.LARGE


def test_single_branch_with_many_contacts_is_large():
    assert estimate_size_tier(_branches(1), _contacts(6)) == SizeTier.LARGE


def test_two_branches_is_medium():
    assert estimate_size_tier(_branches(2), []) == SizeTier.MEDIUM


def test_single_branch_with_three_contacts_is_medium():
    assert estimate_size_tier(_branches(1), _contacts(3)) == SizeTier.MEDIUM
