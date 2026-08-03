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
   - Universal provider, service-offering, customer-market, lead-subject, opportunity-signal, qualification, and first-page generation model
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

## Source-specific models

Source-specific models define how one external source is planned, queried, extracted, governed, retained, and connected to Harvester evidence. They remain subordinate to the roadmap, operating model, services model, applicable scoring profile, and integration framework.

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
- Healthcare domain definitions, family assignments, first-release visibility, cross-sector mappings, and Healthcare domain-to-activity applicability belong in `taxonomy/healthcare-domain-registry.md`, subordinate to the broad-sector registry and `SERVICES.md`.
- Provider-specific opportunity weights, rubrics, confidence, risk, and recommendations belong in an explicitly scoped scoring profile.
- The NEWAX Opportunity Scoring Model applies only to selected NEWAX business-infrastructure offerings and must not be treated as the universal Harvester score.
- Source query, extraction, field-mask, coverage, retention, attribution, failure, cost, and source-specific compliance changes belong in the relevant source model.
- Source-specific models cannot override product boundaries, service eligibility, evidence invariants, scoring separation, security requirements, or current provider terms.
- Integration-boundary changes belong in the integration framework or the relevant adapter document.
- Superseded versions remain in Git history rather than duplicate active documentation.
- Do not create parallel roadmaps, duplicate module counts, hidden product dependencies, competing universal opportunity definitions, or undocumented source behavior.
