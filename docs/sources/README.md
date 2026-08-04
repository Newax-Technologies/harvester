# Harvester Source Input and Formatting Index

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented unless a linked source document explicitly states otherwise**

This directory defines how Harvester stores customer and operator inputs, creates immutable Harvest Job input snapshots, receives provider-native records, converts them into a canonical source envelope, and applies source-specific formatting, retention, permission, and evidence rules.

The source layer follows this sequence:

```text
User and workspace inputs
→ approved versioned market definition
→ source selection and source-specific configuration
→ immutable Harvest Job input snapshot
→ source request and response outcome
→ source-native observation
→ canonical source envelope
→ normalized evidence claims
→ entity resolution and opportunity assessment
```

A source adapter may create observations and evidence. It may not independently create a service gap, qualified opportunity, outreach authorization, or canonical identity.

## Core input and formatting models

- [User Input Storage Model](user-input-storage-model.md)
  - Defines tenant-isolated drafts, approvals, versions, source selections, credential references, query profiles, overrides, and immutable job snapshots.
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
2. Credentials are stored only as secret references, never as plaintext configuration values.
3. Every Harvest Job freezes the exact approved input, source-plan, taxonomy, keyword, offering, and policy versions used for that run.
4. Provider-native identifiers remain provider references until entity resolution links them to Harvester entities.
5. Missing source fields mean `NOT_DETECTED`, not confirmed absence.
6. Source failures, zero results, partial results, permission failures, and policy blocks remain distinct outcomes.
7. Raw-payload retention is source-specific and may be shorter than Harvester's general evidence retention.
8. Source-native data and independently verified facts remain distinct.
9. A keyword match or source record cannot independently prove an activity, service gap, buying intent, or opportunity.
10. A new source may not be activated until it has an approved source-format document, permission basis, retention policy, failure taxonomy, field mapping, and verification plan.

## Delivery boundary

These documents define repository-integrated architecture and data contracts. They do not implement database tables, migrations, API routes, connectors, credentials, schedulers, source calls, user interfaces, evidence extraction, scoring, or releases.