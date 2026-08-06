# Harvester Technology Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **127** canonical domains in `BS-014 Technology` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-014-AP-001` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-COM-011`; `ACT-DIG-002`; `ACT-OPS-017`; `ACT-OPS-004` | `ACT-OPS-005`; `ACT-OPS-007`; `ACT-COM-026`; `ACT-DIG-005` | `ACT-COM-010`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-DIG-007` |
| `BS-014-AP-002` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-COM-011`; `ACT-DIG-002`; `ACT-OPS-017` | `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-007`; `ACT-COM-026`; `ACT-DIG-005` | `ACT-COM-010`; `ACT-PRF-022`; `ACT-EDU-002` |
| `BS-014-AP-003` | `ACT-RND-007`; `ACT-DIG-005`; `ACT-DIG-007`; `ACT-RND-019`; `ACT-DIG-008` | `ACT-DIG-022`; `ACT-DIG-023`; `ACT-DIG-024`; `ACT-DIG-025`; `ACT-PRF-001` | `ACT-DIG-002`; `ACT-DIG-013`; `ACT-RND-001` |
| `BS-014-AP-004` | `ACT-RND-007`; `ACT-DIG-005`; `ACT-DIG-007`; `ACT-RND-019`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-DIG-022`; `ACT-DIG-023`; `ACT-DIG-024`; `ACT-DIG-025`; `ACT-PRF-001`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-DIG-002`; `ACT-DIG-013`; `ACT-RND-001`; `ACT-EDU-002`; `ACT-LEG-013` |
| `BS-014-AP-005` | `ACT-RND-007`; `ACT-DIG-005`; `ACT-DIG-007`; `ACT-RND-019`; `ACT-DIG-008`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-022`; `ACT-DIG-023`; `ACT-DIG-024`; `ACT-DIG-025`; `ACT-PRF-001`; `ACT-OPS-005`; `ACT-DIG-002`; `ACT-OPS-017` | `ACT-DIG-013`; `ACT-RND-001`; `ACT-OPS-007` |
| `BS-014-AP-006` | `ACT-DIG-002`; `ACT-DIG-003`; `ACT-DIG-012`; `ACT-OPS-011`; `ACT-DIG-026` | `ACT-DIG-020`; `ACT-DIG-010`; `ACT-DIG-006`; `ACT-OPS-017`; `ACT-PRF-022` | `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-031` |
| `BS-014-AP-007` | `ACT-DIG-002`; `ACT-DIG-003`; `ACT-DIG-012`; `ACT-OPS-011`; `ACT-DIG-026`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-020`; `ACT-DIG-010`; `ACT-DIG-006`; `ACT-OPS-017`; `ACT-PRF-022`; `ACT-OPS-005` | `ACT-OPS-031`; `ACT-OPS-007`; `ACT-DIG-007` |
| `BS-014-AP-008` | `ACT-DIG-002`; `ACT-DIG-003`; `ACT-DIG-012`; `ACT-OPS-011`; `ACT-DIG-026`; `ACT-DIG-017`; `ACT-OPS-010` | `ACT-DIG-020`; `ACT-DIG-010`; `ACT-DIG-006`; `ACT-OPS-017`; `ACT-PRF-022`; `ACT-OPS-001`; `ACT-OPS-012` | `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-031`; `ACT-OPS-018`; `ACT-SRC-014` |
| `BS-014-AP-009` | `ACT-DIG-002`; `ACT-DIG-003`; `ACT-DIG-012`; `ACT-OPS-011`; `ACT-DIG-026`; `ACT-END-001`; `ACT-END-002` | `ACT-DIG-020`; `ACT-DIG-010`; `ACT-DIG-006`; `ACT-OPS-017`; `ACT-PRF-022`; `ACT-END-008`; `ACT-END-012` | `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-031`; `ACT-END-004`; `ACT-END-005` |
| `BS-014-AP-010` | `ACT-DIG-010`; `ACT-QLT-013`; `ACT-QLT-005`; `ACT-QLT-022`; `ACT-OPS-017` | `ACT-DIG-011`; `ACT-QLT-010`; `ACT-QLT-012`; `ACT-PRF-022`; `ACT-EDU-002` | `ACT-RND-018`; `ACT-OPS-011`; `ACT-OPS-034` |
| `BS-014-AP-011` | `ACT-DIG-010`; `ACT-QLT-013`; `ACT-QLT-005`; `ACT-QLT-022`; `ACT-OPS-017`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-011`; `ACT-QLT-010`; `ACT-QLT-012`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-OPS-005`; `ACT-DIG-002` | `ACT-OPS-011`; `ACT-OPS-034`; `ACT-OPS-007`; `ACT-DIG-007` |
| `BS-014-AP-012` | `ACT-DIG-010`; `ACT-QLT-013`; `ACT-QLT-005`; `ACT-QLT-022`; `ACT-OPS-017`; `ACT-RND-021`; `ACT-QLT-001` | `ACT-DIG-011`; `ACT-QLT-010`; `ACT-QLT-012`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-003`; `ACT-QLT-004`; `ACT-DIG-008` | `ACT-RND-018`; `ACT-OPS-011`; `ACT-OPS-034`; `ACT-QLT-006`; `ACT-QLT-007` |
| `BS-014-AP-013` | `ACT-DIG-010`; `ACT-QLT-013`; `ACT-QLT-005`; `ACT-QLT-022`; `ACT-OPS-017`; `ACT-QLT-010` | `ACT-DIG-011`; `ACT-QLT-012`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-RND-018`; `ACT-OPS-011`; `ACT-OPS-034`; `ACT-LEG-013` |
| `BS-014-AP-014` | `ACT-DIG-017`; `ACT-OPS-010`; `ACT-OPS-001`; `ACT-OPS-011`; `ACT-OPS-012` | `ACT-DIG-020`; `ACT-OPS-018`; `ACT-FIN-029`; `ACT-OPS-017` | `ACT-SRC-014`; `ACT-COM-012`; `ACT-OPS-034` |
| `BS-014-AP-015` | `ACT-DIG-017`; `ACT-OPS-010`; `ACT-OPS-001`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-020`; `ACT-OPS-018`; `ACT-FIN-029`; `ACT-OPS-017`; `ACT-OPS-005`; `ACT-DIG-002` | `ACT-SRC-014`; `ACT-COM-012`; `ACT-OPS-034`; `ACT-OPS-007`; `ACT-DIG-007` |
| `BS-014-AP-016` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021` | `ACT-COM-001`; `ACT-OPS-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-COM-012`; `ACT-OPS-019`; `ACT-END-018` |
| `BS-014-AP-017` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-LOG-001`; `ACT-LOG-003` | `ACT-COM-001`; `ACT-OPS-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-COM-012`; `ACT-OPS-019`; `ACT-END-018`; `ACT-DIG-009`; `ACT-LOG-027` |
| `BS-014-AP-018` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-SRC-014`; `ACT-OPS-001` | `ACT-COM-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017` | `ACT-COM-012`; `ACT-OPS-019`; `ACT-END-018`; `ACT-OPS-016` |
| `BS-014-AP-019` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-COM-001`; `ACT-OPS-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017`; `ACT-OPS-005`; `ACT-DIG-002` | `ACT-COM-012`; `ACT-OPS-019`; `ACT-END-018`; `ACT-OPS-007`; `ACT-DIG-007` |
| `BS-014-AP-020` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-PRD-016`; `ACT-PRD-027`; `ACT-RND-021`; `ACT-RND-001`; `ACT-RND-007` | `ACT-COM-001`; `ACT-OPS-001`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-017`; `ACT-DIG-007`; `ACT-DIG-008`; `ACT-EDU-014` | `ACT-COM-012`; `ACT-OPS-019`; `ACT-END-018`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-014-AP-021` | `ACT-PRF-001`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRF-022`; `ACT-OPS-017`; `ACT-RND-018` | `ACT-OPS-007`; `ACT-OPS-026`; `ACT-EDU-002`; `ACT-PRF-021`; `ACT-OPS-011`; `ACT-DIG-002` | `ACT-PRF-028`; `ACT-DIG-007` |
| `BS-014-AP-022` | `ACT-PRF-001`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRF-022`; `ACT-OPS-017` | `ACT-OPS-007`; `ACT-OPS-026`; `ACT-EDU-002`; `ACT-PRF-021`; `ACT-OPS-011` | `ACT-RND-018`; `ACT-DIG-002`; `ACT-PRF-028` |
| `BS-014-AP-023` | `ACT-PRF-001`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRF-022`; `ACT-OPS-017`; `ACT-DIG-002`; `ACT-DIG-003` | `ACT-OPS-007`; `ACT-OPS-026`; `ACT-EDU-002`; `ACT-PRF-021`; `ACT-OPS-011`; `ACT-DIG-012`; `ACT-DIG-026` | `ACT-RND-018`; `ACT-PRF-028`; `ACT-DIG-010` |
| `BS-014-AP-024` | `ACT-PRF-001`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRF-022`; `ACT-OPS-017`; `ACT-RND-021`; `ACT-QLT-001` | `ACT-OPS-007`; `ACT-OPS-026`; `ACT-EDU-002`; `ACT-PRF-021`; `ACT-OPS-011`; `ACT-QLT-003`; `ACT-QLT-004`; `ACT-DIG-008` | `ACT-RND-018`; `ACT-DIG-002`; `ACT-PRF-028`; `ACT-QLT-006`; `ACT-QLT-007` |
| `BS-014-AP-025` | `ACT-PRF-001`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRF-022`; `ACT-OPS-017`; `ACT-EDU-002`; `ACT-RND-018` | `ACT-OPS-007`; `ACT-OPS-026`; `ACT-PRF-021`; `ACT-OPS-011`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007`; `ACT-DIG-002` | `ACT-PRF-028`; `ACT-RND-017`; `ACT-DIG-015`; `ACT-DIG-007` |
| `BS-014-AP-026` | `ACT-DIG-004`; `ACT-DIG-015`; `ACT-MKT-020`; `ACT-DIG-016`; `ACT-DIG-005`; `ACT-COM-009`; `ACT-COM-008` | `ACT-DIG-002`; `ACT-DIG-014`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-LOG-006`; `ACT-OPS-018`; `ACT-OPS-005` | `ACT-COM-010`; `ACT-MKT-002`; `ACT-LOG-020`; `ACT-OPS-007` |
| `BS-014-AP-027` | `ACT-DIG-004`; `ACT-DIG-015`; `ACT-MKT-020`; `ACT-DIG-016`; `ACT-DIG-005`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-002`; `ACT-DIG-014`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-OPS-005`; `ACT-QLT-010`; `ACT-QLT-023`; `ACT-OPS-018` | `ACT-COM-008`; `ACT-COM-010`; `ACT-MKT-002`; `ACT-OPS-007`; `ACT-FIN-007`; `ACT-FIN-009` |
| `BS-014-AP-028` | `ACT-DIG-004`; `ACT-DIG-015`; `ACT-MKT-020`; `ACT-DIG-016`; `ACT-DIG-005`; `ACT-MKT-001`; `ACT-MKT-003` | `ACT-DIG-002`; `ACT-DIG-014`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-MKT-005`; `ACT-MKT-015`; `ACT-OPS-005` | `ACT-COM-008`; `ACT-COM-010`; `ACT-MKT-002`; `ACT-MKT-007`; `ACT-OPS-007` |
| `BS-014-AP-029` | `ACT-DIG-004`; `ACT-DIG-015`; `ACT-MKT-020`; `ACT-DIG-016`; `ACT-DIG-005`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-DIG-002`; `ACT-DIG-014`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-OPS-005` | `ACT-COM-008`; `ACT-COM-010`; `ACT-MKT-002`; `ACT-OPS-007` |
| `BS-014-AP-030` | `ACT-DIG-004`; `ACT-DIG-015`; `ACT-MKT-020`; `ACT-DIG-016`; `ACT-DIG-005`; `ACT-MKT-001`; `ACT-MKT-003` | `ACT-RND-018`; `ACT-DIG-002`; `ACT-DIG-014`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-MKT-005`; `ACT-MKT-015` | `ACT-COM-008`; `ACT-COM-010`; `ACT-MKT-002`; `ACT-MKT-007` |

