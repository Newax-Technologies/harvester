# Harvester Keyword Taxonomy Index

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This directory defines the controlled discovery-keyword layer for the Harvester sector, domain, and activity taxonomy.

Version 1.1 replaces the first generated baseline with reviewed lexical forms, corrected whole-phrase handling, stricter organization-cue classification, and removal of malformed automatic stems. These files remain documentation datasets, not production search configuration.

## Coverage

| Controlled layer | Coverage |
| --- | ---: |
| Broad sectors | 16 |
| Canonical domains with separate keyword profiles | 1,586 |
| Canonical activities with separate keyword profiles | 519 |
| Organization-cue profiles | 8 |
| Exclusion and negative-context profiles | 15 |

## Governing model

```text
Selected broad sector
→ selected domain
→ approved domain-specific activity
→ domain identity terms
→ canonical activity terms
→ organization cues
→ exclusions and negative context
→ evidence candidates

Active provider offering
→ service-specific target terms
→ problem and buying signals
→ existing-solution and competitor signals
→ verified evidence
→ supported opportunity assessment
```

Domain and activity keywords classify what an organization is and what it appears to do. They do not establish that the organization needs a provider's service.

## Shared keyword controls

- [Keyword Control Profiles](control-profiles.md)
  - Organization cues for institutions, products, services, commerce, software, government, and nonprofit targets
  - Exclusion controls for ambiguous terms such as bank, cloud, port, plant, security, audit, trust, market, asset, network, and AI

## Canonical activity keyword registries

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

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

A future implementation must preserve match mode, source, language, profile version, timestamp, and the exact text or entity that matched.

## Version 1.1 quality corrections

- Whole phrases are transformed only at word boundaries.
- Malformed stems such as truncated `formulat`, `manufactur`, or `franchis` are prohibited.
- Digital and software domain families use software-provider cues unless a reviewed physical-system exception applies.
- Physical systems such as fire-safety, solar mounting, aluminium, embedded, and control systems are not automatically classified as software.
- Broad aliases cannot qualify a target without corroborating organization, sector, activity, or entity evidence.
- Service-gap, buying-intent, problem, competitor, and existing-solution terms remain outside this baseline until an active provider offering is selected.
- Locale-specific aliases require separately reviewed language packs.

## Non-negotiable rules

1. Keywords discover evidence; they do not independently prove a domain, activity, gap, opportunity, or lead.
2. Every domain profile remains separate, even when domains share words or activities.
3. Every canonical activity has one shared identity, but activity applicability and user selection remain domain-specific.
4. Selecting or detecting an activity for one domain never activates it for another domain.
5. Domain terms, activity terms, organization cues, and exclusions remain independently versioned.
6. Service-gap, buying-intent, competitor, existing-solution, and problem-signal keywords require an active provider offering and are not defined by this registry.
7. Broad terms require corroborating sector, organization, activity, or entity context.
8. Source reliability, recency, negative context, duplicate evidence, language, and coverage affect confidence.
9. “Not found” is not “absent” without adequate source coverage.
10. Urdu, Roman Urdu, and other locale aliases require reviewed language packs; translation or transliteration must not silently mutate canonical English profiles.
11. User feedback may propose profile changes, but production profiles do not mutate silently.
12. Completed harvest jobs preserve every keyword and control-profile version used when they ran.

## Delivery boundary

These Markdown registries are **defined and repository-integrated documentation datasets**.

They do not implement database tables, migrations, search indexes, embeddings, classifiers, APIs, interface controls, evidence decisions, opportunity scoring, or releases. Runtime implementation remains separate engineering work requiring schema, migration, API, interface, testing, security, and release verification.
