# Harvester Input-Page Output Selection Specification

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not started**  
Audience: **Harvester product, frontend, backend, data, compliance, QA and release engineers**

## 1. Purpose

This document defines the **Output Selection** part of Harvester's guided input and market-definition page.

The output section answers:

> What should Harvester produce from this configuration, how much should it produce, which fields and evidence should be included, and where may the result be delivered?

The section extends Step `P — Configure contact and output policy` in the [Frontend Configuration and Responsive UI Delivery Plan](frontend-configuration-and-responsive-ui-delivery-plan.md).

The output selection is a governed result contract. It is not merely a file-format dropdown.

The locked flow is:

```text
Provider
→ active offering
→ lead-generation profile
→ sectors
→ domains
→ independent activities
→ keyword and signal profiles
→ sources, geography and evidence rules
→ output selection
→ validation and preview
→ review and approval
→ immutable Harvest Job snapshot
→ governed result generation
```

## 2. Intended business outcome

An authorized operator must be able to define the exact result Harvester is permitted to create without:

- direct database access
- command-line configuration
- undocumented API calls
- silently inherited output fields
- automatic publication to external systems
- lowering qualification standards merely to fill a requested quota
- exposing restricted evidence or contact data

The interface should let an operator request useful lead intelligence while preserving provider capacity, evidence quality, privacy, consent, suppression, jurisdiction, destination and publication rules.

## 3. Product boundary

Output selection defines the result contract for a future Harvest Job.

It is separate from:

- **Source configuration**, which controls where evidence may be collected.
- **Keyword configuration**, which controls how evidence may be discovered.
- **Qualification**, which determines whether a record satisfies approved criteria.
- **Daily selection**, which reserves eligible leads for operational use.
- **Exports**, which download already-authorized records.
- **Publication**, which sends approved data to an external product or endpoint.
- **Outreach**, which remains governed by Communicator or another approved delivery system.

Generating a result does not automatically export, publish, contact or message anyone.

## 4. Location in the input page

The Output Selection section appears after the operator has configured:

1. Provider and business unit
2. Active offering
3. Lead-generation profile
4. Broad sectors
5. Domains inside each selected sector
6. Activities independently inside every selected domain
7. Domain, activity and organization keyword profiles
8. Offering-specific signal profiles
9. Approved sources
10. Geography and locale
11. Evidence, freshness and contradiction controls
12. Contact policy

The operator may view the output step earlier, but cannot validate it fully until the required upstream configuration exists.

Recommended step label:

> **Select Output**

Supporting instruction:

> Choose what Harvester should produce, how much evidence and detail to include, and where approved results may be delivered.

## 5. Output selection structure

The page must group output configuration into seven areas:

```text
A. Result purpose
B. Quantity and capacity
C. Eligibility and quality
D. Fields and evidence depth
E. Ordering and deduplication
F. Destination and format
G. Delivery timing and retention
```

A desktop layout may use a left-side form with a sticky readiness summary.

A mobile layout must use a single-column step flow with a summary sheet or final review page.

## 6. Result purpose

The operator selects one **primary output** and may enable compatible supporting artifacts.

### 6.1 Primary output types

| Code | Output type | Purpose |
| --- | --- | --- |
| `LEAD_INTELLIGENCE_RESULTS` | Lead Intelligence Results | In-app evidence-backed organization results for research and review |
| `QUALIFIED_LEAD_LIST` | Qualified Lead List | Organizations that satisfy the approved qualification and opportunity rules |
| `DAILY_SELECTION_QUEUE` | Daily Selection Queue | Eligible leads prepared for controlled reservation and operational consumption |
| `ACCOUNT_BRIEFS` | Account Briefs | Evidence-backed organization summaries for research or sales preparation |
| `CONTACT_READY_RECORDS` | Contact-Ready Records | Qualified records with policy-approved responsible-person or contact-route evidence |
| `OUTREACH_DRAFT_CANDIDATES` | Outreach Draft Candidates | Records eligible to proceed to a separate readiness and draft-review process |
| `EVIDENCE_REVIEW_DATASET` | Evidence Review Dataset | Records and evidence prepared for human quality, taxonomy or classifier review |
| `INTEGRATION_PUBLICATION_PAYLOAD` | Integration Publication Payload | Approved records prepared for an optional Core, Communicator or webhook adapter |

