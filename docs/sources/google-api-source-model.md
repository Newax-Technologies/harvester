# NEWAX Harvester Google API Source and Extraction Model

Status: **Normative planned source architecture**  
Source family: **Google Places public discovery and Google Business Profile authorized data**  
Document version: **v1**  
Implementation state: **Current Google Places connector is partial; target architecture is not yet implemented**  
Last external-reference review: **2026-08-03**  

Authority: This document defines how NEWAX Harvester should plan, call, extract, verify, retain, explain, and use Google APIs. It does not create a second roadmap and does not claim that the current runtime already follows this model.

Read with:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [NEWAX Harvester Opportunity Scoring Model v3](../architecture/opportunity-scoring-model-v3.md)
- [Standalone Product and Integration Framework](../architecture/standalone-product-and-integration-framework.md)

---

## 1. Purpose

Google APIs can help Harvester discover organizations, branches, public access paths, operating status, location context, limited public reputation signals, and customer-authorized Business Profile performance.

They must not become an ungoverned substitute for Harvester's evidence model.

This document answers:

1. Which Google APIs Harvester may integrate.
2. How a market definition becomes a Google source plan.
3. How geographic coverage should be performed.
4. How Text Search and Nearby Search should cooperate.
5. How Place IDs should be deduplicated and refreshed.
6. Which fields should be requested during discovery and enrichment.
7. How reviews, photos, posts, and performance metrics may be used.
8. How Google results should hand off to the website crawler.
9. Which states represent no result, non-detection, failure, and confirmed absence.
10. How cost, quota, security, attribution, retention, and compliance should be governed.
11. How Google evidence may influence Opportunity Scoring Model v3.
12. What must be implemented and verified before production activation.

The goal is not to copy Google Maps into Harvester.

The goal is to use approved Google APIs as bounded discovery and authorized intelligence sources inside a larger evidence-backed operating model.

---

## 2. Locked source boundary

Harvester must separate two Google modes.

```text
GOOGLE_PLACES_PUBLIC
GOOGLE_BUSINESS_PROFILE_AUTHORIZED
```

### 2.1 Google Places public mode

Google Places public mode is for discovering and retrieving public place information through the official Places API.

Primary capabilities:

- Text Search (New)
- Nearby Search (New)
- Place Details (New)
- Place Photos (New), when specifically approved
- Google Maps links for operator navigation

Primary role:

```text
Discover candidate places
→ obtain a stable Google Place ID
→ retrieve bounded public place fields
→ create transient discovery evidence
→ identify independent research paths
```

### 2.2 Google Business Profile authorized mode

Google Business Profile authorized mode is for locations that an authenticated customer or operator is authorized to manage.

Potential capabilities include:

- Managed location information
- Reviews and review responses
- Local Posts
- Media
- Notifications
- Place actions
- Business Profile performance metrics
- Search keyword impressions

Primary role:

```text
Customer-authorized operating intelligence
→ managed-location analysis
→ demand and engagement trends
→ customer-controlled improvement recommendations
```

### 2.3 The modes must not be silently combined

Public Places data and authorized Business Profile data differ in:

- Permission
- Authentication
- Available fields
- Intended use
- Retention obligations
- Attribution obligations
- Scoring authority
- Customer ownership
- Risk

A public prospect must never be treated as if Harvester manages its Business Profile.

---

## 3. Non-negotiable rules

### 3.1 Do not scrape the Google Maps website

Harvester must not crawl or automate extraction from:

```text
maps.google.com
www.google.com/maps
google.com/maps
Google Maps review pages
Google Maps photo pages
Google Maps internal browser endpoints
undocumented Maps application requests
```

The approved programmatic interfaces are the official APIs and operator-facing links.

The general website crawler must block Google Maps targets.

### 3.2 Google non-return is not confirmed absence

```text
Google returns websiteUri
→ WEBSITE_PRESENT_FROM_GOOGLE

Google omits websiteUri
→ WEBSITE_NOT_DETECTED_BY_GOOGLE

Google query fails
→ GOOGLE_INSPECTION_FAILED
```

None of the following proves absence:

- Missing `websiteUri`
- Missing phone
- Missing rating
- Missing reviews
- Missing photos
- No Text Search results
- No Nearby Search results
- Reaching a result limit
- A blocked request
- Quota exhaustion
- An invalid field mask
- A connector timeout

Confirmed absence requires a separate evidence process defined by the Opportunity Scoring Model v3.

### 3.3 Google type is not Harvester taxonomy truth

Google `primaryType` and `types` are source-native classifications.

They may support Harvester classification, but they must not become the canonical sector or organization type without mapping and evidence.

### 3.4 Google Place ID is provider identity, not eternal canonical identity

A Place ID is a strong Google-provider identifier.

It is not the same as:

- Legal organization identity
- Harvester canonical institution ID
- Branch identity across every source
- Permanent immutable identity

The same place may have multiple Place IDs, and Place IDs may change over time.

### 3.5 Google content is not automatically Harvester-owned evidence

The current Google Maps Platform Terms restrict scraping, caching, bulk storage, copying business names, addresses, and reviews, and creating content from Google Maps Content except where expressly permitted.

Therefore:

- Place IDs may be retained where Google documentation permits.
- Latitude and longitude may only be cached within the applicable permitted period.
- Other Google Maps Content must not be persisted, transformed, or scored beyond the approved legal and policy profile.
- Public reviews and photos must not be used to train, validate, or fine-tune machine-learning models.
- A Google response must not be stored indefinitely merely because Harvester normally preserves raw evidence.

The source-specific compliance profile overrides generic raw-retention behavior.

### 3.6 Independently verified facts become independent-source evidence

A Google field may provide a transient research path.

Example:

```text
Google websiteUri
→ transient crawl seed
→ organization website fetched directly
→ website self-identifies organization
→ website URL stored as WEBSITE-source evidence
```

The permanently retained fact should be supported by the independent source, not silently represented as Google-owned content.

### 3.7 A score never grants permission

Google-derived signals do not grant:

- Communication consent
- Publication permission
- Data-resale permission
- Business Profile management authority
- Identity certainty
- Outreach authorization

---

## 4. Official Google services in scope

## 4.1 Places API (New)

The planned public discovery connector may use:

```text
POST /v1/places:searchText
POST /v1/places:searchNearby
GET  /v1/places/{PLACE_ID}
GET  /v1/{PHOTO_NAME}/media
```

### Text Search (New)

Use for:

- Category and natural-language discovery
- Local terminology
- Organization names
- Named-place verification
- Phone-number lookup
- Service-area businesses where appropriate
- Synonyms that do not map cleanly to Google Place types

### Nearby Search (New)

Use for:

- Geographic coverage by circle
- Supported Google type filters
- Distance-ranked passes
- Popularity-ranked passes
- Saturation detection
- Coverage-cell discovery

