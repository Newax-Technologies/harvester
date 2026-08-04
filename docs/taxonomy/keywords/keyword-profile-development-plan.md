# Harvester Keyword Profile Development Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document defines how Harvester will turn the existing sector, domain, activity, provider-offering, source, evidence, decision-maker, and contact registries into governed keyword profiles and evidence-backed lead discovery.

It is additive to the existing keyword registries. It does not replace any domain list, activity list, control profile, source rule, lead-signal profile, or evidence requirement.

## 1. Intended outcome

Harvester must let a provider configure a target market through:

```text
Broad sector
→ product or service domain
→ independently selected domain-specific activities
→ active provider offering
→ governed keyword profile
→ source-appropriate queries
→ collected evidence
→ supported opportunity
→ qualified lead
```

The keyword layer must improve discovery and relevance without treating ordinary words as proof that an organization performs an activity, has a service gap, intends to buy, or is eligible for contact.

## 2. Keyword layers

Keyword profiles are separated into independently governed layers.

### 2.1 Domain identity terms

These terms help identify what product, service, institution, or market domain an organization belongs to.

Examples:

- pharmaceutical products
- diagnostic laboratory
- cold-chain logistics
- property management
- legal practice
- payment gateway

Domain identity terms do not prove a particular business activity.

### 2.2 Activity terms

These terms help identify what an organization appears to do with the selected domain.

Examples:

- manufacturing
- distributing
- warehousing
- retailing
- installing
- maintaining
- promoting
- recycling

Activity terms come from the shared canonical activity registry, but their applicability and user selection remain independent for every domain.

### 2.3 Organization cues

Organization cues distinguish an operating organization from a product mention, article, job candidate, academic discussion, consumer review, or unrelated entity.

Examples:

- company
- manufacturer
- distributor
- hospital
- university
- law firm
- operator
- authority
- foundation

Organization cues strengthen classification but do not independently establish identity.

### 2.4 Exclusions and negative context

Exclusion profiles suppress or downgrade irrelevant and misleading matches.

Examples include:

- jobs and individual résumés when organization discovery is intended
- research papers when commercial organizations are intended
- consumer product reviews
- unrelated meanings of ambiguous words
- closed, dissolved, inactive, cancelled, awarded, or expired opportunities
- duplicated directory and press-release copies

Negative context must remain visible in evidence records rather than being silently discarded when it materially affects a decision.

### 2.5 Lead-generation signals

Lead-generation signals explain why a resolved organization may be commercially relevant now.

They may include:

- direct inquiry
- procurement or tender activity
- expansion
- hiring
- system replacement
- integration requirement
- operational pain
- compliance requirement
- maintenance requirement
- technology footprint
- budget or funding evidence
- current responsible-role and lawful-contact evidence

Lead-generation signals may only influence opportunity assessment when an applicable provider offering is active.

### 2.6 Service-specific terms

Service-gap, buying-intent, competitor, existing-solution, problem-signal, and replacement terms belong to a provider offering or offering family.

They must not be copied into the general domain identity profile.

For example:

```text
Domain: Pharmaceuticals
Activity: Distribution
Provider offering: Distributor Management System
```

Only this approved combination may activate terms concerning dealer portals, order booking, territory management, sales-force automation, distributor reconciliation, or related service evidence.

## 3. Separate profile rule

Every canonical domain receives its own domain keyword profile.

Every canonical activity receives one shared canonical activity keyword profile.

Every provider offering receives its own service-specific signal profile.

The final query and evidence configuration is composed from references. It is not created by merging the underlying registries permanently.

```text
Domain profile
+
selected activity profile
+
organization-cue profile
+
exclusion profile
+
active provider-offering profile
+
source and locale rules
=
versioned query plan
```

Selecting or detecting an activity for one domain must never activate the same activity for another domain automatically.

## 4. Query composition plan

For every approved target combination, Harvester must create source-appropriate query families rather than one universal search string.

### 4.1 Precision query

Uses exact domain identity, activity, organization, geography, and provider-offering context.

### 4.2 Recall query

Uses shorter reviewed aliases to discover candidates missed by the precision query.

### 4.3 Entity query

Searches a resolved organization name together with activity, technology, event, or opportunity terms.

### 4.4 Negative query

Searches for contradiction, cancellation, closure, award, inactivity, suppression, or disqualifying context.

### 4.5 Source-specific query

Adapts terms and syntax for organization websites, business directories, government registries, procurement portals, job boards, news, maps, authorized social sources, application marketplaces, and structured feeds.

A query plan must record:

- selected sector
- selected domain
- selected activity
- active provider offering
- keyword profile versions
- source class
- locale
- geography
- match mode
- generated query
- exclusions
- execution timestamp

## 5. Match modes

The implementation must support:

```text
EXACT
PHRASE
SEMANTIC
ENTITY
REGEX
```

Match mode is part of the evidence record. A semantic match must not be represented as an exact phrase match merely because both produced a candidate.

## 6. Evidence plan

A keyword match creates an evidence observation, not a business conclusion.

Each observation must preserve:

- source
- source URL or source identifier
- source class
- retrieved text or structured field
- matched term
- match mode
- keyword profile version
- event date where known
- collection date
- language
- organization candidate
- domain candidate
- activity candidate
- provider-offering context where applicable
- positive or negative context
- confidence dimensions

Harvester must assess:

- source reliability
- source suitability for the claimed signal
- recency
- event date
- entity resolution confidence
- domain confidence
- activity confidence
- contradiction
- duplicate evidence origin
- language and translation uncertainty
- coverage adequacy

