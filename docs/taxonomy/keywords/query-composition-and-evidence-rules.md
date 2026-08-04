# Harvester Query Composition and Evidence Rules

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This document defines how domain, activity, signal, geography, role, and source keywords are composed into governed discovery plans.

The system must not submit one enormous query containing every selected term. Query families are generated separately, evaluated independently, and reconciled through the evidence graph.

## 1. Query layers

```text
Domain identity
+
Domain-specific activity
+
Lead-generation signal
+
Optional geography
+
Optional organization or role cue
+
Source-specific syntax
```

Each layer remains versioned and independently explainable.

## 2. Query families

| Query family | Purpose | Typical composition |
| --- | --- | --- |
| `QF-IDENTITY` | Discover organizations in an eligible domain | domain phrase + organization cue + geography |
| `QF-ACTIVITY` | Confirm what the organization does | organization/entity + activity phrase |
| `QF-TRIGGER` | Discover recent business events | domain/entity + launch, expansion, funding, hiring, tender, renewal, or compliance signal |
| `QF-PAIN` | Discover directly stated operational problems | entity/domain + reviewed pain phrase |
| `QF-PROCUREMENT` | Discover formal buying activity | domain/service context + RFP/RFQ/tender/procurement terms |
| `QF-TECHNOLOGY` | Discover existing software, devices, vendors, or integrations | entity + software/platform/device/integration phrase |
| `QF-ROLE` | Resolve likely responsible functions | entity + reviewed title/role phrases |
| `QF-CONTACT` | Find approved organizational contact routes | entity + official contact, procurement, vendor, or inquiry route |
| `QF-NEGATIVE` | Find closure, cancellation, award, suppression, or contradiction | entity/opportunity + negative profile |
| `QF-VERIFY` | Confirm an existing candidate or claim | exact entity + exact claim + authoritative source constraint |

## 3. Composition restrictions

1. A domain term alone may discover candidates but cannot qualify them.
2. Broad terms must be paired with organization, activity, entity, or source context.
3. Problem and buying-intent query families require an active offering and approved signal profile.
4. Decision-maker queries run only after entity resolution reaches the configured threshold.
5. Contact queries run only when the intended use has a lawful basis and the profile permits outreach preparation.
6. Negative queries run for every material positive opportunity to detect cancellations, awards, closure, suppression, or contradiction.
7. Query terms must use source-appropriate syntax and rate limits.
8. Search-engine snippets are discovery hints; the underlying page or authoritative record must be inspected before evidence is accepted.
9. Semantic retrieval may expand recall but must retain the originating canonical profile and explanation.
10. Regex is limited to reviewed structured identifiers, formats, or exact patterns; it is not a substitute for semantic understanding.

## 4. Evidence thresholds

| Evidence grade | Minimum pattern | Permitted use |
| --- | --- | --- |
| `E1-DIRECT` | One attributable direct inquiry, authoritative tender, explicit request, or official statement | May support confirmed or strongly indicated need subject to policy gates |
| `E2-AUTHORITATIVE` | One authoritative registry, regulator, official report, or procurement record | May support identity, event, compliance, scale, or operating-status claims |
| `E3-CORROBORATED` | Two independent sources supporting the same claim | May support strongly indicated opportunity or activity |
| `E4-INDIRECT` | One or more weak or circumstantial indicators | Research queue only; not contact-ready |
| `E5-INFERENCE` | Model or analyst inference without sufficient direct support | Must be labeled inference and normally requires human review |
| `E0-NONE` | No supporting evidence | No claim or score contribution |

Contradictory evidence is never discarded merely because positive evidence exists.

## 5. Freshness and lifecycle

- Direct inquiries: normally 30 days or provider-defined.
- Open procurement: until deadline, cancellation, or award.
- Hiring: normally 90 days.
- Launch and expansion: normally 180 days.
- Technology footprint: normally 365 days, with reverification before outreach.
- Compliance and recurring-service events: until obligation or service window expires.
- Organization and decision-maker contacts: reverification according to contact policy.

The underlying event date controls freshness where available. A newly crawled old page remains old evidence.

## 6. Duplicate and overlap controls

1. Resolve the organization before combining evidence from several sectors or domains.
2. Store one evidence item once and reference it from every relevant profile.
3. Detect mirrored pages, syndicated press releases, copied tenders, and directory replicas.
4. Separate one organization qualifying for several offerings from several duplicate leads.
5. Keep profile-specific fit, intent, and opportunity assessments separate even when they reuse evidence.

## 7. Scoring inputs

Keyword results may contribute only to bounded dimensions:

- domain fit;
- activity fit;
- event or trigger strength;
- expressed intent;
- operational-problem evidence;
- technology footprint;
- scale and strategic fit;
- decision-maker confidence;
- contactability;
- evidence coverage and freshness.

A raw keyword count is never a lead score.

## 8. Example

```text
Provider offering
Warehouse management system

Target
Pharmaceutical distributors operating cold-chain warehouses in Punjab

Queries
QF-IDENTITY: pharmaceutical distributor + supplier/distributor cue + Punjab
QF-ACTIVITY: resolved entity + warehousing/cold storage/distribution
QF-TRIGGER: resolved entity + expansion/tender/hiring/warehouse opening
QF-PAIN: resolved entity + inventory mismatch/expiry/manual dispatch/temperature excursion
QF-TECHNOLOGY: resolved entity + WMS/ERP/barcode/cold-chain monitoring
QF-ROLE: resolved entity + warehouse/logistics/IT/procurement roles
QF-NEGATIVE: resolved entity + closed/cancelled/awarded/no longer operating
```

The example does not prove a gap. It defines a reproducible evidence plan.

## 9. Acceptance criteria

- Query families remain independently explainable.
- Negative and verification queries accompany positive discovery.
- Evidence thresholds are explicit and do not rely on raw match counts.
- Event freshness uses the underlying event date where possible.
- Duplicate source origins do not inflate corroboration.
- Decision-maker and contact queries run only after the appropriate gates.
- Runtime implementation is not falsely claimed.
