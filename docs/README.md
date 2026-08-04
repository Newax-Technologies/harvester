# Harvester Documentation Map

This directory contains the authoritative product, architecture, source, and delivery documentation for NEWAX Harvester.

Harvester is standalone lead-intelligence infrastructure. It converts a governed, provider-defined service market into evidence-backed, reviewable, and operationally usable opportunities while preserving customer ownership and control.

## Authority order

When documents overlap, use this order:

1. [Harvester Standalone Product Roadmap](ROADMAP.md)
   - Authoritative 64-module product and delivery roadmap
   - Module ownership, outcomes, exclusions, acceptance criteria, delivery gates, and crosswalks

2. [Harvester Intelligence Operating Model](architecture/harvester-intelligence-operating-model.md)
   - Normative operating, evidence, data, decision, confidence, learning, economics, and authority model
   - Strengthens the existing 64 modules without creating a second roadmap

3. [Harvester Services and Opportunity Model](SERVICES.md)
   - Universal provider, service-offering, customer-market, lead-subject, opportunity-signal, qualification, and first-page lead-generation model
   - Requires the complete service and target definition before **Generate Leads**
   - Supports B2B, B2C, referral, professional, healthcare, legal, local, remote, appointment, project, and recurring services
   - Establishes service gap as one signal type rather than the universal product model

4. [NEWAX Harvester Opportunity Scoring Model v3](architecture/opportunity-scoring-model-v3.md)
   - NEWAX-specific provider scoring profile for business-infrastructure opportunities
   - Defines opportunity value, pursuit readiness, infrastructure-gap, coverage, confidence, risk, and recommendation behavior for NEWAX offerings
   - Remains subordinate to the universal services model and must not be applied to unrelated providers or unselected services

5. [Standalone Product and Integration Framework](architecture/standalone-product-and-integration-framework.md)
   - Product boundaries, connector framework, credentials, mappings, synchronization, destinations, tenancy, and recovery

6. [Optional NEWAX Core Synchronization](architecture/newax-core-automatic-sync.md)
   - Optional Harvester-to-Core streams, application identity, credentials, delivery, links, reconciliation, and failure behavior

## Service and market taxonomy

Taxonomy documents define controlled registries and mappings used by the Services and Opportunity Model. They remain subordinate to `SERVICES.md` and cannot independently create an eligible service, gap, opportunity, or lead.

- [Sector, Domain, Activity and Keyword Taxonomy Index](taxonomy/README.md)
  - Links all 16 broad-sector domain registries
  - Covers 1,586 canonical product and service domains
  - Covers 519 canonical business activities
  - Confirms an explicit activity-profile assignment and separate keyword profile for every canonical domain
  - Preserves multi-sector selection, independent domain activity groups, canonical identity reuse, and duplicate prevention

- [Canonical Activity Registry and Domain Mappings](taxonomy/activity-registry.md)
  - Defines the shared 519-activity library with stable activity codes
  - Maps all 1,586 domains to explicit `CORE`, `COMMON`, and `OPTIONAL` applicability profiles
  - Treats activities absent from a profile as `NOT_APPLICABLE` by default
  - Prevents one domain's activity selection from propagating to another domain

- [Keyword Taxonomy Index](taxonomy/keywords/README.md)
  - Defines separate discovery profiles for all 1,586 domains and all 519 canonical activities
  - Separates domain terms, activity terms, organization cues, exclusions, and negative context
  - Defines exact, phrase, semantic, entity, and regex match-mode requirements
  - Keeps problem, buying-intent, competitor, existing-solution, and service-gap keywords subordinate to an active provider offering
  - Prohibits a keyword match from independently proving a domain, activity, service gap, opportunity, or qualified lead

- [Broad Sector Registry and Selection Framework](taxonomy/broad-sector-registry.md)
  - Defines the first-stage registry of 16 broad sectors
  - Supports multiple sectors, multiple domains per sector, and separate activity groups per selected domain
  - Prevents activities from propagating across domains and prevents duplicate targets or scores across overlapping classifications
  - Defines the minimum registry, applicability, selection, provenance, and acceptance requirements

- [Healthcare Product and Service Domain Registry](taxonomy/healthcare-domain-registry.md)
  - Defines the controlled domain registry for broad sector `BS-001 Healthcare`
  - Includes 142 canonical domains across medicines, devices, supplies, facilities, digital health, operations, research, education, and public health
  - Provides a 40-domain first-release presentation shortlist without replacing canonical domain identities
  - Requires independent activity groups, approved domain–activity combinations, cross-sector reuse, evidence attribution, and duplicate prevention

## Source input and formatting

Source documents define how user inputs become immutable job snapshots and how provider-native records enter the Harvester evidence model. They remain subordinate to the roadmap, operating model, services model, applicable scoring profile, integration framework, and provider terms.

- [Source Input and Formatting Index](sources/README.md)
  - Links the user-input storage model, canonical source envelope, adapter template, named provider formats, and remaining approved source families
  - Covers Google, Yandex, LinkedIn, Meta and Instagram, X, Bing, Indeed, Crunchbase, Apple Maps, Telegram, websites, official registries, directories, job boards, procurement, news, marketplaces, imports, APIs and feeds

