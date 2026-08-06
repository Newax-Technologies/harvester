# Harvester User Input Storage Model

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how Harvester stores user, operator, and customer configuration before a Harvest Job begins.

The objective is to preserve exactly what the user intended, prevent silent changes, isolate credentials, support several reusable lead-generation profiles without activating all of them, and make every completed result reproducible from an immutable input snapshot.

```text
Editable draft
→ validation
→ approval
→ inactive approved profile version
→ explicit activation or schedule
→ immutable Harvest Job input snapshot
→ source plans
→ collection and evidence
```

Stored configuration is not operational permission.

The locked rule is:

> **Stored does not mean active. Approved does not mean running. Connected does not mean authorized.**

## 2. Stored input layers

Harvester stores inputs in eight separate layers.

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

A workspace may manage one or several provider organizations according to tenant entitlement and permission.

### 2.2 Provider, business-unit and offering portfolio

```text
ProviderOrganizationVersion
ProviderBusinessUnitVersion
OfferingPortfolioVersion
ProviderServiceOfferingVersion
```

These records identify who is using Harvester, which operating unit owns the strategy, everything the provider can offer, and which offering versions may be selected by a lead-generation profile.

Minimum provider fields:

```text
provider_id
provider_version
workspace_id
legal_name
display_name
provider_type
primary_industry
registration_identifiers
default_locale
default_timezone
version_status
operational_status
created_by
approved_by
approved_at
```

Minimum business-unit fields:

```text
business_unit_id
business_unit_version
provider_id
parent_business_unit_id
name
unit_type
geographic_scope
default_delivery_modes
default_owner_team_id
version_status
operational_status
```

Minimum provider-service fields:

```text
offering_id
offering_version
provider_id
business_unit_id
service_definition_id
service_code
service_name
service_description
customer_markets
delivery_modes
supported_geographies
pricing_model
capacity
priority
minimum_opportunity_value
qualification_rules
exclusion_rules
compliance_requirements
effective_from
effective_until
version_status
operational_status
approved_by
approved_at
```

Offering version status:

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
SUPERSEDED
REVOKED
ARCHIVED
```

Offering operational status:

```text
PLANNED
AVAILABLE
PAUSED
CAPACITY_LIMITED
DISCONTINUED
```

A provider may store many offerings.

Only an approved offering version with an operationally eligible status may be selected by an active lead-generation profile.

A service that is merely present in the provider portfolio cannot create a service gap, opportunity, score, export, publication, or outreach context.

### 2.3 Reusable lead-generation profiles

```text
LeadGenerationProfile
LeadGenerationProfileVersion
ProfileOfferingSelection
ProfileActivation
```

A lead-generation profile is one reusable commercial strategy.

A provider may maintain many profiles without activating all of them.

Minimum profile fields:

```text
id
tenant_id
workspace_id
provider_id
business_unit_id
name
description
objective
owner_user_id
owner_team_id
profile_status
created_at
updated_at
archived_at
```

Minimum profile-version fields:

```text
profile_version_id
lead_generation_profile_id
version
provider_definition_version
business_unit_version
name
objective
customer_markets
lead_subject_types
delivery_modes
geographic_scope
organization_size_rules
taxonomy_registry_version
source_policy_version
evidence_policy_version
qualification_policy_version
compliance_policy_version
contact_policy_version
scoring_profile_version
output_policy_version
run_policy_version
version_status
change_reason
created_by
created_at
approved_by
approved_at
supersedes_version_id
```

Profile version status:

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
SUPERSEDED
REVOKED
ARCHIVED
```

A profile version selects a subset of provider offerings:

```text
ProfileOfferingSelection

profile_version_id
service_offering_version_id
priority
capacity_allocation
minimum_opportunity_value_override
qualification_override
exclusion_override
status
```

Profile operational activation remains separate:

```text
ProfileActivation

id
profile_version_id
activation_state
generation_mode
starts_at
ends_at
schedule_rule
timezone
maximum_concurrent_jobs
daily_job_limit
daily_lead_limit
monthly_lead_limit
request_budget
cost_budget
capacity_policy
deduplication_scope
overlap_policy
stopping_rules
notification_policy
activated_by
activated_at
paused_by
paused_at
suspended_reason
```

Activation states:

```text
INACTIVE
ACTIVE
SCHEDULED
PAUSED
SUSPENDED
EXPIRED
COMPLETED
CANCELLED
```

An inactive, paused, suspended, expired, completed, or cancelled profile activation creates no new source plan or production Harvest Job.

Editing an approved or active profile version creates a new draft and does not modify the version pinned by running or completed jobs.

### 2.4 Market and taxonomy selection

