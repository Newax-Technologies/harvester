# Harvester Input-Page Output Selection Specification

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not started**

This specification defines the governed output contract for Harvester's guided provider, market, evidence, and lead-generation configuration flow.

## 1. Purpose

Output selection answers:

- what Harvester should produce;
- how many records may be produced;
- which eligibility, quality, freshness, evidence, contradiction, and contact rules apply;
- which fields and evidence depth may be included;
- how results are ranked and deduplicated;
- where approved results may be delivered;
- how scheduling, retention, review, activation, and history are controlled.

It is not merely a file-format dropdown.

## 2. Locked sequence

```text
Provider and business unit
→ active offering
→ lead-generation profile
→ market and sector-pack selection
→ domains and independent activities
→ keywords, signals, sources, geography, locale, and evidence rules
→ contact policy
→ output selection
→ validation and preview
→ review and approval
→ immutable Harvest Job snapshot
→ governed result generation
```

## 3. Product boundary

Output selection remains separate from source acquisition, evidence extraction, entity resolution, qualification, opportunity scoring, daily reservation, export, publication, and outreach.

Generating a result never automatically exports, publishes, contacts, or messages anyone.

## 4. Required configuration groups

```text
A. Result purpose
B. Quantity and capacity
C. Eligibility and quality
D. Fields and evidence depth
E. Ordering and deduplication
F. Destination and format
G. Delivery timing and retention
```

## 5. Primary output types

| Code | Output type | Purpose |
| --- | --- | --- |
| `LEAD_INTELLIGENCE_RESULTS` | Lead Intelligence Results | In-app evidence-backed entities for research and review |
| `QUALIFIED_LEAD_LIST` | Qualified Lead List | Entities satisfying approved qualification and opportunity policies |
| `DAILY_SELECTION_QUEUE` | Daily Selection Queue | Eligible leads prepared for controlled reservation |
| `ACCOUNT_BRIEFS` | Account Briefs | Evidence-backed organization dossiers |
| `CONTACT_READY_RECORDS` | Contact-Ready Records | Qualified records with approved contact-route evidence |
| `OUTREACH_DRAFT_CANDIDATES` | Outreach Draft Candidates | Records eligible for a separate readiness and draft-review process |
| `EVIDENCE_REVIEW_DATASET` | Evidence Review Dataset | Records prepared for human taxonomy, evidence, or model review |
| `INTEGRATION_PUBLICATION_PAYLOAD` | Integration Publication Payload | Approved records prepared for an optional adapter or signed webhook |

One primary output is selected. Compatible supporting artifacts may include score summaries, evidence digests, dossiers, contradiction reports, coverage reports, exclusion summaries, run manifests, and schema manifests.

## 6. Compatibility rules

- Contact-ready results require an approved contact policy.
- Outreach-draft candidates require active offerings, readiness rules, and allowed-channel policy.
- Daily selection requires reservation and capacity settings.
- External publication requires an authorized destination and schema.
- Evidence-review datasets may contain non-qualified records but must remain classified as review data.
- No output may bypass tenant, permission, suppression, consent, jurisdiction, conflict, evidence, source, or field restrictions.

## 7. Quantity and capacity

Required controls include:

- target result count;
- hard maximum;
- optional reserve count;
- per-sector, per-domain, per-geography, and per-group concentration limits;
- provider capacity;
- cost or budget ceiling where supported.

The requested count is a target, not a guarantee. Harvester returns fewer results when fewer records satisfy approved rules. Qualification, evidence, compliance, or confidence thresholds are never reduced silently to fill a quota. Zero results are valid.

## 8. Eligibility and quality

Configurable minimums may include:

- qualification and opportunity state;
- lead score;
- entity, domain, activity, and signal confidence;
- source diversity;
- freshness;
- operating status;
- permitted detection states;
- contradiction and quality-flag policy;
- manual review;
- responsible-function and contact verification.

Raw keyword counts are not eligibility or ranking criteria. `NOT_CRAWLED`, `CRAWL_FAILED`, `NOT_DETECTED`, `UNKNOWN`, and `ABSENT_CONFIRMED` remain separate.

## 9. Field groups

### Organization and entity identity

- canonical identifiers;
- legal and display names;
- entity type and operating state;
- website, locations, group relationships, and authorized identifiers.

### Market classification

- sectors and sector-pack versions;
- domains and activities;
- organization type;
- geography and offering fit;
- market-definition version.

### Opportunity and qualification

- qualification and opportunity state;
- score and dimensions;
- supporting and negative signals;
- capability, replacement, and integration relevance;
- rejection and exclusion reasons.

### Evidence

- evidence summaries and references;
- source classes and diversity;
- matched controlled profiles;
- permitted excerpts;
- event, collection, and verification dates;
- freshness, coverage, contradiction, duplicate-origin, and provenance data.

### People and contact routes

- responsible function and role evidence;
- person candidate where authorized;
- organization or person contact points;
- verification, consent, suppression, and channel eligibility.

### Operational metadata

- Harvest Job, output specification, schema, policy, model, and profile versions;
- generation, review, publication, and audit references.

Restricted payloads, credentials, secrets, and internal security configuration are never selectable. Contact fields remain excluded by default.

## 10. Evidence depth

### Summary

