# NEWAX Lead Harvester

Lead Harvester is the lead-discovery, verification, qualification, and audience-preparation infrastructure used to convert fragmented public and authorized source evidence into canonical, reviewable business opportunities.

It is not intended to be a generic scraper. The target system must let a user define a market, run the correct workflow for each selected source, observe the real backend process, review evidence-backed leads, and pass an approved audience into Communicator or NEWAX Core.

> **Product principle:** Define the market. Let the infrastructure discover, verify, resolve, qualify, and prepare the opportunities while the operator remains in control.

---

## Document status

This README has three responsibilities:

1. Explain the backend and commands that exist in the repository today.
2. Define the required next-generation backend and product workflow that is **planned but not yet fully implemented**.
3. Define the locked frontend design system, page architecture, secure integration-management experience, and frontend delivery sequence.

The distinction matters. A detailed architecture diagram is not proof that the software already performs the workflow. Markdown remains tragically incapable of executing Python.

### Status terms

- **Current:** Present in the repository today.
- **Partial:** Some required models or services exist, but the complete product workflow is not connected.
- **Correction pending:** Implemented in an open correction branch or PR but not yet integrated into `master`.
- **Planned:** Required architecture that still needs implementation and verification.
- **Restricted:** Must not be enabled until source-access, security, legal, compliance, and operational requirements are approved.

---

# 1. Product journey

The target user journey is:

```text
Generate Leads
→ Define lead type, sector, geography, source mix, quantity, and quality rules
→ Create Harvest Job
→ Watch source-specific processing in Harvest Run
→ Review the frozen results in Generated Leads
→ Search canonical organizations in Master Leads
→ Open a complete Lead Dossier
→ Export selected leads or create a Communicator campaign
→ Send qualified commercial opportunities to NEWAX Core
```

The principal product pages are:

1. **Generate Leads** — configure the market and create a harvest job.
2. **Harvest Runs** — list, search, and monitor every job.
3. **Harvest Run** — show real backend progress separately for every source.
4. **Generated Leads** — show the frozen results of one completed harvest job.
5. **Master Leads** — show canonical leads across all previous harvests.
6. **Lead Dossier** — show all current facts, contacts, evidence, scores, history, compliance, and communication readiness for one organization.
7. **Qualification Policies** — manage versioned sector- and objective-specific qualification rules.
8. **Communicator** — create controlled campaigns from approved selected leads.
9. **Secrets & Integrations** — securely configure and rotate source and service credentials.
10. **Operations** — monitor jobs, source health, failures, audit history, and event delivery.

---

# 2. Current implementation

## 2.1 Current entry points

The main ingestion pipeline is currently started through the CLI:

```bash
lead-harvester run --config job.yaml
```

The CLI loads `job.yaml`, creates `LeadPipeline`, and invokes `LeadPipeline.run()`.

Other current CLI operations include:

```bash
lead-harvester import-authorized ...
lead-harvester qualify-leads ...
lead-harvester select-daily-leads ...
lead-harvester verify-data-quality ...
lead-harvester export-leads ...
lead-harvester process-outbox ...
lead-harvester linkedin-run ...
lead-harvester linkedin-research ...
lead-harvester linkedin-send ...
```

The FastAPI service currently exposes routes for institutions, lead profiles, resolution reviews, sectors, compliance, verification, daily selection, exports, operations, outbox, manual leads, and outreach draft review.

## 2.2 Current ingestion flow

```text
YAML configuration
→ Select one source mode
→ Collect source records
→ Persist SourceRun and RawSourceRecord data
→ Normalize name, phone, domain, and location
→ Generate entity-resolution candidates
→ Score match candidates
→ Merge, attach, create, or send to human review
→ Create or update canonical institution, branches, contacts, and provenance
→ Persist detected signals
→ Refresh LeadProfile and score history
→ Complete or fail SourceRun
```

## 2.3 Current source-selection limitation

`LeadPipeline.run()` currently selects one ingestion branch through an `if/elif` chain. A single invocation runs one of the following paths:

- Authorized import
- Website crawling and optional Brave Search seed discovery
- Telegram
- Apple Maps
- Yandex Maps
- Google Places

A single parent job coordinating several selected sources does not yet exist.

## 2.4 Current canonical data model

The backend already provides important foundations:

- `SourceRun`
- `RawSourceRecord`
- `RawPageSnapshot`
- `CanonicalInstitution`
- `Branch`
- `ContactPoint`
- `PersonCandidate`
- `FieldProvenance`
- `ResolutionCandidate`
- `MatchAssessment`
- `Sector`
- `QualificationAssessment`
- `Signal`
- `ResearchJob`
- `ResearchFinding`
- `LeadProfile`
- `LeadScoreSnapshot`
- `LeadReservation`
- `SuppressionEntry`
- `DataQualityFlag`
- `EventOutbox`
- `AccountBrief`
- `OutreachDraft`
- `OutreachOutcome`

These models must be reused or evolved. The planned job system must not create a second competing lead database merely because naming fresh tables feels productive.

## 2.5 Current entity resolution

Incoming raw records are normalized and compared using:

- Exact normalized phone match
- Exact normalized domain match
- Geographic proximity plus name similarity

Candidate pairs are assessed as:

```text
MERGE
PENDING
LINK_ONLY
REJECT
```

Ambiguous matches remain unresolved for human review. Confident matches enrich an existing canonical institution or create a new canonical institution.

## 2.6 Current scoring and qualification

A `LeadProfile` is refreshed after normal ingestion changes canonical data. Current scoring considers:

- Scale
- Contactability
- Category fit
- Qualification
- Research signals
- Freshness
- Identity confidence

The profile also calculates:

- Size tier
- Operational maturity
- ICP match
- Website-quality tier
- Service-gap score
- Organization summary

The existing sector layer supports limited sector-specific rules. The complete versioned, objective-specific policy system described below is planned.

## 2.7 Current exports and outreach

Current exports support CSV and JSON with operating-status, score, qualification, and sector filters. Current outreach follows:

```text
AccountBrief
→ OutreachDraft
→ Human review and approval
→ OutreachAutomator
→ Email or professional-network send
→ OutreachOutcome
```

Daily lead reservations and selected Master Leads are not yet connected to a full Communicator campaign model.

---

# 3. Required next-generation architecture

## 3.1 Architectural rule

The planned architecture must use:

> **One stable Harvest Job orchestration standard with an independently upgradable workflow for each source.**

Google Places, Yandex Maps, Apple Maps, public websites, authorized imports, Telegram, and professional-network data have different access methods, pagination, evidence, rate limits, failure modes, entity types, and upgrade cycles.

They must have separate internal workflows, but they must not have separate incompatible job models, status vocabularies, event formats, evidence formats, or frontend applications.

## 3.2 Common Harvest Job orchestrator

The parent orchestrator owns:

- Requested market
- Lead type and objective
- Selected sectors and organization types
- Geography
- Source mix
- Target accepted lead count
- Candidate budget
- Quality mode
- Required data
- Exclusions
- Overall state
- Pause, resume, retry, and cancellation
- Accepted result count
- Errors and warnings
- Cost and quota usage
- Audit trail
- Frozen result snapshot

