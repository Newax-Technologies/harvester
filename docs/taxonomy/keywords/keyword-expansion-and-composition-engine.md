# Harvester Keyword Expansion and Composition Engine

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document defines how Harvester should turn the controlled domain, activity, signal, role, geography, source, exclusion, and locale registries into deep but bounded query and classification plans.

The engine must create depth through controlled composition, not by copying thousands of uncontrolled phrases into one flat list.

## 1. Inputs

```text
Selected sector
Selected domain
Approved domain-specific activity
Active provider offering
Approved signal profiles
Geographic and organization-size scope
Permitted source classes
Language and locale packs
Precision mode
Evidence and contact policies
```

## 2. Composable packs

| Pack family | Examples |
| --- | --- |
| Domain identity | pharmaceutical; medicine; pharma |
| Organization archetype | manufacturer; distributor; clinic; operator |
| Activity | manufacturing; importing; warehousing; selling |
| Facility and asset | plant; warehouse; branch; fleet; laboratory |
| Process | batch release; order fulfilment; patient intake |
| Event | expansion; tender; hiring; renewal; maintenance due |
| Problem | manual entry; delayed reporting; stock mismatch |
| Existing solution | ERP; EMR; legacy platform; current vendor |
| Role | operations head; procurement manager; IT director |
| Contact route | supplier registration; procurement portal; official inquiry |
| Geography | country; province; city; district; industrial estate |
| Source | registry category; website heading; tender field; job title |
| Negative | jobs only; course; definition; cancelled; awarded; closed |
| Locale | English; Urdu; Roman Urdu; reviewed local trade terms |

## 3. Query generation sequence

```text
1. Resolve eligible domain profile
2. Resolve approved activities for that domain
3. Resolve active provider offering and eligible signal profiles
4. Select source class and its permitted query family
5. Select precision mode and query budget
6. Generate high-precision identity queries
7. Generate activity-confirmation queries
8. Generate event, intent, pain, technology, role, and contact queries only after gates
9. Generate negative and contradiction queries
10. Deduplicate equivalent queries
11. Rank by expected information gain and source cost
12. Execute within source policy and rate limits
13. Preserve every component and profile version with the result
```

## 4. Precision modes

### `HIGH_PRECISION`

Use when false positives are expensive, the sector is sensitive, or outreach preparation is near.

- exact and reviewed high-precision aliases;
- organization or structured category requirement;
- approved activity co-occurrence;
- authoritative or first-party sources preferred;
- narrow geography only when required;
- semantic expansion disabled or low-weight;
- negative query mandatory.

### `BALANCED`

Default mode for broad research.

- exact, high-precision, and contextual aliases;
- one corroborating organization, activity, or source cue;
- limited semantic expansion;
- multiple source classes;
- negative and verification queries for material candidates.

### `BROAD`

Used only for vocabulary discovery, early market mapping, and candidate recall.

- broader parent and semantic terms;
- larger query budget;
- results remain research candidates;
- no contact-ready state;
- no service-gap conclusion;
- mandatory downstream precision pass.

## 5. Query families and templates

```text
IDENTITY:
  <domain_exact> + <organization_cue> + <optional_geography>

ACTIVITY:
  <resolved_entity> + <approved_activity_alias>

FACILITY:
  <resolved_entity_or_domain> + <facility_or_asset_cue> + <activity>

TRIGGER:
  <entity_or_domain> + <business_event> + <date_or_geography>

PROCUREMENT:
  <domain_or_offering_context> + <RFP/RFQ/tender/EOI> + <authority_or_location>

PAIN:
  <entity_or_domain> + <offering-specific_problem_signal>

TECHNOLOGY:
  <entity> + <software/device/vendor/integration cue>

ROLE:
  <entity> + <responsible_function>

CONTACT:
  <entity> + <lawful_official_route>

NEGATIVE:
  <entity_or_event> + <cancelled/awarded/closed/superseded/do-not-contact>

VERIFY:
  <exact_entity> + <exact_claim> + <authoritative_source_constraint>
```

## 6. Domain–activity multiplication control

Selecting several domains and activities can create hundreds of combinations. The engine must not blindly generate the Cartesian product.

It must use the approved `DomainActivityAssignment` records:

```text
Selected domains
× only approved activities for each domain
× only active provider offerings applicable to that combination
× only approved signals for that offering
```

Every generated plan must retain the exact domain–activity combination that authorized it.

## 7. Query budget

A source plan must define:

- maximum queries per source;
- maximum semantic expansions;
- maximum role and contact queries per organization;
- stopping conditions;
- duplicate-yield threshold;
- acceptable cost per verified candidate;
- minimum evidence gain before continuing;
- cooldown and rate-limit policy.

Suggested stopping rules include:

- authoritative identity and activity evidence found;
- the candidate is disqualified or closed;
- additional queries return only duplicate origins;
- source coverage is exhausted;
- query budget is reached;
- confidence cannot improve without a different source class;
- contact investigation is not policy-eligible.

## 8. Deduplication

Deduplicate at four levels:

1. equivalent query strings;
2. normalized URLs and mirrored pages;
3. copied evidence origins such as syndicated press releases;
4. resolved organizations and branches.

Repeated aliases on the same page are one evidence item, not several votes.

## 9. Semantic expansion

Semantic retrieval may use:

- canonical concept description;
- parent and child concepts;
- operational process descriptions;
- approved activity descriptions;
- reviewed positive examples;
- sector-specific vocabulary;
- locale-aware embeddings where validated.

Semantic results must retain:

- originating canonical profile;
- similarity score;
- model and embedding version;
- source text;
- explanation or nearest reviewed seed;
- precision tier;
- human-review state.

Semantic similarity alone cannot prove an activity or opportunity.

## 10. Dynamic geography

Geography is an independent layer. Do not permanently duplicate every keyword for every city.

```text
canonical phrase
+ country/province/city/district/site/service-area selector
```

The engine should understand:

- organization headquarters versus operating locations;
- branch, facility, project, route, and service-area relevance;
- local-language place variants;
- geocoding confidence;
- remote or national service availability;
- cross-border delivery restrictions.

## 11. Variant generation rules

Permitted automatic candidates, subject to review:

- punctuation and ampersand variants;
- British and American spelling pairs;
- reviewed singular and plural forms;
- hyphenation variants;
- case-insensitive acronym forms;
- legal suffix and organization-name normalization;
- common transliteration variants from approved locale packs.

Prohibited automatic generation:

- blind stemming;
- arbitrary suffix removal;
- uncontrolled substring replacement;
- machine translation activated without review;
- every possible typo;
- acronyms without ambiguity controls;
- generic buzzword expansion.

## 12. Evidence output

Every executed query should produce a structured `QueryExecutionRecord` containing:

```text
query_family
composed_query
component_profile_ids and versions
source class and adapter version
precision mode
geography and language
execution time and cost
result identifiers
accepted, rejected, duplicate, and contradictory evidence counts
stopping reason
```

## 13. Acceptance criteria

- No query is generated without an eligible domain and approved activity context.
- Offering-specific signals require an active provider offering.
- Query families are separate and explainable.
- Broad mode cannot produce contact-ready leads.
- Negative and verification plans accompany material positive opportunities.
- Geography and locale remain compositional rather than copied into every canonical profile.
- Query budgets and stopping rules prevent uncontrolled source consumption.
- Every result retains the profiles and versions that produced it.
- Runtime implementation is not falsely claimed.
