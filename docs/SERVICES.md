# Harvester Services and Opportunity Model

## Authority and status

Status: **Planned**

This document defines how Harvester represents providers, service offerings, lead subjects, demand signals, qualification rules, and the first-page lead-generation setup.

Harvester is not limited to NEWAX, enterprise software, or B2B infrastructure services. It must support any lawful B2B, B2C, B2B2C, public-sector, referral-based, professional, local, remote, appointment-based, project-based, and recurring service model.

The product rule is:

> **No active offering, no opportunity. No relevant signal, no qualified lead.**

A capability gap is only one possible opportunity signal. It must not be treated as the universal definition of demand.

---

# 1. Product objective

Harvester must help a service provider define:

1. What services they offer.
2. Who can buy or require each service.
3. Where and how the service can be delivered.
4. What evidence indicates a relevant need.
5. What disqualifies a candidate.
6. What legal, ethical, privacy, consent, and contact restrictions apply.
7. How many leads should be generated.
8. Which sources may be used.
9. How strong the evidence must be before a candidate becomes a lead.

Harvester then searches only for opportunities relevant to the provider's active offerings.

It must never create, score, recommend, export, or draft outreach for a service the provider has not selected or created.

---

# 2. Mandatory first-page lead setup

The very first operational page of Harvester must contain the complete lead-definition workflow before the **Generate Leads** button.

The button must not appear as the primary action until the minimum required selections are complete.

## 2.1 First-page structure

```text
Harvester
Find qualified demand for the services you provide.

1. Provider or business type
2. Services offered
3. Customer or lead type
4. Target industries or customer categories
5. Geography and delivery mode
6. Opportunity signals
7. Qualification rules
8. Exclusions and compliance restrictions
9. Sources and evidence threshold
10. Lead quantity and generation mode

[Review Search Definition]
[Generate Leads]
```

The page may use expandable sections, progressive disclosure, or a guided form, but all active selections must remain visible in a final summary before generation begins.

## 2.2 Required selections before generation

The **Generate Leads** button remains disabled until the user has selected or entered:

- At least one active service offering.
- At least one eligible lead-subject type.
- At least one customer market.
- A delivery geography or an explicit remote or international scope.
- At least one applicable opportunity signal.
- A contact and evidence policy.
- A target lead count or bounded generation limit.

Where the selected service belongs to a regulated or sensitive category, the user must also complete the required compliance configuration.

## 2.3 First-page summary

Before generation, Harvester must present a human-readable search definition.

Example:

```text
Provider
Independent graphic designer

Services
Brand identity design
Packaging design

Target customers
New businesses and growing consumer brands

Market
B2B

Geography
Pakistan, remote delivery permitted

Opportunity signals
New business launch
New product launch
Public request for a designer
Visible brand inconsistency

Exclusions
Existing agencies
Businesses outside selected industries
Candidates without a lawful contact route

Evidence threshold
At least one direct signal or two corroborating indirect signals

Requested output
25 qualified leads
```

The user must be able to edit any section before generation.

## 2.4 Saved and reusable searches

The first-page configuration may be saved as a named search profile.

Examples:

- Islamabad corporate-law prospects.
- Remote logo-design opportunities.
- Orthopaedic referral inquiries.
- Emergency plumbing requests within 15 kilometres.
- Tax-filing leads before the annual deadline.

A saved profile stores configuration only. It does not silently reuse stale evidence, expired consent, or previous qualification decisions.

## 2.5 Generation modes

The first page should support:

```text
ONE_TIME
SCHEDULED
CONTINUOUS_MONITORING
IMPORT_AND_QUALIFY
VERIFY_EXISTING_LIST
REFERRAL_INTAKE
DIRECT_INQUIRY_INTAKE
```

Continuous or scheduled generation must require an explicit recurrence, source policy, quota, freshness window, and stop condition.

---

# 3. Universal provider model

## 3.1 Provider profile

Harvester must represent the party seeking leads independently from NEWAX or any single profession.

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

