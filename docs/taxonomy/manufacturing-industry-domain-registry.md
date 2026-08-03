# Harvester Manufacturing and Industry Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-011 Manufacturing and Industry`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Manufacturing and Industry
→ select one or more domains
→ configure a separate activity group for each domain
→ approve domain–activity combinations
→ attach services the provider actually offers
→ configure keywords and evidence
→ assess supported opportunities
→ qualify leads
```

Selecting this sector does not select every domain or activity. Activities do not propagate between domains. Cross-sector reuse preserves one canonical domain identity and does not duplicate organizations, evidence, opportunities, or scores.

## 2. Registry summary

This registry contains **111 canonical domains** in **9 families**.

| Family | Name | Count |
| --- | --- | --- |
| `MFG-FNB` | Food, beverage and agricultural manufacturing | 12 |
| `MFG-LIF` | Life sciences and healthcare manufacturing | 10 |
| `MFG-TEX` | Textiles, apparel and leather | 11 |
| `MFG-CHE` | Chemicals, plastics and materials | 13 |
| `MFG-MET` | Metals, machinery and engineered products | 15 |
| `MFG-AUT` | Automotive, transport and mobility manufacturing | 11 |
| `MFG-ELE` | Electronics and technology hardware | 10 |
| `MFG-PKG` | Packaging, paper, furniture and consumer products | 12 |
| `MFG-OPS` | Industrial operations and support | 17 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Food, beverage and agricultural manufacturing

| Code | Domain |
| --- | --- |
| `MFG-FNB-001` | Food Manufacturing |
| `MFG-FNB-002` | Beverage Manufacturing |
| `MFG-FNB-003` | Dairy Processing |
| `MFG-FNB-004` | Meat and Poultry Processing |
| `MFG-FNB-005` | Seafood Processing |
| `MFG-FNB-006` | Grain Milling |
| `MFG-FNB-007` | Bakery Manufacturing |
| `MFG-FNB-008` | Confectionery Manufacturing |
| `MFG-FNB-009` | Edible Oil Processing |
| `MFG-FNB-010` | Sugar Processing |
| `MFG-FNB-011` | Tea and Coffee Processing |
| `MFG-FNB-012` | Animal Feed Manufacturing |

### 4.2 Life sciences and healthcare manufacturing

| Code | Domain |
| --- | --- |
| `MFG-LIF-001` | Pharmaceutical Manufacturing |
| `MFG-LIF-002` | Biopharmaceutical Manufacturing |
| `MFG-LIF-003` | Vaccine Manufacturing |
| `MFG-LIF-004` | Medical Device Manufacturing |
| `MFG-LIF-005` | Diagnostic Product Manufacturing |
| `MFG-LIF-006` | Surgical Instrument Manufacturing |
| `MFG-LIF-007` | Medical Consumables Manufacturing |
| `MFG-LIF-008` | Personal Protective Equipment Manufacturing |
| `MFG-LIF-009` | Clinical Nutrition Manufacturing |
| `MFG-LIF-010` | Cosmetics and Personal Care Manufacturing |

### 4.3 Textiles, apparel and leather

| Code | Domain |
| --- | --- |
| `MFG-TEX-001` | Fibre and Yarn Manufacturing |
| `MFG-TEX-002` | Textile Weaving |
| `MFG-TEX-003` | Textile Knitting |
| `MFG-TEX-004` | Dyeing and Finishing |
| `MFG-TEX-005` | Garment Manufacturing |
| `MFG-TEX-006` | Home Textile Manufacturing |
| `MFG-TEX-007` | Technical Textiles |
| `MFG-TEX-008` | Footwear Manufacturing |
| `MFG-TEX-009` | Leather Processing |
| `MFG-TEX-010` | Leather Goods Manufacturing |
| `MFG-TEX-011` | Carpet Manufacturing |

### 4.4 Chemicals, plastics and materials

| Code | Domain |
| --- | --- |
| `MFG-CHE-001` | Industrial Chemicals |
| `MFG-CHE-002` | Specialty Chemicals |
| `MFG-CHE-003` | Fertilizer Manufacturing |
| `MFG-CHE-004` | Paints and Coatings |
| `MFG-CHE-005` | Detergents and Cleaning Products |
| `MFG-CHE-006` | Plastics Manufacturing |
| `MFG-CHE-007` | Plastic Packaging |
| `MFG-CHE-008` | Rubber Products |
| `MFG-CHE-009` | Glass Manufacturing |
| `MFG-CHE-010` | Ceramics Manufacturing |
| `MFG-CHE-011` | Cement Manufacturing |
| `MFG-CHE-012` | Concrete Products |
| `MFG-CHE-013` | Composite Materials |

### 4.5 Metals, machinery and engineered products

| Code | Domain |
| --- | --- |
| `MFG-MET-001` | Steel Manufacturing |
| `MFG-MET-002` | Non-Ferrous Metals |
| `MFG-MET-003` | Metal Fabrication |
| `MFG-MET-004` | Casting and Foundry |
| `MFG-MET-005` | Machining and Precision Engineering |
| `MFG-MET-006` | Industrial Machinery |
| `MFG-MET-007` | Agricultural Machinery |
| `MFG-MET-008` | Construction Equipment |
| `MFG-MET-009` | Pumps and Compressors |
| `MFG-MET-010` | Valves and Piping Equipment |
| `MFG-MET-011` | Electrical Equipment |
| `MFG-MET-012` | Transformers and Switchgear |
| `MFG-MET-013` | Industrial Automation Equipment |
| `MFG-MET-014` | Tools and Hardware |
| `MFG-MET-015` | Fasteners and Components |

### 4.6 Automotive, transport and mobility manufacturing

| Code | Domain |
| --- | --- |
| `MFG-AUT-001` | Automobile Manufacturing |
| `MFG-AUT-002` | Commercial Vehicle Manufacturing |
| `MFG-AUT-003` | Motorcycle Manufacturing |
| `MFG-AUT-004` | Automotive Parts Manufacturing |
| `MFG-AUT-005` | Tyre Manufacturing |
| `MFG-AUT-006` | Battery Manufacturing |
| `MFG-AUT-007` | Rail Equipment Manufacturing |
| `MFG-AUT-008` | Marine Equipment Manufacturing |
| `MFG-AUT-009` | Aerospace Components |
| `MFG-AUT-010` | Electric Vehicle Components |
| `MFG-AUT-011` | Bicycle Manufacturing |

### 4.7 Electronics and technology hardware

| Code | Domain |
| --- | --- |
| `MFG-ELE-001` | Consumer Electronics Manufacturing |
| `MFG-ELE-002` | Computer Hardware Manufacturing |
| `MFG-ELE-003` | Telecommunications Equipment |
| `MFG-ELE-004` | Semiconductor and Electronic Components |
| `MFG-ELE-005` | Printed Circuit Boards |
| `MFG-ELE-006` | Sensors and Instrumentation |
| `MFG-ELE-007` | Control Systems |
| `MFG-ELE-008` | Solar Equipment Manufacturing |
| `MFG-ELE-009` | Lighting Products |
| `MFG-ELE-010` | Home Appliances |

### 4.8 Packaging, paper, furniture and consumer products

| Code | Domain |
| --- | --- |
| `MFG-PKG-001` | Paper and Pulp Manufacturing |
| `MFG-PKG-002` | Paper Packaging |
| `MFG-PKG-003` | Corrugated Packaging |
| `MFG-PKG-004` | Flexible Packaging |
| `MFG-PKG-005` | Labels and Printing |
| `MFG-PKG-006` | Wood Products |
| `MFG-PKG-007` | Furniture Manufacturing |
| `MFG-PKG-008` | Mattress Manufacturing |
| `MFG-PKG-009` | Household Products |
| `MFG-PKG-010` | Toys and Recreational Products |
| `MFG-PKG-011` | Jewellery Manufacturing |
| `MFG-PKG-012` | Office and School Supplies Manufacturing |

### 4.9 Industrial operations and support

| Code | Domain |
| --- | --- |
| `MFG-OPS-001` | Contract Manufacturing |
| `MFG-OPS-002` | Original Equipment Manufacturing |
| `MFG-OPS-003` | Private-Label Manufacturing |
| `MFG-OPS-004` | Industrial Design |
| `MFG-OPS-005` | Product Engineering |
| `MFG-OPS-006` | Tooling and Mould Making |
| `MFG-OPS-007` | Quality Testing |
| `MFG-OPS-008` | Calibration Services |
| `MFG-OPS-009` | Industrial Maintenance |
| `MFG-OPS-010` | Plant Engineering |
| `MFG-OPS-011` | Production Planning Systems |
| `MFG-OPS-012` | Manufacturing Execution Systems |
| `MFG-OPS-013` | Industrial IoT |
| `MFG-OPS-014` | Warehouse and Material Handling |
| `MFG-OPS-015` | Industrial Safety |
| `MFG-OPS-016` | Waste and Scrap Recovery |
| `MFG-OPS-017` | Industrial Energy Management |

## 5. First-release presentation shortlist

Food Manufacturing, Beverage Manufacturing, Pharmaceutical Manufacturing, Medical Device Manufacturing, Textile Manufacturing, Garment Manufacturing, Leather Products, Industrial Chemicals, Paints and Coatings, Plastics Manufacturing, Cement Manufacturing, Steel Manufacturing, Metal Fabrication, Industrial Machinery, Agricultural Machinery, Construction Equipment, Electrical Equipment, Automotive Manufacturing, Automotive Parts, Battery Manufacturing, Consumer Electronics, Telecommunications Equipment, Solar Equipment, Home Appliances, Paper and Packaging, Labels and Printing, Furniture Manufacturing, Contract Manufacturing, OEM Manufacturing, Private-Label Manufacturing, Product Engineering, Quality Testing, Industrial Maintenance, Production Planning, Manufacturing Execution Systems, Industrial IoT, Material Handling, Waste and Scrap Recovery, Industrial Energy Management.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Manufacturers:** Designing, Sourcing, Manufacturing, Assembling, Testing, Packaging
- **Contract manufacturers:** Quoting, Planning, Producing, Quality assuring, Delivering
- **Industrial equipment:** Manufacturing, Importing, Selling, Installing, Maintaining
- **Waste and scrap:** Collecting, Sorting, Dismantling, Recovering, Recycling, Reselling

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Pharmaceutical manufacturing | Healthcare | Formulating; manufacturing; testing |
| Food manufacturing | Food and Agriculture | Processing; packaging; distributing |
| Construction materials | Construction | Manufacturing; distributing; installing |
| Industrial IoT | Technology; Energy | Monitoring; automating; optimizing |

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

- The shortlist and all 111 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
