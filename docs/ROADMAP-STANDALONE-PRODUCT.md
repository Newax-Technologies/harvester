# Harvester Standalone Product Transition Crosswalk

## Status

Status: **Integrated into the authoritative 64-module roadmap**

The standalone-product workstreams HSP-0 through HSP-11 are no longer an additional layer of product modules.

Their requirements are now incorporated directly into:

- [`docs/ROADMAP.md`](ROADMAP.md)

The previous standalone roadmap remains available in Git history and the pull-request diff.

Harvester therefore has one authoritative count:

> **64 top-level standalone product modules**

Humans have created enough parallel roadmaps already. This document exists only to preserve traceability from the earlier HSP labels to the new module identities.

## Crosswalk

| Earlier workstream | Integrated modules | Result |
| --- | --- | --- |
| HSP-0 Architecture and product boundary | 01–08 | Standalone application, tenancy, authentication, permissions, ownership, configuration and audit |
| HSP-1 Connections and credentials | 09–10 | Credential vault and connection profiles |
| HSP-2 Database adapter kernel | 11, 23 | Connector framework and database source adapters |
| HSP-3 Source schemas and mappings | 12–14 | Schema registry, mappings, preview, validation and quarantine |
| HSP-4 Harvester normalization boundary | 29–40 | Raw observations, evidence, resolution, Master Leads and lead intelligence |
| HSP-5 Synchronization engine | 15–16, 56 | Checkpoints, retries, conflict handling, reconciliation and durable event exchange |
| HSP-6 Publishing rules and output profiles | 49–52 | Filters, groups, exports, publishing rules, frozen audiences and payloads |
| HSP-7 Direct Communicator integration | 53 | Optional direct adapter without Core |
| HSP-8 Optional NEWAX Core adapter | 54 | Optional source-native publication and identity-link reconciliation |
| HSP-9 Administration UI | 58 | Connections, secrets, schemas, mappings, sync, publication and adapter administration |
| HSP-10 Multi-tenant resale | 03, 59–61 | Tenant isolation, product administration, licensing and controlled branding |
| HSP-11 Packaging and rollout | 62–64 | Deployment, backup, restore, upgrades, security and release governance |

## Decisions preserved

1. Harvester operates without NEWAX Core or Communicator.
2. Harvester owns its database, identifiers, mapping and lead-intelligence format.
3. Every source and destination uses a versioned credentialed adapter.
4. Direct Harvester-to-Communicator integration works without Core.
5. Core remains an optional identity and governance destination.
6. Publishing is controlled by filters, rules, frozen audiences, payload profiles and approvals.
7. Multi-tenant resale, licensing, packaging, backup, restore and upgrades are first-class product requirements.
8. No HSP workstream is counted as an extra top-level module.

## Change-control rule

Future roadmap changes must modify the relevant numbered module in `docs/ROADMAP.md`.

Do not create another parallel top-level module count unless the existing 64-module architecture is formally re-baselined with an archived predecessor, explicit migration map and verified reason.
