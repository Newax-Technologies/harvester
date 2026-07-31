import httpx

from lead_harvester.sources.telegram_channels import TelegramChannelConnector

_CHANNEL_HTML = """
<html>
<head>
<meta property="og:site_name" content="Beacon House School Official" />
<meta property="og:description" content="Admissions open for Fall 2026. Email admissions@beaconhouse.example.edu." />
<title>Beacon House School Official</title>
</head>
<body>
<div class="tgme_widget_message_text">
Admissions open for Fall 2026. Email admissions@beaconhouse.example.edu or call +923001234567.
</div>
</body>
</html>
"""

_EMPTY_CHANNEL_HTML = """
<html><head><title>Telegram: Contact @nonexistent</title></head>
<body><div class="tgme_page_description">If you have Telegram, you can view and join right away.</div></body>
</html>
"""


def test_fetch_channel_extracts_name_and_contacts():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/s/beaconhouseofficial"
        return httpx.Response(200, text=_CHANNEL_HTML)

    connector = TelegramChannelConnector()
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    result = connector.fetch_channel("beaconhouseofficial")

    assert result is not None
    assert result["channel"] == "beaconhouseofficial"
    assert result["preview_url"] == "https://t.me/s/beaconhouseofficial"
    assert result["name"] == "Beacon House School Official"
    assert "admissions@beaconhouse.example.edu" in result["all_emails"]
    assert any(p for p in result["all_phones"])


def test_fetch_channel_strips_leading_at_sign():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/s/beaconhouseofficial"
        return httpx.Response(200, text=_CHANNEL_HTML)

    connector = TelegramChannelConnector()
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    result = connector.fetch_channel("@beaconhouseofficial")

    assert result is not None


def test_fetch_channel_returns_none_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404)

    connector = TelegramChannelConnector()
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    assert connector.fetch_channel("missingchannel") is None


def test_fetch_channel_returns_none_for_blank_channel():
    connector = TelegramChannelConnector()
    assert connector.fetch_channel("   ") is None
