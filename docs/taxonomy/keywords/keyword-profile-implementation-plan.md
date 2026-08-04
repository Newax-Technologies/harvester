# Harvester Keyword Profile Implementation Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document adds the implementation plan for the existing Harvester domain, activity, keyword, lead-signal, role-cue, source-suitability, and evidence-governance registries.

It does not replace:

- [Keyword Taxonomy and Lead-Signal Index](README.md)
- [Sector, Domain, Activity and Keyword Taxonomy Index](../README.md)
- [Harvester Services and Opportunity Model](../../SERVICES.md)
- [Harvester Intelligence Operating Model](../../architecture/harvester-intelligence-operating-model.md)
- [Provider Portfolio and Lead-Generation Profile Model](../../architecture/provider-portfolio-and-lead-generation-profile-model.md)
- [Harvester Standalone Product Roadmap](../../ROADMAP.md)

It adds the missing runtime-delivery sequence and preserves the existing 64-module roadmap rather than creating another module count.

---

## 1. Intended outcome

Harvester must allow a provider to define a target market through controlled selections and then use separate keyword layers to discover evidence without turning ordinary word matches into unsupported opportunities.

The complete chain is:

```text
Provider
→ active offering
→ selected broad sector
→ selected product or service domain
→ approved activity for that domain
→ domain identity profile
→ activity keyword profile
→ organization cues and exclusions
→ offering-specific lead-signal profile
→ source-appropriate query composition
→ evidence capture and contradiction review
→ qualification
→ supported opportunity
→ lawful contact readiness
```

The system does not ask the user to invent keyword lists from a blank screen. It proposes reviewed defaults, allows explicit editing, previews the effect, and versions every approved change.

---

## 2. Keyword layers

The implementation must preserve distinct keyword responsibilities.

### 2.1 Domain identity profile

Answers:

> What product, service, market, institution, material, or operational domain does this organization appear to belong to?

Examples:

- Pharmaceuticals
- Diagnostic Laboratories
- Crop Farming
- Commercial Property
- Corporate Law
- Payment Gateways
- Postal and Courier Services
- Industrial Automation

A domain identity match provides classification evidence. It does not prove an activity, service need, buying intent, gap, or opportunity.

### 2.2 Activity keyword profile

Answers:

> What does the organization appear to do with, for, or around the selected domain?

Examples:

- Manufacturing
- Processing
- Importing
- Distributing
- Warehousing
- Selling
- Promoting
- Installing
- Maintaining
- Repairing
- Recycling
- Advising
- Treating
- Teaching
- Financing

Every domain receives its own applicable activity group through the existing domain–activity mapping. Detecting or selecting an activity for one domain never activates it for another domain.

### 2.3 Organization cues

Answers:

> Does the source describe a real organization, facility, practice, institution, operator, company, program, platform, or public body rather than an unrelated mention?

Organization cues improve precision but cannot replace entity resolution.

### 2.4 Exclusions and negative context

Answers:

> Does the text indicate an irrelevant meaning, individual consumer context, academic discussion, historical mention, closed operation, duplicate listing, unsupported jurisdiction, suppression, or another disqualifying context?

Negative context is evaluated with positive context. It is not applied as a blind global blocklist.

### 2.5 Offering-specific lead-signal profile

Answers:

> Why may this target be relevant now for a service the provider actively offers?

Signal families include:

- Direct inquiry
- Active buying intent
- Procurement or tender activity
- New business, product, branch, facility, or project
- Hiring and organizational expansion
- Replacement, migration, integration, or upgrade need
- Operational pain
- Compliance or reporting requirement
- Maintenance or recurring service due
- Technology footprint
- Contract, renewal, funding, or budget event
- Sector-specific operational trigger

These signals remain subordinate to the active provider offering. No active offering means no service-specific opportunity.

### 2.6 Role and contact cues

Role cues help resolve the function that may own the problem, budget, process, system, asset, or procurement decision.

Contact-route cues identify lawful public or authorized routes such as:

- Official contact page
- Business email
- Main telephone number
- Procurement portal
- Authorized directory record
- Public professional profile
- Direct inquiry or referral channel

