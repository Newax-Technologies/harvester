import httpx
import pytest

from lead_harvester.sources.search import BraveSearchSource, SearchResult


def test_requires_api_key():
    with pytest.raises(ValueError, match="BRAVE_SEARCH_API_KEY"):
        BraveSearchSource(api_key="")


@pytest.mark.asyncio
async def test_search_returns_results_and_filters_out_missing_urls():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-Subscription-Token"] == "test-key"
        assert request.url.params["q"] == "school in Karachi"
        return httpx.Response(
            200,
            json={
                "web": {
                    "results": [
                        {
                            "title": "Beacon House School",
                            "url": "https://beaconhouse.example.edu",
                            "description": "A school in Karachi.",
                        },
                        # No "url" -- must be filtered out.
                        {"title": "No URL", "description": "..."},
                    ]
                }
            },
        )

    source = BraveSearchSource(api_key="test-key")
    source.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    results = await source.search("school in Karachi")

    assert results == [
        SearchResult(
            title="Beacon House School",
            url="https://beaconhouse.example.edu",
            description="A school in Karachi.",
        )
    ]


@pytest.mark.asyncio
async def test_search_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    source = BraveSearchSource(api_key="test-key")
    source.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    with pytest.raises(httpx.HTTPStatusError):
        await source.search("school in Karachi")
