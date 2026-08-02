# NEWAX Lead Harvester

Harvester is a standalone lead-discovery, evidence, verification, resolution, qualification, opportunity-intelligence, and research application.

It connects approved public, authorized, customer-owned, and partner sources, preserves source evidence, resolves organizations and people, builds lead profiles, applies qualification and opportunity policies, and prepares controlled outputs for exports or optional destination systems.

> **Product principle:** Define the market. Let the infrastructure discover, verify, resolve, qualify, assess, and prepare the opportunities while the operator remains in control.

The [Harvester Intelligence Operating Model](docs/architecture/harvester-intelligence-operating-model.md) defines the strengthened domain objects, evidence graph, decision contracts, confidence model, bounded automation, learning loop, operational economics, and architectural tests used across the existing 64-module roadmap.

The [NEWAX Harvester Opportunity Scoring Model v3](docs/architecture/opportunity-scoring-model-v3.md) defines how confirmed infrastructure absence, severe weakness, strategic fit, account value, buying timing, pursuit readiness, evidence quality, identity confidence, coverage, and risk must combine into an explainable opportunity decision.

## Product boundary

Harvester is designed as a separate, resellable application with its own:

- Operational database and migrations
- Authentication, authorization, and tenant isolation
- Versioned market definitions and Harvest Jobs
- Connection and credential profiles
- Source connectors and source-schema registry
- Mapping and normalization engine
- Raw observations, evidence artifacts, assertions, coverage, and provenance
- Resolved organizations, people, branches, contacts, and relationships
- Lead profiles, qualification, opportunity assessment, research, and dossiers
- Decision records, review queues, snapshots, selections, and reservations
- Synchronization, outbox, retry, reconciliation, feedback, and audit
- Model and policy versions, operational metrics, quality debt, and recovery
- Backup, restore, export, licensing, and upgrade path

Harvester does not require Communicator or NEWAX Core.

Both are optional integrations:

```text
Harvester only
Sources → Harvester → leads, dossiers, exports, APIs, or customer systems

Harvester + Communicator
Harvester publishing rule → direct adapter → Communicator mapping and normalization

Harvester + NEWAX Core
Optional raw-observation, resolved-entity, and approved lead-context streams
→ Core ingestion, canonical identity, provenance, and governance

Full NEWAX deployment
Harvester
├── optional direct Communicator adapter
├── optional NEWAX Core adapter
└── optional customer or partner destinations
```

## Strengthened intelligence flow

Harvester formats incoming information according to lead-intelligence needs while keeping every material decision explainable:

```text
Versioned market definition
→ Harvest Job and source plans
→ source-native observations
→ evidence artifacts and assertions
→ coverage and detection states
→ local resolution candidates and decisions
→ resolved organization, person, branch, contact, or relationship
→ lead profile
→ qualification assessment
→ opportunity assessment and service-gap hypotheses
→ research dossier
→ human or automated decision record
→ frozen selection and publication package
→ outcome feedback
→ governed learning
```

This remains separate from:

```text
Communicator
Communication profiles, groups, audiences, campaigns, conversations, and engagement

NEWAX Core
Existence, canonical identity, relationships, provenance, and governed source facets
```

A shared source or common event envelope does not create a shared internal database schema.

## Decision separation

Harvester keeps these decisions independent:

```text
Entity resolution
≠ qualification
≠ opportunity scoring
≠ selection
≠ publication approval
≠ communication consent
```

A score may prioritize review. It does not prove identity, grant consent, authorize publication, or guarantee a sales outcome.

## Connections and credentials

Harvester is planned to support credentialed adapters for:

- PostgreSQL
- MySQL
- MariaDB
- Microsoft SQL Server
- SQLite for bounded local use
- MongoDB
- Supabase
- Neon
- Amazon RDS-compatible relational services
- Google Cloud SQL-compatible relational services
- Azure SQL
- REST and GraphQL APIs
- CSV and JSON imports
- Webhooks
- Message queues
- Object storage
- Communicator
- NEWAX Core
- Approved customer and partner systems

"Any database" is implemented through versioned adapters with declared capabilities, least-privilege credentials, schema discovery, mapping, checkpoints, validation, and audit. It is not unrestricted SQL access to whatever server responds politely.

Every source is mapped and normalized into Harvester's own evidence and lead model. Every destination receives only customer-approved data through publishing rules and payload profiles.

## Core product journey

