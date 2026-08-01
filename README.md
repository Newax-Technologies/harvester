# NEWAX Lead Harvester

Lead Harvester is the lead-discovery, verification, qualification, and audience-preparation infrastructure used to convert fragmented public and authorized source evidence into canonical, reviewable business opportunities.

It is not intended to be a generic scraper. The target system must let a user define a market, run the correct workflow for each selected source, observe the real backend process, review evidence-backed leads, and pass an approved audience into Communicator or NEWAX Core.

> **Product principle:** Define the market. Let the infrastructure discover, verify, resolve, qualify, and prepare the opportunities.

---

## Document status

This README has two responsibilities:

1. Explain the backend and commands that exist in the repository today.
2. Define the required next-generation backend and UI workflow that is **planned but not yet fully implemented**.

The distinction matters. A detailed architecture diagram is not proof that the software already performs the workflow. Markdown remains tragically incapable of executing Python.

### Status terms used in this document

- **Current:** Present in the repository today.
- **Partial:** Some required models or services exist, but the complete product workflow is not connected.
- **Planned:** Required architecture that still needs implementation and verification.
- **Restricted:** Must not be enabled until source-access, security, legal, compliance, and operational requirements are approved.

---

# 1. Product journey

The target user journey is:

```text
Lead Generation Command Center
→ Define lead type, sector, geography, source mix, quantity, and quality rules
→ Create Harvest Job
→ Watch source-specific processing in Harvest Run
→ Review the leads produced by that job
→ Search all canonical leads across every previous harvest
→ Open a complete Lead Dossier
→ Export selected leads or create a Communicator campaign
→ Send qualified opportunities to NEWAX Core
```

The principal product pages are:

1. **Generate Leads** — configure the market and create a harvest job.
2. **Harvest Run** — show real backend progress, separately for every source.
3. **Generated Leads** — show the frozen results of one completed harvest job.
4. **Master Leads** — show canonical leads from all previous harvests.
5. **Lead Dossier** — show all current facts, contacts, evidence, scores, history, and communication readiness for one lead.
6. **Communicator** — create controlled campaigns from approved selected leads.

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

The current normal ingestion path is:

```text
YAML configuration
→ Select one source mode
→ Collect source records
→ Persist SourceRun and RawSourceRecord data
→ Normalize name, phone, domain, and location
→ Generate entity-resolution candidates
→ Score match candidates
→ Merge, attach, create, or send to human review
→ Create/update canonical institution, branches, contacts, and provenance
→ Persist detected signals
→ Refresh LeadProfile and score history
→ Complete or fail SourceRun
```

## 2.3 Current source selection limitation

`LeadPipeline.run()` currently selects one ingestion branch through an `if/elif` chain. A single invocation runs one of the following paths:

- Authorized import
- Website crawling and optional Brave Search seed discovery
- Telegram
- Apple Maps
- Yandex Maps
- Google Places

A single parent job that coordinates Google Maps, Yandex, websites, and another approved source together does not yet exist.

## 2.4 Current canonical data model

The current backend already provides important foundations:

- `SourceRun`
- `RawSourceRecord`
- `RawPageSnapshot`
- `CanonicalInstitution`
- `Branch`
- `ContactPoint`
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

These models must be reused or evolved. The planned job system must not create a second, competing lead database merely because naming new tables is easier than integrating existing ones.

## 2.5 Current entity resolution

Incoming raw records are normalized and compared using:

- Exact normalized phone match
- Exact normalized domain match
- Geographic proximity plus name similarity

Candidate pairs are assessed as:

- `MERGE`
- `PENDING`
- `LINK_ONLY`
- `REJECT`

Ambiguous matches remain unresolved for human review. Confident matches enrich an existing canonical institution or create a new canonical institution.

## 2.6 Current scoring and qualification

A `LeadProfile` is refreshed after normal ingestion changes canonical data. The current score considers:

- Scale
- Contactability
- Category fit
- Qualification
- Research signals
- Freshness
- Identity confidence

The profile also calculates business-intelligence fields such as:

- Size tier
- Operational maturity
- ICP match
- Website-quality tier
- Service-gap score
- Organization summary

Qualification currently runs as a separate process. The existing sector layer supports a small number of sector-specific rules, including disqualifying name keywords and minimum branch count. The complete versioned, objective-specific sector qualification system described later in this README is not yet implemented.

## 2.7 Current exports and outreach

Current exports support CSV and JSON, with filters such as operating status, score, qualification status, and sector. Export granularity is one row per contact point.

Current outreach operates through:

```text
AccountBrief
→ OutreachDraft
→ Human review and approval
→ OutreachAutomator
→ Email or LinkedIn send
→ OutreachOutcome
```

Daily lead reservations and selected Master Leads are not yet connected to a full Communicator campaign model.

---

# 3. Required next-generation architecture

## 3.1 Architectural rule

The planned architecture must use:

> **One stable Harvest Job orchestration standard with an independently upgradable workflow for each source.**

