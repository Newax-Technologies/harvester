# Harvester Keyword Documentation Sequence and Connection Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Documentation integrated; runtime not implemented**

This document defines the authoritative reading order, dependency order, runtime connection chain, ownership boundaries, and delivery sequence for the Harvester sector, domain, activity, keyword, provider-offering, source, evidence, opportunity, and lawful-contact documentation.

It does not replace the Harvester roadmap, operating model, services model, provider-portfolio model, taxonomy registries, source models, scoring profiles, or delivery addenda. It connects them in one controlled sequence so the same concept is not redefined in several places.

---

## 1. Intended outcome

A provider must be able to define exactly which organizations are relevant, what those organizations do, which provider services may apply, which evidence may support relevance, and when a candidate may become an opportunity or contact-ready lead.

The complete governed chain is:

```text
Provider organization
→ provider business unit
→ active provider offering
→ lead-generation profile
→ selected broad sector
→ selected product or service domain
→ approved activity for that domain
→ domain identity keyword profile
→ activity keyword profile
→ organization cues and exclusions
→ offering-specific problem, intent, event and technology profiles
→ approved source classes
→ source-specific query composition
→ immutable source observations
→ entity resolution
→ domain and activity classification
→ freshness, contradiction and duplicate-origin review
→ qualification
→ supported opportunity
→ responsible-function assessment
→ lawful contact readiness
→ approved publication, export or communication package
```

No later stage may silently bypass an earlier eligibility, evidence, review, consent, suppression, or policy gate.

---

## 2. Authority order

When documents overlap, apply this order:

1. [Harvester Standalone Product Roadmap](../../ROADMAP.md)
   - Authoritative 64-module delivery roadmap.
2. [Harvester Intelligence Operating Model](../../architecture/harvester-intelligence-operating-model.md)
   - Evidence, resolution, decisions, confidence, learning, economics and operating invariants.
3. [Harvester Services and Opportunity Model](../../SERVICES.md)
   - Universal provider, offering, target-market, opportunity and qualification rules.
4. [Provider Portfolio and Lead-Generation Profile Model](../../architecture/provider-portfolio-and-lead-generation-profile-model.md)
   - Provider portfolios, business units, reusable profiles, activation, schedules, budgets and jobs.
5. [Sector, Domain, Activity and Keyword Taxonomy Index](../README.md)
   - Controlled classification registries and mappings.
6. [Keyword Taxonomy and Lead-Signal Index](README.md)
   - Controlled keyword, signal, role, source, query and validation layers.
7. Source-specific models under [`docs/sources/`](../../sources/README.md)
   - Approved acquisition, extraction, retention and provider-policy behavior.
8. Provider-specific scoring profiles
   - Apply only to explicitly selected providers and offerings.
9. Delivery and implementation addenda
   - Define how approved documentation becomes runtime behavior without creating a second roadmap.

A lower document may deepen an approved rule. It may not weaken or replace a higher-order invariant.

---

## 3. Documentation reading sequence

### Sequence A — Product and authority foundation

Read first:

1. `docs/ROADMAP.md`
2. `docs/architecture/harvester-intelligence-operating-model.md`
3. `docs/SERVICES.md`
4. `docs/architecture/provider-portfolio-and-lead-generation-profile-model.md`

These documents answer:

- What Harvester owns.
- Who the provider is.
- Which services are offered.
- Which target profiles may be activated.
- What an opportunity means.
- Which evidence and decision boundaries must remain separate.

### Sequence B — Market classification

Read next:

1. `docs/taxonomy/broad-sector-registry.md`
2. The selected sector domain registry.
3. `docs/taxonomy/activity-registry.md`
4. The selected sector's domain-to-activity mapping.

These documents answer:

- Which broad market is selected.
- Which product or service domains exist inside it.
- Which activities may apply to each domain.
- Which activity selections remain independent.

### Sequence C — Domain and activity discovery

Read next:

1. `docs/taxonomy/keywords/control-profiles.md`
2. `docs/taxonomy/keywords/activity-keywords-part-1.md`
3. `docs/taxonomy/keywords/activity-keywords-part-2.md`
4. `docs/taxonomy/keywords/activity-keywords-part-3.md`
5. The selected sector's domain keyword registry.

These documents answer:

- Which terms identify a domain.
- Which terms indicate an activity.
- Which organization cues improve precision.
- Which exclusions and negative contexts must be evaluated.