Provider type is descriptive. It must not hardcode qualification logic.

## 3.2 Customer markets

Each offering declares one or more customer markets:

```text
B2B
B2C
B2B2C
PUBLIC_SECTOR
NONPROFIT
PROFESSIONAL_REFERRAL
INTERNAL_OR_GROUP
```

A provider may offer the same service to different markets under separate configurations.

Example:

```text
Graphic design for companies -> B2B
Wedding invitation design -> B2C
White-label design for agencies -> B2B2B or partner channel
```

---

# 4. Universal service offering model

## 4.1 Service offering

Every user must select a suggested service or create a custom service.

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

Only `ACTIVE` offerings participate in lead discovery, qualification, scoring, selection, exports, or outreach preparation.

## 4.2 Delivery modes

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

## 4.3 Pricing models

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

Pricing information may improve qualification but must not be required for every provider.

## 4.4 Suggested and custom services

Harvester should provide editable templates by profession, industry, and provider type.

Templates are suggestions, not restrictions.

The user may:

- Select a suggested service.
- Rename it.
- Add a custom description.
- Create a fully custom service.
- Combine multiple templates.
- Disable irrelevant suggestions.
- Apply different targeting rules to the same service in different markets.

---

# 5. Service catalogue templates

The catalogue should be extensible and versioned. The following groups are initial templates, not a closed list.

## 5.1 Creative services

- Graphic design.
- Brand identity design.
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
- Product visualisation.

## 5.2 Legal services

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
- Legal documentation.
- Company formation.
- Legal advisory retainers.

## 5.3 Healthcare services

- General medical consultation.
- Specialist consultation.
- Diagnostic services.
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

Healthcare lead handling must use consented inquiries, valid referrals, approved campaigns, lawful public information, and configured follow-up rules. Harvester must not infer private diagnoses or exploit sensitive health information.

## 5.4 Business and professional services

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
- Insurance-support services where lawful and approved.
- Business infrastructure.
- Enterprise software.
- Intelligent automation.
- Connected infrastructure.

## 5.5 Home and local services

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

## 5.6 Education services

- School tutoring.
- Test preparation.
- Language instruction.
- Professional training.
- Career counselling.
- Online courses.
- Special-education support.
- Corporate training.
- Academic writing support where lawful.
- Admissions counselling.
- Skills training.

## 5.7 Personal, event, and lifestyle services

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

## 5.8 Property and financial services

- Real-estate brokerage.
- Property management.
- Valuation.
- Mortgage or financing support where lawful.
- Islamic finance services.
- Financial planning where licensed.
- Investment support where licensed.
- Debt recovery where lawful.
- Property inspection.

---

# 6. Lead-subject model

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

Examples:

| Provider | Eligible lead subjects |
| --- | --- |
| Graphic designer | Organization, creator, project, event, person |
| Lawyer | Person, organization, case, referral source |
| Doctor | Patient inquiry, referral source, approved existing-patient follow-up |
| Accountant | Organization, independent professional, person |
| Plumber | Household, person, property, property manager, organization |
| Software provider | Organization, public institution, project |
| Wedding photographer | Person, household, event |
| Tutor | Student, parent, household, school |
| Recruitment firm | Organization, job or contract |
| Real-estate agent | Buyer request, seller request, person, property owner |

The lead-subject model must preserve lawful identity boundaries. A patient inquiry, legal case, household, property, and company must not be forced into one organization record merely because one table was easier to build.

---

# 7. Opportunity signals

## 7.1 Universal signal types

```text
OpportunitySignalType

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
OpportunitySignalType = CAPABILITY_GAP
```

It is not the universal model.

## 7.2 Signal profile

Each offering must define one or more signal profiles.

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

## 7.3 Evidence principles

Harvester must distinguish:

```text
DIRECT_EVIDENCE
CORROBORATING_EVIDENCE
INDIRECT_EVIDENCE
INFERENCE
CONTRADICTORY_EVIDENCE
NO_EVIDENCE
```