## 3.3 Source-specific workflow engine

Each connector owns:

- Credential and capability validation
- Source-specific planning
- Query generation or crawl planning
- Pagination or traversal
- Rate-limit handling
- Source-specific retries
- Source-specific evidence collection
- Source-specific checkpoints
- Source-specific metrics
- Source API compatibility
- Connector and workflow versions

All connectors emit a common normalized evidence contract into shared resolution, enrichment, qualification, and scoring services.

---

# 4. Planned Harvest Job data model

The exact schema must be validated against existing models and migrations before implementation.

## 4.1 `HarvestJob`

Represents the complete user request.

Suggested responsibilities:

```text
id
name
status
lead_type
quality_mode
target_count
minimum_accepted_count
maximum_candidates
requested_by
configuration_snapshot
started_at
completed_at
paused_at
cancelled_at
failure_code
failure_message
created_at
updated_at
```

## 4.2 `HarvestSourceRun`

Represents one selected source inside a parent job.

```text
id
harvest_job_id
source_type
status
connector_version
workflow_version
normalization_version
source_api_version
taxonomy_version
configuration_snapshot
capability_snapshot
started_at
completed_at
failure_code
failure_message
```

The existing `SourceRun` should be evolved or linked to this role rather than duplicated without a migration strategy.

## 4.3 `HarvestStageRun`

Represents one backend-defined source stage.

```text
id
harvest_source_run_id
stage_key
stage_name
stage_description
stage_order
status
processed_count
total_count
metrics
warning_count
error_count
started_at
completed_at
last_heartbeat_at
failure_code
failure_message
```

## 4.4 `HarvestJobEvent`

Append-only event stream for live UI, auditability, and investigation.

```text
id
harvest_job_id
harvest_source_run_id
harvest_stage_run_id
event_type
severity
message
payload
created_at
```

## 4.5 `HarvestJobResult`

Freezes accepted, rejected, and review-required results from one job.

```text
id
harvest_job_id
institution_id
result_status
score_at_completion
qualification_status_at_completion
qualification_policy_id
qualification_policy_version
accepted_reason
rejection_reasons
source_contributions
evidence_summary
created_at
```

`Generated Leads` reads the frozen job result. `Master Leads` reads the current canonical organization.

---

# 5. Common workflow contract

## 5.1 Lifecycle

```text
Validate
→ Plan
→ Execute
→ Normalize
→ Persist raw evidence
→ Resolve entities
→ Enrich canonical records
→ Qualify
→ Score
→ Finalize source contribution
```

## 5.2 Status vocabulary

```text
PENDING
VALIDATING
PLANNING
RUNNING
PAUSING
PAUSED
RETRYING
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
SKIPPED
CANCELLING
CANCELLED
```

Source-specific conditions belong in structured warning and failure codes, not incompatible statuses.

## 5.3 Connector contract

A connector should expose a stable conceptual interface:

```python
class SourceConnector:
    source_type: SourceType
    connector_version: str
    workflow_version: str
    normalization_version: str

    def capabilities(self) -> SourceCapabilities: ...
    def workflow_definition(self) -> list[SourceStageDefinition]: ...

    async def validate(self, context: SourceRunContext) -> ValidationResult: ...
    async def plan(self, context: SourceRunContext) -> SourcePlan: ...
    async def execute(self, context: SourceRunContext, plan: SourcePlan): ...
    async def normalize(self, raw_item: object) -> list[NormalizedEvidence]: ...
    async def finalize(self, context: SourceRunContext) -> SourceRunSummary: ...
```

## 5.4 Capability declarations

Each connector declares whether it supports:

- Organization discovery
- Person discovery
- Phone discovery
- Email discovery
- Website discovery
- Geographic search
- Branch discovery
- Incremental results
- Pause and resume
- Cost estimation

The Generate Leads page must explain source capabilities rather than making the operator infer them from connector names.

---

# 6. Source-specific workflows

## 6.1 Google Places

```text
Validate Google credentials
→ Resolve quota and cost limits
→ Translate sector and organization types into categories and queries
→ Build geographic coverage
→ Execute text and nearby searches
→ Follow pagination tokens
→ Fetch required place details
→ Normalize identity, phone, domain, address, and coordinates
→ Persist raw evidence incrementally
→ Resolve institutions and branches
→ Report coverage, quota, cost, and failures
```

Required metrics include areas, queries, requests, pages, places, unique provider IDs, duplicates removed, normalized records, resolution outcomes, quota, estimated cost, retries, and failures.

## 6.2 Yandex Maps

```text
Validate Yandex credentials
→ Translate sector taxonomy
→ Build geographic search areas
→ Execute organization searches
→ Parse GeoJSON features
→ Process provider identifiers, names, categories, phones, URLs, addresses, and coordinates
→ Handle pagination and rate limits
→ Normalize and persist evidence
→ Resolve institutions and branches
→ Report coverage and failures
```

Yandex keeps its own taxonomy mapping and parser while emitting the shared evidence contract.

## 6.3 Apple Maps

```text
Validate MapKit signing configuration
→ Sign or refresh access token
→ Translate requested categories
→ Build search plan
→ Execute searches
→ Derive stable versioned source identifiers when needed
→ Normalize and persist evidence
→ Resolve institutions and branches
→ Report token, quota, coverage, and failures
```

Derived identifier algorithms must be versioned.

## 6.4 Public websites

```text
Receive or discover seed domains
→ Normalize and validate URLs
→ Apply SSRF and network-destination protections
→ Apply source policy and robots rules
→ Prioritize relevant pages
→ Crawl incrementally
→ Persist every fetch attempt
→ Extract organization identity
→ Extract all usable phones and emails
→ Extract social profiles and contact forms
→ Extract person and role candidates with evidence
→ Detect technologies and operational signals
→ Aggregate evidence by domain and organization
→ Resolve organizations, branches, people, and contacts
→ Compute evidence-aware detection states
→ Report coverage and failures
```