### Sequence D — Offering-specific commercial relevance

Read next:

1. `docs/taxonomy/keywords/provider-offering-keyword-profile-standard.md`
2. `docs/taxonomy/keywords/deep-keyword-pack-registry.md`
3. `docs/taxonomy/keywords/lead-generation-signal-registry.md`
4. `docs/taxonomy/keywords/sector-lead-generation-overlays.md`
5. `docs/taxonomy/keywords/decision-maker-and-contact-cues.md`

These documents answer:

- Why a target may matter now.
- Which active offering makes the evidence commercially relevant.
- Which problem, intent, procurement, event, replacement, integration, expansion or technology signals apply.
- Which responsible function may own the issue.

### Sequence E — Source and query execution

Read next:

1. `docs/taxonomy/keywords/source-signal-matrix.md`
2. `docs/taxonomy/keywords/source-query-template-library.md`
3. `docs/taxonomy/keywords/query-composition-and-evidence-rules.md`
4. `docs/taxonomy/keywords/keyword-expansion-and-composition-engine.md`
5. `docs/taxonomy/keywords/semantic-entity-and-classification-expansion.md`
6. The applicable source model under `docs/sources/`.

These documents answer:

- Which sources are suitable for which signals.
- Which query family may be used.
- How positive and negative queries are composed.
- How geography, locale, semantic expansion, entities and classification systems are controlled.

### Sequence F — Evidence, qualification and validation

Read next:

1. `docs/architecture/keyword-evidence-profile-integration-addendum.md`
2. `docs/taxonomy/keywords/keyword-quality-and-review-standard.md`
3. `docs/taxonomy/keywords/benchmark-and-gold-set-standard.md`
4. `docs/taxonomy/keywords/keyword-validation-plan.md`
5. `docs/taxonomy/keywords/ultimate-depth-coverage-matrix.md`

These documents answer:

- How keyword matches enter the evidence graph.
- How context, source suitability, contradiction, freshness and duplicate origin affect confidence.
- Which benchmark and review evidence is required before activation.
- Which parts are defined, reviewed, partial, blocked or unimplemented.

### Sequence G — Runtime implementation and delivery

Read last:

1. `docs/taxonomy/keywords/keyword-profile-implementation-plan.md`
2. `docs/delivery/keyword-profile-delivery-addendum.md`
3. `docs/taxonomy/keywords/01-sector-keyword-connection-matrix.md`

These documents answer:

- Which runtime objects, APIs, interfaces and snapshots are required.
- Which existing roadmap modules own each implementation slice.
- Which sector-specific files must be imported and connected.
- Which verification gates define completion.

---

## 4. Runtime connection contract

### 4.1 Provider and offering gate

A target configuration is not commercially complete until it references:

```text
provider_id
business_unit_id where applicable
active_service_offering_id
lead_generation_profile_version_id
```

An inactive, paused, archived, superseded or unselected offering cannot contribute service-specific intent, problem, competitor, existing-solution, gap or opportunity logic.

### 4.2 Sector gate

A selected broad sector controls which domain registries are presented.

```text
BroadSectorSelection
→ approved DomainSelection records
```

Broad-sector selection does not automatically activate every domain.

### 4.3 Domain gate

Every selected domain must retain:

```text
domain_id
domain_registry_version
domain_keyword_profile_version
sector_mapping_version
status
priority
```

The same canonical domain may appear under several sectors without becoming several identities.

### 4.4 Activity gate

Activities come from the shared canonical library, but each domain has its own applicability and user selection.

```text
DomainSelection
→ DomainActivityApplicability
→ approved TargetDomainActivity
```

Selecting `Manufacturing` for Pharmaceuticals does not activate it for Medical Devices, Food Products, Textiles or any other domain.

### 4.5 Keyword gate

The query definition combines independently versioned profiles:

```text
DomainKeywordProfile
+ ActivityKeywordProfile
+ OrganizationCueProfile
+ ExclusionProfile
+ LocaleKeywordPack
```

These profiles discover and classify evidence. They do not independently prove a service need or opportunity.

### 4.6 Offering-signal gate

Commercial relevance is evaluated only through the selected offering:

```text
active offering
+ problem profile
+ buying-intent profile
+ procurement profile
+ event profile
+ technology profile
+ competitor profile
+ existing-solution profile
+ replacement/integration/expansion profile
```

