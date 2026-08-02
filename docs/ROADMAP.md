# Harvester Standalone Product Roadmap

## Authority and status

Status: **Planned and partially implemented**

This is the authoritative top-level module roadmap for Harvester as an independent, standalone, resellable lead-intelligence application.

It **re-baselines all 64 top-level modules** around the approved product boundary. The former roadmap remains available in Git history and the pull-request diff for historical reference.

The earlier HSP workstreams are now a transition crosswalk, not an extra module count. Harvester has **64 top-level product modules**, not 64 modules plus another stack of architecture labels pretending arithmetic is a strategy.

## Locked product boundary

Harvester must operate without NEWAX Core or Communicator.

```text
Harvester
Owns source intake, observations, evidence, resolution, lead records,
qualification, scoring, research, dossiers, selection, exports,
publishing rules, synchronization, operations, and product administration.

Communicator
Optionally receives approved lead and context payloads.
Owns communication profiles, audiences, campaigns, messages,
conversations, engagement, replies, and follow-up.

NEWAX Core
Optionally receives source-native observations, resolved entities,
and approved source-owned lead facets.
Owns enterprise existence, canonical identity, relationships,
provenance, field governance, and cross-system identity links.
```

No product shares database tables, credentials, migrations, internal schemas, or runtime availability.

## Module completion contract

Every top-level module is treated as a reusable product unit. Where applicable, it must include:

```text
UI
Backend services
Database ownership and migrations
Public or internal API
Validation
Permissions
Tests
Documentation
Changelog
Version and compatibility policy
Operational visibility
```

A module is not Complete because one endpoint exists or because a markdown heading has developed confidence.

## Status vocabulary

- **Current:** The principal capability exists in the repository today.
- **Partial:** Useful foundations exist, but the complete standalone product workflow is not connected.
- **Planned:** Required future work.
- **Restricted:** Disabled until access, legal, security, compliance, and operational approval exist.

## Module domains

| Domain | Modules | Purpose |
| --- | ---: | --- |
| Product Foundation | 01–08 | Independent application, access, ownership and audit |
| Connections and Data Exchange | 09–16 | Credentials, connectors, schemas, mappings and synchronization |
| Harvest Orchestration and Source Workflows | 17–24 | Jobs, workers and governed intake |
| Discovery, Evidence and Resolution | 25–32 | Source discovery, evidence preservation and identity resolution |
| Lead Intelligence | 33–40 | Lead records, people, contacts, research, qualification and scoring |
| Workspaces and Governance | 41–48 | Quality, compliance, review and operator workspaces |
| Activation and Optional Integrations | 49–56 | Filters, exports, publishing and optional destinations |
| Operations, Resale and Release | 57–64 | Reliability, administration, productization and release quality |

---

# A. Product Foundation

## Module 01 — Application Shell and Navigation

**Status:** Partial

**Outcome:** Provide the standalone Harvester application frame, navigation, environment visibility, responsive layout, and route ownership.

**Owns:** App shell, page headers, breadcrumbs, responsive navigation, environment indicator, permission-aware menus.

**Does not own:** Lead discovery logic, connector logic, and customer communication.

**Acceptance:** All standalone workspaces are reachable without NEWAX Core or Communicator; navigation reflects permissions and deployment capabilities.

## Module 02 — Design System and Accessibility Foundation

**Status:** Partial

**Outcome:** Provide one calm, enterprise-ready visual and interaction system across the product.

**Owns:** Tokens, typography, spacing, buttons, inputs, tables, dialogs, status patterns, loading states, keyboard behavior, reduced motion.

**Does not own:** Business rules or source-specific workflow state.

**Acceptance:** Shared components pass accessibility checks and every module uses the same visual language instead of inventing another shade of dashboard anxiety.

## Module 03 — Tenant and Workspace Isolation

**Status:** Planned

**Outcome:** Separate every customer's data, configuration, credentials, jobs, leads, exports, and audit history.

**Owns:** Tenant identity, workspace boundaries, tenant-scoped queries, storage prefixes, background-job scope, tenant tests.

**Does not own:** Cross-tenant analytics without explicit governed aggregation.

**Acceptance:** A tenant cannot read, write, export, infer, or operate on another tenant's data through UI, API, worker, file, cache, or event path.

## Module 04 — Authentication and Session Security

**Status:** Partial

