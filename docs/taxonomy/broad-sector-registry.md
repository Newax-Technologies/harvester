# Harvester Broad Sector Registry and Selection Framework

Status: **Proposed**

Version: **1.0**

Date: **3 August 2026**

Implementation status: **Not implemented.** This document defines the approved product direction for the first-stage target-market taxonomy.

Authority:

- [Harvester Standalone Product Roadmap](../ROADMAP.md) remains the authoritative delivery roadmap.
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md) remains authoritative for evidence, decisions, confidence, operations, and learning.
- [Harvester Services and Opportunity Model](../SERVICES.md) remains authoritative for provider offerings, target markets, opportunity signals, qualification, and generation rules.
- This registry defines the broad-sector selection layer subordinate to those documents.

Harvester should identify commercially relevant opportunities by understanding what a provider offers and which businesses are likely to need it. The taxonomy must reduce noise rather than merely classify the internet.

## 1. Purpose

This document defines the broad-sector layer of the Harvester target-market model.

Broad sectors are the user's first market selections. They determine which product or service domains Harvester presents next while allowing one target profile to span several markets.

The locked hierarchy is:

```text
Broad Sector
→ Product or Service Domain
→ Domain-Specific Activities
→ Product–Activity Combination
→ Provider Services
→ Keywords and Evidence
→ Service Gap
→ Opportunity
→ Lead
```

## 2. Governing model

1. A workspace may select one or more broad sectors.
2. Each broad sector may contain multiple product or service domains.
3. The same canonical domain may be mapped to more than one broad sector.
4. Each selected domain has its own activity group and activity selections.
5. An activity selected for one domain must not automatically apply to another domain.
6. The user must approve the resulting domain–activity combinations before lead discovery begins.
7. Only services actively offered by the provider may be assessed for gaps.
8. Keywords create evidence signals; they do not independently prove a gap.
9. Matching several sectors or combinations must not duplicate one target organization, its evidence, or its opportunity score.

## 3. Broad sector registry

The first release provides the following 16 broad sectors. They are market-entry filters, not mutually exclusive legal classifications.

| Code | Broad sector | Scope | Example domains |
| --- | --- | --- | --- |
| BS-001 | Healthcare | Organizations delivering healthcare or dealing with medicines, medical products, diagnostics, treatment, rehabilitation, or care services. | Pharmaceuticals; medical devices; diagnostics; hospital supplies; rehabilitation; healthcare services |
| BS-002 | Education | Organizations delivering education, training, assessment, research, certification, or learning content. | School education; higher education; vocational training; EdTech; research; learning content |
| BS-003 | Food and Agriculture | Organizations producing, processing, storing, distributing, or selling agricultural, livestock, dairy, fishery, food, or beverage products. | Crops; livestock; dairy; fisheries; food products; beverages; farm inputs |
| BS-004 | Real Estate | Organizations developing, selling, leasing, operating, or managing residential, commercial, industrial, or mixed-use property. | Residential property; commercial property; industrial property; brokerage; property management; facilities |
| BS-005 | Construction | Organizations designing, building, supplying, installing, or maintaining buildings and infrastructure. | Contracting; architecture; engineering; construction materials; building services; fit-out |
| BS-006 | Legal | Organizations delivering legal, regulatory, case, documentation, registration, dispute-resolution, or compliance services. | Corporate law; litigation; intellectual property; tax law; compliance; legal documentation |
| BS-007 | Finance | Organizations handling banking, financing, payments, investment, protection, accounting, audit, tax, and related financial operations. | Islamic banking; fintech; payments; Takaful; investment; accounting; audit; tax; microfinance |
| BS-008 | Retail | Organizations selling products directly to consumers through stores, chains, marketplaces, or digital channels. | Grocery; apparel; electronics; furniture; beauty; automotive; luxury; online retail |
| BS-009 | Hospitality | Organizations providing accommodation, guest services, venue operations, and related hospitality experiences. | Hotels; resorts; guest houses; serviced apartments; venues; guest services |
| BS-010 | Travel | Organizations arranging movement, tourism, ticketing, tours, pilgrimage, and destination services. | Travel agencies; tour operators; Hajj and Umrah; ticketing; destination services |
| BS-011 | Manufacturing and Industry | Organizations transforming, assembling, fabricating, packaging, or producing physical goods and industrial products. | Pharmaceuticals; textiles; food; electronics; chemicals; metals; machinery; packaging |
| BS-012 | Logistics | Organizations moving, storing, sorting, delivering, or fulfilling products, parcels, documents, and freight. | Postal and courier; freight; warehousing; fulfilment; cold chain; fleet; last-mile; shipping |
| BS-013 | Energy | Organizations producing, distributing, installing, managing, or monitoring energy and essential utility infrastructure. | Power; solar; renewable energy; fuel products; electricity; gas; water; utility operations |
| BS-014 | Technology | Organizations building, operating, integrating, hosting, protecting, or selling software, digital products, communications, and technology infrastructure. | Software and SaaS; IT services; telecom; data centres; cloud; cybersecurity; digital products |
| BS-015 | Government | Public authorities and institutions responsible for administration, regulation, municipal operations, public services, and public safety. | Federal; provincial; local government; municipal services; regulators; public safety |
| BS-016 | Nonprofit | Mission-led organizations operating for public benefit, membership, charity, development, relief, professional representation, or community service. | NGOs; charities; foundations; Zakat; Waqf; associations; chambers; professional bodies |

