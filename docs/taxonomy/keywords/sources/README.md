# Harvester Source Specification Index

Status: **Proposed**  
Version: **2.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This directory separates every approved Harvester source class into its own governed Markdown specification.

The split is intentional. Organization websites, government registries, procurement notices, job listings, professional networks, news, maps, directories, social platforms, technology catalogues, formal company reports, certification sources, authorized imports, and direct inquiries have different fields, authority, freshness, access rules, weaknesses, and legal boundaries. Treating them as one generic search source would be convenient in precisely the way that creates unreliable evidence.

## 1. Source registry

| Source code | Source class | Specification | Primary evidentiary use |
| --- | --- | --- | --- |
| `SRC-WEB` | Organization Websites | [organization-websites.md](organization-websites.md) | Official organization name and self-description. |
| `SRC-REG` | Government and Professional Registries | [government-professional-registries.md](government-professional-registries.md) | Legal or registered name. |
| `SRC-PROC` | Procurement and Tender Portals | [procurement-tender-portals.md](procurement-tender-portals.md) | Active purchase intent tied to a notice. |
| `SRC-JOBS` | Job Boards and Careers Pages | [job-boards-careers-pages.md](job-boards-careers-pages.md) | A published vacancy, role, location, department, and stated responsibilities. |
| `SRC-PROF` | Authorized Professional Networks | [authorized-professional-networks.md](authorized-professional-networks.md) | Authorized current organization and role fields. |
| `SRC-NEWS` | News and Media | [news-media.md](news-media.md) | A dated event reported by a credible origin or confirmed by an official source. |
| `SRC-MAPS` | Maps and Business Listings | [maps-business-listings.md](maps-business-listings.md) | Provider-specific place identifier, name, location, branch, category, operating status, and official website path where returned. |
| `SRC-DIR` | Business Directories | [business-directories.md](business-directories.md) | A directory record exists with a named organization, category, location, website, or public contact route. |
| `SRC-SOCIAL` | Social Platforms | [social-platforms.md](social-platforms.md) | An announcement or service update from a verified or independently resolved official organization account. |
| `SRC-TECH` | App Marketplaces and Technology Directories | [app-marketplaces-technology-directories.md](app-marketplaces-technology-directories.md) | A vendor, product, integration, listing, supported region, category, or official partner relationship. |
| `SRC-REPORT` | Company Reports and Investor Publications | [company-reports-investor-publications.md](company-reports-investor-publications.md) | Formal organization identity, reporting period, governance, strategy, disclosed projects, scale, and officially stated risks. |
| `SRC-CERT` | Certification and Accreditation Sources | [certification-accreditation-sources.md](certification-accreditation-sources.md) | Certificate or accreditation identifier. |
| `SRC-IMPORT` | Manual Authorized Imports | [manual-authorized-imports.md](manual-authorized-imports.md) | Customer-owned account context, known organization relationships, prior interactions, consent, suppression, referral, and operational notes when properly authorized. |
| `SRC-DIRECT` | Direct Inquiries and Referrals | [direct-inquiries-referrals.md](direct-inquiries-referrals.md) | Expressed need, problem, objective, urgency, requested scope, preferred route, and contact permission within the stated interaction. |

## 2. Shared source contract

Every source specification uses the same top-level structure:

1. Purpose.
2. Approved source boundary.
3. Strong signal uses.
4. Secondary signal uses.
5. Weak, unsupported, or prohibited inferences.
6. Source fields and evidence targets.
7. Keyword and query inputs.
8. Governed query or mapping templates.
9. Inspection sequence.
10. Required provenance.
11. Freshness and event time.
12. Duplication and corroboration.
13. Privacy, authorization, and compliance.
14. Non-detection and failure states.
15. Acceptance criteria.
16. Related documents.
17. Delivery boundary.

Shared structure does not mean shared behavior. Every source has an independent collection boundary and evidentiary role.

All source classes additionally inherit the [Raw Source Response Preservation Standard](raw-source-response-preservation-standard.md).

## 3. Locked rules

1. Source authorization and provider policy override keyword configuration and generic retention defaults.
2. A source request must ask only for the fields, records, pages, dates, geography, and enrichment required for the approved purpose.
3. Field masks, projections, schema mappings, and request profiles must be versioned.
4. Harvester must not request every available field merely for possible future use.
5. Where retention is permitted, Harvester preserves the complete response actually returned as an immutable raw snapshot, including successful, empty, partial, failed, paginated, and retry outcomes.
6. Permitted raw responses are retained indefinitely by default for audit, reproducibility, historical comparison, and future reprocessing.
7. Law, binding legal process, provider terms, API policy, licence, contract, privacy, consent, deletion obligations, and stricter source-specific profiles override indefinite retention.
8. Mandatory deletion should leave a non-reconstructive audit tombstone where permitted.
9. Raw response preservation does not make every returned field verified, canonical, scoreable, publishable, contactable, or eligible for every future purpose.
10. A source adapter may collect only fields and records supported by its documented interface and approved authorization.
11. Domain and activity keywords support identity and activity evidence; they do not prove an opportunity.
12. Offering-specific problem, intent, replacement, integration, competitor, existing-solution, procurement, and gap terms require an active provider offering.
13. Source authority and signal relevance are separate dimensions.
14. Publication date, event date, effective date, expiry date, collection date, and last verification date remain separate where applicable.
15. `NOT_DETECTED`, unavailable, restricted, failed, stale, contradicted, and confirmed absence are separate states.
16. Copied pages, syndicated articles, mirrored notices, repeated directory records, cross-posts, and repeated imports do not inflate source diversity.
17. Decision-role resolution begins only after organization resolution.
18. A role title does not prove authority.
19. A public contact route does not create consent or override suppression, conflict, procurement, jurisdiction, or channel policy.
20. Sensitive or private data cannot be inferred from weak public signals.
21. Completed Harvest Jobs preserve the source-class, adapter, request, query, field-mask, keyword-profile, evidence-policy, classifier, retention-policy, and contact-policy versions used.
22. These specifications define documentation datasets and controls; they do not claim runtime implementation.

## 4. Provider-specific source models

These source-class specifications remain subordinate to any stricter provider-specific model:

- [Google API Source and Extraction Model](../../../sources/google-api-source-model.md).
- [Yandex Maps API Source and Extraction Model](../../../sources/yandex-maps-api-source-model.md).
- [LinkedIn Authorized Data Source Model](../../../sources/linkedin-authorized-data-source-model.md).
- [User Input Storage Model](../../../sources/user-input-storage-model.md).

## 5. Cross-source controls

- [Raw Source Response Preservation Standard](raw-source-response-preservation-standard.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).
- [Query Composition and Evidence Rules](../query-composition-and-evidence-rules.md).
- [Ultimate Keyword Profile Standard](../ultimate-keyword-profile-standard.md).
- [Keyword Validation Plan](../keyword-validation-plan.md).

## 6. Delivery boundary

The source specifications are documentation standards. Credentials, adapters, source execution, request minimization, data storage, retention enforcement, audit tombstones, evidence resolution, classifiers, scoring, approval, and contact workflows remain separate implementation work.
