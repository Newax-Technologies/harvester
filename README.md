# NEWAX Harvester

Harvester is standalone Agency Intelligence Infrastructure.

It converts governed provider and client markets into evidence-backed opportunities, market intelligence, competitor intelligence, and controlled outputs while preserving source truth, tenant isolation, customer ownership, and human control.

> **Product principle:** Define the provider, offering, market, evidence standard, source authority, and output. Let the infrastructure collect, verify, resolve, qualify, assess, and prepare the intelligence while the operator retains control.

## Part of the NEWAX ecosystem

This is one of several connected NEWAX repos. See [`ECOSYSTEM.md`](ECOSYSTEM.md)
for the full picture. Harvester already follows the right pattern — it
talks to Communicator only via REST, never direct DB access — which is the
model every other repo is moving toward via the Module Gateway.

> ⚠️ GitHub Dependabot is reporting 4 high-severity vulnerabilities on this
> repo's default branch as of 2026-10-22. Not yet triaged. See the
> [Security tab](https://github.com/Newax-Technologies/harvester/security/dependabot).

## Product boundary

Harvester is not merely a scraper, crawler, list generator, CRM clone, autonomous outreach engine, or collection of AI prompts.

It is designed as a standalone, resellable application with its own:

- operational database and migrations;
- authentication, authorization, tenancy, client workspaces, and audit;
- providers, brands, business units, offering portfolios, and reusable lead-generation profiles;
- versioned market definitions and Harvest Jobs;
- connections, credential references, source policies, connectors, schemas, mappings, rate limits, pricing, and checkpoints;
- raw observations, evidence artifacts, assertions, claims, coverage, contradictions, and provenance;
- resolved organizations, people, brands, facilities, locations, products, services, technologies, contacts, and relationships;
- lead profiles, qualification, Opportunity Scoring Model v3 assessments, research, and dossiers;
- market and competitor intelligence;
- decisions, review queues, selections, reservations, outputs, and publication rules;
- AI task routing, evaluation, cost accounting, and human-review controls;
- operations, quality debt, feedback, backup, restore, licensing, deployment, and upgrade paths.

Harvester does not require Communicator or NEWAX Core.

```text
Harvester only
Approved Sources → Harvester → intelligence, leads, dossiers, reports, exports, APIs, or customer systems

Harvester + Communicator
Approved Harvester output → Communicator mapping → audiences, campaigns, messages, conversations, and engagement

Harvester + NEWAX Core
Optional source-native observations, resolved entities, and approved Harvester facets
→ Core ingestion, enterprise identity, relationships, provenance governance, and cross-system links
```

No product shares private tables, database-owner credentials, migrations, internal schemas, or runtime availability.

## Authoritative documentation

Read documentation in this order:

1. [Documentation Map](docs/README.md)
2. [Standalone Product Roadmap](docs/ROADMAP.md)
3. [Agency Intelligence Re-baseline](docs/architecture/agency-intelligence-rebaseline.md)
4. [Intelligence Operating Model](docs/architecture/harvester-intelligence-operating-model.md)
5. [Architecture Index](docs/architecture/README.md)
6. [Services and Opportunity Model](docs/SERVICES.md)
7. [Taxonomy Index](docs/taxonomy/README.md)
8. [Source Index](docs/sources/README.md)
9. [Delivery Index](docs/delivery/README.md)
10. [Agency Intelligence Implementation Sequence](docs/delivery/agency-intelligence-implementation-sequence.md)

The re-baseline preserves the existing 64-module roadmap. It does not create another module count.

## Eight-plane architecture

```text
Control
→ Acquisition
→ Evidence
→ Resolution
→ Intelligence
→ Decision
→ Activation
→ Operations and Learning
```

### Control

Tenants, workspaces, agencies, clients, providers, offerings, markets, users, permissions, entitlements, budgets, policies, and approved versions.

### Acquisition

Connections, credentials, connectors, source plans, source runs, stages, schemas, mappings, checkpoints, rates, quotas, costs, and source-native capture.

### Evidence

Raw observations, snapshots, documents, excerpts, assertions, claims, coverage, contradictions, freshness, source reliability, retention, and provenance.

### Resolution

Organizations, people, brands, business units, facilities, locations, products, services, technologies, contacts, relationships, candidates, conflicts, decisions, and reversals.

### Intelligence

Lead profiles, signals, pains, needs, qualification, Opportunity Scoring Model v3, dossiers, markets, competitors, trends, analyses, and recommendations.

### Decision

Review queues, assignments, ranking, selections, reservations, approvals, frozen snapshots, and decision records.

### Activation

Exports, reports, APIs, webhooks, CRMs, warehouses, advertising and analytics handoffs, Communicator, Core, and customer destinations.

### Operations and Learning

Health, metrics, costs, quality debt, evaluation, feedback, drift, rollout, rollback, backup, restore, release, and upgrade governance.

## Strengthened intelligence flow

```text
Tenant and client workspace
→ provider organization and active offering
→ versioned market definition
→ approved source and output policies
→ Harvest Job and source plans
→ source-native observations
→ evidence artifacts, assertions, claims, and coverage
→ local resolution candidates and decisions
→ resolved entities and relationships
→ client- and market-specific lead profile
→ qualification assessment
→ Opportunity Scoring Model v3 assessment
→ research, market, or competitor intelligence product
→ human or policy decision
→ frozen selection and controlled output
→ outcome feedback
→ governed learning
```

## Decision separation

```text
Entity resolution
≠ Qualification
≠ Opportunity scoring
≠ Selection
≠ Publication approval
≠ Contact eligibility
≠ Communication consent
```

A score may prioritize review. It cannot prove identity, grant consent, authorize publication, or promise a commercial outcome.

## Universal core and sector packs

Harvester uses a universal entity and evidence core plus independently versioned sector packs.

The repository currently documents 16 sectors, 1,586 product and service domains, 519 business activities, and corresponding keyword, signal, role, source, exclusion, and evidence-control profiles.

Healthcare and Education are the first required operational sector packs. Their runtime model includes client types, facilities, professionals, buyers, customers, products, services, projects, activities, employment and procurement models, pains, needs, signals, lead types, data classes, integrations, compliance rules, and conditional input questions.

The documentation datasets are not runtime completion.

## Source governance

A connector is not permission. Public visibility is not universal reuse authority.

Every source execution must resolve:

```text
Tenant and workspace
→ purpose
→ source and access class
→ active policy version
→ credential and scope
→ data class, region, retention, and redistribution
→ rate and price versions
→ budget and approval
→ execution
```

Stealth browser automation, account farms, fingerprint evasion, CAPTCHA solving, and access-control circumvention are not supported enterprise source capabilities.

## AI boundary

AI may assist extraction, classification, research, synthesis, translation, review, and drafting.

AI does not own:

- authentication or authorization;
- tenant isolation;
- source rights or lawful purpose;
- consent, suppression, deletion, or retention;
- billing and quotas;
- exact identifiers;
- workflow authority;
- export or publication approval;
- audit or cryptography.

All provider calls must ultimately pass through the planned AI gateway with task contracts, data classification, redaction, structured-output validation, evidence grounding, evaluation, cost control, and human-review policies.

## Current implementation

The current repository provides substantial backend foundations, including:

- source runs and raw source records;
- website snapshots;
- canonical institutions, branches, contacts, and people candidates;
- field provenance and resolution review;
- sector classification;
- qualification assessments;
- signals and research findings;
- lead profiles and score history;
- daily selection and reservations;
- suppression, deletion, and data-quality controls;
- exports and event outbox;
- account briefs, outreach drafts, outcomes, FastAPI routes, CLI workflows, and a partial React frontend.

The following remain planned or partial until implemented and verified:

- production multi-tenancy and client isolation;
- production authentication and relationship-aware authorization;
- provider portfolios, active offering versions, reusable profiles, and complete market definitions;
- source-policy execution gates, credential vault, generic connector runtime, schemas, mappings, pricing, and quotas;
- multi-source Harvest Job orchestration;
- universal entities and full evidence graph;
- runtime sector packs;
- Opportunity Scoring Model v3 runtime;
- AI model gateway and evaluation;
- market and competitor intelligence;
- complete frontend configuration and operational coverage;
- resale, licensing, dedicated tenant cells, packaging, backup, restore, and enterprise release hardening.

## Immediate correction gate

Before broad expansion, the delivery sequence requires:

1. exact institution linkage for raw page snapshots;
2. correction of detection semantics so non-detection is not confirmed absence;
3. recomputation and trust marking of affected profiles;
4. production disabling of contested professional-network automation;
5. production authentication and tenant isolation;
6. source-policy execution gating;
7. object-storage evidence and retention controls.

See [Agency Intelligence Implementation Sequence](docs/delivery/agency-intelligence-implementation-sequence.md).

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

Current CLI examples:

```bash
lead-harvester run --config job.yaml
lead-harvester import-authorized ...
lead-harvester qualify-leads ...
lead-harvester select-daily-leads ...
lead-harvester verify-data-quality ...
lead-harvester export-leads ...
lead-harvester process-outbox ...
```

Verification:

```bash
ruff check .
ruff format --check .
pytest -q
```

Database changes must validate the full Alembic chain against PostgreSQL. Frontend changes must pass applicable type, lint, format, unit, build, accessibility, and end-to-end checks.

## Status language

- **Current:** implemented and verified in the referenced branch.
- **Partial:** useful foundations exist but the complete governed workflow is not connected.
- **Planned:** documented architecture awaiting implementation and verification.
- **Restricted:** disabled until access, legal, privacy, security, commercial, and operational approval exists.
- **Correction required:** current behavior or derived data is untrusted until the specified remediation is integrated and executed.

## Governing rules

1. Harvester is standalone Agency Intelligence Infrastructure.
2. A versioned provider, offering, market, source, evidence, qualification, scoring, and output definition exists before production collection.
3. Source-native observations and evidence are immutable.
4. Every material claim remains traceable to exact evidence.
5. Non-detection is not confirmed absence.
6. Resolution, qualification, scoring, selection, publication, and contact authority remain separate.
7. Confidence is multidimensional.
8. High-impact or ambiguous automation requires review.
9. Client-private data never becomes another client's intelligence input.
10. Source schemas map into Harvester contracts rather than becoming its internal model.
11. Customer publishing rules determine what leaves Harvester.
12. Core and Communicator remain optional adapters.
13. Secrets are write-only, encrypted, permission-protected, and audited.
14. Outcome feedback creates new evidence and never rewrites source history.
15. Production models and policies change only through versioned evaluation, approval, rollout, and rollback.
16. External failures are visible and recoverable.
17. The system should perform repeatable work while the operator controls objectives, exceptions, and action.
18. A change is complete only after exact-head verification without unresolved internal issues.

> **Locked rule:** Harvester converts governed commercial definitions into evidence-backed intelligence. It preserves source truth, explains material decisions, keeps automation within authority, and leaves customers in control of their data, infrastructure, and next action.
