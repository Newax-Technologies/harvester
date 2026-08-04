# Harvester Bing Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**  
External-reference review: **Microsoft's currently available Bing Search, Grounding with Bing, Bing Custom Search, usage, display, and licensing terms must be confirmed before implementation**

## 1. Purpose

This document defines how permitted Bing web, news, custom-search, grounding, and operator-reference results may enter Harvester.

Bing is primarily a discovery and research-path source. Search snippets and rankings are not permanent proof of an organization's claims, complete market coverage, or website contents.

## 2. Source modes

```text
BING_WEB_SEARCH_LICENSED
BING_NEWS_SEARCH_LICENSED
BING_CUSTOM_SEARCH_LICENSED
BING_GROUNDING_RESPONSE
BING_OPERATOR_REFERENCE
```

A mode may be activated only when the corresponding Microsoft product and agreement are actually available to NEWAX. Historical SDK documentation does not itself create current production access.

## 3. User configuration

```text
mode
credential_or_connection_reference_id
contract_profile_id
query_profile_version
query_terms
market
language
safe_search
freshness
count
maximum_pages
custom_search_instance
allowed_domains
blocked_domains
request_budget
cost_budget
citation_policy_version
retention_policy_version
operator_review_requirement
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Web result | Provider result URL plus position | Website discovery path |
| News result | Article URL plus provider metadata | News and event discovery path |
| Custom-search result | URL plus configured instance | Bounded-domain discovery |
| Grounded citation | Citation URL plus response reference | Research provenance |
| Search page | Query, offset and response ID | Coverage and query outcome |
| Operator reference | Bing result or search URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = BING
source.mode = selected Bing mode
native.object_type = web_result | news_result | grounded_citation | search_page
native.object_id = response ID + result position, or stable provider identifier when supplied
native.url = result URL
content.title = provider result title
content.summary = provider snippet or bounded citation text
content.published_at = provider date for news when supplied
entity_hints.domains = domain extracted from result URL
signals.keyword_matches = query and taxonomy matches
quality.completeness = PARTIAL
quality.review_required = true
policy.authorization_basis = LICENSED_API | CUSTOMER_CONNECTION | MANUAL_OPERATOR_REFERENCE
```

Search results should normally hand off to the organization website, official registry, news publisher, or another independently fetched source. The target page becomes a separate observation.

## 6. Example result envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "BING", "mode": "BING_WEB_SEARCH_LICENSED"},
  "native": {
    "object_type": "web_result",
    "object_id": "response-123:4",
    "url": "https://example.pk/about"
  },
  "entity_hints": {"domains": ["example.pk"]},
  "content": {
    "title": "Example Manufacturing Company",
    "summary": "Search-result snippet; requires direct-page verification.",
    "language": "en",
    "content_type": "search_result"
  },
  "quality": {
    "completeness": "PARTIAL",
    "freshness": "UNKNOWN",
    "review_required": true,
    "conflict_flags": []
  },
  "policy": {
    "authorization_basis": "LICENSED_API",
    "retention_policy": "BING_PRODUCT_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
BING_SUCCESS
BING_ZERO_RESULTS
BING_PARTIAL_RESULTS
BING_MARKET_UNSUPPORTED
BING_QUERY_REJECTED
BING_SAFE_SEARCH_FILTERED
BING_RATE_LIMITED
BING_QUOTA_EXHAUSTED
BING_CONNECTION_UNAVAILABLE
BING_PRODUCT_UNAVAILABLE
BING_DISPLAY_REQUIREMENT_UNMET
BING_CITATION_MISSING
BING_POLICY_BLOCKED
```

## 8. Retention and citations

- Store query, market, language, freshness, result position, URL, response identifier, and observation time when permitted.
- Search snippets and grounded response text follow the active product's storage and display rules.
- Citations and search-query links must be preserved when the product requires them.
- Directly fetched target pages create separate `WEBSITE` or `NEWS_MEDIA` observations.
- Ranking position is provider context, not evidence of organization quality or importance.

## 9. Evidence boundaries

Bing may support website discovery, news discovery, source-diversity expansion, and operator research.

It cannot independently prove page contents, organization identity, complete market coverage, service absence, buying intent, or contact permission.

## 10. Delivery boundary

This document does not implement Microsoft connections, searches, grounding, custom-search instances, citation rendering, target-page crawling, retention enforcement, or scoring.