# Harvester Keyword Profile Runtime Delivery Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Audience: **Harvester backend, frontend, data, QA, security and release engineers**

## 1. Purpose

This is the developer-facing plan for implementing Harvester's complete keyword-profile capability.

It preserves the existing keyword plans and registries. It does not replace, delete, collapse, summarize away or regenerate their substantive content.

The authority order is:

1. This runtime delivery plan governs implementation sequence, affected layers, verification and release.
2. `keyword-profile-implementation-plan.md` governs the normative keyword runtime model.
3. `keyword-profile-development-plan.md` governs the additive profile-development model.
4. `keyword-plan-application-map.md` governs how the plan applies to the existing registries.
5. `keyword-plan-preservation-rule.md` and `keyword-plan-change-control.md` govern preservation and later change.
6. The keyword registries remain the controlled source datasets.
7. The architecture and delivery addenda govern evidence integration and roadmap placement.

When documents overlap, engineers must preserve the stricter rule. A conflict must be recorded and resolved through change control before coding continues.

## 2. Intended business outcome

Harvester must let a provider define a market and activate only the keyword, source and evidence logic relevant to services that provider actually offers.

```text
Provider
→ active provider offering
→ broad sector
→ one or more product or service domains
→ separate activities selected inside each domain
→ versioned keyword and control profiles
→ source-appropriate query plans
→ evidence observations
→ entity, domain and activity assessment
→ offering-specific opportunity assessment
→ lawful contact readiness
→ qualified lead
```

The system must reduce operational complexity for the operator:

- reviewed defaults instead of blank keyword forms
- guided configuration instead of giant flat lists
- previews before activation
- explicit versioning and rollback
- evidence-backed decisions instead of raw match counts
- one controlled path from market definition to lead generation

## 3. Non-negotiable invariants

1. Keywords discover evidence. They do not independently prove a domain, activity, service gap, opportunity, lead, authority or consent.
2. Every domain retains an independent keyword profile.
3. Every activity has one canonical identity, but applicability and user selection remain domain-specific.
4. Selecting an activity for one domain never activates it for another domain.
5. Service-specific problem, intent, competitor, existing-solution, replacement, integration and gap profiles require an active provider offering.
6. Canonical profiles cannot be mutated by tenant overrides.
7. Production profiles never mutate silently from model output, feedback or newly collected evidence.
8. Completed Harvest Jobs retain immutable taxonomy, profile, query, source, classifier and policy versions.
9. Positive evidence is evaluated with exclusions, negative context, contradiction, freshness, duplicate origin and source suitability.
10. “Not found” is not “absent” without adequate source coverage.
11. Existing-solution evidence can mean no opportunity, replacement, migration, integration, optimization, support or expansion.
12. Public contact information does not override consent, suppression, jurisdiction, conflict, channel or platform policy.
13. Sensitive sectors and services use stricter source, retention, review, permission and inference controls.
14. Every write is tenant-scoped, authorized, validated, audited and concurrency-safe.
15. No task is Complete until the latest exact commit passes the applicable verification sequence.

## 4. Scope

This plan includes:

- complete keyword depth
- keyword validation
- canonical registry ingestion
- PostgreSQL runtime schema and Alembic migrations
- FastAPI contracts and endpoints
- workflow and lifecycle state handling
- provider-offering integration
- market-definition and Harvest Job snapshots
- query preview and composition
- keyword-match evidence capture
- feedback, quality and benchmark governance
- React configuration interfaces
- responsive, accessible and mobile correction
- security, tenant isolation, observability and audit
- migration, rollout, rollback and exact-head verification

This plan does not authorize:

- uncontrolled web scraping
- bypassing source terms, access controls or platform policies
- automatic outreach from a keyword match
- sensitive personal inference without lawful evidence and required review
- copying Harvester's private provider strategy into NEWAX Core or Communicator
- replacing the authoritative 64-module roadmap with another top-level roadmap

# Part I — Complete keyword depth

## 5. Profile layers

The runtime must preserve these independently versioned layers.

### 5.1 Domain identity profiles

Purpose: identify the product, service, institution, material or operational domain.

Required term classes:

- canonical name
- reviewed exact aliases
- phrase aliases
- abbreviations
- former or historical names where relevant
- organization-type cues
- domain-specific positive context
- domain-specific exclusions
- ambiguous-term controls
- jurisdiction terms
- locale-pack references

### 5.2 Activity profiles

Purpose: identify what the organization appears to do with, for or around the selected domain.

Examples include manufacturing, processing, distributing, warehousing, selling, promoting, installing, maintaining, repairing, advising, treating, teaching, financing, recycling and disposal.

Each activity profile must support:

- canonical verb and noun forms
- approved industry phrases
- actor phrases
- process phrases
- output phrases
- facility cues
- equipment cues
- activity-specific exclusions
- ambiguity controls
- source suitability

Activity participation is resolved through the approved domain–activity mapping, never through global propagation.

### 5.3 Organization-cue profiles

Purpose: distinguish an operating organization from a product listing, article, person, job candidate, consumer review, course, policy discussion or unrelated mention.

Cue groups include:

- company and enterprise
- institution and facility
- operator and network
- professional practice
- public authority
- nonprofit body
- software provider
- manufacturer, distributor, retailer and service provider

