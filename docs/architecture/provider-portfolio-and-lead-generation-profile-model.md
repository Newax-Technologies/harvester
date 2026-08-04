# Harvester Provider Portfolio and Lead-Generation Profile Model

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

Authority:

- [Harvester Standalone Product Roadmap](../ROADMAP.md) remains the authoritative 64-module delivery roadmap.
- [Harvester Intelligence Operating Model](harvester-intelligence-operating-model.md) remains authoritative for control, evidence, decisions, operations, and learning.
- [Harvester Services and Opportunity Model](../SERVICES.md) remains authoritative for provider, offering, market, signal, qualification, and universal generation rules.
- [Harvester User Input Storage Model](../sources/user-input-storage-model.md) remains authoritative for versioned configuration storage and immutable job snapshots.
- This document strengthens the provider-portfolio, reusable-profile, activation, scheduling, overlap, first-page, and scale model without creating another top-level module count.

## 1. Decision

The provider offering is a mandatory first-page input.

However, it must not be treated as one temporary field that the user re-enters for every run.

Harvester must distinguish:

```text
Provider organization
→ optional business unit or brand
→ complete offering portfolio
→ reusable lead-generation profiles
→ independently approved profile versions
→ independently activated schedules or runs
→ immutable Harvest Job snapshots
```

A company may maintain many offerings and many lead-generation profiles without activating all of them.

The locked rule is:

> **Stored does not mean active. Approved does not mean running. Connected does not mean authorized.**

Only an explicitly approved and operationally active profile version may create a production Harvest Job.

## 2. Why the existing model needs strengthening

A provider profile plus a saved search configuration is insufficient for complex organizations.

It does not fully define:

- several brands, divisions, branches, practices, or business units under one company;
- a portfolio containing many services that are not all promoted at the same time;
- several lead-generation strategies for the same service;
- different markets, geographies, sectors, signals, sources, budgets, and compliance rules per strategy;
- inactive, paused, seasonal, scheduled, experimental, or archived strategies;
- profile ownership, approval, capacity, concurrency, and spend controls;
- overlap detection between profiles;
- shared evidence reuse without duplicate organizations or duplicated costs;
- independent performance measurement and governed improvement per profile.

Without these boundaries, one company-level configuration becomes a giant mutable form. That is not scalability. It is a spreadsheet wearing a database badge.

## 3. Core object hierarchy

### 3.1 Tenant

The customer-isolation boundary.

One tenant may contain one or more workspaces according to product entitlement.

### 3.2 Workspace

The operating boundary for users, permissions, configuration, jobs, leads, costs, and audit.

A workspace may manage one provider or several approved provider organizations.

Examples:

- one company operating one brand;
- a holding company operating several subsidiaries;
- an agency managing lead generation for several clients;
- a group practice containing several clinics;
- a nonprofit network operating several programs.

### 3.3 ProviderOrganization

The stable organization or professional entity whose demand Harvester is finding.

```text
ProviderOrganization

id
tenant_id
workspace_id
legal_name
display_name
provider_type
registration_identifiers
primary_industry
default_locale
default_timezone
status
created_at
updated_at
```

Provider status:

```text
DRAFT
ACTIVE
SUSPENDED
RETIRED
ARCHIVED
```

Provider status controls whether its configuration may be used. It does not independently activate an offering or lead-generation profile.

### 3.4 ProviderBusinessUnit

An optional operating division, brand, branch, practice, product line, regional team, or subsidiary.

```text
ProviderBusinessUnit

id
provider_organization_id
parent_business_unit_id
name
unit_type
geographic_scope
default_delivery_modes
default_owner_team_id
status
created_at
updated_at
```

Examples:

- NEWAX Enterprise Software;
- NEWAX Intelligent Automation;
- NEWAX Connected Infrastructure;
- a pharmaceutical company's manufacturing division;
- the same company's distribution division;
- a law firm's corporate-practice group;
- a hospital group's diagnostics business unit.

A business unit inherits nothing operationally unless an explicit effective-configuration rule says so.

### 3.5 OfferingPortfolio

The controlled catalogue of everything a provider or business unit can offer.

```text
OfferingPortfolio

id
provider_organization_id
business_unit_id
name
description
status
created_at
updated_at
```

A portfolio may contain hundreds of offerings. Portfolio membership does not make every offering eligible for every profile.

