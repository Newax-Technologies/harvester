# Agency Intelligence Implementation Sequence

Status: **Authoritative delivery sequence for the re-baseline**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Not started by this document**

## 1. Purpose

This document converts the Agency Intelligence re-baseline into a dependency-ordered engineering sequence within the existing 64-module roadmap.

It does not create additional top-level modules. Every slice maps to existing module ownership and must update the authoritative roadmap status when integrated and verified.

## 2. Delivery principles

1. Correct known data-integrity defects before building on affected outputs.
2. Establish tenant, authentication, authorization, credentials, and source-policy boundaries before multi-client operation.
3. Preserve current working paths through expand, migrate, compare, and contract phases.
4. Keep source, sector, AI, persistence, presentation, and destination changes isolated.
5. Use small complete pull requests with one migration or contract concern where practical.
6. Documentation status changes only after exact-head verification.
7. No roadmap or architecture document proves runtime completion.

## 3. Gate 0 — Data integrity and restricted-source correction

### Slice 0.1 — Raw page snapshot ownership

Deliver:

- `normalized_domain`, `raw_source_record_id`, and `institution_id` linkage;
- migration and backfill using source run plus normalized domain;
- institution-scoped snapshot reads;
- regression tests for multi-domain runs;
- recomputation command and progress cursor;
- trust marking for pre-correction website and service-gap scores.

Maps to Modules 29–31, 38, 40, and 64.

### Slice 0.2 — Detection-state correction

Deliver:

- explicit PRESENT, ABSENT_CONFIRMED, NOT_DETECTED, NOT_INSPECTED or NOT_CRAWLED, INSPECTION_FAILED or CRAWL_FAILED, UNKNOWN, and NOT_APPLICABLE states;
- no full absence credit from static-crawler silence;
- persisted website and technology detection state;
- score recomputation and API exposure;
- tests across the complete state space.

Maps to Modules 31, 38, 40, 41, and 64.

### Slice 0.3 — Restricted professional-network shutdown

Deliver:

- feature-disabled production profile for account automation, stealth browser, CAPTCHA solving, and fingerprint evasion;
- removal from supported product claims and default dependencies;
- migration or quarantine plan for existing acquired data;
- approved replacement access paths;
- security, legal, and source-policy review.

Maps to Modules 11, 24, 28, 42, and 64.

### Gate 0 exit criteria

- affected tests and migrations pass;
- historical affected scores are identifiable;
- recomputation completes or produces a durable remediation backlog;
- restricted source paths cannot activate;
- no unresolved data-integrity issue remains in the affected scoring path.

## 4. Gate 1 — Standalone enterprise foundation

### Slice 1.1 — Tenant and workspace schema

Deliver:

- tenant, workspace, agency or enterprise profile, client workspace, and membership records;
- tenant and workspace keys on controlled business records;
- scoped repositories and query helpers;
- tenant-aware queues, object paths, caches, search routing, exports, events, and audit;
- migration defaults and backfill for the current single-tenant installation.

Maps to Modules 03, 06, 08, 59, and 64.

### Slice 1.2 — Production authentication

Deliver:

- removal of hard-coded production tokens;
- secure user and service authentication;
- session lifecycle, expiry, revocation, and reauthentication;
- development bypass restricted to explicit local environments;
- SSO-ready identity boundary.

Maps to Module 04.

### Slice 1.3 — Authorization registry

Deliver:

- explicit permissions;
- role and relationship-aware checks;
- deny-by-default APIs, workers, exports, files, and administration;
- denied-action audit;
- permission-aware frontend navigation.

Maps to Module 05.

### Slice 1.4 — Configuration and entitlements

Deliver:

- tenant and deployment configuration versions;
- feature and connector entitlements;
- environment profiles;
- safe defaults and configuration history;
- no plaintext secrets in configuration.

Maps to Modules 07, 60, and 61.

### Gate 1 exit criteria

- tenant boundary tests pass across every storage and execution path;
- Harvester operates independently from Core and Communicator;
- mock authentication is unavailable in production;
- every protected action maps to a permission;
- current single-tenant data is migrated and accessible only in its assigned workspace.

## 5. Gate 2 — Connections, credentials, source governance, and economics

### Slice 2.1 — Credential vault abstraction

Deliver:

- write-only credential submission;
- vault references and fingerprints;
- validation, rotation, retirement, and revocation;
- per-tenant and per-workspace scope;
- no plaintext retrieval.

Maps to Module 09.

### Slice 2.2 — Connection profiles

Deliver:

- source and destination connection records;
- endpoint metadata, region, purpose, access mode, capability, and health;
- least-privilege validation;
- administration API and UI foundations.