### Place Details (New)

Use after deduplication for:

- Identity details
- Address components
- Business status
- Website and phone
- Opening hours
- Moved-place handling
- Optional reviews and photos

### Place Photos (New)

Use only when:

- The source plan explicitly enables photo retrieval
- The use case is approved
- Attribution is preserved
- Photo-name caching restrictions are enforced
- The image is not used for model training
- The cost profile allows retrieval

## 4.2 Google Business Profile APIs

Authorized mode may use:

- Business Information API
- Reviews API
- Local Posts API
- Media API
- Notifications API
- Place Actions API
- Verifications API, when required
- Business Profile Performance API

Access requires:

- Approved Google Business Profile API access
- OAuth 2.0
- Appropriate business-management scope
- Customer-authorized account and location access
- Tenant-aware credential isolation

---

## 5. Current repository implementation

The current runtime provides a thin Google Places Text Search connector.

Relevant files:

```text
src/lead_harvester/sources/google_places.py
src/lead_harvester/sources/geographic_tiling.py
src/lead_harvester/intelligence/taxonomy.py
src/lead_harvester/pipeline.py
src/lead_harvester/canonical/merger.py
src/lead_harvester/models/source.py
```

### 5.1 Current request

The connector calls:

```text
POST https://places.googleapis.com/v1/places:searchText
```

with:

```json
{
  "textQuery": "school in F-7 Islamabad"
}
```

It sends one fixed field mask requesting:

```text
places.id
places.displayName
places.formattedAddress
places.location
places.types
places.primaryType
places.businessStatus
places.nationalPhoneNumber
places.internationalPhoneNumber
places.websiteUri
places.rating
places.userRatingCount
places.regularOpeningHours
places.googleMapsUri
```

### 5.2 Current query generation

The current geographic-tiling module is a placeholder.

It converts configured city-zone pairs into query prefixes such as:

```text
F-7 Islamabad
Blue Area Islamabad
```

The taxonomy expands category keys into synonyms, then produces text queries such as:

```text
school in F-7 Islamabad
private school in F-7 Islamabad
college in F-7 Islamabad
montessori in F-7 Islamabad
```

### 5.3 Current extraction

For each returned place, the pipeline extracts:

```text
place.id
place.displayName.text
place.internationalPhoneNumber or nationalPhoneNumber
place.websiteUri
place.location.latitude
place.location.longitude
```

It stores the entire Place response as `RawSourceRecord.raw_payload`, then derives normalized name, phone, domain, and location fields before entity resolution.

### 5.4 Current canonical contribution

The merger can use Google data for:

- Display name
- Formatted address
- Website
- Primary type
- Business status
- Phone
- Branch coordinates
- Google provider ID
- Provenance

### 5.5 Current limitations

The current implementation has no complete support for:

- Real geographic cells
- Polygon or rectangle coverage
- Explicit location restriction
- Nearby Search
- Text Search pagination
- Saturation handling
- Place-ID-first discovery profiles
- Deduplication before expensive enrichment
- Place Details stage
- Structured address components
- Moved-place chains
- Future-opening businesses
- Query-level persistence
- Page-level persistence
- Retry classification
- Rate-limit handling
- Cost ledger
- Field-mask versions
- Review extraction
- Photo extraction
- Business Profile OAuth
- Posts
- Performance metrics
- Search keyword impressions
- Google-specific retention policy
- Attribution enforcement

### 5.6 Current correctness defects

#### Failure becomes empty results

The connector catches HTTP errors and returns an empty list.

This can collapse:

```text
NO_RESULTS
TIMEOUT
AUTHENTICATION_FAILED
RATE_LIMITED
SERVER_ERROR
```

into one apparent outcome.

#### Source run may still complete

Because the pipeline receives an empty list, the source run may be marked completed even when Google requests failed.

#### No pagination

The connector ignores `nextPageToken`.

#### No explicit geographic restriction

Without `locationBias` or `locationRestriction`, Text Search may use IP biasing.

#### Full field profile on every overlapping query

The same place can appear in many synonym searches, causing repeated retrieval of expensive fields.

#### Indefinite raw-payload storage

The generic immutable raw-record model currently stores complete Place objects. This must be redesigned before production because Google-specific content restrictions may prohibit that retention and derived use.

---

## 6. Target operating flow

```text
Versioned Market Definition
→ Google Source Plan
→ Google connection and policy validation
→ geography resolution
→ coverage-cell generation
→ Harvester-to-Google type mapping
→ Nearby Search coverage passes
→ Text Search synonym and named passes
→ pagination and saturation handling
→ query/page outcome persistence
→ Place ID deduplication
→ bounded Place Details enrichment
→ optional review/photo retrieval
→ compliance-filtered transient observation
→ independent website and registry handoff
→ Harvester evidence and entity resolution
→ source coverage, yield, cost, and quality report
```

Authorized Business Profile flow:

```text
Customer authorizes Google Business Profile
→ accounts and locations resolved
→ managed-location mapping
→ reviews/posts/media/performance retrieval
→ customer-owned operational analysis
→ evidence-backed recommendations
→ customer-controlled publication or action
```

---

## 7. Google source plan

Every Google run must begin with a versioned `GoogleSourcePlan`.

Recommended fields:

```text
id
market_definition_id
source_plan_version
mode
objective
country_code
region_code
language_codes
geographic_boundary_id
coverage_strategy
coverage_cell_policy
included_sectors
included_organization_types
excluded_organization_types
google_type_mapping_version
text_query_template_version
synonym_set_versions
include_future_opening_businesses
include_service_area_businesses
search_methods
rank_preferences
page_size
maximum_pages_per_query
maximum_results_per_query
maximum_unique_places
maximum_requests
maximum_estimated_cost
discovery_field_mask_version
details_field_mask_version
review_policy
photo_policy
business_profile_policy
retention_policy_version
attribution_policy_version
minimum_coverage
stopping_rules
created_by
approved_by
created_at
```

The plan must freeze the inputs used by a Harvest Job.

---

## 8. Geography model

## 8.1 Geography input

A target geography should be represented by one or more:

- Country
- Administrative area
- City
- District
- Zone
- Postal area
- Polygon
- Bounding rectangle
- Center-radius circle

A text label alone is not sufficient for systematic coverage.

## 8.2 Coverage cells

Large areas should be divided into deterministic coverage cells.

```text
GoogleCoverageCell
```

Recommended fields:

```text
id
source_plan_id
parent_geography_id
cell_version
geometry_type
center_latitude
center_longitude
radius_meters
southwest_latitude
southwest_longitude
northeast_latitude
northeast_longitude
parent_cell_id
subdivision_depth
status
expected_type_groups
completed_type_groups
request_count
result_count
unique_place_count
saturation_state
failure_state
coverage_started_at
coverage_completed_at
```

