# Harvester Modular Change-Isolation and Evolution Model

Decision status: **Approved architecture requirement**  
Implementation status: **Not yet implemented or verified**  
Version: **1.1**  
Date: **6 August 2026**

## 1. Purpose

Harvester will evolve across sectors, sources, taxonomies, evidence, identity, scoring, AI, presentation, destinations, deployment, and database policy. Each concern must have a clear owner, stable contract, independent version, and controlled dependency direction.

> A change in one bounded module must not alter unrelated modules without a demonstrated public-contract dependency.

Examples:

- a Healthcare pack change must not alter Education;
- a LinkedIn connector change must not alter Google, Yandex, websites, or registries;
- a frontend formatting change must not alter taxonomy, evidence, scoring, or retention;
- a database change must not silently change source, sector, or opportunity meaning;
- an AI model change must not change deterministic policy or activate without evaluation.

## 2. Structural decision

Harvester begins as a **modular monolith with extractable boundaries**.

This permits one repository and primary deployable while requiring:

- explicit module ownership;
- public contracts and private implementation;
- controlled dependency direction;
- independently versioned datasets, policies, adapters, models, and templates;
- module, contract, migration, integration, and regression tests;
- later service extraction only when measured scale, isolation, reliability, compliance, or ownership requires it.

Premature services would replace code coupling with distributed failures and invoices, humanity's traditional method for making architecture look expensive.

## 3. Required bounded modules

### 3.1 Core contracts

Owns stable cross-module identifiers, version references, commands, queries, events, errors, source envelopes, evidence references, entity references, job snapshots, and output contracts.

It does not own sector content, source-specific logic, provider-specific scoring, UI formatting, or persistence implementation.

### 3.2 Tenant, identity, and access

Owns tenants, workspaces, users, service identities, teams, memberships, roles, relationships, permissions, entitlements, support access, and isolation controls.

No module may invent a second tenant or permission system.

### 3.3 Provider and market configuration

Owns providers, brands, business units, portfolios, offering versions, lead-generation profiles, market definitions, output specifications, activation, schedules, budgets, and immutable job snapshots.

### 3.4 Sector packs

Each sector pack independently owns its sector-specific organization, facility, person, product, service, project, activity, role, pain, need, signal, data, integration, compliance, input, output, and benchmark definitions.

Shared identity, evidence, source, authorization, AI, and activation controls remain outside sector packs.

### 3.5 Taxonomy and keyword packs

Separately version:

- sectors;
- domains;
- activities;
- domain-activity mappings;
- domain keyword profiles;
- activity keyword profiles;
- organization cues;
- exclusions;
- locale packs;
- signal and role profiles.

Service-specific problem, intent, competitor, replacement, integration, and existing-solution profiles require an active offering and remain separate from generic discovery identity.

### 3.6 Source adapters

Every source adapter owns authentication needs, query construction, pagination, rates, pricing, retries, provider-native mapping, attribution, retention, restrictions, fixtures, and adapter version.

Adapters emit shared source and evidence contracts. They do not write directly to qualification, scoring, or another adapter's state.

### 3.7 Evidence and provenance

Owns immutable observations, artifacts, excerpts, assertions, claims, coverage, contradictions, detection states, freshness, source reliability, transformation history, and evidence access.

It does not decide commercial eligibility or presentation.

### 3.8 Resolution and identity

Owns entity candidates, identifiers, aliases, relationships, match features, conflicts, merge, link, reject, split, reversal, and review decisions.

It consumes evidence without rewriting source history.

### 3.9 Qualification and opportunity policies

Separately own:

- eligibility and qualification;
- capability condition;
- Opportunity Value;
- Pursuit Readiness;
- coverage and confidence;
- risk and recommended action;
- provider-specific profiles.

Policy upgrades create new versions and never rewrite historical assessments.

### 3.10 AI gateway

Owns task definitions, providers, models, prompts, routing, redaction, execution, structured output, grounding, evaluations, cost, drift, rollout, and rollback.

Business modules do not call provider SDKs directly after gateway introduction.

### 3.11 Persistence

Owns schema conventions, module table ownership, repositories, migrations, constraints, indexing, tenant enforcement, retention implementation, backups, restoration, and derived read models.

Direct cross-module table access is prohibited unless an explicit shared read model or contract exists.

### 3.12 Presentation

Owns navigation, components, layouts, tables, forms, accessibility, responsive behavior, labels, locale formatting, themes, and export presentation.

It consumes public APIs and read models and does not decide evidence validity or business policy.

### 3.13 Destination adapters

Each destination independently owns credentials, mappings, capability, delivery, receipts, retries, reconciliation, and feedback commands.

A destination adapter cannot require another destination or read private Harvester tables.

### 3.14 Operations and release

