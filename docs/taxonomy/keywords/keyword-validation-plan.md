# Harvester Keyword Validation Plan

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Audience: **Harvester taxonomy, data, backend, search, QA, compliance, security and release teams**

## 1. Purpose

This plan defines the complete validation process for Harvester keyword profiles before they may be approved, activated, used in a Harvest Job, or allowed to influence evidence, opportunity, contact-readiness or lead decisions.

It operationalizes the validation requirements already defined by:

- `docs/delivery/keyword-profile-runtime-delivery-plan.md`;
- `docs/taxonomy/keywords/ultimate-keyword-profile-standard.md`;
- `docs/taxonomy/keywords/benchmark-and-gold-set-standard.md`;
- `docs/taxonomy/keywords/keyword-quality-and-review-standard.md`;
- `docs/taxonomy/keywords/keyword-plan-change-control.md`;
- the NEWAX AI Engineering Accuracy and Verification Protocol.

The benchmark standard defines the required example classes, sample depth, metrics and provisional thresholds. This document defines how those requirements are executed, reviewed, recorded, released and monitored.

A profile is not valid merely because its Markdown row exists, its syntax parses, or a few examples look plausible. It becomes eligible for activation only after the applicable automated checks, human reviews, benchmark gates, shadow tests, policy controls and exact-version approval evidence pass.

## 2. Validation scope

This plan applies to every version of:

- 1,586 domain identity profiles;
- 519 canonical activity profiles;
- organization-cue profiles;
- exclusions and negative-context profiles;
- ambiguity and acronym controls;
- facility, asset, process and relationship vocabulary packs;
- semantic seeds and entity-expansion profiles;
- classification-code crosswalks;
- provider-offering intent, procurement, pain, technology, replacement, integration and existing-solution profiles;
- event and freshness profiles;
- source-suitability profiles;
- source-specific query templates;
- decision-role profiles;
- contact-route profiles;
- geography profiles;
- English, Urdu, Roman Urdu and mixed-language locale packs;
- query-composition profiles;
- benchmark and gold-set versions.

The plan validates candidate configuration and observed behavior. It does not authorize source access, outreach, sensitive inference, or production activation by itself.

## 3. Non-negotiable validation rules

1. Keywords discover evidence; they do not independently prove a domain, activity, gap, intent, opportunity, authority, consent or lead.
2. Every domain remains independently configured and validated.
3. Activity applicability and selection remain independent inside every domain.
4. A term selected or matched for one domain must not silently activate another domain.
5. Offering-specific commercial profiles require an active provider offering.
6. Positive profiles must be tested with exclusions, contradictions, stale evidence, duplicate origins and unsuitable sources.
7. Broad, ambiguous or one-word terms require explicit context controls.
8. “Not found” is not “absent” without adequate source coverage.
9. Semantic similarity, embeddings and classification codes cannot bypass profile, entity, evidence or policy validation.
10. Public contact information does not establish consent or permission to use a channel.
11. Sensitive-sector profiles require stricter review and zero harmful inference from weak evidence.
12. Active versions are immutable. Revisions create new candidate versions.
13. Completed Harvest Jobs retain the exact validated versions used.
14. No aggregate metric may hide a failing high-risk profile.
15. No profile is Complete until applicable runtime, benchmark, workflow, security and exact-head verification evidence exists.

## 4. Validation outcomes and finding severity

### 4.1 Validation outcomes

Every gate returns one of:

| Outcome | Meaning |
| --- | --- |
| `PASS` | All mandatory checks passed. |
| `PASS_WITH_REVIEW` | Automated checks passed, but a defined human review remains mandatory before progression. |
| `FAIL` | One or more blocking findings exist. Progression is prohibited. |
| `BLOCKED` | Required data, source access, reviewer capability or tooling is unavailable. The unproven scope must be stated. |
| `NOT_APPLICABLE` | The gate does not apply, with recorded rationale. |

### 4.2 Finding severity

