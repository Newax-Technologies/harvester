# Harvester Travel Domain Keyword Registry

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for the **75** canonical domains in the Travel sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-TRV-AGY-001-V1` | Retail Travel Agencies | retail travel agencies; retail travel agency; retail tourism agencies | `ORG-COMMERCE` | `EX-PHRASE` |
| `KW-TRV-AGY-002-V1` | Corporate Travel Management | corporate travel management; corporate tourism management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-003-V1` | Online Travel Agencies | online travel agencies; online travel agency; online tourism agencies | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-AGY-004-V1` | Business Travel Services | business travel services; business travel service; business tourism services; business travel providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-005-V1` | Ticketing Agencies | ticketing agencies; ticketing agency | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-AGY-006-V1` | Airline Booking Services | airline booking services; airline booking service; airline booking providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-007-V1` | Hotel Booking Services | hotel booking services; hotel booking service; hotel booking providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-008-V1` | Rail Booking Services | rail booking services; rail booking service; rail booking providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-009-V1` | Bus Booking Services | bus booking services; bus booking service; bus booking providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-AGY-010-V1` | Travel Consolidators | travel consolidators; travel consolidator; tourism consolidators | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-AGY-011-V1` | Travel Metasearch | travel metasearch; tourism metasearch | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-AGY-012-V1` | Travel Membership Services | travel membership services; travel membership service; tourism membership services; travel membership providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-TOU-001-V1` | Inbound Tour Operators | inbound tour operators; inbound tour operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-002-V1` | Outbound Tour Operators | outbound tour operators; outbound tour operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-003-V1` | Domestic Tour Operators | domestic tour operators; domestic tour operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-004-V1` | Destination Management Companies | destination management companies; destination management company | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-TOU-005-V1` | City Tours | city tours; city tour | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-006-V1` | Cultural and Heritage Tours | cultural and heritage tours; cultural & heritage tours | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-007-V1` | Adventure Tourism | adventure tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-008-V1` | Eco-Tourism | eco-tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-009-V1` | Medical Tourism | medical tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-010-V1` | Educational Tours | educational tours; educational tour; learning tours | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-011-V1` | Religious Tourism | religious tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-012-V1` | Luxury Travel | luxury travel; luxury tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-013-V1` | Group Travel | group travel; group tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-TOU-014-V1` | Independent Travel Services | independent travel services; independent travel service; independent tourism services; independent travel providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-TOU-015-V1` | Guided Tour Services | guided tour services; guided tour service; guided tour providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-TOU-016-V1` | Excursion and Activity Providers | excursion and activity providers; excursion & activity providers | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-001-V1` | Hajj Operators | hajj operators; hajj operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-002-V1` | Umrah Operators | umrah operators; umrah operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-003-V1` | Pilgrimage Travel Agencies | pilgrimage travel agencies; pilgrimage travel agency; pilgrimage tourism agencies | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-004-V1` | Religious Tour Packages | religious tour packages; religious tour package | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-005-V1` | Pilgrim Accommodation Coordination | pilgrim accommodation coordination | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-006-V1` | Pilgrim Transport Coordination | pilgrim transport coordination | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-007-V1` | Visa and Documentation Support | visa and documentation support; visa & documentation support | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-PIL-008-V1` | Group Leader and Guide Services | group leader and guide services; group leader & guide services; group leader and guide providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-PIL-009-V1` | Pilgrim Welfare Services | pilgrim welfare services; pilgrim welfare service; pilgrim welfare providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-PIL-010-V1` | Religious Travel Platforms | religious travel platforms; religious travel platform; religious tourism platforms | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-MOB-001-V1` | Airlines | airlines; airline | `ORG-GENERIC` | `EX-BROAD` |
| `KW-TRV-MOB-002-V1` | Charter Aviation | charter aviation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-003-V1` | Airport Passenger Services | airport passenger services; airport passenger service; airport passenger providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-MOB-004-V1` | Rail Passenger Services | rail passenger services; rail passenger service; rail passenger providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-MOB-005-V1` | Intercity Bus Services | intercity bus services; intercity bus service; intercity bus providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-MOB-006-V1` | Coach Operators | coach operators; coach operator | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-007-V1` | Car Rental | car rental | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-008-V1` | Chauffeur Services | chauffeur services; chauffeur service; chauffeur providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TRV-MOB-009-V1` | Ride-Hailing | ride-hailing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-010-V1` | Ferry and Passenger Shipping | ferry and passenger shipping; ferry & passenger shipping | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-011-V1` | Cruise Travel | cruise travel; cruise tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-MOB-012-V1` | Tourist Transport | tourist transport | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-001-V1` | Visa Services | visa services; visa service; visa providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TRV-DOC-002-V1` | Passport and Documentation Assistance | passport and documentation assistance; passport & documentation assistance | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-003-V1` | Travel Insurance and Takaful | travel insurance and takaful; travel insurance & takaful; tourism insurance and takaful | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-004-V1` | Foreign Exchange for Travel | foreign exchange for travel; foreign exchange for tourism | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-005-V1` | Travel Health Services | travel health services; travel health service; tourism health services; travel health providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-DOC-006-V1` | Travel Vaccination Services | travel vaccination services; travel vaccination service; tourism vaccination services; travel vaccination providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-DOC-007-V1` | Travel Assistance and Emergency Support | travel assistance and emergency support; travel assistance & emergency support; tourism assistance and emergency support | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-008-V1` | Relocation Services | relocation services; relocation service; relocation providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TRV-DOC-009-V1` | Immigration Support | immigration support | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TRV-DOC-010-V1` | Destination Information Services | destination information services; destination information service; destination information providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TRV-DIG-001-V1` | Reservation Systems | reservation systems; reservation system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-TRV-DIG-002-V1` | Global Distribution Systems | global distribution systems; global distribution system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-003-V1` | Travel Agency Management Systems | travel agency management systems; travel agency management system; tourism agency management systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-004-V1` | Tour Operator Management Systems | tour operator management systems; tour operator management system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-005-V1` | Itinerary Management | itinerary management | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-TRV-DIG-006-V1` | Travel CRM Systems | travel crm systems; travel crm system; tourism crm systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-007-V1` | Fare and Rate Management | fare and rate management; fare & rate management | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-008-V1` | Travel Payment Systems | travel payment systems; travel payment system; tourism payment systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-009-V1` | Travel Inventory Systems | travel inventory systems; travel inventory system; tourism inventory systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-010-V1` | Dynamic Packaging Platforms | dynamic packaging platforms; dynamic packaging platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-011-V1` | Travel Mobile Applications | travel mobile applications; travel mobile application; tourism mobile applications | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-012-V1` | Destination Content Platforms | destination content platforms; destination content platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-013-V1` | Travel Analytics | travel analytics; tourism analytics | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-014-V1` | Loyalty and Rewards Platforms | loyalty and rewards platforms; loyalty & rewards platforms | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TRV-DIG-015-V1` | Travel Customer Support Platforms | travel customer support platforms; travel customer support platform; tourism customer support platforms | `ORG-SOFTWARE` | `EX-PHRASE` |

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
