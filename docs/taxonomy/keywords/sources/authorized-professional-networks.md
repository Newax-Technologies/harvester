# Harvester Source Specification: Authorized Professional Networks

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-PROF`**

## 1. Purpose

Use authorized professional-network access to support current organization affiliation, role, function, public organization descriptions, hiring, announcements, and lawful relationship context.

## 2. Approved source boundary

- Approved APIs.
- Customer-authorized organization data.
- Member-consented data.
- Licensed partner integrations.
- Authorized imports and bounded manual operator references.
- No scraping, cookie reuse, session automation, access-control bypass, or unauthorized bulk collection.

## 3. Strong signal uses

- Authorized current organization and role fields.
- Customer-administered organization-page activity and analytics where approved.
- Member-consented identity fields and contract-approved partner data.

## 4. Secondary signal uses

- Functional-owner cues.
- Hiring, growth, partnerships, and announcements.
- Current affiliation corroboration when supported by another reliable source.

## 5. Weak or unsupported inferences

- A title does not prove decision authority.
- Self-reported affiliations may be stale.
- Public visibility does not authorize automated collection.
- A member profile does not create contact consent.
- Professional-network evidence does not independently prove purchase intent.

## 6. Source fields and evidence targets

- source mode and authorization basis
- organization or member source identifier
- organization, role, function, location, and approved descriptions
- scopes, access tier, API version, connection date, verification date, and revocation state
- permitted customer-owned activity and analytics fields

## 7. Keyword and query inputs

- resolved organization identity
- responsible function and role groups
- approved domain, activity, event, hiring, partnership, and organization terms
- provider-supported fields and filters only
- no inferred personal-contact search

## 8. Governed query templates

```text
<resolved organization> + <responsible function>
<resolved organization> + <authorized current role>
<organization> + hiring/expansion/partnership announcement
<organization identifier> + approved organization fields
```

## 9. Inspection sequence

1. Confirm the approved source mode and authorization.
2. Resolve organization identity before person or role resolution.
3. Verify current affiliation and role recency.
4. Keep functional responsibility separate from decision authority and contact permission.
5. Apply deletion, revocation, retention, consent, and suppression rules.

## 10. Required provenance

- provider, source mode, authorization record, scopes, and API version
- organization or member source identifier
- returned fields and current-affiliation timestamp
- matched role, organization, event, activity, and source-profile versions
- retention, deletion, and consent state

## 11. Freshness and event time

Affiliation, role, authorization, and organization activity are time-sensitive. Revoked or expired authorization blocks future collection.

## 12. Duplication and corroboration

The same organization or person may appear through organization APIs, partner tools, authorized imports, and operator references. Resolve the entity without counting repeated records as independent evidence.

## 13. Privacy, authorization, and compliance

- Provider terms and explicit authorization govern collection, storage, reuse, export, and deletion.
- Do not infer or reconstruct private contact details.
- Do not automate messaging, connections, reactions, comments, or other engagement without separate approval.
- Source visibility does not override suppression or consent.

## 14. Non-detection and failure states

- `PROFESSIONAL_RECORD_AUTHORIZED`
- `PROFESSIONAL_RECORD_NOT_DETECTED`
- `PROFESSIONAL_AUTHORIZATION_MISSING`
- `PROFESSIONAL_AUTHORIZATION_REVOKED`
- `PROFESSIONAL_ACCESS_RESTRICTED`
- `PROFESSIONAL_SOURCE_FAILED`
- `PROFESSIONAL_AFFILIATION_STALE`

## 15. Acceptance criteria

- The approved source mode and authorization are retained.
- Organization resolution precedes role resolution.
- Role, authority, and contact permission remain separate.
- Provider restrictions override keyword configuration.
- Repeated records do not inflate evidence diversity.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [LinkedIn Authorized Data Source Model](../../../sources/linkedin-authorized-data-source-model.md).
- [Decision-Maker and Contact-Cue Registry](../decision-maker-and-contact-cues.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement provider approval, credentials, APIs, imports, storage, role resolution, scoring, or contact workflows.