Required website states:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_CRAWLED
CRAWL_FAILED
UNKNOWN
```

A crawler’s silence is not proof of absence. Website snapshots used for scoring must be scoped to the correct institution or domain. Contact-to-person attribution requires evidence.

## 6.5 Authorized imports

```text
Validate source authority
→ Inspect encoding and schema
→ Map columns
→ Validate identity fields
→ Normalize organization and contact data
→ Reject invalid rows with explicit reasons
→ Detect unchanged reimports
→ Detect new evidence in known rows
→ Persist append-only raw import evidence
→ Resolve organizations and people
→ Produce import and rejection reports
```

## 6.6 Telegram

```text
Validate configured public channels and source policy
→ Fetch permitted public metadata and content
→ Extract organization identity and public contacts
→ Normalize and persist evidence
→ Resolve organizations
→ Record coverage and failures
```

Telegram evidence should not automatically become high-confidence identity evidence without corroboration.

## 6.7 Manual entry

```text
Validate authorized input
→ Create manual source run
→ Preserve original submission
→ Normalize identity and contacts
→ Submit through duplicate resolution
→ Create or enrich canonical institution
→ Add branch, person, contact, and provenance evidence
→ Classify sector
→ Refresh LeadProfile
→ Attempt durable Core synchronization when enabled
```

Manual entry must not bypass duplicate resolution.

## 6.8 Professional networks

Status: **Restricted**.

```text
Validate approved access method
→ Receive or discover permitted profile references
→ Collect permitted evidence
→ Identify person and role
→ Identify organization reference
→ Resolve organization against canonical institutions
→ Resolve or create PersonCandidate
→ Attach contacts only when attribution is supported
→ Run structured research with prompt-injection controls
→ Separate facts from inferences
→ Persist findings, signals, and account brief
→ Refresh readiness
```

A person must not be created as though that person were the organization.

---

# 7. Normalized evidence contract

Every connector emits normalized evidence while preserving the immutable raw source payload.

Organization example:

```json
{
  "source_type": "google_places",
  "source_id": "place-123",
  "entity_type": "organization",
  "identity": {
    "name": "Riverside Academy",
    "domain": "riverside.edu.pk",
    "website": "https://riverside.edu.pk",
    "phone": "+92511234567"
  },
  "organization_type": "school",
  "location": {
    "address": "F-8, Islamabad",
    "city": "Islamabad",
    "country_code": "PK",
    "latitude": 33.6844,
    "longitude": 73.0479
  },
  "contacts": [],
  "evidence": [],
  "captured_at": "2026-08-02T04:00:00+05:00",
  "raw_payload": {}
}
```

Person example:

```json
{
  "source_type": "professional_network",
  "source_id": "profile-456",
  "entity_type": "person",
  "identity": {
    "name": "Sara Ahmed"
  },
  "role": "Principal",
  "organization_reference": {
    "name": "Riverside Academy",
    "domain": "riverside.edu.pk"
  },
  "contacts": [],
  "evidence": [],
  "captured_at": "2026-08-02T04:00:00+05:00",
  "raw_payload": {}
}
```

---

# 8. Planned end-to-end backend workflow

## 8.1 Create Harvest Job

Planned endpoint:

```http
POST /api/v1/harvest-jobs
```

The request defines lead type, sectors, organization types, locations, sources, target count, candidate budget, quality mode, required evidence, exclusions, and objective.

## 8.2 Pin versions

At creation, persist connector, workflow, normalization, source API, taxonomy, qualification-policy, capability, and configuration versions.

## 8.3 Plan source runs

```text
HarvestJob
├── Google Places source run
├── Yandex source run
└── Website source run
```

Each source produces its own plan, stage definition, cost estimate, and capability warnings.

## 8.4 Execute and persist incrementally

Raw records, snapshots, stage progress, checkpoints, and events are written during execution so partial work remains visible and recoverable.

## 8.5 Resolve and enrich

```text
Raw evidence
→ Normalize fields
→ Generate match candidates
→ Score candidates
→ Resolve automatically when safe
→ Queue ambiguity for human review
→ Create or enrich canonical organization, branch, person, and contact records
→ Persist provenance
```

## 8.6 Verify, qualify, and score

The system verifies identity, contactability, source corroboration, freshness, detection states, suppression, and evidence quality before applying the correct versioned qualification policy. Qualification and opportunity scoring remain separate decisions.

## 8.7 Accept and freeze results

A candidate counts toward the target only when the job’s acceptance requirements are satisfied. Every accepted, rejected, and review-required result is frozen with reasons and source contributions.

---

# 9. Live Harvest Run UI contract

The parent summary shows target, accepted count, candidates, completed sources, status, warnings, and estimated source cost.

Every source receives a separate card rendered from backend-provided workflow definitions.

The frontend must not hardcode workflow state with source-specific `if` statements. It renders:

- Stage name and description
- Status
- Processed and total counts
- Concrete metrics
- Warnings and errors
- Retry state
- Pause and cancellation capability

Recommended live endpoint:

```http
GET /api/v1/harvest-jobs/{job_id}/events
```

Server-Sent Events are appropriate for progress. Commands remain authenticated ordinary API calls.

The UI must never fabricate progress. If a total is unknown, show indeterminate activity with concrete backend metrics.

---

# 10. Sector-specific qualification

## 10.1 Policy identity

Qualification is selected by:

```text
Sector
+
Lead type
+
Organization type
+
Assessment or campaign objective
+
Policy version
```

## 10.2 Universal safeguards

- Canonical identity exists.
- Identity conflicts are below the allowed threshold.
- Operating status is acceptable.
- Required contactability exists.
- Intended channel is not suppressed.
- Confidence reaches the minimum threshold.
- Required evidence is recent enough.
- Organization passes NEWAX ethical restrictions.
- Organization is not already in an incompatible campaign.
- Existing customers are excluded when requested.
- Missing evidence is not converted into a positive fact.

## 10.3 Rule types

Policies may define required, weighted, disqualifying, review-trigger, evidence, staleness, organization-type, source, threshold, and objective-specific rules. Arbitrary executable Python or SQL must not be stored as policy logic.

## 10.4 Outcomes

```text
Qualified
Disqualified
Needs Review
```

Every assessment preserves policy identity, version, score, threshold, criterion results, evidence snapshot, rationale, and assessment time.

## 10.5 Sector policy families

Detailed policies are required for:

- Education
- Healthcare
- Real estate
- Legal
- Hospitality
- Retail
- Islamic finance
- Professional services

A school, hospital, law firm, hotel, retailer, and property company cannot be evaluated through one universal checklist. Sector alone also does not determine qualification; objective and organization type matter.

Qualification answers whether an organization may enter the usable lead pool. Opportunity scoring ranks the value and timing of the opportunity.

---

# 11. Lead workspaces

## 11.1 Generated Leads

Shows the frozen results of one Harvest Job with search, filters, sorting, selection, rejection reasons, selected-ID export, dossier access, and Communicator setup.

## 11.2 Master Leads

Shows canonical organizations across every harvest with server-side search, filters, saved views, source coverage, current score, qualification, communication state, suppression, column control, exports, Communicator handoff, and NEWAX Core handoff.

## 11.3 Lead Dossier

Aggregates:

- Canonical organization identity
- Sector and organization type
- Operating status
- Branches and locations
- Contacts
- People and roles
- Attribution confidence
- Website and technology intelligence
- Service-gap states
- Opportunity analysis
- Qualification and policy version
- Lead score and history
- Evidence and provenance
- Source and harvest history
- Data-quality flags
- Communication readiness
- Campaign history
- Compliance and suppression
- Audit activity
- Ownership and notes

Facts, detections, inferences, and unknowns must be visually distinct.

---

# 12. Export and Communicator

Exports should support selected canonical IDs, filtered results, saved views, completed harvests, configurable fields, CSV, Excel, JSON, summary reports, background jobs, audit records, expiring links, and email delivery.

Communicator setup must follow:

```text
Selected leads
→ Validate canonical IDs
→ Freeze audience
→ Check suppression and channel eligibility
→ Exclude incompatible campaigns
→ Choose objective and channels
→ Choose or create sequence
→ Configure personalization, schedule, timezone, and limits
→ Require approval where configured
→ Create campaign
→ Generate drafts
→ Review
→ Send
→ Pause on reply and record outcomes
```

Campaign creation must not silently send messages.

---

# 13. Locked frontend visual system

The frontend must feel calm, precise, operational, premium, reliable, and enterprise-ready. It must not use gradients, neon accents, glass effects, decorative dashboards, or a different colour for every emotional state a database row might experience.

## 13.1 Colour tokens

```css
:root {
  --background: #F7F7F4;
  --surface: #FFFFFF;
  --surface-muted: #F0F0EC;
  --surface-hover: #EAEAE5;

  --soft-black: #1A1A18;
  --strong-black: #10100F;
  --text-secondary: #666660;
  --text-muted: #8A8A84;

  --border: #DADAD4;
  --border-strong: #AFAFAA;
}
```

The primary application background is soft white. Cards, tables, dialogs, and drawers use white surfaces. The monochrome hierarchy is created through typography, spacing, borders, fill weight, icons, and elevation.

Semantic states may use restrained accessible colour only where necessary. Status must never rely on colour alone.

## 13.2 Buttons

### Primary

```css
background: #1A1A18;
color: #F9F9F7;
border: 1px solid #1A1A18;
border-radius: 8px;
```

Hover uses `#10100F`. Use one principal primary action per section.

