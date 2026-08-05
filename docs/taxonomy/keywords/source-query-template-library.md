# Harvester Source Query Template Library

Status: **Proposed**  
Version: **2.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This library defines the shared query-composition contract used by the fourteen separate [Harvester source specifications](sources/README.md).

It does not authorize scraping, access-control bypass, private-data collection, provider-term violations, or source usage outside an approved adapter and authorization profile.

Read with the [Raw Source Response Preservation Standard](sources/raw-source-response-preservation-standard.md), which separates minimal source requests from long-term preservation of the responses actually returned.

## 1. General rule

A source adapter must translate canonical keyword profiles into the exact fields, filters, syntax, request limits, and authorization modes supported by that source.

It must request only the fields and records required for the approved purpose. It must not request every available field for possible future use.

```text
Canonical profile
→ source-specific composition
→ minimum required field mask or mapping
→ bounded source execution
→ immutable permitted raw response snapshot
→ contextual evidence candidate
→ source, entity, freshness, duplication and contradiction review
```

Every source is different. A registry identifier lookup, a map text search, an official-site crawl, a tender filter, a CRM import mapping, and an inbound inquiry extraction are not interchangeable query types.

## 2. Separate source specifications

| Source code | Source specification |
| --- | --- |
| `SRC-WEB` | [Organization Websites](sources/organization-websites.md) |
| `SRC-REG` | [Government and Professional Registries](sources/government-professional-registries.md) |
| `SRC-PROC` | [Procurement and Tender Portals](sources/procurement-tender-portals.md) |
| `SRC-JOBS` | [Job Boards and Careers Pages](sources/job-boards-careers-pages.md) |
| `SRC-PROF` | [Authorized Professional Networks](sources/authorized-professional-networks.md) |
| `SRC-NEWS` | [News and Media](sources/news-media.md) |
| `SRC-MAPS` | [Maps and Business Listings](sources/maps-business-listings.md) |
| `SRC-DIR` | [Business Directories](sources/business-directories.md) |
| `SRC-SOCIAL` | [Social Platforms](sources/social-platforms.md) |
| `SRC-TECH` | [App Marketplaces and Technology Directories](sources/app-marketplaces-technology-directories.md) |
| `SRC-REPORT` | [Company Reports and Investor Publications](sources/company-reports-investor-publications.md) |
| `SRC-CERT` | [Certification and Accreditation Sources](sources/certification-accreditation-sources.md) |
| `SRC-IMPORT` | [Manual Authorized Imports](sources/manual-authorized-imports.md) |
| `SRC-DIRECT` | [Direct Inquiries and Referrals](sources/direct-inquiries-referrals.md) |

The individual source files define admissible fields, signal strengths, weaknesses, provenance, freshness, duplication, privacy, failure states, and acceptance criteria.

## 3. Required query families

A source adapter may support only the families that fit its interface.

### 3.1 Identity

Purpose:

- discover or verify an organization, branch, facility, product, service, or regulated record;
- map source-native categories to candidate Harvester domains;
- resolve aliases, legal names, brands, and identifiers.

```text
<domain identity>
+ <organization cue>
+ <geography or identifier>
```

### 3.2 Activity

Purpose:

- discover evidence that a resolved target performs an approved activity inside a selected domain.

```text
<resolved target>
+ <selected domain>
+ <approved activity>
+ <supporting process, output, facility, equipment, or role cue>
```

An activity match for one domain never activates that activity for another domain.

### 3.3 Precision

Use exact phrases, stable identifiers, reviewed aliases, classification codes, and required co-occurrence to reduce false positives.

```text
<exact or high-precision term>
+ <required context>
- <known ambiguity>
```

### 3.4 Recall

Use reviewed aliases, abbreviations, local terminology, transliteration, semantic seeds, and source-native categories within source, query-budget, geography, precision-tier, negative-context, and review controls.

### 3.5 Entity verification

```text
<name or identifier>
+ <address/domain/phone/registry/location relationship>
```

### 3.6 Event

```text
<resolved entity>
+ <event profile>
+ <date or geography context>
```

Event date and publication date remain separate.

### 3.7 Procurement

```text
<offering or capability>
+ <tender/RFP/RFQ/EOI/procurement vocabulary>
+ <buyer, geography, or category>
```

Every positive procurement query must be paired with amendment, extension, cancellation, award, completion, and expiry checks.

### 3.8 Technology and existing solution

```text
<resolved entity>
+ <technology or existing-solution profile>
+ <official or source-supported context>
```

Technology presence does not prove adoption, satisfaction, replacement intent, or absence of alternatives.

### 3.9 Role and contact route

```text
<resolved organization>
+ <responsible function>
+ <official or authorized contact-route cue>
```

A title does not prove authority. A public route does not create consent.

### 3.10 Negative and contradiction

Common logical terms include:

```text
cancelled
awarded
completed
closed
expired
suspended
revoked
withdrawn
moved
renamed
merged
superseded
deprecated
discontinued
corrected
denied
filled
delisted
do not contact
no longer employed
```

Terms must be interpreted in context. `Closed for Eid` is not dissolution, because sentences remain inconveniently important.

## 4. Composition layers

```text
sector
+ domain identity
+ approved domain-specific activity
+ organization cues
+ geography
+ language and locale
+ source overlay
+ active provider-offering signals
+ negative and contradiction controls
```

Optional layers may include entity identifiers, facility and equipment cues, classification codes, event windows, role groups, contact-route profiles, source-native categories, semantic expansion, proximity, and co-occurrence constraints.

## 5. Offering isolation

The following profiles are ineligible unless an active provider offering is selected and mapped to the target domain and activity:

- buying and procurement intent;
- operational pain;
- replacement and migration;
- integration and competitor;
- existing solution and technology gap;
- maintenance and expansion;
- budget or funding;
- service-gap hypothesis.

A domain keyword cannot quietly become a sales claim merely because it appeared near the word `system`.

## 6. Match, field and filter controls

Every generated query or mapping must preserve:

- source class, source mode, adapter version, and authorization state;
- query family and contributing profile versions;
- keyword type, precision tier, language, locale, and match mode;
- geography and date window;
- positive, negative, and contradiction inputs;
- field mask, projection, selected attributes, or schema-mapping version;
- query budget, page and record limits, stopping rule, and source limitations;
- retention-policy and source-policy versions.

Supported match modes remain:

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

A source may support only a subset.

## 7. Source-specific execution rules

1. Use only fields and syntax supported by the source.
2. Request only fields and records required for the approved source purpose.
3. Do not request all available fields merely because the source exposes them.
4. Version every field mask, projection, mapping, date range, geography, page limit, and enrichment profile.
5. Do not manufacture operators for a source that does not support them.
6. Do not convert an import mapping or direct inquiry into a public-search query.
7. Do not expand collection because a keyword profile contains an interesting term.
8. Source authorization, contract, provider policy, privacy, rate limits, and retention rules override query breadth and raw preservation.
9. Preserve the complete returned response as an immutable raw snapshot where the applicable policy permits it.
10. Preserve successful, empty, partial, failed, paginated, warning, rate-limit, retry, and provider-error outcomes separately where permitted.
11. Default permitted raw responses to indefinite archival; apply stricter source-specific deletion or time limits when required.
12. Store source non-return separately from source failure.
13. Preserve event, effective, expiry, publication, collection, and verification dates separately.
14. Run negative and contradiction checks for material opportunities.
15. Detect duplicate origins before counting evidence diversity.
16. Preserve the exact request, query, field-mask, profile, adapter, source-policy, and retention-policy versions used by completed Harvest Jobs.

## 8. Query preview requirements

Before activation, an authorized operator must be able to review:

- source and query family;
- rendered query or field mapping;
- requested fields, field mask, projection, page scope, record scope, and enrichment stage;
- contributing domain, activity, offering, locale, and source profiles;
- positive, negative, blocked, and unsupported terms;
- estimated breadth, cost, storage, retention, privacy, and rate-limit effect where available;
- bounded samples, policy warnings, and approval state.

Preview does not authorize execution.

## 9. Evidence handoff

A query result becomes an evidence candidate only after creating or referencing the permitted immutable raw source-response snapshot and preserving:

- raw snapshot identifier and checksum;
- source and source-native identifier;
- exact request, query, field mask, or mapping;
- matched field or text and surrounding context;
- entity candidate, language, and locale;
- event and collection times;
- source suitability, duplication, negative, and contradiction states;
- profile, adapter, source-policy, and retention-policy versions.

Raw response preservation does not make every returned field verified evidence. Entity resolution, domain/activity assessment, opportunity analysis, qualification, and contact policy remain separate decisions.

## 10. Acceptance criteria

- All fourteen source classes have separate specifications.
- Every source uses only required supported fields, modes, syntax, and authorization.
- Field masks, projections, mappings, page limits, and enrichment stages are versioned.
- Query families remain distinguishable.
- Complete permitted returned responses are preserved without broadening the request.
- Permitted raw responses are immutable and indefinite by default.
- Provider, legal, contractual, privacy, consent, and deletion requirements override indefinite retention.
- Domain, activity, organization, offering, locale, source, and negative controls retain provenance.
- Offering-specific sales signals cannot activate without an active provider offering.
- Positive queries are paired with appropriate negative and contradiction checks.
- Non-detection is not treated as universal absence.
- Duplicate origins do not inflate evidence diversity.
- Query preview is required before activation.
- Runtime implementation is not falsely claimed.

## 11. Delivery boundary

This library and the individual source specifications are repository-integrated documentation after merge. They do not implement adapters, credentials, query rendering, source execution, request minimization, raw-response storage, retention enforcement, deletion workflows, evidence resolution, scoring, approval, contact workflows, or releases.
