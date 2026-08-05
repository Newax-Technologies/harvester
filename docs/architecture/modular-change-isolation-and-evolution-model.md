# Harvester Modular Change-Isolation and Evolution Model

Decision status: **Approved architecture requirement**  
Implementation status: **Not yet implemented or verified**  
Version: **1.0**  
Date: **5 August 2026**

## 1. Purpose

Harvester is intended to remain under continuous development for years. New sectors, domains, activities, keywords, sources, scoring rules, evidence policies, database capabilities, interface improvements, exports and integrations will be added and revised repeatedly.

The architecture must therefore prevent a change in one bounded area from forcing unrelated areas to change, retest, redeploy or migrate without a demonstrated dependency.

The governing principle is:

> Every capability must have a clear owner, stable contract, independent version and controlled dependency direction.

A Healthcare taxonomy upgrade must not alter Education, Finance or any other sector unless a shared canonical contract deliberately changes.

A LinkedIn source upgrade must not modify Google, Yandex, website, registry or other source adapters.

A formatting or presentation upgrade must not alter domain definitions, evidence, scoring or database policy.

A database-policy change must not silently rewrite source behaviour, taxonomy meaning, interface formatting or opportunity rules.

This document defines the boundaries, contracts, versioning rules, dependency rules, migration rules, testing requirements and release controls required to achieve that outcome.

## 2. Architectural decision

Harvester will use a **modular monolith with extractable boundaries** as its initial structural model.

This means:

- The product may remain one repository and one primary deployable application where operationally sensible.
- Internally, capabilities are separated into bounded modules with explicit public contracts.
- Modules do not read or modify another module's private implementation or private tables directly.
- Independently versioned registries, policies and adapters may be released without revising unrelated modules.
- A module may later become a separately deployed service only when scale, isolation, compliance, ownership or reliability evidence justifies the operational cost.

Independent upgradeability does **not** require one repository, database or network service per file. Premature service separation would replace code coupling with distributed transactions, network failures, deployment coordination and invoices, which is a rather elaborate method of feeling architectural.

## 3. Required bounded modules

Harvester must maintain at least the following independently governed boundaries.

### 3.1 Core contracts

Owns only the stable cross-module language required for interoperability, including:

- Canonical identifiers
- Version references
- Source observation envelopes
- Evidence and provenance references
- Domain, activity and keyword references
- Provider-offering references
- Job snapshot references
- Error and outcome codes
- Events explicitly intended for cross-module use

Core contracts must not contain sector-specific business content, source-specific extraction logic, presentation formatting or provider-specific scoring.

### 3.2 Sector packs

Each broad sector is an independently versioned sector pack.

Examples:

```text
sector-healthcare
sector-education
sector-food-agriculture
sector-real-estate
sector-construction
sector-legal
sector-finance
sector-retail
sector-hospitality
sector-travel
sector-manufacturing-industry
sector-logistics
sector-energy
sector-technology
sector-government
sector-nonprofit
```

Each sector pack may own:

- Sector metadata
- Domain families
- Domain definitions
- First-release visibility defaults
- Sector-local aliases
- Sector-to-domain applicability
- Sector-local keyword profiles
- Sector-local activity-profile assignments
- Sector-local exclusions and negative context
- Sector-specific validation fixtures
- Sector-specific test scenarios

A sector pack must not own:

- Another sector's definitions
- Canonical activity identities
- Shared source-adapter implementation
- Database connection policy
- Global formatting rules
- Universal provider-service eligibility
- Unrelated scoring profiles

A Healthcare sector-pack release changes only the Healthcare pack version unless it deliberately depends on a new shared contract version.

### 3.3 Canonical activity library

The shared activity library owns stable activity identities such as manufacturing, distributing, warehousing, selling, installing, treating, teaching and auditing.

It must remain separate from sector packs because the same activity may apply to several domains and sectors.

A change to one domain's activity applicability does not modify the canonical activity itself and does not propagate the user's selection to any other domain.

### 3.4 Keyword packs

Keyword data must be separated into independently versioned layers:

1. Domain identity keywords
2. Canonical activity keywords
3. Locale and language packs
4. Organization cues
5. Exclusions and negative context
6. Service-specific target and opportunity keywords