### Secondary

```css
background: #FFFFFF;
color: #1A1A18;
border: 1px solid #BDBDB7;
border-radius: 8px;
```

Hover uses the muted surface and stronger border.

### Tertiary

Transparent background, no border, and medium-neutral text for low-priority actions.

### Destructive

Remain monochrome, use explicit destructive wording and iconography, and require confirmation. Irreversible operations must not depend on red paint to explain themselves.

Button heights:

```text
Small    32px
Default  40px
Large    46px
```

## 13.3 Shape and spacing

```text
Button radius      8px
Input radius       8px
Card radius        10px
Dialog radius      12px
Status chip radius 999px
```

Spacing scale:

```text
4  8  12  16  20  24  32  40  48px
```

Maximum content width is 1600px. Standard page padding is 24px, increasing to 32px on large screens and reducing to 16px on mobile.

## 13.4 Typography

Preferred stack:

```css
font-family: "Inter", "Geist", "Segoe UI", sans-serif;
```

Recommended hierarchy:

```text
Page title     28/34, weight 650
Section title  20/28, weight 600
Card title     16/24, weight 600
Body           14/22, weight 400
Table text     13/20, weight 400
Label          12/18, weight 550
Metric value   28–36, weight 650
```

## 13.5 Surfaces, inputs, and tables

Standard card:

```css
background: #FFFFFF;
border: 1px solid #DEDED8;
border-radius: 10px;
box-shadow: 0 1px 2px rgba(20, 20, 18, 0.04);
```

Input:

```css
height: 40px;
background: #FFFFFF;
border: 1px solid #CFCFC9;
border-radius: 8px;
color: #1A1A18;
```

Focus:

```css
border-color: #1A1A18;
box-shadow: 0 0 0 3px rgba(26, 26, 24, 0.10);
```

Tables use muted headers, white rows, subtle horizontal separators, soft-white row hover, and a soft-black inset edge for selected rows. Avoid enclosing every cell in a border.

## 13.6 Progress and status

Progress bars use a 6px muted track and soft-black fill. Show concrete backend counts wherever possible.

Acceptable:

```text
47 of 120 planned queries completed
```

Not acceptable unless the backend can justify it:

```text
73% complete
```

Statuses use icon, label, border, and fill weight. Colour is supplementary, never the sole signal.

---

# 14. Frontend application shell

## 14.1 Navigation

Expanded sidebar: 248px. Collapsed sidebar: 72px. Soft-white surface with a subtle border.

Navigation groups:

### Discover

- Generate Leads
- Harvest Runs
- Generated Leads

### Manage

- Master Leads
- Lead Dossiers
- Daily Selection

### Review

- Resolution Reviews
- Qualification Reviews
- Data Quality

### Activate

- Exports
- Communicator
- Outreach Drafts

### Governance

- Compliance
- Qualification Policies
- Source Policies

### Operations

- Source Health
- Jobs
- Event Outbox
- Audit Log
- Secrets & Integrations
- Settings

The active navigation item uses a soft-black background and white text. Inactive items are transparent with neutral text and a muted hover surface.

## 14.2 Top bar

Contains breadcrumbs, global search, environment indicator, notifications, and user menu.

## 14.3 Standard page structure

```text
Breadcrumb
Page title and explanation
Primary page action
Optional summary metrics
Filters or controls
Main content
Contextual drawer or detail panel
```

---

# 15. Frontend page architecture

## 15.1 Generate Leads

Five sections:

1. Define lead type and objective.
2. Define sector, organization type, and evidence requirements.
3. Define geography and target accepted count.
4. Select and configure sources using capability-aware source cards.
5. Review pinned policy and connector versions, then save draft or start harvest.

Each source card shows availability, capabilities, required credentials, expected evidence, quota or cost information, and restrictions.

## 15.2 Harvest Runs and Harvest Run

The list page supports status, source, sector, creator, and date filters.

The detail page displays:

- Parent job summary
- Target and accepted counts
- Candidates, qualified, rejected, and review-required counts
- Duration and cost
- Pause, resume, retry, and cancel controls
- One source card per child run
- Backend-defined stage timeline
- Source-specific metrics
- Live event stream

## 15.3 Generated Leads

Tabs:

```text
Accepted
Needs Review
Rejected
All Candidates
```

Supports advanced filters, canonical-ID selection, export, Master Leads actions, Communicator setup, and Lead Dossier access.

## 15.4 Master Leads

Supports global canonical search, saved views, column control, advanced filters, bulk selection, exports, Communicator handoff, and dossier access.

Recommended views include High Opportunity, Needs Qualification Review, No Decision Maker, Website Opportunity, Automation Opportunity, Connected Infrastructure Opportunity, Recently Updated, and Not Contacted.

## 15.5 Lead Dossier

A persistent organization summary appears beside tabs for Overview, People, Infrastructure, Qualification, Evidence, History, and Compliance.

## 15.6 Qualification Policies

The policy list shows sector, lead type, organization type, objective, version, state, effective date, and owner.

The editor supports policy identity, required criteria, weighted criteria, disqualifiers, review triggers, evidence requirements, staleness, threshold, testing, and publishing. Used policy versions are immutable; changes create a new version.

## 15.7 Source settings

Each connector page shows state, version, capabilities, last successful run, recent failures, credential state, quota, and cost. Complete secrets are never displayed.

## 15.8 Operations

Operations pages cover job monitoring, source health, stranded work, outbox delivery, audit logs, configuration summaries, failures, retries, and recovery actions.

---

# 16. Secrets & Integrations page

Status: **Planned**.

Route:

```text
/settings/secrets
```

Navigation:

```text
Operations
└── Secrets & Integrations
```

Access is restricted to administrators or a future dedicated Secrets Manager role.

## 16.1 Purpose

The page allows authorized users to add, replace, validate, disable, re-enable, and rotate credentials without editing server files manually.

The frontend must never retrieve or display an existing plaintext secret. A key-management page that helpfully reveals every key would be a very efficient security incident.