## 3. Domain assignments

### 3.1 Software products and platforms

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-SFW-001` | Enterprise Software | `BS-014-AP-001` |
| `TEC-SFW-002` | Software as a Service | `BS-014-AP-001` |
| `TEC-SFW-003` | Mobile Applications | `BS-014-AP-001` |
| `TEC-SFW-004` | Web Applications | `BS-014-AP-001` |
| `TEC-SFW-005` | Business Operating Systems | `BS-014-AP-001` |
| `TEC-SFW-006` | Customer Relationship Management | `BS-014-AP-002` |
| `TEC-SFW-007` | Enterprise Resource Planning | `BS-014-AP-002` |
| `TEC-SFW-008` | Human Resource Management Systems | `BS-014-AP-001` |
| `TEC-SFW-009` | Accounting and Finance Software | `BS-014-AP-001` |
| `TEC-SFW-010` | Document Management Systems | `BS-014-AP-001` |
| `TEC-SFW-011` | Workflow and Automation Platforms | `BS-014-AP-001` |
| `TEC-SFW-012` | Project Management Software | `BS-014-AP-001` |
| `TEC-SFW-013` | Collaboration Software | `BS-014-AP-001` |
| `TEC-SFW-014` | Vertical Industry Software | `BS-014-AP-001` |
| `TEC-SFW-015` | Developer Tools | `BS-014-AP-002` |
| `TEC-SFW-016` | Low-Code and No-Code Platforms | `BS-014-AP-001` |

### 3.2 Data, analytics and artificial intelligence

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-DAT-001` | Business Intelligence | `BS-014-AP-003` |
| `TEC-DAT-002` | Data Warehousing | `BS-014-AP-003` |
| `TEC-DAT-003` | Data Engineering | `BS-014-AP-003` |
| `TEC-DAT-004` | Data Integration | `BS-014-AP-003` |
| `TEC-DAT-005` | Master Data Management | `BS-014-AP-003` |
| `TEC-DAT-006` | Data Governance | `BS-014-AP-004` |
| `TEC-DAT-007` | Analytics Platforms | `BS-014-AP-005` |
| `TEC-DAT-008` | Artificial Intelligence Systems | `BS-014-AP-005` |
| `TEC-DAT-009` | Machine Learning Platforms | `BS-014-AP-005` |
| `TEC-DAT-010` | Natural Language Processing | `BS-014-AP-003` |
| `TEC-DAT-011` | Computer Vision | `BS-014-AP-003` |
| `TEC-DAT-012` | Decision Support Systems | `BS-014-AP-005` |
| `TEC-DAT-013` | Search and Knowledge Systems | `BS-014-AP-005` |
| `TEC-DAT-014` | Geospatial Analytics | `BS-014-AP-003` |
| `TEC-DAT-015` | Data Quality Tools | `BS-014-AP-003` |
| `TEC-DAT-016` | Database Products | `BS-014-AP-003` |

