# Harvester Standalone Product and Integration Framework

Status: **Planned architecture**

## 1. Product decision

Harvester is a standalone, resellable application.

It must be deployable, configured, operated, upgraded, backed up, restored, licensed, and supported without requiring NEWAX Core or Communicator.

Harvester may integrate with NEWAX Core, Communicator, a customer CRM, a customer database, a partner API, a message queue, object storage, or another approved system. Every integration is optional and replaceable.

> Harvester owns discovery, evidence, resolution, qualification, and lead intelligence. External systems may consume selected outputs, but they do not define Harvester's internal model.

## 2. Non-negotiable boundaries

Harvester must:

- Own its operational database and migrations.
- Own its authentication, authorization, tenant isolation, audit, retention, and backup behavior.
- Own its source-connector framework.
- Own its credential and connection profiles.
- Own its source-schema registry.
- Own its mapping and normalization engine.
- Own its raw observations, evidence, resolved entities, lead profiles, qualification, scoring, research, and source history.
- Continue harvesting and resolving data when every optional integration is unavailable.
- Use APIs, webhooks, event delivery, exports, imports, or approved database connectors rather than another product's internal tables.

Harvester must not:

- Require NEWAX Core to create or use leads.
- Require Communicator to qualify or export leads.
- Read or write another product's private tables.
- Share database-owner credentials with another application.
- Format its internal records as NEWAX Core Registry rows or Communicator conversation rows.
- Treat a connected database as trusted merely because credentials work.

## 3. Harvester's internal formatting

Harvester formats incoming information for research and lead operations:

```text
Source-native record
→ Raw observation
→ Normalized evidence
→ Resolution candidate
→ Resolved organization, person, branch, contact, or relationship
→ Lead profile
→ Qualification assessment
→ Opportunity score
→ Research dossier
```

The Harvester model may contain:

- Source record identity and version
- Immutable raw payload
- Evidence and provenance
- Canonical institution or organization view
- People and roles
- Branches and locations
- Contact points and verification
- Qualification policy and result
- Lead score and score history
- Opportunity signals and service gaps
- Research findings and confidence
- Compliance and suppression
- Outreach readiness

This format remains independent from:

```text
NEWAX Core
Existence, identity, relationships, provenance, and governed source facets

Communicator
Contact profiles, audiences, campaigns, conversations, messages, consent, and engagement
```

## 4. Connection and credential system

Harvester requires a general connection framework at:

```text
/settings/connections
```

Connection categories:

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

A connection profile stores non-secret metadata:

```text
id
name
connector_type
engine_or_provider
environment
host
port
database_or_resource
schema_or_namespace
ssl_mode
network_mode
access_mode
secret_reference
status
capability_snapshot
last_validated_at
last_successful_sync_at
created_at
updated_at
```

Secrets remain write-only after submission. The frontend may show configured state and a short fingerprint, never the stored value.

Production secret resolution order:

```text
Deployment secret manager
→ encrypted application vault
→ explicitly enabled local development secret adapter
```

## 5. Database connector framework

"Connect to any database" means a pluggable adapter contract, not arbitrary SQL against an unknown server.

Initial relational adapters:

- PostgreSQL
- MySQL
- MariaDB
- Microsoft SQL Server
- SQLite for bounded local use

Initial document and managed-service adapters:

- MongoDB
- Supabase
- Neon
- Amazon RDS-compatible relational databases
- Google Cloud SQL-compatible relational databases
- Azure SQL

Later adapters may cover Oracle, DynamoDB, Firebase, Elasticsearch, Snowflake, BigQuery, ClickHouse, and approved customer-specific systems.

Every adapter declares:

- Supported engine and versions
- Read, write, import, export, polling, webhook, or change-data-capture capability
- Schema discovery support
- Transaction support
- Cursor and checkpoint behavior
- Identifier and timestamp behavior
- Rate, batch, and payload limits
- TLS and network requirements
- Safe validation query
- Required database permissions

