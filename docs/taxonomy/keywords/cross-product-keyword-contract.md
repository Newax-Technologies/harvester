# Harvester Cross-Product Keyword Contract

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This document defines how Harvester's controlled keyword taxonomy may be referenced by NEWAX Core and Communicator without copying Harvester's private discovery configuration into either product.

## 1. Ownership

Harvester is the authoritative owner of:

- 16 broad-sector definitions used for lead discovery;
- 1,586 product-or-service domain keyword profiles;
- 519 canonical activity keyword profiles;
- organization-cue profiles;
- exclusion and negative-context profiles;
- locale-specific keyword packs;
- match modes, weights, source scopes, profile status, and version history;
- keyword-to-evidence evaluation;
- service-specific problem, buying, existing-solution, competitor, and exclusion signals;
- opportunity assessment based on the provider's active offerings.

NEWAX Core and Communicator do not become secondary owners of these datasets merely because they receive Harvester output.

## 2. Non-export rule

Harvester must not export complete raw keyword registries to another product by default.

A cross-product message may contain stable references and bounded evidence summaries, but it must not contain:

- unrestricted keyword lists;
- private weights or ranking rules;
- complete exclusion dictionaries;
- proprietary semantic prompts or embeddings;
- internal source-query strategies;
- provider-specific opportunity logic;
- hidden competitor or existing-solution profiles;
- credentials, customer data, or unrestricted source payloads.

An explicit administrative export for backup, migration, or authorized audit is a separate controlled workflow. It is not the normal integration contract.

## 3. Exportable references

Harvester may publish the following bounded fields after a material classification or opportunity decision:

| Field | Purpose |
| --- | --- |
| `taxonomy_version` | Version of the broad-sector, domain, and activity registry |
| `keyword_registry_version` | Version of the keyword and control-profile dataset |
| `sector_codes` | Selected or supported broad-sector identifiers |
| `domain_codes` | Supported product-or-service domain identifiers |
| `activity_codes` | Supported domain-specific activity identifiers |
| `provider_offering_codes` | Active provider services relevant to the assessment |
| `keyword_profile_ids` | Stable references to profiles used during discovery |
| `evidence_reference_ids` | Harvester-owned evidence identifiers |
| `evidence_summary` | Bounded, redacted explanation suitable for the recipient |
| `match_mode_summary` | Counts or categories such as exact, phrase, semantic, entity, or regex |
| `confidence_dimensions` | Versioned confidence values with their meanings preserved |
| `opportunity_codes` | Harvester-owned supported opportunity classifications |
| `assessment_version` | Version of the decision policy used |
| `assessed_at` | Time of the Harvester assessment |
| `expires_at` | Optional time after which the context must be refreshed |

A profile identifier is a reference, not permission for the receiving product to recreate or reinterpret the private keyword profile.

## 4. Core projection

NEWAX Core may store an optional governance projection containing:

- Harvester source identity;
- tenant and organization scope;
- taxonomy and keyword registry versions;
- sector, domain, activity, offering, and opportunity codes;
- bounded evidence and confidence summaries;
- source event identifiers and provenance;
- synchronization, retention, and audit metadata.

Core must not:

- run Harvester's discovery queries;
- independently classify a service gap from Harvester keyword references;
- mutate Harvester keyword profiles;
- treat a keyword match as canonical organization truth;
- expose private keyword configuration through a general Core API;
- reverse a Harvester decision merely because Core has a different record.

## 5. Communicator context

Communicator may receive only the context required to communicate responsibly, including:

- resolved target and contact references;
- sector, domain, and activity labels suitable for message context;
- provider offering and supported opportunity references;
- approved outreach themes;
- bounded evidence explanation;
- confidence and freshness information;
- prohibited claims and exclusions;
- consent, suppression, and channel-eligibility state;
- locale and tone guidance;
- Harvester decision and registry versions.

Communicator must not use discovery keywords to independently decide that a target needs a service. It owns messaging, consent, engagement, and conversation context, not Harvester's opportunity judgment.

## 6. Integration modes

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

Core must remain optional. Direct Harvester-to-Communicator operation must not depend on Core runtime availability.

## 7. Version and replay requirements

Every exported assessment must preserve:

- source product;
- source installation;
- tenant and environment;
- source event ID;
- entity and opportunity IDs;
- taxonomy version;
- keyword registry version;
- provider offering version;
- evidence policy version;
- assessment policy version;
- creation and expiry timestamps.

Consumers must process retries idempotently and must not silently reinterpret an old assessment using newer local assumptions.

## 8. Security and privacy

Cross-product keyword context must follow least disclosure.

- Evidence summaries must be redacted and bounded.
- Sensitive personal data must not be included merely because a source page contained it.
- Internal search queries, credentials, provider tokens, and unrestricted raw evidence must remain in Harvester.
- Recipient products must enforce their own tenant, authorization, retention, audit, and deletion rules.
- Logs must not contain complete private keyword profiles or sensitive evidence payloads.

## 9. Acceptance criteria

- [x] Harvester remains the only authoritative keyword-registry owner.
- [x] Core receives references and bounded governance summaries only.
- [x] Communicator receives qualified communication context only.
- [x] Direct Harvester-to-Communicator operation remains supported.
- [x] Core remains optional.
- [x] Raw keyword registries are not duplicated across product databases or repositories.
- [x] Keyword matches remain evidence candidates rather than proof.
- [x] Every exported decision preserves registry and assessment versions.
- [x] Retry and replay semantics are explicitly idempotent.
- [x] Runtime implementation is not falsely claimed.

## 10. Delivery boundary

This document defines a cross-product architecture contract only.

It does not implement events, APIs, schemas, migrations, credentials, synchronization, message generation, search, classification, evidence scoring, or production activation.
