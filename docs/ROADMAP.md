# NEWAX Lead Harvester Roadmap

## Document purpose

This roadmap is the delivery plan for evolving the existing NEWAX Lead Harvester into a controlled, source-aware lead-discovery and qualification system.

The roadmap has four responsibilities:

1. Preserve the capabilities that already exist and avoid rebuilding them under new names.
2. Correct security, data-integrity, evidence, and operational weaknesses before adding orchestration.
3. Define the next-generation Harvest Job workflow, source-specific processing model, adaptive source UI, sector-specific qualification policies, result workspaces, exports, and Communicator handoff.
4. Divide the work into small but meaningful delivery modules that can be implemented, reviewed, tested, and merged safely.

The roadmap describes required work. A detailed item is not proof that it has already been implemented.

### Status vocabulary

- **Current**: available in the repository today.
- **Correction pending**: implemented in an open correction branch or PR but not yet integrated into `master`.
- **Planned**: required future work.
- **Restricted**: must remain disabled until the access, security, compliance, and operating model is approved.
- **Deferred**: intentionally outside the active delivery sequence.

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
4. Recalculation of affected historical lead profiles after the evidence corrections.

No-detection, no-crawl, and crawl-failure states must not be treated as confirmed absence.

---

# 3. Delivery model

This roadmap contains **64 delivery modules**.

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

The architecture must therefore use:

> **One stable Harvest Job orchestration standard with an independently upgradable workflow for each source.**

The parent orchestration layer owns:

- User request
- Sector and objective
- Organization type
- Geography
- Source mix
- Target accepted lead count
- Candidate budget
- Quality mode
- Required data
- Exclusions
- Overall status
- Pause, resume, retry, and cancellation
- Aggregate progress
- Audit history
- Frozen results

Each connector owns:

- Credential and capability validation
- Source-specific planning
- Source queries or crawl plan
- Pagination or traversal
- Rate limits and quotas
- Source-specific retries
- Source-specific evidence extraction
- Source-specific checkpoints
- Source metrics
- Connector and workflow versions
- Source API compatibility

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

The UI uses a generic stage renderer but displays separate source cards, metrics, warnings, and details for each connector.

## 4.3 Common statuses

Jobs, source runs, and stages use a compatible vocabulary:

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

Source-specific conditions are represented through machine-readable error codes, warning codes, and metrics, not incompatible status values.

## 4.4 Version every execution

Every source run records:

- Connector version
- Workflow version
- Normalization version
- Source API version
- Taxonomy version
- Qualification-policy version
- Configuration snapshot
- Capability snapshot

A running job remains pinned to the versions selected when it starts.

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

## 5.1 Source selection principles

The user chooses sources according to the market, evidence required, cost, access rights, and expected contribution.

A source must declare capabilities such as:

- Organization discovery
- Person discovery
- Phone discovery
- Email discovery
- Website discovery
- Geographic search
- Branch discovery
- Technology detection
- Incremental results
- Pause and resume
- Cost estimation

The Generate Leads page should explain what each source can and cannot contribute.

A source is not selected merely because it exists. It is selected because it contributes useful evidence for the requested sector, organization type, geography, and objective.

## 5.2 Google Places sourcing plan

Purpose:

- Organization discovery
- Physical-location discovery
- Public phone and website discovery
- Provider ID and operating-status evidence

Planned workflow:

```text
Validate Google access
→ Resolve quota and cost limits
→ Translate sector and organization types into categories and search queries
→ Build geographic coverage
→ Execute text and nearby searches
→ Follow pagination tokens
→ Fetch required place details
→ Normalize identity, phone, domain, address, and coordinates
→ Persist raw Google evidence
→ Resolve institutions and branches
→ Report coverage, quota, cost, and failures
```

Required metrics:

- Areas planned and completed
- Queries planned and completed
- Requests made
- Pages processed
- Places returned
- Unique provider IDs
- Duplicate provider results removed
- Records normalized
- Institutions created
- Institutions enriched
- Ambiguous matches
- Quota consumed
- Estimated cost
- Rate-limit retries
- Failed requests

## 5.3 Yandex Maps sourcing plan

Purpose:

- Additional organization and location coverage
- Cross-source corroboration
- Region-specific map evidence