### 5.4 Exclusion and negative-context profiles

Required exclusion families include:

- individual consumer context
- individual résumé or job-seeker context
- academic article or research-only context
- news mention without operating-organization evidence
- product listing without organization evidence
- closed, dissolved or inactive organization
- cancelled, expired or awarded opportunity
- duplicate directory or mirrored content
- unsupported geography or jurisdiction
- suppressed entity or route
- unrelated lexical meaning
- stale or unverifiable affiliation
- unsafe or prohibited sensitive inference

Exclusions may block, downgrade or route to review. They must not be applied as an unexplained global blocklist.

### 5.5 Offering-specific signal profiles

These exist only for active provider offerings.

Required signal families:

- direct inquiry
- active buying intent
- procurement, tender, RFP or quotation
- new organization, branch, facility, product or project
- hiring and team expansion
- replacement, migration or modernization
- integration need
- operational pain or process weakness
- reporting, compliance or audit requirement
- recurring maintenance or service due
- technology footprint
- budget, funding, grant or investment event
- contract, renewal or expiry event
- sector-specific operational trigger
- contactability and responsible-function evidence
- negative and disqualifying signals

### 5.6 Existing-solution and competitor profiles

These must remain separate from domain identity and activity profiles.

They record:

- current platform, vendor or system
- implementation state
- recency
- replacement indicators
- integration indicators
- dissatisfaction or limitation indicators
- support or maintenance indicators
- renewal or contract timing
- evidence source and confidence

### 5.7 Decision-maker role profiles

Role cues identify likely responsibility, not guaranteed authority.

Required dimensions:

- function
- seniority
- current affiliation
- organization scope
- responsibility context
- evidence date
- source suitability
- conflict or stale-role indicators

### 5.8 Contact-route profiles

Required route types:

- official contact page
- official business email
- main telephone number
- procurement portal
- authorized directory record
- public professional profile
- direct inquiry
- referral or partner route

Every route stores purpose, source, collection date, verification state, suppression state, allowed channels and policy outcome.

### 5.9 Source-suitability profiles

Source suitability is signal-specific, not one universal reputation score.

The runtime must distinguish official websites, registries, procurement sources, job boards, directories, maps, news, reviews, professional profiles, technology listings, structured feeds, customer-owned data, direct inquiries and partner-authorized sources.

### 5.10 Locale packs

Canonical English identities remain stable. Urdu, Roman Urdu, abbreviations, transliterations, regional spellings and jurisdiction terms are maintained as reviewed locale packs.

Each locale term must reference its canonical term, language, locale, reviewer, version, examples and activation state.

### 5.11 Query-composition profiles

Required query families:

- precision
- recall
- entity
- direct intent
- procurement
- event
- technology
- role
- contact route
- negative and contradiction
- source-specific
- locale-specific

Every generated query must preserve the contributing profile versions and never use uncontrolled Cartesian expansion.

# Part II — Complete validation plan

## 6. Validation layers

Validation runs at import, edit, review, activation, preview, execution and release.

### 6.1 Structural validation

Validate:

- required fields
- code format
- enum values
- supported match modes
- valid language and locale
- valid weights and requirement levels
- valid source classes
- valid state and transition
- valid dates and version ancestry
- tenant ownership

### 6.2 Referential validation

Validate that:

- every domain code exists
- every activity code exists
- every domain–activity assignment exists
- every offering reference exists and is active when required
- every term belongs to a valid profile version
- every locale term has a canonical parent
- every source rule references a supported adapter or source class
- every benchmark references a valid profile version
- no orphaned references remain after deprecation

### 6.3 Lexical validation

Reject or review:

- malformed stems such as truncated words
- whitespace-only or punctuation-only terms
- duplicate aliases after normalization
- aliases identical to exclusions
- overbroad one-word aliases without controls
- unsupported regex
- catastrophic or excessively expensive regex
- invisible characters
- control characters
- unsafe query syntax
- accidental partial-word substitutions
- locale terms with no canonical relationship

### 6.4 Semantic validation

Review:

- whether the term actually belongs to the domain or activity
- whether a physical system was mislabeled as software
- whether a service provider was mislabeled as a product manufacturer
- whether a role term was confused with a purchasing authority
- whether an event term is being treated as permanent identity
- whether a broad term needs sector, organization, activity or source corroboration
- whether sensitive meaning is being inferred from weak evidence

### 6.5 Profile-composition validation

The composed target profile must contain:

- selected sector
- selected domain
- approved activities for that domain
- active provider offering for service-specific signals
- domain identity profile
- selected activity profiles
- organization cues
- exclusions
- approved source classes
- geography
- language and locale
- evidence thresholds
- freshness rules
- contradiction policy

Block activation when required layers are absent or contradictory.

### 6.6 Query validation

Validate:

- non-empty query
- supported source syntax
- bounded term expansion
- positive and negative query availability
- source rate and length limits
- deduplicated aliases
- no secret or credential material
- no prohibited personal or sensitive terms
- no unsupported jurisdiction
- estimated breadth and cost
- query-family provenance

### 6.7 Benchmark validation

Every activatable profile must have reviewed cases covering:

- known positive
- known negative
- ambiguous
- stale
- duplicate-origin
- contradictory
- multilingual or locale-specific where applicable
- source mismatch
- sensitive-sector edge case where applicable
- domain/activity non-propagation
- inactive-offering isolation

### 6.8 Data-quality validation

Measure:

- malformed-term rate
- duplicate-term rate
- overbroad-term rate
- unresolved-reference rate
- false-positive rate
- false-negative rate from reviewed samples
- source-mismatch rate
- contradiction-miss rate
- duplicate-origin inflation
- stale-profile rate
- locale-error rate
- reviewer agreement

### 6.9 Activation gate

A profile version can become ACTIVE only when:

- structural, referential and lexical validation pass
- required benchmarks pass
- required reviewer approval exists
- sensitive-sector approval exists where applicable
- query preview succeeds
- no unresolved blocking conflict remains
- version diff and rollback target are available
- activation is authorized and audited

### 6.10 Release validation

Before runtime release:

- all 1,586 domain profiles import successfully
- all 519 activity profiles import successfully
- counts match source registries
- stable codes and meanings remain unchanged
- migrations pass from empty and current production-equivalent databases
- downgrade or forward-fix strategy is tested
- API contracts pass
- frontend paths pass
- permission and tenant-isolation tests pass
- benchmark regression passes
- CI and security checks pass against the exact head

# Part III — Runtime schema plan

## 7. Schema principles

- PostgreSQL remains the source of truth.
- SQLAlchemy models and Alembic migrations follow existing repository patterns.
- Canonical records and tenant-owned configuration remain separate.
- History is append-only where decisions must remain reproducible.
- Mutable drafts use optimistic concurrency.
- Activated versions are immutable.
- Harvester stores references to source evidence rather than flattening every decision into one score.

## 8. Canonical catalog tables

### `keyword_definitions`

Minimum fields:

```text
id UUID PK
code TEXT UNIQUE NOT NULL
canonical_text TEXT NOT NULL
keyword_type ENUM NOT NULL
language_code TEXT NOT NULL
locale_code TEXT NULL
ambiguity_class ENUM NOT NULL
sensitive_classification ENUM NOT NULL
status ENUM NOT NULL
created_at
updated_at
```

### `keyword_definition_aliases`

```text
id
keyword_definition_id FK
alias_text
normalized_text
language_code
locale_code
match_mode
status
source_reference
reviewed_by
reviewed_at
UNIQUE(keyword_definition_id, normalized_text, language_code, locale_code, match_mode)
```

### `keyword_profile_templates`

Platform-managed profile identities for domain, activity, organization, exclusion, source, locale, role, contact and signal profiles.

### `keyword_profile_template_versions`

Immutable canonical template versions with source-document references, checksum, approval and activation metadata.

### `keyword_profile_template_terms`

Term participation, match mode, polarity, requirement level, default weight, source scope, geography scope, language scope and evidence controls.

### Canonical references

```text
domain_keyword_profile_references
activity_keyword_profile_references
control_profile_references
source_suitability_profile_references
locale_pack_references
```

## 9. Tenant and provider configuration tables

### `keyword_profiles`

```text
id
workspace_id
provider_id
profile_type
name
status
active_version_id
created_by
created_at
updated_at
```

### `keyword_profile_versions`

```text
id
keyword_profile_id
version_number
parent_version_id
base_template_version_id
state
change_reason
validation_summary
reviewed_by
reviewed_at
activated_by
activated_at
superseded_at
lock_version
created_by
created_at
```

### `keyword_profile_terms`

```text
id
keyword_profile_version_id
keyword_definition_id
custom_text NULL
term_type
match_mode
polarity
requirement_level
weight
source_scope JSONB
geography_scope JSONB
language_scope JSONB
freshness_policy_id NULL
status
notes
```

### `provider_offering_keyword_profiles`

Links active provider offerings to problem, intent, competitor, existing-solution, replacement, integration, gap and sector-overlay profiles.

### `market_definition_keyword_configs`

Links a versioned market definition to selected domain, activity and offering profile versions.

## 10. Validation and benchmark tables

```text
keyword_profile_validation_runs
keyword_profile_validation_findings
keyword_profile_benchmarks
keyword_profile_benchmark_cases
keyword_profile_benchmark_runs
keyword_profile_benchmark_results
keyword_profile_change_proposals
keyword_profile_feedback
```

Every run stores input version, validator version, timestamps, outcome, metrics and findings.

## 11. Query and execution tables

```text
query_composition_profiles
query_templates
query_template_versions
query_previews
query_preview_results
query_plans
query_plan_versions
query_executions
```

A `query_plan_version` freezes sector, domain, activity, offering, profile versions, source class, geography, language, locale, positive query, negative query, limits and policy versions.

## 12. Evidence tables

```text
keyword_match_evidence
keyword_context_assessments
keyword_evidence_links
keyword_duplicate_origins
keyword_contradictions
keyword_source_suitability_assessments
```

Evidence must preserve:

- Harvest Job
- source record
- source class
- query execution
- keyword definition and profile version
- matched text and context span
- match mode
- polarity
- event date
- collection date
- language and locale
- extractor or classifier version
- confidence dimensions
- duplicate-origin key

## 13. Snapshot and audit tables

