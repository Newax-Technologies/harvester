# Harvester Manufacturing and Industry Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **111** canonical domains in `BS-011 Manufacturing and Industry` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-011-AP-001` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-QLT-016`; `ACT-LOG-001`; `ACT-LOG-002`; `ACT-COM-001`; `ACT-SRC-008` | `ACT-COM-003`; `ACT-END-006`; `ACT-END-008`; `ACT-OPS-013` |
| `BS-011-AP-002` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-QLT-016`; `ACT-LOG-001`; `ACT-LOG-002`; `ACT-COM-001`; `ACT-SRC-008` | `ACT-COM-003`; `ACT-END-006`; `ACT-END-008` |
| `BS-011-AP-003` | `ACT-RND-001`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-QLT-003`; `ACT-PRD-030` | `ACT-QLT-009`; `ACT-QLT-010`; `ACT-QLT-011`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-LOG-001` | `ACT-LOG-002`; `ACT-QLT-017`; `ACT-END-010`; `ACT-OPS-013` |
| `BS-011-AP-004` | `ACT-RND-001`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-QLT-003`; `ACT-PRD-030`; `ACT-RND-021` | `ACT-QLT-009`; `ACT-QLT-010`; `ACT-QLT-011`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-LOG-001`; `ACT-QLT-004`; `ACT-DIG-008` | `ACT-LOG-002`; `ACT-QLT-017`; `ACT-END-010`; `ACT-OPS-013`; `ACT-QLT-006`; `ACT-QLT-007` |
| `BS-011-AP-005` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-PRD-022`; `ACT-PRD-023`; `ACT-PRD-024`; `ACT-PRD-025`; `ACT-SRC-008`; `ACT-COM-001`; `ACT-LOG-001` | `ACT-PRD-033`; `ACT-END-006`; `ACT-END-004`; `ACT-OPS-013` |
| `BS-011-AP-006` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-PRD-022`; `ACT-PRD-023`; `ACT-PRD-024`; `ACT-PRD-025`; `ACT-SRC-008`; `ACT-COM-001` | `ACT-PRD-033`; `ACT-END-006`; `ACT-END-004` |
| `BS-011-AP-007` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030`; `ACT-RND-001`; `ACT-RND-007` | `ACT-QLT-003`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-001`; `ACT-DIG-007`; `ACT-DIG-008`; `ACT-EDU-014` | `ACT-SRC-008`; `ACT-END-006`; `ACT-END-009`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-011-AP-008` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-QLT-003`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-001` | `ACT-SRC-008`; `ACT-END-006`; `ACT-END-009` |
| `BS-011-AP-009` | `ACT-SRC-001`; `ACT-PRD-008`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-QLT-003`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-001`; `ACT-LOG-001` | `ACT-SRC-008`; `ACT-END-006`; `ACT-END-009`; `ACT-OPS-013` |
| `BS-011-AP-010` | `ACT-PRF-024`; `ACT-PRD-017`; `ACT-PRD-018`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-PRD-019`; `ACT-PRD-021`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-COM-001`; `ACT-LOG-001` | `ACT-OPS-001`; `ACT-OPS-014`; `ACT-END-004`; `ACT-END-006`; `ACT-SRC-008`; `ACT-OPS-013` |
| `BS-011-AP-011` | `ACT-PRF-024`; `ACT-PRD-017`; `ACT-PRD-018`; `ACT-PRD-016`; `ACT-QLT-001` | `ACT-PRD-019`; `ACT-PRD-021`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-COM-001` | `ACT-OPS-001`; `ACT-OPS-014`; `ACT-END-004`; `ACT-END-006` |
| `BS-011-AP-012` | `ACT-PRF-024`; `ACT-PRD-017`; `ACT-PRD-018`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-SRC-014`; `ACT-OPS-001` | `ACT-PRD-019`; `ACT-PRD-021`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-COM-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-END-004`; `ACT-END-006`; `ACT-COM-012`; `ACT-OPS-016`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-011-AP-013` | `ACT-PRF-024`; `ACT-PRD-017`; `ACT-PRD-018`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-SRC-014`; `ACT-OPS-001` | `ACT-PRD-019`; `ACT-PRD-021`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-COM-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-END-004`; `ACT-END-006`; `ACT-COM-012`; `ACT-OPS-016` |
| `BS-011-AP-014` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-RND-021`; `ACT-SRC-015`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-COM-025`; `ACT-LOG-001` | `ACT-OPS-014`; `ACT-OPS-019`; `ACT-END-006`; `ACT-OPS-013` |
| `BS-011-AP-015` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-QLT-001`; `ACT-PRD-030`; `ACT-SRC-014` | `ACT-RND-021`; `ACT-SRC-015`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-COM-025`; `ACT-LOG-001`; `ACT-OPS-012`; `ACT-OPS-014` | `ACT-OPS-019`; `ACT-END-006`; `ACT-OPS-013`; `ACT-COM-012`; `ACT-OPS-016` |
| `BS-011-AP-016` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-QLT-001` | `ACT-RND-021`; `ACT-SRC-015`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-COM-025` | `ACT-OPS-014`; `ACT-OPS-019`; `ACT-END-006` |
| `BS-011-AP-017` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-COM-001`; `ACT-SRC-008`; `ACT-LOG-001` | `ACT-OPS-014`; `ACT-OPS-019`; `ACT-END-018`; `ACT-OPS-013` |
| `BS-011-AP-018` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-SRC-014`; `ACT-OPS-001` | `ACT-QLT-001`; `ACT-PRD-030`; `ACT-COM-001`; `ACT-SRC-008`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-OPS-019`; `ACT-END-018`; `ACT-COM-012`; `ACT-OPS-016` |
| `BS-011-AP-019` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021` | `ACT-QLT-001`; `ACT-PRD-030`; `ACT-COM-001`; `ACT-SRC-008` | `ACT-OPS-014`; `ACT-OPS-019`; `ACT-END-018` |
| `BS-011-AP-020` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-QLT-001`; `ACT-PRD-030` | `ACT-COM-001`; `ACT-SRC-008`; `ACT-LOG-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-OPS-019`; `ACT-END-018`; `ACT-OPS-013`; `ACT-COM-012`; `ACT-OPS-016` |
| `BS-011-AP-021` | `ACT-SRC-001`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030`; `ACT-COM-001` | `ACT-PRD-026`; `ACT-PRD-033`; `ACT-LOG-001`; `ACT-COM-004` | `ACT-END-006`; `ACT-END-004`; `ACT-END-015`; `ACT-SRC-008`; `ACT-OPS-013` |
| `BS-011-AP-022` | `ACT-SRC-001`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030`; `ACT-COM-001` | `ACT-PRD-026`; `ACT-PRD-033`; `ACT-LOG-001`; `ACT-COM-004` | `ACT-END-006`; `ACT-END-004`; `ACT-END-015` |
| `BS-011-AP-023` | `ACT-SRC-001`; `ACT-PRD-016`; `ACT-QLT-001`; `ACT-PRD-030`; `ACT-COM-001`; `ACT-EDU-002` | `ACT-PRD-026`; `ACT-PRD-033`; `ACT-LOG-001`; `ACT-COM-004`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-END-006`; `ACT-END-004`; `ACT-END-015`; `ACT-SRC-008`; `ACT-OPS-013`; `ACT-RND-017` |
| `BS-011-AP-024` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-PRD-016`; `ACT-QLT-001` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-LOG-001`; `ACT-COM-001` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-SRC-008` |
| `BS-011-AP-025` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-RND-001`; `ACT-RND-007` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-011-AP-026` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015` |
| `BS-011-AP-027` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-RND-021`; `ACT-QLT-001` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-QLT-003`; `ACT-QLT-004` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-QLT-006`; `ACT-QLT-007` |
| `BS-011-AP-028` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-OPS-012`; `ACT-OPS-014` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-SRC-015`; `ACT-DIG-007` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-OPS-019`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-011-AP-029` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-LOG-001`; `ACT-LOG-003` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-LOG-027` |
| `BS-011-AP-030` | `ACT-OPS-008`; `ACT-OPS-025`; `ACT-QLT-002`; `ACT-QLT-014`; `ACT-DIG-008`; `ACT-END-001`; `ACT-END-002` | `ACT-OPS-013`; `ACT-SRC-002`; `ACT-OPS-031`; `ACT-OPS-032`; `ACT-DIG-009`; `ACT-END-008`; `ACT-END-012` | `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-015`; `ACT-END-004`; `ACT-END-005` |

## 3. Domain assignments

### 3.1 Food, beverage and agricultural manufacturing

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-FNB-001` | Food Manufacturing | `BS-011-AP-001` |
| `MFG-FNB-002` | Beverage Manufacturing | `BS-011-AP-001` |
| `MFG-FNB-003` | Dairy Processing | `BS-011-AP-002` |
| `MFG-FNB-004` | Meat and Poultry Processing | `BS-011-AP-002` |
| `MFG-FNB-005` | Seafood Processing | `BS-011-AP-002` |
| `MFG-FNB-006` | Grain Milling | `BS-011-AP-002` |
| `MFG-FNB-007` | Bakery Manufacturing | `BS-011-AP-001` |
| `MFG-FNB-008` | Confectionery Manufacturing | `BS-011-AP-001` |
| `MFG-FNB-009` | Edible Oil Processing | `BS-011-AP-002` |
| `MFG-FNB-010` | Sugar Processing | `BS-011-AP-002` |
| `MFG-FNB-011` | Tea and Coffee Processing | `BS-011-AP-002` |
| `MFG-FNB-012` | Animal Feed Manufacturing | `BS-011-AP-001` |

