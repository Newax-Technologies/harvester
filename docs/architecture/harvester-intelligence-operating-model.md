# Harvester Intelligence Operating Model

Status: **Normative planned architecture**

Authority:

- [Harvester Standalone Product Roadmap](../ROADMAP.md) remains the authoritative 64-module delivery roadmap.
- This document strengthens the operating, data, decision, evidence, and learning model implemented across those modules.
- This document does not create additional top-level modules or a parallel roadmap.

## 1. Product position

Harvester is not merely a scraper, crawler, enrichment utility, or list generator.

Harvester is standalone lead-intelligence infrastructure that turns a governed market definition into evidence-backed, reviewable, and operationally usable opportunities.

```text
Market definition
→ governed source strategy
→ source-native observations
→ evidence graph
→ local entity resolution
→ lead profile
→ qualification
→ opportunity assessment
→ research dossier
→ controlled selection
→ export or optional publication
→ outcome feedback
→ governed learning
```

The business outcome is reduced manual research, stronger operational visibility, better lead quality, faster decision-making, and long-term customer control over data and infrastructure.

Harvester must continue operating when NEWAX Core, Communicator, customer destinations, or external providers are unavailable.

## 2. Strong model principles

The model is governed by twelve principles.

1. **The market is defined before collection starts.**
   Sources do not decide what a useful lead is.
2. **Raw source material is immutable.**
   Interpretation may change; the original evidence does not.
3. **Every material claim is traceable.**
   A fact without evidence is not a fact in Harvester.
4. **Non-detection is not confirmed absence.**
   Coverage and failure states remain explicit.
5. **Resolution, qualification, scoring, and selection are separate decisions.**
   One decision must not silently stand in for another.
6. **Confidence is multidimensional.**
   One decorative percentage must not hide weak coverage, stale evidence, or identity ambiguity.
7. **Automation is bounded by authority.**
   High-impact or ambiguous actions require explicit review.
8. **Current state and historical snapshots are both first-class.**
   Later enrichment must not rewrite what was known at an earlier decision point.
9. **External outcomes create new evidence.**
   They do not erase the source history that preceded them.
10. **Optional integrations are destinations, not dependencies.**
    Harvester owns its local transaction and local identifiers.
11. **The customer controls what leaves Harvester.**
    Connection alone never authorizes publication.
12. **The system should remove operational complexity.**
    Operators define objectives and resolve exceptions; the infrastructure performs repeatable work.

## 3. Eight-plane architecture

The stronger model is organized into eight cooperating planes.

### 3.1 Control plane

Defines what the product is allowed and expected to do.

Owns:

- Tenant and workspace
- Users, teams, permissions, ownership, and assignment
- Market definitions
- Harvest objectives
- Source policies
- Budgets, quotas, and stopping rules
- Environment configuration
- Feature and connector entitlements
- Approval policies
- Model and policy activation

The control plane never stores plaintext secrets and never executes provider-specific collection logic.

### 3.2 Acquisition plane

Executes approved source work through versioned connectors.

Owns:

- Source plans
- Connection and credential references
- Connector capabilities
- Collection stages
- Cursors and checkpoints
- Rate and concurrency controls
- Cost and quota accounting
- Source-native payload capture
- Failure isolation

A source failure affects its own run. It does not erase results from other sources or roll back committed Harvester data.

### 3.3 Evidence plane

Preserves what was observed and what was derived from it.

Owns:

- Raw observations
- Snapshots and documents
- Extracted assertions
- Provenance
- Coverage records
- Contradictions
- Freshness
- Source reliability
- Detection state
- Evidence retention

The evidence plane does not decide whether an entity is commercially useful.

### 3.4 Resolution plane

Determines which observations probably refer to the same local Harvester entity.

Owns:

- Candidate generation
- Match features
- Identity confidence
- Merge, link, reject, and review decisions
- Reversible resolution history
- Conflict workbench
- Harvester-local organization, person, branch, contact, domain, and relationship identity

The resolution plane does not claim NEWAX Core canonical identity.

### 3.5 Intelligence plane

Builds an explainable commercial interpretation from resolved entities and evidence.

Owns:

- Lead profiles
- Organization and person context
- Contact verification
- Signals
- Technology and operational indicators
- Qualification assessments
- Opportunity assessments
- Maturity and service-gap analysis
- Research findings
- Dossiers