External sources do not work the same way. Google Places, Yandex Maps, public websites, authorized CSV imports, Telegram channels, and professional-network data have different access methods, pagination, evidence, rate limits, failures, and entity types.

They must therefore have separate internal workflows.

They must **not** have separate incompatible job models, status vocabularies, event formats, evidence formats, or frontend applications.

## 3.2 Two-layer design

### Layer A: common Harvest Job orchestrator

The parent orchestrator owns:

- Requested market
- Selected sectors
- Selected organization types
- Selected geography
- Selected source mix
- Target verified lead count
- Minimum acceptable result count
- Maximum candidate budget
- Quality mode
- Required fields
- Exclusions
- Overall job status
- Pause and cancellation
- Accepted result count
- Errors and warnings
- Cost and quota usage
- Audit trail
- Final result snapshot

### Layer B: source-specific workflow engine

Each connector owns:

- Source credential and capability validation
- Source-specific planning
- Query generation
- Pagination or crawling
- Rate-limit handling
- Source-specific retries
- Source-specific evidence collection
- Source-specific normalization
- Source-specific metrics
- Source API compatibility
- Connector version and workflow version

All connectors eventually emit normalized evidence into the common entity-resolution and qualification layers.

---

# 4. Planned Harvest Job data model

The exact schema must be validated against existing models and migrations before implementation. The following represents the required responsibilities.

## 4.1 `HarvestJob`

Represents the complete user request.

Suggested fields:

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

Represents one selected source within a parent harvest job.

Suggested fields:

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

The existing `SourceRun` should either be evolved into this role or linked to it. The system must not keep two unrelated run histories that future operators are expected to mentally reconcile.

## 4.3 `HarvestStageRun`

Represents one source-specific stage.

Suggested fields:

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

Suggested fields:

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

Freezes the result set of one harvest job.

Suggested fields:

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

This model allows:

- **Generated Leads** to show one completed job’s frozen results.
- **Master Leads** to show the current canonical institution across every run.

---

# 5. Common workflow contract

Every source workflow may contain different stages, but every connector must obey the same external contract.

## 5.1 Common lifecycle

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

A connector may split or repeat these responsibilities internally, but it must report them through a common job and event contract.

## 5.2 Common status vocabulary

All jobs, source runs, and stages should use a common status vocabulary:

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

Source-specific conditions belong in `failure_code`, `warning_code`, and metrics. They must not invent incompatible statuses that the parent orchestrator cannot interpret.

## 5.3 Connector interface

A connector should expose a stable interface similar to:

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

This is a conceptual contract. Implementation must follow existing repository patterns and avoid duplicating current connector logic without reason.

## 5.4 Source capability declarations

Each connector must declare capabilities rather than forcing the UI to guess.

Example:

```json
{
  "source": "google_places",
  "connector_version": "2.1.0",
  "capabilities": {
    "organization_discovery": true,
    "person_discovery": false,
    "phone_discovery": true,
    "email_discovery": false,
    "website_discovery": true,
    "geographic_search": true,
    "incremental_results": true,
    "pause_resume": true,
    "cost_estimation": true
  }
}
```

The Generate Leads page can then explain what each source can contribute.

---

# 6. Source-specific workflows

## 6.1 Google Places workflow

Planned workflow:

```text
Validate Google credentials
→ Resolve source quotas and limits
→ Translate sector and organization types into Google categories and text queries
→ Build geographic coverage plan
→ Generate tiles or search areas
→ Execute text/nearby searches
→ Follow pagination tokens
→ Collect place summaries
→ Fetch required place details when needed
→ Normalize organization identity, phone, domain, address, and coordinates
→ Persist raw Google evidence
→ Resolve against existing institutions and branches
→ Add or update canonical organization evidence
→ Report source coverage, quota usage, and failures
```

Required Google metrics:

- Areas planned
- Queries planned
- Queries completed
- API requests made
- Pages processed
- Places returned
- Unique source IDs
- Duplicate provider results removed
- Records normalized
- Institutions created
- Institutions enriched
- Ambiguous matches
- Quota consumed
- Estimated source cost
- Failed requests
- Rate-limit retries

Current geographic tiling is a phase-one stub based on named city zones. The planned system should support real coordinate coverage where the source API and commercial requirements justify it.

## 6.2 Yandex Maps workflow

Planned workflow:

```text
Validate Yandex credentials
→ Translate sector taxonomy into Yandex-compatible queries
→ Build geographic search areas
→ Execute organization searches
→ Parse GeoJSON features
→ Process provider identifiers, names, categories, phones, URLs, addresses, and coordinates
→ Handle pagination and rate limits
→ Normalize records
→ Persist raw Yandex evidence
→ Resolve institutions and branches
→ Report coverage and errors
```

Yandex must maintain its own category translation and response parser. It must still emit the same normalized evidence contract as Google.

## 6.3 Apple Maps workflow

Planned workflow:

