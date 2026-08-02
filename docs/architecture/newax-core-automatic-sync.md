# Optional NEWAX Core Synchronization

Status: **Planned optional integration**

## 1. Product boundary

Harvester is a standalone product. NEWAX Core synchronization is an optional destination adapter governed by Modules 09–16, 29, 31, 33, 54, 56, 58, 63, and 64 in the authoritative roadmap.

Harvester continues to collect, store, resolve, qualify, score, research, export, and serve leads when Core is absent, disabled, paused, or unavailable.

```text
Harvester local transaction
→ commit source-native observation or resolved-entity change
→ create local outbox event when Core sync is enabled
→ deliver asynchronously through the optional Core adapter
```

Core never participates in Harvester's local transaction and never defines Harvester's internal schema.

Read first:

- [Authoritative Harvester Roadmap](../ROADMAP.md)
- [Standalone Product and Integration Framework](standalone-product-and-integration-framework.md)
- [Detailed historical Core-sync specification](../archive/newax-core-automatic-sync-detailed.md)

## 2. Three independently controlled streams

When the Core integration is configured and enabled, Harvester may publish three independent streams.

### 2.1 Raw observation stream

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

### 2.2 Resolved-entity stream

Every new or materially changed Harvester-resolved entity may be queued after local resolution and validation.

```text
BEGIN
Create or update Harvester resolved entity
Increase local revision
Build source-native projection
Calculate deterministic hash
Create RESOLVED_ENTITY outbox event when materially changed
COMMIT
```

Resolved-entity events may cover organizations, people, locations, contacts, and relationships.

Harvester owns these local resolved records. NEWAX Core independently determines canonical identity, relationships, provenance, source facets, field ownership, and merge policy. Harvester must not describe its own records as Core canonical truth.

### 2.3 Lead-context stream

Harvester may publish selected Harvester-owned lead interpretation through an approved publishing rule and payload profile:

- Qualification result
- Lead score
- Opportunity summary
- Research summary
- Freshness and confidence
- Dossier reference
- Approved service-gap or operational-need summaries

Lead context is not Core identity truth. It remains a Harvester-owned source facet and can be updated, superseded, or removed according to the integration contract.

## 3. Core developer application and credential lifecycle

Every Harvester installation and environment connecting to Core receives its own registered Core application identity. Harvester must never share one universal Core key with Communicator, another tenant, or another environment.

Recommended registration structure:

```text
Core developer application
→ Harvester product installation
→ environment-specific credential
→ bounded application principal
```

Example identities:

```text
Harvester Customer A Production
Harvester Customer A Staging
Harvester NEWAX Managed Production
```

Core may support one or more approved authentication methods by deployment profile:

- API key for bounded server-to-server use
- OAuth 2.0 client credentials with short-lived access tokens
- Signed JWT service authentication
- Mutual TLS for higher-assurance enterprise installations
- Separate webhook-signing credentials for Core callbacks

The preferred production flow is:

```text
Harvester installation credential
→ Core token exchange
→ short-lived access token
→ tenant, environment, audience, scope, and restriction validation
→ authorized Core endpoint
```

Permanent secrets are displayed once, stored only through secure secret handling, never returned to the browser, and never written to logs.

## 4. Application scopes and restrictions

The Harvester Core application principal must be least-privilege and explicitly restricted.

Possible Harvester scopes include:

```text
core.observations.publish
core.entities.propose
core.facets.write
core.identity-links.read
core.identity-links.write
core.delivery.receipts.read
core.commands.read
```

The final scope registry is owned and versioned by Core. Harvester must not assume a scope exists merely because a similarly named endpoint answers politely.

Credential and token restrictions may include:

```text
Core application ID
Product installation ID
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
Daily quota
Credential expiry
Token lifetime
```

Authentication success never bypasses Core domain authorization, identity resolution, field ownership, or merge policy.

## 5. Capability negotiation

Before activation and periodically thereafter, Harvester discovers or validates Core capabilities.

The capability snapshot should include:

- Supported integration and schema versions
- Accepted event types
- Required scopes
- Maximum request and batch sizes
- Token and signature requirements
- Idempotency behavior
- Rate and quota limits
- Receipt and acknowledgement support
- Command and feedback support
- Backfill constraints
- Deprecation dates

A materially incompatible capability change blocks new delivery safely and creates an operator-visible compatibility issue. It must not silently reinterpret queued payloads.

