# Harvester Logistics Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **101** canonical domains in `BS-012 Logistics` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-012-AP-001` | `ACT-LOG-012`; `ACT-LOG-013`; `ACT-LOG-014`; `ACT-LOG-025`; `ACT-LOG-024` | `ACT-LOG-010`; `ACT-LOG-011`; `ACT-LOG-028`; `ACT-LOG-001`; `ACT-OPS-018` | `ACT-COM-007`; `ACT-QLT-013`; `ACT-COM-019` |
| `BS-012-AP-002` | `ACT-LOG-016`; `ACT-LOG-018`; `ACT-LOG-019`; `ACT-LOG-020`; `ACT-LOG-024` | `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-033`; `ACT-OPS-018`; `ACT-LOG-008` | `ACT-LOG-001`; `ACT-LOG-026`; `ACT-DIG-016`; `ACT-LOG-017` |
| `BS-012-AP-003` | `ACT-LOG-016`; `ACT-LOG-018`; `ACT-LOG-019`; `ACT-LOG-020`; `ACT-LOG-024` | `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-033`; `ACT-OPS-018` | `ACT-LOG-001`; `ACT-LOG-026`; `ACT-DIG-016` |
| `BS-012-AP-004` | `ACT-LOG-016`; `ACT-LOG-018`; `ACT-LOG-019`; `ACT-LOG-020`; `ACT-LOG-024`; `ACT-COM-009`; `ACT-COM-008` | `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-033`; `ACT-OPS-018`; `ACT-DIG-016`; `ACT-LOG-006` | `ACT-LOG-001`; `ACT-LOG-026`; `ACT-DIG-007` |
| `BS-012-AP-005` | `ACT-LOG-001`; `ACT-LOG-003`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-LOG-008`; `ACT-LOG-011`; `ACT-LOG-026`; `ACT-LOG-023`; `ACT-DIG-008` | `ACT-LOG-002`; `ACT-DIG-009`; `ACT-LOG-027` |
| `BS-012-AP-006` | `ACT-LOG-001`; `ACT-LOG-003`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024`; `ACT-COM-001`; `ACT-COM-002` | `ACT-LOG-008`; `ACT-LOG-011`; `ACT-LOG-026`; `ACT-LOG-023`; `ACT-DIG-008`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-LOG-002`; `ACT-DIG-009`; `ACT-LOG-027`; `ACT-COM-017` |
| `BS-012-AP-007` | `ACT-LOG-001`; `ACT-LOG-003`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024`; `ACT-COM-009`; `ACT-COM-008` | `ACT-LOG-008`; `ACT-LOG-011`; `ACT-LOG-026`; `ACT-LOG-023`; `ACT-DIG-008`; `ACT-DIG-016`; `ACT-LOG-006`; `ACT-OPS-018` | `ACT-LOG-002`; `ACT-DIG-009`; `ACT-LOG-027`; `ACT-DIG-007`; `ACT-LOG-020` |
| `BS-012-AP-008` | `ACT-LOG-001`; `ACT-LOG-003`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024`; `ACT-RND-001`; `ACT-RND-007` | `ACT-LOG-008`; `ACT-LOG-011`; `ACT-LOG-026`; `ACT-LOG-023`; `ACT-DIG-008`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-LOG-002`; `ACT-DIG-009`; `ACT-LOG-027`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-012-AP-009` | `ACT-LOG-035`; `ACT-LOG-013`; `ACT-LOG-001`; `ACT-LOG-024`; `ACT-QLT-010` | `ACT-LOG-002`; `ACT-LOG-034`; `ACT-QLT-002`; `ACT-QLT-013` | `ACT-LOG-025`; `ACT-LOG-027`; `ACT-OPS-034` |
| `BS-012-AP-010` | `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-013`; `ACT-OPS-012` | `ACT-LOG-024`; `ACT-OPS-024`; `ACT-OPS-030`; `ACT-QLT-014` | `ACT-COM-012`; `ACT-OPS-014`; `ACT-DIG-017`; `ACT-HSP-014` |
| `BS-012-AP-011` | `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-013`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-015` | `ACT-LOG-024`; `ACT-OPS-024`; `ACT-OPS-030`; `ACT-QLT-014`; `ACT-OPS-017`; `ACT-SRC-015` | `ACT-COM-012`; `ACT-DIG-017`; `ACT-OPS-019`; `ACT-OPS-013`; `ACT-HSP-014` |
| `BS-012-AP-012` | `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-013`; `ACT-OPS-012` | `ACT-LOG-024`; `ACT-OPS-024`; `ACT-OPS-030`; `ACT-QLT-014` | `ACT-COM-012`; `ACT-OPS-014`; `ACT-DIG-017` |
| `BS-012-AP-013` | `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-LOG-013`; `ACT-OPS-012`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-LOG-024`; `ACT-OPS-024`; `ACT-OPS-030`; `ACT-QLT-014`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-COM-012`; `ACT-OPS-014`; `ACT-DIG-017`; `ACT-EDU-002`; `ACT-LEG-013`; `ACT-HSP-014` |
| `BS-012-AP-014` | `ACT-LOG-014`; `ACT-LOG-029`; `ACT-LOG-030`; `ACT-LOG-028`; `ACT-LOG-031` | `ACT-LOG-025`; `ACT-LOG-012`; `ACT-LOG-024`; `ACT-LOG-001` | `ACT-LOG-022`; `ACT-QLT-014`; `ACT-QLT-015` |
| `BS-012-AP-015` | `ACT-LOG-014`; `ACT-LOG-029`; `ACT-LOG-030`; `ACT-LOG-028`; `ACT-LOG-031`; `ACT-LOG-012`; `ACT-LOG-013` | `ACT-LOG-025`; `ACT-LOG-024`; `ACT-LOG-001` | `ACT-LOG-022`; `ACT-QLT-014`; `ACT-QLT-015` |
| `BS-012-AP-016` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005` | `ACT-LOG-024`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-013` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-024` |
| `BS-012-AP-017` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-LOG-001`; `ACT-LOG-003` | `ACT-LOG-024`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-013`; `ACT-LOG-005`; `ACT-LOG-007` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-024`; `ACT-LOG-027` |
| `BS-012-AP-018` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-LOG-019`; `ACT-LOG-020` | `ACT-LOG-024`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-013`; `ACT-LOG-008`; `ACT-LOG-023` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-024`; `ACT-LOG-017`; `ACT-LOG-018` |
| `BS-012-AP-019` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-COM-009`; `ACT-COM-008` | `ACT-LOG-024`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-013`; `ACT-DIG-016`; `ACT-LOG-006`; `ACT-OPS-018` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-024`; `ACT-LOG-020`; `ACT-LOG-028`; `ACT-LOG-001` |
| `BS-012-AP-020` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-LOG-012`; `ACT-LOG-013` | `ACT-LOG-024`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-013`; `ACT-LOG-014`; `ACT-LOG-025` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-024`; `ACT-LOG-028`; `ACT-LOG-001` |

## 3. Domain assignments

### 3.1 Freight and forwarding

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-FRT-001` | Freight Forwarding | `BS-012-AP-001` |
| `LOG-FRT-002` | Road Freight | `BS-012-AP-001` |
| `LOG-FRT-003` | Rail Freight | `BS-012-AP-001` |
| `LOG-FRT-004` | Air Freight | `BS-012-AP-001` |
| `LOG-FRT-005` | Ocean Freight | `BS-012-AP-001` |
| `LOG-FRT-006` | Multimodal Transport | `BS-012-AP-001` |
| `LOG-FRT-007` | Project Cargo | `BS-012-AP-001` |
| `LOG-FRT-008` | Bulk Cargo | `BS-012-AP-001` |
| `LOG-FRT-009` | Container Transport | `BS-012-AP-001` |
| `LOG-FRT-010` | Customs Brokerage | `BS-012-AP-001` |
| `LOG-FRT-011` | Import and Export Logistics | `BS-012-AP-001` |
| `LOG-FRT-012` | Cross-Border Logistics | `BS-012-AP-001` |
| `LOG-FRT-013` | Third-Party Logistics | `BS-012-AP-001` |
| `LOG-FRT-014` | Fourth-Party Logistics | `BS-012-AP-001` |

