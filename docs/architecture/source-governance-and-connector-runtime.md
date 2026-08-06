# Source Governance and Connector Runtime

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned; current source adapters and static policy declarations remain partial**

## 1. Purpose

This document defines how Harvester discovers, authorizes, prices, executes, monitors, retains, and decommissions external source and destination integrations.

A connector is not permission. Public visibility is not universal reuse authority. A working parser is not a lawful or commercially sustainable integration.

## 2. Source classes

Every source belongs to one governed access class:

```text
OFFICIAL_PUBLIC_API
CUSTOMER_AUTHORIZED_OAUTH
APPROVED_PARTNER_API
LICENSED_DATA_FEED
OPEN_DATASET
BULK_DOWNLOAD
RSS_OR_ATOM
WEBHOOK
CUSTOMER_UPLOAD
CUSTOMER_DATABASE
PERMITTED_PUBLIC_WEB
MANUAL_RESEARCH
RESTRICTED
PROHIBITED
```

A source may expose several access classes. Each class receives a separate policy and connector capability declaration.

## 3. Source registry

```text
SourceDefinition

id
stable_code
owner
source_family
access_classes
commercial_status
legal_contact
support_contact
documentation_reference
terms_reference
privacy_reference
status
created_at
updated_at
```

Source status:

```text
DRAFT
UNDER_REVIEW
APPROVED
RESTRICTED
SUSPENDED
DEPRECATED
PROHIBITED
```

## 4. Source policy version

```text
SourcePolicyVersion

id
source_id
version
access_class
permitted_purposes
prohibited_purposes
authorization_type
required_scopes
app_review_required
user_consent_required
rate_limit_policy_id
pricing_policy_id
caching_allowed
maximum_cache_duration
retention_limit
redistribution_allowed
derivative_use_allowed
attribution_required
personal_data_classes
sensitive_data_classes
allowed_regions
prohibited_regions
deletion_requirements
terms_version
verified_at
verified_by
status
```

An activated policy version is immutable. A terms or permission change creates a new version and may suspend affected connectors or jobs.

## 5. Purpose registry

Collection, storage, analysis, export, publication, contact preparation, and customer reporting are separate purposes.

Initial purpose codes:

```text
MARKET_RESEARCH
ACCOUNT_DISCOVERY
CONTACT_RESEARCH
COMPETITOR_MONITORING
PROCUREMENT_MONITORING
PARTNERSHIP_DISCOVERY
RECRUITMENT_RESEARCH
CUSTOMER_DATA_ENRICHMENT
DATA_VERIFICATION
CAMPAIGN_MEASUREMENT
CLIENT_REPORTING
CRM_PUBLICATION
COMMUNICATION_PREPARATION
MODEL_EVALUATION
```

A source approved for market research is not automatically approved for contact preparation or redistribution.

## 6. Connection profile

```text
ConnectionProfile

id
tenant_id
workspace_id
source_or_destination_id
connector_definition_id
environment
endpoint_metadata
region
access_mode
purpose_scope
credential_reference
health_state
status
created_at
updated_at
```

Access modes:

```text
READ_ONLY
IMPORT
EXPORT
WRITE
BIDIRECTIONAL
INSPECTION_ONLY
```

## 7. Credential lifecycle

Credentials are write-only and stored through a vault abstraction.

```text
CredentialReference

id
tenant_id
workspace_id
connection_id
credential_type
vault_reference
fingerprint
scope_summary
created_at
rotated_at
expires_at
revoked_at
status
```

The browser, logs, reports, APIs, and database rows must never return stored plaintext secrets after submission.

Credential replacement follows:

```text
candidate secret
→ validation
→ capability and scope inspection
→ approval when required
→ activation
→ previous-secret retirement
```

A failed replacement leaves the current credential active.

## 8. Connector definition

```text
ConnectorDefinition

id
stable_code
version
source_or_destination_id
runtime_type
capabilities
supported_access_classes
supported_authentication
supported_regions
schema_discovery
incremental_sync
webhook_support
write_support
deletion_support
health_check_support
status
```

Every connector implements the equivalent of:

```text
describe()
authorize()
discover_schema()
validate_configuration()
estimate_cost()
check_policy()
read()
write()
get_state()
set_state()
handle_rate_limit()
handle_webhook()
test_connection()
revoke()
delete_data()
```

Unsupported capabilities fail explicitly.

## 9. Source schema registry

```text
SourceSchemaVersion

id
connection_or_source_id
schema_name
version
field_definitions
sample_reference
compatibility_classification
activated_at
deprecated_at
```

A changed external schema must not silently reuse an incompatible mapping.

## 10. Mapping profile

```text
MappingProfileVersion

id
tenant_id
workspace_id
source_schema_version_id
target_contract_version
rules
validation_rules
quarantine_rules
status
created_by
approved_by
activated_at
```

