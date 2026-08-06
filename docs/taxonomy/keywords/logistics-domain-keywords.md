# Harvester Logistics Domain Keyword Registry

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for the **101** canonical domains in the Logistics sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-LOG-FRT-001-V1` | Freight Forwarding | freight forwarding | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-002-V1` | Road Freight | road freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-003-V1` | Rail Freight | rail freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-004-V1` | Air Freight | air freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-005-V1` | Ocean Freight | ocean freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-006-V1` | Multimodal Transport | multimodal transport | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-007-V1` | Project Cargo | project cargo | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-008-V1` | Bulk Cargo | bulk cargo | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-009-V1` | Container Transport | container transport | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-010-V1` | Customs Brokerage | customs brokerage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-011-V1` | Import and Export Logistics | import and export logistics; import & export logistics; import and export freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-012-V1` | Cross-Border Logistics | cross-border logistics; cross-border freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-013-V1` | Third-Party Logistics | third-party logistics; third-party freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FRT-014-V1` | Fourth-Party Logistics | fourth-party logistics; fourth-party freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-001-V1` | Postal Networks | postal networks; postal network | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-002-V1` | Domestic Courier | domestic courier | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-003-V1` | International Courier | international courier | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-004-V1` | Express Delivery | express delivery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-005-V1` | Parcel Delivery | parcel delivery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-006-V1` | Document Delivery | document delivery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-007-V1` | Last-Mile Delivery | last-mile delivery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-008-V1` | Same-Day Delivery | same-day delivery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-009-V1` | E-Commerce Delivery | e-commerce delivery; ecommerce delivery | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-LOG-PAR-010-V1` | Cash-on-Delivery Logistics | cash-on-delivery logistics; cash-on-delivery freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-011-V1` | Reverse Pickup | reverse pickup | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-012-V1` | Mailroom Services | mailroom services; mailroom service; mailroom providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-LOG-PAR-013-V1` | Branch and Franchise Courier Networks | branch and franchise courier networks; branch & franchise courier networks | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-PAR-014-V1` | Delivery Aggregation Platforms | delivery aggregation platforms; delivery aggregation platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-WAR-001-V1` | General Warehousing | general warehousing; general warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-002-V1` | Bonded Warehousing | bonded warehousing; bonded warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-003-V1` | Distribution Centres | distribution centres; distribution centers; distribution centre | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-LOG-WAR-004-V1` | E-Commerce Fulfilment | e-commerce fulfilment; ecommerce fulfilment | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-LOG-WAR-005-V1` | Retail Fulfilment | retail fulfilment | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-LOG-WAR-006-V1` | Industrial Warehousing | industrial warehousing; industrial warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-007-V1` | Pharmaceutical Warehousing | pharmaceutical warehousing; medicine warehousing; pharmaceutical warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-008-V1` | Food Warehousing | food warehousing; food warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-009-V1` | Cold Storage | cold storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-010-V1` | Temperature-Controlled Warehousing | temperature-controlled warehousing; temperature-controlled warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-011-V1` | Document and Records Storage | document and records storage; document & records storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-012-V1` | Self-Storage | self-storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-013-V1` | Inventory Management Services | inventory management services; inventory management service; inventory management providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-LOG-WAR-014-V1` | Pick-and-Pack Services | pick-and-pack services; pick-and-pack service; pick-and-pack providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-LOG-WAR-015-V1` | Cross-Docking | cross-docking | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-WAR-016-V1` | Yard Management | yard management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-LOG-CHN-001-V1` | Cold Chain Logistics | cold chain logistics; cold chain freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-002-V1` | Pharmaceutical Logistics | pharmaceutical logistics; medicine logistics; pharmaceutical freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-003-V1` | Healthcare Logistics | healthcare logistics; health care logistics; medical logistics; healthcare freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-004-V1` | Food Logistics | food logistics; food freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-005-V1` | Agricultural Logistics | agricultural logistics; agricultural freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-006-V1` | Automotive Logistics | automotive logistics; automotive freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-007-V1` | Construction Logistics | construction logistics; building logistics; construction freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-008-V1` | Retail Logistics | retail logistics; retail freight | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-LOG-CHN-009-V1` | Fashion Logistics | fashion logistics; fashion freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-010-V1` | Electronics Logistics | electronics logistics; electronics freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-011-V1` | Chemical and Hazardous-Goods Logistics | chemical and hazardous-goods logistics; chemical & hazardous-goods logistics; chemical and hazardous-goods freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-012-V1` | Humanitarian Logistics | humanitarian logistics; humanitarian freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-CHN-013-V1` | Military and Government Logistics | military and government logistics; military & government logistics; military and government freight; military and public sector logistics | `ORG-PUBLIC` | `EX-PHRASE` |
| `KW-LOG-CHN-014-V1` | Event Logistics | event logistics; event freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-001-V1` | Trucking Fleets | trucking fleets; trucking fleet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-002-V1` | Commercial Vehicle Fleets | commercial vehicle fleets; commercial vehicle fleet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-003-V1` | Delivery Fleets | delivery fleets; delivery fleet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-004-V1` | Passenger Transport Fleets | passenger transport fleets; passenger transport fleet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-005-V1` | Fleet Leasing | fleet leasing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-006-V1` | Vehicle Rental Fleets | vehicle rental fleets; vehicle rental fleet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-007-V1` | Fleet Maintenance | fleet maintenance | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-LOG-FLT-008-V1` | Fuel Management | fuel management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-LOG-FLT-009-V1` | Driver Management | driver management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-LOG-FLT-010-V1` | Route Planning | route planning | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-011-V1` | Dispatch Operations | dispatch operations; dispatch operation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-012-V1` | Telematics and Fleet Tracking | telematics and fleet tracking; telematics & fleet tracking | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-FLT-013-V1` | Transport Safety and Compliance | transport safety and compliance; transport safety & compliance | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-001-V1` | Shipping Lines | shipping lines; shipping line | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-002-V1` | Shipping Agencies | shipping agencies; shipping agency | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-003-V1` | Port Operators | port operators; port operator | `ORG-INSTITUTION` | `EX-PORT` |
| `KW-LOG-MAR-004-V1` | Container Terminals | container terminals; container terminal | `ORG-GENERIC` | `EX-PORT` |
| `KW-LOG-MAR-005-V1` | Inland Container Depots | inland container depots; inland container depot | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-006-V1` | Marine Logistics | marine logistics; marine freight | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-007-V1` | Air Cargo Terminals | air cargo terminals; air cargo terminal | `ORG-GENERIC` | `EX-PORT` |
| `KW-LOG-MAR-008-V1` | Airport Ground Handling | airport ground handling | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-LOG-MAR-009-V1` | Cargo Airlines | cargo airlines; cargo airline | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-010-V1` | Freight Airports | freight airports; freight airport | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-LOG-MAR-011-V1` | Ship Chandling | ship chandling | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-012-V1` | Marine Warehousing | marine warehousing; marine warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-LOG-MAR-013-V1` | Customs and Border Terminals | customs and border terminals; customs & border terminals | `ORG-GENERIC` | `EX-PORT` |
| `KW-LOG-DIG-001-V1` | Transport Management Systems | transport management systems; transport management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-002-V1` | Warehouse Management Systems | warehouse management systems; warehouse management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-003-V1` | Courier Management Systems | courier management systems; courier management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-004-V1` | Shipment Tracking Platforms | shipment tracking platforms; shipment tracking platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-005-V1` | Route Optimization Systems | route optimization systems; route optimization system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-006-V1` | Fleet Management Systems | fleet management systems; fleet management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-007-V1` | Freight Marketplaces | freight marketplaces; freight marketplace | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-008-V1` | Digital Freight Platforms | digital freight platforms; digital freight platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-009-V1` | Delivery Management Systems | delivery management systems; delivery management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-010-V1` | Proof-of-Delivery Systems | proof-of-delivery systems; proof-of-delivery system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-011-V1` | Logistics Control Towers | logistics control towers; logistics control tower; freight control towers | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-012-V1` | Supply-Chain Visibility | supply-chain visibility | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-013-V1` | Customs Management Systems | customs management systems; customs management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-LOG-DIG-014-V1` | Logistics Analytics | logistics analytics; freight analytics | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-015-V1` | Barcode and RFID Systems | barcode and rfid systems; barcode & rfid systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-016-V1` | Logistics Payment and Settlement | logistics payment and settlement; logistics payment & settlement; freight payment and settlement | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-LOG-DIG-017-V1` | Packaging and Pallet Services | packaging and pallet services; packaging & pallet services; packaging and pallet providers | `ORG-SOFTWARE` | `EX-PHRASE` |

## Locked interpretation

1. Every canonical domain retains a separate keyword profile and version.
2. Domain terms identify the market or subject area; activity terms remain separately governed.
3. Organization cues improve precision but are not mandatory when authoritative classification evidence exists.
4. Broad or ambiguous phrases require sector, organization, activity, source, entity, proximity, or co-occurrence context.
5. Service-gap, buying-intent, problem, competitor, replacement, integration, and existing-solution terms require an active provider offering and separate service-specific profiles.
6. Urdu, Roman Urdu, and other locale aliases require reviewed locale packs and gold-set validation before activation.
7. A matched phrase is an evidence candidate, not a domain, activity, opportunity, authority, consent, or lead decision.
8. Completed Harvest Jobs preserve the exact keyword-profile and control-profile versions used when they ran.

## Delivery boundary

This Markdown registry is a controlled documentation dataset. It does not implement database records, APIs, search indexes, embeddings, source queries, classifiers, evidence scoring, opportunity scoring, contact discovery, outreach, or releases.
