# Harvester Source-to-Signal Matrix

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This matrix compares the fourteen approved source classes. Each source has its own fully formatted specification under [`sources/`](sources/README.md).

A source adapter may collect only what its authorization, provider policy, contract, documented interface, and approved purpose permit.

## 1. Source comparison

| Code | Source class | Strong signal uses | Secondary uses | Principal weaknesses |
| --- | --- | --- | --- | --- |
| `SRC-WEB` | [Organization Websites](sources/organization-websites.md) | First-party identity, offerings, facilities, locations, official documents, and public routes | Operational language, partners, public leadership, and expansion | Marketing bias, stale pages, and silence is not absence |
| `SRC-REG` | [Government and Professional Registries](sources/government-professional-registries.md) | Legal identity, registration, licence, regulated category, status, and dates | Renewal, status, and governed relationship changes | Limited operational detail and possible update delay |
| `SRC-PROC` | [Procurement and Tender Portals](sources/procurement-tender-portals.md) | Dated purchase notice, scope, buyer, deadline, eligibility, and status | Specifications, disclosed value, and procurement function | Amendment, cancellation, award, and expiry change quickly |
| `SRC-JOBS` | [Job Boards and Careers Pages](sources/job-boards-careers-pages.md) | Vacancy, role, location, hiring, and stated responsibilities | Expansion, technology, implementation, and ownership cues | Does not prove external budget or purchase intent |
| `SRC-PROF` | [Authorized Professional Networks](sources/authorized-professional-networks.md) | Authorized current role, affiliation, and approved organization data | Functional-owner cues, growth, partnerships, and hiring | Access restrictions, self-reporting, and title is not authority |
| `SRC-NEWS` | [News and Media](sources/news-media.md) | Dated launch, expansion, funding, acquisition, award, action, or incident | Strategic priorities and executive changes | Syndication, speculation, and event-date ambiguity |
| `SRC-MAPS` | [Maps and Business Listings](sources/maps-business-listings.md) | Place, branch, location, provider category, status, and public route | Branch count, local presence, and independent research seed | User edits, duplicates, provider limits, and non-return ambiguity |
| `SRC-DIR` | [Business Directories](sources/business-directories.md) | Directory identity, category, location, public route, and governed relationships | Supplier, distributor, and association discovery | Stale, copied, user-submitted, or reseller records |
| `SRC-SOCIAL` | [Social Platforms](sources/social-platforms.md) | Official or authorized announcement, service update, and public route | Recruitment, events, campaigns, product, and facility signals | Informal language, impersonation, comments, and platform limits |
| `SRC-TECH` | [App Marketplaces and Technology Directories](sources/app-marketplaces-technology-directories.md) | Product, vendor, listing, integration, documentation, and support status | Existing-solution, partner, migration, and upgrade context | Presence does not prove adoption or replacement intent |
| `SRC-REPORT` | [Company Reports and Investor Publications](sources/company-reports-investor-publications.md) | Formal strategy, period, scale, projects, governance, and disclosed risk | Technology and operational priorities | Reporting lag, selective disclosure, and forward-looking statements |
| `SRC-CERT` | [Certification and Accreditation Sources](sources/certification-accreditation-sources.md) | Standard, certificate, scope, status, and validity | Facility, product, quality, and compliance context | Does not prove operational effectiveness or demand |
| `SRC-IMPORT` | [Manual Authorized Imports](sources/manual-authorized-imports.md) | Customer-owned records, consent, suppression, known accounts, and relationship context | Verification, enrichment, and internal aliases | Quality, age, lawful-use basis, and free-text reliability vary |
| `SRC-DIRECT` | [Direct Inquiries and Referrals](sources/direct-inquiries-referrals.md) | Expressed need, scope, urgency, and interaction-specific permission | Qualification, routing, buying stage, and constraints | Identity, authority, fit, and continuing permission still require verification |

## 2. Signal suitability matrix

Legend:

- **Strong**: the source may directly support the signal when the exact record and source policy permit it.
- **Supporting**: the source may corroborate or contextualize the signal.
- **Weak**: the source is normally insufficient without stronger evidence.
- **Not applicable**: the source should not be used for that signal.