### 3.1 Sector-specific domain registries

Broad-sector rows define market entry points, not the complete domain datasets. Detailed domain definitions belong in controlled sector-specific registries.

- [Healthcare Product and Service Domain Registry](healthcare-domain-registry.md)
  - Defines all 142 canonical product and service domains for `BS-001 Healthcare`
  - Groups them across medicines, devices, supplies, clinical services, digital health, operations, research, education, and public health
  - Provides the 40-domain first-release presentation shortlist
  - Defines Healthcare-specific activity separation, cross-sector reuse, safeguards, and acceptance criteria

## 4. Multi-sector and reusable-domain rules

Broad sectors are deliberately non-exclusive. A target business may operate across several markets, and one canonical domain may be relevant to several sectors.

Harvester must preserve one domain identity while allowing several sector mappings.

| Example business | Selected sectors | Canonical domain | Activities for that domain |
| --- | --- | --- | --- |
| Pharmaceutical manufacturer | Healthcare; Manufacturing and Industry | Pharmaceuticals | Manufacturing; packaging; quality testing; export |
| Pharmaceutical distributor | Healthcare; Logistics | Pharmaceuticals | Importing; distribution; warehousing; cold storage |
| Food processor | Food and Agriculture; Manufacturing and Industry | Food products | Processing; manufacturing; packaging; distribution |
| Hotel booking platform | Hospitality; Travel; Technology | Accommodation booking | Publishing; booking; payments; platform operations |
| Postal and courier operator | Logistics | Postal, courier and parcel delivery | Sorting; transporting; delivering; branch operations |

A broad-sector mapping gives context. It does not create a second copy of the domain.

## 5. Harvester user flow

### 5.1 Select broad sectors

The user chooses one or more markets to target.

### 5.2 Select domains within each sector

Harvester presents approved product and service domains mapped to the selected sectors.

A user may select more than one domain inside the same sector.

### 5.3 Configure activities separately for every domain

Each selected domain receives an independent activity group.

Selecting an activity in one domain has no effect on another domain.

Example:

```text
Healthcare

Pharmaceuticals
✓ Manufacturing
✓ Packaging
✓ Distribution
✗ Retail selling

Medical devices
✓ Importing
✓ Distribution
✓ Installation
✓ Maintenance
✗ Manufacturing
```

### 5.4 Approve target combinations

Harvester generates domain–activity combinations that the user may enable, disable, or prioritize.

### 5.5 Select provider services

The user identifies which services they actually offer for every approved target combination.

### 5.6 Review keywords and evidence profiles

Harvester recommends service-specific terms, problem signals, existing-solution signals, exclusions, and evidence thresholds.

### 5.7 Activate discovery

Only approved sector–domain–activity–service configurations may generate gaps and opportunities.

## 6. Domain and activity applicability

Activities come from a shared canonical activity library, but every domain receives its own allowed and recommended activity set.

This provides consistency without forcing irrelevant activities into the interface.

Examples:

- A pharmaceutical domain may expose manufacturing, formulation, testing, packaging, distribution, warehousing, promotion, selling, and disposal.
- A medical-device domain may expose manufacturing, importing, distribution, installation, calibration, maintenance, repair, leasing, refurbishing, and recycling.
- A legal domain may expose advising, representing, drafting, reviewing, filing, registering, investigating, mediating, and managing cases.
- A software domain may expose developing, publishing, licensing, implementing, integrating, reselling, hosting, maintaining, and supporting.

The system must not recommend nonsensical combinations merely because an activity exists globally.

## 7. Minimum data model

The sector layer uses canonical registries and many-to-many mappings. It must not hard-code every possible business as a unique sector.

| Entity | Minimum fields |
| --- | --- |
| `BroadSector` | `id`; `code`; `name`; `description`; `status`; `version` |
| `DomainDefinition` | `id`; `code`; `name`; `domain_type`; `description`; `status`; `version` |
| `SectorDomainApplicability` | `sector_id`; `domain_id`; `applicability`; `default_priority`; `qualification_guidance`; `status` |
| `TargetSectorSelection` | `id`; `workspace_id`; `sector_id`; `status`; `priority`; `geography`; `organization_size_rules` |
| `TargetDomainSelection` | `id`; `target_sector_selection_id`; `domain_id`; `status`; `priority` |
| `ActivityDefinition` | `id`; `code`; `name`; `activity_family`; `description`; `status` |
| `DomainActivityApplicability` | `domain_id`; `activity_id`; `applicability`; `recommended`; `priority`; `status` |
| `TargetDomainActivity` | `id`; `target_domain_selection_id`; `activity_id`; `status`; `priority`; `qualification_rules`; `exclusion_rules` |

Suggested applicability values:

```text
CORE
COMMON
OPTIONAL
SPECIALIZED
NOT_APPLICABLE
```

Suggested selection statuses:

```text
ACTIVE
PAUSED
EXPERIMENTAL
DISABLED
```

## 8. Product behaviour and safeguards

- Selecting a broad sector filters the next stage; it does not activate every domain in that sector.
- Selecting a domain does not activate every available activity.
- The same domain may appear under several sectors, but Harvester preserves one canonical domain identity.
- Duplicate sector mappings must not duplicate leads, organizations, evidence, or opportunity scores.
- A user may pause a sector, domain, activity, or combination without deleting historical evidence.
- Custom sectors and domains may be proposed, but should map to a canonical definition where possible.
- Broad sectors remain stable identifiers; labels may evolve through versioned display names and aliases.
- Manufacturing may exist as a broad market context and as a domain activity. Those meanings must remain distinct in storage and APIs.
- Every opportunity must retain the sector, domain, activity, provider offering, evidence, and decision path that produced it.

## 9. Non-negotiable relevance rule

```text
No selected sector
→ no domains available

No selected domain
→ no activities available

No approved domain–activity combination
→ no services assessed

No offered service
→ no service gap

No supported gap
→ no opportunity

No qualified opportunity
→ no lead
```

Keywords discover evidence. They do not independently establish a service gap.

## 10. Acceptance criteria

- The interface presents all 16 approved broad sectors.
- A user can select multiple broad sectors in one target profile.
- Each selected sector presents only mapped product or service domains.
- A user can select multiple domains inside the same sector.
- Each selected domain displays an independent activity group.
- Activities selected for one domain do not propagate to other domains.
- The user can enable, disable, and prioritize each domain–activity combination.
- The same target organization is not duplicated when it matches several selected sectors or combinations.
- Lead scoring records which sector, domain, activity, offered service, evidence, and gap produced the opportunity.
- No unselected service or unsupported service gap influences lead generation, scoring, exports, publication, or outreach preparation.
- Existing completed harvest jobs preserve the registry and mapping versions used when they ran.

## 11. Delivery boundary

This document defines the broad-sector layer only.

Sector-specific product-domain registries, domain-specific activity mappings, provider service catalogues, keyword profiles, evidence rules, and gap scoring require separate controlled datasets and implementation phases. The Healthcare domain registry is defined in [Healthcare Product and Service Domain Registry](healthcare-domain-registry.md).

The broad-sector registry and selection rules are **defined**, but they are not **implemented**, **integrated**, or **verified** until corresponding schema, migration, API, interface, test, and release work is complete.
