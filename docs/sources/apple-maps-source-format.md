# Harvester Apple Maps Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Existing runtime source type exists; governed production adapter format is not implemented**

## 1. Purpose

This document defines how permitted Apple Maps, MapKit, Maps Server API, customer-authorized business-profile, licensed result, and operator-reference records may enter Harvester.

Harvester must not scrape Apple Maps interfaces, automate consumer applications, intercept undocumented endpoints, or treat search results as complete market coverage.

## 2. Source modes

```text
APPLE_MAPS_API_LICENSED
APPLE_BUSINESS_CONNECT_AUTHORIZED
APPLE_MAPS_OPERATOR_REFERENCE
```

## 3. User configuration

```text
mode
credential_reference_id
team_or_connection_reference
contract_profile_id
language
country_code
geographic_boundary_id
query_profile_version
category_mapping_version
maximum_results
request_budget
cost_budget
field_profile_version
retention_policy_version
attribution_policy_version
authorized_location_references
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Place or POI | Provider place identifier when supplied | Candidate organization or branch |
| Search response | Query and response identifier | Coverage outcome |
| Business Connect location | Customer-authorized location ID | Customer-owned profile data |
| Operator reference | Apple Maps URL | Manual navigation only |

## 5. Canonical formatting

```text
source.code = APPLE_MAPS
source.mode = selected Apple mode
native.object_type = place | search_result | authorized_location
native.object_id = provider identifier or response-position reference
native.url = permitted Maps URL
entity_hints.organization_names = provider place name
entity_hints.phones = permitted phone fields
entity_hints.domains = permitted website domain
entity_hints.addresses = provider address fields
entity_hints.coordinates = contract-permitted coordinates
entity_hints.provider_identifiers = Apple provider references
signals.domain_codes = mapped source-native categories
policy.retention_policy = APPLE_SOURCE_SPECIFIC
```

## 6. Example observation

```json
{
  "schema_version": "1.0",
  "source": {"code": "APPLE_MAPS", "mode": "APPLE_MAPS_API_LICENSED"},
  "native": {"object_type": "place", "object_id": "provider-place-id", "url": "https://maps.apple.com/?q=example"},
  "entity_hints": {
    "organization_names": ["Example Clinic"],
    "domains": ["exampleclinic.pk"],
    "addresses": ["Islamabad, Pakistan"],
    "provider_identifiers": [{"type": "APPLE_MAPS_PLACE_ID", "value": "provider-place-id"}]
  },
  "policy": {
    "authorization_basis": "LICENSED_API",
    "retention_policy": "APPLE_SOURCE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
APPLE_SUCCESS
APPLE_ZERO_RESULTS
APPLE_PARTIAL_RESULTS
APPLE_TOKEN_INVALID
APPLE_AUTHORIZATION_FAILED
APPLE_RATE_LIMITED
APPLE_RESULT_LIMIT_REACHED
APPLE_PLACE_REMOVED
APPLE_LICENSE_BLOCKED
APPLE_ATTRIBUTION_BLOCKED
APPLE_POLICY_BLOCKED
```

## 8. Retention and evidence boundaries

Provider content, identifiers, geometry, display, caching, attribution, and derived use follow the active Apple agreement. Independently fetched websites create separate observations.

Apple Maps may support discovery, branch, location and contact hints. It cannot independently prove legal identity, complete coverage, service absence, buying intent or communication consent.

## 9. Delivery boundary

This document does not implement Apple authorization, API calls, Business Connect access, parsing, retention enforcement or scoring.