### 3.6 ProviderServiceOfferingVersion

A versioned description of one service, product, referral capability, program, or commercial offer.

```text
ProviderServiceOfferingVersion

id
offering_id
version
provider_organization_id
business_unit_id
service_definition_id
service_code
name
description
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
created_by
approved_by
approved_at
```

Version status:

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
SUPERSEDED
REVOKED
ARCHIVED
```

Offering operational status remains separate:

```text
PLANNED
AVAILABLE
PAUSED
CAPACITY_LIMITED
DISCONTINUED
```

Only an `APPROVED` offering version with operational status `AVAILABLE` or an explicitly allowed `CAPACITY_LIMITED` state may be selected by an active lead-generation profile.

## 4. Lead-generation profile

### 4.1 Purpose

A `LeadGenerationProfile` is one reusable commercial strategy.

It answers:

- Which provider or business unit is seeking demand?
- Which selected offerings are in scope?
- Which customer markets and lead-subject types are eligible?
- Which sectors, domains, and domain-specific activities are targeted?
- Which geographies and delivery modes apply?
- Which signals and keyword profiles indicate relevance?
- Which qualification, exclusion, evidence, compliance, and contact rules apply?
- Which sources may be used?
- Which cost, capacity, schedule, output, and stopping rules apply?

A profile is not a lead list, campaign, source connection, saved filter, or Harvest Job.

### 4.2 LeadGenerationProfile

```text
LeadGenerationProfile

id
tenant_id
workspace_id
provider_organization_id
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

Profile status describes the logical record:

```text
DRAFT
READY
ACTIVE_CONFIGURATION_EXISTS
SUSPENDED
ARCHIVED
```

The actual editable configuration belongs to a version.

### 4.3 LeadGenerationProfileVersion

```text
LeadGenerationProfileVersion

id
lead_generation_profile_id
version
provider_definition_version
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

Version status:

```text
DRAFT
VALIDATION_FAILED
READY_FOR_REVIEW
APPROVED
SUPERSEDED
REVOKED
ARCHIVED
```

Editing an approved or active version creates a new draft.

Running and completed jobs continue using the version they originally pinned.

## 5. Profile-owned selections

Every profile version owns explicit selections rather than inheriting an uncontrolled provider-wide checkbox cloud.

### 5.1 Offering selections

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

Rules:

1. A profile selects a subset of the provider's approved available offerings.
2. An offering may appear in many profiles.
3. The same offering may use different markets, signals, geography, qualification, and source strategies in different profiles.
4. Removing an offering from one profile does not pause it globally.
5. Pausing an offering globally prevents new profile activations that depend on it and applies the approved running-job policy.

### 5.2 Market selections

```text
ProfileMarketSelection

profile_version_id
customer_market
lead_subject_type
organization_type
included
priority
```

### 5.3 Taxonomy selections

```text
ProfileSectorSelection
ProfileDomainSelection
ProfileDomainActivitySelection
```

Every domain receives its own activity group.

Selecting `Manufacturing` for Pharmaceuticals does not activate it for Medical Devices, Food Products, Textiles, or any other domain.

### 5.4 Signal and keyword selections

```text
ProfileOpportunitySignalSelection
ProfileDomainKeywordSelection
ProfileActivityKeywordSelection
ProfileServiceKeywordSelection
ProfileLocaleKeywordPackSelection
ProfileNegativeContextSelection
```

The effective keyword definition is:

```text
selected domain keywords
+ selected domain-activity keywords
+ selected offering-specific signal keywords
+ selected locale packs
+ explicit workspace overrides
+ exclusions and negative context
```

A keyword match creates an evidence candidate. It does not prove activity, demand, a service gap, or an opportunity.

### 5.5 Source selections

```text
ProfileSourceSelection

