# Harvester Government Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **96** canonical domains in `BS-015 Government` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-015-AP-001` | `ACT-PUB-001`; `ACT-PUB-024`; `ACT-PUB-002`; `ACT-PUB-008`; `ACT-DIG-008` | `ACT-PUB-003`; `ACT-PUB-004`; `ACT-PUB-026`; `ACT-PUB-025` | `ACT-PUB-005`; `ACT-PUB-009`; `ACT-DIG-015` |
| `BS-015-AP-002` | `ACT-PUB-001`; `ACT-PUB-024`; `ACT-PUB-002`; `ACT-PUB-008`; `ACT-DIG-008`; `ACT-PUB-007` | `ACT-PUB-003`; `ACT-PUB-004`; `ACT-PUB-026`; `ACT-PUB-025` | `ACT-PUB-005`; `ACT-PUB-009`; `ACT-DIG-015` |
| `BS-015-AP-003` | `ACT-PUB-001`; `ACT-PUB-024`; `ACT-PUB-002`; `ACT-PUB-008`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-PUB-003`; `ACT-PUB-004`; `ACT-PUB-026`; `ACT-PUB-025`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-PUB-005`; `ACT-PUB-009`; `ACT-DIG-015`; `ACT-EDU-002`; `ACT-LEG-013` |
| `BS-015-AP-004` | `ACT-PUB-007`; `ACT-PUB-009`; `ACT-PUB-008`; `ACT-PUB-022`; `ACT-PUB-023` | `ACT-PUB-029`; `ACT-FIN-027`; `ACT-MKT-013`; `ACT-DIG-008` | `ACT-PUB-028`; `ACT-PUB-032`; `ACT-PUB-015` |
| `BS-015-AP-005` | `ACT-PUB-007`; `ACT-PUB-009`; `ACT-PUB-008`; `ACT-PUB-022`; `ACT-PUB-023`; `ACT-OPS-012`; `ACT-OPS-014` | `ACT-PUB-029`; `ACT-FIN-027`; `ACT-MKT-013`; `ACT-DIG-008`; `ACT-OPS-017`; `ACT-SRC-015` | `ACT-PUB-028`; `ACT-PUB-032`; `ACT-PUB-015`; `ACT-OPS-019`; `ACT-OPS-013` |
| `BS-015-AP-006` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008`; `ACT-HLT-024`; `ACT-HLT-017` | `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-MKT-013`; `ACT-PUB-008` | `ACT-FIN-027`; `ACT-EDU-002`; `ACT-RND-001`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-007` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-PUB-008` | `ACT-FIN-027`; `ACT-EDU-002`; `ACT-RND-001`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-008` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025` | `ACT-FIN-027`; `ACT-EDU-002`; `ACT-RND-001` |
| `BS-015-AP-009` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008`; `ACT-HLT-018` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-LOG-002`; `ACT-QLT-011` | `ACT-FIN-027`; `ACT-EDU-002`; `ACT-RND-001`; `ACT-MKT-013` |
| `BS-015-AP-010` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020`; `ACT-PUB-008` | `ACT-FIN-027`; `ACT-EDU-002`; `ACT-RND-001`; `ACT-LEG-013`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-011` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008`; `ACT-EDU-002` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007`; `ACT-PUB-008` | `ACT-FIN-027`; `ACT-RND-001`; `ACT-RND-017`; `ACT-DIG-015`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-012` | `ACT-PUB-001`; `ACT-PUB-009`; `ACT-PUB-023`; `ACT-PUB-007`; `ACT-DIG-008`; `ACT-EDU-002` | `ACT-HLT-024`; `ACT-EDU-022`; `ACT-PUB-002`; `ACT-PUB-025`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-FIN-027`; `ACT-RND-001`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-015-AP-013` | `ACT-PUB-001`; `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-026`; `ACT-PUB-007` | `ACT-SRC-002`; `ACT-REA-017`; `ACT-OPS-024`; `ACT-OPS-011`; `ACT-OPS-034` | `ACT-QLT-015`; `ACT-DIG-009`; `ACT-PUB-008` |
| `BS-015-AP-014` | `ACT-PUB-001`; `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-026`; `ACT-PUB-007` | `ACT-SRC-002`; `ACT-REA-017`; `ACT-OPS-024`; `ACT-OPS-011`; `ACT-OPS-034`; `ACT-PUB-002`; `ACT-PUB-008`; `ACT-DIG-008` | `ACT-QLT-015`; `ACT-DIG-009`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-015` | `ACT-PUB-001`; `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-026`; `ACT-PUB-007`; `ACT-OPS-011` | `ACT-SRC-002`; `ACT-REA-017`; `ACT-OPS-024`; `ACT-OPS-034`; `ACT-OPS-012`; `ACT-QLT-014` | `ACT-QLT-015`; `ACT-DIG-009`; `ACT-PUB-008`; `ACT-OPS-027` |
| `BS-015-AP-016` | `ACT-PUB-001`; `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-026`; `ACT-PUB-007`; `ACT-END-001`; `ACT-END-002` | `ACT-SRC-002`; `ACT-REA-017`; `ACT-OPS-024`; `ACT-OPS-011`; `ACT-OPS-034`; `ACT-END-008`; `ACT-END-012` | `ACT-QLT-015`; `ACT-DIG-009`; `ACT-PUB-008`; `ACT-END-004`; `ACT-END-005` |
| `BS-015-AP-017` | `ACT-PUB-005`; `ACT-OPS-034`; `ACT-LEG-013`; `ACT-PUB-007`; `ACT-QLT-022` | `ACT-LEG-014`; `ACT-PUB-028`; `ACT-PUB-008`; `ACT-DIG-008` | `ACT-EDU-002`; `ACT-OPS-011`; `ACT-PUB-021` |
| `BS-015-AP-018` | `ACT-PUB-005`; `ACT-OPS-034`; `ACT-LEG-013`; `ACT-PUB-007`; `ACT-QLT-022`; `ACT-HLT-011` | `ACT-LEG-014`; `ACT-PUB-028`; `ACT-PUB-008`; `ACT-DIG-008`; `ACT-LOG-023`; `ACT-HLT-031`; `ACT-HLT-010` | `ACT-EDU-002`; `ACT-OPS-011`; `ACT-PUB-021`; `ACT-LOG-022` |
| `BS-015-AP-019` | `ACT-PUB-001`; `ACT-PUB-002`; `ACT-PUB-003`; `ACT-COM-019`; `ACT-DIG-008` | `ACT-PUB-024`; `ACT-RND-002`; `ACT-FIN-027`; `ACT-PUB-025` | `ACT-QLT-004`; `ACT-QLT-006`; `ACT-PUB-009` |
| `BS-015-AP-020` | `ACT-PUB-001`; `ACT-PUB-002`; `ACT-PUB-003`; `ACT-COM-019`; `ACT-DIG-008`; `ACT-MKT-001`; `ACT-MKT-003` | `ACT-PUB-024`; `ACT-RND-002`; `ACT-FIN-027`; `ACT-PUB-025`; `ACT-MKT-005`; `ACT-MKT-015` | `ACT-QLT-004`; `ACT-QLT-006`; `ACT-PUB-009`; `ACT-MKT-002`; `ACT-MKT-007` |
| `BS-015-AP-021` | `ACT-PUB-001`; `ACT-PUB-002`; `ACT-PUB-003`; `ACT-COM-019`; `ACT-DIG-008`; `ACT-PUB-007` | `ACT-PUB-024`; `ACT-RND-002`; `ACT-FIN-027`; `ACT-PUB-025`; `ACT-PUB-008` | `ACT-QLT-004`; `ACT-QLT-006`; `ACT-PUB-009`; `ACT-PUB-004` |
| `BS-015-AP-022` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-DIG-002`; `ACT-OPS-017` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-007` |
| `BS-015-AP-023` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027`; `ACT-PUB-001`; `ACT-PUB-007` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-DIG-002`; `ACT-OPS-017`; `ACT-PUB-002` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-007`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-024` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027`; `ACT-PUB-001`; `ACT-PUB-007` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-PUB-002`; `ACT-DIG-008` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-PUB-003`; `ACT-PUB-004` |
| `BS-015-AP-025` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009` |
| `BS-015-AP-026` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027`; `ACT-DIG-010`; `ACT-QLT-013` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-QLT-005`; `ACT-DIG-011`; `ACT-QLT-022`; `ACT-PUB-002` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-PUB-003` |
| `BS-015-AP-027` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027`; `ACT-FIN-006`; `ACT-FIN-031` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-QLT-010`; `ACT-QLT-023`; `ACT-OPS-018` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-FIN-007`; `ACT-FIN-009` |
| `BS-015-AP-028` | `ACT-RND-018`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-004`; `ACT-DIG-027`; `ACT-FIN-006`; `ACT-FIN-031` | `ACT-DIG-005`; `ACT-DIG-028`; `ACT-DIG-010`; `ACT-PUB-008`; `ACT-DIG-015`; `ACT-DIG-002`; `ACT-OPS-017`; `ACT-QLT-010` | `ACT-DIG-003`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-007`; `ACT-FIN-007`; `ACT-FIN-009` |

## 3. Domain assignments

### 3.1 Public administration and governance

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-ADM-001` | Federal Ministries | `BS-015-AP-001` |
| `GOV-ADM-002` | Provincial Departments | `BS-015-AP-002` |
| `GOV-ADM-003` | Local Government Authorities | `BS-015-AP-002` |
| `GOV-ADM-004` | District Administration | `BS-015-AP-001` |
| `GOV-ADM-005` | Municipal Corporations | `BS-015-AP-002` |
| `GOV-ADM-006` | Regulatory Authorities | `BS-015-AP-003` |
| `GOV-ADM-007` | Public Commissions | `BS-015-AP-001` |
| `GOV-ADM-008` | Public Boards | `BS-015-AP-001` |
| `GOV-ADM-009` | Government Secretariats | `BS-015-AP-002` |
| `GOV-ADM-010` | Public Service Commissions | `BS-015-AP-001` |
| `GOV-ADM-011` | Election Administration | `BS-015-AP-001` |
| `GOV-ADM-012` | Civil Registration and Identity Services | `BS-015-AP-001` |
| `GOV-ADM-013` | Land and Revenue Administration | `BS-015-AP-001` |
| `GOV-ADM-014` | Public Records and Archives | `BS-015-AP-001` |

