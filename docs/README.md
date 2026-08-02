# Harvester Documentation Map

This directory contains the authoritative product, architecture, and delivery documentation for NEWAX Harvester.

Harvester is standalone lead-intelligence infrastructure. It converts a governed market definition into evidence-backed, reviewable, and operationally usable opportunities while preserving customer ownership and control.

## Authority order

When documents overlap, use this order:

1. [Harvester Standalone Product Roadmap](ROADMAP.md)
   - Authoritative 64-module product and delivery roadmap
   - Module ownership, outcomes, exclusions, acceptance criteria, delivery gates, and crosswalks

2. [Harvester Intelligence Operating Model](architecture/harvester-intelligence-operating-model.md)
   - Normative operating, evidence, data, decision, confidence, learning, economics, and authority model
   - Strengthens the existing 64 modules without creating a second roadmap

3. [NEWAX Harvester Opportunity Scoring Model v3](architecture/opportunity-scoring-model-v3.md)
   - Normative planned opportunity-value, pursuit-readiness, infrastructure-gap, coverage, confidence, risk, and recommendation model
   - Prioritizes confirmed absence and severe weakness of relevant business infrastructure while keeping eligibility and evidence authority separate from points

4. [Standalone Product and Integration Framework](architecture/standalone-product-and-integration-framework.md)
   - Product boundaries, connector framework, credentials, mappings, synchronization, destinations, tenancy, and recovery

5. [Optional NEWAX Core Synchronization](architecture/newax-core-automatic-sync.md)
   - Optional Harvester-to-Core streams, application identity, credentials, delivery, links, reconciliation, and failure behavior

Previous versions remain available through Git history and pull-request history rather than duplicate archive documents inside the active repository.

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
- Opportunity weights, rubrics, infrastructure-gap rules, coverage, confidence, risk, and recommendation changes belong in the Opportunity Scoring Model and require a new approved model version when behavior changes.
- Integration-boundary changes belong in the integration framework or the relevant adapter document.
- Superseded versions remain in Git history rather than duplicate active documentation.
- Do not create parallel roadmaps, duplicate module counts, hidden product dependencies, or competing opportunity-score definitions.
