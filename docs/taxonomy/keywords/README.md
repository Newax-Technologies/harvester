# Harvester Keyword Taxonomy Index

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This directory defines controlled discovery keyword profiles for the Harvester sector, domain, and activity taxonomy.

## Coverage

| Layer | Coverage |
| --- | ---: |
| Broad sectors | 16 |
| Canonical domains with separate profiles | 1,586 |
| Canonical activities with alias profiles | 519 |

## Canonical activity keyword registries

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

## Sector-specific domain keyword registries

| Sector | Domains | Keyword registry |
| --- | ---: | --- |
| `BS-001` Healthcare | 142 | [Healthcare domain keywords](healthcare-domain-keywords.md) |
| `BS-002` Education | 95 | [Education domain keywords](education-domain-keywords.md) |
| `BS-003` Food and Agriculture | 103 | [Food and Agriculture domain keywords](food-agriculture-domain-keywords.md) |
| `BS-004` Real Estate | 88 | [Real Estate domain keywords](real-estate-domain-keywords.md) |
| `BS-005` Construction | 93 | [Construction domain keywords](construction-domain-keywords.md) |
| `BS-006` Legal | 97 | [Legal domain keywords](legal-domain-keywords.md) |
| `BS-007` Finance | 109 | [Finance domain keywords](finance-domain-keywords.md) |
| `BS-008` Retail | 84 | [Retail domain keywords](retail-domain-keywords.md) |
| `BS-009` Hospitality | 79 | [Hospitality domain keywords](hospitality-domain-keywords.md) |
| `BS-010` Travel | 75 | [Travel domain keywords](travel-domain-keywords.md) |
| `BS-011` Manufacturing and Industry | 111 | [Manufacturing and Industry domain keywords](manufacturing-industry-domain-keywords.md) |
| `BS-012` Logistics | 101 | [Logistics domain keywords](logistics-domain-keywords.md) |
| `BS-013` Energy | 94 | [Energy domain keywords](energy-domain-keywords.md) |
| `BS-014` Technology | 127 | [Technology domain keywords](technology-domain-keywords.md) |
| `BS-015` Government | 96 | [Government domain keywords](government-domain-keywords.md) |
| `BS-016` Nonprofit | 92 | [Nonprofit domain keywords](nonprofit-domain-keywords.md) |

## Keyword layers

```text
Domain identity terms
+ domain-specific activity terms
+ organization cues
+ exclusions and negative context
= classification evidence candidates

Active provider service
+ service-specific problem and buying signals
+ verified evidence
= supported opportunity assessment
```

## Non-negotiable rules

1. Keywords discover evidence; they do not independently prove a domain, activity, gap, opportunity, or lead.
2. Domain and activity keyword profiles are separate and versioned.
3. An activity selected or detected for one domain never propagates to another domain.
4. Service-gap, buying-intent, competitor, existing-solution, and problem-signal keywords require a selected provider offering and are not defined by this registry.
5. Exact, phrase, semantic, entity, and regex match modes must remain distinguishable in implementation.
6. Source reliability, recency, negative context, duplicate evidence, and coverage must be considered before qualification.
7. Locale aliases require reviewed language packs; transliteration and translation must not silently mutate canonical terms.
8. Completed harvest jobs preserve the keyword profile versions used when they ran.

## Delivery boundary

These Markdown files are controlled proposed datasets. They do not implement database tables, migrations, APIs, search indexes, embeddings, classifiers, interface controls, scoring, or releases.