### 3.2 Citizen and social services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-SOC-001` | Social Protection | `BS-015-AP-004` |
| `GOV-SOC-002` | Pension Administration | `BS-015-AP-004` |
| `GOV-SOC-003` | Zakat Administration | `BS-015-AP-004` |
| `GOV-SOC-004` | Public Welfare Services | `BS-015-AP-004` |
| `GOV-SOC-005` | Child Protection | `BS-015-AP-004` |
| `GOV-SOC-006` | Women's Development | `BS-015-AP-004` |
| `GOV-SOC-007` | Youth Affairs | `BS-015-AP-004` |
| `GOV-SOC-008` | Disability Services | `BS-015-AP-004` |
| `GOV-SOC-009` | Senior Citizen Services | `BS-015-AP-004` |
| `GOV-SOC-010` | Labour and Employment Services | `BS-015-AP-004` |
| `GOV-SOC-011` | Immigration and Citizenship Services | `BS-015-AP-004` |
| `GOV-SOC-012` | Public Grievance and Complaint Services | `BS-015-AP-004` |
| `GOV-SOC-013` | Citizen Service Centres | `BS-015-AP-005` |

### 3.3 Public health and education administration

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-HLT-001` | Public Health Departments | `BS-015-AP-006` |
| `GOV-HLT-002` | Government Hospitals | `BS-015-AP-007` |
| `GOV-HLT-003` | Primary Health Programs | `BS-015-AP-008` |
| `GOV-HLT-004` | Disease Surveillance | `BS-015-AP-008` |
| `GOV-HLT-005` | Vaccination Programs | `BS-015-AP-009` |
| `GOV-HLT-006` | Drug Regulatory Services | `BS-015-AP-010` |
| `GOV-HLT-007` | Public Education Departments | `BS-015-AP-011` |
| `GOV-HLT-008` | Government Schools | `BS-015-AP-011` |
| `GOV-HLT-009` | Public Universities | `BS-015-AP-008` |
| `GOV-HLT-010` | Technical Education Authorities | `BS-015-AP-012` |
| `GOV-HLT-011` | Examination Boards | `BS-015-AP-008` |
| `GOV-HLT-012` | Education Accreditation and Standards | `BS-015-AP-012` |

### 3.4 Infrastructure, utilities and municipal services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-INF-001` | Road and Highway Authorities | `BS-015-AP-013` |
| `GOV-INF-002` | Public Works Departments | `BS-015-AP-014` |
| `GOV-INF-003` | Urban Development Authorities | `BS-015-AP-013` |
| `GOV-INF-004` | Housing Authorities | `BS-015-AP-013` |
| `GOV-INF-005` | Water and Sanitation Agencies | `BS-015-AP-015` |
| `GOV-INF-006` | Waste Management Authorities | `BS-015-AP-016` |
| `GOV-INF-007` | Electricity Authorities | `BS-015-AP-015` |
| `GOV-INF-008` | Gas Utilities | `BS-015-AP-015` |
| `GOV-INF-009` | Transport Authorities | `BS-015-AP-013` |
| `GOV-INF-010` | Public Transit Operators | `BS-015-AP-013` |
| `GOV-INF-011` | Parks and Recreation Authorities | `BS-015-AP-013` |
| `GOV-INF-012` | Building Control Authorities | `BS-015-AP-013` |
| `GOV-INF-013` | Development Planning Authorities | `BS-015-AP-013` |