### 3.2 Postal, courier and parcel delivery

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-PAR-001` | Postal Networks | `BS-012-AP-002` |
| `LOG-PAR-002` | Domestic Courier | `BS-012-AP-002` |
| `LOG-PAR-003` | International Courier | `BS-012-AP-002` |
| `LOG-PAR-004` | Express Delivery | `BS-012-AP-003` |
| `LOG-PAR-005` | Parcel Delivery | `BS-012-AP-002` |
| `LOG-PAR-006` | Document Delivery | `BS-012-AP-003` |
| `LOG-PAR-007` | Last-Mile Delivery | `BS-012-AP-002` |
| `LOG-PAR-008` | Same-Day Delivery | `BS-012-AP-003` |
| `LOG-PAR-009` | E-Commerce Delivery | `BS-012-AP-004` |
| `LOG-PAR-010` | Cash-on-Delivery Logistics | `BS-012-AP-003` |
| `LOG-PAR-011` | Reverse Pickup | `BS-012-AP-003` |
| `LOG-PAR-012` | Mailroom Services | `BS-012-AP-003` |
| `LOG-PAR-013` | Branch and Franchise Courier Networks | `BS-012-AP-002` |
| `LOG-PAR-014` | Delivery Aggregation Platforms | `BS-012-AP-003` |

### 3.3 Warehousing and fulfilment

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-WAR-001` | General Warehousing | `BS-012-AP-005` |
| `LOG-WAR-002` | Bonded Warehousing | `BS-012-AP-005` |
| `LOG-WAR-003` | Distribution Centres | `BS-012-AP-006` |
| `LOG-WAR-004` | E-Commerce Fulfilment | `BS-012-AP-007` |
| `LOG-WAR-005` | Retail Fulfilment | `BS-012-AP-005` |
| `LOG-WAR-006` | Industrial Warehousing | `BS-012-AP-008` |
| `LOG-WAR-007` | Pharmaceutical Warehousing | `BS-012-AP-005` |
| `LOG-WAR-008` | Food Warehousing | `BS-012-AP-005` |
| `LOG-WAR-009` | Cold Storage | `BS-012-AP-005` |
| `LOG-WAR-010` | Temperature-Controlled Warehousing | `BS-012-AP-005` |
| `LOG-WAR-011` | Document and Records Storage | `BS-012-AP-005` |
| `LOG-WAR-012` | Self-Storage | `BS-012-AP-005` |
| `LOG-WAR-013` | Inventory Management Services | `BS-012-AP-005` |
| `LOG-WAR-014` | Pick-and-Pack Services | `BS-012-AP-005` |
| `LOG-WAR-015` | Cross-Docking | `BS-012-AP-005` |
| `LOG-WAR-016` | Yard Management | `BS-012-AP-005` |