### 3.2 Life sciences and healthcare manufacturing

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-LIF-001` | Pharmaceutical Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-002` | Biopharmaceutical Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-003` | Vaccine Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-004` | Medical Device Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-005` | Diagnostic Product Manufacturing | `BS-011-AP-004` |
| `MFG-LIF-006` | Surgical Instrument Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-007` | Medical Consumables Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-008` | Personal Protective Equipment Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-009` | Clinical Nutrition Manufacturing | `BS-011-AP-003` |
| `MFG-LIF-010` | Cosmetics and Personal Care Manufacturing | `BS-011-AP-003` |

### 3.3 Textiles, apparel and leather

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-TEX-001` | Fibre and Yarn Manufacturing | `BS-011-AP-005` |
| `MFG-TEX-002` | Textile Weaving | `BS-011-AP-006` |
| `MFG-TEX-003` | Textile Knitting | `BS-011-AP-006` |
| `MFG-TEX-004` | Dyeing and Finishing | `BS-011-AP-006` |
| `MFG-TEX-005` | Garment Manufacturing | `BS-011-AP-005` |
| `MFG-TEX-006` | Home Textile Manufacturing | `BS-011-AP-005` |
| `MFG-TEX-007` | Technical Textiles | `BS-011-AP-006` |
| `MFG-TEX-008` | Footwear Manufacturing | `BS-011-AP-005` |
| `MFG-TEX-009` | Leather Processing | `BS-011-AP-006` |
| `MFG-TEX-010` | Leather Goods Manufacturing | `BS-011-AP-005` |
| `MFG-TEX-011` | Carpet Manufacturing | `BS-011-AP-005` |

### 3.4 Chemicals, plastics and materials

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-CHE-001` | Industrial Chemicals | `BS-011-AP-007` |
| `MFG-CHE-002` | Specialty Chemicals | `BS-011-AP-008` |
| `MFG-CHE-003` | Fertilizer Manufacturing | `BS-011-AP-009` |
| `MFG-CHE-004` | Paints and Coatings | `BS-011-AP-008` |
| `MFG-CHE-005` | Detergents and Cleaning Products | `BS-011-AP-008` |
| `MFG-CHE-006` | Plastics Manufacturing | `BS-011-AP-009` |
| `MFG-CHE-007` | Plastic Packaging | `BS-011-AP-008` |
| `MFG-CHE-008` | Rubber Products | `BS-011-AP-008` |
| `MFG-CHE-009` | Glass Manufacturing | `BS-011-AP-009` |
| `MFG-CHE-010` | Ceramics Manufacturing | `BS-011-AP-009` |
| `MFG-CHE-011` | Cement Manufacturing | `BS-011-AP-009` |
| `MFG-CHE-012` | Concrete Products | `BS-011-AP-008` |
| `MFG-CHE-013` | Composite Materials | `BS-011-AP-008` |

