# Harvester Organization Website Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Current website crawler is partial; target governed format is not fully implemented**

## 1. Purpose

This document defines how publicly accessible organization-owned websites, permitted pages, sitemaps, structured data, documents, feeds, and customer-authorized private website areas enter Harvester.

Organization websites are often the strongest source for self-asserted services, locations, leadership, policies, contact paths and operational claims. They remain organization-authored claims and may be incomplete, stale or promotional.

## 2. Source modes

```text
ORGANIZATION_WEBSITE_PUBLIC
ORGANIZATION_WEBSITE_AUTHORIZED
ORGANIZATION_SITEMAP_PUBLIC
ORGANIZATION_FEED_PUBLIC
ORGANIZATION_DOCUMENT_PUBLIC
WEBSITE_OPERATOR_REFERENCE
```

## 3. User configuration

```text
mode
seed_urls
allowed_domains
allowed_subdomains
blocked_paths
robots_policy
sitemap_policy
feed_policy
maximum_depth
maximum_pages
maximum_response_bytes
content_types
language_filters
freshness_window
rendering_policy
javascript_policy
login_connection_reference
request_budget
crawl_delay
retention_policy_version
document_policy
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Domain | Normalized domain | Organization-owned source boundary |
| Web page | Canonical URL | Page-level evidence |
| Sitemap entry | URL plus last-modified value | Discovery path |
| Feed entry | Feed and entry ID | Announcement or update evidence |
| Structured-data object | Page URL plus object index or ID | Organization, location, product, job or event hint |
| Downloaded document | URL plus checksum | Policy, report, brochure, filing or tender evidence |
| Fetch attempt | URL plus request time | Coverage and failure evidence |

## 5. Canonical formatting

```text
source.code = WEBSITE
source.mode = selected website mode
native.object_type = domain | page | feed_entry | structured_data | document | fetch_attempt
native.object_id = canonical URL or checksum-backed object ID
native.url = requested or final URL
entity_hints.organization_names = page title, structured organization names and verified branding
entity_hints.person_names = leadership or contact names with page provenance
entity_hints.domains = normalized source domain
entity_hints.emails = published business contact addresses
entity_hints.phones = published business phone numbers
entity_hints.addresses = published locations
content.title = page or document title
content.summary = bounded extracted summary
content.body_ref = retained HTML, text or document artifact reference when policy permits
signals.domain_codes = domain keyword and semantic matches
signals.activity_codes = activity evidence extracted from page text
signals.service_codes = only active provider-service target matches
signals.event_types = hiring, branch, procurement, launch, partnership, outage or policy events
```

## 6. Example page envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "WEBSITE", "mode": "ORGANIZATION_WEBSITE_PUBLIC"},
  "native": {
    "object_type": "page",
    "object_id": "https://example.pk/services/distribution",
    "url": "https://example.pk/services/distribution",
    "payload_ref": "artifact://website/page/sha256-example",
    "payload_hash": "sha256:example"
  },
  "entity_hints": {
    "organization_names": ["Example Pharmaceuticals"],
    "domains": ["example.pk"],
    "emails": ["info@example.pk"],
    "phones": ["+92510000000"]
  },
  "content": {
    "title": "Pharmaceutical Distribution",
    "summary": "The organization states that it distributes pharmaceutical products nationwide.",
    "language": "en",
    "published_at": null,
    "content_type": "web_page"
  },
  "signals": {
    "domain_codes": ["HC-MED-001"],
    "activity_codes": ["ACT-LOG-001"],
    "keyword_matches": ["pharmaceutical distribution"]
  },
  "policy": {
    "authorization_basis": "PUBLIC_WEBSITE_WITH_ROBOTS_COMPLIANCE",
    "retention_policy": "WEBSITE_CONTENT_POLICY",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
WEBSITE_SUCCESS
WEBSITE_NO_RELEVANT_CONTENT
WEBSITE_ROBOTS_DISALLOWED
WEBSITE_HTTP_ERROR
WEBSITE_REDIRECT_LOOP
WEBSITE_NON_HTML_CONTENT
WEBSITE_RESPONSE_TOO_LARGE
WEBSITE_UNSUPPORTED_CONTENT_TYPE
WEBSITE_JAVASCRIPT_REQUIRED
WEBSITE_LOGIN_REQUIRED
WEBSITE_RATE_LIMITED
WEBSITE_TIMEOUT
WEBSITE_TLS_FAILED
WEBSITE_MALWARE_BLOCKED
WEBSITE_PARSING_FAILED
WEBSITE_DUPLICATE_CONTENT
```

## 8. Crawling and evidence rules

- Respect robots directives, terms, crawl delays and legal restrictions.
- Preserve requested URL, final URL, status, content type, checksum, fetch time and failure reason.
- Canonicalization and duplicate detection must not erase distinct historical evidence.
- Structured data is source-authored and requires corroboration for material claims.
- Search-engine snippets do not substitute for fetching the target page.
- Missing pages or terms remain `NOT_DETECTED`; coverage and absence rules apply separately.
- Documents require size, type, malware, extraction and retention controls.

## 9. Evidence boundaries

Organization websites may strongly support organization identity, service domains, activities, locations, leadership, contact paths and public announcements.

They do not independently prove legal registration, current operational performance, truthful claims, service absence, buying intent, budget or contact consent.

## 10. Delivery boundary

This document does not complete the website crawler, document pipeline, rendering, structured-data parser, retention policy, evidence extraction or scoring.