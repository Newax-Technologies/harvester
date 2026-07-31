from lead_harvester.intelligence.operational_maturity import compute_operational_maturity
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.signal import Signal, SignalType


def _institution(website: str | None = "https://example.edu") -> CanonicalInstitution:
    return CanonicalInstitution(canonical_name="Example School", website=website)


def _signal(signal_type: SignalType) -> Signal:
    return Signal(institution_id=None, signal_type=signal_type, signal_text="x")


def test_baseline_with_website_and_no_signals():
    score = compute_operational_maturity(_institution(), [])
    assert score == 70  # baseline 50 + website bonus 20


def test_no_website_scores_lower_than_baseline_with_website():
    with_site = compute_operational_maturity(_institution(website="https://example.edu"), [])
    without_site = compute_operational_maturity(_institution(website=None), [])
    assert without_site < with_site


def test_pain_points_reduce_the_score():
    baseline = compute_operational_maturity(_institution(), [])
    with_pain = compute_operational_maturity(
        _institution(), [_signal(SignalType.PAIN_POINT), _signal(SignalType.PAIN_POINT)]
    )
    assert with_pain < baseline


def test_buying_signals_slightly_increase_the_score():
    baseline = compute_operational_maturity(_institution(), [])
    with_buying = compute_operational_maturity(_institution(), [_signal(SignalType.BUYING_SIGNAL)])
    assert with_buying > baseline


def test_score_is_clamped_to_0_and_100():
    many_pain_points = [_signal(SignalType.PAIN_POINT) for _ in range(20)]
    assert compute_operational_maturity(_institution(), many_pain_points) == 0

    many_buying_signals = [_signal(SignalType.BUYING_SIGNAL) for _ in range(20)]
    assert compute_operational_maturity(_institution(), many_buying_signals) <= 100