Non-detection is not proof of absence.

A missing website feature may indicate a possible capability gap, but it must not automatically prove that the organization lacks the underlying capability.

## 7.4 Example signals

### Graphic designer

Service: `Brand identity design`

Useful signals:

- Newly registered business.
- New product launch.
- Rebranding announcement.
- Public request for a designer.
- New social presence.
- Inconsistent public branding.
- Packaging or campaign launch.
- Hiring or outsourcing request for design work.

### Lawyer

Service: `Corporate contract drafting`

Useful signals:

- Company formation.
- New partnership.
- Vendor expansion.
- Franchise activity.
- Investment or acquisition.
- Employment expansion.
- Public request for contract assistance.
- Explicit contract dispute or review request.

Harvester must not accuse a person or organization of misconduct or invent a legal problem from weak evidence.

### Doctor

Service: `Orthopaedic consultation`

Permitted high-value signals may include:

- Direct appointment inquiry.
- Valid professional referral.
- Consented campaign response.
- Voluntary search or request for the speciality.
- Approved existing-patient follow-up due.
- Location-qualified request for care.

Harvester must not scrape private medical records, infer diagnoses from unrelated activity, or expose sensitive medical information to unauthorised users.

### Accountant

Service: `Tax filing`

Useful signals:

- New business registration.
- Tax deadline.
- Public request for tax help.
- New independent professional.
- Company expansion.
- Existing customer renewal due.

### Plumber

Service: `Emergency plumbing repair`

Useful signals:

- Direct emergency inquiry.
- Local marketplace request.
- Property-manager maintenance request.
- Referral.
- Repeat-maintenance trigger.

### NEWAX

Service: `Business infrastructure assessment`

Useful signals:

- Disconnected systems.
- Repeated manual workflows.
- Limited operational visibility.
- New branch or operational expansion.
- Public procurement or project requirement.
- Existing system replacement or integration need.

NEWAX is one provider configuration within the universal model, not the product's default identity.

---

# 8. Qualification model

## 8.1 Universal opportunity record

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

## 8.2 Qualification rule

An opportunity may be created only when:

```text
Active provider offering
+
Eligible lead-subject type
+
Applicable customer market
+
Geographic or delivery fit
+
Relevant opportunity signal
+
Required evidence threshold
+
Compliance and contact eligibility
=
Qualified or reviewable service opportunity
```

## 8.3 Disqualification examples

- Service is inactive or paused.
- Candidate is outside the service area.
- Candidate belongs to an excluded industry or category.
- Required licence, jurisdiction, or referral condition is not met.
- Evidence is stale or contradictory.
- Candidate is already a customer and the search excludes existing customers.
- No lawful contact route exists.
- Consent is required but absent.
- Conflict-of-interest rule applies.
- Capacity is unavailable.
- Minimum opportunity value is not met.
- Candidate has requested suppression or deletion.

---

# 9. Adaptive scoring

Harvester must not apply one universal scoring formula to every service.

## 9.1 B2B capability service

```text
Industry fit
× capability-gap strength
× organization fit
× decision-maker access
× commercial potential
× evidence confidence
```

## 9.2 B2C local service

```text
Expressed need
× location fit
× urgency
× provider availability
× budget fit
× contactability
```

## 9.3 Legal service

```text
Matter relevance
× jurisdiction fit
× service-type fit
× conflict eligibility
× evidence confidence
× contact or referral permission
```

## 9.4 Healthcare service

```text
Appointment intent
× speciality relevance
× location or telemedicine fit
× referral validity
× service availability
× consent and privacy eligibility
```

## 9.5 Creative service

```text
Project need
× capability or style fit
× timeline
× budget potential
× buyer readiness
× evidence confidence
```

## 9.6 Overall lead score

An overall score may use:

- The highest eligible service-opportunity score.
- The number of distinct qualified opportunities.
- Provider priority.
- Evidence quality.
- Contactability.
- Freshness.
- Commercial potential.

