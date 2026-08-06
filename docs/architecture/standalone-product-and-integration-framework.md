# Harvester Standalone Product and Integration Framework

Status: **Planned architecture**

Authoritative roadmap:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)

## 1. Product decision

Harvester is a standalone, resellable lead-intelligence application.

It must be deployable, configured, operated, upgraded, backed up, restored, licensed, and supported without requiring NEWAX Core or Communicator.

Harvester may integrate with NEWAX Core, Communicator, a customer CRM, a customer database, a partner API, a message queue, object storage, or another approved system. Every integration is optional, separately credentialed, and replaceable.

> Harvester owns discovery, evidence, resolution, qualification, scoring, research, and lead intelligence. External systems may consume selected outputs, but they do not define Harvester's internal model.

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
- Share one universal integration credential across products, tenants, or environments.
- Format its internal records as NEWAX Core Registry rows or Communicator conversation rows.
- Treat a connected database or application as trusted merely because credentials work.

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
- Resolved institution or organization view
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
Existence, canonical identity, relationships, provenance,
field ownership, merge policy, and governed source facets

Communicator
Communication profiles, groups, audiences, campaigns,
conversations, messages, consent, and engagement
```

Harvester may resolve its own lead-oriented records, but it must not present them as Core canonical identity truth.

## 4. General connection and credential system

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

Every connection declares an explicit access mode:

```text
Schema inspection only
Read only
Import only
Export only
Write
Bidirectional
Migration
Backup or restore
```

Read-only or import-only access is the default. More powerful modes require explicit approval, separate credentials, preview, conflict policy, and audit.

## 5. Authentication profiles by destination

Different destinations may require different authentication methods. The connector declares what it supports and what the deployment permits.

Possible profiles include:

- Username and password
- Database-native credentials
- API key
- OAuth 2.0 client credentials
- OAuth 2.0 Authorization Code with PKCE for delegated user authorization
- Signed JWT service authentication
- Mutual TLS
- HMAC or asymmetric webhook signing
- Cloud-provider workload identity where supported

Permanent application secrets must not be embedded in browser or mobile code.

Credential lifecycle:

```text
Create candidate credential
→ validate without replacing active access
→ approve and activate
→ monitor use
→ rotate with overlap
→ revoke or expire
→ retain non-secret audit metadata
```

A failed replacement leaves the previously active credential available unless an authorized operator explicitly revokes it.

## 6. NEWAX Core developer application identity

A Harvester installation connecting to NEWAX Core must first be registered as a Core developer application or product installation.

```text
Core developer application
→ Harvester installation identity
→ environment-specific credential
→ bounded Core application principal
```

Harvester Production, Harvester Staging, and Communicator Production receive separate identities and credentials. They must not reuse one universal Core API key.

Preferred production flow:

```text
Harvester service credential
→ Core client-credential token exchange
→ short-lived access token
→ tenant, environment, audience, scope, and restriction validation
→ authorized Core API or ingestion endpoint
```

Core may also approve API keys, signed JWT identities, or mTLS for specific deployment profiles.

Possible Harvester Core scopes include:

```text
core.observations.publish
core.entities.propose
core.facets.write
core.identity-links.read
core.identity-links.write
core.delivery.receipts.read
core.commands.read
```

The final scope registry belongs to Core and is versioned there.

Restrictions may include:

```text
Application ID
Installation ID
Tenant
Environment
Audience
Allowed endpoints
Allowed event contracts
Allowed entity types
Allowed field groups
Allowed IP ranges
Allowed regions
Rate limit
Quota
Credential expiry
Token lifetime
```

Authentication success never bypasses Core domain authorization, identity resolution, field ownership, or merge policy.

## 7. Database connector framework

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

## 8. Connector kernel

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

Unsupported operations fail explicitly. A connector must not emulate support by silently dropping fields, ignoring errors, or broadening access.

## 9. Capability discovery and compatibility

Each connector records a versioned capability snapshot covering:

- Supported operations
- Authentication methods
- Schema versions
- Batch and payload limits
- Cursor or checkpoint semantics
- Idempotency behavior
- Rate and quota limits
- Receipt and acknowledgement support
- Conflict support
- Deprecation dates

A materially incompatible capability change blocks activation or new delivery safely and creates an operator-visible compatibility issue.

Running jobs remain pinned to the connector, schema, mapping, and normalization versions with which they started.

## 10. Independent schema registry

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

## 11. Mapping engine

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
→ normalized organization-name evidence

customer.website_url
→ website observation

customer.industry_code
→ Harvester sector taxonomy

customer.last_activity
→ freshness evidence
```

