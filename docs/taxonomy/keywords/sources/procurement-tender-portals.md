# Harvester Source Specification: Procurement and Tender Portals

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-PROC`**

## 1. Purpose

Use official procurement sources to identify dated purchase notices, buyers, scopes, requirements, deadlines, eligibility, amendments, cancellations, awards, and permitted submission routes.

This document does not authorize collection or contact outside the portal, notice, provider, contract, or legal rules.

## 2. Approved source boundary

- Official buyer procurement pages.
- Public procurement and development-partner portals.
- Authorized tender feeds.
- Notices, attachments, clarifications, amendments, cancellations, awards, and completion records.

## 3. Strong signal uses

- Active purchase intent tied to a current notice.
- Buyer, scope, category, deadline, eligibility, and submission route.
- Official amendment, extension, cancellation, award, or completion status.

## 4. Secondary signal uses

- Technology, asset, service, integration, compliance, and delivery requirements.
- Disclosed estimated value.
- Responsible procurement function and public clarification route.

## 5. Weak or unsupported inferences

- A notice may be expired, superseded, cancelled, awarded, or copied.
- A broad category does not prove exact fit.
- A planning notice does not always mean immediate purchase.
- A procurement notice does not authorize communication outside the stated route.
- An aggregator copy is not equivalent to the authoritative notice.

## 6. Source fields and evidence targets

- portal, buyer, notice identifier, and authoritative URL
- title, description, category, scope, eligibility, and submission method
- publication, clarification, pre-bid, deadline, amendment, cancellation, award, and completion dates
- attachments, version, checksum, status, disclosed value, and geography

## 7. Keyword and query inputs

- active provider-offering capability and procurement vocabulary
- selected domain and approved activity
- buyer, geography, category, and reviewed classification code
- RFP, RFQ, EOI, tender, bid, quotation, amendment, extension, cancellation, award, and completion terms
- offering-specific exclusions and contradictions

Procurement queries require an active provider offering. Ordinary domain keywords cannot independently create purchase intent.

## 8. Governed query templates

```text
<offering or capability> + tender/RFP/RFQ/EOI
<domain> + procurement + <geography>
<buyer> + current notices
<notice identifier> + amendment/clarification/extension
<notice identifier> + cancellation/award/completion
```

The adapter must translate these logical patterns into the fields and syntax supported by the source.

## 9. Inspection sequence

1. Open the authoritative notice and material attachments.
2. Capture the current status and every amendment.
3. Resolve the buyer and domain/activity context.
4. Check deadline, eligibility, route, value, geography, and current stage.
5. Run cancellation, award, completion, expiry, and supersession checks.

## 10. Required provenance

- source and notice identifier
- buyer and authoritative URL
- notice version and attachment checksums
- publication, deadline, amendment, cancellation, award, completion, and retrieval dates
- contributing offering, domain, activity, keyword, and source-profile versions

## 11. Freshness and event time

The latest official status controls active use. Publication, deadline, amendment, cancellation, award, completion, collection, and verification times remain separate.

## 12. Duplication and corroboration

Aggregators, reposts, mirrored PDFs, and repeated announcements must resolve to the authoritative notice origin. Copies do not create independent evidence diversity.

## 13. Privacy, authorization, and compliance

- Respect portal terms, account restrictions, rate limits, and submission rules.
- Use only the permitted procurement or clarification route.
- Do not infer undisclosed evaluation or commercial details.

## 14. Non-detection and failure states

- `PROCUREMENT_NOTICE_ACTIVE`
- `PROCUREMENT_NOTICE_NOT_DETECTED`
- `PROCUREMENT_NOTICE_EXPIRED`
- `PROCUREMENT_NOTICE_CANCELLED`
- `PROCUREMENT_NOTICE_AWARDED`
- `PROCUREMENT_SOURCE_UNAVAILABLE`
- `PROCUREMENT_INSPECTION_FAILED`
- `PROCUREMENT_NOTICE_SUPERSEDED`

Non-detection, source failure, expiry, cancellation, award, and confirmed absence are different states.

## 15. Acceptance criteria

- The authoritative notice and current status are retained.
- Amendments, extensions, cancellations, awards, deadlines, and completion states are checked.
- Queries use only supported source fields and authorization.
- Procurement signals cannot activate without an active provider offering.
- Copies do not inflate corroboration.
- Contact remains limited to the notice's permitted route.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Provider-Offering Keyword Profile Standard](../provider-offering-keyword-profile-standard.md).
- [Query Composition and Evidence Rules](../query-composition-and-evidence-rules.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement portal credentials, adapters, query execution, storage, qualification, scoring, submission, contact workflows, or releases.