The intelligence plane must distinguish observed facts, calculated values, model inferences, operator assessments, and unknown states.

### 3.6 Decision plane

Turns intelligence into governed actions.

Owns:

- Review queues
- Selection rules
- Ranking
- Reservations
- Approvals
- Saved filters and groups
- Frozen job results
- Frozen publication audiences
- Decision records

The decision plane never treats a score as permission to publish or contact.

### 3.7 Activation plane

Moves approved outputs to files, APIs, Communicator, NEWAX Core, or customer destinations.

Owns:

- Export jobs
- Publishing rules
- Payload profiles
- Redaction
- Destination mappings
- Outbox events
- Delivery attempts
- Receipts
- Feedback commands
- Reconciliation

Every destination is separately credentialed, mapped, permissioned, observable, pausable, and recoverable.

### 3.8 Operations and learning plane

Keeps the product reliable and improves decisions without corrupting evidence.

Owns:

- Health and metrics
- Cost and yield analytics
- Alerts and runbooks
- Quality debt
- Outcome feedback
- Evaluation datasets
- Model versions
- Approval and rollout
- Drift detection
- Backup, restore, upgrade, and release governance

Production behavior must never change merely because new feedback arrived. A reviewed and versioned policy or model release is required.

## 4. Core domain objects

The model is built around explicit domain objects rather than loosely related tables.

### 4.1 MarketDefinition

Represents the governed target universe.

```text
id
version
name
business_objective
lead_type
sectors
organization_types
geographies
size_bands
required_characteristics
excluded_characteristics
source_constraints
compliance_constraints
quality_requirements
owner
status
created_at
activated_at
retired_at
```

A MarketDefinition is versioned. Editing it creates a new version rather than changing the meaning of completed jobs.

### 4.2 HarvestJob

Represents one reproducible request to produce a bounded lead result.

```text
id
tenant_id
market_definition_id
market_definition_version
objective
target_count
quality_mode
budget_limit
time_limit
source_mix
acceptance_rules
stopping_rules
pinned_connector_versions
pinned_mapping_versions
pinned_policy_versions
status
created_by
created_at
started_at
completed_at
```

A HarvestJob records the definition used at execution time, not merely a pointer to whatever the current configuration later becomes.

### 4.3 SourcePlan

Defines how one source contributes to a HarvestJob.

```text
id
harvest_job_id
source_type
connection_id
connector_version
workflow_version
query_or_scope
geography_partition
expected_cost
quota
priority
coverage_goal
stop_condition
policy_state
```

Source plans allow the orchestrator to compare expected and actual yield, cost, coverage, and reliability.

### 4.4 SourceRun

Represents one durable execution of a SourcePlan.

```text
id
source_plan_id
attempt
stage
status
cursor
checkpoint
lease_owner
heartbeat_at
records_examined
observations_created
records_rejected
records_quarantined
cost_consumed
quota_consumed
started_at
completed_at
failure_class
```

Retries preserve source identity and checkpoint history rather than pretending the previous attempt never existed.

### 4.5 RawObservation

Preserves one accepted source-native record before interpretation.

```text
id
tenant_id
source_system
source_record_id
source_record_version
source_schema_version
connector_version
captured_at
payload_hash
raw_payload_reference
authority_reference
retention_policy
supersedes_observation_id
```

RawObservation is immutable.

### 4.6 EvidenceArtifact

Preserves the document, page, file, message, image, or response from which assertions were extracted.

```text
id
observation_id
artifact_type
content_hash
storage_reference
source_url
mime_type
fetch_status
captured_at
access_classification
retention_policy
```

Artifacts may be redacted or access-restricted without deleting the existence and audit history of the observation.

### 4.7 EvidenceAssertion

Represents one normalized claim derived from source material.

```text
id
subject_candidate_id
predicate
normalized_value
value_type
assertion_kind
source_observation_id
evidence_artifact_id
extractor_type
extractor_version
source_reliability
extraction_certainty
corroboration_state
freshness_state
coverage_state
valid_from
valid_until
status
```

Allowed assertion kinds:

```text
OBSERVED_FACT
DERIVED_VALUE
MODEL_INFERENCE
OPERATOR_ASSESSMENT
NEGATIVE_EVIDENCE
UNKNOWN
CONFLICT
```

An assertion must not silently change kind.

