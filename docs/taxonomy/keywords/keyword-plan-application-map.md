# Harvester Keyword Plan Application Map

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document applies the [Harvester Keyword Profile Development Plan](keyword-profile-development-plan.md) to the existing keyword Markdown registries without replacing, rewriting, collapsing, or reclassifying their current content.

It is the authoritative documentation sequence for the keyword layer. Exact sector-to-domain-registry, activity-applicability and domain-keyword links are maintained in the [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md).

The existing keyword files remain controlled datasets. This map defines how they are composed, tested, executed, evidenced, qualified, reviewed, versioned, and integrated into lead generation.

## 1. Documentation and implementation sequence

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

Primary reading order:

1. [`../../ROADMAP.md`](../../ROADMAP.md)
2. [`../../architecture/agency-intelligence-rebaseline.md`](../../architecture/agency-intelligence-rebaseline.md)
3. [`../../architecture/harvester-intelligence-operating-model.md`](../../architecture/harvester-intelligence-operating-model.md)
4. [`../../SERVICES.md`](../../SERVICES.md)
5. [`../../architecture/provider-portfolio-and-lead-generation-profile-model.md`](../../architecture/provider-portfolio-and-lead-generation-profile-model.md)
6. [`../broad-sector-registry.md`](../broad-sector-registry.md)
7. The selected sector domain registry
8. [`../activity-registry.md`](../activity-registry.md) and the selected domain-activity mapping
9. The selected sector domain keyword registry
10. [`activity-keywords-part-1.md`](activity-keywords-part-1.md), [`activity-keywords-part-2.md`](activity-keywords-part-2.md), and [`activity-keywords-part-3.md`](activity-keywords-part-3.md)
11. [`control-profiles.md`](control-profiles.md)
12. [`provider-offering-keyword-profile-standard.md`](provider-offering-keyword-profile-standard.md)
13. [`lead-generation-signal-registry.md`](lead-generation-signal-registry.md) and [`sector-lead-generation-overlays.md`](sector-lead-generation-overlays.md)
14. [`source-signal-matrix.md`](source-signal-matrix.md) and the applicable source model
15. [`source-query-template-library.md`](source-query-template-library.md), [`query-composition-and-evidence-rules.md`](query-composition-and-evidence-rules.md), and [`keyword-expansion-and-composition-engine.md`](keyword-expansion-and-composition-engine.md)
16. [`semantic-entity-and-classification-expansion.md`](semantic-entity-and-classification-expansion.md)
17. [`../../architecture/keyword-evidence-profile-integration-addendum.md`](../../architecture/keyword-evidence-profile-integration-addendum.md)
18. [`keyword-quality-and-review-standard.md`](keyword-quality-and-review-standard.md), [`benchmark-and-gold-set-standard.md`](benchmark-and-gold-set-standard.md), and [`keyword-validation-plan.md`](keyword-validation-plan.md)
19. [`keyword-profile-implementation-plan.md`](keyword-profile-implementation-plan.md) and [`../../delivery/keyword-profile-delivery-addendum.md`](../../delivery/keyword-profile-delivery-addendum.md)

A later file may deepen an earlier rule. It cannot silently override provider eligibility, domain identity, activity applicability, evidence invariants, source restrictions, contact policy, tenant isolation, or the authoritative roadmap.

## 2. Additive rule

```text
Existing keyword registry
+ Keyword Profile Development Plan
+ this application map
+ Sector Keyword Connection Matrix
= controlled implementation specification
```

This map does not supersede canonical domain or activity codes, identity terms, activity terms, organization cues, exclusions, evidence controls, signals, source suitability, query rules, decision-maker cues, contact safeguards, or product boundaries.

Conflicts require explicit change control. Existing registry content is never silently replaced by generated plan language.

## 3. Canonical activity keyword registries

Shared activity-term authorities:

- [Activity keywords, part 1](activity-keywords-part-1.md)
- [Activity keywords, part 2](activity-keywords-part-2.md)
- [Activity keywords, part 3](activity-keywords-part-3.md)

Rules:

1. Preserve one canonical keyword identity per activity code.
2. Compose activity terms only after that activity is approved for the selected domain.
3. Do not propagate activity selection between domains.
4. Preserve match mode, language, term type, status, and profile version.
5. Benchmark activity terms separately from domain identity terms.
6. Treat activity matches as evidence candidates, not proof.

## 4. Sector-specific domain keyword registries

The [Sector Keyword Connection Matrix](01-sector-keyword-connection-matrix.md) provides exact upstream domain and activity authorities for all 16 sectors.

Sector application rules:

- **Healthcare:** keep medicines, devices, supplies, care services, facilities, digital health, operations, research, education, and public health separate; apply sensitive-health restrictions.
- **Education:** separate institutions, learning services, content, technology, assessment, research, and operations; never treat student records or individual courses as organizations.
- **Food and Agriculture:** separate crops, livestock, fisheries, inputs, processing, products, cold chain, distribution, and services; preserve halal, food-safety, seasonal, and commodity controls.
- **Real Estate:** separate development, brokerage, property management, facilities, valuation, leasing, investment, and property technology; distinguish listings from organizations.
- **Construction:** separate contractors, engineering, architecture, materials, systems, equipment, installation, inspection, and project services; keep physical and digital systems distinct.
- **Legal:** separate practice areas, institutions, operations, compliance, dispute resolution, and technology; distinguish firms from cases, legislation, courts, articles, and individual professionals.
- **Finance:** separate banking, payments, investment, Islamic finance, Takaful, accounting, audit, tax, risk, compliance, and technology; enforce ambiguity and ethical controls.
- **Retail:** separate product categories, store formats, e-commerce, marketplaces, franchising, operations, and systems; distinguish retailers from product listings and consumer posts.
- **Hospitality:** separate accommodation, food service, venues, events, guest services, property operations, and systems; distinguish operators from booking listings and reviews.
- **Travel:** separate agencies, tour operations, destination services, pilgrimage, ticketing, transport-linked travel, and systems; preserve geography and seasonality.
- **Manufacturing and Industry:** separate manufacturing families, fabrication, assembly, processing, equipment, industrial services, quality, and systems; distinguish manufacturers from suppliers and repairers.
- **Logistics:** separate freight, courier, delivery, warehousing, fulfilment, cold chain, fleets, ports, aviation, maritime, and systems.
- **Energy:** separate generation, transmission, distribution, renewables, fuels, utilities, water, efficiency, equipment, and systems; distinguish physical infrastructure from software and services.
- **Technology:** separate software products, SaaS, IT services, infrastructure, cloud, data, cybersecurity, telecommunications, hardware, and operations; broad technology words require context.
- **Government:** separate administration, municipal services, regulators, public safety, emergency services, infrastructure, citizen services, and systems; distinguish institutions from policy discussion and office-holders.
- **Nonprofit:** separate charities, foundations, NGOs, associations, chambers, religious institutions, development organizations, membership bodies, and systems; distinguish organizations from campaigns and donation pages.

## 5. Shared governance files

- [Keyword Control Profiles](control-profiles.md)
- [Keyword Quality and Review Standard](keyword-quality-and-review-standard.md)
- [Lead-Generation Signal Registry](lead-generation-signal-registry.md)
- [Sector Lead-Generation Overlays](sector-lead-generation-overlays.md)
- [Decision-Maker and Contact-Cue Registry](decision-maker-and-contact-cues.md)
- [Source-to-Signal Matrix](source-signal-matrix.md)
- [Query Composition and Evidence Rules](query-composition-and-evidence-rules.md)
- [Cross-Product Keyword and Profile Contract](cross-product-keyword-contract.md)

These files own reusable ambiguity, source, evidence, signal, role, contact, query, quality, lifecycle, and cross-product rules. Sector registries cannot override them.

## 6. Required composition sequence

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

No step is skipped merely because a keyword appears persuasive.

## 7. Required version connection

Every activated profile and Harvest Job preserves versions for provider, business unit, offering, lead-generation profile, broad sector, domain, sector-domain mapping, domain-activity assignment, activity, domain and activity keyword profiles, organization cues, exclusions, offering signals, sector overlay, source suitability, source model, locale pack, query templates, query composition, semantic and classification models, evidence policy, qualification, scoring, and contact policy.

Later changes apply only to future jobs unless an operator explicitly creates a replacement job.

## 8. Preservation rule

This map is additive. It does not authorize replacing controlled Markdown registries with summaries, generated prose, spreadsheets, databases, embeddings, or runtime configuration without stable codes, versions, traceability, review, and migration evidence.

## 9. Acceptance criteria

The keyword connection is acceptable only when:

1. every sector resolves through the sector connection matrix;
2. every domain and activity retains stable identity and a separate profile;
3. activity applicability remains domain-specific;
4. offering-specific signals require an active offering;
5. queries preserve all contributing profile and source versions;
6. matches preserve source, context, time, match mode, language, and profile origin;
7. keyword matches cannot independently create gaps, opportunities, authority, consent, or contact-ready leads;
8. positive evidence is evaluated with exclusions, contradictions, freshness, coverage, and duplicate-origin controls;
9. role and contact discovery follows entity resolution and supported-opportunity gates;
10. jobs remain reproducible from immutable snapshots;
11. the Harvester roadmap remains the only top-level delivery roadmap.

## 10. Delivery boundary

The development plan, this map, the connection matrix, and linked registries are controlled documentation datasets. They do not implement database records, migrations, APIs, interfaces, search execution, embeddings, classifiers, evidence scoring, opportunity scoring, contact eligibility, outreach, or releases.
