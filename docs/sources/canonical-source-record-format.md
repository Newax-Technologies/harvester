# Harvester Canonical Source Record Format

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines the common record envelope used by every Harvester source adapter.

Provider responses remain source-native. Harvester does not force a Facebook Page, a job posting, a company registry filing, a map place, and a website page into one flattened table. Instead, every adapter produces a consistent envelope around source-specific content.

```text
Source-native payload or artifact
+
canonical provenance and outcome envelope
+
normalized entity and evidence hints
=
Harvester source observation
```

## 2. Four storage layers

### 2.1 Source request

```text
SourceRequestRecord
```

Records what Harvester attempted.

Minimum fields:

```text
id
source_run_id
source_code
source_mode
request_sequence
request_type
query_or_object_reference
request_parameters_redacted
field_profile_version
locale
geography_reference
requested_at
credential_reference_id
request_hash
```

### 2.2 Source response outcome

```text
SourceResponseRecord
```

Records what happened without collapsing failures into an empty list.

Minimum fields:

```text
id
source_request_id
provider_request_id
http_status
outcome_state
provider_error_code
retryable
rate_limit_state
page_cursor_or_token
result_count
retrieved_at
latency_ms
estimated_cost
response_hash
```

Allowed outcome states:

```text
SUCCESS
SUCCESS_ZERO_RESULTS
SUCCESS_PARTIAL
NOT_MODIFIED
AUTHENTICATION_FAILED
AUTHORIZATION_FAILED
CONSENT_REQUIRED
RATE_LIMITED
QUOTA_EXHAUSTED
INVALID_REQUEST
NOT_FOUND
REMOVED_OR_DELETED
ROBOTS_DISALLOWED
POLICY_BLOCKED
LICENSE_BLOCKED
TIMEOUT
NETWORK_FAILED
PROVIDER_FAILED
PARSING_FAILED
RETENTION_REJECTED
CANCELLED
```

### 2.3 Source-native observation

```text
SourceObservation
```

One observation represents one provider-native object or one bounded assertion observed at one time.

Minimum fields:

```text
id
source_run_id
source_request_id
source_code
source_mode
native_object_type
native_object_id
native_parent_id
native_url
observed_at
provider_created_at
provider_updated_at
native_payload_ref
native_payload_retention_class
payload_hash
```

### 2.4 Normalized claims and evidence

```text
SourceClaim
EvidenceArtifact
```

A claim is one explicit statement derived from an observation.

Examples:

```text
organization name is X
organization operates at location Y
organization website is Z
page published a hiring announcement
job posting requests ERP experience
registry filing lists incorporation date
website offers cold-chain services
```

Minimum claim fields:

```text
id
observation_id
claim_type
subject_hint
predicate
value
value_type
normalized_value
source_field_path
extraction_method
extraction_version
confidence
freshness_state
verification_state
policy_state
created_at
```

## 3. Canonical observation envelope

```json
{
  "schema_version": "1.0",
  "observation_id": "obs_01",
  "source": {
    "code": "GOOGLE",
    "mode": "GOOGLE_PLACES_PUBLIC",
    "connection_id": null,
    "run_id": "run_01",
    "request_id": "req_14"
  },
  "native": {
    "object_type": "place",
    "object_id": "provider-id",
    "parent_id": null,
    "url": "https://provider.example/object/provider-id",
    "created_at": null,
    "updated_at": null,
    "payload_ref": "transient://payload/abc",
    "payload_hash": "sha256:..."
  },
  "entity_hints": {
    "organization_names": [],
    "person_names": [],
    "domains": [],
    "emails": [],
    "phones": [],
    "addresses": [],
    "coordinates": [],
    "provider_identifiers": []
  },
  "content": {
    "title": null,
    "summary": null,
    "body_ref": null,
    "language": "en",
    "published_at": null,
    "content_type": null
  },
  "signals": {
    "domain_codes": [],
    "activity_codes": [],
    "service_codes": [],
    "keyword_matches": [],
    "event_types": [],
    "technology_mentions": [],
    "job_roles": []
  },
  "provenance": {
    "observed_at": "2026-08-04T10:00:00Z",
    "source_field_paths": [],
    "extractor_version": "1.0",
    "request_hash": "sha256:...",
    "response_hash": "sha256:..."
  },
  "quality": {
    "completeness": "PARTIAL",
    "freshness": "CURRENT",
    "identity_confidence": null,
    "content_confidence": null,
    "conflict_flags": [],
    "review_required": false
  },
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "SOURCE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false,
    "expires_at": null
  }
}
```

## 4. Normalized field standards

- Timestamps use UTC ISO 8601.
- Countries use ISO 3166-1 alpha-2 where known.
- Currencies use ISO 4217.
- Languages use BCP 47 or an approved provider locale mapping.
- Phone numbers use E.164 when validation is possible; the original formatted value is also retained when permitted.
- URLs are normalized but the original provider URL is preserved.
- Coordinates use WGS 84 with latitude and longitude stored separately from provider-native geometry.
- Money values store amount, currency, and unit or period.
- Counts remain source-native measurements and retain their observation timestamp.
- Provider identifiers never replace Harvester canonical identifiers.

## 5. Detection and absence states

Each claim uses one of:

```text
PRESENT
NOT_DETECTED
UNKNOWN
CONFLICTING
STALE
REMOVED
CONFIRMED_ABSENT
```

`CONFIRMED_ABSENT` is not assigned merely because one source omitted a field or returned no results. It requires the evidence and coverage rules defined by the applicable opportunity model.

## 6. Raw payload policies

Raw payload handling is selected per source and object type:

```text
PERSIST_FULL
PERSIST_REDACTED
PERSIST_HASH_ONLY
PERSIST_REFERENCE_ONLY
TRANSIENT_EXTRACT_AND_DELETE
CUSTOMER_CONTROLLED_IMPORT
PROHIBITED
```

The source-specific policy overrides the generic desire to preserve immutable raw evidence.

## 7. Provenance and independent verification

Source-derived facts remain attributed to the source.

When a provider supplies a research path and Harvester verifies it independently, two observations are created.

```text
Map provider returns website URL
→ map-provider observation
→ website fetched directly
→ website observation
→ independently supported website claim
```

The independent claim must not be represented as if it were permanently licensed provider content.

## 8. Identity and deduplication

Adapters supply identity hints only.

Possible hints include:

```text
provider organization ID
provider person ID
legal registration number
website domain
phone
email
address
coordinates
social profile URL
```

Entity resolution decides whether observations refer to the same person, organization, branch, product, or location.

Overlapping sources must not duplicate opportunities, scores, exports, or outreach packages.

## 9. Evidence boundaries

A source observation may support:

- organization existence
- location or branch evidence
- product or service domain evidence
- activity evidence
- public contact-path evidence
- hiring or expansion events
- technology mentions
- customer-authorized performance signals
- public statements and announcements

It does not independently prove:

- service absence
- buying authority
- budget
- consent to contact
- legal ownership
- canonical identity
- opportunity qualification
- permission to republish

## 10. Minimum adapter contract

Every adapter must implement or document:

```text
validate_configuration
validate_connection
build_source_plan
build_requests
execute_request
classify_outcome
parse_native_objects
create_observations
extract_claims
apply_retention_policy
apply_attribution_policy
report_coverage
report_cost
report_failures
```

## 11. Delivery boundary

This document defines the shared contract. It does not implement storage, schemas, APIs, queues, connectors, parsing, extraction, entity resolution, evidence scoring, retention jobs, or user interfaces.