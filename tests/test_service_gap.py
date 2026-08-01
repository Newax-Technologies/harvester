from lead_harvester.intelligence.service_gap import _DETECTION_GAP_WEIGHT, compute_service_gap_score
from lead_harvester.models.profile import DetectionStatus, SizeTier, WebsiteQualityTier
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import RawPageSnapshot


def _lms_signal() -> Signal:
    return Signal(signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Has a parent portal.")


def _successful_snapshot() -> RawPageSnapshot:
    return RawPageSnapshot(url="https://x.edu", html="<html>hi</html>", fetch_error="")


def _failed_snapshot() -> RawPageSnapshot:
    return RawPageSnapshot(url="https://x.edu", html=None, fetch_error="http_error: 500")


def test_only_absent_confirmed_contributes_a_full_missing_product_score():
    # [Certain] the core constraint this correction exists to enforce.
    assert _DETECTION_GAP_WEIGHT[DetectionStatus.ABSENT_CONFIRMED] == 1.0
    assert 0.0 < _DETECTION_GAP_WEIGHT[DetectionStatus.NOT_DETECTED] < 1.0
    assert 0.0 < _DETECTION_GAP_WEIGHT[DetectionStatus.UNKNOWN] < 1.0
    assert _DETECTION_GAP_WEIGHT[DetectionStatus.NOT_CRAWLED] == 0.0
    assert _DETECTION_GAP_WEIGHT[DetectionStatus.CRAWL_FAILED] == 0.0
    assert _DETECTION_GAP_WEIGHT[DetectionStatus.PRESENT] == 0.0


def test_no_website_at_all_is_reduced_confidence_not_full():
    # Correction regression test: no website on file used to score as a
    # full (1.0) missing-product gap -- it's now UNKNOWN (we generally
    # can't confirm true absence), a reduced contribution.
    result = compute_service_gap_score(None, [], WebsiteQualityTier.NONE, [], SizeTier.SMALL)
    assert result.website_status == DetectionStatus.UNKNOWN
    assert result.lms_status == DetectionStatus.NOT_CRAWLED  # nothing to crawl at all
    assert result.score == _DETECTION_GAP_WEIGHT[DetectionStatus.UNKNOWN]  # 0.15 * 1.0 size


def test_good_website_and_lms_present_has_no_gap():
    result = compute_service_gap_score(
        "https://x.edu",
        [_successful_snapshot()],
        WebsiteQualityTier.GOOD,
        [_lms_signal()],
        SizeTier.SMALL,
    )
    assert result.website_status == DetectionStatus.PRESENT
    assert result.lms_status == DetectionStatus.PRESENT
    assert result.score == 0.0


def test_poor_website_with_crawl_evidence_is_a_partial_gap():
    result = compute_service_gap_score(
        "https://x.edu",
        [_successful_snapshot()],
        WebsiteQualityTier.POOR,
        [_lms_signal()],
        SizeTier.SMALL,
    )
    assert result.website_status == DetectionStatus.PRESENT
    assert result.score == 0.5  # POOR website gap (0.5) + LMS present (0.0)


def test_website_never_crawled_contributes_nothing():
    # Website is known (a URL is on file) but no fetch was ever attempted
    # -- a pure data gap, distinct from "no website at all" (UNKNOWN).
    # No evidence at all means no basis to call it a missing product.
    result = compute_service_gap_score(
        "https://x.edu", [], WebsiteQualityTier.NONE, [], SizeTier.SMALL
    )
    assert result.website_status == DetectionStatus.NOT_CRAWLED
    assert result.score == 0.0


def test_website_crawl_failed_contributes_nothing():
    result = compute_service_gap_score(
        "https://x.edu", [_failed_snapshot()], WebsiteQualityTier.NONE, [], SizeTier.SMALL
    )
    assert result.website_status == DetectionStatus.CRAWL_FAILED
    assert result.score == 0.0


def test_lms_not_detected_after_real_crawl_is_reduced_not_full():
    # [Certain]: a real crawl that found no LMS mention is genuine but
    # incomplete evidence (an authenticated portal or JS-rendered
    # dashboard is invisible to a static crawler) -- NOT_DETECTED, scored
    # at a reduced weight, never the full 1.0 ABSENT_CONFIRMED would get.
    result = compute_service_gap_score(
        "https://x.edu",
        [_successful_snapshot()],
        WebsiteQualityTier.GOOD,
        [],
        SizeTier.SMALL,
    )
    assert result.lms_status == DetectionStatus.NOT_DETECTED
    assert result.score == _DETECTION_GAP_WEIGHT[DetectionStatus.NOT_DETECTED]
    assert result.score < 1.0


def test_non_lms_technology_signal_does_not_count_as_lms_present():
    other_signal = Signal(
        signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Uses some unrelated widget."
    )
    result = compute_service_gap_score(
        "https://x.edu",
        [_successful_snapshot()],
        WebsiteQualityTier.GOOD,
        [other_signal],
        SizeTier.SMALL,
    )
    assert result.lms_status == DetectionStatus.NOT_DETECTED
    assert result.score == 0.3  # website gap 0.0 (GOOD) + lms NOT_DETECTED (0.3)


def test_larger_institution_with_the_same_gaps_scores_higher():
    small = compute_service_gap_score(None, [], WebsiteQualityTier.NONE, [], SizeTier.SMALL)
    large = compute_service_gap_score(None, [], WebsiteQualityTier.NONE, [], SizeTier.LARGE)
    assert large.score > small.score
    assert small.score == _DETECTION_GAP_WEIGHT[DetectionStatus.UNKNOWN] * 1.0
    assert large.score == _DETECTION_GAP_WEIGHT[DetectionStatus.UNKNOWN] * 2.0