Maps to Module 10.

### Slice 2.3 — Connector contract

Deliver:

- connector definition and version registry;
- explicit capabilities;
- schema discovery, validation, state, health, cost estimation, deletion, and webhook interfaces;
- source-specific adapters behind the shared contract;
- contract tests.

Maps to Module 11.

### Slice 2.4 — Source, policy, rate, and price registries

Deliver:

- source definitions and access classes;
- versioned purpose permissions and restrictions;
- terms, scopes, regions, personal-data classes, retention, caching, redistribution, and deletion rules;
- rate-limit and pricing versions;
- verified-at and reviewed-by metadata.

Maps to Modules 07, 11, 42, 57, and 60.

### Slice 2.5 — Connector execution gate

Deliver:

- purpose, source, policy, credential, consent, region, retention, output, quota, cost, and approval checks;
- approved, review-required, and blocked decisions;
- fail-closed runtime behavior;
- policy decision records.

Maps to Modules 15, 20, 42, 47, and 64.

### Gate 2 exit criteria

- no connector executes without active policy and purpose;
- credentials cannot cross tenant or workspace boundaries;
- rate and cost state is observable;
- unsupported capabilities fail explicitly;
- source terms and policy changes can suspend future work without corrupting history.

## 6. Gate 3 — Provider portfolio and governed market configuration

### Slice 3.1 — Provider and business-unit runtime

Deliver:

- provider organizations;
- brands and business units;
- offering portfolios;
- provider and unit ownership;
- status and lifecycle.

Maps to Modules 06, 07, 33, and 59.

### Slice 3.2 — Versioned offerings

Deliver:

- products, services, projects, subscriptions, referrals, employment, partnerships, and other offer types;
- customer markets, delivery models, pricing models, capacity, geography, qualification, exclusions, and compliance;
- approval and operational status separation.

Maps to Modules 07, 39, and 40.

### Slice 3.3 — Lead-generation profiles

Deliver:

- reusable profile identity and versions;
- selected offerings, markets, sectors, domains, activities, signals, sources, budgets, schedules, outputs, and policies;
- profile overlap warnings;
- independent approval and activation.

Maps to Modules 17, 39, 40, 49, and 59.

### Slice 3.4 — Market definitions and output specifications

Deliver:

- versioned market definitions;
- bounded lead target, quality mode, exclusions, stopping rules, and generation mode;
- output type, count, fields, evidence depth, review, destination, schedule, and retention;
- immutable activation snapshot.

Maps to Modules 17, 44, 49–52.

### Gate 3 exit criteria

- no production job can run without active offering and approved market definition;
- editing active configuration creates a new version;
- completed jobs can retain exact versions;
- tenant overrides cannot mutate canonical taxonomy or sector records;
- requested quantity cannot lower qualification or evidence thresholds silently.

## 7. Gate 4 — Multi-source Harvest Job orchestration

### Slice 4.1 — Harvest Job and Source Plan

Deliver:

- parent job contract;
- pinned market, offering, taxonomy, source, connector, mapping, policy, evidence, qualification, scoring, and output versions;
- source plans with expected cost, quota, priority, coverage, and stop conditions.

Maps to Modules 17 and 19.

### Slice 4.2 — Source-run stage engine

Deliver:

- generic stages, cursors, checkpoints, leases, heartbeats, counters, warnings, and failure classes;
- generic frontend progress contract;
- versioned connector and workflow identity.

Maps to Modules 19 and 20.

### Slice 4.3 — Parent orchestrator

Deliver:

- multi-source execution;
- partial success;
- pause, resume, cancel, retry, and stopping rules;
- acceptance accounting;
- cost, quota, yield, and coverage rollup;
- durable completion.

Maps to Modules 18 and 20.

### Slice 4.4 — Import preview and quarantine

Deliver:

- source sample;
- schema and mapping preview;
- validation, duplicate hints, create/update/skip/quarantine actions;
- operator approval and rejection report.

Maps to Modules 12–14.

### Gate 4 exit criteria

- one source failure does not erase another source's accepted results;
- jobs resume from durable checkpoints;
- retries do not duplicate observations;
- completed job configuration is reproducible;
- frontend state derives from backend stage records.

## 8. Gate 5 — Universal entity and evidence graph

### Slice 5.1 — Object-storage evidence artifacts

Deliver:

- object storage for HTML, documents, images, and large payloads;
- artifact metadata, hashes, access classes, retention, and locators;
- bounded migration of current page snapshots;
- signed or permission-checked access.

Maps to Modules 29, 30, 42, and 62.

