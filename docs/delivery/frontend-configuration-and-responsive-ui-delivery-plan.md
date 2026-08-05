# Harvester Frontend Configuration and Responsive UI Delivery Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not started**  
Audience: **Harvester frontend, backend, product, design, QA, security and release engineers**

## 1. Purpose

This document defines the complete delivery plan for:

1. Harvester's end-to-end frontend configuration workspace.
2. Full frontend coverage of the existing backend operational domains.
3. Correction of responsive behavior across the complete application.
4. Accessibility, contract, testing, security, performance and release verification required before the frontend can be called complete.

This plan extends, but does not replace:

- `docs/ROADMAP.md`
- `docs/architecture/harvester-intelligence-operating-model.md`
- `docs/SERVICES.md`
- `docs/architecture/provider-portfolio-and-lead-generation-profile-model.md`
- `docs/delivery/keyword-profile-runtime-delivery-plan.md`
- `docs/taxonomy/README.md`
- `docs/sources/user-input-storage-model.md`

When requirements overlap, preserve the stricter rule. A conflict must be documented and resolved before implementation continues.

## 2. Intended business outcome

Harvester must let an authorized operator configure, validate, activate and monitor a provider-specific lead-generation market without using command-line tools, direct database access, undocumented API calls or giant flat dropdowns.

The complete operator path is:

```text
Provider organization
→ business unit
→ active provider offering
→ reusable lead-generation profile
→ broad sectors
→ one or more domains inside each sector
→ separate activities inside every selected domain
→ domain, activity and organization keyword profiles
→ offering-specific problem and opportunity signals
→ sources, geography, language and locale
→ evidence, freshness and contradiction rules
→ query preview and sample review
→ validation and benchmark
→ review and approval
→ activation and scheduling
→ immutable Harvest Job snapshot
→ evidence-backed lead intelligence
→ quality feedback and controlled improvement
```

The interface must reduce operational complexity through guided configuration, reviewed defaults, task-oriented navigation, clear readiness states, reversible versioning and evidence-backed explanations.

## 3. Non-negotiable product rules

1. Broad sectors are multi-select.
2. Domains are selected separately inside each sector.
3. Activities are selected independently inside each domain.
4. Selecting an activity for one domain never activates it for another domain.
5. Service-specific problem, intent, competitor, existing-solution, replacement, integration and gap profiles require an active provider offering.
6. Keywords discover evidence. They do not independently prove a domain, activity, service gap, opportunity, authority, consent or qualified lead.
7. Canonical taxonomy records are read-only for ordinary tenant users.
8. Tenant overrides never mutate canonical records.
9. Activated profile versions are immutable.
10. Draft writes use optimistic concurrency.
11. Every state-changing action is permission-checked, tenant-scoped and audited.
12. Completed Harvest Jobs retain the exact configuration, taxonomy, keyword, source, classifier and policy versions used when they ran.
13. Public contact information does not override suppression, consent, jurisdiction, route or channel policy.
14. Responsive correction must preserve critical information rather than hiding it to make layouts fit.
15. No screen may be called complete without loading, empty, error, permission, stale, conflict, partial-success and success behavior where applicable.
16. No task is Complete until the exact latest commit passes all applicable checks and the real workflow is verified.

# Part I — Live baseline and gap analysis

## 4. Current frontend baseline

The current frontend uses:

- React 19
- TypeScript
- React Router
- TanStack Query
- `openapi-fetch`
- Tailwind CSS
- Lucide icons
- Vite

The current visible routes cover:

- Command Center
- Institution Explorer
- Institution Dossier
- Resolution Queue and Detail
- Readiness Gate and Draft Detail
- Manual Lead drawer

The current backend also exposes operational APIs for:

- sectors
- entities, person candidates and signals
- lead profiles and score history
- daily selection and reservation actions
- verification flags and sweeps
- compliance suppressions and deletion requests
- event outbox processing and requeue
- exports
- source runs, source health, stranded records, page snapshots, audit, safe configuration, metrics and health

These backend-backed domains require complete human-facing UI coverage.

## 5. Current frontend risks to correct before expansion

### 5.1 Contract drift

- OpenAPI-generated types must be regenerated from the latest backend contract.
- Handwritten `any` types must be removed from API-facing code.
- Manual `fetch()` calls must be replaced with generated client coverage when the endpoint exists in OpenAPI.
- CI must fail when the committed generated contract is stale.

### 5.2 No frontend test harness

The current frontend has lint, formatting and build checks but no component, route, accessibility, end-to-end or visual-regression test command.

Before feature expansion, add a verified test foundation using compatible versions of:

- Vitest or the repository-approved equivalent
- React Testing Library
- user-event
- automated accessibility checks
- Playwright or the repository-approved browser-test equivalent

Dependency selection remains subject to peer, runtime, licence, maintenance and security verification.

### 5.3 Desktop-only shell assumptions

Current patterns requiring correction include:

