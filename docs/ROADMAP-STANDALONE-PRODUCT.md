# Harvester Standalone Product Roadmap

Status: **Planned**

This roadmap converts Harvester from a NEWAX-specific lead service into a standalone, resellable lead-intelligence application while preserving optional integrations with Communicator and NEWAX Core.

The roadmap supplements `docs/ROADMAP.md`. It does not change the existing count of 64 top-level product modules. These are bounded submodules and delivery slices.

## Product outcome

Harvester must be able to:

- Operate without NEWAX Core or Communicator.
- Connect to approved databases, APIs, files, queues, and object stores through credentialed adapters.
- Preserve source-native data.
- Map and normalize each source into Harvester's own observation, evidence, resolution, qualification, and lead model.
- Publish customer-selected outputs to Communicator, NEWAX Core, customer systems, or exports.
- Support multi-tenant resale, controlled white-labeling, licensing, upgrades, backup, restore, and audit.

## Delivery principles

1. Product autonomy before cross-product convenience.
2. Optional integrations never participate in Harvester's local transaction.
3. Each connector declares capabilities and limitations.
4. Every mapping and normalization version is auditable.
5. Secrets remain write-only.
6. External writes are disabled by default.
7. Direct database access never bypasses Harvester services.
8. Core and Communicator adapters are ordinary optional adapters.
9. No shared database tables between products.
10. Implementation status is not inferred from documentation.

# Phase HSP-0: Architecture and product boundary

Deliver:

- Standalone-product architecture decision.
- Product ownership matrix.
- Harvester, Communicator, and Core data-format boundaries.
- Optional integration contract.
- Connector capability vocabulary.
- Connection access modes.
- Cross-product event envelope.
- Tenant and licensing assumptions.

Acceptance:

- Harvester core workflows have no runtime dependency on Core or Communicator.
- Current direct assumptions are identified and assigned migration tasks.
- Existing NEWAX Core synchronization remains disabled unless configured.

# Phase HSP-1: Connection and credential foundation

Deliver:

- `ConnectionProfile`.
- `CredentialReference`.
- Connector registry.
- Environment profiles.
- Read-only, import, export, write, bidirectional, and schema-inspection modes.
- Encrypted secret-provider abstraction.
- Metadata-only credential APIs.
- Validation and rotation workflows.
- Tenant ownership and permissions.

Initial connection categories:

```text
Database
REST API
GraphQL API
Webhook
Message queue
Object storage
File import
NEWAX application
Custom connector
```

Acceptance:

- Plaintext credentials never return after submission.
- Candidate credentials validate before activation.
- Failed replacement preserves the previous working credential.
- Every connection is tenant-scoped and audited.

# Phase HSP-2: Database adapter kernel

Deliver initial adapters:

- PostgreSQL
- MySQL
- MariaDB
- Microsoft SQL Server
- SQLite
- MongoDB
- Supabase
- Neon
- Amazon RDS-compatible relational services
- Google Cloud SQL-compatible relational services
- Azure SQL

Deliver adapter contract:

- Validation
- Schema discovery
- Safe preview
- Incremental read
- Bounded write where approved
- Cursor and checkpoint
- Transaction capability
- Batch limits
- Error classification
- Health metrics

Acceptance:

- Unsupported capability requests fail explicitly.
- Database-owner credentials are rejected or warned according to policy.
- Table, schema, collection, and operation allowlists are enforced.
- Adapter contract tests pass against supported engine versions.

# Phase HSP-3: Source-schema registry and mapping

Deliver:

- `SourceSchemaDefinition`.
- `SourceSchemaVersion`.
- `MappingProfile`.
- `MappingVersion`.
- Preview and sample fixtures.
- Direct, rename, constant, conditional, enum, split, combine, lookup, normalize, metadata, ignore, and review mappings.
- Mapping diff and rollback.
- Environment-specific activation.

Acceptance:

- A source-schema change cannot silently reuse an incompatible mapping.
- Mapping preview shows source, transformed, validation, and intended action.
- Every synchronized record retains source schema and mapping versions.

# Phase HSP-4: Harvester normalization boundary

Deliver:

```text
Source-native record
→ raw observation
→ normalized evidence
→ resolution candidate
→ resolved entity
→ lead profile
→ qualification
→ score
→ dossier
```

Work:

- Normalize external database rows through the same evidence boundary used by source connectors.
- Preserve raw payloads and source references.
- Reuse duplicate and identity resolution.
- Reuse qualification and scoring.
- Separate organization/person existence from lead interpretation inside Harvester.
- Ensure imported records do not bypass provenance or conflict review.

Acceptance:

- No external connector writes canonical or lead tables directly.
- All source paths preserve raw evidence.
- Duplicate handling is consistent across APIs, files, databases, and built-in sources.

# Phase HSP-5: Synchronization engine

Deliver:

- `SynchronizationProfile`.
- `SynchronizationRun`.
- `SynchronizationCheckpoint`.
- `SynchronizationConflict`.
- `SynchronizationDeliveryAttempt`.
- Transactional outbox integration.
- Retry, backoff, dead letter, circuit breaker, and backpressure.
- Manual, scheduled, polling, webhook, and event-driven modes.
- Change-data-capture only for adapters with approved semantics.
- Reconciliation and repair.

