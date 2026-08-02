# Automatic NEWAX Core Synchronization Roadmap

## Status

- Lifecycle: Planned
- Parent roadmap: `docs/ROADMAP.md`
- Top-level module count: Remains 64
- Frontend sequence after this addendum: F1–F17

This addendum defines Harvester's automatic publication of raw observations and canonical entities to NEWAX Core. It is intended to be integrated into the main roadmap and does not claim that the complete workflow is currently implemented.

## Locked product boundary

Harvester publishes two independent streams:

```text
Raw Observation Stream
Every accepted source observation is queued immediately after durable local storage.

Canonical Entity Stream
Every new or materially changed resolved entity is queued after resolution and validation.
```

Lead qualification does not control publication.

An organization, person, location, contact method, domain, website, or relationship may exist in NEWAX Core without being a lead. Lead status is a later business classification.

## Current baseline

Harvester already contains a durable `EventOutbox` foundation with stable event identity, persisted payload, retry metadata, exponential backoff, concurrency-safe claiming, dead-letter handling, and manual requeue.

The current durable path is not yet a complete two-stream publisher. It is mainly connected to institution-oriented manual and resynchronization workflows. Raw-storage boundaries and every canonical create or update path do not yet publish through one shared scheduler.

The roadmap must evolve the existing outbox rather than build a second competing delivery ledger.

## Bounded roadmap submodules

The existing 64 top-level modules remain unchanged. Automatic Core synchronization is delivered through bounded submodules inside the existing architecture.

### Module 9D: Core integration identity and configuration

Module 9 expands to:

```text
9A  Service authentication and frontend sessions
9B  Secret provider and metadata-only secret management
9C  Database connection and environment control
9D  NEWAX Core integration identity, endpoint, contracts, and permissions
```

Deliver:

- Core environment profile
- Service-account identity metadata
- Core endpoint reference
- Signing-secret reference managed through Secrets & Integrations
- Connection validation
- Active source schema compatibility
- Raw and canonical stream controls
- Rate, concurrency, retry, circuit-breaker, and backlog configuration
- Permissions, reauthentication, and audit
- No-secret logging or frontend exposure

### Module 19B: Common Core integration envelope and stream contracts

Module 19 retains the normalized evidence contract and gains:

```text
19B  Source-native integration envelope, raw-observation contract, and canonical-entity contract
```

Deliver:

- Standard outer envelope
- Stable event ID
- Source system, connector, and schema identity
- Event and receipt timestamps
- Tenant reference
- Source-record reference
- Entity reference
- Subject hint
- Correlation ID
- Canonical revision
- Payload checksum
- Source-native payload
- Supporting raw observation IDs on canonical events
- Contract and compatibility tests

Raw event type:

```text
observation.recorded
```

Subject hints:

```text
organization
person
location
contact_method
domain
website
relationship
document
social_profile
unknown
```

Canonical events include organization, person, location, and relationship create, update, and retirement events.

### Module 23B: Canonical revisions, Core projections, and permanent links

Module 23 gains:

```text
23B  Canonical revision records, CoreSyncProjection, projection hashing, and CoreSyncLink
```

Deliver:

- Canonical revision per entity
- Source-native Core projection
- Deterministic serialization
- SHA-256 projection hash
- Material changed-field summary
- Supporting observation links
- Permanent Harvester-to-Core ID link
- Latest applied event, revision, and hash
- Sync and reconciliation state

Unchanged projections create no event. New material revisions receive a new event ID.

### Module 33C: Automatic Core delivery and reconciliation jobs

Module 33 expands to:

```text
33A  Live Harvest Job event streaming
33B  Database operation jobs
33C  Automatic Core delivery, retry, circuit breaker, backpressure, backfill, and reconciliation
```

Deliver:

- Automatic delivery worker
- Concurrency-safe claims
- Per-aggregate ordering
- Exact-payload retry
- HMAC signing over transmitted bytes
- Transient/permanent failure classification
- Backoff with bounded jitter
- Circuit breaker
- Backpressure thresholds
- Priority scheduling
- Dead-letter recovery
- Response and Core-ID persistence
- Reconciliation runs
- Historical backfill jobs
- Operational metrics and audit

Priority:

```text
1. Live canonical changes
2. Recent live raw observations
3. Reconciliation and repair
4. Historical backfill
```

### Module 36B: Transactional raw-observation publishing