- fixed-width desktop sidebar
- `h-screen` layouts that do not account for mobile browser chrome
- desktop-only four-column dashboard grids
- fixed two-column and three-column detail layouts
- twelve-column review workspace with no mobile transformation
- inline filter bars that cannot wrap safely
- tables with no mobile strategy
- action groups that can overflow
- tabs with no overflow or compact behavior
- drawer grids that are too dense for narrow screens
- direct use of browser `alert()` instead of accessible application feedback

### 5.4 Repeated page-local UI logic

The frontend needs shared primitives for:

- page headers
- toolbars
- filters
- status badges
- cards
- tables and mobile record views
- pagination
- forms
- comboboxes and multi-selects
- steppers
- drawers and sheets
- dialogs
- confirmation flows
- loading, empty and error states
- optimistic-lock conflicts
- permission gates
- unsaved-change protection
- job progress
- audit metadata

# Part II — Information architecture and navigation

## 6. Navigation model

Do not place every route as an equal sidebar item. Use grouped navigation with desktop expansion, tablet rail behavior and mobile sheet navigation.

### 6.1 Overview

- Command Center
- Assigned Work
- Recent Activity

### 6.2 Market Configuration

- Providers and Business Units
- Provider Offerings
- Lead-Generation Profiles
- Market Definitions
- Taxonomy Catalog
- Keyword Profiles
- Query Previews

### 6.3 Lead Intelligence

- Institutions
- Lead Profiles
- People Candidates
- Signals
- Daily Selection

### 6.4 Review and Quality

- Resolution Queue
- Verification Flags
- Readiness Gate
- Keyword Evidence
- Keyword Quality
- Feedback and Change Proposals

### 6.5 Operations

- Source Runs
- Source Health
- Stranded Records
- Page Snapshots
- Event Outbox
- Exports

### 6.6 Governance and Administration

- Compliance
- Locale Packs
- Registry Imports
- Audit Log
- Runtime Health and Safe Configuration

## 7. Route plan

### 7.1 Existing routes to preserve and improve

```text
/
/institutions
/institutions/:institutionId
/resolution
/resolution/:reviewId
/readiness
/readiness/:draftId
```

### 7.2 Operational parity routes

```text
/lead-profiles
/lead-profiles/:institutionId
/entities/people
/entities/signals
/daily-selection
/verification
/compliance/suppressions
/compliance/deletion-requests
/outbox
/exports
/operations
/operations/source-runs
/operations/source-runs/:runId
/operations/source-health
/operations/stranded-records
/operations/page-snapshots
/operations/audit
/operations/health
/sectors
```

### 7.3 Complete configuration routes

```text
/providers
/providers/:providerId
/providers/:providerId/business-units
/provider-offerings
/provider-offerings/:offeringId
/lead-generation-profiles
/lead-generation-profiles/:profileId
/market-definitions
/market-definitions/new
/market-definitions/:marketDefinitionId
/market-definitions/:marketDefinitionId/configure
/taxonomy
/taxonomy/sectors
/taxonomy/domains/:domainId
/taxonomy/activities/:activityId
/keyword-catalog
/keyword-profiles
/keyword-profiles/:profileId
/keyword-profiles/:profileId/versions/:versionId
/query-previews
/query-previews/:previewId
/keyword-evidence
/keyword-evidence/:evidenceId
/keyword-quality
/keyword-feedback
/locale-packs
/keyword-imports
/keyword-imports/:importId
/keyword-audit
```

Every route must define:

- page title and breadcrumb
- permission requirement
- query and mutation ownership
- URL-filter contract
- responsive pattern
- loading, empty, error and conflict states
- test coverage
- analytics or audit needs where applicable

# Part III — A-to-Z configuration journey

## 8. Complete operator journey

The configuration experience is a guided workflow with saved drafts. It must allow safe exit and resumption without forcing the operator to restart.

### A — Select workspace and provider

- current workspace
- provider organization
- tenant and permission context
- provider status
- incomplete-provider warning

### B — Select business unit

- optional or required according to provider structure
- unit description, ownership and active status
- inherited versus unit-specific settings

### C — Select active provider offering

- only active offerings are eligible
- offering type, delivery model and customer type
- applicable sectors, domains and activities
- capacity, geography and channel constraints
- inactive-offering warning with no silent bypass

### D — Create or select a lead-generation profile

- new profile or existing reusable profile
- profile purpose
- owner
- priority
- activation state
- schedule and capacity summary

### E — Define profile identity and scope

- profile name
- internal description
- business outcome
- geographic scope
- languages
- target organization size
- exclusions
- budget and capacity constraints where supported

### F — Select broad sectors

- searchable multi-select
- sector descriptions and stable codes
- selected count
- recommended sectors shown as recommendations, never silent selections

### G — Select domains inside each sector

- sector-grouped domain browser
- family filters
- search
- stable codes and descriptions
- canonical versus reused relationship
- no flat 1,586-item dropdown

### H — Select activities independently inside every domain