## 16.2 Managed integrations

### Source credentials

- Google Places API key
- Yandex Maps API key
- Brave Search API key
- Apple MapKit team ID
- Apple MapKit key ID
- Apple MapKit private key

### Intelligence services

- OpenAI API key

### Communication services

- SMTP host and port
- SMTP username
- SMTP password
- Default sender identity

### Integration security

- NEWAX Core webhook URL
- NEWAX Core webhook signing secret

### Restricted tooling

Professional-network proxy, CAPTCHA service, and restricted-source credentials remain hidden or disabled until the operating model is approved.

## 16.3 Metadata table

Columns:

```text
Integration
Credential
Status
Environment
Last Validated
Last Rotated
Updated By
Actions
```

Values are represented only through metadata and a short fingerprint such as:

```text
••••••••••••4Kd9
```

The backend must never return the plaintext value after submission.

## 16.4 Manage-secret drawer

Shows:

- Integration and credential name
- Status
- Fingerprint
- Environment
- Last validation and rotation
- Updating user
- Connector usage
- Validate, replace, disable, or enable actions

It must not offer Reveal Secret, Copy Existing Secret, or Download Secret.

## 16.5 Add or replace workflow

```text
Choose integration and credential type
→ Choose environment
→ Enter candidate secret
→ Reauthenticate when required
→ Submit through secure API
→ Encrypt and store candidate version
→ Validate candidate through a safe provider request
→ Activate only when validation succeeds
→ Retire previous version
→ Record immutable audit event
```

A failed candidate must leave the previous working version active.

The frontend clears the value after submission and excludes it from browser persistence, analytics, telemetry, and logs.

## 16.6 Rotation history

Store metadata only:

- Version
- Fingerprint
- Created time
- Activated time
- Retired time
- Updated by
- Validation outcome
- Rotation reason

Historical plaintext values remain unavailable.

## 16.7 Permissions

Suggested permissions:

```text
secrets.read_metadata
secrets.create
secrets.replace
secrets.validate
secrets.disable
secrets.enable
secrets.view_audit
```

Require reauthentication for replacing production credentials, disabling active production credentials, changing webhook signing secrets, and updating private signing keys.

## 16.8 Planned API

```http
GET    /api/v1/secrets
GET    /api/v1/secrets/{secret_id}
POST   /api/v1/secrets
POST   /api/v1/secrets/{secret_id}/replace
POST   /api/v1/secrets/{secret_id}/validate
POST   /api/v1/secrets/{secret_id}/disable
POST   /api/v1/secrets/{secret_id}/enable
GET    /api/v1/secrets/{secret_id}/history
```

Responses return metadata only.

Example:

```json
{
  "id": "google_places_api_key",
  "display_name": "Google Places API Key",
  "configured": true,
  "status": "valid",
  "fingerprint": "4Kd9",
  "environment": "production",
  "last_validated_at": "2026-08-02T00:43:00Z",
  "last_rotated_at": "2026-08-02T00:40:00Z"
}
```

## 16.9 Storage model

Local development may use an ignored `.env.secrets` file through an explicitly enabled development adapter. Production must use an approved encrypted deployment secret store, Vault, cloud secret manager, or equivalent system.

Production secrets must never be stored in frontend state, browser storage, GitHub, `job.yaml`, logs, analytics, audit payloads, screenshots, or plaintext database fields.

A separate configuration PR proposes `.env.secrets` and `.env.secrets.example`; until that work is integrated, it must not be described as current `master` behavior.

---

# 17. Shared frontend components

Foundation components:

```text
AppShell
Sidebar
TopBar
PageHeader
Breadcrumb
PrimaryButton
SecondaryButton
TertiaryButton
IconButton
TextInput
Select
MultiSelect
Checkbox
RadioGroup
DatePicker
FilterBar
StatusChip
MetricCard
DataTable
Pagination
Tabs
Dialog
Drawer
Toast
EmptyState
Skeleton
ProgressBar
StageTimeline
EvidencePanel
VersionBadge
PermissionGate
```

Business components:

```text
SourceSelector
HarvestJobSummary
SourceWorkflowCard
StageProgressList
LeadResultTable
LeadScoreBreakdown
QualificationAssessmentPanel
PolicyRuleBuilder
SourceContributionPanel
PersonEvidenceCard
DossierTimeline
ExportDialog
CampaignAudienceDialog
SecretMetadataTable
SecretManagementDrawer
SecretRotationHistory
CredentialValidationResult
```

---

# 18. Frontend delivery modules

These are implementation submodules under the roadmap’s top-level frontend milestone. They may use separate PRs while remaining one product milestone.

## F1. Design tokens and foundations

Colour tokens, typography, spacing, radii, elevation, buttons, inputs, focus, tables, status, progress, dark-text contrast, and reduced-motion behavior.

## F2. Application shell

Sidebar, top bar, breadcrumbs, responsive layout, environment indicator, and permission-aware navigation.

## F3. Shared data components

Tables, filters, pagination, dialogs, drawers, toasts, empty states, loading states, status chips, and optimistic-lock conflict handling.

## F4. Authentication and runtime configuration

API base URL, real session lifecycle, expiry, logout, forbidden states, and environment-safe runtime configuration.

## F5. Generate Leads

Objective, sector, organization type, geography, target, source capability selection, quality controls, version preview, validation, draft, and submission.

## F6. Harvest Runs and live Harvest Run

Job list, parent summary, source cards, generic stage renderer, SSE client, reconnect, pause, resume, retry, cancel, warnings, failures, and recovery state.

## F7. Source-specific metric displays

Google, Yandex, Apple Maps, website, import, Telegram, manual, and restricted-source displays layered over generic backend-defined stages.

## F8. Generated Leads

Frozen result tabs, filters, selection, rejection reasons, export, dossier, and Communicator actions.

## F9. Master Leads

Canonical global search, saved views, advanced filtering, column control, selection, exports, and handoffs.

## F10. Lead Dossier

Overview, people, infrastructure, qualification, evidence, history, compliance, and organization summary.

## F11. Qualification and governance

Policy list, immutable versions, rule builder, testing, publishing, review queues, source policies, and permission controls.

## F12. Secrets & Integrations

Metadata table, category and environment filters, add-secret dialog, manage drawer, replacement, validation, enable/disable, rotation history, reauthentication, audit display, and no-secret-leak tests.

## F13. Export and Communicator

Export setup, audience preview, eligibility exclusions, campaign sequence, schedule, limits, approval, and creation.

## F14. Operations

Job monitoring, source health, failures, retries, event outbox, audit logs, configuration summaries, and recovery actions.

## F15. End-to-end and rollout verification

Desktop, tablet, mobile review, accessibility, permissions, empty states, failure states, live-backend integration, E2E flows, performance, security review, and deployment verification.

---

# 19. Responsive and accessibility requirements

## Desktop

Full sidebar, wide tables, split dossier layout, and complete policy and secrets administration.

## Tablet

Collapsed navigation, horizontally scrollable tables, and drawers replacing secondary columns.

## Mobile

Prioritize job monitoring, lead summaries, reviews, approvals, pause, and cancellation. Dense policy and secret administration remain desktop-first.

