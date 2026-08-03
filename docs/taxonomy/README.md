# Harvester Sector and Domain Taxonomy Index

Status: **Proposed**

Version: **1.0**

Date: **3 August 2026**

Implementation status: **Not implemented**

This directory contains the controlled broad-sector and sector-specific product and service domain registries used by the Harvester Services and Opportunity Model.

The locked classification chain is:

```text
Broad Sector
→ Product or Service Domain
→ Domain-Specific Activity
→ Approved Domain–Activity Combination
→ Active Provider Offering
→ Keywords and Evidence
→ Supported Opportunity
→ Qualified Lead
```

## Governing documents

- [Broad Sector Registry and Selection Framework](broad-sector-registry.md)
- [Harvester Services and Opportunity Model](../SERVICES.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [Harvester Standalone Product Roadmap](../ROADMAP.md)

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

## Locked rules

1. Broad sectors are multi-select.
2. Domains are multi-select within each selected sector.
3. Every selected domain receives its own independent activity group.
4. Activities selected for one domain never propagate automatically to another domain.
5. The same canonical domain may be mapped to several sectors without creating duplicate identities.
6. The user must approve domain–activity combinations before attaching provider services.
7. Only active services actually offered by the provider may generate opportunity assessments.
8. Keywords discover evidence; they do not independently prove an activity, service gap, or opportunity.
9. Overlapping sectors and domains must not duplicate organizations, evidence, opportunities, scores, exports, or outreach packages.
10. Completed harvest jobs preserve the registry, mapping, offering, keyword, evidence, and scoring versions used when they ran.

## Delivery boundary

These registries define controlled taxonomy datasets. They do not implement database records, migrations, APIs, interface controls, activity mappings, provider service catalogues, keyword profiles, evidence rules, scoring behaviour, or releases.

The taxonomy is **defined**, but it is not **implemented**, **integrated**, **CI Green**, or **complete** until the corresponding engineering work is verified.
