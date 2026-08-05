# Agency, Market and Competitor Intelligence Model

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned; current lead, signal, dossier, export, and audit foundations remain partial**

## 1. Purpose

This document defines the agency operating model and the first-class market and competitor intelligence domains added by the Agency Intelligence re-baseline.

Harvester must support agencies, enterprise growth teams, professional service providers, and internal research teams without turning private client knowledge into a shared data pool.

## 2. Tenant and client hierarchy

```text
Platform
└── Agency or Enterprise Tenant
    ├── Tenant Organization
    ├── Internal Teams
    ├── Shared Approved Assets
    └── Client Workspaces
        └── Client Organization
            ├── Brands
            ├── Business Units
            ├── Markets
            ├── Campaigns
            ├── Research Projects
            └── Integrations
```

A non-agency provider may use one client workspace representing its own organization. The model must not force unnecessary agency terminology into every deployment.

## 3. Agency tenant

```text
AgencyTenantProfile

id
tenant_id
legal_name
display_name
service_catalogue_id
default_branding_profile_id
default_region
default_timezone
operating_model
status
```

Operating models may include:

```text
FULL_SERVICE_AGENCY
PERFORMANCE_AGENCY
CREATIVE_AGENCY
MEDIA_AGENCY
PR_AGENCY
SALES_DEVELOPMENT
RESEARCH_FIRM
IN_HOUSE_GROWTH_TEAM
PROFESSIONAL_SERVICES
OTHER
```

These describe operations. They do not change security or evidence rules.

## 4. Client workspace

```text
ClientWorkspace

id
tenant_id
client_organization_id
workspace_name
service_scope
contract_reference
primary_owner_team_id
confidentiality_classification
retention_policy_id
branding_profile_id
status
created_at
updated_at
```

Every client-specific record, credential, job, source permission, evidence item, entity projection, lead profile, output, cost, and audit event carries workspace scope.

## 5. Data-sharing classes

```text
GLOBAL_PUBLIC_REFERENCE
LICENSED_SHARED_REFERENCE
TENANT_PRIVATE
CLIENT_PRIVATE
USER_PRIVATE
REGULATED_RESTRICTED
```

Sharing rules:

- global public reference data may be reused only when source rights allow it;
- licensed shared data follows provider and contract restrictions;
- agency-private methods and templates may be shared within the tenant;
- client-private evidence, strategies, conversions, contacts, performance, and outcomes remain isolated;
- regulated data receives stricter processing and cannot enter general marketing pools.

## 6. Agency service catalogue

```text
AgencyServiceDefinition

id
tenant_id
stable_code
name
service_family
description
delivery_model
default_outputs
default_workflow_template_id
status
```

Service families may include:

- research and strategy;
- lead generation;
- account-based marketing;
- sales intelligence;
- media planning;
- content and creative;
- campaign operations;
- analytics and measurement;
- marketing automation;
- CRM operations;
- reputation intelligence;
- market entry;
- competitor intelligence;
- partnership development.

## 7. Agency operating lifecycle

```text
Positioning
→ Prospecting
→ Qualification
→ Discovery
→ Research
→ Strategy
→ Proposal
→ Contract
→ Onboarding
→ Planning
→ Production
→ Approval
→ Activation
→ Monitoring
→ Optimization
→ Reporting
→ Renewal
→ Expansion
```

Harvester owns the intelligence and controlled handoff parts of this lifecycle. It does not need to become the agency's accounting, media buying, design, or communication system.

## 8. Agency task taxonomy

### 8.1 Business development

- target-account research;
- trigger monitoring;
- prospect dossiers;
- outreach preparation;
- proposal evidence;
- case-study selection;
- pipeline intelligence;
- partner and referral discovery.

### 8.2 Strategy

- market research;
- customer and buyer research;
- competitor analysis;
- category analysis;
- positioning evidence;
- offer development;
- channel analysis;
- measurement planning.

