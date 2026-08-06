# Harvester Source Specification: Job Boards and Careers Pages

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-JOBS`**

## 1. Purpose

Use official careers pages and permitted job sources to identify hiring, functional ownership, location growth, technology footprint, implementation activity, and capability expansion.

## 2. Approved source boundary

- Official organization careers pages.
- Authorized job-board APIs and permitted public listings.
- User-authorized recruitment datasets.
- No automated collection from restricted platforms without explicit authorization.

## 3. Strong signal uses

- Published vacancy, role, department, location, and stated responsibilities.
- Hiring or team-expansion activity.
- Explicit technology, process, implementation, integration, or operational ownership requirements.

## 4. Secondary signal uses

- New facility, branch, function, project, or capability.
- Responsible-function and internal terminology cues.
- Technology-stack and workflow context.

## 5. Weak or unsupported inferences

- A vacancy does not prove external budget or purchase intent.
- A role does not prove dissatisfaction with current systems.
- A listing may be stale, duplicated, speculative, evergreen, or filled.
- A title does not prove decision authority.
- Generic recruitment language may not describe actual operations.

## 6. Source fields and evidence targets

- organization and vacancy identifier
- role, department, location, and employment type
- responsibilities, requirements, technologies, and process terms
- publication, update, closing, removal, and filled dates
- official or authorized application route

## 7. Keyword and query inputs

- resolved organization and responsible function
- selected domain and approved activity
- implementation, integration, automation, data, security, operations, facility, and expansion terms
- active provider-offering technology or process profiles
- closed, filled, expired, cancelled, or unavailable terms

## 8. Governed query templates

```text
<entity> + <responsible role>
<entity> + implementation/integration/automation role
<domain> + new facility or operations hiring
<entity> + <technology> + careers
<vacancy identifier> + closed/filled/expired
```

## 9. Inspection sequence

1. Prefer the official careers page.
2. Resolve organization, location, department, and vacancy identity.
3. Separate stated responsibilities from inferred commercial intent.
4. Check closing date and current vacancy state.
5. Use the result only for hiring, ownership, growth, technology, or process evidence.

## 10. Required provenance

- source, vacancy identifier, canonical URL, and organization
- role, department, location, responsibilities, and stated technologies
- publication, closing, update, removal, and retrieval dates
- matched domain, activity, role, technology, and source-profile versions

## 11. Freshness and event time

Active, filled, removed, expired, recurring, and evergreen listings must remain distinct. Publication, closing, removal, collection, and verification times remain separate.

## 12. Duplication and corroboration

The same vacancy may appear on several boards. Match organization, role, location, description, and source identifier before counting evidence diversity.

## 13. Privacy, authorization, and compliance

- Use only permitted public or authorized vacancy data.
- Do not collect applicant data.
- Do not infer sensitive personal characteristics.
- Do not bypass restricted job platforms or application systems.

## 14. Non-detection and failure states

- `JOB_LISTING_ACTIVE`
- `JOB_LISTING_NOT_DETECTED`
- `JOB_LISTING_EXPIRED`
- `JOB_LISTING_FILLED_OR_REMOVED`
- `JOB_SOURCE_UNAVAILABLE`
- `JOB_ACCESS_RESTRICTED`
- `JOB_INSPECTION_FAILED`

## 15. Acceptance criteria

- Current vacancy state and dates are retained.
- Hiring evidence remains separate from purchase intent.
- Role evidence remains separate from authority.
- Duplicate listings do not inflate corroboration.
- Restricted platforms are not accessed without authorization.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Decision-Maker and Contact-Cue Registry](../decision-maker-and-contact-cues.md).
- [Authorized Professional Networks](authorized-professional-networks.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement job-source credentials, adapters, collection, storage, role resolution, qualification, scoring, or contact workflows.