- separate activity panel for every selected domain
- `CORE`, `COMMON`, `OPTIONAL`, `SPECIALIZED` and `NOT_APPLICABLE` guidance
- explicit selection per domain
- recommendation preview with confirmation
- no cross-domain propagation

### I — Review domain identity profiles

- canonical terms
- aliases
- abbreviations
- organization cues
- exclusions
- ambiguous-term controls
- source and language scope
- examples

### J — Review selected activity profiles

- activity terms inside the selected domain context
- actor, process, output, facility and equipment cues
- exclusions
- source suitability
- independent enable or disable state

### K — Attach offering-specific signal profiles

- direct inquiry
- buying intent
- procurement
- expansion
- hiring
- replacement
- migration
- integration
- existing solution
- competitor
- compliance
- maintenance
- funding and budget
- sector-specific triggers

### L — Configure approved sources

- source classes
- source authorization state
- source-specific limitations
- expected evidence types
- retention and attribution warnings
- cost and rate-limit guidance

### M — Configure geography

- countries
- provinces or regions
- cities
- service radius where appropriate
- inclusion and exclusion areas
- no unsupported jurisdiction activation

### N — Configure language and locale packs

- canonical English identity
- Urdu
- Roman Urdu
- transliteration and spelling variants
- locale approval state
- source-specific language support

### O — Configure organization and evidence controls

- minimum organization evidence
- entity confidence
- domain confidence
- activity confidence
- signal confidence
- source diversity
- freshness
- duplicate-origin handling
- contradiction policy
- human-review requirements

### P — Configure contact and output policy

- responsible-function evidence
- contact-route types
- suppression policy
- allowed channels
- consent and jurisdiction rules
- export and publishing limits
- no automatic outreach from keyword matches

### Q — Review composed keyword configuration

- domain profiles
- selected activity profiles
- organization cues
- exclusions
- offering-specific signal profiles
- source, locale and policy overlays
- missing required layer warnings

### R — Preview generated queries

- source tabs
- precision, recall, entity, procurement, event, technology, role, contact and negative families
- contributing profile and term provenance
- positive and negative queries
- breadth, estimated cost and rate-limit warnings
- unsafe or unsupported query blocking

### S — Run sample results

- bounded sample execution
- source status
- result snippets
- matched terms
- context
- source suitability
- duplicate and contradiction cues
- no sample execution when source authorization is absent

### T — Review benchmark cases

- known positive
- known negative
- ambiguous
- stale
- duplicate-origin
- contradictory
- locale-specific
- source mismatch
- sensitive-sector edge case

### U — Resolve validation findings

- blocking, warning and informational findings
- safe next action
- linked field or profile
- reviewer comments
- rerun validation
- no conversion of a blocked state into an unexplained low-confidence score

### V — Review version diff

- canonical defaults versus tenant overrides
- prior version versus proposed version
- added, removed and changed terms
- affected market definitions
- future-job impact
- rollback target

### W — Submit for review

- change reason
- validation summary
- benchmark summary
- unresolved non-blocking findings
- reviewer assignment where allowed
- immutable submission snapshot

### X — Approve and activate

- permission check
- explicit confirmation
- transactional activation
- prior-version supersession
- activation schedule
- audit reference
- rollback readiness

### Y — Review final readiness summary

- provider and business unit
- offering
- profile
- sectors
- domains
- independent activities
- keyword and policy versions
- sources
- geography
- locale
- evidence thresholds
- query readiness
- capacity and schedule
- contact and output policy

### Z — Start, monitor and improve

- freeze immutable Harvest Job snapshot
- start or schedule job
- monitor source and query execution
- review evidence and quality metrics
- submit feedback
- create controlled change proposal
- benchmark, approve and release later profile versions

# Part IV — Configuration workspace specifications

## 9. Provider and business-unit workspace

Required functions:

- provider list and search
- provider status
- business units
- ownership and permissions
- active offerings count
- active profiles count
- operational activation summary
- incomplete setup warnings
- read-only identity fields where owned elsewhere

## 10. Provider-offering workspace

Required functions:

- offering list, filters and lifecycle status
- offering details
- applicable customer and lead-subject types
- sector, domain and activity applicability
- attached signal profiles
- missing-profile warnings
- inactive-offering isolation
- capacity and geography constraints
- dependency impact before pause, archive or supersession

## 11. Lead-generation profile workspace

Required functions:

- reusable profile list
- draft, active, paused, scheduled, suspended and archived states
- provider and business-unit ownership
- offering references
- version history
- market-definition references
- overlap and duplicate-target controls
- capacity, budget and schedule
- last run and next run
- performance and quality summary
- clone, compare, pause, resume and archive actions

## 12. Market-definition wizard

Required functions:

- autosaved draft
- A-to-Z step navigation
- completion state per step
- blocking and warning counts
- direct return to incomplete steps
- desktop summary panel
- mobile summary sheet
- save and exit
- unsaved-change protection
- validation before review
- immutable readiness snapshot