### 3.5 Metals, machinery and engineered products

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-MET-001` | Steel Manufacturing | `BS-011-AP-010` |
| `MFG-MET-002` | Non-Ferrous Metals | `BS-011-AP-011` |
| `MFG-MET-003` | Metal Fabrication | `BS-011-AP-011` |
| `MFG-MET-004` | Casting and Foundry | `BS-011-AP-011` |
| `MFG-MET-005` | Machining and Precision Engineering | `BS-011-AP-011` |
| `MFG-MET-006` | Industrial Machinery | `BS-011-AP-012` |
| `MFG-MET-007` | Agricultural Machinery | `BS-011-AP-013` |
| `MFG-MET-008` | Construction Equipment | `BS-011-AP-013` |
| `MFG-MET-009` | Pumps and Compressors | `BS-011-AP-011` |
| `MFG-MET-010` | Valves and Piping Equipment | `BS-011-AP-013` |
| `MFG-MET-011` | Electrical Equipment | `BS-011-AP-013` |
| `MFG-MET-012` | Transformers and Switchgear | `BS-011-AP-011` |
| `MFG-MET-013` | Industrial Automation Equipment | `BS-011-AP-012` |
| `MFG-MET-014` | Tools and Hardware | `BS-011-AP-011` |
| `MFG-MET-015` | Fasteners and Components | `BS-011-AP-011` |

### 3.6 Automotive, transport and mobility manufacturing

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-AUT-001` | Automobile Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-002` | Commercial Vehicle Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-003` | Motorcycle Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-004` | Automotive Parts Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-005` | Tyre Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-006` | Battery Manufacturing | `BS-011-AP-014` |
| `MFG-AUT-007` | Rail Equipment Manufacturing | `BS-011-AP-015` |
| `MFG-AUT-008` | Marine Equipment Manufacturing | `BS-011-AP-015` |
| `MFG-AUT-009` | Aerospace Components | `BS-011-AP-016` |
| `MFG-AUT-010` | Electric Vehicle Components | `BS-011-AP-016` |
| `MFG-AUT-011` | Bicycle Manufacturing | `BS-011-AP-014` |

### 3.7 Electronics and technology hardware

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-ELE-001` | Consumer Electronics Manufacturing | `BS-011-AP-017` |
| `MFG-ELE-002` | Computer Hardware Manufacturing | `BS-011-AP-017` |
| `MFG-ELE-003` | Telecommunications Equipment | `BS-011-AP-018` |
| `MFG-ELE-004` | Semiconductor and Electronic Components | `BS-011-AP-019` |
| `MFG-ELE-005` | Printed Circuit Boards | `BS-011-AP-019` |
| `MFG-ELE-006` | Sensors and Instrumentation | `BS-011-AP-018` |
| `MFG-ELE-007` | Control Systems | `BS-011-AP-019` |
| `MFG-ELE-008` | Solar Equipment Manufacturing | `BS-011-AP-020` |
| `MFG-ELE-009` | Lighting Products | `BS-011-AP-019` |
| `MFG-ELE-010` | Home Appliances | `BS-011-AP-019` |