Default access is read-only. Write, bidirectional, migration, backup, and change-data-capture capabilities require explicit approval and separate credentials.

## 6. Connector kernel

A stable connector contract should resemble:

```python
class ConnectionAdapter:
    connector_type: str
    adapter_version: str

    async def validate(self, profile, credential) -> ValidationResult: ...
    async def discover_schema(self, profile) -> SourceSchema: ...
    async def preview(self, profile, cursor=None) -> PreviewBatch: ...
    async def read(self, profile, cursor=None) -> SourceBatch: ...
    async def write(self, profile, records) -> WriteResult: ...
    async def checkpoint(self, run) -> Checkpoint: ...
```

Provider-specific behavior stays inside the adapter. Harvester services consume normalized connector results rather than provider clients directly.

## 7. Independent schema registry

Harvester maintains its own source-schema registry:

```text
source_system
source_schema_name
source_schema_version
connector_version
mapping_version
normalization_version
active_from
active_until
compatibility_state
```

Examples:

```text
customer_crm.accounts.v2
customer_postgres.organizations.v4
harvester.google_places.place.v1
partner_api.company.v3
```

A source schema describes what arrived. It does not redefine Harvester's internal database schema.

## 8. Mapping engine

Every connection may use a versioned Harvester-owned mapping.

Supported mapping operations:

- Direct mapping
- Rename
- Constant value
- Conditional mapping
- Enumeration mapping
- Split
- Combine
- Lookup table
- Normalization
- Ignore
- Store as metadata
- Preserve as raw evidence
- Require review

Example:

```text
customer.account_name
→ normalized organization name evidence

customer.website_url
→ website observation

customer.industry_code
→ Harvester sector taxonomy

customer.last_activity
→ freshness evidence
```

Mappings must support preview, test fixtures, validation, versioning, rollback, audit, and environment-specific activation.

## 9. Import and synchronization pipeline

```text
Connection profile
→ credential resolution
→ capability validation
→ source schema discovery
→ source-native read
→ immutable raw persistence
→ mapping
→ Harvester normalization
→ duplicate and identity resolution
→ lead and evidence services
→ local transaction commit
→ optional outbound publication
```

The local Harvester transaction succeeds independently of optional outbound delivery.

## 10. Synchronization modes

Supported target modes:

```text
Manual import
Scheduled import
Continuous polling
Webhook-triggered import
Change-data-capture where an adapter safely supports it
Manual export
Scheduled export
Event-driven publication
Bidirectional synchronization for explicitly approved records
```

Every synchronization run stores:

- Connection and mapping versions
- Source cursor or checkpoint
- Rows or records examined
- Created, updated, skipped, quarantined, and rejected counts
- Conflict decisions
- Error details without secrets
- Start and completion times
- Actor or scheduler identity
- Retry and recovery state

## 11. Optional product integrations

### 11.1 Harvester only

```text
Sources
→ Harvester
→ local leads, dossiers, exports, APIs, or customer database
```

### 11.2 Harvester and Communicator

```text
Harvester publishing rule
→ Harvester-to-Communicator adapter
→ Communicator mapping and normalization
```

Harvester may publish selected organizations, people, contacts, lead summaries, qualification, evidence summaries, opportunity signals, and dossier references.

Communicator decides how those records become communication profiles, groups, audiences, and context. Harvester never writes Communicator tables.

### 11.3 Harvester and NEWAX Core

```text
Harvester raw observation and canonical-entity streams
→ optional Core adapter
→ Core ingestion and identity governance
```

Core integration is disabled unless configured. Core downtime never stops local Harvester intake, resolution, qualification, or export.

### 11.4 Full NEWAX deployment

```text
Harvester
→ optional Core identity and governance
→ optional Communicator activation
```

The full deployment provides stronger cross-system identity and governance, but no product loses standalone operation.

## 12. Publishing rules