“Not found” is not “absent” unless source coverage is sufficient for the claim.

## 7. Opportunity qualification plan

A supported opportunity requires the complete eligibility chain:

```text
Provider selected the sector
+
provider selected the domain
+
provider approved the activity for that domain
+
provider actively offers the service
+
the service applies to the domain–activity combination
+
relevant evidence exists
+
contradictions and exclusions are resolved
+
confidence meets the approved threshold
```

A domain match alone must not create a service gap.

An activity match alone must not create buying intent.

An existing solution may indicate replacement, integration, optimization, support, migration, or no opportunity. It is not an automatic disqualification.

## 8. Decision-maker and contact plan

Decision-maker discovery starts only after the organization is resolved to the configured confidence threshold.

Role terms identify likely responsibility, not guaranteed authority.

A contact-ready lead requires:

- resolved organization
- supported opportunity
- current responsible function or role evidence
- current affiliation evidence
- lawful public or authorized contact route
- suppression and consent checks
- jurisdiction and channel-policy compliance

Public contact information does not create permission to contact automatically.

## 9. Local-language plan

Canonical profiles remain in controlled English.

Urdu, Roman Urdu, and other locale terms are maintained in separately reviewed language packs.

Locale packs may contain:

- translations
- transliterations
- common local abbreviations
- regional organization terminology
- local commercial vocabulary
- spelling variants

Translation or transliteration must not silently alter the canonical profile.

Every locale term must preserve its canonical parent term and review status.

## 10. Profile lifecycle

Every keyword profile follows:

```text
Draft
→ reviewed
→ tested against benchmark cases
→ approved
→ activated
→ monitored
→ revised through version control
→ deprecated when replaced
```

Production profiles must never mutate silently from user feedback or automated learning.

Feedback may create a proposed profile change. Activation requires review, benchmark testing, versioning, and rollback capability.

## 11. Preview and test plan

Before activation, the interface must let an authorized user preview:

- generated queries
- included terms
- excluded terms
- selected sources
- source-specific variations
- expected match modes
- example positive cases
- example negative cases
- estimated breadth
- profile version

The test facility must support known-positive, known-negative, ambiguous, multilingual, stale, duplicate, and contradictory examples.

## 12. Minimum data model

| Entity | Minimum fields |
| --- | --- |
| `KeywordProfile` | `id`; `code`; `profile_type`; `name`; `status`; `version`; `language`; `owner` |
| `KeywordTerm` | `id`; `profile_id`; `term`; `term_type`; `match_mode`; `weight`; `status`; `canonical_term_id` |
| `DomainKeywordProfileReference` | `domain_id`; `keyword_profile_id`; `status`; `version` |
| `ActivityKeywordProfileReference` | `activity_id`; `keyword_profile_id`; `status`; `version` |
| `OfferingKeywordProfileReference` | `provider_offering_id`; `keyword_profile_id`; `status`; `version` |
| `QueryPlan` | `id`; `target_profile_id`; `source_class`; `locale`; `query_family`; `generated_query`; `profile_versions` |
| `KeywordEvidenceObservation` | `id`; `query_plan_id`; `source_id`; `matched_term_id`; `match_mode`; `text`; `event_date`; `collected_at`; `polarity` |
| `KeywordProfileBenchmark` | `id`; `profile_id`; `case_type`; `input`; `expected_result`; `status` |
| `KeywordProfileChangeProposal` | `id`; `profile_id`; `reason`; `evidence`; `proposed_change`; `review_status` |

## 13. Implementation sequence

### KWP-1: Registry ingestion

Convert the approved Markdown datasets into versioned runtime records without changing canonical codes or meanings.

### KWP-2: Profile composition

Compose domain, activity, organization, exclusion, offering, source, geography, and locale references into a query plan.

### KWP-3: Preview and benchmark testing

Provide profile preview, query preview, positive and negative benchmark cases, and review workflow.

### KWP-4: Source execution

Execute source-specific queries through approved adapters and preserve raw observations.

### KWP-5: Evidence classification

Classify domain, activity, organization, event, intent, technology, role, contact, and contradiction evidence separately.

### KWP-6: Opportunity integration

Allow evidence to influence opportunity assessment only through an applicable active provider offering.

### KWP-7: Governance and learning

Record profile performance, false positives, false negatives, review decisions, revisions, deprecations, and rollback history.

## 14. Acceptance criteria

The keyword-profile implementation is not accepted unless:

1. All 1,586 domain profiles retain separate identities.
2. All 519 activity profiles retain shared canonical identities without shared user selection.
3. Domain, activity, organization, exclusion, provider-offering, lead-signal, source, role, contact, and locale layers remain independently versioned.
4. Every query plan records the exact profile versions used.
5. Service-specific terms cannot affect leads when the provider offering is inactive.
6. Negative and contradictory evidence is preserved and evaluated.
7. Duplicate evidence origins do not inflate confidence or score.
8. Match mode and source suitability remain visible.
9. Profile previews and benchmark cases exist before activation.
10. Completed harvest jobs preserve the full profile and query-plan versions used.
11. User feedback cannot silently mutate production profiles.
12. No keyword match independently proves a domain, activity, service gap, opportunity, purchase intent, authority, or consent.

## 15. Delivery boundary

This plan and the existing keyword Markdown files are controlled documentation datasets.

They do not implement database records, migrations, search indexes, embeddings, classifiers, source queries, evidence decisions, opportunity scoring, decision-maker resolution, contact eligibility, outreach, or releases.

Runtime delivery remains separate engineering work requiring schema, migration, API, interface, test, security, and exact-commit CI verification.
