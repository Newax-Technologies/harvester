# Harvester Travel Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **75** canonical domains in `BS-010 Travel` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-010-AP-001` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-HSP-012`; `ACT-OPS-018`; `ACT-FIN-006` | `ACT-HSP-003`; `ACT-HSP-016`; `ACT-HSP-017`; `ACT-HSP-027` | `ACT-HSP-028`; `ACT-HSP-030`; `ACT-MKT-003` |
| `BS-010-AP-002` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-HSP-012`; `ACT-OPS-018`; `ACT-FIN-006`; `ACT-HSP-001`; `ACT-HSP-003` | `ACT-HSP-016`; `ACT-HSP-017`; `ACT-HSP-027`; `ACT-HSP-002`; `ACT-HSP-004`; `ACT-HSP-019` | `ACT-HSP-028`; `ACT-HSP-030`; `ACT-MKT-003`; `ACT-HSP-020`; `ACT-HSP-018` |
| `BS-010-AP-003` | `ACT-HSP-009`; `ACT-HSP-013`; `ACT-HSP-012`; `ACT-HSP-026`; `ACT-OPS-018` | `ACT-HSP-010`; `ACT-HSP-014`; `ACT-HSP-007`; `ACT-MKT-003` | `ACT-HSP-011`; `ACT-HSP-030`; `ACT-HSP-001` |
| `BS-010-AP-004` | `ACT-HSP-009`; `ACT-HSP-013`; `ACT-HSP-012`; `ACT-HSP-026`; `ACT-OPS-018`; `ACT-EDU-002` | `ACT-HSP-010`; `ACT-HSP-014`; `ACT-HSP-007`; `ACT-MKT-003`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-HSP-011`; `ACT-HSP-030`; `ACT-HSP-001`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-010-AP-005` | `ACT-HSP-015`; `ACT-HSP-010`; `ACT-HSP-001`; `ACT-HSP-014`; `ACT-HSP-027` | `ACT-HSP-016`; `ACT-HSP-017`; `ACT-HSP-030`; `ACT-OPS-018` | `ACT-HSP-009`; `ACT-PUB-009`; `ACT-PUB-028` |
| `BS-010-AP-006` | `ACT-HSP-015`; `ACT-HSP-010`; `ACT-HSP-001`; `ACT-HSP-014`; `ACT-HSP-027`; `ACT-HSP-009`; `ACT-HSP-013` | `ACT-HSP-016`; `ACT-HSP-017`; `ACT-HSP-030`; `ACT-OPS-018`; `ACT-HSP-012`; `ACT-HSP-026` | `ACT-PUB-009`; `ACT-PUB-028`; `ACT-MKT-003` |
| `BS-010-AP-007` | `ACT-HSP-015`; `ACT-HSP-010`; `ACT-HSP-001`; `ACT-HSP-014`; `ACT-HSP-027`; `ACT-HSP-003` | `ACT-HSP-016`; `ACT-HSP-017`; `ACT-HSP-030`; `ACT-OPS-018`; `ACT-HSP-002`; `ACT-HSP-004`; `ACT-HSP-019` | `ACT-HSP-009`; `ACT-PUB-009`; `ACT-PUB-028`; `ACT-HSP-020`; `ACT-HSP-018` |
| `BS-010-AP-008` | `ACT-HSP-014`; `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-OPS-018` | `ACT-HSP-011`; `ACT-HSP-003`; `ACT-OPS-011`; `ACT-OPS-012` | `ACT-DIG-016`; `ACT-LOG-020`; `ACT-HSP-027` |
| `BS-010-AP-009` | `ACT-HSP-014`; `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-OPS-018`; `ACT-LOG-014`; `ACT-LOG-028` | `ACT-HSP-011`; `ACT-HSP-003`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-LOG-029`; `ACT-LOG-030`; `ACT-LOG-025` | `ACT-DIG-016`; `ACT-LOG-020`; `ACT-HSP-027`; `ACT-LOG-031`; `ACT-QLT-014` |
| `BS-010-AP-010` | `ACT-HSP-014`; `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-OPS-018`; `ACT-LOG-013`; `ACT-LOG-014` | `ACT-HSP-011`; `ACT-HSP-003`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-LOG-029`; `ACT-LOG-030`; `ACT-LOG-025` | `ACT-DIG-016`; `ACT-LOG-020`; `ACT-HSP-027`; `ACT-COM-012`; `ACT-LOG-031`; `ACT-QLT-014` |
| `BS-010-AP-011` | `ACT-HSP-014`; `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-OPS-018`; `ACT-LOG-013` | `ACT-HSP-011`; `ACT-HSP-003`; `ACT-OPS-011`; `ACT-OPS-012` | `ACT-DIG-016`; `ACT-LOG-020`; `ACT-HSP-027`; `ACT-COM-012` |
| `BS-010-AP-012` | `ACT-HSP-014`; `ACT-LOG-022`; `ACT-LOG-023`; `ACT-LOG-021`; `ACT-OPS-018`; `ACT-HSP-009`; `ACT-HSP-013` | `ACT-HSP-011`; `ACT-HSP-003`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-HSP-012`; `ACT-HSP-026`; `ACT-LOG-029`; `ACT-LOG-030` | `ACT-DIG-016`; `ACT-LOG-020`; `ACT-HSP-027`; `ACT-MKT-003`; `ACT-COM-012`; `ACT-LOG-031` |
| `BS-010-AP-013` | `ACT-HSP-017`; `ACT-HSP-016`; `ACT-PRF-012`; `ACT-OPS-018`; `ACT-QLT-010` | `ACT-PRF-033`; `ACT-PRF-015`; `ACT-HSP-027`; `ACT-HLT-020` | `ACT-PRF-031`; `ACT-LEG-001`; `ACT-HSP-028` |
| `BS-010-AP-014` | `ACT-HSP-017`; `ACT-HSP-016`; `ACT-PRF-012`; `ACT-OPS-018`; `ACT-QLT-010`; `ACT-FIN-013`; `ACT-FIN-015` | `ACT-PRF-033`; `ACT-PRF-015`; `ACT-HSP-027`; `ACT-HLT-020`; `ACT-QLT-013` | `ACT-PRF-031`; `ACT-LEG-001`; `ACT-HSP-028`; `ACT-QLT-023`; `ACT-FIN-010` |
| `BS-010-AP-015` | `ACT-HSP-017`; `ACT-HSP-016`; `ACT-PRF-012`; `ACT-OPS-018`; `ACT-QLT-010`; `ACT-HSP-009`; `ACT-HSP-013` | `ACT-PRF-033`; `ACT-PRF-015`; `ACT-HSP-027`; `ACT-HLT-020`; `ACT-HSP-012`; `ACT-HSP-026` | `ACT-PRF-031`; `ACT-LEG-001`; `ACT-HSP-028`; `ACT-HSP-014`; `ACT-MKT-003` |
| `BS-010-AP-016` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017` | `ACT-OPS-007`; `ACT-DIG-003` |
| `BS-010-AP-017` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004`; `ACT-COM-001`; `ACT-COM-002` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-010-AP-018` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004`; `ACT-HSP-010`; `ACT-HSP-011` | `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017`; `ACT-HSP-012`; `ACT-OPS-018`; `ACT-FIN-006` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-HSP-016`; `ACT-HSP-017` |
| `BS-010-AP-019` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004`; `ACT-HSP-009`; `ACT-HSP-013` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017`; `ACT-HSP-012`; `ACT-HSP-026` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-HSP-014`; `ACT-MKT-003` |
| `BS-010-AP-020` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-OPS-017` |
| `BS-010-AP-021` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-DIG-004`; `ACT-OPS-004`; `ACT-FIN-006`; `ACT-FIN-031` | `ACT-HSP-010`; `ACT-HSP-011`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017`; `ACT-QLT-010`; `ACT-QLT-023` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-FIN-007`; `ACT-FIN-009` |

