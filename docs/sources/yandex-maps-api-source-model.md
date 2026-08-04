# NEWAX Harvester Yandex Maps API Source and Extraction Model

Status: **Normative planned source architecture**  
Source family: **Yandex Places API public organization discovery and customer-authorized Yandex Business exports**  
Document version: **v1**  
Implementation state: **Current Yandex connector is partial and must remain restricted for production persistence until licensing compatibility is confirmed**  
Last external-reference review: **2026-08-03**  

Authority: This document defines how NEWAX Harvester should plan, call, extract, verify, cache, explain, and use Yandex Maps and Yandex Business information. It does not create a second roadmap and does not claim that the current runtime already follows this model.

Read with:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [NEWAX Harvester Opportunity Scoring Model v3](../architecture/opportunity-scoring-model-v3.md)
- [Standalone Product and Integration Framework](../architecture/standalone-product-and-integration-framework.md)
- [Google API Source and Extraction Model](google-api-source-model.md)

Official references reviewed for this version:

- Yandex Places API overview: <https://yandex.com/maps-api/docs/geosearch-api/index.html>
- Request format: <https://yandex.com/maps-api/docs/geosearch-api/request.html>
- Response format: <https://yandex.com/maps-api/docs/geosearch-api/response.html>
- Examples: <https://yandex.com/maps-api/docs/geosearch-api/examples.html>
- Commercial Organization Search description: <https://yandex.com/dev/commercial/doc/en/concepts/geosearch>
- Places API terms: <https://yandex.com/dev/tariffs/doc/en/geosearch/terms/>
- Maps API service agreement: <https://yandex.com/legal/maps_api_service_agreement/en/>
- Free-use restrictions: <https://yandex.com/dev/commercial/doc/en/>
- Yandex Business reviews: <https://yandex.com/support/business-priority/en/manage/reviews>
- Yandex Business statistics: <https://yandex.com/support/business-priority/en/manage/general-statistics>

---

## 1. Purpose

Yandex Maps can help Harvester discover organizations and branches, obtain structured public business attributes, and identify independent research paths.

Yandex Business can also provide customer-authorized operational statistics and profile information when the customer controls the organization profile and supplies an authorized export.

Neither source may become an ungoverned copy of Yandex data inside Harvester.

This document answers:

1. Which Yandex source modes Harvester may use.
2. What the current connector does and where it is incomplete.
3. How a market definition becomes a Yandex source plan.
4. How geographic search should use `bbox`, `ll`, `spn`, and `rspn`.
5. How organization queries, phone queries, service queries, and exact verification queries should be generated.
6. How result paging and saturated searches should be handled.
7. Which documented response fields may be parsed.
8. Which undocumented fields must be ignored.
9. How websites, phones, categories, hours, and accessibility features should be interpreted.
10. Why no Yandex field may prove the absence of internal business infrastructure.
11. How Yandex results should hand off to independent website and registry research.
12. How reviews, photos, posts, and profile statistics may or may not be used.
13. How licensing, caching, attribution, display, and deletion obligations constrain the architecture.
14. How Yandex evidence may influence Opportunity Scoring Model v3.
15. What must be implemented and verified before production activation.

The goal is not to recreate Yandex Maps in Harvester.

The goal is to use permitted Yandex capabilities as bounded discovery signals while preserving Harvester's evidence integrity, customer control, and long-term ownership of independently verified information.

---

## 2. Locked source boundary

Harvester must separate three Yandex modes.

```text
YANDEX_PLACES_TRANSIENT
YANDEX_BUSINESS_AUTHORIZED_EXPORT
YANDEX_MAPS_OPERATOR_LINK
```

### 2.1 `YANDEX_PLACES_TRANSIENT`

This mode uses the official Yandex Places HTTP API to search for businesses or geographical objects.

Primary role:

```text
Discover a possible organization or branch
→ receive temporary Yandex search data
→ identify independent research paths
→ verify through organization-owned or otherwise permitted sources
→ expire Yandex-derived cached content
```

It is not a permanent lead-data source by default.

### 2.2 `YANDEX_BUSINESS_AUTHORIZED_EXPORT`

This mode handles data exported by a customer from a Yandex Business profile the customer is authorized to manage.

Possible customer-authorized inputs may include:

- Profile statistics exported to Excel
- Traffic to the organization profile
- Routes built
- Call-button clicks
- Website traffic
- Direct and discovery traffic
- Customer-supplied review exports or summaries where permitted
- Customer-owned profile data

This is an authorized import workflow, not public scraping and not the same as the Places API.

The import must retain:

```text
authorization_reference
account_owner
business_profile_reference
exported_at
source_period
file_hash
imported_at
retention_policy
customer_deletion_policy
```

### 2.3 `YANDEX_MAPS_OPERATOR_LINK`

Harvester may retain or generate a permitted link that lets an operator open a relevant location in Yandex Maps when the applicable terms allow it.

The link is for navigation and human review.

It is not permission for Harvester to crawl the Yandex Maps website.

---

## 3. Locked prohibitions

Harvester must not:

- Scrape `yandex.com/maps` or another Yandex Maps website.
- Use browser automation to copy organization cards.
- Intercept private or undocumented Yandex endpoints.
- Copy reviews, ratings, photos, posts, or profile content from the public Maps website.
- Depend on undocumented fields returned by the Places API.
- Persist Places API responses beyond the licensed cache period.
- Reorder, modify, hide, or republish Yandex search results contrary to applicable terms.
- Present Yandex data without required attribution and map-display conditions.
- Treat zero results as confirmed absence.
- Treat a missing website as confirmed website absence.
- Treat a missing phone as confirmed lack of contactability.
- Treat an omitted feature as proof that a capability does not exist.
- Train models on Yandex content without explicit written permission.
- Use a free Maps API license for a closed, resold, or commercial Harvester workflow.
- bypass contractual restrictions merely because the API technically returns JSON.

A browser pretending to be a user remains a scraper. Adding JavaScript does not confer legal wisdom.

---

## 4. Licensing and production gate

### 4.1 Standard free-use incompatibility

Yandex's published free-use conditions state that free use is intended for openly accessible projects, cannot be used for solutions developed for resale, and prohibits storing or changing API data.

Harvester is a standalone enterprise product and may be resold or deployed in closed customer systems.

Therefore:

```text
Free-use key
→ development exploration only where permitted
→ not production Harvester authorization
```