### 3.4 Specialized supply chains

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-CHN-001` | Cold Chain Logistics | `BS-012-AP-009` |
| `LOG-CHN-002` | Pharmaceutical Logistics | `BS-012-AP-009` |
| `LOG-CHN-003` | Healthcare Logistics | `BS-012-AP-009` |
| `LOG-CHN-004` | Food Logistics | `BS-012-AP-009` |
| `LOG-CHN-005` | Agricultural Logistics | `BS-012-AP-009` |
| `LOG-CHN-006` | Automotive Logistics | `BS-012-AP-009` |
| `LOG-CHN-007` | Construction Logistics | `BS-012-AP-009` |
| `LOG-CHN-008` | Retail Logistics | `BS-012-AP-009` |
| `LOG-CHN-009` | Fashion Logistics | `BS-012-AP-009` |
| `LOG-CHN-010` | Electronics Logistics | `BS-012-AP-009` |
| `LOG-CHN-011` | Chemical and Hazardous-Goods Logistics | `BS-012-AP-009` |
| `LOG-CHN-012` | Humanitarian Logistics | `BS-012-AP-009` |
| `LOG-CHN-013` | Military and Government Logistics | `BS-012-AP-009` |
| `LOG-CHN-014` | Event Logistics | `BS-012-AP-009` |

### 3.5 Fleet and transport operations

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-FLT-001` | Trucking Fleets | `BS-012-AP-010` |
| `LOG-FLT-002` | Commercial Vehicle Fleets | `BS-012-AP-010` |
| `LOG-FLT-003` | Delivery Fleets | `BS-012-AP-010` |
| `LOG-FLT-004` | Passenger Transport Fleets | `BS-012-AP-010` |
| `LOG-FLT-005` | Fleet Leasing | `BS-012-AP-010` |
| `LOG-FLT-006` | Vehicle Rental Fleets | `BS-012-AP-010` |
| `LOG-FLT-007` | Fleet Maintenance | `BS-012-AP-011` |
| `LOG-FLT-008` | Fuel Management | `BS-012-AP-012` |
| `LOG-FLT-009` | Driver Management | `BS-012-AP-012` |
| `LOG-FLT-010` | Route Planning | `BS-012-AP-012` |
| `LOG-FLT-011` | Dispatch Operations | `BS-012-AP-012` |
| `LOG-FLT-012` | Telematics and Fleet Tracking | `BS-012-AP-010` |
| `LOG-FLT-013` | Transport Safety and Compliance | `BS-012-AP-013` |