## 8.3 Cell sizing

Cell size should depend on:

- Urban density
- Target type density
- Google result limits
- Query budget
- Result saturation
- Required recall

The system should not lock one global radius such as 2 km for every market.

## 8.4 Saturation

Nearby Search returns at most the configured maximum, up to 20.

A response at the maximum indicates possible saturation, not complete coverage.

```text
result_count < maxResultCount
→ NOT_SATURATED_CANDIDATE

result_count = maxResultCount
→ POSSIBLY_SATURATED
```

Possible saturation responses:

- Subdivide the geographic cell
- Separate Google type groups
- Run both distance and popularity passes
- Use narrower primary types
- Add complementary Text Search queries
- Record accepted incompleteness when limits are reached

## 8.5 No point-in-polygon derivation from retained Google coordinates

Google terms may restrict using Places latitude and longitude to create derived geographic content and restrict caching beyond 30 days.

Therefore:

- Cell inclusion should be governed at request time.
- Coordinates may be used transiently within approved constraints.
- Long-term geometry should come from an independent permitted source when required.

---

## 9. Taxonomy and type mapping

Harvester taxonomy and Google Place Types must remain separate.

```text
GoogleTypeMapping
```

Recommended fields:

```text
id
mapping_version
harvester_sector
harvester_organization_type
google_included_types
google_excluded_types
google_included_primary_types
google_excluded_primary_types
text_search_included_type
strict_type_filtering
positive_synonyms
negative_synonyms
local_language_synonyms
known_ambiguities
review_required_patterns
created_at
approved_at
```

### 9.1 Type rules

- Nearby Search may accept multiple included or excluded Table A types.
- Text Search accepts one `includedType`.
- Table B types may be returned but cannot be used as filters.
- A Google type must not directly overwrite the canonical Harvester sector.
- Ambiguous types require other evidence.

### 9.2 Example education mapping

Conceptual example only:

```text
Harvester organization type: FORMAL_EDUCATION_PROVIDER

Nearby included primary types:
- school
- primary_school
- secondary_school
- preschool
- university

Text synonyms:
- school
- private school
- college
- montessori
- preschool
- academy
```

The exact mapping must be verified against the current Google Place Types table before activation.

---

## 10. Nearby Search design

## 10.1 Purpose

Nearby Search is the primary systematic geographic discovery method for supported place types.

Endpoint:

```text
POST https://places.googleapis.com/v1/places:searchNearby
```

## 10.2 Required request elements

- API credential
- Field mask
- Geographic circle

## 10.3 Recommended request profile

Conceptual request:

```json
{
  "includedPrimaryTypes": [
    "school",
    "preschool",
    "university"
  ],
  "maxResultCount": 20,
  "locationRestriction": {
    "circle": {
      "center": {
        "latitude": 33.7000,
        "longitude": 73.0500
      },
      "radius": 2000.0
    }
  },
  "rankPreference": "POPULARITY",
  "languageCode": "en",
  "regionCode": "PK"
}
```

## 10.4 Rank passes

Two bounded passes may be useful:

```text
POPULARITY
DISTANCE
```

They must not be assumed to return identical result sets.

Each pass is separately recorded and deduplicated by Place ID.

## 10.5 Result-limit behavior

Nearby Search supports `maxResultCount` from 1 to 20.

It does not provide Text Search-style pagination.

Coverage must therefore use cell subdivision and type refinement rather than pretending a 20-result response is complete.

## 10.6 Future-opening businesses

When strategically useful, enable:

```text
includeFutureOpeningBusinesses = true
```

Request:

```text
places.businessStatus
places.openingDate
```

Future openings can support buying-timing signals, but opening dates may be incomplete and must remain source-attributed.

## 10.7 Service-area businesses

Nearby Search is physical-location centered.

Text Search may be required for pure service-area businesses.

The source plan must state whether service-area organizations are in scope.

---

## 11. Text Search design

## 11.1 Purpose

Text Search complements geographic type search.

Endpoint:

```text
POST https://places.googleapis.com/v1/places:searchText
```

## 11.2 Query families

### Category query

```text
private schools
hospitals
law firms
hotels
property management companies
```

### Category plus geography

```text
private schools in F-7 Islamabad
hospitals in Rawalpindi
law firms in Blue Area Islamabad
```

### Local terminology

```text
academy in Islamabad
clinic in Rawalpindi
marriage hall in Islamabad
```

### Organization subtype

```text
Montessori in F-8 Islamabad
cardiology hospital Rawalpindi
commercial property manager Islamabad
```

### Named organization verification

```text
Beaconhouse F-7 Islamabad
Shifa International Hospital Islamabad
```

### Phone verification

Use the international country code and the corresponding region code where possible.

## 11.3 Location control

Use one of:

```text
locationRestriction
locationBias
```

Never both.

For market coverage, prefer `locationRestriction`.

Use `locationBias` only where out-of-area candidates may still be useful.

If neither is supplied, Google may use IP-based biasing. That is not acceptable for deterministic market coverage.

## 11.4 Type filtering

Use:

```text
includedType
strictTypeFiltering
```

where the query family supports reliable filtering.

Do not force strict type filtering on named-address or geopolitical queries where Google documents limitations.

## 11.5 Pagination

Text Search can return up to 20 results per page and a maximum of 60 across pages, subject to change.

The connector must request every permitted page until:

- `nextPageToken` is absent
- The source-plan page limit is reached
- The API reports an error
- The run is cancelled
- A cost or quota boundary is reached

`nextPageToken` must be included in the response field mask.

## 11.6 Query saturation

A query that reaches the maximum available depth is marked:

```text
SATURATED
```

Refinement actions may include:

- Smaller geography
- Narrower type
- Local-language synonym
- More specific organization subtype
- Zone-specific query
- Separate branded-chain query

## 11.7 Non-determinism

Google documents that identical Text Search requests are not guaranteed to return identical place lists.

Every query must retain:

- Request hash
- Query text
- Location restriction
- Type filters
- Language and region
- Field mask
- Request time
- Page token
- Connector version
- Response status

---

## 12. Query and page ledger

## 12.1 `GoogleQueryRun`

```text
id
source_run_id
source_plan_id
coverage_cell_id
search_method
query_family
query_text
included_types
excluded_types
included_primary_types
excluded_primary_types
included_type
strict_type_filtering
location_policy
location_request
rank_preference
language_code
region_code
include_future_opening_businesses
include_service_area_businesses
field_mask_version
request_hash
status
started_at
completed_at
```

## 12.2 `GoogleQueryPage`

```text
id
query_run_id
page_number
page_token_hash
request_attempts
http_status
api_status
result_count
next_page_token_present
response_received_at
estimated_sku
estimated_cost
failure_code
failure_message
retry_after
status
```

## 12.3 Query statuses

