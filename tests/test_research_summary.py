from lead_harvester.intelligence.research_summary import summarize_signals
from lead_harvester.models.signal import Signal, SignalType


def _signal(signal_type: SignalType, text: str) -> Signal:
    return Signal(institution_id=None, signal_type=signal_type, signal_text=text)


def test_no_signals_returns_empty_string():
    assert summarize_signals([]) == ""


def test_summarizes_pain_points_only():
    signals = [_signal(SignalType.PAIN_POINT, "uses whatsapp with no booking portal")]
    summary = summarize_signals(signals)
    assert "1 pain point detected" in summary
    assert "uses whatsapp with no booking portal" in summary


def test_summarizes_buying_signals_only():
    signals = [_signal(SignalType.BUYING_SIGNAL, "now hiring")]
    summary = summarize_signals(signals)
    assert "1 buying signal" in summary
    assert "now hiring" in summary


def test_pluralizes_multiple_signals():
    signals = [
        _signal(SignalType.PAIN_POINT, "a"),
        _signal(SignalType.PAIN_POINT, "b"),
    ]
    summary = summarize_signals(signals)
    assert "2 pain points detected" in summary


def test_summarizes_both_types_together():
    signals = [
        _signal(SignalType.PAIN_POINT, "a"),
        _signal(SignalType.BUYING_SIGNAL, "b"),
    ]
    summary = summarize_signals(signals)
    assert "pain point" in summary
    assert "buying signal" in summary