### 8.3 Campaign and content support

- audience evidence;
- creative and messaging analysis;
- content opportunities;
- campaign briefs;
- approval evidence;
- asset and claim references;
- localization context.

### 8.4 Analytics and reporting

- data intake and reconciliation;
- KPI definitions;
- funnel analysis;
- cohort analysis;
- attribution inputs;
- incrementality evidence;
- market and competitor movement;
- recommendation drafts;
- executive reports.

### 8.5 Client operations

- onboarding;
- approvals;
- action tracking;
- SLA and review queues;
- reporting;
- renewal evidence;
- expansion opportunities.

## 9. Research project

```text
ResearchProject

id
tenant_id
workspace_id
name
project_type
business_question
decision_supported
owner_user_id
owner_team_id
market_definition_ids
source_policy_ids
budget
start_at
due_at
status
```

Project types include:

```text
LEAD_DISCOVERY
MARKET_MAPPING
MARKET_ENTRY
COMPETITOR_MONITORING
PARTNERSHIP_DISCOVERY
PROCUREMENT_MONITORING
CAMPAIGN_ANALYSIS
CUSTOMER_RESEARCH
PRICING_RESEARCH
LOCATION_ANALYSIS
TECHNOLOGY_INTELLIGENCE
CASE_STUDY
```

## 10. Market model

```text
Market

id
tenant_id
workspace_id
stable_reference
name
market_type
geographic_scope
sector_pack_versions
category_ids
customer_markets
languages
valid_from
valid_until
status
```

Market types may include geographic, industry, category, customer, channel, procurement, talent, and technology markets.

## 11. Category model

```text
MarketCategory

id
market_id
canonical_domain_id
name
parent_category_id
description
measurement_definition
status
```

Taxonomy identity and analytical market definitions remain separate. One canonical domain may participate in several client-specific market categories.

## 12. Competitor model

```text
CompetitorProfile

id
tenant_id
workspace_id
organization_entity_id
competitor_type
markets
categories
relationship_to_client
status
created_at
updated_at
```

Competitor types:

```text
DIRECT
INDIRECT
SUBSTITUTE
EMERGING
REGIONAL
CHANNEL
INTERNAL_ALTERNATIVE
DO_NOT_CLASSIFY
```

Competitor status must be evidence-backed and reviewable.

## 13. Competitor observations

First-class competitor observations include:

- products and services;
- pricing and packaging;
- positioning and claims;
- website and experience;
- campaigns and advertising;
- content and publication activity;
- technology footprint;
- hiring and organization changes;
- partnerships;
- locations and expansion;
- customer reviews;
- procurement and contract awards;
- regulatory and accreditation events.

Each observation remains linked to source, evidence, date, market, category, and confidence.

## 14. Competitor change event

```text
CompetitorChangeEvent

id
competitor_profile_id
change_type
before_claim_ids
after_claim_ids
effective_at
detected_at
materiality
markets
categories
confidence_dimensions
review_state
```

Change types include launch, retirement, price change, positioning change, campaign launch, partnership, expansion, leadership change, hiring surge, technology change, and reputation movement.

## 15. Market signal

```text
MarketSignal

id
market_id
category_id
signal_type
subject_entity_id
event_time
detected_time
magnitude
direction
freshness
evidence_ids
source_diversity
confidence_dimensions
expiry_time
status
```

Signals may indicate:

- demand growth or decline;
- funding;
- procurement activity;
- hiring;
- expansion;
- new entrants;
- consolidation;
- pricing movement;
- capacity constraints;
- regulatory change;
- technology adoption;
- reputation trends;
- campaign intensity.

## 16. Analysis types

Harvester intelligence products may use:

```text
DESCRIPTIVE
DIAGNOSTIC
PREDICTIVE
PRESCRIPTIVE
CAUSAL
FUNNEL
COHORT
SEGMENTATION
ATTRIBUTION
INCREMENTALITY
MARKET_SIZING
GEOSPATIAL
COMPETITOR
SHARE_OF_VOICE
SENTIMENT
TOPIC
CREATIVE
MESSAGING
OFFER
PRICING
DEMAND
WHITESPACE
NETWORK
```

The analysis type, methodology, assumptions, source coverage, uncertainty, and applicable decision must be explicit.

## 17. Intelligence product

```text
IntelligenceProduct

id
tenant_id
workspace_id
project_id
product_type
version
input_snapshot_id
methodology_reference
facts
inferences
unknowns
conflicts
recommendations
citations
review_state
created_at
approved_at
```

Product types include:

- account dossier;
- contact dossier;
- market map;
- market report;
- competitor dossier;
- competitor-change report;
- category report;
- trend report;
- demand report;
- location analysis;
- technology report;
- partnership map;
- procurement report;
- campaign brief;
- strategy brief;
- messaging brief;
- creative brief;
- battlecard;
- executive report;
- evidence appendix.

## 18. Case-study model

```text
CaseStudy

id
tenant_id
workspace_id
case_type
client_context
problem
baseline
constraints
hypothesis
intervention
timeline
data_sources
methodology
metrics
evidence
confounding_factors
outcome
attribution_confidence
client_approval
anonymization_state
reusable_lessons
status
```

Case-study types include lead generation, market entry, campaign performance, conversion, retention, automation, operational efficiency, attribution, competitive response, content, media, ABM, and data integration.

Improvement after an intervention does not automatically establish causation. The record distinguishes correlation, contribution, and demonstrated causal impact.

## 19. Output specifications

A workspace may define output profiles for:

- in-application views;
- CSV, JSON, spreadsheet, and report files;
- CRM handoff;
- sales-engagement handoff;
- advertising and analytics handoff;
- Slack or Teams alerts;
- client portals;
- warehouses;
- signed webhooks;
- optional Core and Communicator adapters.

Every output profile specifies fields, redaction, evidence depth, freshness, review, retention, and destination restrictions.

## 20. White-label delivery

White-label configuration may change:

- logo;
- product display name;
- approved colors and typography;
- domain and sender identity;
- report covers;
- terminology labels;
- legal notices.

It must not change:

- tenant isolation;
- evidence semantics;
- compliance controls;
- permissions;
- audit;
- product ownership boundaries;
- customer export rights.

## 21. Outcome feedback

Outcome records may include:

- accepted or rejected lead;
- outreach attempted;
- engagement;
- meeting;
- opportunity;
- won or lost;
- campaign response;
- client acceptance;
- correction;
- invalid or stale record;
- model or policy override.

Feedback creates new evidence and evaluation data. It never rewrites the source material or historical decision that preceded it.

## 22. Agency metrics

Operational metrics include:

- research time saved;
- onboarding time;
- manual actions removed;
- report preparation time;
- approval turnaround;
- source cost and yield;
- cost per verified entity;
- cost per qualified opportunity;
- lead acceptance and conversion;
- evidence coverage;
- client usage;
- renewal and expansion;
- quality debt;
- data-sharing and policy incidents.

## 23. Required tests

Tests must prove:

1. client-private data cannot appear in another client workspace;
2. shared templates do not expose client evidence or outcomes;
3. one public entity may have different client-specific lead profiles without duplicate identity;
4. market and competitor claims remain evidence-backed and dated;
5. competitor changes preserve before and after evidence;
6. case studies distinguish correlation, contribution, and causal evidence;
7. white-label changes cannot weaken controls;
8. outputs enforce workspace, field, suppression, evidence, and destination policy;
9. outcome feedback does not rewrite historical evidence or decisions;
10. reports remain reproducible from pinned input and policy versions.

## 24. Locked rule

> Harvester may reuse approved methods and public reference knowledge. It must never treat one client's private intelligence as another client's raw material.
