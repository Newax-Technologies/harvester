# Harvester Source Input and Formatting Index

Status: **Authoritative source-document index**  
Version: **2.0**  
Date: **6 August 2026**  
Implementation status: **Planned unless a linked runtime document and exact-head verification prove otherwise**

This directory defines how approved user inputs and source-native records enter Harvester. Runtime authorization, pricing, rate limits, credentials, connector capabilities, and execution gates are governed by [Source Governance and Connector Runtime](../architecture/source-governance-and-connector-runtime.md).

## 1. Required source sequence

```text
Tenant and client workspace
→ provider organization and business unit
→ active offering
→ approved lead-generation profile and market definition
→ permitted purpose
→ approved source and access class
→ active source-policy version
→ connection and credential scope
→ connector, source-schema, mapping, rate, and price versions
→ immutable Harvest Job source plan
→ source request and response outcome
→ source-native RawObservation
→ EvidenceArtifact and EvidenceAssertion
→ coverage, contradiction, freshness, and provenance
→ entity resolution
→ qualification and opportunity assessment
→ controlled output
```

A source adapter may create observations and evidence. It may not independently create canonical identity, a confirmed service gap, a qualified opportunity, contact authority, publication approval, or profile activation.

## 2. Governing documents

- [Source Governance and Connector Runtime](../architecture/source-governance-and-connector-runtime.md)
  - Source classes, purposes, policies, credentials, connections, connector contracts, schemas, mappings, quotas, pricing, execution gates, economics, suspension, and restricted paths.

- [Universal Entity and Evidence Model](../architecture/universal-entity-and-evidence-model.md)
  - Raw observations, artifacts, excerpts, assertions, claims, coverage, contradictions, provenance, and resolved entities.

- [User Input Storage Model](user-input-storage-model.md)
  - Tenant-isolated configuration, providers, business units, offerings, profiles, activation, source selections, secret references, outputs, and immutable job snapshots.

- [Canonical Source Record Format](canonical-source-record-format.md)
  - Shared request, outcome, source-native observation, artifact, assertion, provenance, quality, retention, and failure envelopes.

- [Source Adapter Documentation Template](source-adapter-template.md)
  - Mandatory documentation and acceptance structure for a source family.

## 3. Named platform source formats

- [Google Source Format](google-source-format.md)
- [Yandex Source Format](yandex-source-format.md)
- [LinkedIn Source Format](linkedin-source-format.md)
- [Meta and Instagram Source Format](meta-source-format.md)
- [X Source Format](x-source-format.md)
- [Bing Source Format](bing-source-format.md)
- [Indeed Source Format](indeed-source-format.md)
- [Crunchbase Source Format](crunchbase-source-format.md)
- [Apple Maps Source Format](apple-maps-source-format.md)
- [Telegram Source Format](telegram-source-format.md)

A named format defines source-native structure and mapping expectations. It does not prove that access is approved, commercially available, or enabled for production.

## 4. Other source families

- [Organization Website Source Format](organization-website-source-format.md)
- [Government and Official Registry Source Format](government-registry-source-format.md)
- [Business and Industry Directory Source Format](business-directory-source-format.md)
- [General Job Board Source Format](job-board-source-format.md)
- [Procurement and Tender Source Format](procurement-tender-source-format.md)
- [News and Media Source Format](news-media-source-format.md)
- [Application and Marketplace Source Format](app-marketplace-source-format.md)
- [Manual and Authorized Import Source Format](manual-authorized-import-source-format.md)
- [Generic API, Feed and Licensed Dataset Source Format](generic-api-feed-source-format.md)

## 5. Detailed acquisition authorities

- [Google API Source and Extraction Model](google-api-source-model.md)
  - Public discovery and customer-authorized Google data, coverage, field masks, attribution, cost, retention, and scoring boundaries.

- [Yandex Maps API Source and Extraction Model](yandex-maps-api-source-model.md)
  - Yandex discovery and customer-authorized data, geography, pagination, extraction, cost, caching, attribution, and production restrictions.

- [LinkedIn Authorized Data Source Model](linkedin-authorized-data-source-model.md)
  - Approved APIs, partnerships, customer-authorized imports, consented references, privacy, retention, and the quarantine and removal path for contested legacy automation.

Stricter provider terms and active policy versions override general source guidance.

## 6. Access classes

Every source use resolves to one class:

```text
OFFICIAL_PUBLIC_API
CUSTOMER_AUTHORIZED_OAUTH
APPROVED_PARTNER_API
LICENSED_DATA_FEED
OPEN_DATASET
BULK_DOWNLOAD
RSS_OR_ATOM
WEBHOOK
CUSTOMER_UPLOAD
CUSTOMER_DATABASE
PERMITTED_PUBLIC_WEB
MANUAL_RESEARCH
RESTRICTED
PROHIBITED
```

Technical reachability does not select an access class or grant authority.

## 7. Source and destination separation

Reading from a source and writing to a destination are separately governed capabilities.

A connection may be:

```text
READ_ONLY
IMPORT
EXPORT
WRITE
BIDIRECTIONAL
INSPECTION_ONLY
```

Each direction requires its own purpose, scope, policy, mapping, credential, approval, and audit.

## 8. Preservation and storage

Harvester preserves the source-native response actually returned when policy permits it.

Storage follows:

- PostgreSQL for identity, metadata, status, hashes, policy, and references;
- object storage for large HTML, PDF, image, document, and media bodies;
- exact excerpts and locators for material assertions;
- immutable versions for changed payloads;
- source-specific retention, access, redaction, and deletion.

Public visibility does not authorize indefinite retention or redistribution.

## 9. Failure and coverage states

The source layer preserves:

```text
SUCCESS
EMPTY
PARTIAL
FAILED
BLOCKED
POLICY_BLOCKED
PERMISSION_DENIED
RATE_LIMITED
QUOTA_EXHAUSTED
CANCELLED
STALE
SCHEMA_INCOMPATIBLE
```

Evidence evaluation separately preserves:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_INSPECTED
INSPECTION_FAILED
UNKNOWN
NOT_APPLICABLE
```

No failed, skipped, uninspected, or incomplete source path may become confirmed absence.

## 10. Restricted professional-network behavior

Stealth browser automation, account farms, fingerprint evasion, CAPTCHA solving, and access-control circumvention are not supported enterprise source capabilities.

Professional-network data remains restricted until an approved API, partnership, licensed feed, customer-authorized export, consented user reference, or manual research path is recorded in an active source policy.

## 11. New-source admission

A source cannot activate until it has:

1. source definition and access class;
2. approved purposes and prohibited purposes;
3. current terms and privacy review;
4. permission and credential model;
5. connector capability declaration;
6. source schema and mapping versions;
7. rate-limit and pricing records;
8. retention, redistribution, attribution, and deletion rules;
9. failure and coverage taxonomy;
10. security and privacy review;
11. contract, policy, integration, and regression tests;
12. reviewed production activation.

## 12. Locked rules

1. Connection does not mean authorization.
2. Public does not mean unrestricted.
3. A connector runs only after the execution gate approves source, purpose, credential, data class, region, retention, output, quota, cost, and review requirements.
4. Provider-native identifiers remain source references until resolution.
5. Missing fields and zero results do not prove absence.
6. Copied or syndicated origins do not increase source diversity.
7. Source records and keyword matches do not independently establish activity, opportunity, authority, consent, or qualification.
8. Completed jobs retain exact source, connector, schema, mapping, policy, rate, price, query, field-mask, and retention versions.
9. Source and destination failures remain visible and recoverable.
10. These documents are architecture and contract authorities, not claims of runtime implementation.
