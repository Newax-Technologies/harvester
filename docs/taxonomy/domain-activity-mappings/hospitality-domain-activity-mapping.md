# Harvester Hospitality Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **79** canonical domains in `BS-009 Hospitality` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-009-AP-001` | `ACT-HSP-001`; `ACT-HSP-003`; `ACT-HSP-002`; `ACT-HSP-004`; `ACT-HSP-019` | `ACT-HSP-020`; `ACT-OPS-023`; `ACT-HSP-005`; `ACT-OPS-018`; `ACT-HSP-021` | `ACT-HSP-007`; `ACT-HSP-018`; `ACT-DIG-016` |
| `BS-009-AP-002` | `ACT-PRD-040`; `ACT-HSP-005`; `ACT-HSP-006`; `ACT-QLT-001`; `ACT-OPS-018` | `ACT-SRC-002`; `ACT-LOG-003`; `ACT-HSP-003`; `ACT-HSP-007`; `ACT-QLT-016` | `ACT-LOG-032`; `ACT-COM-009`; `ACT-MKT-003` |
| `BS-009-AP-003` | `ACT-HSP-008`; `ACT-HSP-007`; `ACT-HSP-003`; `ACT-HSP-002`; `ACT-OPS-023` | `ACT-HSP-006`; `ACT-HSP-023`; `ACT-MKT-011`; `ACT-OPS-018` | `ACT-MKT-012`; `ACT-HSP-011`; `ACT-HSP-024` |
| `BS-009-AP-004` | `ACT-HSP-002`; `ACT-HSP-018`; `ACT-OPS-018`; `ACT-HSP-003`; `ACT-MKT-020` | `ACT-HSP-027`; `ACT-HSP-021`; `ACT-HSP-007`; `ACT-DIG-016` | `ACT-HSP-014`; `ACT-HSP-013` |
| `BS-009-AP-005` | `ACT-PRF-022`; `ACT-SRC-002`; `ACT-OPS-023`; `ACT-OPS-030`; `ACT-DIG-008` | `ACT-HSP-004`; `ACT-OPS-025`; `ACT-QLT-016`; `ACT-OPS-017` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-EDU-002` |
| `BS-009-AP-006` | `ACT-PRF-022`; `ACT-SRC-002`; `ACT-OPS-023`; `ACT-OPS-030`; `ACT-DIG-008`; `ACT-PRD-040`; `ACT-HSP-005` | `ACT-HSP-004`; `ACT-OPS-025`; `ACT-QLT-016`; `ACT-OPS-017`; `ACT-HSP-006`; `ACT-QLT-001`; `ACT-OPS-018` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-EDU-002`; `ACT-LOG-032`; `ACT-MKT-003` |
| `BS-009-AP-007` | `ACT-PRF-022`; `ACT-SRC-002`; `ACT-OPS-023`; `ACT-OPS-030`; `ACT-DIG-008`; `ACT-OPS-012`; `ACT-OPS-014` | `ACT-HSP-004`; `ACT-OPS-025`; `ACT-QLT-016`; `ACT-OPS-017`; `ACT-SRC-015` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-EDU-002`; `ACT-OPS-019`; `ACT-OPS-013` |
| `BS-009-AP-008` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-DIG-004` | `ACT-HSP-003`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-MKT-020` |
| `BS-009-AP-009` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-DIG-004`; `ACT-COM-009`; `ACT-COM-008` | `ACT-HSP-003`; `ACT-DIG-016`; `ACT-DIG-007`; `ACT-OPS-005`; `ACT-OPS-017`; `ACT-LOG-006`; `ACT-OPS-018` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-MKT-020`; `ACT-LOG-020` |

## 3. Domain assignments

### 3.1 Accommodation

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-ACC-001` | Hotels | `BS-009-AP-001` |
| `HOS-ACC-002` | Business Hotels | `BS-009-AP-001` |
| `HOS-ACC-003` | Luxury Hotels | `BS-009-AP-001` |
| `HOS-ACC-004` | Budget Hotels | `BS-009-AP-001` |
| `HOS-ACC-005` | Boutique Hotels | `BS-009-AP-001` |
| `HOS-ACC-006` | Resorts | `BS-009-AP-001` |
| `HOS-ACC-007` | Guest Houses | `BS-009-AP-001` |
| `HOS-ACC-008` | Hostels | `BS-009-AP-001` |
| `HOS-ACC-009` | Serviced Apartments | `BS-009-AP-001` |
| `HOS-ACC-010` | Vacation Rentals | `BS-009-AP-001` |
| `HOS-ACC-011` | Eco-Lodges | `BS-009-AP-001` |
| `HOS-ACC-012` | Religious and Pilgrim Accommodation | `BS-009-AP-001` |
| `HOS-ACC-013` | Extended-Stay Properties | `BS-009-AP-001` |
| `HOS-ACC-014` | Conference Hotels | `BS-009-AP-001` |

