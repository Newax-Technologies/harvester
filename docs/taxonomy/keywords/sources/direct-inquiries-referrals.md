# Harvester Source Specification: Direct Inquiries and Referrals

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-DIRECT`**

## 1. Purpose

Use direct organization inquiries, user-authorized referrals, event conversations, and approved relationship introductions as high-value expressed-need evidence while separately verifying identity, authority, fit, scope, and contact permission.

## 2. Approved source boundary

- Inbound forms, emails, calls, and meetings.
- Authorized referrals and customer-approved introductions.
- Operator-entered notes and attachments.
- The interaction record must preserve channel, origin, permission, scope, and participants.

## 3. Strong signal uses

- Expressed need, problem, objective, urgency, requested scope, and preferred route.
- Interaction-specific contact permission.
- Referral relationship and introduction context when authorized.
- Organization-provided current operational context.

## 4. Secondary signal uses

- Qualification, prioritization, timeline, constraints, and next-step routing.
- Responsible-function and buying-stage context.
- Provider-offering relevance and relationship history.

## 5. Weak or unsupported inferences

- The contact may lack authority or complete information.
- A referral may be outdated, incomplete, biased, or unauthorized for further sharing.
- Interest does not guarantee budget, fit, approval, or procurement route.
- Free-text statements may contain sensitive or unverified information.
- Permission for one interaction does not create unlimited channel consent.

## 6. Source fields and evidence targets

- interaction identifier, channel, date, origin, participants, organization, and relationship
- expressed problem, objective, scope, urgency, timeline, and next step
- voluntarily provided budget state where appropriate
- contact permission, consent, suppression, conflict, jurisdiction, and preferred route
- operator notes, attachments, referral basis, and verification state

## 7. Keyword and classification inputs

- selected domain and approved activity
- active provider-offering problem, intent, scope, buying-stage, contradiction, and qualification profiles
- role, authority, contact-route, suppression, conflict, and consent controls

Direct sources use extraction and classification profiles rather than public-discovery queries.

## 8. Governed mapping templates

```text
Inbound form field → canonical inquiry field
Meeting or call note → attributed statement + context
Referral → referrer + referred party + authorized scope
Expressed need → offering-specific problem or intent profile
```

## 9. Inspection sequence

1. Verify organization and participant identity.
2. Record the exact expressed need, requested scope, and source context.
3. Separate participant role, functional responsibility, decision authority, and contact permission.
4. Check suppression, conflict, jurisdiction, procurement, and channel rules.
5. Qualify fit without converting enthusiasm into certainty.

## 10. Required provenance

- interaction, channel, origin, participants, and operator
- date, event time, organization, attributed statements, and attachments
- consent, permission, suppression, conflict, and referral authorization
- matched domain, activity, offering, problem, intent, qualification, and source-profile versions

## 11. Freshness and event time

Need, authority, urgency, contact permission, and status require revalidation as the interaction ages. Interaction time, follow-up time, withdrawal time, and last verification remain separate.

## 12. Duplication and corroboration

Repeated submissions, forwarded messages, meeting notes, CRM copies, and referral records must link to one interaction or relationship timeline.

## 13. Privacy, authorization, and compliance

- Collect only necessary information for the approved inquiry or referral purpose.
- Protect sensitive notes and attachments through tenant and role controls.
- Consent and permission are channel- and purpose-specific.
- Honor withdrawal, suppression, deletion, and conflict requirements.

## 14. Non-detection and failure states

- `DIRECT_INQUIRY_VERIFIED`
- `DIRECT_INQUIRY_UNVERIFIED`
- `DIRECT_INQUIRY_DUPLICATE`
- `DIRECT_INQUIRY_SUPPRESSED_OR_CONFLICTED`
- `REFERRAL_AUTHORIZATION_MISSING`
- `DIRECT_IDENTITY_OR_AUTHORITY_UNRESOLVED`
- `DIRECT_FOLLOWUP_PERMISSION_EXPIRED_OR_WITHDRAWN`

## 15. Acceptance criteria

- Interaction origin and participants are retained.
- Need, role, authority, fit, and permission remain separate.
- Referrals preserve authorization scope.
- Consent and suppression are enforced independently of opportunity quality.
- Duplicate records link to one interaction timeline.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Decision-Maker and Contact-Cue Registry](../decision-maker-and-contact-cues.md).
- [Provider-Offering Keyword Profile Standard](../provider-offering-keyword-profile-standard.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement forms, email or call ingestion, referral workflows, storage, consent enforcement, qualification, scoring, or follow-up.
