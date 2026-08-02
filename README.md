# NEWAX Lead Harvester

Harvester is a standalone lead-discovery, evidence, verification, resolution, qualification, and research application.

It connects approved public, authorized, customer-owned, and partner sources, preserves source evidence, resolves organizations and people, builds lead profiles, applies qualification policies, and prepares controlled outputs for exports or optional destination systems.

> **Product principle:** Define the market. Let the infrastructure discover, verify, resolve, qualify, and prepare the opportunities while the operator remains in control.

## Product boundary

Harvester is designed as a separate, resellable application with its own:

- Operational database and migrations
- Authentication, authorization, and tenant isolation
- Connection and credential profiles
- Source connectors and source-schema registry
- Mapping and normalization engine
- Raw observations, evidence, and provenance
- Resolved organizations, people, branches, contacts, and relationships
- Lead profiles, qualification, scoring, research, and dossiers
- Synchronization, outbox, retry, reconciliation, and audit
- Backup, restore, export, licensing, and upgrade path

Harvester does not require Communicator or NEWAX Core.

Both are optional integrations:

```text
Harvester only
Sources → Harvester → leads, dossiers, exports, APIs, or customer systems

Harvester + Communicator
Harvester publishing rule → direct adapter → Communicator mapping and normalization

Harvester + NEWAX Core
Optional raw-observation and canonical-entity streams → Core ingestion and identity governance

Full NEWAX deployment
Harvester + optional Core identity and governance + optional Communicator activation
```

## Independent formatting

Harvester formats incoming information according to lead-intelligence needs:

```text
Source-native record
→ raw observation
→ normalized evidence
→ resolution candidate
→ resolved organization, person, branch, contact, or relationship
→ lead profile
→ qualification assessment
→ opportunity score
→ research dossier
```

This remains separate from:

```text
Communicator
Communication profiles, groups, audiences, campaigns, conversations, and engagement

NEWAX Core
Existence, canonical identity, relationships, provenance, and governed source facets
```

A shared source or common event envelope does not create a shared internal database schema.

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
Generate Leads
→ define objective, sector, geography, sources, quantity, and quality rules
→ create Harvest Job
→ monitor source-specific work
→ review frozen Generated Leads
→ search current Master Leads
→ inspect complete Lead Dossier
→ export or publish selected records
```

Principal workspaces:

- Generate Leads
- Harvest Runs
- Generated Leads
- Master Leads
- Lead Dossier
- Resolution Reviews
- Qualification Policies
- Data Quality
- Exports
- Connections and Credentials
- Synchronization
- Communicator integration
- NEWAX Core integration
- Operations and Audit

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

The complete multi-source Harvest Job orchestration, generic connection framework, resale foundation, and optional-product integration architecture remain planned until implemented and verified.

## Automatic publication

When optional destinations are configured, Harvester may publish through durable local outboxes.

### Raw observations

Every accepted source observation may be queued after durable local storage.

### Canonical entities

Every new or materially changed resolved entity may be queued after Harvester resolution and validation.

### Lead context

Customer-selected lead summaries, qualification, score, opportunity signals, research summaries, or dossier references may be published through explicit rules.

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

- [Detailed Product and Architecture Specification](docs/archive/README-detailed-product-specification.md)
- [Main Roadmap](docs/ROADMAP.md)
- [Standalone Product and Integration Framework](docs/architecture/standalone-product-and-integration-framework.md)
- [Standalone Product Roadmap](docs/ROADMAP-STANDALONE-PRODUCT.md)
- [Automatic NEWAX Core Synchronization](docs/architecture/newax-core-automatic-sync.md)
- [Core Synchronization Roadmap](docs/ROADMAP-CORE-SYNC.md)

## Status language

- **Current:** Present in the repository today.
- **Partial:** Some required models or services exist, but the complete workflow is not connected.
- **Correction pending:** Implemented in an open branch or PR but not integrated into `master`.
- **Planned:** Required architecture awaiting implementation and verification.
- **Restricted:** Disabled until access, security, legal, compliance, and operational requirements are approved.

## Governing rules

1. Harvester is a standalone lead-intelligence product.
2. Different source workflows use one orchestration standard.
3. Raw evidence is immutable; resolved records are governed views.
4. Facts, detections, inferences, and unknowns remain distinct.
5. Qualification and opportunity ranking are separate.
6. Source schemas are mapped into Harvester's model, not adopted as Harvester's model.
7. Customer publishing rules determine what leaves Harvester.
8. Communicator and NEWAX Core remain optional adapters.
9. Products never share private tables or database credentials.
10. Secrets are encrypted, write-only, permission-protected, and audited.
11. External failures are expected, visible, and recoverable.
12. A change is complete only after exact-head verification without unresolved issues.

## Locked rule

> Harvester may connect to many sources and destinations, but it always owns how data becomes evidence, a resolved entity, a qualified lead, and a research dossier.