### 3.5 Public safety, justice and emergency

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-SAF-001` | Police Services | `BS-015-AP-017` |
| `GOV-SAF-002` | Traffic Police | `BS-015-AP-017` |
| `GOV-SAF-003` | Fire and Rescue Services | `BS-015-AP-018` |
| `GOV-SAF-004` | Emergency Medical Services | `BS-015-AP-018` |
| `GOV-SAF-005` | Civil Defence | `BS-015-AP-017` |
| `GOV-SAF-006` | Disaster Management Authorities | `BS-015-AP-017` |
| `GOV-SAF-007` | Prison and Corrections Services | `BS-015-AP-017` |
| `GOV-SAF-008` | Courts and Judicial Administration | `BS-015-AP-017` |
| `GOV-SAF-009` | Prosecution Services | `BS-015-AP-017` |
| `GOV-SAF-010` | Forensic Services | `BS-015-AP-017` |
| `GOV-SAF-011` | Border and Customs Services | `BS-015-AP-017` |
| `GOV-SAF-012` | Cybercrime and Digital Investigation | `BS-015-AP-017` |

### 3.6 Economic, trade and sector administration

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-ECO-001` | Tax and Revenue Authorities | `BS-015-AP-019` |
| `GOV-ECO-002` | Customs Administration | `BS-015-AP-019` |
| `GOV-ECO-003` | Trade Development Authorities | `BS-015-AP-019` |
| `GOV-ECO-004` | Investment Promotion Agencies | `BS-015-AP-020` |
| `GOV-ECO-005` | Industry Departments | `BS-015-AP-021` |
| `GOV-ECO-006` | Agriculture Departments | `BS-015-AP-021` |
| `GOV-ECO-007` | Livestock Departments | `BS-015-AP-021` |
| `GOV-ECO-008` | Food Authorities | `BS-015-AP-019` |
| `GOV-ECO-009` | Tourism Authorities | `BS-015-AP-019` |
| `GOV-ECO-010` | Energy Regulators | `BS-015-AP-021` |
| `GOV-ECO-011` | Telecommunications Regulators | `BS-015-AP-021` |
| `GOV-ECO-012` | Financial Regulators | `BS-015-AP-021` |
| `GOV-ECO-013` | Environmental Protection Agencies | `BS-015-AP-019` |
| `GOV-ECO-014` | Statistics and Census Agencies | `BS-015-AP-019` |

