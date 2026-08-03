# Harvester Food and Agriculture Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-003 Food and Agriculture`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Food and Agriculture
→ select one or more domains
→ configure a separate activity group for each domain
→ approve domain–activity combinations
→ attach services the provider actually offers
→ configure keywords and evidence
→ assess supported opportunities
→ qualify leads
```

Selecting this sector does not select every domain or activity. Activities do not propagate between domains. Cross-sector reuse must preserve one canonical domain identity and must not duplicate organizations, evidence, opportunities, or scores.

## 2. Registry summary

This registry contains **103 canonical domains** in **6 families**.

| Family | Name | Count |
| --- | --- | --- |
| `FAG-CRO` | Crops and cultivation | 20 |
| `FAG-LIV` | Livestock, dairy and animal products | 16 |
| `FAG-AQU` | Fisheries and aquaculture | 9 |
| `FAG-INP` | Agricultural inputs and equipment | 16 |
| `FAG-PRO` | Food and beverage products | 22 |
| `FAG-OPS` | Agrifood services and infrastructure | 20 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Crops and cultivation

| Code | Domain |
| --- | --- |
| `FAG-CRO-001` | Cereal Crops |
| `FAG-CRO-002` | Rice |
| `FAG-CRO-003` | Wheat |
| `FAG-CRO-004` | Maize and Corn |
| `FAG-CRO-005` | Pulses and Legumes |
| `FAG-CRO-006` | Oilseed Crops |
| `FAG-CRO-007` | Sugar Crops |
| `FAG-CRO-008` | Cotton and Fibre Crops |
| `FAG-CRO-009` | Vegetables |
| `FAG-CRO-010` | Fruits |
| `FAG-CRO-011` | Citrus Fruits |
| `FAG-CRO-012` | Dates |
| `FAG-CRO-013` | Nuts and Dry Fruits |
| `FAG-CRO-014` | Herbs and Spices |
| `FAG-CRO-015` | Tea and Coffee |
| `FAG-CRO-016` | Medicinal and Aromatic Plants |
| `FAG-CRO-017` | Floriculture |
| `FAG-CRO-018` | Nurseries and Seedlings |
| `FAG-CRO-019` | Greenhouse Farming |
| `FAG-CRO-020` | Hydroponics and Controlled-Environment Agriculture |

### 4.2 Livestock, dairy and animal products

| Code | Domain |
| --- | --- |
| `FAG-LIV-001` | Cattle Farming |
| `FAG-LIV-002` | Buffalo Farming |
| `FAG-LIV-003` | Sheep and Goat Farming |
| `FAG-LIV-004` | Poultry Farming |
| `FAG-LIV-005` | Egg Production |
| `FAG-LIV-006` | Dairy Farming |
| `FAG-LIV-007` | Milk Collection |
| `FAG-LIV-008` | Animal Feed |
| `FAG-LIV-009` | Animal Breeding and Genetics |
| `FAG-LIV-010` | Veterinary Livestock Services |
| `FAG-LIV-011` | Meat Production |
| `FAG-LIV-012` | Slaughterhouses and Abattoirs |
| `FAG-LIV-013` | Leather and Hides |
| `FAG-LIV-014` | Beekeeping and Honey |
| `FAG-LIV-015` | Camel Farming |
| `FAG-LIV-016` | Equine and Working Animals |

### 4.3 Fisheries and aquaculture

| Code | Domain |
| --- | --- |
| `FAG-AQU-001` | Marine Fisheries |
| `FAG-AQU-002` | Inland Fisheries |
| `FAG-AQU-003` | Fish Farming |
| `FAG-AQU-004` | Shrimp and Prawn Farming |
| `FAG-AQU-005` | Hatcheries |
| `FAG-AQU-006` | Aquaculture Feed |
| `FAG-AQU-007` | Seafood Processing |
| `FAG-AQU-008` | Cold-Water Fisheries |
| `FAG-AQU-009` | Fish Markets and Auctions |

### 4.4 Agricultural inputs and equipment

| Code | Domain |
| --- | --- |
| `FAG-INP-001` | Seeds |
| `FAG-INP-002` | Fertilizers |
| `FAG-INP-003` | Crop Protection Products |
| `FAG-INP-004` | Soil Conditioners |
| `FAG-INP-005` | Irrigation Equipment |
| `FAG-INP-006` | Farm Machinery |
| `FAG-INP-007` | Tractors and Implements |
| `FAG-INP-008` | Greenhouse Equipment |
| `FAG-INP-009` | Livestock Equipment |
| `FAG-INP-010` | Poultry Equipment |
| `FAG-INP-011` | Dairy Equipment |
| `FAG-INP-012` | Aquaculture Equipment |
| `FAG-INP-013` | Agricultural Drones |
| `FAG-INP-014` | Farm Sensors and Telemetry |
| `FAG-INP-015` | Agricultural Packaging |
| `FAG-INP-016` | Farm Energy and Solar Systems |

### 4.5 Food and beverage products

| Code | Domain |
| --- | --- |
| `FAG-PRO-001` | Grains and Milling Products |
| `FAG-PRO-002` | Flour and Bakery Ingredients |
| `FAG-PRO-003` | Edible Oils and Fats |
| `FAG-PRO-004` | Sugar and Sweeteners |
| `FAG-PRO-005` | Fresh Produce |
| `FAG-PRO-006` | Frozen Foods |
| `FAG-PRO-007` | Canned Foods |
| `FAG-PRO-008` | Dairy Products |
| `FAG-PRO-009` | Meat and Poultry Products |
| `FAG-PRO-010` | Seafood Products |
| `FAG-PRO-011` | Bakery Products |
| `FAG-PRO-012` | Confectionery |
| `FAG-PRO-013` | Snacks |
| `FAG-PRO-014` | Spices and Condiments |
| `FAG-PRO-015` | Sauces and Preserves |
| `FAG-PRO-016` | Ready-to-Eat Meals |
| `FAG-PRO-017` | Beverages |
| `FAG-PRO-018` | Bottled Water |
| `FAG-PRO-019` | Juices |
| `FAG-PRO-020` | Tea and Coffee Products |
| `FAG-PRO-021` | Infant and Clinical Foods |
| `FAG-PRO-022` | Halal Food Products |

### 4.6 Agrifood services and infrastructure

| Code | Domain |
| --- | --- |
| `FAG-OPS-001` | Farm Management Services |
| `FAG-OPS-002` | Agricultural Extension Services |
| `FAG-OPS-003` | Crop Testing Laboratories |
| `FAG-OPS-004` | Food Testing Laboratories |
| `FAG-OPS-005` | Quality Certification |
| `FAG-OPS-006` | Halal Certification |
| `FAG-OPS-007` | Commodity Trading |
| `FAG-OPS-008` | Agricultural Cooperatives |
| `FAG-OPS-009` | Produce Markets |
| `FAG-OPS-010` | Grain Storage |
| `FAG-OPS-011` | Silos |
| `FAG-OPS-012` | Cold Storage |
| `FAG-OPS-013` | Pack Houses and Grading Centres |
| `FAG-OPS-014` | Food Warehousing |
| `FAG-OPS-015` | Refrigerated Transport |
| `FAG-OPS-016` | Agricultural Export Services |
| `FAG-OPS-017` | Farm-to-Market Platforms |
| `FAG-OPS-018` | Food Traceability Systems |
| `FAG-OPS-019` | Agricultural Finance Services |
| `FAG-OPS-020` | Agricultural Insurance and Takaful |

## 5. First-release presentation shortlist

The interface should initially present these grouped entries, with search and family expansion into the full registry:

Cereal Crops, Fruits, Vegetables, Livestock, Poultry, Dairy, Fisheries, Seeds, Fertilizers, Crop Protection Products, Farm Machinery, Irrigation Equipment, Fresh Produce, Grains and Milling, Dairy Products, Meat and Poultry Products, Seafood Products, Bakery Products, Beverages, Ready-to-Eat Foods, Spices and Condiments, Food Processing, Food Packaging, Cold Storage, Grain Storage, Food Warehousing, Refrigerated Transport, Commodity Trading, Food Testing, Halal Certification, Produce Markets, Agricultural Cooperatives, Farm Management Services, Food Traceability Systems, Agricultural Export Services, Farm-to-Market Platforms.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Crops:** Growing, Harvesting, Grading, Packaging, Storing, Exporting
- **Food products:** Processing, Manufacturing, Packaging, Distributing, Wholesaling, Retailing
- **Livestock:** Breeding, Raising, Feeding, Processing, Trading, Transporting
- **Cold storage:** Receiving, Storing, Monitoring, Dispatching, Transporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Food products | Manufacturing and Industry; Retail | Processing; manufacturing; packaging; selling |
| Cold storage | Logistics; Energy | Warehousing; temperature monitoring; distributing |
| Agricultural machinery | Manufacturing and Industry; Retail | Manufacturing; importing; selling; servicing |
| Food testing laboratories | Healthcare; Technology | Testing; certifying; reporting |

## 8. Required domain metadata

```text
id
code
name
description
domain_type
family_code
status
version
aliases
sector_mappings
allowed_activity_ids
recommended_activity_ids
qualification_guidance
exclusion_guidance
created_at
updated_at
```

## 9. Acceptance criteria

- The shortlist and all 103 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
