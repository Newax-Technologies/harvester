# Harvester Domain–Activity Registry Index

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This registry completes the controlled business-activity taxonomy for all **1,586 canonical domains** across all 16 broad sectors.

The dataset contains:

- **519 canonical activities** with stable activity codes.
- **1,586 explicit domain-to-activity-profile assignments**.
- Applicability levels of `CORE`, `COMMON`, `OPTIONAL`, and implicit `NOT_APPLICABLE` when an activity is absent from a profile.
- Independent user approval for every selected domain–activity combination.

A shared activity identity does not create a shared selection. Selecting `Manufacturing` for Pharmaceuticals does not activate it for Medical Devices, Food Products, Textiles, or any other domain.

## Activity definitions

- [Canonical activities, part 1](activity-registry-part-1.md)
  - Research, production, sourcing, quality, logistics, and commerce activities.
- [Canonical activities, part 2](activity-registry-part-2.md)
  - Marketing, operations, digital, professional, healthcare, and education activities.
- [Canonical activities, part 3](activity-registry-part-3.md)
  - Finance, legal, public, hospitality, property, and end-of-life activities.

## Sector-specific applicability mappings

| Sector | Canonical domains | Applicability profiles and assignments |
| --- | ---: | --- |
| `BS-001 Healthcare` | 142 | [Profiles](activity-profiles-part-1.md#bs-001-healthcare) and [domain assignments](domain-assignments-part-1.md#bs-001-healthcare) |
| `BS-002 Education` | 95 | [Profiles](activity-profiles-part-1.md#bs-002-education) and [domain assignments](domain-assignments-part-1.md#bs-002-education) |
| `BS-003 Food and Agriculture` | 103 | [Profiles](activity-profiles-part-2.md#bs-003-food-and-agriculture) and [domain assignments](domain-assignments-part-2.md#bs-003-food-and-agriculture) |
| `BS-004 Real Estate` | 88 | [Profiles](activity-profiles-part-2.md#bs-004-real-estate) and [domain assignments](domain-assignments-part-2.md#bs-004-real-estate) |
| `BS-005 Construction` | 93 | [Profiles](activity-profiles-part-3.md#bs-005-construction) and [domain assignments](construction-domain-activity-assignments.md) |
| `BS-006 Legal` | 97 | [Profiles](activity-profiles-part-3.md#bs-006-legal) and [domain assignments](legal-domain-activity-assignments.md) |
| `BS-007 Finance` | 109 | [Complete Finance mapping](domain-activity-mappings/finance-domain-activity-mapping.md) |
| `BS-008 Retail` | 84 | [Complete Retail mapping](domain-activity-mappings/retail-domain-activity-mapping.md) |
| `BS-009 Hospitality` | 79 | [Complete Hospitality mapping](domain-activity-mappings/hospitality-domain-activity-mapping.md) |
| `BS-010 Travel` | 75 | [Complete Travel mapping](domain-activity-mappings/travel-domain-activity-mapping.md) |
| `BS-011 Manufacturing and Industry` | 111 | [Complete Manufacturing and Industry mapping](domain-activity-mappings/manufacturing-industry-domain-activity-mapping.md) |
| `BS-012 Logistics` | 101 | [Complete Logistics mapping](domain-activity-mappings/logistics-domain-activity-mapping.md) |
| `BS-013 Energy` | 94 | [Complete Energy mapping](domain-activity-mappings/energy-domain-activity-mapping.md) |
| `BS-014 Technology` | 127 | [Complete Technology mapping](domain-activity-mappings/technology-domain-activity-mapping.md) |
| `BS-015 Government` | 96 | [Complete Government mapping](domain-activity-mappings/government-domain-activity-mapping.md) |
| `BS-016 Nonprofit` | 92 | [Complete Nonprofit mapping](domain-activity-mappings/nonprofit-domain-activity-mapping.md) |
| **Total** | **1,586** | **All canonical domains explicitly mapped** |

## Locked rules

1. Activities are shared canonical identities.
2. Every domain is explicitly assigned to a default applicability profile.
3. Selecting an activity for one domain never activates it for another domain.
4. `CORE`, `COMMON`, and `OPTIONAL` are interface defaults, not evidence that a target performs an activity.
5. Activities absent from a profile are `NOT_APPLICABLE` by default.
6. A user may override recommended applicability only through an explicit, versioned target configuration.
7. Users approve each domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, export, publication, or lead generation.
8. Keywords may help discover activity evidence but cannot independently prove an activity.
9. Overlapping domains and sectors do not duplicate organizations, evidence, opportunities, or scores.
10. Completed harvest jobs retain the sector, domain, activity, profile, offering, evidence, and scoring versions used when they ran.

## Minimum data model

| Entity | Minimum fields |
| --- | --- |
| `ActivityDefinition` | `id`; `code`; `name`; `family`; `description`; `aliases`; `status`; `version` |
| `DomainActivityProfile` | `id`; `code`; `sector_id`; `core_activity_ids`; `common_activity_ids`; `optional_activity_ids`; `status`; `version` |
| `DomainActivityAssignment` | `domain_id`; `profile_id`; `status`; `version`; `rationale`; `reviewed_at` |
| `TargetDomainActivity` | `target_domain_selection_id`; `activity_id`; `status`; `priority`; `qualification_rules`; `exclusion_rules` |

## Delivery boundary

The canonical activity registry and all 1,586 domain mappings are **defined and repository-integrated documentation datasets**.

They do not implement database records, migrations, APIs, interface controls, activity detection, evidence scoring, provider-service matching, or releases. Runtime implementation remains separate engineering work requiring schema, migration, API, interface, test, security, and release verification.