```text
Define Market
→ define objective, sectors, organization types, geography, quality, budget, and source policy
→ create Harvest Job
→ monitor source plans, coverage, yield, cost, and exceptions
→ review frozen Generated Leads
→ search current Master Leads
→ inspect complete Lead Dossier
→ select, reserve, export, or publish approved records
→ receive outcome feedback without rewriting source evidence
```

Principal workspaces:

- Define Market
- Generate Leads
- Harvest Runs
- Generated Leads
- Master Leads
- Lead Dossier
- Resolution Reviews
- Qualification Policies
- Opportunity Models
- Data Quality and Quality Debt
- Exports
- Connections and Credentials
- Synchronization
- Communicator integration
- NEWAX Core integration
- Operations, Economics, Learning, and Audit

## Current implementation

The repository currently provides substantial backend foundations, including:

- Source runs and raw source records
- Website snapshots
- Canonical institutions, branches, contacts, and people candidates
- Provenance and resolution review
- Sector classification
- Qualification assessments
- Signals and research findings
- Lead profiles and score history
- Daily selection and reservations
- Suppression and data-quality controls
- Exports
- Event outbox
- Account briefs, outreach drafts, and outcomes
- FastAPI routes and CLI workflows

The complete market-definition engine, multi-source Harvest Job orchestration, evidence graph, decision-contract model, Opportunity Scoring Model v3 runtime, generic connection framework, governed learning loop, resale foundation, and optional-product integration architecture remain planned until implemented and verified.

## Automatic publication

When optional destinations are configured, Harvester may publish through durable local outboxes.

### Raw observations

Every accepted source observation may be queued after durable local storage.

### Resolved entities

Every new or materially changed Harvester-resolved entity may be queued after local resolution and validation.

### Lead context

Customer-selected lead summaries, qualification, opportunity assessment, research summaries, or dossier references may be published through explicit rules.

Optional destination failure never rolls back a committed Harvester observation or lead update.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

Current CLI examples include:

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

Database changes must validate the full Alembic migration chain against PostgreSQL. Frontend changes must pass relevant type, lint, format, unit, build, accessibility, and end-to-end checks.

## Documentation

- [Documentation Authority Map](docs/README.md)
- [Authoritative Roadmap](docs/ROADMAP.md)
- [Harvester Intelligence Operating Model](docs/architecture/harvester-intelligence-operating-model.md)
- [NEWAX Harvester Opportunity Scoring Model v3](docs/architecture/opportunity-scoring-model-v3.md)
- [Standalone Product and Integration Framework](docs/architecture/standalone-product-and-integration-framework.md)
- [Automatic NEWAX Core Synchronization](docs/architecture/newax-core-automatic-sync.md)

Previous versions remain available through Git history and pull-request history instead of duplicate archive documents.

## Status language

- **Current:** Present in the repository today.
- **Partial:** Some required models or services exist, but the complete workflow is not connected.
- **Correction pending:** Implemented in an open branch or PR but not integrated into `master`.
- **Planned:** Required architecture awaiting implementation and verification.
- **Restricted:** Disabled until access, security, legal, compliance, and operational requirements are approved.

## Governing rules

1. Harvester is standalone lead-intelligence infrastructure.
2. A versioned market definition exists before collection begins.
3. Different source workflows use one orchestration standard.
4. Raw observations and evidence artifacts are immutable.
5. Every material claim remains traceable to evidence.
6. Facts, derived values, model inferences, operator assessments, unknowns, and conflicts remain distinct.
7. Non-detection is not confirmed absence; coverage and failure states remain explicit.
8. Entity resolution, qualification, opportunity scoring, selection, and publication are separate.
9. Confidence remains multidimensional even when a composite rank is calculated.
10. Source schemas are mapped into Harvester's model, not adopted as Harvester's model.
11. Customer publishing rules determine what leaves Harvester.
12. Communicator and NEWAX Core remain optional adapters.
13. Products never share private tables or database credentials.
14. Secrets are encrypted, write-only, permission-protected, and audited.
15. Outcome feedback creates new evidence and never rewrites source history.
16. Production policies and models change only through versioned approval and rollback controls.
17. External failures are expected, visible, and recoverable.
18. A change is complete only after exact-head verification without unresolved issues.

## Locked rule

> Harvester converts a governed market definition into evidence-backed opportunity intelligence. It preserves source truth, explains every material decision, keeps automation within authority, and leaves the customer in control of the data, infrastructure, and next action.