### 3.7 Digital government and public operations

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `GOV-DIG-001` | Digital Citizen Portals | `BS-015-AP-022` |
| `GOV-DIG-002` | Government Service Platforms | `BS-015-AP-023` |
| `GOV-DIG-003` | Government Enterprise Resource Planning | `BS-015-AP-024` |
| `GOV-DIG-004` | Public Financial Management Systems | `BS-015-AP-022` |
| `GOV-DIG-005` | Electronic Procurement | `BS-015-AP-025` |
| `GOV-DIG-006` | Electronic Licensing | `BS-015-AP-025` |
| `GOV-DIG-007` | Permit Management | `BS-015-AP-025` |
| `GOV-DIG-008` | Case and Workflow Management | `BS-015-AP-025` |
| `GOV-DIG-009` | Government Document Management | `BS-015-AP-024` |
| `GOV-DIG-010` | Open Data Platforms | `BS-015-AP-022` |
| `GOV-DIG-011` | Government Analytics | `BS-015-AP-024` |
| `GOV-DIG-012` | Geographic Information Systems | `BS-015-AP-022` |
| `GOV-DIG-013` | Smart City Systems | `BS-015-AP-022` |
| `GOV-DIG-014` | Public Asset Management | `BS-015-AP-025` |
| `GOV-DIG-015` | Government Cybersecurity | `BS-015-AP-026` |
| `GOV-DIG-016` | Interagency Data Exchange | `BS-015-AP-027` |
| `GOV-DIG-017` | Public Contact Centres | `BS-015-AP-025` |
| `GOV-DIG-018` | Digital Payments for Government | `BS-015-AP-028` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