| Severity | Meaning | Default effect |
| --- | --- | --- |
| `BLOCKER` | Missing authority, broken reference, unsafe design, unavailable mandatory evidence or invalid lifecycle state | Stops validation and activation |
| `CRITICAL` | Harmful false positive, private-data exposure, contact-policy violation, sensitive inference, tenant leak or query safety failure | Stops activation and requires incident-level review |
| `HIGH` | Material semantic error, source mismatch, activity propagation, offering-isolation failure, benchmark threshold failure or known regression | Stops activation |
| `MEDIUM` | Narrow quality defect with controlled impact | Requires correction or explicit approved exception before activation |
| `LOW` | Minor wording, metadata or maintainability issue | May be scheduled with owner and due date |
| `INFO` | Observation or improvement suggestion | Does not block |

No `BLOCKER`, `CRITICAL` or `HIGH` finding may remain open when a profile becomes `APPROVED` or `ACTIVE`.

## 5. Roles and separation of duties

| Role | Responsibility |
| --- | --- |
| Profile author | Creates or revises candidate terms and rationale |
| Taxonomy custodian | Protects canonical codes, meanings, ancestry and registry consistency |
| Lexical reviewer | Reviews normalization, spelling, morphology, match modes, regex and phrase boundaries |
| Domain reviewer | Confirms sector, domain, activity and organization meaning |
| Source reviewer | Confirms source suitability, syntax, query limits and evidence limitations |
| Locale reviewer | Reviews language, script, transliteration and local trade terminology |
| Compliance or sensitive-sector reviewer | Reviews privacy, prohibited inference, contact policy and regulated-sector risk |
| Benchmark curator | Builds and freezes development, validation and holdout examples |
| QA validator | Runs automated, regression, workflow and release validation |
| Approver | Authorizes an immutable version for a defined rollout stage |
| Operator | Activates only approved versions and monitors post-activation behavior |

Required controls:

- An author must not be the sole approver of a high-risk profile.
- Sensitive-sector, role, contact-route and provider-intent profiles require at least two qualified reviewers across the relevant dimensions.
- Holdout adjudication must not be performed solely by the person who tuned the profile.
- Reviewer identity, role, decision, date and rationale must be retained.

## 6. Validation lifecycle

The controlled lifecycle is:

```text
DRAFT
→ STRUCTURAL_VALIDATION
→ LEXICAL_REVIEW
→ DOMAIN_REVIEW
→ SOURCE_REVIEW
→ LOCALE_REVIEW where applicable
→ COMPLIANCE_REVIEW where applicable
→ READY_FOR_TEST
→ BENCHMARK_VALIDATION
→ REGRESSION_VALIDATION
→ SHADOW_NO_DECISION
→ APPROVED_FOR_STAGE
→ ACTIVE_IN_STAGE
→ POST_ACTIVATION_REVIEW
→ SUPERSEDED, REVOKED or ARCHIVED
```

A lifecycle state may advance only when the required validation record identifies the exact profile version, validator version, benchmark version and result.

## 7. Gate 0 — Inventory and source-integrity validation

Before reviewing individual terms, validate the controlled dataset itself.

Required checks:

- all expected registry files exist;
- every file is indexed by the keyword taxonomy entry point;
- sector, domain, activity and profile counts match authoritative registries;
- all 16 sectors are represented;
- all 1,586 domain profiles are represented exactly once in their canonical sector registry;
- all 519 activity identities are represented exactly once in the canonical activity registry;
- stable codes have not been reused or silently reassigned;
- duplicate source documents do not define competing active truth;
- checksums or source revisions are recorded for imported datasets;
- generated outputs identify their generator and source version;
- no temporary, superseded or local-generation file is treated as an active authority.

Blocking conditions include missing profiles, count mismatches, duplicate canonical codes, unindexed authorities or unexplained code meaning changes.

## 8. Gate 1 — Structural validation

Validate every profile and term for:

- required identifiers and metadata;
- valid code format and uniqueness;
- valid profile type;
- valid keyword type;
- valid match mode;
- valid language and locale codes;
- valid polarity and requirement level;
- valid weight range;
- valid source, geography and freshness scopes;
- valid lifecycle state;
- valid version number and ancestry;
- valid effective, review and expiry dates;
- valid tenant ownership for tenant-created profiles;
- valid immutable-versus-mutable state rules.

Structural validation must be deterministic and automated before human review begins.

## 9. Gate 2 — Referential-integrity validation

Validate that:

- every domain reference resolves to one canonical domain;
- every activity reference resolves to one canonical activity;
- every domain–activity combination is allowed by the controlled mapping;
- every control-profile reference exists;
- every provider-offering reference exists and is active when required;
- every locale term references one canonical parent term;
- every semantic seed references an approved profile version;
- every classification code stores its system, edition, jurisdiction and effective date;
- every source rule references a supported source class or adapter contract;
- every benchmark case references an immutable profile and benchmark version;
- every superseded version has a valid successor or recorded retirement reason;
- no orphaned reference remains after deprecation.

Referential errors are `BLOCKER` findings.

## 10. Gate 3 — Normalization and lexical validation

### 10.1 Normalization

Compute and retain reviewed normalized forms using explicit rules for:

- Unicode normalization;
- case folding where appropriate;
- whitespace normalization;
- punctuation handling;
- hyphen, apostrophe and slash handling;
- diacritics where supported;
- script and transliteration identity;
- language-specific tokenization;
- exact phrase boundaries.

The original reviewed text must never be discarded merely because a normalized form exists.

### 10.2 Lexical rejection and review checks

Reject or route to review:

- blank, whitespace-only or punctuation-only terms;
- control or invisible characters;
- malformed stems such as `formulat`, `manufactur` or `franchis`;
- blind singularization or pluralization;
- accidental partial-word substitutions;
- duplicated aliases after normalization;
- aliases identical to an exclusion in the same profile;
- unsupported wildcards or source syntax;
- unsafe, catastrophic or unbounded regex;
- one-character or overbroad one-word aliases without explicit context;
- acronyms with multiple common meanings and no disambiguation rule;
- generated translations with no locale review;
- terms containing secrets, credentials or private personal data.

### 10.3 Regex validation

Every regex term requires:

- a stated purpose;
- positive and negative examples;
- anchoring and boundary review;
- adversarial input tests;
- an approved execution-time and input-size budget;
- a supported engine declaration;
- a non-regex fallback where practical.

The provisional validator target is no catastrophic backtracking and execution within the approved per-expression budget against the adversarial corpus. The runtime team must set and document the production budget before activation.

## 11. Gate 4 — Semantic and domain validation

A qualified reviewer must confirm:

- the term genuinely belongs to the intended domain or activity;
- the term does not merely describe a customer, user, article, job, product listing or unrelated concept;
- physical systems are not mislabeled as software;
- software platforms are not mislabeled as public authorities, facilities or manufacturers;
- service providers are not mislabeled as product manufacturers;
- a facility term is not treated as proof of the activity performed inside it;
- an event term is not treated as permanent organization identity;
- a role term is not treated as purchase authority;
- a technology mention is not treated as confirmed ownership, active use or dissatisfaction;
- a broad term has sufficient sector, organization, source, activity, entity, proximity or co-occurrence controls;
- sensitive meaning is not inferred from weak, private or unrelated evidence.

Every accepted ambiguous term must record its ambiguity class, required corroboration and negative examples.

## 12. Gate 5 — Cross-profile collision and ambiguity validation

Generate a collision report across all active and candidate profiles.

Review:

- identical normalized terms in several domains;
- identical acronyms with different meanings;
- parent and child domain overlap;
- product and service overlap;
- activity and identity overlap;
- organization-cue and domain-term overlap;
- positive and exclusion overlap;
- English and locale collision;
- source-specific meanings;
- semantic-neighbor confusion.

An overlap is not automatically an error. It must be classified as:

```text
SAFE_SHARED_TERM
CONTEXT_REQUIRED
MUTUALLY_EXCLUSIVE
PARENT_CHILD
SOURCE_DEPENDENT
LOCALE_DEPENDENT
PROHIBITED_COLLISION
```

Profiles with substantial vocabulary overlap require explicit disambiguation tests. No arbitrary overlap percentage may automatically approve or reject a profile, but the validator must surface high-overlap pairs for review.

## 13. Gate 6 — Organization-cue, exclusion and contradiction validation

For each positive identity, activity or signal profile, verify that the relevant negative controls are present and effective.

Test at minimum:

- consumer and personal context;
- résumé, vacancy and job-seeker context;
- article, academic or research-only context;
- news mention without operating-organization evidence;
- product listing without organization evidence;
- dissolved, closed, inactive or former organizations;
- cancelled, expired or awarded opportunities;
- wrong geography or unsupported jurisdiction;
- duplicated, mirrored or syndicated sources;
- unrelated lexical meanings;
- stale affiliation or former role;
- explicit contradiction;
- suppression and contact restrictions;
- prohibited sensitive inference.