## 13. Taxonomy catalog explorer

Required functions:

- sector, domain and activity browsing
- stable codes
- descriptions
- family and relationship view
- cross-sector reuse
- domain-to-activity applicability
- keyword-profile references
- canonical versus tenant-owned distinction
- deprecated and superseded state
- usage count
- read-only canonical records unless platform-admin permission exists

## 14. Keyword-profile library

Required functions:

- filters by profile type, owner, state, sector, domain, activity, offering, locale and source
- version status
- active version
- validation status
- benchmark status
- usage count
- stale profile warning
- compare and clone
- create tenant override from approved canonical template

## 15. Keyword-profile editor

Required functions:

- metadata
- version ancestry
- term search and filtering
- term type
- match mode
- polarity
- requirement level
- weight
- source scope
- geography scope
- language scope
- freshness policy
- examples
- exclusions and ambiguous-term controls
- bulk actions
- import and export where permitted
- lexical and semantic findings
- benchmark results
- diff
- review comments
- activate, pause, supersede and rollback actions

Activated versions are read-only.

## 16. Query-preview workspace

Required functions:

- source tabs
- query families
- generated query
- positive and negative terms
- contributing profiles and versions
- source syntax validation
- breadth, rate and cost estimate
- sample status and results
- accept, reject, cancel, expire and recreate actions
- stale-preview invalidation when any contributing version changes

## 17. Evidence explorer

Required functions:

- source record
- matched term
- match mode
- context span
- source class and suitability
- event and collection date
- duplicate-origin group
- positive and negative context
- contradiction
- linked entity, domain, activity and signal assessments
- review outcome
- reverse trace to query execution and profile versions

## 18. Quality and feedback workspace

Required functions:

- false positives
- false negatives
- malformed terms
- overbroad terms
- source mismatches
- contradiction misses
- stale profiles
- benchmark regressions
- reviewer disagreement
- duplicate-origin inflation
- locale errors
- feedback triage
- change proposal state
- before-and-after metrics

## 19. Locale-pack workspace

Required functions:

- canonical parent term
- language and locale
- transliteration
- examples
- reviewer
- version
- approval and activation state
- profile and source usage
- duplicate and conflict warnings

## 20. Registry-import workspace

Required functions:

- upload or controlled source selection
- checksum
- source-document version
- dry run
- parse result
- structural, referential, lexical and semantic findings
- count reconciliation
- apply confirmation
- progress
- terminal failure
- rollback or forward-fix guidance
- audit reference

## 21. Audit workspace

Required functions:

- actor
- tenant and provider
- entity type and ID
- action
- state transition
- previous and new version
- timestamp
- correlation ID
- filter and export controls subject to permission
- redaction of sensitive payloads

# Part V — Complete operational frontend coverage

## 22. Command Center

Correct and expand:

- responsive metric cards
- pipeline and quality summaries
- assigned review work
- source health
- active-profile and market-definition readiness
- recent failures and blocked jobs
- no `any`-based dashboard mapping

## 23. Institution Explorer

Correct and expand:

- server-side filters and pagination
- name, city, sector, operating status, confidence and qualification filters
- URL-preserved filter state
- responsive table/card pattern
- no client-only filtering over one fixed 50-record page

## 24. Institution Dossier

Correct and expand:

- responsive header and action placement
- overview, branches, contacts, findings and evidence tabs
- lead profile and score history
- person candidates and signals
- verification flags
- opportunity and readiness context
- accessible overflow behavior for tabs

## 25. Manual Lead

Correct and expand:

- generated API contract
- full-screen mobile sheet
- responsive field grouping
- per-field validation
- accessible error summary
- unsaved-change confirmation
- keyboard and screen-reader behavior
- no hard-coded API URL
- no browser-only alert behavior

## 26. Lead Profiles

Add:

- ranked list
- score and qualification filters
- sector filter
- pagination
- detail route
- score dimensions
- score history visualization with text alternative
- evidence and freshness context

## 27. Person Candidates and Signals

Add:

- institution filter
- signal type filter
- candidate affiliation and evidence
- source and recency
- links back to institution dossier
- no authority claim from role cues alone

## 28. Daily Selection

Add:

- batch creation form
- limit, TTL, minimum score, label and sector
- current reservations
- reservation status
- expiry countdown
- consume and release actions
- confirmation and retry-safe handling
- batch result summary

## 29. Resolution Queue and Detail

Correct and expand:

- responsive list/card behavior
- evidence comparison that stacks on mobile
- visible version and score
- feedback requirement rules
- merge, separate and branch decisions
- optimistic-lock conflict recovery
- accessible confirmation for irreversible outcomes

## 30. Verification

Add:

- flag list and filters
- sweep form
- created-count result
- resolve and dismiss actions
- notes
- contact-unreachable action where context exists
- stale and freshness indicators

## 31. Readiness Gate and Draft Detail

Correct and expand:

