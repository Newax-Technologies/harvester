# Harvester Sector, Domain, Activity and Keyword Taxonomy Index

Status: **Proposed**

Version: **1.0**

Date: **3 August 2026**

Implementation status: **Not implemented**

This directory contains the controlled broad-sector, product-or-service-domain, business-activity, and discovery-keyword registries used by the Harvester Services and Opportunity Model.

The locked classification chain is:

```text
Broad Sector
→ Product or Service Domain
→ Domain-Specific Activity
→ Approved Domain–Activity Combination
→ Active Provider Offering
→ Domain and Activity Keywords
→ Service-Specific Signals
→ Verified Evidence
→ Supported Opportunity
→ Qualified Lead
```

## Governing documents

- [Broad Sector Registry and Selection Framework](broad-sector-registry.md)
- [Canonical Activity Registry and Domain Mappings](activity-registry.md)
- [Keyword Taxonomy Index](keywords/README.md)
- [Harvester Services and Opportunity Model](../SERVICES.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
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
| Shared exclusion and negative-context profiles | 15 |

The activity library is shared for stable naming and reuse. Applicability remains domain-specific: every canonical domain has an explicit activity profile, and user selections remain independent for each domain.

The keyword library follows the same rule. Domain and activity terms are reusable identities, but each domain retains its own keyword profile, organization cues, exclusions, and version history.

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

Examples:

```text
Pharmaceuticals
→ Manufacturing; Formulating; Quality Control; Packaging; Distribution

Medical Devices
→ Designing; Manufacturing; Installing; Calibrating; Maintaining; Repairing

Hospitals
→ Diagnosing; Treating; Patient Monitoring; Clinical Documentation; Care Coordination

Legal Services
→ Advising; Drafting; Reviewing; Filing; Representing; Case Management
```

## Keyword classification

The complete keyword dataset is indexed by [Keyword Taxonomy Index](keywords/README.md).

Keyword layers are deliberately separated:

```text
Domain identity terms
Activity terms
Organization cues
Exclusions and negative context
Service-specific problem and buying signals
```

The first four layers help discover and classify evidence. The service-specific layer exists only after the provider activates a relevant offering.

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
10. Domain keywords, activity keywords, organization cues, exclusions, and service-specific signals remain separately versioned.
11. Service-gap, buying-intent, competitor, existing-solution, and problem-signal keywords require an active provider offering.
12. Overlapping sectors and domains must not duplicate organizations, evidence, opportunities, scores, exports, or outreach packages.
13. Completed harvest jobs preserve the registry, mapping, offering, keyword, evidence, and scoring versions used when they ran.

## Delivery boundary

The broad-sector, domain, canonical-activity, activity-profile, domain-assignment, domain-keyword, activity-keyword, organization-cue, and exclusion datasets are **defined and repository-integrated documentation**.

They do not implement database records, migrations, APIs, search indexes, embeddings, classifiers, interface controls, activity detection, provider-service catalogues, evidence rules, scoring behaviour, or releases.

The taxonomy documentation is complete for the current 16-sector registry, but runtime implementation is not complete until the corresponding engineering work is built and verified.