### 4.2 Organization Search commercial limitation

Yandex's commercial Organization Search page states that only a basic license is available and that saving or modifying data received from the API is prohibited.

The Places API terms published by Yandex permit temporary caching for up to thirty calendar days for internal performance purposes, then require removal when the service term ends. They also place display, attribution, map-background, and result-order obligations on the customer.

The exact agreement governing NEWAX may differ by territory, contract, product, and commercial arrangement.

Therefore the production gate is:

```text
Written license and terms review
→ approved usage profile
→ approved fields
→ approved cache duration
→ approved display behavior
→ approved derived-data behavior
→ approved independent-verification workflow
→ production activation
```

### 4.3 Current connector restriction

The current runtime stores the complete Yandex response in an append-only `RawSourceRecord` without an automatic thirty-day expiry.

Until the connector is redesigned and the license is approved:

```text
YANDEX connector status = RESTRICTED
```

It must not be enabled for production lead harvesting merely because an API key exists.

### 4.4 Contract profile

Every Yandex connection must reference a versioned compliance profile:

```text
YandexComplianceProfile

contract_reference
territory
permitted_products
permitted_use_cases
permitted_users
permitted_fields
cache_duration_days
persistent_identifiers_allowed
independent_derivation_allowed
public_display_allowed
closed_system_allowed
result_reranking_allowed
map_display_required
attribution_text
attribution_layout_reference
delete_on_termination
export_allowed
model_training_allowed
reviewed_by
reviewed_at
expires_at
```

No default policy should assume broad storage rights.

---

## 5. Current runtime implementation

The current connector uses:

```text
GET https://search-maps.yandex.ru/v1/
```

with:

```text
apikey=<configured key>
text=<free-text query>
lang=en_US
type=biz
results=20 by default, maximum 50
```

The connector:

1. Receives one text query.
2. Calls the Yandex Places API synchronously through `httpx`.
3. Parses the returned `FeatureCollection`.
4. Returns only `features`.
5. Catches all HTTP errors.
6. Prints an error.
7. Returns an empty list.

The pipeline reuses the same current pseudo-tiling logic used by other map connectors:

```text
configured city + configured zone
→ text query prefix
→ category synonyms
→ "synonym in zone city"
```

For each returned business it extracts:

```text
CompanyMetaData.id
CompanyMetaData.name
first phone
CompanyMetaData.url
geometry.coordinates
raw Feature payload
```

It then creates an immutable raw source record and sends the candidate to entity resolution.

---

## 6. Current implementation gaps

### 6.1 No real geographic restriction

The connector does not send:

- `ll`
- `spn`
- `bbox`
- `rspn`

Therefore a query such as:

```text
school in F-7 Islamabad
```

is only text.

It does not prove that Harvester inspected the full target area or prevented results outside it.

### 6.2 No strict area behavior

Yandex documents that when `rspn` is omitted or set to `0`, the service may search outside the specified area if nothing is found inside it.

A coverage run must use:

```text
rspn=1
```

when strict geographic containment is required.

### 6.3 No pagination

The current connector requests one page and ignores `skip`.

The API supports:

```text
results: maximum 50
skip: maximum 1000
```

When `skip` is used, `results` must also be set and `skip` must divide evenly by `results`.

### 6.4 Search is best-match, not exhaustive

Yandex states that business search returns organizations that best match a query rather than every organization in the area.

Therefore:

```text
completed query
≠ complete market coverage
```

### 6.5 Failures become empty results

The current connector collapses:

```text
successful zero-result response
invalid request
invalid API key
rate limit
network timeout
server failure
```

into one empty list.

The pipeline may then complete the source run without preserving the failure.

### 6.6 Complete raw payload is stored indefinitely

This conflicts with the conservative interpretation of Yandex's published storage and caching restrictions.

### 6.7 One phone only

The current connector keeps only the first phone even though the documented response supports a list of contact methods with a type and formatted value.

### 6.8 Structured address is discarded

The Yandex response may contain:

- Country code
- Formatted address
- Postal code
- Address components
- Additional information
- Floor identifier

The current canonical path does not fully preserve these fields.

### 6.9 Categories are flattened

The current merger uses only the first category name as an institution type candidate.

It does not preserve all category classes and names as source-native evidence.

### 6.10 Hours and accessibility features are discarded

The documented response may include:

- Opening hours
- Availability intervals
- Twenty-four-hour status
- Accessibility features

These are currently lost from normalized intelligence.

### 6.11 No source economics

The current run does not persist:

- Requests consumed
- Pages retrieved
- Results per query
- Duplicates
- Estimated cost
- Rate-limit events
- Yield by geography
- Yield by synonym
- Cache-expiry obligations

### 6.12 No terms-aware lifecycle

There is no automatic expiration of Yandex-derived content or deletion on contract termination.

---

## 7. Official Places API capability

The Yandex Places HTTP API supports forward and reverse search for geographical objects and businesses.

For organization discovery, Harvester uses:

```text
type=biz
```

The documented request supports:

```text
apikey
text
lang
type
ll
spn
bbox
rspn
results
skip
uri
```

The endpoint is:

```text
https://search-maps.yandex.ru/v1/
```

The published API limit is up to 50 requests per second, subject to the active commercial plan and contract.

Harvester must use its configured contractual quota rather than treating the public maximum as an entitlement.

---

## 8. Request parameters

### 8.1 `apikey`

Required API credential issued through Yandex's developer tooling.

The key is secret operational configuration.

It must not be committed to the repository or exposed to the browser.

### 8.2 `text`

Required search text unless a permitted `uri` workflow is used.

Documented business-query examples include:

- Business name
- Address
- Phone number
- Service provided
- Multiple criteria

Harvester may generate:

```text
organization-type queries
service queries
exact-name queries
name plus address queries
phone verification queries
category plus area queries
```

### 8.3 `lang`

Required response locale.

Documented values include:

```text
ru_RU
uk_UA
be_BY
en_RU
en_US
tr_TR
```

If another locale is supplied, Yandex may select the closest supported language.

The language affects returned names and regional conventions.

The selected locale must be stored with every query.

For Pakistan, no dedicated `en_PK` locale is documented. A source plan may use `en_US` only after explicit acceptance that the provider may normalize regional conventions differently.

### 8.4 `type`

For organization discovery:

```text
type=biz
```

For geographical boundary lookup or area verification:

```text
type=geo
```

Harvester must not allow automatic type detection for governed organization collection because the same text may otherwise produce mixed toponyms and businesses.

### 8.5 `ll` and `spn`

`ll` defines the search-area center as:

```text
longitude,latitude
```

`spn` defines longitude and latitude spans.

These parameters must be supplied together.

### 8.6 `bbox`

`bbox` defines the lower-left and upper-right corners in longitude, latitude order.

It takes priority over `ll` and `spn` when both are supplied.

A governed source plan should prefer `bbox` for rectangular coverage cells because the exact boundary is easier to preserve and audit.

### 8.7 `rspn`

```text
rspn=0
```

allows the service to search beyond the defined area when no result is found inside it.

```text
rspn=1
```

strictly prevents search outside the defined area.

Coverage runs use `rspn=1` by default.

Named-organization verification may use a non-strict query only when the purpose is explicitly broader than one cell.

### 8.8 `results`

Maximum objects requested per page.

```text
1 to 50
```

Harvester should normally use `50` for systematic coverage to reduce request overhead, subject to contract and result-quality testing.

### 8.9 `skip`

Offset into the result set.

Rules:

- Maximum `1000`
- `results` must be set
- `skip` must divide evenly by `results`

With `results=50`, pages use:

```text
skip=0
skip=50
skip=100
...
skip=1000
```

### 8.10 `uri`

The documented `uri` request parameter is intended for additional information about an object identified through Yandex Geosuggest.

Harvester must not assume that every `properties.uri` returned by Places Search may be used as a general Place Details endpoint unless Yandex confirms that behavior for the active product and contract.

No undocumented enrichment call should be introduced.

---

## 9. Recommended Yandex source flow

```text
Market Definition
→ Yandex Source Plan
→ contract and credential validation
→ territory and locale validation
→ target boundary resolution
→ real geographic coverage cells
→ Yandex query taxonomy
→ strict business searches
→ pagination
→ saturation detection
→ transient result deduplication
→ independent website and registry verification
→ Harvester-owned evidence
→ entity and branch resolution
→ coverage, yield, failure, cost, and expiry report
→ deletion of expired Yandex cache
```

---

## 10. Yandex Source Plan

Every run must begin with a versioned source plan.

```text
YandexSourcePlan
```

Recommended fields:

```text
id
tenant_id
market_definition_id
version
compliance_profile_id
connection_id
country_code
provider_locale
territory_approved
geographic_boundary_reference
coverage_strategy
coverage_cell_size
strict_area_default
sector_keys
organization_types
query_families
synonym_set_versions
page_size
maximum_skip
maximum_queries
maximum_requests
maximum_cost
maximum_runtime
cache_duration
website_verification_required
minimum_independent_sources
created_by
approved_by
activated_at
retired_at
```

A source plan is immutable after activation.

Changes create a new version.

---

## 11. Geographic planning

### 11.1 Text labels are not geometry

```text
F-7 Islamabad
```

is a label.

It is not a coverage boundary.

### 11.2 Area object

Every target geography should resolve to:

```text
AreaDefinition

area_id
name
country_code
boundary_type
polygon
bounding_box
source
resolution_confidence
approved_at
```

### 11.3 Coverage cells

A large area is divided into auditable rectangular cells.

```text
CoverageCell

cell_id
parent_area_id
lower_left_longitude
lower_left_latitude
upper_right_longitude
upper_right_latitude
bbox_string
status
query_count
result_count
unique_business_count
saturation_state
failure_state
```

### 11.4 Strict search

Every coverage-cell business request should send:

```text
bbox=<cell boundary>
rspn=1
type=biz
```

### 11.5 Boundary validation

Every returned point must still be checked against the intended polygon.

A rectangular cell may overlap areas outside an irregular administrative boundary.

Therefore:

```text
Yandex strict bbox
+ Harvester point-in-polygon validation
```

### 11.6 Overlap

Cells may overlap slightly to reduce edge loss.

Overlap must be versioned and measured so duplicate discovery is expected rather than treated as source error.

---

## 12. Query taxonomy

Yandex Places accepts free-text organization search rather than a separate documented included-type taxonomy equivalent to Google's Places types.

Harvester therefore needs a governed query taxonomy.

### 12.1 Category queries

Examples:

```text
school
private school
college
hospital
clinic
hotel
law firm
property management
supermarket
```

### 12.2 Service queries

Examples:

```text
online admissions
appointment booking
property management
corporate legal services
facility management
```

Service queries may improve discovery but can also return organizations whose primary type does not match the target.

They require stronger post-search classification.

### 12.3 Exact-name queries

```text
<organization name>
```

Used for verification, not broad coverage.

### 12.4 Name plus address

```text
<organization name>, <street or district>
```

Useful for distinguishing branches.

### 12.5 Phone queries

Yandex documents business lookup by phone number.

A normalized phone can be used to verify whether an existing candidate matches a Yandex business.

Phone lookup is not permission to persist the Yandex response beyond the licensed cache period.

### 12.6 Multi-criteria queries

Yandex supports text queries combining business type, service, address, and other characteristics.

Examples:

```text
pharmacy, 24 hours, pay with card
school, F-7, Islamabad
hospital, emergency, Rawalpindi
```

These may be used as bounded recall-expansion queries.

### 12.7 Local-language queries

A source plan may define local-language synonyms independently of response `lang`.

Each synonym must retain:

```text
term
language
script
category mapping
source
approved version
```

### 12.8 Query explosion control

Do not multiply every:

```text
sector
× subtype
× synonym
× service
× cell
× language
```

without budget controls.

The source planner should estimate:

```text
planned request count
maximum pages
expected cost
expected duplicate rate
expected unique yield
```

before activation.

---

## 13. Query execution and paging

### 13.1 Query record

Every request creates:

```text
YandexQueryRun

id
source_run_id
source_plan_id
coverage_cell_id
query_family
query_text
locale
type
bbox
ll
spn
rspn
results
skip
request_hash
attempt
status
http_status
provider_found
returned_count
estimated_cost
started_at
completed_at
failure_code
failure_message
cache_expires_at
```

### 13.2 Statuses

```text
PLANNED
RUNNING
SUCCEEDED
NO_RESULTS
PARTIAL
SATURATED
RATE_LIMITED
AUTHENTICATION_FAILED
INVALID_REQUEST
NETWORK_FAILED
PROVIDER_FAILED
RETRY_EXHAUSTED
CANCELLED
LICENSE_BLOCKED
```