- responsive list/card behavior
- mobile editor layout
- target context, editable draft and readiness checks
- sticky but non-obstructive actions
- explicit save state
- rejection feedback requirement where policy requires
- optimistic-lock conflict recovery
- accessible status announcements

## 32. Compliance

Add:

### Suppressions

- list
- search and filters
- create suppression
- reason, channel, actor and note
- remove confirmation
- normalization preview

### Deletion requests

- list and status filter
- create request
- subject type and ID
- fulfill irreversible confirmation
- reject with reason
- audit and completion result

## 33. Event Outbox

Add:

- status filters
- event metadata
- attempt count
- next attempt
- error summary
- process pending action
- dead-letter requeue
- idempotency and duplicate-delivery explanation

## 34. Exports

Add:

- CSV or JSON
- operating status
- minimum score
- qualification status
- sector
- limit
- estimated row count when supported
- export policy warning
- safe download handling
- empty-result and failure states

## 35. Operations

Add:

- source runs list and detail
- source health
- stranded records
- page snapshots
- audit log
- safe runtime configuration
- metrics
- health status
- filtering, pagination and responsive data patterns
- no exposure of secrets or unsafe raw payloads

## 36. Sector administration

Add only for authorized users:

- list and detail
- create and edit
- code, display name, institution types, ICP criteria and qualification rules
- canonical-registry relationship warning
- version and audit behavior when later introduced

# Part VI — Shared frontend architecture

## 37. Application shell

Create shared components:

```text
AppShell
DesktopSidebar
TabletNavigationRail
MobileTopBar
MobileNavigationSheet
PageContainer
PageHeader
Breadcrumbs
RouteErrorBoundary
PermissionBoundary
```

Rules:

- use `min-h-dvh` or equivalent rather than assuming fixed `h-screen`
- one intentional scroll container per screen
- preserve browser back and forward behavior
- active route indication must be programmatic, not color-only
- mobile navigation traps focus while open and returns focus when closed

## 38. Shared async states

Create:

```text
PageLoadingState
SectionLoadingState
BackgroundRefreshIndicator
EmptyState
FilteredEmptyState
ErrorState
PermissionDeniedState
StaleDataBanner
PartialSuccessState
JobRunningState
TerminalJobFailureState
RetryAction
```

Each state must provide:

- what happened
- what remains unavailable or unproven
- safe next action
- correlation or audit reference where useful

## 39. Shared data-display components

Create:

```text
MetricCard
StatusBadge
DefinitionList
DataTable
ResponsiveRecordList
Pagination
ColumnChooser
FilterBar
FilterSheet
SearchField
DateTimeDisplay
ConfidenceDisplay
VersionBadge
AuditMetadata
EvidenceSummary
```

Do not build one universal component so abstract that every screen becomes harder to understand.

## 40. Shared form components

Create only the necessary primitives:

```text
FormField
Input
Textarea
Select
Combobox
MultiSelect
TreeSelector
CheckboxGroup
RadioGroup
Switch
NumberInput
DateTimeInput
TagEditor
TermEditor
ScopeEditor
ValidationSummary
FieldError
```

Requirements:

- visible labels
- help and error association
- keyboard operation
- touch target sizing
- no placeholder-only labels
- no silent coercion of invalid values

## 41. Workflow components

Create:

```text
WizardShell
StepNavigation
ProgressSummary
ReadinessSummary
UnsavedChangesGuard
ConflictDialog
ConfirmationDialog
ResponsiveDrawer
MobileSheet
JobProgress
DiffViewer
BenchmarkCaseReview
QueryProvenancePanel
```

## 42. State and data-management rules

- OpenAPI is authoritative for request and response types.
- Query-key factories exist per resource family.
- Mutations define exact invalidation or cache update behavior.
- Filters, sort and pagination live in the URL when users may share or revisit the view.
- Draft wizard state persists server-side.
- Local state is limited to temporary interaction state.
- Background jobs use bounded polling, server events or the approved repository pattern.
- Optimistic updates are used only when rollback behavior is safe and tested.
- Write operations support optimistic concurrency.
- Retry controls appear only for retry-safe operations.
- Permission-denied responses never masquerade as empty data.

# Part VII — Complete responsive correction

## 43. Responsive support matrix

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

Also test:

- mobile landscape
- tablet portrait and landscape
- browser zoom
- text enlargement
- virtual keyboard open
- safe-area insets
- reduced motion
- high-content and long-label cases

## 44. Responsive layout ranges

These are implementation guides, not device assumptions.

### Narrow: 320–430

- one-column content
- mobile top bar
- full-screen or near-full-screen sheets
- compact progress summary
- stacked actions
- card or definition-list data presentation where appropriate

### Compact: 431–767

- one-column primary content
- optional two-column related fields
- mobile navigation sheet
- horizontally scrollable tabs only when all items remain accessible

### Tablet: 768–1023

- navigation rail or compact drawer
- one or two content columns
- compact step navigation
- selected secondary panels may become tabs or drawers