Mappings must support preview, test fixtures, validation, versioning, rollback, audit, and environment-specific activation.

## 12. Import and synchronization pipeline

```text
Connection profile
→ credential resolution
→ authentication and restriction validation
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

No connector writes directly to Harvester business tables. It submits source-native records through governed intake services.

## 13. Synchronization modes

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

- Connection and credential-reference versions
- Connector, source-schema, mapping, and normalization versions
- Source cursor or checkpoint
- Rows or records examined
- Created, updated, skipped, quarantined, and rejected counts
- Conflict decisions
- Error details without secrets
- Start and completion times
- Actor, application principal, or scheduler identity
- Retry and recovery state

## 14. Optional product integrations

Optional integrations are parallel destinations, not a mandatory chain.

```text
Harvester
├── local leads, dossiers, exports, and APIs
├── optional direct Communicator adapter
├── optional NEWAX Core adapter
└── optional customer or partner destinations
```

### 14.1 Harvester only

```text
Sources
→ Harvester
→ local leads, dossiers, exports, APIs, or customer database
```

### 14.2 Harvester and Communicator

```text
Harvester publishing rule
→ direct Harvester-to-Communicator adapter
→ Communicator mapping and normalization
```

Harvester may publish selected organizations, people, contacts, lead summaries, qualification, evidence summaries, opportunity signals, and dossier references.

Communicator decides how those records become communication profiles, groups, audiences, and context. Harvester never writes Communicator tables.

### 14.3 Harvester and NEWAX Core

```text
Harvester raw-observation, resolved-entity, and approved lead-context streams
→ optional Core adapter using a registered Core application identity
→ Core ingestion, canonical identity, provenance, and governance
```

Core integration is disabled unless configured. Core downtime or credential failure never stops local Harvester intake, resolution, qualification, scoring, research, or export.

### 14.4 Full NEWAX deployment

```text
Harvester
├── optional Core identity and governance
└── optional direct Communicator activation

Communicator
└── optional Core identity and governed context
```

The full deployment provides stronger cross-system identity and governance, but Core is not a mandatory relay between Harvester and Communicator. No product loses standalone operation.

## 15. Publishing rules

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
Minimal Contact
Standard Lead
Full Lead Context
Raw Observation
Resolved Entity
Custom Mapping
```

Every publication stores the applied rule, payload profile, mapping version, exact payload hash, destination, application or connection identity, event identity, and result.

## 16. Direct Communicator context package

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

Communicator owns communication profiles, audiences, campaigns, messages, conversations, engagement, consent, replies, and follow-up.

## 17. Core synchronization package

When configured, Harvester can publish three independently controlled source-native streams:

```text
RAW_OBSERVATION
RESOLVED_ENTITY
LEAD_CONTEXT
```

Harvester retains its own IDs. Core may return optional permanent links from Harvester IDs to Core IDs, but missing Core links never invalidate Harvester records.

Retries reuse the same event ID and exact serialized bytes. A new material revision receives a new event ID.

See [Optional NEWAX Core Synchronization](newax-core-automatic-sync.md) for the detailed delivery, credential, capability, and failure-recovery contract.

## 18. Multi-tenant and resale requirements

A resellable Harvester deployment requires:

- Tenant isolation
- Tenant-owned connections and credentials
- Per-tenant connector permissions
- Configurable terminology and branding
- Subscription and product-license enforcement
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