### 13.3 First page

```text
results=50
skip=0
```

### 13.4 Later pages

Continue while:

- The provider indicates more results may exist.
- The returned page is full.
- `skip` remains within the allowed limit.
- Cost and request budgets remain available.
- The stopping policy has not been met.

### 13.5 Saturation

Mark a query saturated when:

- The last permitted page remains full.
- The provider reports more results than can be retrieved.
- Repeated pages do not materially increase unique yield but the search remains capped.
- The source plan reaches `skip=1000` without exhausting results.

### 13.6 Saturation response

Refine by:

- Smaller geographic cells
- More specific organization subtype
- More specific service query
- Separate query languages
- Separate branch categories

Saturation must remain visible in coverage reporting.

### 13.7 Duplicate paging defense

Store the ordered provider IDs and response hash for each page.

If the same page repeats unexpectedly:

```text
PAGINATION_STALLED
```

Stop rather than paying to admire the same businesses repeatedly.

---

## 14. Official response model

Yandex returns a partial GeoJSON-compatible `FeatureCollection`.

The response contains:

```text
properties.ResponseMetaData.SearchRequest
properties.ResponseMetaData.SearchResponse
features[]
```

Harvester may parse only fields documented by Yandex for the active API version.

Yandex explicitly warns that undocumented fields may not remain supported.

### 14.1 Request metadata

Documented fields include:

```text
request
results
skip
boundedBy
```

### 14.2 Response metadata

Documented fields include:

```text
found
boundedBy
display
```

### 14.3 Business feature

Documented containers include:

```text
properties.name
properties.description
properties.boundedBy
properties.uri
properties.CompanyMetaData
geometry
```

### 14.4 Company metadata

Documented fields include:

```text
id
name
address
Address
url
Categories
Phones
Hours
Features
```

---

## 15. Business identity extraction

### 15.1 Provider business ID

```text
CompanyMetaData.id
```

is the documented provider business ID.

It is a strong transient provider reference.

It is not automatically Harvester canonical identity.

Persistent storage of the ID must be allowed by the active compliance profile.

### 15.2 Provider URI

```text
properties.uri
```

may provide a Yandex object reference.

It must be treated as Yandex-owned source content and follow the same cache and retention policy.

### 15.3 Name

Preferred source-native business name:

```text
CompanyMetaData.name
```

Fallback:

```text
properties.name
```

Harvester stores the original display value only within the permitted cache.

A separately verified organization name may be persisted as Harvester evidence from an independent source.

### 15.4 Identity evidence

A Yandex candidate can help generate identity hypotheses using:

- Provider ID
- Name
- Address
- Coordinates
- Phone
- Website
- Category

It cannot independently authorize a permanent canonical merge when the underlying source data must expire.

A durable merge requires independent supporting evidence or a license explicitly permitting the necessary persistence.

---

## 16. Address extraction

### 16.1 Source-native address

```text
CompanyMetaData.address
```

provides a business-address string.

### 16.2 Structured address

```text
CompanyMetaData.Address
```

may contain:

```text
country_code
formatted
postal_code
additional_info
indoor_level_id
Components[]
```

### 16.3 Components

Each component contains:

```text
kind
name
```

Potential component kinds may include:

- Country
- Province
- Area
- District
- Locality
- Street
- House

Harvester must preserve the source-native kind rather than forcing all providers into one unreviewed address schema.

### 16.4 Canonical mapping

A mapping profile may derive:

```text
country
country_code
administrative_area
city
area
district
street
house
postal_code
formatted_address
```

Every derived field retains the component evidence link and mapping version.

### 16.5 Coordinate order

Yandex GeoJSON coordinates are:

```text
[longitude, latitude]
```

The connector must never transpose them.

### 16.6 Location validation

Validate:

- Longitude range
- Latitude range
- Point inside intended coverage boundary
- Plausible address-country agreement
- Duplicate coordinates across unrelated businesses

---

## 17. Website extraction

### 17.1 Source field

```text
CompanyMetaData.url
```

may provide the business website.

### 17.2 Interpretation

A returned website supports:

```text
WEBSITE_PRESENT_IN_YANDEX
```

within the permitted transient source context.

It does not prove:

- Domain ownership
- Current availability
- Official status
- Quality
- Security
- Infrastructure maturity

### 17.3 Missing URL

No returned URL means:

```text
WEBSITE_NOT_DETECTED_BY_YANDEX
```

It does not mean:

```text
WEBSITE_ABSENT_CONFIRMED
```

### 17.4 Website handoff

```text
Yandex URL candidate
→ URL safety validation
→ independent domain resolution
→ organization-name verification
→ official-site confirmation
→ website crawler
→ Harvester-owned page evidence
```

The Yandex URL must not be copied indefinitely merely to avoid doing independent verification.

### 17.5 Safe-fetch checks

Before crawling:

- Reject non-HTTP schemes
- Resolve DNS safely
- Block private and link-local destinations
- Revalidate redirects
- Respect robots rules
- Apply response-size and content-type limits
- Deduplicate normalized domains

---

## 18. Phone and contact extraction

### 18.1 Source field

```text
CompanyMetaData.Phones[]
```

Each entry may include:

```text
type
formatted
```

### 18.2 Preserve all documented contacts

Do not keep only the first phone.

Create one transient contact candidate per documented entry.

### 18.3 Contact type

Possible values may represent:

- Phone
- Fax
- Another documented contact class

Preserve Yandex's exact source type.

### 18.4 Phone normalization

Normalize separately using the best supported region hint.

Retain:

```text
raw_formatted_value
normalized_value
normalization_region
normalization_status
```

### 18.5 Contact scope

A Yandex phone is normally an organization or branch contact.

It is not a named decision-maker.

### 18.6 Missing phone

No phone means:

```text
PHONE_NOT_DETECTED_BY_YANDEX
```

not confirmed absence.

---

## 19. Category extraction

### 19.1 Source fields

```text
CompanyMetaData.Categories[]
```

Each category may contain:

```text
class
name
```

### 19.2 Preserve full category list

Store all categories within the permitted cache.

Do not reduce the organization to the first returned category.

### 19.3 Taxonomy mapping

```text
Yandex category class and name
→ versioned Yandex-to-Harvester mapping
→ Harvester sector candidate
→ Harvester organization-type candidate
```

