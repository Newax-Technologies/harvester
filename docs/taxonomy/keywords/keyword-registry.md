# Harvester Keyword Registry and Composition Rules

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This registry defines controlled keyword profiles for Harvester's **1586 canonical product or service domains** and **519 canonical business activities**. Keywords are discovery aids and evidence-strengthening signals. They never independently prove an activity, service gap, opportunity, or lead qualification.

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

Domain and activity keywords remain separate. Service-gap and buying-intent keywords belong to active provider service profiles.

## Keyword classes

`DOMAIN_TERM`; `DOMAIN_ALIAS`; `ACTIVITY_TERM`; `ACTIVITY_PHRASE`; `ORGANIZATION_SIGNAL`; `PROBLEM_SIGNAL`; `BUYING_SIGNAL`; `EXISTING_SOLUTION`; `EXCLUSION`; `LOCAL_TERMINOLOGY`

## Match modes

`EXACT`; `PHRASE`; `SEMANTIC`; `ENTITY`; reviewed `REGEX`

## Universal safeguards

1. A keyword match creates a candidate evidence signal, not a classification fact.
2. Domain and activity terms must normally co-occur within bounded source context.
3. Search snippets alone are insufficient evidence.
4. Duplicate sources do not increase confidence.
5. ‘Not found’ is not ‘absent’ without sufficient coverage.
6. Employment, training, dictionary, news-only, marketplace, and consumer contexts require explicit handling.
7. Local-language profiles are separately versioned and reviewed.
8. Service and buying terms attach only to active provider offerings.
9. Profiles cannot silently mutate after approval.
10. Completed jobs preserve exact profile versions.

## Activity keyword files

- [Part 1](activity-keywords-part-1.md)
- [Part 2](activity-keywords-part-2.md)
- [Part 3](activity-keywords-part-3.md)

## Sector domain keyword files

- [Construction](domain-keywords/construction-domain-keywords.md)
- [Education](domain-keywords/education-domain-keywords.md)
- [Energy](domain-keywords/energy-domain-keywords.md)
- [Finance](domain-keywords/finance-domain-keywords.md)
- [Food and Agriculture](domain-keywords/food-agriculture-domain-keywords.md)
- [Government](domain-keywords/government-domain-keywords.md)
- [Healthcare](domain-keywords/healthcare-domain-keywords.md)
- [Hospitality](domain-keywords/hospitality-domain-keywords.md)
- [Legal](domain-keywords/legal-domain-keywords.md)
- [Logistics](domain-keywords/logistics-domain-keywords.md)
- [Manufacturing and Industry](domain-keywords/manufacturing-industry-domain-keywords.md)
- [Nonprofit](domain-keywords/nonprofit-domain-keywords.md)
- [Real Estate](domain-keywords/real-estate-domain-keywords.md)
- [Retail](domain-keywords/retail-domain-keywords.md)
- [Technology](domain-keywords/technology-domain-keywords.md)
- [Travel](domain-keywords/travel-domain-keywords.md)

## Delivery boundary

These files define controlled documentation datasets. They do not implement search queries, connectors, classifiers, scoring, interfaces, or runtime evidence decisions.