**Outcome:** Authenticate users and service identities independently of other NEWAX products.

**Owns:** Login, logout, session lifecycle, password or external identity integration, service credentials, expiry, revocation, reauthentication.

**Does not own:** Business permissions and connector credentials.

**Acceptance:** Harvester can be deployed and accessed without Core authentication; session and service-token behavior is tested.

## Module 05 — Authorization and Permission Registry

**Status:** Partial

**Outcome:** Control every business and administrative action through explicit permissions.

**Owns:** Permission catalog, role composition, policy checks, API guards, worker authorization context, denied-action audit.

**Does not own:** Hardcoded business behavior based on role names.

**Acceptance:** Every protected UI action and API operation maps to an explicit permission and is denied by default.

## Module 06 — Users, Teams, Ownership and Assignment

**Status:** Planned

**Outcome:** Manage operators, reviewers, administrators, owners, and work assignment inside Harvester.

**Owns:** User lifecycle, teams, lead ownership, review assignment, workload visibility, reassignment history.

**Does not own:** Customer communication ownership once records are published to Communicator.

**Acceptance:** Leads, reviews, jobs, and operational tasks can be assigned and traced without relying on another application.

## Module 07 — Product Configuration and Environment Profiles

**Status:** Partial

**Outcome:** Manage tenant and deployment configuration without editing application code.

**Owns:** Development, testing, staging and production profiles; feature settings; limits; taxonomies; safe defaults; configuration history.

**Does not own:** Secrets and database passwords.

**Acceptance:** Configuration is validated, versioned, tenant-scoped where applicable, and distinguishable from credentials.

## Module 08 — Audit and Activity History

**Status:** Partial

**Outcome:** Preserve who did what, when, from where, and against which object.

**Owns:** User actions, service actions, approvals, configuration changes, exports, publications, security events, correlation IDs.

**Does not own:** Raw source evidence, which remains in evidence modules.

**Acceptance:** Material actions are append-only, queryable, exportable under permission, and never contain plaintext secrets.

# B. Connections and Data Exchange

## Module 09 — Credential Vault and Secret Lifecycle

**Status:** Planned

**Outcome:** Store and use database, API, webhook, queue, signing, and provider credentials safely.

**Owns:** Write-only secrets, encryption, secret references, fingerprints, candidate validation, activation, rotation, retirement, audit.

**Does not own:** Returning stored plaintext secrets to the browser or logs.

**Acceptance:** A failed replacement leaves the previous credential active; plaintext is unavailable after submission.

## Module 10 — Connection Profiles and Access Modes

**Status:** Planned

**Outcome:** Describe every external source or destination independently from its credentials.

**Owns:** Connector type, environment, endpoint metadata, database metadata, SSL, tenant, purpose, health, read/write mode.

**Does not own:** Source-specific field mapping and Harvester normalization.

**Acceptance:** Every connection declares read-only, import, export, write, bidirectional, or inspection capability and uses least privilege.

## Module 11 — Connector Registry and Capability Framework

**Status:** Partial

**Outcome:** Provide one plugin contract for built-in and future connectors.

**Owns:** Connector registration, version, capabilities, limits, validation, schema discovery, cursors, health, contract tests.

**Does not own:** Embedding source-specific assumptions into the central orchestrator.

**Acceptance:** Unsupported operations fail explicitly and a connector can be upgraded without changing Harvester's lead model.

## Module 12 — Source Schema Registry

**Status:** Planned

**Outcome:** Version the structure and meaning of every incoming source.

**Owns:** Schema identity, versions, field metadata, samples, compatibility, activation, deprecation, source ownership.

**Does not own:** Harvester's internal lead schema.

**Acceptance:** A changed source schema cannot silently reuse an incompatible mapping or corrupt previously understood records.

## Module 13 — Mapping and Transformation Profiles

**Status:** Partial

**Outcome:** Convert source-native fields into Harvester intake contracts while preserving the original payload.

**Owns:** Direct mapping, rename, constants, conditions, enums, split, combine, lookup, normalization, metadata, ignore, review rules.

**Does not own:** Final lead qualification, scoring, or Core formatting.

**Acceptance:** Mappings are versioned, previewable, testable, rollback-capable, and independent for every source and tenant.

## Module 14 — Import Preview, Validation and Quarantine

**Status:** Planned

