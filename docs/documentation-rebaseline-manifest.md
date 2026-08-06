# Harvester Documentation Re-baseline Manifest

Status: **Normative documentation-governance manifest**  
Version: **1.0**  
Date: **6 August 2026**

## 1. Purpose

This manifest classifies the existing Markdown corpus after the Agency Intelligence re-baseline.

It prevents old plans, source models, registry datasets, delivery drafts, and open documentation pull requests from becoming competing authorities merely because they remain searchable.

## 2. Classification values

```text
AUTHORITATIVE
PRESERVED_AND_EXTENDED
SUBORDINATE_DETAIL
CONTROLLED_DATASET
DELIVERY_PLAN
TRANSITION_REFERENCE
RESTRICTED_SOURCE_AUTHORITY
SUPERSEDED_BY_SEQUENCE
HISTORICAL_ONLY
```

## 3. Authoritative entrypoints

| Document | Classification | Role |
| --- | --- | --- |
| `README.md` | `AUTHORITATIVE` | Product entrypoint, current/planned boundary, governing rules, and documentation sequence. |
| `docs/README.md` | `AUTHORITATIVE` | Repository-wide authority map and change ownership. |
| `docs/ROADMAP.md` | `AUTHORITATIVE` | Existing 64-module ownership and delivery roadmap. |
| `docs/architecture/agency-intelligence-rebaseline.md` | `AUTHORITATIVE` | Approved architecture and product delta without a new module count. |
| `docs/delivery/agency-intelligence-implementation-sequence.md` | `AUTHORITATIVE` | Dependency-ordered implementation sequence mapped to the existing modules. |

## 4. Preserved and extended architecture

| Document | Classification | Re-baseline treatment |
| --- | --- | --- |
| `docs/architecture/harvester-intelligence-operating-model.md` | `PRESERVED_AND_EXTENDED` | Eight-plane architecture remains authoritative. New entity, source, AI, agency, market, competitor, and sector-pack documents add detail. |
| `docs/architecture/standalone-product-and-integration-framework.md` | `PRESERVED_AND_EXTENDED` | Standalone product, optional Core and Communicator, adapter, synchronization, and resale decisions remain locked. |
| `docs/architecture/provider-portfolio-and-lead-generation-profile-model.md` | `PRESERVED_AND_EXTENDED` | Provider, business-unit, offering, profile, activation, scheduling, and overlap model remains authoritative. Agency and client workspace requirements extend it. |
| `docs/architecture/opportunity-scoring-model-v3.md` | `PRESERVED_AND_EXTENDED` | Remains the scoring authority. The runtime implementation sequence replaces the simpler current score in controlled stages. |
| `docs/architecture/newax-core-automatic-sync.md` | `SUBORDINATE_DETAIL` | Optional Core adapter detail; cannot make Core a dependency or bypass source-owned contracts. |
| `docs/architecture/keyword-evidence-profile-integration-addendum.md` | `SUBORDINATE_DETAIL` | Keyword participation in evidence remains valid under the universal evidence and sector-pack models. |

## 5. New architecture authorities

| Document | Classification | Role |
| --- | --- | --- |
| `docs/architecture/universal-entity-and-evidence-model.md` | `AUTHORITATIVE` | Universal identity, evidence, claim, coverage, contradiction, and migration model. |
| `docs/architecture/source-governance-and-connector-runtime.md` | `AUTHORITATIVE` | Source, policy, credential, connector, schema, mapping, rate, pricing, and execution-gate model. |
| `docs/architecture/ai-model-gateway-and-evaluation.md` | `AUTHORITATIVE` | AI task, provider, model, routing, evaluation, cost, review, and agent isolation model. |
| `docs/architecture/agency-market-and-competitor-intelligence.md` | `AUTHORITATIVE` | Agency, client, market, competitor, analysis, intelligence product, and case-study model. |
| `docs/architecture/sector-pack-runtime-model.md` | `AUTHORITATIVE` | Runtime sector-pack model, including Healthcare and Education operational packs. |
| `docs/architecture/README.md` | `AUTHORITATIVE` | Architecture-directory sequence and change-isolation index. |

## 6. Services and commercial definitions

| Document | Classification | Treatment |
| --- | --- | --- |
| `docs/SERVICES.md` | `PRESERVED_AND_EXTENDED` | Universal provider, offering, customer-market, lead-subject, signal, qualification, and contact rules remain authoritative. Agency and sector-pack models extend operating context. |
| Provider- or offering-specific scoring profiles | `SUBORDINATE_DETAIL` | Apply only when the relevant offering and market definition activate them. |

## 7. Taxonomy corpus

| Path | Classification | Treatment |
| --- | --- | --- |
| `docs/taxonomy/README.md` | `AUTHORITATIVE` | Taxonomy index and runtime relationship. |
| `docs/taxonomy/broad-sector-registry.md` | `CONTROLLED_DATASET` | Canonical sector identities and selection guidance. |
| `docs/taxonomy/*-domain-registry.md` | `CONTROLLED_DATASET` | Canonical domain records; no runtime claim. |
| `docs/taxonomy/activity-registry.md` and linked mappings | `CONTROLLED_DATASET` | Canonical activities and domain applicability. |
| `docs/taxonomy/keywords/README.md` | `CONTROLLED_DATASET` | Keyword and signal dataset index. |
| `docs/taxonomy/keywords/*-domain-keywords.md` | `CONTROLLED_DATASET` | Domain discovery profiles requiring review, benchmark, and activation. |
| `docs/taxonomy/keywords/activity-keywords*.md` | `CONTROLLED_DATASET` | Activity discovery profiles. |
| `docs/taxonomy/keywords/control-profiles.md` and related controls | `CONTROLLED_DATASET` | Shared organization, exclusion, evidence, contact, and source controls. |
| `docs/taxonomy/keywords/locale-packs/*.md` | `CONTROLLED_DATASET` | Locale and transliteration profiles requiring locale review and gold-set validation. |
| Keyword implementation and delivery plans | `DELIVERY_PLAN` | Must follow the primary implementation sequence and universal evidence contract. |

