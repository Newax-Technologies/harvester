# Harvester X Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**  
External-reference review: **X API v2 access plans, endpoints, fields, pricing and retention rules must be revalidated before implementation**

## 1. Purpose

This document defines how permitted X API records, customer-authorized account data, licensed search results, webhooks or streams, authorized imports, and manual operator references may enter Harvester.

Harvester must not scrape `x.com`, automate browser sessions, reuse login cookies, bypass API access plans, or treat public posts as unrestricted reusable data.

## 2. Source modes

```text
X_PUBLIC_API_SEARCH
X_ACCOUNT_AUTHORIZED
X_STREAM_AUTHORIZED
X_AUTHORIZED_IMPORT
X_OPERATOR_REFERENCE
```

## 3. User configuration

```text
mode
credential_reference_id
connection_reference_id
approved_access_plan
approved_scopes
user_ids
usernames
search_query_profile_version
search_window
language_filters
geography_filters
expansions
post_fields
user_fields
media_fields
maximum_results
maximum_pages
stream_rule_version
request_budget
cost_budget
retention_policy_version
attribution_policy_version
```

Search operators and field expansions must be frozen in the source plan so results can be reproduced and costed.

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| User | X user ID | Account and organization-person hint |
| Post | Post ID | Public statement, event or activity evidence |
| Mention | Post ID plus referenced user | Relationship or event hint |
| Media | Media key | Supporting content reference |
| Place | Place ID | Source-native location hint |
| Search page | Query plus pagination token | Query and coverage outcome |
| Stream event | Rule and Post ID | Near-real-time event observation |
| Authorized import row | Customer external ID | Licensed or customer-owned historical record |
| Operator reference | X URL | Manual navigation and bounded assertion |

## 5. Canonical formatting

### User observation

```text
source.code = X
source.mode = selected X mode
native.object_type = user
native.object_id = X user ID
native.url = profile URL derived from username
entity_hints.organization_names = account name only when organization evidence supports it
entity_hints.person_names = account name only when person evidence supports it
entity_hints.domains = expanded profile URL domains when permitted
entity_hints.provider_identifiers = X user ID and username
quality.review_required = true for role, organization and parody ambiguity
```

### Post observation

```text
native.object_type = post
native.object_id = Post ID
native.parent_id = author user ID
content.summary = permitted Post text or bounded excerpt
content.published_at = created_at
content.language = provider language field
entity_hints.provider_identifiers = author and referenced object IDs
signals.keyword_matches = versioned query and taxonomy matches
signals.event_types = hiring, expansion, launch, outage, partnership or operational announcement hypotheses
```

## 6. Example post envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "X", "mode": "X_PUBLIC_API_SEARCH"},
  "native": {
    "object_type": "post",
    "object_id": "1900000000000000000",
    "parent_id": "1800000000000000000",
    "url": "https://x.com/example/status/1900000000000000000"
  },
  "entity_hints": {
    "organization_names": ["Example Logistics"],
    "provider_identifiers": [
      {"type": "X_USER_ID", "value": "1800000000000000000"},
      {"type": "X_POST_ID", "value": "1900000000000000000"}
    ]
  },
  "content": {
    "summary": "Public post announced hiring for warehouse systems roles.",
    "language": "en",
    "published_at": "2026-08-01T09:00:00Z",
    "content_type": "post"
  },
  "signals": {
    "event_types": ["HIRING_SIGNAL"],
    "job_roles": ["warehouse systems manager"]
  },
  "policy": {
    "authorization_basis": "PUBLIC_API",
    "retention_policy": "X_ACCESS_PLAN_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
X_SUCCESS
X_ZERO_RESULTS
X_PARTIAL_SEARCH_WINDOW
X_QUERY_INVALID
X_OPERATOR_UNAVAILABLE
X_ACCESS_PLAN_INSUFFICIENT
X_RATE_LIMITED
X_COST_LIMIT_REACHED
X_TOKEN_EXPIRED
X_REAUTHORIZATION_REQUIRED
X_POST_DELETED
X_USER_SUSPENDED
X_PROTECTED_ACCOUNT
X_STREAM_DISCONNECTED
X_STREAM_RULE_REJECTED
X_POLICY_BLOCKED
```

Deleted posts, suspended users, inaccessible objects, and protected-account responses remain distinct.

## 8. Retention and compliance

- Store only fields permitted by the active X access plan and agreement.
- Preserve Post and user identifiers, observation time, query, requested fields, expansions, and provider response state.
- Recheck deletion or suspension requirements where the contract requires compliance refreshes.
- Do not train models on X content unless the active agreement explicitly permits it.
- Operator references do not authorize automated opening or extraction.
- Public posts remain source-authored claims and may be promotional, mistaken, satirical, impersonated, or stale.

## 9. Evidence boundaries

X may support public announcements, hiring, operational events, organization activity, role hints, and customer-authorized account intelligence.

It cannot independently prove legal identity, procurement authority, budget, service absence, consent to outreach, or a qualified opportunity.

## 10. Delivery boundary

This document does not implement X API access, search, streaming, OAuth, token storage, deletion compliance, source parsing, evidence extraction, or scoring.