### 3.3 Cloud, hosting and infrastructure

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-CLD-001` | Cloud Computing | `BS-014-AP-006` |
| `TEC-CLD-002` | Cloud Platforms | `BS-014-AP-007` |
| `TEC-CLD-003` | Managed Cloud Services | `BS-014-AP-006` |
| `TEC-CLD-004` | Web Hosting | `BS-014-AP-006` |
| `TEC-CLD-005` | Application Hosting | `BS-014-AP-007` |
| `TEC-CLD-006` | Data Centres | `BS-014-AP-006` |
| `TEC-CLD-007` | Colocation Services | `BS-014-AP-006` |
| `TEC-CLD-008` | Content Delivery Networks | `BS-014-AP-008` |
| `TEC-CLD-009` | Backup and Recovery | `BS-014-AP-009` |
| `TEC-CLD-010` | Disaster Recovery | `BS-014-AP-009` |
| `TEC-CLD-011` | Infrastructure as a Service | `BS-014-AP-006` |
| `TEC-CLD-012` | Platform as a Service | `BS-014-AP-007` |
| `TEC-CLD-013` | Server Management | `BS-014-AP-006` |
| `TEC-CLD-014` | Virtualization | `BS-014-AP-006` |
| `TEC-CLD-015` | Container Platforms | `BS-014-AP-007` |
| `TEC-CLD-016` | Edge Computing | `BS-014-AP-006` |
| `TEC-CLD-017` | Domain and DNS Services | `BS-014-AP-006` |

### 3.4 Cybersecurity and trust

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-SEC-001` | Managed Security Services | `BS-014-AP-010` |
| `TEC-SEC-002` | Security Operations Centres | `BS-014-AP-010` |
| `TEC-SEC-003` | Identity and Access Management | `BS-014-AP-010` |
| `TEC-SEC-004` | Endpoint Security | `BS-014-AP-010` |
| `TEC-SEC-005` | Network Security | `BS-014-AP-010` |
| `TEC-SEC-006` | Cloud Security | `BS-014-AP-010` |
| `TEC-SEC-007` | Application Security | `BS-014-AP-011` |
| `TEC-SEC-008` | Data Security | `BS-014-AP-010` |
| `TEC-SEC-009` | Email Security | `BS-014-AP-010` |
| `TEC-SEC-010` | Security Information and Event Management | `BS-014-AP-010` |
| `TEC-SEC-011` | Vulnerability Management | `BS-014-AP-010` |
| `TEC-SEC-012` | Penetration Testing | `BS-014-AP-012` |
| `TEC-SEC-013` | Governance, Risk and Compliance | `BS-014-AP-013` |
| `TEC-SEC-014` | Digital Identity | `BS-014-AP-011` |
| `TEC-SEC-015` | Electronic Signatures | `BS-014-AP-010` |
| `TEC-SEC-016` | Fraud and Threat Intelligence | `BS-014-AP-010` |

