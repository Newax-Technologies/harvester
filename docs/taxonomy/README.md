# Harvester Sector, Domain, Activity and Keyword Taxonomy Index

Status: **Authoritative taxonomy index**  
Version: **2.1**  
Date: **6 August 2026**  
Implementation status: **Controlled documentation datasets; runtime sector-pack implementation remains planned**

This directory contains Harvester's canonical broad-sector, product-and-service-domain, business-activity, discovery-keyword, lead-signal, role, contact-route, source-suitability, exclusion, and evidence-control registries.

The registries are inputs to [Sector Pack Runtime Model](../architecture/sector-pack-runtime-model.md). They are not separate application schemas and do not independently prove a lead or opportunity.

## 1. Authority sequence

1. [Agency Intelligence Re-baseline](../architecture/agency-intelligence-rebaseline.md)
2. [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
3. [Sector Pack Runtime Model](../architecture/sector-pack-runtime-model.md)
4. [Harvester Services and Opportunity Model](../SERVICES.md)
5. [Provider Portfolio and Lead-Generation Profile Model](../architecture/provider-portfolio-and-lead-generation-profile-model.md)
6. [Broad Sector Registry and Selection Framework](broad-sector-registry.md)
7. [Canonical Activity Registry and Domain Mappings](activity-registry.md)
8. [Keyword Taxonomy and Lead-Signal Index](keywords/README.md)
9. [Keyword Plan Application Map](keywords/keyword-plan-application-map.md)
10. [Sector Keyword Connection Matrix](keywords/01-sector-keyword-connection-matrix.md)
11. Sector-specific domain registries and controlled profile datasets
12. [Agency Intelligence Implementation Sequence](../delivery/agency-intelligence-implementation-sequence.md)

A lower taxonomy document may add terms, mappings, examples, or source guidance. It cannot weaken active offering, evidence, source-policy, compliance, contact, tenant, or review requirements.

## 2. Locked classification and opportunity chain

```text
Broad Sector
→ selected Product or Service Domains
→ independent Activities for every selected Domain
→ approved Domain–Activity combinations
→ active Provider Offerings
→ Domain and Activity discovery profiles
→ offering-specific Pains, Needs, Signals, and Exclusions
→ source-appropriate Query Families
→ evidence, Coverage, Freshness, and Contradiction review
→ resolved Entities and Roles
→ Qualification
→ Opportunity Scoring Model v3
→ Decision and controlled Output
```

The order matters. A keyword result cannot jump directly to a qualified or contact-ready lead, despite humanity's persistent belief that more rows equal more truth.

## 3. Registry coverage

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

These counts describe repository-integrated documentation. They do not prove runtime tables, migrations, APIs, search indexes, classifiers, interfaces, benchmarks, or production activation.

## 4. Required keyword reading sequence

Use the [Keyword Plan Application Map](keywords/keyword-plan-application-map.md) for the authoritative keyword-documentation and implementation order.

Use the [Sector Keyword Connection Matrix](keywords/01-sector-keyword-connection-matrix.md) to resolve every sector through:

```text
sector domain registry
→ domain-to-activity applicability
→ sector domain keyword registry
→ shared activity keywords
→ offering-specific signals
→ source and query controls
→ evidence and validation controls
```

The application map and matrix provide navigation and dependency control. They do not replace the underlying canonical registries or runtime governance.

## 5. Sector-specific domain registries

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

## 6. Activity applicability

The complete activity dataset is indexed by [Canonical Activity Registry and Domain Mappings](activity-registry.md).

Applicability guidance:

```text
CORE
COMMON
OPTIONAL
NOT_APPLICABLE
```

The shared activity library provides stable identities. Applicability and user selection remain domain-specific.

Rules:

- selecting an activity for one domain never activates it for another domain;
- guidance does not prove that a target performs the activity;
- activity evidence remains source- and date-backed;
- tenant overlays may adjust approved defaults but cannot mutate canonical records;
- completed jobs retain exact activity-registry and selection versions.

## 7. Keyword and signal layers

The [Keyword Taxonomy and Lead-Signal Index](keywords/README.md) keeps these layers separate:

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
Offering-specific problem, buying, competitor, replacement, integration, and existing-solution profiles
Locale and transliteration packs
Evidence and validation controls
```

Match modes remain explicit:

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

A semantic or regex match is not a superior form of evidence merely because it required more computing.

## 8. Runtime sector packs

A runtime `SectorPackVersion` pins:

- canonical sector, domain, activity, keyword, signal, role, contact, source, and control-profile versions;
- organization, person, facility, product, service, project, employment, procurement, pain, need, lead, data, integration, and compliance definitions;
- conditional input schema;
- qualification and capability defaults;
- locale and tenant overlays;
- benchmark dataset;
- activation and rollback state.

Healthcare and Education are the first required operational packs. Their runtime scope, data restrictions, project types, roles, pains, needs, lead types, and integrations are defined in the Sector Pack Runtime Model.

## 9. Tenant overlays

Tenant or client overlays may:

- add aliases and approved locale terms;
- disable irrelevant defaults;
- add custom exclusions;
- select independent activities;
- configure weights within approved bounds;
- attach active provider offerings;
- define market-specific evidence and output rules.

They may not:

- alter canonical IDs;
- delete canonical history;
- turn unsupported evidence into fact;
- bypass source or compliance policy;
- change another tenant's configuration;
- make a keyword match a qualification or scoring decision.

## 10. Locked rules

1. Broad sectors are multi-select.
2. Domains are selected within sectors and may reuse canonical identity across sectors.
3. Every selected domain receives its own activity selection.
4. Activities never propagate automatically across domains.
5. Only approved and operationally active offerings may produce opportunity assessments.
6. Keywords discover evidence candidates; they do not prove sector, domain, activity, need, opportunity, authority, consent, contact eligibility, or qualification.
7. Direct intent, procurement, events, operational pain, technology, roles, and contactability remain separate evidence dimensions.
8. Offering-specific problem, competitor, replacement, integration, and existing-solution logic requires an active offering.
9. Decision-maker discovery follows entity resolution.
10. Public contact information does not override suppression, consent, jurisdiction, route, channel, or client policy.
11. Positive opportunities require negative, contradiction, freshness, closure, cancellation, award, and non-applicability checks where relevant.
12. Raw keyword counts never become a lead score.
13. Overlapping sectors, domains, profiles, and clients must not duplicate identity, evidence, opportunities, scores, outputs, or cost.
14. Activated sector-pack and profile versions are immutable.
15. Completed jobs retain exact taxonomy, pack, overlay, offering, keyword, signal, role, source, evidence, qualification, scoring, and output versions.
16. Healthcare patient-level marketing data and Education protected student or minor data remain restricted according to pack policy.
17. Every sector-to-domain-to-activity-to-keyword connection resolves through the approved application map and connection matrix rather than undocumented file-name assumptions.

## 11. Runtime delivery references

- [Sector Pack Runtime Model](../architecture/sector-pack-runtime-model.md)
- [Keyword Plan Application Map](keywords/keyword-plan-application-map.md)
- [Sector Keyword Connection Matrix](keywords/01-sector-keyword-connection-matrix.md)
- [Keyword Profile Development Plan](keywords/keyword-profile-development-plan.md)
- [Keyword Profile Implementation Plan](keywords/keyword-profile-implementation-plan.md)
- [Keyword and Evidence Profile Integration Addendum](../architecture/keyword-evidence-profile-integration-addendum.md)
- [Keyword Profile Runtime Delivery Plan](../delivery/keyword-profile-runtime-delivery-plan.md)
- [Keyword Profile Delivery Addendum](../delivery/keyword-profile-delivery-addendum.md)
- [Agency Intelligence Implementation Sequence](../delivery/agency-intelligence-implementation-sequence.md)

## 12. Delivery boundary

The taxonomy registries are controlled documentation datasets. Runtime completion requires:

- database records and migrations;
- immutable version and activation lifecycle;
- tenant overlays;
- APIs and frontend workspaces;
- query preview and source execution;
- evidence, coverage, contradiction, and provenance links;
- qualification and Opportunity Scoring Model v3 integration;
- sector and locale benchmark datasets;
- security, privacy, accessibility, performance, migration, and exact-head release verification.
