# Harvester Construction Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-005 Construction`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Construction
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

This registry contains **93 canonical domains** in **6 families**.

| Family | Name | Count |
| --- | --- | --- |
| `CON-BLD` | Building construction | 12 |
| `CON-INF` | Civil and public infrastructure | 12 |
| `CON-DES` | Design, engineering and surveying | 15 |
| `CON-TRD` | Specialist trades and installation | 17 |
| `CON-MAT` | Construction materials and components | 20 |
| `CON-OPS` | Construction operations and support | 17 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Building construction

| Code | Domain |
| --- | --- |
| `CON-BLD-001` | Residential Construction |
| `CON-BLD-002` | Commercial Construction |
| `CON-BLD-003` | Industrial Construction |
| `CON-BLD-004` | Institutional Construction |
| `CON-BLD-005` | Healthcare Facility Construction |
| `CON-BLD-006` | Education Facility Construction |
| `CON-BLD-007` | Hospitality Construction |
| `CON-BLD-008` | Retail Construction |
| `CON-BLD-009` | Warehouse Construction |
| `CON-BLD-010` | High-Rise Construction |
| `CON-BLD-011` | Low-Rise Construction |
| `CON-BLD-012` | Modular and Prefabricated Construction |

### 4.2 Civil and public infrastructure

| Code | Domain |
| --- | --- |
| `CON-INF-001` | Road Construction |
| `CON-INF-002` | Bridge Construction |
| `CON-INF-003` | Rail Infrastructure |
| `CON-INF-004` | Airport Infrastructure |
| `CON-INF-005` | Port and Marine Construction |
| `CON-INF-006` | Water Infrastructure |
| `CON-INF-007` | Sewerage Infrastructure |
| `CON-INF-008` | Drainage and Flood Control |
| `CON-INF-009` | Power Infrastructure |
| `CON-INF-010` | Telecommunications Infrastructure |
| `CON-INF-011` | Urban Infrastructure |
| `CON-INF-012` | Public-Space and Landscape Construction |

### 4.3 Design, engineering and surveying

| Code | Domain |
| --- | --- |
| `CON-DES-001` | Architecture |
| `CON-DES-002` | Urban Planning |
| `CON-DES-003` | Interior Architecture |
| `CON-DES-004` | Civil Engineering |
| `CON-DES-005` | Structural Engineering |
| `CON-DES-006` | Mechanical Engineering |
| `CON-DES-007` | Electrical Engineering |
| `CON-DES-008` | Plumbing Engineering |
| `CON-DES-009` | MEP Engineering |
| `CON-DES-010` | Geotechnical Engineering |
| `CON-DES-011` | Environmental Engineering |
| `CON-DES-012` | Quantity Surveying |
| `CON-DES-013` | Land Surveying |
| `CON-DES-014` | Building Information Modelling |
| `CON-DES-015` | Construction Design Management |

### 4.4 Specialist trades and installation

| Code | Domain |
| --- | --- |
| `CON-TRD-001` | Electrical Contracting |
| `CON-TRD-002` | Plumbing Contracting |
| `CON-TRD-003` | HVAC Installation |
| `CON-TRD-004` | Fire-Safety Systems |
| `CON-TRD-005` | Elevator and Escalator Installation |
| `CON-TRD-006` | Solar Installation |
| `CON-TRD-007` | Security-System Installation |
| `CON-TRD-008` | Low-Voltage and Networking Installation |
| `CON-TRD-009` | Glass and Aluminium Works |
| `CON-TRD-010` | Carpentry and Joinery |
| `CON-TRD-011` | Masonry and Concrete Works |
| `CON-TRD-012` | Steel Erection |
| `CON-TRD-013` | Roofing |
| `CON-TRD-014` | Waterproofing |
| `CON-TRD-015` | Painting and Finishing |
| `CON-TRD-016` | Flooring and Tiling |
| `CON-TRD-017` | Landscaping and Irrigation |

### 4.5 Construction materials and components

| Code | Domain |
| --- | --- |
| `CON-MAT-001` | Cement |
| `CON-MAT-002` | Concrete and Ready-Mix |
| `CON-MAT-003` | Bricks and Blocks |
| `CON-MAT-004` | Steel and Reinforcement |
| `CON-MAT-005` | Structural Steel |
| `CON-MAT-006` | Aggregates and Sand |
| `CON-MAT-007` | Glass |
| `CON-MAT-008` | Aluminium Systems |
| `CON-MAT-009` | Timber and Wood Products |
| `CON-MAT-010` | Doors and Windows |
| `CON-MAT-011` | Roofing Materials |
| `CON-MAT-012` | Insulation Materials |
| `CON-MAT-013` | Waterproofing Materials |
| `CON-MAT-014` | Tiles and Ceramics |
| `CON-MAT-015` | Paints and Coatings |
| `CON-MAT-016` | Pipes and Fittings |
| `CON-MAT-017` | Electrical Materials |
| `CON-MAT-018` | HVAC Equipment |
| `CON-MAT-019` | Sanitary Ware |
| `CON-MAT-020` | Prefabricated Components |

### 4.6 Construction operations and support

| Code | Domain |
| --- | --- |
| `CON-OPS-001` | General Contracting |
| `CON-OPS-002` | Subcontracting |
| `CON-OPS-003` | Construction Project Management |
| `CON-OPS-004` | Construction Cost Management |
| `CON-OPS-005` | Procurement and Material Management |
| `CON-OPS-006` | Construction Equipment Rental |
| `CON-OPS-007` | Heavy Equipment Operations |
| `CON-OPS-008` | Site Logistics |
| `CON-OPS-009` | Health and Safety Services |
| `CON-OPS-010` | Quality Inspection |
| `CON-OPS-011` | Material Testing |
| `CON-OPS-012` | Construction Waste Management |
| `CON-OPS-013` | Demolition |
| `CON-OPS-014` | Renovation and Refurbishment |
| `CON-OPS-015` | Fit-Out Contracting |
| `CON-OPS-016` | Building Maintenance |
| `CON-OPS-017` | Construction Software and Field Systems |

## 5. First-release presentation shortlist

Residential Construction, Commercial Construction, Industrial Construction, Road Construction, Bridge Construction, Water Infrastructure, Power Infrastructure, Architecture, Civil Engineering, Structural Engineering, MEP Engineering, Quantity Surveying, Building Information Modelling, General Contracting, Construction Project Management, Electrical Contracting, Plumbing Contracting, HVAC Installation, Fire-Safety Systems, Solar Installation, Security-System Installation, Interior Fit-Out, Renovation and Refurbishment, Cement, Concrete and Ready-Mix, Steel and Reinforcement, Bricks and Blocks, Glass and Aluminium, Doors and Windows, Tiles and Ceramics, Paints and Coatings, Pipes and Fittings, Construction Equipment Rental, Site Logistics, Quality Inspection, Construction Software and Field Systems.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Construction contractors:** Tendering, Estimating, Building, Managing projects, Procuring, Subcontracting
- **Construction materials:** Manufacturing, Importing, Distributing, Warehousing, Selling, Installing
- **Architecture and engineering:** Designing, Surveying, Advising, Reviewing, Supervising
- **Specialist trades:** Installing, Testing, Commissioning, Maintaining, Repairing

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Construction materials | Manufacturing and Industry; Retail | Manufacturing; distributing; selling |
| Building maintenance | Real Estate; Hospitality | Inspecting; maintaining; repairing |
| Power infrastructure | Energy; Government | Constructing; installing; commissioning |
| Construction software | Technology | Developing; implementing; integrating |

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

- The shortlist and all 93 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