### 3.5 Telecommunications and connectivity

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-TEL-001` | Mobile Network Operators | `BS-014-AP-014` |
| `TEC-TEL-002` | Fixed-Line Telecommunications | `BS-014-AP-014` |
| `TEC-TEL-003` | Internet Service Providers | `BS-014-AP-014` |
| `TEC-TEL-004` | Fibre Networks | `BS-014-AP-014` |
| `TEC-TEL-005` | Wireless Internet | `BS-014-AP-014` |
| `TEC-TEL-006` | Satellite Communications | `BS-014-AP-014` |
| `TEC-TEL-007` | Unified Communications | `BS-014-AP-014` |
| `TEC-TEL-008` | Voice over IP | `BS-014-AP-014` |
| `TEC-TEL-009` | Contact Centre Platforms | `BS-014-AP-015` |
| `TEC-TEL-010` | Messaging Platforms | `BS-014-AP-015` |
| `TEC-TEL-011` | Network Infrastructure | `BS-014-AP-014` |
| `TEC-TEL-012` | Telecommunications Towers | `BS-014-AP-014` |
| `TEC-TEL-013` | Internet Exchange Points | `BS-014-AP-014` |
| `TEC-TEL-014` | Managed Network Services | `BS-014-AP-014` |
| `TEC-TEL-015` | IoT Connectivity | `BS-014-AP-014` |

### 3.6 Technology hardware and connected infrastructure

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-HWD-001` | Computer Hardware | `BS-014-AP-016` |
| `TEC-HWD-002` | Servers and Storage | `BS-014-AP-017` |
| `TEC-HWD-003` | Networking Equipment | `BS-014-AP-018` |
| `TEC-HWD-004` | Telecommunications Equipment | `BS-014-AP-018` |
| `TEC-HWD-005` | Point-of-Sale Hardware | `BS-014-AP-016` |
| `TEC-HWD-006` | Barcode and RFID Equipment | `BS-014-AP-018` |
| `TEC-HWD-007` | Sensors and Telemetry | `BS-014-AP-016` |
| `TEC-HWD-008` | Internet of Things Platforms | `BS-014-AP-019` |
| `TEC-HWD-009` | Smart Building Systems | `BS-014-AP-019` |
| `TEC-HWD-010` | Industrial Automation | `BS-014-AP-020` |
| `TEC-HWD-011` | Embedded Systems | `BS-014-AP-019` |
| `TEC-HWD-012` | Robotics | `BS-014-AP-016` |
| `TEC-HWD-013` | Electronic Devices | `BS-014-AP-018` |
| `TEC-HWD-014` | Digital Signage | `BS-014-AP-019` |
| `TEC-HWD-015` | Access-Control Hardware | `BS-014-AP-016` |

