import httpx
import pytest

from lead_harvester.sources.yandex_maps import YandexMapsConnector


def test_requires_api_key():
    with pytest.raises(ValueError, match="YANDEX_MAPS_API_KEY"):
        YandexMapsConnector(api_key="")


def _feature(name: str) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [67.0011, 24.8607]},
        "properties": {
            "name": name,
            "description": "Some Street, Karachi",
            "CompanyMetaData": {
                "id": "1234567890",
                "name": name,
                "address": "Some Street, Karachi",
                "Phones": [{"type": "phone", "formatted": "+92 300 1234567"}],
                "url": "http://example.edu",
                "Categories": [{"name": "School"}],
            },
        },
    }


def test_search_returns_features_on_success():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["apikey"] == "test-key"
        assert request.url.params["text"] == "school in Karachi"
        return httpx.Response(200, json={"features": [_feature("Sunrise Academy")]})

    connector = YandexMapsConnector(api_key="test-key")
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    features = connector.search("school in Karachi")

    assert len(features) == 1
    assert features[0]["properties"]["name"] == "Sunrise Academy"


def test_search_returns_empty_list_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    connector = YandexMapsConnector(api_key="test-key")
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    assert connector.search("school in Karachi") == []
