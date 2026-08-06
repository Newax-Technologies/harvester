# Harvester Ultimate Keyword Depth Coverage Matrix

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This matrix defines the intended completion surface of the Harvester keyword and evidence layer.

## 1. Current controlled coverage

| Layer | Defined coverage |
| --- | ---: |
| Broad sectors | 16 |
| Domain identity profiles | 1,586 |
| Activity identity profiles | 519 |
| Organization-cue profiles | 8 |
| Exclusion and context profiles | 28 |
| Evidence-control profiles | 9 |
| Lead-generation signal profiles | 29 |
| Functional role groups | 20 |
| Contact-route profiles | 8 |
| Sector lead overlays | 16 |
| Source classes | 14 |
| Query families | 10 |

## 2. Depth dimensions

| Dimension | Required state | Current documentation state |
| --- | --- | --- |
| Canonical domain terms | Every domain separate | Defined |
| Canonical activity terms | Every activity separate | Defined |
| Organization archetypes | Shared controlled packs | Defined |
| Lexical variants | Reviewed exact and common variants | Partially defined; requires profile-by-profile review |
| Acronyms and shorthand | Ambiguity-controlled | Partially defined |
| Parent and child concepts | Ontology-linked | Standard defined; mappings require implementation and review |
| Facility and asset cues | Sector and domain aware | Standard defined |
| Process vocabulary | Domain–activity aware | Standard defined |
| Regulatory vocabulary | Jurisdiction and source aware | Standard defined; authoritative mappings pending |
| Event and trigger signals | Dated and freshness-controlled | Defined |
| Provider-offering intent and pain | Active offering dependent | Standard defined; offering catalogue profiles pending |
| Existing-solution and competitor terms | Multi-interpretation | Defined at framework level |
| Decision roles | Function based, not title-only authority | Defined |
| Contact routes | Lawful and current | Defined |
| Geography | Compositional | Defined |
| Source-specific query templates | Source aware | Defined |
| Exclusions and contradictions | Positive profiles paired with negatives | Defined |
| English baseline | Canonical | Defined |
| Pakistan Urdu and Roman Urdu | Reviewed locale pack | Candidate pack defined separately; human review required |
| Semantic seeds | Explainable and model-versioned | Standard defined |
| Classification crosswalks | Code-system and edition aware | Standard defined; actual mappings pending authoritative sources |
| Benchmarks | Positive, negative, ambiguous, source, locale | Standard defined; gold sets pending |
| Runtime schema and APIs | Versioned profile objects and evidence | Not implemented |
| Search and source adapters | Query generation and execution | Not implemented |
| Classifiers and embeddings | Calibrated by sector | Not implemented |
| Approval workflow | Draft to active with rollback | Not implemented |
| Production metrics | Precision, recall, overturn, complaints | Not implemented |

## 3. Definition of ultimate depth

Ultimate depth is achieved when every eligible provider-offering and target combination can produce an explainable plan containing:

```text
Sector
+ Domain
+ Domain-specific Activity
+ Organization archetype
+ Facility / Asset / Process cues
+ Active Provider Offering
+ Direct intent / Procurement / Pain / Event signals
+ Existing solution and contradiction checks
+ Decision function
+ Lawful contact route
+ Geography
+ Source-specific syntax
+ Language and locale
+ Precision mode
+ Evidence threshold
+ Freshness
+ Benchmark version
```

The system must then retain exactly which components produced every evidence candidate and decision.

## 4. What cannot be truthfully called complete yet

The following require future engineering or authoritative data:

- provider-offering catalogue and reviewed signal profiles for every offered service;
- authoritative classification-code mappings;
- reviewed Urdu and Roman Urdu domain aliases for all 1,586 domains;
- profile-level gold sets and measured precision/recall;
- runtime storage, APIs, query preview, source execution, embeddings, classifiers, scoring, review, and rollback;
- production and contact-policy verification.

Documenting a requirement is not the same as proving it works. NEWAX’s verification protocol requires exact status language and execution evidence before completion is claimed.

## 5. Delivery sequence

```text
1. Lock profile schemas and pack codes
2. Build provider-offering catalogue
3. Create offering-specific signal profiles
4. Review highest-priority sector/domain/activity profiles
5. Build English gold sets
6. Build Pakistan locale packs and locale gold sets
7. Implement versioned storage and APIs
8. Implement query preview and explanation
9. Implement source adapters in shadow mode
10. Calibrate lexical and semantic matching
11. Validate evidence, contradiction, freshness and deduplication
12. Add human review and feedback workflow
13. Run limited workspace rollout
14. Verify exact-head CI, security and operational behaviour
15. Activate only approved profiles
```

## 6. Status

The v2.0 documents establish the intended ultimate-depth standard and close the major architectural gaps in keyword composition, offering dependency, semantic expansion, source templates, locale governance, and benchmark validation.

Status remains **Proposed / Documentation only** until runtime and benchmark evidence exist.
