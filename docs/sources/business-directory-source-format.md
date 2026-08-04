# Harvester Business and Industry Directory Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how chamber directories, association member lists, trade directories, professional directories, franchise directories, local business listings, sector databases and licensed directory exports enter Harvester.

Directories are discovery sources. Their records may be self-submitted, paid, duplicated, outdated, incomplete or editorially normalized.

## 2. Source modes

```text
BUSINESS_DIRECTORY_API_LICENSED
BUSINESS_DIRECTORY_EXPORT_LICENSED
BUSINESS_DIRECTORY_PUBLIC_PAGE
ASSOCIATION_MEMBER_DIRECTORY_AUTHORIZED
BUSINESS_DIRECTORY_OPERATOR_REFERENCE
```

## 3. User configuration

```text
directory_code
mode
credential_or_connection_reference_id
license_profile_id
category_filters
membership_filters
geographic_filters
name_queries
identifier_queries
page_size
maximum_pages
freshness_window
field_profile_version
request_budget
retention_policy_version
attribution_policy_version
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Directory listing | Listing ID | Organization discovery hint |
| Member record | Membership or directory ID | Association relationship evidence |
| Category | Category ID or path | Source-native classification |
| Location listing | Listing and location ID | Branch or service-area hint |
| Profile update | Update timestamp or revision ID | Freshness evidence |
| Export row | Dataset and row ID | Licensed batch record |
| Operator reference | Directory URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = BUSINESS_DIRECTORY
source.mode = selected directory mode
native.object_type = listing | member_record | category | location_listing | export_row
native.object_id = provider listing or membership ID
native.url = directory profile URL
entity_hints.organization_names = listing name and aliases
entity_hints.domains = listed website domain
entity_hints.emails = listed business email when permitted
entity_hints.phones = listed business phone
entity_hints.addresses = listed address and service area
entity_hints.provider_identifiers = listing and membership identifiers
signals.domain_codes = mapped directory categories
signals.activity_codes = explicitly listed activities only
quality.review_required = true
policy.authorization_basis = LICENSED_DATASET | PUBLIC_WEBSITE_WITH_ROBOTS_COMPLIANCE | CUSTOMER_AUTHORIZED_IMPORT
```

## 6. Example listing envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "BUSINESS_DIRECTORY", "mode": "BUSINESS_DIRECTORY_API_LICENSED"},
  "native": {"object_type": "listing", "object_id": "listing-123", "url": "https://directory.example/listing-123"},
  "entity_hints": {
    "organization_names": ["Example Engineering Works"],
    "domains": ["exampleengineering.pk"],
    "phones": ["+92510000000"],
    "addresses": ["Rawalpindi, Pakistan"],
    "provider_identifiers": [{"type": "DIRECTORY_LISTING_ID", "value": "listing-123"}]
  },
  "signals": {"domain_codes": ["MFG-MET-001"], "activity_codes": ["ACT-PRD-017"]},
  "quality": {"completeness": "PARTIAL", "freshness": "UNKNOWN", "review_required": true, "conflict_flags": []},
  "policy": {
    "authorization_basis": "LICENSED_DATASET",
    "retention_policy": "DIRECTORY_LICENSE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
DIRECTORY_SUCCESS
DIRECTORY_ZERO_RESULTS
DIRECTORY_LISTING_NOT_FOUND
DIRECTORY_LISTING_STALE
DIRECTORY_DUPLICATE_LISTING
DIRECTORY_CATEGORY_AMBIGUOUS
DIRECTORY_MEMBERSHIP_UNVERIFIED
DIRECTORY_RATE_LIMITED
DIRECTORY_LICENSE_EXPIRED
DIRECTORY_POLICY_BLOCKED
```

## 8. Evidence boundaries

Directories may support organization discovery, directory membership, business contact paths, category hints and location hints.

They do not independently prove legal identity, active operations, service quality, current membership, complete market coverage, service gaps, buying intent or contact consent.

## 9. Delivery boundary

This document does not implement directory connectors, page parsing, exports, membership validation, retention or scoring.