The customer controls what leaves Harvester.

Selection methods:

- Saved filter
- Dynamic group
- Static selection
- Frozen harvest result
- Schedule
- Event trigger
- API request

Example publishing rule:

```text
qualification_status = qualified
lead_score >= 70
verified_email = true
suppressed = false
sector = healthcare
country = PK
```

Payload profiles:

```text
Minimal contact
Standard lead
Full lead context
Raw observation
Canonical entity
Custom mapping
```

Every publication stores the applied rule, payload profile, mapping version, exact payload hash, destination, event identity, and result.

## 13. Direct Communicator context package

When configured, Harvester can publish a bounded context package containing:

- Source Harvester IDs
- Organization and person summaries
- Contact channels and verification
- Qualification and score
- Opportunity signals
- Detected operational problems
- Relevant research summary
- Evidence freshness and confidence
- Dossier reference
- Permitted supporting facts

The full raw dossier remains in Harvester unless the customer explicitly authorizes a broader export.

## 14. Multi-tenant and resale requirements

A resellable Harvester deployment requires:

- Tenant isolation
- Tenant-owned connections and credentials
- Per-tenant connector permissions
- Configurable terminology and branding
- Subscription and license enforcement
- Usage and quota controls
- Feature flags
- Custom domains
- Import and export portability
- Tenant retention policies
- Tenant backup and restore
- Audit export
- Deployment documentation
- No hard-coded NEWAX organization assumptions

NEWAX remains the product brand by default. Controlled enterprise white-labeling may be supported without changing the internal security model.

## 15. Administration pages

```text
/settings/connections
/settings/credentials
/settings/source-schemas
/settings/mappings
/settings/synchronization
/integrations/communicator
/integrations/newax-core
```

Pages show metadata, health, capabilities, mapping versions, sync history, backlog, conflicts, and recovery. They never reveal stored secret values.

## 16. Security requirements

- Separate runtime, read-only, write, migration, and backup credentials.
- TLS validation and approved network destinations.
- SSRF protections for URL-based connectors.
- Parameterized queries and adapter-owned query generation.
- Table, collection, schema, and operation allowlists.
- Payload, response, and batch limits.
- Tenant-scoped connection resolution.
- HMAC or asymmetric signing for product events.
- Event idempotency, replay protection, and payload hashing.
- Credential rotation without exposing previous values.
- Audit without secrets or unrestricted raw personal data.
- No automatic write-back to an external database until preview, ownership, and conflict policy are approved.

## 17. Acceptance criteria

The standalone integration architecture is not complete until:

1. Harvester starts and performs its core workflows with Core and Communicator disabled.
2. Each tenant owns independent connections, credentials, mappings, cursors, and audit records.
3. Source-native data is preserved before transformation.
4. Harvester mappings are versioned and previewable.
5. External schemas never become Harvester's internal schema by accident.
6. A failed optional integration cannot roll back a committed Harvester observation or lead update.
7. Database access defaults to least privilege.
8. Connector capabilities and limitations are explicit.
9. Unknown or incompatible fields enter review or metadata rather than disappearing silently.
10. Direct Harvester-to-Communicator delivery works without Core.
11. Harvester-to-Core delivery works without Communicator.
12. Customer databases can be used as sources or destinations through approved adapters.
13. Product-specific formats remain independent.
14. Publishing rules determine what leaves Harvester.
15. Secrets remain encrypted and write-only.
16. Retries are idempotent and dead-lettered when exhausted.
17. Reconciliation detects missing, conflicting, or stale cross-system links.
18. Packaging, licensing, tenant isolation, backup, restore, and upgrade paths are verified.
19. Exact-head tests, security checks, migrations, runtime workflows, and CI pass before activation.

## 18. Locked rule

> Harvester is a standalone lead-intelligence product. It may connect to many sources and destinations through credentialed adapters, but it always maps and normalizes data according to Harvester's own evidence, resolution, qualification, and lead model.