The domain and activity layers may be shared safely. Service-specific problem, buying-intent, competitor, existing-solution and gap profiles require an active provider offering and must remain outside generic sector discovery data.

A keyword-pack upgrade must not alter domain IDs, activity IDs or historical evidence.

### 3.5 Source adapters

Every acquisition source is an independent adapter module.

Examples:

```text
source-google
source-yandex
source-linkedin
source-meta-instagram
source-x
source-bing
source-apple-maps
source-websites
source-official-registries
source-directories
source-job-boards
source-procurement
source-news
source-marketplaces
source-imports
```

Each adapter owns:

- Authentication and credential requirements
- Query construction
- Rate limits and cost controls
- Provider-native request and response handling
- Provider-native field mapping
- Pagination and stopping rules
- Source-specific retries
- Attribution and retention requirements
- Source-specific compliance restrictions
- Source-specific test fixtures
- Adapter version

Each adapter emits the canonical source envelope and must not write directly into scoring, qualification or another adapter's internal state.

Changing LinkedIn must not require changing Google. Changing Google must not require changing Yandex. Shared behaviour belongs in a deliberately versioned adapter SDK or canonical envelope, not in copy-pasted cross-adapter assumptions.

### 3.6 Evidence and provenance

The evidence module owns immutable observations, claims, provenance, source references, detection state, coverage and quality metadata.

It must not decide provider-service eligibility or presentation formatting.

Source adapters may submit observations through the evidence intake contract. They may not rewrite accepted history after ingestion.

### 3.7 Resolution and entity identity

Resolution owns local entity candidates, matches, merge decisions, conflicts and source-to-entity links.

It consumes evidence contracts but does not own source acquisition or sector taxonomy.

Resolution changes must not alter source-native observations.

### 3.8 Opportunity and scoring policies

Scoring must be policy-driven and independently versioned.

Separate policies may exist for:

- Qualification
- Opportunity value
- Pursuit readiness
- Confidence
- Risk
- Coverage
- Provider-specific scoring profiles

A scoring-policy upgrade must not mutate raw evidence, source adapters, taxonomy definitions or historical results. Historical assessments retain the exact scoring-policy version used when they were created.

### 3.9 Database and persistence policy

Database architecture owns:

- Schema ownership rules
- Table and migration conventions
- Transaction boundaries
- Retention enforcement
- Index and performance policy
- Row-level tenant isolation
- Encryption and secret-reference rules
- Backup and recovery policy
- Read-model and derived-data policy

Database policy must not own sector meaning, source queries, user-interface formatting or scoring logic.

Modules own their data through explicit repositories or ports. Another module must not reach into private tables merely because SQL makes trespassing convenient.

### 3.10 Presentation and formatting

Presentation owns:

- Interface formatting
- Tables, cards and layouts
- Export templates
- Human-readable labels
- Locale presentation
- Date, number and currency formatting
- Accessibility presentation rules
- Theme and visual tokens

Presentation consumes read models and public contracts. It must not determine evidence validity, domain identity, activity applicability, qualification or database retention.

A formatting change must not create a database migration or change source acquisition unless the underlying data contract truly changed.

### 3.11 Integrations and destinations

Each destination adapter is independently versioned.

Examples include:

- NEWAX Core
- Communicator
- CRM exports
- Webhooks
- CSV and spreadsheet exports
- Approved APIs

Destination adapters consume approved publication contracts. They do not own Harvester's private data model and cannot require other destinations to be present.

## 4. Dependency direction

Dependencies must flow toward stable contracts and never form cycles.

```text
Presentation
    ↓
Application use cases
    ↓
Domain modules and policies
    ↓
Ports and public contracts
    ↓
Adapters and persistence implementations
```

For acquisition:

```text
Source adapter
    ↓
Canonical source envelope
    ↓
Evidence intake
    ↓
Resolution
    ↓
Qualification and opportunity policies
    ↓
Approved publication package
    ↓
Destination adapter
```

Prohibited dependency examples:

- Healthcare importing Education internals
- LinkedIn importing Google adapter internals
- Presentation importing database repositories directly
- Scoring importing source-provider SDK response types
- Database migrations importing interface components
- A destination adapter reading private Harvester tables
- A sector pack changing universal provider-service eligibility
- A formatter deciding whether evidence proves absence