**Outcome:** Show what an import or synchronization will do before records enter normal processing.

**Owns:** Samples, mapped preview, validation results, duplicate hints, create/update/skip/quarantine actions, rejection reasons.

**Does not own:** Direct writes to Master Leads.

**Acceptance:** Operators can inspect source, transformed result, validation, intended action, and errors before activation.

## Module 15 — Synchronization Engine and Checkpoints

**Status:** Partial

**Outcome:** Move data reliably between Harvester and approved sources or destinations without coupling local transactions to remote availability.

**Owns:** Manual, scheduled, polling, webhook and event modes; checkpoints; retries; backoff; dead letter; backpressure; idempotency.

**Does not own:** Product-specific mapping or destination business logic.

**Acceptance:** Runs resume from durable checkpoints, preserve event identity on retry, and never roll back committed Harvester data because a remote system is unavailable.

## Module 16 — Synchronization Conflicts, Reconciliation and Repair

**Status:** Planned

**Outcome:** Detect and resolve drift, missing deliveries, conflicting revisions, and partial synchronization.

**Owns:** Conflict records, dry-run comparison, replay, repair, backfill, checksums, operator decisions, reconciliation reports.

**Does not own:** Silent last-write-wins behavior.

**Acceptance:** Every conflict has evidence, a resolution state, an audit trail, and a safe replay or manual-repair path.

# C. Harvest Orchestration and Source Workflows

## Module 17 — Harvest Job Definition

**Status:** Planned

**Outcome:** Represent one complete lead-generation request independently of any particular source.

**Owns:** Objective, lead type, sectors, organization types, geography, source mix, target count, quality mode, exclusions, pinned versions.

**Does not own:** Source execution details.

**Acceptance:** The same job contract works when one or many sources are selected and remains historically reproducible.

## Module 18 — Harvest Job Orchestrator

**Status:** Planned

**Outcome:** Coordinate selected source workflows, acceptance targets, pause, resume, retry, cancellation, completion, and partial failure.

**Owns:** Parent lifecycle, child-run creation, acceptance accounting, failure isolation, cost and quota summary, frozen completion state.

**Does not own:** Source-specific crawling, pagination, or parsing.

**Acceptance:** One source failure does not erase other results; the parent state is derived from durable child state rather than frontend optimism.

## Module 19 — Source Run and Stage Engine

**Status:** Partial

**Outcome:** Give every connector an independently versioned workflow under one common lifecycle.

**Owns:** Source run, stage definitions, stage state, metrics, cursors, warnings, failures, heartbeats, pinned connector and workflow versions.

**Does not own:** Hardcoded frontend progress logic.

**Acceptance:** The backend publishes real stages and metrics; the frontend renders them generically.

## Module 20 — Scheduler, Worker and Execution Control

**Status:** Partial

**Outcome:** Run harvest, verification, research, synchronization, export, and maintenance work reliably.

**Owns:** Queues, worker leases, concurrency, retries, priorities, schedules, cancellation, stranded-work recovery, workload limits.

**Does not own:** Source or lead business rules.

**Acceptance:** No work is silently lost, duplicated, or executed outside the correct tenant and permission context.

## Module 21 — Manual Lead and Evidence Entry

**Status:** Current

**Outcome:** Allow authorized users to submit organizations, people, contacts, and evidence through the same governed pipeline as automated sources.

**Owns:** Original submission, validation, normalization, duplicate resolution, provenance, correction history.

**Does not own:** Bypassing identity resolution or qualification.

**Acceptance:** Manual entry preserves the original input and cannot create a duplicate merely because a human clicked confidently.

## Module 22 — Authorized File Import

**Status:** Current

**Outcome:** Import licensed or customer-owned CSV, JSON, and approved tabular datasets.

**Owns:** Authority reference, encoding and schema inspection, column mapping, row validation, reimport detection, rejection report.

**Does not own:** Unlicensed acquisition or uncontrolled spreadsheet-to-table copying.

**Acceptance:** Every row retains source authority, source identity, mapping version, raw evidence, and a deterministic import result.

## Module 23 — Database Source Connectors

**Status:** Planned

**Outcome:** Read approved data from customer or partner databases through pluggable adapters.

**Owns:** PostgreSQL, MySQL, MariaDB, SQL Server, SQLite, MongoDB, Supabase, Neon, RDS-compatible, Cloud SQL-compatible, Azure SQL.

