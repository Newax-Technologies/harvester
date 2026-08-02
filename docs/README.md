# Harvester Documentation Map

This directory contains the authoritative product, architecture, delivery, and historical documentation for NEWAX Harvester.

Harvester is standalone lead-intelligence infrastructure. It converts a governed market definition into evidence-backed, reviewable, and operationally usable opportunities while preserving customer ownership and control.

## Authority order

When documents overlap, use this order:

1. [Harvester Standalone Product Roadmap](ROADMAP.md)
   - Authoritative 64-module product and delivery roadmap
   - Module ownership, outcomes, exclusions, acceptance criteria, delivery gates, and crosswalks

2. [Harvester Intelligence Operating Model](architecture/harvester-intelligence-operating-model.md)
   - Normative operating, evidence, data, decision, confidence, learning, economics, and authority model
   - Strengthens the existing 64 modules without creating a second roadmap

3. [Standalone Product and Integration Framework](architecture/standalone-product-and-integration-framework.md)
   - Product boundaries, connector framework, credentials, mappings, synchronization, destinations, tenancy, and recovery

4. [Optional NEWAX Core Synchronization](architecture/newax-core-automatic-sync.md)
   - Optional Harvester-to-Core streams, application identity, credentials, delivery, links, reconciliation, and failure behavior

5. Historical specifications in [`archive/`](archive/)
   - Preserved for context and traceability
   - Not authoritative when they conflict with current documents

## Locked product boundaries

```text
Harvester
Owns market definition, source intake, observations, evidence,
local resolution, lead profiles, qualification, opportunity intelligence,
research, dossiers, selection, exports, publishing rules, and operations.

Communicator
Optionally receives approved lead and context packages.
Owns communication profiles, audiences, campaigns, messages,
conversations, consent, engagement, replies, and follow-up.

NEWAX Core
Optionally receives source-native observations, resolved entities,
and approved Harvester-owned lead facets.
Owns enterprise existence, canonical identity, relationships,
provenance, field governance, and cross-system identity links.
```

No product shares private database tables, database-owner credentials, migrations, internal schemas, or runtime availability.

## Change-control rule

- Product delivery changes belong in `ROADMAP.md`.
- Operating-model and decision-invariant changes belong in the intelligence operating model.
- Integration-boundary changes belong in the integration framework or the relevant adapter document.
- Historical documents remain archived rather than silently rewritten into apparent current authority.
- Do not create parallel roadmaps, duplicate module counts, or hidden product dependencies.