Planned workflow:

```text
Validate Yandex access
→ Translate sector taxonomy
→ Build geographic search areas
→ Execute organization searches
→ Parse GeoJSON features
→ Process names, categories, phones, URLs, addresses, coordinates, and provider identifiers
→ Handle pagination and rate limits
→ Normalize evidence
→ Persist raw Yandex records
→ Resolve institutions and branches
→ Report coverage and failures
```

Yandex maintains its own taxonomy mapping and response parser while emitting the shared normalized-evidence contract.

## 5.4 Apple Maps sourcing plan

Purpose:

- Alternative map coverage
- Cross-source identity and location corroboration

Planned workflow:

```text
Validate MapKit signing configuration
→ Create or refresh token
→ Translate requested categories
→ Build geographic search plan
→ Execute searches
→ Derive stable versioned source identifiers when required
→ Normalize evidence
→ Persist source records
→ Resolve institutions and branches
→ Report token, quota, coverage, and failure metrics
```

Any derived source-ID algorithm must be versioned.

## 5.5 Website sourcing plan

Purpose:

- Organization enrichment
- Email and phone extraction
- Decision-maker evidence
- Technology and operational-signal detection
- Website-quality evidence
- Service-gap evidence

Planned workflow:

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
→ Extract person and role candidates with evidence
→ Detect technologies and operational signals
→ Aggregate evidence by domain and organization
→ Resolve organizations, branches, people, and contacts
→ Compute evidence-aware detection states
→ Report coverage and failure reasons
```

Priority pages may include:

- Homepage
- Contact
- About
- Team
- Leadership
- Services
- Admissions
- Locations
- Portal
- Careers
- Privacy and legal pages when needed for identity evidence

Required metrics:

- Seeds supplied and discovered
- Domains accepted and rejected
- Domains crawled
- Pages planned and fetched
- Successful pages
- Robots-disallowed pages
- HTTP failures
- Non-HTML pages
- Oversized responses
- Decode failures
- Contacts extracted
- Person candidates extracted
- Signals detected
- Institutions resolved

Required evidence rules:

- A static crawler cannot prove universal technology absence.
- `NOT_DETECTED` is not `ABSENT_CONFIRMED`.
- `NOT_CRAWLED` and `CRAWL_FAILED` contribute no confirmed absence evidence.
- Website snapshots used for scoring must be linked to the correct institution or domain.
- Contact-to-person attribution requires supporting evidence.

## 5.6 Authorized import sourcing plan

Purpose:

- Licensed, partner, customer-provided, or otherwise authorized structured data
- Controlled bulk intake

Planned workflow:

```text
Validate source authority
→ Inspect encoding and schema
→ Map columns
→ Validate identity fields
→ Normalize organization and contact data
→ Reject invalid rows with explicit reasons
→ Detect unchanged reimports
→ Detect new evidence in known rows
→ Persist append-only raw import evidence
→ Resolve organizations and people
→ Produce import and rejection reports
```

Required metrics:

- Rows read
- Rows valid
- Rows rejected
- Unchanged rows skipped
- New institutions created
- Existing institutions enriched
- Contacts added
- Ambiguous matches

## 5.7 Telegram sourcing plan

Purpose:

- Public-channel organization and contact evidence where permitted
- Secondary corroboration

Planned workflow:

```text
Validate configured channels and source policy
→ Fetch permitted public metadata and content
→ Extract organization identity and public contacts
→ Normalize evidence
→ Persist source records
→ Resolve organizations
→ Record coverage and failures
```

Telegram evidence should not automatically become high-confidence identity evidence without corroboration.

## 5.8 Manual sourcing plan

Purpose:

- Referrals
- Field research
- Existing business knowledge
- Controlled operator entry

Planned workflow:

```text
Validate authorized user input
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

Manual entry must not bypass duplicate resolution through unconditional canonical creation.

## 5.9 Professional-network sourcing plan

Status: **Restricted**.

The source remains disabled until an approved platform-access method, source-policy basis, credential model, security controls, and operating procedure are documented and implemented.

The future workflow is person-aware:

```text
Validate approved access method
→ Receive or discover permitted profile references
→ Collect permitted evidence
→ Identify person and role
→ Identify organization reference
→ Resolve organization against canonical institutions
→ Resolve or create PersonCandidate
→ Attach contact evidence only when attribution is supported
→ Run structured research with prompt-injection controls
→ Separate facts from inferences
→ Persist findings, signals, and account brief
→ Refresh organization and person readiness
```

A person must not be created as though the person were the organization.

---

# 6. Qualification architecture and sector rules

## 6.1 Qualification and opportunity scoring are separate

Qualification answers:

```text
Should this organization enter the usable lead pool for this objective?
```

Opportunity scoring answers:

```text
How valuable, relevant, and timely does the opportunity appear?
```

A lead may qualify but have a modest opportunity score because its infrastructure is already mature.

A lead may show a large service gap but still be disqualified because it is unreachable, prohibited, permanently closed, suppressed, or based on insufficient evidence.

## 6.2 Policy identity

Qualification is selected using:

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

Example:

```text
education / new_business / private_school / admissions_automation / version_3
```

## 6.3 Universal eligibility safeguards

Every sector policy operates after common safeguards:

- Canonical organization identity exists.
- Identity conflicts are below the allowed threshold.
- Operating status is acceptable.
- Required contactability exists for the objective.
- Intended contact channel is not suppressed.
- Data confidence reaches the minimum threshold.
- Required evidence is recent enough.
- Organization is not excluded by NEWAX ethical policy.
- Organization is not already in an incompatible campaign.
- Existing customers are excluded when the job requests new business only.
- Missing evidence is not converted into a positive fact.

## 6.4 Qualification rule types

Policies may define:

- Required rules
- Weighted rules
- Disqualifying rules
- Review-trigger rules
- Evidence requirements
- Staleness rules
- Allowed organization types
- Excluded organization types
- Minimum qualification score
- Source requirements for specific claims
- Objective-specific overrides

Arbitrary executable Python or SQL expressions must not be stored as policy rules.

## 6.5 Qualification outcomes

### Qualified

All mandatory rules pass and the qualification score reaches the threshold.

### Disqualified

A hard exclusion or mandatory requirement fails.

### Needs review

Evidence is missing, stale, conflicting, or too uncertain for automatic qualification.

Every assessment stores:

- Institution ID
- Harvest Job ID when applicable
- Policy ID and version
- Status
- Score and threshold
- Criterion results
- Evidence snapshot
- Rationale
- Assessment timestamp

Historical assessments do not silently change when a policy is updated.

## 6.6 Education policy plan

Possible organization types:

- School
- College
- University
- Academy
- Training organization

Possible qualification dimensions:

- Active institutional operation
- Reachable administration
- Admissions or student operations
- Branch or scale indicators
- Parent, student, faculty, fee, attendance, or communication complexity
- Manual workflow signals
- Existing portal or LMS evidence state
- Multi-campus reporting requirements

Possible objectives:

- Admissions automation
- Student operations
- LMS or portal opportunity
- Website modernization
- Parent communication
- Multi-campus operating system

Relevant NEWAX outcomes:

- Simplify admissions
- Reduce manual administration
- Improve student-operation visibility
- Centralize communication
- Strengthen institutional control

## 6.7 Healthcare policy plan

Possible organization types:

- Clinic
- Hospital
- Diagnostic laboratory
- Dental clinic
- Rehabilitation center
- Healthcare network

Possible qualification dimensions:

- Active facility identity
- Reachable administration or management
- Appointment, patient coordination, inventory, reporting, or branch complexity
- Multiple departments or locations
- Secure workflow requirements
- Operational handoff complexity

Safeguards:

- Do not collect unnecessary patient information.
- Do not infer patient medical conditions.
- Do not use sensitive personal health information as sales evidence.

Relevant NEWAX outcomes:

- Improve operational coordination
- Strengthen visibility
- Reduce manual handoffs
- Protect sensitive workflows

## 6.8 Real-estate policy plan

Possible organization types:

- Property developer
- Real-estate agency
- Property manager
- Facility operator
- Real-estate group

Possible qualification dimensions:

- Active portfolio, development, or listings
- Number of properties, agents, branches, or developments
- Lead distribution and follow-up complexity
- Inventory and availability visibility
- Property-management workflows
- Connected-building or facility-monitoring opportunity

