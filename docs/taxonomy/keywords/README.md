# Harvester Keyword Taxonomy Index

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This directory defines the controlled keyword, semantic, source, evidence, qualification, and contact-preparation layer for the Harvester sector, domain, activity, provider-offering, and opportunity model.

Version 2.1 preserves the 1,586 separate domain profiles, 519 separate activity profiles, organization cues, exclusions, lead-generation signals, role groups, contact routes, source rules, sector overlays, precision tiers, semantic expansion, locale controls, benchmark standards and validation gates. It adds one authoritative documentation sequence and one complete sector connection matrix so every registry has an explicit upstream and downstream path.

These files are documentation datasets and standards. They are not production search configuration.

## Start here

Read the keyword documentation in this order:

1. [Keyword Documentation Sequence and Connection Plan](00-keyword-sequence-and-connections.md)
   - Defines authority, reading order, runtime gates, object ownership, version snapshots, implementation stages and connection acceptance criteria.
2. [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md)
   - Connects all 16 sector domain registries to their activity-applicability sources and domain keyword registries.
3. [Keyword Profile Implementation Plan](keyword-profile-implementation-plan.md)
   - Defines runtime objects, APIs, interface behavior, delivery slices and verification requirements.
4. [Complete Keyword Validation Plan](keyword-validation-plan.md)
   - Defines structural, semantic, source, locale, collision, gold-set, regression, rollout and activation gates.
5. [Ultimate Keyword Depth Coverage Matrix](ultimate-depth-coverage-matrix.md)
   - Records what is defined, partial, dependent on authoritative data or still unimplemented.

The sequence documents connect existing authorities. They do not create a second taxonomy, a second opportunity model or a second roadmap.

## Coverage

| Controlled layer | Defined coverage |
| --- | ---: |
| Broad sectors | 16 |
| Canonical domains with separate profiles | 1,586 |
| Canonical activities with separate profiles | 519 |
| Organization-cue profiles | 8 |
| Exclusion and negative-context profiles | 28 |
| Evidence-control profiles | 9 |
| Reusable lead-generation signal profiles | 29 |
| Functional decision-maker role groups | 20 |
| Contact-route profiles | 8 |
| Sector lead-generation overlays | 16 |
| Source classes with signal guidance | 14 |
| Governed query families | 10 |
| Ultimate profile dimensions | 32 |
| Pakistan locale baseline | English, Urdu and Roman Urdu candidate pack |

## Governing model

```text
Selected broad sector
→ selected domain
→ approved domain-specific activity
→ domain and activity identity evidence
→ organization, facility, process, regulatory and source context
→ resolved organization candidate

Active provider offering
→ offering-specific intent, problem, technology, event and contradiction profiles
→ source-appropriate query plan
→ dated evidence candidates
→ entity, freshness, duplication and contradiction review
→ decision-function and lawful-contact assessment
→ supported opportunity
→ contact-ready lead only when policy permits
```

Keywords discover evidence. They never independently prove a domain, activity, capability gap, buying intent, opportunity, authority, or permission to contact.

## Ultimate-depth standards

- [Deep Keyword Pack Registry](deep-keyword-pack-registry.md)
  - Supplies reusable organization, commercial-activity, facility, process, event, intent, problem, technology, role, contact, negative and contradiction vocabulary packs.
- [Sector and Domain-Family Vocabulary Registry](sector-domain-family-vocabulary.md)
  - Adds reviewed candidate vocabulary across all 16 sectors and their major domain families without collapsing separate domain identities.
- [Ultimate Keyword Profile Standard](ultimate-keyword-profile-standard.md)
  - Defines 32 independently versioned profile dimensions, keyword types, precision tiers, match modes, proximity, co-occurrence, weighting, source policy, sensitive-sector review, lifecycle, and approval gates.
- [Keyword Expansion and Composition Engine](keyword-expansion-and-composition-engine.md)
  - Defines composable packs, precision modes, query families, query budgets, deduplication, semantic expansion, geography, stopping rules, and traceable query execution.
- [Provider-Offering Keyword Profile Standard](provider-offering-keyword-profile-standard.md)
  - Defines offering eligibility, direct intent, procurement, operational pain, existing solution, replacement, integration, expansion, buying stage, contradictions, evidence thresholds, and gap states.
- [Semantic, Entity and Classification Expansion](semantic-entity-and-classification-expansion.md)
  - Defines organization aliases, entity types, ontology relationships, facilities, brands, branches, semantic seeds, classification crosswalk fields, and entity-resolution controls.
- [Source Query Template Library](source-query-template-library.md)
  - Defines source-specific query and inspection patterns for websites, directories, registries, procurement, jobs, news, social, technology sources, app marketplaces, professional networks, and authorized imports.
- [Keyword Benchmark and Gold-Set Standard](benchmark-and-gold-set-standard.md)
  - Defines example classes, minimum sample depth, metrics, provisional activation thresholds, evaluation splits, locale validation, regression testing, shadow rollout, and completion evidence.
- [Complete Keyword Validation Plan](keyword-validation-plan.md)
  - Defines validation outcomes and severity, reviewer separation, 18 execution gates, structural and semantic checks, collision handling, offering isolation, source and locale validation, gold-set execution, regression, shadow rollout, activation, rollback, monitoring, CI evidence and acceptance criteria.
- [Ultimate Keyword Depth Coverage Matrix](ultimate-depth-coverage-matrix.md)
  - Shows what is defined, what remains partially reviewed, what requires authoritative data, and what remains unimplemented.