A title match does not prove purchase authority. A public contact route does not override consent, suppression, channel, jurisdiction, platform, conflict, or tenant policy.

---

## 3. Required profile separation

The following profiles remain independently versioned:

```text
DomainKeywordProfile
ActivityKeywordProfile
OrganizationCueProfile
ExclusionProfile
OfferingLeadSignalProfile
DecisionMakerRoleProfile
ContactRouteProfile
SourceSuitabilityProfile
LocaleKeywordPack
QueryCompositionProfile
```

They may reference shared canonical terms, but activation, weights, exclusions, evidence requirements, source permissions, and version history remain explicit.

A provider may use the same canonical domain or activity in several target profiles without copying the canonical registry.

---

## 4. User configuration flow

The first-page lead-definition workflow must add keyword configuration after the provider, offering, sector, domain, and activity selections are valid.

```text
1. Select provider
2. Select active offering
3. Select broad sector
4. Select one or more domains
5. Select activities separately inside each domain
6. Review proposed domain and activity keyword profiles
7. Review offering-specific lead signals
8. Review exclusions and negative context
9. Select approved source classes
10. Preview query composition and sample matches
11. Set confidence, evidence and freshness requirements
12. Approve and activate the versioned profile
13. Review final search definition
14. Generate leads
```

The interface must support:

- Accepting recommended terms
- Removing irrelevant terms
- Adding custom terms
- Adjusting required, preferred, optional, or excluded status
- Selecting match mode
- Selecting languages and locale packs
- Restricting terms to source classes
- Previewing positive and negative examples
- Testing against sample sources
- Saving a draft
- Activating a reviewed version
- Rolling back to a prior approved version

Production profiles must not mutate silently from user feedback, model output, or new collected evidence.

---

## 5. Match modes

Every keyword definition must declare one or more supported match modes.

```text
EXACT
PHRASE
SEMANTIC
ENTITY
REGEX
```

The system must preserve:

- The term or entity that matched
- Match mode
- Profile and version
- Source class
- Source record
- Language and locale
- Match position or evidence span where available
- Collection time
- Underlying event time where available
- Positive and negative context
- Query family
- Extraction or classifier version

Raw match counts do not become opportunity scores.

---

## 6. Source-appropriate query composition

Queries are assembled from approved layers rather than one giant keyword string.

Example:

```text
Healthcare
+ Pharmaceuticals
+ Distribution
+ active offering: Distributor Management System
+ selected lead signals: expansion, dealer-network complexity, order-processing pain
+ approved source class: company websites and procurement sources
+ geography
+ exclusions
```

The query composer must:

1. Use only selected sector, domain, activity, offering, signal, source, geography, language, and policy versions.
2. Generate positive and negative query families.
3. Avoid unsupported Cartesian expansion of every term combination.
4. Deduplicate equivalent aliases.
5. Respect source query limits and terms.
6. Preserve query provenance.
7. Preview estimated breadth before execution.
8. Warn when a query is excessively broad, contradictory, empty, or likely to produce mostly irrelevant results.
9. Keep direct-intent queries distinct from indirect discovery queries.
10. Keep sensitive-service queries subject to stronger review and consent rules.

---

## 7. Evidence and classification behavior

A keyword match creates a `KeywordMatchEvidence` observation.

It must not directly create:

- A confirmed organization identity
- A confirmed domain
- A confirmed activity
- A service gap
- A qualified opportunity
- A contact-ready lead

The evidence pipeline is:

```text
Keyword match
→ context extraction
→ source and source-signal suitability
→ entity resolution
→ domain classification
→ activity classification
→ lead-signal assessment
→ contradiction and freshness review
→ evidence threshold
→ opportunity assessment
```

“Not found” remains different from “absent.”

An existing solution may indicate:

- No opportunity
- Replacement
- Migration
- Integration
- Optimization
- Support
- Expansion
- Renewal

The outcome depends on the provider offering and evidence, not on the mere presence of a vendor or technology term.

---

## 8. Proposed runtime objects

### 8.1 KeywordDefinition

```text
id
code
canonical_text
keyword_type
supported_match_modes
language
locale
aliases
status
version
created_at
updated_at
```

### 8.2 KeywordProfile