The same organization may be relevant for one active offering and irrelevant for another.

### 4.7 Source gate

Each query must retain:

```text
source_class
source_model_version
query_family
query_template_version
geography
language and locale
terms and pack origins
negative-query version
execution limits
```

A source may be suitable for organization identity but unsuitable for buying intent, authority, absence or contact readiness.

### 4.8 Evidence gate

A keyword match produces an observation, not a decision.

```text
KeywordMatchEvidence
→ context extraction
→ source suitability
→ entity resolution
→ classification
→ signal assessment
→ contradiction review
→ freshness review
→ duplicate-origin review
→ confidence dimensions
```

Raw match counts must not become qualification or opportunity scores.

### 4.9 Opportunity gate

A supported opportunity requires:

```text
resolved organization
+ approved target profile
+ active offering
+ sufficient evidence
+ adequate coverage
+ no unresolved material contradiction
+ applicable qualification rules
+ provider capacity and policy eligibility
```

“Not found” is not “absent” without adequate coverage.

### 4.10 Contact-readiness gate

Responsible-role and public-contact discovery occurs after organization resolution and supported opportunity assessment.

Contact-ready status additionally requires:

```text
lawful or authorized route
+ consent or permitted basis where required
+ suppression check
+ conflict check
+ channel policy
+ jurisdiction policy
+ tenant policy
+ current contact evidence
```

A title match does not prove authority. A public address does not create consent.

---

## 5. Object and file ownership map

| Concept | Authoritative documentation |
| --- | --- |
| Provider and offering eligibility | `docs/SERVICES.md` |
| Provider portfolio, business units and profile activation | `docs/architecture/provider-portfolio-and-lead-generation-profile-model.md` |
| Broad sectors | `docs/taxonomy/broad-sector-registry.md` |
| Domain definitions | Sector domain registry files under `docs/taxonomy/` |
| Canonical activities | `docs/taxonomy/activity-registry.md` and linked files |
| Domain-to-activity applicability | Sector mapping files linked by `activity-registry.md` |
| Domain keyword profiles | Sector keyword registry files under `docs/taxonomy/keywords/` |
| Activity keyword profiles | `activity-keywords-part-1.md` through `part-3.md` |
| Organization and exclusion profiles | `control-profiles.md` |
| Offering-specific keyword behavior | `provider-offering-keyword-profile-standard.md` |
| Reusable lead signals | `lead-generation-signal-registry.md` |
| Sector signal adjustments | `sector-lead-generation-overlays.md` |
| Role and contact cues | `decision-maker-and-contact-cues.md` |
| Source suitability | `source-signal-matrix.md` and source-specific models |
| Query templates | `source-query-template-library.md` |
| Query composition | `query-composition-and-evidence-rules.md` and `keyword-expansion-and-composition-engine.md` |
| Entity and classification expansion | `semantic-entity-and-classification-expansion.md` |
| Evidence-graph integration | `docs/architecture/keyword-evidence-profile-integration-addendum.md` |
| Benchmarks and activation thresholds | `benchmark-and-gold-set-standard.md` |
| Validation execution | `keyword-validation-plan.md` |
| Implementation sequence | `keyword-profile-implementation-plan.md` |
| Delivery gates | `docs/delivery/keyword-profile-delivery-addendum.md` |
| Coverage and remaining work | `ultimate-depth-coverage-matrix.md` |

No file may redefine a concept owned by another file merely to make local reading convenient. It may reference the authoritative definition and add scoped detail.

---

## 6. Required version snapshot

Every activated profile and every Harvest Job must preserve the exact versions used:

```text
provider_version
business_unit_version
offering_version
lead_generation_profile_version
broad_sector_version
domain_version
sector_domain_mapping_version
domain_activity_assignment_version
activity_version
domain_keyword_profile_version
activity_keyword_profile_version
organization_cue_profile_version
exclusion_profile_version
offering_signal_profile_versions
sector_overlay_version
role_profile_version
contact_route_profile_version
source_suitability_profile_version
source_model_version
locale_pack_version
query_template_version
query_composition_version
semantic_model_version
classification_crosswalk_version
evidence_policy_version
qualification_version
scoring_profile_version
contact_policy_version
```

Later edits apply only to future jobs unless an operator explicitly creates a replacement job.

