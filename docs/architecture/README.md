# Harvester Architecture Index

Status: **Authoritative architecture-directory index**  
Version: **2.0**  
Date: **6 August 2026**

The repository-wide authority order remains [Harvester Documentation Map](../README.md). The [Documentation Re-baseline Manifest](../documentation-rebaseline-manifest.md) classifies the older Markdown corpus and open documentation work after this re-baseline.

## 1. Re-baseline and operating architecture

1. [Agency Intelligence Re-baseline](agency-intelligence-rebaseline.md)
   - Product delta, preserved decisions, additions, authority sequence, status vocabulary, and correction gate.

2. [Harvester Intelligence Operating Model](harvester-intelligence-operating-model.md)
   - Control, Acquisition, Evidence, Resolution, Intelligence, Decision, Activation, and Operations and Learning planes.

3. [Modular Change-Isolation and Evolution Model](modular-change-isolation-and-evolution-model.md)
   - Module ownership, dependency direction, independent source and sector upgrades, database evolution, contract tests, release composition, and change-impact declarations.
   - This document is introduced by the currently open modular-isolation work and must be rebased against this index before integration.

## 2. Product, provider, and integration boundaries

4. [Standalone Product and Integration Framework](standalone-product-and-integration-framework.md)
   - Independent product ownership, connectors, mappings, synchronization, destinations, tenancy, packaging, and recovery.

5. [Provider Portfolio and Lead-Generation Profile Model](provider-portfolio-and-lead-generation-profile-model.md)
   - Providers, business units, brands, offering portfolios, reusable profiles, activation, schedules, capacity, budgets, overlap, and job snapshots.

6. [Optional NEWAX Core Synchronization](newax-core-automatic-sync.md)
   - Optional source-native observation, resolved-entity, and approved lead-context streams to Core.

## 3. Data, identity, and evidence

7. [Universal Entity and Evidence Model](universal-entity-and-evidence-model.md)
   - Universal entities, identifiers, aliases, relationships, observations, artifacts, excerpts, assertions, claims, coverage, contradictions, provenance, and migration from current institution models.

8. [Keyword and Evidence Profile Integration Addendum](keyword-evidence-profile-integration-addendum.md)
   - Keyword-profile participation in the evidence graph, confidence separation, source suitability, and cross-product boundaries.

## 4. Source and AI governance

9. [Source Governance and Connector Runtime](source-governance-and-connector-runtime.md)
   - Source classes, purposes, policies, credentials, connection profiles, connector contracts, schemas, mappings, rates, pricing, execution gates, and restricted-source controls.

10. [AI Model Gateway and Evaluation](ai-model-gateway-and-evaluation.md)
    - AI tasks, providers, models, prompts, routing, redaction, structured output, grounding, evaluation, cost, review, drift, and agent-runtime isolation.

## 5. Commercial intelligence

11. [Harvester Services and Opportunity Model](../SERVICES.md)
    - Universal offering, customer market, lead subject, signal, qualification, and contact rules.

12. [Agency, Market and Competitor Intelligence Model](agency-market-and-competitor-intelligence.md)
    - Agencies, client workspaces, research projects, markets, categories, competitors, analyses, intelligence products, case studies, and white-label outputs.

13. [Sector Pack Runtime Model](sector-pack-runtime-model.md)
    - Universal core, versioned sector packs, conditional questions, commercial roles, pains, needs, signals, capabilities, and Healthcare and Education operational packs.

14. [Opportunity Scoring Model v3](opportunity-scoring-model-v3.md)
    - Eligibility gates, capability conditions, Opportunity Value, Pursuit Readiness, coverage, confidence, risk, and recommendation.

## 6. Implementation sequence

Architecture delivery follows [Agency Intelligence Implementation Sequence](../delivery/agency-intelligence-implementation-sequence.md).

The locked order is:

```text
Correct integrity
→ tenancy and security
→ governed sources and credentials
→ providers, offerings, profiles, and markets
→ multi-source orchestration
→ universal evidence and identity
→ sector packs
→ opportunity intelligence
→ AI gateway
→ agency, market, and competitor intelligence
→ controlled activation
→ productization and release
```

## 7. Change-isolation rules

- A Healthcare change must not alter Education or another sector pack.
- A provider-specific connector change must not alter unrelated connectors.
- A formatting or frontend change must not change taxonomy, evidence, scoring, or persistence semantics.
- A database-policy change declares contract, migration, backfill, compatibility, and rollback impact.
- A model or prompt change requires task evaluation and reviewed activation.
- A destination change cannot weaken source, consent, suppression, output, or tenant policy.
- A new architecture document must identify its owner, authority relationship, affected modules, and why an existing authority cannot contain the change.

## 8. Status boundary

Architecture documents describe required behavior. They do not prove implementation.

Runtime status remains **Planned** or **Partial** until code, migrations, APIs, interfaces, tests, deployment, and exact-head workflow verification support the claim.
