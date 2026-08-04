# Harvester User Input Storage Model

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how Harvester stores user, operator, and customer configuration before a Harvest Job begins.

The objective is to preserve exactly what the user intended, prevent silent changes, isolate credentials, support review and approval, and make every completed result reproducible from an immutable input snapshot.

```text
Editable draft
→ validation
→ approval
→ versioned active configuration
→ immutable Harvest Job input snapshot
→ source plans
→ collection and evidence
```

## 2. Stored input layers

Harvester stores inputs in seven separate layers.

### 2.1 Workspace context

```text
WorkspaceDefinition
```

Minimum fields:

```text
id
tenant_id
organization_id
name
timezone
default_country_code
default_language_codes
default_currency_code
status
created_by
created_at
updated_at
```

### 2.2 Provider and offering definition

```text
ProviderDefinitionVersion
ProviderServiceOfferingVersion
```

These records identify who is using Harvester, which services they actually offer, and which service versions may create eligible opportunity assessments.

Minimum provider-service fields:

```text
provider_id
service_code
service_version
service_name
service_description
active_status
delivery_modes
supported_geographies
supported_customer_types
qualification_rules
exclusion_rules
approved_by
approved_at
```

A service that is not active for the provider cannot create a service gap or opportunity.

### 2.3 Market and taxonomy selection

```text
MarketDefinitionVersion
TargetSectorSelection
TargetDomainSelection
TargetDomainActivitySelection
```

Minimum market fields:

```text
id
workspace_id
version
name
objective
country_codes
administrative_areas
cities
geographic_boundaries
organization_size_rules
included_sector_codes
excluded_sector_codes
included_domain_codes
excluded_domain_codes
included_domain_activity_pairs
excluded_domain_activity_pairs
included_organization_types
excluded_organization_types
created_by
approved_by
status
created_at
approved_at
```

Activities are selected independently for each domain. Selecting `Manufacturing` for Pharmaceuticals does not select it for Medical Devices or Food Products.

### 2.4 Keyword and evidence configuration

```text
KeywordProfileSelectionVersion
EvidencePolicySelectionVersion
```

Minimum fields:

```text
market_definition_id
domain_keyword_profile_versions
activity_keyword_profile_versions
service_keyword_profile_versions
locale_keyword_pack_versions
problem_signal_profile_versions
buying_signal_profile_versions
existing_solution_profile_versions
competitor_profile_versions
exclusion_profile_versions
match_modes
minimum_signal_diversity
minimum_source_diversity
coverage_requirements
recency_rules
negative_context_rules
status
```

Canonical keyword profiles remain separate from workspace overrides.

```text
Canonical profile
+
explicit workspace override
=
versioned effective profile
```

No model or feedback process may silently mutate an active keyword profile.

### 2.5 Source selection and configuration

```text
SourceSelectionVersion
SourceConnectionReference
SourceQueryProfileVersion
```

Minimum source-selection fields:

```text
id
market_definition_id
source_code
source_mode
enabled
priority
objective
credential_reference_id
connection_reference_id
query_profile_version
field_profile_version
geography_profile_version
retention_policy_version
attribution_policy_version
compliance_profile_version
request_budget
cost_budget
rate_limit_policy
retry_policy
stopping_rules
operator_review_requirement
status
```

Source-specific configuration is stored in a validated `configuration` object whose schema is owned by the source adapter.

### 2.6 Credential references

Secrets do not belong in ordinary database rows, logs, exports, snapshots, or documentation.

```text
SourceCredentialReference
```

Minimum fields:

```text
id
tenant_id
source_code
secret_provider
secret_path_or_key
credential_type
approved_scopes
owner_reference
status
created_by
last_verified_at
expires_at
revoked_at
```

The record stores a reference to a secret manager, not the secret itself.

Forbidden fields include:

```text
access_token
refresh_token
api_key
password
session_cookie
private_key
client_secret
```

