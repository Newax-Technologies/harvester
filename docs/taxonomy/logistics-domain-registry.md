# Harvester Logistics Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-012 Logistics`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Logistics
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

This registry contains **101 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `LOG-FRT` | Freight and forwarding | 14 |
| `LOG-PAR` | Postal, courier and parcel delivery | 14 |
| `LOG-WAR` | Warehousing and fulfilment | 16 |
| `LOG-CHN` | Specialized supply chains | 14 |
| `LOG-FLT` | Fleet and transport operations | 13 |
| `LOG-MAR` | Ports, shipping and aviation logistics | 13 |
| `LOG-DIG` | Logistics technology and support | 17 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Freight and forwarding

| Code | Domain |
| --- | --- |
| `LOG-FRT-001` | Freight Forwarding |
| `LOG-FRT-002` | Road Freight |
| `LOG-FRT-003` | Rail Freight |
| `LOG-FRT-004` | Air Freight |
| `LOG-FRT-005` | Ocean Freight |
| `LOG-FRT-006` | Multimodal Transport |
| `LOG-FRT-007` | Project Cargo |
| `LOG-FRT-008` | Bulk Cargo |
| `LOG-FRT-009` | Container Transport |
| `LOG-FRT-010` | Customs Brokerage |
| `LOG-FRT-011` | Import and Export Logistics |
| `LOG-FRT-012` | Cross-Border Logistics |
| `LOG-FRT-013` | Third-Party Logistics |
| `LOG-FRT-014` | Fourth-Party Logistics |

### 4.2 Postal, courier and parcel delivery

| Code | Domain |
| --- | --- |
| `LOG-PAR-001` | Postal Networks |
| `LOG-PAR-002` | Domestic Courier |
| `LOG-PAR-003` | International Courier |
| `LOG-PAR-004` | Express Delivery |
| `LOG-PAR-005` | Parcel Delivery |
| `LOG-PAR-006` | Document Delivery |
| `LOG-PAR-007` | Last-Mile Delivery |
| `LOG-PAR-008` | Same-Day Delivery |
| `LOG-PAR-009` | E-Commerce Delivery |
| `LOG-PAR-010` | Cash-on-Delivery Logistics |
| `LOG-PAR-011` | Reverse Pickup |
| `LOG-PAR-012` | Mailroom Services |
| `LOG-PAR-013` | Branch and Franchise Courier Networks |
| `LOG-PAR-014` | Delivery Aggregation Platforms |

### 4.3 Warehousing and fulfilment

| Code | Domain |
| --- | --- |
| `LOG-WAR-001` | General Warehousing |
| `LOG-WAR-002` | Bonded Warehousing |
| `LOG-WAR-003` | Distribution Centres |
| `LOG-WAR-004` | E-Commerce Fulfilment |
| `LOG-WAR-005` | Retail Fulfilment |
| `LOG-WAR-006` | Industrial Warehousing |
| `LOG-WAR-007` | Pharmaceutical Warehousing |
| `LOG-WAR-008` | Food Warehousing |
| `LOG-WAR-009` | Cold Storage |
| `LOG-WAR-010` | Temperature-Controlled Warehousing |
| `LOG-WAR-011` | Document and Records Storage |
| `LOG-WAR-012` | Self-Storage |
| `LOG-WAR-013` | Inventory Management Services |
| `LOG-WAR-014` | Pick-and-Pack Services |
| `LOG-WAR-015` | Cross-Docking |
| `LOG-WAR-016` | Yard Management |

### 4.4 Specialized supply chains

| Code | Domain |
| --- | --- |
| `LOG-CHN-001` | Cold Chain Logistics |
| `LOG-CHN-002` | Pharmaceutical Logistics |
| `LOG-CHN-003` | Healthcare Logistics |
| `LOG-CHN-004` | Food Logistics |
| `LOG-CHN-005` | Agricultural Logistics |
| `LOG-CHN-006` | Automotive Logistics |
| `LOG-CHN-007` | Construction Logistics |
| `LOG-CHN-008` | Retail Logistics |
| `LOG-CHN-009` | Fashion Logistics |
| `LOG-CHN-010` | Electronics Logistics |
| `LOG-CHN-011` | Chemical and Hazardous-Goods Logistics |
| `LOG-CHN-012` | Humanitarian Logistics |
| `LOG-CHN-013` | Military and Government Logistics |
| `LOG-CHN-014` | Event Logistics |

### 4.5 Fleet and transport operations

