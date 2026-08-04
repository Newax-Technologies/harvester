# Harvester Travel Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-010 Travel`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Travel
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

This registry contains **75 canonical domains** in **6 families**.

| Family | Name | Count |
| --- | --- | --- |
| `TRV-AGY` | Travel agencies and booking | 12 |
| `TRV-TOU` | Tours and destination services | 16 |
| `TRV-PIL` | Hajj, Umrah and pilgrimage | 10 |
| `TRV-MOB` | Passenger mobility | 12 |
| `TRV-DOC` | Travel documentation and assistance | 10 |
| `TRV-DIG` | Travel technology and operations | 15 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Travel agencies and booking

| Code | Domain |
| --- | --- |
| `TRV-AGY-001` | Retail Travel Agencies |
| `TRV-AGY-002` | Corporate Travel Management |
| `TRV-AGY-003` | Online Travel Agencies |
| `TRV-AGY-004` | Business Travel Services |
| `TRV-AGY-005` | Ticketing Agencies |
| `TRV-AGY-006` | Airline Booking Services |
| `TRV-AGY-007` | Hotel Booking Services |
| `TRV-AGY-008` | Rail Booking Services |
| `TRV-AGY-009` | Bus Booking Services |
| `TRV-AGY-010` | Travel Consolidators |
| `TRV-AGY-011` | Travel Metasearch |
| `TRV-AGY-012` | Travel Membership Services |

### 4.2 Tours and destination services

| Code | Domain |
| --- | --- |
| `TRV-TOU-001` | Inbound Tour Operators |
| `TRV-TOU-002` | Outbound Tour Operators |
| `TRV-TOU-003` | Domestic Tour Operators |
| `TRV-TOU-004` | Destination Management Companies |
| `TRV-TOU-005` | City Tours |
| `TRV-TOU-006` | Cultural and Heritage Tours |
| `TRV-TOU-007` | Adventure Tourism |
| `TRV-TOU-008` | Eco-Tourism |
| `TRV-TOU-009` | Medical Tourism |
| `TRV-TOU-010` | Educational Tours |
| `TRV-TOU-011` | Religious Tourism |
| `TRV-TOU-012` | Luxury Travel |
| `TRV-TOU-013` | Group Travel |
| `TRV-TOU-014` | Independent Travel Services |
| `TRV-TOU-015` | Guided Tour Services |
| `TRV-TOU-016` | Excursion and Activity Providers |

### 4.3 Hajj, Umrah and pilgrimage

| Code | Domain |
| --- | --- |
| `TRV-PIL-001` | Hajj Operators |
| `TRV-PIL-002` | Umrah Operators |
| `TRV-PIL-003` | Pilgrimage Travel Agencies |
| `TRV-PIL-004` | Religious Tour Packages |
| `TRV-PIL-005` | Pilgrim Accommodation Coordination |
| `TRV-PIL-006` | Pilgrim Transport Coordination |
| `TRV-PIL-007` | Visa and Documentation Support |
| `TRV-PIL-008` | Group Leader and Guide Services |
| `TRV-PIL-009` | Pilgrim Welfare Services |
| `TRV-PIL-010` | Religious Travel Platforms |

### 4.4 Passenger mobility

| Code | Domain |
| --- | --- |
| `TRV-MOB-001` | Airlines |
| `TRV-MOB-002` | Charter Aviation |
| `TRV-MOB-003` | Airport Passenger Services |
| `TRV-MOB-004` | Rail Passenger Services |
| `TRV-MOB-005` | Intercity Bus Services |
| `TRV-MOB-006` | Coach Operators |
| `TRV-MOB-007` | Car Rental |
| `TRV-MOB-008` | Chauffeur Services |
| `TRV-MOB-009` | Ride-Hailing |
| `TRV-MOB-010` | Ferry and Passenger Shipping |
| `TRV-MOB-011` | Cruise Travel |
| `TRV-MOB-012` | Tourist Transport |

### 4.5 Travel documentation and assistance

| Code | Domain |
| --- | --- |
| `TRV-DOC-001` | Visa Services |
| `TRV-DOC-002` | Passport and Documentation Assistance |
| `TRV-DOC-003` | Travel Insurance and Takaful |
| `TRV-DOC-004` | Foreign Exchange for Travel |
| `TRV-DOC-005` | Travel Health Services |
| `TRV-DOC-006` | Travel Vaccination Services |
| `TRV-DOC-007` | Travel Assistance and Emergency Support |
| `TRV-DOC-008` | Relocation Services |
| `TRV-DOC-009` | Immigration Support |
| `TRV-DOC-010` | Destination Information Services |

### 4.6 Travel technology and operations

| Code | Domain |
| --- | --- |
| `TRV-DIG-001` | Reservation Systems |
| `TRV-DIG-002` | Global Distribution Systems |
| `TRV-DIG-003` | Travel Agency Management Systems |
| `TRV-DIG-004` | Tour Operator Management Systems |
| `TRV-DIG-005` | Itinerary Management |
| `TRV-DIG-006` | Travel CRM Systems |
| `TRV-DIG-007` | Fare and Rate Management |
| `TRV-DIG-008` | Travel Payment Systems |
| `TRV-DIG-009` | Travel Inventory Systems |
| `TRV-DIG-010` | Dynamic Packaging Platforms |
| `TRV-DIG-011` | Travel Mobile Applications |
| `TRV-DIG-012` | Destination Content Platforms |
| `TRV-DIG-013` | Travel Analytics |
| `TRV-DIG-014` | Loyalty and Rewards Platforms |
| `TRV-DIG-015` | Travel Customer Support Platforms |

## 5. First-release presentation shortlist

Travel Agencies, Corporate Travel Management, Online Travel Agencies, Ticketing Agencies, Airline Booking, Hotel Booking, Inbound Tour Operators, Outbound Tour Operators, Domestic Tour Operators, Destination Management Companies, Adventure Tourism, Medical Tourism, Educational Tours, Religious Tourism, Hajj Operators, Umrah Operators, Pilgrimage Services, Airlines, Airport Passenger Services, Rail Passenger Services, Intercity Bus Services, Car Rental, Chauffeur Services, Tourist Transport, Visa Services, Travel Takaful, Travel Assistance, Reservation Systems, Travel Agency Management Systems, Tour Operator Management Systems, Itinerary Management, Travel CRM Systems, Dynamic Packaging Platforms, Travel Mobile Applications, Travel Analytics.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Travel agencies:** Advising, Booking, Ticketing, Packaging, Supporting, Collecting payments
- **Tour operators:** Designing tours, Contracting suppliers, Scheduling, Guiding, Operating transport
- **Pilgrimage services:** Registering, Documenting, Grouping, Booking, Coordinating, Supporting pilgrims
- **Travel technology:** Developing, Licensing, Integrating, Hosting, Supporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Hotel booking | Hospitality; Technology | Booking; payments; channel integration |
| Passenger transport | Logistics | Scheduling; ticketing; transporting |
| Medical tourism | Healthcare; Hospitality | Coordinating; booking; supporting |
| Travel payments | Finance; Technology | Processing; reconciling; refunding |

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

- The shortlist and all 75 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
