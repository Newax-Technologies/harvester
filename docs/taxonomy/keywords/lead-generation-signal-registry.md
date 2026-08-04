# Harvester Lead-Generation Signal Registry

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This registry defines reusable lead-generation signal profiles that sit above domain and activity identity keywords and below provider-offering qualification.

A domain keyword answers **what the organization is**. An activity keyword answers **what it appears to do**. A lead signal answers **why this organization may be commercially relevant now**.

The locked sequence is:

```text
Selected provider offering
→ eligible sector, domain and activity
→ lead-generation signal profile
→ source-appropriate keyword family
→ evidence candidate
→ corroboration and contradiction review
→ qualification
→ supported opportunity
```

No signal profile may create an opportunity for an inactive provider offering.

## 1. Signal families

| Profile code | Signal type | Purpose | Example phrases or entities | Default freshness | Minimum evidence |
| --- | --- | --- | --- | --- | --- |
| `SIG-DIRECT-001` | `DIRECT_INQUIRY` | Detect a voluntary request directed to the provider or an approved intake channel | request a quote; contact us about; need help with; book consultation; request demo | 30 days | One direct, attributable inquiry |
| `SIG-INTENT-001` | `ACTIVE_PURCHASE_INTENT` | Detect explicit active buying or vendor-selection language | looking for a vendor; seeking supplier; request for proposal; quotation required; vendor required | 60 days | One direct source or two independent indirect sources |
| `SIG-TENDER-001` | `PROJECT_REQUIREMENT` | Detect a formal procurement, tender, grant, or project requirement | tender notice; RFP; RFQ; expression of interest; bid invitation; procurement notice | Until deadline | One authoritative procurement source |
| `SIG-REPLACE-001` | `REPLACEMENT_NEED` | Detect replacement, migration, modernization, or dissatisfaction with an existing solution | replace existing system; migrate from; legacy system; end of support; vendor replacement | 180 days | One direct statement or two corroborating sources |
| `SIG-UPGRADE-001` | `UPGRADE_NEED` | Detect a need to extend or improve an existing capability | upgrade; expand capacity; add module; modernize; integrate new feature; performance improvement | 180 days | One direct or two corroborating sources |
| `SIG-INTEGRATE-001` | `CAPABILITY_GAP` | Detect disconnected tools, manual transfers, duplicate entry, or integration demand | systems do not integrate; manual data transfer; duplicate entry; API integration; data synchronization | 180 days | Two independent indicators unless directly stated |
| `SIG-MANUAL-001` | `OPERATIONAL_PROBLEM` | Detect materially manual workflows and spreadsheet dependence | manual process; spreadsheet based; paper records; manual approval; repetitive data entry | 180 days | Two independent indicators or one direct statement |
| `SIG-VISIBILITY-001` | `OPERATIONAL_PROBLEM` | Detect reporting, visibility, traceability, or management-information problems | no real-time visibility; delayed reports; difficult to track; lack of dashboard; incomplete reporting | 180 days | Two indicators or one direct statement |
| `SIG-QUALITY-001` | `OPERATIONAL_PROBLEM` | Detect recurring errors, rework, inconsistency, or quality failures | frequent errors; rework; inconsistent process; quality issue; reconciliation problem | 120 days | Two corroborating sources or one authoritative finding |
| `SIG-CAPACITY-001` | `OPERATIONAL_PROBLEM` | Detect operational overload, demand growth, backlog, or capacity constraints | backlog; high demand; capacity expansion; overwhelmed; waiting list; delayed fulfilment | 90 days | One direct operational source or two corroborating sources |
| `SIG-HIRING-001` | `HIRING_OR_EXPANSION_EVENT` | Detect hiring that indicates growth, new capability, replacement need, or implementation work | hiring; vacancy; careers; new role; implementation manager; transformation lead | 90 days | One current job posting plus entity match |
| `SIG-EXPAND-001` | `HIRING_OR_EXPANSION_EVENT` | Detect branch, facility, geographic, production, or service expansion | new branch; opening soon; expansion plan; additional facility; new location; increased capacity | 180 days | One authoritative announcement or two independent sources |
| `SIG-LAUNCH-001` | `NEW_BUSINESS_OR_PRODUCT_LAUNCH` | Detect new organizations, brands, products, services, or digital channels | launched; new company; new product; new service; coming soon; newly registered | 120 days | One authoritative or attributable source |
| `SIG-FUNDING-001` | `BUSINESS_EVENT` | Detect funding, investment, grant, acquisition, or budget availability | raised funding; investment round; grant awarded; capital expenditure; approved budget | 180 days | One authoritative financial, registry, or company source |
| `SIG-MA-001` | `BUSINESS_EVENT` | Detect merger, acquisition, ownership change, restructuring, or consolidation | acquired; merger; takeover; new ownership; restructuring; consolidation | 365 days | One authoritative announcement or registry source |
| `SIG-COMPLY-001` | `COMPLIANCE_REQUIREMENT` | Detect compliance deadlines, audit findings, licence obligations, standards, or mandatory reporting | compliance deadline; regulatory requirement; licence renewal; audit finding; certification required | Until obligation expires | One authoritative rule, notice, or organization statement |
| `SIG-CONTRACT-001` | `CONTRACT_OR_RENEWAL_EVENT` | Detect renewal, expiry, retender, support end, or contract change | contract expiry; renewal due; retender; support ending; maintenance contract; subscription renewal | 180 days | One direct or authoritative source |
| `SIG-MAINT-001` | `RECURRING_SERVICE_DUE` | Detect maintenance, inspection, calibration, servicing, replacement, or lifecycle events | maintenance due; calibration due; inspection required; service interval; equipment replacement | According to asset cycle | One asset, service, or authoritative operational record |
| `SIG-LOCATION-001` | `LOCATION_BASED_NEED` | Detect local, branch, property, facility, route, or service-area relevance | near me; service area; new location; branch; site; facility; delivery zone | 90 days | Verified location plus service-delivery fit |
| `SIG-SEASON-001` | `SEASONAL_DEMAND` | Detect recurring seasonal or deadline-driven demand | tax season; admission season; Hajj season; holiday demand; harvest season; annual audit | Event-specific | Known calendar event plus eligible target |
| `SIG-DIGITAL-001` | `CAPABILITY_GAP` | Detect weak or missing digital access, self-service, commerce, portal, booking, or public information | no online booking; no customer portal; manual application; no e-commerce; offline registration | 180 days | Confirmed capability assessment, not website silence alone |
| `SIG-DATA-001` | `CAPABILITY_GAP` | Detect data-control, portability, ownership, duplication, or reporting concerns | data export limitation; data silos; duplicate records; vendor lock-in; no audit trail | 180 days | Direct statement or two corroborating operational indicators |
| `SIG-IOT-001` | `CAPABILITY_GAP` | Detect disconnected physical operations, telemetry, monitoring, or alerting needs | sensor monitoring; telemetry; remote monitoring; equipment alerts; facility monitoring; cold chain | 180 days | Applicable physical operation plus evidence of need or limitation |
| `SIG-SECURITY-001` | `OPERATIONAL_PROBLEM` | Detect access, continuity, backup, incident, or security-control weaknesses | unauthorized access; weak permissions; outage; backup failure; security incident; audit trail missing | 90 days | Authoritative incident, audit, or direct statement; human review required |
| `SIG-TECH-001` | `EXISTING_SOLUTION` | Detect current software, platform, device, vendor, or technology footprint | powered by; using; implemented; integrated with; technology partner; software stack | 365 days | One reliable technical source plus entity match |
| `SIG-COMPETITOR-001` | `EXISTING_SOLUTION` | Detect an existing vendor or competing solution relevant to replacement, integration, or optimization | implementation partner; current vendor; existing platform; managed by; solution provider | 365 days | One attributable source; never an automatic disqualifier |
| `SIG-BUDGET-001` | `BUSINESS_EVENT` | Detect budget, purchase authority, financial capacity, or project scale | approved budget; capital plan; procurement allocation; project value; annual plan | 180 days | One authoritative source or provider-approved inference rule |
| `SIG-CONTACT-001` | `CONTACTABILITY` | Detect a lawful, relevant route to the organization or responsible role | official email; contact form; procurement portal; business phone; named public role | 180 days | Public or authorized contact route plus policy eligibility |
| `SIG-NEGATIVE-001` | `DISQUALIFIER` | Detect conditions that reduce or block pursuit | permanently closed; dissolved; tender cancelled; no longer operating; already awarded; do not contact | Immediate | One authoritative source or two high-confidence sources |