profile_version_id
source_code
source_mode
connection_reference_id
credential_reference_id
query_profile_version
priority
request_budget
cost_budget
coverage_goal
rate_limit_policy
retention_policy_version
compliance_policy_version
enabled
```

A source connection may be reused across profiles. Connection reuse never activates a source for every profile.

### 5.6 Output and destination selections

A profile may define approved local outputs and optional destinations, but no destination is authorized merely because it is connected.

Publishing remains governed by Modules 49–56 and separate publication rules.

## 6. Operational activation

Configuration status and operational state must remain separate.

### 6.1 ProfileActivation

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

Generation modes:

```text
ONE_TIME
SCHEDULED
CONTINUOUS_MONITORING
IMPORT_AND_QUALIFY
VERIFY_EXISTING_LIST
REFERRAL_INTAKE
DIRECT_INQUIRY_INTAKE
```

### 6.2 Activation rules

A profile may activate only when:

- its version status is `APPROVED`;
- its provider is operationally active;
- every selected offering version remains approved and available;
- at least one offering is selected;
- required market, lead-subject, domain, activity, geography, signal, source, evidence, qualification, exclusion, compliance, contact, budget, and output rules are valid;
- required credentials are valid and sufficiently scoped;
- product entitlements and tenant limits permit activation;
- no blocking conflict or policy violation exists.

An inactive profile:

- creates no source plan;
- consumes no request or cost budget;
- generates no lead;
- changes no score;
- publishes nothing;
- triggers no outreach preparation;
- remains editable through a new draft version.

### 6.3 Several profiles may exist without running

A company may maintain:

```text
ACTIVE
NEWAX healthcare infrastructure — Pakistan

PAUSED
NEWAX education automation — Pakistan

SCHEDULED
NEWAX logistics telemetry — GCC, weekdays

INACTIVE
NEWAX real-estate customer portals — draft market test

ARCHIVED
Legacy website-only prospecting
```

The existence of these profiles does not cause cross-activation.

## 7. First operational page

The first operational page must be a **Portfolio and Lead Definition Workspace**, not a bare job form.

### 7.1 Header controls

The page begins with:

```text
Provider selector
Business-unit selector
Lead-generation profile selector
Profile-version indicator
Validation status
Approval status
Operational activation state
Owner
Last run
Next scheduled run
```

The user can:

- create a provider when permitted;
- select an existing provider;
- create or select a business unit;
- create a new profile;
- clone an existing profile;
- create a new version;
- compare versions;
- save a draft;
- validate;
- submit for review;
- approve when authorized;
- activate;
- pause;
- schedule;
- run once;
- archive.

### 7.2 Required sequence

```text
1. Provider and business unit
2. Lead-generation profile
3. Selected provider offerings
4. Customer markets and lead-subject types
5. Broad sectors
6. Product or service domains
7. Separate activities for each selected domain
8. Geography and delivery modes
9. Opportunity signals
10. Domain, activity, service, locale, and exclusion keywords
11. Qualification and exclusion rules
12. Sources, credentials, evidence, coverage, and freshness
13. Compliance, privacy, consent, contact, and human-review rules
14. Capacity, quota, budget, output, and destination rules
15. Generation mode, recurrence, stopping rules, and notifications
16. Human-readable review summary
```

The provider offering selection appears before target-market definition because a market is commercially incomplete until Harvester knows what the provider actually offers.

### 7.3 Actions

The page must expose separate actions:

```text
Save Draft
Validate
Submit for Review
Approve
Activate
Schedule
Run Once
Pause
Clone
Create New Version
Archive
```

`Generate Leads` or `Run Once` remains disabled until the profile version is approved and operationally eligible.

### 7.4 Portfolio overview

The first page or its immediate parent view must show:

- all providers and business units the user may manage;
- all lead-generation profiles;
- active, scheduled, paused, inactive, invalid, suspended, and archived states;
- offerings used by each profile;
- geography and target summary;
- last and next run;
- cost and lead quota;
- profile owner;
- warnings, conflicts, and validation failures;
- current yield and quality summary.

The system should make the active configuration obvious. The user should not need to infer it from seventeen tabs and a hopeful memory.

## 8. Example configurations

### 8.1 Pharmaceutical company

Provider organization:

```text
Alpha Pharmaceuticals
```

Offering portfolio:

```text
Contract manufacturing
Pharmaceutical distribution
Cold-chain warehousing
Regulatory documentation support
```

Profiles:

```text
Profile A
Contract manufacturing prospects
Targets: pharmaceutical brands
Domains: Pharmaceuticals
Activities: Manufacturing, Formulating, Packaging
State: ACTIVE

Profile B
Distribution partnerships
Targets: pharmacies, hospitals, healthcare distributors
Domains: Pharmaceuticals, Hospital Supplies
Activities: Distribution, Wholesaling
State: PAUSED