Owns health, metrics, alerts, cost and yield, quality debt, runbooks, release manifests, compatibility, feature flags, deployment, backup, restore, and exact-head verification.

## 4. Dependency direction

```text
Presentation
→ application use cases
→ domain policies and modules
→ public ports and contracts
→ adapters and persistence implementations
```

Acquisition to activation:

```text
Source adapter
→ source-native observation contract
→ evidence intake
→ resolution
→ qualification and opportunity policies
→ decision
→ approved output contract
→ destination adapter
```

Prohibited dependencies include:

- one sector importing another sector's internals;
- one connector importing another connector's internals;
- UI importing private repositories;
- scoring importing provider SDK response types;
- migrations importing UI code;
- destinations querying private business tables;
- formatters determining evidence or qualification;
- models changing deterministic policy.

## 5. Public contracts

A module exposes only the minimum required:

- commands;
- queries;
- events;
- read models;
- value objects;
- versioned schemas;
- error and outcome codes.

Contracts are explicit, documented, versioned, validated, and contract-tested. Framework- or provider-specific types do not leak unless the contract deliberately represents that provider.

## 6. Versioned assets

At minimum, independently version:

- module public contracts;
- sector packs;
- domain and activity registries;
- mappings and keyword packs;
- locale packs;
- source and destination adapters;
- source schemas and mappings;
- evidence, resolution, qualification, scoring, contact, output, and compliance policies;
- AI tasks, models, prompts, routing, and evaluations;
- database schema and read models;
- frontend design system and output templates.

Completed jobs and decisions retain exact version references.

## 7. Compatibility

Use semantic intent:

- `PATCH`: compatible correction without changed intended meaning;
- `MINOR`: backward-compatible addition;
- `MAJOR`: incompatible contract, semantic, or migration change.

Breaking changes require consumer identification, migration or translation, deprecation plan, compatibility tests, removal criteria, and rollback or forward repair.

## 8. Database evolution

Material schema changes follow:

```text
expand
→ backfill or dual-write
→ compare and verify
→ move readers
→ contract old structure
```

Rules:

- every table has an owner;
- migrations are immutable after release;
- backfills are resumable and observable;
- constraints are validated before enforcement;
- historical records retain original versions;
- derived data is rebuildable;
- rollback or forward repair is documented;
- tenant isolation is tested before activation.

## 9. Testing boundaries

### Module tests

Verify private module behavior without unrelated modules.

### Contract tests

Verify producer and consumer agreement.

### Adapter tests

Verify one source or destination against recorded fixtures or approved sandboxes.

### Sector-pack tests

Verify stable IDs, counts, mappings, keywords, policies, restrictions, and benchmarks independently.

### Migration tests

Verify forward migration, backfill, compatibility, tenant isolation, restoration, and repair.

### Architecture tests

Reject prohibited imports, direct table access, provider SDK bypass, unscoped queries, and missing impact declarations.

### Release regression

Run broad checks before release without using them as an excuse for broad code changes.

## 10. Pull-request impact declaration

Every implementation PR declares:

```text
Primary modules changed
Public contracts changed
Database and migration impact
Tenant and workspace impact
Sector packs affected
Source and destination adapters affected
Qualification or scoring policies affected
AI tasks or models affected
Presentation affected
Backward compatibility
Rollback or repair
Focused checks
Full exact-head verification
```

A blank field means none, not “we hoped nobody would ask.”

## 11. Release composition

A product release records the tested versions composing it, including application, schema, contracts, sector packs, adapters, policies, models, prompts, frontend, and destinations.

The product version does not erase independent component versions.

## 12. Feature flags

Flags have an owner, purpose, scope, default, audit, expiry, and removal condition. They cannot bypass authentication, authorization, tenant, evidence, consent, source, or publication controls.

## 13. Observability

Every module exposes sufficient operational evidence:

- module and version;
- tenant and correlation identifiers;
- success, failure, retry, and latency;
- cost and quota where relevant;
- validation and policy failures;
- migration and rollout state;
- output and delivery outcomes.

One optional source or destination failure must not disable unrelated work unless the approved job explicitly requires it.

## 14. Acceptance criteria

This architecture is implemented only when:

1. principal modules have documented owners and public contracts;
2. tenant and permission boundaries are shared and tested;
3. sectors and connectors upgrade independently;
4. presentation does not import private domain or persistence code;
5. table and migration ownership is explicit;
6. historical assessments retain policy and evidence versions;
7. contracts and prohibited dependencies are tested;
8. source, sector, AI, database, and frontend changes can be delivered independently when contracts remain stable;
9. release manifests identify the tested composition;
10. exact-head checks pass without unresolved isolation defects.

## 15. Delivery boundary

This document approves the architecture requirement. It does not prove that the current runtime already satisfies it.

Implementation follows [Agency Intelligence Implementation Sequence](../delivery/agency-intelligence-implementation-sequence.md).