Acceptance:

- Harvester local commits do not depend on destination availability.
- Retried payloads preserve event identity and exact bytes.
- Sync jobs can resume from durable checkpoints.
- Backfill does not starve live work.

# Phase HSP-6: Publishing rules and output profiles

Deliver:

- Saved filters.
- Dynamic groups.
- Static selections.
- Frozen publication audiences.
- Publishing rules.
- Destination profiles.
- Minimal Contact, Standard Lead, Full Lead Context, Raw Observation, Canonical Entity, and Custom payload profiles.
- Field-level allowlist and redaction.
- Preview and approval.

Acceptance:

- The customer controls what leaves Harvester.
- Every publication records rule, audience, payload profile, mapping, hash, destination, and result.
- Suppressed or prohibited records cannot be published through a broader filter.

# Phase HSP-7: Direct Communicator integration

Deliver:

- Optional Harvester-to-Communicator adapter.
- Communicator capability discovery.
- Source profile and credential configuration.
- Lead and context payload mappings.
- Organization/person/contact references.
- Full Lead Context package.
- Communicator acknowledgement and link storage.
- Delivery outcome, reply, bounce, opt-out, and invalid-contact feedback intake.
- Verification and refresh request intake.

Acceptance:

- Harvester and Communicator operate together without Core.
- Communicator maps incoming data into its own model.
- Harvester remains source of lead intelligence, not conversation history.
- Hard bounce or invalid-contact feedback can trigger re-verification without deleting evidence history.

# Phase HSP-8: Optional NEWAX Core adapter

Deliver:

- Raw observation stream.
- Canonical entity stream.
- Independent enable, pause, and disable controls.
- Core source schema and capability negotiation.
- Core link and reconciliation.
- Core outage and backlog handling.
- Explicit statement that Core is optional.

Acceptance:

- Core downtime does not block harvesting.
- Core receives source-native Harvester data, not Harvester database rows.
- Core performs its own normalization and identity governance.
- Direct Communicator integration remains available without Core.

# Phase HSP-9: Administration UI

Routes:

```text
/settings/connections
/settings/credentials
/settings/source-schemas
/settings/mappings
/settings/synchronization
/integrations/communicator
/integrations/newax-core
```

Deliver:

- Connection list and health.
- Add and validate connection.
- Write-only credential replacement.
- Schema explorer.
- Mapping designer and preview.
- Synchronization run history.
- Conflict review.
- Retry and dead-letter recovery.
- Destination publishing rules.
- Communicator and Core integration pages.
- Audit timeline.

Acceptance:

- The UI never reveals stored secrets.
- Every action is permission-aware.
- Product autonomy is visible: disabled integrations do not create broken navigation or unusable lead workflows.

# Phase HSP-10: Multi-tenant resale foundation

Deliver:

- Tenant provisioning.
- Tenant-isolated data and connections.
- Tenant-specific branding and terminology.
- Subscription and license state.
- Connector and usage quotas.
- Feature flags.
- Custom domains.
- Tenant export and deletion.
- Tenant backup and restore.
- Upgrade and migration compatibility.
- Controlled white-label configuration.

Acceptance:

- No hard-coded NEWAX tenant or organization assumptions.
- One tenant cannot discover another tenant's connections, schemas, mappings, data, logs, or credentials.
- License enforcement does not make customer data inaccessible for export.

# Phase HSP-11: Packaging, verification, and rollout

Deliver:

- Docker-compatible deployment package.
- Environment templates.
- Supported database matrix.
- Connector certification matrix.
- Migration and rollback guide.
- Backup and restore runbook.
- Security review.
- Load and backlog testing.
- Failure-recovery testing.
- Multi-tenant isolation tests.
- Direct Harvester-to-Communicator E2E test.
- Harvester-to-Core E2E test.
- Harvester-only E2E test.

Activation requires:

- Exact-head CI.
- Supported migration chain validation.
- Runtime connector tests.
- Secret-leak tests.
- Tenant-isolation tests.
- Outage, retry, dead-letter, resume, and reconciliation tests.
- Documentation and support readiness.

# Existing roadmap integration

The following existing areas should absorb the work without creating duplicate top-level modules:

```text
Module 9   Authentication, authorization, tenants, and service identities
Module 19  Event and integration contracts
Module 23  Entity references, source links, and revisions
Module 33  Outbox, delivery, retry, and reconciliation
Module 36  Source ingestion and raw persistence
Module 52  Provenance, field ownership, and conflict handling
Module 63  Integration and administration APIs
Frontend   Connections, mappings, synchronization, Communicator, Core, and operations pages
```

Detailed implementation dependencies must be reconciled against the current `docs/ROADMAP.md` before code begins.

# Final acceptance

Harvester is ready for resale only when a customer can deploy it, connect approved sources, map data, generate and manage leads, export or synchronize selected results, back up and restore the system, and operate it without a NEWAX Core or Communicator account.