```text
harvest_job_keyword_snapshots
keyword_profile_state_transitions
keyword_profile_audit_events
keyword_profile_import_runs
keyword_profile_import_errors
```

Snapshot records are immutable after the Harvest Job begins.

## 14. Enums

At minimum:

```text
KeywordProfileType
KeywordType
MatchMode
Polarity
RequirementLevel
ProfileState
ValidationSeverity
ValidationOutcome
BenchmarkCaseType
BenchmarkOutcome
QueryFamily
QueryPlanState
QueryExecutionState
FeedbackType
FeedbackState
ImportState
SensitiveClassification
AmbiguityClass
```

## 15. Constraints and indexes

Required controls include:

- uniqueness for stable codes
- uniqueness for one version number per profile
- one active version per profile
- tenant composite indexes
- provider and offering composite indexes
- profile-state and review-queue indexes
- term normalized-text indexes
- source, event-date and collection-date indexes
- Harvest Job and query-execution indexes
- evidence duplicate-origin indexes
- GIN indexes only where measured query patterns justify them
- database checks for valid state-dependent fields
- foreign keys preserving canonical identities

No denormalized search index becomes the source of truth.

# Part IV — API plan

## 16. API standards

- FastAPI and Pydantic follow existing repository patterns.
- OpenAPI remains authoritative for generated frontend types.
- Every list endpoint supports bounded pagination, filtering and sorting.
- Every write validates tenant, permission, state transition and optimistic-lock version.
- Create operations accept idempotency keys where retries can duplicate work.
- Errors use stable machine codes and safe human messages.
- Sensitive query or evidence details require elevated permission.

## 17. Catalog APIs

```text
GET /api/broad-sectors
GET /api/domains
GET /api/domains/{domain_id}
GET /api/domains/{domain_id}/activities
GET /api/activities
GET /api/activities/{activity_id}
GET /api/keyword-definitions
GET /api/keyword-profile-templates
GET /api/keyword-profile-templates/{id}
GET /api/locale-packs
GET /api/source-suitability-profiles
```

## 18. Provider-offering APIs

```text
GET  /api/providers/{provider_id}/offerings
GET  /api/provider-offerings/{offering_id}/keyword-profiles
PUT  /api/provider-offerings/{offering_id}/keyword-profiles
POST /api/provider-offerings/{offering_id}/validate-keyword-profiles
```

Inactive offerings cannot activate service-specific profiles.

## 19. Tenant profile APIs

```text
GET    /api/keyword-profiles
POST   /api/keyword-profiles
GET    /api/keyword-profiles/{id}
PATCH  /api/keyword-profiles/{id}
POST   /api/keyword-profiles/{id}/versions
GET    /api/keyword-profiles/{id}/versions
GET    /api/keyword-profile-versions/{version_id}
PATCH  /api/keyword-profile-versions/{version_id}
POST   /api/keyword-profile-versions/{version_id}/validate
POST   /api/keyword-profile-versions/{version_id}/submit-review
POST   /api/keyword-profile-versions/{version_id}/approve
POST   /api/keyword-profile-versions/{version_id}/activate
POST   /api/keyword-profile-versions/{version_id}/pause
POST   /api/keyword-profile-versions/{version_id}/supersede
POST   /api/keyword-profile-versions/{version_id}/rollback
POST   /api/keyword-profile-versions/{version_id}/clone
GET    /api/keyword-profile-versions/{version_id}/diff
```

## 20. Term APIs

```text
GET    /api/keyword-profile-versions/{version_id}/terms
POST   /api/keyword-profile-versions/{version_id}/terms
PATCH  /api/keyword-profile-versions/{version_id}/terms/{term_id}
DELETE /api/keyword-profile-versions/{version_id}/terms/{term_id}
POST   /api/keyword-profile-versions/{version_id}/terms/bulk
POST   /api/keyword-profile-versions/{version_id}/terms/import
GET    /api/keyword-profile-versions/{version_id}/terms/export
```

Activated versions reject term mutation.

## 21. Market-definition APIs

```text
GET  /api/market-definitions/{id}/keyword-config
PUT  /api/market-definitions/{id}/keyword-config
POST /api/market-definitions/{id}/validate-keywords
POST /api/market-definitions/{id}/freeze-keyword-snapshot
GET  /api/market-definitions/{id}/keyword-summary
```

## 22. Query preview APIs

```text
POST /api/query-previews
GET  /api/query-previews/{id}
POST /api/query-previews/{id}/sample
POST /api/query-previews/{id}/validate
POST /api/query-previews/{id}/approve
POST /api/query-previews/{id}/cancel
GET  /api/query-previews/{id}/results
GET  /api/query-previews/{id}/provenance
```

## 23. Benchmark and quality APIs

```text
GET  /api/keyword-benchmarks
POST /api/keyword-benchmarks
POST /api/keyword-benchmarks/{id}/runs
GET  /api/keyword-benchmark-runs/{id}
GET  /api/keyword-quality/metrics
GET  /api/keyword-quality/review-queue
POST /api/keyword-profile-feedback
GET  /api/keyword-profile-feedback
POST /api/keyword-profile-feedback/{id}/triage
POST /api/keyword-profile-feedback/{id}/resolve
```

## 24. Evidence APIs

