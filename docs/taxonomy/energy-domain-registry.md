# Harvester Energy Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-013 Energy`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Energy
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

This registry contains **94 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `ENE-GEN` | Power generation | 12 |
| `ENE-REN` | Renewable-energy products and services | 14 |
| `ENE-GRD` | Electricity networks and utility operations | 13 |
| `ENE-FUE` | Fuel, petroleum and gas | 14 |
| `ENE-WAT` | Water and essential utilities | 12 |
| `ENE-EFF` | Energy services and efficiency | 13 |
| `ENE-DIG` | Energy technology and operations systems | 16 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Power generation

| Code | Domain |
| --- | --- |
| `ENE-GEN-001` | Thermal Power Generation |
| `ENE-GEN-002` | Hydroelectric Power |
| `ENE-GEN-003` | Solar Power Generation |
| `ENE-GEN-004` | Wind Power Generation |
| `ENE-GEN-005` | Biomass and Biogas Power |
| `ENE-GEN-006` | Waste-to-Energy |
| `ENE-GEN-007` | Cogeneration and Combined Heat and Power |
| `ENE-GEN-008` | Captive Power Plants |
| `ENE-GEN-009` | Distributed Generation |
| `ENE-GEN-010` | Microgrids |
| `ENE-GEN-011` | Backup and Emergency Power |
| `ENE-GEN-012` | Independent Power Producers |

### 4.2 Renewable-energy products and services

| Code | Domain |
| --- | --- |
| `ENE-REN-001` | Solar Panels |
| `ENE-REN-002` | Solar Inverters |
| `ENE-REN-003` | Solar Batteries |
| `ENE-REN-004` | Solar Mounting Systems |
| `ENE-REN-005` | Solar Water Heating |
| `ENE-REN-006` | Wind Turbines |
| `ENE-REN-007` | Small Hydro Systems |
| `ENE-REN-008` | Biogas Systems |
| `ENE-REN-009` | Renewable-Energy Engineering |
| `ENE-REN-010` | Solar EPC Services |
| `ENE-REN-011` | Renewable-Energy Operations and Maintenance |
| `ENE-REN-012` | Energy Storage Systems |
| `ENE-REN-013` | Electric Vehicle Charging |
| `ENE-REN-014` | Renewable-Energy Financing |

### 4.3 Electricity networks and utility operations

| Code | Domain |
| --- | --- |
| `ENE-GRD-001` | Electricity Transmission |
| `ENE-GRD-002` | Electricity Distribution |
| `ENE-GRD-003` | Grid Operations |
| `ENE-GRD-004` | Substations |
| `ENE-GRD-005` | Smart Grid Systems |
| `ENE-GRD-006` | Metering and Smart Meters |
| `ENE-GRD-007` | Utility Billing |
| `ENE-GRD-008` | Outage Management |
| `ENE-GRD-009` | Demand-Side Management |
| `ENE-GRD-010` | Power Quality Management |
| `ENE-GRD-011` | Grid Protection and Control |
| `ENE-GRD-012` | Rural Electrification |
| `ENE-GRD-013` | Utility Customer Services |

### 4.4 Fuel, petroleum and gas

| Code | Domain |
| --- | --- |
| `ENE-FUE-001` | Oil and Gas Exploration |
| `ENE-FUE-002` | Oil and Gas Production |
| `ENE-FUE-003` | Petroleum Refining |
| `ENE-FUE-004` | Fuel Distribution |
| `ENE-FUE-005` | Fuel Retail Stations |
| `ENE-FUE-006` | LPG Distribution |
| `ENE-FUE-007` | Natural Gas Transmission |
| `ENE-FUE-008` | Natural Gas Distribution |
| `ENE-FUE-009` | Industrial Gas Supply |
| `ENE-FUE-010` | Lubricants |
| `ENE-FUE-011` | Fuel Storage Terminals |
| `ENE-FUE-012` | Pipeline Operations |
| `ENE-FUE-013` | Petroleum Logistics |
| `ENE-FUE-014` | Gas Metering |

### 4.5 Water and essential utilities