Accessibility requirements:

- Minimum 4.5:1 text contrast
- Visible keyboard focus
- Full keyboard operation
- Accessible labels for every icon action
- Status not communicated through colour alone
- Minimum 40px primary interaction target
- Correct table headers
- Focus-trapped dialogs
- Reduced-motion support
- Announced loading and live states

---

# 20. Source and policy upgrades

Every source run records connector, workflow, normalization, API, taxonomy, policy, configuration, and capability versions.

Upgrade rules:

1. New jobs use the latest approved versions.
2. Running jobs remain pinned.
3. Historical runs retain their stored workflow definition.
4. Resume uses the original versions unless an explicit migration exists.
5. Connector upgrades pass contract tests.
6. Workflow upgrades pass schema compatibility checks.
7. Rollback remains possible.
8. Historical score and policy context remains intact.
9. Requalification and rescoring are explicit actions.
10. Source changes remain isolated inside the relevant connector wherever possible.

---

# 21. Reliability and operations

## Idempotency

Job creation supports idempotency keys. Source items use stable identifiers. Retries do not create duplicate institutions, results, campaign recipients, or outbound events.

## Concurrency

Mixed-source parallel execution remains disabled until identity resolution uses a proven strategy such as advisory locks, a durable resolution queue, safe uniqueness constraints, short transactions, and post-commit reconciliation.

## Pause and resume

Resumable connectors persist stage, cursor, remaining plan, processed IDs, quota, cost, and checkpoint state.

## Failure isolation

One malformed record does not fail a source. One source failure does not necessarily fail the parent. Partial completion uses explicit warnings. Skips and rejections preserve reasons. Stranded work remains visible and recoverable.

## Observability

Metrics include job and stage duration, records, requests, retries, rate limits, errors, resolution outcomes, qualification outcomes, yield, cost per accepted lead, source contribution, duplicates, review rate, suppression rate, export volume, and Communicator eligibility.

---

# 22. Security and governance

The system must:

- Respect source API terms, website terms, `robots.txt`, and applicable law.
- Use official APIs or authorized data where required.
- Never bypass access controls without an explicitly approved lawful method.
- Avoid unnecessary sensitive personal data.
- Preserve evidence and provenance.
- Support suppression, deletion, retention, and audit requirements.
- Protect secrets and source sessions.
- Apply SSRF protections.
- Limit response size, redirects, protocols, and network destinations.
- Separate organization contacts from personal attribution.
- Require approval before communication where policy requires it.
- Stop communication on opt-out or suppression.
- Keep professional-network automation restricted until approved.
- Treat secrets as write-only after submission.
- Keep secrets out of logs, errors, analytics, telemetry, and audit payloads.

---

# 23. Planned APIs

```http
POST   /api/v1/harvest-jobs
GET    /api/v1/harvest-jobs
GET    /api/v1/harvest-jobs/{job_id}
POST   /api/v1/harvest-jobs/{job_id}/pause
POST   /api/v1/harvest-jobs/{job_id}/resume
POST   /api/v1/harvest-jobs/{job_id}/cancel
POST   /api/v1/harvest-jobs/{job_id}/retry
GET    /api/v1/harvest-jobs/{job_id}/events
GET    /api/v1/harvest-jobs/{job_id}/source-runs
GET    /api/v1/harvest-jobs/{job_id}/results

GET    /api/v1/leads
GET    /api/v1/leads/{institution_id}/dossier
POST   /api/v1/leads/search
POST   /api/v1/leads/export-jobs

GET    /api/v1/qualification-policies
POST   /api/v1/qualification-policies
POST   /api/v1/qualification-policies/{policy_id}/versions
POST   /api/v1/institutions/{institution_id}/requalify

POST   /api/v1/communicator/campaigns
GET    /api/v1/communicator/campaigns/{campaign_id}
POST   /api/v1/communicator/campaigns/{campaign_id}/approve
POST   /api/v1/communicator/campaigns/{campaign_id}/pause
POST   /api/v1/communicator/campaigns/{campaign_id}/resume

GET    /api/v1/secrets
GET    /api/v1/secrets/{secret_id}
POST   /api/v1/secrets
POST   /api/v1/secrets/{secret_id}/replace
POST   /api/v1/secrets/{secret_id}/validate
POST   /api/v1/secrets/{secret_id}/disable
POST   /api/v1/secrets/{secret_id}/enable
GET    /api/v1/secrets/{secret_id}/history
```

These are planned interfaces, not claims about current endpoints.

---

# 24. Implementation sequence

## Phase A: prerequisite correctness and security

Authentication, authorization, website snapshot linkage, detection status, deletion graph, outbox correctness, resolution concurrency, migration-driven testing, contact materialization, research safety, and frontend runtime authentication.

## Phase B: Harvest Job foundation

Models, source-run relationship, stage definitions, events, validation, version snapshots, and state controls.

## Phase C: connector adaptation

Google, Yandex, Apple Maps, website, authorized imports, Telegram, manual, and restricted professional-network redesign.

## Phase D: qualification policies

Versioned policy model, rule engine, universal safeguards, sector and objective policies, assessment snapshots, editor, and requalification.

## Phase E: result and dossier APIs

Frozen job results, Master Leads, Dossier, selected-ID exports, and saved views.

## Phase F: secret management and Communicator

Encrypted credential backend, metadata-only secret APIs, provider validation, rotation, campaign, audience, sequence, channel eligibility, approval, send controls, and reply tracking.

## Phase G: frontend

F1 through F15 in dependency order, with shells allowed earlier only when they do not imply unavailable backend behavior.

---

# 25. Acceptance criteria

The target workflow is not complete until:

1. Authorized users can create Harvest Jobs from UI and API.
2. Requests pin connector, workflow, taxonomy, normalization, and policy versions.
3. Multiple sources create separate child runs.
4. Every source exposes real backend-defined stages.
5. The UI does not fabricate progress.
6. Raw evidence is incremental and auditable.
7. Concurrent sources do not silently duplicate canonical organizations.
8. Ambiguous matches enter human review.
9. Website evidence distinguishes absence, non-detection, no crawl, failure, and unknown.
10. Contact-to-person attribution is evidence-backed.
11. Each sector and objective uses the correct versioned policy.
12. Qualification and opportunity scoring remain separate.
13. Results are frozen with reasons.
14. Generated Leads shows one job snapshot.
15. Master Leads shows canonical organizations across harvests.
16. Lead Dossier distinguishes facts, detections, inferences, unknowns, evidence, and history.
17. Selected leads can be exported by canonical ID.
18. Communicator freezes its audience.
19. Suppressed recipients cannot be contacted.
20. Campaign creation does not automatically send before approval.
21. Administrators can add, replace, validate, disable, enable, and rotate supported credentials.
22. Plaintext secrets are never returned after submission.
23. Failed secret replacement leaves the previous active credential working.
24. Secret actions are permission-protected, reauthenticated where required, and audited without secret values.
25. Pause, resume, retry, cancel, partial failure, and recovery states are tested.
26. Migrations upgrade and downgrade cleanly.
27. Frontend accessibility and responsive behavior are verified.
28. Backend tests, frontend checks, security checks, runtime verification, and exact-commit CI pass.