```text
MarketDefinitionVersion
ProfileMarketSelection
ProfileSectorSelection
ProfileDomainSelection
ProfileDomainActivitySelection
```

Minimum market fields:

```text
id
profile_version_id
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

Activities are selected independently for each domain.

Selecting `Manufacturing` for Pharmaceuticals does not select it for Medical Devices, Food Products, Textiles, or any other domain.

A market definition without selected provider offerings is commercially incomplete and cannot be approved for production generation.

### 2.5 Keyword, signal and evidence configuration

```text
KeywordProfileSelectionVersion
OpportunitySignalSelectionVersion
EvidencePolicySelectionVersion
```

Minimum fields:

```text
profile_version_id
market_definition_id
domain_keyword_profile_versions
activity_keyword_profile_versions
service_keyword_profile_versions
locale_keyword_pack_versions
opportunity_signal_profile_versions
problem_signal_profile_versions
buying_signal_profile_versions
existing_solution_profile_versions
competitor_profile_versions
exclusion_profile_versions
negative_context_profile_versions
match_modes
minimum_signal_diversity
minimum_source_diversity
coverage_requirements
recency_rules
status
```

Canonical keyword profiles remain separate from workspace and profile overrides.

```text
Canonical profile
+
explicit workspace or profile override
=
versioned effective profile
```

No model, feedback process, source result, or operator convenience may silently mutate an approved or active keyword profile.

Keyword matches create evidence candidates.

They do not independently prove a domain, activity, service gap, purchase intent, opportunity, or qualified lead.

### 2.6 Source selection and configuration

```text
ProfileSourceSelectionVersion
SourceConnectionReference
SourceQueryProfileVersion
```

Minimum source-selection fields:

```text
id
profile_version_id
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
coverage_goal
rate_limit_policy
retry_policy
stopping_rules
operator_review_requirement
status
```

Source-specific configuration is stored in a validated `configuration` object whose schema is owned by the source adapter.

A source connection may be reused by many profiles.

Connection reuse does not activate the source for every profile.

### 2.7 Credential references

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

An expired, revoked, or insufficiently scoped credential affects only the profiles that reference it.

A failed credential replacement leaves the previous valid credential active.

### 2.8 Output, review and destination preferences

```text
OutputPolicyVersion
ReviewPolicyVersion
DestinationSelectionVersion
```

Minimum fields:

```text
profile_version_id
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

Destination connection does not authorize publication.

An active publishing rule and approved payload profile remain required.

## 3. Draft, approval and activation states

Editable configuration and operational activation use separate state machines.

### 3.1 Configuration-version states

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
SUPERSEDED
REVOKED
ARCHIVED
```

### 3.2 Operational states

```text
INACTIVE
ACTIVE
SCHEDULED
PAUSED
SUSPENDED
EXPIRED
COMPLETED
CANCELLED
```

Only an `APPROVED` profile version with an eligible `ACTIVE` or due `SCHEDULED` activation may start a production Harvest Job.

Editing an active version creates a new draft.

It does not modify the version used by a running or completed job.

Approval does not automatically activate the profile.

Activation does not bypass offering availability, credentials, compliance, budget, capacity, overlap, entitlement, or source-policy validation.

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
provider_organization_version
business_unit_version
service_offering_versions
lead_generation_profile_version
profile_activation_id
market_definition_version
taxonomy_registry_version
domain_activity_mapping_version
keyword_registry_version
keyword_profile_versions
opportunity_signal_profile_versions
evidence_policy_version
source_selection_version
source_plan_versions
output_policy_version
scoring_profile_version
retention_policy_versions
compliance_profile_versions
contact_policy_version
destination_policy_versions
created_at
snapshot_hash
```

The snapshot contains configuration values and version references, but replaces credentials with secret-reference identifiers.

Completed results must always remain traceable to this snapshot.

## 5. Validation rules

A production profile or input set is invalid when any of the following is true:

- No provider organization is selected.
- The provider is suspended, retired, or archived.
- No approved and operationally eligible provider offering is selected.
- A selected offering belongs to another provider or unauthorized business unit.
- No customer market or eligible lead-subject type is selected.
- No broad sector is selected where sector targeting is required.
- A selected sector has no domain.
- A selected domain has no approved activity when activity evidence is required.
- A service-specific opportunity profile is enabled for a service the provider does not offer.
- No applicable opportunity signal is selected for a selected offering.
- A selected source lacks a source-specific configuration schema.
- A credential reference is missing, expired, revoked, or insufficiently scoped.
- Geography is text-only where systematic geographic coverage requires geometry.
- Cost, request, capacity, concurrency, or stopping limits are absent where required.
- Active profile allocations exceed an enforced provider or offering capacity limit.
- A blocking overlap or deduplication conflict remains unresolved.
- Retention or attribution requirements are unknown.
- The source's permission basis is absent.
- Compliance, consent, privacy, contact, or human-review rules are incomplete.
- Product entitlement does not permit the requested provider, profile, source, schedule, or concurrency level.
- The profile version is not approved.
- The activation state is not operationally eligible.