### 3.8 Packaging, paper, furniture and consumer products

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-PKG-001` | Paper and Pulp Manufacturing | `BS-011-AP-021` |
| `MFG-PKG-002` | Paper Packaging | `BS-011-AP-022` |
| `MFG-PKG-003` | Corrugated Packaging | `BS-011-AP-022` |
| `MFG-PKG-004` | Flexible Packaging | `BS-011-AP-022` |
| `MFG-PKG-005` | Labels and Printing | `BS-011-AP-022` |
| `MFG-PKG-006` | Wood Products | `BS-011-AP-022` |
| `MFG-PKG-007` | Furniture Manufacturing | `BS-011-AP-021` |
| `MFG-PKG-008` | Mattress Manufacturing | `BS-011-AP-021` |
| `MFG-PKG-009` | Household Products | `BS-011-AP-022` |
| `MFG-PKG-010` | Toys and Recreational Products | `BS-011-AP-022` |
| `MFG-PKG-011` | Jewellery Manufacturing | `BS-011-AP-021` |
| `MFG-PKG-012` | Office and School Supplies Manufacturing | `BS-011-AP-023` |

### 3.9 Industrial operations and support

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `MFG-OPS-001` | Contract Manufacturing | `BS-011-AP-024` |
| `MFG-OPS-002` | Original Equipment Manufacturing | `BS-011-AP-024` |
| `MFG-OPS-003` | Private-Label Manufacturing | `BS-011-AP-024` |
| `MFG-OPS-004` | Industrial Design | `BS-011-AP-025` |
| `MFG-OPS-005` | Product Engineering | `BS-011-AP-026` |
| `MFG-OPS-006` | Tooling and Mould Making | `BS-011-AP-026` |
| `MFG-OPS-007` | Quality Testing | `BS-011-AP-027` |
| `MFG-OPS-008` | Calibration Services | `BS-011-AP-026` |
| `MFG-OPS-009` | Industrial Maintenance | `BS-011-AP-028` |
| `MFG-OPS-010` | Plant Engineering | `BS-011-AP-024` |
| `MFG-OPS-011` | Production Planning Systems | `BS-011-AP-026` |
| `MFG-OPS-012` | Manufacturing Execution Systems | `BS-011-AP-024` |
| `MFG-OPS-013` | Industrial IoT | `BS-011-AP-025` |
| `MFG-OPS-014` | Warehouse and Material Handling | `BS-011-AP-029` |
| `MFG-OPS-015` | Industrial Safety | `BS-011-AP-025` |
| `MFG-OPS-016` | Waste and Scrap Recovery | `BS-011-AP-030` |
| `MFG-OPS-017` | Industrial Energy Management | `BS-011-AP-025` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