---

# 26. Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Current `master` uses `.env` configuration:

```bash
cp .env.example .env
```

A separate pending configuration change proposes:

```bash
cp .env.example .env
cp .env.secrets.example .env.secrets
```

Do not use the second command until the relevant configuration change is integrated. Deployed environments should use an approved secret manager.

---

# 27. Current run examples

Website seeds:

```yaml
seeds:
  - https://www.lums.edu.pk/
  - https://nust.edu.pk/
  - https://www.fast.edu.pk/
sector: education
```

Search-discovered website seeds:

```yaml
search_queries:
  - private schools Islamabad
  - colleges Rawalpindi
sector: education
```

Google Places:

```yaml
places_provider: google
cities:
  Islamabad:
    - F-8
    - F-10
categories:
  - FORMAL_EDUCATION
sector: education
```

Yandex Maps:

```yaml
places_provider: yandex
cities:
  Islamabad:
    - F-8
categories:
  - FORMAL_EDUCATION
sector: education
```

Authorized import:

```bash
lead-harvester import-authorized \
  --file licensed-leads.csv \
  --source-reference "Contract ABC / Dataset 2026-08" \
  --country-code PK
```

---

# 28. Verification

```bash
ruff check .
ruff format --check .
pytest -q
```

Database changes must validate the full Alembic chain against PostgreSQL.

Frontend changes must run type checking, lint, formatting, unit tests, build, accessibility checks, and relevant E2E tests.

A change is complete only after the latest exact commit passes relevant local checks, runtime workflow validation, security checks, and CI without unresolved issues.

---

# 29. Governing principles

1. Different source workflows, one orchestration standard.
2. One canonical lead database.
3. Raw evidence is immutable; canonical records are resolved views.
4. Facts, detections, inferences, and unknowns are distinct.
5. No detection is not proof of absence.
6. Qualification is sector-, objective-, and version-specific.
7. Qualification and opportunity ranking are separate.
8. The backend defines source stages; the frontend renders them.
9. Every run is versioned and historically explainable.
10. External failures are expected and recoverable.
11. No outreach begins without eligibility checks and required approval.
12. Secrets are write-only, encrypted, permission-protected, and auditable.
13. Soft-white surfaces and soft-black actions define the frontend hierarchy.
14. The system should do the work; the operator should remain in control.

---

# 30. Database Connections & Synchronization

Status: **Planned**.

Route:

```text
/settings/databases
```

Navigation:

```text
Operations
└── Database Connections
```

## 30.1 Boundary

PostgreSQL is provisioned separately on a server, container platform, or managed database service. The Harvester page does **not** install PostgreSQL. It connects the application to an already provisioned database, validates that connection, reports schema state, manages approved credential replacement, applies controlled migrations, coordinates backups, and runs explicit synchronization jobs.

Supported deployment patterns include:

```text
Development server
├── Harvester
└── Development PostgreSQL
```

```text
Application server
└── Harvester

Dedicated database server or managed service
└── Production PostgreSQL
```

Development, testing, staging, and production must use separate databases. Several non-production databases may share one PostgreSQL instance initially, but production should use a dedicated instance or managed service when reliability and scale justify it.

## 30.2 Environment profiles

Required environments:

```text
Development
Testing
Staging
Production
```

Optional future profiles:

```text
Preview
Training
Disaster Recovery
```

Each `DatabaseConnectionProfile` stores metadata such as environment, engine, host, port, database name, SSL mode, pool settings, secret reference, schema revision, state, validation time, and backup state.

Passwords, complete connection URLs, client keys, and tokens remain encrypted and write-only. After storage, the UI shows only metadata and a short credential fingerprint.

## 30.3 Database roles

Use separate PostgreSQL roles:

```text
harvester_runtime
Application read/write permissions only

harvester_migration
DDL and Alembic migration permissions

harvester_readonly
Health, diagnostics, and reporting

harvester_backup
Backup and restore permissions where supported
```

The normal runtime application must not possess migration or unrestricted administrative authority.

## 30.4 Connection validation and activation

```text
Enter candidate connection details
→ Reauthenticate
→ Store candidate credentials securely
→ Resolve host and test network access
→ Verify TLS
→ Authenticate
→ Confirm expected server and database identity
→ Verify environment identity marker
→ Check required extensions and permissions
→ Read current Alembic revision
→ Run a safe health query
→ Activate candidate atomically
→ Retire previous credential version
→ Record audit event
```

A failed candidate leaves the currently active connection unchanged.

Each database must expose an environment marker such as:

```text
application = newax-harvester
environment = production
```

The backend must reject activation when the expected environment does not match the database marker.

## 30.5 Separate synchronization operations

“Sync database” is not one undifferentiated operation.

### Schema synchronization

Compares application and database Alembic revisions, shows pending migrations, performs preflight checks, creates or confirms a backup, applies approved migrations, and runs post-migration verification.

### Reference-data synchronization

Moves approved non-sensitive versioned datasets such as sector definitions, source taxonomies, qualification-policy templates, and lookup records between environments using stable identifiers, dry-run comparison, conflict reporting, approval, and checksum verification.

### Controlled business-data transfer

Moves explicitly selected and governed datasets only. Production-to-non-production transfers require anonymization or redaction. Development-to-production transfer is denied by default. Credentials, sessions, sensitive personal data, and unrestricted audit history are not copied casually between environments.

## 30.6 Schema comparison

The page may compare:

```text
Alembic revision
Tables
Columns
Data types
Constraints
Indexes
Extensions
Unexpected objects
Missing objects
```

Schema drift produces a report and migration review. The frontend must not generate and execute uncontrolled “make target match source” SQL.

## 30.7 Backups and restore

Connection metadata includes last backup, backup age, type, retention, encryption state, storage reference, integrity result, and last restore test.

Production restore requires reauthentication, separate approval, explicit target confirmation, maintenance-state confirmation, backup-integrity validation, and rollback planning.

## 30.8 Database operation jobs

Use durable jobs such as:

```text
DatabaseValidationRun
DatabaseMigrationRun
DatabaseBackupRecord
DatabaseSyncJob
DatabaseOperationApproval
```

Sync-job statuses:

```text
DRAFT
VALIDATING
AWAITING_APPROVAL
BACKING_UP
RUNNING
VERIFYING
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
CANCELLED
ROLLED_BACK
```

Every job records source and target environment, operation type, actor, approver, selected datasets, revisions, backup reference, row counts, conflicts, validation, timing, failures, and rollback result.

## 30.9 Permissions

```text
databases.read_metadata
databases.create_connection
databases.update_connection
databases.validate_connection
databases.activate_connection
databases.disable_connection
databases.view_schema
databases.run_migration
databases.create_backup
databases.restore_backup
databases.sync_reference_data
databases.transfer_data
databases.view_audit
```

Production connection activation, credential replacement, migration, restore, and business-data transfer require reauthentication and a second approval.

## 30.10 Planned APIs