## 19. Administration pages

```text
/settings/connections
/settings/credentials
/settings/source-schemas
/settings/mappings
/settings/synchronization
/integrations/communicator
/integrations/newax-core
```

Pages show metadata, health, authentication type, credential fingerprint, scopes, restrictions, capabilities, mapping versions, synchronization history, usage, backlog, conflicts, and recovery. They never reveal stored secret values.

Dangerous operations require reauthentication and explicit permission.

## 20. Security requirements

- Separate runtime, read-only, write, migration, backup, and webhook-signing credentials.
- Separate application identities by product, tenant, installation, and environment.
- Short-lived access tokens for production service access where supported.
- TLS validation and approved network destinations.
- SSRF protections for URL-based connectors.
- Parameterized queries and adapter-owned query generation.
- Table, collection, schema, field, and operation allowlists.
- Payload, response, and batch limits.
- Tenant-scoped connection resolution.
- Audience, endpoint, IP, origin, region, entity, and field restrictions where required.
- HMAC, asymmetric signing, or mTLS for product events according to the approved profile.
- Event idempotency, replay protection, and payload hashing.
- Credential rotation without exposing previous values.
- Immediate credential revocation and emergency application disablement.
- Authorization-header and secret redaction in logs and traces.
- Audit without secrets or unrestricted raw personal data.
- No automatic write-back to an external database until preview, ownership, and conflict policy are approved.

## 21. Failure, conflict, and recovery rules

External systems are expected to fail.

The architecture must provide:

- Durable checkpoints
- Exponential backoff and jitter
- Circuit breakers
- Dead-letter queues
- Backpressure
- Per-entity ordering where required
- Idempotent replay
- Same-ID/different-payload conflict detection
- Reconciliation reports
- Dry-run repair and backfill
- Live-work priority over historical backfill
- Operator-visible credential, scope, quota, schema, and compatibility failures

Optional destination failure never rolls back committed Harvester data.

## 22. Acceptance criteria

The standalone integration architecture is not complete until:

1. Harvester starts and performs its core workflows with Core and Communicator absent or disabled.
2. Each tenant owns independent connections, credentials, mappings, cursors, and audit records.
3. Source-native data is preserved before transformation.
4. Harvester mappings are versioned and previewable.
5. External schemas never become Harvester's internal schema by accident.
6. A failed optional integration cannot roll back a committed Harvester observation or lead update.
7. Database access defaults to least privilege.
8. Connector capabilities and limitations are explicit and versioned.
9. Unknown or incompatible fields enter review or metadata rather than disappearing silently.
10. Direct Harvester-to-Communicator delivery works without Core.
11. Harvester-to-Core delivery works without Communicator.
12. Customer databases can be used as sources or destinations through approved adapters.
13. Product-specific formats and identifiers remain independent.
14. Publishing rules determine what leaves Harvester.
15. Secrets remain encrypted, write-only, and non-retrievable after issuance.
16. Credential rotation supports controlled overlap and safe rollback.
17. Retries are idempotent and dead-lettered when exhausted.
18. Reconciliation detects missing, conflicting, stale, or revoked cross-system state.
19. Every Core-connected Harvester installation and environment has its own application identity and credential lifecycle.
20. Harvester and Communicator cannot share one universal Core credential.
21. Core application scopes, tenant, environment, audience, endpoint, IP, entity, field, rate, quota, expiry, and revocation restrictions are enforced.
22. The full deployment uses parallel optional adapters rather than making Core a mandatory relay.
23. Packaging, product licensing, tenant isolation, backup, restore, and upgrade paths are verified.
24. Exact-head tests, security checks, migrations, runtime workflows, and CI pass before activation.

## 23. Locked rule

> Harvester is a standalone lead-intelligence product. It may connect to many sources and destinations through separately credentialed, versioned adapters, but it always maps and normalizes data according to Harvester's own evidence, resolution, qualification, scoring, and research model.
