# Harvester Services and Opportunity Model

Status: **Normative planned architecture**

Authority:

- [Harvester Standalone Product Roadmap](ROADMAP.md) remains the authoritative 64-module delivery roadmap.
- [Harvester Intelligence Operating Model](architecture/harvester-intelligence-operating-model.md) remains the authority for evidence, decisions, confidence, operations, and learning.
- This document defines the universal provider, service-offering, target, opportunity-signal, qualification, and first-page lead-generation model.
- Provider-specific scoring profiles remain subordinate to this document.

Harvester must support lawful B2B, B2C, B2B2C, public-sector, referral, professional, healthcare, legal, local, remote, appointment, project, emergency, and recurring service models.

Harvester is not limited to NEWAX or business-infrastructure services.

The locked product rule is:

> **No active offering, no opportunity. No relevant signal, no qualified lead. No lawful contact basis, no contact-ready lead.**

A service gap is one possible opportunity signal. It is not the universal lead model.

---

## 1. Product objective

Harvester converts a provider-defined service market into evidence-backed opportunities.

```text
Provider profile
→ active service offerings
→ eligible customer and lead-subject types
→ geography and delivery rules
→ opportunity-signal profiles
→ qualification and exclusion rules
→ approved sources and evidence thresholds
→ reproducible harvest job
→ evidence-backed service opportunities
```

Harvester must never discover, score, recommend, export, publish, or prepare outreach for a service the provider has not activated.

NEWAX business-infrastructure services are one valid provider configuration. They are not the product default.

---

## 2. Mandatory first-page lead definition

The very first operational page must contain the complete lead-definition workflow before the **Generate Leads** button.

A blank dashboard with an eager generation button is not an acceptable product flow.

### 2.1 First-page sequence

```text
Harvester
Find qualified demand for the services you provide.

1. Who is providing the service?
2. What services are being offered?
3. Who can become a lead?
4. Which customer markets, industries, or categories are eligible?
5. Where and how can the service be delivered?
6. What signals indicate relevant demand?
7. What qualifies or disqualifies a candidate?
8. Which sources and evidence standards may be used?
9. What consent, privacy, legal, and contact rules apply?
10. How many leads should be generated and in which mode?

[Review Search Definition]
[Generate Leads]
```

The workflow may use cards, sections, an accordion, or a guided form, but every active choice must remain visible in a final review summary.

### 2.2 Required selections

The **Generate Leads** button remains disabled until the user has provided:

- A provider profile.
- At least one `ACTIVE` service offering.
- At least one eligible customer market.
- At least one eligible lead-subject type.
- Geography or an explicit remote or international scope.
- At least one opportunity signal for every selected service.
- Qualification and exclusion rules.
- An approved source policy.
- An evidence and confidence threshold.
- A contact-eligibility policy.
- A bounded target lead count.
- A generation mode.

Sensitive or regulated services also require the relevant consent, referral, licence, jurisdiction, conflict, privacy, and human-review settings.

### 2.3 First-page review summary

Before generation, Harvester must produce a human-readable search definition.

```text
Provider
Independent graphic designer

Active services
Brand identity design
Packaging design

Customer market
B2B

Eligible leads
New businesses and growing consumer brands

Geography and delivery
Pakistan; remote delivery permitted

Opportunity signals
New business launch
New product launch
Public request for a designer
Visible brand inconsistency

Exclusions
Existing agencies
Unsupported industries
Candidates without a lawful contact route

Evidence standard
One direct signal or two corroborating indirect signals

Requested output
25 qualified leads
```

The user must be able to edit any section without leaving the first page.

### 2.4 Saved search profiles

The complete first-page configuration may be saved and reused.

Examples:

- Islamabad corporate-law prospects.
- Remote brand-identity projects.
- Orthopaedic referral inquiries.
- Emergency plumbing requests within 15 kilometres.
- Tax-filing leads before the annual deadline.
- NEWAX healthcare-infrastructure opportunities.

A saved profile stores configuration. It must not silently reuse expired consent, stale evidence, old scoring outputs, or previous qualification decisions.

### 2.5 Generation modes

```text
ONE_TIME
SCHEDULED
CONTINUOUS_MONITORING
IMPORT_AND_QUALIFY
VERIFY_EXISTING_LIST
REFERRAL_INTAKE
DIRECT_INQUIRY_INTAKE
```