| Code | Domain |
| --- | --- |
| `LOG-FLT-001` | Trucking Fleets |
| `LOG-FLT-002` | Commercial Vehicle Fleets |
| `LOG-FLT-003` | Delivery Fleets |
| `LOG-FLT-004` | Passenger Transport Fleets |
| `LOG-FLT-005` | Fleet Leasing |
| `LOG-FLT-006` | Vehicle Rental Fleets |
| `LOG-FLT-007` | Fleet Maintenance |
| `LOG-FLT-008` | Fuel Management |
| `LOG-FLT-009` | Driver Management |
| `LOG-FLT-010` | Route Planning |
| `LOG-FLT-011` | Dispatch Operations |
| `LOG-FLT-012` | Telematics and Fleet Tracking |
| `LOG-FLT-013` | Transport Safety and Compliance |

### 4.6 Ports, shipping and aviation logistics

| Code | Domain |
| --- | --- |
| `LOG-MAR-001` | Shipping Lines |
| `LOG-MAR-002` | Shipping Agencies |
| `LOG-MAR-003` | Port Operators |
| `LOG-MAR-004` | Container Terminals |
| `LOG-MAR-005` | Inland Container Depots |
| `LOG-MAR-006` | Marine Logistics |
| `LOG-MAR-007` | Air Cargo Terminals |
| `LOG-MAR-008` | Airport Ground Handling |
| `LOG-MAR-009` | Cargo Airlines |
| `LOG-MAR-010` | Freight Airports |
| `LOG-MAR-011` | Ship Chandling |
| `LOG-MAR-012` | Marine Warehousing |
| `LOG-MAR-013` | Customs and Border Terminals |

### 4.7 Logistics technology and support

| Code | Domain |
| --- | --- |
| `LOG-DIG-001` | Transport Management Systems |
| `LOG-DIG-002` | Warehouse Management Systems |
| `LOG-DIG-003` | Courier Management Systems |
| `LOG-DIG-004` | Shipment Tracking Platforms |
| `LOG-DIG-005` | Route Optimization Systems |
| `LOG-DIG-006` | Fleet Management Systems |
| `LOG-DIG-007` | Freight Marketplaces |
| `LOG-DIG-008` | Digital Freight Platforms |
| `LOG-DIG-009` | Delivery Management Systems |
| `LOG-DIG-010` | Proof-of-Delivery Systems |
| `LOG-DIG-011` | Logistics Control Towers |
| `LOG-DIG-012` | Supply-Chain Visibility |
| `LOG-DIG-013` | Customs Management Systems |
| `LOG-DIG-014` | Logistics Analytics |
| `LOG-DIG-015` | Barcode and RFID Systems |
| `LOG-DIG-016` | Logistics Payment and Settlement |
| `LOG-DIG-017` | Packaging and Pallet Services |

## 5. First-release presentation shortlist

Freight Forwarding, Road Freight, Air Freight, Ocean Freight, Multimodal Transport, Customs Brokerage, Third-Party Logistics, Postal and Courier, Express Delivery, Parcel Delivery, Last-Mile Delivery, E-Commerce Delivery, Cash-on-Delivery Logistics, General Warehousing, Distribution Centres, E-Commerce Fulfilment, Cold Storage, Cold Chain Logistics, Pharmaceutical Logistics, Food Logistics, Retail Logistics, Trucking Fleets, Delivery Fleets, Fleet Maintenance, Route Planning, Dispatch Operations, Shipping Lines, Port Operators, Air Cargo Terminals, Transport Management Systems, Warehouse Management Systems, Courier Management Systems, Shipment Tracking, Route Optimization, Fleet Management Systems, Proof of Delivery, Supply-Chain Visibility, Barcode and RFID Systems.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Courier and postal:** Accepting, Sorting, Routing, Transporting, Delivering, Handling returns
- **Warehousing:** Receiving, Storing, Picking, Packing, Dispatching, Counting
- **Freight forwarding:** Quoting, Booking, Documenting, Consolidating, Customs clearing, Tracking
- **Fleet operations:** Scheduling, Dispatching, Tracking, Fueling, Maintaining, Reporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Pharmaceutical logistics | Healthcare | Warehousing; cold chain; delivering |
| E-commerce fulfilment | Retail; Technology | Picking; packing; shipping |
| Construction logistics | Construction | Transporting; site delivery; material control |
| Fleet telematics | Technology; Energy | Tracking; monitoring; optimizing |

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

- The shortlist and all 101 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
