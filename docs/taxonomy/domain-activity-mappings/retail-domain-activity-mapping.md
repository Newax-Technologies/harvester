# Harvester Retail Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **84** canonical domains in `BS-008 Retail` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-008-AP-001` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-COM-018`; `ACT-LOG-003` | `ACT-SRC-003`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-MKT-003`; `ACT-COM-024` | `ACT-COM-009`; `ACT-LOG-032`; `ACT-LOG-026` |
| `BS-008-AP-002` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-COM-018`; `ACT-LOG-003` | `ACT-SRC-003`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-MKT-003`; `ACT-COM-024`; `ACT-OPS-018` | `ACT-COM-009`; `ACT-LOG-032`; `ACT-LOG-026` |
| `BS-008-AP-003` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-COM-018`; `ACT-MKT-003` | `ACT-SRC-007`; `ACT-LOG-003`; `ACT-COM-009`; `ACT-MKT-004`; `ACT-OPS-018` | `ACT-PRD-033`; `ACT-COM-005`; `ACT-LOG-026` |
| `BS-008-AP-004` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-COM-018`; `ACT-MKT-003` | `ACT-SRC-007`; `ACT-LOG-003`; `ACT-COM-009`; `ACT-MKT-004` | `ACT-PRD-033`; `ACT-COM-005`; `ACT-LOG-026` |
| `BS-008-AP-005` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-LOG-003`; `ACT-OPS-018` | `ACT-SRC-007`; `ACT-LOG-001`; `ACT-COM-009`; `ACT-LOG-032`; `ACT-OPS-001`; `ACT-COM-018` | `ACT-OPS-014`; `ACT-COM-012`; `ACT-COM-029`; `ACT-MKT-003` |
| `BS-008-AP-006` | `ACT-SRC-001`; `ACT-COM-006`; `ACT-COM-004`; `ACT-COM-020`; `ACT-LOG-003` | `ACT-SRC-007`; `ACT-FIN-002`; `ACT-COM-012`; `ACT-COM-029`; `ACT-OPS-015` | `ACT-COM-009`; `ACT-OPS-014`; `ACT-SRC-015` |
| `BS-008-AP-007` | `ACT-SRC-001`; `ACT-COM-006`; `ACT-COM-004`; `ACT-COM-020`; `ACT-LOG-003`; `ACT-COM-003` | `ACT-SRC-007`; `ACT-FIN-002`; `ACT-COM-012`; `ACT-COM-029`; `ACT-OPS-015`; `ACT-COM-018`; `ACT-OPS-018` | `ACT-COM-009`; `ACT-OPS-014`; `ACT-SRC-015`; `ACT-MKT-003` |
| `BS-008-AP-008` | `ACT-SRC-001`; `ACT-COM-006`; `ACT-COM-004`; `ACT-COM-020`; `ACT-LOG-003`; `ACT-COM-003`; `ACT-SRC-014` | `ACT-SRC-007`; `ACT-FIN-002`; `ACT-COM-012`; `ACT-COM-029`; `ACT-OPS-015`; `ACT-COM-018`; `ACT-OPS-018`; `ACT-OPS-012` | `ACT-COM-009`; `ACT-SRC-015`; `ACT-MKT-003`; `ACT-OPS-016`; `ACT-HSP-014` |
| `BS-008-AP-009` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-LOG-003`; `ACT-QLT-010`; `ACT-HLT-004` | `ACT-SRC-007`; `ACT-LOG-001`; `ACT-MKT-003`; `ACT-OPS-018`; `ACT-COM-018`; `ACT-QLT-011` | `ACT-COM-009` |
| `BS-008-AP-010` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-LOG-003`; `ACT-QLT-010` | `ACT-SRC-007`; `ACT-LOG-001`; `ACT-MKT-003`; `ACT-OPS-018`; `ACT-COM-018` | `ACT-HLT-004`; `ACT-COM-009`; `ACT-QLT-011` |
| `BS-008-AP-011` | `ACT-SRC-001`; `ACT-COM-003`; `ACT-COM-004`; `ACT-LOG-003`; `ACT-QLT-010`; `ACT-EDU-002` | `ACT-SRC-007`; `ACT-LOG-001`; `ACT-MKT-003`; `ACT-OPS-018`; `ACT-COM-018`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-HLT-004`; `ACT-COM-009`; `ACT-QLT-011`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-008-AP-012` | `ACT-COM-009`; `ACT-COM-008`; `ACT-LOG-006`; `ACT-LOG-007`; `ACT-DIG-016`; `ACT-COM-003`; `ACT-COM-004` | `ACT-LOG-003`; `ACT-OPS-018`; `ACT-LOG-026`; `ACT-MKT-015`; `ACT-DIG-007`; `ACT-COM-018` | `ACT-COM-010`; `ACT-LOG-020`; `ACT-DIG-004`; `ACT-MKT-003` |
| `BS-008-AP-013` | `ACT-COM-009`; `ACT-COM-008`; `ACT-LOG-006`; `ACT-LOG-007`; `ACT-DIG-016` | `ACT-LOG-003`; `ACT-OPS-018`; `ACT-LOG-026`; `ACT-MKT-015`; `ACT-DIG-007` | `ACT-COM-010`; `ACT-LOG-020`; `ACT-DIG-004` |
| `BS-008-AP-014` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002` |
| `BS-008-AP-015` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-COM-003`; `ACT-COM-004` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002`; `ACT-COM-009`; `ACT-MKT-003` |
| `BS-008-AP-016` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-COM-009`; `ACT-COM-008` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030`; `ACT-DIG-016`; `ACT-LOG-006` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002`; `ACT-LOG-020` |
| `BS-008-AP-017` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-LOG-001`; `ACT-COM-003` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002`; `ACT-LOG-027`; `ACT-COM-009`; `ACT-MKT-003` |
| `BS-008-AP-018` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-MKT-001`; `ACT-MKT-003` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030`; `ACT-MKT-005`; `ACT-MKT-015` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002`; `ACT-MKT-002`; `ACT-MKT-007` |
| `BS-008-AP-019` | `ACT-PRF-022`; `ACT-LOG-003`; `ACT-COM-024`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-COM-003`; `ACT-COM-004` | `ACT-COM-018`; `ACT-SRC-002`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-OPS-030`; `ACT-MKT-005`; `ACT-MKT-015` | `ACT-PRF-021`; `ACT-DIG-007`; `ACT-EDU-002`; `ACT-COM-009`; `ACT-MKT-002`; `ACT-MKT-007` |

