# Harvester Healthcare Product and Service Domain Registry

Status: **Proposed**

Version: **1.0**

Date: **3 August 2026**

Implementation status: **Not implemented.** This document defines the approved product and service domains for broad sector `BS-001 Healthcare`.

Authority:

- [Harvester Standalone Product Roadmap](../ROADMAP.md) remains the authoritative delivery roadmap.
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md) remains authoritative for evidence, decisions, confidence, operations, and learning.
- [Harvester Services and Opportunity Model](../SERVICES.md) remains authoritative for provider offerings, target markets, opportunity signals, qualification, and generation rules.
- [Broad Sector Registry and Selection Framework](broad-sector-registry.md) remains authoritative for broad-sector selection and sector-to-domain behaviour.
- This document defines the controlled domain registry for `BS-001 Healthcare` and is subordinate to those documents.

## 1. Purpose

This registry defines the product and service domains that may appear after a user selects **Healthcare** as a broad sector.

The label is deliberately **Product or Service Domain**, not merely product. Healthcare includes physical products, medicines, devices, facilities, professional services, digital systems, operational services, research, education, and public-health programs.

The locked hierarchy is:

```text
Healthcare
→ one or more healthcare product or service domains
→ separate activity group for every selected domain
→ approved domain–activity combinations
→ provider services
→ service-specific keywords and evidence
→ supported service gap or other opportunity signal
→ qualified opportunity
→ lead
```

## 2. Governing rules

1. Selecting Healthcare does not automatically select every healthcare domain.
2. A user may select one or more healthcare domains.
3. Every selected domain receives its own independent activity group.
4. Activities selected for one healthcare domain must not propagate to another domain.
5. The same canonical domain may also be mapped to another broad sector without creating a duplicate domain record.
6. Domain overlap must not duplicate organizations, evidence, opportunities, or scores.
7. A domain is market context. It does not prove that a target performs a particular activity.
8. Only approved domain–activity combinations may proceed to provider-service selection.
9. Only services actively offered by the provider may be assessed for gaps or other opportunities.
10. Keywords create evidence signals; they do not independently prove an activity, service gap, or qualified opportunity.

## 3. Domain families

Healthcare domains are organized into eight families.

| Family code | Domain family | Purpose |
| --- | --- | --- |
| `HC-MED` | Medicines and therapeutics | Medicines, vaccines, biological products, therapeutic categories, and clinical nutrition |
| `HC-DEV` | Medical devices and equipment | Diagnostic, monitoring, treatment, surgical, rehabilitation, assistive, and home-care equipment |
| `HC-SUP` | Medical supplies and consumables | Disposable, protective, laboratory, wound-care, sterilization, transfusion, and packaging supplies |
| `HC-CLI` | Healthcare facilities and clinical services | Hospitals, clinics, diagnostics, pharmacy, rehabilitation, emergency, home-care, and specialist services |
| `HC-DIG` | Digital health and healthcare software | Clinical, operational, patient, analytics, billing, exchange, and decision-support systems |
| `HC-OPS` | Healthcare operations and support | Staffing, billing, claims, maintenance, facilities, logistics, warehousing, waste, and procurement services |
| `HC-RES` | Research, testing and education | Clinical research, trials, biomedical research, certification, accreditation, and healthcare education |
| `HC-PUB` | Public and community healthcare | Public health, community programs, screening, vaccination, occupational health, and preventive services |

## 4. Canonical healthcare domain registry

### 4.1 Medicines and therapeutics

| Code | Product or service domain |
| --- | --- |
| `HC-MED-001` | Prescription Pharmaceuticals |
| `HC-MED-002` | Generic Medicines |
| `HC-MED-003` | Over-the-Counter Medicines |
| `HC-MED-004` | Biological Medicines |
| `HC-MED-005` | Biosimilars |
| `HC-MED-006` | Vaccines and Immunization Products |
| `HC-MED-007` | Specialty Medicines |
| `HC-MED-008` | Oncology Medicines |
| `HC-MED-009` | Cardiovascular Medicines |
| `HC-MED-010` | Diabetes and Endocrine Medicines |
| `HC-MED-011` | Neurology and Psychiatric Medicines |
| `HC-MED-012` | Antibiotics and Anti-Infective Medicines |
| `HC-MED-013` | Respiratory Medicines |
| `HC-MED-014` | Gastrointestinal Medicines |
| `HC-MED-015` | Dermatology Medicines |
| `HC-MED-016` | Ophthalmic Medicines |
| `HC-MED-017` | Women's Health and Fertility Medicines |
| `HC-MED-018` | Anaesthesia and Critical-Care Medicines |
| `HC-MED-019` | Rare-Disease and Orphan Medicines |
| `HC-MED-020` | Herbal and Traditional Healthcare Products |
| `HC-MED-021` | Clinical Nutrition Products |
| `HC-MED-022` | Medical Nutrition and Enteral Feeding Products |

