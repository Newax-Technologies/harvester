# Harvester Education Product and Service Domain Registry

Status: **Proposed**

Version: **1.0**

Date: **3 August 2026**

Implementation status: **Not implemented.** This document defines the approved product and service domains for broad sector `BS-002 Education`.

Authority:

- [Harvester Standalone Product Roadmap](../ROADMAP.md) remains the authoritative delivery roadmap.
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md) remains authoritative for evidence, decisions, confidence, operations, and learning.
- [Harvester Services and Opportunity Model](../SERVICES.md) remains authoritative for provider offerings, target markets, opportunity signals, qualification, and generation rules.
- [Broad Sector Registry and Selection Framework](broad-sector-registry.md) remains authoritative for broad-sector selection and sector-to-domain behaviour.
- This document defines the controlled domain registry for `BS-002 Education` and is subordinate to those documents.

## 1. Purpose

This registry defines the product and service domains that may appear after a user selects **Education** as a broad sector.

The field is named **Product or Service Domain** because target organizations may deal with physical products, digital products, professional services, institutional services, infrastructure, regulated activities, or combinations of them.

The locked hierarchy is:

```text
Education
→ one or more product or service domains
→ separate activity group for every selected domain
→ approved domain–activity combinations
→ provider services
→ service-specific keywords and evidence
→ supported service gap or other opportunity signal
→ qualified opportunity
→ lead
```

## 2. Governing rules

1. Selecting Education does not automatically select every domain in this registry.
2. A user may select one or more domains.
3. Every selected domain receives its own independent activity group.
4. Activities selected for one domain must not propagate to another domain.
5. The same canonical domain may also be mapped to another broad sector without creating a duplicate domain record.
6. Domain overlap must not duplicate organizations, evidence, opportunities, or scores.
7. A domain supplies market context; it does not prove that a target performs a particular activity.
8. Only approved domain–activity combinations may proceed to provider-service selection.
9. Only services actively offered by the provider may be assessed for gaps or other opportunities.
10. Keywords create evidence signals; they do not independently prove an activity, gap, or qualified opportunity.
11. Sector, domain, activity, provider offering, keyword profile, evidence profile, and scoring-profile versions must remain traceable.
12. Custom domains may be proposed, but Harvester should map them to canonical definitions or aliases where possible.

## 3. Domain families

This registry contains **95 canonical domains** organized into **6 families**.

| Family code | Domain family | Canonical domains |
| --- | --- | --- |
| `EDU-INS` | Education institutions | 22 |
| `EDU-TRN` | Training and professional development | 14 |
| `EDU-DIG` | Digital education and learning technology | 18 |
| `EDU-CON` | Educational content and publishing | 13 |
| `EDU-RES` | Research and knowledge services | 12 |
| `EDU-SUP` | Education operations and support | 16 |

## 4. Canonical domain registry

### 4.1 Education institutions

| Code | Product or service domain |
| --- | --- |
| `EDU-INS-001` | Early Childhood Education Centres |
| `EDU-INS-002` | Primary Schools |
| `EDU-INS-003` | Secondary Schools |
| `EDU-INS-004` | Higher Secondary Schools |
| `EDU-INS-005` | International Schools |
| `EDU-INS-006` | Boarding Schools |
| `EDU-INS-007` | Special Education Schools |
| `EDU-INS-008` | Religious Education Institutions |
| `EDU-INS-009` | Technical and Vocational Institutes |
| `EDU-INS-010` | Community Colleges |
| `EDU-INS-011` | Colleges |
| `EDU-INS-012` | Universities |
| `EDU-INS-013` | Graduate and Postgraduate Institutions |
| `EDU-INS-014` | Medical Colleges |
| `EDU-INS-015` | Dental Colleges |
| `EDU-INS-016` | Nursing Colleges |
| `EDU-INS-017` | Allied Health Institutes |
| `EDU-INS-018` | Engineering Universities |
| `EDU-INS-019` | Business Schools |
| `EDU-INS-020` | Law Colleges |
| `EDU-INS-021` | Teacher Education Institutions |
| `EDU-INS-022` | Distance-Learning Institutions |

### 4.2 Training and professional development

