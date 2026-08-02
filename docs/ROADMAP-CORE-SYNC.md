# Optional NEWAX Core Adapter Roadmap

## Status

Status: **Planned optional integration**

Parent roadmap:

- [`docs/ROADMAP.md`](ROADMAP.md)

This document is a delivery crosswalk for the optional NEWAX Core adapter. It does not create additional top-level Harvester modules.

The previous 9D, 19B, 23B, 33C, 36B, 52B and 63B labels are retired. Their requirements are now incorporated into the authoritative standalone module architecture.

## Product boundary

Harvester operates fully when NEWAX Core is absent, disabled or unavailable.

```text
Harvester local workflow
→ source intake
→ raw evidence
→ Harvester resolution
→ lead intelligence
→ local commit
→ optional Core outbox event
→ asynchronous delivery
```

Core never participates in Harvester's local transaction and never defines Harvester's database schema.

## Authoritative module mapping

| Core-sync concern | Harvester module |
| --- | --- |
| Credentials and signing secrets | Module 09 — Credential Vault and Secret Lifecycle |
| Core connection metadata and access mode | Module 10 — Connection Profiles and Access Modes |
| Adapter capabilities and version | Module 11 — Connector Registry and Capability Framework |
| Core-facing source schemas | Module 12 — Source Schema Registry |
| Source-native outbound mapping | Module 13 — Mapping and Transformation Profiles |
| Durable checkpoints and retry | Module 15 — Synchronization Engine and Checkpoints |
| Reconciliation, backfill and repair | Module 16 — Synchronization Conflicts, Reconciliation and Repair |
| Raw observation source | Module 29 — Raw Observation Store |
| Evidence and provenance projection | Module 31 — Normalized Evidence and Provenance |
| Harvester entity source | Module 33 — Master Lead Registry |
| Optional Core adapter | Module 54 — Optional NEWAX Core Adapter |
| Outbox delivery and command intake | Module 56 — Event Delivery, Feedback and Command Intake |
| Core administration page | Module 58 — Integration Administration UI |
| Compatibility and upgrade policy | Module 63 — Upgrade, Migration and Compatibility Management |
| Security and release verification | Module 64 — Security, Quality and Release Governance |

## Optional streams

### Raw observations

Every accepted source observation may be queued after durable local storage.

### Resolved entities

Every new or materially changed Harvester-resolved organization, person, location, contact or relationship may be queued after resolution and validation.

### Lead context

Selected Harvester-owned qualification, score, opportunity, research or dossier summaries may be published only through an approved payload profile and publishing rule.

Lead context remains a source-owned facet. It is not Core identity truth.

## Delivery requirements

The adapter must provide:

- Independent enable, pause and disable controls
- Source-native versioned payloads
- Stable event identity
- Deterministic payload hashes
- Exact-byte signing
- Idempotent retries
- Per-entity ordering where required
- Dead letter
- Circuit breaker
- Backpressure
- Live-work priority over backfill
- Permanent optional Harvester-to-Core links
- Reconciliation and repair
- Metrics and audit

## Acceptance criteria

The optional Core integration is not complete until:

1. Harvester performs its full local workflow with Core disabled.
2. Core downtime never rolls back or blocks local Harvester commits.
3. Raw, resolved-entity and lead-context streams can be controlled independently.
4. Harvester sends source-native contracts rather than Core database rows.
5. Core performs its own schema validation, normalization, identity resolution, provenance and merge policy.
6. Harvester IDs remain valid before and after a Core link exists.
7. Retries reuse the same event ID and exact serialized payload.
8. A new material revision receives a new event ID.
9. Backfill cannot starve live events.
10. Direct Harvester-to-Communicator operation remains available without Core.
11. Tenant, permission, signing, secret, replay and no-leak tests pass.
12. The exact release commit passes Module 64 verification.

## Implementation sequence

```text
Module 09–13 foundations
→ Module 15–16 synchronization
→ Module 29 and 31 source contracts
→ Module 54 adapter
→ Module 56 delivery and commands
→ Module 58 administration
→ Module 63 compatibility
→ Module 64 release verification
```

No Core-specific work should be embedded into unrelated source connectors, lead scoring, qualification, exports or frontend pages.
