# Sector Pack Runtime Model

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned; current sector table and documentation registries remain partial**

## 1. Purpose

This document defines how Harvester converts the existing sector, domain, activity, keyword, signal, role, source, and control registries into independently versioned runtime sector packs.

A sector pack is a governed configuration and behavior package. It is not a fork of the application and does not own its own incompatible database schema.

## 2. Universal core and sector overlays

The universal core owns:

- tenants and workspaces;
- entities, relationships, observations, evidence, claims, and provenance;
- providers, offerings, market definitions, jobs, leads, qualifications, opportunities, decisions, and outputs;
- source, compliance, AI, cost, and activation controls.

A sector pack adds:

- sector-specific organization, person, facility, product, service, project, activity, role, pain, need, signal, procurement, employment, data, integration, and compliance definitions;
- conditional input questions;
- evidence and qualification defaults;
- sector-specific output templates;
- validation and benchmark cases.

## 3. Sector pack identity

```text
SectorPack

id
stable_code
name
description
owner
status
created_at
updated_at
```

```text
SectorPackVersion

id
sector_pack_id
version
canonical_sector_registry_version
taxonomy_registry_version
keyword_registry_version
signal_registry_version
role_registry_version
source_guidance_version
compliance_profile_version
input_schema_version
output_schema_version
benchmark_dataset_version
status
created_by
approved_by
activated_at
retired_at
```

An activated version is immutable. New behavior requires a new version.

## 4. Pack contents

Every pack may define:

```text
organization_types
person_types
facility_types
customer_types
buyer_roles
professional_roles
products
services
subservices
projects
activities
employment_models
procurement_models
pricing_models
delivery_modes
pains
needs
desired_outcomes
signals
lead_types
offer_types
data_types
integration_types
compliance_rules
contact_rules
conditional_questions
qualification_defaults
opportunity_capabilities
output_templates
benchmark_cases
```

## 5. Taxonomy relationship

The existing broad-sector, domain, activity, keyword, signal, role, and source registries remain canonical documentation inputs.

Runtime records preserve stable identifiers from those registries. Tenant overlays may:

- add aliases;
- add approved locale terms;
- adjust applicability or weights within allowed bounds;
- disable irrelevant defaults;
- add client-specific exclusions;
- add custom offerings and outputs.

Tenant overlays must not mutate canonical records.

## 6. Domain and activity selection

```text
Broad Sector
→ selected Domains
→ independent Activities per Domain
→ active Provider Offerings
→ signal and evidence profiles
→ source-appropriate query families
→ supported opportunity
```

Selecting an activity for one domain never activates it for another domain.

Keywords discover evidence candidates. They do not independently prove sector, domain, activity, opportunity, authority, consent, contact eligibility, or qualification.

## 7. Conditional input schema

A sector pack defines questions as versioned data:

```text
SectorQuestion

id
sector_pack_version_id
stable_code
question_group
prompt
help_text
response_type
options
required_when
visible_when
validation_rule
sensitivity_classification
maps_to_contract_field
```

Response types may include boolean, text, number, currency, date, date range, single select, multi-select, entity reference, geography, file, and structured group.

Rules use controlled expressions rather than arbitrary executable code.

## 8. Commercial role model

Sector packs distinguish:

- provider;
- customer;
- beneficiary;
- buyer;
- decision-maker;
- influencer;
- approver;
- user;
- regulator;
- referrer;
- partner;
- supplier;
- distributor;
- employer;
- candidate.

A person may hold several roles. Role attribution requires evidence and dates.

## 9. Pain and need model

```text
SectorPainDefinition

id
sector_pack_version_id
stable_code
name
pain_family
description
applicable_entity_types
applicable_activities
severity_guidance
evidence_requirements
prohibited_inferences
```

```text
SectorNeedDefinition

id
sector_pack_version_id
stable_code
name
description
applicable_offerings
required_outcomes
evidence_requirements
```

A pain or need is not inferred from protected or sensitive personal data merely because it could improve targeting.

## 10. Signal model