Scheduled and continuous modes require an explicit recurrence, quota, freshness window, source policy, stop condition, and notification policy.

---

## 3. Relationship to MarketDefinition

`MarketDefinition` remains the governed target universe, but it must include the provider and service context required to make a lead commercially relevant.

A market definition must reference:

```text
provider_profile_version
service_offering_versions
customer_markets
lead_subject_types
target_industries_or_categories
geographies
delivery_modes
signal_profile_versions
qualification_rules
exclusion_rules
source_policy_versions
evidence_thresholds
compliance_policy_versions
scoring_profile_versions
```

A sector, location, or organization type without an active service offering is not a complete market definition.

Editing an active definition creates a new version. Completed jobs retain their original meaning.

---

## 4. Provider model

### 4.1 ProviderProfile

```text
ProviderProfile

id
workspace_id
provider_type
business_name
professional_category
industry
service_area
delivery_modes
target_customer_types
status
created_at
updated_at
```

Provider types may include:

```text
COMPANY
AGENCY
INDEPENDENT_PROFESSIONAL
MEDICAL_PRACTICE
LEGAL_PRACTICE
CLINIC
CONTRACTOR
TRADESPERSON
EDUCATOR
CONSULTANT
MARKETPLACE_SELLER
NONPROFIT
PUBLIC_SERVICE_PROVIDER
OTHER
```

Provider type is descriptive. It must not hardcode the lead model.

### 4.2 Customer markets

```text
B2B
B2C
B2B2C
PUBLIC_SECTOR
NONPROFIT
PROFESSIONAL_REFERRAL
INTERNAL_OR_GROUP
```

A provider may configure the same service differently for different customer markets.

---

## 5. Service-offering model

### 5.1 ServiceOffering

```text
ServiceOffering

id
provider_id
service_definition_id
service_name
service_category
description
customer_markets
delivery_modes
pricing_model
geographic_scope
status
capacity
priority
minimum_opportunity_value
qualification_rules
exclusion_rules
created_at
updated_at
```

Statuses:

```text
ACTIVE
PAUSED
PLANNED
DISCONTINUED
```

Only `ACTIVE` offerings participate in discovery, qualification, scoring, selection, export, publication, or outreach preparation.

### 5.2 Delivery modes

```text
ONSITE
REMOTE
HYBRID
AT_PROVIDER_LOCATION
AT_CUSTOMER_LOCATION
DIGITAL_DELIVERY
EMERGENCY
APPOINTMENT_BASED
PROJECT_BASED
RECURRING
REFERRAL_BASED
```

### 5.3 Pricing models

```text
FIXED_PRICE
HOURLY
DAILY
PROJECT_BASED
RETAINER
SUBSCRIPTION
COMMISSION
PER_APPOINTMENT
PER_CASE
PER_SESSION
USAGE_BASED
CUSTOM_QUOTE
FREE_OR_PUBLIC_SERVICE
```

Pricing may improve qualification but is not required for every provider.

### 5.4 Suggested and custom services

Harvester should suggest service templates based on provider type, profession, and industry.

The user may:

- Select a suggested service.
- Rename it.
- Edit its description.
- Create a fully custom service.
- Create different market profiles for the same service.
- Pause or discontinue a service.
- Change service priority and capacity.
- Reject irrelevant suggestions.

The catalogue is assistance, not a cage.

---

## 6. Initial service catalogue

The catalogue is extensible and versioned. These groups are initial templates, not a closed list.

### 6.1 Creative services

- Graphic design.
- Brand identity.
- Logo design.
- Social-media design.
- UI and UX design.
- Illustration.
- Packaging design.
- Motion graphics.
- Video editing.
- Photography.
- Copywriting.
- Print design.
- Presentation design.
- Web design.

### 6.2 Legal services

- Corporate law.
- Contract drafting and review.
- Civil litigation.
- Criminal defence.
- Family law.
- Property law.
- Tax law.
- Intellectual-property law.
- Employment law.
- Immigration law.
- Regulatory compliance.
- Mediation and arbitration.
- Company formation.

### 6.3 Healthcare services

- General consultation.
- Specialist consultation.
- Diagnostics.
- Physiotherapy.
- Rehabilitation.
- Dental care.
- Mental-health services.
- Nutrition services.
- Home healthcare.
- Preventive care.
- Medical follow-up.
- Telemedicine.
- Allied-health services.
- Medical equipment and orthotic services.
- Referral-based care.

