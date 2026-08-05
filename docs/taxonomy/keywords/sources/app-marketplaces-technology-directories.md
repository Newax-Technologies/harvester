# Harvester Source Specification: App Marketplaces and Technology Directories

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-TECH`**

## 1. Purpose

Use official integration catalogues, app marketplaces, technology directories, public technical documentation, and lawful technology-footprint evidence to identify products, vendors, integrations, release activity, and possible existing-solution context.

## 2. Approved source boundary

- Official vendor app stores, integration pages, partner directories, and product documentation.
- Licensed technology directories and approved public technical metadata.
- Public DNS, headers, scripts, and metadata only where lawful and source-appropriate.
- Technology presence and adoption remain probabilistic unless directly confirmed.

## 3. Strong signal uses

- Vendor, product, integration, listing, supported region, category, or official partner relationship.
- Public technical documentation or official implementation statement.
- Listing status, release, deprecation, or support state.

## 4. Secondary signal uses

- Possible existing solution and technology footprint.
- Integration, migration, replacement, upgrade, maintenance, and compatibility context.
- Implementation-partner or customer case-study references.

## 5. Weak or unsupported inferences

- A marketplace listing does not prove customer adoption.
- A script, shared host, or public header does not prove ownership or active use.
- Presence does not prove satisfaction or replacement intent.
- Absence does not prove non-use.
- Ratings, reviews, and installation indicators may be unreliable or restricted.

## 6. Source fields and evidence targets

- marketplace or directory, product, vendor, listing identifier, category, and region
- integration relationship, listing status, release, deprecation, support, and update dates
- official documentation, case study, partner, and implementation references
- public technical indicator, collection method, confidence, and timestamp

## 7. Keyword and query inputs

- resolved organization, vendor, or product
- platform, integration, API, plugin, connector, migration, replacement, upgrade, deprecation, and support terms
- active provider-offering technology, competitor, existing-solution, integration, and contradiction profiles
- unsupported, discontinued, end-of-life, removed, or delisted terms

## 8. Governed query templates

```text
<vendor/product> + integration/app marketplace
<organization> + <technology> + official case study
<product> + supported region/category/listing status
<technology> + deprecated/end-of-life/removed
<organization> + integration/migration/replacement
```

## 9. Inspection sequence

1. Prefer official vendor, marketplace, and documentation sources.
2. Resolve product, vendor, integration, organization, and partner relationships separately.
3. Distinguish listing availability from customer adoption.
4. Record confidence and time sensitivity for technical indicators.
5. Run deprecation, removal, unsupported, and contradiction checks.

## 10. Required provenance

- source, listing or product identifier, vendor, and canonical URL
- category, integration relationship, region, status, and dates
- technical collection method, indicator, confidence, and timestamp
- matched technology, existing-solution, competitor, offering, and source-profile versions

## 11. Freshness and event time

Technology listings, integrations, scripts, DNS, headers, versions, and support states are time-sensitive and require source-specific refresh.

## 12. Duplication and corroboration

The same product or integration may appear on vendor, marketplace, partner, and customer pages. Resolve the relationship graph without treating copies as independent adoption evidence.

## 13. Privacy, authorization, and compliance

- Use only lawful public technical indicators and approved APIs or datasets.
- Do not probe private systems, bypass controls, exploit vulnerabilities, or collect credentials.
- Follow marketplace licensing, attribution, and retention rules.

## 14. Non-detection and failure states

- `TECHNOLOGY_RECORD_DETECTED`
- `TECHNOLOGY_RECORD_NOT_DETECTED`
- `TECHNOLOGY_SOURCE_UNAVAILABLE`
- `TECHNOLOGY_ACCESS_RESTRICTED`
- `TECHNOLOGY_INSPECTION_FAILED`
- `TECHNOLOGY_INDICATOR_STALE`
- `TECHNOLOGY_RECORD_DEPRECATED_REMOVED_OR_CONTRADICTED`

## 15. Acceptance criteria

- Listing availability and customer adoption remain separate.
- Technology presence, satisfaction, and replacement intent remain separate.
- Public technical indicators retain method, confidence, and time.
- Deprecation and support states are checked.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Provider-Offering Keyword Profile Standard](../provider-offering-keyword-profile-standard.md).
- [Organization Websites](organization-websites.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement technology scanning, marketplace credentials, APIs, storage, classifiers, scoring, or contact workflows.
