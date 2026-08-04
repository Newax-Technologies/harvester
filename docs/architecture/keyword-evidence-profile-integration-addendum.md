# Harvester Keyword and Evidence Profile Integration Addendum

Status: **Normative planned architecture addendum**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This addendum strengthens the existing Harvester architecture by defining how domain keywords, activity keywords, provider-offering signals, source-specific query composition, evidence capture, and profile versioning enter the operating model.

It adds to, and does not replace:

- [Harvester Intelligence Operating Model](harvester-intelligence-operating-model.md)
- [Provider Portfolio and Lead-Generation Profile Model](provider-portfolio-and-lead-generation-profile-model.md)
- [Harvester Services and Opportunity Model](../SERVICES.md)
- [Keyword Profile Implementation Plan](../taxonomy/keywords/keyword-profile-implementation-plan.md)
- [Keyword Taxonomy and Lead-Signal Index](../taxonomy/keywords/README.md)

---

## 1. Architectural position

Keyword processing spans several existing Harvester planes.

```text
Control Plane
- provider offering selection
- market definition
- domain and activity selections
- profile versions
- source and locale policy

Acquisition Plane
- source-specific query composition
- request and response capture
- provider-native observations

Evidence Plane
- keyword-match evidence
- context spans
- positive and negative context
- source suitability
- event freshness
- duplicate evidence origin

Resolution Plane
- organization and person resolution
- current role and affiliation resolution

Intelligence Plane
- domain classification
- activity classification
- lead-signal assessment
- contradiction review

Decision Plane
- qualification
- opportunity assessment
- contact readiness

Operations and Learning Plane
- profile quality
- false positives and false negatives
- review queues
- profile version proposals
- rollback and benchmark evaluation
```

No plane may bypass the responsibilities of the preceding plane merely because a keyword matched.

---

## 2. Architectural invariants

1. A keyword match is an observation, not a business conclusion.
2. Domain identity, activity identity, provider-offering signals, role cues, contact routes, and exclusions remain separate profile types.
3. Every selected domain has its own approved activity group.
4. Every selected domain and activity combination has independently approved keyword participation.
5. An activity detected for one domain does not activate or prove the same activity for another domain.
6. Service-specific signals require an active provider offering.
7. Raw match counts do not become domain confidence, activity confidence, opportunity score, or contact-readiness score.
8. Every material decision remains traceable to source evidence, context, profile versions, query versions, and decision-policy versions.
9. Positive evidence is reviewed with negative, contradictory, stale, closed, cancelled, awarded, duplicate, or irrelevant context.
10. Completed Harvest Jobs are immutable with respect to the keyword, query, signal, source, classification, and scoring versions they used.
11. User feedback can propose a new profile version but cannot rewrite historical evidence or silently modify production.
12. Sensitive-sector and sensitive-service rules override ordinary discovery convenience.

---

## 3. Domain objects

The architecture adds or formalizes the following planned objects.

```text
KeywordDefinition
KeywordProfile
KeywordProfileVersion
KeywordProfileTerm
DomainKeywordProfileReference
ActivityKeywordProfileReference
OfferingKeywordProfileReference
OrganizationCueProfile
ExclusionProfile
LeadSignalProfile
DecisionMakerRoleProfile
ContactRouteProfile
SourceSuitabilityProfile
LocaleKeywordPack
QueryCompositionProfile
QueryTemplate
QueryExecution
KeywordMatchEvidence
KeywordContextAssessment
KeywordProfileFeedback
KeywordProfileBenchmark
```

These objects remain distinct from:

```text
Observation
Claim
EvidenceItem
ResolvedOrganization
ResolvedPerson
DomainAssessment
ActivityAssessment
OpportunitySignal
ServiceOpportunity
ContactEligibilityDecision
```

A `KeywordMatchEvidence` record may support those later objects. It does not replace them.

---

## 4. Evidence graph additions

The evidence graph must preserve the following edges.

```text
KeywordDefinition
→ included in KeywordProfileVersion

KeywordProfileVersion
→ referenced by MarketDefinitionVersion

MarketDefinitionVersion
→ frozen in HarvestJobSnapshot

HarvestJobSnapshot
→ produced QueryExecution

QueryExecution
→ produced SourceObservation

SourceObservation
→ contained KeywordMatchEvidence

KeywordMatchEvidence
→ assessed by KeywordContextAssessment

KeywordContextAssessment
→ may support DomainAssessment
→ may support ActivityAssessment
→ may support OpportunitySignal
→ may contradict a prior assessment

DomainAssessment + ActivityAssessment + OpportunitySignal
→ may support ServiceOpportunity

ServiceOpportunity + lawful current route + policy approval
→ may support ContactEligibilityDecision
```