```text
PLANNED
RUNNING
SUCCEEDED
NO_RESULTS
PARTIAL
SATURATED
RATE_LIMITED
AUTHENTICATION_FAILED
PERMISSION_DENIED
INVALID_REQUEST
QUOTA_EXHAUSTED
SERVER_ERROR
TIMEOUT
RETRY_EXHAUSTED
CANCELLED
```

## 12.4 Completion semantics

```text
NO_RESULTS
≠ FAILED

PARTIAL
≠ COMPLETED

SATURATED
≠ COMPLETE_COVERAGE
```

A source run may be completed with accepted limitations only when those limitations are explicit in the coverage report.

---

## 13. Field-mask architecture

Field masks determine response content, latency, and billing tier.

They must be versioned.

## 13.1 Discovery ID profile

Purpose:

- Obtain Place IDs with the lowest practical field tier
- Deduplicate before enrichment

Candidate Text Search mask:

```text
places.id
places.name
places.movedPlace
places.movedPlaceId
nextPageToken
```

Text Search supports an IDs-only tier for these fields.

Nearby Search does not offer the same IDs-only tier; even `places.id` is within its Pro field set. The cost plan must account for that difference.

## 13.2 Discovery classification profile

Purpose:

- Place ID
- Basic classification
- Business status
- Location for immediate coverage processing

Candidate fields:

```text
places.id
places.name
places.displayName
places.primaryType
places.types
places.businessStatus
places.location
places.movedPlace
places.movedPlaceId
nextPageToken
```

This profile may trigger a Pro SKU.

## 13.3 Place Details identity profile

```text
id
name
movedPlace
movedPlaceId
addressComponents
formattedAddress
location
types
businessStatus
displayName
primaryType
openingDate
pureServiceAreaBusiness
googleMapsLinks
googleMapsUri
```

## 13.4 Place Details contact profile

```text
internationalPhoneNumber
nationalPhoneNumber
websiteUri
regularOpeningHours
currentOpeningHours
userRatingCount
rating
```

These fields may trigger an Enterprise tier.

## 13.5 Atmosphere profile

Fields such as `reviews` and review summaries may trigger Enterprise + Atmosphere pricing.

They must never be part of the default discovery profile.

## 13.6 Photo profile

`photos` references are retrieved separately from actual media.

Photo media calls have their own SKU.

## 13.7 Wildcard prohibition

Production must not use:

```text
X-Goog-FieldMask: *
```

The exact field mask used by every request must be persisted as a versioned profile reference.

---

## 14. Place ID registry and deduplication

## 14.1 `GooglePlaceReference`

```text
id
tenant_id
google_place_id
resource_name
first_seen_at
last_seen_at
last_refreshed_at
current_status
superseded_by_place_id
refresh_due_at
source_plan_ids
query_run_ids
canonical_institution_id
branch_id
```

## 14.2 Within-run deduplication

The same Place ID may appear in:

- Multiple synonyms
- Multiple query pages
- Nearby and Text Search
- Popularity and distance passes
- Overlapping coverage cells

The run must create:

```text
one GooglePlaceReference
many discovery links
one bounded details request per field profile
```

## 14.3 Cross-run refresh

Google recommends refreshing Place IDs older than 12 months.

The registry should schedule a refresh before relying on an old ID.

## 14.4 Moved places

When Place Details returns:

```text
movedPlace
movedPlaceId
```

Harvester must:

1. Preserve the provider-level relationship.
2. Retrieve the next place where permitted.
3. Follow chains with a bounded hop limit.
4. Avoid merging old and new branches without resolution evidence.
5. Mark the old place permanently closed.
6. Create a review task when organization continuity is ambiguous.

## 14.5 Multiple IDs for one place

Place ID equality is strong evidence for a match.

Place ID inequality does not prove different entities.

Resolution still considers:

- Name
- Phone
- Website
- Address
- Coordinates within permitted use
- Branch context
- Moved-place relationship
- Independent sources

---

## 15. Place Details enrichment

## 15.1 Enrichment policy

Not every discovered Place ID should receive every detail field.

Eligibility may consider:

- Target type
- Target geography
- Business status
- Deduplication status
- Existing canonical match
- Cost budget
- Research priority
- Source-plan objective

## 15.2 Identity and branch fields

Potential fields:

```text
id
name
displayName
formattedAddress
shortFormattedAddress
addressComponents
postalAddress
location
plusCode
primaryType
types
businessStatus
openingDate
pureServiceAreaBusiness
movedPlace
movedPlaceId
googleMapsUri
googleMapsLinks
```

## 15.3 Contact and operating fields

Potential fields:

```text
internationalPhoneNumber
nationalPhoneNumber
websiteUri
regularOpeningHours
currentOpeningHours
userRatingCount
rating
```

## 15.4 Structured address extraction

`addressComponents` should be requested when Harvester needs:

- City
- Administrative area
- Postal code
- Country code
- Street components

Address components can change order and may be absent in later responses.

Extraction must use component types, not fixed array positions.

## 15.5 Business status

Supported statuses include:

```text
OPERATIONAL
CLOSED_TEMPORARILY
CLOSED_PERMANENTLY
FUTURE_OPENING
```

Behavior:

- `CLOSED_PERMANENTLY` invokes qualification or eligibility review.
- `CLOSED_TEMPORARILY` remains visible and is not treated as permanently closed.
- `FUTURE_OPENING` may create a timing signal.
- Missing status remains unknown.

## 15.6 Website field

Google describes `websiteUri` as the authoritative website for the place, often for the individual branch rather than the overall chain.

Harvester must distinguish:

```text
BRANCH_WEBSITE_CANDIDATE
ORGANIZATION_WEBSITE_CANDIDATE
UNKNOWN_SCOPE
```

The URL should be treated as a transient seed until independently verified.

## 15.7 Phone field

Google phone fields support general contactability.

They do not identify a person or decision-maker.

A Google phone observation must not create:

- Person name
- Job title
- Decision authority
- Consent

---

## 16. Reviews

## 16.1 Public Places reviews

The Place resource may return at most five reviews, sorted by relevance.

This is not a complete review dataset.

Public Places reviews may contain:

```text
review resource name
localized text
original text
rating
author attribution
publish time
visit date
Google Maps URI
```

## 16.2 Review limitations

The returned reviews are:

- Limited in number
- Relevance-selected
- Potentially language-dependent
- User-generated
- Not statistically representative
- Potentially stale
- Potentially unrelated to infrastructure

## 16.3 Potential intelligence value

Reviews may reveal hypotheses concerning:

- Digital-access friction
- Failed booking or portal experience
- Repeated data submission
- Manual queues
- Communication failures
- Reliability problems
- Customer-service delay
- Branch inconsistency

## 16.4 Public-review scoring restriction

Because Google terms restrict copying reviews and creating content from Google Maps Content, public reviews must not automatically become permanent Harvester score inputs.