### Slice 5.2 — Evidence assertions, excerpts, claims, coverage, and contradictions

Deliver:

- exact evidence excerpts and locators;
- assertion kinds;
- claim-to-evidence links;
- corroboration and duplicate-origin controls;
- coverage and contradiction records;
- fact, calculation, inference, operator assessment, unknown, and conflict separation.

Maps to Modules 30, 31, 37, 41, 43, and 46.

### Slice 5.3 — Universal entity registry

Deliver:

- organizations, people, brands, business units, facilities, locations, products, services, technologies, roles, publications, events, markets, and relationships;
- identifiers, names, aliases, dates, confidence, and sensitivity;
- stable local IDs and optional external links.

Maps to Modules 32–34.

### Slice 5.4 — Resolution migration

Deliver:

- backfill from institutions, branches, contacts, and people candidates;
- dual-write and comparison;
- reversible decisions;
- conflict workbench updates;
- compatibility reads until cutover.

Maps to Modules 32–34, 46, 47, and 63.

### Gate 5 exit criteria

- every material current value can trace to exact evidence;
- contradictory sources remain visible;
- one entity can have different workspace-specific lead profiles;
- identity merges are reversible;
- current APIs continue through the compatibility period;
- object retention and deletion follow source and tenant policy.

## 9. Gate 6 — Runtime sector packs

### Slice 6.1 — Sector-pack kernel

Deliver:

- pack and version records;
- canonical registry references;
- tenant overlays;
- activation, rollback, and affected-market preview;
- independent pack release manifests.

Maps to Modules 07, 17, 39, 40, 59, and 63.

### Slice 6.2 — Conditional input and commercial roles

Deliver:

- versioned conditional questions;
- provider, customer, beneficiary, buyer, approver, user, regulator, referrer, partner, supplier, employer, and candidate roles;
- controlled response schemas and validation.

Maps to Modules 17, 34, and 39.

### Slice 6.3 — Healthcare pack

Deliver:

- runtime client, facility, professional, buyer, service, product, project, pain, need, signal, lead, data, integration, and compliance records;
- patient-level marketing restrictions;
- clinical integration boundary;
- benchmark and policy tests.

Maps to Modules 17, 34–43, and 64.

### Slice 6.4 — Education pack

Deliver:

- runtime institution, learner-market, buyer, program, service, project, pain, need, signal, lead, data, integration, and compliance records;
- student and minor restrictions;
- benchmark and policy tests.

Maps to Modules 17, 34–43, and 64.

### Gate 6 exit criteria

- pack changes cannot alter unrelated sectors;
- activated versions are immutable;
- healthcare and education prohibited-data tests pass;
- completed jobs retain exact pack and overlay versions;
- keywords remain evidence discovery inputs rather than qualification or scoring authority.

## 10. Gate 7 — Opportunity intelligence runtime

### Slice 7.1 — Lead profile by workspace and market

Deliver:

- entity identity separated from client-specific commercial projections;
- profile revision, quality, compliance, current summary, contacts, and history;
- workspace and market context.

Maps to Module 36.

### Slice 7.2 — Versioned qualification policy

Deliver:

- required, weighted, disqualifying, and review rules;
- evidence snapshots;
- policy versions;
- qualified, not qualified, review required, insufficient evidence, and policy blocked outcomes.

Maps to Module 39.

### Slice 7.3 — Opportunity Scoring Model v3

Deliver:

- eligibility gates;
- relevant capability condition assessments;
- opportunity value;
- pursuit readiness;
- coverage and confidence;
- risk and recommended action;
- evidence and explanation per subfactor;
- model versions and historical snapshots.

Maps to Module 40.

### Slice 7.4 — Dossier and review workspaces

Deliver:

- facts, inferences, unknowns, conflicts, source coverage, identity, people, contacts, signals, opportunities, score, quality, compliance, and citations;
- assignment, SLA, decisions, rationale, and optimistic concurrency.

Maps to Modules 43, 46, and 47.

### Gate 7 exit criteria

- scores cannot override eligibility or compliance gates;
- opportunity, readiness, confidence, coverage, and risk remain separate;
- every point and recommendation is explainable;
- stale or contradictory evidence affects the appropriate dimensions;
- high-impact ambiguity enters review.

## 11. Gate 8 — AI gateway

### Slice 8.1 — Provider, model, task, prompt, and routing registries

Deliver the versioned control records and tenant policies defined by the AI architecture.

### Slice 8.2 — Gateway execution and structured output

Deliver data classification, redaction, provider routing, cost and latency limits, schema validation, evidence checks, retries, fallback, and execution records.