Reverse explainability is mandatory.

From any qualified lead, an authorized operator must be able to trace backward to:

- The selected provider offering
- The selected sector, domain, and activity
- The keyword and signal profiles
- The query templates and executions
- The sources and source records
- The exact match evidence and context
- The entity-resolution decision
- The classification and contradiction decisions
- The qualification and contact-readiness policies

---

## 5. Confidence separation

Keyword confidence must not be collapsed into one universal percentage.

Harvester should preserve separate dimensions such as:

```text
MATCH_CONFIDENCE
CONTEXT_CONFIDENCE
SOURCE_SUITABILITY
ENTITY_CONFIDENCE
DOMAIN_CONFIDENCE
ACTIVITY_CONFIDENCE
SIGNAL_CONFIDENCE
FRESHNESS_CONFIDENCE
CONTRADICTION_RISK
CONTACT_ROUTE_CONFIDENCE
```

An exact phrase on a weak directory may have high match confidence and low source suitability.

A semantic match may have moderate match confidence but strong corroborating context.

A current procurement notice may have strong opportunity relevance but still lack a responsible contact route.

The decision layer uses the relevant dimensions. It does not average them into decorative certainty.

---

## 6. Query execution boundary

The query composer receives only approved references from the frozen market definition.

It may not:

- Invent a provider offering.
- Add a domain or activity that the user did not select.
- Add sensitive personal attributes.
- Ignore source or jurisdiction restrictions.
- Convert every alias into every possible Cartesian combination.
- Omit required negative queries.
- Reuse a stale profile after a new active version was selected.
- Mutate the market definition while a job is running.

Every `QueryExecution` records:

```text
harvest_job_id
query_template_version
source_policy_version
profile_version_ids
locale_pack_version
positive_query
negative_query
request_parameters
source_class
execution_time
cost
result_count
response_outcome
```

---

## 7. Source suitability

A source class is evaluated according to what it can credibly support.

Examples:

- Official organization pages can support current services, locations, leadership, announcements, and contact routes.
- Procurement sources can support active or historical procurement events, amendments, awards, deadlines, and requirements.
- Job postings can support hiring, skills, technology, expansion, and functional ownership signals but do not independently prove buying budget.
- Reviews can support reported operational experiences but require identity, recency, manipulation, and representativeness controls.
- Direct inquiries can strongly support expressed need and contact permission within the stated purpose.
- Directories can support discovery but often require independent verification for current identity, activity, location, or contact details.
- Technology listings can support possible technology footprint but require recency and first-party or corroborating evidence.

Source suitability is profile- and signal-specific. It is not a single global reputation score.

---

## 8. Sensitive-sector controls

Healthcare, legal, financial, employment, housing, education, public-service, and other sensitive contexts require stronger controls.

The system must support:

- Source restrictions
- Sensitive-term restrictions
- Consent and referral requirements
- Human review
- Shorter retention
- Restricted context display
- Stronger permissions
- Jurisdiction controls
- Conflict checks
- Prohibited inference rules
- Audit trails
- Suppression and deletion enforcement

Keywords must not be used to infer a private diagnosis, allegation, protected characteristic, legal wrongdoing, financial distress, employment vulnerability, or another sensitive condition without lawful, relevant, authorized evidence and required review.

---

## 9. Provider and tenant ownership

Canonical keyword definitions and reviewed default profiles may be platform-managed.

Tenant-owned configuration includes:

- Profile overrides
- Offering-specific signals
- Custom exclusions
- Custom source restrictions
- Geography and language scope
- Weight and requirement-level adjustments
- Activation state
- Review decisions
- Feedback

Tenant overrides reference canonical identities. They do not edit shared canonical records.

Provider-specific strategy remains private to the provider workspace unless an explicit bounded publication or synchronization contract permits otherwise.

---

## 10. Cross-product boundary

Harvester owns:

- Canonical keyword and signal identities used by Harvester
- Tenant keyword-profile versions
- Query composition
- Match evidence
- Classification support
- Opportunity support
- Contact-readiness decisions

NEWAX Core may receive bounded references such as:

```text
profile_code
profile_version
canonical domain code
canonical activity code
lead-signal code
assessment outcome
confidence dimensions
provenance references
```

It must not receive private provider search strategy, secret terms, hidden exclusions, proprietary weights, raw credentials, or unrestricted query templates unless an explicit contract authorizes them.

