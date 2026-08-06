# Harvester News and Media Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how licensed news APIs, publisher feeds, public publisher pages, press releases, customer-authorized monitoring exports, and manual references enter Harvester.

News and media records can support event, timing, expansion, funding, leadership, outage, regulatory and reputation evidence. Publisher content remains copyrighted and may contain errors, opinion, duplication or unverified claims.

## 2. Source modes

```text
NEWS_API_LICENSED
NEWS_FEED_PUBLIC_OR_LICENSED
NEWS_PUBLISHER_PUBLIC_PAGE
PRESS_RELEASE_PUBLIC
NEWS_MONITORING_AUTHORIZED_EXPORT
NEWS_OPERATOR_REFERENCE
```

## 3. User configuration

```text
provider_code
mode
credential_or_connection_reference_id
license_profile_id
publisher_allowlist
publisher_blocklist
queries
organization_filters
person_filters
event_filters
language_filters
country_filters
publication_window
freshness_window
maximum_pages
request_budget
retention_policy_version
quotation_policy_version
operator_review_requirement
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Article | Provider article ID or canonical URL | Event and claim evidence |
| Publisher | Provider publisher ID or domain | Source-quality context |
| Feed entry | Feed and entry ID | Update discovery |
| Press release | Release ID or canonical URL | Organization-authored announcement |
| Topic or entity | Provider entity ID | Source-native classification |
| Monitoring export row | Customer external ID | Authorized historical evidence |
| Operator reference | Publisher URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = NEWS_MEDIA
source.mode = selected news mode
native.object_type = article | feed_entry | press_release | publisher | export_row
native.object_id = provider ID or canonical URL
native.url = canonical publisher URL
entity_hints.organization_names = named organizations with extraction provenance
entity_hints.person_names = named persons with extraction provenance
entity_hints.domains = publisher and subject domains kept separately
content.title = article or release title
content.summary = licensed summary or Harvester-generated bounded summary
content.body_ref = licensed or permitted artifact reference only
content.published_at = publisher date
signals.event_types = funding, acquisition, expansion, hiring, leadership, outage, partnership, regulatory or closure events
quality = publisher quality, corroboration, recency and conflict flags
```

## 6. Example article envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "NEWS_MEDIA", "mode": "NEWS_API_LICENSED"},
  "native": {"object_type": "article", "object_id": "article-123", "url": "https://publisher.example/article-123"},
  "entity_hints": {
    "organization_names": ["Example Energy Company"],
    "provider_identifiers": [{"type": "NEWS_ARTICLE_ID", "value": "article-123"}]
  },
  "content": {
    "title": "Example Energy Company announces new solar facility",
    "summary": "Licensed summary reports a planned facility expansion; independent verification required.",
    "language": "en",
    "published_at": "2026-08-01T06:00:00Z",
    "content_type": "news_article"
  },
  "signals": {"event_types": ["EXPANSION_ANNOUNCEMENT"]},
  "quality": {"completeness": "PARTIAL", "freshness": "CURRENT", "review_required": true, "conflict_flags": []},
  "policy": {
    "authorization_basis": "LICENSED_API",
    "retention_policy": "NEWS_LICENSE_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
NEWS_SUCCESS
NEWS_ZERO_RESULTS
NEWS_DUPLICATE_SYNDICATION
NEWS_ARTICLE_REMOVED
NEWS_PAYWALL_OR_RESTRICTED
NEWS_PUBLISHER_BLOCKED
NEWS_DATE_AMBIGUOUS
NEWS_LANGUAGE_UNSUPPORTED
NEWS_RATE_LIMITED
NEWS_LICENSE_BLOCKED
NEWS_QUOTATION_LIMIT_REACHED
NEWS_POLICY_BLOCKED
```

## 8. Copyright and provenance

- Store identifiers, URLs, titles, dates, publisher, licensed summaries and bounded excerpts only as permitted.
- Do not store or reproduce full copyrighted articles without authorization.
- Press releases remain organization-authored claims and are labeled separately from independent reporting.
- Syndicated copies must not inflate signal diversity.
- Material events require corroboration from independent or official sources when practical.
- Quotation limits and source attribution remain attached to every observation.

## 9. Evidence boundaries

News may support event timing, public announcements, reputation context, expansion, funding, leadership, regulatory and operational events.

It does not independently prove legal facts, service gaps, buying authority, budget, current operational state, contact consent or a qualified opportunity.

## 10. Delivery boundary

This document does not implement news providers, feeds, publisher crawling, deduplication, copyright controls, corroboration, retention or scoring.