## 6. Audit requirements

Every configuration mutation records:

```text
actor_id
action
entity_type
entity_id
provider_id
business_unit_id
profile_id
profile_version
previous_version
new_version
reason
changed_fields
occurred_at
request_id
```

Approval, activation, pause, schedule, suspension, revocation, budget override, capacity override, conflict resolution, and archival require an explicit actor and reason.

## 7. Tenant, provider and authorization rules

- Every input record belongs to one tenant.
- Cross-tenant reads and writes are prohibited.
- Provider and business-unit scope must be enforced independently of workspace access.
- Users require explicit permissions to edit, approve, activate, pause, schedule, run, revoke, or archive a profile.
- Users require separate permissions to manage providers, business units, offerings, budgets, compliance, and credentials.
- Source credentials may be shared only through an approved tenant-owned connection object.
- Customer-authorized social or business accounts must remain linked to the authorizing tenant, provider, organization, and permitted profiles.
- A profile may reference only offerings owned by its provider or an explicitly authorized business-unit relationship.
- High-risk self-approval is configurable and disabled by default for regulated or enterprise deployments.

## 8. Example effective input

```json
{
  "workspace_id": "ws_01",
  "provider": {
    "provider_id": "provider_newax",
    "provider_version": 4,
    "business_unit_id": "bu_connected_infrastructure"
  },
  "profile": {
    "profile_id": "profile_logistics_telemetry_pk",
    "profile_version": 3,
    "activation_id": "activation_92",
    "activation_state": "ACTIVE",
    "generation_mode": "SCHEDULED"
  },
  "selected_service_offerings": [
    "SVC-CONNECTED-INFRA-001",
    "SVC-AUTOMATION-004"
  ],
  "market": {
    "version": 7,
    "sectors": ["BS-012"],
    "domains": ["LOG-FLT-001", "LOG-CLD-001"],
    "domain_activities": [
      {
        "domain": "LOG-FLT-001",
        "activities": ["ACT-LOG-014", "ACT-OPS-021"]
      },
      {
        "domain": "LOG-CLD-001",
        "activities": ["ACT-LOG-004", "ACT-OPS-022"]
      }
    ],
    "geography": {
      "country": "PK",
      "cities": ["Islamabad", "Rawalpindi"]
    }
  },
  "sources": [
    {
      "source": "GOOGLE",
      "mode": "GOOGLE_PLACES_PUBLIC",
      "enabled": true
    },
    {
      "source": "WEBSITE",
      "mode": "ORGANIZATION_WEBSITE_PUBLIC",
      "enabled": true
    }
  ],
  "budgets": {
    "maximum_requests": 1000,
    "maximum_estimated_cost": 50,
    "daily_lead_limit": 25
  },
  "approval": {
    "version_status": "APPROVED",
    "approved_by": "user_17",
    "activation_state": "ACTIVE",
    "activated_by": "user_21"
  }
}
```

Other provider profiles in the same workspace may remain `INACTIVE`, `PAUSED`, `SCHEDULED`, or `ARCHIVED` without participating in this job.

## 9. Scale and overlap requirements

- A workspace may contain many providers according to entitlement.
- A provider may contain many business units.
- A provider may store hundreds of offerings.
- A provider may maintain many lead-generation profiles and profile versions.
- Several profiles may be active concurrently when budgets, capacity, source limits, and product entitlements permit it.
- Profile activation must compile a bounded effective configuration for job execution.
- Ordinary workers must not scan every provider profile to process one source record.
- Overlapping profiles must reuse eligible evidence without duplicating master entities.
- Qualification, opportunity scoring, contact eligibility, and selection remain profile-specific.
- Deduplication scope must be explicit: `PER_JOB`, `PER_PROFILE`, `PER_PROVIDER`, `PER_WORKSPACE`, or `PER_TENANT`.
- Profile overlap and capacity conflicts must be validated before activation.

## 10. Delivery boundary

This document defines the storage, versioning, approval, activation, and immutable-snapshot contract only.

Database schema, migrations, validation services, profile compilation, overlap analysis, capacity controls, schedulers, secret-manager integration, permissions, APIs, UI, snapshot generation, profile-specific assessments, analytics, tests, and releases remain separate engineering work.

Status remains **Proposed / Not implemented**.
