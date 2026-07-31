from __future__ import annotations

import httpx

from .base import CRMConnector, CRMSyncOutcome, CRMSyncPayload


class GenericCRMConnector(CRMConnector):
    """
    Generic REST adapter for a licensed CRM (HubSpot, Salesforce, Pipedrive,
    etc.). Each of those has its own object model and auth scheme, so this
    expects a normalized JSON contract instead of hardcoding one vendor:

        POST {api_url}/companies        (create, no external_id yet)
        PUT  {api_url}/companies/{id}   (update, external_id known)

        request body:  {"name": ..., "domain": ..., "website": ...,
                         "contacts": [{"type", "value", "name", "role"}, ...]}
        response body: {"id": "<crm record id>", ...}

    If your CRM's API looks different, adapt `_build_request`/`_parse_response`
    rather than the calling code.
    """

    name = "generic_crm"

    def __init__(self, api_url: str, api_key: str, timeout_seconds: float = 15.0):
        if not api_url or not api_key:
            raise ValueError("CRM sync requires both an API URL and an API key.")
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    async def upsert_company(self, payload: CRMSyncPayload) -> CRMSyncOutcome:
        body = {
            "name": payload.institution_name,
            "domain": payload.domain,
            "website": payload.website,
            "contacts": [
                {"type": c.contact_type, "value": c.value, "name": c.person_name, "role": c.role}
                for c in payload.contacts
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            if payload.external_id:
                response = await client.put(f"{self.api_url}/companies/{payload.external_id}", json=body, headers=headers)
            else:
                response = await client.post(f"{self.api_url}/companies", json=body, headers=headers)
            response.raise_for_status()
            data = response.json()

        external_id = str(data.get("id") or payload.external_id or "")
        if not external_id:
            raise ValueError(f"CRM response did not include a record id: {data!r}")

        return CRMSyncOutcome(external_id=external_id, raw_response=data)