### 19.4 Classification confidence

A Yandex category is provider classification evidence.

It is not automatically final ICP fit or sector truth.

### 19.5 Unknown mappings

Unrecognized category values create:

```text
TAXONOMY_MAPPING_REQUIRED
```

They must not silently become `UNKNOWN` and disappear from quality reporting.

---

## 20. Opening-hours extraction

### 20.1 Source field

```text
CompanyMetaData.Hours
```

May include:

- Availability groups
- Day flags
- Time intervals
- Twenty-four-hour status
- Human-readable text

### 20.2 Uses

Opening hours may support:

- Branch operating context
- Contact timing
- Twenty-four-hour service identification
- Website consistency checks
- Branch differentiation

### 20.3 Limitations

Hours do not prove:

- Current operating status
- Service quality
- Staffing
- Digital infrastructure
- Purchase intent

### 20.4 Freshness

Opening hours are volatile.

They must carry retrieval time and expire with the Yandex cache.

---

## 21. Accessibility and facility features

### 21.1 Source field

```text
CompanyMetaData.Features[]
```

Documented examples include accessibility-related features such as:

- Accessible parking
- Wheelchair-accessible entrance
- Automatic door
- Accessible toilet
- Call button
- Elevator
- Ramp
- Other accessibility vocabulary

### 21.2 Use

These features may provide supporting physical-facility context.

They can support:

- Facility profile
- Accessibility context
- Branch differentiation
- Connected Infrastructure research hypotheses

### 21.3 Scoring prohibition

A Yandex accessibility feature must not directly add Opportunity Score points merely because it is present or absent.

Absence from the response means only:

```text
FEATURE_NOT_DETECTED_BY_YANDEX
```

### 21.4 Independent verification

Material facility claims require:

- Organization-owned source
- Authorized customer data
- Reliable public registry
- Human confirmation
- Another permitted source

---

## 22. Operating status limitation

Unlike the current Google Places response used by Harvester, the documented Yandex Places business response does not expose a direct `businessStatus` field.

Therefore Yandex cannot reliably classify:

```text
OPERATIONAL
CLOSED_TEMPORARILY
CLOSED_PERMANENTLY
```

from the documented response alone.

Default interpretation:

```text
operating_status = UNKNOWN
```

unless independent evidence establishes another state.

Do not infer operational status from opening hours alone.

---

## 23. Ratings, reviews, photos, and posts

### 23.1 Places API limitation

The documented Yandex Places response does not include supported fields for:

- Ratings
- Review text
- Review count
- Photos
- Public posts
- Profile views
- Search impressions

Harvester must ignore undocumented response fields even if observed experimentally.

### 23.2 No Maps website scraping

Do not open the public Yandex Maps organization card with a crawler to extract these fields.

### 23.3 Customer-authorized Yandex Business information

Yandex Business provides owners with profile reviews and statistics through the Business interface.

Published Yandex Business guidance describes:

- Reviews in the managed profile
- Review analysis
- Profile traffic
- Routes built
- Call clicks
- Website traffic
- Direct traffic
- Discovery traffic
- Excel export of statistics

Harvester may ingest a customer-supplied export only when:

- The customer controls the profile.
- The customer authorizes the import.
- The export is obtained through an allowed product workflow.
- The import terms permit Harvester's intended processing.
- The source period and authorization are recorded.

### 23.4 Reviews

Customer-authorized reviews may support operational research when permitted.

They must not become simple arithmetic such as:

```text
negative review count × points
```

Review claims require:

```text
issue classification
infrastructure relevance
severity
freshness
repetition
corroboration
confidence
```

### 23.5 Statistics

Authorized Yandex Business statistics may support:

- Demand context
- Branch activity
- Route interest
- Call interest
- Website engagement
- Direct versus discovery traffic

They remain customer-owned operational evidence and must be kept separate from public Places search results.

---

## 24. Search result completeness

Yandex states that business search returns the organizations that best match the query, not all organizations.

Therefore the model uses:

```text
SEARCH_RESULT_SET
```

not:

```text
COMPLETE_DIRECTORY
```

### 24.1 Coverage dimensions

```text
Geographic coverage
Query-family coverage
Language coverage
Pagination coverage
Provider-result coverage
Independent-verification coverage
```

### 24.2 No-result state

A successful query with zero features creates:

```text
NO_RESULTS_FOR_QUERY
```

It does not create:

- No organizations exist
- No websites exist
- No software exists
- No opportunity exists

### 24.3 Provider ranking

The source response order is Yandex's ranking.

Harvester must preserve it inside the transient query record.

Harvester's independent opportunity ranking may operate only on independently verified Harvester entities and evidence, subject to the active license.

---

## 25. Deduplication

### 25.1 Within one query

Deduplicate repeated provider IDs.

### 25.2 Across pages

The same provider ID may not create multiple transient business candidates.

Preserve all query-page appearances as evidence links.

### 25.3 Across queries

The same business may appear under:

- Different synonyms
- Different services
- Adjacent cells
- Different languages
- Exact-name verification

One transient provider candidate may link to many query runs.

### 25.4 Provider-ID uncertainty

Do not assume Yandex IDs are permanent unless the active contract and documentation explicitly support that use.

### 25.5 Fallback duplicate features

When provider IDs differ, candidate matching may compare:

- Normalized name
- Normalized phone
- Independently verified domain
- Address
- Coordinates

A provider-derived match remains provisional until permitted evidence supports a durable merge.

---

## 26. Detection and absence states

Yandex source processing must preserve:

```text
PRESENT_IN_YANDEX
NOT_DETECTED_BY_YANDEX
NO_RESULTS_FOR_QUERY
NOT_INSPECTED
INSPECTION_FAILED
RATE_LIMITED
LICENSE_BLOCKED
UNKNOWN
NOT_APPLICABLE
```

`ABSENT_CONFIRMED` cannot be created by Yandex Places alone.

### 26.1 Examples

```text
Yandex returns a URL
→ website present in Yandex result

Yandex returns no URL
→ website not detected by Yandex

Yandex query fails with 429
→ inspection rate-limited

Yandex returns no businesses in one cell
→ no results for that query and cell

Yandex returns no accessibility feature
→ feature not detected by Yandex
```

---

## 27. Independent verification bridge

The safe long-term architecture is:

```text
Transient Yandex result
→ organization name, phone, address, website candidate
→ independent search or organization-owned website
→ independent evidence artifact
→ Harvester assertion
→ entity resolution
→ opportunity assessment
→ expiry of Yandex cache
```

### 27.1 Independent sources

Possible permitted sources include:

- Organization-owned website
- Authorized customer data
- Government or regulator registry
- Sector registry
- Customer-supplied spreadsheet
- Public procurement notice
- Another licensed source with compatible rights

### 27.2 Derived evidence standard

Harvester may persist independently verified facts.

It must not merely copy Yandex data, rename it as a derived fact, and declare contractual enlightenment.

### 27.3 Verification trace

Every durable fact originally prompted by Yandex should retain a source-transition record:

```text
Yandex discovery reference
→ independent verification task
→ independent evidence ID
→ resulting Harvester assertion
```

After Yandex cache expiry, the durable Harvester assertion remains supported by the independent evidence, not by deleted Yandex content.

---

## 28. Opportunity Scoring Model v3 integration

### 28.1 Public Yandex mode

By default, public Yandex Places data is a discovery and research-planning input.

Direct score contribution is disabled unless the compliance profile explicitly permits the required retention and use.

### 28.2 Potential contributions after independent verification

| Yandex discovery signal | Independent evidence destination |
|---|---|
| Business name | Organization identity |
| Address and coordinates | Branch identity and footprint |
| Website candidate | Digital-access inspection |
| Phone candidate | General contactability verification |
| Categories | Sector and organization-type classification |
| Multiple branch candidates | Account scale and operating footprint |
| Hours | Branch context |
| Accessibility features | Facility context |

### 28.3 What Yandex cannot establish

Yandex Places cannot independently prove:

- Website absence
- CRM absence
- ERP absence
- LMS absence
- Workflow automation absence
- Manual-process dependence
- Weak internal software
- Data fragmentation
- Connected Infrastructure absence
- Buying intent
- Budget
- Procurement activity
- Decision-maker identity
- Communication consent

### 28.4 Authorized Business statistics

Customer-authorized Yandex Business exports may support:

```text
Account value and scale
Buying intent and timing
Digital demand
Branch activity
Website engagement
Contact demand
```

They do not create a new scoring dimension.

### 28.5 Score explanation

A score explanation must never cite deleted Yandex cached content as the sole evidence.

Before activation, either:

- Independent evidence replaces it.
- A permitted Yandex reference remains available under the active contract.
- The subfactor becomes unknown.

---

## 29. Source confidence

Recommended dimensions:

```text
provider authority
query specificity
geographic containment
category relevance
identity agreement
phone agreement
website agreement
freshness
independent corroboration
license usability
```

### 29.1 Provider authority

Yandex is authoritative for what Yandex returned.

It is not authoritative for every fact about the organization.

### 29.2 Query specificity

```text
exact phone + strict area
```

may provide stronger identity evidence than:

```text
school
```

### 29.3 Independent corroboration

Confidence increases when independent sources agree on:

- Name
- Domain
- Phone
- Address
- Coordinates
- Parent organization

### 29.4 License usability

A fact that cannot legally be retained or used for the intended decision has low operational evidence authority even if the provider response is technically clear.

---

## 30. Error model

Documented provider errors include:

```text
400 invalid or missing parameter
403 invalid API key
429 too many requests
```

Harvester also needs:

```text
NETWORK_TIMEOUT
DNS_FAILURE
TLS_FAILURE
INVALID_JSON
SCHEMA_MISMATCH
PROVIDER_5XX
CACHE_WRITE_FAILURE
CACHE_EXPIRY_FAILURE
LICENSE_BLOCKED
```

### 30.1 No silent empty list

A failed request must never return the same result type as a successful zero-result request.

Recommended connector result:

```text
YandexSearchResult

status
features
response_metadata
http_status
error_code
error_message
request_id
attempt_count
```

### 30.2 Retry policy

Retry only transient conditions:

- Timeout
- Connection reset
- Selected 5xx responses
- Rate limit after `Retry-After` or bounded backoff

Do not retry indefinitely:

- Invalid key
- Invalid parameter
- License block
- Unsupported locale configuration

### 30.3 Backoff

Use bounded exponential backoff with jitter.

The run must stop when:

- Retry budget is exhausted.
- Cost budget is exhausted.
- Contract quota is exhausted.
- Operator cancellation is requested.

---

## 31. Quota and cost governance

The public API documentation states an upper limit of 50 requests per second.

Actual usable limits and fees depend on the active contract.

Every source plan should define:

```text
contract request allowance
requests per second
requests per day
requests per month
included request volume
overage price
maximum run cost
maximum tenant cost
alert thresholds
hard stop thresholds
```

### 31.1 Cost ledger

```text
YandexUsageLedger

connection_id
tenant_id
source_run_id
query_run_id
request_count
response_count
estimated_cost
confirmed_cost
quota_remaining
recorded_at
```

### 31.2 Query economics

Track:

```text
cost per query
cost per returned feature
cost per unique provider ID
cost per independently verified organization
cost per accepted opportunity
```

### 31.3 Adaptive stopping

Stop low-yield query families when:

- Marginal unique yield falls below policy.
- Duplicate rate exceeds policy.
- Verification cost exceeds value.
- Market coverage target is already met.

The adaptation must remain within the approved source plan.

---

## 32. Security model

### 32.1 Key storage

The API key must be:

- Server-side only
- Encrypted at rest
- Permission-protected
- Write-only after creation where possible
- Rotatable
- Audited

### 32.2 Environment separation

Use separate credentials for:

```text
development
staging
production
```

### 32.3 Request logging

Never log the full API key.

Redact query parameters containing credentials.

### 32.4 Outbound controls

Allow outbound access only to approved Yandex API hosts.

### 32.5 Customer isolation

Each customer connection must have separate ownership, permissions, quota, and audit history.

### 32.6 Authorized export security

Yandex Business exports may contain customer-sensitive operational information.

Apply:

- File malware scanning
- Tenant-scoped storage
- Encryption
- Access control
- Retention
- Deletion
- Audit

---

## 33. Cache and deletion model

### 33.1 Transient cache object

```text
YandexTransientObservation

id
query_run_id
provider_business_id
provider_uri
raw_payload_encrypted
response_hash
retrieved_at
cache_expires_at
deleted_at
compliance_profile_id
```

### 33.2 Expiry

