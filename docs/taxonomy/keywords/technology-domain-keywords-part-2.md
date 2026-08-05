# Harvester Technology Domain Keyword Registry

Part **2 of 2**

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for a portion of the **127** canonical domains in the Technology sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-TEC-HWD-001-V1` | Computer Hardware | computer hardware | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-HWD-002-V1` | Servers and Storage | servers and storage; servers & storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-HWD-003-V1` | Networking Equipment | networking equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-TEC-HWD-004-V1` | Telecommunications Equipment | telecommunications equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-TEC-HWD-005-V1` | Point-of-Sale Hardware | point-of-sale hardware; point of sale hardware; POS; point of sale | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-HWD-006-V1` | Barcode and RFID Equipment | barcode and rfid equipment; barcode & rfid equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-TEC-HWD-007-V1` | Sensors and Telemetry | sensors and telemetry; sensors & telemetry | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-HWD-008-V1` | Internet of Things Platforms | internet of things platforms; internet of things platform; IoT; connected devices | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-HWD-009-V1` | Smart Building Systems | smart building systems; smart building system | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-TEC-HWD-010-V1` | Industrial Automation | industrial automation | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-HWD-011-V1` | Embedded Systems | embedded systems; embedded system | `ORG-PRODUCT` | `EX-BROAD` |
| `KW-TEC-HWD-012-V1` | Robotics | robotics | `ORG-GENERIC` | `EX-BROAD` |
| `KW-TEC-HWD-013-V1` | Electronic Devices | electronic devices; electronic device | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-TEC-HWD-014-V1` | Digital Signage | digital signage | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-HWD-015-V1` | Access-Control Hardware | access-control hardware | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-001-V1` | Software Development Services | software development services; software development service; application development services; software development providers | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SRV-002-V1` | Systems Integration | systems integration | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TEC-SRV-003-V1` | IT Consulting | it consulting | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SRV-004-V1` | Managed IT Services | managed it services; managed it service; managed it providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SRV-005-V1` | Technical Support | technical support | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-006-V1` | IT Outsourcing | it outsourcing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-007-V1` | Cloud Migration | cloud migration | `ORG-SOFTWARE` | `EX-CLOUD` |
| `KW-TEC-SRV-008-V1` | Application Modernization | application modernization | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SRV-009-V1` | Data Migration | data migration | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-010-V1` | Enterprise Architecture | enterprise architecture | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-011-V1` | Quality Assurance and Testing | quality assurance and testing; quality assurance & testing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-012-V1` | DevOps Services | devops services; devops service; devops providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TEC-SRV-013-V1` | User Experience Design | user experience design | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-014-V1` | Technology Training | technology training; tech training | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SRV-015-V1` | IT Procurement | it procurement | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SRV-016-V1` | Field Technology Services | field technology services; field technology service; field tech services; field technology providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-COM-001-V1` | E-Commerce Platforms | e-commerce platforms; ecommerce platforms; e-commerce platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-COM-002-V1` | Payment Technology | payment technology; payment tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-003-V1` | Marketplace Platforms | marketplace platforms; marketplace platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-COM-004-V1` | Marketing Technology | marketing technology; marketing tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-005-V1` | Advertising Technology | advertising technology; advertising tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-006-V1` | Customer Engagement Platforms | customer engagement platforms; customer engagement platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-COM-007-V1` | Social Media Management | social media management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-COM-008-V1` | Content Management Systems | content management systems; content management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-TEC-COM-009-V1` | Digital Experience Platforms | digital experience platforms; digital experience platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-COM-010-V1` | Learning Technology | learning technology; learning tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-011-V1` | Health Technology | health technology; health tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-012-V1` | Legal Technology | legal technology; legal tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-013-V1` | Property Technology | property technology; property tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-014-V1` | Financial Technology | financial technology; financial tech | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-COM-015-V1` | Government Technology | government technology; government tech; public sector technology | `ORG-PUBLIC` | `EX-PHRASE` |
| `KW-TEC-COM-016-V1` | Travel Technology | travel technology; tourism technology; travel tech | `ORG-GENERIC` | `EX-PHRASE` |

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