### Desktop: 1024–1279

- full navigation
- two-column and constrained three-column layouts where justified
- side summaries only when content remains readable

### Wide: 1280 and above

- controlled maximum widths
- no uncontrolled stretching
- dense workspaces may use resizable side panels where tested

## 45. Application-shell correction

- replace fixed `w-64` behavior with responsive sidebar, rail and sheet modes
- replace `h-screen` assumptions with dynamic viewport-safe layout
- allow header content to wrap or collapse
- prevent header actions from overlapping status messages
- move non-critical identity text into an account menu on narrow widths
- keep the primary page action reachable without covering content
- preserve visible route and page context on mobile

## 46. Page-header correction

Every page header must support:

- title wrapping
- description wrapping
- breadcrumb wrapping
- status badges moving below the title
- primary and secondary actions stacking
- long organization names
- localization expansion

## 47. Dashboard correction

- `grid-cols-4` becomes responsive 1, 2 and 4-column behavior
- metric cards retain readable labels and values
- charts provide text alternatives
- status and failure cards appear before decorative analytics on narrow screens

## 48. Filter correction

- desktop inline filter bars
- compact wrapping where safe
- mobile filter sheet for dense filters
- visible active-filter count
- clear-all action
- URL state preserved
- submit behavior explicit where queries are expensive

## 49. Table and record correction

Choose per dataset:

1. Responsive columns for moderate tables.
2. Horizontal scroll with sticky first column for genuinely tabular comparison.
3. Card or definition-list transformation for mobile operational review.
4. Progressive disclosure for secondary metadata.
5. Column chooser for wide desktop tables.

Rules:

- critical state, version, score, validation and action information must remain available
- table captions and headers remain semantic
- horizontal scrolling never causes whole-page viewport overflow
- row actions remain keyboard accessible
- bulk selection remains understandable on mobile

## 50. Detail-workspace correction

### Institution Dossier

- header stacks
- title and confidence badge separate safely
- metadata wraps
- tabs scroll or become a selector
- three-column overview becomes one column, then two columns, then three where justified

### Resolution Detail

- two records stack on mobile
- comparison labels remain visible
- decision actions stack
- feedback stays before decisions in reading order

### Draft Review

- three-panel layout becomes tabbed or sequential on narrow screens
- editable draft receives sufficient height
- readiness checks remain reachable
- sticky actions account for virtual keyboard and safe areas

## 51. Wizard correction

- desktop: step navigation, main form and summary panel
- tablet: compact step navigation and collapsible summary
- mobile: one-column current step with progress and summary sheet
- selected sector, domain and activity summaries remain reachable
- no step requires horizontal viewport scrolling
- primary actions never cover fields
- save and exit remains available

## 52. Editor correction

- one-column mobile form
- related two-column fields only when width allows
- term tables transform into compact records or safe horizontal scroll
- advanced filters move into a sheet
- inline help becomes expandable
- query and code blocks wrap or scroll internally
- validation findings link to the affected term or field

## 53. Drawer, sheet and dialog correction

- manual lead and configuration drawers become full-screen sheets on narrow mobile
- dialogs never exceed viewport height
- long dialogs use internal scrolling with fixed accessible header and action region
- destructive confirmations show the exact target
- focus is trapped and restored correctly
- Escape and backdrop behavior follow action risk

## 54. Sticky-action correction

- account for `env(safe-area-inset-bottom)` where supported
- avoid covering the last form field
- account for virtual keyboard
- collapse secondary actions into an overflow menu when necessary
- disabled actions explain the blocking requirement

## 55. Typography and spacing correction

- responsive type scale
- readable line length
- no fixed heading sizes that dominate narrow screens
- spacing tokens rather than page-local arbitrary values
- long codes, URLs and organization names wrap safely
- no reliance on tiny text to fit more controls

## 56. Responsive audit record

For every route and shared component, record:

- tested widths
- viewport overflow result
- internal overflow result
- text wrapping
- action visibility
- filter behavior
- table or card behavior
- focus order
- touch behavior
- keyboard behavior
- loading, empty, error and conflict states
- screenshots
- defects and resolution status

# Part VIII — Accessibility

## 57. Accessibility target

Target WCAG 2.2 Level AA for principal operator journeys.

Required controls:

- semantic landmarks and heading hierarchy
- keyboard access for every function
- visible focus
- logical focus order
- screen-reader labels and descriptions
- accessible field and form errors
- status announcements
- table captions and headers
- no color-only state
- sufficient contrast
- reduced-motion support
- touch target sizing
- zoom and reflow
- text equivalent for charts, diagrams and visual confidence indicators
- accessible dialog and sheet focus management

## 58. Manual accessibility verification

Automated tools are required but insufficient. Manually verify:

- keyboard-only completion of the A-to-Z configuration journey
- screen-reader navigation and form completion
- mobile screen-reader behavior
- conflict and validation announcements
- loading and background-refresh announcements
- table and card transformations
- dialog and sheet focus return

