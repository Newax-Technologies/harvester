# Harvester Retail Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-008 Retail`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Retail
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

This registry contains **84 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `RET-FMC` | Food and everyday consumer retail | 12 |
| `RET-FAS` | Fashion and personal goods | 12 |
| `RET-HOM` | Home, electronics and durable goods | 12 |
| `RET-AUT` | Automotive and mobility retail | 10 |
| `RET-HLT` | Health and specialist retail | 11 |
| `RET-ECM` | Digital and channel retail | 11 |
| `RET-OPS` | Retail operations and services | 16 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Food and everyday consumer retail

| Code | Domain |
| --- | --- |
| `RET-FMC-001` | Supermarkets |
| `RET-FMC-002` | Hypermarkets |
| `RET-FMC-003` | Grocery Stores |
| `RET-FMC-004` | Convenience Stores |
| `RET-FMC-005` | Fresh Produce Retail |
| `RET-FMC-006` | Meat and Poultry Retail |
| `RET-FMC-007` | Bakery Retail |
| `RET-FMC-008` | Dairy Retail |
| `RET-FMC-009` | Beverage Retail |
| `RET-FMC-010` | Health Food Retail |
| `RET-FMC-011` | Household Goods Retail |
| `RET-FMC-012` | General Merchandise Retail |

### 4.2 Fashion and personal goods

| Code | Domain |
| --- | --- |
| `RET-FAS-001` | Apparel Retail |
| `RET-FAS-002` | Footwear Retail |
| `RET-FAS-003` | Textile and Fabric Retail |
| `RET-FAS-004` | Jewellery Retail |
| `RET-FAS-005` | Watches and Accessories |
| `RET-FAS-006` | Luxury Goods Retail |
| `RET-FAS-007` | Cosmetics Retail |
| `RET-FAS-008` | Beauty and Personal Care Retail |
| `RET-FAS-009` | Perfume Retail |
| `RET-FAS-010` | Sportswear Retail |
| `RET-FAS-011` | Children's Products Retail |
| `RET-FAS-012` | Modest Fashion Retail |

### 4.3 Home, electronics and durable goods

| Code | Domain |
| --- | --- |
| `RET-HOM-001` | Electronics Retail |
| `RET-HOM-002` | Mobile Phone Retail |
| `RET-HOM-003` | Computer and IT Retail |
| `RET-HOM-004` | Home Appliance Retail |
| `RET-HOM-005` | Furniture Retail |
| `RET-HOM-006` | Home Furnishing Retail |
| `RET-HOM-007` | Kitchenware Retail |
| `RET-HOM-008` | Lighting Retail |
| `RET-HOM-009` | Hardware Retail |
| `RET-HOM-010` | Building Materials Retail |
| `RET-HOM-011` | Gardening Retail |
| `RET-HOM-012` | Office Supplies Retail |

### 4.4 Automotive and mobility retail

| Code | Domain |
| --- | --- |
| `RET-AUT-001` | Vehicle Dealerships |
| `RET-AUT-002` | Used Vehicle Retail |
| `RET-AUT-003` | Motorcycle Retail |
| `RET-AUT-004` | Automotive Parts Retail |
| `RET-AUT-005` | Tyre Retail |
| `RET-AUT-006` | Battery Retail |
| `RET-AUT-007` | Lubricants Retail |
| `RET-AUT-008` | Commercial Vehicle Retail |
| `RET-AUT-009` | Bicycle Retail |
| `RET-AUT-010` | Mobility Equipment Retail |

### 4.5 Health and specialist retail

| Code | Domain |
| --- | --- |
| `RET-HLT-001` | Pharmacy Retail |
| `RET-HLT-002` | Medical Supply Retail |
| `RET-HLT-003` | Optical Retail |
| `RET-HLT-004` | Dental Supply Retail |
| `RET-HLT-005` | Orthotics and Prosthetics Retail |
| `RET-HLT-006` | Baby and Maternity Retail |
| `RET-HLT-007` | Pet Supply Retail |
| `RET-HLT-008` | Bookstores |
| `RET-HLT-009` | Educational Supply Retail |
| `RET-HLT-010` | Religious Product Retail |
| `RET-HLT-011` | Gift and Floral Retail |

### 4.6 Digital and channel retail

| Code | Domain |
| --- | --- |
| `RET-ECM-001` | E-Commerce Stores |
| `RET-ECM-002` | Online Marketplaces |
| `RET-ECM-003` | Social Commerce |
| `RET-ECM-004` | Direct-to-Consumer Brands |
| `RET-ECM-005` | Omnichannel Retail |
| `RET-ECM-006` | Subscription Commerce |
| `RET-ECM-007` | Mobile Commerce |
| `RET-ECM-008` | Marketplace Sellers |
| `RET-ECM-009` | Retail Franchises |
| `RET-ECM-010` | Catalogue and Telephone Retail |
| `RET-ECM-011` | Click-and-Collect Retail |

### 4.7 Retail operations and services

| Code | Domain |
| --- | --- |
| `RET-OPS-001` | Point-of-Sale Systems |
| `RET-OPS-002` | Retail Inventory Systems |
| `RET-OPS-003` | E-Commerce Platforms |
| `RET-OPS-004` | Order Management Systems |
| `RET-OPS-005` | Warehouse and Fulfilment for Retail |
| `RET-OPS-006` | Retail CRM and Loyalty |
| `RET-OPS-007` | Merchandising Systems |
| `RET-OPS-008` | Pricing and Promotion Systems |
| `RET-OPS-009` | Retail Analytics |
| `RET-OPS-010` | Store Operations Systems |
| `RET-OPS-011` | Loss Prevention |
| `RET-OPS-012` | Retail Workforce Management |
| `RET-OPS-013` | Retail Procurement |
| `RET-OPS-014` | Returns and Reverse Logistics |
| `RET-OPS-015` | Retail Payment Services |
| `RET-OPS-016` | Retail Marketing Services |

## 5. First-release presentation shortlist

Supermarkets, Grocery Stores, General Merchandise Retail, Apparel Retail, Footwear Retail, Jewellery and Luxury Retail, Cosmetics and Beauty Retail, Electronics Retail, Mobile Phone Retail, Computer and IT Retail, Home Appliance Retail, Furniture Retail, Hardware Retail, Vehicle Dealerships, Automotive Parts Retail, Pharmacy Retail, Medical Supply Retail, Bookstores, Gift and Floral Retail, E-Commerce Stores, Online Marketplaces, Social Commerce, Direct-to-Consumer Brands, Omnichannel Retail, Retail Franchises, Point-of-Sale Systems, Retail Inventory Systems, E-Commerce Platforms, Order Management Systems, Retail CRM and Loyalty, Merchandising Systems, Pricing and Promotion Systems, Retail Analytics, Store Operations Systems, Returns and Reverse Logistics.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Physical retail:** Buying, Merchandising, Selling, Promoting, Stocking, Returning
- **E-commerce:** Listing, Selling online, Processing orders, Fulfilling, Delivering, Managing returns
- **Automotive retail:** Importing, Displaying, Financing, Selling, Servicing
- **Retail technology:** Developing, Licensing, Implementing, Integrating, Supporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Pharmacy retail | Healthcare | Selling; dispensing; inventory management |
| Building materials retail | Construction | Warehousing; selling; delivering |
| E-commerce stores | Technology; Logistics | Publishing; selling; fulfilling |
| Vehicle dealerships | Finance; Logistics | Selling; financing; delivering |

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

- The shortlist and all 84 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