| Source | Identity | Domain/activity | Event | Procurement intent | Technology/existing solution | Role/function | Contact permission |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SRC-WEB` | Strong | Strong or supporting | Strong or supporting | Supporting | Supporting | Supporting | Weak |
| `SRC-REG` | Strong | Supporting | Supporting | Weak | Not applicable | Weak or supporting | Not applicable |
| `SRC-PROC` | Strong for buyer and notice | Strong for notice scope | Strong | Strong | Supporting | Supporting | Route-specific only |
| `SRC-JOBS` | Strong for listing and entity | Supporting | Strong for hiring | Weak | Supporting | Strong or supporting | Not applicable |
| `SRC-PROF` | Strong when authorized | Supporting | Supporting | Weak | Weak or supporting | Strong or supporting | Weak and policy-bound |
| `SRC-NEWS` | Strong or supporting | Supporting | Strong | Supporting | Supporting | Supporting | Not applicable |
| `SRC-MAPS` | Strong for place | Supporting | Supporting | Not applicable | Not applicable | Weak | Weak |
| `SRC-DIR` | Supporting | Supporting | Weak | Weak | Weak | Weak | Weak |
| `SRC-SOCIAL` | Supporting | Supporting | Strong or supporting | Weak or supporting | Supporting | Weak or supporting | Weak and route-specific |
| `SRC-TECH` | Strong for product and vendor | Supporting | Strong for release or deprecation | Weak | Strong or supporting | Weak | Not applicable |
| `SRC-REPORT` | Strong | Supporting | Strong or supporting | Supporting | Supporting | Supporting | Not applicable |
| `SRC-CERT` | Strong for certificate and entity | Supporting | Strong for status | Weak | Weak | Weak | Not applicable |
| `SRC-IMPORT` | Source-dependent | Source-dependent | Source-dependent | Source-dependent | Source-dependent | Source-dependent | Strong only when documented |
| `SRC-DIRECT` | Strong after verification | Strong or supporting | Strong for interaction | Strong or supporting | Strong or supporting | Strong or supporting | Strong only within recorded scope |

The matrix guides source planning. It does not replace source-specific inspection or evidence thresholds.

## 3. Recommended source combinations

| Objective | Preferred source combination |
| --- | --- |
| New legal entity or regulated facility | `SRC-REG` + `SRC-WEB` + `SRC-MAPS` where relevant |
| New branch or customer-facing location | `SRC-WEB` + `SRC-MAPS` + `SRC-REG` or `SRC-NEWS` where available |
| Active procurement | `SRC-PROC` + buyer `SRC-WEB` + amendment, cancellation, and award monitoring |
| Expansion | `SRC-WEB` or `SRC-NEWS` + `SRC-JOBS` + location or registry corroboration |
| Existing technology | `SRC-TECH` + official `SRC-WEB` or `SRC-REPORT` + independent technical evidence |
| Technology replacement | Direct or procurement evidence + `SRC-TECH` context + responsible-function evidence |
| Operational pain | `SRC-DIRECT` or an explicit first-party statement + process evidence + a second source |
| Certification or regulated scope | `SRC-CERT` + `SRC-REG` + organization website context |
| Decision-function resolution | Official organization source + authorized professional source |
| Contact-ready lead | Supported opportunity + current lawful route + suppression, conflict, consent, and channel checks |
| Customer-owned enrichment | `SRC-IMPORT` + authoritative identity sources + row-level provenance |
| Referral opportunity | `SRC-DIRECT` + organization verification + authority and permission review |

## 4. Source selection rules

1. Use the highest-authority source reasonably available for the exact claim.
2. Match the source to the signal; general source reputation does not make every field authoritative.
3. Preserve source-native identifiers and classifications before mapping.
4. Preserve event, effective, expiry, publication, collection, and verification dates separately.
5. Detect copied content, syndication, mirrors, reposts, directory replication, and repeated imports as shared origins.
6. Source failure, access denial, or non-return reduces coverage; it does not prove absence.
7. Procurement evidence must track amendments, extensions, cancellations, awards, completion, and deadlines.
8. Role and contact data must be current enough for the approved contact policy.
9. Public contact information does not override suppression, conflict, consent, jurisdiction, or route rules.
10. Sensitive personal data is excluded unless explicitly authorized, necessary, and governed.
11. Provider-specific source models override this generic matrix where stricter.
12. Completed Harvest Jobs preserve source-policy, adapter, query, profile, evidence, and contact-policy versions.

## 5. Evidence-state separation

Every source adapter must distinguish at least:

```text
DETECTED
NOT_DETECTED
SOURCE_UNAVAILABLE
ACCESS_RESTRICTED
INSPECTION_FAILED
STALE
CONTRADICTED
SUPERSEDED
```

Additional states are defined in the individual source specifications.

Confirmed absence requires the applicable coverage and evidence process. It cannot be created merely by substituting confidence for missing evidence.

## 6. Acceptance criteria

- All fourteen source classes link to separate specifications.
- Strong, supporting, weak, and not-applicable uses remain distinguishable.
- Source authority and signal relevance remain separate dimensions.
- Provider-specific rules override generic guidance.
- Duplicate origins do not inflate corroboration.
- Direct inquiry and authorized import remain separate from public discovery.
- Contact permission remains separate from public route availability.
- Non-detection is not treated as absence.
- Runtime implementation is not falsely claimed.

## 7. Delivery boundary

This matrix and the linked source specifications are documentation standards. They do not implement source adapters, credentials, collection, query execution, storage, evidence resolution, scoring, approval, contact workflows, or releases.
