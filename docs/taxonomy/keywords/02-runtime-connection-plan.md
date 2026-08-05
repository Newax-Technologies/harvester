# Harvester Keyword Runtime Connection Plan

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This document converts the documentation sequence into a runtime connection plan. It remains subordinate to the Harvester roadmap, intelligence operating model, services model, provider-portfolio model, keyword development plan, application map, connection matrix, source models, and delivery addendum.

It does not create a second roadmap or authorize implementation by itself.

## 1. Runtime objective

The runtime must assemble one immutable lead-generation definition from independently governed references rather than copying registries into one flattened configuration.

```text
Provider
→ business unit
→ active offering
→ lead-generation profile version
→ sector selection
→ domain selection
→ domain-specific activity selections
→ domain and activity keyword profiles
→ organization and exclusion profiles
→ offering-specific commercial-signal profiles
→ sector overlay
→ source and query profiles
→ evidence and decision policies
→ immutable Harvest Job snapshot
```

## 2. Required connection records

### Provider configuration

```text
Provider
ProviderBusinessUnit
ServiceOffering
LeadGenerationProfile
LeadGenerationProfileVersion
OperationalActivation
```

### Market configuration

```text
BroadSectorSelection
DomainSelection
DomainActivitySelection
GeographicScope
OrganizationScaleScope
ExclusionRuleSelection
```

### Keyword configuration

```text
DomainKeywordProfileReference
ActivityKeywordProfileReference
OrganizationCueProfileReference
ExclusionProfileReference
LocalePackReference
```

### Commercial relevance configuration

```text
OfferingLeadSignalProfileReference
ProblemSignalProfileReference
BuyingIntentProfileReference
ProcurementSignalProfileReference
ExistingSolutionProfileReference
CompetitorProfileReference
ReplacementProfileReference
IntegrationProfileReference
ExpansionProfileReference
SectorOverlayReference
```

### Source and query configuration

```text
SourceSuitabilityProfileReference
SourceModelReference
QueryTemplateReference
QueryCompositionProfileReference
SemanticExpansionProfileReference
ClassificationCrosswalkReference
```

### Decision configuration

```text
EvidencePolicyReference
QualificationProfileReference
ScoringProfileReference
DecisionMakerRoleProfileReference
ContactRouteProfileReference
ContactPolicyReference
PublicationPolicyReference
```

## 3. Connection rules

1. Canonical sector, domain, activity and keyword records are read-only to tenants.
2. Tenant configuration stores references and versioned overrides rather than copying canonical identities.
3. A domain activity selection must reference an approved domain-to-activity applicability record.
4. Activity selection remains independent for every domain.
5. Offering-specific signal profiles require an active offering.
6. Source templates may only use source classes approved by the profile and current source model.
7. Query composition must preserve the origin of every term, signal, exclusion and semantic expansion.
8. Keyword matches remain evidence observations.
9. Classification, qualification, scoring and contact readiness remain separate decisions.
10. A completed job preserves every contributing version.

## 4. Proposed activation sequence

```text
DRAFT
→ STRUCTURALLY_VALIDATED
→ SEMANTICALLY_REVIEWED
→ SOURCE_VALIDATED
→ BENCHMARKED
→ APPROVED
→ ACTIVE
→ PAUSED or SUPERSEDED
→ ARCHIVED
```

A profile may not become active when:

- The provider or offering is inactive.
- A domain or activity reference is invalid.
- Required positive or negative query families are missing.
- A required source model is restricted or unapproved.
- Benchmark thresholds have not been met.
- Sensitive-sector review is incomplete.
- Tenant, consent, suppression or contact-policy dependencies are unresolved.

## 5. Immutable Harvest Job snapshot

Every job must snapshot:

```text
provider and business-unit versions
offering and lead-generation-profile versions
sector and domain versions
domain-to-activity assignment versions
activity versions
domain and activity keyword-profile versions
organization and exclusion-profile versions
offering-signal-profile versions
sector-overlay version
source suitability and source-model versions
locale and geography versions
query template and composition versions
semantic and classification versions
evidence, qualification and scoring-policy versions
role, contact-route and contact-policy versions
publication and export-policy versions
```

Changing a profile after job creation must not alter historical job meaning.

## 6. API connection sequence

The eventual API should enforce this order:

```text
1. Read provider and active offerings
2. Create or select lead-generation profile
3. Add sectors
4. Add domains inside sectors
5. Add activities inside each domain
6. Review domain and activity keyword profiles
7. Add offering-specific commercial signals
8. Add source classes, locale and geography
9. Preview positive and negative query families
10. Validate structural and policy connections
11. Benchmark or sample-test the profile
12. Submit for review
13. Activate approved version
14. Create Harvest Job from immutable snapshot
```

The interface must not expose a “generate leads” action before the complete chain is valid.

## 7. Evidence connection sequence

```text
Query execution
→ immutable source observation
→ keyword match evidence
→ context extraction
→ source suitability assessment
→ entity resolution
→ domain classification
→ activity classification
→ commercial-signal assessment
→ contradiction and freshness assessment
→ coverage assessment
→ qualification
→ opportunity assessment
→ responsible-function assessment
→ lawful-contact assessment
→ publication or export decision
```

No stage may rewrite an earlier source observation.

## 8. Delivery sequence

This plan maps to the existing roadmap through the keyword implementation and delivery addenda.

### Connection slice 1

- Registry import.
- Stable-code and version validation.
- Canonical read APIs.

### Connection slice 2

- Provider, offering and profile references.
- Sector, domain and activity configuration.
- Independent activity selections.

### Connection slice 3

- Domain, activity, organization and exclusion keyword references.
- Locale and override handling.

### Connection slice 4

- Offering-specific commercial-signal references.
- Sector overlays.
- Offering-isolation safeguards.

### Connection slice 5

- Source suitability.
- Query templates.
- Positive and negative preview.

### Connection slice 6

- Match evidence.
- Entity resolution and classification.
- Contradiction, freshness, duplicate-origin and coverage logic.

### Connection slice 7

- Qualification and scoring integration.
- Responsible role and lawful contact readiness.

### Connection slice 8

- Review, activation, rollback, feedback and immutable job snapshots.
- Full verification and controlled release.

## 9. Verification requirements

The runtime connection is not complete until tests prove:

1. Every canonical reference resolves.
2. Invalid cross-sector or domain-activity combinations are rejected.
3. Activity selections never propagate between domains.
4. Inactive offerings cannot attach or execute service-specific signals.
5. Tenant overrides cannot mutate canonical records.
6. Every query preserves complete provenance.
7. Every evidence record preserves source, context, time and profile versions.
8. Duplicate sources do not inflate confidence.
9. Negative and contradiction evidence is retained.
10. “Not found” does not become “absent” without coverage.
11. Historical jobs remain reproducible after profile changes.
12. Contact readiness cannot bypass suppression, consent, conflict, channel, jurisdiction or tenant policy.
13. Permissions and tenant isolation pass.
14. Benchmark and regression gates pass.
15. CI passes against the exact latest commit.

## 10. Accurate status

This file completes the documentation-level runtime connection plan.

It does not implement schemas, migrations, APIs, interface behavior, query execution, evidence processing, scoring, contact policy or releases.
