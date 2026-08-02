# Optional NEWAX Core Synchronization

Status: **Planned optional integration**

## 1. Product boundary

Harvester is a standalone product. NEWAX Core synchronization is an optional destination adapter.

Harvester continues to collect, store, resolve, qualify, score, research, export, and serve leads when Core is disabled or unavailable.

```text
Harvester local transaction
→ commit observation or canonical change
→ create local outbox event when Core sync is enabled
→ deliver asynchronously
```

Core never participates in Harvester's local transaction and never defines Harvester's internal schema.

Read first:

- [Standalone Product and Integration Framework](standalone-product-and-integration-framework.md)
- [Standalone Product Roadmap](../ROADMAP-STANDALONE-PRODUCT.md)
- [Detailed historical Core-sync specification](../archive/newax-core-automatic-sync-detailed.md)

## 2. Two optional streams

When the Core integration is configured and enabled, Harvester may publish two independent streams.

### Raw observation stream

Every accepted source observation may be queued after durable local storage.

```text
BEGIN
Persist source-native observation
Create RAW_OBSERVATION outbox event
COMMIT
```

Raw observations may concern:

- Organizations
- People
- Locations
- Contact methods
- Domains
- Websites
- Relationships
- Documents
- Social profiles
- Unknown subjects

Lead qualification does not control raw publication. A company or person remains an entity even when it is not commercially useful.

### Canonical entity stream

Every new or materially changed Harvester-resolved entity may be queued after resolution and validation.

```text
BEGIN
Create or update Harvester canonical entity
Increase local revision
Build source-native projection
Calculate deterministic hash
Create CANONICAL_ENTITY outbox event when materially changed
COMMIT
```

Canonical events may cover organizations, people, locations, contacts, and relationships.

## 3. Lead context is separate

Harvester may optionally publish a third source-owned facet or payload profile containing selected lead interpretation:

- Qualification result
- Lead score
- Opportunity summary
- Research summary
- Freshness and confidence
- Dossier reference

Lead context is not Core identity truth. It remains owned by Harvester and can be updated or removed according to the integration contract.

## 4. Source-native envelope

Harvester sends a common outer envelope with a Harvester-native payload:

```json
{
  "integration_version": 1,
  "event_id": "unique-event-id",
  "event_type": "harvester.observation.recorded",
  "source_system": "harvester",
  "source_schema": "harvester.observation.v1",
  "occurred_at": "ISO-8601 timestamp",
  "tenant_reference": "tenant-identifier",
  "entity_reference": "source-entity-id",
  "correlation_id": "optional-workflow-id",
  "causation_id": "optional-causing-event-id",
  "payload_checksum": "sha256",
  "payload": {}
}
```

Harvester does not format the payload as Core Prisma rows or Registry service arguments.

Core owns:

- Core schema validation
- Core source adapter
- Core normalization
- Core entity candidates
- Core identity resolution
- Core provenance
- Core field ownership and merge policy
- Core canonical writes

## 5. Independent identifiers

Harvester keeps its local IDs.

Core may return a permanent optional link:

```text
Harvester entity ID ↔ Core entity ID
```

A missing Core link never makes the Harvester entity unusable.

Suggested link fields:

```text
harvester_entity_type
harvester_entity_id
core_entity_type
core_entity_id
last_event_id
last_local_revision
last_projection_hash
last_applied_at
last_reconciled_at
status
```

## 6. Outbox streams

The existing `EventOutbox` should be evolved rather than replaced.

```text
RAW_OBSERVATION
CANONICAL_ENTITY
LEAD_CONTEXT
RECONCILIATION
BACKFILL
```

Every retry reuses the same event ID and exact serialized payload. A new source version or local canonical revision receives a new event ID.

Recommended delivery priority:

```text
1. Live canonical changes
2. Recent raw observations
3. Lead-context updates
4. Reconciliation and repair
5. Historical backfill
```

## 7. Delivery worker

The Core delivery worker provides:

- Concurrency-safe claims
- Per-entity ordering where required
- Exact-byte request signing
- Retry classification
- Exponential backoff and jitter
- Dead letter
- Circuit breaker
- Backpressure
- Destination health
- Core link updates
- Delivery metrics

The worker is independently pausable. Pausing delivery never pauses harvesting or local outbox creation.

## 8. Core outage behavior

When Core is unavailable:

- Harvester continues ingesting.
- Raw observations continue being stored.
- Canonical resolution continues.
- Qualification and scoring continue.
- Exports and direct Communicator publication continue.
- Core outbox events accumulate safely.
- Retry and circuit-breaker rules protect both systems.

After recovery, live events take priority over historical backfill.

## 9. Direct Communicator mode remains available

Core is not required between Harvester and Communicator.

```text
Harvester publishing rule
→ Harvester-to-Communicator adapter
→ Communicator mapping and normalization
```

The customer may choose:

- Direct Communicator integration
- Core integration
- Both
- Neither

Each destination has independent credentials, mappings, publishing rules, outbox state, retry history, links, and reconciliation.

## 10. Dedicated page

Route:

```text
/integrations/newax-core
```

Tabs:

```text
Overview
Raw Observations
Canonical Entities
Lead Context
Delivery Queue
Dead Letter
Entity Links
Backfill
Reconciliation
Settings
```

Controls:

```text
Integration enabled or disabled
Raw observation stream enabled or disabled
Canonical entity stream enabled or disabled
Lead-context stream enabled or disabled
Delivery paused or running
Backfill paused or running
```

The page shows connection state, contracts, schema versions, queue depth, oldest pending event, delivery latency, retries, dead letter, links, and reconciliation.

Secrets are managed through the general credential system and never displayed here.

## 11. Core prerequisites

Production activation remains blocked until Core provides:

- Durable event-ID inbox
- Same-ID/different-payload conflict detection
- Idempotent response replay
- Source schema registry
- Harvester adapters
- Raw event preservation
- Core normalization and candidate models
- Identity resolution
- Provenance
- Field ownership and merge policy
- Safe canonical write boundary
- Source facets
- Reprocessing and reconciliation
- Tenant-scoped service identity and permissions

## 12. Security

- Dedicated service identity per installation and environment
- Tenant-scoped permissions
- HMAC or asymmetric signatures
- Timestamp and replay validation
- Payload hashes
- TLS validation
- Rate and batch limits
- Secret references rather than plaintext settings
- No browser access to signing secrets
- No direct Registry-table writes
- Audit without unrestricted raw personal data

## 13. Acceptance criteria

The optional integration is not complete until:

1. Harvester works normally with Core disabled.
2. Core downtime does not block local Harvester work.
3. Raw and canonical streams can be controlled independently.
4. Lead qualification does not gate entity publication.
5. Source-native payloads are preserved.
6. Retries use the same event ID and bytes.
7. New source or canonical revisions use new event IDs.
8. Duplicate and stale events are handled idempotently.
9. Core links are optional and permanent when present.
10. Direct Harvester-to-Communicator mode works without Core.
11. Backfill cannot starve live delivery.
12. Dead-letter and reconciliation are operator-visible.
13. Secrets remain encrypted and write-only.
14. Tenant and installation identities are verified.
15. Exact-head runtime, security, failure-recovery, and CI checks pass before activation.

## 14. Locked rule

> Harvester may publish raw observations, resolved entities, and selected lead context to NEWAX Core, but Core synchronization is always optional and never changes Harvester's independent product ownership or formatting.