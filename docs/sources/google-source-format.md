# Harvester Google Source Format

Status: **Proposed formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Current Google Places connector is partial; this target format is not implemented**

Authority: [Google API Source and Extraction Model](google-api-source-model.md) remains authoritative for acquisition, coverage, field masks, licensing, attribution, retention, cost, and production gates. This document defines how permitted Google records enter the [Canonical Source Record Format](canonical-source-record-format.md).

## 1. Source modes

```text
GOOGLE_PLACES_PUBLIC
GOOGLE_BUSINESS_PROFILE_AUTHORIZED
GOOGLE_OPERATOR_LINK
```

## 2. User configuration

Google configuration may include:

```text
mode
credential_reference_id
authorized_account_reference
authorized_location_references
country_code
language_code
geographic_boundary_id
coverage_cell_policy
google_type_mapping_version
text_query_profile_version
search_methods
rank_preferences
page_size
maximum_pages
maximum_unique_places
discovery_field_profile_version
details_field_profile_version
review_policy
photo_policy
business_profile_metric_policy
request_budget
cost_budget
retention_policy_version
attribution_policy_version
```

Public Places configuration must not contain customer Business Profile credentials. Authorized Business Profile configuration must not be reused for public prospect discovery.

## 3. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Place | Google Place ID | Candidate place or branch reference |
| Search page | Request plus page token | Coverage and query outcome |
| Photo | Photo resource name | Optional transient media reference |
| Managed location | Business Profile location name | Customer-authorized location |
| Review | Review resource name | Customer-authorized reputation evidence |
| Local Post | Post resource name | Customer-authored activity evidence |
| Performance metric | Location, metric and period | Customer-authorized operating intelligence |
| Search keyword impression | Location, keyword and period | Customer-authorized demand evidence |

## 4. Canonical mapping

### Place observation

```text
source.code = GOOGLE
source.mode = GOOGLE_PLACES_PUBLIC
native.object_type = place
native.object_id = place.id
native.url = place.googleMapsUri
entity_hints.organization_names = place.displayName.text
entity_hints.phones = documented phone fields
entity_hints.domains = domain extracted from websiteUri
entity_hints.addresses = formatted and structured address fields
entity_hints.coordinates = transient permitted coordinates
entity_hints.provider_identifiers = Google Place ID
signals.domain_codes = mapped from primaryType and types, never copied directly as canonical truth
content.summary = editorialSummary when requested and permitted
quality.review_required = true when type, identity, moved-place, or address evidence conflicts
```

### Authorized Business Profile observation

```text
source.mode = GOOGLE_BUSINESS_PROFILE_AUTHORIZED
native.object_type = managed_location | review | local_post | performance_metric
native.object_id = provider resource name
entity_hints.provider_identifiers = account and location references
content = customer-owned or customer-authorized material
signals.event_types = expansion, update, campaign, operational or demand signals when supported
policy.authorization_basis = CUSTOMER_OAUTH
```

## 5. Example place envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "GOOGLE", "mode": "GOOGLE_PLACES_PUBLIC"},
  "native": {
    "object_type": "place",
    "object_id": "ChIJ...",
    "url": "https://maps.google.com/?cid=...",
    "payload_ref": "transient://google/place/ChIJ..."
  },
  "entity_hints": {
    "organization_names": ["Example Medical Supplies"],
    "domains": ["example.pk"],
    "phones": ["+92510000000"],
    "addresses": ["Islamabad, Pakistan"],
    "provider_identifiers": [{"type": "GOOGLE_PLACE_ID", "value": "ChIJ..."}]
  },
  "signals": {
    "domain_codes": ["HC-SUP-001"],
    "activity_codes": [],
    "keyword_matches": []
  },
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "GOOGLE_SOURCE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 6. Outcome states

Google-specific outcomes include:

```text
GOOGLE_SUCCESS
GOOGLE_ZERO_RESULTS
GOOGLE_PARTIAL_PAGE_SET
GOOGLE_POSSIBLY_SATURATED
GOOGLE_INVALID_FIELD_MASK
GOOGLE_INVALID_PAGE_TOKEN
GOOGLE_RATE_LIMITED
GOOGLE_QUOTA_EXHAUSTED
GOOGLE_AUTHENTICATION_FAILED
GOOGLE_AUTHORIZATION_FAILED
GOOGLE_PLACE_MOVED
GOOGLE_PLACE_CLOSED
GOOGLE_POLICY_BLOCKED
GOOGLE_RETENTION_REJECTED
```

A missing `websiteUri`, phone, rating, review, or result is `NOT_DETECTED`, not confirmed absence.

## 7. Retention and provenance

- Place IDs may be retained only as permitted by the applicable Google terms.
- Full Places payloads use `TRANSIENT_EXTRACT_AND_DELETE` or another approved source-specific policy.
- Independently crawled organization websites create separate `WEBSITE` observations.
- Reviews, photos, and Maps content must not be used for model training.
- Required attribution and display conditions remain attached to every observation.
- Authorized Business Profile data remains tenant-owned, connection-scoped, and deletion-aware.

## 8. Evidence boundaries

Google may support organization discovery, branch evidence, location context, public contact paths, business status, and customer-authorized performance or content signals.

Google cannot independently prove legal identity, service absence, buying intent, consent to contact, or a qualified opportunity.

## 9. Delivery boundary

This format is a documentation contract. It does not implement Google schemas, source requests, token handling, payload expiry, observation creation, or scoring.