```text
SectorSignalProfile

id
sector_pack_version_id
stable_code
signal_type
applicable_entities
applicable_domains
applicable_activities
supporting_sources
required_evidence
contradiction_checks
freshness_window
expiry_rule
review_policy
```

Signals include direct inquiry, procurement, hiring, expansion, funding, leadership, technology, accreditation, regulatory, reputation, capacity, replacement, integration, and partnership events.

## 11. Opportunity capability model

Each pack defines capabilities relevant to its organization and project types.

```text
SectorCapabilityDefinition

id
sector_pack_version_id
stable_code
name
capability_family
applicable_entity_types
relevance_rules
condition_scale
business_impact_guidance
evidence_requirements
```

Opportunity Scoring Model v3 evaluates only capabilities made relevant by active market, sector, organization, and offering context.

## 12. Healthcare pack

### 12.1 Default client and organization types

- hospitals and health systems;
- clinics and physician groups;
- dental practices;
- diagnostic laboratories;
- imaging centers;
- rehabilitation, physiotherapy, orthotics, and prosthetics facilities;
- mental-health organizations;
- telemedicine providers;
- home-care and emergency providers;
- pharmacies and long-term-care facilities;
- medical-device, pharmaceutical, biotechnology, diagnostic, and health-technology companies;
- distributors, research organizations, staffing, logistics, facility, and support providers;
- public-health bodies, NGOs, and research institutions.

### 12.2 Buyer and decision roles

- board, owner, chief executive, chief operating and financial officers;
- chief medical, nursing, information, technology, and medical-information officers;
- marketing, growth, operations, procurement, revenue-cycle, quality, compliance, facility, biomedical, laboratory, radiology, pharmacy, human-resources, and service-line leaders;
- practice, department, and program managers.

### 12.3 Default pains and needs

Growth:

- referral leakage;
- poor service-line discovery;
- weak local visibility;
- reputation deterioration;
- unfilled capacity;
- facility launch and expansion.

Operations:

- no-shows;
- call-center delays;
- manual intake;
- scheduling fragmentation;
- equipment downtime;
- inventory shortages;
- repeated data entry;
- staffing constraints.

Data and systems:

- disconnected systems;
- weak interoperability;
- duplicate records;
- manual reporting;
- poor operational visibility;
- consent and security gaps.

### 12.4 Healthcare projects and lead types

Projects include facility mapping, service-line demand, competitor monitoring, referral intelligence, professional outreach, directory correction, facility launch, equipment and supply opportunity discovery, tenders, recruitment, reputation, authorized patient-journey analysis, appointment-funnel analysis, attribution, telehealth entry, and research partnerships.

Lead types include facility, provider group, professional, procurement, tender, partnership, referral, recruitment, distributor, research site, service-line expansion, technology replacement, new facility, and compliance remediation.

### 12.5 Healthcare data boundary

Default marketing and opportunity workflows operate on organization, facility, professional-business, public service, procurement, technology, accreditation, job, publication, and authorized operational data.

Protected health information, patient-level records, inferred medical conditions, and clinical data are prohibited from ordinary marketing workflows unless a separately approved lawful clinical or operational purpose exists. The pack must not convert Harvester into an EHR or patient-marketing database.

### 12.6 Healthcare integrations

Business integrations may include CRM, marketing automation, call tracking, analytics, advertising, reputation, contact center, appointment, and BI systems.

Clinical and operational integrations such as FHIR, HL7, DICOM, EHR, practice management, laboratory, and radiology systems require dedicated authorization, minimum-necessary access, tenant isolation, and audit.

## 13. Education pack

### 13.1 Default client and organization types

- schools and school systems;
- colleges and universities;
- vocational, technical, training, tutoring, language, and test-preparation organizations;
- online academies and certification bodies;
- professional associations and corporate-learning teams;
- publishers, EdTech and learning-content providers;
- student recruitment and research organizations;
- libraries, public education bodies, and NGOs.

### 13.2 Buyer and decision roles