Communicator may receive only approved contact-ready packages and necessary context. It does not own Harvester keyword profiles or qualification logic.

---

## 11. Quality and learning

The operations and learning plane tracks:

- False-positive rate
- False-negative findings from reviewed samples
- Irrelevant-term rate
- Ambiguous-term rate
- Source mismatch rate
- Stale-profile rate
- Contradiction miss rate
- Duplicate-origin inflation
- Profile coverage
- Query yield
- Qualified-opportunity yield
- Contact-ready yield
- Reviewer agreement
- Sensitive-sector exceptions

A profile change requires:

```text
Observed problem
→ evidence sample
→ proposed change
→ benchmark evaluation
→ human review
→ version creation
→ controlled activation
→ monitoring
→ rollback path
```

Learning creates new governed configuration. It does not alter source history or self-modify production behavior.

---

## 12. Failure states

The architecture must represent explicit failure states including:

```text
PROFILE_NOT_FOUND
PROFILE_VERSION_INACTIVE
INVALID_PROFILE_REFERENCE
UNSUPPORTED_MATCH_MODE
UNSUPPORTED_SOURCE_PROFILE
LOCALE_PACK_NOT_APPROVED
QUERY_TOO_BROAD
QUERY_EMPTY
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

A failure is not silently converted into low confidence. The operator and job record must show what failed and what remains unproven.

---

## 13. Security requirements

- Tenant isolation applies to every profile, override, preview, feedback item, query, match, and evidence record.
- Profile changes require authorization and audit logging.
- Sensitive query and evidence details require restricted permissions.
- Secrets remain external secret references and never appear in keyword profiles or query logs.
- Query logs must avoid unnecessary personal or sensitive data.
- Public contact information remains subject to purpose, channel, suppression, consent, and retention controls.
- Exported packages must not expose internal query strategy unless explicitly approved.
- Profile and query inputs require validation against injection, malformed regex, excessive expansion, and denial-of-service risks.

---

## 14. Architectural verification scenarios

### Scenario 1 — Independent domain activities

The provider selects Pharmaceuticals and Medical Devices.

Manufacturing is selected only for Pharmaceuticals.

Expected:

- Pharmaceutical manufacturing keywords participate.
- Medical-device manufacturing keywords do not participate.
- No activity propagates between domains.

### Scenario 2 — Inactive service

A provider has a paused Warehouse Management System offering.

Expected:

- Warehouse domain and activity classification may still occur when selected for market discovery.
- The paused offering contributes no problem, intent, gap, opportunity, or contact-readiness signals.

### Scenario 3 — Broad keyword

A source contains the word “healthcare” but no organization, domain, activity, or entity context.

Expected:

- The match remains weak classification evidence.
- It does not qualify the target.

### Scenario 4 — Existing solution

A target publicly uses a competing CRM.

Expected:

- The system does not automatically reject or qualify the target.
- It evaluates replacement, integration, optimization, support, migration, expansion, or no-opportunity evidence according to the selected offering.

### Scenario 5 — Job posting

A company posts for an ERP administrator.

Expected:

- The evidence may support technology footprint, growth, internal ownership, or operational complexity.
- It does not independently prove procurement intent or budget.

### Scenario 6 — Procurement closure

A positive tender notice is followed by an award notice.

Expected:

- Negative and closure checks detect the award.
- The old active-procurement opportunity is not presented as current.

### Scenario 7 — Locale pack

A Roman Urdu term matches an approved locale pack.

Expected:

- The match preserves the locale-pack version and canonical reference.
- The English canonical profile is not mutated.

### Scenario 8 — Sensitive healthcare term

A public social post contains a medical-condition term.

Expected:

- No private diagnosis or direct patient targeting is inferred.
- Sensitive-service policy determines whether the observation may be retained or used.

### Scenario 9 — Historical reproducibility

A profile is updated after a Harvest Job completes.

Expected:

- The completed job still resolves to its original profile, query, source, and classifier versions.

### Scenario 10 — Feedback

An operator marks a term as repeatedly irrelevant.

Expected:

- Feedback enters review.
- A proposed profile version may be created.
- The active profile remains unchanged until approved.

---

## 15. Delivery boundary

This addendum defines planned architecture only.

It does not change runtime behavior, schema, migration, API, query execution, evidence processing, scoring, contact eligibility, or releases.

Implementation remains subject to the existing roadmap, testable acceptance criteria, exact-head verification, security review, and no-known-unresolved-issue completion standard.