## 2. Signal composition rules

A lead-generation signal is evaluated within a complete context:

```text
provider offering
+
selected sector
+
selected domain
+
approved domain-specific activity
+
signal profile
+
source policy
+
geography and delivery fit
```

The same phrase may have different meaning under different offerings. `Hiring` may indicate growth, internal capability, or reduced outsourcing demand. `Existing software` may indicate replacement, integration, optimization, support, or no opportunity.

## 3. Evidence rules

1. Direct inquiries, authoritative tenders, and attributable procurement notices may qualify as direct evidence.
2. Generic marketing language is normally weak evidence.
3. Website silence is not proof that a capability is absent.
4. Job posts may reveal growth, technology, workflow, or implementation needs but do not prove budget or buying intent.
5. News aggregation and copied press releases count as one evidence origin.
6. A target's own website, official registry, approved procurement portal, or direct inquiry normally outranks an unauthenticated directory.
7. Security, legal, medical, financial, and reputational signals require stricter evidence and human-review rules.
8. Contradictory evidence must be retained and reduce confidence.
9. Signal freshness is measured from the underlying event date where known, not merely the crawl date.
10. A signal that has expired, been cancelled, been awarded, or been superseded must not remain active.

## 4. Opportunity-stage restrictions

The following remain prohibited before an active provider offering is selected:

- service-gap claims;
- buying-readiness claims;
- competitor-displacement claims;
- recommended outreach themes;
- provider-specific commercial scoring;
- contact-ready classification.

This registry supplies reusable signal identities. Offering-specific keyword sets, weights, disqualifiers, and evidence thresholds remain versioned under `OfferingSignalProfile` or an equivalent provider-owned configuration.

## 5. Acceptance criteria

- Every signal has a stable code and universal signal type.
- Every signal defines a freshness policy and minimum evidence rule.
- Direct intent is separated from indirect operational indicators.
- Existing-solution evidence is not treated as automatic disqualification.
- Negative and cancellation signals can suppress stale positive evidence.
- Sensitive signals require stronger evidence and human review.
- Keyword matches remain evidence candidates rather than opportunity proof.
- Runtime implementation is not falsely claimed.
