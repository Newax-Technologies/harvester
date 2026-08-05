# Harvester Source Specification: Social Platforms

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-SOCIAL`**

## 1. Purpose

Use permitted public or customer-authorized social content as bounded evidence for official announcements, service updates, events, recruitment, campaigns, public inquiry routes, and product or facility context.

## 2. Approved source boundary

- Official organization accounts.
- Customer-authorized account data.
- Licensed APIs and permitted public posts.
- Provider terms, authorization, access mode, and jurisdiction govern collection.
- User comments and follower data receive lower authority and stricter privacy review.

## 3. Strong signal uses

- An announcement or service update from a verified or independently resolved official account.
- Customer-authorized account activity and analytics within approved scopes.
- Official public service or inquiry route.

## 4. Secondary signal uses

- Launch, event, recruitment, seasonal activity, branch, product, service, and facility signals.
- Public customer-service pressure or operational interruption when independently corroborated.

## 5. Weak or unsupported inferences

- Informal language and abbreviated context increase ambiguity.
- Account impersonation and ownership changes are possible.
- Comments, reactions, follower counts, and popularity are weak evidence.
- Public activity does not prove budget, capability, quality, authority, or buying intent.
- Private messages and comments are not public evidence unless lawfully authorized and necessary.

## 6. Source fields and evidence targets

- platform, account identifier, account URL, and ownership evidence
- source mode and authorization scope
- post identifier, text, media metadata, public links, and referenced entities
- publication, update, deletion, event, and retrieval dates

## 7. Keyword and query inputs

- resolved official account and organization
- selected domain and approved activity
- service, event, facility, recruitment, launch, and public-route terms
- active provider-offering event and intent profiles only when allowed
- deleted, corrected, postponed, cancelled, fake, unofficial, or impersonation terms

## 8. Governed query templates

```text
<official account> + <domain/activity/event>
<organization> + branch/service/product launch
<organization> + recruitment/event/service update
<post or campaign> + cancelled/postponed/corrected
```

## 9. Inspection sequence

1. Resolve account ownership before using content.
2. Prefer official or customer-authorized content.
3. Capture post context, links, media, and event dates.
4. Separate official statement, public comment, allegation, and engagement metric.
5. Check deletion, correction, cancellation, impersonation, and later updates.

## 10. Required provenance

- platform, source mode, account identifier, and authorization basis
- post identifier, canonical URL, matched text or media location
- publication, update, deletion, event, and retrieval dates
- account-resolution evidence and retention policy
- contributing domain, activity, offering, signal, and source-profile versions

## 11. Freshness and event time

Social evidence is highly time-sensitive. Deleted, edited, corrected, scheduled, ephemeral, and event-based content must remain distinguishable.

## 12. Duplication and corroboration

Cross-posts, reposts, screenshots, shared campaigns, and syndicated announcements must resolve to the originating account or statement.

## 13. Privacy, authorization, and compliance

- Use only public or authorized content under provider and jurisdiction rules.
- Do not mine comments or follower graphs for sensitive or private inferences.
- Do not automate engagement or messaging without separate approval.
- Public route availability does not override consent or suppression.

## 14. Non-detection and failure states

- `SOCIAL_POST_DETECTED`
- `SOCIAL_POST_NOT_DETECTED`
- `SOCIAL_ACCOUNT_UNRESOLVED`
- `SOCIAL_AUTHORIZATION_MISSING`
- `SOCIAL_ACCESS_RESTRICTED`
- `SOCIAL_INSPECTION_FAILED`
- `SOCIAL_POST_DELETED_CORRECTED_OR_CONTRADICTED`

## 15. Acceptance criteria

- Account ownership and source mode are retained.
- Official statements remain separate from public comments and metrics.
- Deleted, edited, corrected, and cancelled states are checked.
- Reposts and screenshots do not inflate corroboration.
- Provider restrictions override keyword configuration.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Authorized Professional Networks](authorized-professional-networks.md).
- [Decision-Maker and Contact-Cue Registry](../decision-maker-and-contact-cues.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement social-provider credentials, APIs, collection, storage, engagement, classifiers, scoring, or contact workflows.
