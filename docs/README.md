# Harvester Documentation Map

Status: **Authoritative documentation index**  
Version: **2.0**  
Date: **6 August 2026**

Harvester is standalone Agency Intelligence Infrastructure. It converts governed provider and client markets into evidence-backed opportunities, market intelligence, competitor intelligence, and controlled outputs while preserving customer ownership, tenant isolation, source rights, and human control.

## 1. Authority order

When documents overlap, apply the first stricter rule in this sequence:

1. [Harvester Standalone Product Roadmap](ROADMAP.md)
   - Authoritative 64-module ownership and delivery roadmap.
   - Module status changes only after implementation and exact-head verification.

2. [Agency Intelligence Re-baseline](architecture/agency-intelligence-rebaseline.md)
   - Approved product and architecture delta.
   - Preserves the 64-module count, standalone boundary, eight-plane architecture, Opportunity Scoring Model v3, and existing taxonomy work.
   - Adds agency and client workspaces, universal entities, governed connectors, sector packs, AI governance, market intelligence, and competitor intelligence.

3. [Harvester Intelligence Operating Model](architecture/harvester-intelligence-operating-model.md)
   - Normative Control, Acquisition, Evidence, Resolution, Intelligence, Decision, Activation, and Operations and Learning model.
   - Defines evidence, confidence, decisions, authority, economics, and learning invariants.

4. [Standalone Product and Integration Framework](architecture/standalone-product-and-integration-framework.md)
   - Product ownership, adapters, credentials, mappings, synchronization, destinations, tenancy, resilience, and recovery.

5. [Provider Portfolio and Lead-Generation Profile Model](architecture/provider-portfolio-and-lead-generation-profile-model.md)
   - Provider organizations, brands and business units, offering portfolios, reusable lead-generation profiles, activation, scheduling, capacity, overlap, and immutable job snapshots.

6. [Universal Entity and Evidence Model](architecture/universal-entity-and-evidence-model.md)
   - Universal entities, identifiers, aliases, relationships, observations, artifacts, excerpts, assertions, claims, coverage, contradictions, resolution, lead profiles, and opportunity hypotheses.

7. [Source Governance and Connector Runtime](architecture/source-governance-and-connector-runtime.md)
   - Source and access classes, purposes, policy versions, credentials, connections, connector contracts, schemas, mappings, rate limits, pricing, execution gates, and restricted-source behavior.

8. [AI Model Gateway and Evaluation](architecture/ai-model-gateway-and-evaluation.md)
   - AI task contracts, provider and model registries, routing, redaction, evidence grounding, structured outputs, evaluations, cost control, human review, and agent isolation.

9. [Agency, Market and Competitor Intelligence Model](architecture/agency-market-and-competitor-intelligence.md)
   - Agency and client workspaces, research projects, markets, categories, competitors, analysis types, intelligence products, case studies, white-label outputs, and outcome learning.

10. [Sector Pack Runtime Model](architecture/sector-pack-runtime-model.md)
    - Universal core plus independently versioned sector packs.
    - Defines the operational Healthcare and Education packs and the runtime path for the remaining sectors.

11. [Harvester Services and Opportunity Model](SERVICES.md)
    - Universal provider, offering, customer-market, lead-subject, signal, qualification, first-page definition, and lawful-contact rules.
    - No active offering means no opportunity assessment.

12. [Opportunity Scoring Model v3](architecture/opportunity-scoring-model-v3.md)
    - Eligibility gates, capability conditions, Opportunity Value, Pursuit Readiness, coverage, confidence, risk, and recommended action.
    - Remains the authoritative scoring direction; current runtime scoring is partial.

13. [Sector, Domain, Activity and Keyword Taxonomy Index](taxonomy/README.md)
    - Canonical sectors, domains, activities, keywords, signals, roles, source guidance, and controlled runtime-delivery references.

14. [Source Input and Formatting Index](sources/README.md)
    - User-input storage, source envelopes, provider-specific formats, adapters, permissions, retention, and acquisition authorities.

15. [Delivery Plans](delivery/README.md)
    - Dependency-ordered implementation and release-verification plans.
    - Delivery plans never independently prove runtime completion.

## 2. Required reading paths

### 2.1 Product or roadmap change

```text
ROADMAP.md
→ agency-intelligence-rebaseline.md
→ owning architecture document
→ delivery implementation sequence
```

### 2.2 Source or connector change