A solo agent may qualify for a simple CRM objective but fail a multi-site infrastructure objective.

## 6.9 Legal policy plan

Possible organization types:

- Law firm
- Structured legal-services organization

Possible qualification dimensions:

- Multiple lawyers, departments, or offices
- Matter intake complexity
- Document-control requirements
- Client communication
- Deadline management
- Secure internal operations
- Reachable administrative or partner-level contact

Relevant NEWAX outcomes:

- Improve matter visibility
- Strengthen document control
- Simplify client intake
- Build dependable internal operations

## 6.10 Hospitality policy plan

Possible organization types:

- Hotel
- Approved restaurant group
- Event venue
- Hospitality operator

Possible qualification dimensions:

- Active public operation
- Reservation and guest-service workflow
- Inventory and staff coordination
- Multiple departments or branches
- Facility monitoring
- Connected-infrastructure needs

NEWAX ethical industry restrictions apply before qualification.

## 6.11 Retail policy plan

Possible organization types:

- Retail store
- Retail chain
- Distributor
- Supermarket
- Boutique
- Showroom
- Omnichannel seller

Possible qualification dimensions:

- Number of locations and channels
- Inventory complexity
- Procurement complexity
- Order and customer operations
- Centralized reporting requirements
- Reachable management

## 6.12 Islamic-finance policy plan

Possible organization types:

- Sharia-compliant financial institution
- Islamic fintech
- Approved takaful-related organization
- Islamic accounting or financial-services organization

Possible qualification dimensions:

- Regulatory and operating legitimacy
- Approval and record complexity
- Reporting and integration requirements
- Secure data control
- Workflow ownership requirements

Conventional interest-based financial operations are excluded according to NEWAX policy.

## 6.13 Professional-services policy plan

Possible organization types:

- Accounting firm
- Architecture or engineering firm
- Structured advisory firm
- Other repeatable business-services organization

Possible qualification dimensions:

- Structured firm rather than an isolated informal operator
- Repeatable client-delivery processes
- Multiple team members or service lines
- Client onboarding
- Task, document, reporting, and CRM complexity

## 6.14 Policy upgrade rules

1. New jobs use the latest approved policy version.
2. Running jobs remain pinned to their starting policy version.
3. Historical assessments retain the original policy and evidence snapshot.
4. Requalification is an explicit action.
5. Policy edits create a new version instead of rewriting history.
6. Policy activation and retirement require authorization and audit logs.

---

# 7. The 64 delivery modules

## Phase 1: Stabilize the existing repository

### Module 1: Open-PR and branch cleanup

Review every open PR and classify it as merge, rebase, split, replace, or close. Retire obsolete branches and prevent superseded work from being merged accidentally.

Acceptance:

- Dependency graph recorded.
- Unsafe and obsolete PRs identified.
- No unclear stacked branch remains in the active sequence.

### Module 2: Website evidence and detection corrections

Integrate institution/domain-scoped page snapshots, evidence-aware detection statuses, service-gap scoring corrections, regression tests, and the profile-recomputation command.

Acceptance:

- Cross-institution snapshot contamination is impossible.
- Detection states remain distinct.
- Existing affected profiles can be recomputed deliberately.

### Module 3: Deletion graph and data correction

Integrate complete deletion cascades, shared-evidence handling, deletion manifests, residual-data verification, migration-chain tests, and post-correction data operations.

### Module 4: Architecture documentation integration

Merge the updated README and this roadmap after the correction stack is stable.

### Module 5: Frontend PR disposition

Review existing frontend PRs and classify reusable components and pages as reuse, rebase, split, replace, or close.

### Module 6: Repository baseline verification

Establish the exact verified starting SHA with complete backend tests, migration-chain checks, frontend build, type checking, static analysis, CodeQL, and documented external-security-check status.

---

## Phase 2: Authentication, permissions, and security

### Module 7: Strict authentication

Reject unknown tokens, define explicit development authentication, enforce expiry, and test invalid-token behavior.

### Module 8: Authorization matrix

Define and apply permissions for viewer, operator, reviewer, compliance officer, administrator, and service account roles across every route.

### Module 9: Service authentication and frontend sessions