## 5. Public contracts and private implementation

Every module must expose only the minimum contract required by other modules.

Public contracts may include:

- Commands
- Queries
- Events
- Read models
- Value objects
- Versioned schemas
- Error codes

Everything else is private by default.

A module may change its internal implementation without affecting consumers when its public contract remains compatible.

Cross-module contracts must be:

- Explicit
- Versioned
- Documented
- Validated at runtime where external input is involved
- Covered by contract tests
- Free from provider-native or framework-specific leakage unless the contract explicitly exists for that provider

## 6. Versioning model

Each independently upgradeable part must have its own version.

Minimum versioned assets include:

- Sector pack
- Domain registry
- Activity registry
- Domain-activity mapping
- Keyword pack
- Locale pack
- Source adapter
- Canonical source envelope
- Evidence policy
- Resolution policy
- Qualification policy
- Scoring policy
- Database schema
- Read model
- Export template
- Destination adapter
- Interface design system

Semantic versioning guidance:

- `PATCH`: compatible corrections that do not change intended meaning or contract shape
- `MINOR`: backward-compatible additions
- `MAJOR`: incompatible contract, meaning or migration change

A release record must identify the exact versions composed into the deployed product.

A Harvest Job snapshot must retain the exact configuration and policy versions used when it ran.

## 7. Upgrade isolation rules

### 7.1 Sector upgrades

A sector upgrade may change only:

- That sector's registry
- That sector's mappings
- That sector's keywords
- That sector's tests
- Shared contracts only when genuinely required

It must not alter another sector's data, version or selection state.

### 7.2 Source upgrades

A source upgrade may change only:

- That source adapter
- Its credentials or permission definitions
- Its native mappings
- Its source-specific tests and documentation
- Shared adapter contracts only through controlled versioning

It must not alter another source's queries, limits, credentials or retention behaviour.

### 7.3 Formatting upgrades

A formatting upgrade may change only:

- Presentation components
- Export templates
- Read-model presentation
- Theme and accessibility formatting

It must not change domain meaning, evidence, scoring or persistence rules.

### 7.4 Database upgrades

A database upgrade may change only:

- Owned schemas
- Migrations
- repositories
- indexes
- constraints
- retention implementation
- read-model generation

It must preserve module contracts or release an explicit contract version and migration plan.

### 7.5 Scoring upgrades

A scoring upgrade may change only:

- A named scoring policy
- Its weights and rules
- Its explanation model
- Its test corpus
- Its version

It must not rewrite source evidence or historical assessments.

## 8. Database evolution rules

Database evolution must use controlled, reversible practices.

Required rules:

- Every table has a clear owning module.
- Cross-module access uses repositories, services, events or approved read models.
- Migrations are versioned and immutable after release.
- Destructive changes use an expand-migrate-contract sequence.
- Backfills are resumable and observable.
- New constraints are validated against existing data before enforcement.
- Old readers and new writers, or new readers and old writers, remain compatible during staged rollout where zero-downtime deployment is required.
- Derived data can be rebuilt from authoritative data and versioned policies.
- Historical job and assessment records retain their original version references.
- Rollback and forward-recovery procedures are defined for material migrations.

## 9. Testing and verification boundaries

Every module must have tests proportional to its responsibility.

### 9.1 Module tests

Verify private business behaviour without loading unrelated modules.

### 9.2 Contract tests

Verify that producers and consumers agree on public schemas, events and errors.

### 9.3 Adapter tests

Verify one source or destination adapter against recorded fixtures or approved sandboxes without activating unrelated adapters.

### 9.4 Sector-pack tests

Verify domain counts, stable IDs, duplicate prevention, activity applicability, keyword controls and exclusions for one sector independently.

### 9.5 Migration tests

Verify forward migration, compatibility, rollback or recovery, tenant isolation and existing-data handling.

### 9.6 Integration tests

Verify only the boundaries intentionally affected by the change.

### 9.7 Regression tests

Run broader checks before release, but broad regression coverage does not justify broad source changes.

The latest exact commit must pass applicable checks before a change is called CI Green or Complete. This follows the mandatory NEWAX verification protocol.

