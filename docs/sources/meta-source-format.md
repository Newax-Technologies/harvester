# Harvester Meta and Instagram Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**  
External-reference review: **Meta Graph API, Pages API and Instagram professional-account documentation must be revalidated before implementation**

## 1. Purpose

This document defines how customer-authorized Facebook Page, Instagram professional-account, Meta Business, webhook, and authorized import records may enter Harvester.

Harvester must not treat Meta as an unrestricted public business directory or use browser automation to collect profiles, posts, followers, comments, groups, or personal accounts.

## 2. Source modes

```text
META_FACEBOOK_PAGE_AUTHORIZED
META_INSTAGRAM_PROFESSIONAL_AUTHORIZED
META_BUSINESS_AUTHORIZED
META_WEBHOOK_AUTHORIZED
META_AUTHORIZED_IMPORT
META_OPERATOR_REFERENCE
```

## 3. Permission basis

| Mode | Required basis |
| --- | --- |
| Facebook Page | Customer OAuth, approved app, Page access and required permissions |
| Instagram professional | Customer authorization for a Business or Creator account and approved API permissions |
| Meta Business | Customer-controlled business and asset authorization |
| Webhook | Approved subscription, verified callback and authorized asset |
| Import | Customer-owned or licensed export with declared purpose |
| Operator reference | Manual URL and bounded operator assertion only |

Harvester must not accept copied access tokens, login cookies, browser storage, personal passwords, or undocumented endpoints.

## 4. User configuration

```text
mode
connection_reference_id
credential_reference_id
meta_app_reference
business_reference
page_ids
instagram_account_ids
approved_permissions
webhook_subscription_types
field_profile_version
metric_profile_version
content_window
freshness_window
retention_policy_version
deletion_policy_version
operator_reference_urls
```

Only assets explicitly selected and authorized by the customer may be queried.

## 5. Native objects

| Native object | Identifier | Primary role |
| --- | --- | --- |
| Facebook Page | Page ID | Customer organization and asset reference |
| Page post | Post ID | Customer-authored announcement or activity evidence |
| Page insight | Page, metric and period | Customer-authorized performance signal |
| Instagram professional account | Instagram user ID | Customer-authorized professional presence |
| Instagram media | Media ID | Customer-authored content and event evidence |
| Instagram insight | Account or media, metric and period | Customer-authorized engagement signal |
| Comment or message event | Provider object ID | Customer-authorized operational event only |
| Webhook event | Event and object IDs | Change notification and refresh trigger |
| Authorized import row | Customer external ID | Customer-owned historical record |
| Operator reference | Public URL | Manual navigation and bounded assertion |

## 6. Canonical formatting

### Facebook Page or Instagram account

```text
source.code = META
source.mode = selected authorized mode
native.object_type = facebook_page | instagram_professional_account
native.object_id = provider asset ID
entity_hints.organization_names = authorized account or Page name
entity_hints.domains = authorized website field when permitted
entity_hints.emails = authorized business contact field when permitted
entity_hints.phones = authorized business contact field when permitted
entity_hints.addresses = authorized business location fields when permitted
entity_hints.provider_identifiers = Page, Business or Instagram account IDs
policy.authorization_basis = CUSTOMER_OAUTH
```

### Post or media observation

```text
native.object_type = facebook_page_post | instagram_media
native.object_id = provider content ID
native.parent_id = authorized Page or professional-account ID
content.summary = permitted caption or message excerpt
content.published_at = provider timestamp
content.content_type = post | reel | image | video | story where supported
signals.event_types = expansion, launch, hiring, event, campaign or operational announcement hypotheses
```

### Insight observation

```text
native.object_type = page_metric | account_metric | media_metric
native.object_id = asset + metric + period
content = no raw personal audience data
signals = aggregated customer-authorized performance measurements
```

## 7. Example observation

```json
{
  "schema_version": "1.0",
  "source": {"code": "META", "mode": "META_INSTAGRAM_PROFESSIONAL_AUTHORIZED"},
  "native": {
    "object_type": "instagram_media",
    "object_id": "17890000000000000",
    "parent_id": "17840000000000000",
    "url": "https://www.instagram.com/p/example/"
  },
  "entity_hints": {
    "organization_names": ["Example Hospitality Group"],
    "provider_identifiers": [{"type": "INSTAGRAM_PROFESSIONAL_ACCOUNT_ID", "value": "17840000000000000"}]
  },
  "content": {
    "summary": "Customer-authorized post announced a new location.",
    "language": "en",
    "published_at": "2026-08-01T12:00:00Z",
    "content_type": "instagram_media"
  },
  "signals": {"event_types": ["EXPANSION_ANNOUNCEMENT"]},
  "policy": {
    "authorization_basis": "CUSTOMER_OAUTH",
    "retention_policy": "META_CONNECTION_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 8. Outcome states

```text
META_SUCCESS
META_TOKEN_EXPIRING
META_REAUTHORIZATION_REQUIRED
META_ASSET_NOT_AUTHORIZED
META_PERMISSION_REJECTED
META_APP_REVIEW_REQUIRED
META_OBJECT_REMOVED
META_WEBHOOK_SIGNATURE_INVALID
META_WEBHOOK_DELIVERY_DUPLICATE
META_RATE_LIMITED
META_DATA_ACCESS_EXPIRED
META_DELETION_REQUIRED
META_POLICY_BLOCKED
```

## 9. Webhook rules

- Verify signatures and application secrets.
- Treat webhooks as refresh triggers, not complete source truth.
- Deduplicate deliveries by provider event and object identifiers.
- Fetch current authorized state after the event when required.
- Preserve event time, delivery time, retry number, and verification result.

## 10. Privacy, retention and deletion

- Personal Facebook and Instagram accounts are out of scope unless the person explicitly consents through an approved product and purpose.
- Audience and engagement metrics remain aggregated.
- Direct messages, comments, and customer-service content require a separate operational purpose and stricter personal-data policy.
- Revocation, asset removal, app deauthorization, and customer deletion requests must trigger source-specific deletion and reauthorization workflows.
- Public visibility does not grant automated collection or redistribution rights.

## 11. Evidence boundaries

Authorized Meta data may support customer-owned presence, content activity, campaigns, location announcements, aggregated engagement, and operational change signals.

It does not independently prove service gaps, purchasing authority, budget, consent to cold outreach, or legal identity.

## 12. Delivery boundary

This document does not implement Meta Login, Graph API calls, Instagram authorization, webhooks, token storage, app review, deletion callbacks, source parsing, or scoring.