## 3. Domain assignments

### 3.1 Travel agencies and booking

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-AGY-001` | Retail Travel Agencies | `BS-010-AP-001` |
| `TRV-AGY-002` | Corporate Travel Management | `BS-010-AP-001` |
| `TRV-AGY-003` | Online Travel Agencies | `BS-010-AP-001` |
| `TRV-AGY-004` | Business Travel Services | `BS-010-AP-001` |
| `TRV-AGY-005` | Ticketing Agencies | `BS-010-AP-001` |
| `TRV-AGY-006` | Airline Booking Services | `BS-010-AP-001` |
| `TRV-AGY-007` | Hotel Booking Services | `BS-010-AP-002` |
| `TRV-AGY-008` | Rail Booking Services | `BS-010-AP-001` |
| `TRV-AGY-009` | Bus Booking Services | `BS-010-AP-001` |
| `TRV-AGY-010` | Travel Consolidators | `BS-010-AP-001` |
| `TRV-AGY-011` | Travel Metasearch | `BS-010-AP-001` |
| `TRV-AGY-012` | Travel Membership Services | `BS-010-AP-001` |

### 3.2 Tours and destination services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-TOU-001` | Inbound Tour Operators | `BS-010-AP-003` |
| `TRV-TOU-002` | Outbound Tour Operators | `BS-010-AP-003` |
| `TRV-TOU-003` | Domestic Tour Operators | `BS-010-AP-003` |
| `TRV-TOU-004` | Destination Management Companies | `BS-010-AP-003` |
| `TRV-TOU-005` | City Tours | `BS-010-AP-003` |
| `TRV-TOU-006` | Cultural and Heritage Tours | `BS-010-AP-003` |
| `TRV-TOU-007` | Adventure Tourism | `BS-010-AP-003` |
| `TRV-TOU-008` | Eco-Tourism | `BS-010-AP-003` |
| `TRV-TOU-009` | Medical Tourism | `BS-010-AP-003` |
| `TRV-TOU-010` | Educational Tours | `BS-010-AP-004` |
| `TRV-TOU-011` | Religious Tourism | `BS-010-AP-003` |
| `TRV-TOU-012` | Luxury Travel | `BS-010-AP-003` |
| `TRV-TOU-013` | Group Travel | `BS-010-AP-003` |
| `TRV-TOU-014` | Independent Travel Services | `BS-010-AP-003` |
| `TRV-TOU-015` | Guided Tour Services | `BS-010-AP-003` |
| `TRV-TOU-016` | Excursion and Activity Providers | `BS-010-AP-003` |