```text
id
workspace_id
profile_type
name
status
version
parent_version_id
created_by
reviewed_by
activated_at
created_at
updated_at
```

### 8.3 KeywordProfileTerm

```text
profile_id
keyword_definition_id
match_mode
weight
requirement_level
source_scope
geography_scope
language_scope
positive_or_negative
notes
status
```

Requirement levels:

```text
REQUIRED
PREFERRED
OPTIONAL
EXCLUDED
```

### 8.4 DomainKeywordProfileReference

```text
domain_id
keyword_profile_id
status
version
```

### 8.5 ActivityKeywordProfileReference

```text
activity_id
keyword_profile_id
status
version
```

### 8.6 OfferingKeywordProfileReference

```text
service_offering_id
lead_signal_profile_id
problem_signal_profile_id
buying_intent_profile_id
existing_solution_profile_id
competitor_profile_id
status
version
```

### 8.7 QueryTemplate

```text
id
profile_version_ids
source_class
query_family
query_structure
negative_query_structure
limits
status
version
```

### 8.8 KeywordMatchEvidence

```text
id
harvest_job_id
source_record_id
keyword_definition_id
keyword_profile_id
match_mode
matched_text
context_excerpt
language
source_class
query_template_id
positive_or_negative
event_date
collected_at
classifier_version
confidence
```

### 8.9 KeywordProfileFeedback

```text
id
profile_id
profile_version
feedback_type
keyword_definition_id
source_record_id
reason
submitted_by
review_status
reviewed_by
created_at
resolved_at
```

Feedback may propose a new version. It must not rewrite the active version silently.

---

## 9. Versioning and immutable job snapshots

Every Harvest Job snapshot must preserve:

```text
broad_sector_versions
domain_versions
domain_activity_assignments
activity_versions
domain_keyword_profile_versions
activity_keyword_profile_versions
offering_signal_profile_versions
organization_cue_profile_versions
exclusion_profile_versions
role_profile_versions
contact_route_profile_versions
source_suitability_profile_versions
locale_pack_versions
query_template_versions
classifier_versions
scoring_profile_versions
```

Later profile edits apply only to future jobs unless the operator explicitly creates a replacement job.

---

## 10. Locale support

Canonical English profiles remain stable.

Urdu, Roman Urdu, regional terminology, abbreviations, spelling variants, and jurisdiction-specific language are delivered through reviewed locale packs.

Locale packs must:

- Reference canonical keyword definitions
- Preserve language and locale
- Record reviewer and version
- Include positive and negative examples
- Avoid automatic translation becoming production configuration
- Support script and transliteration variants
- Remain independently activatable by target profile

---

## 11. Implementation sequence

This plan strengthens existing roadmap modules and does not create additional top-level modules.

### KWP-1 — Registry persistence

- Persist canonical keyword definitions.
- Persist profile types and profile versions.
- Import the existing 1,586 domain profiles and 519 activity profiles.
- Validate stable codes, uniqueness, references, and version metadata.

### KWP-2 — Domain and activity profile APIs

- Read canonical profiles.
- Create tenant-owned profile overrides.
- Validate match modes, requirement levels, sources, languages, and status transitions.
- Preserve canonical records from tenant mutation.

### KWP-3 — Offering-specific signal profiles

- Attach problem, intent, procurement, event, competitor, existing-solution, replacement, integration, and gap profiles only to active service offerings.
- Prevent unselected offerings from affecting discovery or scoring.

### KWP-4 — Profile review and activation

- Draft, review, activate, pause, supersede, and roll back versions.
- Record actor, time, reason, and change diff.
- Prohibit silent production mutation.

### KWP-5 — Query preview and composition

- Compose source-specific positive and negative queries.
- Show term origin and profile version.
- Warn on breadth, contradiction, unsupported source usage, and missing evidence controls.
- Allow sample testing before activation.

### KWP-6 — Match evidence capture

- Persist matched term, context, source, query, match mode, language, event date, and profile version.
- Separate raw keyword evidence from classification and opportunity decisions.

### KWP-7 — Classification and contradiction review

- Evaluate context, source suitability, entity resolution, domain, activity, lead signal, negative evidence, freshness, and duplicate origin.
- Require stronger review for sensitive sectors and services.