```text
GET /api/keyword-match-evidence
GET /api/keyword-match-evidence/{id}
GET /api/keyword-match-evidence/{id}/context
GET /api/keyword-match-evidence/{id}/provenance
GET /api/keyword-match-evidence/{id}/contradictions
POST /api/keyword-match-evidence/{id}/review
```

## 25. Import and administration APIs

```text
POST /api/admin/keyword-registry-imports
GET  /api/admin/keyword-registry-imports
GET  /api/admin/keyword-registry-imports/{id}
POST /api/admin/keyword-registry-imports/{id}/validate
POST /api/admin/keyword-registry-imports/{id}/apply
POST /api/admin/keyword-registry-imports/{id}/rollback
GET  /api/admin/keyword-audit
```

## 26. Permissions

At minimum:

```text
keywords.catalog.view
keywords.profile.view
keywords.profile.create
keywords.profile.edit
keywords.profile.review
keywords.profile.approve
keywords.profile.activate
keywords.profile.rollback
keywords.benchmark.manage
keywords.query.preview
keywords.evidence.view
keywords.evidence.review
keywords.feedback.submit
keywords.feedback.resolve
keywords.import.manage
keywords.audit.view
```

# Part V — Workflow and state handling

## 27. Profile lifecycle

```text
DRAFT
→ VALIDATING
→ VALIDATION_FAILED | REVIEW_REQUIRED
→ IN_REVIEW
→ CHANGES_REQUESTED | APPROVED
→ ACTIVE
→ PAUSED
→ SUPERSEDED
→ DEPRECATED
→ ARCHIVED
```

Rules:

- only DRAFT or CHANGES_REQUESTED versions are editable
- VALIDATING is system-controlled
- APPROVED requires reviewer permission and passing gates
- ACTIVE requires activation permission
- only one ACTIVE version exists per profile
- activation supersedes the prior active version atomically
- PAUSED remains immutable but does not participate in new jobs
- rollback creates or reactivates an approved compatible version through an audited transition
- historical Harvest Jobs continue referencing their frozen versions

## 28. Validation lifecycle

```text
QUEUED
→ RUNNING
→ PASSED | FAILED | BLOCKED | CANCELLED
```

A failed or blocked validation cannot be represented as low confidence.

## 29. Query-preview lifecycle

```text
DRAFT
→ COMPOSING
→ READY
→ SAMPLING
→ REVIEW_REQUIRED
→ APPROVED | REJECTED | EXPIRED | CANCELLED
```

A preview is invalidated when any contributing profile, source, geography, language, offering or policy version changes.

## 30. Import lifecycle

```text
UPLOADED
→ PARSING
→ STRUCTURAL_VALIDATION
→ REFERENTIAL_VALIDATION
→ SEMANTIC_REVIEW
→ READY_TO_APPLY
→ APPLYING
→ APPLIED
→ VERIFIED
```

Failure states:

```text
PARSE_FAILED
VALIDATION_FAILED
APPLY_FAILED
ROLLBACK_REQUIRED
ROLLED_BACK
BLOCKED
```

Import application must be transactional or safely resumable with an explicit checkpoint.

## 31. Feedback lifecycle

```text
SUBMITTED
→ TRIAGED
→ ACCEPTED | REJECTED | DUPLICATE
→ CHANGE_PROPOSED
→ BENCHMARKED
→ APPROVED
→ RELEASED
→ VERIFIED
```

Feedback never edits active production records directly.

## 32. Harvest Job interaction

Before a Harvest Job starts:

1. Validate the market definition.
2. Resolve all active profile versions.
3. Freeze the complete keyword and query snapshot.
4. Confirm source and policy authorization.
5. Record the snapshot checksum.
6. Start execution.

After execution begins, profile edits affect future jobs only.

## 33. Concurrency and retries

- Draft writes use `lock_version` or ETag/If-Match.
- State transitions run in transactions.
- Activation uses a row or advisory lock per profile.
- Idempotency keys protect retryable create or transition requests.
- Background jobs record attempt number, next retry and terminal reason.
- Duplicate queue delivery must not duplicate profile versions, evidence or audit events.
- User-visible retry controls appear only for retry-safe operations.

## 34. Failure handling

Stable failure codes include:

```text
PROFILE_NOT_FOUND
PROFILE_VERSION_INACTIVE
PROFILE_VERSION_IMMUTABLE
OPTIMISTIC_LOCK_CONFLICT
INVALID_STATE_TRANSITION
VALIDATION_REQUIRED
VALIDATION_FAILED
BENCHMARK_REQUIRED
BENCHMARK_FAILED
REVIEW_REQUIRED
OFFERING_INACTIVE
INVALID_PROFILE_REFERENCE
UNSUPPORTED_MATCH_MODE
LOCALE_PACK_NOT_APPROVED
QUERY_EMPTY
QUERY_TOO_BROAD
QUERY_CONTRADICTORY
NEGATIVE_QUERY_MISSING
SOURCE_POLICY_BLOCKED
SOURCE_RATE_LIMITED
SOURCE_AUTHORIZATION_FAILED
MATCH_CONTEXT_UNAVAILABLE
ENTITY_UNRESOLVED
DOMAIN_UNRESOLVED
ACTIVITY_UNRESOLVED
SIGNAL_UNSUPPORTED
EVIDENCE_STALE
EVIDENCE_CONTRADICTORY
CONTACT_POLICY_BLOCKED
```

