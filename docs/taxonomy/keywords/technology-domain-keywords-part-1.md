# Harvester Technology Domain Keyword Registry

Part **1 of 2**

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
| `KW-TEC-SFW-001-V1` | Enterprise Software | enterprise software; enterprise application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-002-V1` | Software as a Service | software as a service; application as a service | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-003-V1` | Mobile Applications | mobile applications; mobile application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-004-V1` | Web Applications | web applications; web application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-005-V1` | Business Operating Systems | business operating systems; business operating system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-006-V1` | Customer Relationship Management | customer relationship management; CRM; customer management software | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SFW-007-V1` | Enterprise Resource Planning | enterprise resource planning; ERP; enterprise management software | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SFW-008-V1` | Human Resource Management Systems | human resource management systems; human resource management system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-009-V1` | Accounting and Finance Software | accounting and finance software; accounting & finance software; accounting and finance application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-010-V1` | Document Management Systems | document management systems; document management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-TEC-SFW-011-V1` | Workflow and Automation Platforms | workflow and automation platforms; workflow & automation platforms | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-012-V1` | Project Management Software | project management software; project management application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-013-V1` | Collaboration Software | collaboration software; collaboration application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-014-V1` | Vertical Industry Software | vertical industry software; vertical industry application | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SFW-015-V1` | Developer Tools | developer tools; developer tool | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SFW-016-V1` | Low-Code and No-Code Platforms | low-code and no-code platforms; low-code & no-code platforms | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-001-V1` | Business Intelligence | business intelligence | `ORG-GENERIC` | `EX-AI` |
| `KW-TEC-DAT-002-V1` | Data Warehousing | data warehousing; data warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-003-V1` | Data Engineering | data engineering | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-004-V1` | Data Integration | data integration | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-005-V1` | Master Data Management | master data management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-DAT-006-V1` | Data Governance | data governance | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-007-V1` | Analytics Platforms | analytics platforms; analytics platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-008-V1` | Artificial Intelligence Systems | artificial intelligence systems; artificial intelligence system; AI; machine intelligence | `ORG-SOFTWARE` | `EX-AI` |
| `KW-TEC-DAT-009-V1` | Machine Learning Platforms | machine learning platforms; machine learning platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-010-V1` | Natural Language Processing | natural language processing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-011-V1` | Computer Vision | computer vision | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-012-V1` | Decision Support Systems | decision support systems; decision support system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-013-V1` | Search and Knowledge Systems | search and knowledge systems; search & knowledge systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-014-V1` | Geospatial Analytics | geospatial analytics | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-DAT-015-V1` | Data Quality Tools | data quality tools; data quality tool | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-DAT-016-V1` | Database Products | database products; database product | `ORG-PRODUCT` | `EX-BROAD` |
| `KW-TEC-CLD-001-V1` | Cloud Computing | cloud computing | `ORG-SOFTWARE` | `EX-CLOUD` |
| `KW-TEC-CLD-002-V1` | Cloud Platforms | cloud platforms; cloud platform | `ORG-SOFTWARE` | `EX-CLOUD` |
| `KW-TEC-CLD-003-V1` | Managed Cloud Services | managed cloud services; managed cloud service; managed cloud providers | `ORG-SOFTWARE` | `EX-CLOUD` |
| `KW-TEC-CLD-004-V1` | Web Hosting | web hosting | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-CLD-005-V1` | Application Hosting | application hosting | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-CLD-006-V1` | Data Centres | data centres; data centers; data centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-TEC-CLD-007-V1` | Colocation Services | colocation services; colocation service; colocation providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TEC-CLD-008-V1` | Content Delivery Networks | content delivery networks; content delivery network | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-CLD-009-V1` | Backup and Recovery | backup and recovery; backup & recovery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-CLD-010-V1` | Disaster Recovery | disaster recovery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-CLD-011-V1` | Infrastructure as a Service | infrastructure as a service | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-CLD-012-V1` | Platform as a Service | platform as a service | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-CLD-013-V1` | Server Management | server management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TEC-CLD-014-V1` | Virtualization | virtualization | `ORG-GENERIC` | `EX-BROAD` |
| `KW-TEC-CLD-015-V1` | Container Platforms | container platforms; container platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-CLD-016-V1` | Edge Computing | edge computing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-CLD-017-V1` | Domain and DNS Services | domain and dns services; domain & dns services; domain and dns providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SEC-001-V1` | Managed Security Services | managed security services; managed security service; managed security providers | `ORG-SERVICE` | `EX-SECURITY` |
| `KW-TEC-SEC-002-V1` | Security Operations Centres | security operations centres; security operations centers; security operations centre | `ORG-INSTITUTION` | `EX-SECURITY` |
| `KW-TEC-SEC-003-V1` | Identity and Access Management | identity and access management; identity & access management | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-SEC-004-V1` | Endpoint Security | endpoint security | `ORG-GENERIC` | `EX-SECURITY` |
| `KW-TEC-SEC-005-V1` | Network Security | network security | `ORG-GENERIC` | `EX-SECURITY` |
| `KW-TEC-SEC-006-V1` | Cloud Security | cloud security | `ORG-SOFTWARE` | `EX-CLOUD` |
| `KW-TEC-SEC-007-V1` | Application Security | application security | `ORG-SOFTWARE` | `EX-SECURITY` |
| `KW-TEC-SEC-008-V1` | Data Security | data security | `ORG-GENERIC` | `EX-SECURITY` |
| `KW-TEC-SEC-009-V1` | Email Security | email security | `ORG-GENERIC` | `EX-SECURITY` |
| `KW-TEC-SEC-010-V1` | Security Information and Event Management | security information and event management; security information & event management | `ORG-SERVICE` | `EX-SECURITY` |
| `KW-TEC-SEC-011-V1` | Vulnerability Management | vulnerability management | `ORG-SERVICE` | `EX-BROAD` |
| `KW-TEC-SEC-012-V1` | Penetration Testing | penetration testing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SEC-013-V1` | Governance, Risk and Compliance | governance, risk and compliance; governance, risk & compliance; GRC; governance risk compliance | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SEC-014-V1` | Digital Identity | digital identity | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-SEC-015-V1` | Electronic Signatures | electronic signatures; electronic signature | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-SEC-016-V1` | Fraud and Threat Intelligence | fraud and threat intelligence; fraud & threat intelligence | `ORG-GENERIC` | `EX-AI` |
| `KW-TEC-TEL-001-V1` | Mobile Network Operators | mobile network operators; mobile network operator | `ORG-GENERIC` | `EX-NETWORK` |
| `KW-TEC-TEL-002-V1` | Fixed-Line Telecommunications | fixed-line telecommunications; fixed-line telecommunication | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-003-V1` | Internet Service Providers | internet service providers; internet service provider | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-TEC-TEL-004-V1` | Fibre Networks | fibre networks; fibre network | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-005-V1` | Wireless Internet | wireless internet | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-006-V1` | Satellite Communications | satellite communications; satellite communication | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-007-V1` | Unified Communications | unified communications; unified communication | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-008-V1` | Voice over IP | voice over ip | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-009-V1` | Contact Centre Platforms | contact centre platforms; contact center platforms; contact centre platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-TEL-010-V1` | Messaging Platforms | messaging platforms; messaging platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-TEC-TEL-011-V1` | Network Infrastructure | network infrastructure | `ORG-GENERIC` | `EX-NETWORK` |
| `KW-TEC-TEL-012-V1` | Telecommunications Towers | telecommunications towers; telecommunications tower | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-013-V1` | Internet Exchange Points | internet exchange points; internet exchange point | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-TEC-TEL-014-V1` | Managed Network Services | managed network services; managed network service; managed network providers | `ORG-SERVICE` | `EX-NETWORK` |
| `KW-TEC-TEL-015-V1` | IoT Connectivity | iot connectivity | `ORG-GENERIC` | `EX-PHRASE` |

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
