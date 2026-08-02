# NEWAX Lead Harvester Roadmap

## Document purpose

This roadmap is the delivery plan for evolving the existing NEWAX Lead Harvester into a controlled, source-aware lead-discovery and qualification system with a complete enterprise operating interface.

The roadmap has five responsibilities:

1. Preserve capabilities that already exist and avoid rebuilding them under new names.
2. Correct security, data-integrity, evidence, and operational weaknesses before adding orchestration.
3. Define the next-generation Harvest Job workflow, source-specific processing model, adaptive source UI, sector-specific qualification policies, result workspaces, exports, and Communicator handoff.
4. Lock the frontend visual system, navigation, product pages, secure Secrets & Integrations experience, and frontend implementation sequence.
5. Divide the work into small but meaningful delivery modules that can be implemented, reviewed, tested, and merged safely.

The roadmap describes required work. A detailed item is not proof that it has already been implemented.

### Status vocabulary

- **Current:** available in the repository today.
- **Correction pending:** implemented in an open correction branch or PR but not yet integrated into `master`.
- **Planned:** required future work.
- **Restricted:** must remain disabled until the access, security, compliance, and operating model is approved.
- **Deferred:** intentionally outside the active delivery sequence.

---

# 1. Product boundary

Harvester is part of a larger NEWAX business-infrastructure workflow.

```text
Harvester
Finds, verifies, resolves, enriches, qualifies, scores, and prepares opportunities.

Communicator / Engagement Engine
Creates controlled campaigns, sends approved messages, follows up, receives replies, and records outcomes.

NEWAX Core / CRM
Owns the canonical commercial relationship, customers, opportunities, contracts, and operating history.
```

Harvester may prepare a communication-ready audience, but it must not silently become an uncontrolled bulk-messaging system.

The product principle is:

> Define the market. Let the infrastructure discover, verify, resolve, qualify, and prepare the opportunities while the operator remains in control.

---

# 2. Current implementation baseline

The current repository already contains valuable foundations. The next architecture must evolve these rather than create a second parallel system.

## Current capabilities

- Source runs and append-only raw source records
- Google Places, Yandex Maps, Apple Maps, website, Telegram, manual, and authorized-import source paths
- Website page snapshots
- Field normalization
- Entity-resolution candidates and assessments
- Canonical institutions, branches, contacts, people candidates, and provenance
- Human resolution review
- Sector registry and basic sector visibility
- Basic sector-aware qualification fields
- Lead profiles and score history
- Service-gap and website-quality scoring
- Verification and data-quality flags
- Suppression and deletion requests
- Daily selection and reservations
- CSV and JSON exports
- Durable Harvester-side event outbox
- NEWAX Core lead-sync integration
- Account briefs, outreach drafts, approval states, and outreach outcomes
- Operations, health, metrics, and audit APIs
- A React frontend covering a limited subset of backend capabilities

## Current architectural limitations

- The main pipeline is primarily CLI and YAML driven.
- A single normal pipeline invocation selects one source branch.
- There is no parent `HarvestJob` coordinating multiple selected sources.
- There is no job API backing the planned Generate Leads page.
- Source processing is not represented as independently versioned stage workflows.
- Website crawling does not provide a complete parent-job live-progress model.
- Entity resolution can create duplicates under concurrent source execution.
- Authentication and authorization require hardening before production use.
- Sector qualification is too limited for the planned product.
- Qualification is not yet policy-versioned by sector, lead type, organization type, and objective.
- Generated Leads and Master Leads are not yet separate first-class workspaces.
- Lead Dossier data is spread across multiple APIs and models.
- Daily selection is not connected to a full Communicator campaign model.
- Selected-ID exports and frozen campaign audiences do not exist.
- Professional-network research is not safely integrated into organization and person resolution.
- Frontend runtime configuration and authentication remain development-oriented.
- There is no production-safe UI for credential metadata, replacement, provider validation, or rotation.

## Open correction sequence

The roadmap assumes the following corrections are integrated first:

1. Institution/domain-scoped website page snapshots.
2. Evidence-aware detection statuses:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_CRAWLED
CRAWL_FAILED
UNKNOWN
```

3. Complete deletion graph, deletion manifest, and residual-data verification.
4. Recalculation of affected historical lead profiles after evidence corrections.

No-detection, no-crawl, and crawl-failure states must not be treated as confirmed absence.

---

# 3. Delivery model

This roadmap contains **64 top-level delivery modules**.

The frontend milestone is further decomposed into **15 frontend submodules, F1–F15**. These submodules do not change the top-level count; they make Module 64 executable instead of leaving “build the frontend” as one enormous and faintly threatening sentence.

A module is a bounded implementation outcome, usually delivered through one pull request. A module may contain related models, services, routes, migrations, frontend work, and tests when splitting them would create unusable half-features.

## Module sizing rules

Each module should normally:

- Deliver one coherent capability.
- Have clear acceptance criteria.
- Introduce no more than one main migration.
- Avoid unrelated refactoring.
- Include focused tests and affected regression tests.
- Update OpenAPI and generated frontend types when routes change.
- Be independently reviewable.
- Remain below roughly 1,500 meaningful changed source lines, excluding generated files, migration boilerplate, and test fixtures.
- Be split when security risk, migration risk, or review surface becomes excessive.

No more than two dependent PRs should remain stacked at the same time.

No more than six to ten modules should be active simultaneously.

## Required delivery process

```text
Inspect live state
→ Confirm exact base SHA
→ Define acceptance criteria
→ Implement the smallest complete change
→ Run focused tests
→ Run full affected tests
→ Validate migrations
→ Run security and static checks
→ Build frontend when affected
→ Review the final diff
→ Verify the runtime workflow
→ Verify exact-commit CI
→ Merge only with no unresolved issues
```

---

# 4. Governing architecture

## 4.1 One orchestration standard, different source workflows

Every source works differently. Google Places, Yandex Maps, Apple Maps, websites, imports, Telegram, and professional-network data have different access methods, evidence, pagination, rate limits, failure modes, entity types, and upgrade cycles.

The architecture must use:

> **One stable Harvest Job orchestration standard with an independently upgradable workflow for each source.**

The parent orchestration layer owns the user request, market, objective, source mix, target, quality rules, overall state, aggregate progress, audit history, and frozen result set.

Each connector owns credential and capability validation, planning, queries or crawl traversal, pagination, rate limits, retries, evidence extraction, checkpoints, metrics, and connector compatibility.

All connectors eventually emit common normalized evidence into shared resolution, enrichment, qualification, and scoring services.

## 4.2 Backend-driven source UI

The frontend must not hardcode an invented universal process for every source.

Each source run returns its workflow definition and live stage states from the backend.

Example Google stages:

```text
Credential validation
Geographic planning
Query planning
Place search
Pagination
Place details
Normalization
Evidence persistence
Entity resolution
Finalization
```

Example website stages:

```text
Seed discovery
URL validation
Crawl planning
Robots checks
Page fetching
Contact extraction
Organization aggregation
Technology and signal detection
Evidence persistence
Entity resolution
Finalization
```

The UI uses a generic stage renderer while displaying separate source cards, metrics, warnings, and detail panels for each connector.

## 4.3 Common statuses

```text
PENDING
VALIDATING
PLANNING
RUNNING
PAUSING
PAUSED
RETRYING
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
SKIPPED
CANCELLING
CANCELLED
```

Source-specific conditions are represented through machine-readable error codes, warning codes, and metrics.

## 4.4 Execution versioning

Every source run records:

- Connector version
- Workflow version
- Normalization version
- Source API version
- Taxonomy version
- Qualification-policy version
- Configuration snapshot
- Capability snapshot

A running job remains pinned to its starting versions.

## 4.5 Target product workflow

```text
Generate Leads
→ Validate request
→ Create Harvest Job
→ Pin connector and policy versions
→ Create source-specific child runs
→ Execute source workflows
→ Persist raw evidence incrementally
→ Normalize evidence
→ Resolve organizations, branches, people, and contacts
→ Enrich and verify
→ Apply sector and objective qualification
→ Score opportunities
→ Accept, reject, or request review
→ Freeze Harvest Job results
→ Generated Leads
→ Master Leads
→ Lead Dossier
→ Export or create Communicator campaign
→ Send qualified commercial opportunities to NEWAX Core
```

---

# 5. Sourcing strategy

## 5.1 Source-selection principles

A source is selected because it contributes useful evidence for the requested market, not merely because a connector exists.

Every connector declares capabilities such as organization discovery, person discovery, phone, email, website, geographic coverage, branch discovery, incremental results, pause/resume, and cost estimation.

The Generate Leads page explains what each selected source can and cannot contribute.

## 5.2 Google Places sourcing plan

Purpose:

- Organization discovery
- Physical-location discovery
- Public phone and website discovery
- Provider ID and operating-status evidence

```text
Validate Google access
→ Resolve quota and cost limits
→ Translate sector and organization types into categories and queries
→ Build geographic coverage
→ Execute text and nearby searches
→ Follow pagination tokens
→ Fetch required place details
→ Normalize identity, phone, domain, address, and coordinates
→ Persist raw Google evidence
→ Resolve institutions and branches
→ Report coverage, quota, cost, and failures
```

Required metrics include areas, queries, requests, pages, places, unique IDs, provider duplicates, normalized records, resolution outcomes, quota, estimated cost, rate-limit retries, and failures.

## 5.3 Yandex Maps sourcing plan

Purpose:

- Additional organization and location coverage
- Cross-source corroboration
- Region-specific map evidence

```text
Validate Yandex access
→ Translate sector taxonomy
→ Build geographic search areas
→ Execute organization searches
→ Parse GeoJSON features
→ Process identity, contact, address, coordinate, and provider evidence
→ Handle pagination and rate limits
→ Normalize and persist evidence
→ Resolve institutions and branches
→ Report coverage and failures
```

Yandex maintains its own taxonomy and parser while emitting the common evidence contract.

## 5.4 Apple Maps sourcing plan

Purpose:

- Alternative map coverage
- Cross-source identity and location corroboration

```text
Validate MapKit signing configuration
→ Create or refresh token
→ Translate requested categories
→ Build geographic search plan
→ Execute searches
→ Derive stable versioned source identifiers when required
→ Normalize and persist evidence
→ Resolve institutions and branches
→ Report token, quota, coverage, and failures
```

## 5.5 Website sourcing plan

Purpose:

- Organization enrichment
- Contact extraction
- Decision-maker evidence
- Technology and operational-signal detection
- Website-quality and service-gap evidence

```text
Receive or discover seed domains
→ Normalize and validate URLs
→ Apply SSRF and network protections
→ Apply source policy and robots rules
→ Prioritize relevant pages
→ Crawl incrementally
→ Persist every fetch attempt
→ Extract organization identity
→ Extract all usable phones and emails
→ Extract social profiles and contact forms
→ Extract people and roles with evidence
→ Detect technologies and operational signals
→ Aggregate evidence by domain and organization
→ Resolve organizations, branches, people, and contacts
→ Compute evidence-aware detection states
→ Report coverage and failures
```

Required evidence rules:

- `NOT_DETECTED` is not `ABSENT_CONFIRMED`.
- `NOT_CRAWLED` and `CRAWL_FAILED` contribute no confirmed absence evidence.
- Website snapshots used for scoring are institution/domain scoped.
- Contact-to-person attribution requires evidence.

## 5.6 Authorized-import sourcing plan

```text
Validate source authority
→ Inspect encoding and schema
→ Map columns
→ Validate identity fields
→ Normalize organization and contact data
→ Reject invalid rows with explicit reasons
→ Detect unchanged reimports
→ Detect new evidence in known rows
→ Persist append-only raw evidence
→ Resolve organizations and people
→ Produce import and rejection reports
```

## 5.7 Telegram sourcing plan

```text
Validate channels and source policy
→ Fetch permitted public metadata and content
→ Extract organization identity and public contacts
→ Normalize and persist evidence
→ Resolve organizations
→ Record coverage and failures
```

Telegram evidence does not automatically become high-confidence identity evidence without corroboration.

## 5.8 Manual sourcing plan

```text
Validate authorized input
→ Create manual source run
→ Preserve original input
→ Normalize identity and contacts
→ Submit through duplicate resolution
→ Create or enrich canonical institution
→ Add branch, person, contact, and provenance evidence
→ Classify sector
→ Refresh LeadProfile
→ Attempt durable Core synchronization when enabled
```

Manual entry must not bypass duplicate resolution.

## 5.9 Professional-network sourcing plan

Status: **Restricted**.

```text
Validate approved access method
→ Receive or discover permitted profile references
→ Collect permitted evidence
→ Identify person and role
→ Identify organization reference
→ Resolve organization
→ Resolve or create PersonCandidate
→ Attach contacts only when attribution is supported
→ Run structured research with prompt-injection controls
→ Separate facts from inferences
→ Persist findings, signals, and account brief
→ Refresh readiness
```

A person must not be created as the organization.

---

# 6. Qualification architecture and sector rules

## 6.1 Qualification and opportunity scoring are separate

Qualification asks whether an organization enters the usable pool for a specific objective. Opportunity scoring ranks value, relevance, and timing.

A qualified organization may have a modest opportunity score. A large service gap does not override suppression, closure, ethical exclusions, unreachable status, or inadequate evidence.

## 6.2 Policy identity

```text
Sector
+
Lead type
+
Organization type
+
Assessment or campaign objective
+
Policy version
```

## 6.3 Universal eligibility safeguards

- Canonical identity exists.
- Identity conflicts are below threshold.
- Operating status is acceptable.
- Required contactability exists.
- Intended channel is not suppressed.
- Confidence reaches threshold.
- Required evidence is recent enough.
- NEWAX ethical restrictions pass.
- No incompatible campaign conflict exists.
- Existing customers are excluded when requested.
- Missing evidence is not converted into a fact.

## 6.4 Rule types

- Required rules
- Weighted rules
- Disqualifying rules
- Review triggers
- Evidence requirements
- Staleness rules
- Allowed and excluded organization types
- Source requirements
- Minimum score
- Objective overrides

Arbitrary executable Python or SQL must not be stored as policy rules.

## 6.5 Outcomes

```text
Qualified
Disqualified
Needs Review
```

Every assessment stores institution, job, policy, version, state, score, threshold, criterion results, evidence snapshot, rationale, and timestamp.

## 6.6 Education policy plan

Organization types include schools, colleges, universities, academies, and training organizations.

Dimensions may include active operation, reachable administration, admissions and student operations, scale, parent/student/faculty workflows, manual admissions, fee, attendance, communication, portal/LMS evidence, and multi-campus reporting.

## 6.7 Healthcare policy plan

Organization types include clinics, hospitals, diagnostic laboratories, dental clinics, rehabilitation centres, and healthcare networks.

Dimensions may include active facility identity, reachable administration, appointment and patient-coordination operations, inventory, reporting, departments, locations, secure workflow requirements, and handoff complexity.

Sensitive patient information is not collected or used as sales evidence.

## 6.8 Real-estate policy plan

Organization types include developers, agencies, property managers, facility operators, and groups.

Dimensions may include active portfolio, properties, agents, branches, developments, lead distribution, inventory visibility, property operations, and connected-building opportunity.

## 6.9 Legal policy plan

Dimensions may include firm structure, lawyers, departments, offices, matter intake, documents, communication, deadlines, secure operations, and administrative or partner contacts.

## 6.10 Hospitality policy plan

Organization types include approved hotels, restaurant groups, venues, and hospitality operators.

Dimensions may include reservations, guest service, inventory, staff, departments, branches, facilities, and connected infrastructure. Ethical industry restrictions apply first.

## 6.11 Retail policy plan

Organization types include stores, chains, distributors, supermarkets, boutiques, showrooms, and omnichannel sellers.

Dimensions may include locations, channels, inventory, procurement, orders, customer operations, reporting, and reachable management.

## 6.12 Islamic-finance policy plan

Organization types include Sharia-compliant institutions, Islamic fintech, approved takaful-related organizations, and Islamic financial services.

Conventional interest-based operations are excluded according to NEWAX policy.

## 6.13 Professional-services policy plan

Dimensions may include structured teams, repeatable delivery, service lines, onboarding, tasks, documents, reporting, CRM, and workflow complexity.

## 6.14 Policy upgrades

1. New jobs use the latest approved policy.
2. Running jobs remain pinned.
3. Historical assessments retain original policy and evidence.
4. Requalification is explicit.
5. Policy edits create new versions.
6. Activation and retirement require authorization and audit.

---

# 7. Locked frontend design and product plan

## 7.1 Visual direction

The frontend must feel calm, precise, operational, premium, reliable, and enterprise-ready.

The hierarchy is created through typography, spacing, borders, neutral surfaces, fill weight, icons, and restrained elevation. Do not use gradients, glass effects, neon accents, decorative charts, or a separate bright colour for every status.

## 7.2 Design tokens

```css
:root {
  --background: #F7F7F4;
  --surface: #FFFFFF;
  --surface-muted: #F0F0EC;
  --surface-hover: #EAEAE5;

  --soft-black: #1A1A18;
  --strong-black: #10100F;
  --text-secondary: #666660;
  --text-muted: #8A8A84;

  --border: #DADAD4;
  --border-strong: #AFAFAA;
}
```

The primary background is soft white. Operational surfaces are white. Soft black is reserved for primary actions, active navigation, headings, selected states, and critical values.

Semantic colour may be used sparingly where accessibility requires it. No state relies on colour alone.

## 7.3 Button hierarchy

### Primary button

Soft-black background, soft-white text, 1px soft-black border, and 8px radius. Hover uses strong black. Use one principal primary action per section.

### Secondary button

White background, soft-black text, neutral/soft-black border, and 8px radius. Hover uses the muted surface.

### Tertiary button

Transparent, borderless, and reserved for low-priority actions.

### Destructive button

Monochrome with explicit wording, icon, confirmation, and stronger authorization where required.

Heights:

```text
Small    32px
Default  40px
Large    46px
```

## 7.4 Shape, spacing, and typography

```text
Button radius       8px
Input radius        8px
Card radius        10px
Dialog radius      12px
Status-chip radius 999px
```

Spacing scale:

```text
4  8  12  16  20  24  32  40  48px
```

Typography stack:

```css
font-family: "Inter", "Geist", "Segoe UI", sans-serif;
```

Recommended hierarchy:

```text
Page title     28/34, weight 650
Section title  20/28, weight 600
Card title     16/24, weight 600
Body           14/22, weight 400
Table text     13/20, weight 400
Label          12/18, weight 550
Metric value   28–36, weight 650
```

## 7.5 Surfaces, tables, forms, and progress

Cards use white surfaces, subtle borders, 10px radius, and minimal shadow.

Inputs are 40px high with a white background and neutral border. Focus uses a soft-black border and low-opacity focus ring.

Tables use muted headers, white rows, subtle horizontal separators, muted hover, and a soft-black inset edge for selection.

Progress bars are 6px high with muted track and soft-black fill. Concrete counts are preferred over percentages. Unknown totals use indeterminate activity plus actual backend metrics.

## 7.6 Application shell

Expanded sidebar: 248px. Collapsed: 72px.

Navigation:

### Discover

- Generate Leads
- Harvest Runs
- Generated Leads

### Manage

- Master Leads
- Lead Dossiers
- Daily Selection

### Review

- Resolution Reviews
- Qualification Reviews
- Data Quality

### Activate

- Exports
- Communicator
- Outreach Drafts

### Governance

- Compliance
- Qualification Policies
- Source Policies

### Operations

- Source Health
- Jobs
- Event Outbox
- Audit Log
- Secrets & Integrations
- Settings

The top bar contains breadcrumbs, global search, environment indicator, notifications, and user menu.

## 7.7 Standard page structure

```text
Breadcrumb
Page title and explanation
Primary page action
Optional summary metrics
Filters or controls
Main content
Contextual drawer or detail panel
```

## 7.8 Product pages

### Generate Leads

Objective, sector, organization type, geography, target, quality requirements, source capability selection, exclusions, version preview, validation, draft, and start action.

### Harvest Runs and Harvest Run

Job list, parent summary, source cards, backend-defined stages, live events, concrete metrics, pause, resume, retry, cancel, warnings, and recovery.

### Generated Leads

Frozen result tabs for Accepted, Needs Review, Rejected, and All Candidates with advanced filtering, canonical-ID selection, export, dossier, and Communicator actions.

### Master Leads

Canonical global search, saved views, filters, columns, bulk selection, exports, Communicator handoff, Core handoff, and dossier access.

### Lead Dossier

Organization summary plus Overview, People, Infrastructure, Qualification, Evidence, History, and Compliance tabs.

### Qualification Policies

Version list, immutable policy versions, bounded rule builder, test mode, publishing, activation, retirement, and audit.

### Source settings

Connector state, versions, capabilities, last run, failures, credential metadata, quota, cost, and validation state.

### Operations

Job monitoring, source health, stranded work, event outbox, audit, failure queues, retries, and recovery.

---

# 8. Secrets & Integrations plan

Status: **Planned**.

Route:

```text
/settings/secrets
```

Navigation:

```text
Operations
└── Secrets & Integrations
```

## 8.1 Purpose

Authorized administrators can add, replace, validate, disable, enable, and rotate supported API keys, passwords, proxies, signing credentials, and integration secrets.

The frontend never retrieves or displays existing plaintext secrets.

## 8.2 Credential categories

### Source credentials

- Google Places
- Yandex Maps
- Brave Search
- Apple MapKit team ID, key ID, and private key

### Intelligence

- OpenAI

### Communication

- SMTP host, port, user, password, and sender identity

### Integration security

- NEWAX Core webhook URL and signing secret

### Restricted tooling

Professional-network proxy, CAPTCHA service, and restricted-source credentials remain hidden or disabled until approved.

## 8.3 Metadata table

```text
Integration
Credential
Status
Environment
Last Validated
Last Rotated
Updated By
Actions
```

Only metadata and a short fingerprint are displayed.

## 8.4 Add and replacement workflow

```text
Choose integration and environment
→ Enter candidate secret
→ Reauthenticate where required
→ Submit through secure API
→ Encrypt and store candidate version
→ Validate through a safe provider request
→ Activate only on success
→ Retire previous version
→ Record audit event without secret value
```

A failed candidate leaves the current working credential active.

## 8.5 Secret actions

- Validate
- Replace
- Disable
- Enable
- View metadata-only history

Forbidden actions:

- Reveal existing secret
- Copy existing secret
- Download existing secret

## 8.6 Rotation metadata

Store version, fingerprint, creation, activation, retirement, actor, validation result, and rotation reason. Historical plaintext remains unavailable.

## 8.7 Permissions

```text
secrets.read_metadata
secrets.create
secrets.replace
secrets.validate
secrets.disable
secrets.enable
secrets.view_audit
```

Production replacement, production disablement, webhook signing changes, and private-key changes require reauthentication.

## 8.8 Planned APIs

```http
GET    /api/v1/secrets
GET    /api/v1/secrets/{secret_id}
POST   /api/v1/secrets
POST   /api/v1/secrets/{secret_id}/replace
POST   /api/v1/secrets/{secret_id}/validate
POST   /api/v1/secrets/{secret_id}/disable
POST   /api/v1/secrets/{secret_id}/enable
GET    /api/v1/secrets/{secret_id}/history
```

Responses return metadata only.

## 8.9 Storage rules

Local development may use an explicitly enabled ignored `.env.secrets` adapter. Production uses an approved encrypted deployment secret manager, Vault, cloud secret manager, or equivalent.

Secrets never enter frontend persistence, GitHub, job configuration, logs, error details, analytics, telemetry, audit payloads, screenshots, or plaintext database fields.

A separate configuration change proposes `.env.secrets` support. Until integrated, that file is not current `master` behavior.

---

# 9. The 64 top-level delivery modules

## Phase 1: Stabilize the existing repository

### Module 1: Open-PR and branch cleanup

Classify open PRs as merge, rebase, split, replace, or close. Retire obsolete and unsafe work.

### Module 2: Website evidence and detection corrections

Integrate institution/domain-scoped snapshots, evidence-aware detection, scoring corrections, regression tests, and profile recomputation.

### Module 3: Deletion graph and data correction

Integrate deletion cascades, shared-evidence handling, manifests, residual verification, migrations, and post-correction operations.

### Module 4: Architecture documentation integration

Merge README and roadmap after the correction stack is stable.

### Module 5: Frontend PR disposition

Classify existing frontend work as reuse, rebase, split, replace, or close against the locked frontend architecture.

### Module 6: Repository baseline verification

Establish the exact baseline SHA with backend tests, migration chain, frontend checks, static analysis, CodeQL, and documented external-security status.

---

## Phase 2: Authentication, permissions, security, and secret foundation

### Module 7: Strict authentication

Reject unknown tokens, define explicit development authentication, enforce expiry, and test invalid-token behavior.

### Module 8: Authorization matrix

Define and apply viewer, operator, reviewer, compliance officer, administrator, service account, and secrets-manager permissions across all routes.

### Module 9: Service authentication, frontend sessions, and secret-store foundation

Deliver service-to-service authentication, frontend session lifecycle, production CORS, logout, expiry, approved secret-provider abstraction, encryption-at-rest contract, metadata-only secret access, write-only submission, provider validation, version activation, rotation metadata, and no-secret logging safeguards.

This module may use two bounded PRs:

```text
9A  Service authentication and frontend sessions
9B  Secret provider, metadata APIs, permissions, audit, and validation contract
```

### Module 10: Crawler and raw-data security

Implement SSRF controls, redirect validation, private-network blocking, protocol restrictions, response limits, HTML retention, and purge policy.

### Module 11: Contact and person evidence integrity

Persist all supported contacts, require evidence for person attribution, store attribution confidence, and prevent false decision-maker links.

### Module 12: Migration-driven test infrastructure

Build test databases through Alembic and verify fresh schema, upgrades, downgrades, and post-migration behavior.

---

## Phase 3: Resolution consistency

### Module 13: Resolution concurrency protection

Implement proven identity locking, preferably PostgreSQL advisory locking around normalized organization keys.

### Module 14: Concurrent duplicate reconciliation

Detect and safely reconcile duplicates that still emerge from overlapping transactions.

### Module 15: Resolution transaction boundaries

Define per-record transactions, savepoints, retry safety, partial failures, and profile-refresh timing.

### Module 16: Resolution observability

Add events and metrics for merge, pending, link-only, reject, lock conflict, retry, and reconciliation.

---

## Phase 4: Shared Harvest Job contracts

### Module 17: Common status and error contracts

Define job, source-run, stage statuses, warnings, and machine-readable failure codes.

### Module 18: Source capability and workflow schemas

Define backend-provided capabilities, stages, metrics, retries, pause/resume support, credential-state metadata, and UI labels.

### Module 19: Normalized evidence contract

Define common envelopes for organizations, branches, people, contacts, locations, and signals while preserving raw payloads.

### Module 20: Execution versioning

Persist connector, workflow, normalization, API, taxonomy, configuration, capability, and qualification-policy versions.

---

## Phase 5: Harvest Job persistence

### Module 21: Harvest Job models

Create `HarvestJob`, configuration snapshot, requested counts, status, timestamps, creator, and idempotency key.

### Module 22: Source-run and stage-run models

Create or evolve the parent-child source-run relationship and add `HarvestStageRun` progress and source snapshots.

### Module 23: Harvest events and result models

Create append-only `HarvestJobEvent` and frozen `HarvestJobResult` records.

### Module 24: Harvest Job migration and indexes

Deliver schema migration, constraints, indexes, downgrade path, and compatibility tests.

---

## Phase 6: Harvest Job APIs

### Module 25: Job creation and validation API

Implement creation with request validation, source compatibility, sector/objective validation, version pinning, and idempotency.

### Module 26: Job listing and detail APIs

Implement list and detail endpoints with pagination, filters, source summaries, stages, counts, warnings, and permissions.

### Module 27: Job state-control APIs

Implement pause, resume, cancel, and retry with legal transitions.

### Module 28: Source-run and result APIs

Expose source-run details, stages, frozen results, rejection reasons, and source contribution.

---

## Phase 7: Runtime and worker orchestration

### Module 29: Parent-job planner

Convert a validated market request into independently versioned child source-run plans.

### Module 30: Worker claiming, leases, and heartbeats

Implement atomic claims, lease expiry, heartbeats, stuck-work detection, and safe reassignment.

### Module 31: Retry and checkpoint engine

Support source retry policy, backoff, cursors, crawl checkpoints, processed IDs, quotas, cost, and resumability.

### Module 32: Job progress aggregation

Calculate real parent progress from child metrics without fabricated elapsed-time percentages.

### Module 33: Live event streaming

Implement authenticated Server-Sent Events with cursors, reconnect, replay, and source/stage filtering.

---

## Phase 8: Connector framework

### Module 34: Source connector protocol and registry

Create the shared connector interface and version-aware registry.

### Module 35: Connector execution context

Provide cancellation, checkpointing, events, credentials, quotas, cost tracking, and evidence sinks.

### Module 36: Incremental evidence persistence

Persist raw and normalized evidence while a source is running.

### Module 37: Connector contract test harness

Require common tests for validation, stage reporting, cancellation, retry, versioning, evidence output, credential failure, and partial failure.

---

## Phase 9: Map source connectors

### Module 38: Google planning workflow

Credential validation, category mapping, geographic coverage, query planning, quota estimation, and stages.

### Module 39: Google collection workflow

Searches, pagination, details, incremental storage, checkpoints, metrics, errors, and retries.

### Module 40: Yandex complete workflow

Taxonomy translation, planning, GeoJSON parsing, pagination, normalization, checkpoints, and metrics.

### Module 41: Apple Maps complete workflow

Token lifecycle, search planning, stable IDs, normalization, checkpoints, and metrics.

### Module 42: Cross-map normalization tests

Verify equivalent organizations produce compatible normalized evidence across map connectors.

---

## Phase 10: Website and secondary sources

### Module 43: Website discovery and crawl planning

Seed normalization, approved search discovery, URL validation, priority pages, domain plans, and stages.

### Module 44: Incremental website crawling

Persist fetch progress, checkpoints, robots decisions, failures, and metrics incrementally.

### Module 45: Website extraction and aggregation

Extract supported contacts, organization identity, people, technology signals, and domain evidence safely.

### Module 46: Authorized-import workflow

Schema inspection, mapping, validation, unchanged-row detection, rejection reporting, and resolution handoff.

### Module 47: Manual and Telegram workflows

Adapt both sources to common connector, job, evidence, and resolution contracts.

### Module 48: Restricted professional-network workflow

Build safe person-aware evidence and resolution while keeping execution disabled until approved.

---

## Phase 11: Resolution and enrichment integration

### Module 49: Normalized-evidence dispatcher

Route organization, branch, person, contact, location, and signal evidence to the correct service.

### Module 50: Organization and branch resolution

Resolve canonical institutions and physical branches within safe identity transactions.

### Module 51: Person and contact resolution

Resolve people, roles, organization associations, contacts, attribution confidence, and unsupported relationships.

### Module 52: Provenance and source contribution

Record which source contributed each field, location, contact, person, signal, and qualification fact.

### Module 53: Job-linked human review

Link ambiguous cases to job, source run, evidence, reviewer decision, and result state.

### Module 54: Transactional lead-profile refresh

Refresh scoring after durable canonical changes and preserve score history.

---

## Phase 12: Qualification policy engine

### Module 55: Qualification policy models and versioning

Create versioned policies scoped by sector, lead type, organization type, and objective.

### Module 56: Qualification rule engine

Implement bounded required, weighted, disqualifying, review, evidence, and staleness rules.

### Module 57: Universal eligibility and policy selection

Apply common safeguards and choose the most specific valid policy through documented fallback.

### Module 58: Qualification assessments and requalification

Persist criterion evidence, score, threshold, rationale, policy version, and explicit reassessment.

### Module 59: Education and healthcare policies

Implement and test the first detailed policies.

### Module 60: Remaining sector policies

Implement real estate, legal, hospitality, retail, Islamic finance, and professional-services policies.

---

## Phase 13: Lead workspace and integrations

### Module 61: Generated Leads and Master Leads APIs

Implement frozen job-result and canonical all-run queries with search, filters, sorting, pagination, selection, and saved views.

### Module 62: Lead Dossier and activity timeline

Aggregate organization, branches, contacts, people, scores, qualification, evidence, source history, compliance, communication, and audit.

### Module 63: Export and Communicator backend

Implement selected-ID and filter-snapshot exports, secure delivery, campaign, frozen audience, recipient eligibility, sequence, approval, scheduling, and stop rules.

Split export and Communicator into separate PRs when required by migration or review size.

### Module 64: Complete frontend and rollout

Deliver the locked frontend through submodules F1–F15 described below. The submodules may use separate PRs while remaining one final product milestone.

---

# 10. Frontend delivery submodules for Module 64

## F1: Design tokens and foundations

Deliver colour variables, typography, spacing, radii, elevation, primary/secondary/tertiary/destructive buttons, inputs, tables, focus styles, progress, status, reduced motion, and contrast tests.

Acceptance:

- Soft-white background and white operational surfaces are consistent.
- Primary buttons use soft black.
- Secondary buttons use white with soft-black/neutral borders.
- No gradients or decorative accent system is introduced.
- Components pass contrast and keyboard-focus checks.

## F2: Application shell

Deliver sidebar, top bar, breadcrumbs, responsive layout, environment indicator, notifications shell, user menu, and permission-aware navigation.

## F3: Shared data components

Deliver tables, filters, pagination, dialogs, drawers, toasts, empty states, loading states, status chips, confirm dialogs, and optimistic-lock conflict handling.

## F4: Authentication and runtime configuration

Deliver API base configuration, session lifecycle, expiry, logout, forbidden state, protected routes, environment safety, and reauthentication support for sensitive actions.

## F5: Generate Leads

Deliver lead type, objective, sector, organization type, geography, target, evidence requirements, source capability cards, quality controls, version preview, validation, draft, and job submission.

## F6: Harvest Runs and live Harvest Run

Deliver job list, parent summary, source cards, generic backend-driven stage rendering, SSE client, reconnect, pause, resume, retry, cancel, warnings, errors, and recovery state.

## F7: Source-specific metric displays

Deliver registered metric panels for Google, Yandex, Apple Maps, website, import, Telegram, manual, and restricted source workflows. Stage-state logic remains generic and backend driven.

## F8: Generated Leads

Deliver frozen result tabs, advanced filters, selection, rejection reasons, export, dossier, and Communicator actions.

## F9: Master Leads

Deliver canonical search, saved views, filtering, column control, selection, export, Communicator, Core handoff, and dossier access.

## F10: Lead Dossier

Deliver Overview, People, Infrastructure, Qualification, Evidence, History, Compliance, and persistent organization summary.

## F11: Qualification and governance

Deliver policy list, immutable versions, bounded rule builder, policy testing, publishing, activation, retirement, review queues, source policies, and permission controls.

## F12: Secrets & Integrations

Deliver:

- Credential metadata table
- Category and environment filters
- Add-secret dialog
- Manage-secret drawer
- Write-only submission
- Temporary show/hide only while entering a new value
- Provider validation status
- Atomic replacement workflow
- Enable and disable controls
- Rotation history
- Reauthentication
- Permission gates
- Metadata-only audit history
- Loading, empty, invalid, expired, disabled, and rotation-required states
- Tests proving plaintext values are never rendered, persisted, logged, or returned

Dependencies:

- Module 8 authorization matrix
- Module 9B secret provider, APIs, audit, validation, and rotation contract
- F2 application shell
- F3 shared components
- F4 authentication and reauthentication

## F13: Export and Communicator

Deliver export setup, audience preview, eligibility exclusions, sequence, schedule, timezone, limits, approval, and campaign creation.

## F14: Operations

Deliver job monitoring, source health, failures, retry/recovery, event outbox, audit logs, configuration summaries, and operational metrics.

## F15: End-to-end and rollout verification

Deliver desktop, tablet, mobile review, accessibility, permissions, loading, empty, failure, and conflict states, live-backend E2E, performance checks, security review, deployment runbook, and post-deployment verification.

---

# 11. Dependency order

```text
Modules 1–16
Repository stability, authentication, secret foundation, security, data integrity, and resolution
        ↓
