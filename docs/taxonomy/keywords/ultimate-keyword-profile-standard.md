# Harvester Ultimate Keyword Profile Standard

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This standard defines the maximum controlled depth of a Harvester keyword profile. It applies to all 1,586 domain profiles, 519 activity profiles, provider-offering profiles, lead-signal profiles, decision-maker profiles, contact-route profiles, source profiles, exclusions, and locale packs.

The objective is not to accumulate the largest possible word list. The objective is to create a precise, explainable, source-aware evidence system that finds relevant organizations while controlling false positives, stale signals, duplicate evidence, sensitive-data risk, and unsupported commercial conclusions.

## 1. Governing principle

```text
Canonical meaning
→ reviewed lexical forms
→ contextual combinations
→ source-appropriate queries
→ evidence candidates
→ entity resolution
→ corroboration and contradiction review
→ offering-specific qualification
→ supported opportunity
```

A keyword is never a lead. A keyword is never proof of absence. A keyword is never permission to contact.

## 2. Complete profile anatomy

Every material keyword profile may contain the following independently versioned layers.

| Layer | Purpose | Examples |
| --- | --- | --- |
| `L01_CANONICAL` | Stable human-readable concept | Pharmaceutical Distribution |
| `L02_EXACT` | Exact phrases with highest lexical precision | pharmaceutical distribution; medicine distribution |
| `L03_VARIANT` | Reviewed spelling, punctuation, singular/plural, British/American variants | centre/center; fulfilment/fulfillment |
| `L04_ACRONYM` | Acronyms and initialisms with ambiguity rules | EMR; EHR; WMS; TMS |
| `L05_SHORTHAND` | Industry shorthand, abbreviations, trade usage | pharma distributor; 3PL; O&P |
| `L06_SYNONYM` | Reviewed equivalent expressions | medicine wholesaler; drug distributor |
| `L07_BROADER` | Parent concepts used only with corroboration | pharmaceuticals; healthcare supply |
| `L08_NARROWER` | Child concepts and specialist expressions | oncology medicine distributor |
| `L09_ORGANIZATION` | Organization archetypes and legal-operating forms | manufacturer; stockist; operator; institute |
| `L10_ACTIVITY` | Approved activities for the selected domain | manufacturing; importing; warehousing |
| `L11_ASSET_FACILITY` | Relevant facilities, assets, equipment, and physical environments | plant; warehouse; clinic; fleet; cold room |
| `L12_PROCESS` | Operational processes and workflow language | batch release; order fulfilment; patient intake |
| `L13_REGULATORY` | Licences, standards, registrations, reporting, and compliance concepts | GMP; accreditation; licence renewal |
| `L14_EVENT` | Launch, expansion, funding, merger, hiring, tender, renewal, maintenance | new facility; RFP; contract expiry |
| `L15_PROBLEM` | Offering-dependent operational pain and constraint language | duplicate entry; delayed dispatch |
| `L16_EXISTING_SOLUTION` | Existing software, equipment, vendors, integrations, and legacy systems | ERP; current vendor; legacy platform |
| `L17_ROLE` | Responsible functions and current public roles | operations manager; procurement head |
| `L18_CONTACT` | Lawful organizational contact-route cues | procurement portal; official inquiry form |
| `L19_GEOGRAPHY` | Country, province, city, district, branch, service area, route, site | Punjab; Karachi; industrial estate |
| `L20_SOURCE` | Source-specific terms and structured fields | category label; schema type; tender notice |
| `L21_NEGATIVE` | Explicit exclusions, homonyms, irrelevant intents, stale and closed states | jobs only; definition; permanently closed |
| `L22_CONTRADICTION` | Cancellation, award, replacement completed, closure, or no-longer-current evidence | tender awarded; project cancelled |
| `L23_LOCALE` | Reviewed translations, transliterations, mixed-language and local trade terms | گودام; godam; warehouse |
| `L24_SEMANTIC` | Concept descriptions and embedding seeds | regulated medicine supply chain |
| `L25_IDENTIFIER` | Structured identifiers and classification references | licence number; registration code; industry code |
| `L26_PROXIMITY` | Terms that must occur within a controlled distance or document region | distributor near pharmaceutical |
| `L27_CO_OCCURRENCE` | Required, optional, and prohibited term combinations | domain + activity + organization cue |
| `L28_WEIGHT` | Bounded contribution to evidence dimensions | exact phrase 1.0; broad semantic 0.2 |
| `L29_FRESHNESS` | Event-specific validity and reverification window | tender until deadline; role 90 days |
| `L30_SOURCE_POLICY` | Permitted sources, minimum source grade, and evidence use | regulator for licence claim |
| `L31_REVIEW_POLICY` | Human-review, sensitive-sector, and escalation requirements | mandatory review for misconduct allegation |
| `L32_BENCHMARK` | Positive, negative, ambiguous, multilingual, and source-specific test cases | reviewed gold-set examples |

