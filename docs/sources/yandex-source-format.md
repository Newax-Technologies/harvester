# Harvester Yandex Source Format

Status: **Proposed formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Current connector is partial and restricted; this target format is not implemented**

Authority: [Yandex Maps API Source and Extraction Model](yandex-maps-api-source-model.md) remains authoritative for acquisition, licensing, cache duration, attribution, coverage, independent verification, and production gates.

## 1. Source modes

```text
YANDEX_PLACES_TRANSIENT
YANDEX_BUSINESS_AUTHORIZED_EXPORT
YANDEX_MAPS_OPERATOR_LINK
```

## 2. User configuration

```text
mode
credential_reference_id
contract_or_license_profile_id
language_locale
geographic_boundary_id
bbox_or_center_span_policy
strict_area_search
query_profile_version
category_mapping_version
results_per_page
maximum_pages
maximum_skip
request_budget
cost_budget
cache_duration_days
attribution_policy_version
authorized_export_reference
operator_review_requirement
```

`strict_area_search` should use the provider's strict-area behavior when systematic coverage is intended. A free-text area name alone does not establish complete coverage.

## 3. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Business feature | `CompanyMetaData.id` or documented provider URI | Candidate organization or branch |
| Search page | Request plus `skip` | Query and coverage outcome |
| Geographic object | Provider URI | Geography validation where approved |
| Authorized Business export row | Customer export record identifier | Customer-owned profile and performance evidence |
| Operator link | Yandex Maps URL | Human navigation only |

## 4. Canonical mapping

```text
source.code = YANDEX
source.mode = selected Yandex mode
native.object_type = business_feature | geographic_object | authorized_export_row | operator_link
native.object_id = documented provider identifier
native.url = permitted provider URI or operator URL
entity_hints.organization_names = CompanyMetaData.name
entity_hints.phones = documented phone list
entity_hints.domains = domain derived from documented URL when permitted
entity_hints.addresses = formatted address and documented address components
entity_hints.coordinates = transient permitted geometry
entity_hints.provider_identifiers = Yandex organization identifier
signals.domain_codes = mapped from documented categories
quality.review_required = true when best-match results, category ambiguity, or geographic uncertainty exists
policy.retention_policy = YANDEX_SOURCE_SPECIFIC
```

## 5. Example transient observation

```json
{
  "schema_version": "1.0",
  "source": {"code": "YANDEX", "mode": "YANDEX_PLACES_TRANSIENT"},
  "native": {
    "object_type": "business_feature",
    "object_id": "provider-business-id",
    "url": "https://yandex.com/maps/org/...",
    "payload_ref": "transient://yandex/business/provider-business-id"
  },
  "entity_hints": {
    "organization_names": ["Example Logistics"],
    "domains": ["examplelogistics.pk"],
    "phones": ["+92510000000"],
    "addresses": ["Rawalpindi, Pakistan"],
    "provider_identifiers": [{"type": "YANDEX_BUSINESS_ID", "value": "provider-business-id"}]
  },
  "quality": {
    "completeness": "PARTIAL",
    "freshness": "CURRENT",
    "review_required": true,
    "conflict_flags": []
  },
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "TRANSIENT_EXTRACT_AND_DELETE",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 6. Authorized export mapping

A customer-supplied Yandex Business export uses:

```text
source.mode = YANDEX_BUSINESS_AUTHORIZED_EXPORT
native.object_type = authorized_business_export_row
policy.authorization_basis = CUSTOMER_AUTHORIZED_IMPORT
policy.retention_policy = CUSTOMER_CONTROLLED_IMPORT
```

The import must retain:

```text
authorization_reference
account_owner
business_profile_reference
exported_at
source_period
file_hash
imported_at
retention_policy
customer_deletion_policy
```

## 7. Outcome states

```text
YANDEX_SUCCESS
YANDEX_ZERO_RESULTS
YANDEX_PARTIAL_PAGE_SET
YANDEX_OUTSIDE_AREA_RESULT_REJECTED
YANDEX_RESULT_LIMIT_REACHED
YANDEX_BEST_MATCH_ONLY
YANDEX_INVALID_LOCALE
YANDEX_INVALID_GEOMETRY
YANDEX_RATE_LIMITED
YANDEX_AUTHENTICATION_FAILED
YANDEX_LICENSE_BLOCKED
YANDEX_CACHE_EXPIRED
YANDEX_ATTRIBUTION_BLOCKED
YANDEX_PROVIDER_FAILED
```

Zero results, missing websites, and missing phones remain non-detection states.

## 8. Retention and provenance

- Public Places content uses a contract-specific transient cache or reference-only policy.
- Full payloads must not remain in the generic immutable store when the active agreement prohibits that storage.
- Independently fetched websites or official registries create separate observations.
- Authorized exports remain linked to the customer authorization and deletion policy.
- Operator links do not authorize automatic page extraction.

## 9. Evidence boundaries

Yandex may support discovery, source-native category evidence, branch and contact hints, opening-hours hints, and customer-authorized profile statistics.

It cannot independently prove complete market coverage, legal identity, service absence, buying intent, or communication consent.

## 10. Delivery boundary

This document defines formatting only. Production use remains blocked until the applicable contract, retention, attribution, closed-system use, and derived-data rules are approved and implemented.