# Part IX — Security, privacy and permissions

## 59. Frontend security requirements

- no secrets in frontend bundles
- environment-specific API base URL
- authorization header handled centrally
- permission-aware navigation and controls
- backend remains authoritative for authorization
- no canonical tenant mutation controls without permission
- input length and file-size limits surfaced before submission
- regex and query warnings surfaced from backend validation
- no raw sensitive evidence in ordinary list views
- export controls respect permission and policy
- destructive actions require explicit confirmation
- no unsafe HTML rendering of evidence or source content

## 60. Privacy requirements

- do not expose personal contact details until the workflow and permissions permit them
- redact sensitive values in logs and errors
- separate organization discovery from person and contact resolution
- suppression and deletion state must be visible where relevant
- no analytics collection of raw free-text configuration or evidence

# Part X — Testing and verification

## 61. Required frontend test classes

- utility and formatter unit tests
- component tests
- form validation tests
- route tests
- query and mutation tests
- optimistic-lock conflict tests
- permission tests
- URL-filter tests
- accessibility tests
- responsive tests
- visual-regression tests
- end-to-end tests
- contract-generation tests
- production-build tests

## 62. Mandatory end-to-end scenarios

1. An operator creates a provider-specific profile and saves a draft.
2. The operator selects several sectors.
3. The operator selects multiple domains within one sector.
4. The operator selects Manufacturing for Pharmaceuticals.
5. Manufacturing remains unselected for Medical Devices.
6. An inactive offering cannot attach or activate offering-specific signal profiles.
7. The operator configures sources, geography and locale.
8. A missing required negative query blocks readiness.
9. A malformed or overbroad term links to a visible validation finding.
10. The operator previews queries and reviews provenance.
11. A profile change invalidates an older query preview.
12. Known positive, negative and ambiguous benchmark cases can be reviewed.
13. A failed validation cannot be submitted as approved.
14. Two reviewers editing the same draft receive a safe conflict state.
15. Activation supersedes the prior version atomically.
16. A running Harvest Job keeps its frozen configuration after a later profile edit.
17. A mobile user completes the full configuration journey at 320 CSS pixels.
18. A keyboard-only user completes the full journey.
19. Suppressed contact policy remains visible and prevents unsafe progression.
20. A destructive deletion-fulfillment action requires explicit confirmation and reports the final result.
21. A dead-letter outbox item can be requeued safely.
22. An export with no matching rows returns a clear empty result rather than a broken download.
23. Every operational route exposes loading, empty, error and permission behavior.

## 63. Responsive visual-regression matrix

Capture representative states for:

- application shell
- mobile navigation
- dashboard
- institution explorer and dossier
- manual lead sheet
- lead-profile list and detail
- daily selection
- resolution queue and comparison
- verification
- readiness queue and editor
- compliance
- outbox
- exports
- operations
- provider and offering workspaces
- market-definition wizard
- sector and domain selection
- independent activity selection
- keyword profile editor
- query preview
- validation findings
- evidence explorer
- quality dashboard
- imports and audit
- dialogs, conflict states and destructive confirmations

At minimum capture 320, 390, 768, 1024, 1440 and one mobile-landscape state. Use additional widths for components with known breakpoint risk.

## 64. Performance requirements

- route-level code splitting where it produces measured value
- bounded list sizes and server pagination
- no unbounded rendering of 1,586 domains or 519 activities
- virtualization only when measured need justifies it
- debounced search where appropriate
- bounded background polling
- no repeated full-catalog refetch after every small mutation
- large query, evidence and diff panels load progressively
- no layout instability from loading content
- production bundle analysis before release

## 65. CI requirements

Frontend CI must include:

```text
npm ci
format check
oxlint
OpenAPI generation or drift check
type-check
component and route tests
accessibility tests
production build
browser end-to-end tests
responsive or visual-regression checks
npm audit or approved dependency audit
```

Checks must run against the exact latest commit.

# Part XI — Implementation sequence

## 66. Pull-request sequence

Each PR must remain reviewable and must not combine unrelated feature work with broad formatting or dependency upgrades.

### FUI-01 — Baseline audit and traceability

- live route and component inventory
- backend endpoint-to-screen matrix
- responsive defect register
- acceptance matrix
- no runtime behavior

### FUI-02 — OpenAPI contract regeneration

- current OpenAPI artifact
- generated types
- central API base URL
- remove direct endpoint duplication
- contract-drift CI check

### FUI-03 — Frontend test foundation

- compatible test dependencies
- component harness
- accessibility harness
- browser harness
- CI integration

### FUI-04 — Design tokens and shared states

- spacing, typography, radius, elevation and status tokens
- loading, empty, error, permission, stale and conflict states

### FUI-05 — Responsive application shell

- desktop sidebar
- tablet rail
- mobile top bar and navigation sheet
- route grouping
- dynamic viewport correction

### FUI-06 — Shared form, table and workflow primitives

