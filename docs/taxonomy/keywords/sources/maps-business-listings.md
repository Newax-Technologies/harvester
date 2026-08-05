# Harvester Source Specification: Maps and Business Listings

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-MAPS`**

## 1. Purpose

Use approved map and local-business APIs to discover candidate places, branches, locations, public categories, operating status, official website paths, public contact routes, and bounded local context.

## 2. Approved source boundary

- Official map and local-business APIs.
- Customer-authorized business-profile data.
- Permitted operator links.
- Public place discovery and customer-authorized operating intelligence remain separate modes.
- No scraping of provider map websites, undocumented endpoints, or browser sessions.

## 3. Strong signal uses

- Provider-specific place identifier, name, location, branch, category, operating status, and official website path where returned.
- Customer-authorized managed-location data within approved scope.
- Public contact and opening information subject to provider rules.

## 4. Secondary signal uses

- Branch count and local presence.
- Service-area and location-growth context.
- Transient research seeds for independent website or registry verification.

## 5. Weak or unsupported inferences

- Provider category is not canonical Harvester taxonomy truth.
- Missing website, phone, rating, review, or result does not prove absence.
- User edits and duplicates may create incorrect records.
- A place identifier is not eternal legal identity.
- Public reviews and ratings require strict provider-specific treatment.

## 6. Source fields and evidence targets

- provider and source mode
- provider place or organization identifier
- name, provider categories, address, coordinates, operating status, official website path, public phone, and hours where permitted
- query geometry, field mask, attribution, retrieval time, and provider retention policy

## 7. Keyword and query inputs

- selected domain identity and reviewed local terminology
- approved geography, radius, grid, or administrative area
- provider-supported categories, text queries, and field masks
- resolved organization or branch names
- closed, moved, duplicate, renamed, or permanently closed states

## 8. Governed query templates

```text
<domain or category> + <geography>
<organization or branch name> + <location>
<address or phone> exact lookup
<provider place identifier> details refresh
<candidate place> + official website verification path
```

## 9. Inspection sequence

1. Use only documented provider APIs and approved source modes.
2. Capture query geometry and field mask.
3. Resolve place, branch, and legal-organization identity separately.
4. Use provider-returned website paths only as bounded research seeds where policy permits.
5. Verify moved, closed, duplicate, renamed, and current-status signals.

## 10. Required provenance

- provider, API or source mode, request type, query, geometry, and field mask
- provider identifiers and returned public fields
- attribution, provider-policy version, retrieval time, and permitted retention
- independent verification source when transient data becomes durable evidence

## 11. Freshness and event time

Operating status, hours, contact, place identifiers, and branch data are time-sensitive. Provider-specific refresh and retention rules control reuse.

## 12. Duplication and corroboration

Duplicate listings, moved places, alternate-language names, brands, departments, and branches must be resolved without collapsing distinct locations or counting provider copies as independent sources.

## 13. Privacy, authorization, and compliance

- Provider API terms, attribution, caching, retention, privacy, and field-use rules override generic storage.
- Do not scrape map websites or internal browser endpoints.
- Public place data does not create communication consent.

## 14. Non-detection and failure states

- `MAP_PLACE_DETECTED`
- `MAP_PLACE_NOT_DETECTED`
- `MAP_SOURCE_UNAVAILABLE`
- `MAP_QUOTA_OR_RATE_LIMITED`
- `MAP_ACCESS_RESTRICTED`
- `MAP_INSPECTION_FAILED`
- `MAP_PLACE_CLOSED_MOVED_OR_DUPLICATE`

## 15. Acceptance criteria

- Public and customer-authorized modes remain separate.
- Provider categories remain source-native until mapped.
- Non-return is not treated as absence.
- Provider storage and attribution rules are retained.
- Place, branch, and legal identity remain separate.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Google API Source and Extraction Model](../../../sources/google-api-source-model.md).
- [Yandex Maps API Source and Extraction Model](../../../sources/yandex-maps-api-source-model.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement provider credentials, APIs, map queries, storage, entity resolution, scoring, or contact workflows.