Default policy:

```text
PUBLIC_GOOGLE_REVIEW
→ transient operator context only
→ attribution required
→ no model training
→ no permanent derived claim
→ no Opportunity Score contribution
```

A different policy requires explicit legal approval identifying the permitted use, retention period, attribution, and transformation limits.

## 16.5 Independent corroboration path

A review may trigger independent research:

```text
Google review mentions broken portal
→ inspect official website portal
→ inspect service-status or public notices
→ collect permitted independent evidence
→ score the independently supported infrastructure condition
```

The permanent score explanation references the independent evidence, not copied Google review text.

## 16.6 Authorized Business Profile reviews

For customer-owned managed locations, the Reviews API may support:

- Review retrieval
- Review response workflows
- Operational theme analysis
- Customer-experience reporting

This remains subject to Business Profile API policies and tenant authorization.

Authorized-review analysis must preserve:

- Location ownership
- OAuth subject
- Permission scope
- Review provenance
- Customer policy
- Retention policy
- Model-use restrictions

---

## 17. Photos

## 17.1 Place photo references

A Place result may return up to ten photo references.

Each photo record may include:

```text
photo resource name
width
height
author attributions
flag-content URI
Google Maps URI
```

## 17.2 Place Photos request

Endpoint form:

```text
GET https://places.googleapis.com/v1/{PHOTO_NAME}/media
```

Request must provide:

- API key
- `maxHeightPx`, `maxWidthPx`, or both

Supported size values are bounded by Google documentation.

## 17.3 Photo-name caching

Google documents that photo names cannot be cached and may expire.

Harvester must obtain a current photo name from a current Place response before requesting media.

## 17.4 Attribution

When `authorAttributions` is present, Harvester must display the required attribution wherever the photo is shown.

## 17.5 Potential intelligence value

Photos may support operator hypotheses about:

- Facility footprint
- New construction
- Branch branding
- Physical assets
- Service environment
- Equipment context
- Connected Infrastructure relevance

## 17.6 Photo limitations

A photo may be:

- Old
- Promotional
- User-contributed
- Misleading
- Atypical
- Associated with a different period
- Focused on appearance rather than operations

A photo cannot prove:

- No software exists
- No automation exists
- No telemetry exists
- A system is reliable
- A facility is operationally mature

## 17.7 Public-photo scoring restriction

Default policy:

```text
PUBLIC_GOOGLE_PHOTO
→ operator-facing attributed context
→ no model training
→ no permanent computer-vision extraction
→ no Opportunity Score contribution
```

Any image-analysis workflow requires explicit legal and compliance approval.

## 17.8 Authorized Business Profile media

Customer-authorized media may be analyzed under a separate Business Profile policy when:

- The customer controls the profile
- The use is within the approved purpose
- The media policy allows analysis
- Model use is approved
- Retention and deletion are defined

---

## 18. Google Business Profile authorized mode

## 18.1 Access prerequisites

- Valid Google Account
- Valid business reason
- Google Cloud project
- Approved Business Profile API access
- OAuth 2.0 credentials
- `business.manage` scope where applicable
- Authorized account and location access

## 18.2 Tenant isolation

Every connection must bind:

```text
tenant_id
connection_id
google_account_subject
approved_accounts
approved_locations
scopes
access_granted_at
access_expires_at
refresh_token_reference
revocation_state
```

One tenant must never access another tenant's Business Profile data.

## 18.3 Managed-location mapping

```text
GoogleManagedLocation
```

Recommended fields:

```text
id
tenant_id
connection_id
google_account_name
google_location_name
store_code
place_id
canonical_institution_id
branch_id
verification_state
voice_of_merchant_state
mapping_confidence
mapping_review_state
first_synced_at
last_synced_at
```

## 18.4 Local Posts

Posts may include:

- Updates
- Events
- Offers
- Calls to action

Potential intelligence value:

- Expansion
- Launches
- Service changes
- Promotions
- Time-bound events
- Booking initiatives
- Customer communication cadence

Posts are timing and operating signals for the authorized customer's own locations, not public prospect data to scrape.

## 18.5 Performance API

The Business Profile Performance API provides daily and monthly metrics for authorized managed locations.

Potential metrics include:

- Search impressions
- Maps impressions
- Website clicks
- Call clicks
- Direction requests
- Conversations
- Bookings
- Food-order interactions
- Menu interactions
- Search keyword impressions

The available metric enum must be read from the current API version at implementation time.

## 18.6 Performance-derived indicators

Potential customer-authorized metrics:

```text
Digital Demand
Contact Engagement Rate
Website Engagement Rate
Direction Intent Rate
Booking Conversion Proxy
Demand Growth
Search Intent Mix
```

Example formulas:

```text
Digital Demand = Search impressions + Maps impressions

Website Engagement Rate = Website clicks ÷ eligible impressions

Contact Engagement Rate = Call clicks ÷ eligible impressions

Demand Growth = current period ÷ comparable prior period
```

Rules:

- Use minimum-volume thresholds.
- Preserve raw metric definitions.
- Do not compare incompatible periods.
- Record timezone and date boundaries.
- Mark unavailable metrics as unknown.
- Do not infer causation from correlation.

## 18.7 Authorized scoring role

Business Profile performance is primarily customer operational intelligence.

It may support:

- Current customer diagnostics
- Digital access optimization
- Service conversion analysis
- Branch performance comparison
- Infrastructure investment justification

It should not be used as public-prospect intelligence without explicit authorization.

---

## 19. Website-crawler handoff

## 19.1 Website present in Google

```text
Google websiteUri
→ transient URL seed
→ URL safety validation
→ domain normalization
→ duplicate crawl check
→ official website crawl
→ website self-identification
→ independent WEBSITE observation
```

## 19.2 Website absent from Google response

```text
websiteUri missing
→ WEBSITE_NOT_DETECTED_BY_GOOGLE
→ independent website discovery
```

Independent discovery may use:

- Approved web search provider
- Exact organization-name query
- Organization name plus city
- Organization name plus phone
- Official registry
- Sector directory
- Authorized import
- Independently discovered social profile

Only after sufficient coverage may a capability assessment consider `ABSENT_CONFIRMED`.

## 19.3 Crawler blocklist

The website crawler must reject:

```text
maps.google.com
www.google.com/maps
google.com/maps
places.googleapis.com
maps.googleapis.com
streetviewpixels-pa.googleapis.com
```

API clients may call approved API endpoints. The general crawler may not.

## 19.4 Google links

`googleMapsUri` and `googleMapsLinks` are operator navigation links.

They may support:

- Open place
- Directions
- View reviews
- View photos
- Write review

They are not crawler seeds.

---

## 20. Extraction and normalization contracts

## 20.1 Transient Google place observation

