# Harvester Hospitality Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-009 Hospitality`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Hospitality
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

This registry contains **79 canonical domains** in **6 families**.

| Family | Name | Count |
| --- | --- | --- |
| `HOS-ACC` | Accommodation | 14 |
| `HOS-FNB` | Food and beverage hospitality | 12 |
| `HOS-VEN` | Venues and events | 12 |
| `HOS-GST` | Guest experience and services | 12 |
| `HOS-OPS` | Hospitality operations and supply | 18 |
| `HOS-DIG` | Hospitality digital commerce and intelligence | 11 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Accommodation

| Code | Domain |
| --- | --- |
| `HOS-ACC-001` | Hotels |
| `HOS-ACC-002` | Business Hotels |
| `HOS-ACC-003` | Luxury Hotels |
| `HOS-ACC-004` | Budget Hotels |
| `HOS-ACC-005` | Boutique Hotels |
| `HOS-ACC-006` | Resorts |
| `HOS-ACC-007` | Guest Houses |
| `HOS-ACC-008` | Hostels |
| `HOS-ACC-009` | Serviced Apartments |
| `HOS-ACC-010` | Vacation Rentals |
| `HOS-ACC-011` | Eco-Lodges |
| `HOS-ACC-012` | Religious and Pilgrim Accommodation |
| `HOS-ACC-013` | Extended-Stay Properties |
| `HOS-ACC-014` | Conference Hotels |

### 4.2 Food and beverage hospitality

| Code | Domain |
| --- | --- |
| `HOS-FNB-001` | Hotel Restaurants |
| `HOS-FNB-002` | Standalone Restaurants |
| `HOS-FNB-003` | Cafes and Coffee Shops |
| `HOS-FNB-004` | Quick-Service Restaurants |
| `HOS-FNB-005` | Fine Dining |
| `HOS-FNB-006` | Cloud Kitchens |
| `HOS-FNB-007` | Institutional Food Services |
| `HOS-FNB-008` | Room Service Operations |
| `HOS-FNB-009` | Banqueting and Catering |
| `HOS-FNB-010` | Bakeries and Dessert Shops |
| `HOS-FNB-011` | Food Courts |
| `HOS-FNB-012` | Corporate Dining |

### 4.3 Venues and events

| Code | Domain |
| --- | --- |
| `HOS-VEN-001` | Banquet Halls |
| `HOS-VEN-002` | Wedding Venues |
| `HOS-VEN-003` | Conference Centres |
| `HOS-VEN-004` | Convention Centres |
| `HOS-VEN-005` | Exhibition Venues |
| `HOS-VEN-006` | Event Spaces |
| `HOS-VEN-007` | Meeting Venues |
| `HOS-VEN-008` | Cultural Venues |
| `HOS-VEN-009` | Sports Hospitality |
| `HOS-VEN-010` | Corporate Event Services |
| `HOS-VEN-011` | Event Catering |
| `HOS-VEN-012` | Venue Booking Platforms |

### 4.4 Guest experience and services

| Code | Domain |
| --- | --- |
| `HOS-GST-001` | Front-Office Operations |
| `HOS-GST-002` | Reservations |
| `HOS-GST-003` | Guest Relations |
| `HOS-GST-004` | Concierge Services |
| `HOS-GST-005` | Housekeeping |
| `HOS-GST-006` | Laundry and Linen |
| `HOS-GST-007` | Spa and Wellness |
| `HOS-GST-008` | Recreation Services |
| `HOS-GST-009` | Kids Clubs and Family Services |
| `HOS-GST-010` | Guest Transport |
| `HOS-GST-011` | Loyalty Programs |
| `HOS-GST-012` | Guest Feedback and Reputation Management |

### 4.5 Hospitality operations and supply

| Code | Domain |
| --- | --- |
| `HOS-OPS-001` | Property Management Systems |
| `HOS-OPS-002` | Hotel Booking Engines |
| `HOS-OPS-003` | Channel Management Systems |
| `HOS-OPS-004` | Revenue Management Systems |
| `HOS-OPS-005` | Restaurant POS Systems |
| `HOS-OPS-006` | Kitchen Management Systems |
| `HOS-OPS-007` | Housekeeping Management Systems |
| `HOS-OPS-008` | Maintenance Management Systems |
| `HOS-OPS-009` | Hospitality CRM |
| `HOS-OPS-010` | Inventory and Procurement Systems |
| `HOS-OPS-011` | Food Safety and Hygiene Services |
| `HOS-OPS-012` | Hospitality Staffing |
| `HOS-OPS-013` | Hospitality Supplies |
| `HOS-OPS-014` | Hotel Furniture and Fixtures |
| `HOS-OPS-015` | Commercial Kitchen Equipment |
| `HOS-OPS-016` | Hospitality Laundry Services |
| `HOS-OPS-017` | Hotel Security Services |
| `HOS-OPS-018` | Facility and Energy Management |

### 4.6 Hospitality digital commerce and intelligence

| Code | Domain |
| --- | --- |
| `HOS-DIG-001` | Direct Booking Platforms |
| `HOS-DIG-002` | Online Reputation Platforms |
| `HOS-DIG-003` | Guest Messaging Systems |
| `HOS-DIG-004` | Digital Check-In and Check-Out |
| `HOS-DIG-005` | Mobile Guest Applications |
| `HOS-DIG-006` | Hospitality Analytics |
| `HOS-DIG-007` | Dynamic Pricing Systems |
| `HOS-DIG-008` | Digital Menus and Ordering |
| `HOS-DIG-009` | Contactless Guest Services |
| `HOS-DIG-010` | Loyalty and Membership Platforms |
| `HOS-DIG-011` | Hospitality Marketplace Integrations |

## 5. First-release presentation shortlist

Hotels, Resorts, Guest Houses, Serviced Apartments, Vacation Rentals, Restaurants, Cafes and Coffee Shops, Quick-Service Restaurants, Cloud Kitchens, Banquet Halls, Wedding Venues, Conference Centres, Event Spaces, Reservations, Guest Relations, Housekeeping, Laundry and Linen, Spa and Wellness, Loyalty Programs, Property Management Systems, Hotel Booking Engines, Channel Management Systems, Revenue Management Systems, Restaurant POS, Kitchen Management Systems, Housekeeping Management Systems, Maintenance Management Systems, Hospitality CRM, Inventory and Procurement, Hospitality Staffing, Hospitality Supplies, Direct Booking Platforms, Guest Messaging Systems, Digital Check-In, Hospitality Analytics, Facility and Energy Management.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Hotels:** Operating, Booking, Hosting, Housekeeping, Maintaining, Managing revenue
- **Restaurants:** Preparing, Serving, Ordering, Delivering, Catering, Managing inventory
- **Venues:** Booking, Hosting events, Catering, Scheduling, Managing facilities
- **Hospitality technology:** Developing, Implementing, Integrating, Hosting, Supporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Hotel booking | Travel; Technology | Publishing; booking; payments |
| Hospitality property | Real Estate | Leasing; operating; maintaining |
| Food services | Food and Agriculture; Retail | Sourcing; preparing; selling |
| Facility and energy management | Construction; Energy | Monitoring; maintaining; optimizing |

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

- The shortlist and all 79 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
