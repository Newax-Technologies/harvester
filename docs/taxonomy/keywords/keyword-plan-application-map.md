# Harvester Keyword Plan Application Map

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document applies the [Harvester Keyword Profile Development Plan](keyword-profile-development-plan.md) to the existing keyword Markdown registries without replacing, rewriting, collapsing, or reclassifying their current content.

It is also the authoritative documentation sequence for the keyword layer. The exact sector-to-domain-registry, activity-applicability and domain-keyword links are maintained in the [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md).

The existing keyword files remain the controlled datasets. The development plan defines how those datasets will later be composed, tested, executed, evidenced, qualified, reviewed, versioned, and integrated into lead generation.

## Documentation and implementation sequence

Read and apply the documentation in this order:

```text
1. Harvester roadmap and operating authority
2. Services and provider-offering eligibility
3. Broad-sector selection
4. Sector domain registry
5. Domain-to-activity applicability
6. Domain keyword registry
7. Shared activity keyword registry
8. Organization and exclusion controls
9. Active-offering lead-signal profiles
10. Sector overlay
11. Source suitability and source model
12. Query composition and semantic expansion
13. Evidence capture and entity resolution
14. Classification, contradiction, freshness and coverage review
15. Qualification and opportunity assessment
16. Responsible-function and lawful-contact assessment
17. Validation, benchmark, activation and rollback
18. Runtime delivery through existing roadmap modules
```

Use these files as the main sequence:

1. [`../../ROADMAP.md`](../../ROADMAP.md)
2. [`../../architecture/harvester-intelligence-operating-model.md`](../../architecture/harvester-intelligence-operating-model.md)
3. [`../../SERVICES.md`](../../SERVICES.md)
4. [`../../architecture/provider-portfolio-and-lead-generation-profile-model.md`](../../architecture/provider-portfolio-and-lead-generation-profile-model.md)
5. [`../broad-sector-registry.md`](../broad-sector-registry.md)
6. The selected sector domain registry under `docs/taxonomy/`
7. [`../activity-registry.md`](../activity-registry.md) and the selected sector activity mapping
8. The selected sector domain keyword registry in this directory
9. [`activity-keywords-part-1.md`](activity-keywords-part-1.md), [`activity-keywords-part-2.md`](activity-keywords-part-2.md), and [`activity-keywords-part-3.md`](activity-keywords-part-3.md)
10. [`control-profiles.md`](control-profiles.md)
11. [`provider-offering-keyword-profile-standard.md`](provider-offering-keyword-profile-standard.md)
12. [`lead-generation-signal-registry.md`](lead-generation-signal-registry.md) and [`sector-lead-generation-overlays.md`](sector-lead-generation-overlays.md)
13. [`source-signal-matrix.md`](source-signal-matrix.md) and the applicable model under [`../../sources/`](../../sources/README.md)
14. [`source-query-template-library.md`](source-query-template-library.md), [`query-composition-and-evidence-rules.md`](query-composition-and-evidence-rules.md), and [`keyword-expansion-and-composition-engine.md`](keyword-expansion-and-composition-engine.md)
15. [`semantic-entity-and-classification-expansion.md`](semantic-entity-and-classification-expansion.md)
16. [`../../architecture/keyword-evidence-profile-integration-addendum.md`](../../architecture/keyword-evidence-profile-integration-addendum.md)
17. [`keyword-quality-and-review-standard.md`](keyword-quality-and-review-standard.md), [`benchmark-and-gold-set-standard.md`](benchmark-and-gold-set-standard.md), and [`keyword-validation-plan.md`](keyword-validation-plan.md)
18. [`keyword-profile-implementation-plan.md`](keyword-profile-implementation-plan.md) and [`../../delivery/keyword-profile-delivery-addendum.md`](../../delivery/keyword-profile-delivery-addendum.md)

A later file may deepen an earlier rule. It may not silently override provider eligibility, domain identity, activity applicability, evidence invariants, source restrictions, contact policy or the authoritative roadmap.

## 1. Additive rule

The relationship is:

```text
Existing keyword registry
+
Keyword Profile Development Plan
+
This application map
+
Sector Keyword Connection Matrix
=
controlled implementation specification
```

