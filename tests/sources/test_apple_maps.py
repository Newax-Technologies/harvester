import httpx
import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from lead_harvester.sources.apple_maps import AppleMapsConnector


@pytest.fixture
def private_key_pem() -> str:
    key = ec.generate_private_key(ec.SECP256R1())
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


def test_requires_all_three_credentials(private_key_pem):
    with pytest.raises(ValueError, match="APPLE_MAPS_TEAM_ID"):
        AppleMapsConnector(team_id="", key_id="key1", private_key=private_key_pem)
    with pytest.raises(ValueError, match="APPLE_MAPS_TEAM_ID"):
        AppleMapsConnector(team_id="team1", key_id="", private_key=private_key_pem)
    with pytest.raises(ValueError, match="APPLE_MAPS_TEAM_ID"):
        AppleMapsConnector(team_id="team1", key_id="key1", private_key="")


def test_developer_token_is_signed_with_team_id_and_key_id(private_key_pem):
    connector = AppleMapsConnector(team_id="TEAM123", key_id="KEY456", private_key=private_key_pem)

    token = connector._developer_token()
    header = jwt.get_unverified_header(token)
    payload = jwt.decode(token, options={"verify_signature": False})

    assert header["kid"] == "KEY456"
    assert header["alg"] == "ES256"
    assert payload["iss"] == "TEAM123"


def test_search_exchanges_developer_token_for_access_token_then_searches(private_key_pem):
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path == "/v1/token":
            assert request.headers["Authorization"].startswith("Bearer ")
            return httpx.Response(200, json={"accessToken": "access-123", "expiresInSeconds": 1800})
        assert request.headers["Authorization"] == "Bearer access-123"
        assert request.url.params["q"] == "school in Karachi"
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "name": "Sunrise Academy",
                        "formattedAddressLines": ["1 Test Street", "Karachi, Pakistan"],
                        "coordinate": {"latitude": 24.86, "longitude": 67.00},
                    }
                ]
            },
        )

    connector = AppleMapsConnector(team_id="TEAM123", key_id="KEY456", private_key=private_key_pem)
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    results = connector.search("school in Karachi")

    assert len(calls) == 2
    assert results[0]["name"] == "Sunrise Academy"


def test_access_token_is_cached_across_multiple_searches(private_key_pem):
    token_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal token_calls
        if request.url.path == "/v1/token":
            token_calls += 1
            return httpx.Response(200, json={"accessToken": "access-123", "expiresInSeconds": 1800})
        return httpx.Response(200, json={"results": []})

    connector = AppleMapsConnector(team_id="TEAM123", key_id="KEY456", private_key=private_key_pem)
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    connector.search("school in Karachi")
    connector.search("college in Lahore")

    assert token_calls == 1


def test_search_returns_empty_list_on_http_error(private_key_pem):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/token":
            return httpx.Response(200, json={"accessToken": "access-123", "expiresInSeconds": 1800})
        return httpx.Response(500)

    connector = AppleMapsConnector(team_id="TEAM123", key_id="KEY456", private_key=private_key_pem)
    connector.client = httpx.Client(transport=httpx.MockTransport(handler))

    assert connector.search("school in Karachi") == []
