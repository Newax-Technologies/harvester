# Harvester Cross-Product Keyword and Profile Contract

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This document defines how Harvester's controlled provider, lead-generation-profile, taxonomy, keyword, evidence, and opportunity context may be referenced by NEWAX Core and Communicator without copying Harvester's private discovery configuration into either product.

## 1. Ownership

Harvester is the authoritative owner of:

- provider organizations used for lead generation;
- provider business units;
- offering portfolios and offering versions;
- reusable lead-generation profiles;
- profile versions, activation state, schedules, budgets, overlap rules, and run policies;
- 16 broad-sector definitions used for lead discovery;
- 1,586 product-or-service domain keyword profiles;
- 519 canonical activity keyword profiles;
- organization-cue profiles;
- exclusion and negative-context profiles;
- locale-specific keyword packs;
- match modes, weights, source scopes, profile status, and version history;
- keyword-to-evidence evaluation;
- service-specific problem, buying, existing-solution, competitor, and exclusion signals;
- qualification and opportunity assessment based on the profile's selected provider offerings.

NEWAX Core and Communicator do not become secondary owners of these datasets merely because they receive Harvester output.

They cannot approve, activate, pause, schedule, clone, mutate, or reinterpret a Harvester lead-generation profile unless a separate authenticated command contract is explicitly designed and authorized.

## 2. Non-export rule

Harvester must not export complete provider-profile or raw keyword configuration to another product by default.

A cross-product message may contain stable references and bounded evidence summaries, but it must not contain:

- unrestricted keyword lists;
- private weights or ranking rules;
- complete exclusion dictionaries;
- proprietary semantic prompts or embeddings;
- internal source-query strategies;
- provider portfolio configuration beyond approved bounded labels and references;
- complete lead-generation-profile configuration;
- activation credentials, source budgets, secret references, or internal schedules;
- provider-specific opportunity logic;
- hidden competitor or existing-solution profiles;
- credentials, customer data, or unrestricted source payloads.

An explicit administrative export for backup, migration, authorized audit, or customer-owned configuration portability is a separate controlled workflow.

It is not the normal integration contract.

## 3. Exportable references

Harvester may publish the following bounded fields after a material classification, qualification, selection, or opportunity decision:

| Field | Purpose |
| --- | --- |
| `provider_organization_id` | Harvester-local provider whose demand is being assessed |
| `provider_business_unit_id` | Optional provider unit or brand responsible for the profile |
| `provider_offering_codes` | Selected provider services relevant to the assessment |
| `provider_offering_versions` | Exact offering versions used |
| `lead_generation_profile_id` | Stable Harvester profile identity |
| `lead_generation_profile_version` | Exact approved profile version used |
| `profile_activation_id` | Activation or schedule that authorized the job |
| `harvest_job_input_snapshot_id` | Immutable effective-input record |
| `taxonomy_version` | Version of the broad-sector, domain, and activity registry |
| `keyword_registry_version` | Version of the keyword and control-profile dataset |
| `sector_codes` | Selected or supported broad-sector identifiers |
| `domain_codes` | Supported product-or-service domain identifiers |
| `activity_codes` | Supported domain-specific activity identifiers |
| `keyword_profile_ids` | Stable references to profiles used during discovery |
| `signal_profile_ids` | Offering-specific opportunity-signal profiles used |
| `evidence_reference_ids` | Harvester-owned evidence identifiers |
| `evidence_summary` | Bounded, redacted explanation suitable for the recipient |
| `match_mode_summary` | Counts or categories such as exact, phrase, semantic, entity, or regex |
| `confidence_dimensions` | Versioned confidence values with their meanings preserved |
| `qualification_assessment_id` | Profile-specific qualification decision |
| `opportunity_assessment_id` | Profile- and offering-specific opportunity decision |
| `opportunity_codes` | Harvester-owned supported opportunity classifications |
| `assessment_version` | Version of the decision policy used |
| `assessed_at` | Time of the Harvester assessment |
| `expires_at` | Optional time after which the context must be refreshed |

A profile identifier is a reference.

It is not permission for the receiving product to reconstruct, activate, schedule, or reinterpret the private profile.

## 4. Profile-specific interpretation

One resolved organization may qualify differently for several lead-generation profiles.

Cross-product messages must therefore preserve:

```text
resolved_entity_id
+
provider_organization_id
+
lead_generation_profile_id
+
lead_generation_profile_version
+
selected offering versions
+
profile-specific qualification
+
profile-specific opportunity assessment
```

Consumers must not collapse these into one universal organization score or one universal service need.

Several Harvester profiles may reference the same resolved entity and evidence history without creating duplicate canonical identity.