```text
Validate MapKit signing configuration
→ Sign or refresh access token
→ Translate requested categories
→ Build search plan
→ Execute searches
→ Normalize source results
→ Derive stable source identifiers where the API does not provide them
→ Persist evidence
→ Resolve institutions and branches
→ Report token, quota, coverage, and failure metrics
```

Derived provider IDs must be versioned because changes in the derivation algorithm can otherwise make the same source result appear new after an upgrade.

## 6.4 Public website workflow

Planned workflow:

```text
Receive or discover seed domains
→ Normalize and validate URLs
→ Apply SSRF and network-destination protections
→ Check robots.txt and source policy
→ Prioritize homepage, contact, about, team, services, admissions, portal, and other relevant pages
→ Crawl with per-domain concurrency and rate limits
→ Record every fetch attempt
→ Extract organization identity
→ Extract every usable email and phone
→ Extract social profiles and contact forms
→ Detect decision-maker evidence without unsafe person/contact attribution
→ Detect operational and technology signals
→ Aggregate page evidence by organization and domain
→ Normalize evidence
→ Persist raw page snapshots and raw source records
→ Resolve organizations, branches, people, and contacts
→ Compute evidence-aware website quality and detection states
→ Report crawl coverage and failure reasons
```

Required website metrics:

- Seeds supplied
- Seeds discovered
- Domains accepted
- Domains rejected
- Domains crawled
- Pages planned
- Pages fetched
- Successful pages
- Robots-disallowed pages
- HTTP failures
- Non-HTML pages
- Oversized responses
- Decode failures
- Contacts extracted
- Decision-maker candidates extracted
- Signals detected
- Institutions resolved

### Required website evidence states

Technology or service-gap detection must distinguish:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_CRAWLED
CRAWL_FAILED
UNKNOWN
```

A crawler’s failure to detect something is not proof that it is absent. `NOT_DETECTED`, `NOT_CRAWLED`, and `CRAWL_FAILED` must not be treated as equivalent to `ABSENT_CONFIRMED`.

Every `RawPageSnapshot` used for an institution’s website-quality or service-gap score must be scoped to that specific institution or domain, not merely to a multi-domain source run.

## 6.5 Authorized CSV import workflow

Planned workflow:

```text
Validate file access and declared source authority
→ Inspect encoding and schema
→ Map input columns to canonical import fields
→ Validate required identity fields
→ Normalize names, websites, domains, phones, countries, and contacts
→ Reject malformed rows with explicit reasons
→ Detect unchanged reimports
→ Detect new evidence in previously imported rows
→ Persist append-only raw import evidence
→ Resolve against existing institutions
→ Add all declared contact types and person metadata
→ Produce import summary and rejection report
```

Required import metrics:

- Rows read
- Rows valid
- Rows rejected
- Institutions parsed
- Unchanged rows skipped
- Existing institutions enriched
- New institutions created
- Contacts added
- Ambiguous matches

## 6.6 Telegram workflow

Planned workflow:

```text
Validate configured public channels and access rules
→ Fetch channel metadata and permitted public content
→ Extract organization identity and public contacts
→ Normalize evidence
→ Persist source records
→ Resolve organizations
→ Record source coverage and failures
```

Telegram evidence must not be automatically promoted to high-confidence organization identity without corroboration.

## 6.7 Professional-network or LinkedIn workflow

This source is **restricted** until an approved access method, platform-policy basis, security model, and operating procedure are defined.

The future workflow must be person-aware:

```text
Validate approved source-access method
→ Receive or discover permitted profile references
→ Collect permitted profile evidence
→ Identify person identity
→ Identify current role and organization reference
→ Resolve organization reference against canonical institutions
→ Resolve or create PersonCandidate
→ Attach public contact evidence only when attribution is supported
→ Run structured research with prompt-injection and evidence controls
→ Separate facts from inferences
→ Persist ResearchJob, ResearchFinding, Signal, and AccountBrief data
→ Refresh organization and person readiness
```

It must not create a person as though the person were the organization. It must support relationships such as:

```text
CanonicalInstitution
└── PersonCandidate / stakeholder
    ├── role
    ├── public profile evidence
    ├── contact points supported by evidence
    └── confidence and current-status assessment