## 6. Source-native envelope

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
  "installation_reference": "harvester-installation-id",
  "entity_reference": "source-entity-id",
  "correlation_id": "optional-workflow-id",
  "causation_id": "optional-causing-event-id",
  "payload_checksum": "sha256",
  "payload": {}
}
```

Harvester does not format the payload as Core database rows, ORM models, or Registry service arguments.

Core owns:

- Core application and token validation
- Core schema validation
- Core source adapter
- Core normalization
- Core entity candidates
- Core identity resolution
- Core provenance
- Core source facets
- Core field ownership and merge policy
- Core canonical writes

## 7. Independent identifiers and optional links

Harvester keeps its local IDs before, during, and after Core integration.

Core may return a permanent optional link:

```text
Harvester entity ID ↔ Core entity ID
```

A missing, revoked, stale, or unresolved Core link never makes the Harvester entity unusable.

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

## 8. Outbox streams and event identity

The existing `EventOutbox` should be evolved rather than replaced.

```text
RAW_OBSERVATION
RESOLVED_ENTITY
LEAD_CONTEXT
RECONCILIATION
BACKFILL
```

Every retry reuses the same event ID and exact serialized payload. A new source version or materially changed local resolved-entity revision receives a new event ID.

Recommended delivery priority:

```text
1. Live resolved-entity changes
2. Recent raw observations
3. Lead-context updates
4. Reconciliation and repair
5. Historical backfill
```

## 9. Delivery worker

The Core delivery worker provides:

- Concurrency-safe claims
- Per-entity ordering where required
- Short-lived token acquisition and refresh
- Exact-byte request signing where required
- Retry classification
- Exponential backoff and jitter
- Dead letter
- Circuit breaker
- Backpressure
- Rate and quota enforcement
- Destination health
- Core-link updates
- Delivery receipts
- Delivery metrics and audit

The worker is independently pausable. Pausing delivery never pauses harvesting, local resolution, or local outbox creation.

Revoked, expired, wrong-environment, wrong-tenant, or insufficient-scope credentials fail closed and create actionable operator-visible errors.

## 10. Core outage and credential-failure behavior

When Core is unavailable or access is temporarily invalid:

- Harvester continues ingesting.
- Raw observations continue being stored.
- Local entity resolution continues.
- Qualification and scoring continue.
- Exports and direct Communicator publication continue.
- Core outbox events accumulate safely.
- Retry and circuit-breaker rules protect both systems.
- Credential or token failures do not erase queued work.

After recovery, live events take priority over historical backfill.

Credential rotation supports controlled overlap:

```text
Old credential active
→ new credential issued and validated
→ Harvester switches safely
→ old credential revoked
```

A failed replacement leaves the previously active credential usable until an authorized operator resolves the problem or explicitly revokes it.

## 11. Direct Communicator mode remains available

Core is not required between Harvester and Communicator.

```text
Harvester publishing rule
→ direct Harvester-to-Communicator adapter
→ Communicator mapping and normalization
```

The customer may choose:

- Direct Communicator integration
- Core integration
- Both
- Neither

Each destination has independent application identities or credentials, mappings, publishing rules, outbox state, retry history, links, and reconciliation.

## 12. Administration experience

Primary route:

```text
/integrations/newax-core
```

Related general administration:

```text
/settings/connections
/settings/credentials
/settings/source-schemas
/settings/mappings
/settings/synchronization
```

Core integration tabs:

```text
Overview
Application Identity
Capabilities
Raw Observations
Resolved Entities
Lead Context
Delivery Queue
Dead Letter
Entity Links
Backfill
Reconciliation
Usage and Quotas
Audit
Settings
```

Controls:

```text
Integration enabled or disabled
Raw-observation stream enabled or disabled
Resolved-entity stream enabled or disabled
Lead-context stream enabled or disabled
Delivery paused or running
Backfill paused or running
Credential rotation
Emergency application disablement
```

The page shows connection state, application and installation identity, credential fingerprint, granted scopes, restrictions, capability versions, queue depth, oldest pending event, delivery latency, retries, dead letter, links, quota state, and reconciliation.

Secrets are managed through the general credential system and never displayed after initial issuance.

## 13. Core prerequisites

Production activation remains blocked until Core provides:

- Developer application registry
- Product-installation identities
- Environment-specific credential issuance
- Secure API-key verification where enabled
- OAuth client-credential token exchange and short-lived tokens where enabled
- Scope registry and application-principal authorization
- Tenant, environment, audience, endpoint, entity, and field restrictions
- Credential rotation, expiry, revocation, and emergency disablement
- Usage accounting, quotas, rate limits, and audit
- Separate webhook-signing credential management
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

## 14. Security requirements

- Dedicated Core application and installation identity per tenant and environment
- Least-privilege scopes and deny-by-default authorization
- Short-lived access tokens for production service access where supported
- HMAC, asymmetric signatures, or mTLS according to the approved profile
- Separate inbound API and outbound webhook credentials
- Timestamp, nonce, and replay validation
- Payload hashes and exact-byte signing
- TLS validation and approved network destinations
- IP, origin, region, audience, endpoint, entity, and field restrictions where required
- Rate and batch limits
- Secret references rather than plaintext settings
- One-time display for permanent secrets
- Credential rotation and immediate revocation
- No browser access to service or signing secrets
- No direct Registry-table writes
- Authorization-header and secret redaction in logs and traces
- Audit without unrestricted raw personal data

## 15. Acceptance criteria

The optional integration is not complete until:

1. Harvester works normally with Core absent or disabled.
2. Core downtime does not block local Harvester work.
3. Raw-observation, resolved-entity, and lead-context streams can be controlled independently.
4. Lead qualification does not gate entity publication.
5. Source-native payloads are preserved.
6. Harvester resolved entities are not represented as Core canonical truth.
7. Retries use the same event ID and exact serialized bytes.
8. New source or resolved-entity revisions use new event IDs.
9. Duplicate and stale events are handled idempotently.
10. Core links are optional and permanent when present.
11. Direct Harvester-to-Communicator mode works without Core.
12. Backfill cannot starve live delivery.
13. Dead-letter and reconciliation are operator-visible.
14. Every installation and environment has its own Core application identity and credential lifecycle.
15. Harvester and Communicator cannot share one universal Core credential.
16. Scopes, tenant, environment, audience, endpoint, IP, entity, field, rate, quota, expiry, and revocation restrictions are enforced.
17. Permanent secrets remain non-retrievable after issuance.
18. Credential rotation supports overlap without losing queued work.
19. Revoked credentials and replayed events fail closed.
20. Exact-head runtime, security, failure-recovery, compatibility, and CI checks pass before activation.

## 16. Locked rule

> Harvester may publish raw observations, locally resolved entities, and selected lead context to NEWAX Core through its own registered application identity, but Core synchronization is always optional and never changes Harvester's independent product ownership, identifiers, transactions, or formatting.
