# Automatic NEWAX Core Synchronization

## Status

- Lifecycle: Planned
- Harvester role: Automatic source-native publisher
- Core role: Durable ingestion, normalization, identity resolution, merge policy, and canonical Registry application

This document defines Harvester's side of the NEWAX Core integration. It does not claim that the complete two-stream workflow is currently implemented.

## Locked boundary

Harvester publishes two independent automatic streams to NEWAX Core:

1. Every accepted raw observation after it is durably stored in Harvester.
2. Every new or materially changed canonical entity after Harvester resolves and validates it.

Lead qualification is not a prerequisite for either stream.

An organization remains an organization whether it becomes a lead, customer, supplier, partner, competitor, regulator, or no commercial relationship at all. A person remains a person whether or not that person is useful for outreach. Lead status is a business classification attached later; it is not an admission gate for entity existence.

```text
Raw Observation
→ Entity Candidate
→ Canonical Entity
→ Business Roles and Classifications
→ Lead / Customer / Supplier / Partner / Competitor / Other
```

## Stream 1: raw observations

### Purpose

The raw stream preserves what each approved source actually reported before final identity resolution.

Raw observations may describe:

- Organizations
- People
- Locations
- Contact methods
- Domains
- Websites
- Social profiles
- Relationships
- Documents
- Products and services
- Business classifications
- Operating states
- Unknown subjects that require later interpretation

### Publishing boundary

Every accepted raw observation is stored and queued atomically:

```text
BEGIN

Persist RawSourceRecord, RawPageSnapshot, or approved raw observation
Create raw-observation EventOutbox row with exact event payload

COMMIT
```

The source request does not wait for Core processing. A background worker delivers the already-persisted event.

### Raw event envelope

```json
{
  "integration_version": 1,
  "event_id": "01915f26-f4d5-7d16-8f93-dfa3b42006dd",
  "event_type": "observation.recorded",
  "source_system": "newax_harvester",
  "source_connector": "google_places",
  "source_schema": "harvester.google_places.place.v1",
  "occurred_at": "2026-08-02T02:00:00.000Z",
  "received_at": "2026-08-02T02:00:03.000Z",
  "tenant_reference": "newax",
  "source_record_reference": "ChIJ123456789",
  "entity_reference": null,
  "subject_hint": "organization",
  "correlation_id": "harvest-job-id",
  "canonical_revision": null,
  "payload_checksum": "sha256-value",
  "payload": {}
}
```

Recommended subject hints:

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

The outer envelope is standardized. `payload` remains source-native. Harvester does not reshape every raw source record into Core's internal Prisma or Registry format.

### Observation identity and versions

Harvester and Core distinguish:

- Same source record and same payload hash: idempotent duplicate, no new observation version.
- Same source record and changed payload hash: new immutable observation version.
- Different sources reporting the same real entity: separate observations retained for provenance and later linked to one canonical entity.

Suggested identity inputs:

```text
source_system
source_connector
source_record_reference
source_record_version
payload_hash
```

## Stream 2: canonical entities

### Purpose

The canonical stream sends Harvester's resolved understanding after normalization, deduplication, evidence consolidation, identity resolution, and validation.

Canonical entities include organizations, people, locations, contact methods, domains, websites, and relationships. They are not limited to qualified leads.

### Publishing boundary

```text
BEGIN

Create or update canonical entity
Increase canonical revision
Build source-native Core projection
Calculate projection hash
Create canonical-entity EventOutbox row when the material projection changed

COMMIT
```

The canonical write and event insertion either both commit or both roll back.

### Material-change detection

```text
Build projection
→ Canonically serialize projection
→ Calculate SHA-256 hash
→ Compare with last successfully scheduled projection hash
```

Same hash means no duplicate event. A different hash creates a new event with a new event ID and a higher canonical revision.

Suggested projection record:

```text
CoreSyncProjection

id
entity_type
entity_id
source_schema
source_schema_version
mapping_version
canonical_revision
payload
payload_hash
changed_fields
validation_result
created_at
```

### Canonical event types

```text
organization.canonical_created
organization.canonical_updated
organization.canonical_retired
person.canonical_created
person.canonical_updated
person.canonical_retired
location.canonical_created
location.canonical_updated
relationship.canonical_created
relationship.canonical_updated
relationship.canonical_retired
```

Canonical events include supporting raw observation IDs where available, creating the provenance chain:

```text
Core canonical entity
→ Harvester canonical entity
→ Raw observations
→ Original sources
```

## Common source-native envelope

Harvester understands the common integration protocol, not Core's internal database layout.