**Does not own:** Database-owner access, arbitrary SQL from the browser, or direct writes to Harvester business tables.

**Acceptance:** Adapters enforce allowlists, bounded queries, least privilege, contract tests, checkpoints, and explicit capability limits.

## Module 24 — API and Webhook Source Connectors

**Status:** Planned

**Outcome:** Receive or retrieve approved records from REST, GraphQL, webhook, partner, and customer APIs.

**Owns:** Authentication, pagination, rate limits, signatures, retries, schema versions, polling and event intake.

**Does not own:** Provider-specific business normalization outside adapter and mapping layers.

**Acceptance:** Every accepted payload is authenticated where required, preserved source-native, versioned, and traceable to its connection.

# D. Discovery, Evidence and Resolution

## Module 25 — Public Website and Search Discovery

**Status:** Partial

**Outcome:** Discover and inspect approved public websites and search results for organization, person, contact, technology, and operational evidence.

**Owns:** Seed discovery, URL policy, robots and terms controls, crawl planning, SSRF protection, page extraction, crawl states.

**Does not own:** Treating non-detection as confirmed absence.

**Acceptance:** Fetch attempts, coverage, failures, snapshots, evidence and detection states remain explicit and auditable.

## Module 26 — Map Provider Discovery

**Status:** Partial

**Outcome:** Discover organizations and branches through approved map providers.

**Owns:** Google Places, Yandex Maps, Apple Maps, category translation, geography planning, pagination, quota, provider IDs, place details.

**Does not own:** One universal parser pretending every provider has the same taxonomy.

**Acceptance:** Every provider has an isolated workflow and emits the common evidence contract with versioned source identity.

## Module 27 — Telegram and Approved Public-Channel Discovery

**Status:** Partial

**Outcome:** Collect permitted public-channel evidence under explicit source policy.

**Owns:** Configured channels, permitted metadata and content, public contacts, organization hints, coverage, corroboration requirements.

**Does not own:** Private access, access-control bypass, or automatic high-confidence identity claims.

**Acceptance:** Public-channel evidence remains low-confidence until corroborated and can be disabled by policy.

## Module 28 — Professional-Network Discovery

**Status:** Restricted

**Outcome:** Support lawful, approved professional-network research without making it a default dependency.

**Owns:** Approved access methods, profile references, person-role evidence, organization links, research safety, facts versus inference.

**Does not own:** Credential abuse, access-control bypass, anti-bot circumvention, or representing a person as an organization.

**Acceptance:** The module stays disabled until access, legal, security, compliance, and operational approval are recorded.

## Module 29 — Raw Observation Store

**Status:** Current

**Outcome:** Preserve every accepted source observation before interpretation.

**Owns:** Immutable raw records, source identity, payload hash, versions, capture time, tenant, connector, schema, authority, retention.

**Does not own:** Canonical lead decisions.

**Acceptance:** Identical payloads deduplicate safely; changed payloads create new immutable versions; different sources remain separate evidence.

## Module 30 — Snapshot and Document Evidence Store

**Status:** Partial

**Outcome:** Preserve website pages, documents, attachments, and other evidence artifacts used for extraction or verification.

**Owns:** Content hash, storage reference, MIME type, fetch result, source URL, timestamps, retention, access controls.

**Does not own:** Unbounded storage without policy or copying credentials into artifacts.

**Acceptance:** Every extracted fact can point to the correct artifact and access follows tenant, privacy, and retention rules.

## Module 31 — Normalized Evidence and Provenance

**Status:** Partial

**Outcome:** Convert raw source material into comparable evidence without losing its origin.

**Owns:** Normalized names, domains, phones, locations, roles, contacts, field provenance, confidence, detection state, source references.

**Does not own:** Lead qualification, scoring, or customer relationship state.

**Acceptance:** Facts, detections, inferences, unknowns and conflicts are distinguishable and linked back to raw evidence.

## Module 32 — Entity Resolution and Conflict Workbench

**Status:** Partial

**Outcome:** Resolve duplicate organizations, branches, people, contacts, domains, and relationships safely.

**Owns:** Candidate generation, match scoring, merge/link/reject/review decisions, concurrency protection, conflict evidence, human review.

**Does not own:** NEWAX Core canonical identity; Harvester resolves its own lead-oriented records.