Harvester must not inflate an organization's score using services the provider does not offer.

---

# 10. First-page user controls

## 10.1 Provider and service controls

The first page must let the user:

- Select or create a provider profile.
- Select one or more active services.
- Create a custom service without leaving the page.
- Set priority and capacity for each service.
- Pause a service.
- Define a minimum opportunity value where relevant.

## 10.2 Target controls

The user must be able to select:

- Customer market.
- Lead-subject types.
- Industries or customer categories.
- Organization size where relevant.
- Consumer characteristics only where lawful and non-discriminatory.
- Geography.
- Remote, onsite, hybrid, provider-location, or customer-location delivery.
- Language requirements.
- Jurisdiction, licence, or referral constraints.

## 10.3 Signal controls

For each selected service, the user must be able to:

- Select suggested signals.
- Add a custom signal.
- Set direct or corroborating evidence requirements.
- Set freshness windows.
- Set confidence thresholds.
- Mark a signal as required, preferred, or optional.
- Disable inappropriate signal types.

## 10.4 Exclusion controls

The user must be able to exclude:

- Existing customers.
- Competitors.
- Specific organizations or people.
- Unsupported industries.
- Unsupported case or patient types.
- Conflicts of interest.
- Restricted locations.
- Low-budget opportunities.
- Candidates without verified contact paths.
- Suppressed, opted-out, or deleted subjects.
- Any custom exclusion rule.

## 10.5 Source controls

The user must be able to select approved sources appropriate to the service and lead type.

Examples:

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
- Authorized file imports.

Unavailable, restricted, or unauthorized sources must not appear as active options.

## 10.6 Output controls

The user may define:

- Requested lead count.
- Maximum source cost.
- Maximum generation duration.
- Minimum confidence.
- Minimum score.
- Review-before-acceptance mode.
- Deduplication scope.
- Export or destination preference.
- One-time or recurring operation.

---

# 11. Generate Leads button behaviour

The **Generate Leads** button must:

1. Validate all required selections.
2. Display unresolved configuration errors inline.
3. Present warnings for weak or overly broad definitions.
4. Require confirmation for sensitive or regulated workflows.
5. Freeze a versioned snapshot of the search definition.
6. Create a harvest job using the frozen configuration.
7. Preserve the provider, offerings, signal profiles, sources, exclusions, scoring policy, and compliance policy used.
8. Show the generated job immediately with real backend status.

The button must not:

- Generate generic leads before services are selected.
- Infer services from the provider name without confirmation.
- Add extra services automatically.
- treat every non-detection as a gap.
- Start regulated targeting without required consent and policy configuration.
- Hide which offering caused a candidate to qualify.

---

# 12. Lead result presentation

Every lead must explain its relationship to the selected offering.

Example:

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
Current packaging evidence was incomplete and requires verification.

Evidence confidence
Medium

