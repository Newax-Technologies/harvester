# Universal Entity and Evidence Model

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned; current institution and provenance foundations remain partial**

## 1. Purpose

This document defines the runtime model required to evolve Harvester from `CanonicalInstitution`-centred persistence into a universal, evidence-backed commercial intelligence registry.

It preserves current raw records, institutions, branches, contacts, person candidates, provenance, resolution reviews, signals, lead profiles, qualification, and score history as migration inputs. It does not authorize a destructive rewrite.

## 2. Core distinction

A source record, observation, assertion, claim, resolved entity, lead profile, opportunity, and decision are different objects.

```text
Source-native payload
→ RawObservation
→ EvidenceArtifact
→ EvidenceAssertion
→ ResolutionCandidate
→ ResolutionDecision
→ ResolvedEntity
→ LeadProfile
→ QualificationAssessment
→ OpportunityAssessment
→ DecisionRecord
```

No object may silently stand in for another.

## 3. Universal entity types

Harvester must support at least:

```text
ORGANIZATION
PERSON
BRAND
BUSINESS_UNIT
FACILITY
LOCATION
PRODUCT
SERVICE
TECHNOLOGY
ROLE
DEPARTMENT
WEBSITE
APPLICATION
PUBLICATION
EVENT
JOB_POSTING
PROCUREMENT_NOTICE
CAMPAIGN
ADVERTISEMENT
MARKET
CATEGORY
```

Sector packs may introduce typed attributes and controlled subtypes. They must not create separate incompatible entity tables for each sector.

## 4. ResolvedEntity

```text
ResolvedEntity

id
tenant_id
workspace_id
entity_type
stable_key
revision
current_state
identity_confidence
quality_state
sensitivity_classification
first_seen_at
last_seen_at
last_material_change_at
created_at
updated_at
```

Harvester IDs remain stable when optional Core links are absent, added, changed, or removed.

## 5. Identity and identifiers

```text
EntityIdentifier

id
entity_id
identifier_type
normalized_value
original_value
issuing_authority
source_observation_id
verification_state
valid_from
valid_until
created_at
```

Examples:

- legal registration number;
- domain;
- provider-specific place ID;
- social-profile URL;
- professional registration;
- tax identifier;
- application-store identifier;
- customer-owned external ID.

Identifiers are evidence-backed and may conflict. One source does not automatically become universal truth.

## 6. Aliases and names

```text
EntityName

id
entity_id
name_type
original_value
normalized_value
language
script
source_observation_id
valid_from
valid_until
is_current
```

Name types include legal, trading, brand, local-language, transliterated, former, abbreviation, and source-specific display name.

## 7. Relationships

```text
EntityRelationship

id
tenant_id
subject_entity_id
relationship_type
object_entity_id
valid_from
valid_until
confidence
status
evidence_snapshot_id
created_at
```

Initial relationship types include:

```text
OWNS
OPERATES
EMPLOYS
HOLDS_ROLE
LOCATED_IN
BRANCH_OF
PART_OF
SELLS
PROVIDES
USES_TECHNOLOGY
PARTNERS_WITH
COMPETES_WITH
DISTRIBUTES
SUPPLIES
REFERS_TO
PUBLISHED
ATTENDED
AWARDED_TO
TARGETS_MARKET
```

## 8. RawObservation

```text
RawObservation

id
tenant_id
workspace_id
source_system
source_record_id
source_record_version
source_schema_version
connector_version
collection_job_id
source_run_id
captured_at
payload_hash
raw_payload_reference
authority_reference
access_classification
retention_policy
supersedes_observation_id
```

Raw observations are immutable. Repeated identical payloads may deduplicate by source identity and hash. Changed payloads create new versions.

## 9. EvidenceArtifact

```text
EvidenceArtifact

id
raw_observation_id
artifact_type
content_hash
storage_reference
source_locator
mime_type
fetch_status
captured_at
published_at
effective_at
access_classification
retention_policy
redaction_state
```

Large HTML, PDF, image, media, and document bodies belong in object storage. PostgreSQL stores metadata, hashes, locators, access rules, and extraction references.

## 10. EvidenceExcerpt

```text
EvidenceExcerpt

id
evidence_artifact_id
excerpt_type
text_or_value
page_number
selector
start_offset
end_offset
bounding_box
content_hash
created_at
```

An excerpt identifies the exact part of an artifact supporting an assertion. A URL alone is not sufficient evidence when a page contains several unrelated statements.

## 11. EvidenceAssertion

