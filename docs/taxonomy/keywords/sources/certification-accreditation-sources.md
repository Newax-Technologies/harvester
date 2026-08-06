# Harvester Source Specification: Certification and Accreditation Sources

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-CERT`**

## 1. Purpose

Use official certifier, accreditor, standards-body, regulator, and organization records to verify certification, accreditation, assessed scope, facility or product coverage, status, and validity dates.

## 2. Approved source boundary

- Official certifier, accreditor, standards-body, and regulator records.
- Public or authorized certificate databases and documents.
- Quality, safety, facility, laboratory, product, education, healthcare, and professional accreditation sources.
- Claims require source, scope, status, and dates.

## 3. Strong signal uses

- Certificate or accreditation identifier.
- Certified or accredited entity, facility, product, standard, scope, status, and validity period.
- Suspension, withdrawal, expiry, renewal, or scope change.

## 4. Secondary signal uses

- Facility, product, laboratory, quality, safety, compliance, or capability context.
- Possible audit, renewal, documentation, or monitoring requirements.

## 5. Weak or unsupported inferences

- Certification does not prove day-to-day operational effectiveness.
- A logo on a website may be outdated or misused.
- A certificate may cover only one site, product, process, or scope.
- Copied certificates may omit expiry, suspension, or withdrawal.
- Compliance status does not independently prove buying intent.

## 6. Source fields and evidence targets

- certifier or accreditor, standard, scheme, identifier, and authoritative source
- entity, facility, product, process, scope, exclusions, and geography
- issue, effective, surveillance, renewal, expiry, suspension, withdrawal, and verification dates
- document version, checksum, and source-native status

## 7. Keyword and query inputs

- resolved entity, facility, product, or laboratory
- standard, scheme, accreditation, certification, quality, safety, compliance, renewal, audit, or surveillance terms
- certificate identifier
- expired, suspended, withdrawn, revoked, lapsed, or scope-changed terms

## 8. Governed query templates

```text
<entity> + <standard or scheme>
<certificate identifier>
<facility/product> + certification/accreditation
<entity> + renewal/surveillance audit
<certificate> + expired/suspended/withdrawn
```

## 9. Inspection sequence

1. Prefer the certifier, accreditor, standards body, or regulator source.
2. Verify entity, site, product, process, standard, and exact scope.
3. Capture issue, expiry, renewal, suspension, withdrawal, and current status.
4. Separate website claims and logos from authoritative verification.
5. Do not convert certification into operational effectiveness or opportunity without additional evidence.

## 10. Required provenance

- authority, scheme, standard, certificate identifier, and canonical URL
- entity, facility, product, scope, exclusions, and status
- issue, effective, surveillance, renewal, expiry, suspension, withdrawal, and retrieval dates
- document checksum, parser version, and contributing profile versions

## 11. Freshness and event time

Certification evidence is controlled by validity, surveillance, renewal, suspension, withdrawal, and scope dates.

## 12. Duplication and corroboration

The same certificate may appear on an organization website, certifier database, PDF, or directory. The authoritative certifier record controls status.

## 13. Privacy, authorization, and compliance

- Use only public or authorized certificate records.
- Do not imply regulatory approval beyond the exact scope.
- Respect certificate-document licensing and personal-data limitations.

## 14. Non-detection and failure states

- `CERTIFICATION_RECORD_ACTIVE`
- `CERTIFICATION_RECORD_NOT_DETECTED`
- `CERTIFICATION_RECORD_EXPIRED`
- `CERTIFICATION_RECORD_SUSPENDED_OR_WITHDRAWN`
- `CERTIFICATION_SOURCE_UNAVAILABLE`
- `CERTIFICATION_VERIFICATION_FAILED`
- `CERTIFICATION_SCOPE_CONTRADICTED`

## 15. Acceptance criteria

- Authority, identifier, scope, status, and validity dates are retained.
- Website claims remain separate from authoritative verification.
- Expiry, suspension, withdrawal, and scope changes are checked.
- Certification does not independently prove operational effectiveness or demand.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Government and Professional Registries](government-professional-registries.md).
- [Keyword Quality and Review Standard](../keyword-quality-and-review-standard.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement certificate-source credentials, APIs, document verification, storage, classification, scoring, or contact workflows.