### 6.2 Supporting artifacts

Depending on the primary output, the operator may request:

- score and confidence summary
- evidence digest
- full account dossier
- exclusion and contradiction report
- source coverage report
- rejected-record reason summary
- run manifest
- schema and version manifest

Supporting artifacts must not change lead eligibility.

### 6.3 Compatibility rules

- `CONTACT_READY_RECORDS` requires an approved contact policy.
- `OUTREACH_DRAFT_CANDIDATES` requires an active offering, readiness rules and allowed channel policy.
- `DAILY_SELECTION_QUEUE` requires capacity and reservation settings.
- `INTEGRATION_PUBLICATION_PAYLOAD` requires an enabled and authorized destination.
- `EVIDENCE_REVIEW_DATASET` may include records that are not qualified, but they must remain visibly classified as review data rather than leads.
- An output type may never bypass suppression, consent, jurisdiction, conflict, evidence or permission rules.

## 7. Output presets

Presets reduce setup effort but must remain inspectable and editable.

Recommended presets:

### 7.1 Research discovery

```text
Primary output: Lead Intelligence Results
Evidence depth: Standard
Contact data: Excluded
Destination: In-app
Thresholds: Broad discovery with explicit uncertainty
```

### 7.2 Qualified lead list

```text
Primary output: Qualified Lead List
Evidence depth: Standard
Contact data: Organization routes only unless separately approved
Destination: In-app with optional CSV or JSON export
Thresholds: Approved qualification and opportunity policy
```

### 7.3 Daily operational queue

```text
Primary output: Daily Selection Queue
Evidence depth: Summary
Contact data: Policy-approved routes only
Destination: Daily Selection workspace
Thresholds: Operational eligibility and capacity controls
```

### 7.4 Full account research

```text
Primary output: Account Briefs
Evidence depth: Full dossier
Contact data: According to research policy
Destination: In-app
Thresholds: High evidence quality and traceability
```

### 7.5 Controlled integration

```text
Primary output: Integration Publication Payload
Evidence depth: Selected fields
Contact data: Destination-specific allowlist
Destination: Approved adapter or signed webhook
Thresholds: Publication eligibility and schema compatibility
```

Presets must never silently activate a source, channel, destination, service offering or contact policy.

## 8. Quantity and capacity

The output step must let the operator define a target without implying that Harvester will manufacture weak leads to meet it.

### 8.1 Required controls

- target result count
- hard maximum result count
- optional reserve count
- maximum per sector
- maximum per domain
- maximum per geography
- maximum per organization group where applicable
- provider capacity limit
- per-run cost or budget limit where supported

### 8.2 Quantity rules

1. The requested count is a target, not a guarantee.
2. Harvester must return fewer records when fewer records satisfy the approved rules.
3. Qualification, evidence, suppression or compliance thresholds must never be lowered silently to fill a quota.
4. A zero-result outcome is valid when no eligible record exists.
5. The preview must show why the estimated result count is below the requested target.
6. The interface must distinguish:
   - target count
   - eligible estimate
   - hard cap
   - actual produced count
7. Capacity constraints must apply before publication or reservation.

## 9. Eligibility and quality controls

The operator selects or confirms the minimum output conditions.

### 9.1 Possible controls

- minimum qualification status
- minimum opportunity status
- minimum composite lead score
- minimum entity confidence
- minimum domain confidence
- minimum activity confidence
- minimum signal confidence
- minimum source diversity
- maximum evidence age
- required operating-status state
- permitted detection statuses
- contradiction policy
- unresolved quality-flag policy
- manual-review requirement
- responsible-function evidence requirement
- contact-route verification requirement

### 9.2 Locked rules

- Raw keyword-match count is not an output threshold.
- One source copied across several websites does not satisfy source diversity.
- `NOT_CRAWLED`, `CRAWL_FAILED`, `NOT_DETECTED` and `ABSENT_CONFIRMED` remain distinct.
- Unresolved contradictions must be shown, not averaged into an unexplained confidence number.
- The operator may choose stricter thresholds than the profile default.
- Relaxing an approved threshold creates a new draft version and requires validation and review.