## 3. Domain assignments

### 3.1 Food and everyday consumer retail

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-FMC-001` | Supermarkets | `BS-008-AP-001` |
| `RET-FMC-002` | Hypermarkets | `BS-008-AP-001` |
| `RET-FMC-003` | Grocery Stores | `BS-008-AP-002` |
| `RET-FMC-004` | Convenience Stores | `BS-008-AP-002` |
| `RET-FMC-005` | Fresh Produce Retail | `BS-008-AP-002` |
| `RET-FMC-006` | Meat and Poultry Retail | `BS-008-AP-002` |
| `RET-FMC-007` | Bakery Retail | `BS-008-AP-002` |
| `RET-FMC-008` | Dairy Retail | `BS-008-AP-002` |
| `RET-FMC-009` | Beverage Retail | `BS-008-AP-002` |
| `RET-FMC-010` | Health Food Retail | `BS-008-AP-002` |
| `RET-FMC-011` | Household Goods Retail | `BS-008-AP-002` |
| `RET-FMC-012` | General Merchandise Retail | `BS-008-AP-002` |

### 3.2 Fashion and personal goods

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-FAS-001` | Apparel Retail | `BS-008-AP-003` |
| `RET-FAS-002` | Footwear Retail | `BS-008-AP-003` |
| `RET-FAS-003` | Textile and Fabric Retail | `BS-008-AP-003` |
| `RET-FAS-004` | Jewellery Retail | `BS-008-AP-003` |
| `RET-FAS-005` | Watches and Accessories | `BS-008-AP-004` |
| `RET-FAS-006` | Luxury Goods Retail | `BS-008-AP-003` |
| `RET-FAS-007` | Cosmetics Retail | `BS-008-AP-003` |
| `RET-FAS-008` | Beauty and Personal Care Retail | `BS-008-AP-003` |
| `RET-FAS-009` | Perfume Retail | `BS-008-AP-003` |
| `RET-FAS-010` | Sportswear Retail | `BS-008-AP-003` |
| `RET-FAS-011` | Children's Products Retail | `BS-008-AP-003` |
| `RET-FAS-012` | Modest Fashion Retail | `BS-008-AP-003` |