The plan does not supersede:

- canonical domain codes
- canonical activity codes
- domain identity terms
- activity terms
- organization cues
- exclusion profiles
- evidence controls
- lead-generation signals
- source suitability rules
- query composition rules
- decision-maker cues
- contact-route safeguards
- cross-product boundaries

When a conflict is discovered, it must be resolved through explicit change control. Existing registry content must not be silently replaced by generated plan language.

## 2. Canonical activity keyword registries

These files supply the shared activity-term layer used by approved domain-specific activity selections:

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

Plan application:

1. Preserve one canonical keyword identity per activity code.
2. Compose activity terms only after the user approves that activity for the selected domain.
3. Do not propagate activity selection between domains.
4. Preserve match mode, language, term type, status, and profile version.
5. Benchmark activity terms independently from domain identity terms.
6. Treat an activity match as evidence, not proof that the organization performs the activity.

## 3. Sector-specific domain keyword registries

Each domain registry supplies identity terms, aliases, organization cues, exclusions, and evidence controls for its own canonical domains.

The exact upstream domain and activity files for every sector are listed in the [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md).

### `BS-001 Healthcare`

- [Healthcare domain keywords, part 1](healthcare-domain-keywords-part-1.md)
- [Healthcare domain keywords, part 2](healthcare-domain-keywords-part-2.md)

Plan application:

- Keep medicines, devices, supplies, clinical services, digital health, operational support, research, education, and public-health profiles separate.
- Apply sensitive-health exclusions and stronger source requirements where appropriate.
- Do not infer clinical service delivery from product terminology or infer manufacturing from medicine mentions.

### `BS-002 Education`

- [Education domain keywords](education-domain-keywords.md)

Plan application:

- Keep institutions, education services, learning content, education technology, assessment, research, and support operations separate.
- Distinguish schools, universities, training providers, content publishers, platforms, and education-service organizations.
- Do not treat an individual course, student record, or job advertisement as an organization.

### `BS-003 Food and Agriculture`

- [Food and Agriculture domain keywords](food-agriculture-domain-keywords.md)

Plan application:

- Separate crops, livestock, fisheries, inputs, processing, food products, cold chain, distribution, and agricultural services.
- Compose growing, processing, manufacturing, grading, storing, distributing, selling, and exporting activities independently.
- Preserve food-safety, halal, seasonal, geographic, and commodity ambiguity controls.

### `BS-004 Real Estate`

- [Real Estate domain keywords](real-estate-domain-keywords.md)

Plan application:

- Separate development, brokerage, property management, facilities, valuation, leasing, investment, and property technology.
- Distinguish a property listing from an operating organization.
- Require corroboration for broad words such as property, asset, development, project, unit, and management.

### `BS-005 Construction`

- [Construction domain keywords](construction-domain-keywords.md)

Plan application:

- Separate contractors, engineering, architecture, materials, systems, equipment, installation, inspection, and project services.
- Preserve the distinction between physical systems and software systems.
- Compose manufacturing, supplying, installing, maintaining, renting, and recycling activities separately.

### `BS-006 Legal`

- [Legal domain keywords](legal-domain-keywords.md)

Plan application:

- Separate practice areas, legal institutions, legal operations, compliance services, dispute resolution, and legal technology.
- Distinguish law firms and service providers from judgments, cases, articles, legislation, courts, and individual lawyers.
- Treat role terms as responsibility cues, not guaranteed purchasing authority.

### `BS-007 Finance`

- [Finance domain keywords](finance-domain-keywords.md)

Plan application:

- Separate banking, payments, investment, Takaful, accounting, audit, tax, risk, compliance, and financial technology.
- Apply strict ambiguity controls to terms such as trust, security, filing, asset, audit, capital, and account.
- Preserve Islamic finance and Takaful identities rather than merging them into conventional finance profiles.

### `BS-008 Retail`

- [Retail domain keywords](retail-domain-keywords.md)

Plan application:

- Separate product categories, store formats, e-commerce, marketplaces, franchising, retail operations, and supporting systems.
- Distinguish a retailer from a product listing, consumer review, promotional post, or reseller account.
- Compose selling, retailing, reselling, promoting, distributing, warehousing, and fulfilment independently.