### 4.2 Medical devices and equipment

| Code | Product or service domain |
| --- | --- |
| `HC-DEV-001` | General Medical Devices |
| `HC-DEV-002` | Diagnostic Imaging Equipment |
| `HC-DEV-003` | Laboratory and In-Vitro Diagnostic Equipment |
| `HC-DEV-004` | Patient Monitoring Equipment |
| `HC-DEV-005` | Critical-Care and ICU Equipment |
| `HC-DEV-006` | Anaesthesia Equipment |
| `HC-DEV-007` | Respiratory and Ventilation Equipment |
| `HC-DEV-008` | Cardiology Devices |
| `HC-DEV-009` | Dialysis and Renal-Care Equipment |
| `HC-DEV-010` | Surgical Instruments |
| `HC-DEV-011` | Operating-Theatre Equipment |
| `HC-DEV-012` | Orthopaedic Implants and Devices |
| `HC-DEV-013` | Orthotics and Prosthetics |
| `HC-DEV-014` | Rehabilitation and Physiotherapy Equipment |
| `HC-DEV-015` | Mobility and Assistive Devices |
| `HC-DEV-016` | Dental Equipment and Devices |
| `HC-DEV-017` | Ophthalmology and Optical Equipment |
| `HC-DEV-018` | ENT Equipment and Devices |
| `HC-DEV-019` | Urology Equipment and Devices |
| `HC-DEV-020` | Gynaecology and Obstetric Equipment |
| `HC-DEV-021` | Neonatal and Paediatric Equipment |
| `HC-DEV-022` | Emergency and Ambulance Equipment |
| `HC-DEV-023` | Home Medical Equipment |
| `HC-DEV-024` | Biomedical Testing and Calibration Equipment |

### 4.3 Medical supplies and consumables

| Code | Product or service domain |
| --- | --- |
| `HC-SUP-001` | Medical Disposables |
| `HC-SUP-002` | Syringes, Needles and Injection Products |
| `HC-SUP-003` | Surgical Consumables |
| `HC-SUP-004` | Wound-Care and Dressing Products |
| `HC-SUP-005` | Infection-Control Products |
| `HC-SUP-006` | Sterilization and Disinfection Products |
| `HC-SUP-007` | Personal Protective Equipment |
| `HC-SUP-008` | Hospital Linen and Patient-Care Supplies |
| `HC-SUP-009` | Medical Gases |
| `HC-SUP-010` | Blood-Bank and Transfusion Supplies |
| `HC-SUP-011` | Laboratory Reagents and Consumables |
| `HC-SUP-012` | Diagnostic Test Kits |
| `HC-SUP-013` | Pharmacy Supplies |
| `HC-SUP-014` | Medical Packaging and Medicine Containers |

### 4.4 Healthcare facilities and clinical services