---

## 7. Implementation sequence

The sequence strengthens existing roadmap modules and does not create another top-level module count.

### Stage 1 — Registry integrity

- Import and validate 16 broad sectors.
- Import and validate 1,586 canonical domains.
- Import and validate 519 canonical activities.
- Import all explicit domain-to-activity assignments.
- Import all separate domain and activity keyword profiles.
- Validate stable codes, uniqueness and references.

### Stage 2 — Provider and offering configuration

- Persist providers, business units and complete offering portfolios.
- Require active offering selection before service-specific signals.
- Persist reusable lead-generation profiles and immutable versions.

### Stage 3 — Guided market definition

- Select sectors.
- Select domains per sector.
- Select activities independently per domain.
- Review domain, activity, organization and exclusion profiles.
- Prevent automatic propagation across domains.

### Stage 4 — Offering signal configuration

- Attach only offering-relevant problem, intent, procurement, technology, event, competitor and existing-solution profiles.
- Add sector overlays without replacing offering logic.
- Preview positive and negative examples.

### Stage 5 — Source and query planning

- Select approved source classes.
- Apply source-specific templates and limits.
- Compose positive and negative query families.
- Apply geography, language and locale packs.
- Preserve query provenance and breadth warnings.

### Stage 6 — Evidence capture and resolution

- Store immutable source observations.
- Store match spans, context, source, time and profile versions.
- Resolve organizations and aliases.
- Prevent mirrored or copied sources from inflating corroboration.

### Stage 7 — Classification and opportunity assessment

- Classify domain and activity separately.
- Evaluate commercial signals only for the active offering.
- Evaluate freshness, contradiction, closure, award, cancellation and existing-solution outcomes.
- Require coverage-aware evidence thresholds.

### Stage 8 — Role and lawful-contact readiness

- Resolve responsible function after opportunity support.
- Resolve current public or authorized routes.
- Apply suppression, consent, conflict, jurisdiction, channel and tenant policies.

### Stage 9 — Review, feedback and versioning

- Support draft, review, activate, pause, supersede and rollback.
- Route false-positive and false-negative feedback to review.
- Create new versions rather than mutating active or historical profiles.

### Stage 10 — Verification and controlled release

- Structural validation.
- Semantic review.
- Collision and exclusion tests.
- Offering isolation tests.
- Locale and source tests.
- Gold-set execution.
- Tenant and permission tests.
- Snapshot reproducibility tests.
- Performance tests.
- Shadow rollout.
- Exact-head CI verification.

---

## 8. Connection acceptance criteria

The documentation connection plan is satisfied only when:

1. Every sector links to one domain registry, one activity applicability source and one domain keyword registry.
2. Every canonical domain has one stable identity and one separately versioned keyword profile.
3. Every canonical activity has one stable identity and one separately versioned keyword profile.
4. Every domain has an explicit activity applicability assignment.
5. Every active offering references only its own approved commercial-signal profiles.
6. Every source query preserves the originating sector, domain, activity, offering, signal, locale, source and query versions.
7. Every keyword match preserves source, context, time, match mode and profile origin.
8. No keyword layer directly creates a confirmed gap, opportunity or contact-ready lead.
9. Positive evidence is evaluated with applicable exclusions, contradictions, freshness and duplicate-origin controls.
10. Role and contact discovery cannot bypass entity resolution and supported-opportunity gates.
11. Completed jobs remain reproducible from immutable configuration snapshots.
12. The authoritative roadmap remains the only top-level delivery roadmap.
13. No connection depends on hidden shared tables, undocumented runtime behavior or silent profile mutation.
14. Documentation links and anchors pass automated link validation before merge.
15. CI passes against the exact latest commit before the work is called CI Green.

---

## 9. Accurate status

The connected documentation model is defined by this plan and the existing registries.

The following remain **not implemented** until engineering work proves otherwise:

- Runtime taxonomy storage.
- Profile import and migration.
- APIs.
- Guided interface controls.
- Query preview and execution.
- Search indexes.
- Semantic and classification models.
- Evidence scoring.
- Opportunity scoring.
- Role resolution.
- Lawful-contact checks.
- Feedback workflows.
- Benchmark execution.
- Controlled activation.

Documentation integration must not be described as runtime completion. Human beings have already invented enough ways to confuse a map with the territory.