```text
source-governance-and-connector-runtime.md
→ sources/README.md
→ provider-specific source model
→ source-format contract
→ source policy, schema, mapping, test, and delivery records
```

### 2.3 Entity, evidence, or resolution change

```text
harvester-intelligence-operating-model.md
→ universal-entity-and-evidence-model.md
→ current model and migration contracts
→ implementation sequence
```

### 2.4 AI change

```text
ai-model-gateway-and-evaluation.md
→ task-specific contract
→ evidence and data policy
→ evaluation dataset
→ rollout and rollback plan
```

### 2.5 Sector change

```text
sector-pack-runtime-model.md
→ taxonomy/README.md
→ sector domain registry
→ domain-activity mappings
→ keyword and source guidance
→ pack benchmark and policy tests
```

### 2.6 Agency, market, or competitor change

```text
agency-market-and-competitor-intelligence.md
→ provider portfolio and market definition
→ universal entity and evidence model
→ output and activation policies
```

## 3. Current versus planned boundary

Status words are evidence terms:

- **Current:** implemented and verified in the referenced branch.
- **Partial:** useful foundations exist, but the complete governed workflow is not connected.
- **Planned:** architecture or delivery is documented but runtime implementation is absent.
- **Restricted:** disabled until legal, access, privacy, security, commercial, and operational approval exists.
- **Correction required:** existing runtime data or behavior is untrusted until remediation is integrated and executed.

A Markdown object, schema sketch, acceptance criterion, or PR title is not runtime completion.

## 4. Immediate correction authority

Before broad feature expansion, the implementation sequence requires:

1. exact institution linkage for raw page snapshots;
2. detection states that do not convert non-detection into confirmed absence;
3. recomputation and trust marking of affected lead profiles;
4. production disabling of contested professional-network account automation;
5. production authentication and tenant isolation;
6. source-policy execution gating;
7. object-storage evidence retention and access controls.

See [Agency Intelligence Implementation Sequence](delivery/agency-intelligence-implementation-sequence.md).

## 5. Product boundaries

```text
Harvester
Owns standalone agency and provider intelligence, client workspaces,
market definitions, source intake, observations, evidence, local identity,
lead and opportunity intelligence, market and competitor intelligence,
reviews, selections, outputs, publication rules, and operations.

Communicator
Optionally receives approved lead and context packages.
Owns communication profiles, audiences, campaigns, messages,
conversations, consent, engagement, replies, and follow-up.

NEWAX Core
Optionally receives source-native observations, resolved entities,
and approved Harvester-owned facets.
Owns enterprise existence, canonical identity, relationships,
provenance governance, and cross-system identity links.
```

No product shares private tables, database-owner credentials, migrations, internal schemas, or runtime availability.

## 6. Controlled registries

The repository currently documents:

- 16 broad sectors;
- 1,586 canonical product and service domains;
- 519 canonical business activities;
- 1,586 domain keyword profiles;
- 519 activity keyword profiles;
- reusable signal, role, contact, source, exclusion, and evidence-control profiles.

These are documentation datasets until runtime records, migrations, APIs, interfaces, benchmarks, and release verification exist.

## 7. Change-control ownership

- Module ownership, delivery gates, and status belong in `ROADMAP.md`.
- Re-baseline decisions belong in `architecture/agency-intelligence-rebaseline.md`.
- Operating and decision invariants belong in the intelligence operating model.
- Universal identity and evidence semantics belong in the universal entity and evidence model.
- Source permission, connector, pricing, and execution behavior belongs in the source-governance model and applicable provider source documents.
- AI task, provider, model, prompt, routing, evaluation, cost, and review behavior belongs in the AI gateway model.
- Agency, client, market, competitor, analysis, and case-study behavior belongs in the agency intelligence model.
- Sector-specific commercial and compliance depth belongs in versioned sector packs.
- Provider, offering, profile, and market-definition behavior belongs in the provider portfolio and Services models.
- Taxonomy identity belongs under `taxonomy/`; tenant overlays never mutate canonical records.
- Implementation order belongs in `delivery/agency-intelligence-implementation-sequence.md`.

Do not create another parallel roadmap, module count, universal lead definition, scoring authority, or undocumented source behavior.

## 8. Historical documents

Superseded versions remain available through Git and pull-request history. Active directories should contain one current authority for each concern rather than duplicate archives with indistinguishable names.