### 2.7 Output, review and destination preferences

```text
OutputPolicyVersion
ReviewPolicyVersion
DestinationSelectionVersion
```

Minimum fields:

```text
required_review_stages
minimum_confidence_dimensions
publication_rules
export_rules
contactability_rules
suppression_rules
selected_destinations
communicator_delivery_enabled
core_sync_enabled
retention_rules
operator_assignment_rules
```

## 3. Draft, approval and activation states

Every editable configuration uses controlled states:

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
ACTIVE
SUPERSEDED
SUSPENDED
REVOKED
ARCHIVED
```

Only an `ACTIVE` approved version may start a production Harvest Job.

Editing an active version creates a new draft. It does not modify the version used by a running or completed job.

## 4. Immutable Harvest Job input snapshot

When a job starts, Harvester creates:

```text
HarvestJobInputSnapshot
```

Minimum fields:

```text
id
harvest_job_id
workspace_id
provider_definition_version
service_offering_versions
market_definition_version
taxonomy_registry_version
domain_activity_mapping_version
keyword_profile_versions
evidence_policy_version
source_selection_version
source_plan_versions
output_policy_version
scoring_profile_version
retention_policy_versions
compliance_profile_versions
created_at
snapshot_hash
```

The snapshot contains configuration values and version references, but replaces credentials with secret-reference identifiers.

Completed results must always remain traceable to this snapshot.

## 5. Validation rules

A production input set is invalid when any of the following is true:

- No active provider service is selected.
- No broad sector is selected.
- A selected sector has no domain.
- A selected domain has no approved activity when activity evidence is required.
- A selected source lacks a source-specific configuration schema.
- A credential reference is missing, expired, revoked, or insufficiently scoped.
- Geography is text-only where systematic geographic coverage requires geometry.
- Cost, request, or stopping limits are absent for a metered source.
- Retention or attribution requirements are unknown.
- The source's permission basis is absent.
- A service-specific opportunity profile is enabled for a service the provider does not offer.

## 6. Audit requirements

Every configuration mutation records:

```text
actor_id
action
entity_type
entity_id
previous_version
new_version
reason
changed_fields
occurred_at
request_id
```

Approval and revocation require an explicit actor and reason.

## 7. Tenant and authorization rules

- Every input record belongs to one tenant.
- Cross-tenant reads and writes are prohibited.
- Users require explicit permissions to edit, approve, activate, revoke, or view credential references.
- Source credentials may be shared only through an approved tenant-owned connection object.
- Customer-authorized social or business accounts must remain linked to the authorizing tenant and organization.

## 8. Example effective input

```json
{
  "workspace_id": "ws_01",
  "provider": {
    "version": 4,
    "active_service_offerings": ["SVC-WMS-001", "SVC-AUTO-004"]
  },
  "market": {
    "version": 7,
    "sectors": ["BS-001"],
    "domains": ["HC-MED-001", "HC-OPS-014"],
    "domain_activities": [
      {"domain": "HC-MED-001", "activities": ["ACT-PRD-016", "ACT-LOG-003"]},
      {"domain": "HC-OPS-014", "activities": ["ACT-LOG-003", "ACT-LOG-004"]}
    ],
    "geography": {"country": "PK", "cities": ["Islamabad", "Rawalpindi"]}
  },
  "sources": [
    {"source": "GOOGLE", "mode": "GOOGLE_PLACES_PUBLIC", "enabled": true},
    {"source": "WEBSITE", "mode": "ORGANIZATION_WEBSITE_PUBLIC", "enabled": true}
  ],
  "budgets": {"maximum_requests": 1000, "maximum_estimated_cost": 50},
  "approval": {"status": "ACTIVE", "approved_by": "user_17"}
}
```

## 9. Delivery boundary

This document defines the storage and versioning contract only. Database schema, migrations, validation services, secret-manager integration, permissions, APIs, UI, snapshot generation, and tests remain separate engineering work.