Healthcare lead handling must favour direct inquiries, valid referrals, consented campaigns, approved directories, and authorised existing-patient workflows.

### 6.4 Business and professional services

- Accounting.
- Tax preparation.
- Audit support.
- Bookkeeping.
- Recruitment.
- Human-resources services.
- Business consulting.
- Marketing.
- Sales support.
- Procurement.
- Logistics.
- Corporate training.
- Translation.
- Research.
- Business infrastructure.
- Enterprise software.
- Intelligent automation.
- Connected infrastructure.

### 6.5 Home and local services

- Plumbing.
- Electrical work.
- Cleaning.
- Pest control.
- Landscaping.
- Interior design.
- Construction.
- Appliance repair.
- Security installation.
- Moving services.
- Painting.
- Carpentry.
- Air-conditioning service.
- Property maintenance.
- Vehicle repair.

### 6.6 Education services

- School tutoring.
- Test preparation.
- Language instruction.
- Professional training.
- Career counselling.
- Online courses.
- Special-education support.
- Corporate training.
- Admissions counselling.
- Skills training.

### 6.7 Personal, event, and lifestyle services

- Wedding planning.
- Photography.
- Catering.
- Makeup services.
- Tailoring.
- Floristry.
- Decoration.
- Personal training.
- Beauty services.
- Travel planning.
- Event management.
- Baking and gifting.
- Music and entertainment services.

### 6.8 Property and financial services

- Real-estate brokerage.
- Property management.
- Valuation.
- Lawful financing support.
- Islamic finance services.
- Licensed financial planning.
- Licensed investment support.
- Lawful debt recovery.
- Property inspection.

---

## 7. Lead-subject model

A lead is not always an organization.

```text
LeadSubjectType

ORGANIZATION
PERSON
HOUSEHOLD
PROPERTY
PROJECT
EVENT
CASE
PATIENT_INQUIRY
REFERRAL_SOURCE
PUBLIC_INSTITUTION
JOB_OR_CONTRACT
BUYER_REQUEST
SELLER_REQUEST
OTHER
```

| Provider | Eligible lead subjects |
| --- | --- |
| Graphic designer | Organization, creator, project, event, person |
| Lawyer | Person, organization, case, referral source |
| Doctor | Patient inquiry, referral source, approved follow-up |
| Accountant | Organization, professional, person |
| Plumber | Household, person, property, property manager, organization |
| Software provider | Organization, public institution, project |
| Wedding photographer | Person, household, event |
| Tutor | Student, parent, household, school |
| Recruitment firm | Organization, job or contract |
| Real-estate agent | Buyer request, seller request, person, property owner |

A patient inquiry, legal case, household, property, and company must not be collapsed into one organization record.

---

## 8. Opportunity-signal model

### 8.1 Universal signal types

```text
CAPABILITY_GAP
ACTIVE_PURCHASE_INTENT
EXPRESSED_NEED
DIRECT_INQUIRY
REFERRAL
LIFE_EVENT
BUSINESS_EVENT
LEGAL_TRIGGER
MEDICAL_CARE_NEED
COMPLIANCE_REQUIREMENT
PROJECT_REQUIREMENT
REPLACEMENT_NEED
UPGRADE_NEED
OPERATIONAL_PROBLEM
RECURRING_SERVICE_DUE
LOCATION_BASED_NEED
SEASONAL_DEMAND
CONTRACT_OR_RENEWAL_EVENT
HIRING_OR_EXPANSION_EVENT
NEW_BUSINESS_OR_PRODUCT_LAUNCH
PROPERTY_OR_MAINTENANCE_EVENT
OTHER
```

A service gap is represented as:

```text
OpportunitySignal.type = CAPABILITY_GAP
```

It is only relevant when the provider actively offers the related service.

### 8.2 OfferingSignalProfile

```text
OfferingSignalProfile

id
service_offering_id
signal_type
signal_name
description
positive_evidence_rules
negative_evidence_rules
required_evidence
confidence_threshold
freshness_window
qualification_weight
disqualification_rules
privacy_classification
consent_requirement
created_at
updated_at
```

### 8.3 Evidence states

```text
DIRECT_EVIDENCE
CORROBORATING_EVIDENCE
INDIRECT_EVIDENCE
INFERENCE
CONTRADICTORY_EVIDENCE
NO_EVIDENCE
```

Non-detection is not proof of absence.