```http
GET    /api/v1/database-connections
GET    /api/v1/database-connections/{connection_id}
POST   /api/v1/database-connections
POST   /api/v1/database-connections/{connection_id}/replace-credentials
POST   /api/v1/database-connections/{connection_id}/validate
POST   /api/v1/database-connections/{connection_id}/activate
POST   /api/v1/database-connections/{connection_id}/disable

GET    /api/v1/database-connections/{connection_id}/schema
POST   /api/v1/database-connections/{connection_id}/schema/compare
GET    /api/v1/database-connections/{connection_id}/migrations
POST   /api/v1/database-connections/{connection_id}/migrations/apply

GET    /api/v1/database-connections/{connection_id}/backups
POST   /api/v1/database-connections/{connection_id}/backups
POST   /api/v1/database-connections/{connection_id}/restore

POST   /api/v1/database-sync-jobs
GET    /api/v1/database-sync-jobs
GET    /api/v1/database-sync-jobs/{job_id}
POST   /api/v1/database-sync-jobs/{job_id}/validate
POST   /api/v1/database-sync-jobs/{job_id}/approve
POST   /api/v1/database-sync-jobs/{job_id}/execute
POST   /api/v1/database-sync-jobs/{job_id}/cancel
```

Responses expose metadata and status only, never plaintext database credentials.

## 30.11 Frontend page

Tabs:

```text
Connections
Schema & Migrations
Synchronization
Backups
Audit
```

The page follows the locked soft-white and soft-black system. Environment cards show connection state, engine, safe host metadata, database name, schema revision, application revision, last validation, and last backup.

Primary actions include Test and Save, Apply Migration, Start Sync, and Create Backup. Secondary actions include Compare Schema, View History, and Export Report.

## 30.12 Frontend module update

This section supersedes the F13–F15 numbering in section 18:

```text
F13  Database Connections & Sync
F14  Export and Communicator
F15  Operations
F16  End-to-end and rollout verification
```

F13 delivers environment cards, connection editing, write-only credential replacement, validation, schema comparison, migration review, synchronization jobs, conflict reports, backup metadata, approval workflows, audit history, and no-secret-leak tests.

Dependencies:

- Authorization matrix
- Authentication and reauthentication
- Secret-provider abstraction
- Migration-driven test infrastructure
- Approved backup provider
- F2 application shell
- F3 shared components
- F4 authentication
- F12 Secrets & Integrations

## 30.13 Additional acceptance criteria

The database-management capability is not complete until:

1. Each environment uses an explicit independent database profile.
2. PostgreSQL installation remains outside the frontend boundary.
3. Candidate credentials are validated before atomic activation.
4. Failed activation preserves the previous working connection.
5. The database identity marker matches the selected environment.
6. Runtime and migration roles are separate.
7. Schema drift is reported without uncontrolled SQL execution.
8. Production migrations require backup and approval.
9. Reference-data synchronization supports dry run, conflict review, and verification.
10. Controlled data transfer enforces direction, classification, redaction, approval, and audit.
11. Backup integrity and restore procedures are tested.
12. Plaintext database credentials never return to the frontend or enter logs, telemetry, analytics, screenshots, or audit payloads.

---

# 31. Automatic NEWAX Core Synchronization

Status: **Planned**.

Harvester publishes two independent automatic streams to NEWAX Core:

```text
Raw Observation Stream
Every accepted source observation is queued immediately after durable local storage.

Canonical Entity Stream
Every new or materially changed resolved entity is queued after Harvester resolution and validation.
```

Lead qualification does not control publication. An organization, person, location, contact method, domain, website, or relationship may exist in NEWAX Core without being a lead. Lead status is a later commercial classification, not an admission gate for entity existence.

## 31.1 Raw observation stream

Every accepted raw observation is stored and queued atomically:

```text
BEGIN
Persist RawSourceRecord, RawPageSnapshot, or another approved raw observation
Create RAW_OBSERVATION EventOutbox row with exact source-native payload
COMMIT
```

Raw observations use `observation.recorded` with a subject hint such as organization, person, location, contact method, domain, website, relationship, document, social profile, or unknown.

Exact duplicates use stable source identity and payload hashes. A changed source payload creates a new immutable observation version. Different sources remain separate evidence even when later linked to one canonical entity.

## 31.2 Canonical entity stream

After normalization, deduplication, identity resolution, evidence consolidation, and validation:

```text
BEGIN
Create or update canonical entity
Increase canonical revision
Build source-native Core projection
Calculate deterministic projection hash
Create CANONICAL_ENTITY event when materially changed
COMMIT
```

Canonical events cover organizations, people, locations, and relationships. They reference supporting raw observation IDs where available. Unchanged projections do not create duplicate events.

## 31.3 Common source-native envelope

The outer integration envelope contains event identity, source system, connector, source schema, timestamps, tenant reference, source-record reference, canonical entity reference, subject hint, correlation ID, canonical revision, payload checksum, and source-native payload.

Harvester does not map every source into Core’s internal Prisma or Registry fields. NEWAX Core owns final normalization, identity resolution, field ownership, merge policy, and canonical Registry writes.

## 31.4 Multi-stream outbox

The existing `EventOutbox` is evolved rather than replaced. Planned stream types are:

```text
RAW_OBSERVATION
CANONICAL_ENTITY
RECONCILIATION
BACKFILL
```

Every retry reuses the same event ID and exact serialized payload. A genuinely changed observation version or new canonical revision receives a new event ID.

Delivery priority is:

```text
1. Live canonical changes
2. Recent live raw observations
3. Reconciliation and repair
4. Historical backfill
```

The worker provides concurrency-safe claims, ordering, bounded coalescing, retries, dead letter, circuit breaker, backpressure, permanent Core links, reconciliation, and operational metrics.

## 31.5 Dedicated page

Route:

```text
/integrations/newax-core
```

Navigation:

```text
Operations
└── NEWAX Core Sync
```

Tabs:

```text
Overview
Raw Observations
Canonical Entities
Delivery Queue
Dead Letter
Entity Links
Reconciliation
Settings
```

Raw and canonical streams can be enabled, paused, or disabled independently. Pausing stops delivery claims but never stops local harvesting, raw persistence, canonical resolution, or outbox creation.

## 31.6 Frontend sequence update

This section supersedes the F13–F16 numbering in sections 18 and 30:

```text
F13  Database Connections & Sync
F14  NEWAX Core Sync
F15  Export and Communicator
F16  Operations
F17  End-to-end and rollout verification
```

F14 delivers the dedicated page, independent stream controls, live queue, event detail, Core response, permanent links, dead-letter recovery, backfill, reconciliation, permission gates, outage states, and no-secret-leak verification.

## 31.7 Core prerequisites

Automatic production delivery remains disabled until NEWAX Core provides durable event-ID inbox replay protection, payload-hash conflict detection, source schema registry, raw and canonical Harvester adapters, normalization, entity candidates, identity resolution, provenance, field ownership, merge policy, and a safe transaction or resumable canonical-application boundary.

The complete Harvester design, APIs, permissions, delivery behavior, and acceptance criteria are defined in:

- [`docs/architecture/newax-core-automatic-sync.md`](docs/architecture/newax-core-automatic-sync.md)
- [`docs/ROADMAP-CORE-SYNC.md`](docs/ROADMAP-CORE-SYNC.md)