No implementation is required to activate every layer for every profile. Every activated layer must have a clear purpose and must be reviewable independently.

## 3. Keyword types

The runtime taxonomy must distinguish at least:

```text
DOMAIN_IDENTITY
ACTIVITY_IDENTITY
ORGANIZATION_CUE
ASSET_OR_FACILITY
PROCESS_CUE
REGULATORY_CUE
BUSINESS_EVENT
DIRECT_INTENT
PROCUREMENT_INTENT
OPERATIONAL_PROBLEM
EXISTING_SOLUTION
COMPETITOR_OR_VENDOR
DECISION_ROLE
CONTACT_ROUTE
GEOGRAPHY
SOURCE_CUE
EXCLUSION
CONTRADICTION
LOCALE_ALIAS
SEMANTIC_SEED
STRUCTURED_IDENTIFIER
```

The type controls which evidence dimension a match may affect. A `DOMAIN_IDENTITY` match cannot contribute to purchase intent. A `CONTACT_ROUTE` match cannot contribute to opportunity strength. A `BUSINESS_EVENT` match cannot prove a provider-service gap.

## 4. Precision tiers

| Tier | Meaning | Typical activation rule |
| --- | --- | --- |
| `P1_EXACT` | Canonical exact phrase or reviewed unique identifier | May discover and strongly support identity |
| `P2_HIGH` | Reviewed synonym, acronym, or narrow specialist phrase | Requires entity or sector context when ambiguous |
| `P3_CONTEXTUAL` | Broader term plus organization, activity, source, or geography context | Cannot qualify alone |
| `P4_SEMANTIC` | Conceptually related text found through embeddings or classification | Research queue unless corroborated |
| `P5_EXPLORATORY` | Weak expansion used only to discover new candidates or vocabulary | Never contributes directly to qualification |

Production profiles must state which precision tiers are enabled in `BROAD`, `BALANCED`, and `HIGH_PRECISION` modes.

## 5. Match modes

```text
EXACT
PHRASE
TOKEN_SET
PROXIMITY
REGEX
ENTITY
CLASSIFICATION_CODE
SEMANTIC
STRUCTURED_FIELD
```

Every match record must preserve:

- profile and version;
- keyword or semantic seed identifier;
- match mode;
- matched text or entity;
- source and source location;
- language and locale;
- event date where applicable;
- collection time;
- precision tier;
- evidence dimension;
- exclusion or contradiction result;
- final disposition.

## 6. Co-occurrence and proximity rules

Profiles may define:

- `MUST`: all required concepts must appear;
- `SHOULD`: strengthens the match but is not mandatory;
- `MAY`: exploratory expansion;
- `MUST_NOT`: suppresses or redirects the match;
- `NEAR(n)`: concepts must occur within a reviewed token or structural distance;
- `SAME_FIELD`: terms must occur in the same title, heading, category, record, or structured field;
- `SAME_ENTITY`: evidence must resolve to the same organization;
- `SAME_EVENT`: terms must describe the same dated event rather than unrelated pages.

Example:

```text
Domain: Pharmaceuticals
Activity: Distribution

MUST: pharmaceutical OR medicine
MUST: distributor OR wholesaler OR stockist OR distribution
SHOULD: warehouse OR dealer network OR supply chain
MUST_NOT: university course OR dictionary definition OR personal prescription
```

