# Harvester Provider-Offering Keyword Profile Standard

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Domain and activity keywords identify what an organization is and does. They cannot answer whether the organization has a need that matches a service offered by a provider. This document defines the separate provider-offering keyword layer required for commercially relevant lead generation.

## 1. Eligibility gate

```text
Active provider
→ active provider offering
→ selected target sectors
→ selected target domains
→ approved activities for each domain
→ approved offering-signal profile
→ evidence assessment
```

A service not offered by the provider must not:

- create a gap;
- affect opportunity scoring;
- produce outreach messaging;
- influence daily selection;
- appear in exports;
- create contact-ready status.

## 2. Offering profile layers

| Layer | Purpose |
| --- | --- |
| Offering identity | Canonical service name, aliases, exclusions |
| Applicable market | Eligible sectors, domains, activities, sizes, geographies |
| Direct intent | Explicit request, tender, quotation, demo, vendor search |
| Operational pain | Problems the offering can legitimately address |
| Existing solution | Current platform, equipment, vendor, manual workaround |
| Replacement | Legacy, end-of-life, dissatisfaction, migration, retender |
| Integration | Disconnected tools, duplicate entry, API, synchronization |
| Upgrade and expansion | Capacity, branch, location, users, modules, performance |
| Compliance and risk | Applicable obligations and evidence thresholds |
| Maintenance lifecycle | Inspection, calibration, support, renewal, replacement |
| Business event | Funding, hiring, merger, facility launch, new contract |
| Buying-stage | Research, planning, approved budget, procurement, award |
| Decision function | Likely operational owner and supporting functions |
| Disqualifier | No fit, completed project, unsupported geography, inactive entity |
| Contradiction | Awarded, cancelled, renewed elsewhere, capability already confirmed |
| Evidence threshold | Direct, authoritative, corroborated, indirect, inference |
| Freshness | Validity by event and source type |
| Contact policy | Lawful route and permitted preparation state |

## 3. Signal strength

| Level | Meaning | Example |
| --- | --- | --- |
| `S5_DIRECT` | Explicit request or formal procurement | active RFP for warehouse system |
| `S4_STRONG` | Directly stated problem, replacement, integration, or approved project | migrating from legacy EMR |
| `S3_CORROBORATED` | Several independent indicators aligned to the offering | new branches + operations hiring + manual process description |
| `S2_INDIRECT` | Plausible but circumstantial evidence | rapid growth and spreadsheets mentioned |
| `S1_EXPLORATORY` | Vocabulary or market context only | organization is a distributor |
| `S0_NONE` | No offering-relevant evidence | domain match only |

Only `S5`, `S4`, or policy-approved `S3` evidence should normally reach opportunity review. Lower levels remain research context.

## 4. Required profile fields

```text
offering_profile_id
provider_id
provider_offering_id
version
status
service_identity_terms
eligible_sector_ids
eligible_domain_ids
eligible_activity_ids
organization_size and geography rules
direct_intent_terms
procurement_terms
problem_signal_terms
replacement_terms
integration_terms
upgrade_terms
existing_solution_terms
competitor_or_vendor_terms
compliance_terms
maintenance_terms
business_event_terms
decision_role_profile_ids
contact_route_profile_ids
exclusion and contradiction terms
source suitability
freshness windows
evidence thresholds
precision modes
sensitive-sector policy
benchmark_set_id
review and approval metadata
```

## 5. Problem-signal rule

A problem term must describe an operational condition that the selected offering can plausibly address.

Bad profile:

```text
Offering: CRM
Keywords: growth; digital; customer; efficiency
```

These are vague and commercially meaningless.

Better profile:

```text
Offering: CRM and lead-management system
Direct signals: CRM RFP; lead-management software required
Pain signals: leads tracked in spreadsheets; missed follow-up; duplicate customer records
Integration signals: website leads manually copied; CRM not connected to ERP
Existing solution: current CRM; Salesforce; HubSpot; custom database
Replacement signals: migrate CRM; CRM contract expiry; legacy CRM
Contradictions: CRM implementation completed; tender awarded; no longer seeking vendor
```

## 6. Example: Warehouse Management System

### Eligible combinations

- Pharmaceuticals + Warehousing
- Food Products + Cold Storage
- Retail Products + Fulfilment
- Logistics + Warehousing
- Manufacturing + Inventory and Storage

### Direct intent

- warehouse management system RFP;
- WMS vendor required;
- warehouse software quotation;
- inventory and warehouse platform procurement.

### Operational pain

- stock mismatch;
- manual picking list;
- paper-based receiving;
- delayed dispatch;
- no bin-level visibility;
- expiry and batch tracking difficulty;
- inventory reconciliation backlog;
- temperature excursion not linked to stock;
- multiple warehouses with separate records.

### Existing solution and technology

- WMS;
- ERP inventory module;
- barcode system;
- handheld scanning;
- spreadsheet inventory;
- legacy warehouse software.

### Expansion and event signals

- new distribution centre;
- warehouse expansion;
- new fulfilment facility;
- cold-store commissioning;
- hiring warehouse systems manager.

### Exclusions and contradictions

- warehouse property for rent with no operating business context;
- academic WMS research;
- implementation completed;
- tender awarded;
- facility permanently closed.

## 7. Existing-solution interpretation

An existing solution may indicate:

```text
replacement
integration
optimization
support
migration
additional module
multi-site rollout
contract renewal
no opportunity
```

The system must not treat the presence of a competitor or existing product as automatic disqualification or automatic replacement intent.

## 8. Gap-state vocabulary

```text
UNASSESSED
INSUFFICIENT_COVERAGE
CAPABILITY_NOT_OBSERVED
CAPABILITY_INDICATED
CAPABILITY_CONFIRMED
LIMITATION_INDICATED
LIMITATION_CONFIRMED
REPLACEMENT_INDICATED
INTEGRATION_INDICATED
PROJECT_CONFIRMED
NO_CURRENT_OPPORTUNITY
CONTRADICTED
```

`CAPABILITY_NOT_OBSERVED` is not `CAPABILITY_CONFIRMED_ABSENT`.

## 9. Buying-stage states

```text
UNAWARE_OR_UNKNOWN
RESEARCHING
PROBLEM_RECOGNIZED
REQUIREMENTS_FORMING
BUDGET_OR_PROJECT_INDICATED
VENDOR_DISCOVERY
FORMAL_PROCUREMENT
EVALUATION
AWARDED_OR_COMMITTED
IMPLEMENTING
LIVE_OR_RENEWAL
CANCELLED_OR_DEFERRED
```

The state requires dated evidence and can regress or expire.

## 10. Acceptance criteria

- Every commercial signal is tied to an active provider offering.
- Eligible domains and activities are explicit.
- Direct intent is separated from indirect pain and growth indicators.
- Existing solutions support several interpretations.
- Absence is never inferred from website silence.
- Contradiction and completion signals can suppress stale opportunities.
- Sensitive-sector signals use stronger evidence and review.
- Decision-role and contact discovery occur only after organization resolution and opportunity gates.
- The profile includes a benchmark set and rollback path.
- Runtime implementation is not falsely claimed.