| Code | Product or service domain |
| --- | --- |
| `HC-CLI-001` | Hospitals and Health Systems |
| `HC-CLI-002` | General Medical Clinics |
| `HC-CLI-003` | Primary-Care Practices |
| `HC-CLI-004` | Specialist Medical Clinics |
| `HC-CLI-005` | Diagnostic Laboratories |
| `HC-CLI-006` | Diagnostic Imaging Centres |
| `HC-CLI-007` | Pharmacies |
| `HC-CLI-008` | Dental Clinics |
| `HC-CLI-009` | Eye Hospitals and Optical Clinics |
| `HC-CLI-010` | Maternity and Women's Health Centres |
| `HC-CLI-011` | Fertility and Reproductive Health Centres |
| `HC-CLI-012` | Dialysis Centres |
| `HC-CLI-013` | Cancer Treatment Centres |
| `HC-CLI-014` | Cardiac Care Centres |
| `HC-CLI-015` | Rehabilitation Centres |
| `HC-CLI-016` | Physiotherapy Clinics |
| `HC-CLI-017` | Orthotics and Prosthetics Clinics |
| `HC-CLI-018` | Mental Health and Psychiatry Services |
| `HC-CLI-019` | Addiction Treatment and Recovery Services |
| `HC-CLI-020` | Home Healthcare Services |
| `HC-CLI-021` | Nursing and Elder-Care Services |
| `HC-CLI-022` | Ambulance and Emergency Medical Services |
| `HC-CLI-023` | Blood Banks |
| `HC-CLI-024` | Day-Surgery and Ambulatory Care Centres |
| `HC-CLI-025` | Medical Tourism Services |

### 4.5 Digital health and healthcare software

| Code | Product or service domain |
| --- | --- |
| `HC-DIG-001` | Hospital Management Systems |
| `HC-DIG-002` | Clinic Management Systems |
| `HC-DIG-003` | Electronic Medical Record Systems |
| `HC-DIG-004` | Electronic Health Record Systems |
| `HC-DIG-005` | Laboratory Information Systems |
| `HC-DIG-006` | Radiology Information Systems |
| `HC-DIG-007` | Picture Archiving and Communication Systems |
| `HC-DIG-008` | Pharmacy Management Systems |
| `HC-DIG-009` | Appointment and Queue Management Systems |
| `HC-DIG-010` | Patient Portals |
| `HC-DIG-011` | Telemedicine Platforms |
| `HC-DIG-012` | Remote Patient Monitoring Systems |
| `HC-DIG-013` | Healthcare CRM Systems |
| `HC-DIG-014` | Medical Billing and Revenue-Cycle Systems |
| `HC-DIG-015` | Healthcare Inventory and Procurement Systems |
| `HC-DIG-016` | Clinical Decision-Support Systems |
| `HC-DIG-017` | Healthcare Analytics and Reporting Systems |
| `HC-DIG-018` | Medical Practice Management Systems |
| `HC-DIG-019` | Health Information Exchange Systems |
| `HC-DIG-020` | Healthcare Compliance and Documentation Systems |

### 4.6 Healthcare operations and support

| Code | Product or service domain |
| --- | --- |
| `HC-OPS-001` | Healthcare Staffing and Recruitment |
| `HC-OPS-002` | Medical Billing Services |
| `HC-OPS-003` | Healthcare Claims Administration |
| `HC-OPS-004` | Biomedical Equipment Maintenance |
| `HC-OPS-005` | Medical Equipment Installation |
| `HC-OPS-006` | Medical Equipment Calibration |
| `HC-OPS-007` | Hospital Facility Management |
| `HC-OPS-008` | Healthcare Laundry Services |
| `HC-OPS-009` | Healthcare Catering and Nutrition Services |
| `HC-OPS-010` | Medical Waste Management |
| `HC-OPS-011` | Healthcare Cleaning and Infection-Control Services |
| `HC-OPS-012` | Pharmaceutical Cold-Chain Services |
| `HC-OPS-013` | Healthcare Logistics and Distribution |
| `HC-OPS-014` | Medical Warehousing |
| `HC-OPS-015` | Hospital Procurement Services |

### 4.7 Research, testing and education

| Code | Product or service domain |
| --- | --- |
| `HC-RES-001` | Clinical Research Organizations |
| `HC-RES-002` | Clinical Trials |
| `HC-RES-003` | Pharmaceutical Research |
| `HC-RES-004` | Medical Device Research |
| `HC-RES-005` | Biomedical Research |
| `HC-RES-006` | Medical Testing and Certification |
| `HC-RES-007` | Healthcare Quality Accreditation |
| `HC-RES-008` | Medical Education |
| `HC-RES-009` | Nursing Education |
| `HC-RES-010` | Allied Health Education |
| `HC-RES-011` | Continuing Medical Education |
| `HC-RES-012` | Healthcare Simulation and Training |

### 4.8 Public and community healthcare