```

A phone number or email discovered on the same page as a person’s name must not automatically be assigned to that person without supporting evidence.

## 6.8 Manual entry workflow

Manual entry remains a source with its own workflow:

```text
Validate authorized user input
→ Create manual SourceRun
→ Preserve original submitted data
→ Normalize identity and contacts
→ Resolve or create canonical institution
→ Create branch and contact evidence
→ Classify sector
→ Refresh LeadProfile
→ Attempt durable NEWAX Core synchronization when enabled
```

Manual entry must eventually use the same duplicate-resolution safeguards as automated sources instead of bypassing them through unconditional canonical creation.

---

# 7. Normalized evidence contract

Every connector should emit normalized evidence while preserving the raw source payload.

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

The normalized contract is not a replacement for `RawSourceRecord`. Raw evidence must remain immutable and auditable.

---

# 8. Planned end-to-end backend workflow

## Phase 1: Create Harvest Job

Planned endpoint:

```http
POST /api/v1/harvest-jobs
```

Example request:

```json
{
  "name": "Islamabad private schools",
  "lead_type": "new_business",
  "sector_codes": ["education"],
  "organization_types": ["private_school"],
  "locations": [
    {
      "country_code": "PK",
      "city": "Islamabad"
    }
  ],
  "sources": ["google_places", "yandex", "website"],
  "target_count": 100,
  "minimum_accepted_count": 75,
  "maximum_candidates": 500,
  "quality_mode": "balanced",
  "required_fields": ["phone_or_email"],
  "exclusions": {
    "suppressed": true,
    "closed_permanently": true,
    "existing_customers": true
  }
}
```

The API must validate the complete configuration before scheduling external work.

## Phase 2: Pin versions and policy snapshots

At job creation, store:

- Connector version for each source
- Workflow version for each source
- Normalization version
- Source API version
- Source taxonomy version
- Sector qualification policy version
- Job configuration snapshot
- Capability snapshot

A running job must not silently switch to newer connector or qualification versions after it starts.

## Phase 3: Plan source runs

The parent orchestrator creates one child source run per selected source.

```text
HarvestJob
├── Google Places source run
├── Yandex source run
└── Website source run
```

Each source produces its own plan, stage definition, cost estimate, and capability warnings.

## Phase 4: Execute source-specific collection

Sources may run sequentially or concurrently according to:

- Source limits
- Resolution consistency requirements
- Cost policy
- Worker capacity
- User quality mode
- Concurrency-safety guarantees

Parallel source execution must not create duplicate canonical institutions because separate transactions cannot see one another’s uncommitted records. The implementation must use a safe concurrency strategy before mixed-source parallelism is enabled.

## Phase 5: Persist raw evidence incrementally

Raw records and source events must be written during execution, not only after the entire external crawl or API session finishes.

This allows the UI to show real progress and ensures partial evidence is not lost when a worker fails.

## Phase 6: Normalize and resolve entities

```text
Raw evidence
→ Normalize fields
→ Generate match candidates
→ Score candidates
→ Resolve automatically when safe
→ Queue ambiguous matches for human review
→ Create or enrich canonical institution, branch, person, and contact records
→ Persist provenance
```

## Phase 7: Enrich and verify

Planned checks include:

- Contact normalization
- Public-listing evidence
- Duplicate contact detection
- Person/contact attribution confidence
- Source corroboration
- Operating-status confidence
- Website reachability and crawl coverage
- Detection status
- Data freshness
- Suppression eligibility
- Conflicting evidence
- Stale evidence

## Phase 8: Apply sector and objective qualification

The job selects the correct qualification policy and creates a versioned assessment for each institution.

## Phase 9: Score opportunities

Qualification answers whether the lead may enter the usable lead pool.

Opportunity scoring answers how relevant and valuable the lead appears.

These must remain separate.

## Phase 10: Accept results

A candidate counts toward the requested target only when it satisfies the job’s acceptance requirements.

Example:

```text
412 raw candidates discovered
183 canonical institutions resolved
146 qualification assessments completed
121 contactable institutions
100 accepted verified leads
```

The job stops when one of the following occurs:

- Target accepted count reached
- Maximum candidate budget reached
- Every selected source is exhausted
- A mandatory source fails and policy requires failure
- User cancels the job

## Phase 11: Finalize frozen result set

Every accepted, rejected, and review-required result receives a `HarvestJobResult` record with the score, policy version, source contribution, and reasons that applied at completion.

---

# 9. Live Harvest Run UI

## 9.1 Parent job summary

The page should show:

```text
Harvest Run: Islamabad Private Schools
Target: 100 verified leads
Accepted: 47
Candidates: 186
Sources complete: 1 of 3
Overall status: Running
```

## 9.2 Separate UI workflow for each source

Every source receives an expandable source card rendered from backend-provided workflow definitions.

Example:

```text
Google Places
● Fetching place details
92 candidates discovered
63 records processed
4 requests remaining
```

```text
Website Discovery
● Crawling organization websites
74 domains discovered
48 crawled
6 blocked
3 failed
```

```text
Yandex Maps
✓ Completed with warnings
48 candidates discovered
39 accepted for resolution
```

## 9.3 Backend-driven stage rendering

The frontend must not hardcode source workflow logic such as:

```typescript
if (source === "google") {
  renderGoogleSteps();
}
```

The backend should return:

```json
{
  "source": "google_places",
  "connector_version": "2.1.0",
  "workflow_version": "3",
  "stages": [
    {
      "key": "geographic_planning",
      "name": "Preparing map coverage",
      "status": "completed",
      "processed": 12,
      "total": 12,
      "metrics": {}
    },
    {
      "key": "place_search",
      "name": "Searching Google Maps",
      "status": "running",
      "processed": 26,
      "total": 40,
      "metrics": {
        "places_found": 92
      }
    }
  ]
}
```

The frontend becomes a generic renderer for:

- Stage name
- Description
- Status
- Progress
- Metrics
- Warnings
- Errors
- Child activities
- Retry state
- Pause and cancellation capability

A future connector update may add, remove, rename, or reorder internal stages without requiring the frontend to understand that source’s implementation.

## 9.4 Live event delivery

Recommended endpoint:

```http
GET /api/v1/harvest-jobs/{job_id}/events
```

Server-Sent Events are appropriate for one-way live progress. Commands such as pause, resume, cancel, or retry should remain ordinary authenticated API calls.

## 9.5 Progress integrity rule

The UI must display real backend progress only.

It must not animate a fake percentage according to elapsed time. When a total is unknown, show indeterminate activity with concrete metrics such as requests completed, pages crawled, records normalized, or institutions resolved.

---

# 10. Sector-specific qualification system

## 10.1 Qualification principle

Each sector requires its own versioned qualification policy.

A hospital, school, law firm, property company, retailer, and hotel cannot be evaluated using one universal checklist. They have different operating models, evidence, scale signals, decision-makers, regulatory contexts, and NEWAX opportunities.

Qualification must consider:

```text
Sector
+
Lead type
+
Organization type
+
Campaign or assessment objective
```

Example policy identity:

```text
education / admissions_automation / private_school / version_3
```

## 10.2 Universal eligibility safeguards

These apply across sectors:

- Canonical organization identity exists.
- Operating status is acceptable.
- At least one usable contact method exists when the objective requires contactability.
- Contact is not suppressed for the intended channel.
- Data confidence meets the minimum threshold.
- Evidence is recent enough for the decision.
- Organization is not excluded by NEWAX ethical policy.
- Organization is not already in an incompatible active campaign.
- Organization is not an existing customer when the job excludes customers.
- Ambiguous identity conflicts are not treated as qualified facts.

## 10.3 Policy rule types

Each sector policy should define:

- Required rules
- Weighted rules
- Disqualifying rules
- Review-trigger rules
- Evidence requirements
- Minimum qualification score
- Staleness limits
- Opportunity signals
- Allowed and excluded organization types
- Allowed source types for specific claims
- Objective-specific overrides

## 10.4 Planned policy model

Suggested `SectorQualificationPolicy` responsibilities:

```text
id
sector_id
lead_type
organization_type
campaign_objective
version
status
rule_definition
minimum_score
effective_from
retired_at
created_by
created_at
updated_at
```

## 10.5 Planned qualification assessment

Every assessment must preserve:

```text
institution_id
harvest_job_id
policy_id
policy_version
status
score
criterion_results
evidence_snapshot
rationale
assessed_at
```

Historical assessments must not silently change when a policy is edited later.

## 10.6 Qualification outcomes

Use three principal outcomes:

### Qualified

All required rules pass and the qualification score reaches the threshold.

### Disqualified

A mandatory requirement or hard exclusion fails.

### Needs review

Evidence is missing, conflicting, stale, or too uncertain for an automated decision.

Example:

```json
{
  "status": "needs_review",
  "score": 61,
  "threshold": 65,
  "policy_version": 3,
  "passed": [
    "active institution",
    "public contact available",
    "education sector match"
  ],
  "failed": [],
  "uncertain": [
    "branch count not confirmed",
    "student portal status not checked"
  ],
  "rationale": "Potential fit, but operational scale and portal evidence require review."
}
```

## 10.7 Education policy examples

Possible qualification dimensions:

- School, college, university, academy, or training organization
- Operating status
- Reachable administration
- Admissions or student operations
- Branch count or scale indicators
- Student, parent, or faculty workflow complexity
- Manual admissions, attendance, fee, or communication signals
- Existing portal or LMS evidence state
- Multi-campus reporting requirements

Relevant NEWAX outcomes:

- Simplify admissions
- Improve student-operation visibility
- Centralize communication
- Reduce manual administration
- Strengthen institutional control

## 10.8 Healthcare policy examples

Possible dimensions:

- Clinic, hospital, laboratory, rehabilitation center, or healthcare network
- Active facility identity
- Reachable administration or management
- Appointment, patient coordination, inventory, reporting, or branch complexity
- Multiple departments or locations
- Secure operational-system requirements

Safeguards:

- Do not collect unnecessary patient information.
- Do not infer patient medical conditions.
- Do not treat sensitive personal health data as sales evidence.

Relevant NEWAX outcomes:

- Improve operational coordination
- Strengthen visibility
- Reduce manual handoffs
- Protect sensitive workflows

## 10.9 Real estate policy examples

Possible dimensions:

- Developer, agency, property manager, facility operator, or real-estate group
- Active portfolio or listings
- Number of properties, agents, branches, or developments
- Lead distribution and follow-up complexity
- Inventory and availability visibility
- Facility or connected-infrastructure requirements

A solo agent may qualify for one objective and fail another. Sector alone must not determine qualification.

## 10.10 Legal policy examples

Possible dimensions:

- Structured legal firm or legal-services organization
- Multiple lawyers, departments, or offices
- Matter intake and document complexity
- Client communication and deadline-management requirements
- Secure internal workflow requirements
- Reachable administrative or partner-level contact

Relevant NEWAX outcomes:

- Improve matter visibility
- Strengthen document control
- Simplify client intake
- Build dependable internal operations

## 10.11 Hospitality policy examples

Possible dimensions:

- Hotel, restaurant group, venue, or hospitality operator
- Active public operation
- Reservation and guest-service workflow
- Inventory and staff coordination
- Multiple departments or branches
- Facility monitoring or connected-infrastructure needs

NEWAX ethical industry restrictions must be checked before qualification.

## 10.12 Retail policy examples

Possible dimensions:

- Active retailer, chain, distributor, or omnichannel seller
- Number of locations or channels
- Inventory and procurement complexity
- Order and customer-operation complexity
- Centralized reporting requirements
- Reachable management

## 10.13 Islamic finance policy examples

Possible dimensions:

- Sharia-compliant financial institution, Islamic fintech, or approved takaful-related organization
- Regulatory and operating legitimacy
- Approval, record, reporting, and integration complexity
- Secure data and workflow-control requirements

Conventional interest-based financial operations must be excluded according to NEWAX policy.

## 10.14 Professional services policy examples

Possible dimensions:

- Structured firm rather than an informal isolated operator
- Repeatable client-delivery processes
- Multiple team members or service lines
- Client onboarding, task, document, or reporting complexity
- CRM and workflow-automation opportunity

## 10.15 Qualification versus opportunity score

These are different decisions.

### Qualification

```text
Should this organization enter the usable lead pool for this objective?
```

### Opportunity scoring

```text
How valuable, timely, and relevant does the opportunity appear?
```

A lead can be qualified but have a low opportunity score because its infrastructure is already mature.

A lead can show a large service gap but still be disqualified because it is unreachable, prohibited, permanently closed, or based on insufficient evidence.

---

# 11. Generated Leads, Master Leads, and Lead Dossier

## 11.1 Generated Leads

Shows results belonging to one `HarvestJob`.

Required capabilities:

- Frozen job result list
- Search
- Filters for every important column
- Sort
- Select current page or all filtered results
- Export selected results
- Email an export or secure download link
- Review rejection reasons
- Open Lead Dossier
- Start Communicator setup for eligible selected leads

## 11.2 Master Leads

Shows canonical leads across every harvest.

Required capabilities:

- Server-side global search
- Server-side filters and sorting
- Canonical institution rows rather than one row per source appearance
- Harvest history
- Source confirmation count
- Current score and qualification
- Communication status
- Suppression status
- Saved views
- Column selection and ordering
- Bulk actions
- Selected-ID export
- Communicator handoff
- NEWAX Core handoff

## 11.3 Lead Dossier

The dossier should aggregate:

- Canonical organization identity
- Sector and organization type
- Operating status
- Locations and branches
- Every contact point
- People and decision-maker candidates
- Contact attribution confidence
- Website intelligence
- Technology and service-gap detection states
- Opportunity analysis
- Qualification assessment and policy version
- Lead score and score history
- Evidence and provenance
- Source and harvest history
- Data-quality flags
- Communication readiness
- Campaign history
- Compliance and suppression status
- Audit activity
- Internal notes and ownership

Facts, detected signals, inferences, and missing evidence must be visually distinguishable.

---

# 12. Export requirements

Current CSV and JSON export should evolve to support:

- Selected lead IDs
- Current filtered result set
- Saved view
- Entire completed harvest result
- Entire Master Leads scope, subject to permission and limits
- CSV
- Excel
- JSON
- Management summary
- Custom field selection
- Export presets
- Background export jobs for large datasets
- Export audit records
- Secure expiring download links
- Email delivery of small files or secure links

Suppressed contacts may be present in a data extract, but every export must clearly carry suppression and communication-eligibility fields.

---

# 13. Communicator handoff

The planned **Run Communicator** action must not immediately send messages.

Required flow:

```text
Selected leads
→ Validate canonical IDs
→ Freeze audience snapshot
→ Check suppression and do-not-contact state
→ Check approved available channels
→ Exclude incompatible active campaigns
→ Select campaign objective
→ Select communication channels
→ Select or create sequence
→ Configure personalization
→ Configure limits, schedule, and timezone
→ Require human approval where configured
→ Create Communicator campaign
→ Generate drafts
→ Review
→ Send
→ Pause on reply and record outcomes
```

Planned campaign models should include:

- `CommunicatorCampaign`
- `CommunicatorAudienceSnapshot`
- `CommunicatorRecipient`
- `CommunicatorSequence`
- `CommunicatorSequenceStep`
- `CommunicatorMessage`
- `CommunicatorDeliveryAttempt`
- `CommunicatorReply`

The existing `AccountBrief`, `OutreachDraft`, and `OutreachOutcome` models should be evaluated for reuse or migration rather than abandoned by default.

Audience membership must be frozen when the campaign is created. Later edits to a saved view or lead list must not silently add or remove recipients from an active campaign.

---

# 14. Source and policy upgrades

## 14.1 Version every execution

Every source run must record:

- Connector version
- Workflow version
- Normalization version
- Source API version
- Taxonomy version
- Qualification policy version
- Configuration snapshot

## 14.2 Upgrade rules

1. New jobs use the latest approved connector and policy versions.
2. Running jobs remain pinned to the versions selected at start.
3. Old runs remain readable using their stored workflow definition.
4. Resume must use the same versions unless an explicit migration exists.
5. Connector upgrades require contract tests for normalized evidence.
6. Workflow upgrades require schema compatibility checks.
7. Rollback must be possible when a source update fails.
8. Historical results must retain their original score and qualification context.
9. Requalification or rescoring must be an explicit operation.
10. Platform changes must be isolated inside the relevant connector wherever possible.

A run started with Google Connector `2.1.0` and workflow `3` must not resume halfway through with Connector `2.2.0` and workflow `4` merely because deployment happened overnight.

---

# 15. Reliability and operations

## 15.1 Idempotency

- Harvest Job creation should support idempotency keys.
- External source pages or records must use stable source identifiers where possible.
- Retries must not create duplicate canonical entities or duplicate campaign recipients.
- Outbound events must reuse stable event IDs across retries.

## 15.2 Concurrency

Before mixed-source parallel processing is enabled, entity resolution must safely handle simultaneous records for the same organization.

Possible mechanisms include:

- PostgreSQL advisory locks by normalized identity key
- Durable resolution queue
- Safe uniqueness constraints
- Short per-record transactions with post-commit reconciliation

The chosen mechanism must be proven with concurrent tests.

## 15.3 Pause and resume

A resumable connector must persist:

- Current stage
- Pagination cursor
- Search-area cursor
- Remaining query plan
- Processed source IDs
- Quota and cost state
- Last successful checkpoint

Pause and cancellation must be cooperative. A worker should stop at safe checkpoints and preserve durable state.

## 15.4 Failure isolation

- One malformed record must not fail an entire source run.
- One failed source must not necessarily fail the parent job unless policy requires it.
- Source completion with partial failures should use `COMPLETED_WITH_WARNINGS`.
- Every skipped or rejected record should have a reason.
- Dead-letter or stranded work must be visible and recoverable.

## 15.5 Observability

Required metrics include:

- Job and source duration
- Stage duration
- Records per stage
- API requests
- Crawl requests
- Retry counts
- Rate-limit events
- Source errors
- Resolution outcomes
- Qualification outcomes
- Accepted-result yield
- Cost per accepted lead
- Source contribution per accepted lead
- Duplicate rate
- Review rate
- Suppression rate
- Export volume
- Communicator eligibility rate

Logs should be structured and include job ID, source-run ID, stage-run ID, raw-record ID, institution ID, and request ID where applicable.

---

# 16. Security, compliance, and source governance

The system must:

- Respect source API terms, website terms, `robots.txt`, and applicable law.
- Use official APIs or authorized data wherever required.
- Never bypass authentication, CAPTCHAs, access controls, or platform restrictions without an explicitly approved and lawful method.
- Avoid sensitive personal data that is not required for the business purpose.
- Preserve evidence and provenance.
- Support suppression, deletion, retention, and audit requirements.
- Protect secrets and source sessions.
- Apply SSRF protections to website crawling.
- Limit response size, redirects, protocols, and network destinations.
- Separate organizational contact evidence from personal contact attribution.
- Require human review before outbound communication when policy requires it.
- Stop communication on opt-out or suppression.

LinkedIn or equivalent professional-network automation must remain restricted until its approved operating model is documented and implemented.

---

# 17. Planned APIs

Conceptual API surface:

```http
POST   /api/v1/harvest-jobs
GET    /api/v1/harvest-jobs
GET    /api/v1/harvest-jobs/{job_id}
POST   /api/v1/harvest-jobs/{job_id}/pause
POST   /api/v1/harvest-jobs/{job_id}/resume
POST   /api/v1/harvest-jobs/{job_id}/cancel
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
```

These routes are planned interfaces, not claims about currently available endpoints.

---

# 18. Implementation sequence

The recommended order is:

## Phase A: prerequisite correctness and security

- Authentication and authorization hardening
- Institution-scoped website snapshot linkage
- Evidence-aware detection statuses
- Complete deletion graph and retention behavior
- Transactionally correct outbox behavior
- Entity-resolution concurrency protection
- LinkedIn restriction and session protection
- Migration-driven test setup
- Complete contact materialization
- Prompt-injection and research-evidence controls
- Runtime frontend configuration and real authentication

## Phase B: Harvest Job foundation

- `HarvestJob`
- Parent-child source-run relationship
- Source workflow definitions
- Stage-run persistence
- Event stream
- Job configuration validation
- Version snapshots
- Pause/cancel state machine

## Phase C: connector adaptation

- Adapt Google Places to source-run contract
- Adapt Yandex
- Adapt Apple Maps
- Adapt website crawler with incremental persistence
- Adapt authorized imports
- Adapt Telegram
- Redesign restricted professional-network workflow around person and organization resolution

## Phase D: qualification policies

- Versioned sector policies
- Policy editor and validation
- Universal safeguards
- Objective-specific policies
- Assessment snapshots
- Requalification workflow

## Phase E: result and dossier APIs

- Frozen Harvest Job results
- Master Leads search
- Complete Lead Dossier aggregation
- Selected-ID exports
- Saved views

## Phase F: Communicator

- Campaign model
- Audience snapshots
- Sequence model
- Channel eligibility
- Human approval
- Sending controls
- Reply and outcome tracking

## Phase G: UI

- Generate Leads
- Adaptive Harvest Run
- Generated Leads
- Master Leads
- Lead Dossier
- Communicator campaign setup and monitoring

---

# 19. Acceptance criteria for the new workflow

The planned architecture is not complete until the following are proven:

1. An authorized user can create a harvest job from the UI or API.
2. The request pins source, workflow, taxonomy, normalization, and qualification-policy versions.
3. Multiple selected sources create separate child runs under one parent job.
4. Every source displays its real, source-specific workflow through backend-provided stages.
5. The UI does not fabricate progress.
6. Raw evidence is persisted incrementally and remains auditable.
7. Concurrent sources do not create duplicate canonical institutions for the same organization.
8. Ambiguous matches enter human review without being hidden by an automatic merge.
9. Website absence claims distinguish confirmed absence from lack of detection or crawl failure.
10. Each sector and objective uses the correct versioned qualification policy.
11. Qualification and opportunity scoring remain separate.
12. Accepted results are frozen for the completed job.
13. Master Leads shows canonical records across every harvest.
14. Lead Dossier exposes facts, inferences, uncertainty, evidence, and history.
15. Selected leads can be exported by ID.
16. Selected eligible leads can create a frozen Communicator audience.
17. Suppressed or do-not-contact recipients cannot be sent messages.
18. Campaign creation does not automatically send before required approval.
19. Pause, resume, retry, cancel, and partial failure states work and are tested.
20. Full migrations, tests, security checks, builds, runtime workflow validation, and CI pass against the exact final commit.

---

# 20. Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Copy and configure environment variables:

```bash
cp .env.example .env
```

Examples may include:

```bash
export GOOGLE_PLACES_API_KEY="..."
export YANDEX_MAPS_API_KEY="..."
export BRAVE_SEARCH_API_KEY="..."
export LEAD_HARVESTER_USER_AGENT="NEWAXLeadHarvester/1.0 (+https://newax.co/contact)"
```

Use an approved secret manager in deployed environments.

---

# 21. Current run examples

## Website seeds

`job.yaml`:

```yaml
seeds:
  - https://www.lums.edu.pk/
  - https://nust.edu.pk/
  - https://www.fast.edu.pk/

