# Harvester Healthcare Domain Keyword Registry

Part **1 of 2**

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for a portion of the **142** canonical domains in the Healthcare sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-HC-CLI-001-V1` | Hospitals and Health Systems | hospitals and health systems; hospitals & health systems | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-002-V1` | General Medical Clinics | general medical clinics | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-003-V1` | Primary-Care Practices | primary-care practices; primary-care practice | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-004-V1` | Specialist Medical Clinics | specialist medical clinics | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-005-V1` | Diagnostic Laboratories | diagnostic laboratories; diagnostic laboratory; diagnostic labs | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-006-V1` | Diagnostic Imaging Centres | diagnostic imaging centres; diagnostic imaging centers; diagnostic imaging centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-007-V1` | Pharmacies | pharmacies; pharmacy | `ORG-INSTITUTION` | `EX-BROAD` |
| `KW-HC-CLI-008-V1` | Dental Clinics | dental clinics | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-009-V1` | Eye Hospitals and Optical Clinics | eye hospitals and optical clinics; eye hospitals & optical clinics | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-010-V1` | Maternity and Women’s Health Centres | maternity and women’s health centres; maternity and women's health centres; maternity & women's health centres; maternity and women's health centers; maternity and women's health centre; maternity & women’s health centres | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-011-V1` | Fertility and Reproductive Health Centres | fertility and reproductive health centres; fertility & reproductive health centres; fertility and reproductive health centers | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-012-V1` | Dialysis Centres | dialysis centres; dialysis centers; dialysis centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-013-V1` | Cancer Treatment Centres | cancer treatment centres; cancer treatment centers; cancer treatment centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-014-V1` | Cardiac Care Centres | cardiac care centres; cardiac care centers; cardiac care centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-015-V1` | Rehabilitation Centres | rehabilitation centres; rehabilitation centers; rehabilitation centre | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-016-V1` | Physiotherapy Clinics | physiotherapy clinics | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-017-V1` | Orthotics and Prosthetics Clinics | orthotics and prosthetics clinics; orthotics & prosthetics clinics; O&P; orthotic and prosthetic | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-018-V1` | Mental Health and Psychiatry Services | mental health and psychiatry services; mental health & psychiatry services; mental health and psychiatry providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-CLI-019-V1` | Addiction Treatment and Recovery Services | addiction treatment and recovery services; addiction treatment & recovery services; addiction treatment and recovery providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-CLI-020-V1` | Home Healthcare Services | home healthcare services; home health care services; home healthcare service; home medical services; home healthcare providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-CLI-021-V1` | Nursing and Elder-Care Services | nursing and elder-care services; nursing & elder-care services; nursing and elder-care providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-CLI-022-V1` | Ambulance and Emergency Medical Services | ambulance and emergency medical services; ambulance & emergency medical services; ambulance and emergency medical providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-CLI-023-V1` | Blood Banks | blood banks; blood bank | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-024-V1` | Day-Surgery and Ambulatory Care Centres | day-surgery and ambulatory care centres; day-surgery & ambulatory care centres; day-surgery and ambulatory care centers | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-HC-CLI-025-V1` | Medical Tourism Services | medical tourism services; medical tourism service; medical tourism providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-HC-DEV-001-V1` | General Medical Devices | general medical devices; general medical device; general medical equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-002-V1` | Diagnostic Imaging Equipment | diagnostic imaging equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-003-V1` | Laboratory and In-Vitro Diagnostic Equipment | laboratory and in-vitro diagnostic equipment; laboratory & in-vitro diagnostic equipment; laboratory and in vitro diagnostic equipment; IVD; laboratory diagnostic; lab and in-vitro diagnostic equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-004-V1` | Patient Monitoring Equipment | patient monitoring equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-005-V1` | Critical-Care and ICU Equipment | critical-care and icu equipment; critical-care & icu equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-006-V1` | Anaesthesia Equipment | anaesthesia equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-007-V1` | Respiratory and Ventilation Equipment | respiratory and ventilation equipment; respiratory & ventilation equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-008-V1` | Cardiology Devices | cardiology devices; cardiology device | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-009-V1` | Dialysis and Renal-Care Equipment | dialysis and renal-care equipment; dialysis & renal-care equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-010-V1` | Surgical Instruments | surgical instruments; surgical instrument | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-DEV-011-V1` | Operating-Theatre Equipment | operating-theatre equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-012-V1` | Orthopaedic Implants and Devices | orthopaedic implants and devices; orthopaedic implants & devices | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-013-V1` | Orthotics and Prosthetics | orthotics and prosthetics; orthotics & prosthetics; O&P; orthotic and prosthetic | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-DEV-014-V1` | Rehabilitation and Physiotherapy Equipment | rehabilitation and physiotherapy equipment; rehabilitation & physiotherapy equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-015-V1` | Mobility and Assistive Devices | mobility and assistive devices; mobility & assistive devices | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-016-V1` | Dental Equipment and Devices | dental equipment and devices; dental equipment & devices | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-017-V1` | Ophthalmology and Optical Equipment | ophthalmology and optical equipment; ophthalmology & optical equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-018-V1` | ENT Equipment and Devices | ent equipment and devices; ent equipment & devices | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-019-V1` | Urology Equipment and Devices | urology equipment and devices; urology equipment & devices | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-020-V1` | Gynaecology and Obstetric Equipment | gynaecology and obstetric equipment; gynaecology & obstetric equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-021-V1` | Neonatal and Paediatric Equipment | neonatal and paediatric equipment; neonatal & paediatric equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-022-V1` | Emergency and Ambulance Equipment | emergency and ambulance equipment; emergency & ambulance equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-023-V1` | Home Medical Equipment | home medical equipment; home healthcare equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DEV-024-V1` | Biomedical Testing and Calibration Equipment | biomedical testing and calibration equipment; biomedical testing & calibration equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-DIG-001-V1` | Hospital Management Systems | hospital management systems; hospital management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-HC-DIG-002-V1` | Clinic Management Systems | clinic management systems; clinic management system | `ORG-SOFTWARE` | `EX-CLINIC` |
| `KW-HC-DIG-003-V1` | Electronic Medical Record Systems | electronic medical record systems; electronic medical record system; EMR systems; electronic medical records | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-004-V1` | Electronic Health Record Systems | electronic health record systems; electronic health record system; EHR systems; electronic health records | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-005-V1` | Laboratory Information Systems | laboratory information systems; laboratory information system; lab information systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-006-V1` | Radiology Information Systems | radiology information systems; radiology information system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-007-V1` | Picture Archiving and Communication Systems | picture archiving and communication systems; picture archiving & communication systems; PACS; medical imaging archive | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-008-V1` | Pharmacy Management Systems | pharmacy management systems; pharmacy management system | `ORG-SOFTWARE` | `EX-BROAD` |
| `KW-HC-DIG-009-V1` | Appointment and Queue Management Systems | appointment and queue management systems; appointment & queue management systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-010-V1` | Patient Portals | patient portals; patient portal | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-011-V1` | Telemedicine Platforms | telemedicine platforms; telemedicine platform | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-012-V1` | Remote Patient Monitoring Systems | remote patient monitoring systems; remote patient monitoring system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-013-V1` | Healthcare CRM Systems | healthcare crm systems; health care crm systems; healthcare crm system; medical crm systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-014-V1` | Medical Billing and Revenue-Cycle Systems | medical billing and revenue-cycle systems; medical billing & revenue-cycle systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-015-V1` | Healthcare Inventory and Procurement Systems | healthcare inventory and procurement systems; healthcare inventory & procurement systems; health care inventory and procurement systems; medical inventory and procurement systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-016-V1` | Clinical Decision-Support Systems | clinical decision-support systems; clinical decision-support system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-017-V1` | Healthcare Analytics and Reporting Systems | healthcare analytics and reporting systems; healthcare analytics & reporting systems; health care analytics and reporting systems; medical analytics and reporting systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-018-V1` | Medical Practice Management Systems | medical practice management systems; medical practice management system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-019-V1` | Health Information Exchange Systems | health information exchange systems; health information exchange system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-DIG-020-V1` | Healthcare Compliance and Documentation Systems | healthcare compliance and documentation systems; healthcare compliance & documentation systems; health care compliance and documentation systems; medical compliance and documentation systems | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-HC-MED-001-V1` | Prescription Pharmaceuticals | prescription pharmaceuticals; prescription pharmaceutical; prescription medicines | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-002-V1` | Generic Medicines | generic medicines; generic medicine; generic medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-003-V1` | Over-the-Counter Medicines | over-the-counter medicines; over-the-counter medicine; over-the-counter medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-004-V1` | Biological Medicines | biological medicines; biological medicine; biological medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-005-V1` | Biosimilars | biosimilars; biosimilar | `ORG-GENERIC` | `EX-BROAD` |
| `KW-HC-MED-006-V1` | Vaccines and Immunization Products | vaccines and immunization products; vaccines & immunization products | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-HC-MED-007-V1` | Specialty Medicines | specialty medicines; specialty medicine; specialty medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-008-V1` | Oncology Medicines | oncology medicines; oncology medicine; oncology medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-009-V1` | Cardiovascular Medicines | cardiovascular medicines; cardiovascular medicine; cardiovascular medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-010-V1` | Diabetes and Endocrine Medicines | diabetes and endocrine medicines; diabetes & endocrine medicines; diabetes and endocrine medications | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-HC-MED-011-V1` | Neurology and Psychiatric Medicines | neurology and psychiatric medicines; neurology & psychiatric medicines; neurology and psychiatric medications | `ORG-GENERIC` | `EX-PHRASE` |

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