### 3.3 Home, electronics and durable goods

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-HOM-001` | Electronics Retail | `BS-008-AP-005` |
| `RET-HOM-002` | Mobile Phone Retail | `BS-008-AP-005` |
| `RET-HOM-003` | Computer and IT Retail | `BS-008-AP-005` |
| `RET-HOM-004` | Home Appliance Retail | `BS-008-AP-005` |
| `RET-HOM-005` | Furniture Retail | `BS-008-AP-005` |
| `RET-HOM-006` | Home Furnishing Retail | `BS-008-AP-005` |
| `RET-HOM-007` | Kitchenware Retail | `BS-008-AP-005` |
| `RET-HOM-008` | Lighting Retail | `BS-008-AP-005` |
| `RET-HOM-009` | Hardware Retail | `BS-008-AP-005` |
| `RET-HOM-010` | Building Materials Retail | `BS-008-AP-005` |
| `RET-HOM-011` | Gardening Retail | `BS-008-AP-005` |
| `RET-HOM-012` | Office Supplies Retail | `BS-008-AP-005` |

### 3.4 Automotive and mobility retail

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-AUT-001` | Vehicle Dealerships | `BS-008-AP-006` |
| `RET-AUT-002` | Used Vehicle Retail | `BS-008-AP-007` |
| `RET-AUT-003` | Motorcycle Retail | `BS-008-AP-007` |
| `RET-AUT-004` | Automotive Parts Retail | `BS-008-AP-007` |
| `RET-AUT-005` | Tyre Retail | `BS-008-AP-007` |
| `RET-AUT-006` | Battery Retail | `BS-008-AP-007` |
| `RET-AUT-007` | Lubricants Retail | `BS-008-AP-007` |
| `RET-AUT-008` | Commercial Vehicle Retail | `BS-008-AP-007` |
| `RET-AUT-009` | Bicycle Retail | `BS-008-AP-007` |
| `RET-AUT-010` | Mobility Equipment Retail | `BS-008-AP-008` |

### 3.5 Health and specialist retail

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-HLT-001` | Pharmacy Retail | `BS-008-AP-009` |
| `RET-HLT-002` | Medical Supply Retail | `BS-008-AP-010` |
| `RET-HLT-003` | Optical Retail | `BS-008-AP-010` |
| `RET-HLT-004` | Dental Supply Retail | `BS-008-AP-010` |
| `RET-HLT-005` | Orthotics and Prosthetics Retail | `BS-008-AP-010` |
| `RET-HLT-006` | Baby and Maternity Retail | `BS-008-AP-010` |
| `RET-HLT-007` | Pet Supply Retail | `BS-008-AP-010` |
| `RET-HLT-008` | Bookstores | `BS-008-AP-010` |
| `RET-HLT-009` | Educational Supply Retail | `BS-008-AP-011` |
| `RET-HLT-010` | Religious Product Retail | `BS-008-AP-010` |
| `RET-HLT-011` | Gift and Floral Retail | `BS-008-AP-010` |

### 3.6 Digital and channel retail

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-ECM-001` | E-Commerce Stores | `BS-008-AP-012` |
| `RET-ECM-002` | Online Marketplaces | `BS-008-AP-013` |
| `RET-ECM-003` | Social Commerce | `BS-008-AP-013` |
| `RET-ECM-004` | Direct-to-Consumer Brands | `BS-008-AP-013` |
| `RET-ECM-005` | Omnichannel Retail | `BS-008-AP-012` |
| `RET-ECM-006` | Subscription Commerce | `BS-008-AP-013` |
| `RET-ECM-007` | Mobile Commerce | `BS-008-AP-013` |
| `RET-ECM-008` | Marketplace Sellers | `BS-008-AP-013` |
| `RET-ECM-009` | Retail Franchises | `BS-008-AP-012` |
| `RET-ECM-010` | Catalogue and Telephone Retail | `BS-008-AP-012` |
| `RET-ECM-011` | Click-and-Collect Retail | `BS-008-AP-012` |

### 3.7 Retail operations and services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `RET-OPS-001` | Point-of-Sale Systems | `BS-008-AP-014` |
| `RET-OPS-002` | Retail Inventory Systems | `BS-008-AP-015` |
| `RET-OPS-003` | E-Commerce Platforms | `BS-008-AP-016` |
| `RET-OPS-004` | Order Management Systems | `BS-008-AP-014` |
| `RET-OPS-005` | Warehouse and Fulfilment for Retail | `BS-008-AP-017` |
| `RET-OPS-006` | Retail CRM and Loyalty | `BS-008-AP-015` |
| `RET-OPS-007` | Merchandising Systems | `BS-008-AP-014` |
| `RET-OPS-008` | Pricing and Promotion Systems | `BS-008-AP-018` |
| `RET-OPS-009` | Retail Analytics | `BS-008-AP-015` |
| `RET-OPS-010` | Store Operations Systems | `BS-008-AP-015` |
| `RET-OPS-011` | Loss Prevention | `BS-008-AP-014` |
| `RET-OPS-012` | Retail Workforce Management | `BS-008-AP-015` |
| `RET-OPS-013` | Retail Procurement | `BS-008-AP-015` |
| `RET-OPS-014` | Returns and Reverse Logistics | `BS-008-AP-014` |
| `RET-OPS-015` | Retail Payment Services | `BS-008-AP-015` |
| `RET-OPS-016` | Retail Marketing Services | `BS-008-AP-019` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
