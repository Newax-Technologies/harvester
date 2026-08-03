# Harvester Government Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-015 Government`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Government
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

This registry contains **96 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `GOV-ADM` | Public administration and governance | 14 |
| `GOV-SOC` | Citizen and social services | 13 |
| `GOV-HLT` | Public health and education administration | 12 |
| `GOV-INF` | Infrastructure, utilities and municipal services | 13 |
| `GOV-SAF` | Public safety, justice and emergency | 12 |
| `GOV-ECO` | Economic, trade and sector administration | 14 |
| `GOV-DIG` | Digital government and public operations | 18 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Public administration and governance

| Code | Domain |
| --- | --- |
| `GOV-ADM-001` | Federal Ministries |
| `GOV-ADM-002` | Provincial Departments |
| `GOV-ADM-003` | Local Government Authorities |
| `GOV-ADM-004` | District Administration |
| `GOV-ADM-005` | Municipal Corporations |
| `GOV-ADM-006` | Regulatory Authorities |
| `GOV-ADM-007` | Public Commissions |
| `GOV-ADM-008` | Public Boards |
| `GOV-ADM-009` | Government Secretariats |
| `GOV-ADM-010` | Public Service Commissions |
| `GOV-ADM-011` | Election Administration |
| `GOV-ADM-012` | Civil Registration and Identity Services |
| `GOV-ADM-013` | Land and Revenue Administration |
| `GOV-ADM-014` | Public Records and Archives |

### 4.2 Citizen and social services

| Code | Domain |
| --- | --- |
| `GOV-SOC-001` | Social Protection |
| `GOV-SOC-002` | Pension Administration |
| `GOV-SOC-003` | Zakat Administration |
| `GOV-SOC-004` | Public Welfare Services |
| `GOV-SOC-005` | Child Protection |
| `GOV-SOC-006` | Women's Development |
| `GOV-SOC-007` | Youth Affairs |
| `GOV-SOC-008` | Disability Services |
| `GOV-SOC-009` | Senior Citizen Services |
| `GOV-SOC-010` | Labour and Employment Services |
| `GOV-SOC-011` | Immigration and Citizenship Services |
| `GOV-SOC-012` | Public Grievance and Complaint Services |
| `GOV-SOC-013` | Citizen Service Centres |

### 4.3 Public health and education administration

| Code | Domain |
| --- | --- |
| `GOV-HLT-001` | Public Health Departments |
| `GOV-HLT-002` | Government Hospitals |
| `GOV-HLT-003` | Primary Health Programs |
| `GOV-HLT-004` | Disease Surveillance |
| `GOV-HLT-005` | Vaccination Programs |
| `GOV-HLT-006` | Drug Regulatory Services |
| `GOV-HLT-007` | Public Education Departments |
| `GOV-HLT-008` | Government Schools |
| `GOV-HLT-009` | Public Universities |
| `GOV-HLT-010` | Technical Education Authorities |
| `GOV-HLT-011` | Examination Boards |
| `GOV-HLT-012` | Education Accreditation and Standards |

### 4.4 Infrastructure, utilities and municipal services

| Code | Domain |
| --- | --- |
| `GOV-INF-001` | Road and Highway Authorities |
| `GOV-INF-002` | Public Works Departments |
| `GOV-INF-003` | Urban Development Authorities |
| `GOV-INF-004` | Housing Authorities |
| `GOV-INF-005` | Water and Sanitation Agencies |
| `GOV-INF-006` | Waste Management Authorities |
| `GOV-INF-007` | Electricity Authorities |
| `GOV-INF-008` | Gas Utilities |
| `GOV-INF-009` | Transport Authorities |
| `GOV-INF-010` | Public Transit Operators |
| `GOV-INF-011` | Parks and Recreation Authorities |
| `GOV-INF-012` | Building Control Authorities |
| `GOV-INF-013` | Development Planning Authorities |

### 4.5 Public safety, justice and emergency