```json
{
  "integration_version": 1,
  "event_id": "01915f26-f4d5-7d16-8f93-dfa3b42006ee",
  "event_type": "organization.canonical_updated",
  "source_system": "newax_harvester",
  "source_connector": "canonical_registry",
  "source_schema": "harvester.organization.v1",
  "occurred_at": "2026-08-02T02:10:00.000Z",
  "received_at": "2026-08-02T02:10:00.000Z",
  "tenant_reference": "newax",
  "source_record_reference": null,
  "entity_reference": "institution_01J8AC9",
  "subject_hint": "organization",
  "correlation_id": "harvest-job-id",
  "canonical_revision": 12,
  "payload_checksum": "sha256-value",
  "supporting_observation_ids": [
    "observation_001",
    "observation_002"
  ],
  "payload": {}
}
```

Core owns the final mapping from this source-native payload to Registry services.

## Event outbox evolution

Harvester already has a durable `EventOutbox` foundation. It must evolve from one institution-sync payload into a general multi-stream delivery ledger.

Suggested fields:

```text
id
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

Every retry reuses the same event ID and exact serialized payload. A genuinely newer observation version or canonical revision receives a new event ID.

## Central scheduling services

Source connectors must not construct Core payloads independently.

Suggested services:

```text
RawObservationPublisher
CanonicalChangePublisher
CoreSyncProjectionBuilder
CoreSyncScheduler
CoreSyncDeliveryWorker
CoreSyncReconciliationService
```

All raw-storage paths call one raw publisher. All canonical create and update paths call one canonical scheduler.

Required raw paths include map sources, websites, imports, Telegram, manual submissions, professional-network evidence where approved, page snapshots, research findings, and future connectors.

Required canonical paths include organization, person, branch or location, contact, domain, website, and relationship resolution workflows.

## Delivery priorities

```text
1. Live canonical changes
2. Recent live raw observations
3. Reconciliation and repair
4. Historical backfill
```

Canonical updates must not wait behind a large historical raw-data backfill.

## Delivery worker

The automatic worker:

1. Claims pending events using a concurrency-safe database query.
2. Preserves per-aggregate ordering where required.
3. Serializes the payload once.
4. Signs the exact serialized bytes.
5. Sends to the configured Core endpoint.
6. Records the Core result.
7. Updates the permanent Harvester-to-Core link for canonical entities.
8. Retries transient failures.
9. Dead-letters exhausted or permanent failures.
10. Emits metrics and audit events.

Recommended defaults:

```text
Polling fallback                5 seconds
Batch size                     50
Maximum concurrent deliveries   5
Maximum requests per second    10
```

## Retry classification

Retry transient conditions such as network errors, timeouts, HTTP 408, HTTP 429, and HTTP 500–599.

Do not endlessly retry permanent conditions such as unsupported schema, invalid signature, forbidden service account, unknown tenant, invalid required data, or mapping incompatibility.

Suggested schedule:

```text
Attempt 1  Immediate
Attempt 2  1 minute
Attempt 3  5 minutes
Attempt 4  15 minutes
Attempt 5  1 hour
Attempt 6  6 hours
Then       Dead letter
```

Use bounded jitter.

## Circuit breaker and backpressure

When Core is repeatedly unavailable, Harvester keeps harvesting and persisting events while reducing network attempts.

Suggested circuit breaker:

```text
Open after 10 consecutive transport failures
Half-open health check after 5 minutes
Close after successful recovery checks
```

Suggested backlog thresholds:

```text
Warning   1,000 pending events
Critical 10,000 pending events
```

At critical backlog, Harvester continues durable storage but pauses nonessential historical backfill and alerts operators. Events are never discarded merely to make a dashboard number smaller.

## Ordering, supersession, and coalescing

Canonical events carry aggregate ID and revision.

- Older revisions become stale or superseded.
- Same revision and same hash is idempotent.
- Same revision and different hash is an integrity conflict.
- Newer revision is evaluated normally.

Rapid canonical updates may use a configurable coalescing window, initially 30 seconds. Only undelivered events may be superseded. A delivery retry is never mutated.

## Permanent Core links

Suggested model:

```text
CoreSyncLink

entity_type
entity_id
core_entity_type
core_entity_id
last_event_id
last_canonical_revision
last_projection_hash
last_applied_at
last_reconciled_at
sync_status
```

The durable link is based on stable IDs, not names or domains.

## Pause behavior

Raw and canonical delivery are independently controllable:

```text
Raw Observation Sync
Enabled | Paused | Disabled

