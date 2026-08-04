# Harvester Government and Official Registry Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how official company registries, tax registries, licensing bodies, professional registers, public-sector directories, court or filing systems, regulated-entity lists, nonprofit registers, and other government-issued records enter Harvester.

Official records may provide strong evidence of legal existence, identifiers, status, dates, regulated permissions and registered addresses. They do not necessarily prove current operations, services, ownership control, solvency, contactability or market activity.

## 2. Source modes

```text
GOVERNMENT_REGISTRY_API
GOVERNMENT_REGISTRY_EXPORT
GOVERNMENT_REGISTRY_PUBLIC_PAGE
GOVERNMENT_OPEN_DATASET
GOVERNMENT_OPERATOR_REFERENCE
```

## 3. User configuration

```text
jurisdiction
registry_code
mode
credential_reference_id
license_or_open_data_profile_id
entity_types
identifier_queries
name_queries
status_filters
filing_type_filters
date_window
geographic_filters
page_size
maximum_pages
request_budget
field_profile_version
retention_policy_version
attribution_policy_version
operator_review_requirement
```

Every registry connection must identify the issuing authority and jurisdiction.

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Registered entity | Official registration number | Legal existence and identity evidence |
| License or permit | License number | Regulated activity evidence |
| Filing | Filing or document ID | Historical status and event evidence |
| Officer or representative | Registry-specific ID | Officially filed role evidence |
| Registered address | Entity and address record ID | Legal-address evidence |
| Dataset row | Dataset and row key | Open-data evidence |
| Operator reference | Official URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = GOVERNMENT_REGISTRY
source.mode = selected official mode
native.object_type = registered_entity | license | filing | officer | address | dataset_row
native.object_id = official identifier
native.url = official record or document URL
entity_hints.organization_names = registered legal and trading names
entity_hints.person_names = officially filed persons where permitted
entity_hints.addresses = registered addresses
entity_hints.provider_identifiers = registration, tax, license and filing numbers
content.title = filing, license or record title
content.published_at = filing, registration or issue date
signals.domain_codes = mapped regulated activity or entity classification
signals.event_types = incorporation, dissolution, license, renewal, filing, director change or status event
policy.authorization_basis = PUBLIC_API | PUBLIC_WEBSITE_WITH_ROBOTS_COMPLIANCE | LICENSED_DATASET
```

## 6. Example entity envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "GOVERNMENT_REGISTRY", "mode": "GOVERNMENT_REGISTRY_API"},
  "native": {
    "object_type": "registered_entity",
    "object_id": "0325802",
    "url": "https://registry.example/entity/0325802"
  },
  "entity_hints": {
    "organization_names": ["EXAMPLE (SMC-PRIVATE) LIMITED"],
    "addresses": ["Islamabad, Pakistan"],
    "provider_identifiers": [{"type": "CORPORATE_REGISTRATION_NUMBER", "value": "0325802"}]
  },
  "content": {
    "title": "Registered company record",
    "summary": "Official record shows active registration.",
    "language": "en",
    "published_at": "2026-02-09T00:00:00Z",
    "content_type": "official_registry_record"
  },
  "signals": {"event_types": ["INCORPORATION_EVENT"]},
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "JURISDICTION_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
REGISTRY_SUCCESS
REGISTRY_ZERO_RESULTS
REGISTRY_ENTITY_NOT_FOUND
REGISTRY_IDENTIFIER_INVALID
REGISTRY_RECORD_RESTRICTED
REGISTRY_DOCUMENT_UNAVAILABLE
REGISTRY_STATUS_AMBIGUOUS
REGISTRY_RATE_LIMITED
REGISTRY_AUTHENTICATION_FAILED
REGISTRY_DATASET_STALE
REGISTRY_JURISDICTION_UNSUPPORTED
REGISTRY_POLICY_BLOCKED
```

## 8. Provenance and conflict rules

- Preserve issuing authority, jurisdiction, registry code, identifier, record version, filing date, effective date and retrieval date.
- Legal names are not silently replaced by marketing names.
- Registered address, operating address and branch address remain separate claim types.
- Officer or representative listings remain dated filings and may be stale.
- Conflicts between official records and websites remain visible for review.
- One jurisdiction's identifier does not become a universal organization identifier.

## 9. Evidence boundaries

Official registries may strongly support legal existence, legal name, registration status, identifiers, filing dates, official roles, licenses and registered addresses.

They do not independently prove current operations, offered services, active branches, customer demand, service gaps, budget, contact consent or a qualified opportunity.

## 10. Delivery boundary

This document does not implement jurisdiction adapters, API access, page retrieval, document extraction, identifier validation, retention, reconciliation or scoring.