| Code | Domain |
| --- | --- |
| `GOV-SAF-001` | Police Services |
| `GOV-SAF-002` | Traffic Police |
| `GOV-SAF-003` | Fire and Rescue Services |
| `GOV-SAF-004` | Emergency Medical Services |
| `GOV-SAF-005` | Civil Defence |
| `GOV-SAF-006` | Disaster Management Authorities |
| `GOV-SAF-007` | Prison and Corrections Services |
| `GOV-SAF-008` | Courts and Judicial Administration |
| `GOV-SAF-009` | Prosecution Services |
| `GOV-SAF-010` | Forensic Services |
| `GOV-SAF-011` | Border and Customs Services |
| `GOV-SAF-012` | Cybercrime and Digital Investigation |

### 4.6 Economic, trade and sector administration

| Code | Domain |
| --- | --- |
| `GOV-ECO-001` | Tax and Revenue Authorities |
| `GOV-ECO-002` | Customs Administration |
| `GOV-ECO-003` | Trade Development Authorities |
| `GOV-ECO-004` | Investment Promotion Agencies |
| `GOV-ECO-005` | Industry Departments |
| `GOV-ECO-006` | Agriculture Departments |
| `GOV-ECO-007` | Livestock Departments |
| `GOV-ECO-008` | Food Authorities |
| `GOV-ECO-009` | Tourism Authorities |
| `GOV-ECO-010` | Energy Regulators |
| `GOV-ECO-011` | Telecommunications Regulators |
| `GOV-ECO-012` | Financial Regulators |
| `GOV-ECO-013` | Environmental Protection Agencies |
| `GOV-ECO-014` | Statistics and Census Agencies |

### 4.7 Digital government and public operations

| Code | Domain |
| --- | --- |
| `GOV-DIG-001` | Digital Citizen Portals |
| `GOV-DIG-002` | Government Service Platforms |
| `GOV-DIG-003` | Government Enterprise Resource Planning |
| `GOV-DIG-004` | Public Financial Management Systems |
| `GOV-DIG-005` | Electronic Procurement |
| `GOV-DIG-006` | Electronic Licensing |
| `GOV-DIG-007` | Permit Management |
| `GOV-DIG-008` | Case and Workflow Management |
| `GOV-DIG-009` | Government Document Management |
| `GOV-DIG-010` | Open Data Platforms |
| `GOV-DIG-011` | Government Analytics |
| `GOV-DIG-012` | Geographic Information Systems |
| `GOV-DIG-013` | Smart City Systems |
| `GOV-DIG-014` | Public Asset Management |
| `GOV-DIG-015` | Government Cybersecurity |
| `GOV-DIG-016` | Interagency Data Exchange |
| `GOV-DIG-017` | Public Contact Centres |
| `GOV-DIG-018` | Digital Payments for Government |

## 5. First-release presentation shortlist

Federal Ministries, Provincial Departments, Local Government, Municipal Corporations, Regulatory Authorities, Civil Registration, Land and Revenue Administration, Social Protection, Public Welfare, Citizen Service Centres, Public Health Departments, Government Hospitals, Public Education Departments, Road and Highway Authorities, Public Works, Urban Development, Water and Sanitation, Waste Management, Transport Authorities, Police Services, Fire and Rescue, Disaster Management, Courts and Judicial Administration, Tax and Revenue Authorities, Customs Administration, Trade Development, Food Authorities, Tourism Authorities, Environmental Protection, Statistics and Census, Digital Citizen Portals, Government Service Platforms, Public Financial Management, Electronic Procurement, Electronic Licensing, Permit Management, Government Document Management, Open Data, Smart City Systems, Government Cybersecurity.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Government departments:** Regulating, Licensing, Inspecting, Administering, Reporting, Serving citizens
- **Municipal services:** Planning, Operating, Maintaining, Collecting fees, Responding
- **Public safety:** Dispatching, Investigating, Responding, Recording, Coordinating
- **Digital government:** Publishing services, Processing applications, Exchanging data, Collecting payments, Auditing

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Government hospitals | Healthcare | Operating; treating; reporting |
| Public infrastructure | Construction; Energy | Planning; procuring; maintaining |
| Citizen portals | Technology | Developing; integrating; operating |
| Public transport | Travel; Logistics | Scheduling; ticketing; operating |

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

- The shortlist and all 96 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