**Acceptance:** Ambiguous matches remain reviewable, concurrent sources cannot silently create duplicates, and every merge is reversible or reconstructable from evidence.

# E. Lead Intelligence

## Module 33 — Master Lead Registry

**Status:** Current

**Outcome:** Maintain Harvester's resolved lead-oriented organizations, branches, people, contacts, and relationships.

**Owns:** Harvester IDs, current resolved views, source links, operating state, branch structure, current contacts, revision history.

**Does not own:** Enterprise-wide existence or canonical identity owned by optional NEWAX Core.

**Acceptance:** The registry works independently and can retain optional external identity links without replacing Harvester IDs.

## Module 34 — Person, Role and Relationship Attribution

**Status:** Partial

**Outcome:** Connect people to organizations and roles only when supported by evidence.

**Owns:** Person candidates, role history, organization relationship, attribution confidence, source evidence, review state.

**Does not own:** Assuming every email or phone belongs to a named person.

**Acceptance:** Person-role links expose confidence and evidence; unsupported attribution stays organization-level or unknown.

## Module 35 — Contact Method Verification

**Status:** Partial

**Outcome:** Assess whether email, phone, WhatsApp, website, form, and other contact methods are usable and current.

**Owns:** Syntax, domain, reachability where lawful, source corroboration, verification time, invalidation, replacement, history.

**Does not own:** Campaign sending or conversation management.

**Acceptance:** Invalidation never deletes historical evidence; verification freshness and intended-channel eligibility remain explicit.

## Module 36 — Lead Profile and History

**Status:** Current

**Outcome:** Summarize the current commercial lead interpretation of a resolved entity.

**Owns:** Lead status, profile attributes, size, contactability, category fit, research summary, score snapshots, change history.

**Does not own:** Entity existence or customer communication history.

**Acceptance:** Profile changes are versioned and traceable to evidence, policy, and scoring inputs.

## Module 37 — Signals and Research Findings

**Status:** Current

**Outcome:** Store detected opportunities, risks, needs, events, facts, and structured research findings.

**Owns:** Signal type, evidence, confidence, freshness, source, status, review, supersession.

**Does not own:** Presenting inference as fact.

**Acceptance:** Signals distinguish observed fact, model inference, operator assessment, and unknown state.

## Module 38 — Website and Technology Intelligence

**Status:** Partial

**Outcome:** Assess the organization's public digital and operational infrastructure from scoped evidence.

**Owns:** Technology detection, website quality, forms, portals, analytics, accessibility, infrastructure indicators, detection states.

**Does not own:** Declaring absence when crawl coverage is insufficient.

**Acceptance:** Every detection records evidence, scope, confidence, freshness, and PRESENT/ABSENT_CONFIRMED/NOT_DETECTED/NOT_CRAWLED/CRAWL_FAILED/UNKNOWN state.

## Module 39 — Qualification Policy and Assessment

**Status:** Partial

**Outcome:** Decide whether a resolved entity belongs in a usable lead pool under a versioned policy.

**Owns:** Sector, lead type, organization type, objective, policy versions, required rules, weighted rules, disqualifiers, review triggers, evidence requirements.

**Does not own:** Opportunity ranking or Core entity admission.

**Acceptance:** Assessments preserve policy version, criteria, evidence snapshot, rationale, threshold, outcome, and review state.

## Module 40 — Opportunity Scoring, Maturity and Service-Gap Analysis

**Status:** Partial

**Outcome:** Rank qualified or reviewable opportunities by value, fit, urgency, and likely operational need.

**Owns:** Score model, scale, maturity, service gaps, website opportunity, automation opportunity, connected-infrastructure opportunity, score history.

**Does not own:** Qualification eligibility or guaranteed sales outcomes.

**Acceptance:** Scoring is explainable, versioned, historically reproducible, and separate from qualification.

# F. Workspaces and Governance

## Module 41 — Data Quality, Freshness and Verification

**Status:** Current

**Outcome:** Detect missing, stale, contradictory, weak, or suspicious lead data.

**Owns:** Quality rules, flags, severity, verification jobs, freshness policies, remediation, closure evidence.

**Does not own:** Silently correcting source data without provenance.

**Acceptance:** Quality flags remain visible until resolved with evidence, accepted as known limitation, or superseded.

## Module 42 — Compliance, Suppression and Channel Eligibility

**Status:** Current