## 10. Field selection

The operator selects output field groups rather than confronting one enormous list of database columns, humanity having suffered enough.

### 10.1 Organization identity

Possible fields:

- canonical organization ID
- legal name
- display name
- organization type
- operating status
- website
- locations
- parent or group relationship
- identifiers where authorized

### 10.2 Market classification

Possible fields:

- broad sectors
- selected domains
- approved activities
- organization-type assessment
- geographic fit
- provider-offering fit
- market-definition version

### 10.3 Opportunity and qualification

Possible fields:

- qualification status
- opportunity status
- lead score
- score dimensions
- service-opportunity references
- positive signals
- negative signals
- existing-solution state
- replacement or integration relevance
- rejection or exclusion reasons

### 10.4 Evidence

Possible fields:

- evidence summary
- source classes
- source references
- matched terms and profiles
- context excerpts within policy limits
- event date
- collection date
- freshness state
- source suitability
- duplicate-origin group
- contradiction state
- provenance references

### 10.5 People and contact routes

Possible fields:

- responsible function
- person candidate
- job title or role cue
- organization email
- person email
- phone
- public contact route
- contact verification state
- consent state
- suppression state
- channel eligibility

People and contact fields require field-level permission and policy approval.

### 10.6 Operational metadata

Possible fields:

- Harvest Job ID
- output specification version
- query execution references
- profile versions
- schema version
- generation timestamp
- review state
- publication state
- audit reference

### 10.7 Field rules

- Required identifiers and version metadata cannot be removed from machine-readable outputs.
- Restricted raw-source payloads must not be selectable.
- Secret values, credentials and internal security configuration must never appear.
- Contact data is excluded by default unless the selected output and policy permit it.
- Selecting a field group must display which exact fields are included.
- Destination-specific field allowlists may be stricter than the operator's selection.

## 11. Evidence depth

The operator chooses one of the following default evidence depths.

### 11.1 Summary

Includes:

- organization identity
- primary classification
- qualification and opportunity state
- top supporting signals
- confidence summary
- critical warnings
- traceability references

### 11.2 Standard

Includes Summary plus:

- selected activities
- score dimensions
- source diversity
- evidence freshness
- positive and negative evidence digest
- contradiction summary
- selected contact-policy fields

### 11.3 Full dossier

Includes Standard plus:

- complete approved evidence list
- source and collection provenance
- profile and query contribution
- version history references
- quality flags
- review decisions
- detailed opportunity rationale

Full dossier does not mean unrestricted raw data. Source, privacy, retention and licensing rules still apply.

## 12. Ordering and prioritization

Available ordering controls may include:

- composite lead score
- opportunity confidence
- provider-offering fit
- qualification status
- evidence confidence
- source diversity
- recency
- geography priority
- domain priority
- activity priority
- organization size
- most recently changed

The interface must show the primary sort and tie-break order.

Raw keyword counts, contact count or source-page count must not become default ranking methods.

## 13. Deduplication and update behavior

### 13.1 Deduplication unit

The default result unit is one canonical organization.

The operator may include child records such as:

- branches
- locations
- people candidates
- contact routes
- opportunities

without duplicating the organization as several independent leads.

### 13.2 Output update modes

The operator may select:

- all eligible records
- new records since the last successful run
- new or materially changed records
- records with score or qualification changes
- records requiring review
- records not previously published to the selected destination

### 13.3 Locked rules

- Duplicate source origins do not create duplicate evidence diversity.
- Repeated publication uses idempotency keys and destination history.
- A canonical merge or split must be represented explicitly in later outputs.
- Completed outputs retain the identities and versions used at generation time.

## 14. Destination selection

The default destination is **Harvester in-app results**.

Possible destinations:

| Destination | Purpose |
| --- | --- |
| In-app results | Review, filtering, research and controlled next actions |
| Daily Selection workspace | Operational reservation and consumption |
| CSV download | Human-readable approved tabular export |
| JSON download | Structured approved export |
| NEWAX Core adapter | Optional canonical or approved lead-context publication |
| Communicator adapter | Optional approved outreach-candidate publication |
| Signed webhook | Approved external integration |