A missing website feature may support a possible capability gap. It does not automatically prove that the underlying capability is absent.

---

## 9. Service-specific examples

### 9.1 Graphic designer

Offering: `Brand identity design`

Relevant signals:

- New business registration.
- New product launch.
- Rebranding announcement.
- Public request for a designer.
- New social presence.
- Inconsistent public branding.
- Packaging or campaign launch.
- Hiring or outsourcing request for design work.

Harvester must not generate video-production opportunities unless the provider also offers video production.

### 9.2 Lawyer

Offering: `Corporate contract drafting`

Relevant signals:

- Company formation.
- New partnership.
- Vendor expansion.
- Franchise activity.
- Investment or acquisition.
- Employment expansion.
- Public request for contract assistance.
- Explicit contract-review request.

Harvester must not accuse a person or organization of misconduct or invent a legal problem from weak evidence.

### 9.3 Doctor

Offering: `Orthopaedic consultation`

Permitted high-value signals may include:

- Direct appointment inquiry.
- Valid professional referral.
- Consented campaign response.
- Voluntary request for the speciality.
- Approved existing-patient follow-up due.
- Location-qualified request for care.

Harvester must not scrape private health records, infer diagnoses from unrelated activity, or expose sensitive information to unauthorised users.

### 9.4 Accountant

Offering: `Tax filing`

Relevant signals:

- New business registration.
- Tax deadline.
- Public request for tax help.
- New independent professional.
- Company expansion.
- Existing-customer renewal due.

### 9.5 Plumber

Offering: `Emergency plumbing repair`

Relevant signals:

- Direct emergency inquiry.
- Local marketplace request.
- Property-manager maintenance request.
- Referral.
- Repeat-maintenance trigger.

### 9.6 NEWAX

Offering: `Business infrastructure assessment`

Relevant signals:

- Disconnected systems.
- Repeated manual workflows.
- Limited operational visibility.
- Operational expansion.
- Procurement or project requirement.
- Existing system replacement or integration need.

NEWAX-specific infrastructure-gap scoring is a provider-specific scoring profile under this universal model.

---

## 10. Qualification model

### 10.1 ServiceOpportunity

```text
ServiceOpportunity

id
provider_id
service_offering_id
lead_subject_type
lead_subject_id
signal_type
signal_summary
need_status
qualification_status
fit_score
intent_score
confidence_score
urgency_score
commercial_value_score
contactability_score
evidence_references
consent_basis
privacy_classification
recommended_next_action
created_at
expires_at
updated_at
```

Need statuses:

```text
CONFIRMED
STRONGLY_INDICATED
POSSIBLE
UNKNOWN
NOT_RELEVANT
DISQUALIFIED
```

Qualification statuses:

```text
NEW
NEEDS_VERIFICATION
QUALIFIED
REJECTED
CONTACT_READY
REFERRED
CONVERTED
EXPIRED
```

### 10.2 Qualification equation

```text
Active provider offering
+
eligible lead-subject type
+
applicable customer market
+
geographic and delivery fit
+
relevant opportunity signal
+
required evidence threshold
+
compliance eligibility
=
qualified or reviewable service opportunity
```

### 10.3 Common disqualifiers

- Offering is inactive or paused.
- Candidate is outside the service area.
- Candidate belongs to an excluded category.
- Required licence, jurisdiction, or referral condition is not met.
- Evidence is stale or contradictory.
- Existing customer is excluded by the search.
- No lawful contact route exists.
- Required consent is absent.
- Conflict-of-interest rule applies.
- Provider capacity is unavailable.
- Minimum opportunity value is not met.
- Suppression or deletion applies.

---

## 11. Adaptive scoring profiles

Harvester must not apply one universal score formula to every service.

### 11.1 B2B capability service

```text
Industry fit
× capability-gap strength
× organization fit
× decision-maker access
× commercial potential
× evidence confidence
```

### 11.2 B2C local service

```text
Expressed need
× location fit
× urgency
× provider availability
× budget fit
× contactability
```

### 11.3 Legal service

```text
Matter relevance
× jurisdiction fit
× service-type fit
× conflict eligibility
× evidence confidence
× contact or referral permission
```

### 11.4 Healthcare service

```text
Appointment intent
× speciality relevance
× location or telemedicine fit
× referral validity
× service availability
× consent and privacy eligibility
```

### 11.5 Creative service

```text
Project need
× capability or style fit
× timeline
× budget potential
× buyer readiness
× evidence confidence
```