### KWP-8 — First-page interface integration

- Insert domain and activity keyword review into the lead-definition flow.
- Insert offering-specific signal review after active offering selection.
- Present final query and evidence summary before generation.

### KWP-9 — Feedback and quality governance

- Capture false-positive, false-negative, irrelevant-term, missing-alias, source-mismatch, and stale-profile feedback.
- Route feedback to human review.
- Produce a new version rather than editing historical jobs.

### KWP-10 — Verification and release

- Import validation
- Unit tests
- API tests
- Query-composition tests
- Negative-context tests
- Locale tests
- Sensitive-sector tests
- Permission and tenant-isolation tests
- Snapshot reproducibility tests
- Performance tests
- Complete CI against the exact head

---

## 12. Planned API boundaries

Names may change during implementation, but the boundaries remain required.

```text
GET    /api/keyword-definitions
GET    /api/keyword-profiles
GET    /api/keyword-profiles/{id}
POST   /api/keyword-profiles
POST   /api/keyword-profiles/{id}/versions
POST   /api/keyword-profiles/{id}/review
POST   /api/keyword-profiles/{id}/activate
POST   /api/keyword-profiles/{id}/pause
POST   /api/keyword-profiles/{id}/rollback

GET    /api/domains/{id}/keyword-profile
GET    /api/activities/{id}/keyword-profile
GET    /api/service-offerings/{id}/keyword-profiles

POST   /api/query-previews
POST   /api/query-previews/{id}/sample
POST   /api/market-definitions/{id}/validate-keywords

GET    /api/keyword-match-evidence
POST   /api/keyword-profile-feedback
GET    /api/keyword-profile-feedback
POST   /api/keyword-profile-feedback/{id}/resolve
```

---

## 13. Interface safeguards

The interface must not:

- Show all 1,586 domain profiles in one undifferentiated dropdown.
- Apply one activity selection to every selected domain.
- Activate every suggested keyword automatically.
- Treat every keyword match as relevant.
- Hide exclusions, negative queries, or source restrictions.
- Allow inactive provider services to attach service-specific signals.
- Allow a user to activate a profile that has not passed required validation.
- Merge locale aliases into canonical English records.
- Present raw keyword counts as opportunity confidence.

The interface should use search, guided refinement, hierarchical selection, reusable profiles, previews, examples, and progressive disclosure.

---

## 14. Acceptance criteria

This plan is satisfied only when:

1. All 1,586 canonical domains resolve to separate versioned domain keyword profiles.
2. All 519 canonical activities resolve to separate versioned activity keyword profiles.
3. Domain and activity profiles remain separate from offering-specific signal profiles.
4. Activities and activity keywords selected for one domain do not propagate to another domain.
5. Service-specific problem, intent, competitor, existing-solution, replacement, integration, and gap profiles require an active selected offering.
6. Every match preserves term, profile version, source, query, match mode, language, context, and time.
7. Positive and negative query families are both supported.
8. Raw keyword counts do not directly affect qualification or opportunity scoring.
9. Existing-solution evidence can produce several reviewed outcomes rather than automatic rejection.
10. Source suitability, event freshness, duplicate evidence origin, contradiction, and negative context affect evidence confidence.
11. Users can preview and test profiles before activation.
12. Canonical profiles cannot be mutated by tenant overrides.
13. Feedback creates a reviewable proposed version and does not silently alter production.
14. Harvest Jobs preserve every relevant profile and query version.
15. Sensitive services enforce stronger consent, privacy, role, source, and human-review controls.
16. The complete verification sequence passes against the exact latest commit before runtime work is called complete.

---

## 15. Delivery boundary

The existing keyword registries and this implementation plan are **repository-integrated documentation**.

They do not implement:

- Database tables
- Migrations
- Import jobs
- APIs
- Interface controls
- Search queries
- Search indexes
- Embeddings
- Classifiers
- Evidence decisions
- Opportunity scoring
- Contact eligibility
- Outreach
- Releases

Runtime delivery remains future engineering work governed by the roadmap, operating model, services model, provider-portfolio model, source policies, security requirements, and exact-head verification standard.
