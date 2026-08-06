# Harvester Real Estate Domain Keyword Registry

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for the **88** canonical domains in the Real Estate sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-REA-RES-001-V1` | Single-Family Housing | single-family housing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-002-V1` | Apartments and Flats | apartments and flats; apartments & flats | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-003-V1` | Condominiums | condominiums; condominium | `ORG-GENERIC` | `EX-BROAD` |
| `KW-REA-RES-004-V1` | Gated Communities | gated communities; gated community | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-005-V1` | Housing Societies | housing societies; housing society | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-006-V1` | Affordable Housing | affordable housing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-007-V1` | Luxury Residential Property | luxury residential property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-008-V1` | Student Housing | student housing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-009-V1` | Senior Living | senior living | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-010-V1` | Serviced Residences | serviced residences; serviced residence | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-011-V1` | Vacation Homes | vacation homes; vacation home | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-RES-012-V1` | Mixed Residential Communities | mixed residential communities; mixed residential community | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-001-V1` | Office Buildings | office buildings; office building | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-002-V1` | Retail Property | retail property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-003-V1` | Shopping Centres and Malls | shopping centres and malls; shopping centres & malls; shopping centers and malls | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-REA-COM-004-V1` | Hospitality Property | hospitality property; accommodation property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-005-V1` | Healthcare Property | healthcare property; health care property; medical property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-006-V1` | Education Property | education property; learning property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-007-V1` | Warehouses and Logistics Property | warehouses and logistics property; warehouses & logistics property; warehouses and freight property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-008-V1` | Data Centre Property | data centre property; data center property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-009-V1` | Co-Working Spaces | co-working spaces; co-working space | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-010-V1` | Business Parks | business parks; business park | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-011-V1` | Industrial Estates | industrial estates; industrial estate | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-COM-012-V1` | Special Economic Zones | special economic zones; special economic zone | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-001-V1` | Industrial Property | industrial property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-002-V1` | Factories and Production Sites | factories and production sites; factories & production sites | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-003-V1` | Agricultural Land | agricultural land | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-004-V1` | Development Land | development land | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-005-V1` | Plots and Subdivisions | plots and subdivisions; plots & subdivisions | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-006-V1` | Mining and Resource Land | mining and resource land; mining & resource land | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-007-V1` | Storage Yards | storage yards; storage yard | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-008-V1` | Cold-Storage Property | cold-storage property | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-009-V1` | Utility and Energy Sites | utility and energy sites; utility & energy sites; utility and power sites | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-IND-010-V1` | Telecommunications Sites | telecommunications sites; telecommunications site | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-001-V1` | Residential Development | residential development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-002-V1` | Commercial Development | commercial development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-003-V1` | Industrial Development | industrial development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-004-V1` | Mixed-Use Development | mixed-use development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-005-V1` | Land Development | land development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-006-V1` | Property Investment | property investment | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-007-V1` | Real Estate Funds | real estate funds; real estate fund; property funds | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-008-V1` | Real Estate Investment Trusts | real estate investment trusts; real estate investment trust; property investment trusts | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-009-V1` | Joint-Venture Development | joint-venture development | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-010-V1` | Urban Redevelopment | urban redevelopment | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DEV-011-V1` | Public-Private Property Development | public-private property development | `ORG-PUBLIC` | `EX-PHRASE` |
| `KW-REA-DEV-012-V1` | Master-Planned Communities | master-planned communities; master-planned community | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-001-V1` | Real Estate Brokerage | real estate brokerage; property brokerage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-002-V1` | Property Sales | property sales; property sale | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-003-V1` | Property Leasing | property leasing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-004-V1` | Tenant Representation | tenant representation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-005-V1` | Buyer Representation | buyer representation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-006-V1` | Property Valuation | property valuation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-007-V1` | Property Appraisal | property appraisal | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-008-V1` | Real Estate Advisory | real estate advisory; property advisory | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-009-V1` | Investment Advisory | investment advisory | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-REA-TRN-010-V1` | Market Research | market research | `ORG-SERVICE` | `EX-MARKET` |
| `KW-REA-TRN-011-V1` | Title and Ownership Services | title and ownership services; title & ownership services; title and ownership providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-REA-TRN-012-V1` | Property Auction Services | property auction services; property auction service; property auction providers | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-013-V1` | Mortgage and Financing Brokerage | mortgage and financing brokerage; mortgage & financing brokerage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-TRN-014-V1` | Real Estate Legal Support | real estate legal support; property legal support | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-MGT-001-V1` | Property Management | property management | `ORG-GENERIC` | `EX-BROAD` |
| `KW-REA-MGT-002-V1` | Community and Society Management | community and society management; community & society management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-REA-MGT-003-V1` | Tenant Management | tenant management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-REA-MGT-004-V1` | Lease Administration | lease administration | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-REA-MGT-005-V1` | Facilities Coordination | facilities coordination | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-MGT-006-V1` | Maintenance Management | maintenance management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-REA-MGT-007-V1` | Service-Charge Management | service-charge management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-REA-MGT-008-V1` | Rent Collection | rent collection | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-MGT-009-V1` | Owner and Investor Portals | owner and investor portals; owner & investor portals | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-MGT-010-V1` | Tenant Portals | tenant portals; tenant portal | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-MGT-011-V1` | Visitor Management | visitor management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-REA-MGT-012-V1` | Parking Management | parking management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-REA-MGT-013-V1` | Complaint and Work-Order Management | complaint and work-order management; complaint & work-order management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-REA-MGT-014-V1` | Utility Billing | utility billing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-MGT-015-V1` | Property Inspection | property inspection | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-REA-DIG-001-V1` | Property Listing Platforms | property listing platforms; property listing platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-002-V1` | Real Estate Marketplaces | real estate marketplaces; real estate marketplace; property marketplaces | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-003-V1` | Brokerage CRM Systems | brokerage crm systems; brokerage crm system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-004-V1` | Property Management Systems | property management systems; property management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-REA-DIG-005-V1` | Lease Management Systems | lease management systems; lease management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-REA-DIG-006-V1` | Community Management Systems | community management systems; community management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-REA-DIG-007-V1` | Digital Property Portals | digital property portals; digital property portal | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-008-V1` | Virtual Tour Platforms | virtual tour platforms; virtual tour platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-009-V1` | Property Analytics | property analytics | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-010-V1` | Building Information Platforms | building information platforms; building information platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-011-V1` | Digital Title and Registry Systems | digital title and registry systems; digital title & registry systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-012-V1` | Real Estate Document Management | real estate document management; property document management | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-REA-DIG-013-V1` | Smart Property Systems | smart property systems; smart property system | `ORG-SOFTWARE` | `EX-PHRASE` |

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
