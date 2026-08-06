# Harvester Delivery Plans

Status: **Authoritative delivery index**  
Version: **2.1**  
Date: **6 August 2026**

Delivery plans translate the 64-module roadmap and normative architecture into implementation slices. They remain subordinate to `docs/ROADMAP.md` and the authority order in `docs/README.md`.

## 1. Primary implementation sequence

- [Agency Intelligence Implementation Sequence](agency-intelligence-implementation-sequence.md)
  - The dependency-ordered delivery authority for the Agency Intelligence re-baseline.
  - Starts with known data-integrity and restricted-source corrections.
  - Continues through tenancy, security, source governance, provider and market configuration, Harvest Job orchestration, universal evidence and identity, sector packs, Opportunity Scoring Model v3, AI governance, agency intelligence, activation, and productization.
  - Maps every slice back to the existing 64 modules instead of inventing another module count.

## 2. Frontend delivery

- [Frontend Configuration and Responsive UI Delivery Plan](frontend-configuration-and-responsive-ui-delivery-plan.md)
  - Defines the complete configuration journey and full frontend coverage for current and planned operational domains.
  - Defines shared frontend architecture, responsive correction, accessibility, testing, security, and rollout requirements.
  - Its pull-request sequence must now follow the foundation, tenancy, source-governance, provider, market-definition, sector-pack, and universal-entity contracts established by the primary implementation sequence.

- [Input-Page Output Selection Specification](input-page-output-selection-specification.md)
  - Defines what an authorized operator may ask Harvester to produce from a configured provider and market.
  - Covers result purpose, quantity, eligibility, fields, evidence depth, ranking, deduplication, destinations, formats, scheduling, retention, preview, review, activation, and history.
  - Keeps result generation separate from export, publication, and outreach.
  - Prohibits silent quality-threshold reduction merely to fill a requested quota.

## 3. Keyword and taxonomy runtime

- [Keyword Profile Runtime Delivery Plan](keyword-profile-runtime-delivery-plan.md)
  - Defines runtime schema, APIs, lifecycle, validation, query preview, evidence, quality, locale, and frontend workspaces for keyword profiles.
  - Keywords remain evidence-discovery inputs and cannot independently qualify or score a lead.

- [Keyword Profile Delivery Addendum](keyword-profile-delivery-addendum.md)
  - Connects keyword-profile delivery to the roadmap, evidence model, source suitability, sector packs, and release gates.

## 4. Delivery precedence

When plans overlap:

1. correct known data-integrity and restricted-source issues;
2. establish tenant, authentication, authorization, credential, and policy boundaries;
3. implement provider, offering, profile, and market contracts;
4. implement source orchestration and evidence contracts;
5. implement sector, intelligence, AI, frontend, and activation work against those stable boundaries.

A lower plan may add detail but must not schedule a dependent feature before its required foundation.

## 5. Status boundary

Delivery plans are planning and sequencing artifacts. They do not independently prove that schemas, migrations, APIs, routes, workers, interfaces, deployments, or runtime behavior exist.

A slice becomes **Current** only when:

- the intended code and migrations are integrated;
- applicable format, lint, type, test, build, security, migration, accessibility, performance, and workflow checks pass;
- the real workflow is verified at the exact latest commit;
- unresolved internal and external integration statuses are reported honestly;
- owning documentation status is updated.

## 6. Pull-request requirements

Every implementation PR states:

```text
Owning module or modules
Affected contracts
Migration impact
Tenant and workspace impact
Source-policy impact
Sector-pack impact
AI impact
Frontend impact
Destination impact
Compatibility and rollback
Checks executed
Exact head SHA
```

Stacked PRs declare and preserve their dependency order. Stale branches are rebased or reimplemented rather than merged by optimism.
