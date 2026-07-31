from lead_harvester.config import Settings
from lead_harvester.sources.web import Lead, WebCrawler


def test_extract_lead_populates_detected_signals():
    html = """
    <html><body>
    <h1>Beacon House School</h1>
    <p>Email us at admissions@beaconhouse.example.edu or call +923001234567.</p>
    <p>We're now hiring teachers for the new term.</p>
    </body></html>
    """
    crawler = WebCrawler(Settings(google_places_api_key="dummy-test-key"))
    lead, _links = crawler._extract_lead(html, "https://beaconhouse.example.edu")

    assert lead is not None
    assert lead.raw["detected_signals"] == [
        {
            "signal_type": "buying_signal",
            "text": "Actively hiring -- may indicate growth/budget.",
        }
    ]


def test_extract_lead_with_no_signals_gets_empty_list():
    html = """
    <html><body>
    <h1>Beacon House School</h1>
    <p>Email us at admissions@beaconhouse.example.edu or call +923001234567.</p>
    </body></html>
    """
    crawler = WebCrawler(Settings(google_places_api_key="dummy-test-key"))
    lead, _links = crawler._extract_lead(html, "https://beaconhouse.example.edu")

    assert lead is not None
    assert lead.raw["detected_signals"] == []


def _lead(**raw_overrides) -> Lead:
    raw = {
        "description": "",
        "all_emails": [],
        "all_phones": [],
        "pages": ["https://example.edu"],
        "detected_signals": [],
    }
    raw.update(raw_overrides)
    return Lead(
        source="website",
        source_url="https://example.edu",
        name="",
        organization="Example School",
        title="",
        email="",
        phone="",
        website="https://example.edu",
        location="",
        social_profiles=[],
        evidence="",
        raw=raw,
    )


def test_merge_combines_and_dedupes_detected_signals_from_both_pages():
    existing = _lead(
        detected_signals=[
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            }
        ]
    )
    incoming = _lead(
        detected_signals=[
            # Duplicate of an existing signal -- must not appear twice.
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            },
            {
                "signal_type": "pain_point",
                "text": "Uses WhatsApp for communication with no online booking/portal.",
            },
        ]
    )

    merged = WebCrawler._merge(existing, incoming)

    assert len(merged.raw["detected_signals"]) == 2
    assert {
        "signal_type": "pain_point",
        "text": "Uses WhatsApp for communication with no online booking/portal.",
    } in merged.raw["detected_signals"]


def test_merge_with_no_existing_lead_returns_incoming_unchanged():
    incoming = _lead(
        detected_signals=[
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            }
        ]
    )

    merged = WebCrawler._merge(None, incoming)

    assert merged is incoming