Profile C
Cold-chain storage demand
Targets: pharmaceutical distributors and laboratories
Domains: Pharmaceuticals, Laboratory Supplies
Activities: Warehousing, Cold Storage
State: SCHEDULED
```

One profile does not activate the others.

### 8.2 NEWAX

Provider organization:

```text
NEWAX
The Business Infrastructure Company
```

Offering portfolio:

```text
Enterprise Software
Intelligent Automation
Connected Infrastructure
```

Profiles:

```text
Healthcare operational infrastructure
Offerings: Enterprise Software, Intelligent Automation, Connected Infrastructure
State: ACTIVE

Education workflow automation
Offerings: Enterprise Software, Intelligent Automation
State: PAUSED

Logistics telemetry and fleet visibility
Offerings: Connected Infrastructure, Intelligent Automation
State: SCHEDULED

Legal matter and document operations
Offerings: Enterprise Software, Intelligent Automation
State: INACTIVE
```

The provider portfolio remains stable while each profile defines a different market strategy.

## 9. Overlap, duplicate, and shared-evidence rules

Several profiles may target overlapping organizations.

Harvester must avoid duplicating identity and source work while preserving profile-specific commercial interpretation.

### 9.1 One local entity

An organization, person, property, project, event, or other lead subject receives one Harvester-local resolved identity per tenant scope.

Profiles do not create duplicate master entities.

### 9.2 Shared observations

When policy, freshness, authority, and retention allow it, an existing observation or evidence artifact may support several profile assessments.

The system must preserve:

- the original source and capture context;
- profile-specific applicability;
- profile-specific signal evaluation;
- profile-specific qualification;
- profile-specific opportunity score;
- profile-specific selection and output state.

### 9.3 Profile overlap detection

Before activation, Harvester should calculate overlap indicators based on:

- provider and offering selection;
- sectors, domains, and activities;
- organization types and lead subjects;
- geography;
- sources;
- keyword and signal profiles;
- schedule and freshness windows.

Overlap states:

```text
NO_MATERIAL_OVERLAP
EXPECTED_OVERLAP
HIGH_OVERLAP
CONFLICTING_PROFILE
REVIEW_REQUIRED
```

High overlap does not automatically block activation. It requires a documented overlap policy.

### 9.4 Deduplication scopes

Supported scopes may include:

```text
PER_JOB
PER_PROFILE
PER_PROVIDER
PER_WORKSPACE
PER_TENANT
```

Default commercial lead deduplication should normally be at least `PER_PROVIDER` or `PER_WORKSPACE`, while evidence reuse may operate at tenant scope subject to policy.

### 9.5 Multi-profile qualification

The same organization may:

- qualify for several offerings;
- qualify under one profile and fail another;
- have different urgency, value, evidence coverage, and contact eligibility per profile.

Harvester therefore stores profile-specific assessment records rather than placing one universal qualification or opportunity score on the organization.

## 10. Capacity, budgets, and scheduling

### 10.1 Capacity allocation

An offering may allocate capacity across profiles.

```text
Offering capacity
→ profile allocation
→ job quota
→ selection quota
```

The system must prevent active profiles from collectively exceeding an enforced capacity limit unless an authorized override exists.

### 10.2 Resource fairness

The scheduler must support:

- tenant-level concurrency limits;
- workspace-level concurrency limits;
- provider-level limits;
- profile-level limits;
- source-level rate limits;
- cost budgets;
- priority classes;
- fair scheduling;
- backpressure;
- pause and emergency stop.

One continuous-monitoring profile must not starve every other customer or profile.

### 10.3 Seasonal and event profiles

Profiles may be scheduled for:

- annual tax periods;
- admission cycles;
- Hajj and Umrah seasons;
- tenders;
- contract renewals;
- product launches;
- harvest seasons;
- maintenance windows;
- regulatory deadlines.

An expired seasonal activation becomes `EXPIRED`; it does not silently restart next year without an approved recurrence rule.

## 11. Permissions and separation of duties

Minimum permissions:

```text
providers.view
providers.manage
business_units.manage
offerings.view
offerings.manage
offerings.approve
profiles.view
profiles.create
profiles.edit
profiles.validate
profiles.submit_for_review
profiles.approve
profiles.activate
profiles.pause
profiles.schedule
profiles.run
profiles.clone
profiles.archive
profile_versions.compare
profile_budgets.override
profile_conflicts.resolve
```

Recommended separation:

- an editor may change a draft;
- a reviewer may approve;
- an operator may run or pause;
- a finance or administrator role may approve budget overrides;
- a compliance role may suspend a profile;
- no ordinary user may activate a profile outside their provider or tenant scope.

High-risk self-approval must be configurable and disabled by default for regulated or enterprise deployments.

## 12. Performance and analytics

Every profile must expose operational metrics without confusing activity with value.

### 12.1 Profile metrics

```text
jobs_started
jobs_completed
source_requests
cost_consumed
records_examined
observations_created
unique_entities_resolved
qualified_leads
review_required
disqualified
duplicate_candidates
contact_eligible
selected
exported
published
yield_per_source
cost_per_qualified_lead
coverage_dimensions
freshness_distribution
quality_debt
```

### 12.2 Outcome metrics

Where lawful feedback exists:

```text
accepted_by_sales
rejected_by_sales
contact_attempted
positive_response
negative_response
invalid_contact
suppressed
opportunity_created
won
lost
reason_codes
```

Feedback creates new evidence and evaluation data.

It must not silently rewrite an active profile, keyword pack, scoring model, or source policy.

### 12.3 Profile comparison

Authorized users should be able to compare versions and profiles by:

- yield;
- cost;
- source contribution;
- duplicate rate;
- qualification rate;
- review burden;
- evidence quality;
- contact eligibility;
- opportunity outcomes;
- policy violations;
- operator workload.

Comparison is analytical. It does not auto-activate the apparently best profile.

## 13. Versioning and reproducibility

A production Harvest Job pins:

```text
provider_organization_version
business_unit_version
service_offering_versions
lead_generation_profile_version
profile_activation_id
taxonomy_registry_version
domain_activity_mapping_version
keyword_registry_version
keyword_profile_versions
signal_profile_versions
qualification_policy_version
evidence_policy_version
source_selection_version
source_query_versions
compliance_policy_version
contact_policy_version
scoring_profile_version
output_policy_version
destination_policy_versions
```

The resulting `HarvestJobInputSnapshot` is immutable and hashable.

A completed result remains explainable even after:

- the profile changes;
- an offering is paused;
- a keyword pack is revised;
- a source connector is upgraded;
- geography changes;
- a new model is released;
- the provider reorganizes its business units.

## 14. Scalability requirements

The design must support:

- many tenants;
- many workspaces per entitled tenant;
- many providers per entitled workspace;
- nested or flat business units;
- hundreds of offerings per provider;
- thousands of profile versions;
- several concurrently active profiles;
- scheduled and continuous execution;
- profile-level budgets and quotas;
- independent source plans;
- paginated portfolio administration;
- asynchronous validation and overlap analysis;
- indexed queries by tenant, provider, business unit, status, owner, offering, sector, domain, geography, and schedule;
- immutable snapshots;
- retention and archival;
- horizontal worker scaling;
- no cross-tenant data leakage;
- no global profile scan during ordinary job execution.

Profile activation must compile a bounded effective configuration so workers do not repeatedly reconstruct a large provider portfolio while processing every source record.

## 15. Failure and lifecycle behavior

### 15.1 Provider suspended

New activations and jobs stop.

Running jobs follow the configured safe-stop policy.

Historical evidence and completed snapshots remain accessible under retention and permission rules.

### 15.2 Offering paused

New jobs requiring the offering do not start.

Affected active profiles become `SUSPENDED` or `REVIEW_REQUIRED` according to policy.

Other profiles and offerings continue.

### 15.3 Credential expires

Only profiles using that credential are affected.

The previous valid credential is never replaced by an invalid candidate.

### 15.4 Budget exhausted

The profile pauses or stops according to its run policy.

It must not borrow budget invisibly from another profile.

### 15.5 Profile version revoked

No new job may pin it.

Running-job behavior follows explicit revocation severity and safe-stop policy.

Completed job history remains unchanged.

### 15.6 Source unavailable

Other source plans continue when their acceptance and evidence rules permit.

The profile records degraded coverage rather than converting failure into confirmed absence.

## 16. Roadmap integration

This document strengthens the existing 64 modules.

| Concern | Existing roadmap module |
| --- | --- |
| Provider, profile and environment configuration | Module 07 |
| Audit, approvals, activation and lifecycle history | Module 08 |
| Tenant and workspace isolation | Module 03 |
| Permissions and separation of duties | Modules 05–06 |
| Provider connections and credentials | Modules 09–10 |
| Profile input preview and validation | Module 14 |
| Profile-based Harvest Job definition | Module 17 |
| Concurrent active-profile orchestration | Modules 18–20 |
| Profile-specific qualification | Module 39 |
| Offering- and profile-specific opportunity scoring | Module 40 |
| Immutable completed-job membership and scores | Module 44 |
| Portfolio, profile and current-lead workspaces | Modules 45–47 |
| Capacity-aware daily selection and ownership | Module 48 |
| Reusable views and profile result groups | Module 49 |
| Profile-controlled exports and publication | Modules 50–52 |
| Profile health, yield, cost and alerts | Module 57 |
| Multi-provider and multi-tenant administration | Module 59 |
| Profile, connector and concurrency entitlements | Module 60 |
| Version compatibility and migration | Module 63 |
| Security, scale, exact-head and release verification | Module 64 |

This crosswalk does not create module 65. Arithmetic may remain calm.

## 17. Minimum interface surfaces

Harvester requires:

1. **Provider Portfolio**
   - providers, business units, offerings, availability, capacity, ownership.
2. **Lead-Generation Profiles**
   - all profile states, versions, owners, targets, offerings, schedules, warnings, metrics.
3. **Profile Builder**
   - complete first-page definition and review flow.
4. **Activation and Schedule**
   - run once, schedule, continuous monitoring, limits, stop rules.
5. **Profile Validation**
   - missing requirements, expired credentials, offering conflicts, budget and policy failures.
6. **Overlap and Conflict Review**
   - profile overlap, duplicate scope, shared evidence, capacity conflict.
7. **Profile Performance**
   - yield, cost, quality, review burden, source contribution and outcome feedback.
8. **Profile Version Comparison**
   - field-level and policy-level differences.
9. **Audit History**
   - draft, approval, activation, pause, suspension, clone, version, run and override history.

## 18. Acceptance criteria

The architecture is not satisfied until tests prove:

1. A provider offering is required before market targeting can be approved.
2. A provider can store many offerings without activating all of them.
3. A provider can maintain several lead-generation profiles.
4. An inactive or paused profile creates no source plan, job, score, lead, export, publication, or cost.
5. One profile may select a subset of available offerings.
6. The same offering may be configured differently across several profiles.
7. Editing an active profile creates a new draft version and does not change running or completed jobs.
8. Activation, approval, scheduling, and execution permissions are separately enforced.
9. Profile schedules respect tenant, provider, source, concurrency, capacity, and cost limits.
10. Two overlapping profiles do not create duplicate master entities.
11. Shared evidence preserves one source history while supporting profile-specific assessments.
12. One organization may qualify differently under different profiles without one universal score overwriting those results.
13. Pausing one profile does not pause unrelated profiles.
14. Pausing one offering affects only dependent profiles.
15. Expired credentials affect only profiles that reference them.
16. Completed jobs retain immutable input snapshots and exact versions.
17. Profile overlap is detected and governed before activation.
18. Profile performance is measurable separately.
19. Feedback cannot silently mutate or activate a profile.
20. Tenant and provider boundaries hold across UI, API, workers, files, caches, schedules, exports, events, and analytics.
21. Exact-head formatting, links, documentation validation, tests, builds, and security checks pass before release.
22. Runtime implementation is not falsely claimed by the existence of this document.

## 19. Delivery sequence

```text
Provider and business-unit foundation
→ offering portfolio and offering versions
→ profile record and profile versions
→ profile-owned selections
→ validation and human-readable review
→ approval and activation
→ schedule and concurrency controls
→ immutable job snapshot
→ overlap and deduplication controls
→ profile-specific qualification and scoring
→ portfolio, profile, performance and audit interfaces
→ permissions, tenant isolation, migration and release verification
```

## 20. Delivery boundary

This document defines planned architecture and product behavior.

It does not implement:

- database schema or migrations;
- APIs;
- permissions;
- UI;
- schedulers;
- workers;
- overlap analysis;
- budgets or entitlements;
- profile validation;
- activation;
- immutable snapshots;
- profile-specific qualification;
- profile-specific scoring;
- exports or publication;
- analytics;
- runtime tests;
- production release.

Status remains **Proposed / Not implemented** until the corresponding roadmap modules are built and verified.