| Code | Product or service domain |
| --- | --- |
| `HC-PUB-001` | Public Health Services |
| `HC-PUB-002` | Community Health Services |
| `HC-PUB-003` | Healthcare NGOs |
| `HC-PUB-004` | Maternal and Child Health Programs |
| `HC-PUB-005` | Vaccination Programs |
| `HC-PUB-006` | Disease-Screening Programs |
| `HC-PUB-007` | Occupational Health Services |
| `HC-PUB-008` | School Health Services |
| `HC-PUB-009` | Corporate Health and Wellness Services |
| `HC-PUB-010` | Preventive Healthcare Services |

## 5. First-release presentation shortlist

The canonical registry contains 142 domains. The initial user interface should present the following 40 high-level choices and reveal narrower domains through search, expansion, or guided refinement.

| Priority | First-release domain |
| --- | --- |
| 1 | Pharmaceuticals |
| 2 | Vaccines |
| 3 | Biological Medicines |
| 4 | Clinical Nutrition |
| 5 | General Medical Devices |
| 6 | Diagnostic Imaging |
| 7 | Laboratory Diagnostics |
| 8 | Patient Monitoring |
| 9 | Critical-Care Equipment |
| 10 | Surgical Equipment |
| 11 | Orthopaedic Devices |
| 12 | Orthotics and Prosthetics |
| 13 | Rehabilitation Equipment |
| 14 | Dental Equipment |
| 15 | Ophthalmology Equipment |
| 16 | Home Medical Equipment |
| 17 | Medical Consumables |
| 18 | Wound Care |
| 19 | Infection Control |
| 20 | Laboratory Supplies |
| 21 | Hospitals |
| 22 | Clinics |
| 23 | Diagnostic Laboratories |
| 24 | Imaging Centres |
| 25 | Pharmacies |
| 26 | Dental Clinics |
| 27 | Rehabilitation Services |
| 28 | Mental Health Services |
| 29 | Home Healthcare |
| 30 | Emergency Medical Services |
| 31 | Digital Health |
| 32 | Hospital Management Systems |
| 33 | Electronic Medical Records |
| 34 | Telemedicine |
| 35 | Healthcare Analytics |
| 36 | Biomedical Equipment Services |
| 37 | Healthcare Logistics |
| 38 | Medical Warehousing |
| 39 | Clinical Research |
| 40 | Public and Community Health |

The shortlist is a presentation layer. It must not replace the canonical domain IDs or collapse historically distinct selections.

## 6. Domain-specific activity groups

Activities come from the shared canonical activity library, but every healthcare domain receives its own allowed and recommended activity mapping.

### 6.1 Pharmaceuticals example

Recommended activities may include:

```text
Researching
Developing
Formulating
Manufacturing
Processing
Quality testing
Packaging
Importing
Exporting
Distributing
Wholesaling
Warehousing
Cold storing
Promoting
Marketing
Retail selling
Disposing
```

### 6.2 Medical devices example

Recommended activities may include:

```text
Designing
Researching
Manufacturing
Assembling
Testing
Certifying
Importing
Exporting
Distributing
Wholesaling
Warehousing
Selling
Reselling
Installing
Calibrating
Maintaining
Repairing
Leasing
Refurbishing
Recycling
```

### 6.3 Hospitals and health systems example

Recommended activities may include:

```text
Providing inpatient care
Providing outpatient care
Diagnosing
Treating
Performing procedures
Managing appointments
Managing emergencies
Operating facilities
Procuring supplies
Managing pharmacies
Managing laboratories
Managing imaging
Managing patient records
Billing
Referring patients
Training staff
```

### 6.4 Healthcare software example

Recommended activities may include:

```text
Developing
Publishing
Licensing
Implementing
Customizing
Integrating
Hosting
Operating
Reselling
Maintaining
Supporting
Training
```

An activity selected for Pharmaceuticals must not automatically apply to Medical Devices, Hospitals, Healthcare Software, or another selected domain.

## 7. Cross-sector mappings

A healthcare domain may also appear under another broad sector when the market context is genuinely relevant.

