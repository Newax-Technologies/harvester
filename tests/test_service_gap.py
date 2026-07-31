from lead_harvester.intelligence.service_gap import compute_service_gap_score
from lead_harvester.models.profile import SizeTier, WebsiteQualityTier
from lead_harvester.models.signal import Signal, SignalType


def _lms_signal() -> Signal:
    return Signal(
        signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Has a parent portal."
    )


def test_no_website_and_no_lms_is_fully_missing():
    score = compute_service_gap_score(WebsiteQualityTier.NONE, [], SizeTier.SMALL)
    assert score == 2.0  # (1.0 website + 1.0 lms) * 1.0 size


def test_good_website_and_lms_present_has_no_gap():
    score = compute_service_gap_score(
        WebsiteQualityTier.GOOD, [_lms_signal()], SizeTier.SMALL
    )
    assert score == 0.0


def test_poor_website_is_a_partial_gap():
    score = compute_service_gap_score(WebsiteQualityTier.POOR, [_lms_signal()], SizeTier.SMALL)
    assert score == 0.5


def test_larger_institution_with_same_gaps_scores_higher():
    small = compute_service_gap_score(WebsiteQualityTier.NONE, [], SizeTier.SMALL)
    large = compute_service_gap_score(WebsiteQualityTier.NONE, [], SizeTier.LARGE)
    assert large > small
    assert large == 4.0  # 2.0 missing_product_count * 2.0 size multiplier


def test_non_lms_technology_signal_does_not_count_as_lms_present():
    other_signal = Signal(
        signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Uses some unrelated widget."
    )
    score = compute_service_gap_score(
        WebsiteQualityTier.GOOD, [other_signal], SizeTier.SMALL
    )
    assert score == 1.0  # website gap 0.0 + lms gap 1.0