```text
GoogleTransientPlaceObservation
```

Recommended fields:

```text
request_id
query_page_id
place_id
resource_name
retrieved_at
field_mask_version
response_hash
permitted_transient_payload_reference
attribution_requirements
expiry_at
processing_state
```

The transient payload must be automatically deleted according to the approved Google compliance policy.

## 20.2 Persisted Google identifier record

```text
GooglePlaceReference
```

Persists only permitted provider identifiers and governance metadata.

## 20.3 Independent branch candidate

After independent confirmation, Harvester may create a normal evidence-backed branch candidate containing:

```text
organization_name
branch_name
address
city
country_code
postal_code
website
phone
operating_status
location
source_type
source_reference
```

Every retained field must identify the independent source that supports it.

## 20.4 Contact extraction

Google public mode may identify a general phone or website candidate.

It must not fabricate:

- Email
- Person name
- Role
- Decision authority

## 20.5 Source-native and canonical separation

```text
Google primaryType
≠ Harvester organization type

Google businessStatus
≠ final qualification

Google Place ID
≠ canonical institution ID

Google phone
≠ verified decision-maker contact
```

---

## 21. Evidence-state semantics

Every Google-derived claim uses explicit states.

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_INSPECTED
INSPECTION_FAILED
UNKNOWN
NOT_APPLICABLE
CONTRADICTED
STALE
```

### 21.1 Examples

| Observation | Correct state |
|---|---|
| Google returns websiteUri | `PRESENT_FROM_GOOGLE` |
| Google omits websiteUri | `NOT_DETECTED` |
| Text Search returns no results | `NO_RESULTS_FOR_QUERY` |
| API request times out | `INSPECTION_FAILED` |
| Place is closed permanently | `PRESENT` for status assertion |
| Review mentions no online booking | `TRANSIENT_PUBLIC_CONTEXT` |
| Official website has no booking path after full crawl | `NOT_DETECTED_ON_WEBSITE` |
| Customer confirms no booking system | `ABSENT_CONFIRMED` |

---

## 22. Opportunity Scoring Model v3 integration

## 22.1 Public Google Places contributions

Public Places may support discovery or independent-research planning for:

| v3 concern | Google role |
|---|---|
| Organization existence | Provider-level discovery evidence |
| Branch footprint | Candidate branch evidence |
| Operating status | Public source assertion |
| Organization-type candidate | Source-native classification |
| General contact path | Public phone and website candidates |
| Website presence candidate | `websiteUri` present |
| Account-scale proxy | Number of independently resolved branches |
| Identity resolution | Place ID and transient matching evidence |
| Buying timing | Future opening or moved-place signal |

## 22.2 Public Google Places must not independently prove

- No website exists
- No CRM exists
- No ERP exists
- No LMS exists
- No portal exists
- No automation exists
- No Connected Infrastructure exists
- Internal systems are weak
- Operations are manual
- Procurement is active
- Budget exists
- A named decision-maker exists
- Communication consent exists

## 22.3 Public reviews and photos

Default v1 rule:

```text
No direct Opportunity Score contribution.
```

They may create operator-visible research prompts where compliant.

## 22.4 Independently confirmed evidence

When a Google signal leads to independent confirmation, the independent evidence may contribute to v3 normally.

Example:

```text
Google omits websiteUri
→ independent search finds no official domain
→ registry and sector directory also show none
→ operator/customer confirmation
→ website absence may become ABSENT_CONFIRMED
```

## 22.5 Authorized Business Profile contributions

For customer-owned locations, approved Business Profile performance may support:

- Digital access analysis
- Demand and engagement analysis
- Branch-level visibility
- Timing and momentum
- Operational improvement priorities

This is not prospect scoring unless the customer has authorized that purpose and the policy permits it.

---

## 23. Cost and billing governance

## 23.1 SKU-aware design

Google Places billing depends on method and requested fields.

Relevant categories include:

- Text Search IDs Only
- Text Search Pro
- Text Search Enterprise
- Text Search Enterprise + Atmosphere
- Nearby Search Pro
- Nearby Search Enterprise
- Nearby Search Enterprise + Atmosphere
- Place Details IDs Only
- Place Details Essentials
- Place Details Pro
- Place Details Enterprise
- Place Details Enterprise + Atmosphere
- Place Details Photos

The document deliberately does not lock currency amounts because Google pricing changes.

## 23.2 Cost ledger

```text
GoogleUsageLedger
```

Recommended fields:

```text
id
tenant_id
source_run_id
query_run_id
query_page_id
method
field_mask_version
estimated_sku
request_count
response_count
estimated_unit_cost
estimated_total_cost
currency
pricing_snapshot_version
billing_project
recorded_at
```

## 23.3 Budget controls

Before execution:

```text
estimated requests
× expected SKU cost
≤ approved run budget
```

Runtime stopping conditions:

- Maximum request count
- Maximum unique places
- Maximum estimated cost
- Daily quota threshold
- Monthly quota threshold
- Error-rate threshold
- Marginal-yield threshold

## 23.4 Marginal yield

Track:

```text
new unique Place IDs per request
new accepted institutions per request
new accepted institutions per estimated cost
```

Stop or refine a query family when marginal yield falls below the source-plan threshold.

## 23.5 Discovery before enrichment

The connector should:

```text
find IDs
→ deduplicate
→ enrich selected unique places
```

It should not request Enterprise or Atmosphere fields on every overlapping discovery query.

---

## 24. Quota, retry, and failure handling

## 24.1 Retryable conditions

Potentially retryable:

- Timeout
- Connection reset
- HTTP 429
- Selected 5xx responses
- Temporary upstream errors

## 24.2 Non-retryable conditions

Normally non-retryable until configuration changes:

- Invalid API key
- Permission denied
- Invalid field mask
- Invalid type
- Conflicting included and excluded types
- Invalid location restriction
- Billing disabled

## 24.3 Retry policy

```text
bounded exponential backoff
+ jitter
+ server Retry-After where supplied
+ maximum attempts
+ circuit breaker
```

## 24.4 Failure preservation

Every failure must remain visible.

The connector must never convert an error into `[]` without a failure record.

## 24.5 Partial completion

A run may be `PARTIAL` when:

- Some cells succeeded
- Some query families failed
- Pagination was incomplete
- Cost budget stopped execution
- Quota was exhausted
- Saturation was accepted

The coverage report must identify exactly what was not inspected.

---

## 25. Security and credentials

## 25.1 Public Places credential

Use a server-side credential that is:

- Stored outside source code
- Encrypted at rest
- Restricted to required Google APIs
- Restricted by server IP or network where practical
- Separate by environment
- Separate from browser credentials
- Monitored for unexpected usage
- Rotatable

## 25.2 Business Profile OAuth

Store:

- Encrypted refresh-token reference
- OAuth subject
- Granted scopes
- Authorized accounts and locations
- Grant time
- Last refresh
- Revocation status

Tokens must be tenant isolated and never exposed to the frontend.

## 25.3 Proxy behavior

Clients must not relay arbitrary Google API methods through Harvester.

Server endpoints must:

- Authenticate the Harvester user
- Authorize tenant and action
- Validate a fixed request contract
- Apply source-plan limits
- Filter response fields
- Audit access

## 25.4 Secret logging prohibition

Never log:

- API key
- OAuth access token
- Refresh token
- Authorization code
- Full credential payload

## 25.5 Usage monitoring

Alert on:

- Unusual request volume
- Requests from unexpected IPs
- New API methods
- Unexpected SKU escalation
- Quota spikes
- Repeated authentication failures

---

## 26. Retention, attribution, and compliance

## 26.1 Google compliance profile

```text
GoogleComplianceProfile
```

Recommended fields:

```text
id
profile_version
terms_reviewed_at
terms_version_reference
service_specific_terms_reference
approved_services
approved_fields
prohibited_fields
permitted_identifiers
transient_cache_periods
latitude_longitude_expiry_days
photo_name_cache_policy
review_policy
photo_policy
derived-content_policy
machine-learning-policy
attribution_policy
display_policy
deletion_policy
legal_approval_reference
activated_at
retired_at
```

## 26.2 Default retention posture

Until a legal and policy review approves otherwise:

```text
Place ID
→ persist where permitted

