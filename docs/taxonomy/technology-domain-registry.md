# Harvester Technology Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-014 Technology`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Technology
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

This registry contains **127 canonical domains** in **8 families**.

| Family | Name | Count |
| --- | --- | --- |
| `TEC-SFW` | Software products and platforms | 16 |
| `TEC-DAT` | Data, analytics and artificial intelligence | 16 |
| `TEC-CLD` | Cloud, hosting and infrastructure | 17 |
| `TEC-SEC` | Cybersecurity and trust | 16 |
| `TEC-TEL` | Telecommunications and connectivity | 15 |
| `TEC-HWD` | Technology hardware and connected infrastructure | 15 |
| `TEC-SRV` | Technology services and delivery | 16 |
| `TEC-COM` | Digital commerce and communication technology | 16 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Software products and platforms

| Code | Domain |
| --- | --- |
| `TEC-SFW-001` | Enterprise Software |
| `TEC-SFW-002` | Software as a Service |
| `TEC-SFW-003` | Mobile Applications |
| `TEC-SFW-004` | Web Applications |
| `TEC-SFW-005` | Business Operating Systems |
| `TEC-SFW-006` | Customer Relationship Management |
| `TEC-SFW-007` | Enterprise Resource Planning |
| `TEC-SFW-008` | Human Resource Management Systems |
| `TEC-SFW-009` | Accounting and Finance Software |
| `TEC-SFW-010` | Document Management Systems |
| `TEC-SFW-011` | Workflow and Automation Platforms |
| `TEC-SFW-012` | Project Management Software |
| `TEC-SFW-013` | Collaboration Software |
| `TEC-SFW-014` | Vertical Industry Software |
| `TEC-SFW-015` | Developer Tools |
| `TEC-SFW-016` | Low-Code and No-Code Platforms |

### 4.2 Data, analytics and artificial intelligence

| Code | Domain |
| --- | --- |
| `TEC-DAT-001` | Business Intelligence |
| `TEC-DAT-002` | Data Warehousing |
| `TEC-DAT-003` | Data Engineering |
| `TEC-DAT-004` | Data Integration |
| `TEC-DAT-005` | Master Data Management |
| `TEC-DAT-006` | Data Governance |
| `TEC-DAT-007` | Analytics Platforms |
| `TEC-DAT-008` | Artificial Intelligence Systems |
| `TEC-DAT-009` | Machine Learning Platforms |
| `TEC-DAT-010` | Natural Language Processing |
| `TEC-DAT-011` | Computer Vision |
| `TEC-DAT-012` | Decision Support Systems |
| `TEC-DAT-013` | Search and Knowledge Systems |
| `TEC-DAT-014` | Geospatial Analytics |
| `TEC-DAT-015` | Data Quality Tools |
| `TEC-DAT-016` | Database Products |

### 4.3 Cloud, hosting and infrastructure

| Code | Domain |
| --- | --- |
| `TEC-CLD-001` | Cloud Computing |
| `TEC-CLD-002` | Cloud Platforms |
| `TEC-CLD-003` | Managed Cloud Services |
| `TEC-CLD-004` | Web Hosting |
| `TEC-CLD-005` | Application Hosting |
| `TEC-CLD-006` | Data Centres |
| `TEC-CLD-007` | Colocation Services |
| `TEC-CLD-008` | Content Delivery Networks |
| `TEC-CLD-009` | Backup and Recovery |
| `TEC-CLD-010` | Disaster Recovery |
| `TEC-CLD-011` | Infrastructure as a Service |
| `TEC-CLD-012` | Platform as a Service |
| `TEC-CLD-013` | Server Management |
| `TEC-CLD-014` | Virtualization |
| `TEC-CLD-015` | Container Platforms |
| `TEC-CLD-016` | Edge Computing |
| `TEC-CLD-017` | Domain and DNS Services |

### 4.4 Cybersecurity and trust

| Code | Domain |
| --- | --- |
| `TEC-SEC-001` | Managed Security Services |
| `TEC-SEC-002` | Security Operations Centres |
| `TEC-SEC-003` | Identity and Access Management |
| `TEC-SEC-004` | Endpoint Security |
| `TEC-SEC-005` | Network Security |
| `TEC-SEC-006` | Cloud Security |
| `TEC-SEC-007` | Application Security |
| `TEC-SEC-008` | Data Security |
| `TEC-SEC-009` | Email Security |
| `TEC-SEC-010` | Security Information and Event Management |
| `TEC-SEC-011` | Vulnerability Management |
| `TEC-SEC-012` | Penetration Testing |
| `TEC-SEC-013` | Governance, Risk and Compliance |
| `TEC-SEC-014` | Digital Identity |
| `TEC-SEC-015` | Electronic Signatures |
| `TEC-SEC-016` | Fraud and Threat Intelligence |

### 4.5 Telecommunications and connectivity

