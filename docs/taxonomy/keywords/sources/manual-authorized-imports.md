# Harvester Source Specification: Manual Authorized Imports

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-IMPORT`**

## 1. Purpose

Use customer-owned, licensed, consented, or otherwise authorized CRM records, spreadsheets, notes, exports, datasets, and operator-curated evidence under an explicit import scope.

## 2. Approved source boundary

- User-supplied or licensed files and records with documented provenance and lawful-use basis.
- Tenant-scoped ingestion, row-level validation, and immutable source preservation.
- Imports do not silently overwrite stronger evidence, consent, suppression, or canonical identity.

## 3. Strong signal uses

- Customer-owned account context and known organization relationships.
- Prior interactions, consent, suppression, referral, and operational notes when properly authorized.
- Stable source-record identifiers and customer-defined segmentation.

## 4. Secondary signal uses

- Verification seeds and enrichment candidates.
- Internal aliases and relationship history.
- Known contact routes and workflow state subject to policy.

## 5. Weak or unsupported inferences

- Input quality, age, consent, licensing, identity accuracy, and field definitions may vary.
- Free-text notes may contain opinion, sensitive data, or unverified claims.
- A CRM stage does not prove current opportunity.
- Imported contact data may be stale or suppressed.
- Customer assertions do not automatically override stronger contrary evidence.

## 6. Source fields and evidence targets

- tenant, import job, source owner, authorization basis, licence, and purpose
- file or dataset identifier, checksum, format, schema, row identifier, and source timestamp
- field mapping, consent, suppression, contact, relationship, and provenance state
- validation result, rejected rows, transformation version, and operator approval

## 7. Keyword and mapping inputs

- mapped domain, activity, organization, role, contact, consent, suppression, and offering fields
- approved aliases and customer-defined codes
- validation, deduplication, contradiction, and stale-data rules
- no uncontrolled inference from free text

## 8. Governed mapping templates

```text
<source field> → <canonical field>
<source code> → <reviewed taxonomy identifier>
<row identity> + <tenant scope> + <source record identifier>
```

Manual imports use governed schema mappings rather than public-search queries.

## 9. Inspection sequence

1. Confirm authorization, ownership, licence, purpose, and tenant.
2. Preserve the original file or record reference and checksum.
3. Validate schema, types, identifiers, consent, suppression, and row-level errors.
4. Resolve entities without overwriting stronger evidence.
5. Quarantine sensitive, contradictory, malformed, or unlicensed data.

## 10. Required provenance

- tenant, source owner, authorization, purpose, and licence
- import job, file or dataset identifier, checksum, schema, and source timestamp
- source-row identifier, original fields, mapping version, and transformed fields
- validation, consent, suppression, contradiction, and review state

## 11. Freshness and event time

Imported evidence inherits source timestamps and a field-specific recency policy. Import time does not make old data current.

## 12. Duplication and corroboration

Rows, files, CRM exports, copied spreadsheets, and repeated imports must be deduplicated through source identifiers, checksums, entity resolution, and import lineage.

## 13. Privacy, authorization, and compliance

- Tenant isolation and purpose limitation are mandatory.
- Collect only necessary fields.
- Consent, suppression, deletion, retention, and audit controls apply.
- Do not import datasets without a documented right to use them.
- Sensitive fields require explicit policy and access controls.

## 14. Non-detection and failure states

- `IMPORT_ACCEPTED`
- `IMPORT_PARTIALLY_ACCEPTED`
- `IMPORT_REJECTED`
- `IMPORT_AUTHORIZATION_MISSING`
- `IMPORT_SCHEMA_INVALID`
- `IMPORT_ROW_QUARANTINED`
- `IMPORT_CONSENT_OR_SUPPRESSION_CONFLICT`

## 15. Acceptance criteria

- Authorization, purpose, tenant, and licence are recorded.
- Original records and checksums are preserved.
- Row-level validation and quarantine are supported by the specification.
- Import time is not treated as source freshness.
- Consent and suppression cannot be overwritten silently.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Cross-Product Keyword and Profile Contract](../cross-product-keyword-contract.md).
- [User Input Storage Model](../../../sources/user-input-storage-model.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement file upload, import jobs, schema validation, storage, entity resolution, consent enforcement, scoring, or contact workflows.
