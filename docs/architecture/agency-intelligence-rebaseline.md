# Harvester Agency Intelligence Re-baseline

Status: **Normative architecture delta**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned**

## 1. Purpose

This document records the approved re-baseline that evolves Harvester from an institution-focused lead-discovery application into standalone, multi-tenant Agency Intelligence Infrastructure.

It does not replace the authoritative 64-module roadmap. It changes the interpretation and acceptance requirements of the affected modules and provides the cross-document sequence for implementation.

Harvester remains a standalone product. NEWAX Core, Communicator, customer CRMs, advertising systems, warehouses, and other destinations remain optional integrations.

## 2. Product decision

Harvester converts a governed commercial market definition into evidence-backed, reviewable opportunities and controlled intelligence products.

```text
Agency or provider context
→ client workspace
→ active offering
→ governed market definition
→ approved source strategy
→ source-native observations
→ evidence and coverage
→ entity resolution
→ lead and market intelligence
→ qualification and opportunity assessment
→ human or policy decision
→ controlled output or activation
→ outcome feedback
→ governed learning
```

Harvester is not:

- a universal scraper;
- a CRM replacement;
- an autonomous outreach engine;
- a general-purpose data broker;
- a patient-record system;
- a student-information system;
- a collection of unrelated AI prompts.

## 3. Preserved architectural decisions

The re-baseline preserves:

1. Harvester as an independently deployable and resellable product.
2. The eight-plane architecture: Control, Acquisition, Evidence, Resolution, Intelligence, Decision, Activation, and Operations and Learning.
3. Immutable source-native observations and evidence.
4. Separation of resolution, qualification, opportunity scoring, selection, publication approval, and contact eligibility.
5. The Opportunity Scoring Model v3 as the authoritative opportunity model.
6. Versioned sectors, domains, activities, keyword profiles, signals, roles, policies, and job snapshots.
7. Optional adapters for NEWAX Core and Communicator.
8. Customer control over what leaves Harvester.
9. A modular monolith with extractable worker and connector boundaries.
10. Exact-head verification before any delivery is called complete.

## 4. Re-baseline additions

The product now explicitly requires:

- agency tenants and client workspaces;
- provider organizations, business units, brands, portfolios, and versioned offerings;
- universal resolved entities rather than institution-only canonical models;
- live source-permission, terms, pricing, quota, retention, and redistribution governance;
- multi-source Harvest Job orchestration;
- claim, assertion, evidence, coverage, contradiction, and provenance graphs;
- market intelligence and competitor intelligence;
- multi-provider AI task routing, redaction, evaluation, cost accounting, and human-review policy;
- runtime healthcare and education sector packs;
- agency research, reporting, analysis, case-study, and client-delivery workflows;
- shared SaaS, regulated tenant-cell, and dedicated deployment profiles.

## 5. Eight-plane ownership after re-baseline

### 5.1 Control plane

Owns:

- tenants, workspaces, agencies, clients, providers, brands, and business units;
- users, teams, roles, relationships, permissions, entitlements, and quotas;
- offering portfolios and versions;
- lead-generation profiles and market definitions;
- source, evidence, qualification, scoring, compliance, contact, output, and AI policies;
- feature activation and reviewed configuration versions.

### 5.2 Acquisition plane

Owns:

- connection profiles and credential references;
- source plans, connectors, connector capabilities, schemas, mappings, cursors, and checkpoints;
- Harvest Job source runs and stage state;
- rate, quota, cost, concurrency, and regional-egress controls;
- source-native payload capture and failure isolation.

### 5.3 Evidence plane

Owns:

- raw observations;
- snapshots, documents, excerpts, locators, hashes, and storage references;
- evidence assertions and claim links;
- coverage, non-detection, failed inspection, contradictions, freshness, source reliability, and retention;
- transformation and model-execution provenance.

### 5.4 Resolution plane

Owns:

- organizations, people, brands, business units, facilities, locations, products, services, technologies, publications, events, contacts, and relationships;
- resolution candidates, features, conflicts, decisions, reversals, and history;
- Harvester-local entity identity.

### 5.5 Intelligence plane

Owns:

- lead profiles and account dossiers;
- market, category, competitor, product, service, pricing, campaign, technology, and trend intelligence;
- signals, needs, pains, intent, maturity, infrastructure capability, and opportunity hypotheses;
- qualification and Opportunity Scoring Model v3 assessments;
- facts, calculations, model inferences, operator assessments, unknowns, and conflicts as distinct records.

### 5.6 Decision plane

Owns:

- review queues;
- qualification, scoring, attribution, publication, compliance, and repair decisions;
- ranking, saved views, selections, reservations, assignments, approvals, and frozen result snapshots;
- decision records and reviewer rationale.

### 5.7 Activation plane

Owns:

- exports, reports, APIs, webhooks, CRM handoffs, advertising and analytics handoffs, Communicator and Core adapters, and customer destinations;
- publishing rules, payload profiles, redaction, frozen audiences, outbox delivery, receipts, reconciliation, and feedback commands.

### 5.8 Operations and learning plane

Owns:

- health, metrics, alerts, runbooks, quality debt, cost and yield analytics;
- AI and scoring evaluation datasets;
- feedback, drift, model and policy approval, rollout, rollback, backup, restore, release, and upgrade governance.

## 6. Authority sequence

Read and implement documentation in this order:

1. `README.md`
2. `docs/README.md`
3. `docs/ROADMAP.md`
4. `docs/architecture/agency-intelligence-rebaseline.md`
5. `docs/architecture/harvester-intelligence-operating-model.md`
6. `docs/architecture/standalone-product-and-integration-framework.md`
7. `docs/architecture/provider-portfolio-and-lead-generation-profile-model.md`
8. `docs/architecture/universal-entity-and-evidence-model.md`
9. `docs/architecture/source-governance-and-connector-runtime.md`
10. `docs/architecture/ai-model-gateway-and-evaluation.md`
11. `docs/architecture/agency-market-and-competitor-intelligence.md`
12. `docs/architecture/sector-pack-runtime-model.md`
13. `docs/SERVICES.md`
14. `docs/taxonomy/README.md`
15. `docs/sources/README.md`
16. `docs/delivery/README.md`
17. `docs/delivery/agency-intelligence-implementation-sequence.md`

A lower document may add implementation detail but must not weaken a stricter rule in an earlier authority.

## 7. Runtime truth boundary

Documentation status terms remain evidence terms:

- **Current:** implemented and verified in the current branch.
- **Partial:** useful runtime foundations exist, but the complete governed workflow is not connected.
- **Planned:** architecture or delivery work is documented but not implemented.
- **Restricted:** disabled until access, legal, security, privacy, commercial, and operational approval exists.
- **Correction required:** existing runtime data or behavior cannot be trusted until a specified remediation is integrated and executed.

The repository must not describe planned models as implemented merely because their Markdown representation is unusually confident.

## 8. Immediate correction gate

No large feature expansion should precede:

1. exact institution linkage for raw page snapshots;
2. correction of detection-state semantics so non-detection is not confirmed absence;
3. recomputation and trust marking of affected lead profiles;
4. removal or disabling of contested professional-network account automation;
5. production authentication and tenant isolation foundations;
6. source-policy execution gating;
7. object-storage evidence architecture and retention controls.

## 9. Locked re-baseline rule

> Harvester must make evidence-backed commercial intelligence easier to operate without weakening customer ownership, source rights, tenant isolation, explainability, or human control.