Implement service-to-service authentication, frontend session lifecycle, production CORS, logout, and expiry handling.

### Module 10: Crawler and raw-data security

Implement SSRF controls, redirect revalidation, private-network blocking, protocol restrictions, response-size limits, HTML retention, and purge policy.

### Module 11: Contact and person evidence integrity

Persist all supported contacts, require evidence for person attribution, store attribution confidence, and prevent false decision-maker linkage.

### Module 12: Migration-driven test infrastructure

Build test databases through Alembic and verify fresh schema, full upgrade, downgrade, and post-migration application behavior.

---

## Phase 3: Resolution consistency

### Module 13: Resolution concurrency protection

Implement proven identity locking, preferably PostgreSQL advisory locking around normalized organization keys.

### Module 14: Concurrent duplicate reconciliation

Detect and safely reconcile duplicates that still emerge from overlapping source transactions.

### Module 15: Resolution transaction boundaries

Define per-record transactions, savepoints, retry safety, partial failures, and profile-refresh timing.

### Module 16: Resolution observability

Add structured events and metrics for merge, pending, link-only, reject, lock conflict, retry, and reconciliation outcomes.

---

## Phase 4: Shared Harvest Job contracts

### Module 17: Common status and error contracts

Define job, source-run, and stage statuses plus machine-readable warning and error codes.

### Module 18: Source capability and workflow schemas

Define backend-provided capabilities, source stages, metrics, retry behavior, pause/resume support, and UI labels.

### Module 19: Normalized evidence contract

Define common evidence envelopes for organizations, branches, people, contacts, locations, and signals while preserving raw source payloads.

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

Deliver schema migration, constraints, indexes, downgrade path, and compatibility tests for existing `SourceRun` data.

---

## Phase 6: Harvest Job APIs

### Module 25: Job creation and validation API

Implement `POST /api/v1/harvest-jobs` with request validation, source compatibility, sector/objective validation, version pinning, and idempotency.

### Module 26: Job listing and detail APIs

Implement list and detail endpoints with pagination, filtering, source summaries, stages, counts, warnings, and permissions.

### Module 27: Job state-control APIs

Implement pause, resume, cancel, and retry commands with legal state transitions.

### Module 28: Source-run and result APIs

Expose source-run details, stage details, frozen results, rejection reasons, and source contribution.

---

## Phase 7: Runtime and worker orchestration

### Module 29: Parent-job planner

Convert a validated market request into independently versioned child source-run plans.

### Module 30: Worker claiming, leases, and heartbeats

Implement atomic claims, lease expiry, heartbeats, stuck-work detection, and safe reassignment.

### Module 31: Retry and checkpoint engine

Support source-specific retry policy, backoff, pagination cursors, crawl checkpoints, processed IDs, quota state, and resumability.

### Module 32: Job progress aggregation

Calculate real parent progress from child source metrics without fabricated elapsed-time percentages.

### Module 33: Live event streaming

Implement authenticated Server-Sent Events with cursors, reconnect, missed-event replay, and source/stage filtering.

---

## Phase 8: Connector framework

### Module 34: Source connector protocol and registry

Create the shared connector interface and version-aware connector registry.

### Module 35: Connector execution context

Provide cancellation, checkpointing, events, credentials, quotas, cost tracking, and evidence sinks.

### Module 36: Incremental evidence persistence

Persist raw and normalized evidence while the source is running instead of waiting for complete collection.

### Module 37: Connector contract test harness

Require every connector to pass shared tests for validation, stage reporting, cancellation, retry, versioning, evidence output, and partial failure.

---

## Phase 9: Map source connectors

### Module 38: Google planning workflow

Implement credential validation, category mapping, geographic coverage, query planning, quota estimation, and Google-specific stages.

### Module 39: Google collection workflow

Implement searches, pagination, place details, incremental storage, checkpoints, metrics, errors, and retries.

### Module 40: Yandex complete workflow

Implement taxonomy translation, geographic planning, GeoJSON parsing, pagination, normalization, checkpoints, and metrics.

### Module 41: Apple Maps complete workflow

Implement token lifecycle, search planning, stable source IDs, normalization, checkpoints, and metrics.

### Module 42: Cross-map normalization tests