### 3.2 Food and beverage hospitality

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-FNB-001` | Hotel Restaurants | `BS-009-AP-002` |
| `HOS-FNB-002` | Standalone Restaurants | `BS-009-AP-002` |
| `HOS-FNB-003` | Cafes and Coffee Shops | `BS-009-AP-002` |
| `HOS-FNB-004` | Quick-Service Restaurants | `BS-009-AP-002` |
| `HOS-FNB-005` | Fine Dining | `BS-009-AP-002` |
| `HOS-FNB-006` | Cloud Kitchens | `BS-009-AP-002` |
| `HOS-FNB-007` | Institutional Food Services | `BS-009-AP-002` |
| `HOS-FNB-008` | Room Service Operations | `BS-009-AP-002` |
| `HOS-FNB-009` | Banqueting and Catering | `BS-009-AP-002` |
| `HOS-FNB-010` | Bakeries and Dessert Shops | `BS-009-AP-002` |
| `HOS-FNB-011` | Food Courts | `BS-009-AP-002` |
| `HOS-FNB-012` | Corporate Dining | `BS-009-AP-002` |

### 3.3 Venues and events

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-VEN-001` | Banquet Halls | `BS-009-AP-003` |
| `HOS-VEN-002` | Wedding Venues | `BS-009-AP-003` |
| `HOS-VEN-003` | Conference Centres | `BS-009-AP-003` |
| `HOS-VEN-004` | Convention Centres | `BS-009-AP-003` |
| `HOS-VEN-005` | Exhibition Venues | `BS-009-AP-003` |
| `HOS-VEN-006` | Event Spaces | `BS-009-AP-003` |
| `HOS-VEN-007` | Meeting Venues | `BS-009-AP-003` |
| `HOS-VEN-008` | Cultural Venues | `BS-009-AP-003` |
| `HOS-VEN-009` | Sports Hospitality | `BS-009-AP-003` |
| `HOS-VEN-010` | Corporate Event Services | `BS-009-AP-003` |
| `HOS-VEN-011` | Event Catering | `BS-009-AP-003` |
| `HOS-VEN-012` | Venue Booking Platforms | `BS-009-AP-003` |

### 3.4 Guest experience and services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-GST-001` | Front-Office Operations | `BS-009-AP-004` |
| `HOS-GST-002` | Reservations | `BS-009-AP-004` |
| `HOS-GST-003` | Guest Relations | `BS-009-AP-004` |
| `HOS-GST-004` | Concierge Services | `BS-009-AP-004` |
| `HOS-GST-005` | Housekeeping | `BS-009-AP-004` |
| `HOS-GST-006` | Laundry and Linen | `BS-009-AP-004` |
| `HOS-GST-007` | Spa and Wellness | `BS-009-AP-004` |
| `HOS-GST-008` | Recreation Services | `BS-009-AP-004` |
| `HOS-GST-009` | Kids Clubs and Family Services | `BS-009-AP-004` |
| `HOS-GST-010` | Guest Transport | `BS-009-AP-004` |
| `HOS-GST-011` | Loyalty Programs | `BS-009-AP-004` |
| `HOS-GST-012` | Guest Feedback and Reputation Management | `BS-009-AP-004` |

### 3.5 Hospitality operations and supply

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-OPS-001` | Property Management Systems | `BS-009-AP-005` |
| `HOS-OPS-002` | Hotel Booking Engines | `BS-009-AP-005` |
| `HOS-OPS-003` | Channel Management Systems | `BS-009-AP-005` |
| `HOS-OPS-004` | Revenue Management Systems | `BS-009-AP-005` |
| `HOS-OPS-005` | Restaurant POS Systems | `BS-009-AP-006` |
| `HOS-OPS-006` | Kitchen Management Systems | `BS-009-AP-005` |
| `HOS-OPS-007` | Housekeeping Management Systems | `BS-009-AP-005` |
| `HOS-OPS-008` | Maintenance Management Systems | `BS-009-AP-007` |
| `HOS-OPS-009` | Hospitality CRM | `BS-009-AP-005` |
| `HOS-OPS-010` | Inventory and Procurement Systems | `BS-009-AP-005` |
| `HOS-OPS-011` | Food Safety and Hygiene Services | `BS-009-AP-005` |
| `HOS-OPS-012` | Hospitality Staffing | `BS-009-AP-005` |
| `HOS-OPS-013` | Hospitality Supplies | `BS-009-AP-005` |
| `HOS-OPS-014` | Hotel Furniture and Fixtures | `BS-009-AP-005` |
| `HOS-OPS-015` | Commercial Kitchen Equipment | `BS-009-AP-005` |
| `HOS-OPS-016` | Hospitality Laundry Services | `BS-009-AP-005` |
| `HOS-OPS-017` | Hotel Security Services | `BS-009-AP-005` |
| `HOS-OPS-018` | Facility and Energy Management | `BS-009-AP-005` |

### 3.6 Hospitality digital commerce and intelligence

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `HOS-DIG-001` | Direct Booking Platforms | `BS-009-AP-008` |
| `HOS-DIG-002` | Online Reputation Platforms | `BS-009-AP-008` |
| `HOS-DIG-003` | Guest Messaging Systems | `BS-009-AP-008` |
| `HOS-DIG-004` | Digital Check-In and Check-Out | `BS-009-AP-008` |
| `HOS-DIG-005` | Mobile Guest Applications | `BS-009-AP-008` |
| `HOS-DIG-006` | Hospitality Analytics | `BS-009-AP-008` |
| `HOS-DIG-007` | Dynamic Pricing Systems | `BS-009-AP-008` |
| `HOS-DIG-008` | Digital Menus and Ordering | `BS-009-AP-008` |
| `HOS-DIG-009` | Contactless Guest Services | `BS-009-AP-008` |
| `HOS-DIG-010` | Loyalty and Membership Platforms | `BS-009-AP-008` |
| `HOS-DIG-011` | Hospitality Marketplace Integrations | `BS-009-AP-009` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