- [User Input Storage Model](sources/user-input-storage-model.md)
  - Defines tenant-isolated drafts, approvals, provider offerings, market selections, domain-specific activities, keyword versions, source selections, secret references, output policies and immutable Harvest Job input snapshots
  - Prohibits plaintext credential storage and silent mutation of active configurations

- [Canonical Source Record Format](sources/canonical-source-record-format.md)
  - Defines requests, response outcomes, provider-native observations, artifacts, claims, provenance, quality, policy, retention and failure states shared by all adapters
  - Preserves source meaning rather than flattening unrelated objects into one record type

## Detailed source acquisition models

Detailed source models remain authoritative for provider-specific acquisition, coverage, query behavior, permissions, retention, attribution, cost and production gates.

- [Google API Source and Extraction Model](sources/google-api-source-model.md)
  - Normative planned Google Places public-discovery and Google Business Profile authorized-data architecture
  - Defines geographic coverage, Text Search, Nearby Search, Place Details, reviews, photos, posts, performance metrics, website handoff, scoring boundaries, cost, security, retention, attribution, and compliance gates
  - Explicitly prohibits Google Maps website scraping and prevents non-detection from becoming confirmed absence

- [Yandex Maps API Source and Extraction Model](sources/yandex-maps-api-source-model.md)
  - Normative planned Yandex Places public-discovery and customer-authorized Yandex Business export architecture
  - Defines strict geographic search, pagination, saturation, documented-field extraction, independent verification, scoring boundaries, cost, security, temporary caching, attribution, deletion, and contract gates
  - Marks the current connector restricted for production persistence until the intended Harvester workflow is covered by approved Yandex terms

- [LinkedIn Authorized Data Source Model](sources/linkedin-authorized-data-source-model.md)
  - Normative planned architecture for authorized organization connections, member consent, approved Sales Navigator partnerships, customer-authorized imports, and bounded operator references
  - Defines LinkedIn identity, organization activity, analytics, role evidence, scoring boundaries, consent, privacy, retention, deletion, API approval, and source-transition controls
  - Records the current stealth crawler separately as a quarantined legacy component with a feature freeze, production block, data-remediation plan, and removal path rather than treating it as an approved interim source

Previous versions remain available through Git history and pull-request history rather than duplicate archive documents inside the active repository.

## Locked product boundaries

```text
Harvester
Owns provider and service definition, market definition, source intake,
observations, evidence, local resolution, lead profiles, qualification,
opportunity intelligence, research, dossiers, selection, exports,
publishing rules, and operations.

Communicator
Optionally receives approved lead and context packages.
Owns communication profiles, audiences, campaigns, messages,
conversations, consent, engagement, replies, and follow-up.

NEWAX Core
Optionally receives source-native observations, resolved entities,
and approved Harvester-owned lead facets.
Owns enterprise existence, canonical identity, relationships,
provenance, field governance, and cross-system identity links.
```

No product shares private database tables, database-owner credentials, migrations, internal schemas, or runtime availability.

## Change-control rule

- Product delivery changes belong in `ROADMAP.md`.
- Operating-model and decision-invariant changes belong in the intelligence operating model.
- Provider types, service offerings, customer markets, lead-subject types, opportunity signals, qualification boundaries, first-page configuration, and universal generation rules belong in `SERVICES.md`.
- Broad-sector registry, sector-to-domain applicability, and first-stage market-selection changes belong in `taxonomy/broad-sector-registry.md`, subordinate to `SERVICES.md`.
- Sector-specific domain definitions, family assignments, first-release visibility, and cross-sector mappings belong in the registries listed by `taxonomy/README.md`.
- Canonical activity definitions, applicability profiles, and domain-to-activity assignments belong under `taxonomy/activity-registry.md` and its linked mapping files.
- Domain and activity discovery terms, organization cues, exclusions, negative context, match modes, and locale-specific keyword packs belong under `taxonomy/keywords/`.
- Service-specific target terms, problem signals, buying-intent signals, competitor terms, existing-solution terms, and service-gap profiles require an active provider offering and remain subordinate to `SERVICES.md`.
- Target-workspace activity and keyword overrides must remain explicit, versioned selections and must not silently mutate canonical registries.
- Provider-specific opportunity weights, rubrics, confidence, risk, and recommendations belong in an explicitly scoped scoring profile.
- The NEWAX Opportunity Scoring Model applies only to selected NEWAX business-infrastructure offerings and must not be treated as the universal Harvester score.
- User-input storage, approval, versioning, source selections, credential references and immutable job snapshots belong in `sources/user-input-storage-model.md`.
- Shared request, response, observation, claim, provenance, quality, retention and failure envelopes belong in `sources/canonical-source-record-format.md`.
- Source query, extraction, field-mask, coverage, retention, attribution, failure, cost, field mapping and source-specific compliance changes belong in the relevant source model or source-format document.
- Every new source requires a separate approved source-format document before production activation.
- Source-specific models cannot override product boundaries, service eligibility, evidence invariants, scoring separation, security requirements, or current provider terms.
- Integration-boundary changes belong in the integration framework or the relevant adapter document.
- Superseded versions remain in Git history rather than duplicate active documentation.
- Do not create parallel roadmaps, duplicate module counts, hidden product dependencies, competing universal opportunity definitions, or undocumented source behavior.