A positive match that survives only because its negative query was omitted is a validation failure, not a successful discovery.

## 14. Gate 7 — Domain–activity non-propagation validation

The validation suite must prove that:

- selecting an activity for one domain does not select it for any other domain;
- matching an activity under one domain does not establish that activity under another domain;
- shared canonical activity terms retain separate domain-specific evidence and confidence;
- removing one domain–activity selection does not alter another combination;
- profile version changes affect only the combinations that reference that version;
- broad-sector selection alone does not activate every domain or activity.

Required regression scenarios include pharmaceutical manufacturing versus pharmaceutical distribution, medical-device installation versus manufacturing, food processing versus food retail, software implementation versus physical equipment installation, and postal/courier operations versus general logistics.

Any propagation failure is `HIGH` or `CRITICAL` when it can influence opportunity or contact decisions.

## 15. Gate 8 — Provider-offering isolation validation

Prove that offering-specific profiles cannot participate unless the provider has an active offering mapped to the selected market combination.

Test that inactive or absent offerings cannot:

- activate buying-intent terms;
- create service-gap hypotheses;
- alter opportunity scores;
- select decision-maker roles;
- make a lead contact-ready;
- influence exports or outreach packages;
- appear in explanations as an offered capability.

Existing-solution, competitor, replacement, integration and operational-pain evidence must remain multi-interpretation evidence until the active offering and evidence policy resolve the permitted opportunity state.

Any inactive-offering leakage is a `HIGH` finding.

## 16. Gate 9 — Source-suitability and query validation

### 16.1 Source suitability

Validate each signal against the source classes permitted to support it.

Examples:

- an official registry may support legal identity but not current buying intent;
- a job posting may support hiring and technology evidence but not confirmed budget;
- a procurement portal may support a tender but not prove final award until status evidence exists;
- a directory may support discovery but not high-confidence operational claims;
- a review may support a complaint signal but not an organization-wide fact;
- a public professional profile may support a current role only when affiliation and date are credible.

### 16.2 Query validation

Every generated query must be checked for:

- non-empty executable form;
- supported source syntax;
- source-specific quoting and operators;
- bounded expansion and combination count;
- deduplicated aliases;
- positive, exclusion and contradiction components where required;
- source length, rate, cost and pagination limits;
- prohibited personal or sensitive terms;
- secrets and credentials;
- unsupported jurisdiction or language;
- estimated breadth and result-volume risk;
- contributing profile, term, query-family and version provenance;
- deterministic preview output for the same frozen inputs.

Uncontrolled Cartesian expansion is prohibited.

## 17. Gate 10 — Locale validation

Every locale pack requires:

- native or professionally competent language review;
- canonical parent references;
- script, transliteration and mixed-language examples;
- spelling and spacing variants;
- local trade terminology;
- false friends and culturally specific negatives;
- source-specific examples;
- parity comparison against the canonical English profile;
- independent activation state by language and locale.

Urdu, Roman Urdu and mixed Pakistan business-language terms remain candidate data until their gold sets and qualified review pass.

Machine translation or transliteration may propose terms. It may not activate them.

## 18. Gate 11 — Sensitive-sector, privacy and contact-policy validation

Healthcare, legal, finance, government, employment, security and nonprofit-beneficiary profiles require enhanced review when matches could imply sensitive facts.

Prohibited outcomes include:

- inferring medical diagnosis or treatment need;
- accusing a person or organization of crime, fraud or misconduct from weak evidence;
- inferring financial distress without authoritative support;
- collecting private patient, beneficiary, employee or client data;
- targeting protected characteristics, political beliefs or private vulnerability;
- treating a public contact route as consent;
- bypassing procurement, referral, professional or channel restrictions.

The validation set must contain harmful-near-match cases and prove that the profile blocks or routes them to required review.

Contact-route validation requires current affiliation, official purpose, source, collection date, allowed channel, suppression state and policy outcome. The provisional target for contact-route profiles is at least 0.98 precision with zero private or stale contact acceptance in the reviewed critical set.

## 19. Gate 12 — Gold-set construction and benchmark validation

The [Keyword Benchmark and Gold-Set Standard](benchmark-and-gold-set-standard.md) governs example classes, sample depth, evaluation splits and provisional thresholds.