The existing NEWAX infrastructure opportunity model must be treated as one provider-specific profile, not the universal Harvester scoring model.

Unselected services never contribute points.

---

## 12. First-page controls

### 12.1 Provider and offering controls

- Select or create a provider profile.
- Select one or more active services.
- Create a custom service without leaving the page.
- Set priority and capacity.
- Set delivery mode.
- Set minimum opportunity value where relevant.

### 12.2 Target controls

- Customer market.
- Lead-subject types.
- Industries or customer categories.
- Organization size where relevant.
- Geography.
- Remote, onsite, hybrid, provider-location, or customer-location delivery.
- Language requirements.
- Jurisdiction, licence, referral, or eligibility constraints.

### 12.3 Signal controls

For every selected service:

- Select suggested signals.
- Add custom signals.
- Set direct or corroborating evidence requirements.
- Set freshness windows.
- Set confidence thresholds.
- Mark signals required, preferred, or optional.
- Disable inappropriate signal types.

### 12.4 Exclusion controls

- Existing customers.
- Competitors.
- Specific organizations or people.
- Unsupported industries.
- Unsupported matters, cases, or patient categories.
- Conflicts of interest.
- Restricted locations.
- Low-value opportunities.
- Candidates without verified contact paths.
- Suppressed, opted-out, or deleted subjects.
- Custom exclusion rules.

### 12.5 Source controls

Available sources must depend on the service, lead type, tenant policy, legal authority, connector entitlement, and environment.

Possible sources include:

- Public websites.
- Search engines.
- Licensed directories.
- Customer-owned databases.
- Approved APIs.
- Public procurement sources.
- Public business registries.
- Direct inquiries.
- Referral submissions.
- Consented campaign responses.
- Existing-customer records.
- Authorised file imports.

Restricted or unauthorised sources must not appear as active options.

### 12.6 Output controls

- Requested lead count.
- Maximum source cost.
- Maximum duration.
- Minimum confidence.
- Minimum score.
- Review-before-acceptance mode.
- Deduplication scope.
- Export or destination preference.
- One-time or recurring operation.

---

## 13. Generate Leads behaviour

The **Generate Leads** action must:

1. Validate all required selections.
2. Display unresolved errors inline.
3. Warn when the definition is too broad, contradictory, or weakly evidenced.
4. Require confirmation for sensitive or regulated workflows.
5. Freeze a versioned search-definition snapshot.
6. Create a `HarvestJob` using that snapshot.
7. Preserve the provider, offerings, signals, sources, exclusions, scoring profile, and compliance policy used.
8. Show real backend job status immediately.

It must not:

- Generate generic leads before services are selected.
- Infer services from the provider name without confirmation.
- Add extra services automatically.
- Treat every non-detection as a gap.
- Begin regulated targeting without required controls.
- Hide which offering and signal caused qualification.

---

## 14. Lead result presentation

Every result must explain why it is relevant to the selected service.

```text
Lead subject
Northstar Foods

Selected service
Packaging design

Opportunity signal
New product launch

Why it qualified
The provider actively offers packaging design.
The target announced a new consumer product within the configured freshness window.
Current packaging evidence is incomplete and requires verification.

Evidence confidence
Medium

Recommended next action
Verify the launch and identify the responsible brand or procurement contact.
```

The user must be able to:

- Filter by service.
- Filter by signal type.
- Confirm or reject an opportunity.
- Correct the service association.
- Mark evidence insufficient.
- Mark the subject already served.
- Disable a signal for future searches.
- Request deeper verification.
- Record conversion outcome by service.

---

## 15. Privacy, safety, ethics, and compliance

### 15.1 General rule

Harvester processes only data that is lawful, proportionate, relevant, source-authorised, purpose-bound, and permitted by tenant policy.

### 15.2 Sensitive categories

Healthcare, legal, financial, employment, housing, education, and other sensitive services may require:

- Consent basis.
- Referral authority.
- Jurisdiction and licence validation.
- Conflict checks.
- Sensitive-field restrictions.
- Stronger permissions.
- Shorter retention.
- Contact-channel restrictions.
- Mandatory human review.
- Prohibition of unsupported inferences.

### 15.3 Healthcare restrictions

Harvester must not:

- Infer a private diagnosis from unrelated data.
- Scrape private health records.
- Expose patient information to unauthorised users.
- Present an unverified person as having a medical condition.
- Contact a person about a sensitive condition without lawful authority.