The UI must show what failed, what remains unproven and the safe next action.

# Part VI — Complete frontend configuration UI

## 35. Frontend foundation

Use the repository's current stack:

- React 19
- TypeScript
- React Router
- TanStack Query
- `openapi-fetch`
- Tailwind CSS
- Lucide icons

Before feature work:

1. Regenerate OpenAPI types from the latest backend contract.
2. Remove stale or duplicated handwritten API types.
3. Add route-level error boundaries.
4. Define query-key factories and mutation invalidation rules.
5. Define shared loading, empty, error, conflict and permission-denied states.
6. Add form and table primitives only where existing capabilities are insufficient.
7. Preserve existing optimistic-locking conventions.

## 36. Navigation and routes

Add a grouped **Market Intelligence Configuration** workspace with routes such as:

```text
/market-definitions
/market-definitions/:id
/keyword-catalog
/keyword-profiles
/keyword-profiles/:id
/keyword-profiles/:id/versions/:versionId
/provider-offerings
/query-previews
/query-previews/:id
/keyword-quality
/keyword-feedback
/keyword-evidence
/locale-packs
/keyword-imports
/keyword-audit
```

Do not place every route as an equal sidebar item. Use grouped navigation and task-oriented entry points.

## 37. A-to-Z operator journey

### Step A — Select provider and active offering

- provider selector
- active offering selector
- offering status and applicability summary
- clear warning when the offering is inactive

### Step B — Select broad sectors

- searchable multi-select
- sector descriptions
- selected-count summary

### Step C — Select domains per sector

- hierarchical sector panels
- search and filters
- domain descriptions and codes
- no 1,586-item flat dropdown

### Step D — Select activities separately inside every domain

- independent activity panel per selected domain
- CORE, COMMON, OPTIONAL and SPECIALIZED indicators
- no cross-domain propagation
- bulk recommendations may be previewed but require explicit confirmation

### Step E — Review domain identity profiles

- recommended terms
- aliases
- organization cues
- exclusions
- language and source scope
- examples and evidence controls

### Step F — Review activity profiles

- activity terms shown inside the selected domain context
- source and evidence guidance
- independent enable or disable state

### Step G — Review offering-specific signals

- problem
- intent
- procurement
- expansion
- replacement
- integration
- existing solution
- competitor
- compliance
- maintenance
- budget and funding

### Step H — Configure sources, geography and locale

- approved source classes
- source limitations
- country, province, city and radius controls where applicable
- language and locale packs
- sensitive-sector warnings

### Step I — Configure evidence thresholds

- required source diversity
- freshness
- contradiction handling
- duplicate-origin handling
- minimum entity, domain, activity and signal confidence
- human-review requirements

### Step J — Preview queries

- query families by source
- included and excluded terms
- provenance for every term
- breadth and cost warnings
- positive and negative queries

### Step K — Sample and benchmark

- known-positive, known-negative and ambiguous examples
- result snippets
- match mode
- source suitability
- context and contradiction indicators
- accept, reject or flag controls

### Step L — Review configuration diff

- canonical defaults versus tenant overrides
- previous version versus proposed version
- affected market definitions and future jobs
- rollback target

### Step M — Submit review

- validation summary
- unresolved findings
- reviewer selection where policy allows
- reason and change notes

### Step N — Approve and activate

- explicit confirmation
- permission check
- transactional activation
- prior-version supersession
- audit reference

### Step O — Final market-definition summary

- provider
- active offering
- sectors
- domains
- domain-specific activities
- profile versions
- sources
- locale
- evidence rules
- query summary
- readiness state

### Step P — Generate leads

Lead generation is enabled only when the complete definition passes readiness validation.

## 38. Profile editor

Required capabilities:

- profile metadata
- status and version history
- term search and filtering
- add canonical term
- add custom tenant term
- bulk edit
- match mode
- polarity
- requirement level
- weight
- source scope
- geography scope
- language scope
- freshness policy
- examples
- validation findings
- benchmark results
- diff
- comments and review history
- activate, pause, supersede and rollback controls

## 39. Catalog explorer

- sectors, domains and activities
- stable codes and descriptions
- relationship view
- profile references
- canonical versus tenant-owned distinction
- usage count
- deprecated state
- read-only canonical records unless platform-admin permission exists

## 40. Provider-offering mapping UI

- offering list and status
- applicable sectors, domains and activities
- attached signal profiles
- missing required profile warnings
- inactive-offering isolation
- dependency impact before pausing an offering

## 41. Query-preview workspace

- source tabs
- precision, recall, entity, negative and specialized families
- generated query
- contributing terms and profiles
- sample execution status
- result review
- breadth, cost and rate-limit estimates
- approve, reject, expire and recreate actions

## 42. Quality and feedback workspace

- false positives
- false negatives
- malformed terms
- source mismatches
- contradiction misses
- stale profiles
- benchmark regressions
- reviewer disagreement
- change proposal status
- before and after metrics

## 43. Evidence explorer

- source record
- matched term
- match mode
- context span
- source class and suitability
- event and collection dates
- duplicate-origin group
- positive and negative context
- linked domain, activity and signal assessments
- review outcome
- reverse trace to query and profile versions