## 7. Weighting rules

Weights are bounded evidence inputs, not lead scores.

Recommended default ranges:

| Evidence input | Range |
| --- | ---: |
| Exact canonical identity | `0.80–1.00` |
| Reviewed high-precision alias | `0.60–0.85` |
| Structured category or registry classification | `0.70–1.00` |
| Contextual co-occurrence | `0.35–0.70` |
| Semantic similarity | `0.10–0.50` |
| Broad exploratory term | `0.00–0.20` |
| Authoritative contradiction | `-1.00` to suppression |
| Weak negative context | `-0.10–-0.50` |

Repeated matches from the same evidence origin must not linearly increase confidence.

## 8. Source-aware interpretation

The same term has different evidentiary value by source.

Examples:

- `manufacturer` on an official company profile may strongly support activity.
- `manufacturer` in a user comment is weak evidence.
- `RFP` on an official procurement portal may support active intent.
- `RFP template` on a blog is educational content, not procurement.
- `closed` on an official registry may suppress pursuit.
- `closed` in a holiday-hours notice may be temporary and irrelevant.

Every profile must declare source suitability rather than assuming all text is equal.

## 9. Absence and silence

The following are prohibited:

- website does not mention a portal, therefore no portal exists;
- no job post was found, therefore the organization is not hiring;
- no public API documentation was found, therefore no integration exists;
- no device page was found, therefore physical operations are unmonitored.

Absence requires a coverage model, a capability-specific inspection plan, and a defined `NOT_FOUND`, `NOT_OBSERVED`, `UNVERIFIED`, or `CONFIRMED_ABSENT` state.

## 10. Sensitive-sector controls

Healthcare, finance, legal, government, security, employment, education, and nonprofit profiles must not infer protected, confidential, criminal, medical, financial-distress, political, or beneficiary facts from weak keyword evidence.

Mandatory human review applies when a match could:

- imply misconduct, fraud, sanctions, insolvency, or noncompliance;
- reveal or infer patient, student, employee, beneficiary, or client information;
- affect access to employment, healthcare, finance, housing, education, or public services;
- trigger high-impact outreach or escalation;
- rely on leaked, private, or unlawfully obtained information.

## 11. Profile lifecycle

```text
DRAFT
→ GENERATED_CANDIDATE
→ LEXICAL_REVIEW
→ DOMAIN_REVIEW
→ SOURCE_REVIEW
→ LOCALE_REVIEW
→ COMPLIANCE_REVIEW where required
→ BENCHMARK_READY
→ TESTED
→ APPROVED
→ ACTIVE
→ SUPERSEDED / REVOKED
→ ARCHIVED
```

Generated candidates may be stored, inspected, and tested. They must not become active merely because a script produced them without crashing.

## 12. Minimum profile record

```text
id
code
name
profile_type
canonical_concept_id
provider_offering_id nullable
sector_ids
domain_ids
activity_ids
signal_ids
language
locale
precision_mode
terms and semantic seeds
match and proximity rules
organization and source requirements
exclusions and contradictions
freshness policy
evidence threshold
sensitive-sector policy
review status
version
valid_from
valid_until
supersedes_profile_id
created_by
reviewed_by
approved_by
rollback_reference
```

## 13. Acceptance criteria

A profile may be called **approved** only when:

- its canonical purpose is unambiguous;
- every term has a type and precision tier;
- broad terms have context rules;
- acronyms have ambiguity rules;
- required co-occurrence and proximity are defined;
- exclusions and contradictions are tested;
- source suitability is defined;
- freshness and event dates are handled;
- sensitive-sector risks are reviewed;
- locale terms are human-reviewed;
- positive, negative, ambiguous, and source-specific benchmarks pass;
- duplicate overlap is assessed;
- the latest version is traceable and reversible;
- no keyword match can bypass offering eligibility, entity resolution, evidence review, or contact policy.

## 14. Delivery boundary

This is a normative documentation standard. It does not implement storage, query generation, embeddings, classifiers, evidence scoring, approval workflows, or production profiles.
