# Harvester Real Estate Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-004 Real Estate`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Real Estate
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

This registry contains **88 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `REA-RES` | Residential property | 12 |
| `REA-COM` | Commercial and institutional property | 12 |
| `REA-IND` | Industrial and land assets | 10 |
| `REA-DEV` | Property development and investment | 12 |
| `REA-TRN` | Property transactions and advisory | 14 |
| `REA-MGT` | Property and community operations | 15 |
| `REA-DIG` | Property technology and data | 13 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Residential property

| Code | Domain |
| --- | --- |
| `REA-RES-001` | Single-Family Housing |
| `REA-RES-002` | Apartments and Flats |
| `REA-RES-003` | Condominiums |
| `REA-RES-004` | Gated Communities |
| `REA-RES-005` | Housing Societies |
| `REA-RES-006` | Affordable Housing |
| `REA-RES-007` | Luxury Residential Property |
| `REA-RES-008` | Student Housing |
| `REA-RES-009` | Senior Living |
| `REA-RES-010` | Serviced Residences |
| `REA-RES-011` | Vacation Homes |
| `REA-RES-012` | Mixed Residential Communities |

### 4.2 Commercial and institutional property

| Code | Domain |
| --- | --- |
| `REA-COM-001` | Office Buildings |
| `REA-COM-002` | Retail Property |
| `REA-COM-003` | Shopping Centres and Malls |
| `REA-COM-004` | Hospitality Property |
| `REA-COM-005` | Healthcare Property |
| `REA-COM-006` | Education Property |
| `REA-COM-007` | Warehouses and Logistics Property |
| `REA-COM-008` | Data Centre Property |
| `REA-COM-009` | Co-Working Spaces |
| `REA-COM-010` | Business Parks |
| `REA-COM-011` | Industrial Estates |
| `REA-COM-012` | Special Economic Zones |

### 4.3 Industrial and land assets

| Code | Domain |
| --- | --- |
| `REA-IND-001` | Industrial Property |
| `REA-IND-002` | Factories and Production Sites |
| `REA-IND-003` | Agricultural Land |
| `REA-IND-004` | Development Land |
| `REA-IND-005` | Plots and Subdivisions |
| `REA-IND-006` | Mining and Resource Land |
| `REA-IND-007` | Storage Yards |
| `REA-IND-008` | Cold-Storage Property |
| `REA-IND-009` | Utility and Energy Sites |
| `REA-IND-010` | Telecommunications Sites |

### 4.4 Property development and investment

| Code | Domain |
| --- | --- |
| `REA-DEV-001` | Residential Development |
| `REA-DEV-002` | Commercial Development |
| `REA-DEV-003` | Industrial Development |
| `REA-DEV-004` | Mixed-Use Development |
| `REA-DEV-005` | Land Development |
| `REA-DEV-006` | Property Investment |
| `REA-DEV-007` | Real Estate Funds |
| `REA-DEV-008` | Real Estate Investment Trusts |
| `REA-DEV-009` | Joint-Venture Development |
| `REA-DEV-010` | Urban Redevelopment |
| `REA-DEV-011` | Public-Private Property Development |
| `REA-DEV-012` | Master-Planned Communities |

### 4.5 Property transactions and advisory

| Code | Domain |
| --- | --- |
| `REA-TRN-001` | Real Estate Brokerage |
| `REA-TRN-002` | Property Sales |
| `REA-TRN-003` | Property Leasing |
| `REA-TRN-004` | Tenant Representation |
| `REA-TRN-005` | Buyer Representation |
| `REA-TRN-006` | Property Valuation |
| `REA-TRN-007` | Property Appraisal |
| `REA-TRN-008` | Real Estate Advisory |
| `REA-TRN-009` | Investment Advisory |
| `REA-TRN-010` | Market Research |
| `REA-TRN-011` | Title and Ownership Services |
| `REA-TRN-012` | Property Auction Services |
| `REA-TRN-013` | Mortgage and Financing Brokerage |
| `REA-TRN-014` | Real Estate Legal Support |

### 4.6 Property and community operations

| Code | Domain |
| --- | --- |
| `REA-MGT-001` | Property Management |
| `REA-MGT-002` | Community and Society Management |
| `REA-MGT-003` | Tenant Management |
| `REA-MGT-004` | Lease Administration |
| `REA-MGT-005` | Facilities Coordination |
| `REA-MGT-006` | Maintenance Management |
| `REA-MGT-007` | Service-Charge Management |
| `REA-MGT-008` | Rent Collection |
| `REA-MGT-009` | Owner and Investor Portals |
| `REA-MGT-010` | Tenant Portals |
| `REA-MGT-011` | Visitor Management |
| `REA-MGT-012` | Parking Management |
| `REA-MGT-013` | Complaint and Work-Order Management |
| `REA-MGT-014` | Utility Billing |
| `REA-MGT-015` | Property Inspection |

### 4.7 Property technology and data

| Code | Domain |
| --- | --- |
| `REA-DIG-001` | Property Listing Platforms |
| `REA-DIG-002` | Real Estate Marketplaces |
| `REA-DIG-003` | Brokerage CRM Systems |
| `REA-DIG-004` | Property Management Systems |
| `REA-DIG-005` | Lease Management Systems |
| `REA-DIG-006` | Community Management Systems |
| `REA-DIG-007` | Digital Property Portals |
| `REA-DIG-008` | Virtual Tour Platforms |
| `REA-DIG-009` | Property Analytics |
| `REA-DIG-010` | Building Information Platforms |
| `REA-DIG-011` | Digital Title and Registry Systems |
| `REA-DIG-012` | Real Estate Document Management |
| `REA-DIG-013` | Smart Property Systems |

## 5. First-release presentation shortlist

Residential Property, Commercial Property, Industrial Property, Housing Societies, Gated Communities, Apartments and Flats, Office Buildings, Retail Property, Warehouses and Logistics Property, Real Estate Development, Land Development, Mixed-Use Development, Property Investment, Real Estate Brokerage, Property Sales, Property Leasing, Property Valuation, Property Management, Community Management, Tenant Management, Lease Administration, Rent Collection, Maintenance Management, Owner and Investor Portals, Tenant Portals, Property Listing Platforms, Real Estate Marketplaces, Brokerage CRM Systems, Property Management Systems, Lease Management Systems, Property Analytics, Smart Property Systems.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Residential property:** Developing, Selling, Leasing, Managing, Maintaining
- **Real estate brokerage:** Listing, Marketing, Selling, Leasing, Advising
- **Property management:** Onboarding tenants, Collecting rent, Managing maintenance, Reporting, Inspecting
- **Property platforms:** Publishing listings, Matching buyers, Managing leads, Processing bookings, Integrating payments

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Housing societies | Construction; Government | Developing; regulating; managing |
| Property management | Hospitality; Construction | Operating; maintaining; servicing |
| Warehouse property | Logistics | Leasing; operating; managing |
| Smart property systems | Technology; Energy | Monitoring; integrating; automating |

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

- The shortlist and all 88 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