The active compliance profile determines cache duration.

The default conservative maximum must not exceed thirty days under the reviewed published terms.

A stricter contract wins.

### 33.3 Automatic deletion

A scheduled job must:

1. Find expired Yandex observations.
2. Remove raw payloads.
3. Remove prohibited source-native fields.
4. Retain only permitted audit metadata.
5. Confirm no snapshot, export, backup, or search index still exposes expired content beyond policy.
6. Emit deletion audit events.

### 33.4 Contract termination

On contract termination:

- Stop all new requests.
- Delete cached Yandex content according to the agreement.
- Disable operator links if required.
- Preserve only legally permitted audit records.
- Re-evaluate scores and dossiers that relied on deleted evidence.

### 33.5 Backup handling

The retention design must cover:

- Primary database
- Replicas
- Search indexes
- Object storage
- Logs
- Backups
- Exports
- Development copies

Deleting only the primary row while leaving six cheerful copies elsewhere does not satisfy a deletion policy.

---

## 34. Attribution and display

The active contract may require:

- Text identifying Yandex as the information provider
- Display against a Yandex map
- Organization locations shown near other result information
- Preserved ordering
- Visible Yandex branding or links
- An agreed layout

Harvester must not design public or operator-facing Yandex result screens until these obligations are recorded in the compliance profile.

### 34.1 Internal research mode

Even closed internal systems may remain subject to display and attribution obligations under the applicable Yandex terms.

Closed access is not an exemption.

### 34.2 Independent Harvester entities

Once a fact is independently verified and no longer relies on Yandex content, Harvester may display the independent fact according to its own evidence and source rights.

The source transition must be provable.

---

## 35. Coverage report

A completed Yandex source run should report:

```text
areas planned
areas completed
coverage cells planned
coverage cells completed
strict-area queries
non-strict verification queries
query families
languages
pages requested
pages completed
queries with no results
saturated queries
failed queries
rate-limited queries
provider features returned
unique provider IDs
duplicate appearances
website candidates
phone candidates
category candidates
structured addresses
independent verification tasks
independently verified organizations
resolution candidates
review-required candidates
expired cache count
pending deletion count
requests consumed
estimated cost
confirmed cost
```

### 35.1 Completion definition

A run is complete when:

- Required cells were processed or explicitly failed.
- Required query families were processed.
- Pagination followed the source plan.
- Saturation is resolved or accepted.
- Failures remain visible.
- Cost and quota ledgers are reconciled.
- Cache expiry is scheduled.

A loop ending is not a coverage certificate.

---

## 36. Recommended domain objects

### 36.1 `YandexSourcePlan`

Defines versioned scope, geography, taxonomy, paging, budget, and compliance.

### 36.2 `YandexComplianceProfile`

Defines contract and retention authority.

### 36.3 `YandexQueryRun`

Stores exact request and result metadata.

### 36.4 `YandexTransientObservation`

Stores encrypted provider response within permitted cache duration.

### 36.5 `YandexProviderCandidate`

Transient deduplicated provider-business candidate.

```text
provider_business_id
provider_uri
name
address
coordinates
website_candidate
phones
categories
hours
features
first_seen_at
last_seen_at
cache_expires_at
```

### 36.6 `YandexDiscoveryEvidenceLink`

Links a transient Yandex candidate to an independent verification task.

### 36.7 `YandexAuthorizedBusinessImport`

Stores authorization and metadata for customer-supplied Yandex Business exports.

### 36.8 `YandexUsageLedger`

Tracks quota and cost.

### 36.9 `YandexDeletionAudit`

Records expired-content deletion and downstream re-evaluation.

---

## 37. Planned APIs

Conceptual internal APIs:

```http
GET  /api/v1/source-plans/yandex
POST /api/v1/source-plans/yandex
GET  /api/v1/source-plans/yandex/{plan_id}
POST /api/v1/source-plans/yandex/{plan_id}/validate
POST /api/v1/source-plans/yandex/{plan_id}/run

GET  /api/v1/source-runs/{run_id}/yandex-queries
GET  /api/v1/yandex/query-runs/{query_run_id}
POST /api/v1/yandex/query-runs/{query_run_id}/retry

GET  /api/v1/yandex/candidates/{candidate_id}
POST /api/v1/yandex/candidates/{candidate_id}/verify-independently

POST /api/v1/yandex-business/imports
GET  /api/v1/yandex-business/imports/{import_id}

GET  /api/v1/yandex/usage
GET  /api/v1/yandex/cache-expiry
POST /api/v1/yandex/cache-expiry/run
```

No endpoint should expose the raw API key or expired Yandex content.

---

## 38. Events

Suggested events:

```text
yandex.source_plan_validated
yandex.source_run_started
yandex.query_started
yandex.query_completed
yandex.query_no_results
yandex.query_saturated
yandex.query_failed
yandex.query_rate_limited
yandex.provider_candidate_discovered
yandex.independent_verification_requested
yandex.independent_verification_completed
yandex.business_export_imported
yandex.cache_expiring
yandex.cache_deleted
yandex.usage_threshold_reached
yandex.license_blocked
```

Events must not include the API key or prohibited full provider payloads.

---

## 39. Operator experience

### 39.1 Source-plan screen

Display:

- Contract status
- Territory
- Locale
- Areas
- Query families
- Maximum requests
- Maximum cost
- Cache duration
- Independent verification requirement

### 39.2 Run screen

Display:

- Coverage map
- Cell status
- Query progress
- Pages
- Unique yield
- Saturation
- Failures
- Cost
- Quota
- Cache-expiry countdown

### 39.3 Candidate screen

Display only what the active contract permits.

Clearly label:

```text
Temporary Yandex discovery data
Expires: <date>
Not yet independent evidence
```

### 39.4 Evidence transition

Show:

```text
Yandex discovery
→ official website verification
→ registry verification
→ Harvester assertion
```

### 39.5 Deletion impact

Before cached content expires, show whether:

- Independent evidence exists.
- A dossier still depends on Yandex content.
- A score needs re-evaluation.
- Human review is required.

---

## 40. Implementation sequence

### Gate 0: Legal and product compatibility

- Obtain applicable commercial terms.
- Confirm territory.
- Confirm closed-system use.
- Confirm resale use.
- Confirm temporary cache duration.
- Confirm permitted identifiers.
- Confirm independent-verification workflow.
- Confirm display and attribution.
- Confirm result-reranking rules.
- Confirm deletion requirements.