Canonical Entity Sync
Enabled | Paused | Disabled
```

Pausing delivery:

- Stops claiming new events.
- Allows active requests to finish.
- Continues local raw and canonical persistence.
- Continues outbox creation.
- Preserves ordering and event identity.
- Displays the growing backlog.

It does not disable harvesting, delete events, mark work failed, or regenerate IDs.

## Historical backfill

Future automatic events do not cover records already present before activation.

Backfill supports:

- All eligible raw observations
- Selected sources
- Selected harvest jobs
- Selected date ranges
- Records without recorded Core delivery
- All canonical entities
- Canonical entities without Core links
- Canonical entities changed since a chosen date

Backfill runs at lower priority than live work and supports dry-run counts, rate limits, pause, resume, and reconciliation.

## Dedicated Harvester page

Planned route:

```text
/integrations/newax-core
```

Navigation:

```text
Operations
└── NEWAX Core Sync
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

The overview shows:

- Raw and canonical stream state
- Delivery-worker health
- Core health
- Events sent today
- Pending, retry, and dead-letter counts by stream
- Oldest pending event
- Average delivery delay
- Linked Core entities
- Last reconciliation result

Settings include independent stream controls, coalescing, concurrency, request rate, retry policy, circuit-breaker thresholds, backfill policy, environment, and schema compatibility.

The Core endpoint and signing secret are configured through Secrets & Integrations. Existing plaintext secrets are never displayed here.

## Planned APIs

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

These are planned interfaces.

## Permissions

```text
core_sync.read
core_sync.read_payload
core_sync.configure
core_sync.validate_connection
core_sync.pause_raw
core_sync.pause_canonical
core_sync.retry
core_sync.cancel
core_sync.requeue_dead_letter
core_sync.run_backfill
core_sync.reconcile
core_sync.view_audit
```

Production configuration changes, dead-letter replay, and large backfills require reauthentication and may require a second approval.

## Core requirements

Harvester delivery is safely at least once. Core therefore must provide:

- Durable inbound inbox keyed by event ID
- Payload-hash conflict detection
- Idempotent result replay
- Source schema registry
- Harvester raw-observation and canonical-entity adapters
- Common normalization engine
- Entity candidates
- Identity resolution
- Provenance links
- Field ownership and merge policy
- Safe canonical transaction or durable resumable application boundary
- Applied source-revision tracking

Automatic production delivery must remain disabled until these Core controls and the selected source contracts are integrated and verified.

## Frontend delivery placement

The frontend sequence becomes F1–F17:

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

F14 delivers the dedicated page, raw and canonical stream controls, live queue, event detail, dead-letter recovery, links, backfill, reconciliation, permissions, audit, failure states, and no-secret-leak tests.

## Acceptance criteria

The Harvester integration is not complete until:

1. Every accepted raw observation creates a durable outbound event in the same transaction.
2. Raw observations are published whether or not they represent leads.
3. Organizations, people, locations, and relationships may exist without lead profiles.
4. Exact duplicate observations are idempotent.
5. Changed source records create new immutable observation versions.
6. Observations from different sources remain independently traceable.
7. Every new canonical entity creates an automatic canonical event.
8. Every materially changed canonical entity creates a higher revision and new event.
9. Unchanged canonical projections create no duplicate events.
10. Canonical events reference supporting observations where available.
11. Source connectors do not construct Core-specific Registry payloads independently.
12. Raw and canonical event creation is transactional with local persistence.
13. Retries reuse the exact event ID and payload.
14. New observation versions and canonical revisions receive new event IDs.
15. Per-entity ordering, supersession, and coalescing are deterministic.
16. Core downtime does not stop Harvester ingestion or resolution.
17. Transient failures retry and permanent failures remain reviewable.
18. Circuit breaking and backpressure protect both systems.
19. Pausing a stream loses no data.
20. Live canonical events are prioritized over historical backfill.
21. Core links are stored after canonical application.
22. Reconciliation detects missing events, missing links, revision differences, and payload-hash differences.
23. Raw and canonical streams are independently visible and controllable.
24. Lead qualification remains separate from entity existence and Registry publication.
25. Core provides durable inbox idempotency and safe application boundaries.
26. Secrets never enter payloads, browser persistence, logs, analytics, or audit content.
27. Runtime, outage, recovery, backfill, reconciliation, security, and exact-head CI tests pass.

## Governing principle

> Harvester publishes every accepted raw observation to NEWAX Core's raw-ingestion layer immediately after durable storage. Harvester also publishes every new or materially changed canonical entity after resolution and validation. NEWAX Core owns final normalization and canonical Registry formatting. Lead qualification remains a separate business classification and never determines whether an entity is allowed to exist in the Registry.