sector: education
```

Run:

```bash
lead-harvester run --config job.yaml
```

## Search-discovered website seeds

```yaml
search_queries:
  - private schools Islamabad
  - colleges Rawalpindi

sector: education
```

Requires `BRAVE_SEARCH_API_KEY`.

## Google Places

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

## Yandex Maps

```yaml
places_provider: yandex
cities:
  Islamabad:
    - F-8
categories:
  - FORMAL_EDUCATION
sector: education
```

## Authorized import

```bash
lead-harvester import-authorized \
  --file licensed-leads.csv \
  --source-reference "Contract ABC / Dataset 2026-08" \
  --country-code PK
```

---

# 22. Verification

Current development checks:

```bash
ruff check .
ruff format --check .
pytest -q
```

Database changes must also validate the complete Alembic chain against PostgreSQL.

Frontend changes must run the repository’s type-check, lint, formatting, and build commands.

A change is complete only after the latest commit passes the relevant local checks, runtime workflow validation, security checks, and CI without unresolved issues.

---

# 23. Governing design principles

1. **Different source workflows, one orchestration standard.**
2. **One canonical lead database, not one database per source or run.**
3. **Raw evidence is immutable; canonical records are resolved views.**
4. **Facts, detections, inferences, and unknowns are distinct.**
5. **No detection is not proof of absence.**
6. **Qualification is sector-, objective-, and version-specific.**
7. **Qualification and opportunity ranking are separate.**
8. **The backend defines source stages; the frontend renders them.**
9. **Every run is versioned and historically explainable.**
10. **External failures are expected and must be recoverable.**
11. **No outreach begins without eligibility checks and required approval.**
12. **The system should do the work; the operator should remain in control.**