**Outcome:** Prevent prohibited acquisition, retention, export, publication, and contact preparation.

**Owns:** Source policies, ethical restrictions, suppression, deletion requests, retention, consent evidence, channel eligibility, legal holds.

**Does not own:** Sending messages, which belongs to Communicator or another approved destination.

**Acceptance:** Suppressed or prohibited records cannot escape through export, group, publication, API, or retry path.

## Module 43 — Research Jobs and Account Briefs

**Status:** Partial

**Outcome:** Run structured, evidence-grounded research and create useful lead briefs.

**Owns:** Research requests, findings, source citations, prompt-injection controls, summaries, opportunity framing, account briefs, review.

**Does not own:** Autonomous promises, invented facts, or conversation history.

**Acceptance:** Briefs cite Harvester evidence, distinguish fact from inference, and remain useful whether or not Communicator or Core is installed.

## Module 44 — Generated Leads Snapshots

**Status:** Planned

**Outcome:** Freeze the exact accepted, rejected, and review-required output of one completed Harvest Job.

**Owns:** Job result membership, score and qualification at completion, reasons, source contributions, evidence summary, snapshot version.

**Does not own:** Current Master Lead state after the job ends.

**Acceptance:** Historical job results never change silently when the current lead record is later enriched.

## Module 45 — Master Leads Workspace

**Status:** Partial

**Outcome:** Search, filter, sort, compare, select, and manage current lead records across all harvests.

**Owns:** Server-side search, columns, bulk actions, saved views, source coverage, ownership, qualification, score, freshness, publication state.

**Does not own:** Direct destination sending.

**Acceptance:** Operators can manage current leads without relying on an external CRM or Core interface.

## Module 46 — Lead Dossier Workspace

**Status:** Partial

**Outcome:** Present the complete current lead story in one reviewable workspace.

**Owns:** Identity, branches, people, contacts, evidence, provenance, infrastructure, qualification, score, history, quality, compliance, publications, notes.

**Does not own:** Communicator conversation transcript unless retrieved through an optional governed adapter.

**Acceptance:** Facts, detections, inferences, unknowns and historical changes are visually and semantically distinct.

## Module 47 — Human Review Queues

**Status:** Partial

**Outcome:** Centralize decisions that automation must not make silently.

**Owns:** Resolution review, qualification review, data-quality review, attribution review, publication review, assignment, SLA, decisions, rationale.

**Does not own:** Hiding uncertainty behind a confidence number.

**Acceptance:** Every review item has evidence, permitted actions, assignment, decision history, and optimistic-lock protection.

## Module 48 — Daily Selection, Reservation and Ownership

**Status:** Partial

**Outcome:** Allocate qualified leads for controlled work without duplicate effort.

**Owns:** Eligibility, ranking inputs, daily selection, reservations, owner, expiry, release, conflicts, audit.

**Does not own:** Campaign scheduling or conversation follow-up.

**Acceptance:** One lead cannot be silently reserved by competing operators or destinations, and expiry/release behavior is deterministic.

# G. Activation and Optional Integrations

## Module 49 — Saved Filters, Views and Groups

**Status:** Planned

**Outcome:** Create reusable live or fixed selections inside Harvester.

**Owns:** Saved filters, dynamic groups, static groups, ownership, sharing, permissions, membership preview, refresh.

**Does not own:** Frozen destination audiences, which are created by Module 52.

**Acceptance:** Dynamic membership changes with lead data; static membership changes only through an explicit action.

## Module 50 — Export and Report Jobs

**Status:** Partial

**Outcome:** Produce governed files and summaries for approved lead selections.

**Owns:** CSV, JSON, Excel, summary reports, selected IDs, configurable fields, background jobs, expiring links, checksums, audit.

**Does not own:** Bypassing suppression, field permissions, or retention policy.

**Acceptance:** Exports are reproducible, permission-scoped, redacted where required, and traceable to their exact selection and schema.

## Module 51 — Publishing Rules

**Status:** Planned

**Outcome:** Decide which Harvester records may be sent to which destination and when.

**Owns:** Filter criteria, triggers, schedules, approvals, destination, mapping, redaction, deduplication, pause, dry run.

**Does not own:** Destination-owned communication or identity logic.

**Acceptance:** Nothing leaves Harvester merely because a connector exists; every publication is governed by an explicit active rule.