### 15.4 Legal restrictions

Harvester must not:

- Assert guilt, wrongdoing, liability, or legal need without reliable evidence.
- Use confidential case information without authority.
- Ignore conflict-of-interest requirements.
- Represent solicitation as compliant without jurisdiction-specific approval.

### 15.5 Contact readiness

A qualified opportunity is not automatically contact-ready.

Contact readiness requires:

- Lawful contact information.
- Channel eligibility.
- Suppression and consent checks.
- Source-purpose compatibility.
- Required human approval.

---

## 16. Core domain objects

```text
ProviderProfile
ServiceDefinition
ServiceOffering
ServiceCategory
CustomerMarket
LeadSubjectType
OfferingTargetProfile
OfferingSignalProfile
OpportunitySignal
ServiceOpportunity
QualificationRule
ExclusionRule
SourcePolicy
EvidenceRequirement
MarketDefinition
SavedSearchProfile
HarvestJobSnapshot
```

Canonical service definitions may be shared across tenants. Provider offerings, targeting, capacity, pricing, signals, qualification, and exclusions remain tenant-owned.

---

## 17. Search-definition snapshot

Every generation run preserves:

```text
provider_profile_version
active_service_offering_versions
customer_markets
lead_subject_types
target_industries_or_categories
geography
delivery_modes
signal_profile_versions
qualification_rules
exclusion_rules
source_policy_versions
evidence_thresholds
scoring_profile_versions
compliance_policy_versions
requested_lead_count
generation_mode
created_by
created_at
```

Later edits apply to future runs only unless the user explicitly creates a replacement job.

---

## 18. Planned API boundaries

```text
GET    /api/provider-profile
PUT    /api/provider-profile

GET    /api/service-definitions
POST   /api/service-offerings
GET    /api/service-offerings
GET    /api/service-offerings/{id}
PATCH  /api/service-offerings/{id}
POST   /api/service-offerings/{id}/pause
POST   /api/service-offerings/{id}/activate

GET    /api/service-offerings/{id}/signal-profiles
POST   /api/service-offerings/{id}/signal-profiles
PATCH  /api/offering-signal-profiles/{id}

POST   /api/market-definitions/validate
POST   /api/market-definitions
GET    /api/market-definitions/{id}
PATCH  /api/market-definitions/{id}
POST   /api/market-definitions/{id}/generate

GET    /api/service-opportunities
GET    /api/service-opportunities/{id}
POST   /api/service-opportunities/{id}/confirm
POST   /api/service-opportunities/{id}/reject
POST   /api/service-opportunities/{id}/request-verification
```

Names may change during implementation, but the domain boundaries and locked rules remain authoritative unless explicitly revised.

---

## 19. Acceptance criteria

The model is acceptable only when:

- All service and targeting selections appear before **Generate Leads** on the first operational page.
- The button stays disabled until the minimum search definition is valid.
- B2B, B2C, referral, professional, local, remote, appointment, project, and recurring services can be configured.
- Fully custom services are supported.
- NEWAX services work without becoming the universal default.
- Graphic-design offerings produce creative-project opportunities.
- Legal offerings use matter, jurisdiction, referral, consent, and conflict rules.
- Healthcare offerings use inquiry, referral, privacy, consent, and prohibited-inference rules.
- Local services use location, urgency, availability, and direct-demand signals.
- Leads may represent people, organizations, households, properties, projects, events, cases, inquiries, and referral sources.
- Capability gap remains one signal type.
- Unselected and inactive services never affect discovery, scoring, export, publication, or outreach.
- Every opportunity identifies the offering and signal that caused qualification.
- Every generation run freezes a reproducible definition.
- Qualified opportunity and contact readiness remain separate.
- Sensitive workflows require configured safeguards.
- The user reviews and edits the complete definition before generation.

---

## 20. Locked implementation rules

1. **No active offering, no opportunity.**
2. **No relevant signal, no qualified lead.**
3. **No lawful contact basis, no contact-ready lead.**
4. **Service gap is one signal type, not the product model.**
5. **The first page defines the market before collection starts.**
6. **The provider controls what they offer and whom they serve.**
7. **Harvester explains why every lead qualified.**
8. **Sensitive services use stronger consent, privacy, and human-review controls.**
9. **Unselected services never influence scoring or outreach.**
10. **Every generation run remains historically reproducible.**