- only the primitives required by approved screens
- accessibility and responsive tests

### FUI-07 — Command Center correction

- typed data
- responsive metrics
- operational and configuration readiness summaries

### FUI-08 — Institution Explorer and Dossier correction

- server pagination and filters
- responsive records
- complete dossier tabs and related intelligence

### FUI-09 — Manual Lead correction

- generated API client
- mobile sheet
- validation and unsaved-change protection

### FUI-10 — Resolution correction

- queue and detail
- responsive comparison
- conflict and decision flows

### FUI-11 — Readiness Gate correction

- queue and editor
- responsive three-panel transformation
- accessible save and decision behavior

### FUI-12 — Lead Profiles UI

- list, detail and score history

### FUI-13 — People Candidates and Signals UI

- filters, evidence and institution links

### FUI-14 — Daily Selection UI

- batch creation, reservations, consume and release

### FUI-15 — Verification UI

- flags, sweep, resolve, dismiss and unreachable-contact flow

### FUI-16 — Compliance UI

- suppressions and deletion requests

### FUI-17 — Event Outbox UI

- status, processing and dead-letter requeue

### FUI-18 — Exports UI

- filters, formats, policy and safe download behavior

### FUI-19 — Operations UI

- runs, health, stranded records, snapshots, audit, metrics and safe config

### FUI-20 — Sector and taxonomy catalog UI

- sector administration where authorized
- read-only canonical catalog explorer

### FUI-21 — Provider and business-unit UI

- provider context and business-unit ownership

### FUI-22 — Provider Offering UI

- lifecycle, applicability and signal-profile dependencies

### FUI-23 — Lead-Generation Profile UI

- reusable profiles, versions, schedules, capacity and overlap controls

### FUI-24 — Market-Definition Wizard

- complete A-to-Z guided workflow
- server draft persistence
- readiness summary

### FUI-25 — Keyword Profile Library and Editor

- terms, controls, validation, benchmark, diff and lifecycle

### FUI-26 — Query Preview UI

- source families, provenance, sample results and review

### FUI-27 — Evidence, Quality and Feedback UI

- evidence explorer, quality metrics, feedback and change proposals

### FUI-28 — Locale, Import and Audit UI

- locale packs, registry imports and audit history

### FUI-29 — Full responsive and accessibility audit

- all routes and shared components
- mobile, tablet, desktop, landscape, zoom and screen-reader verification
- visual-regression baselines

### FUI-30 — End-to-end rehearsal and controlled rollout

- complete configuration
- validation
- review
- activation
- job snapshot
- operational monitoring
- rollback
- internal pilot and feature flags

## 67. Per-PR verification

Every frontend PR must perform the applicable equivalent of:

```text
Inspect current implementation
Define testable acceptance criteria
Identify assumptions and affected routes
Implement the smallest complete change
Regenerate contracts and artifacts
Format
Lint
Type-check
Run focused tests
Run complete frontend tests
Run accessibility checks
Build
Review the complete diff
Test the actual workflow
Capture responsive evidence
Verify CI against the exact head
Confirm no unresolved release blocker remains
```

# Part XII — Release and completion gates

## 68. Feature flags and rollout

- configuration workspaces remain behind explicit feature flags until backend contracts and permissions are production-ready
- internal workspace pilot first
- no production mock data
- no hidden route exposure without navigation and permission review
- staged rollout by workspace
- telemetry for errors, abandonments and blocked states
- documented rollback

## 69. Route completion checklist

A route is Complete only when:

- requirement and owner are documented
- API contract exists and generated types agree
- permissions are enforced
- loading, empty, error, permission and stale states exist
- writes handle validation and conflicts
- responsive behavior passes
- keyboard and screen-reader behavior passes
- analytics or audit behavior is correct where required
- tests pass
- production build passes
- exact-head CI passes
- no known blocker remains

## 70. Complete capability definition

The frontend configuration and responsive UI capability may be called Complete only when:

- every existing backend operational domain has usable frontend coverage
- the complete A-to-Z configuration journey is implemented
- all principal configuration workspaces are implemented
- OpenAPI and frontend contracts agree
- canonical and tenant-owned data remain correctly separated
- domain-specific activity selection is verified
- inactive offerings cannot influence service-specific configuration
- every principal route works on desktop, tablet and mobile
- the 320-pixel end-to-end journey passes
- WCAG 2.2 AA gates pass for principal journeys
- responsive and visual-regression coverage passes
- tenant isolation and permissions pass
- optimistic-lock and state-transition behavior passes
- production build, CI and security checks pass on the exact head
- the real end-to-end workflow passes
- rollback is proven
- no known release-blocking issue remains

## 71. Status boundary

This document is a **Proposed** delivery plan.

It does not claim that configuration APIs, frontend routes, database records, permissions, tests, responsive corrections or runtime behavior have been implemented.

Implementation must follow the dependency order above and preserve the existing roadmap, operating model, services model, taxonomy, source models and keyword runtime plan.