## Module 52 — Frozen Audiences and Payload Profiles

**Status:** Planned

**Outcome:** Freeze the exact records and fields approved for one publication or campaign handoff.

**Owns:** Audience snapshot, Minimal Contact, Standard Lead, Full Lead Context, Raw Observation, Resolved Entity, Custom profile, field allowlist.

**Does not own:** Destination-side group membership after delivery.

**Acceptance:** The published audience and bytes remain auditable even when dynamic filters or lead records later change.

## Module 53 — Direct Communicator Adapter

**Status:** Planned

**Outcome:** Allow Harvester and Communicator to work together without NEWAX Core.

**Owns:** Capability discovery, credentials, organization/person/contact references, lead context, acknowledgement links, bounce/opt-out/invalid feedback, refresh requests.

**Does not own:** Communicator profiles, audiences, campaigns, messages, conversations, sentiment, or follow-up logic.

**Acceptance:** Both products remain independently usable; Communicator maps the payload into its own model and Harvester remains lead-intelligence owner.

## Module 54 — Optional NEWAX Core Adapter

**Status:** Planned

**Outcome:** Publish source-native observations, resolved entities, and approved lead facets to NEWAX Core when a customer enables it.

**Owns:** Raw, resolved-entity and lead-context streams; independent controls; signing; links; backfill; reconciliation; Core capability negotiation.

**Does not own:** Making Core mandatory, sharing tables, or formatting Harvester data directly as Core Registry rows.

**Acceptance:** Core downtime creates a recoverable backlog and never blocks local harvesting, resolution, qualification, or export.

## Module 55 — Generic Customer Destination Adapters

**Status:** Planned

**Outcome:** Publish approved Harvester outputs to customer databases, CRMs, ERPs, APIs, files, queues, and object storage.

**Owns:** Destination adapters, outbound mapping, create/update policies, idempotency, acknowledgements, external references, safe write scopes.

**Does not own:** Unrestricted remote writes or destination business logic inside Harvester.

**Acceptance:** Every destination uses its own mapping, least-privilege credential, capability declaration, and reconciliation path.

## Module 56 — Event Delivery, Feedback and Command Intake

**Status:** Partial

**Outcome:** Provide durable product-to-product and system-to-system operational exchange.

**Owns:** Transactional outbox, delivery attempts, HMAC or asymmetric signing, retries, dead letter, receipts, feedback events, verification and refresh commands.

**Does not own:** Synchronous distributed transactions across products.

**Acceptance:** Events and commands are versioned, idempotent, tenant-scoped, authenticated, replay-safe, and observable.

# H. Operations, Resale and Release

## Module 57 — Operations, Health and Metrics

**Status:** Partial

**Outcome:** Make the product's real operational state visible and recoverable.

**Owns:** Job health, source health, worker health, queue depth, failures, retries, throughput, yield, cost, quota, latency, alerts, runbooks.

**Does not own:** Decorative metrics that cannot drive an action.

**Acceptance:** Operators can identify, diagnose, pause, retry, reconcile, and recover failed or degraded workflows.

## Module 58 — Integration Administration UI

**Status:** Planned

**Outcome:** Manage connections, credentials, mappings, schemas, synchronization, destinations, and optional product adapters safely.

**Owns:** Connections, Secrets, Schemas, Mappings, Sync Runs, Conflicts, Publishing, Communicator, Core, Audit tabs.

**Does not own:** Revealing plaintext secrets or permitting uncontrolled SQL.

**Acceptance:** Administrators can configure and validate integrations without server-file editing, and dangerous actions require reauthentication and approval.

## Module 59 — Multi-Tenant Product Administration

**Status:** Planned

**Outcome:** Operate Harvester as a resellable service across isolated customer tenants.

**Owns:** Tenant lifecycle, quotas, plans, regions, data residency, administrators, suspension, deletion, support access, tenant health.

**Does not own:** Cross-tenant access by ordinary operators.

**Acceptance:** Tenant onboarding, operation, support, export and deletion are isolated, permissioned, auditable, and reversible where policy permits.

## Module 60 — Licensing and Feature Entitlements

**Status:** Planned

**Outcome:** Control product editions and paid capabilities without code forks.

**Owns:** License identity, plan, features, usage limits, connector entitlements, expiry, grace, enforcement, audit, offline validation where required.

