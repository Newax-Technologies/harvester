# Harvester Sector Keyword Connection Matrix

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Documentation integrated; runtime not implemented**

This matrix connects every broad sector to its canonical domain registry, domain-to-activity applicability source, domain keyword registry, shared activity keyword registry, and downstream offering, query, evidence and validation controls.

Use this file after reading the [Keyword Plan Application Map](keyword-plan-application-map.md).

---

## 1. Shared files used by every sector

Every sector uses these shared authorities:

| Layer | File |
| --- | --- |
| Broad-sector selection | [`../broad-sector-registry.md`](../broad-sector-registry.md) |
| Canonical activity identities and mapping index | [`../activity-registry.md`](../activity-registry.md) |
| Activity keyword profiles, part 1 | [`activity-keywords-part-1.md`](activity-keywords-part-1.md) |
| Activity keyword profiles, part 2 | [`activity-keywords-part-2.md`](activity-keywords-part-2.md) |
| Activity keyword profiles, part 3 | [`activity-keywords-part-3.md`](activity-keywords-part-3.md) |
| Organization and exclusion controls | [`control-profiles.md`](control-profiles.md) |
| Offering-specific keyword standard | [`provider-offering-keyword-profile-standard.md`](provider-offering-keyword-profile-standard.md) |
| Reusable lead signals | [`lead-generation-signal-registry.md`](lead-generation-signal-registry.md) |
| Sector lead-signal overlays | [`sector-lead-generation-overlays.md`](sector-lead-generation-overlays.md) |
| Decision-maker and contact cues | [`decision-maker-and-contact-cues.md`](decision-maker-and-contact-cues.md) |
| Source suitability | [`source-signal-matrix.md`](source-signal-matrix.md) |
| Source query templates | [`source-query-template-library.md`](source-query-template-library.md) |
| Query composition and evidence rules | [`query-composition-and-evidence-rules.md`](query-composition-and-evidence-rules.md) |
| Expansion and composition engine | [`keyword-expansion-and-composition-engine.md`](keyword-expansion-and-composition-engine.md) |
| Semantic, entity and classification expansion | [`semantic-entity-and-classification-expansion.md`](semantic-entity-and-classification-expansion.md) |
| Evidence integration | [`../../architecture/keyword-evidence-profile-integration-addendum.md`](../../architecture/keyword-evidence-profile-integration-addendum.md) |
| Benchmark and gold sets | [`benchmark-and-gold-set-standard.md`](benchmark-and-gold-set-standard.md) |
| Validation execution | [`keyword-validation-plan.md`](keyword-validation-plan.md) |
| Runtime implementation | [`keyword-profile-implementation-plan.md`](keyword-profile-implementation-plan.md) |
| Delivery gates | [`../../delivery/keyword-profile-delivery-addendum.md`](../../delivery/keyword-profile-delivery-addendum.md) |

The sector files below add domain-specific identity terms. They do not redefine shared activities, offering signals, source policy, evidence rules or contact policy.

---

## 2. Ordered sector connections