### 4.8 CoverageRecord

Explains what was searched, inspected, skipped, blocked, or unavailable.

```text
id
source_run_id
scope_type
scope_reference
planned
attempted
completed
blocked_reason
failure_reason
coverage_ratio
observed_at
```

CoverageRecord prevents `NOT_DETECTED` from being misrepresented as `ABSENT_CONFIRMED`.

### 4.9 ResolutionCandidate

Represents a possible identity match before a decision.

```text
id
left_reference
right_reference
candidate_type
match_features
conflict_features
identity_confidence
policy_version
recommended_action
review_state
```

### 4.10 ResolutionDecision

Records a merge, link, reject, split, or review result.

```text
id
candidate_id
decision
rationale
evidence_snapshot
policy_version
model_version
actor_type
actor_id
created_at
reverses_decision_id
```

Resolution decisions are reconstructable and reversible through history. Physical deletion is not used to disguise a mistaken merge.

### 4.11 ResolvedEntity

Represents Harvester's current local view of an organization, person, branch, contact, domain, or relationship.

```text
id
entity_type
revision
current_state
source_links
identity_confidence
quality_state
first_seen_at
last_seen_at
last_material_change_at
```

Harvester IDs remain stable whether or not optional Core identity links exist.

### 4.12 LeadProfile

Represents the current commercial interpretation of a ResolvedEntity.

```text
id
resolved_entity_id
revision
lead_status
market_fit
contactability
organization_profile
person_profile
operational_context
research_summary
quality_state
compliance_state
updated_at
```

A LeadProfile is not the same object as entity identity.

### 4.13 QualificationAssessment

Answers whether the lead belongs in a usable pool under a specific policy.

```text
id
lead_profile_id
policy_id
policy_version
evidence_snapshot_id
required_rule_results
weighted_rule_results
disqualifier_results
review_triggers
outcome
rationale
assessed_at
```

Allowed outcomes:

```text
QUALIFIED
NOT_QUALIFIED
REVIEW_REQUIRED
INSUFFICIENT_EVIDENCE
POLICY_BLOCKED
```

### 4.14 OpportunityAssessment

Ranks a qualified or reviewable lead by fit, value, urgency, and likely operational need.

```text
id
lead_profile_id
model_id
model_version
evidence_snapshot_id
fit_score
need_score
urgency_score
value_score
contactability_score
confidence_dimensions
service_gap_hypotheses
risk_factors
composite_rank
rationale
assessed_at
```

OpportunityAssessment is a prioritization aid. It is not a promise of revenue or permission to contact.

### 4.15 ResearchDossier

Presents the evidence-backed current lead story.

```text
id
lead_profile_id
revision
facts
inferences
unknowns
conflicts
source_coverage
organization_summary
people_summary
contact_summary
operational_signals
opportunity_hypotheses
quality_warnings
compliance_warnings
citations
created_at
```

A dossier must remain useful when optional destinations are absent.

### 4.16 DecisionRecord

Records any material automated or human decision.

```text
id
decision_type
subject_reference
input_snapshot
policy_version
model_version
recommended_action
final_action
rationale
actor_type
actor_id
review_state
created_at
```

Material decisions include resolution, qualification, scoring overrides, publication approval, suppression, deletion, and repair.

### 4.17 SelectionSnapshot

Freezes the exact leads selected at a point in time.

```text
id
selection_type
source_filter_or_job
member_ids
lead_revisions
qualification_revisions
opportunity_revisions
created_by
created_at
```

### 4.18 PublicationPackage

Freezes exactly what was approved for one destination.

```text
id
selection_snapshot_id
destination_id
publishing_rule_id
payload_profile_id
mapping_version
redaction_policy_version
serialized_payload_hash
approval_state
event_ids
created_at
```

A later lead update does not mutate a previously approved PublicationPackage.

### 4.19 OutcomeFeedback

Preserves destination or operator outcomes as new evidence.

```text
id
source_system
source_reference
harvester_entity_id
feedback_type
feedback_value
evidence_reference
observed_at
received_at
trust_level
```

Examples:

```text
CONTACT_VALID
CONTACT_INVALID
BOUNCE
OPT_OUT
REPLIED
INTERESTED
NOT_RELEVANT
CONVERTED
DUPLICATE_REPORTED
IDENTITY_CORRECTION
QUALIFICATION_CORRECTION
```