### 3.6 Ports, shipping and aviation logistics

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-MAR-001` | Shipping Lines | `BS-012-AP-014` |
| `LOG-MAR-002` | Shipping Agencies | `BS-012-AP-014` |
| `LOG-MAR-003` | Port Operators | `BS-012-AP-014` |
| `LOG-MAR-004` | Container Terminals | `BS-012-AP-014` |
| `LOG-MAR-005` | Inland Container Depots | `BS-012-AP-014` |
| `LOG-MAR-006` | Marine Logistics | `BS-012-AP-014` |
| `LOG-MAR-007` | Air Cargo Terminals | `BS-012-AP-015` |
| `LOG-MAR-008` | Airport Ground Handling | `BS-012-AP-014` |
| `LOG-MAR-009` | Cargo Airlines | `BS-012-AP-015` |
| `LOG-MAR-010` | Freight Airports | `BS-012-AP-015` |
| `LOG-MAR-011` | Ship Chandling | `BS-012-AP-014` |
| `LOG-MAR-012` | Marine Warehousing | `BS-012-AP-014` |
| `LOG-MAR-013` | Customs and Border Terminals | `BS-012-AP-014` |

### 3.7 Logistics technology and support

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `LOG-DIG-001` | Transport Management Systems | `BS-012-AP-016` |
| `LOG-DIG-002` | Warehouse Management Systems | `BS-012-AP-017` |
| `LOG-DIG-003` | Courier Management Systems | `BS-012-AP-018` |
| `LOG-DIG-004` | Shipment Tracking Platforms | `BS-012-AP-016` |
| `LOG-DIG-005` | Route Optimization Systems | `BS-012-AP-016` |
| `LOG-DIG-006` | Fleet Management Systems | `BS-012-AP-016` |
| `LOG-DIG-007` | Freight Marketplaces | `BS-012-AP-019` |
| `LOG-DIG-008` | Digital Freight Platforms | `BS-012-AP-020` |
| `LOG-DIG-009` | Delivery Management Systems | `BS-012-AP-016` |
| `LOG-DIG-010` | Proof-of-Delivery Systems | `BS-012-AP-016` |
| `LOG-DIG-011` | Logistics Control Towers | `BS-012-AP-016` |
| `LOG-DIG-012` | Supply-Chain Visibility | `BS-012-AP-016` |
| `LOG-DIG-013` | Customs Management Systems | `BS-012-AP-016` |
| `LOG-DIG-014` | Logistics Analytics | `BS-012-AP-016` |
| `LOG-DIG-015` | Barcode and RFID Systems | `BS-012-AP-016` |
| `LOG-DIG-016` | Logistics Payment and Settlement | `BS-012-AP-016` |
| `LOG-DIG-017` | Packaging and Pallet Services | `BS-012-AP-016` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