## 44. UI state requirements

Every screen defines:

- initial loading
- background refresh
- empty state
- filtered empty state
- validation failure
- authorization failure
- network failure
- server failure
- optimistic-lock conflict
- stale data
- partial success
- background job running
- terminal job failure
- retry-safe action
- unsaved changes
- successful save or transition

## 45. Accessibility requirements

- keyboard operation for all controls
- visible focus
- semantic headings and landmarks
- labels and descriptions
- accessible validation messages
- status announcements
- table headers and captions
- dialogs with focus management
- no color-only states
- reduced-motion support
- touch-target sizing
- logical mobile reading order
- automated checks plus manual keyboard and screen-reader review

# Part VII — Responsive UI correction plan

## 46. Responsive baseline

Support coherent behavior from approximately 320 CSS pixels through large desktop widths.

Test at minimum:

```text
320
360
390
430
768
1024
1280
1440
1920 CSS pixels
```

Also test landscape mobile and tablet.

## 47. Application shell

- Desktop sidebar becomes a collapsible navigation rail or drawer on smaller widths.
- Header actions must wrap or collapse without overlap.
- Main content must not use fixed widths that force viewport overflow.
- Drawers become full-screen sheets on narrow mobile.
- Sticky actions account for safe areas and virtual keyboards.

## 48. Wizard responsiveness

- Desktop may use step navigation plus content panel.
- Tablet may use compact step navigation.
- Mobile uses a single-column flow with a progress summary.
- Selected sector, domain and activity summaries remain reachable without forcing the user back through every step.
- Primary action remains visible but never covers form content.

## 49. Tables and dense data

Use the appropriate pattern per data type:

- responsive columns for moderate tables
- horizontal scroll with sticky first column for genuinely tabular data
- card or definition-list transformation for mobile review
- progressive disclosure for secondary metadata
- column chooser on desktop where helpful

Never hide critical state, version or validation information merely to avoid scrolling.

## 50. Forms and editors

- one-column mobile forms
- two-column desktop layouts only where fields are related
- long term editors use virtualized or paginated lists when measured need exists
- filters collapse into a sheet on mobile
- inline help becomes expandable text
- code and query blocks wrap or scroll safely
- dialogs never exceed viewport height

## 51. Responsive correction audit

For every page and shared component, record:

- smallest supported width
- overflow result
- text wrapping
- action visibility
- focus order
- touch behavior
- keyboard behavior
- loading and error behavior
- table or card transformation
- screenshot evidence
- defect status

## 52. Visual-regression coverage

Capture representative screenshots for:

- application shell
- sector/domain selection
- domain-specific activity selection
- profile editor
- query preview
- validation findings
- evidence explorer
- quality dashboard
- dialogs, drawers and mobile sheets
- empty, error and conflict states

# Part VIII — Security, privacy and observability

## 53. Security controls

- tenant isolation at query and service layers
- permission checks on every profile and evidence operation
- canonical records protected from tenant mutation
- input size limits
- regex safety controls
- query-expansion limits
- injection protection
- secret references outside profile data
- audit of state-changing actions
- restricted sensitive-sector evidence
- export redaction
- suppression and deletion enforcement
- rate limiting for preview and sample execution
- secure background-job payloads

## 54. Privacy controls

- minimize personal data in query and evidence logs
- apply retention by source and sensitive class
- separate organization discovery from person and contact resolution
- do not collect contact data before a supported opportunity requires it
- record lawful purpose and permitted channel
- honor suppression and deletion throughout derived data

## 55. Observability

Required metrics:

- profile counts by state
- validation duration and failure rate
- benchmark pass rate
- query preview breadth and cost
- source yield
- match yield
- irrelevant-match rate
- duplicate-origin rate
- contradiction rate
- opportunity yield
- contact-ready yield
- reviewer agreement
- activation and rollback count
- import and migration failures

Required logs and traces:

- actor and tenant
- profile and version
- transition
- validation or benchmark run
- query-plan and execution IDs
- stable error code
- correlation ID
- no unnecessary sensitive term or personal-data payload

# Part IX — Implementation sequence

## 56. Pull-request sequence

The developer must implement in dependency order. Each PR remains small enough to review and complete enough to verify.

### KWR-01 — Baseline and ADRs

- approve final data ownership and lifecycle decisions
- add traceability matrix
- confirm migration and rollback policy
- no runtime behavior

### KWR-02 — Canonical schema and enums

- catalog tables
- template versions
- stable enums
- Alembic migration
- schema tests

### KWR-03 — Canonical registry importer

- parse controlled Markdown or generated approved import artifacts
- count and checksum verification
- dry run
- idempotent apply
- rollback

### KWR-04 — Tenant profile schema and lifecycle

- profiles, versions, terms
- optimistic locking
- state transitions
- audit

### KWR-05 — Validation and benchmark schema/services

- validators
- findings
- benchmarks
- quality metrics

### KWR-06 — Catalog read APIs

- sectors, domains, activities, templates, locale and source profiles
- pagination, filters and permissions

### KWR-07 — Profile write and lifecycle APIs

- drafts, versions, terms, validation, review, approval, activation, pause, supersede and rollback

### KWR-08 — Provider-offering integration

