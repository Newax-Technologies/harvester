# Harvester Procurement and Tender Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how official procurement portals, tender systems, request-for-proposal platforms, vendor notices, award notices, customer-authorized procurement exports, and manual references enter Harvester.

Procurement records may provide strong timing and requirement evidence. They do not automatically prove eligibility, fit, availability of budget, award probability, contact consent, or permission to participate.

## 2. Source modes

```text
PROCUREMENT_PORTAL_API
PROCUREMENT_PORTAL_PUBLIC_PAGE
PROCUREMENT_OPEN_DATASET
PROCUREMENT_CUSTOMER_AUTHORIZED_EXPORT
PROCUREMENT_OPERATOR_REFERENCE
```

## 3. User configuration

```text
jurisdiction_or_portal_code
mode
credential_reference_id
license_or_open_data_profile_id
buyer_filters
sector_filters
commodity_codes
service_codes
keywords
publication_date_window
closing_date_window
status_filters
geographic_filters
minimum_and_maximum_value
currency_filters
maximum_pages
request_budget
retention_policy_version
operator_review_requirement
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Buyer or procuring entity | Portal buyer ID | Organization reference |
| Tender or notice | Notice ID | Buying-intent and requirement evidence |
| Lot | Notice and lot ID | Scoped requirement evidence |
| Document | Document ID or checksum | Specification evidence |
| Amendment | Amendment ID | Requirement or deadline change |
| Award | Award ID | Historical supplier and outcome evidence |
| Contract | Contract ID | Historical procurement evidence |
| Operator reference | Official URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = PROCUREMENT
source.mode = selected procurement mode
native.object_type = buyer | tender | lot | document | amendment | award | contract
native.object_id = official portal identifier
native.parent_id = parent notice or buyer identifier
native.url = official record or document URL
entity_hints.organization_names = buyer, issuer and awarded supplier names
entity_hints.provider_identifiers = portal buyer, notice, award and contract IDs
content.title = notice or lot title
content.summary = bounded official description
content.published_at = publication date
signals.service_codes = mapped requested services only when the provider offers them
signals.domain_codes = procurement subject domains
signals.activity_codes = requested or affected activities
signals.event_types = tender, amendment, deadline, award or cancellation
signals.keyword_matches = service and requirement matches
```

## 6. Example tender envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "PROCUREMENT", "mode": "PROCUREMENT_PORTAL_API"},
  "native": {"object_type": "tender", "object_id": "TENDER-2026-123", "parent_id": "BUYER-55", "url": "https://procurement.example/tender/TENDER-2026-123"},
  "entity_hints": {
    "organization_names": ["Example Public Hospital"],
    "provider_identifiers": [
      {"type": "PROCUREMENT_BUYER_ID", "value": "BUYER-55"},
      {"type": "PROCUREMENT_NOTICE_ID", "value": "TENDER-2026-123"}
    ]
  },
  "content": {
    "title": "Hospital inventory and procurement management system",
    "summary": "Official notice requests an integrated inventory and procurement system.",
    "language": "en",
    "published_at": "2026-08-01T00:00:00Z",
    "content_type": "procurement_notice"
  },
  "signals": {
    "service_codes": ["SVC-ERP-INV-001"],
    "event_types": ["TENDER_PUBLISHED"],
    "keyword_matches": ["inventory management", "procurement system"]
  },
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "PORTAL_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
PROCUREMENT_SUCCESS
PROCUREMENT_ZERO_RESULTS
PROCUREMENT_NOTICE_NOT_FOUND
PROCUREMENT_NOTICE_AMENDED
PROCUREMENT_NOTICE_CANCELLED
PROCUREMENT_DEADLINE_PASSED
PROCUREMENT_DOCUMENT_RESTRICTED
PROCUREMENT_DOCUMENT_UNAVAILABLE
PROCUREMENT_BUYER_UNRESOLVED
PROCUREMENT_RATE_LIMITED
PROCUREMENT_POLICY_BLOCKED
```

## 8. Evidence and controls

- Preserve portal, jurisdiction, buyer, notice, lot, document, amendment, deadline, status and retrieval timestamps.
- Amendments create new observations and do not overwrite historical notice state.
- Tender-value fields retain amount, currency, range and source field.
- Requirements in attached documents require checksum-backed artifact provenance.
- Contact details in notices do not automatically create marketing consent.
- Closed, cancelled and awarded notices remain distinct states.

## 9. Evidence boundaries

Procurement sources may provide explicit buying requirements, dates, scopes, buyers, values, documents and awards.

They do not independently prove provider eligibility, competitive position, award likelihood, available budget, legal compliance or permission to contact beyond the procurement rules.

## 10. Delivery boundary

This document does not implement portal connectors, document extraction, deadline monitoring, service matching, eligibility checks, retention or scoring.