# Harvester LinkedIn Source Format

Status: **Proposed formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Authorized API architecture is planned; the legacy stealth crawler remains restricted**

Authority: [LinkedIn Authorized Data Source Model](linkedin-authorized-data-source-model.md) remains authoritative for permission, partner access, consent, imports, operator references, retention, privacy, and legacy-crawler removal.

## 1. Source modes

```text
LINKEDIN_ORGANIZATION_AUTHORIZED
LINKEDIN_MEMBER_CONSENTED
LINKEDIN_SALES_NAVIGATOR_PARTNER
LINKEDIN_AUTHORIZED_IMPORT
LINKEDIN_OPERATOR_REFERENCE
LINKEDIN_LEGACY_RESTRICTED_CRAWLER
```

The legacy restricted crawler is not an approved production input mode.

## 2. User configuration

```text
mode
connection_reference_id
credential_reference_id
approved_product
approved_scopes
organization_urns
member_consent_reference
partner_contract_reference
import_authorization_reference
operator_reference_urls
field_profile_version
analytics_metric_profile
freshness_window
retention_policy_version
deletion_policy_version
review_requirement
```

A customer login session, cookie, or browser profile must never be accepted as a credential configuration.

## 3. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Organization | Organization URN | Customer-authorized organization identity and page data |
| Organization post | Share or post URN | Customer-authored announcement or activity evidence |
| Organization analytics | Organization, metric and period | Customer-authorized performance evidence |
| Consented member | Member URN | Consented identity and current-role evidence |
| Partner account or lead | Contract-specific identifier | Approved Sales Navigator workflow only |
| Imported record | Customer or provider external ID | Authorized import evidence |
| Operator reference | LinkedIn URL | Human-reviewed bounded reference |

## 4. Canonical mapping

### Authorized organization

```text
source.code = LINKEDIN
source.mode = LINKEDIN_ORGANIZATION_AUTHORIZED
native.object_type = organization | organization_post | organization_metric
native.object_id = LinkedIn URN
entity_hints.organization_names = authorized organization name
entity_hints.domains = authorized organization website domain
entity_hints.addresses = permitted organization locations
entity_hints.provider_identifiers = organization URN and vanity name
content = customer-authorized Page or post content
signals.event_types = hiring, expansion, partnership, launch, leadership or operational announcement when supported
policy.authorization_basis = CUSTOMER_OAUTH
```

### Consented member

```text
source.mode = LINKEDIN_MEMBER_CONSENTED
native.object_type = member
native.object_id = member URN
entity_hints.person_names = consented member name
entity_hints.emails = consented email when permitted
entity_hints.provider_identifiers = member URN and approved profile reference
signals.job_roles = consented current role
policy.authorization_basis = MEMBER_CONSENT
```

### Authorized import

```text
source.mode = LINKEDIN_AUTHORIZED_IMPORT
native.object_type = imported_professional_record
policy.authorization_basis = CUSTOMER_AUTHORIZED_IMPORT | LICENSED_DATASET
```

### Operator reference

Operator-reference observations contain the URL, operator assertion, observation time, research purpose, and review state. They do not contain automatically extracted profile content.

## 5. Example organization observation

```json
{
  "schema_version": "1.0",
  "source": {"code": "LINKEDIN", "mode": "LINKEDIN_ORGANIZATION_AUTHORIZED"},
  "native": {
    "object_type": "organization_post",
    "object_id": "urn:li:share:123",
    "parent_id": "urn:li:organization:456",
    "url": "https://www.linkedin.com/feed/update/urn:li:share:123"
  },
  "entity_hints": {
    "organization_names": ["Example Health Group"],
    "provider_identifiers": [{"type": "LINKEDIN_ORGANIZATION_URN", "value": "urn:li:organization:456"}]
  },
  "content": {
    "title": null,
    "summary": "Customer-authorized post announced a new branch.",
    "language": "en",
    "published_at": "2026-08-01T08:00:00Z",
    "content_type": "organization_post"
  },
  "signals": {"event_types": ["EXPANSION_ANNOUNCEMENT"]},
  "policy": {
    "authorization_basis": "CUSTOMER_OAUTH",
    "retention_policy": "LINKEDIN_CONNECTION_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 6. Outcome states

```text
LINKEDIN_SUCCESS
LINKEDIN_TOKEN_EXPIRING
LINKEDIN_REAUTHORIZATION_REQUIRED
LINKEDIN_INSUFFICIENT_ADMIN_ROLE
LINKEDIN_SCOPE_REJECTED
LINKEDIN_PRODUCT_UNAVAILABLE
LINKEDIN_PARTNER_ACCESS_UNAVAILABLE
LINKEDIN_CONSENT_EXPIRED
LINKEDIN_CONSENT_REVOKED
LINKEDIN_IMPORT_AUTHORIZATION_MISSING
LINKEDIN_DELETION_PENDING
LINKEDIN_POLICY_BLOCKED
LINKEDIN_LEGACY_CRAWLER_BLOCKED
```

## 7. Retention and deletion

- Organization and member data remain scoped to the approved product, purpose, tenant, and connection.
- Revocation, deletion requests, reduced scopes, and contract termination must propagate to stored observations and derived data where required.
- Imported records retain owner, authorization, license, permitted purpose, retention period, and suppression state.
- Operator references store minimal human assertions and no automated page copies.
- Cookies, browser sessions, anti-detection metadata, and scraped profile payloads are prohibited production records.

## 8. Evidence boundaries

LinkedIn may support customer-authorized organization activity, member-consented identity and role evidence, licensed imports, and approved partner signals.

It does not independently prove procurement authority, budget, service gap, consent to marketing, buying intent, or canonical identity.

## 9. Delivery boundary

This document defines formatting only. It does not authorize or implement LinkedIn access, partner products, imports, consent flows, token handling, deletion workflows, or scoring.