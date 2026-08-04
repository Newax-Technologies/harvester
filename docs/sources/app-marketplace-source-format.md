# Harvester Application and Marketplace Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how licensed application-store APIs, software marketplaces, integration marketplaces, vendor directories, customer-authorized app inventories, public product pages, and manual references enter Harvester.

Marketplace records may support technology-presence, product, integration, vendor and existing-solution evidence. They do not automatically prove active deployment, usage depth, satisfaction, contract status or replacement intent.

## 2. Source modes

```text
APP_MARKETPLACE_API_LICENSED
APP_MARKETPLACE_PUBLIC_PAGE
VENDOR_MARKETPLACE_AUTHORIZED
CUSTOMER_APP_INVENTORY_AUTHORIZED
APP_MARKETPLACE_AUTHORIZED_IMPORT
APP_MARKETPLACE_OPERATOR_REFERENCE
```

## 3. User configuration

```text
marketplace_code
mode
credential_or_connection_reference_id
license_profile_id
publisher_filters
product_filters
category_filters
integration_filters
platform_filters
country_filters
language_filters
updated_since
maximum_pages
request_budget
retention_policy_version
operator_review_requirement
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Application or product | Marketplace product ID | Software-product evidence |
| Publisher or vendor | Marketplace publisher ID | Vendor identity hint |
| Integration | Integration ID | Technology relationship evidence |
| Category | Marketplace category ID | Source-native classification |
| Release or version | Product and version ID | Freshness and change evidence |
| Review aggregate | Product and period | Bounded reputation context where permitted |
| Customer app inventory item | Customer system ID | Customer-authorized existing-solution evidence |
| Operator reference | Product or publisher URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = APP_MARKETPLACE
source.mode = selected marketplace mode
native.object_type = application | publisher | integration | release | inventory_item
native.object_id = provider product or publisher ID
native.parent_id = publisher or platform ID
native.url = permitted marketplace or vendor URL
entity_hints.organization_names = publisher and vendor names
entity_hints.domains = publisher or product domains
entity_hints.provider_identifiers = marketplace IDs
content.title = product, integration or release name
content.summary = bounded product description
content.published_at = release or update date
signals.technology_mentions = product, platform and integration names
signals.event_types = product launch, integration, update, deprecation or marketplace-removal event
signals = existing-solution evidence only when the organization-product relationship is independently supported
```

## 6. Example product envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "APP_MARKETPLACE", "mode": "APP_MARKETPLACE_API_LICENSED"},
  "native": {"object_type": "application", "object_id": "app-123", "parent_id": "publisher-55", "url": "https://marketplace.example/apps/app-123"},
  "entity_hints": {
    "organization_names": ["Example Software Vendor"],
    "domains": ["examplevendor.com"],
    "provider_identifiers": [
      {"type": "MARKETPLACE_APP_ID", "value": "app-123"},
      {"type": "MARKETPLACE_PUBLISHER_ID", "value": "publisher-55"}
    ]
  },
  "content": {
    "title": "Example Warehouse Integration",
    "summary": "Marketplace listing describes a warehouse integration for an ERP platform.",
    "language": "en",
    "published_at": "2026-07-15T00:00:00Z",
    "content_type": "marketplace_product"
  },
  "signals": {
    "technology_mentions": ["ERP", "warehouse integration"],
    "event_types": ["INTEGRATION_AVAILABLE"]
  },
  "policy": {
    "authorization_basis": "LICENSED_API",
    "retention_policy": "MARKETPLACE_PROVIDER_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
MARKETPLACE_SUCCESS
MARKETPLACE_ZERO_RESULTS
MARKETPLACE_PRODUCT_NOT_FOUND
MARKETPLACE_PRODUCT_REMOVED
MARKETPLACE_VERSION_DEPRECATED
MARKETPLACE_PUBLISHER_UNRESOLVED
MARKETPLACE_RELATIONSHIP_UNVERIFIED
MARKETPLACE_RATE_LIMITED
MARKETPLACE_LICENSE_BLOCKED
MARKETPLACE_POLICY_BLOCKED
```

## 8. Evidence boundaries

Marketplace sources may support product existence, publisher identity, categories, integrations, release dates and customer-authorized software inventories.

A product listing or integration does not independently prove that a target organization uses it. Even confirmed use does not prove dissatisfaction, replacement intent, service gap or purchasing authority.

## 9. Delivery boundary

This document does not implement marketplace adapters, customer inventory imports, relationship verification, retention or scoring.