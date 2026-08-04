# Harvester Crunchbase Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**  
External-reference review: **Crunchbase API package, export, MCP, field, attribution, redistribution and license terms must be confirmed for the selected product before implementation**

## 1. Purpose

This document defines how licensed Crunchbase API, export, MCP, customer-authorized workspace, and manual operator-reference records may enter Harvester.

Crunchbase is a licensed company and private-market data source. Public visibility of a Crunchbase profile does not authorize scraping, bulk copying, redistribution, or use outside the active agreement.

## 2. Source modes

```text
CRUNCHBASE_API_LICENSED
CRUNCHBASE_EXPORT_LICENSED
CRUNCHBASE_MCP_LICENSED
CRUNCHBASE_AUTHORIZED_IMPORT
CRUNCHBASE_OPERATOR_REFERENCE
```

## 3. User configuration

```text
mode
credential_or_connection_reference_id
license_profile_id
api_package
organization_queries
people_queries
funding_queries
acquisition_queries
investor_queries
location_filters
industry_filters
updated_since
field_profile_version
maximum_results
maximum_pages
request_budget
cost_budget
retention_policy_version
attribution_policy_version
export_reference
operator_reference_urls
```

Only fields and entity types available under the selected Crunchbase package may be requested or stored.

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Organization | Crunchbase UUID or permalink | Company identity and market context |
| Person | Crunchbase UUID | Leadership or professional evidence where licensed |
| Funding round | Funding-round UUID | Financing and growth event evidence |
| Acquisition | Acquisition UUID | Ownership and transaction event evidence |
| Investor | Investor UUID | Investor relationship evidence |
| Location | Location identifier | Headquarters or operating-location hint |
| Category group | Category identifier | Source-native industry classification |
| Prediction or insight | Product-specific ID | Licensed forward-looking signal |
| Export row | Dataset and record ID | Licensed batch record |
| Operator reference | Crunchbase profile URL | Manual navigation and bounded assertion |

## 5. Canonical formatting

### Organization observation

```text
source.code = CRUNCHBASE
source.mode = selected licensed mode
native.object_type = organization
native.object_id = Crunchbase UUID
native.url = permitted profile URL
entity_hints.organization_names = legal, display and alias names when supplied
entity_hints.domains = website domain
entity_hints.addresses = headquarters and permitted location fields
entity_hints.provider_identifiers = UUID and permalink
signals.domain_codes = mapped from Crunchbase categories, never copied directly as canonical taxonomy
signals.event_types = founded, closed, funding, acquisition, leadership or growth events when supported
policy.authorization_basis = LICENSED_DATASET
```

### Funding or acquisition observation

```text
native.object_type = funding_round | acquisition
native.object_id = provider UUID
native.parent_id = organization UUID
content.published_at = announced or completed date
signals.event_types = FUNDING_EVENT | ACQUISITION_EVENT
signals = source-native amounts, currencies, stages and participants with field-level provenance
```

## 6. Example organization envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "CRUNCHBASE", "mode": "CRUNCHBASE_API_LICENSED"},
  "native": {
    "object_type": "organization",
    "object_id": "uuid-example",
    "url": "https://www.crunchbase.com/organization/example-company"
  },
  "entity_hints": {
    "organization_names": ["Example Company"],
    "domains": ["example.com"],
    "addresses": ["Karachi, Pakistan"],
    "provider_identifiers": [
      {"type": "CRUNCHBASE_UUID", "value": "uuid-example"},
      {"type": "CRUNCHBASE_PERMALINK", "value": "example-company"}
    ]
  },
  "signals": {
    "domain_codes": ["TECH-SW-001"],
    "event_types": ["FUNDING_EVENT"]
  },
  "policy": {
    "authorization_basis": "LICENSED_DATASET",
    "retention_policy": "CRUNCHBASE_LICENSE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
CRUNCHBASE_SUCCESS
CRUNCHBASE_ZERO_RESULTS
CRUNCHBASE_PACKAGE_FIELD_UNAVAILABLE
CRUNCHBASE_ENTITY_NOT_FOUND
CRUNCHBASE_RATE_LIMITED
CRUNCHBASE_QUOTA_EXHAUSTED
CRUNCHBASE_LICENSE_EXPIRED
CRUNCHBASE_EXPORT_UNAVAILABLE
CRUNCHBASE_MCP_UNAVAILABLE
CRUNCHBASE_ATTRIBUTION_REQUIRED
CRUNCHBASE_REDISTRIBUTION_BLOCKED
CRUNCHBASE_POLICY_BLOCKED
```

## 8. Retention and licensing

- Every connection references a versioned license profile.
- Store package name, endpoint or tool, requested fields, observation date, provider update date, and response hash.
- Redistribution, sublicensing, exports, customer display, model use, and retention follow the selected agreement.
- Provider `updated_at` supports freshness checks but does not prove each field changed at that time.
- Licensed predictions and insights remain separately labeled from historical facts.
- Operator references do not authorize automatic profile extraction.

## 9. Evidence boundaries

Crunchbase may support company identity hints, categories, locations, leadership, funding, acquisitions, investors, growth events, and licensed private-market insights.

It cannot independently prove legal identity in every jurisdiction, current service gaps, technology needs, procurement authority, contact consent, or a qualified opportunity.

## 10. Delivery boundary

This document does not implement Crunchbase licensing, API access, exports, MCP connections, imports, parsing, attribution, deletion, evidence extraction, or scoring.