**Does not own:** Using licensing to weaken data ownership or trap customer exports.

**Acceptance:** Features fail closed according to entitlement while customer-owned data remains exportable under policy.

## Module 61 — Controlled Branding and Terminology

**Status:** Planned

**Outcome:** Support enterprise branding and bounded white-label requirements without fragmenting the product.

**Owns:** Logo, product name, domain, email identity, terminology labels, approved themes, legal notices, default NEWAX branding.

**Does not own:** Per-customer forks of workflows, schemas, or security controls.

**Acceptance:** Brand changes remain configuration, preserve accessibility, and cannot alter product ownership or compliance semantics.

## Module 62 — Packaging, Deployment, Backup and Restore

**Status:** Planned

**Outcome:** Ship Harvester as dependable customer-owned or managed business infrastructure.

**Owns:** Container images, environment manifests, managed and self-hosted profiles, database provisioning guidance, object storage, backup, restore, disaster recovery.

**Does not own:** Assuming one NEWAX-hosted environment is the only deployment.

**Acceptance:** A customer can deploy, back up, restore, and verify Harvester without installing Core or Communicator.

## Module 63 — Upgrade, Migration and Compatibility Management

**Status:** Planned

**Outcome:** Upgrade application, database, connectors, schemas, mappings, policies, and integrations without losing explainability or recoverability.

**Owns:** Semantic versions, migrations, compatibility matrix, deprecation, rollback, pinned run versions, upgrade reports, data repair.

**Does not own:** Silent reinterpretation of historical evidence or job results.

**Acceptance:** Running jobs remain pinned, historical context remains readable, migrations are tested, and rollback or forward repair is documented.

## Module 64 — Security, Quality and Release Governance

**Status:** Partial

**Outcome:** Release only verified, supportable, secure product versions.

**Owns:** Threat review, source-policy review, secret tests, tenant-isolation tests, migration tests, connector contract tests, accessibility, performance, CI, exact-head verification, release notes.

**Does not own:** Treating a detailed roadmap as proof of implementation.

**Acceptance:** A release is not Complete until the exact commit passes required checks with no unresolved security, data-integrity, compliance, migration, accessibility, or operational issue.

# Delivery order

The module numbers are stable product identities, not a command to implement sixty-four things in one heroic branch.

## Foundation gate

Modules 01–16 establish standalone product access, tenancy, credentials, connectors, mappings and reliable synchronization.

## Harvest gate

Modules 17–32 establish the complete source-to-evidence-to-resolution pipeline.

## Intelligence gate

Modules 33–48 establish lead records, qualification, scoring, research, quality, compliance and operator workflows.

## Activation gate

Modules 49–56 establish governed selection, export, publication and optional integrations.

## Productization gate

Modules 57–64 establish operations, administration, tenancy, licensing, packaging, upgrades and release governance.

# Required architectural tests

The roadmap is not satisfied until tests prove:

1. Harvester starts and performs its core workflow with Core and Communicator absent.
2. Every tenant boundary holds across APIs, workers, files, caches, exports and events.
3. Source-native records are preserved before Harvester mapping or interpretation.
4. Each source schema and mapping version is historically identifiable.
5. No connector writes directly to Harvester business tables.
6. Retries do not duplicate observations, leads, exports or publications.
7. Optional destination failure cannot roll back Harvester data.
8. Direct Harvester-to-Communicator operation works without Core.
9. Core synchronization can be disabled without reducing Harvester functionality.
10. Suppression and policy rules apply to exports, groups, APIs, publications and retries.
11. Historical Harvest Job snapshots remain stable after later enrichment.
12. Exact-head formatting, linting, tests, builds, security and migration checks pass before release.

# Governing rules

1. Harvester is a standalone lead-intelligence product.
2. The application owns its operational database, identifiers and formatting.
3. Every external source and destination uses a credentialed, versioned adapter.
4. Raw evidence is immutable; resolved records are governed views.
5. Facts, detections, inferences, unknowns and conflicts remain distinct.
6. Entity resolution and lead qualification are separate.
7. Qualification and opportunity scoring are separate.
8. Core and Communicator are optional adapters, never hidden dependencies.
9. No shared database tables exist between products.
10. The customer controls what leaves Harvester.
11. The system should do the work; the operator should remain in control.
12. Current, Partial, Planned and Restricted are evidence terms, not marketing adjectives.
