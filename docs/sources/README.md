# Harvester Source Input and Formatting Index

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented unless a linked source document explicitly states otherwise**

This directory defines how Harvester stores customer and operator inputs, separates approved configuration from operational activation, creates immutable Harvest Job input snapshots, receives provider-native records, converts them into a canonical source envelope, and applies source-specific formatting, retention, permission, and evidence rules.

The source layer follows this sequence:

```text
Tenant and workspace
→ provider organization and optional business unit
→ offering portfolio
→ reusable lead-generation profile version
→ explicit activation or schedule
→ approved market, taxonomy, keyword, source and policy selections
→ immutable Harvest Job input snapshot
→ source request and response outcome
→ source-native observation
→ canonical source envelope
→ normalized evidence claims
→ entity resolution and profile-specific opportunity assessment
```

A company may maintain many providers, offerings, and lead-generation profiles without activating all of them.

An inactive, paused, suspended, expired, completed, cancelled, or archived profile creates no production source plan, job, score, lead, export, publication, or cost.

A source adapter may create observations and evidence. It may not independently create a service gap, qualified opportunity, outreach authorization, profile activation, or canonical identity.

## Core input and formatting models

- [User Input Storage Model](user-input-storage-model.md)
  - Defines tenant-isolated workspaces, providers, business units, offering portfolios, reusable profile versions, offering selections, activation, source selections, credential references, query profiles, overrides, and immutable job snapshots.
  - Separates configuration approval from operational activation.
  - Preserves independent profile lifecycle, budgets, schedules, overlap controls, and job reproducibility.
- [Provider Portfolio and Lead-Generation Profile Model](../architecture/provider-portfolio-and-lead-generation-profile-model.md)
  - Defines the scalable provider, offering, profile, activation, first-page, scheduling, overlap, capacity, permissions, analytics, and roadmap-integration model.
- [Canonical Source Record Format](canonical-source-record-format.md)
  - Defines the shared request, response, observation, artifact, claim, outcome, provenance, quality, retention, and policy envelope used by every adapter.
- [Source Adapter Documentation Template](source-adapter-template.md)
  - Defines the mandatory structure for adding a new source family.

## Named platform source formats

- [Google Source Format](google-source-format.md)
- [Yandex Source Format](yandex-source-format.md)
- [LinkedIn Source Format](linkedin-source-format.md)
- [Meta and Instagram Source Format](meta-source-format.md)
- [X Source Format](x-source-format.md)
- [Bing Source Format](bing-source-format.md)
- [Indeed Source Format](indeed-source-format.md)
- [Crunchbase Source Format](crunchbase-source-format.md)
- [Apple Maps Source Format](apple-maps-source-format.md)
- [Telegram Source Format](telegram-source-format.md)

## Other approved source families

- [Organization Website Source Format](organization-website-source-format.md)
- [Government and Official Registry Source Format](government-registry-source-format.md)
- [Business and Industry Directory Source Format](business-directory-source-format.md)
- [General Job Board Source Format](job-board-source-format.md)
- [Procurement and Tender Source Format](procurement-tender-source-format.md)
- [News and Media Source Format](news-media-source-format.md)
- [Application and Marketplace Source Format](app-marketplace-source-format.md)
- [Manual and Authorized Import Source Format](manual-authorized-import-source-format.md)
- [Generic API, Feed and Licensed Dataset Source Format](generic-api-feed-source-format.md)

## Existing detailed acquisition authorities

The following documents remain authoritative for their provider-specific acquisition, compliance, coverage, and retention rules:

- [Google API Source and Extraction Model](google-api-source-model.md)
- [Yandex Maps API Source and Extraction Model](yandex-maps-api-source-model.md)
- [LinkedIn Authorized Data Source Model](linkedin-authorized-data-source-model.md)

The corresponding source-format documents define how records enter the canonical Harvester envelope. They do not replace those detailed models.

## Locked rules

1. User inputs are stored as tenant-isolated, versioned configuration objects.
2. Provider identity, business unit, offering portfolio, lead-generation profile, profile version, and operational activation remain separate.
3. A profile selects a subset of approved and available provider offerings.
4. Approval does not automatically activate a profile.
5. Connection does not automatically authorize a source or destination for every profile.
6. Credentials are stored only as secret references, never as plaintext configuration values.
7. Every Harvest Job freezes the exact provider, business unit, profile, activation, source-plan, taxonomy, keyword, offering, signal, qualification, evidence, output, scoring and policy versions used for that run.
8. Provider-native identifiers remain provider references until entity resolution links them to Harvester entities.
9. Missing source fields mean `NOT_DETECTED`, not confirmed absence.
10. Source failures, zero results, partial results, permission failures, and policy blocks remain distinct outcomes.
11. Raw-payload retention is source-specific and may be shorter than Harvester's general evidence retention.
12. Source-native data and independently verified facts remain distinct.
13. A keyword match or source record cannot independently prove an activity, service gap, buying intent, or opportunity.
14. Overlapping profiles reuse eligible evidence without duplicating master entities, while qualification and opportunity assessments remain profile-specific.
15. A new source may not be activated until it has an approved source-format document, permission basis, retention policy, failure taxonomy, field mapping, and verification plan.

## Delivery boundary

These documents define repository-integrated architecture and data contracts. They do not implement database tables, migrations, API routes, provider portfolios, profile activation, connectors, credentials, schedulers, source calls, user interfaces, evidence extraction, scoring, or releases.
