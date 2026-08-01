import uuid

from lead_harvester.models.source import RawSourceRecord, SourceType
from lead_harvester.resolution.normalize import normalize_domain, normalize_name, normalize_phone


def google_places_record(
    run_id,
    *,
    name: str = "Riverside Academy",
    phone: str | None = "+923001234567",
    website: str | None = "https://riverside.edu",
    lat: float | None = 24.8607,
    lng: float | None = 67.0011,
    business_status: str | None = "OPERATIONAL",
    source_id: str | None = None,
) -> RawSourceRecord:
    source_id = source_id or f"gp:{uuid.uuid4().hex[:8]}"
    return RawSourceRecord(
        source_run_id=run_id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=source_id,
        raw_payload={
            "id": source_id,
            "displayName": {"text": name},
            "formattedAddress": "12 River Road, Lahore",
            "websiteUri": website,
            "primaryType": "school",
            "nationalPhoneNumber": phone,
            "businessStatus": business_status,
        },
        normalized_name=normalize_name(name),
        normalized_phone=normalize_phone(phone) if phone else None,
        normalized_domain=normalize_domain(website) if website else None,
        location=(f"SRID=4326;POINT({lng} {lat})" if lat is not None and lng is not None else None),
    )


def website_record(
    run_id,
    *,
    name: str = "Riverside Academy",
    organization: str = "",
    phone: str | None = None,
    email: str | None = None,
    website: str | None = "riverside.edu",
    location_text: str = "Lahore, Pakistan",
    social_profiles: list[str] | None = None,
    source_id: str | None = None,
    description: str = "",
    address_locality: str = "",
    address_country: str = "",
    person_role: str = "",
) -> RawSourceRecord:
    source_id = source_id or website or f"web:{uuid.uuid4().hex[:8]}"
    payload = {
        "source": "search",
        "source_url": "https://example.com/directory",
        "name": name,
        "organization": organization,
        "title": "",
        "email": email or "",
        "phone": phone or "",
        "website": website or "",
        "location": location_text,
        "social_profiles": social_profiles or [],
        "evidence": "",
        "raw": {
            "description": description,
            "address_locality": address_locality,
            "address_country": address_country,
            "person_role": person_role,
        },
    }
    return RawSourceRecord(
        source_run_id=run_id,
        source_type=SourceType.WEBSITE,
        source_id=source_id,
        raw_payload=payload,
        normalized_name=normalize_name(organization or name),
        normalized_phone=normalize_phone(phone) if phone else None,
        normalized_domain=normalize_domain(website) if website else None,
        location=None,
    )