| Code | Domain |
| --- | --- |
| `ENE-WAT-001` | Water Supply |
| `ENE-WAT-002` | Water Treatment |
| `ENE-WAT-003` | Wastewater Treatment |
| `ENE-WAT-004` | Sewerage Operations |
| `ENE-WAT-005` | Desalination |
| `ENE-WAT-006` | Water Distribution Networks |
| `ENE-WAT-007` | Water Metering |
| `ENE-WAT-008` | Irrigation Utilities |
| `ENE-WAT-009` | District Cooling |
| `ENE-WAT-010` | District Heating |
| `ENE-WAT-011` | Utility Asset Management |
| `ENE-WAT-012` | Utility Field Services |

### 4.6 Energy services and efficiency

| Code | Domain |
| --- | --- |
| `ENE-EFF-001` | Energy Audits |
| `ENE-EFF-002` | Energy Management |
| `ENE-EFF-003` | Building Energy Management |
| `ENE-EFF-004` | Industrial Energy Management |
| `ENE-EFF-005` | Energy Service Companies |
| `ENE-EFF-006` | Power-Factor Correction |
| `ENE-EFF-007` | Energy-Efficient Lighting |
| `ENE-EFF-008` | HVAC Efficiency |
| `ENE-EFF-009` | Carbon and Emissions Management |
| `ENE-EFF-010` | Sustainability Reporting |
| `ENE-EFF-011` | Energy Procurement |
| `ENE-EFF-012` | Demand Response |
| `ENE-EFF-013` | Energy Performance Contracting |

### 4.7 Energy technology and operations systems

| Code | Domain |
| --- | --- |
| `ENE-DIG-001` | Energy Management Systems |
| `ENE-DIG-002` | Supervisory Control and Data Acquisition |
| `ENE-DIG-003` | Meter Data Management |
| `ENE-DIG-004` | Advanced Metering Infrastructure |
| `ENE-DIG-005` | Distributed Energy Resource Management |
| `ENE-DIG-006` | Energy Trading and Settlement |
| `ENE-DIG-007` | Utility Customer Information Systems |
| `ENE-DIG-008` | Asset Performance Management |
| `ENE-DIG-009` | Predictive Maintenance |
| `ENE-DIG-010` | Grid Analytics |
| `ENE-DIG-011` | Renewable Plant Monitoring |
| `ENE-DIG-012` | Battery Management Systems |
| `ENE-DIG-013` | Field-Service Management |
| `ENE-DIG-014` | Geographic Information Systems for Utilities |
| `ENE-DIG-015` | Energy IoT and Telemetry |
| `ENE-DIG-016` | Utility Cybersecurity |

## 5. First-release presentation shortlist

Solar Power, Wind Power, Hydroelectric Power, Thermal Power, Distributed Generation, Solar Panels, Solar Inverters, Solar Batteries, Solar EPC, Energy Storage, Electric Vehicle Charging, Electricity Transmission, Electricity Distribution, Smart Grid, Smart Metering, Utility Billing, Outage Management, Fuel Distribution, LPG Distribution, Natural Gas Distribution, Fuel Retail Stations, Water Supply, Water Treatment, Wastewater Treatment, Water Metering, Energy Audits, Building Energy Management, Industrial Energy Management, Energy Service Companies, Energy Management Systems, SCADA, Meter Data Management, Asset Performance Management, Predictive Maintenance, Renewable Plant Monitoring, Field-Service Management, Energy IoT and Telemetry, Utility Cybersecurity.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Solar products:** Manufacturing, Importing, Distributing, Selling, Installing, Maintaining
- **Power utilities:** Generating, Transmitting, Distributing, Metering, Billing, Maintaining
- **Fuel operations:** Producing, Refining, Storing, Transporting, Distributing, Selling
- **Energy services:** Auditing, Designing, Implementing, Monitoring, Optimizing

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Solar equipment | Manufacturing and Industry; Retail | Manufacturing; selling; installing |
| Building energy management | Construction; Real Estate | Monitoring; controlling; optimizing |
| Petroleum logistics | Logistics | Storing; transporting; distributing |
| Utility systems | Technology; Government | Operating; billing; integrating |

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

- The shortlist and all 94 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
