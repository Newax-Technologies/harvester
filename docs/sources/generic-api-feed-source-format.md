# Harvester Generic API, Feed and Licensed Dataset Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines the fallback contract for approved APIs, webhooks, RSS or Atom feeds, XML feeds, SFTP deliveries, object-storage drops, licensed datasets and customer-owned system feeds that do not yet require a dedicated provider document.

It is not a loophole for activating an undocumented source. A source using this contract still requires a named source code, permission basis, schema, mapping, retention policy, failure taxonomy and approval.

## 2. Source modes

```text
GENERIC_REST_API
GENERIC_GRAPHQL_API
GENERIC_WEBHOOK
GENERIC_RSS_ATOM_FEED
GENERIC_XML_JSON_FEED
GENERIC_SFTP_DELIVERY
GENERIC_OBJECT_STORAGE_DELIVERY
GENERIC_LICENSED_DATASET
GENERIC_CUSTOMER_SYSTEM_FEED
```

## 3. User configuration

```text
source_code
provider_name
mode
connection_reference_id
credential_reference_id
authorization_basis
contract_or_license_profile_id
endpoint_or_delivery_reference
request_method
query_or_filter_profile_version
field_profile_version
mapping_profile_version
pagination_policy
cursor_policy
webhook_verification_policy
schedule
freshness_window
request_budget
cost_budget
retention_policy_version
attribution_policy_version
deletion_policy_version
```

## 4. Native objects

The source document must enumerate every provider-native object before activation.

Required metadata for each native object:

```text
object_type
identifier_field
parent_identifier_field
creation_timestamp_field
update_timestamp_field
deletion_state_field
canonical_url_field
pagination_behavior
```

## 5. Canonical formatting

```text
source.code = approved named source code
source.mode = approved generic mode
native.object_type = declared provider object type
native.object_id = declared stable provider identifier
native.parent_id = declared relationship identifier
native.url = permitted canonical URL
entity_hints = mapping-profile output
content = bounded provider content or artifact reference
signals = taxonomy and event extraction output
provenance = endpoint, request, response, delivery, schema and mapping versions
quality = completeness, freshness, conflicts and review state
policy = authorization, retention, attribution, redistribution, model and deletion rules
```

## 6. Example feed envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "EXAMPLE_LICENSED_FEED", "mode": "GENERIC_XML_JSON_FEED"},
  "native": {
    "object_type": "organization_update",
    "object_id": "update-123",
    "parent_id": "organization-55",
    "url": "https://provider.example/records/update-123",
    "payload_ref": "licensed-feed://delivery-77/update-123",
    "payload_hash": "sha256:example"
  },
  "entity_hints": {
    "organization_names": ["Example Organization"],
    "provider_identifiers": [{"type": "EXAMPLE_PROVIDER_ORG_ID", "value": "organization-55"}]
  },
  "content": {
    "title": "Organization update",
    "summary": "Licensed feed reports a new operating location.",
    "language": "en",
    "published_at": "2026-08-01T00:00:00Z",
    "content_type": "provider_update"
  },
  "signals": {"event_types": ["EXPANSION_ANNOUNCEMENT"]},
  "policy": {
    "authorization_basis": "LICENSED_DATASET",
    "retention_policy": "CONTRACT_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

Every source adds source-specific detail beneath the canonical states. Minimum distinctions include:

```text
SUCCESS
SUCCESS_ZERO_RESULTS
SUCCESS_PARTIAL
AUTHENTICATION_FAILED
AUTHORIZATION_FAILED
RATE_LIMITED
QUOTA_EXHAUSTED
INVALID_REQUEST
SCHEMA_CHANGED
SIGNATURE_INVALID
DELIVERY_DUPLICATE
DELIVERY_INCOMPLETE
CHECKSUM_MISMATCH
PARSING_FAILED
LICENSE_BLOCKED
RETENTION_REJECTED
PROVIDER_FAILED
```

## 8. Schema-change controls

- Preserve provider schema version, content type and response or delivery hash.
- Unknown fields do not silently become canonical fields.
- Missing required fields create a schema failure or review state.
- Breaking provider changes require a new mapping profile version.
- Historical observations retain the mapping version used when processed.

## 9. Evidence boundaries

A generic source supports only the claims defined in its approved mapping and evidence profile. It cannot bypass provider-service eligibility, source diversity, corroboration, entity resolution, suppression, contact permission or opportunity qualification.

## 10. Delivery boundary

This document does not implement generic connectors, webhooks, feeds, file deliveries, schema registries, mappings, security, retention or scoring. Each activated source still requires focused tests and provider-specific review.