Identity, primary classification, qualification and opportunity state, top signals, confidence summary, critical warnings, and traceability references.

### Standard

Summary plus activities, score dimensions, source diversity, freshness, positive and negative evidence digest, contradiction summary, and approved contact fields.

### Full dossier

Standard plus the complete permitted evidence set, provenance, profile and query contribution, versions, quality flags, review decisions, and detailed rationale.

Full dossier never means unrestricted raw data.

## 11. Ordering and deduplication

Ordering may use opportunity value, pursuit readiness, offering fit, qualification, evidence confidence, source diversity, recency, geography, domain priority, activity priority, size, or material change.

The default result unit is one canonical organization or other selected lead subject. Branches, locations, people, contacts, and opportunities may appear as children without duplicating the master entity.

Update modes may include all eligible, new, materially changed, score-changed, review-required, or not previously published.

## 12. Destinations

Default destination: Harvester in-app results.

Optional destinations:

- Daily Selection workspace;
- governed CSV or JSON download;
- optional NEWAX Core adapter;
- optional Communicator adapter;
- approved signed webhook.

Every external destination requires authorization, field allowlists, schema versions, scoped credentials, idempotency, retries, dead letter, audit, and recoverable partial failure. Selecting Communicator does not initiate outreach. Selecting Core does not share private Harvester tables.

## 13. Scheduling and retention

Execution may be manual, immediate after approval, one-time scheduled, recurring, or event-triggered where separately supported.

Schedules respect timezone, recurrence, execution windows, blackout periods, source quotas, provider capacity, destination limits, and budget.

Completed outputs retain exact provider, offering, profile, market, taxonomy, keyword, source, scoring, policy, selected-field, destination, and schema versions. Later edits never rewrite history.

## 14. Preview and validation

Preview shows:

- output type and supporting artifacts;
- target, eligible estimate, hard cap, and concentration limits;
- thresholds and field groups;
- evidence depth;
- sort and tie-break order;
- deduplication and update mode;
- destination, format, schema, schedule, retention, cost, and warnings.

Blocking conditions include inactive providers or offerings, incomplete markets, missing source or evidence policy, unauthorized destinations, unavailable required fields, prohibited contact policy, exceeded hard limits, critical unresolved findings, and insufficient permissions.

Warnings never become silent approvals.

## 15. Lifecycle

```text
DRAFT
→ VALIDATING
→ CHANGES_REQUIRED or READY_FOR_REVIEW
→ IN_REVIEW
→ APPROVED
→ SCHEDULED or ACTIVE
→ PAUSED
→ SUPERSEDED
→ ARCHIVED
```

Drafts use optimistic concurrency. Review submissions and approved versions are immutable. Material changes create new versions. Every transition is tenant-scoped, permission-checked, and audited.

## 16. Planned data objects

```text
OutputSpecification
OutputEligibilityPolicy
OutputFieldSelection
OutputDestination
OutputSchedule
OutputPolicySnapshot
OutputGeneration
OutputPublication
```

These objects must reference immutable provider, offering, profile, market, evidence, scoring, contact, publication, and retention versions.

## 17. Planned API responsibilities

The final API follows repository conventions and may support:

```text
list output options
create and update drafts
validate and preview
submit for review
approve, activate, pause, and supersede
list immutable versions
generate governed results
list publication attempts
retry eligible failed publications
```

This document does not approve exact endpoint paths independently of runtime design.

## 18. Permissions

Separate permissions are required for viewing, drafting, reviewing, approving, activating, sensitive fields, destination configuration, generation, publication retry, and downloads.

Approval and destination administration remain separate capabilities.

## 19. Responsive and accessibility requirements

The complete flow must work from 320 CSS pixels through wide desktop, preserve all material controls on mobile, support keyboard-only operation, visible focus, accessible multi-selects, programmatic errors and counts, screen-reader announcements, non-color status cues, and no material horizontal overflow.

## 20. Security and compliance

- Every operation is tenant-scoped and audited.
- Sensitive fields require explicit permission.
- Suppressed routes cannot appear in contact-ready or outreach-candidate outputs.
- Downloads recheck authorization at generation and access time.
- Signed links are short-lived.
- External publication uses scoped credentials and replay-safe identities.
- Logs exclude unrestricted payloads and sensitive contact values.
- Destination outages cannot cause uncontrolled retries.
- Preview uses synthetic or authorized data.
- Public contact data does not imply outreach consent.

## 21. Acceptance criteria

Output Selection is complete only when:

- one primary output and compatible artifacts can be selected;
- quantity, hard cap, capacity, and estimated eligibility remain distinct;
- quality thresholds cannot be silently weakened;
- field groups disclose exact fields and enforce field permissions;
- evidence depth, ordering, deduplication, update mode, destinations, schemas, schedules, and retention are visible;
- preview explains blockers, warnings, exclusions, and estimated yield;
- submission, review, approval, activation, pause, and supersession are versioned and audited;
- tenant, permission, suppression, consent, destination, retry, responsive, accessibility, and exact-head tests pass;
- the real create-to-approved-generation workflow is verified.

## 22. Delivery boundary

This is a product and delivery specification. It does not implement database objects, migrations, APIs, React interfaces, estimators, schedules, exports, adapters, webhooks, scoring, qualification, publication, or outreach.