### 3.3 Hajj, Umrah and pilgrimage

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-PIL-001` | Hajj Operators | `BS-010-AP-005` |
| `TRV-PIL-002` | Umrah Operators | `BS-010-AP-005` |
| `TRV-PIL-003` | Pilgrimage Travel Agencies | `BS-010-AP-005` |
| `TRV-PIL-004` | Religious Tour Packages | `BS-010-AP-006` |
| `TRV-PIL-005` | Pilgrim Accommodation Coordination | `BS-010-AP-007` |
| `TRV-PIL-006` | Pilgrim Transport Coordination | `BS-010-AP-005` |
| `TRV-PIL-007` | Visa and Documentation Support | `BS-010-AP-005` |
| `TRV-PIL-008` | Group Leader and Guide Services | `BS-010-AP-005` |
| `TRV-PIL-009` | Pilgrim Welfare Services | `BS-010-AP-005` |
| `TRV-PIL-010` | Religious Travel Platforms | `BS-010-AP-005` |

### 3.4 Passenger mobility

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-MOB-001` | Airlines | `BS-010-AP-008` |
| `TRV-MOB-002` | Charter Aviation | `BS-010-AP-009` |
| `TRV-MOB-003` | Airport Passenger Services | `BS-010-AP-010` |
| `TRV-MOB-004` | Rail Passenger Services | `BS-010-AP-011` |
| `TRV-MOB-005` | Intercity Bus Services | `BS-010-AP-008` |
| `TRV-MOB-006` | Coach Operators | `BS-010-AP-008` |
| `TRV-MOB-007` | Car Rental | `BS-010-AP-008` |
| `TRV-MOB-008` | Chauffeur Services | `BS-010-AP-008` |
| `TRV-MOB-009` | Ride-Hailing | `BS-010-AP-008` |
| `TRV-MOB-010` | Ferry and Passenger Shipping | `BS-010-AP-010` |
| `TRV-MOB-011` | Cruise Travel | `BS-010-AP-008` |
| `TRV-MOB-012` | Tourist Transport | `BS-010-AP-012` |

### 3.5 Travel documentation and assistance

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-DOC-001` | Visa Services | `BS-010-AP-013` |
| `TRV-DOC-002` | Passport and Documentation Assistance | `BS-010-AP-013` |
| `TRV-DOC-003` | Travel Insurance and Takaful | `BS-010-AP-014` |
| `TRV-DOC-004` | Foreign Exchange for Travel | `BS-010-AP-013` |
| `TRV-DOC-005` | Travel Health Services | `BS-010-AP-013` |
| `TRV-DOC-006` | Travel Vaccination Services | `BS-010-AP-013` |
| `TRV-DOC-007` | Travel Assistance and Emergency Support | `BS-010-AP-013` |
| `TRV-DOC-008` | Relocation Services | `BS-010-AP-013` |
| `TRV-DOC-009` | Immigration Support | `BS-010-AP-013` |
| `TRV-DOC-010` | Destination Information Services | `BS-010-AP-015` |

### 3.6 Travel technology and operations

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TRV-DIG-001` | Reservation Systems | `BS-010-AP-016` |
| `TRV-DIG-002` | Global Distribution Systems | `BS-010-AP-017` |
| `TRV-DIG-003` | Travel Agency Management Systems | `BS-010-AP-018` |
| `TRV-DIG-004` | Tour Operator Management Systems | `BS-010-AP-019` |
| `TRV-DIG-005` | Itinerary Management | `BS-010-AP-020` |
| `TRV-DIG-006` | Travel CRM Systems | `BS-010-AP-016` |
| `TRV-DIG-007` | Fare and Rate Management | `BS-010-AP-020` |
| `TRV-DIG-008` | Travel Payment Systems | `BS-010-AP-021` |
| `TRV-DIG-009` | Travel Inventory Systems | `BS-010-AP-016` |
| `TRV-DIG-010` | Dynamic Packaging Platforms | `BS-010-AP-016` |
| `TRV-DIG-011` | Travel Mobile Applications | `BS-010-AP-016` |
| `TRV-DIG-012` | Destination Content Platforms | `BS-010-AP-019` |
| `TRV-DIG-013` | Travel Analytics | `BS-010-AP-020` |
| `TRV-DIG-014` | Loyalty and Rewards Platforms | `BS-010-AP-016` |
| `TRV-DIG-015` | Travel Customer Support Platforms | `BS-010-AP-016` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