- owner, board, vice chancellor, rector, president, principal, dean, and registrar;
- admissions, marketing, recruitment, program, academic, information-technology, LMS, procurement, finance, student-affairs, corporate-learning, human-resources, research, and international-office leaders.

### 13.3 Default pains and needs

Enrollment:

- low inquiry and application volume;
- slow lead response;
- application abandonment;
- weak program discovery;
- unclear channel attribution;
- international-recruitment friction.

Retention and engagement:

- low learner engagement;
- dropout;
- weak communication;
- low course completion;
- inadequate support;
- poor alumni engagement.

Operations:

- manual admissions;
- disconnected CRM, SIS, and LMS;
- duplicate data;
- manual reporting;
- scheduling and workload constraints;
- document and approval delays.

Strategy:

- unclear employer demand;
- poor program and competitor intelligence;
- pricing uncertainty;
- difficulty launching programs or campuses;
- limited partnership visibility.

### 13.4 Education projects and lead types

Projects include enrollment discovery, admissions-funnel analysis, program demand, competitor program and tuition monitoring, international market mapping, catchment analysis, employer and institutional partnerships, corporate training, scholarship and accreditation monitoring, faculty recruitment, campus feasibility, course launch, and authorized alumni or donor segmentation.

Lead types include institutional client, consented prospective learner, parent inquiry, corporate-training buyer, school or university partner, employer, distributor, content-licensing partner, accreditation, research, recruitment, procurement, and program-expansion opportunity.

### 13.5 Education data boundary

Student records, minor data, protected education records, inferred learning difficulties, and individual academic performance are restricted. Learner-level activation is disabled by default and requires institutional authorization, lawful purpose, consent where required, and strict output policy.

### 13.6 Education integrations

Integrations may include SIS, CRM, LMS, learning record stores, admissions, payments, SSO, LTI, OneRoster, xAPI, SCORM, QTI, Caliper, and SAML. Every integration remains source- and purpose-governed.

## 14. Additional sector packs

The same runtime model applies to Food and Agriculture, Real Estate, Construction, Legal, Finance, Retail, Hospitality, Travel, Manufacturing and Industry, Logistics, Energy, Technology, Government, and Nonprofit packs.

Each pack must undergo sector review, source validation, locale review, benchmark testing, privacy and compliance review, and approved activation. Existing documentation counts do not prove runtime readiness.

## 15. Pack isolation

A Healthcare change must not alter Education or another sector pack unless a shared public contract changes.

Isolation requirements:

- separate version records;
- separate datasets and benchmark sets;
- explicit dependencies;
- contract tests;
- migration declarations;
- release-composition manifests;
- rollback targets;
- no cross-pack mutable globals.

## 16. Pack lifecycle

```text
DRAFT
→ VALIDATION_FAILED or READY_FOR_REVIEW
→ APPROVED
→ ACTIVE
→ SUPERSEDED
→ RETIRED
→ ARCHIVED
```

Stored does not mean active. Approved does not mean selected by a market definition. Selected does not mean a Harvest Job is authorized to run.

## 17. Runtime APIs and UI

Required workspaces include:

- sector-pack catalog;
- version comparison;
- domain and activity selection;
- conditional-question configuration;
- pain, need, signal, role, and capability review;
- locale and source guidance;
- validation and benchmark results;
- tenant overlays;
- activation and rollback;
- audit and affected-market preview.

## 18. Required tests

Tests must prove:

1. a pack change cannot alter unrelated packs;
2. activated versions remain immutable;
3. completed jobs retain exact pack and overlay versions;
4. tenant overrides cannot mutate canonical records;
5. conditional questions produce the same stored contract for repeated inputs;
6. healthcare restrictions block prohibited patient-level marketing data;
7. education restrictions block prohibited student and minor data;
8. keywords cannot directly qualify or score a lead;
9. opportunity capabilities are evaluated only when relevant to active offerings and markets;
10. pack rollback restores the prior approved behavior without rewriting historical jobs.

## 19. Locked rule

> Sector depth belongs in versioned packs. Tenant isolation, evidence semantics, policy controls, and universal entity identity remain shared infrastructure.