Module 36 retains incremental evidence persistence and gains:

```text
36B  Transactional raw-observation outbox publishing from every approved source-storage boundary
```

Deliver:

- One shared `RawObservationPublisher`
- Atomic raw-record and outbox insertion
- Stable source-record identity
- Payload hashing
- Exact duplicate suppression
- Immutable changed-source versions
- Source-native payload preservation
- Connector coverage for Google, Yandex, Apple Maps, websites, imports, Telegram, manual, research, and approved restricted sources
- Failure tests proving source persistence cannot commit without the required outbox row when publishing is enabled

### Module 52B: Core provenance and field-ownership context

Module 52 retains source contribution and gains:

```text
52B  Supporting-observation graph and Core merge-policy context
```

Deliver:

- Canonical events linked to supporting observations
- Source and field provenance
- Confidence and verification times
- Harvester-owned versus Core-owned field context
- Proposed changes rather than blind replacement of protected Core values
- Evidence references for organization, person, location, contact, domain, website, and relationship facts

Harvester supplies provenance and source-native facts. Core owns final normalization and merge decisions.

### Module 63B: NEWAX Core Sync backend APIs

Module 63 retains export and Communicator work and gains a bounded integration slice:

```text
63B  NEWAX Core Sync overview, configuration, queue, dead letter, links, backfill, and reconciliation APIs
```

Planned APIs:

```http
GET    /api/v1/core-sync/overview
GET    /api/v1/core-sync/configuration
PUT    /api/v1/core-sync/configuration
POST   /api/v1/core-sync/connection/validate

GET    /api/v1/core-sync/events
GET    /api/v1/core-sync/events/{event_id}
POST   /api/v1/core-sync/events/{event_id}/retry
POST   /api/v1/core-sync/events/{event_id}/cancel

GET    /api/v1/core-sync/links
GET    /api/v1/core-sync/dead-letter
POST   /api/v1/core-sync/dead-letter/{event_id}/requeue

POST   /api/v1/core-sync/backfills/preview
POST   /api/v1/core-sync/backfills
GET    /api/v1/core-sync/backfills/{backfill_id}
POST   /api/v1/core-sync/backfills/{backfill_id}/pause
POST   /api/v1/core-sync/backfills/{backfill_id}/resume

POST   /api/v1/core-sync/reconciliation-runs
GET    /api/v1/core-sync/reconciliation-runs
GET    /api/v1/core-sync/reconciliation-runs/{run_id}
```

## Outbox model evolution

Generalize the existing delivery ledger with fields such as:

```text
stream_type
event_type
aggregate_type
aggregate_id
aggregate_revision
source_record_reference
payload
payload_hash
priority
status
attempt_count
next_attempt_at
last_error
created_at
delivered_at
```

Stream types:

```text
RAW_OBSERVATION
CANONICAL_ENTITY
RECONCILIATION
BACKFILL
```

Every retry preserves the exact event identity and payload. A changed observation version or new canonical revision creates a different event.

## Automatic scheduling boundaries

### Raw observations

```text
BEGIN
Persist approved raw observation
Create RAW_OBSERVATION outbox event
COMMIT
```

### Canonical entities

```text
BEGIN
Create or update canonical entity
Increase canonical revision
Build Core projection
Compare projection hash
Create CANONICAL_ENTITY event when materially changed
COMMIT
```

Source connectors do not construct Core-specific Registry payloads independently.

## Frontend Module 64 expansion

The frontend milestone contains F1–F17:

```text
F1   Design tokens and foundations
F2   Application shell
F3   Shared data components
F4   Authentication and runtime configuration
F5   Generate Leads
F6   Harvest Runs and live Harvest Run
F7   Source-specific metric displays
F8   Generated Leads
F9   Master Leads
F10  Lead Dossier
F11  Qualification and governance
F12  Secrets & Integrations
F13  Database Connections & Sync
F14  NEWAX Core Sync
F15  Export and Communicator
F16  Operations
F17  End-to-end and rollout verification
```

### F14: NEWAX Core Sync

Planned route:

```text
/integrations/newax-core
```

Tabs:

```text
Overview
Raw Observations
Canonical Entities
Delivery Queue
Dead Letter
Entity Links
Reconciliation
Settings
```

Deliver:

- Raw and canonical stream status
- Independent enable, pause, and disable controls
- Core health and worker health
- Queue, retry, dead-letter, and delivery-delay metrics by stream
- Live event activity
- Event detail and safe payload access
- Core response and canonical ID links
- Retry and dead-letter requeue
- Backfill preview, start, pause, and resume
- Reconciliation runs and repair actions
- Configuration without revealing endpoint secrets
- Permission gates and reauthentication
- Loading, empty, degraded, outage, backlog, failure, and recovery states
- Accessibility and no-secret-leak tests

Dependencies:

- Modules 8, 9B, and 9D
- Modules 19B, 23B, 33C, 36B, 52B, and 63B
- F2 application shell
- F3 shared data components
- F4 authentication
- F12 Secrets & Integrations

## Updated dependency order

```text
Modules 1–16, including 9D
Security, identity, secret, database, and integration foundations
        ↓
Modules 17–37, including 19B, 23B, 33C, and 36B
Contracts, persistence, workers, automatic raw and canonical scheduling
        ↓
Modules 38–54, including 52B
Source workflows, resolution, provenance, and canonical change publication
        ↓
Modules 55–63, including 63B
Qualification, lead workspaces, Core Sync APIs, exports, and Communicator
        ↓
Module 64 / F1–F17
Complete operating interface and rollout
```

## Milestone updates

### Milestone A

Additionally requires:

- Core service identity and signing-secret references
- Source-native envelope contract
- No-secret-leak controls

### Milestone B

Additionally requires:

- Transactional raw and canonical event scheduling
- Automatic delivery worker
- Retry, dead letter, circuit breaker, and backpressure
- Canonical revisions and permanent Core links

### Milestone C

Additionally requires:

- Every approved connector publishes raw observations through the shared publisher
- Connector-specific Core event construction is prohibited

### Milestone D

Additionally requires:

- Canonical organization, person, location, and relationship changes publish automatically
- Supporting observations remain linked
- Lead qualification remains independent from entity publication

### Milestone F

Additionally requires:

- Dedicated NEWAX Core Sync page
- Separate raw and canonical queue visibility
- Independent stream controls
- Backfill, dead-letter, links, and reconciliation workflows
- Complete outage and recovery testing

## Core dependency

Harvester uses at-least-once delivery. Production automatic synchronization remains disabled until NEWAX Core provides:

- Durable inbound inbox keyed by event ID
- Payload-hash conflict detection
- Idempotent result replay
- Source schema registry
- Raw-observation and canonical-entity adapters
- Common normalization engine
- Candidate entities
- Identity resolution
- Provenance linking
- Field ownership and merge policy
- Safe transaction or resumable canonical application
- Applied source-revision tracking

## Additional acceptance criteria

The roadmap is incomplete until:

1. Every accepted raw observation creates an outbox event atomically.
2. Raw publication is independent from lead qualification.
3. Exact duplicate source observations are idempotent.
4. Changed source records create immutable new versions.
5. Observations from different sources remain independently traceable.
6. Every canonical entity creation publishes automatically.
7. Every material canonical change publishes a higher revision.
8. Unchanged canonical projections produce no event.
9. Supporting observation IDs are included where available.
10. Source connectors use shared publishers rather than Core-specific code.
11. Retries preserve event ID and exact payload.
12. New revisions receive new event IDs.
13. Ordering, supersession, and coalescing are deterministic.
14. Core downtime never blocks local source or canonical persistence.
15. Circuit breaking and backpressure are tested.
16. Raw and canonical streams can be paused independently without data loss.
17. Live work is prioritized over historical backfill.
18. Permanent Core entity links are stored and reconciled.
19. Dead-letter events remain visible and recoverable.
20. Organizations and people may exist without lead profiles.
21. Lead qualification remains a separate commercial classification.
22. Core provides durable inbox idempotency and safe application boundaries.
23. F14 passes permission, reauthentication, accessibility, outage, backlog, recovery, and no-secret-leak tests.
24. Exact-head runtime, integration, migration, security, and CI checks pass.

## Governance update

- The top-level roadmap remains 64 modules.
- Modules 9D, 19B, 23B, 33C, 36B, 52B, and 63B are bounded submodules.
- Module 64 contains F1–F17.
- Raw observations and canonical entities are separate streams and separate operational metrics.
- “Not a lead” never means “not an entity.”
- Harvester owns source-native publication and provenance; Core owns canonical formatting and merge policy.
- Production automation remains gated by verified Core inbox and application controls.
