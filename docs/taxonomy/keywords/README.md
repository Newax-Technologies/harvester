# Harvester Keyword Taxonomy Index

Status: **Proposed**  
Version: **1.2**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This directory defines the controlled discovery and lead-signal keyword layer for the Harvester sector, domain, activity, provider-offering, evidence, qualification, and opportunity model.

Version 1.2 preserves the reviewed domain and activity identity baseline and adds the missing commercial-relevance layer: business events, direct intent, procurement, operational pain, technology footprint, decision-maker responsibility, lawful contact routes, source suitability, freshness, contradiction checks, sector overlays, and keyword-quality governance.

These files remain documentation datasets, not production search configuration.

## Coverage

| Controlled layer | Coverage |
| --- | ---: |
| Broad sectors | 16 |
| Canonical domains with separate keyword profiles | 1,586 |
| Canonical activities with separate keyword profiles | 519 |
| Organization-cue profiles | 8 |
| Exclusion and negative-context profiles | 28 |
| Evidence-control profiles | 9 |
| Reusable lead-generation signal profiles | 29 |
| Functional decision-maker role groups | 20 |
| Contact-route profiles | 8 |
| Sector lead-generation overlays | 16 |
| Source classes with signal guidance | 14 |
| Governed query families | 10 |

## Governing model

```text
Selected broad sector
→ selected domain
→ approved domain-specific activity
→ domain identity terms
→ canonical activity terms
→ organization cues
→ exclusions and negative context
→ resolved organization candidate

Active provider offering
→ approved lead-signal profile
→ source-appropriate query family
→ business event, intent, pain, technology, scale or compliance evidence
→ contradiction and freshness checks
→ responsible-role and lawful-contact assessment
→ qualification
→ supported opportunity
→ contact-ready lead only when policy permits
```

Domain and activity keywords classify what an organization is and what it appears to do. Lead-signal profiles explain why the target may be relevant now. Neither layer independently proves that the organization needs a provider's service.

## Shared keyword controls

- [Keyword Control Profiles](control-profiles.md)
  - Organization cues, ambiguity controls, sensitive-sector exclusions, evidence requirements, and contact-order safeguards
- [Keyword Quality and Review Standard](keyword-quality-and-review-standard.md)
  - Profile lifecycle, benchmark examples, sensitive-sector controls, quality metrics, versioning, and rollback

## Canonical activity keyword registries

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

## Lead-generation intelligence registries

- [Lead-Generation Signal Registry](lead-generation-signal-registry.md)
  - Direct inquiry, active intent, procurement, replacement, integration, hiring, expansion, compliance, maintenance, technology, budget, contactability, and negative signals
- [Sector Lead-Generation Overlays](sector-lead-generation-overlays.md)
  - High-value triggers, operational indicators, scale cues, likely responsible functions, source guidance, and critical exclusions for all 16 sectors
- [Decision-Maker and Contact-Cue Registry](decision-maker-and-contact-cues.md)
  - Functional-owner roles, authority confidence, contact-route types, current-affiliation checks, and consent boundaries
- [Source-to-Signal Matrix](source-signal-matrix.md)
  - Which source classes can credibly support each type of lead signal and where their weaknesses lie
- [Query Composition and Evidence Rules](query-composition-and-evidence-rules.md)
  - Query families, evidence grades, freshness, duplicate suppression, negative queries, and scoring restrictions
- [Cross-Product Keyword and Profile Contract](cross-product-keyword-contract.md)
  - Bounded references available to NEWAX Core or Communicator without copying private Harvester strategy

## Sector-specific domain keyword registries

| Sector code | Broad sector | Canonical domains | Registry |
| --- | --- | ---: | --- |
| `BS-001` | Healthcare | 142 | [Part 1](healthcare-domain-keywords-part-1.md) and [Part 2](healthcare-domain-keywords-part-2.md) |
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
| `BS-014` | Technology | 127 | [Part 1](technology-domain-keywords-part-1.md) and [Part 2](technology-domain-keywords-part-2.md) |
| `BS-015` | Government | 96 | [Government](government-domain-keywords.md) |
| `BS-016` | Nonprofit | 92 | [Nonprofit](nonprofit-domain-keywords.md) |
|  | **Total** | **1,586** | **All canonical domains separately profiled** |

## Match modes required by implementation

```text
EXACT
PHRASE
SEMANTIC
ENTITY
REGEX
```

A future implementation must preserve match mode, source, language, profile version, timestamp, event date, freshness, and the exact text or entity that matched.

## Lead-generation safeguards

