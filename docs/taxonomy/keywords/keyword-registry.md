# Harvester Keyword Registry and Composition Rules

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This registry defines controlled keyword profiles for Harvester's **1,586 canonical product or service domains** and **519 canonical business activities**. Keywords are discovery aids and evidence-strengthening signals. They never independently prove an activity, service gap, opportunity, or lead qualification.

## Locked composition model

```text
Selected broad sector
+ selected domain keyword profile
+ selected activity keyword profile
+ provider-selected service keyword profile
+ source and geography constraints
+ exclusions and negative context
= search and evidence profile
```

Domain and activity keywords remain separate. A domain term identifies what the organization deals with. An activity term identifies what the organization does. Service-gap and buying-intent keywords belong to the provider service profile and are not invented by this registry.

## Keyword classes

| Class | Purpose | May prove opportunity? |
| --- | --- | --- |
| `DOMAIN_TERM` | Identifies a product, service, institution, asset, or market domain. | No |
| `DOMAIN_ALIAS` | Alternate spelling, abbreviation, local name, or recognized synonym. | No |
| `ACTIVITY_TERM` | Identifies a business activity. | No |
| `ACTIVITY_PHRASE` | Phrase indicating an organization performs an activity. | No |
| `ORGANIZATION_SIGNAL` | Indicates an organization, department, facility, provider, or operator. | No |
| `PROBLEM_SIGNAL` | Suggests friction or operational need. Defined per provider service. | No |
| `BUYING_SIGNAL` | Suggests active evaluation or procurement. Defined per provider service. | No |
| `EXISTING_SOLUTION` | Identifies an incumbent system, vendor, or internal capability. | No |
| `EXCLUSION` | Removes irrelevant, educational, employment, consumer, or ambiguous contexts. | No |
| `LOCAL_TERMINOLOGY` | Urdu, Roman Urdu, regional spelling, abbreviation, or market language. | No |

## Match modes

- `EXACT`
- `PHRASE`
- `SEMANTIC`
- `ENTITY`
- `REGEX` only after review

## Universal safeguards

1. A keyword match creates a candidate evidence signal, not a classification fact.
2. Domain terms and activity terms must normally co-occur within a bounded page, passage, entity, or source context before a domain–activity hypothesis is strengthened.
3. Search-engine snippets alone are insufficient evidence.
4. Duplicate, syndicated, copied, or mirrored sources do not increase confidence.
5. “Not found” is not “absent” unless source coverage is sufficient and absence rules are satisfied.
6. Employment, training, academic, dictionary, news-only, marketplace, and consumer-shopping contexts must be excluded unless explicitly targeted.
7. Local-language profiles are versioned separately and require human review.
8. Service, problem, buying, competitor, and existing-solution terms are attached only to active provider offerings.
9. Keyword profiles may be suggested automatically but cannot silently mutate after user approval.
10. Every completed harvest job preserves the exact keyword-profile versions used.

## Dataset files

### Activity keywords

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

### Sector domain keywords

- [Construction domain keywords](domain-keywords/construction-domain-keywords.md)
- [Education domain keywords](domain-keywords/education-domain-keywords.md)
- [Energy domain keywords](domain-keywords/energy-domain-keywords.md)
- [Finance domain keywords](domain-keywords/finance-domain-keywords.md)
- [Food Agriculture domain keywords](domain-keywords/food-agriculture-domain-keywords.md)
- [Government domain keywords](domain-keywords/government-domain-keywords.md)
- [Healthcare domain keywords](domain-keywords/healthcare-domain-keywords.md)
- [Hospitality domain keywords](domain-keywords/hospitality-domain-keywords.md)
- [Legal domain keywords](domain-keywords/legal-domain-keywords.md)
- [Logistics domain keywords](domain-keywords/logistics-domain-keywords.md)
- [Manufacturing Industry domain keywords](domain-keywords/manufacturing-industry-domain-keywords.md)
- [Nonprofit domain keywords](domain-keywords/nonprofit-domain-keywords.md)
- [Real Estate domain keywords](domain-keywords/real-estate-domain-keywords.md)
- [Retail domain keywords](domain-keywords/retail-domain-keywords.md)
- [Technology domain keywords](domain-keywords/technology-domain-keywords.md)
- [Travel domain keywords](domain-keywords/travel-domain-keywords.md)

## Default negative-context terms

These are review defaults, not universal hard exclusions:

```text
jobs; job vacancy; salary; career; internship; course; training; tutorial; definition; meaning; wikipedia; pdf; exam question; assignment; template; free download; image; stock photo; consumer review; used for sale
```

They must be relaxed when employment, education, training, recruitment, publishing, retail, or second-hand commerce is part of the selected target. A universal negative list applied blindly would be efficient only at deleting good leads.

## Delivery boundary

These Markdown files define controlled keyword datasets. They do not implement database records, search queries, source connectors, embeddings, classifiers, scoring, user interfaces, or runtime evidence decisions.