| Code | Domain |
| --- | --- |
| `TEC-TEL-001` | Mobile Network Operators |
| `TEC-TEL-002` | Fixed-Line Telecommunications |
| `TEC-TEL-003` | Internet Service Providers |
| `TEC-TEL-004` | Fibre Networks |
| `TEC-TEL-005` | Wireless Internet |
| `TEC-TEL-006` | Satellite Communications |
| `TEC-TEL-007` | Unified Communications |
| `TEC-TEL-008` | Voice over IP |
| `TEC-TEL-009` | Contact Centre Platforms |
| `TEC-TEL-010` | Messaging Platforms |
| `TEC-TEL-011` | Network Infrastructure |
| `TEC-TEL-012` | Telecommunications Towers |
| `TEC-TEL-013` | Internet Exchange Points |
| `TEC-TEL-014` | Managed Network Services |
| `TEC-TEL-015` | IoT Connectivity |

### 4.6 Technology hardware and connected infrastructure

| Code | Domain |
| --- | --- |
| `TEC-HWD-001` | Computer Hardware |
| `TEC-HWD-002` | Servers and Storage |
| `TEC-HWD-003` | Networking Equipment |
| `TEC-HWD-004` | Telecommunications Equipment |
| `TEC-HWD-005` | Point-of-Sale Hardware |
| `TEC-HWD-006` | Barcode and RFID Equipment |
| `TEC-HWD-007` | Sensors and Telemetry |
| `TEC-HWD-008` | Internet of Things Platforms |
| `TEC-HWD-009` | Smart Building Systems |
| `TEC-HWD-010` | Industrial Automation |
| `TEC-HWD-011` | Embedded Systems |
| `TEC-HWD-012` | Robotics |
| `TEC-HWD-013` | Electronic Devices |
| `TEC-HWD-014` | Digital Signage |
| `TEC-HWD-015` | Access-Control Hardware |

### 4.7 Technology services and delivery

| Code | Domain |
| --- | --- |
| `TEC-SRV-001` | Software Development Services |
| `TEC-SRV-002` | Systems Integration |
| `TEC-SRV-003` | IT Consulting |
| `TEC-SRV-004` | Managed IT Services |
| `TEC-SRV-005` | Technical Support |
| `TEC-SRV-006` | IT Outsourcing |
| `TEC-SRV-007` | Cloud Migration |
| `TEC-SRV-008` | Application Modernization |
| `TEC-SRV-009` | Data Migration |
| `TEC-SRV-010` | Enterprise Architecture |
| `TEC-SRV-011` | Quality Assurance and Testing |
| `TEC-SRV-012` | DevOps Services |
| `TEC-SRV-013` | User Experience Design |
| `TEC-SRV-014` | Technology Training |
| `TEC-SRV-015` | IT Procurement |
| `TEC-SRV-016` | Field Technology Services |

### 4.8 Digital commerce and communication technology

| Code | Domain |
| --- | --- |
| `TEC-COM-001` | E-Commerce Platforms |
| `TEC-COM-002` | Payment Technology |
| `TEC-COM-003` | Marketplace Platforms |
| `TEC-COM-004` | Marketing Technology |
| `TEC-COM-005` | Advertising Technology |
| `TEC-COM-006` | Customer Engagement Platforms |
| `TEC-COM-007` | Social Media Management |
| `TEC-COM-008` | Content Management Systems |
| `TEC-COM-009` | Digital Experience Platforms |
| `TEC-COM-010` | Learning Technology |
| `TEC-COM-011` | Health Technology |
| `TEC-COM-012` | Legal Technology |
| `TEC-COM-013` | Property Technology |
| `TEC-COM-014` | Financial Technology |
| `TEC-COM-015` | Government Technology |
| `TEC-COM-016` | Travel Technology |

## 5. First-release presentation shortlist

Enterprise Software, SaaS, Mobile Applications, Business Operating Systems, CRM, ERP, HR Management Systems, Document Management, Workflow Automation, Vertical Software, Business Intelligence, Data Engineering, Data Integration, Artificial Intelligence, Machine Learning, Cloud Computing, Managed Cloud, Web Hosting, Data Centres, Backup and Recovery, Managed Security, Identity and Access Management, Cloud Security, Application Security, Penetration Testing, Internet Service Providers, Fibre Networks, Unified Communications, Contact Centre Platforms, Managed Networks, IoT Platforms, Smart Building Systems, Industrial Automation, Software Development Services, Systems Integration, Managed IT Services, Cloud Migration, DevOps Services, E-Commerce Platforms, Content Management Systems.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Software products:** Developing, Licensing, Implementing, Customizing, Hosting, Supporting
- **Cloud infrastructure:** Provisioning, Hosting, Monitoring, Backing up, Securing, Scaling
- **Cybersecurity:** Assessing, Monitoring, Testing, Responding, Remediating
- **Technology hardware:** Designing, Manufacturing, Importing, Selling, Installing, Maintaining

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Health technology | Healthcare | Developing; implementing; integrating |
| Financial technology | Finance | Processing; onboarding; reporting |
| Property technology | Real Estate | Listing; managing; monitoring |
| Industrial automation | Manufacturing and Industry; Energy | Automating; monitoring; controlling |

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

- The shortlist and all 127 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