- [Pakistan English, Urdu and Roman Urdu Candidate Pack](locale-packs/pakistan-english-urdu-roman-urdu.md)
  - Provides a controlled seed vocabulary for mixed-language Pakistan business sources and requires native/domain review before activation.

## Existing shared controls

- [Keyword Control Profiles](control-profiles.md)
- [Keyword Quality and Review Standard](keyword-quality-and-review-standard.md)
- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)
- [Lead-Generation Signal Registry](lead-generation-signal-registry.md)
- [Sector Lead-Generation Overlays](sector-lead-generation-overlays.md)
- [Decision-Maker and Contact-Cue Registry](decision-maker-and-contact-cues.md)
- [Source-to-Signal Matrix](source-signal-matrix.md)
- [Query Composition and Evidence Rules](query-composition-and-evidence-rules.md)
- [Cross-Product Keyword and Profile Contract](cross-product-keyword-contract.md)

## Sector-specific domain registries

The complete cross-reference to each sector's domain registry and activity-applicability source is maintained in the [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md).

| Sector code | Broad sector | Domains | Registry |
| --- | --- | ---: | --- |
| `BS-001` | Healthcare | 142 | [Part 1](healthcare-domain-keywords-part-1.md), [Part 2](healthcare-domain-keywords-part-2.md) |
| `BS-002` | Education | 95 | [Education](education-domain-keywords.md) |
| `BS-003` | Food and Agriculture | 103 | [Food and Agriculture](food-agriculture-domain-keywords.md) |
| `BS-004` | Real Estate | 88 | [Real Estate](real-estate-domain-keywords.md) |
| `BS-005` | Construction | 93 | [Construction](construction-domain-keywords.md) |
| `BS-006` | Legal | 97 | [Legal](legal-domain-keywords.md) |
| `BS-007` | Finance | 109 | [Finance](finance-domain-keywords.md) |
| `BS-008` | Retail | 84 | [Retail](retail-domain-keywords.md) |
| `BS-009` | Hospitality | 79 | [Hospitality](hospitality-domain-keywords.md) |
| `BS-010` | Travel | 75 | [Travel](travel-domain-keywords.md) |
| `BS-011` | Manufacturing and Industry | 111 | [Manufacturing and Industry](manufacturing-industry-domain-keywords.md) |
| `BS-012` | Logistics | 101 | [Logistics](logistics-domain-keywords.md) |
| `BS-013` | Energy | 94 | [Energy](energy-domain-keywords.md) |
| `BS-014` | Technology | 127 | [Part 1](technology-domain-keywords-part-1.md), [Part 2](technology-domain-keywords-part-2.md) |
| `BS-015` | Government | 96 | [Government](government-domain-keywords.md) |
| `BS-016` | Nonprofit | 92 | [Nonprofit](nonprofit-domain-keywords.md) |
|  | **Total** | **1,586** | **Every canonical domain separately profiled** |

## Required match modes

```text
EXACT
PHRASE
TOKEN_SET
PROXIMITY
REGEX
ENTITY
CLASSIFICATION_CODE
SEMANTIC
STRUCTURED_FIELD
```

Every future match must preserve the originating profile and version, matched text or entity, source and location, language and locale, event date, collection time, precision tier, evidence dimension, exclusion or contradiction result, and final disposition.

## Non-negotiable safeguards

1. Every domain profile remains separate even when domains share words or activities.
2. Every canonical activity has one shared identity, but activity applicability and selection remain domain-specific.
3. Selecting or detecting an activity for one domain never activates it for another.
4. Provider-offering intent, pain, replacement, integration, competitor, technology, maintenance, and gap profiles require an active offered service.
5. Broad terms require organization, activity, sector, source, entity, proximity, or co-occurrence context.
6. Negative and contradiction queries accompany material positive opportunities.
7. Event freshness uses the underlying event date where known.
8. Mirrored pages, copied press releases, directory replicas, and repeated aliases do not inflate corroboration.
9. “Not found” is not “absent” without an adequate coverage model.
10. Decision-role resolution begins only after organization resolution.
11. A title match does not prove authority.
12. A public contact route does not create consent or override suppression, conflict, jurisdiction, platform, or channel policy.
13. Semantic similarity retains the model version, source text, and reviewed profile seed; it cannot independently qualify a lead.
14. Structured classification codes retain their system, edition, jurisdiction, source, and effective date.
15. Urdu, Roman Urdu, and mixed-language terms require reviewed locale packs and gold sets before activation.
16. Sensitive sectors prohibit harmful inference from weak or private data.
17. User feedback creates a versioned candidate revision rather than silently mutating production profiles.
18. Completed Harvest Jobs preserve every taxonomy, keyword, signal, source, model, evidence, qualification, scoring, and contact-policy version used.

## Accurate status

The domain, activity, signal, role, source, exclusion, sequence and v2.1 depth standards are **defined and repository-integrated documentation** after merge.

They are not benchmark-tested, runtime-implemented, active, production-verified, or complete. Provider-offering profiles, authoritative classification mappings, reviewed locale coverage for every domain, profile-level gold sets, storage, APIs, query preview, source execution, classifiers, scoring, approval workflows, and controlled activation remain future work.

## Implementation planning

- [Keyword Documentation Sequence and Connection Plan](00-keyword-sequence-and-connections.md)
- [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md)
- [Keyword Profile Implementation Plan](keyword-profile-implementation-plan.md)
- [Keyword and Evidence Profile Integration Addendum](../../architecture/keyword-evidence-profile-integration-addendum.md)
- [Keyword Profile Delivery Addendum](../../delivery/keyword-profile-delivery-addendum.md)

The authoritative roadmap remains the only top-level module roadmap. These documents deepen existing Harvester modules and do not create a parallel module count.