### 14.1 Destination rules

1. Every external destination is disabled until configured and authorized.
2. A destination has its own field allowlist, schema version, scopes, restrictions and rate limits.
3. Selecting Communicator does not start outreach.
4. Selecting NEWAX Core does not transfer Harvester's private tables or database ownership.
5. A webhook requires authentication, signing, retry, idempotency and dead-letter behavior.
6. Destination failure must not erase the local approved output.
7. Partial publication must be visible and retryable.
8. Exports and publications must be audited.

## 15. Format and schema selection

### 15.1 Human downloads

Supported planned formats:

- CSV
- JSON

Additional formats require a separate approved requirement and implementation.

### 15.2 Machine publication

Machine outputs must include:

- schema name
- schema version
- output specification ID and version
- Harvest Job ID
- generation time
- idempotency key
- record identity
- source product identity
- field-level provenance where required

A destination must reject an unsupported schema version clearly rather than accepting a partially understood payload.

## 16. Delivery timing

The operator may select:

- generate after approval
- run once at a scheduled time
- recurring schedule
- manual-only execution
- generate continuously from an approved event trigger where separately supported

Recurring controls may include:

- timezone
- daily or weekly cadence
- selected days
- execution window
- blackout window
- maximum runs per period
- maximum records per run
- next planned run

Scheduling must not exceed provider capacity, source authorization, rate limits or destination limits.

## 17. Retention and history

The output step must define or inherit:

- local result retention
- export availability period
- publication history retention
- evidence-reference retention
- contact-field retention
- deletion and suppression behavior

A completed output must preserve:

- output specification version
- market-definition version
- offering version
- taxonomy versions
- keyword-profile versions
- source and locale configuration
- scoring and policy versions
- selected fields
- destination and schema version

Later configuration changes must not rewrite a historical output.

## 18. Output preview

Before review or activation, the operator must see a preview containing:

- primary output type
- supporting artifacts
- requested count
- estimated eligible count
- hard cap
- selected thresholds
- selected field groups
- evidence depth
- sort and tie-break order
- deduplication unit
- update mode
- destination
- format and schema version
- schedule
- compliance and contact warnings
- estimated source, processing or publication cost where available

The preview should include a small synthetic or authorized sample showing column and record shape.

A preview must not expose unapproved sensitive data merely to demonstrate layout.

## 19. Validation states

### 19.1 Blocking conditions

The output cannot proceed when:

- no primary output is selected
- the provider or offering is inactive
- no market definition exists
- no domain–activity combination is approved
- the requested output requires a contact policy that is incomplete
- an external destination is unauthorized or unavailable
- required schema fields are removed
- the requested count exceeds a hard approved capacity limit
- jurisdiction or channel rules prohibit the selected output
- unresolved critical validation findings remain
- the operator lacks permission

### 19.2 Warning conditions

Warnings may include:

- estimated results below target
- high evidence-age risk
- low source diversity
- heavy concentration in one sector, domain or geography
- large full-dossier output
- high estimated cost
- destination nearing a rate limit
- selected fields likely to be sparse
- non-blocking contradictions
- manual review required before publication

Warnings require acknowledgement where the policy specifies it.

### 19.3 Informational states

Informational notices may explain:

- why a field is required
- why a contact field is disabled
- why a destination is unavailable
- how deduplication works
- why fewer records may be returned
- which version will be frozen into the next Harvest Job

## 20. Save, review and activation lifecycle

Recommended lifecycle:

```text
DRAFT
→ VALIDATING
→ CHANGES_REQUIRED or READY_FOR_REVIEW
→ IN_REVIEW
→ APPROVED
→ SCHEDULED or ACTIVE
→ PAUSED
→ SUPERSEDED
→ ARCHIVED
```

Rules:

- Drafts are autosaved.
- Draft writes use optimistic concurrency.
- Submitted output specifications are immutable review snapshots.
- Approved output specifications are immutable.
- Any material change creates a new version.
- Pausing output does not delete its history.
- Rollback creates a new approved reference to a previously approved version.
- Every state change is permission-checked, tenant-scoped and audited.

## 21. Recommended data model

### `OutputSpecification`

```text
id
workspace_id
provider_id
business_unit_id
offering_id
lead_generation_profile_id
market_definition_version_id
name
primary_output_type
status
version
requested_count
hard_maximum_count
reserve_count
evidence_depth
update_mode
primary_sort
created_by
reviewed_by
approved_by
created_at
updated_at
submitted_at
approved_at
```

### `OutputEligibilityPolicy`

```text
output_specification_id
minimum_qualification_status
minimum_opportunity_status
minimum_lead_score
minimum_entity_confidence
minimum_domain_confidence
minimum_activity_confidence
minimum_signal_confidence
minimum_source_diversity
maximum_evidence_age
contradiction_policy
quality_flag_policy
manual_review_requirement
```

### `OutputFieldSelection`

```text
output_specification_id
field_group
field_code
selection_state
policy_source
required_by_schema
```

### `OutputDestination`

```text
id
output_specification_id
destination_type
destination_reference
format
schema_name
schema_version
field_allowlist_version
status
```

### `OutputSchedule`

```text
output_specification_id
schedule_type
timezone
recurrence_rule
execution_window
blackout_window
maximum_runs_per_period
maximum_records_per_run
next_run_at
```

### `OutputPolicySnapshot`

```text
id
output_specification_version_id
contact_policy_version
suppression_policy_version
jurisdiction_policy_version
consent_policy_version
publication_policy_version
retention_policy_version
```

### `OutputGeneration`

```text
id
output_specification_version_id
harvest_job_id
status
requested_count
eligible_count
produced_count
excluded_count
schema_version
started_at
completed_at
failure_code
```

### `OutputPublication`

```text
id
output_generation_id
destination_id
status
idempotency_key
attempt_count
published_count
rejected_count
last_attempt_at
completed_at
failure_code
```

## 22. Proposed API surface

The final endpoints must be derived from the repository's established API conventions and OpenAPI contract. A possible bounded surface is:

```text
GET    /api/v1/output-options
GET    /api/v1/output-specifications
POST   /api/v1/output-specifications
GET    /api/v1/output-specifications/{id}
PATCH  /api/v1/output-specifications/{id}
POST   /api/v1/output-specifications/{id}/validate
POST   /api/v1/output-specifications/{id}/preview
POST   /api/v1/output-specifications/{id}/submit-review
POST   /api/v1/output-specifications/{id}/approve
POST   /api/v1/output-specifications/{id}/activate
POST   /api/v1/output-specifications/{id}/pause
GET    /api/v1/output-specifications/{id}/versions
GET    /api/v1/output-generations
GET    /api/v1/output-generations/{id}
GET    /api/v1/output-publications
POST   /api/v1/output-publications/{id}/retry
```

No endpoint is approved for implementation merely because it appears in this planning document. Existing repository patterns, authorization, tenant isolation, contracts and module boundaries must be inspected first.

## 23. Permission model

Possible permissions include:

```text
output-specifications.view
output-specifications.create
output-specifications.update-draft
output-specifications.submit-review
output-specifications.approve
output-specifications.activate
output-specifications.pause
output-specifications.view-sensitive-fields
output-specifications.configure-destinations
output-generations.view
output-publications.retry
exports.download
```

Approval and destination configuration should remain separate permissions.

## 24. Responsive and accessibility requirements

The output step must:

- work from 320 CSS pixels through wide desktop
- preserve all material selections on mobile
- provide keyboard access to every control
- expose selected counts and errors programmatically
- avoid relying on color alone
- support visible focus
- use accessible comboboxes and multi-selects
- provide a text equivalent for result-estimate visualizations
- keep the summary available without trapping focus
- announce validation results and background preview completion
- preserve selections when orientation or viewport changes
- avoid horizontal overflow for field and destination tables

Large field lists should use grouping, search, progressive disclosure and summary counts rather than endless checkbox walls.

## 25. Security, privacy and compliance requirements

