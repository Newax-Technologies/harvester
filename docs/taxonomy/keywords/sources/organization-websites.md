# Harvester Source Specification: Organization Websites

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-WEB`**

## 1. Purpose

Use an organization's own public web properties to establish self-identified identity, offerings, facilities, locations, public leadership, operating context, official documents, and lawful contact routes.

This document defines how keyword profiles may be composed for this source, which signals the source may support, which inferences remain weak or prohibited, and what evidence must be retained. It does not authorize access that the source, provider, contract, law, or customer has not permitted.

## 2. Approved source boundary

- Official corporate, institutional, subsidiary, branch, product, service, careers, newsroom, procurement, documentation, and contact pages.
- Public files intentionally published by the organization, including brochures, catalogues, policies, certifications, annual reports, and technical documentation.
- Only public pages and files that the source policy and crawler rules permit Harvester to inspect.

## 3. Strong signal uses

- Official organization name and self-description.
- Products, services, facilities, locations, branches, and operating scope.
- Official public contact routes and responsible functions.
- Public announcements, case studies, certifications, policies, and procurement notices.
- First-party technology, integration, implementation, or support statements.

## 4. Secondary signal uses

- Operational terminology and process language.
- Partner, distributor, reseller, or implementation ecosystem.
- Public leadership and department names.
- Expansion, hiring, project, or facility signals.

## 5. Weak, unsupported, or prohibited inferences

- Marketing claims do not independently prove operational capability.
- Missing content does not prove absence.
- An outdated page may not represent current operations.
- Parent, subsidiary, branch, and brand pages may be mixed.
- A technology mention does not prove current deployment, satisfaction, or replacement intent.

## 6. Source fields and evidence targets

- canonical URL and final resolved URL
- page title, headings, metadata, and structured data
- organization name, brand, branch, and location references
- product, service, facility, activity, event, role, and contact phrases
- publication, effective, expiry, and last-modified dates where available
- document type, checksum, language, and source location

A source adapter may collect only fields supported by its documented interface and approved authorization. A keyword profile cannot expand the adapter's legal or technical collection boundary.

## 7. Keyword and query inputs

- selected domain identity terms and reviewed aliases
- approved domain-specific activities
- active provider-offering problem, intent, technology, event, and contradiction profiles
- organization, facility, geography, role, and contact-route cues
- negative terms such as closed, discontinued, expired, superseded, cancelled, or no longer offered

Domain identity, activity identity, organization cues, and source context may support discovery. Offering-specific problem, intent, replacement, integration, competitor, existing-solution, procurement, or gap terms require an active provider offering.

## 8. Governed query or mapping templates

```text
site:<official-domain> <domain identity phrase>
site:<official-domain> <approved activity phrase>
site:<official-domain> <offering-specific problem or intent phrase>
site:<official-domain> <facility, location, procurement, hiring, or event phrase>
site:<official-domain> <responsible function or official contact route>
site:<official-domain> <negative or contradiction phrase>
```

Templates are logical patterns. The source adapter must translate them into the exact fields, filters, syntax, and request limits supported by that source.

## 9. Inspection sequence

1. Resolve the official domain and organization relationship before broad crawling.
2. Inspect high-value navigation targets first: About, Products, Services, Facilities, Locations, Careers, News, Procurement, Contact, policies, and public files.
3. Extract evidence with page and section context rather than storing isolated keyword hits.
4. Separate first-party claims from independently verified facts.
5. Run negative and contradiction checks before a material opportunity is supported.

## 10. Required provenance

- source class and adapter version
- requested URL, final URL, page title, section, and retrieval time
- published, effective, expiry, and event dates where present
- matched profile, keyword type, precision tier, and surrounding context
- content checksum, language, parser version, and retention policy

Every material match must retain the originating domain, activity, organization, offering, signal, source, language, locale, match mode, precision tier, and profile version.

## 11. Freshness and event time

Website evidence is page- and claim-specific. Event, policy, certification, product, service, leadership, and contact claims require their own freshness assessment rather than one universal website age.

Collection time, publication time, effective time, event time, expiry time, and last verification time remain separate fields where applicable.

## 12. Duplication and corroboration

Mirrors, translated copies, repeated navigation text, syndicated announcements, cached copies, and copied brochures must resolve to one evidence origin where appropriate.

Duplicate copies never create independent evidence diversity.

## 13. Privacy, authorization, and compliance

- Respect robots, access controls, rate limits, copyright, privacy, and source-specific retention rules.
- Do not bypass authentication, paywalls, anti-bot controls, or unpublished endpoints.
- Public contact information does not create consent or override suppression and channel policy.

Source authorization and policy override keyword ambition.

## 14. Non-detection and failure states

- `WEBSITE_PAGE_DETECTED`
- `WEBSITE_PAGE_NOT_DETECTED`
- `WEBSITE_SOURCE_UNAVAILABLE`
- `WEBSITE_ACCESS_RESTRICTED`
- `WEBSITE_INSPECTION_FAILED`
- `WEBSITE_EVIDENCE_STALE`
- `WEBSITE_EVIDENCE_CONTRADICTED`

`NOT_DETECTED`, access failure, parsing failure, stale evidence, and confirmed absence are different states. This source alone must not convert non-detection into universal absence.

## 15. Acceptance criteria

- The source class has a documented evidentiary purpose.
- Strong, secondary, weak, and prohibited uses remain distinguishable.
- Queries use only supported fields, syntax, authorization, and rate limits.
- Positive, negative, contradiction, status, and freshness checks are retained where relevant.
- Event time is preserved separately from collection time.
- Source copies and mirrors do not inflate corroboration.
- Public contact routes do not override consent, suppression, conflict, jurisdiction, procurement, or channel policy.
- Keyword matches remain evidence candidates rather than final domain, activity, opportunity, authority, or lead decisions.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Google API Source and Extraction Model](../../../sources/google-api-source-model.md), where a Google website URI may be used only as a bounded research seed under provider rules.
- [Query Composition and Evidence Rules](../query-composition-and-evidence-rules.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification is a repository-integrated documentation standard after merge. It does not implement source credentials, adapters, crawling, APIs, schemas, storage, classifiers, query execution, scoring, contact workflows, or releases.