### 3.7 Technology services and delivery

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-SRV-001` | Software Development Services | `BS-014-AP-021` |
| `TEC-SRV-002` | Systems Integration | `BS-014-AP-021` |
| `TEC-SRV-003` | IT Consulting | `BS-014-AP-022` |
| `TEC-SRV-004` | Managed IT Services | `BS-014-AP-022` |
| `TEC-SRV-005` | Technical Support | `BS-014-AP-022` |
| `TEC-SRV-006` | IT Outsourcing | `BS-014-AP-022` |
| `TEC-SRV-007` | Cloud Migration | `BS-014-AP-023` |
| `TEC-SRV-008` | Application Modernization | `BS-014-AP-021` |
| `TEC-SRV-009` | Data Migration | `BS-014-AP-022` |
| `TEC-SRV-010` | Enterprise Architecture | `BS-014-AP-022` |
| `TEC-SRV-011` | Quality Assurance and Testing | `BS-014-AP-024` |
| `TEC-SRV-012` | DevOps Services | `BS-014-AP-022` |
| `TEC-SRV-013` | User Experience Design | `BS-014-AP-022` |
| `TEC-SRV-014` | Technology Training | `BS-014-AP-025` |
| `TEC-SRV-015` | IT Procurement | `BS-014-AP-022` |
| `TEC-SRV-016` | Field Technology Services | `BS-014-AP-021` |

### 3.8 Digital commerce and communication technology

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `TEC-COM-001` | E-Commerce Platforms | `BS-014-AP-026` |
| `TEC-COM-002` | Payment Technology | `BS-014-AP-027` |
| `TEC-COM-003` | Marketplace Platforms | `BS-014-AP-026` |
| `TEC-COM-004` | Marketing Technology | `BS-014-AP-028` |
| `TEC-COM-005` | Advertising Technology | `BS-014-AP-028` |
| `TEC-COM-006` | Customer Engagement Platforms | `BS-014-AP-029` |
| `TEC-COM-007` | Social Media Management | `BS-014-AP-030` |
| `TEC-COM-008` | Content Management Systems | `BS-014-AP-029` |
| `TEC-COM-009` | Digital Experience Platforms | `BS-014-AP-029` |
| `TEC-COM-010` | Learning Technology | `BS-014-AP-029` |
| `TEC-COM-011` | Health Technology | `BS-014-AP-029` |
| `TEC-COM-012` | Legal Technology | `BS-014-AP-029` |
| `TEC-COM-013` | Property Technology | `BS-014-AP-029` |
| `TEC-COM-014` | Financial Technology | `BS-014-AP-029` |
| `TEC-COM-015` | Government Technology | `BS-014-AP-029` |
| `TEC-COM-016` | Travel Technology | `BS-014-AP-029` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
