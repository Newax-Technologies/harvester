# Harvester Delivery Plans

This directory contains implementation-sequencing and release-verification plans that remain subordinate to the authoritative product roadmap, operating model, services model, taxonomy and source models.

## Frontend

- [Frontend Configuration and Responsive UI Delivery Plan](frontend-configuration-and-responsive-ui-delivery-plan.md)
  - Defines the complete A-to-Z configuration journey.
  - Completes frontend coverage for existing backend operational domains.
  - Defines the shared frontend architecture, responsive correction, accessibility, testing, security and rollout requirements.
  - Provides a 30-PR dependency-ordered implementation sequence.

- [Input-Page Output Selection Specification](input-page-output-selection-specification.md)
  - Defines what an authorized operator may ask Harvester to produce from a configured market.
  - Covers result purpose, quantity, eligibility thresholds, field selection, evidence depth, ranking, deduplication, destinations, formats, scheduling, retention, preview, review and activation.
  - Keeps result generation separate from export, publication and outreach.
  - Prohibits silent threshold reduction merely to fill a requested result quota.

## Keyword runtime

- [Keyword Profile Runtime Delivery Plan](keyword-profile-runtime-delivery-plan.md)
  - Defines the runtime schema, APIs, lifecycle, frontend workspaces, validation, query preview, evidence, quality and rollout plan for keyword profiles.

- [Keyword Profile Delivery Addendum](keyword-profile-delivery-addendum.md)
  - Integrates keyword-profile delivery requirements with the wider Harvester architecture and roadmap.

## Status boundary

Delivery plans are planning and sequencing artifacts. They do not independently prove that schema, APIs, frontend routes, tests, migrations, deployment or runtime behavior have been implemented.