### `BS-009 Hospitality`

- [Hospitality domain keywords](hospitality-domain-keywords.md)

Plan application:

- Separate accommodation, food service, venues, events, guest services, property operations, and hospitality systems.
- Keep Hospitality distinct from Travel while allowing explicit cross-sector mappings.
- Distinguish a hotel, restaurant, venue, or operator from a booking listing or consumer review.

### `BS-010 Travel`

- [Travel domain keywords](travel-domain-keywords.md)

Plan application:

- Separate travel agencies, tour operations, destination services, pilgrimage services, ticketing, transport-linked travel, and travel systems.
- Keep Travel distinct from Hospitality and Logistics.
- Apply geographic, seasonal, itinerary, destination, and package ambiguity controls.

### `BS-011 Manufacturing and Industry`

- [Manufacturing and Industry domain keywords](manufacturing-industry-domain-keywords.md)

Plan application:

- Separate manufacturing families, fabrication, assembly, processing, industrial equipment, industrial services, quality, and industrial systems.
- Distinguish a manufacturer from a distributor, supplier, reseller, repairer, or scrap operator.
- Preserve physical manufacturing systems separately from digital manufacturing software.

### `BS-012 Logistics`

- [Logistics domain keywords](logistics-domain-keywords.md)

Plan application:

- Separate freight, postal and courier, last-mile delivery, warehousing, fulfilment, cold chain, fleets, ports, aviation, maritime, and logistics systems.
- Keep postal and courier within the approved shared domain family while preserving their operational subtypes.
- Compose transporting, sorting, storing, delivering, forwarding, clearing, tracking, and returning independently.

### `BS-013 Energy`

- [Energy domain keywords](energy-domain-keywords.md)

Plan application:

- Separate generation, transmission, distribution, renewables, fuels, utilities, water, efficiency, equipment, and energy systems.
- Distinguish physical energy infrastructure from software, analytics, consulting, installation, and maintenance providers.
- Require context for broad terms such as power, grid, solar, utility, plant, distribution, and energy management.

### `BS-014 Technology`

- [Technology domain keywords, part 1](technology-domain-keywords-part-1.md)
- [Technology domain keywords, part 2](technology-domain-keywords-part-2.md)

Plan application:

- Separate software products, SaaS, IT services, infrastructure, cloud, data, cybersecurity, telecommunications, hardware, and technology operations.
- Do not classify every domain containing the word system, platform, data, or network as software without family and organization context.
- Compose developing, publishing, licensing, implementing, integrating, hosting, maintaining, supporting, and reselling independently.

### `BS-015 Government`

- [Government domain keywords](government-domain-keywords.md)

Plan application:

- Separate public administration, municipal services, regulators, public safety, emergency services, public infrastructure, citizen services, and government systems.
- Distinguish a government organization from policy discussion, legislation, political commentary, news, or an individual office-holder.
- Apply public-sector source, authority, procurement, and current-status controls.

### `BS-016 Nonprofit`

- [Nonprofit domain keywords](nonprofit-domain-keywords.md)

Plan application:

- Separate charities, foundations, NGOs, associations, chambers, religious institutions, development organizations, membership bodies, and nonprofit systems.
- Distinguish an operating organization from a campaign, donation page, beneficiary story, event, or volunteer posting.
- Apply mission, program, geography, funding, registration, and current-activity controls.

## 4. Shared control and governance files

### Keyword controls

- [Keyword Control Profiles](control-profiles.md)

Plan application:

- Supply reusable organization cues, exclusions, ambiguity controls, sensitive-sector restrictions, and evidence requirements.
- Remain independently versioned from domain and activity terms.

### Keyword quality

- [Keyword Quality and Review Standard](keyword-quality-and-review-standard.md)

Plan application:

- Govern draft, review, benchmark, approval, activation, monitoring, revision, deprecation, and rollback.
- Prevent malformed stems, overbroad aliases, silent mutation, and untested generated terms.

### Lead-generation signals

- [Lead-Generation Signal Registry](lead-generation-signal-registry.md)

Plan application:

- Supply direct intent, procurement, expansion, hiring, technology, operational pain, compliance, maintenance, budget, contactability, and negative signals.
- Activate only through an applicable active provider offering.

### Sector overlays

- [Sector Lead-Generation Overlays](sector-lead-generation-overlays.md)

Plan application:

- Add sector-specific triggers, operational indicators, scale cues, responsible functions, source guidance, and exclusions.
- Do not replace the underlying domain or activity profiles.

### Decision-makers and contacts

- [Decision-Maker and Contact-Cue Registry](decision-maker-and-contact-cues.md)

Plan application:

- Begin after organization resolution.
- Treat titles as responsibility cues rather than proof of authority.
- Require current affiliation and lawful contact-route evidence.

### Sources

- [Source-to-Signal Matrix](source-signal-matrix.md)

Plan application:

- Determine which source classes can credibly support each signal.
- Preserve source suitability, weakness, freshness, and reliability in evidence.

### Query composition

- [Query Composition and Evidence Rules](query-composition-and-evidence-rules.md)

Plan application:

- Generate precision, recall, entity, negative, and source-specific query families.
- Preserve every contributing profile version, source, locale, geography, match mode, and exclusion.

### Cross-product contract

- [Cross-Product Keyword and Profile Contract](cross-product-keyword-contract.md)

Plan application:

- Expose only bounded references and approved outcomes to NEWAX Core or Communicator.
- Do not copy Harvester's private keyword strategy or raw proprietary configuration into another product.

## 5. Required composition sequence

Every approved target configuration follows:

```text
Provider and business unit
→ active provider offering
→ lead-generation profile
→ sector selection
→ domain selection
→ separate activity approval for that domain
→ domain keyword profile
→ activity keyword profile
→ organization-cue profile
→ exclusion profile
→ offering-specific signal profile
→ sector overlay
→ source rules
→ geography and locale rules
→ versioned query plan
→ evidence observations
→ entity resolution
→ domain and activity classification
→ contradiction, freshness, coverage and duplicate-origin checks
→ qualification
→ supported opportunity
→ responsible-function assessment
→ lawful contact readiness
```

No step may be skipped merely because one keyword appears highly relevant.

## 6. Required version connection

Every activated profile and Harvest Job must preserve the versions of:

```text
provider
business unit
offering
lead-generation profile
broad sector
domain
sector-domain mapping
domain-activity assignment
activity
domain keyword profile
activity keyword profile
organization-cue profile
exclusion profile
offering-signal profiles
sector overlay
source suitability
source model
locale pack
query template
query composition
semantic and classification model
evidence policy
qualification profile
scoring profile
contact policy
```

Later changes apply only to future jobs unless an operator explicitly creates a replacement job.

## 7. Preservation rule

This application map is additive.

It does not authorize replacing the existing Markdown registries with summaries, generated prose, databases, spreadsheets, embeddings, or runtime configuration.

When runtime implementation begins, the approved Markdown records must remain traceable to generated records through stable codes and versions.

## 8. Connection acceptance criteria

The documentation connection is acceptable only when:

1. Every sector resolves to its domain registry, activity mapping and domain keyword registry through the sector connection matrix.
2. Every canonical domain retains one stable identity and one separate keyword profile.
3. Every canonical activity retains one stable identity and one separate activity keyword profile.
4. Activity applicability remains domain-specific.
5. Offering-specific signals require an active selected offering.
6. Every query preserves all contributing profile and source versions.
7. Every match preserves source, context, time, match mode and profile origin.
8. Keyword matches cannot independently create gaps, opportunities or contact-ready leads.
9. Positive evidence is evaluated with applicable exclusions, contradictions, freshness and duplicate-origin controls.
10. Responsible-role and contact discovery cannot bypass organization resolution and supported-opportunity gates.
11. Completed jobs remain reproducible from immutable snapshots.
12. The Harvester roadmap remains the only top-level delivery roadmap.

## 9. Delivery boundary

The development plan, this application map, the sector connection matrix, and all linked registries are controlled documentation datasets.

They do not implement database records, migrations, APIs, user interfaces, search execution, embeddings, classifiers, evidence scoring, opportunity scoring, contact eligibility, outreach, or releases.