Latitude/longitude
→ transient cache, maximum approved period

Other public Places content
→ transient processing only

Reviews
→ do not copy into permanent Harvester storage

Photos/photo names
→ do not cache beyond permitted request lifecycle

Derived score from public Google reviews/photos
→ prohibited by default
```

## 26.3 Attribution

Whenever Google Maps Content is displayed, required Google and author attribution must be displayed without alteration or obscuring.

## 26.4 No model training

Google Maps Content must not be used to train, test, validate, or fine-tune machine-learning or artificial-intelligence models.

This includes:

- Review sentiment training sets
- Photo classifiers
- Entity-resolution training data
- Opportunity-scoring training data
- Extraction model evaluation sets

## 26.5 Terms review cadence

Review current Google terms and API documentation:

- Before first production activation
- Before enabling a new field family
- Before enabling reviews or photos
- Before enabling Business Profile APIs
- At least annually
- After a material Google policy notification

---

## 27. Observability and source report

A Google source run should expose:

### Coverage

- Areas planned
- Areas completed
- Cells planned
- Cells completed
- Cells failed
- Cells saturated
- Type groups planned
- Type groups completed
- Query families planned
- Query families completed
- Pages planned or discovered
- Pages completed

### Yield

- Total result appearances
- Unique Place IDs
- Duplicate appearances
- New Place IDs
- Existing Place IDs
- Unique canonical institutions
- New canonical institutions
- New branches
- Review-required resolutions
- Permanently closed places
- Temporarily closed places
- Future-opening places

### Enrichment

- Details requested
- Details completed
- Details failed
- Websites detected
- Phones detected
- Moved places
- Reviews requested
- Photos requested

### Quality

- Invalid records
- Contradictions
- Stale Place IDs
- Ambiguous type mappings
- Missing structured addresses
- Low-confidence resolutions

### Operations

- Request count by method
- Request count by SKU
- Estimated cost
- Retry count
- Rate-limit count
- Error count
- p50/p95 latency
- Quota consumption

### Compliance

- Transient records awaiting deletion
- Expired coordinate caches
- Attribution exceptions
- Unauthorized-field attempts
- Policy version

---

## 28. Planned domain objects

```text
GoogleConnection
GoogleBusinessProfileConnection
GoogleSourcePlan
GoogleCoverageCell
GoogleTypeMapping
GoogleQueryRun
GoogleQueryPage
GooglePlaceReference
GoogleDetailsFetch
GoogleTransientPlaceObservation
GoogleManagedLocation
GoogleReviewAccessRecord
GooglePhotoAccessRecord
GoogleBusinessProfilePost
GoogleBusinessProfileMetricSeries
GoogleBusinessProfileKeywordMetric
GoogleUsageLedger
GoogleComplianceProfile
GoogleAttributionRecord
```

All objects must be tenant-aware where applicable.

---

## 29. Planned Harvester APIs

Conceptual interfaces:

```http
GET  /api/v1/google/connections
POST /api/v1/google/connections
POST /api/v1/google/connections/{connection_id}/validate

GET  /api/v1/google/source-plans
POST /api/v1/google/source-plans
GET  /api/v1/google/source-plans/{source_plan_id}
POST /api/v1/google/source-plans/{source_plan_id}/estimate
POST /api/v1/google/source-plans/{source_plan_id}/execute

GET  /api/v1/google/runs/{run_id}
GET  /api/v1/google/runs/{run_id}/coverage
GET  /api/v1/google/runs/{run_id}/queries
GET  /api/v1/google/runs/{run_id}/usage

POST /api/v1/google/place-ids/{place_id}/refresh
GET  /api/v1/google/place-ids/{place_id}