Outcome feedback never rewrites raw observations.

### 4.20 LearningDataset and ModelVersion

LearningDataset is a governed snapshot assembled from approved evidence and outcomes.

ModelVersion records:

```text
id
model_type
version
training_dataset_id
feature_contract
calibration_results
known_limitations
approval_state
activated_at
retired_at
rollback_target
```

Production models are immutable after activation. A changed model receives a new version.

## 5. Evidence graph

Harvester should model evidence as a graph rather than a pile of flattened fields.

```text
Source
→ Observation
→ Artifact
→ Assertion
→ Candidate entity
→ Resolution decision
→ Resolved entity
→ Lead profile
→ Qualification assessment
→ Opportunity assessment
→ Decision
→ Selection
→ Publication
→ Outcome feedback
```

The graph must support both forward and reverse explanation.

Forward explanation answers:

> What decisions followed from this observation?

Reverse explanation answers:

> Which evidence, policies, models, and actors produced this result?

Every material field in a current lead view should be able to expose:

- Contributing assertions
- Conflicting assertions
- Winning rule
- Confidence dimensions
- Freshness
- Coverage
- Source links
- Decision history

## 6. Detection and absence model

Every detection must use an explicit state.

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_INSPECTED
INSPECTION_BLOCKED
INSPECTION_FAILED
STALE
CONFLICTING
UNKNOWN
```

Rules:

- `NOT_DETECTED` cannot be converted to `ABSENT_CONFIRMED` without a policy-defined inspection scope.
- `INSPECTION_FAILED` cannot lower an opportunity score as though absence were proven.
- `STALE` preserves the historical assertion but prevents it from being treated as current.
- `CONFLICTING` requires resolution or review before high-impact decisions.

## 7. Confidence model

Confidence must be stored as dimensions, not only a single percentage.

Required dimensions:

```text
SOURCE_AUTHORITY
SOURCE_RELIABILITY
EXTRACTION_CERTAINTY
CORROBORATION
IDENTITY_CERTAINTY
FRESHNESS
COVERAGE
POLICY_FIT
OPPORTUNITY_CERTAINTY
```

A composite confidence value may be calculated for sorting, but the dimensions remain visible and queryable.

Example:

```text
Identity confidence: high
Source reliability: medium
Extraction certainty: high
Freshness: low
Coverage: partial
Opportunity certainty: medium
```

This is more useful than reporting `82% confidence` and making everyone pretend the number explains itself.

## 8. Decision contracts

Every major decision type must use a versioned contract.

### 8.1 Evidence contract

Requires:

- Source identity
- Raw observation
- Extractor version
- Assertion kind
- Evidence reference
- Detection state
- Confidence dimensions
- Freshness
- Coverage

### 8.2 Resolution contract

Requires:

- Candidate identities
- Match and conflict features
- Identity policy version
- Recommendation
- Decision
- Rationale
- Evidence snapshot
- Reversal path

### 8.3 Qualification contract

Requires:

- Market definition version
- Qualification policy version
- Evidence snapshot
- Required rules
- Weighted rules
- Disqualifiers
- Review triggers
- Outcome
- Rationale

### 8.4 Opportunity contract

Requires:

- Qualified or reviewable status
- Model version
- Fit, need, urgency, value, and contactability components
- Service-gap hypotheses
- Risk factors
- Confidence dimensions
- Rationale

### 8.5 Publication contract

Requires:

- Selection snapshot
- Destination
- Active publishing rule
- Payload profile
- Mapping version
- Redaction policy
- Approval state
- Exact payload hash
- Idempotency identity

### 8.6 Feedback contract

Requires:

- Source system
- Outcome type
- Harvester reference
- Evidence or receipt
- Trust level
- Observed time
- Processing decision

## 9. Market-definition engine

Before a HarvestJob runs, Harvester must define the intended market in operational terms.

A market definition should answer:

- What type of organization or person is being sought?
- Which sectors and geographies are included?
- Which organization sizes or operating characteristics matter?
- What counts as sufficient evidence?
- Which sources are allowed, restricted, or prohibited?
- What conditions disqualify a record?
- Which opportunity signals matter?
- What quality level is required?
- What budget, time, and quota limits apply?
- What should cause the job to stop?

The market-definition engine prevents a common failure mode: collecting large volumes first and inventing the target later.

## 10. Source strategy and adaptive orchestration

The orchestrator should allocate work according to policy, expected coverage, observed yield, cost, freshness, and source reliability.

It may adapt:

- Query partitions
- Geography partitions
- Provider order
- Concurrency
- Retry timing
- Source budget
- Verification depth
- Research depth

It must not adapt:

- Compliance boundaries
- Tenant boundaries
- Prohibited-source rules
- Publication permission
- Required evidence thresholds
- Model activation

Adaptive decisions require recorded rationale and pinned strategy versions.

### 10.1 Stopping rules

A source or HarvestJob may stop when:

- Target accepted-lead count is reached
- Marginal accepted-lead yield falls below policy threshold
- Budget is exhausted
- Time window expires
- Quota is exhausted
- Coverage target is reached
- Source quality degrades
- Compliance or security block is raised
- Operator pauses or cancels the job

Stopping must be explicit and reproducible.

## 11. Opportunity model

Opportunity intelligence should describe a business hypothesis, not merely a score.

A service-gap hypothesis contains:

```text
hypothesis_type
observed_condition
supporting_evidence
contradicting_evidence
business_impact_hypothesis
NEWAX_capability_alignment
confidence_dimensions
freshness
review_state
```

Initial opportunity dimensions may include:

- Enterprise software need
- Workflow automation need
- Integration need
- Data visibility need
- Customer or staff portal need
- Operational reporting need
- Connected infrastructure need
- Reliability or ownership concern

External messaging should describe business outcomes such as simplicity, reliability, visibility, efficiency, control, and confidence rather than throwing technology acronyms at the customer like confetti.

## 12. Human authority model

Automation is divided into three authority levels.

### 12.1 Automatically permitted

Low-risk, deterministic, reversible actions:

- Normalize known formats
- Deduplicate identical raw payloads
- Apply approved mappings
- Execute approved source plans
- Calculate versioned scores
- Create review items
- Retry idempotent deliveries
- Apply existing suppression rules

### 12.2 Review required

Ambiguous or high-impact actions:

- Merge uncertain identities
- Attribute a person to an organization with weak evidence
- Confirm absence from partial coverage
- Override qualification
- Approve sensitive fields for export
- Publish a high-impact audience
- Repair conflicting synchronization
- Activate a materially changed model or policy

### 12.3 Prohibited

Harvester must not:

- Invent facts, contacts, citations, or outcomes
- Present inference as observed fact
- Bypass authentication, source restrictions, CAPTCHAs, rate limits, or access controls
- Use a score as automatic consent to contact
- Share plaintext credentials
- Write directly into another product's private tables
- Erase evidence to hide a wrong decision
- Auto-merge conflicting identities without policy authority
- Self-modify production rules from unreviewed feedback
- Send campaigns or own conversations

## 13. Governed learning loop

The learning loop improves future decisions while preserving evidence integrity.

```text
Publication or operator action
→ destination or operator outcome
→ OutcomeFeedback
→ validation and trust classification
→ evaluation dataset
→ analysis
→ proposed policy or model version
→ offline evaluation
→ approval
→ staged activation
→ monitoring
→ rollback when required
```

Feedback categories must remain separate:

- Contact validity
- Identity correctness
- Qualification correctness
- Opportunity quality
- Commercial outcome
- Source quality
- Operator correction
- Destination delivery outcome

A conversion does not prove every preceding inference was correct. A rejection does not prove the entity was incorrectly resolved. Learning must respect decision boundaries.

## 14. Model evaluation and calibration

Every probabilistic or ranking model requires an evaluation contract.

Required evaluation areas:

- Identity match quality
- Qualification decision quality
- Opportunity ranking quality
- Confidence calibration
- Source and geography bias
- Sector performance
- Freshness sensitivity
- Missing-data behavior
- Adversarial and prompt-injection resistance where language models are used
- Regression against previously approved datasets

Model changes must report:

- Dataset version
- Sampling method
- Evaluation metrics
- Comparison with active model
- Known weaknesses
- Affected tenants or sectors
- Rollout plan
- Rollback plan

## 15. Cost, yield, and operational economics

Harvester should optimize for useful verified outcomes, not raw record volume.

Required source and job metrics:

```text
records_examined
observations_created
unique_entities_resolved
qualified_leads
review_required
accepted_leads
verified_contacts
cost_consumed
time_consumed
operator_minutes
```

Derived metrics:

```text
observation_yield
unique_entity_yield
qualification_yield
accepted_lead_yield
verified_contact_yield
cost_per_accepted_lead
time_to_verified_dossier
operator_minutes_per_accepted_lead
source_overlap
source_exclusivity
stale_data_rate
conflict_rate
review_rate
```

Cost optimization must not weaken evidence, compliance, tenant isolation, or source-policy controls.

## 16. Quality debt model

Quality problems are durable work items, not temporary warning banners.

Quality debt categories:

- Missing required evidence
- Stale evidence
- Conflicting identity
- Weak attribution
- Unverified contact
- Partial coverage
- Failed source inspection
- Schema incompatibility
- Mapping uncertainty
- Policy ambiguity
- Synchronization drift
- Unresolved destination feedback

Every quality item includes severity, owner, status, evidence, remediation path, due policy, and closure reason.

A quality item may close as:

```text
RESOLVED
ACCEPTED_LIMITATION
SUPERSEDED
FALSE_POSITIVE
POLICY_EXCEPTION
```

It may not disappear because the dashboard was refreshed.

## 17. Security and trust boundaries

The model requires:

- Tenant-scoped storage, APIs, jobs, caches, files, events, and logs
- Write-only encrypted credentials
- Separate credentials by source, destination, tenant, environment, and capability
- Short-lived service tokens where supported
- Least-privilege database and API access
- SSRF protections
- Parameterized and adapter-owned queries
- Table, collection, field, and operation allowlists
- Payload and response limits
- Signature, timestamp, audience, and replay validation
- Prompt-injection isolation for researched content
- Secret and authorization-header redaction
- Sensitive-field classification and minimization
- Retention, deletion, legal-hold, and suppression enforcement
- Emergency connector and application disablement

Authentication proves an identity. It does not grant unlimited business authority.

## 18. Reliability and recovery model

Every external boundary is assumed to fail.

Required controls:

- Durable checkpoints
- Idempotency keys
- Exact event identity on retry
- Exponential backoff with jitter
- Circuit breakers
- Backpressure
- Dead-letter handling
- Per-entity ordering where needed
- Lease and heartbeat recovery
- Same-ID/different-payload conflict detection
- Dry-run repair
- Reconciliation
- Live-work priority over backfill
- Snapshot-based replay
- Operator-visible failure classification

Local Harvester transactions commit independently from optional outbound delivery.

## 19. API and event boundary

Harvester APIs and events must expose product concepts rather than database rows.

Commands may include:

```text
CreateHarvestJob
ValidateHarvestJob
StartHarvestJob
PauseHarvestJob
ResumeHarvestJob
CancelHarvestJob
SubmitObservation
ReviewResolution
RunQualification
RunOpportunityAssessment
ReserveLead
ReleaseLead
CreateSelectionSnapshot
ApprovePublication
RetryDelivery
ReconcileDestination
ApplyFeedback
```

Events may include:

```text
HarvestJobCreated
HarvestJobStarted
SourceRunStarted
ObservationRecorded
EvidenceAssertionCreated
ResolutionReviewRequired
EntityResolved
LeadProfileUpdated
QualificationCompleted
OpportunityAssessed
QualityIssueRaised
SelectionFrozen
PublicationApproved
DeliverySucceeded
DeliveryFailed
FeedbackReceived
ModelVersionActivated
```

Events are versioned, tenant-scoped, authenticated where external, idempotent, and replay-safe.

## 20. Operator experience

The interface should organize work around decisions and exceptions.

Primary operator journeys:

```text
Define Market
→ Generate Leads
→ Monitor Harvest
→ Review Exceptions
→ Inspect Generated Leads
→ Manage Master Leads
→ Review Dossier
→ Select and Reserve
→ Export or Publish
→ Learn from Outcomes
```

The product should surface:

- What the system knows
- Why it believes it
- What remains unknown
- What failed
- What requires review
- What changed
- What action is permitted
- What action happens next

Operators should not need to reconstruct workflow state by opening five pages and comparing timestamps like amateur forensic accountants.

## 21. Metrics that matter

The operating model should report at least:

### Intelligence quality

- Identity review rate
- False-merge and false-split rate
- Qualification override rate
- Opportunity-ranking quality
- Contact invalidation rate
- Evidence freshness
- Evidence coverage
- Unresolved conflict rate

### Operational efficiency

- Time to first accepted lead
- Time to verified dossier
- Operator minutes per accepted lead
- Source cost per accepted lead
- Job completion rate
- Retry and recovery rate
- Backlog age
- Dead-letter age

### Governance

- Suppression escape attempts blocked
- Cross-tenant access tests
- Secret exposure tests
- Publication approval rate
- Unapproved publication attempts blocked
- Model and policy version coverage
- Reproducibility rate

### Product value

- Accepted leads produced
- Qualified-lead yield
- Verified-contact yield
- Useful opportunity hypotheses
- Outcome-feedback coverage
- Customer exportability and ownership

## 22. Module crosswalk

This model strengthens the existing modules as follows.

| Operating concern | Primary roadmap modules |
| --- | --- |
| Market definition, configuration, permissions, audit | 03–08, 17 |
| Credentials, connectors, schemas, mappings, synchronization | 09–16, 23–24 |
| Orchestration, workers, budgets, stopping rules | 18–20 |
| Source intake and source policy | 21–28, 42 |
| Raw evidence, assertions, coverage, provenance | 29–31, 41 |
| Resolution candidates and decisions | 32–34, 47 |
| Lead profiles, signals, verification, dossiers | 35–38, 43, 46 |
| Qualification and opportunity decisions | 39–40, 47–48 |
| Historical snapshots and current workspaces | 44–46, 49 |
| Selection, export, publication, payload freezing | 48–56 |
| Operations, economics, administration, learning | 57–64 |

No new top-level module count is created.

## 23. Strengthening sequence

The model should be implemented in controlled slices.

### Gate 1 — Contracts and invariants

- Formal domain contracts
- Decision records
- Evidence assertion kinds
- Coverage states
- Confidence dimensions
- Version references
- Tenant invariants

### Gate 2 — Evidence graph

- Raw observation immutability
- Artifact references
- Assertion provenance
- Conflict representation
- Current and historical projection

### Gate 3 — Decision separation

- Resolution contract
- Qualification contract
- Opportunity contract
- Review authority
- Reversible decisions

### Gate 4 — Market and orchestration intelligence

- Versioned market definitions
- Source plans
- Cost and yield tracking
- Stopping rules
- Adaptive but bounded orchestration

### Gate 5 — Operator control

- Exception-first queues
- Evidence explanations
- Quality debt
- Frozen snapshots
- Approval workflows

### Gate 6 — Feedback and governed learning

- OutcomeFeedback
- Evaluation datasets
- Model registry
- Offline evaluation
- Staged rollout and rollback

### Gate 7 — Activation and productization

- Publication contracts
- Destination reconciliation
- Multi-tenant operations
- Packaging, backup, restore, upgrades, and release governance

## 24. Required architectural tests

The strengthened model is not satisfied until tests prove:

1. A completed HarvestJob can be reproduced from pinned definitions, policies, schemas, mappings, connectors, and model versions.
2. Raw observations and evidence artifacts remain immutable after later corrections.
3. Every material assertion can be traced to source evidence.
4. `NOT_DETECTED`, `NOT_INSPECTED`, `INSPECTION_FAILED`, and `ABSENT_CONFIRMED` remain distinct.
5. Resolution, qualification, opportunity scoring, selection, and publication cannot silently trigger one another.
6. A mistaken resolution decision can be reconstructed and reversed without losing evidence.
7. Confidence dimensions remain available even when a composite ranking is calculated.
8. A model or policy change does not reinterpret historical job snapshots.
9. Feedback creates new evidence and cannot directly self-modify production behavior.
10. Budget adaptation cannot weaken source, compliance, tenant, evidence, or approval rules.
11. A failed source or destination cannot roll back committed local work.
12. Suppression applies to export, API, group, publication, retry, and backfill paths.
13. Optional Core and Communicator integrations can be disabled independently.
14. Customer-owned data remains exportable under policy regardless of product plan.
15. Exact-head runtime, migration, security, accessibility, failure-recovery, and CI checks pass before release.

## 25. Locked rule

> Harvester converts a governed market definition into evidence-backed opportunity intelligence. It preserves source truth, explains every material decision, keeps automation within authority, and leaves the customer in control of the data, infrastructure, and next action.