| Code | Product or service domain |
| --- | --- |
| `EDU-TRN-001` | Corporate Training Providers |
| `EDU-TRN-002` | Professional Certification Providers |
| `EDU-TRN-003` | Skills Development Centres |
| `EDU-TRN-004` | Language Learning Centres |
| `EDU-TRN-005` | Test Preparation Centres |
| `EDU-TRN-006` | Coaching Academies |
| `EDU-TRN-007` | Tutoring Services |
| `EDU-TRN-008` | Leadership Development Providers |
| `EDU-TRN-009` | Sales Training Providers |
| `EDU-TRN-010` | Safety Training Providers |
| `EDU-TRN-011` | Technical Training Providers |
| `EDU-TRN-012` | Healthcare Training Providers |
| `EDU-TRN-013` | Teacher Training Providers |
| `EDU-TRN-014` | Continuing Professional Education Providers |

### 4.3 Digital education and learning technology

| Code | Product or service domain |
| --- | --- |
| `EDU-DIG-001` | Learning Management Systems |
| `EDU-DIG-002` | Student Information Systems |
| `EDU-DIG-003` | School Management Systems |
| `EDU-DIG-004` | University Management Systems |
| `EDU-DIG-005` | Admissions Management Systems |
| `EDU-DIG-006` | Examination Management Systems |
| `EDU-DIG-007` | Online Learning Platforms |
| `EDU-DIG-008` | Virtual Classroom Platforms |
| `EDU-DIG-009` | Digital Assessment Platforms |
| `EDU-DIG-010` | Remote Proctoring Systems |
| `EDU-DIG-011` | Education Content Platforms |
| `EDU-DIG-012` | Learning Experience Platforms |
| `EDU-DIG-013` | Adaptive Learning Systems |
| `EDU-DIG-014` | Education Analytics Systems |
| `EDU-DIG-015` | Parent and Student Portals |
| `EDU-DIG-016` | Digital Credentialing Platforms |
| `EDU-DIG-017` | Academic Scheduling Systems |
| `EDU-DIG-018` | Library Management Systems |

### 4.4 Educational content and publishing

| Code | Product or service domain |
| --- | --- |
| `EDU-CON-001` | Textbook Publishing |
| `EDU-CON-002` | Academic Publishing |
| `EDU-CON-003` | Digital Courseware |
| `EDU-CON-004` | Educational Video Content |
| `EDU-CON-005` | Assessment Content |
| `EDU-CON-006` | Question Banks |
| `EDU-CON-007` | Curriculum Development |
| `EDU-CON-008` | Instructional Design |
| `EDU-CON-009` | Learning Materials and Teaching Aids |
| `EDU-CON-010` | Children's Educational Content |
| `EDU-CON-011` | Professional Reference Content |
| `EDU-CON-012` | Open Educational Resources |
| `EDU-CON-013` | Translation and Localization for Education |

### 4.5 Research and knowledge services

| Code | Product or service domain |
| --- | --- |
| `EDU-RES-001` | Research Institutes |
| `EDU-RES-002` | Think Tanks |
| `EDU-RES-003` | Policy Research Centres |
| `EDU-RES-004` | University Research Centres |
| `EDU-RES-005` | Laboratories and Innovation Centres |
| `EDU-RES-006` | Academic Journals |
| `EDU-RES-007` | Research Data Services |
| `EDU-RES-008` | Research Ethics and Review Services |
| `EDU-RES-009` | Grant Management Services |
| `EDU-RES-010` | Academic Conference Services |
| `EDU-RES-011` | Knowledge Management Services |
| `EDU-RES-012` | Institutional Repositories |

### 4.6 Education operations and support

| Code | Product or service domain |
| --- | --- |
| `EDU-SUP-001` | Education Consultancy |
| `EDU-SUP-002` | Admissions and Enrolment Services |
| `EDU-SUP-003` | Student Recruitment Services |
| `EDU-SUP-004` | Scholarship and Financial-Aid Services |
| `EDU-SUP-005` | Education Verification Services |
| `EDU-SUP-006` | Accreditation Services |
| `EDU-SUP-007` | Examination Boards |
| `EDU-SUP-008` | Certification Bodies |
| `EDU-SUP-009` | Student Accommodation Services |
| `EDU-SUP-010` | School Transport Services |
| `EDU-SUP-011` | Campus Catering Services |
| `EDU-SUP-012` | Campus Facilities Management |
| `EDU-SUP-013` | Education Staffing and Recruitment |
| `EDU-SUP-014` | Education Procurement |
| `EDU-SUP-015` | Alumni Management Services |
| `EDU-SUP-016` | Career Services and Placement |

## 5. First-release presentation shortlist

The canonical registry remains complete, but the initial interface should present a smaller high-level shortlist and allow search, family filtering, and expansion into the full registry.

The shortlist contains **30 presentation entries**:

1. Schools
2. Universities
3. Colleges
4. Technical and Vocational Institutes
5. Training Providers
6. Test Preparation Centres
7. Online Learning Platforms
8. Learning Management Systems
9. Student Information Systems
10. School Management Systems
11. Admissions Management Systems
12. Examination Management Systems
13. Virtual Classroom Platforms
14. Digital Assessment Platforms
15. Education Content Platforms
16. Textbook Publishing
17. Curriculum Development
18. Research Institutes
19. Academic Publishing
20. Certification Bodies
21. Accreditation Services
22. Education Consultancy
23. Student Recruitment Services
24. Scholarship Services
25. Library Management Systems
26. Academic Scheduling Systems
27. Parent and Student Portals
28. Career Services and Placement
29. Campus Facilities Management
30. Education Staffing and Recruitment

Presentation labels may group several canonical domains for usability. Storage, evidence, mappings, and completed harvest jobs must continue to use stable canonical IDs rather than mutable display labels.

## 6. Domain-specific activity examples

Activities come from a shared canonical activity library, but each selected domain receives its own allowed and recommended activity set.

### Schools and universities

- Teaching
- Assessing
- Certifying
- Admissions
- Student support
- Researching
- Publishing

### Learning Management Systems

- Developing
- Licensing
- Implementing
- Integrating
- Hosting
- Supporting

### Educational content

- Authoring
- Publishing
- Licensing
- Distributing
- Translating
- Updating

### Training providers

- Training
- Assessing
- Certifying
- Consulting
- Delivering online
- Scheduling

The system must not transfer an activity selection from one domain to another merely because both domains belong to Education.

## 7. Cross-sector reuse examples

A canonical domain may appear under several broad sectors without being duplicated.

| Canonical domain | Additional broad sectors | Example activities |
| --- | --- | --- |
| Learning Management Systems | Technology | Developing; licensing; implementing; hosting |
| Medical Colleges | Healthcare | Teaching; clinical training; certifying |
| Student Accommodation | Real Estate; Hospitality | Leasing; operating; managing |
| Education Publishing | Technology; Retail | Publishing; licensing; selling |

Cross-sector mappings provide context. They must not duplicate the target organization, source evidence, opportunity, or score.

## 8. Minimum data requirements

Each canonical domain requires:

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

`domain_type` should support:

```text
PHYSICAL_PRODUCT
DIGITAL_PRODUCT
PROFESSIONAL_SERVICE
INSTITUTIONAL_SERVICE
INFRASTRUCTURE
RAW_MATERIAL
REGULATED_ACTIVITY
PUBLIC_PROGRAM
```

Sector mapping and domain activity applicability remain many-to-many relationships. They must not be embedded as unversioned arrays that cannot be audited or migrated safely.

## 9. Product behaviour and safeguards

- Selecting a broad sector only filters the domain catalogue.
- Selecting a domain does not activate every available activity.
- Every selected domain displays an independent activity group.
- The user must approve each domain–activity combination before services are attached.
- A paused domain or combination stops new discovery without deleting historical evidence.
- Aliases improve discovery and search but do not create additional canonical identities.
- Duplicate sector mappings must not duplicate organizations, observations, evidence, opportunities, exports, or outreach packages.
- A domain match alone must never be treated as proof of need.
- Service gaps are evaluated only for services the provider has activated for the approved target combination.
- Unsupported or unselected services must not influence lead scoring.
- Completed jobs retain the exact registry, mapping, offering, keyword, evidence, and scoring versions used when they ran.

## 10. Acceptance criteria

- The interface exposes the first-release shortlist and permits access to all 95 canonical domains.
- A user can select several domains under Education.
- Every selected domain receives a separate activity group.
- Activities selected for one domain do not propagate to another domain.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized independently.
- Canonical codes remain stable when display labels or aliases change.
- Cross-sector mappings reuse canonical domain identity.
- The same target organization is not duplicated when it matches several sectors or combinations.
- Every opportunity records the sector, domain, activity, provider offering, evidence, decision, and version path that produced it.
- No unselected service or unsupported gap influences discovery, qualification, ranking, export, publication, or outreach preparation.
- Existing harvest jobs preserve the registry and mapping versions used when they ran.
- Search, filtering, pagination, and accessibility remain usable with the full registry.

## 11. Delivery boundary

This document defines the `BS-002 Education` domain dataset and selection rules.

It does not implement database records, migrations, APIs, interfaces, activity mappings, service catalogues, keyword profiles, evidence rules, or scoring behaviour.

The registry is **defined**, but it is not **implemented**, **integrated**, **CI Green**, or **complete** until the corresponding schema, migration, API, interface, validation, security, test, and release work is verified.