| Canonical domain | Additional broad-sector context | Example activities |
| --- | --- | --- |
| Pharmaceuticals | Manufacturing and Industry | Manufacturing; packaging; quality testing |
| Pharmaceuticals | Logistics | Distribution; warehousing; cold storage |
| Medical Devices | Manufacturing and Industry | Manufacturing; assembling; testing |
| Medical Devices | Retail | Selling; reselling; leasing |
| Healthcare Software | Technology | Developing; licensing; integrating; hosting |
| Medical Warehousing | Logistics | Warehousing; fulfilment; cold storage |
| Clinical Research | Education | Researching; training; publishing |
| Healthcare NGOs | Nonprofit | Delivering programs; fundraising; community services |
| Public Health Services | Government | Administering; regulating; monitoring; delivering programs |

A cross-sector mapping must preserve one canonical domain identity and one evidence history.

## 8. Minimum data requirements

Each healthcare domain record should support:

```text
id
code
name
domain_family
domain_type
description
status
version
parent_domain_id
first_release_visible
search_aliases
created_at
updated_at
```

Recommended `domain_type` values:

```text
PHYSICAL_PRODUCT
MEDICINE_OR_THERAPEUTIC
MEDICAL_DEVICE
SUPPLY_OR_CONSUMABLE
CLINICAL_SERVICE
HEALTHCARE_FACILITY
DIGITAL_PRODUCT
PROFESSIONAL_SERVICE
OPERATIONAL_SERVICE
RESEARCH_OR_EDUCATION
PUBLIC_OR_COMMUNITY_SERVICE
```

Sector mapping should remain separate:

```text
SectorDomainApplicability

sector_id
domain_id
applicability
default_priority
qualification_guidance
status
version
```

Domain-to-activity mapping should remain separate:

```text
DomainActivityApplicability

domain_id
activity_id
applicability
recommended
priority
qualification_guidance
status
version
```

## 9. Selection and relevance safeguards

- The user may search, filter, expand, and select several healthcare domains.
- Selecting a parent or shortlist label must not silently select every child domain.
- A domain selection must record the exact canonical ID and registry version.
- Activities must be configured separately for every selected domain.
- Harvester must require approval of each domain–activity combination.
- Services must be selected for each approved target combination rather than inherited indiscriminately from Healthcare.
- Keywords and evidence rules must be specific to the selected domain, activity, and provider service.
- A target matching multiple domains must remain one resolved organization with multiple attributed classifications.
- A target's self-description is evidence of classification, not automatic proof of every activity or capability.
- Non-detection of a product, activity, or system must not be converted into confirmed absence without sufficient evidence.
- Regulated, sensitive, clinical, patient, or personal data must remain subject to source authorization, consent, privacy, retention, access, and human-review controls.

## 10. Non-negotiable relevance chain

```text
No Healthcare sector selection
→ no Healthcare domains presented

No Healthcare domain selected
→ no domain-specific activities presented

No approved domain–activity combination
→ no provider services assessed for that combination

No active provider service
→ no service gap or opportunity for that service

No relevant evidence
→ no supported opportunity

No qualified opportunity
→ no lead
```

## 11. Acceptance criteria

- The canonical registry contains all 142 healthcare domains defined in this document.
- Every domain has a stable code, family, status, and version.
- The interface initially presents the 40-domain shortlist without deleting or replacing the full registry.
- A user can select multiple healthcare domains.
- Every selected domain displays its own activity group.
- Activity selections do not propagate between healthcare domains.
- Cross-sector mappings reuse canonical domain IDs rather than creating duplicates.
- The user can approve, disable, pause, and prioritize individual domain–activity combinations.
- Harvester records the sector, domain, activity, provider offering, keyword profile, evidence, and decision path behind every resulting opportunity.
- A target organization is not duplicated when it matches several healthcare domains or sectors.
- Unselected services and unsupported gaps do not affect scoring, exports, publication, or outreach preparation.
- Completed harvest jobs retain the healthcare registry, mapping, activity, service, keyword, and policy versions used when they ran.

## 12. Delivery boundary

This document defines the Healthcare domain registry and selection behaviour only.

It does not claim that the registry, schema, migrations, APIs, interface, domain-specific activities, provider service mappings, keyword profiles, evidence policies, scoring, or lead generation are implemented.

The registry is **defined**, but it is not **implemented**, **integrated**, **CI green**, or **complete** until the corresponding product work is delivered and verified.