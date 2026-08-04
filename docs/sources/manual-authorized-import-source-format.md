# Harvester Manual and Authorized Import Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Current manual and authorized-import source types exist; target governed format is not fully implemented**

## 1. Purpose

This document defines how operators and customers submit individual records, CSV files, spreadsheets, JSON files, CRM exports, licensed datasets, customer-owned lists and consent-backed records to Harvester.

Manual entry and imports are not lower-quality by definition. Their authority depends on ownership, provenance, date, permission, validation and corroboration.

## 2. Source modes

```text
MANUAL_OPERATOR_ENTRY
MANUAL_REVIEWED_ASSERTION
CUSTOMER_AUTHORIZED_IMPORT
LICENSED_DATASET_IMPORT
CONSENT_BACKED_CONTACT_IMPORT
SYSTEM_MIGRATION_IMPORT
```

## 3. User configuration and import declaration

Every import must declare:

```text
mode
source_name
source_reference
data_owner
authorization_basis
license_reference
consent_reference
permitted_purposes
prohibited_purposes
exported_at
source_updated_at
retention_period
deletion_policy
contacting_basis
file_reference
file_checksum
mapping_profile_version
deduplication_policy
review_requirement
```

A file without a known owner, purpose and permission basis must not enter production processing.

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Import batch | Batch ID and checksum | Import-level provenance |
| Import row | Batch plus row ID | Submitted entity or event evidence |
| Manual entry | Harvester entry ID | Operator-supplied record |
| Operator assertion | Assertion ID | Human-reviewed bounded claim |
| Mapping error | Batch plus row and field | Validation evidence |
| Rejected row | Batch plus row ID | Audit and remediation evidence |

## 5. Canonical formatting

```text
source.code = MANUAL | AUTHORIZED_IMPORT
source.mode = selected import mode
native.object_type = import_batch | import_row | manual_entry | operator_assertion
native.object_id = batch and row identifier or manual-entry ID
native.url = source reference when available
entity_hints = mapped submitted identity and contact fields
content = submitted notes or document references
signals = mapped taxonomy, activities, services, events and technologies
provenance = owner, exporter, import actor, timestamps, checksum, mapping version and original field paths
quality.review_required = true unless the source and mapping policy explicitly permits automatic acceptance
policy.authorization_basis = CUSTOMER_AUTHORIZED_IMPORT | LICENSED_DATASET | MEMBER_CONSENT | MANUAL_OPERATOR_REFERENCE
```

## 6. Example import row envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "AUTHORIZED_IMPORT", "mode": "CUSTOMER_AUTHORIZED_IMPORT"},
  "native": {
    "object_type": "import_row",
    "object_id": "batch-123:row-45",
    "payload_ref": "customer-import://batch-123/row-45",
    "payload_hash": "sha256:row-example"
  },
  "entity_hints": {
    "organization_names": ["Example Distributor"],
    "domains": ["example.pk"],
    "emails": ["sales@example.pk"],
    "phones": ["+92510000000"],
    "provider_identifiers": [{"type": "CUSTOMER_CRM_ACCOUNT_ID", "value": "ACC-445"}]
  },
  "content": {
    "summary": "Customer CRM export identifies the organization as a pharmaceutical distributor.",
    "language": "en",
    "published_at": null,
    "content_type": "customer_import_row"
  },
  "signals": {"domain_codes": ["HC-MED-001"], "activity_codes": ["ACT-LOG-001"]},
  "quality": {"completeness": "PARTIAL", "freshness": "UNKNOWN", "review_required": true, "conflict_flags": []},
  "policy": {
    "authorization_basis": "CUSTOMER_AUTHORIZED_IMPORT",
    "retention_policy": "CUSTOMER_DECLARED",
    "attribution_required": false,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Validation and rejection states

```text
IMPORT_SUCCESS
IMPORT_PARTIAL_SUCCESS
IMPORT_FILE_INVALID
IMPORT_CHECKSUM_MISMATCH
IMPORT_MAPPING_INVALID
IMPORT_REQUIRED_FIELD_MISSING
IMPORT_AUTHORIZATION_MISSING
IMPORT_LICENSE_UNKNOWN
IMPORT_CONSENT_MISSING
IMPORT_CONTACTING_BASIS_MISSING
IMPORT_DUPLICATE_ROW
IMPORT_CROSS_TENANT_REFERENCE
IMPORT_SENSITIVE_DATA_REJECTED
IMPORT_ROW_REJECTED
IMPORT_POLICY_BLOCKED
```

## 8. Security and privacy

- Files are malware-scanned and size-limited before parsing.
- Original files use tenant-isolated storage and access controls.
- Sensitive and excessive personal data is rejected or quarantined.
- Imported contacts retain consent or business-basis fields and suppression state.
- Customer deletion requests and source-owner revocation propagate to imported observations and derived data where required.
- Mapping, acceptance, rejection and manual corrections remain auditable.

## 9. Evidence boundaries

Authorized imports may support organization, person, relationship, activity, service, event and contact evidence according to the declared owner and permission basis.

They do not bypass entity resolution, suppression, consent, evidence quality, opportunity qualification or review rules.

## 10. Delivery boundary

This document does not implement upload storage, malware scanning, parsers, mappings, validation, rejection workflows, deletion propagation or scoring.