```text
EvidenceAssertion

id
tenant_id
subject_candidate_or_entity_id
predicate
normalized_value
value_type
assertion_kind
source_observation_id
evidence_artifact_id
evidence_excerpt_id
extractor_type
extractor_version
source_reliability
extraction_certainty
corroboration_state
freshness_state
coverage_state
valid_from
valid_until
status
```

Allowed assertion kinds:

```text
OBSERVED_FACT
DERIVED_VALUE
MODEL_INFERENCE
OPERATOR_ASSESSMENT
NEGATIVE_EVIDENCE
UNKNOWN
CONFLICT
```

An assertion kind is immutable. A later review creates a new assertion or decision rather than relabelling history.

## 12. Claim

```text
Claim

id
subject_entity_id
predicate
object_entity_id_or_value
claim_type
claim_status
confidence_dimensions
valid_from
valid_until
created_at
supersedes_claim_id
```

Claim types:

```text
OBSERVED
DERIVED
INFERRED
RECOMMENDED
DISPUTED
SUPERSEDED
```

Claims link to one or more assertions through `ClaimEvidenceLink`. Corroboration counts independent origins, not copied pages or syndication duplicates.

## 13. CoverageRecord

```text
CoverageRecord

id
source_run_id
scope_type
scope_reference
planned
attempted
completed
blocked_reason
failure_reason
coverage_ratio
observed_at
```

Coverage prevents these states from collapsing:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_INSPECTED
INSPECTION_FAILED
UNKNOWN
NOT_APPLICABLE
```

Only sufficiently authoritative evidence may create `ABSENT_CONFIRMED`.

## 14. Contradiction

```text
EvidenceContradiction

id
subject_reference
predicate
left_assertion_id
right_assertion_id
conflict_type
materiality
review_state
resolution_decision_id
created_at
```

A contradiction is preserved even after a reviewer selects the current value.

## 15. Resolution

Resolution follows:

```text
Candidate generation
→ match and conflict features
→ identity confidence
→ recommended action
→ human or policy decision
→ reversible resolution history
```

Decisions include:

```text
MERGE
LINK
REJECT
SPLIT
KEEP_SEPARATE
REVIEW_REQUIRED
REVERSE_PRIOR_DECISION
```

Physical deletion must not be used to disguise a mistaken merge.

## 16. LeadProfile

A lead profile is a current commercial projection of a resolved entity under a workspace and active market context.

```text
LeadProfile

id
tenant_id
workspace_id
resolved_entity_id
revision
lead_status
market_fit
contactability
organization_context
person_context
operational_context
quality_state
compliance_state
current_summary
updated_at
```

One entity may have different lead profiles for different workspaces, clients, markets, or offerings without duplicating identity.

## 17. Opportunity hypothesis

```text
OpportunityHypothesis

id
lead_profile_id
offering_version_id
signal_profile_version_id
need_or_gap_type
supporting_claims
contradicting_claims
coverage_state
confidence_dimensions
status
created_at
```

No active offering means no commercial opportunity assessment.

## 18. Migration from current runtime

The migration sequence is:

1. Add tenant and workspace scope to current records.
2. Introduce universal entity tables without removing current canonical tables.
3. Backfill institutions as `ORGANIZATION` entities and branches as `FACILITY` or `LOCATION` entities according to reviewed rules.
4. Backfill person candidates as `PERSON` entities without upgrading uncertain candidates to confirmed identity.
5. Convert `FieldProvenance` into assertion and claim links while preserving original rows during transition.
6. Introduce object-storage artifact references and migrate large snapshots in bounded batches.
7. Dual-write current and universal models behind one service boundary.
8. Compare projections and resolve discrepancies.
9. Move read APIs and workspaces to universal projections.
10. Retire compatibility tables only after verified rollback and restoration paths exist.

## 19. Architectural tests

Tests must prove:

1. one source observation can support several assertions without payload duplication;
2. several observations can support one claim;
3. copied or syndicated origins do not inflate source diversity;
4. contradictions remain visible after a current-value decision;
5. a merge can be reversed without losing evidence;
6. one entity can hold separate client-specific lead profiles;
7. tenant boundaries hold across evidence, entities, relationships, search, files, and exports;
8. non-detection cannot produce confirmed absence;
9. every client-facing material claim resolves to an exact artifact and excerpt;
10. historical decisions remain reconstructable after later enrichment.

## 20. Locked rule

> Harvester preserves what sources said, what the system inferred, what operators decided, and what is currently believed as separate, traceable records.