| Sequence | Sector | Domain registry | Activity applicability | Domain keyword registry | Domains |
| ---: | --- | --- | --- | --- | ---: |
| 1 | `BS-001 Healthcare` | [`../healthcare-domain-registry.md`](../healthcare-domain-registry.md) | [`../activity-profiles-part-1.md#bs-001-healthcare`](../activity-profiles-part-1.md#bs-001-healthcare) and [`../domain-assignments-part-1.md#bs-001-healthcare`](../domain-assignments-part-1.md#bs-001-healthcare) | [`healthcare-domain-keywords-part-1.md`](healthcare-domain-keywords-part-1.md) and [`healthcare-domain-keywords-part-2.md`](healthcare-domain-keywords-part-2.md) | 142 |
| 2 | `BS-002 Education` | [`../education-domain-registry.md`](../education-domain-registry.md) | [`../activity-profiles-part-1.md#bs-002-education`](../activity-profiles-part-1.md#bs-002-education) and [`../domain-assignments-part-1.md#bs-002-education`](../domain-assignments-part-1.md#bs-002-education) | [`education-domain-keywords.md`](education-domain-keywords.md) | 95 |
| 3 | `BS-003 Food and Agriculture` | [`../food-agriculture-domain-registry.md`](../food-agriculture-domain-registry.md) | [`../activity-profiles-part-2.md#bs-003-food-and-agriculture`](../activity-profiles-part-2.md#bs-003-food-and-agriculture) and [`../domain-assignments-part-2.md#bs-003-food-and-agriculture`](../domain-assignments-part-2.md#bs-003-food-and-agriculture) | [`food-agriculture-domain-keywords.md`](food-agriculture-domain-keywords.md) | 103 |
| 4 | `BS-004 Real Estate` | [`../real-estate-domain-registry.md`](../real-estate-domain-registry.md) | [`../activity-profiles-part-2.md#bs-004-real-estate`](../activity-profiles-part-2.md#bs-004-real-estate) and [`../domain-assignments-part-2.md#bs-004-real-estate`](../domain-assignments-part-2.md#bs-004-real-estate) | [`real-estate-domain-keywords.md`](real-estate-domain-keywords.md) | 88 |
| 5 | `BS-005 Construction` | [`../construction-domain-registry.md`](../construction-domain-registry.md) | [`../activity-profiles-part-3.md#bs-005-construction`](../activity-profiles-part-3.md#bs-005-construction) and [`../construction-domain-activity-assignments.md`](../construction-domain-activity-assignments.md) | [`construction-domain-keywords.md`](construction-domain-keywords.md) | 93 |
| 6 | `BS-006 Legal` | [`../legal-domain-registry.md`](../legal-domain-registry.md) | [`../activity-profiles-part-3.md#bs-006-legal`](../activity-profiles-part-3.md#bs-006-legal) and [`../legal-domain-activity-assignments.md`](../legal-domain-activity-assignments.md) | [`legal-domain-keywords.md`](legal-domain-keywords.md) | 97 |
| 7 | `BS-007 Finance` | [`../finance-domain-registry.md`](../finance-domain-registry.md) | [`../domain-activity-mappings/finance-domain-activity-mapping.md`](../domain-activity-mappings/finance-domain-activity-mapping.md) | [`finance-domain-keywords.md`](finance-domain-keywords.md) | 109 |
| 8 | `BS-008 Retail` | [`../retail-domain-registry.md`](../retail-domain-registry.md) | [`../domain-activity-mappings/retail-domain-activity-mapping.md`](../domain-activity-mappings/retail-domain-activity-mapping.md) | [`retail-domain-keywords.md`](retail-domain-keywords.md) | 84 |
| 9 | `BS-009 Hospitality` | [`../hospitality-domain-registry.md`](../hospitality-domain-registry.md) | [`../domain-activity-mappings/hospitality-domain-activity-mapping.md`](../domain-activity-mappings/hospitality-domain-activity-mapping.md) | [`hospitality-domain-keywords.md`](hospitality-domain-keywords.md) | 79 |
| 10 | `BS-010 Travel` | [`../travel-domain-registry.md`](../travel-domain-registry.md) | [`../domain-activity-mappings/travel-domain-activity-mapping.md`](../domain-activity-mappings/travel-domain-activity-mapping.md) | [`travel-domain-keywords.md`](travel-domain-keywords.md) | 75 |
| 11 | `BS-011 Manufacturing and Industry` | [`../manufacturing-industry-domain-registry.md`](../manufacturing-industry-domain-registry.md) | [`../domain-activity-mappings/manufacturing-industry-domain-activity-mapping.md`](../domain-activity-mappings/manufacturing-industry-domain-activity-mapping.md) | [`manufacturing-industry-domain-keywords.md`](manufacturing-industry-domain-keywords.md) | 111 |
| 12 | `BS-012 Logistics` | [`../logistics-domain-registry.md`](../logistics-domain-registry.md) | [`../domain-activity-mappings/logistics-domain-activity-mapping.md`](../domain-activity-mappings/logistics-domain-activity-mapping.md) | [`logistics-domain-keywords.md`](logistics-domain-keywords.md) | 101 |
| 13 | `BS-013 Energy` | [`../energy-domain-registry.md`](../energy-domain-registry.md) | [`../domain-activity-mappings/energy-domain-activity-mapping.md`](../domain-activity-mappings/energy-domain-activity-mapping.md) | [`energy-domain-keywords.md`](energy-domain-keywords.md) | 94 |
| 14 | `BS-014 Technology` | [`../technology-domain-registry.md`](../technology-domain-registry.md) | [`../domain-activity-mappings/technology-domain-activity-mapping.md`](../domain-activity-mappings/technology-domain-activity-mapping.md) | [`technology-domain-keywords-part-1.md`](technology-domain-keywords-part-1.md) and [`technology-domain-keywords-part-2.md`](technology-domain-keywords-part-2.md) | 127 |
| 15 | `BS-015 Government` | [`../government-domain-registry.md`](../government-domain-registry.md) | [`../domain-activity-mappings/government-domain-activity-mapping.md`](../domain-activity-mappings/government-domain-activity-mapping.md) | [`government-domain-keywords.md`](government-domain-keywords.md) | 96 |
| 16 | `BS-016 Nonprofit` | [`../nonprofit-domain-registry.md`](../nonprofit-domain-registry.md) | [`../domain-activity-mappings/nonprofit-domain-activity-mapping.md`](../domain-activity-mappings/nonprofit-domain-activity-mapping.md) | [`nonprofit-domain-keywords.md`](nonprofit-domain-keywords.md) | 92 |
|  | **Total** |  |  |  | **1,586** |

---

## 3. Per-sector assembly sequence

For any selected sector, assemble configuration in this order:

```text
1. Load broad-sector definition
2. Load sector domain registry
3. Load domain-to-activity applicability
4. Load selected domain keyword profile
5. Load selected activity keyword profiles
6. Load organization and exclusion profiles
7. Confirm active provider offering
8. Load offering-specific signal profiles
9. Apply sector overlay
10. Select approved source classes
11. Compose source-specific positive and negative queries
12. Capture immutable observations and match evidence
13. Resolve organization identity
14. Classify domain and activity
15. Evaluate commercial signals, contradiction, freshness and coverage
16. Assess opportunity
17. Resolve responsible function and lawful contact route
18. Publish only after policy and approval gates pass
```

Skipping a row in this sequence must produce an explicit validation error, not a silent default.

---

## 4. Connection identifiers

A runtime configuration should preserve at least these links:

```text
broad_sector_id
sector_domain_mapping_id
domain_id
domain_activity_assignment_id
activity_id
domain_keyword_profile_id
activity_keyword_profile_id
organization_cue_profile_id
exclusion_profile_id
provider_id
business_unit_id
service_offering_id
lead_generation_profile_id
offering_signal_profile_ids
sector_overlay_id
source_suitability_profile_id
source_model_id
query_template_id
locale_pack_id
semantic_model_id
classification_crosswalk_id
evidence_policy_id
qualification_profile_id
scoring_profile_id
contact_policy_id
```

Every reference must also preserve its version.

---

## 5. Duplicate and overlap controls

The same organization may match several sectors, domains and activities. Harvester must preserve one resolved organization identity and attach several evidence-backed facets.

It must not create duplicate organizations merely because:

- A pharmaceutical distributor matches Healthcare, Manufacturing and Logistics.
- A hotel booking platform matches Hospitality, Travel and Technology.
- A food processor matches Food and Agriculture, Manufacturing and Logistics.
- A payment platform matches Finance, Retail and Technology.
- A public hospital matches Healthcare and Government.
- A charitable hospital matches Healthcare and Nonprofit.

Overlap handling must preserve:

```text
one resolved organization
+ several sector facets
+ several domain facets
+ independently supported activities
+ offering-specific opportunities
```

Evidence and scores may be reused only through explicit shared-evidence references. They must not be counted repeatedly merely because several classifications point to the same source.

---

## 6. File connection rule

Sector domain keyword files are data registries. Their authority is limited to:

- Stable keyword-profile code.
- Canonical domain identity.
- Reviewed domain terms.
- Organization-cue profile reference.
- Exclusion-profile reference.
- Version and status.

They do not own:

- Activity applicability.
- Activity keyword definitions.
- Provider offerings.
- Buying intent.
- Operational pain.
- Competitors.
- Existing solutions.
- Query execution.
- Evidence confidence.
- Qualification.
- Opportunity scoring.
- Contact permission.

Those connections resolve through the shared files listed in Section 1.

---

## 7. Connection verification checklist

Before a sector configuration is accepted:

```text
Sector code resolves: Yes
Domain code resolves: Yes
Domain belongs to selected sector or approved cross-sector mapping: Yes
Domain activity assignment resolves: Yes
Activity is applicable to this domain: Yes
Domain keyword profile resolves: Yes
Activity keyword profile resolves: Yes
Organization and exclusion profiles resolve: Yes
Provider resolves: Yes
Active offering resolves: Yes
Offering-specific signal profiles resolve: Yes
Sector overlay resolves: Yes
Approved source classes resolve: Yes
Query template and composition versions resolve: Yes
Positive and negative query families exist: Yes
Evidence policy resolves: Yes
Qualification and scoring profiles resolve: Yes
Contact policy resolves: Yes
All versions are captured in the job snapshot: Yes
No duplicate organization or evidence inflation is introduced: Yes
```

A failed item blocks activation or job creation until corrected.

---

## 8. Accurate status

This matrix completes the documentation connection map for all 16 sectors, 1,586 domains and 519 activities.

It does not prove that the runtime database, importers, APIs, interface, query engine, classifiers, evidence graph, opportunity engine or contact-policy enforcement have been implemented.