- Direct intent is separated from indirect operational indicators.
- Job postings can indicate hiring, growth, technology, or process ownership but do not prove purchasing budget.
- Procurement signals track amendments, cancellations, awards, and deadlines.
- Existing solutions may indicate replacement, integration, optimization, support, or no opportunity; they are not automatic disqualifiers.
- Decision-maker title matches do not prove purchase authority.
- Public contact routes do not override consent, suppression, conflict, jurisdiction, platform, or channel policy.
- Negative queries accompany material positive opportunities to detect closure, cancellation, award, suppression, or contradiction.
- Raw match counts do not become lead scores.
- Event freshness uses the underlying event date where known, not merely the collection date.
- Copied press releases, mirrored tenders, and directory replicas count as one evidence origin.

## Lexical quality controls

- Whole phrases are transformed only at word boundaries.
- Malformed stems such as truncated `formulat`, `manufactur`, or `franchis` are prohibited.
- Digital and software domain families use software-provider cues unless a reviewed physical-system exception applies.
- Physical systems such as fire-safety, solar mounting, aluminium, embedded, and control systems are not automatically classified as software.
- Broad aliases cannot qualify a target without corroborating organization, sector, activity, or entity evidence.
- Locale-specific aliases require separately reviewed language packs.

## Non-negotiable rules

1. Keywords discover evidence; they do not independently prove a domain, activity, gap, opportunity, or lead.
2. Every domain profile remains separate, even when domains share words or activities.
3. Every canonical activity has one shared identity, but activity applicability and user selection remain domain-specific.
4. Selecting or detecting an activity for one domain never activates it for another domain.
5. Domain terms, activity terms, organization cues, exclusions, lead signals, role cues, source rules, and locale packs remain independently versioned.
6. Service-gap, buying-intent, competitor, existing-solution, and problem-signal evaluation requires an active provider offering.
7. Broad terms require corroborating sector, organization, activity, entity, or source context.
8. Source reliability, source-signal suitability, recency, negative context, duplicate evidence, language, and coverage affect confidence.
9. “Not found” is not “absent” without adequate source coverage.
10. Decision-maker resolution begins only after the organization is resolved to the configured confidence threshold.
11. Contact-ready status requires a supported opportunity and a current lawful contact route.
12. Urdu, Roman Urdu, and other locale aliases require reviewed language packs; translation or transliteration must not silently mutate canonical English profiles.
13. User feedback may propose profile changes, but production profiles do not mutate silently.
14. Completed harvest jobs preserve every taxonomy, keyword, signal, role, source, evidence, qualification, and scoring version used when they ran.

## Delivery boundary

These Markdown registries are **defined and repository-integrated documentation datasets**.

They do not implement database tables, migrations, search indexes, embeddings, classifiers, APIs, interface controls, source queries, evidence decisions, opportunity scoring, contact eligibility, outreach, or releases. Runtime implementation remains separate engineering work requiring schema, migration, API, interface, testing, security, and release verification.

## Implementation and delivery planning

The registries above are now connected to three additive planning documents:

- [Keyword Profile Implementation Plan](keyword-profile-implementation-plan.md)
  - Defines the user configuration flow, keyword layers, planned runtime objects, profile versioning, query composition, evidence behavior, locale packs, APIs, safeguards, implementation slices, and acceptance criteria.
- [Keyword and Evidence Profile Integration Addendum](../../architecture/keyword-evidence-profile-integration-addendum.md)
  - Defines how keyword configuration and match evidence enter the control, acquisition, evidence, resolution, intelligence, decision, and learning planes without allowing a keyword match to bypass entity resolution or evidence review.
- [Keyword Profile Delivery Addendum](../../delivery/keyword-profile-delivery-addendum.md)
  - Adds delivery gates, benchmark requirements, rollout controls, quality metrics, migration sequencing, and definition-of-done rules while preserving the authoritative 64-module roadmap.

### Change-control rule

- Canonical domain and activity keyword terms belong in the sector and activity registries linked above.
- Shared organization cues, exclusions, evidence controls, role cues, contact routes, source suitability, and locale packs belong under this keyword directory.
- Provider-offering problem, intent, procurement, competitor, existing-solution, replacement, integration, maintenance, and service-gap profiles require an active selected offering.
- Runtime objects, API boundaries, query preview, match evidence, versioning, feedback, and interface behavior belong in the implementation plan and architecture addendum.
- Delivery sequencing, verification gates, benchmark requirements, rollout, and production-readiness rules belong in the delivery addendum.
- The authoritative roadmap remains the only top-level module roadmap; these documents strengthen its existing modules and do not create a parallel module count.
