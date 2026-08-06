# Harvester Source Specification: Government and Professional Registries

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-REG`**

## 1. Purpose

Use authoritative public or authorized registries to verify legal identity, registration, licensing, regulated category, status, address, and effective dates for the fields governed by that registry.

This document defines how keyword profiles may be composed for this source, which signals the source may support, which inferences remain weak or prohibited, and what evidence must be retained. It does not authorize access that the source, provider, contract, law, or customer has not permitted.

## 2. Approved source boundary

- Company, charity, tax, professional, licensing, regulated-entity, facility, product, and public-body registries.
- Official registry APIs, search interfaces, downloadable datasets, or operator-provided records used under the source's rules.
- Only fields that the registry is legally and operationally responsible for maintaining.

## 3. Strong signal uses

- Legal or registered name.
- Registration, licence, or professional identifier.
- Legal form, regulated category, registration status, and permitted activity.
- Registered address and official effective, renewal, expiry, suspension, revocation, or dissolution dates.

## 4. Secondary signal uses

- New registration, renewal, ownership, officer, category, or address changes where public and relevant.
- Classification codes and jurisdiction-specific entity relationships.

## 5. Weak, unsupported, or prohibited inferences

- Registry presence does not prove current operational capability.
- A permitted activity does not prove the activity is actively performed.
- Registration does not prove demand, technology use, budget, or buying intent.
- Registry update delays may create stale status.
- A public officer record does not automatically justify outreach.

## 6. Source fields and evidence targets

- registry name, jurisdiction, edition, and authoritative URL
- legal name, trading name, legal form, registration or licence number
- status, category, classification code, address, and governed relationships
- registration, effective, renewal, expiry, suspension, revocation, and closure dates
- record version, retrieval time, and source-native identifiers

A source adapter may collect only fields supported by its documented interface and approved authorization. A keyword profile cannot expand the adapter's legal or technical collection boundary.

## 7. Keyword and query inputs

- exact legal or registered name
- registration, licence, tax, professional, or facility identifier
- reviewed classification code and edition
- regulated category plus geography
- status, renewal, suspension, revocation, dissolution, or expiry terms

Domain identity, activity identity, organization cues, and source context may support discovery. Offering-specific problem, intent, replacement, integration, competitor, existing-solution, procurement, or gap terms require an active provider offering.

## 8. Governed query or mapping templates

```text
<exact legal name>
<registration or licence identifier>
<reviewed classification code> + <jurisdiction>
<entity name> + <regulated category>
<identifier> + status/renewal/expiry/suspension/revocation
```

Templates are logical patterns. The source adapter must translate them into the exact fields, filters, syntax, and request limits supported by that source.

## 9. Inspection sequence

1. Identify the authoritative registry, jurisdiction, and exact field authority.
2. Search by stable identifiers before relying on fuzzy names.
3. Retain the source-native classification and map it separately to Harvester taxonomy.
4. Verify effective dates and status changes.
5. Do not extrapolate operational capability or opportunity from registration alone.

## 10. Required provenance

- registry, jurisdiction, dataset or interface version
- source-native record identifier
- queried name or identifier and returned legal fields
- status and all relevant effective dates
- retrieval time, classification mapping version, and operator review where required

Every material match must retain the originating domain, activity, organization, offering, signal, source, language, locale, match mode, precision tier, and profile version.

## 11. Freshness and event time

Registry freshness depends on the governed field, registry update cadence, effective date, and legal status. The retrieval date must not replace the record's effective date.

Collection time, publication time, effective time, event time, expiry time, and last verification time remain separate fields where applicable.

## 12. Duplication and corroboration

The same legal entity may appear in several registries. Records must be linked by identifiers and jurisdiction without treating repeated legal facts as independent operational corroboration.

Duplicate copies never create independent evidence diversity.

## 13. Privacy, authorization, and compliance

- Collect only lawful, necessary public or authorized fields.
- Do not repurpose personal officer or professional data beyond the approved workflow.
- Honor source terms, retention limits, jurisdiction, suppression, and disclosure rules.

Source authorization and policy override keyword ambition.

## 14. Non-detection and failure states

- `REGISTRY_RECORD_DETECTED`
- `REGISTRY_RECORD_NOT_DETECTED`
- `REGISTRY_SOURCE_UNAVAILABLE`
- `REGISTRY_ACCESS_RESTRICTED`
- `REGISTRY_LOOKUP_FAILED`
- `REGISTRY_STATUS_STALE`
- `REGISTRY_RECORD_CONTRADICTED`

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

- [Semantic, Entity and Classification Expansion](../semantic-entity-and-classification-expansion.md).
- [Keyword Quality and Review Standard](../keyword-quality-and-review-standard.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification is a repository-integrated documentation standard after merge. It does not implement source credentials, adapters, crawling, APIs, schemas, storage, classifiers, query execution, scoring, contact workflows, or releases.