Rules may include direct mapping, rename, constants, conditions, enum translation, split, combine, lookup, normalization, metadata, ignore, and review.

Source schemas map into Harvester contracts. They do not become Harvester's internal model.

## 11. Rate-limit registry

```text
RateLimitPolicyVersion

id
source_id
endpoint_or_operation
window
limit
burst_limit
concurrency_limit
quota_scope
header_mapping
retry_behavior
verified_at
```

Runtime state records observed remaining quota, reset time, throttling, and provider responses.

## 12. Pricing registry

```text
PricingPolicyVersion

id
provider_id
product_or_endpoint
billing_unit
unit_price
currency
minimum_charge
tier_rules
free_allowance
effective_from
effective_until
verified_at
```

Prices and limits are dated operational data. They must not be hard-coded permanently into business logic or documentation claims.

## 13. Execution gate

Every connector execution follows:

```text
Request
→ tenant and workspace scope
→ purpose
→ source and access class
→ active policy version
→ credential and scopes
→ consent and data-class rules
→ region and retention
→ redistribution and output restrictions
→ quota and cost estimate
→ budget and approval
→ execute
```

The gate returns:

```text
APPROVED
REVIEW_REQUIRED
BLOCKED
```

A connector must not execute when the policy service is unavailable unless an explicitly approved fail-closed offline policy exists.

## 14. Harvest Job relationship

A `HarvestJob` owns one or more `SourcePlan` records. Each source plan pins:

- connector version;
- source policy version;
- source schema version;
- mapping version;
- pricing version;
- rate-limit version;
- query or scope;
- geography partition;
- expected cost;
- quota;
- priority;
- coverage goal;
- stop condition.

Completed jobs retain all pinned versions.

## 15. Source run state

```text
SourceRun

id
source_plan_id
attempt
stage
status
cursor
checkpoint
lease_owner
heartbeat_at
records_examined
observations_created
records_rejected
records_quarantined
cost_consumed
quota_consumed
started_at
completed_at
failure_class
```

One source failure does not erase or roll back accepted results from another source.

## 16. Public-web boundary

Permitted public-web collection requires:

- an approved source and purpose policy;
- robots and access-control handling;
- SSRF and redirect protection;
- request identification and rate control;
- content-size and media-type limits;
- copyright, privacy, retention, and redistribution review;
- clear blocked, skipped, failed, and incomplete coverage states.

Harvester must not treat CAPTCHA solving, stealth fingerprinting, login automation, access-control bypass, or provider evasion as ordinary enterprise functionality.

## 17. Professional-network boundary

Professional-network collection is `RESTRICTED` by default.

Allowed paths may include:

- officially approved APIs;
- customer-authorized exports;
- licensed providers;
- approved partner feeds;
- manual business research;
- user-submitted source references.

Current account-farm, stealth-browser, fingerprint-evasion, or CAPTCHA-solving functionality must remain disabled from production profiles and removed from supported product claims.

## 18. Data classes

At minimum, connector policies distinguish:

```text
PUBLIC_ORGANIZATION_DATA
PUBLIC_PROFESSIONAL_DATA
CUSTOMER_OWNED_DATA
LICENSED_DATA
PERSONAL_DATA
SENSITIVE_PERSONAL_DATA
HEALTH_DATA
STUDENT_DATA
PAYMENT_DATA
AUTHENTICATION_DATA
SECRET_DATA
```

Sensitive classes require stricter storage, AI, export, retention, and review rules. Some combinations are prohibited entirely.

## 19. Runtime economics

Every execution records:

- tenant;
- workspace and client;
- provider and endpoint;
- connector and policy versions;
- requests, pages, records, tokens, retries, and cache hits;
- actual and estimated cost;
- accepted observations;
- verified entities;
- qualified leads;
- cost per accepted result;
- cost per qualified opportunity.

## 20. Failure and suspension

Automatic suspension may occur when:

- credentials are revoked;
- terms change;
- app approval expires;
- rate or cost thresholds are exceeded;
- repeated provider errors occur;
- data leakage or policy violations are detected;
- source output no longer matches the active schema;
- security review marks the connector unsafe.

Suspension prevents new work but preserves audit, evidence, and historical job meaning.

## 21. Required tests

Tests must prove:

1. no connector runs without an active policy and permitted purpose;
2. tenant credentials cannot be used by another tenant;
3. unsupported scopes and operations fail closed;
4. rate limits and retries preserve checkpoints and idempotency;
5. terms and policy changes suspend affected new work;
6. cost estimates and actual costs are recorded;
7. source schemas cannot silently reuse incompatible mappings;
8. restricted professional-network paths cannot activate;
9. retention and deletion obligations reach raw observations and artifacts;
10. destination write access is separately approved from source read access.

## 22. Locked rule

> Connection means technical reachability. Policy, purpose, authority, and approval determine whether Harvester may use it.
