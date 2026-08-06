# Harvester Source Specification: Business Directories

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-DIR`**

## 1. Purpose

Use permitted business directories to discover candidate organizations, public categories, supplier or distributor relationships, locations, websites, and public contact routes that require independent verification.

## 2. Approved source boundary

- Public or licensed business directories.
- Chamber, association, supplier, distributor, and member directories.
- Authorized directory APIs and data feeds.
- Directory records are discovery evidence unless the source is authoritative for a specific field.

## 3. Strong signal uses

- A directory record exists for a named organization, category, location, website, or public route.
- Supplier, distributor, association, or membership relationship when the directory governs that list.

## 4. Secondary signal uses

- Organization and branch discovery.
- Category and local-presence context.
- Candidate aliases, identifiers, and public routes.

## 5. Weak or unsupported inferences

- Records may be stale, copied, user-submitted, duplicated, or resold.
- Category assignment does not prove current activity.
- A reseller may be mistaken for a manufacturer or principal.
- Public contact details may be outdated.
- Directory ranking does not prove quality, fit, demand, or authority.

## 6. Source fields and evidence targets

- directory, record identifier, category, name, and location
- website and public contact route
- supplier, distributor, association, or membership relationship
- update date, verification status, licence, and source-native identifiers

## 7. Keyword and query inputs

- selected domain identity and aliases
- organization type and directory category
- supplier, distributor, chamber, association, or member terms
- geography and local terminology
- inactive, closed, unverified, duplicate, or delisted states

## 8. Governed query templates

```text
<domain> + directory + <geography>
<supplier/distributor/category> + <location>
<organization> + directory record
<association or chamber> + member directory
<record> + inactive/closed/delisted
```

## 9. Inspection sequence

1. Identify whether the directory is authoritative, licensed, self-submitted, or aggregated.
2. Resolve the record to an organization or branch candidate.
3. Verify category, status, website, and contact details independently when material.
4. Separate manufacturer, distributor, reseller, agent, and marketplace roles.
5. Cluster copied and repeated records before corroboration.

## 10. Required provenance

- directory, licence or access basis, record identifier, and canonical URL
- category, organization, location, website, public route, and governed relationships
- update or verification date
- independent verification references and duplicate-cluster identifier

## 11. Freshness and event time

Directory evidence requires source-specific update and verification dates. Undated or unverified records have limited authority.

## 12. Duplication and corroboration

Similar names, addresses, phones, websites, descriptions, and identifiers must be clustered. Aggregators that copied one origin do not provide independent corroboration.

## 13. Privacy, authorization, and compliance

- Respect licensing, terms, rate limits, export rules, and privacy requirements.
- Do not collect hidden fields or repurpose personal contacts.
- Public listing does not create consent.

## 14. Non-detection and failure states

- `DIRECTORY_RECORD_DETECTED`
- `DIRECTORY_RECORD_NOT_DETECTED`
- `DIRECTORY_SOURCE_UNAVAILABLE`
- `DIRECTORY_ACCESS_RESTRICTED`
- `DIRECTORY_LOOKUP_FAILED`
- `DIRECTORY_RECORD_STALE`
- `DIRECTORY_RECORD_DUPLICATE_OR_CONTRADICTED`

## 15. Acceptance criteria

- Directory authority and access basis are recorded.
- Directory category remains separate from confirmed activity.
- Organization roles such as manufacturer, distributor, and reseller remain distinct.
- Material fields are independently verified when required.
- Copied records do not inflate evidence diversity.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Maps and Business Listings](maps-business-listings.md).
- [Semantic, Entity and Classification Expansion](../semantic-entity-and-classification-expansion.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement directory licences, adapters, collection, storage, verification, entity resolution, scoring, or contact workflows.
