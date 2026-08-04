# Harvester Sector, Domain, Activity and Keyword Taxonomy Index

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This directory contains the controlled broad-sector, product-or-service-domain, business-activity, discovery-keyword, lead-signal, role-cue, source-suitability, and evidence-governance registries used by the Harvester Services and Opportunity Model.

The locked classification and lead-generation chain is:

```text
Broad Sector
→ Product or Service Domain
→ Domain-Specific Activity
→ Approved Domain–Activity Combination
→ Active Provider Offering
→ Domain and Activity Keywords
→ Lead-Generation Signal Profile
→ Source-Appropriate Query Families
→ Evidence, Freshness and Contradiction Review
→ Responsible-Role and Contact Assessment
→ Supported Opportunity
→ Qualified Lead
```

## Governing documents

- [Broad Sector Registry and Selection Framework](broad-sector-registry.md)
- [Canonical Activity Registry and Domain Mappings](activity-registry.md)
- [Keyword Taxonomy and Lead-Signal Index](keywords/README.md)
- [Harvester Services and Opportunity Model](../SERVICES.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [Provider Portfolio and Lead-Generation Profile Model](../architecture/provider-portfolio-and-lead-generation-profile-model.md)
- [Harvester Standalone Product Roadmap](../ROADMAP.md)

## Registry coverage

| Controlled layer | Coverage |
| --- | ---: |
| Broad sectors | 16 |
| Canonical product and service domains | 1,586 |
| Canonical business activities | 519 |
| Explicit domain-to-activity-profile assignments | 1,586 |
| Separate domain keyword profiles | 1,586 |
| Separate activity keyword profiles | 519 |
| Shared organization-cue profiles | 8 |
| Shared exclusion and negative-context profiles | 28 |
| Evidence-control profiles | 9 |
| Reusable lead-generation signal profiles | 29 |
| Functional decision-maker role groups | 20 |
| Contact-route profiles | 8 |
| Sector lead-generation overlays | 16 |
| Source classes with signal guidance | 14 |
| Governed query families | 10 |

The activity library is shared for stable naming and reuse. Applicability remains domain-specific: every canonical domain has an explicit activity profile, and user selections remain independent for each domain.

The keyword library follows the same rule. Domain and activity terms are reusable identities, but every domain retains its own keyword profile, organization cues, exclusions, and version history.

Lead-generation signals are reusable commercial-event and operational-evidence identities. Their relevance, weights, evidence requirements, and disqualifiers remain specific to the provider offering and lead-generation profile.

## Sector-specific domain registries

| Sector code | Broad sector | Registry | Canonical domains |
| --- | --- | --- | ---: |
| `BS-001` | Healthcare | [Healthcare Product and Service Domain Registry](healthcare-domain-registry.md) | 142 |
| `BS-002` | Education | [Education Product and Service Domain Registry](education-domain-registry.md) | 95 |
| `BS-003` | Food and Agriculture | [Food and Agriculture Product and Service Domain Registry](food-agriculture-domain-registry.md) | 103 |
| `BS-004` | Real Estate | [Real Estate Product and Service Domain Registry](real-estate-domain-registry.md) | 88 |
| `BS-005` | Construction | [Construction Product and Service Domain Registry](construction-domain-registry.md) | 93 |
| `BS-006` | Legal | [Legal Product and Service Domain Registry](legal-domain-registry.md) | 97 |
| `BS-007` | Finance | [Finance Product and Service Domain Registry](finance-domain-registry.md) | 109 |
| `BS-008` | Retail | [Retail Product and Service Domain Registry](retail-domain-registry.md) | 84 |
| `BS-009` | Hospitality | [Hospitality Product and Service Domain Registry](hospitality-domain-registry.md) | 79 |
| `BS-010` | Travel | [Travel Product and Service Domain Registry](travel-domain-registry.md) | 75 |
| `BS-011` | Manufacturing and Industry | [Manufacturing and Industry Product and Service Domain Registry](manufacturing-industry-domain-registry.md) | 111 |
| `BS-012` | Logistics | [Logistics Product and Service Domain Registry](logistics-domain-registry.md) | 101 |
| `BS-013` | Energy | [Energy Product and Service Domain Registry](energy-domain-registry.md) | 94 |
| `BS-014` | Technology | [Technology Product and Service Domain Registry](technology-domain-registry.md) | 127 |
| `BS-015` | Government | [Government Product and Service Domain Registry](government-domain-registry.md) | 96 |
| `BS-016` | Nonprofit | [Nonprofit Product and Service Domain Registry](nonprofit-domain-registry.md) | 92 |
|  | **Total** |  | **1,586** |

## Activity applicability

The complete activity dataset is indexed by [Canonical Activity Registry and Domain Mappings](activity-registry.md).

Applicability values are:

```text
CORE
COMMON
OPTIONAL
NOT_APPLICABLE
```

`CORE`, `COMMON`, and `OPTIONAL` guide the interface. They do not prove that a target performs an activity. `NOT_APPLICABLE` is represented by the activity being absent from a domain's default profile.

## Keyword and lead-signal layers

The complete keyword and signal dataset is indexed by [Keyword Taxonomy and Lead-Signal Index](keywords/README.md).

The layers remain deliberately separate:

```text
Domain identity terms
Activity terms
Organization cues
Exclusions and negative context
Lead-generation signals
Sector overlays
Source-to-signal suitability
Decision-maker role cues
Contact-route cues
Offering-specific problem, buying, competitor and existing-solution logic
```

The first four layers help discover and classify organizations. Lead-signal and sector-overlay layers help determine why a target may be relevant now. Offering-specific logic decides whether that relevance can become an opportunity for the selected provider service.

A match must retain its match mode:

```text
EXACT
PHRASE
SEMANTIC
ENTITY
REGEX
```

## Locked rules

1. Broad sectors are multi-select.
2. Domains are multi-select within each selected sector.
3. Every selected domain receives its own independent activity group.
4. Activities selected for one domain never propagate automatically to another domain.
5. The same canonical domain may be mapped to several sectors without creating duplicate identities.
6. Every canonical domain has an explicit default activity profile and a separate keyword profile.
7. The user must approve domain–activity combinations before attaching provider services.
8. Only active services actually offered by the provider may generate opportunity assessments.
9. Keywords discover evidence; they do not independently prove a domain, activity, service gap, opportunity, or lead.
10. Direct intent, procurement, business events, operational pain, technology footprint, role cues, and contactability remain separate evidence dimensions.
11. Service-gap, buying-intent, competitor, existing-solution, and problem-signal evaluation requires an active provider offering.
12. Decision-maker discovery follows entity resolution; contact-ready status follows opportunity support and lawful-contact checks.
13. Job posts, reviews, tenders, news, directories, maps, social posts, and technology listings are evaluated according to their source-signal suitability.
14. Positive opportunities require negative, contradiction, freshness, closure, cancellation, and award checks where applicable.
15. Raw keyword counts never become a lead score.
16. Overlapping sectors and domains must not duplicate organizations, evidence, opportunities, scores, exports, or outreach packages.
17. Completed harvest jobs preserve the taxonomy, mapping, offering, keyword, signal, role, source, evidence, qualification, and scoring versions used when they ran.

## Delivery boundary

The broad-sector, domain, activity, keyword, signal, role, source, and control-profile datasets are **defined and repository-integrated documentation**.

They do not implement database records, migrations, APIs, interface controls, query execution, search indexes, activity detection, provider-service catalogues, evidence rules, scoring behavior, contact eligibility, outreach, or releases.

The taxonomy documentation is strengthened for the current 16-sector registry, but runtime implementation is not complete until the corresponding engineering work is built and verified.