### 19.1 Required example classes

Every material profile must include applicable examples from:

```text
TRUE_POSITIVE
TRUE_NEGATIVE
NEAR_POSITIVE
AMBIGUOUS
CONTRADICTORY
STALE
DUPLICATE_ORIGIN
WRONG_ENTITY
WRONG_SECTOR
WRONG_ACTIVITY
WRONG_GEOGRAPHY
SOURCE_UNSUITABLE
LOCALE_VARIANT
MALFORMED_OR_NOISY_TEXT
```

### 19.2 Gold-set quality rules

- Real or faithfully sanitized source examples are preferred.
- Synthetic examples may supplement but cannot be the sole activation evidence.
- Source snapshots or immutable references must be retained.
- Development, validation and holdout sets remain separate.
- Holdout examples must not be used to tune the candidate.
- Duplicate origins must not cross evaluation splits.
- Sensitive examples must use protected handling and minimum necessary content.
- Expected match, exclusion, evidence grade and disposition must be adjudicated before execution.

### 19.3 Provisional activation thresholds

Use the benchmark standard’s profile-specific thresholds, including:

- high-precision domain identity: precision `>= 0.95`;
- broad or contextual identity: precision `>= 0.85` with mandatory corroboration;
- activity confirmation: precision `>= 0.90` with entity and domain context;
- direct provider intent: precision `>= 0.95` with verified source and event date;
- operational pain: precision `>= 0.85` with no unsupported accusation;
- contact route: precision `>= 0.98` with zero private or stale critical acceptance;
- sensitive-sector signal: precision `>= 0.98` with zero harmful inference in the critical set.

Thresholds are starting gates and may become stricter through change control. No lower threshold may be introduced merely to make an existing profile pass.

## 20. Gate 13 — Regression, overlap and mutation validation

Every revision must run:

- its own benchmark suite;
- all previously failing examples fixed by the profile;
- overlapping and neighboring profiles;
- parent and child profiles;
- sensitive-sector suite where applicable;
- malformed-token and Unicode suite;
- acronym ambiguity suite;
- source-query parser suite;
- locale suite;
- domain–activity non-propagation suite;
- inactive-offering isolation suite;
- contradiction, stale and duplicate-origin suites.

Use controlled mutation tests to prove that removing required context, exclusions, freshness or source constraints causes the expected validation failure. A test suite that still passes after its safeguard is removed is not testing that safeguard.

A candidate cannot activate when it reintroduces a previously resolved `CRITICAL` or `HIGH` false positive.

## 21. Gate 14 — End-to-end composition validation

Validate complete frozen target configurations rather than only isolated terms.

Each end-to-end scenario must preserve and test:

```text
Sector
+ Domain
+ Domain-specific Activity
+ Organization cue
+ Active Provider Offering where required
+ Positive, exclusion and contradiction profiles
+ Source class
+ Geography
+ Language and locale
+ Query family
+ Freshness policy
+ Evidence threshold
+ Benchmark version
```

Required scenarios include:

- precise identity discovery;
- broad identity requiring corroboration;
- correct organization with wrong activity;
- correct activity under wrong domain;
- inactive offering with apparent buying signal;
- existing solution indicating integration rather than replacement;
- stale procurement event;
- cancelled or awarded opportunity;
- duplicate evidence across mirrored sources;
- conflicting sources;
- role cue without current affiliation;
- public contact blocked by suppression or policy;
- locale match with English canonical explanation;
- sensitive-sector near match routed to human review;
- insufficient coverage producing `UNKNOWN` or `NOT_DETECTED`, never confirmed absence.

## 22. Gate 15 — Shadow and staged validation

The rollout path is:

```text
OFFLINE_TEST
→ SHADOW_NO_DECISION
→ INTERNAL_RESEARCH_ONLY
→ LIMITED_WORKSPACE_ROLLOUT
→ CONTROLLED_PRODUCTION
→ FULLY_ACTIVE
```

### 22.1 Shadow validation

In `SHADOW_NO_DECISION`:

- profiles may generate candidate matches and explanations;
- they may not change qualification, opportunity, selection, export, contact or outreach state;
- reviewers compare shadow outcomes with the current approved baseline;
- false positives, misses, source cost, duplicate inflation and review burden are measured;
- every unexpected high-impact result becomes a regression case.

