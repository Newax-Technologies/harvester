from lead_harvester.enrichment.technology_detector import detect_technology_signals


def test_empty_text_returns_no_signals():
    assert detect_technology_signals("") == []
    assert detect_technology_signals(None) == []  # type: ignore[arg-type]


def test_detects_whatsapp_pain_point_without_booking_terms():
    text = "Contact us on WhatsApp for any queries."
    signals = detect_technology_signals(text)
    assert signals == [
        {
            "signal_type": "pain_point",
            "text": "Uses WhatsApp for communication with no online booking/portal.",
        }
    ]


def test_whatsapp_with_booking_portal_is_not_flagged():
    text = "Message us on WhatsApp or book now through our parent portal."
    signals = detect_technology_signals(text)
    assert signals == []


def test_detects_google_form_admissions_pain_point():
    text = "Fill out our Google Form to apply for admission this year."
    signals = detect_technology_signals(text)
    assert signals == [
        {
            "signal_type": "pain_point",
            "text": "Uses Google Forms for admissions instead of a dedicated system.",
        }
    ]


def test_google_form_without_admission_context_is_not_flagged():
    text = "Fill out this Google Form to give us feedback."
    signals = detect_technology_signals(text)
    assert signals == []


def test_detects_hiring_buying_signal():
    text = "We're now hiring for multiple teaching positions."
    signals = detect_technology_signals(text)
    assert {
        "signal_type": "buying_signal",
        "text": "Actively hiring -- may indicate growth/budget.",
    } in signals


def test_detects_new_campus_buying_signal():
    text = "Excited to announce our grand opening for a new campus next term!"
    signals = detect_technology_signals(text)
    types = {s["text"] for s in signals}
    assert "Recently opened or announced a new campus/location." in types


def test_matching_is_case_insensitive():
    text = "WHATSAPP us anytime, no other way to reach admissions."
    signals = detect_technology_signals(text)
    assert signals == [
        {
            "signal_type": "pain_point",
            "text": "Uses WhatsApp for communication with no online booking/portal.",
        }
    ]


def test_multiple_rules_matching_the_same_message_only_appear_once():
    # "now hiring" and "we're hiring" both map to the same buying-signal
    # message -- must be deduped rather than appended twice.
    text = "We're hiring! We are now hiring across all campuses."
    signals = detect_technology_signals(text)
    hiring_signals = [
        s for s in signals if s["text"] == "Actively hiring -- may indicate growth/budget."
    ]
    assert len(hiring_signals) == 1


def test_multiple_distinct_signals_detected_together():
    text = "We're now hiring teachers. Message us on WhatsApp for any questions."
    signals = detect_technology_signals(text)
    assert len(signals) == 2
    assert {s["signal_type"] for s in signals} == {"pain_point", "buying_signal"}