## 10. Change-impact declaration

Every pull request must declare:

```text
Primary module changed:
Public contracts changed:
Database schema changed:
Sector packs affected:
Source adapters affected:
Scoring policies affected:
Presentation affected:
Destination adapters affected:
Migration required:
Backward compatibility:
Rollback or recovery plan:
Focused tests:
Full verification:
```

A blank field means none, not “we did not check.”

Changes that modify unrelated modules without a documented dependency must be split or justified.

## 11. Release composition

Harvester releases are composed from independently versioned modules.

Example:

```text
Harvester 2.4.0

core-contracts                 2.1.0
sector-healthcare              1.3.0
sector-education               1.1.2
activity-registry              1.0.1
keyword-pack-healthcare        1.4.0
source-google                  2.2.1
source-linkedin                1.5.0
source-websites                3.0.0
evidence-policy                2.0.1
resolution-policy              1.8.0
newax-scoring-profile          3.1.0
database-schema                12.0.0
presentation-system            4.2.0
core-destination-adapter       1.6.0
```

The product release version records the tested composition. It does not erase the independent module versions.

## 12. Compatibility and deprecation

Breaking changes require:

- A new major contract version
- A migration or translation path
- A documented deprecation period where practical
- Consumer identification
- Contract tests for old and new versions during transition
- Removal criteria
- Rollback or forward-recovery guidance

Deprecated contracts must not remain indefinitely without an owner and removal plan. “Temporary” is otherwise one of software's longest-supported versions.

## 13. Feature flags and activation

New modules, source capabilities, sector versions, scoring versions and database-backed behaviours may be deployed before activation when controlled rollout is needed.

Feature flags must:

- Have an owner
- Have a purpose
- Have a default state
- Be tenant- or environment-scoped where required
- Be audited
- Have an expiry or removal condition
- Never bypass authorization, evidence or consent requirements

## 14. Observability and fault isolation

Every independently upgradeable module must expose enough operational evidence to diagnose its behaviour without enabling private cross-module access.

Minimum signals may include:

- Module and version
- Request or job correlation ID
- Success and failure counts
- Latency
- Retry state
- Cost or quota usage where relevant
- Validation failures
- Policy version
- Migration state
- Publication or delivery outcome

A failure in one optional source or destination must not make unrelated sources, analysis or destinations unavailable unless the job explicitly requires it.

## 15. Repository organization guidance

The repository should reflect ownership boundaries clearly. A possible structure is:

```text
src/
  core-contracts/
  application/
  sectors/
    healthcare/
    education/
    ...
  activities/
  keywords/
  sources/
    google/
    linkedin/
    yandex/
    websites/
    ...
  evidence/
  resolution/
  qualification/
  scoring/
  persistence/
  presentation/
  destinations/
  operations/
```

The exact framework-specific folder names may differ, but ownership and dependency rules must remain visible and enforceable.

## 16. Acceptance criteria

This architecture requirement is satisfied only when:

1. Every principal module has a documented owner and public contract.
2. Sector data is packaged and versioned independently.
3. Source adapters are isolated from one another.
4. Presentation does not import private domain or persistence implementations.
5. Database tables and migrations have explicit module ownership.
6. Scoring policies are versioned and historical assessments retain policy references.
7. Contract tests prevent accidental breaking changes.
8. A Healthcare-only change can be built and tested without modifying other sector packs.
9. A LinkedIn-only change can be built and tested without modifying Google or other adapters.
10. A formatting-only change can be released without database, taxonomy or scoring changes.
11. A database-policy change identifies affected contracts and migrations without silently changing source or business meaning.
12. Release manifests identify the exact versions composed into a deployment.
13. Pull requests declare their impact boundaries.
14. CI verifies the latest exact commit.
15. No known unresolved isolation defect remains.

## 17. Delivery boundary

This document approves the required architectural direction.

It does not prove that the current runtime already satisfies these boundaries. Implementation requires repository inspection, dependency mapping, module extraction where needed, contract definition, schema ownership, tests, CI enforcement and migration planning.

Status must therefore remain:

- **Approved architecture requirement** for the decision
- **Not yet implemented or verified** for the current runtime