POST /api/v1/google/business-profile/authorize
GET  /api/v1/google/business-profile/accounts
GET  /api/v1/google/business-profile/locations
POST /api/v1/google/business-profile/locations/{location_id}/sync
GET  /api/v1/google/business-profile/locations/{location_id}/performance
```

The exact routes remain subordinate to the roadmap and API conventions.

---

## 30. Planned events

```text
google.source_plan_created
google.source_plan_approved
google.run_started
google.coverage_cell_started
google.coverage_cell_saturated
google.query_succeeded
google.query_failed
google.query_rate_limited
google.place_discovered
google.place_deduplicated
google.place_details_refreshed
google.place_moved
google.place_closed
google.website_seed_created
google.compliance_expiry_due
google.transient_content_deleted
google.business_profile_authorized
google.business_profile_revoked
google.business_profile_location_synced
google.business_profile_metrics_refreshed
```

Events must not include secrets or prohibited Google content.

---

## 31. Implementation sequence

## Gate 1: Compliance and product decision

- Review current Google Maps Platform Terms.
- Review current Service Specific Terms.
- Define permitted persisted identifiers and fields.
- Define prohibited derived uses.
- Define attribution behavior.
- Decide whether public Google Places is commercially compatible with Harvester's product model.
- Record legal approval or reject the integration.

This gate comes first. Building a sophisticated prohibited data pipeline would be a rather expensive way to discover contracts exist.

## Gate 2: Connector correctness

- Replace empty-list-on-error behavior with typed outcomes.
- Add async HTTP client behavior.
- Add timeout and retry policy.
- Add query and page ledger.
- Add field-mask versions.
- Add pagination.
- Preserve exact request metadata.

## Gate 3: Geographic coverage

- Replace zone-text stub with geometry-backed cells.
- Add Nearby Search.
- Add type-group passes.
- Add saturation detection.
- Add subdivision rules.
- Add coverage reporting.

## Gate 4: Place ID registry

- Deduplicate within and across runs.
- Add refresh dates.
- Add moved-place handling.
- Add old-ID refresh workflow.
- Link Place IDs to resolution evidence without making them canonical identity.

## Gate 5: Bounded Place Details

- Add discovery and enrichment profiles.
- Add structured address extraction.
- Add business-status handling.
- Add transient website and phone handoff.
- Add compliance-driven deletion.

## Gate 6: Website handoff

- Validate and normalize website seeds.
- Block Google Maps crawling.
- Crawl official websites independently.
- Store website-sourced evidence.
- Preserve `NOT_DETECTED` versus `ABSENT_CONFIRMED`.

## Gate 7: Optional public reviews and photos

- Keep disabled by default.
- Require compliance approval.
- Implement attribution.
- Implement transient-only handling.
- Prohibit model training.
- Verify no direct score contribution unless separately approved.

## Gate 8: Authorized Business Profile

- Implement OAuth.
- Add account/location mapping.
- Add tenant isolation.
- Add Reviews, Posts, Media, and Performance integrations as approved.
- Add revocation and deletion.

## Gate 9: Cost and operations

- Add SKU-aware estimates.
- Add quotas and budgets.
- Add marginal-yield stopping rules.
- Add dashboards and alerts.

## Gate 10: Shadow mode

- Run beside current connector.
- Compare coverage, cost, duplicate rate, resolution quality, and failure visibility.
- Do not change production selection until verified.

---

## 32. Verification scenarios

The integration is not complete until tests prove that:

1. A missing `websiteUri` becomes `NOT_DETECTED`, not `ABSENT_CONFIRMED`.
2. A failed Google call becomes `INSPECTION_FAILED`, not no results.
3. Authentication failure fails the appropriate query and is visible.
4. Rate limits trigger bounded retry and remain visible.
5. Text Search pagination continues while a next-page token exists.
6. A saturated Text Search query is marked saturated.
7. Nearby Search result count of 20 triggers possible saturation.
8. Coverage-cell subdivision is bounded.
9. Duplicate Place IDs across queries create one place reference.
10. Duplicate Place IDs retain all discovery links.
11. Place Details is called only according to enrichment policy.
12. Field masks map to the expected cost profile.
13. Production never uses wildcard field masks.
14. Address components are parsed by component type, not array position.
15. Permanently closed places do not silently qualify.
16. Temporarily closed places remain distinct.
17. Future-opening places create a time-bounded signal.
18. Moved-place chains are bounded and reviewable.
19. Old Place IDs receive refresh scheduling.
20. Google `primaryType` does not overwrite Harvester taxonomy directly.
21. General phone does not create a decision-maker.
22. Public reviews do not enter permanent score inputs by default.
23. Public photos do not enter computer-vision pipelines by default.
24. Google Maps URLs are blocked by the website crawler.
25. Google `websiteUri` can create a transient seed.
26. The official website becomes an independent WEBSITE source after validation.
27. Place coordinates expire under the approved cache policy.
28. Photo names are not cached.
29. Required attribution is rendered when Google content is displayed.
30. Google content is excluded from model training datasets.
31. Cost limits stop new requests without hiding partial coverage.
32. Query failures do not mark the whole geography complete.
33. Business Profile data cannot cross tenants.
34. OAuth revocation stops authorized sync.
35. Performance metrics retain date, timezone, and metric definitions.
36. Small denominators do not produce unqualified conversion claims.
37. Every source-run report exposes coverage, yield, failures, cost, and policy version.
38. Events contain no credentials or prohibited content.
39. Current and target connector behavior can be compared in shadow mode.
40. Exact-head tests and CI pass without unresolved issues.

---

## 33. Production acceptance criteria

Production activation requires:

- Written Google compliance profile approved.
- Product use confirmed compatible with current Google terms.
- General Maps-page scraping prohibited technically and procedurally.
- Credential restrictions verified.
- Query and page outcomes persisted.
- Pagination implemented.
- Nearby Search implemented where approved.
- Real geographic coverage implemented.
- Saturation visible.
- Typed failures implemented.
- Place ID registry implemented.
- Field-mask and cost profiles versioned.
- Bounded details enrichment implemented.
- Google content retention and deletion enforced.
- Website handoff independently verifies retained facts.
- Public reviews and photos disabled unless specifically approved.
- Business Profile mode isolated behind OAuth and tenant authorization.
- Attribution verified.
- Security, privacy, and audit tests pass.
- Coverage and cost dashboards exist.
- Shadow-mode evaluation is complete.
- Exact-head CI passes without unresolved issues.

---

## 34. Official references

The implementation team must review the current versions before changing behavior.

### Places API

- Text Search (New): https://developers.google.com/maps/documentation/places/web-service/text-search
- Nearby Search (New): https://developers.google.com/maps/documentation/places/web-service/nearby-search
- Place Details (New): https://developers.google.com/maps/documentation/places/web-service/place-details
- Place Photos (New): https://developers.google.com/maps/documentation/places/web-service/place-photos
- Place resource: https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places
- Place Types: https://developers.google.com/maps/documentation/places/web-service/place-types
- Place IDs: https://developers.google.com/maps/documentation/places/web-service/place-id
- Google Maps links: https://developers.google.com/maps/documentation/places/web-service/maps-links

### Business Profile APIs

- Business Profile overview: https://developers.google.com/my-business/content/overview
- API reference overview: https://developers.google.com/my-business/ref_overview
- Google My Business API reference: https://developers.google.com/my-business/reference/rest
- Business Profile Performance API: https://developers.google.com/my-business/reference/performance/rest
- Performance metric package: https://developers.google.com/my-business/reference/performance/rpc/google.mybusiness.performance.v1
- Local Posts: https://developers.google.com/my-business/content/posts-data

### Security, pricing, and terms

- Google Maps Platform security guidance: https://developers.google.com/maps/api-security-best-practices
- Google Maps Platform pricing: https://developers.google.com/maps/billing-and-pricing/pricing
- Google Maps Platform Terms: https://cloud.google.com/maps-platform/terms
- Google Maps Platform Service Specific Terms: https://cloud.google.com/maps-platform/terms/maps-service-terms

---

## 35. Locked Google source definition

> NEWAX Harvester uses official Google APIs as bounded discovery and customer-authorized intelligence sources. Google Places identifies provider-level place references and transient public signals; independently verified sources establish durable Harvester evidence. Missing Google fields never prove absence, Google Maps pages are never scraped, public reviews and photos do not directly drive opportunity scores by default, customer-owned Business Profile data remains permission-bound, and every request is governed by coverage, cost, attribution, retention, security, and current Google terms.