- active-offering rule
- service-specific profiles
- applicability validation

### KWR-09 — Market-definition keyword configuration

- domain-specific activity selection
- profile references
- readiness validation
- immutable snapshot

### KWR-10 — Query composer and preview

- query families
- provenance
- breadth and cost controls
- negative queries
- sample execution boundary

### KWR-11 — Match evidence capture

- match, context, source, time, profile, query and duplicate-origin provenance

### KWR-12 — Classification and contradiction integration

- evidence-to-assessment boundaries
- source suitability
- freshness
- contradiction and duplicate handling

### KWR-13 — Frontend contract regeneration and route foundation

- current OpenAPI types
- query keys
- route boundaries
- shared states
- navigation grouping

### KWR-14 — Catalog and offering UI

- catalog explorer
- provider-offering mappings
- permissions and responsive behavior

### KWR-15 — Market-definition wizard

- sector, domains, separate activities, offering, sources, locale and evidence rules

### KWR-16 — Profile editor and lifecycle UI

- terms, validation, benchmark, diff, review, activation and rollback

### KWR-17 — Query preview and sample UI

- source families
- provenance
- positive and negative results
- review decisions

### KWR-18 — Evidence and quality UI

- evidence explorer
- feedback queue
- quality metrics
- change proposals

### KWR-19 — Responsive and accessibility correction

- full route audit
- keyboard and screen-reader testing
- mobile and tablet correction
- visual regression

### KWR-20 — Security and performance verification

- tenant isolation
- permissions
- regex and query expansion
- rate limits
- load and response budgets

### KWR-21 — End-to-end workflow and migration rehearsal

- import
- configure
- validate
- benchmark
- review
- activate
- freeze job snapshot
- preview query
- capture evidence
- rollback

### KWR-22 — Controlled rollout

- feature flags
- internal workspace pilot
- shadow evaluation
- benchmark comparison
- staged activation
- monitoring
- rollback readiness

## 57. Per-PR verification

Every PR must perform the repository's applicable equivalent of:

```text
Inspect
Define acceptance criteria
Implement smallest complete change
Generate artifacts
Format
Lint
Type-check
Run focused tests
Run complete tests
Run migration validation when applicable
Run security checks
Build frontend when applicable
Review complete diff
Test actual workflow
Verify CI on exact head
```

Frontend PRs additionally require:

- generated OpenAPI client validation
- unit or component tests
- accessibility checks
- responsive screenshots
- production build
- relevant end-to-end tests

Schema PRs additionally require:

- upgrade from current head
- clean-database upgrade
- migration-chain verification
- data preservation checks
- downgrade or documented forward-fix test

# Part X — Test and acceptance matrix

## 58. Required test classes

- unit tests
- schema and migration tests
- repository and service integration tests
- API contract tests
- permission tests
- tenant-isolation tests
- state-transition tests
- optimistic-lock tests
- idempotency and duplicate-delivery tests
- import and checksum tests
- lexical and semantic validation tests
- regex safety tests
- benchmark regression tests
- query-composition tests
- negative-query tests
- locale tests
- sensitive-sector tests
- evidence provenance tests
- snapshot reproducibility tests
- frontend component tests
- frontend route tests
- accessibility tests
- responsive and visual-regression tests
- end-to-end workflow tests
- load and performance tests
- backup, restore and rollback tests where applicable

## 59. Mandatory business scenarios

1. Pharmaceutical manufacturing activates manufacturing terms only for Pharmaceuticals.
2. Medical Devices remains unaffected unless manufacturing is separately selected there.
3. Pharmaceutical distribution activates distribution terms and applicable offering signals.
4. An inactive Warehouse Management offering cannot influence opportunity assessment.
5. A domain match without organization evidence does not create an organization.
6. An activity match without context does not prove the activity.
7. Existing-solution evidence can route to replacement, integration, optimization or no opportunity.
8. A copied tender appears as one evidence origin.
9. A cancelled or awarded tender contradicts active buying intent.
10. A stale decision-maker role cannot create contact readiness.
11. Public contact data remains blocked when suppression or policy prevents contact.
12. Urdu or Roman Urdu aliases participate only when the approved locale pack is active.
13. A profile edit after job start does not change the running or completed job snapshot.
14. A failed validation cannot be activated.
15. Two concurrent activations produce one valid active version.
16. Mobile users can complete the full configuration journey without hidden or overlapping actions.

## 60. Definition of Done

The complete capability may be called Complete only when:

- all approved requirements are implemented
- all 1,586 domain and 519 activity profiles are imported and traceable
- runtime schema and migrations are verified
- APIs and generated frontend contracts agree
- profile, market-definition and Harvest Job state handling is verified
- every principal frontend workspace is usable on desktop, tablet and mobile
- accessibility gates pass
- tenant isolation and permissions pass
- benchmark and query quality gates pass
- exact-head CI and applicable security checks pass
- the actual end-to-end workflow passes
- rollback is proven
- no known release-blocking issue remains

## 61. Status boundary

Until runtime code, migrations, APIs, frontend interfaces and verification exist, this work remains **Proposed** documentation.

The existing plans and registries are preserved as controlled source material. This document tells developers how to implement them without losing their substance, creating duplicate runtime models or skipping affected layers.