No production implementation passes Gate 0 through optimism.

### Gate 1: Connector correctness

- Replace empty-list failure handling with typed results.
- Parse response metadata.
- Preserve all documented phones.
- Preserve structured address.
- Preserve all categories.
- Preserve hours and features.
- Add explicit timeout, retry, and backoff.

### Gate 2: Real geography

- Add actual area boundaries.
- Generate coverage cells.
- Send `bbox` and `rspn=1`.
- Validate returned points against polygons.

### Gate 3: Pagination and saturation

- Add `skip` paging.
- Respect maximum offset.
- Detect repeated pages.
- Detect saturated queries.
- Subdivide cells or refine queries.

### Gate 4: Transient cache lifecycle

- Add encrypted transient observation storage.
- Add contract-driven expiry.
- Add deletion jobs.
- Cover indexes, logs, exports, and backups.

### Gate 5: Independent verification bridge

- Create website and registry research tasks.
- Store source-transition lineage.
- Prevent unverified Yandex data from becoming durable canonical truth.

### Gate 6: Resolution integration

- Use Yandex only as a candidate source under the approved compliance profile.
- Require independent evidence for durable merge where necessary.
- Preserve review states and conflicts.

### Gate 7: Authorized Yandex Business import

- Add customer authorization record.
- Parse supported Excel or CSV exports.
- Preserve source period and metrics.
- Apply customer data controls.

### Gate 8: Scoring integration

- Keep public Yandex direct score input disabled by default.
- Use independently verified facts.
- Allow authorized Business metrics under explicit policy.
- Re-evaluate scores when source evidence expires.

### Gate 9: Shadow mode

- Run without changing daily selection.
- Measure unique yield.
- Measure independent verification rate.
- Measure cost.
- Measure cache-expiry impact.
- Measure false identity links.

### Gate 10: Governed activation

- Approve source-plan version.
- Approve compliance profile.
- Activate by tenant and territory.
- Monitor quota, failures, cost, and deletion.
- Retain rollback and kill switch.

---

## 41. Verification scenarios

The implementation is incomplete until tests prove that:

1. The connector refuses production operation without an approved compliance profile.
2. A free-use key cannot be activated for a closed resold Harvester deployment.
3. Every coverage query includes real geography.
4. Coverage queries use `rspn=1` by default.
5. Coordinates preserve longitude-latitude order.
6. Returned points outside the target polygon are excluded or flagged.
7. `results` never exceeds 50.
8. `skip` never exceeds 1000.
9. `skip` divides evenly by `results`.
10. Pagination retrieves later pages.
11. Repeated pages trigger `PAGINATION_STALLED`.
12. Full final pages trigger saturation handling.
13. A saturated query does not count as complete coverage.
14. A zero-result response remains distinct from a failed request.
15. HTTP 400 becomes `INVALID_REQUEST`.
16. HTTP 403 becomes `AUTHENTICATION_FAILED`.
17. HTTP 429 becomes `RATE_LIMITED`.
18. Transient network failures retry with bounded backoff.
19. Invalid keys do not retry indefinitely.
20. All documented phone entries are preserved during the cache period.
21. Fax and phone types remain distinct.
22. Structured address components are parsed.
23. Country code and postal code are preserved when present.
24. All categories are preserved rather than only the first.
25. Unknown category mappings create quality debt.
26. Hours are parsed without being treated as operating status.
27. Missing hours remain non-detection.
28. Accessibility features are supporting context only.
29. Missing accessibility features do not prove absence.
30. The connector ignores undocumented rating fields.
31. The connector ignores undocumented review fields.
32. The connector ignores undocumented photo fields.
33. The general crawler blocks Yandex Maps pages.
34. A returned website creates a verification task.
35. A missing website creates `NOT_DETECTED_BY_YANDEX`.
36. No Yandex field directly confirms internal software absence.
37. Provider search order is preserved inside the transient query record.
38. Harvester does not rerank Yandex result cards as if they were Yandex output.
39. Transient observations expire according to the compliance profile.
40. Expiry removes prohibited content from primary storage.
41. Expiry also covers indexes, exports, and backup policy.
42. Contract termination stops new requests.
43. Contract termination triggers deletion.
44. A durable canonical fact requires independent evidence when the license does not permit persistence.
45. Source-transition lineage remains after Yandex content deletion.
46. A dossier cannot cite deleted Yandex content as its sole evidence.
47. An opportunity score is re-evaluated when supporting Yandex content expires.
48. Authorized Business imports require customer authorization.
49. Authorized statistics remain tenant-isolated.
50. Usage and cost are recorded per request.
51. Quota thresholds produce alerts.
52. Hard cost limits stop the run.
53. API keys never appear in logs or events.
54. Customer connections remain isolated.
55. A provider candidate cannot grant communication consent.
56. A high opportunity score cannot bypass a Yandex license block.

---

## 42. Acceptance criteria

The Yandex source model is production-ready only when:

- Applicable commercial rights are documented.
- The approved use case includes Harvester's deployment model.
- Territory is approved.
- Caching and deletion rules are implemented.
- The connector uses typed outcomes.
- Real geographic restrictions are implemented.
- Pagination and saturation are implemented.
- Query and response metadata are preserved.
- Only documented fields are parsed.
- All phones, address components, categories, hours, and features are handled correctly.
- Yandex Maps website scraping is blocked.
- Independent verification is connected.
- Durable Harvester facts do not depend solely on expired Yandex content.
- Opportunity Scoring Model v3 uses only permitted and explainable evidence.
- Authorized Yandex Business imports preserve customer authorization.
- Cost and quota controls are active.
- Credential controls pass review.
- Attribution and display behavior match the contract.
- Cache-expiry tests pass.
- Contract-termination deletion tests pass.
- Exact-head CI and security checks pass without unresolved issues.

---

## 43. Locked source definition

> NEWAX Harvester uses Yandex Maps as a governed, contract-aware and normally transient organization-discovery source. It searches real geographic areas through the official Places API, preserves query and coverage truth, parses only documented business fields, and converts provider results into independent research tasks rather than permanent copied lead data. Yandex Business information enters only through customer-authorized workflows. Missing fields remain non-detection, failures remain visible, expired provider content is deleted, and no Yandex result may override Harvester's evidence, identity, scoring, consent, or customer-control boundaries.