### Slice 8.3 — Evaluation and rollout

Deliver benchmark datasets, metrics, shadow execution, approval, bounded rollout, drift monitoring, and rollback.

### Slice 8.4 — Legacy ResearchBrain migration

Deliver source restrictions, task separation, legacy metadata backfill, and removal of direct provider SDK calls from business modules.

Maps to Modules 37, 43, 57, 60, 63, and 64.

### Gate 8 exit criteria

- no provider call bypasses the gateway;
- invalid outputs are not accepted silently;
- evidence-grounded outputs cite accessible supporting records;
- provider and model changes require evaluation and approval;
- cost is attributable by tenant, client, task, and output.

## 12. Gate 9 — Agency, market, and competitor intelligence

### Slice 9.1 — Agency and client runtime

Deliver agency profiles, client workspaces, service catalogues, templates, teams, and privacy classifications.

### Slice 9.2 — Research projects and market objects

Deliver projects, markets, categories, business questions, methods, budgets, and decisions supported.

### Slice 9.3 — Competitor intelligence

Deliver competitor profiles, observed products, services, prices, positioning, campaigns, technology, reviews, and change events.

### Slice 9.4 — Intelligence products and case studies

Deliver reports, maps, dossiers, briefs, battlecards, methodologies, assumptions, citations, review, and correlation or causation classification.

Maps to Modules 06, 36–47, 49–52, 57, 59, and 61.

### Gate 9 exit criteria

- client-private data cannot cross workspaces;
- public reference reuse follows source rights;
- market and competitor claims are dated and evidenced;
- reports are reproducible from pinned inputs;
- case studies do not overstate causal impact.

## 13. Gate 10 — Activation and integration administration

### Slice 10.1 — Saved views and frozen selections

Deliver live views, static selections, generated-lead snapshots, frozen audiences, and revisions.

### Slice 10.2 — Governed exports and reports

Deliver background jobs, field policies, evidence depth, redaction, checksums, expiring links, and audit.

### Slice 10.3 — Publishing rules and destination adapters

Deliver customer-controlled rules, mappings, payload profiles, CRM, warehouse, webhook, file, Communicator, Core, and generic destination adapters.

### Slice 10.4 — Reconciliation and feedback

Deliver delivery receipts, idempotency, dead letter, replay, conflict records, backfill, repair, and outcome commands.

Maps to Modules 49–58.

### Gate 10 exit criteria

- nothing leaves Harvester because a connector merely exists;
- suppression and policy are rechecked at publication;
- destination failure never rolls back local data;
- retries preserve event identity and payload meaning;
- administration never reveals plaintext secrets.

## 14. Gate 11 — Productization and release

Deliver:

- shared SaaS, regulated cell, and dedicated deployment profiles;
- packaging, object storage, search, backup, restore, and disaster recovery;
- customer-managed keys where required;
- licensing and feature entitlements;
- controlled branding;
- upgrade compatibility and rollback;
- observability, runbooks, service levels, and support access;
- security, accessibility, performance, migration, and tenant-isolation verification.

Maps to Modules 57–64.

### Gate 11 exit criteria

- backup and restore exercises pass;
- regional and tenant policies hold;
- release artifacts and migrations are reproducible;
- accessibility and responsive checks pass;
- exact release commit passes all required checks;
- unresolved Snyk or external integration errors are reported separately rather than hidden behind successful internal CI.

## 15. Pull-request sequencing rules

Each implementation PR declares:

```text
Owning module or modules
Affected public contracts
Schema and migration impact
Tenant and workspace impact
Source-policy impact
Sector-pack impact
AI impact
Frontend impact
Destination impact
Compatibility and rollback
Tests executed
Exact head SHA
```

Stacked PRs must state their dependency chain and must not be merged out of order.

Stale open PRs are re-based or reimplemented against current `master`. They are not merged because their titles sound useful.

## 16. Documentation update rule

When a slice merges:

1. update the owning module status in `docs/ROADMAP.md`;
2. update affected architecture and delivery documents;
3. record migrations, public contracts, and compatibility;
4. remove superseded planning language only after the runtime is verified;
5. keep historical design changes in Git history rather than duplicate archive documents.

## 17. Locked sequence

```text
Correct integrity
→ establish tenancy and security
→ govern sources and credentials
→ define providers and markets
→ orchestrate collection
→ build universal evidence and identity
→ activate sector packs
→ implement opportunity intelligence
→ govern AI
→ add agency, market, and competitor products
→ activate destinations
→ productize and release
```

Skipping an earlier gate requires a written architecture exception, risk owner, compensating controls, and explicit approval.