Verify that equivalent organizations produce compatible normalized evidence across map connectors.

---

## Phase 10: Website and secondary sources

### Module 43: Website discovery and crawl planning

Implement seed normalization, approved search discovery, URL validation, priority-page planning, domain plans, and website stage definitions.

### Module 44: Incremental website crawling

Create source runs before crawling and persist fetch progress, checkpoints, robots decisions, failures, and metrics incrementally.

### Module 45: Website extraction and aggregation

Extract all supported contacts, organization identity, person candidates, technology signals, and domain-level evidence safely.

### Module 46: Authorized import workflow

Implement schema inspection, mapping, validation, unchanged-row detection, rejection reporting, and resolution handoff.

### Module 47: Manual and Telegram workflows

Adapt both sources to the common connector, job, evidence, and entity-resolution contracts.

### Module 48: Restricted professional-network workflow

Build the safe person-aware evidence and resolution model while keeping source execution disabled until approved.

---

## Phase 11: Resolution and enrichment integration

### Module 49: Normalized evidence dispatcher

Route organization, branch, person, contact, location, and signal evidence to the correct shared service.

### Module 50: Organization and branch resolution

Resolve canonical institutions and physical branches within safe identity transactions.

### Module 51: Person and contact resolution

Resolve person candidates, roles, organization associations, contacts, attribution confidence, and unsupported relationships.

### Module 52: Provenance and source contribution

Record which source contributed each identity field, location, contact, person, signal, and qualification fact.

### Module 53: Job-linked human review

Link ambiguous resolution cases to the Harvest Job, source run, evidence, reviewer decision, and result status.

### Module 54: Transactional lead-profile refresh

Refresh scoring only after durable canonical changes and preserve score history.

---

## Phase 12: Qualification policy engine

### Module 55: Qualification policy models and versioning

Create versioned policies scoped by sector, lead type, organization type, and objective.

### Module 56: Qualification rule engine

Implement bounded required, weighted, disqualifying, review-trigger, evidence, and staleness rules.

### Module 57: Universal eligibility and policy selection

Apply common safeguards and select the most specific valid policy using documented fallback rules.

### Module 58: Qualification assessments and requalification

Persist criterion-level evidence, score, threshold, rationale, policy version, and explicit requalification behavior.

### Module 59: Education and healthcare policies

Implement and test the first detailed policies because they provide high-value but materially different operating models.

### Module 60: Remaining sector policies

Implement real estate, legal, hospitality, retail, Islamic finance, and professional-services policy definitions.

---

## Phase 13: Lead workspace and integrations

### Module 61: Generated Leads and Master Leads APIs

Implement frozen job-result queries and canonical all-run lead queries with search, filters, sorting, pagination, selected IDs, and saved views.

### Module 62: Lead Dossier and activity timeline

Aggregate organization, branches, contacts, people, scores, qualification, evidence, source history, compliance, communication, and audit activity.

### Module 63: Export and Communicator backend

Implement selected-ID and filter-snapshot exports, secure download, email delivery, campaign model, frozen audience, recipient eligibility, sequence, approval, scheduling, and stop rules.

Split this module into export and Communicator PRs if migration or review size exceeds the module rules.

### Module 64: Complete frontend and rollout

Deliver internal frontend slices for:

1. Runtime configuration and authentication
2. Generate Leads
3. Harvest Run and live events
4. Source-specific processing displays
5. Generated Leads
6. Master Leads
7. Lead Dossier
8. Export and Communicator setup
9. Operations and failure recovery
10. End-to-end and production verification

These slices may use separate PRs while remaining one final product milestone.

---

# 8. Dependency order

```text
Modules 1–16
Repository stability, security, data integrity, and resolution consistency
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
Modules 61–64
Lead workspaces, exports, Communicator, frontend, and rollout
```

Frontend shells may be explored earlier on disconnected branches, but they must not imply unavailable APIs are operational.

---

# 9. Delivery milestones

## Milestone A: Verified foundation

Modules 1–16

Outcome:

- Existing correction stack integrated
- Unsafe and obsolete PRs retired
- Authentication and permissions hardened
- Crawler and raw-data security improved
- Contacts and people remain evidence-safe
- Resolution is concurrency-aware
- Exact baseline is verified