Recommended next action
Verify the product launch and identify the responsible brand or procurement contact.
```

The user must be able to:

- Filter by service.
- Filter by signal type.
- Confirm or reject an opportunity.
- Correct the service association.
- Mark evidence as insufficient.
- Mark the subject as already served.
- Disable a signal from future searches.
- Request deeper verification.
- Record conversion outcome by service.

---

# 13. Privacy, safety, ethics, and compliance

## 13.1 General rule

Harvester must collect and process only data that is lawful, proportionate, relevant, source-authorized, purpose-bound, and permitted by tenant policy.

## 13.2 Sensitive services

Healthcare, legal, financial, employment, housing, education, and other sensitive categories require additional controls.

Controls may include:

- Consent basis.
- Referral authority.
- Jurisdiction and licence validation.
- Conflict checks.
- Sensitive-field restrictions.
- Stronger access permissions.
- Shorter retention.
- Contact-channel restrictions.
- Mandatory human review.
- Prohibition of unsupported inferences.

## 13.3 Healthcare restrictions

Harvester must not:

- Infer a private diagnosis from unrelated data.
- Scrape private health records.
- Expose patient information to unauthorized users.
- Present an unverified person as having a medical condition.
- Contact a person about a sensitive condition without a lawful basis.

Preferred healthcare lead sources are direct inquiries, valid referrals, consented campaigns, approved directories, and authorized existing-patient workflows.

## 13.4 Legal restrictions

Harvester must not:

- Assert guilt, wrongdoing, liability, or legal need without reliable evidence.
- Use confidential case information without authority.
- Ignore conflict-of-interest rules.
- Present legal advertising or solicitation as compliant without jurisdiction-specific approval.

## 13.5 Protected and discriminatory targeting

Harvester must not qualify or exclude people using protected characteristics where doing so is unlawful, discriminatory, manipulative, or unrelated to service eligibility.

## 13.6 Contact eligibility

A qualified opportunity is not automatically contact-ready.

Contact readiness requires:

- Lawful contact information.
- Channel eligibility.
- Suppression and consent checks.
- Source and purpose compatibility.
- Required human approval.

---

# 14. Core domain records

The implementation should distinguish the following concepts:

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
SearchDefinition
SavedSearchProfile
HarvestJobSnapshot
```

Canonical definitions may be shared across tenants, but provider offerings, targeting, capacity, pricing, signal configuration, and qualification rules remain tenant-owned.

---

# 15. Search-definition snapshot

Every generation run must preserve a complete immutable snapshot containing:

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
scoring_policy_versions
compliance_policy_versions
requested_lead_count
generation_mode
created_by
created_at
```

Later edits affect future runs only unless the user explicitly restarts or reconfigures an active run.

---

# 16. API expectations

The eventual bounded API surface should support:

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

POST   /api/search-definitions/validate
POST   /api/search-definitions
GET    /api/search-definitions/{id}
PATCH  /api/search-definitions/{id}
POST   /api/search-definitions/{id}/generate

GET    /api/service-opportunities
GET    /api/service-opportunities/{id}
POST   /api/service-opportunities/{id}/confirm
POST   /api/service-opportunities/{id}/reject
POST   /api/service-opportunities/{id}/request-verification
```

API names may change during implementation, but the domain boundaries and rules in this document remain authoritative unless explicitly revised.

---

# 17. Acceptance criteria

The services and opportunity model is acceptable only when:

- The first page requires service and target selection before **Generate Leads**.
- A user can configure B2B, B2C, referral, professional, local, remote, appointment, project, and recurring services.
- A user can create fully custom services.
- NEWAX business-infrastructure services work without becoming the universal default.
- Graphic-design services produce creative-project opportunities rather than infrastructure-gap leads.
- Legal services use matter, jurisdiction, consent, referral, and conflict rules.
- Healthcare services use consented inquiries, referrals, privacy controls, and prohibited-inference rules.
- Local services use location, urgency, availability, and direct-demand signals.
- A lead can represent a person, organization, household, property, project, event, case, inquiry, or referral source.
- Capability gap remains one signal type rather than the entire model.
- Unselected and inactive services never affect discovery, scoring, exports, or outreach.
- Every opportunity identifies the service offering and signal that caused qualification.
- Generation freezes a reproducible search-definition snapshot.
- A qualified opportunity is kept separate from contact readiness.
- Sensitive workflows require the configured legal, privacy, consent, and human-review controls.
- The user can review and edit the complete search definition before generation.

---

# 18. Locked implementation rules

1. **No active offering, no opportunity.**
2. **No relevant signal, no qualified lead.**
3. **No lawful contact basis, no contact-ready lead.**
4. **A service gap is one signal type, not the product model.**
5. **The first page defines the search before generation begins.**
6. **The provider controls what they offer and whom they serve.**
7. **Harvester explains why every lead qualified.**
8. **Sensitive services use stronger consent, privacy, and human-review controls.**
9. **Unselected services never influence scoring or outreach.**
10. **Every generation run remains historically reproducible.**