No controlled dataset is runtime-complete until versioned records, APIs, interfaces, evaluation, and release verification exist.

## 8. Source corpus

| Path | Classification | Treatment |
| --- | --- | --- |
| `docs/sources/README.md` | `AUTHORITATIVE` | Source-document index under the governed connector runtime. |
| `docs/sources/user-input-storage-model.md` | `PRESERVED_AND_EXTENDED` | Input configuration and immutable job snapshots remain valid. |
| `docs/sources/canonical-source-record-format.md` | `PRESERVED_AND_EXTENDED` | Source-native envelope remains valid; universal evidence objects extend it. |
| `docs/sources/source-adapter-template.md` | `SUBORDINATE_DETAIL` | New-source documentation template. |
| `docs/sources/*-source-format.md` | `SUBORDINATE_DETAIL` | Provider- or family-specific source structure; activation still requires live policy approval. |
| `docs/sources/google-api-source-model.md` | `SUBORDINATE_DETAIL` | Google-specific acquisition authority under active terms and policy. |
| `docs/sources/yandex-maps-api-source-model.md` | `RESTRICTED_SOURCE_AUTHORITY` | Remains restricted until approved production terms and workflow coverage exist. |
| `docs/sources/linkedin-authorized-data-source-model.md` | `RESTRICTED_SOURCE_AUTHORITY` | Approved paths only. Legacy stealth, account-farm, fingerprint-evasion, and CAPTCHA behavior remains production-blocked. |
| Open PR source-class specifications | `SUBORDINATE_DETAIL` | Rebase after this change and point to the source-governance execution model. |

## 9. Delivery corpus

| Path | Classification | Treatment |
| --- | --- | --- |
| `docs/delivery/README.md` | `AUTHORITATIVE` | Delivery index. |
| `docs/delivery/agency-intelligence-implementation-sequence.md` | `AUTHORITATIVE` | Primary dependency order. |
| `docs/delivery/frontend-configuration-and-responsive-ui-delivery-plan.md` | `DELIVERY_PLAN` | Frontend detail; cannot precede required tenant, provider, source, evidence, and sector contracts. |
| `docs/delivery/keyword-profile-runtime-delivery-plan.md` | `DELIVERY_PLAN` | Keyword runtime detail under sector packs and universal evidence. |
| `docs/delivery/keyword-profile-delivery-addendum.md` | `DELIVERY_PLAN` | Keyword delivery crosswalk. |
| Other module or feature delivery drafts | `DELIVERY_PLAN` | Must declare the owning module and dependencies from the primary sequence. |

## 10. Runtime notes, reviews, and historical documents

Documents whose primary purpose is one-time review, lesson capture, migration history, audit evidence, incident analysis, or completed delivery context remain useful but are not architecture authorities.

They are classified as `TRANSITION_REFERENCE` or `HISTORICAL_ONLY` according to their own stated purpose.

Examples include:

- code-review lessons;
- migration notes;
- completed implementation summaries;
- CI and security status records;
- former roadmap versions preserved through Git history;
- pull-request descriptions and branch-only plans.

A historical document cannot override a current authority.

## 11. Open pull-request treatment

At the time of this re-baseline, documentation and feature branches exist with older bases and overlapping scope.

Rules:

1. Do not merge a stacked or stale PR merely because its content is desirable.
2. Rebase or reimplement it against the latest `master` after this re-baseline.
3. Update its authority references to `docs/README.md` and this manifest.
4. Remove any competing roadmap, module count, product boundary, scoring authority, or source-permission assumption.
5. Preserve useful controlled datasets and implementation detail.
6. Re-run exact-head CI, security, link, and documentation validation.

Known overlap categories include:

- source specification separation;
- input-page output selection;
- keyword taxonomy sequencing;
- modular change isolation;
- domain keyword refinement;
- older stacked frontend parity work;
- known snapshot-linkage and detection-state corrections.

## 12. File-change rules

When changing a Markdown file, identify:

```text
Document owner
Classification
Authority parent
Affected modules
Runtime or documentation-only impact
Required linked-document changes
Implementation and verification status
```

A new Markdown file is justified only when:

- it owns a distinct bounded concern;
- an existing authority cannot contain the change without becoming ambiguous;
- its relationship to existing authorities is explicit;
- it does not create another roadmap or module count;
- indexes are updated in the same change.

## 13. Supersession rules

- Git history preserves old versions.
- Active folders should not contain duplicate files named `final`, `complete`, `ultimate`, `v2-final`, or similar human distress signals.
- When one active document supersedes another, update indexes and remove or clearly mark the older active copy.
- Planned architecture remains planned until runtime evidence supports a status change.

## 14. Locked rule

> One concern has one active authority. Detailed documents may extend it, controlled datasets may feed it, and delivery plans may implement it, but none may quietly become a competing product definition.