## Milestone B: Harvest Job platform

Modules 17–37

Outcome:

- Harvest Jobs can be created and inspected
- Child source runs and source-specific stages exist
- Jobs can pause, resume, retry, and cancel
- Workers use claims, leases, heartbeats, checkpoints, and retries
- Live events are available
- Connectors share one tested contract

## Milestone C: Source workflows

Modules 38–48

Outcome:

- Google, Yandex, Apple, websites, imports, manual, and Telegram use independent workflows
- Each workflow is versioned and upgradeable
- Each source displays its real process and metrics
- Professional-network support remains restricted but structurally safe

## Milestone D: Qualified canonical leads

Modules 49–60

Outcome:

- Organization, branch, person, contact, signal, and provenance evidence resolve correctly
- Human review is job-linked
- Qualification is versioned and objective-specific
- Each sector uses appropriate qualification rules
- Qualification remains separate from opportunity scoring

## Milestone E: Operational lead workspace

Modules 61–63

Outcome:

- Generated Leads represents one frozen job result
- Master Leads represents the current canonical database
- Lead Dossier explains facts, evidence, uncertainty, history, and next actions
- Selected leads can be exported
- Eligible selected leads can create a frozen Communicator audience

## Milestone F: Complete product workflow

Module 64

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

---

# 10. Acceptance criteria for the target workflow

The roadmap is not complete until all of the following are proven:

1. An authorized user can create a Harvest Job from the UI and API.
2. The request pins connector, workflow, normalization, taxonomy, source API, and qualification-policy versions.
3. Multiple selected sources create separate child runs under one parent job.
4. Every source exposes a real source-specific workflow to the UI.
5. The UI does not fabricate progress.
6. Raw evidence is persisted incrementally and remains auditable.
7. Concurrent sources do not silently create duplicate canonical institutions.
8. Ambiguous matches enter human review.
9. Website detection distinguishes absence, non-detection, no crawl, failure, and unknown states.
10. Contact-to-person attribution is evidence-backed.
11. Each sector and objective uses the correct versioned qualification policy.
12. Qualification and opportunity scoring remain separate.
13. Accepted, rejected, and review-required job results are frozen with reasons.
14. Generated Leads shows one job’s result snapshot.
15. Master Leads shows canonical records across every harvest.
16. Lead Dossier exposes facts, detections, inferences, unknowns, evidence, and history distinctly.
17. Selected leads can be exported by canonical ID.
18. A Communicator campaign freezes its audience at creation.
19. Suppressed and ineligible recipients cannot be sent messages.
20. Campaign creation does not automatically send before required approval.
21. Pause, resume, retry, cancel, partial failure, and recovery states are tested.
22. Migrations upgrade and downgrade cleanly.
23. Backend tests, frontend checks, security checks, runtime verification, and exact-commit CI pass.
24. Rollback and post-deployment verification procedures are documented and tested.

---

# 11. Immediate active batch

Only the following modules should begin immediately:

```text
Module 1  Open-PR and branch cleanup
Module 2  Website evidence and detection corrections
Module 3  Deletion graph and data correction
Module 4  Architecture documentation integration
Module 5  Frontend PR disposition
Module 6  Repository baseline verification
```

Modules 7–12 begin only after the corrected baseline is integrated and verified.

The Harvest Job architecture begins only after authentication, evidence integrity, migration testing, and resolution concurrency are no longer blockers.

Building a sophisticated orchestrator on unreliable identity and evidence would not simplify operations. It would merely produce incorrect answers with better progress bars.

---

# 12. Roadmap governance

- This file is the delivery-order source of truth.
- README explains the product and architecture; this roadmap controls implementation sequence.
- A module may be split when its final design exceeds sizing or risk limits.
- Modules may be combined only when they share one migration, one transaction boundary, one API contract, or one inseparable user outcome.
- Dependency order may change only after live-code inspection and documented reasoning.
- Completed modules must be marked with the exact merged PR and commit.
- Historical module descriptions must not be silently rewritten to make past work appear different.
- Only the next six to ten modules should be represented as active implementation issues.
- No module is complete while tests, migrations, security checks, runtime verification, or exact-commit CI remain unresolved.