## 5. Core projection

NEWAX Core may store an optional governance projection containing:

- Harvester source identity;
- tenant, workspace, provider, and business-unit scope;
- lead-generation-profile and activation references;
- immutable input-snapshot reference;
- taxonomy and keyword registry versions;
- sector, domain, activity, offering, and opportunity codes;
- bounded evidence and confidence summaries;
- source event identifiers and provenance;
- synchronization, retention, and audit metadata.

Core must not:

- run Harvester's discovery queries;
- activate, pause, schedule, clone, or mutate Harvester profiles;
- independently classify a service gap from Harvester keyword references;
- mutate Harvester keyword profiles;
- treat a keyword match as canonical organization truth;
- replace profile-specific assessments with one enterprise-wide score;
- expose private provider or keyword configuration through a general Core API;
- reverse a Harvester decision merely because Core has a different record.

## 6. Communicator context

Communicator may receive only the context required to communicate responsibly, including:

- resolved target and contact references;
- provider, business-unit, profile, activation, and selected-offering references;
- sector, domain, and activity labels suitable for message context;
- supported opportunity references;
- approved outreach themes;
- bounded evidence explanation;
- confidence and freshness information;
- prohibited claims and exclusions;
- consent, suppression, and channel-eligibility state;
- locale and tone guidance;
- Harvester decision, profile, and registry versions.

Communicator must not:

- use discovery keywords to independently decide that a target needs a service;
- activate or mutate the Harvester profile;
- expand outreach to offerings that the profile did not select;
- reuse expired or revoked profile context as though it were current;
- treat one profile's result as permission for another provider, business unit, offering, profile, or campaign.

Communicator owns messaging, consent, engagement, and conversation context, not Harvester's opportunity judgment.

## 7. Integration modes

The same bounded contract may be used through either supported path:

```text
Harvester
→ Communicator
```

or:

```text
Harvester
→ NEWAX Core optional governance projection
→ Communicator
```

Core must remain optional.

Direct Harvester-to-Communicator operation must not depend on Core runtime availability.

## 8. Version and replay requirements

Every exported assessment must preserve:

- source product;
- source installation;
- tenant and environment;
- source event ID;
- resolved entity and opportunity IDs;
- provider organization and business-unit IDs;
- offering IDs and versions;
- lead-generation-profile ID and version;
- profile activation ID;
- immutable input-snapshot ID;
- taxonomy version;
- keyword registry version;
- evidence policy version;
- qualification policy version;
- assessment policy version;
- contact and compliance policy versions;
- creation and expiry timestamps.

Consumers must process retries idempotently.

They must not silently reinterpret an old assessment using newer local assumptions, a newer profile, another offering, or a different provider.

A newly approved profile version or materially changed opportunity decision receives a new event identity.

A retry of the same decision reuses the original event identity and exact serialized payload.

## 9. Security and privacy

Cross-product profile and keyword context must follow least disclosure.

- Evidence summaries must be redacted and bounded.
- Sensitive personal data must not be included merely because a source page contained it.
- Internal search queries, credentials, provider tokens, unrestricted raw evidence, budgets, and complete profile configuration must remain in Harvester.
- Recipient products must enforce their own tenant, authorization, retention, audit, and deletion rules.
- Logs must not contain complete private profiles, keyword registries, or sensitive evidence payloads.
- A connected product may not issue profile lifecycle commands without a separate authenticated, permissioned, idempotent, audited command contract.
- Revoked, suspended, or expired profile context must not authorize new destination work.

## 10. Acceptance criteria

- [x] Harvester remains the only authoritative provider-profile and keyword-registry owner.
- [x] Provider, business-unit, offering, profile-version, activation, and snapshot references are preserved.
- [x] Core receives references and bounded governance summaries only.
- [x] Communicator receives qualified communication context only.
- [x] Direct Harvester-to-Communicator operation remains supported.
- [x] Core remains optional.
- [x] Raw provider profiles and keyword registries are not duplicated across product databases or repositories.
- [x] Keyword matches remain evidence candidates rather than proof.
- [x] Qualification and opportunity assessments remain profile-specific.
- [x] A recipient cannot activate or mutate a Harvester profile through ordinary context delivery.
- [x] Every exported decision preserves profile, registry, offering, policy, and assessment versions.
- [x] Retry and replay semantics are explicitly idempotent.
- [x] Runtime implementation is not falsely claimed.

## 11. Delivery boundary

This document defines a cross-product architecture contract only.

It does not implement events, APIs, commands, schemas, migrations, credentials, synchronization, message generation, search, classification, evidence scoring, profile activation, or production release.
