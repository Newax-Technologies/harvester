# Harvester Architecture Index

This directory contains Harvester's active architecture and operating-model documents.

The [Harvester Documentation Map](../README.md) remains authoritative for the repository-wide document order. The documents below must be read within that hierarchy.

## Core architecture

- [Harvester Intelligence Operating Model](harvester-intelligence-operating-model.md)
  - Evidence, decisions, confidence, authority, learning, operations and module invariants.

- [Modular Change-Isolation and Evolution Model](modular-change-isolation-and-evolution-model.md)
  - Independently versioned sector packs, source adapters, policies, persistence, presentation and destinations.
  - Defines public contracts, dependency direction, upgrade isolation, database evolution, testing boundaries, release composition and change-impact declarations.

- [Provider Portfolio and Lead-Generation Profile Model](provider-portfolio-and-lead-generation-profile-model.md)
  - Provider organizations, business units, portfolios, reusable profile versions, activation, scheduling, capacity and overlap.

- [Opportunity Scoring Model v3](opportunity-scoring-model-v3.md)
  - NEWAX-specific opportunity value, pursuit readiness, confidence, coverage and risk profile.

## Product and integration boundaries

- [Standalone Product and Integration Framework](standalone-product-and-integration-framework.md)
  - Standalone product ownership, adapters, credentials, mappings, synchronization and recovery.

- [Optional NEWAX Core Synchronization](newax-core-automatic-sync.md)
  - Optional Harvester-to-Core streams, credentials, delivery, reconciliation and failure behaviour.

## Locked evolution rule

A change must remain inside its owning module unless an explicit public-contract dependency proves that another module is affected.

Examples:

- Healthcare changes must not alter Education or other sector packs.
- LinkedIn changes must not alter Google, Yandex or other source adapters.
- Formatting changes must not alter taxonomy, evidence, scoring or persistence rules.
- Database-policy changes must not silently alter source behaviour, sector meaning or interface presentation.

Every change must identify its module owner, affected contracts, migration requirements, compatibility, tests and rollback or recovery path.