Modules 17–37
Shared contracts, Harvest Job persistence, APIs, runtime, and connector framework
        ↓
Modules 38–48
Source-specific workflows
        ↓
Modules 49–54
Canonical resolution and enrichment integration
        ↓
Modules 55–60
Qualification engine and sector policies
        ↓
Modules 61–63
Lead APIs, dossier, exports, and Communicator backend
        ↓
Module 64 / F1–F15
Frontend, Secrets & Integrations, operations, E2E, and rollout
```

Frontend foundations may be built earlier on disconnected branches, but they must not imply unavailable APIs are operational.

F12 must not begin integration work until Module 9B provides the approved metadata-only secret contract.

---

# 12. Delivery milestones

## Milestone A: Verified foundation

Modules 1–16

Outcome:

- Correction stack integrated
- Unsafe and obsolete PRs retired
- Authentication and permissions hardened
- Secret-provider contract defined
- Crawler and raw-data security improved
- Contacts and people remain evidence-safe
- Resolution is concurrency-aware
- Exact baseline verified

## Milestone B: Harvest Job platform

Modules 17–37

Outcome:

- Harvest Jobs can be created and inspected
- Child source runs and source-specific stages exist
- Jobs pause, resume, retry, and cancel
- Workers use claims, leases, heartbeats, checkpoints, and retries
- Live events are available
- Connectors share one tested contract

## Milestone C: Source workflows

Modules 38–48

Outcome:

- Google, Yandex, Apple, websites, imports, manual, and Telegram use independent workflows
- Workflows are versioned and upgradeable
- Each source exposes real process and metrics
- Professional-network support remains restricted but structurally safe

## Milestone D: Qualified canonical leads

Modules 49–60

Outcome:

- Organization, branch, person, contact, signal, and provenance resolve correctly
- Human review is job linked
- Qualification is versioned and objective specific
- Each sector uses suitable rules
- Qualification remains separate from opportunity scoring

## Milestone E: Operational lead backend

Modules 61–63

Outcome:

- Generated Leads and Master Leads APIs are complete
- Lead Dossier explains evidence and history
- Selected leads can be exported
- Eligible selected leads create frozen Communicator audiences

## Milestone F: Complete operating interface

Module 64 / F1–F15

Outcome:

```text
Generate Leads
→ Harvest Run
→ Generated Leads
→ Master Leads
→ Lead Dossier
→ Export or Communicator
→ NEWAX Core
```

Also included:

- Locked soft-white and soft-black design system
- Qualification and governance UI
- Administrator-only Secrets & Integrations page
- Metadata-only credential management
- Operations and failure recovery
- Responsive, accessible, tested rollout

---

# 13. Acceptance criteria

The roadmap is not complete until all of the following are proven:

1. An authorized user can create a Harvest Job from UI and API.
2. The request pins connector, workflow, normalization, taxonomy, source API, and qualification-policy versions.
3. Multiple selected sources create separate child runs under one parent.
4. Every source exposes a real workflow to the UI.
5. The UI does not fabricate progress.
6. Raw evidence is incremental and auditable.
7. Concurrent sources do not silently duplicate canonical institutions.
8. Ambiguous matches enter human review.
9. Website detection distinguishes absence, non-detection, no crawl, failure, and unknown.
10. Contact-to-person attribution is evidence-backed.
11. Each sector and objective uses the correct versioned policy.
12. Qualification and opportunity scoring remain separate.
13. Accepted, rejected, and review-required results are frozen with reasons.
14. Generated Leads shows one job snapshot.
15. Master Leads shows canonical records across every harvest.
16. Lead Dossier distinguishes facts, detections, inferences, unknowns, evidence, and history.
17. Selected leads can be exported by canonical ID.
18. A Communicator campaign freezes its audience.
19. Suppressed and ineligible recipients cannot be contacted.
20. Campaign creation does not automatically send before approval.
21. The frontend uses the locked soft-white background and soft-black action hierarchy consistently.
22. Primary and secondary buttons follow the defined visual hierarchy.
23. Status is not communicated through colour alone.
24. The UI is keyboard accessible and meets required contrast.
25. Administrators can add, replace, validate, disable, enable, and rotate supported credentials.
26. Existing plaintext secrets are never returned or displayed.
27. A failed replacement leaves the previous active credential working.
28. Secret changes require permissions, reauthentication where required, and audit without secret values.
29. Secrets do not enter logs, errors, analytics, telemetry, screenshots, job configuration, or browser persistence.
30. Pause, resume, retry, cancel, partial failure, and recovery are tested.
31. Migrations upgrade and downgrade cleanly.
32. Backend tests, frontend checks, accessibility, security checks, E2E, runtime verification, and exact-commit CI pass.
33. Rollback and post-deployment verification procedures are documented and tested.

---

# 14. Immediate active batch

Only the following top-level modules begin immediately:

```text
Module 1  Open-PR and branch cleanup
Module 2  Website evidence and detection corrections
Module 3  Deletion graph and data correction
Module 4  Architecture documentation integration
Module 5  Frontend PR disposition
Module 6  Repository baseline verification
```

After the corrected baseline is verified, Modules 7–12 begin.

Frontend F1–F3 may be prepared against the locked visual contract after Module 5 determines what existing frontend work can be safely reused. F4 waits for authentication direction. F5 onward must track real backend contracts. F12 waits for Module 9B.

The Harvest Job orchestrator must not be built on unreliable identity, evidence, authentication, or secret handling. That would merely produce incorrect answers through a beautifully bordered interface.

---

# 15. Roadmap governance

- This file is the delivery-order source of truth.
- README explains product and architecture; this roadmap controls sequence.
- A top-level module may be split when size or risk requires it.
- Modules combine only when they share a migration, transaction boundary, API contract, or inseparable outcome.
- Frontend F1–F15 are submodules of Module 64 and may use separate PRs.
- Dependency order changes only after live-code inspection and documented reasoning.
- Completed modules are marked with the exact merged PR and commit.
- Historical descriptions are not rewritten to make past work appear different.
- Only the next six to ten modules are active implementation issues.
- No module is complete while tests, migrations, security checks, accessibility, runtime verification, or exact-commit CI remain unresolved.