1. Every read and write is tenant-scoped.
2. Every state change is permission-checked and audited.
3. Sensitive fields require explicit permission.
4. Suppressed contact routes cannot appear in a contact-ready or outreach-candidate output.
5. Exported and published data must follow retention and deletion policy.
6. File downloads require authorization at generation and download time.
7. Signed URLs must be short-lived where used.
8. External publications use scoped credentials and idempotency.
9. Logs must not contain unrestricted output payloads or sensitive contact values.
10. A destination outage must not cause uncontrolled retries.
11. Cross-tenant destination references are prohibited.
12. Preview samples must use synthetic or authorized data.
13. Public-source contact data does not equal outreach consent.
14. A deletion or suppression event must affect future eligibility and governed retained copies according to policy.

## 26. Acceptance criteria

The Output Selection section is accepted only when all applicable criteria pass.

### 26.1 Configuration

- An authorized operator can select one primary output.
- Compatible supporting artifacts can be enabled independently.
- Incompatible selections are blocked with a clear reason.
- Quantity, hard cap and capacity are visibly different.
- The operator can select thresholds without using raw keyword counts.
- Field groups expose their included fields.
- Sensitive fields are disabled without permission.
- Evidence depth is selectable and explained.
- Sort, tie-break, deduplication and update mode are visible.
- The default destination is in-app.
- External destinations remain disabled until configured and authorized.
- Schedule and retention selections are reviewable.

### 26.2 Safety and policy

- Requested quantity never causes silent threshold reduction.
- A zero-result output is permitted.
- Contact-ready output requires contact-policy readiness.
- Outreach-draft candidates do not initiate outreach.
- Suppressed routes cannot be included.
- Jurisdiction and channel restrictions are enforced.
- Required machine-output metadata cannot be removed.
- Historical output specifications remain immutable.

### 26.3 Preview and review

- Preview displays estimated eligible count and exclusion reasons.
- Preview displays exact selected fields and destination schema.
- Preview samples do not expose unapproved sensitive data.
- Blocking and warning findings link to the relevant control.
- The operator can save and resume a draft.
- Submission creates an immutable review snapshot.
- Approval and activation require separate authorized actions.

### 26.4 Responsive and accessibility

- The complete flow works at 320 CSS pixels.
- Keyboard-only operation is possible.
- Screen-reader labels, errors and status announcements are present.
- No material information is hidden solely to fit a narrow screen.
- The summary remains usable on mobile and desktop.

### 26.5 Verification

- API contracts are generated and current.
- Focused component and service tests pass.
- End-to-end tests cover safe and blocked configurations.
- Permission and tenant-isolation tests pass.
- Export and publication retry tests pass where implemented.
- Accessibility checks and manual review pass.
- The exact latest commit passes the applicable complete CI sequence.
- The real create, preview, review, approve and activate workflow is verified.

## 27. Example configuration

```text
Provider:
NEWAX

Offering:
Enterprise Operations Platform

Market:
Healthcare
→ Pharmaceuticals
→ Distribution

Primary output:
Qualified Lead List

Requested count:
100

Hard maximum:
120

Minimum source diversity:
2 independent origins

Evidence depth:
Standard

Fields:
Organization identity
Market classification
Opportunity summary
Evidence digest
Organization contact routes
No person-level contacts

Deduplication:
One canonical organization

Update mode:
New or materially changed since last successful run

Sort:
Provider-offering fit
→ opportunity confidence
→ evidence recency

Destination:
Harvester in-app
Optional CSV download after review

Schedule:
Weekly, Monday 09:00 Asia/Karachi

Policy:
No silent threshold reduction
No automatic publication
No outreach activation
```

## 28. Delivery boundary

This document is a **Proposed** product and delivery specification.

It does not implement:

- database tables or migrations
- APIs or OpenAPI contracts
- React routes or components
- output estimation
- scheduling
- exports
- Core or Communicator adapters
- webhooks
- scoring or qualification changes
- publication or outreach behavior

Runtime work remains subject to repository inspection, acceptance criteria, dependency-ordered implementation, local-equivalent verification, exact-head CI and real-workflow validation.