### 22.2 Stage promotion

Promotion requires:

- benchmark thresholds met;
- no open blocker, critical or high finding;
- reviewer approval for the target stage;
- defined permitted downstream actions;
- monitoring and rollback thresholds;
- exact profile, benchmark, query and validator versions;
- an approved rollback version.

## 23. Gate 16 — Activation validation

A profile version may become `ACTIVE` only when:

- structural, referential, lexical, semantic, collision, source, locale and policy gates pass as applicable;
- required gold sets exist and pass;
- regression and end-to-end suites pass;
- shadow or prior rollout-stage evidence passes;
- required reviewers approve;
- the version diff is reviewed;
- the activation scope is explicit;
- the rollback target is tested and available;
- activation is authorized, tenant-scoped where applicable and audited;
- no unresolved blocking conflict remains.

Activation approval must record known limitations and prohibited uses. Approval for one source, locale, sector, offering or precision mode does not imply approval for another.

## 24. Gate 17 — Post-activation validation and drift monitoring

Monitor by profile, source, sector, locale and offering:

- precision from reviewed samples;
- false-positive and false-negative review rates;
- ambiguity rate;
- exclusion accuracy;
- contradiction-detection rate;
- duplicate-origin suppression;
- stale-signal suppression;
- source acceptance and yield;
- entity-resolution error rate;
- reviewer agreement and overturn rate;
- opportunity confirmation rate;
- downstream irrelevance, complaint and suppression rate;
- contact-policy violations;
- query cost and result-volume drift;
- locale parity;
- model or embedding drift where used.

Review cadence must be risk-based:

- critical contact, sensitive-sector and direct-intent profiles: continuous alerts plus scheduled monthly review;
- high-impact commercial profiles: at least quarterly review;
- low-risk narrow identity profiles: at least annual review or event-triggered review;
- every profile: immediate review after material source, law, policy, model, taxonomy or organization change.

These are initial governance cadences and may be made stricter through approved policy.

## 25. Rollback and revocation triggers

Immediately pause, revoke or roll back an affected version when any of the following occurs:

- harmful sensitive inference;
- private or prohibited contact acceptance;
- tenant-isolation failure;
- activity or offering propagation;
- critical false positive;
- benchmark precision below the approved threshold;
- known regression reappears;
- material source-policy change;
- uncontrolled query breadth, cost or rate behavior;
- contradiction, freshness or duplicate suppression failure affecting decisions;
- unexplained spike in reviewer overturn, irrelevance, complaint or suppression;
- corrupted profile, benchmark or version provenance;
- inability to reproduce a material decision.

Rollback must preserve the failed version, evidence and incident record. It must not rewrite completed Harvest Jobs.

## 26. Validation automation requirements

The implementation should provide separate, reviewable validators for:

```text
registry inventory and count validation
schema and enum validation
code and reference validation
Unicode and normalization inspection
lexical and malformed-token detection
duplicate and collision analysis
regex safety testing
source-query syntax validation
query expansion and budget validation
sensitive-term and policy checks
benchmark execution
regression execution
snapshot and version-diff validation
coverage reporting
shadow-result comparison
post-activation drift monitoring
```

Automation must emit machine-readable results and a human-readable report. It may identify semantic risks, but it does not replace qualified human review.

## 27. CI and scheduled validation

### 27.1 Pull-request validation

A pull request changing a keyword, profile, pack, benchmark, source rule or validator must run:

- formatting and documentation-link checks;
- registry count and code checks;
- structural and referential validation;
- lexical and Unicode validation;
- changed-profile benchmark suites;
- overlapping-profile regression suites;
- sensitive and contact-policy suites where affected;
- query snapshot and budget checks;
- version-diff and migration checks where runtime data is affected;
- security checks;
- complete repository CI against the exact head.

### 27.2 Scheduled validation

Run full cross-profile regression, source syntax, locale, stale-profile and drift checks on an approved schedule. Nightly or weekly frequency must be selected according to runtime cost and risk; critical production alerts are not deferred to scheduled runs.

### 27.3 Release validation

Before a runtime release:

- all 1,586 domain profiles import successfully;
- all 519 activity profiles import successfully;
- all controlled counts match;
- migrations pass from empty and production-equivalent databases;
- downgrade or forward-fix strategy is tested;
- API and frontend workflows pass;
- tenant isolation and permissions pass;
- benchmark and regression suites pass;
- source adapters pass contract and policy tests;
- activation and rollback workflows pass;
- exact-head CI and security checks pass;
- no known unresolved release blocker remains.

## 28. Validation evidence record

Every material validation run must retain:

```text
validation_run_id
profile IDs and versions
registry and source revisions
validator name and version
benchmark and gold-set version
query-composition version
source-adapter version where applicable
model or embedding version where applicable
started and completed timestamps
environment and tenant scope
checks executed
metrics by profile and example class
findings with severity and ownership
reviewer decisions and rationale
known limitations
final outcome
approved rollout stage
rollback version
exact commit SHA and CI references
```

A summary without reproducible inputs is not sufficient evidence.

## 29. Validation reporting

Required reports include:

- registry coverage report;
- unresolved-reference report;
- malformed and unsafe-term report;
- collision and ambiguity report;
- source-suitability report;
- benchmark scorecard by profile and example class;
- sensitive-sector and contact-policy report;
- locale parity report;
- regression report;
- shadow comparison report;
- activation-readiness report;
- post-activation drift report;
- rollback and incident report.

Dashboards may summarize results, but the underlying findings and examples must remain inspectable.

## 30. Execution waves

Validation should proceed in dependency order.

### Wave 0 — Validators and authoritative inventory

- lock schemas, enums, codes and lifecycle;
- implement inventory, count, structural, reference, normalization and lexical validators;
- freeze authoritative registry manifests.

### Wave 1 — Shared controls

Validate organization cues, exclusions, ambiguity controls, evidence controls, source suitability, query families, role cues and contact routes before using them across sector profiles.

### Wave 2 — Highest-risk profiles

Prioritize sensitive-sector profiles, contact routes, decision roles, direct intent, procurement, operational pain and broad ambiguous identities.

### Wave 3 — Priority domain and activity profiles

Validate high-value domain–activity combinations and their offering-specific overlays, preserving separate configuration for every domain.

### Wave 4 — Remaining English profiles

Complete all remaining domain, activity, source and provider-offering English profiles across all 16 sectors.

### Wave 5 — Locale packs

Validate Urdu, Roman Urdu and mixed-language packs with qualified reviewers and locale-specific gold sets.

### Wave 6 — Semantic and classification expansion

Validate embeddings, semantic seeds, entity relationships and authoritative classification crosswalks only after explainable lexical baselines are stable.

### Wave 7 — Controlled rollout and monitoring

Run shadow, internal, limited-workspace and controlled-production stages before wider activation.

## 31. Acceptance criteria

The validation capability is accepted only when:

1. Every controlled profile type has a defined validator and owner.
2. Authoritative counts and stable codes are automatically checked.
3. Structural, referential, lexical, semantic, source, locale and policy gates are represented.
4. Cross-profile collisions and ambiguity are reviewable.
5. Domain–activity non-propagation is proven.
6. Inactive provider offerings cannot influence commercial decisions.
7. Gold sets use separated development, validation and holdout examples.
8. Profile-specific thresholds pass without hidden high-risk failures.
9. Known false positives remain permanent regression cases.
10. Query previews are bounded, source-valid and fully traceable.
11. Sensitive-sector and contact-policy suites pass with zero critical violations.
12. Shadow mode cannot influence downstream decisions.
13. Activation and rollback are versioned, authorized and audited.
14. Post-activation monitoring can detect drift and policy violations.
15. Completed Harvest Jobs preserve the validated versions used.
16. Exact-head CI, security and release verification pass for the runtime implementation.
17. No known unresolved blocking issue remains.

## 32. Honest completion status

This document completes the **validation design and execution plan** at documentation level.

It does not mean that:

- the 1,586 domain profiles or 519 activity profiles have gold sets;
- Urdu or Roman Urdu profiles have passed native review;
- validators, benchmark runners or approval workflows exist;
- source queries have been executed;
- profiles have passed shadow rollout;
- any profile is active in production;
- keyword behavior is runtime-verified or Complete.

Until the required datasets, tooling, reviews, benchmarks, runtime workflows and exact-head verification exist, the keyword system remains **Proposed / Not implemented**.
