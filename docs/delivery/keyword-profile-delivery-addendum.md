# Harvester Keyword Profile Delivery Addendum

Status: **Proposed delivery addendum**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This delivery addendum incorporates the domain, activity, and offering-specific keyword plan into the existing Harvester roadmap without replacing the roadmap or creating a second top-level module count.

Authority remains with:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)
- [Harvester Services and Opportunity Model](../SERVICES.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [Keyword and Evidence Profile Integration Addendum](../architecture/keyword-evidence-profile-integration-addendum.md)
- [Keyword Profile Implementation Plan](../taxonomy/keywords/keyword-profile-implementation-plan.md)

---

## 1. Delivery objective

Deliver a versioned keyword-profile system that uses the existing 16-sector, 1,586-domain, 519-activity, lead-signal, role-cue, source-suitability, and evidence-control registries as governed configuration.

The delivered system must let a provider:

1. Select an active service offering.
2. Select one or more broad sectors.
3. Select one or more domains inside each sector.
4. Select activities separately inside each selected domain.
5. Review separate domain and activity keyword profiles.
6. Review offering-specific lead-signal profiles.
7. Configure exclusions, sources, languages, geography, freshness, and evidence thresholds.
8. Preview queries and sample matches.
9. Activate a versioned profile.
10. Generate leads from a frozen, reproducible definition.

---

## 2. Existing-roadmap crosswalk

The keyword plan strengthens existing delivery areas rather than creating new product modules.

| Existing delivery area | Added keyword-profile scope |
| --- | --- |
| Market definition | Sector, domain, domain-specific activity, keyword-profile, locale-pack, source-policy, signal-profile, and query-template versions |
| Provider and service offerings | Offering-specific problem, intent, procurement, competitor, existing-solution, replacement, integration, maintenance, and gap profiles |
| Source planning | Source-suitable query families, positive and negative queries, cost and breadth controls |
| Acquisition | Query execution provenance and source-native result preservation |
| Evidence | Keyword match, context span, match mode, source suitability, event date, contradiction, and duplicate-origin evidence |
| Entity resolution | Organization, person, role, affiliation, location, and contact-route resolution after discovery |
| Verification | Domain, activity, signal, freshness, contradiction, and sensitive-context review |
| Lead profiles | Traceable domain, activity, signal, role, and contact-readiness facets |
| Opportunity scoring | No raw keyword-count scoring; only supported evidence and selected offerings participate |
| Operations | Profile versions, review queues, benchmarks, false-positive feedback, rollback, quality metrics, and audit |
| Frontend | Guided profile review, query preview, sample testing, activation, final search-definition review, and result explanation |
| API and exports | Bounded profile references, evidence references, and approved result packages without exposing private query strategy |

---

## 3. Delivery gates

### Gate K0 — Documentation baseline

Required evidence:

- Canonical registries exist.
- Every domain and activity has a stable code.
- Keyword and signal profile rules are documented.
- Architecture and delivery boundaries are documented.
- No runtime completion claim is made.

### Gate K1 — Schema and migration design

Required outcomes:

- Profile, term, version, reference, feedback, query, and match-evidence schemas are defined.
- Tenant isolation and canonical-versus-tenant ownership are explicit.
- Historical job references remain resolvable.
- Migration and rollback plans exist.
- Existing data compatibility is assessed.

Gate evidence:

- Schema review
- Migration tests
- Rollback test
- Tenant-isolation tests
- Data-import validation

### Gate K2 — Canonical registry import

Required outcomes:

- Existing canonical keyword definitions are imported.
- All 1,586 domain profiles resolve.
- All 519 activity profiles resolve.
- Lead-signal, role-cue, contact-route, source-suitability, and control profiles resolve.
- Duplicate codes, orphan references, malformed terms, and unsupported match modes fail validation.

Gate evidence:

- Deterministic import
- Count reconciliation
- Uniqueness checks
- Referential-integrity checks
- Re-import idempotency

### Gate K3 — Profile lifecycle APIs

Required outcomes:

- Read canonical profiles.
- Create tenant-owned overrides.
- Create versions.
- Review, activate, pause, supersede, and roll back.
- Enforce permissions.
- Prevent tenant mutation of canonical profiles.
- Record audit history.

Gate evidence:

- API tests
- Authorization tests
- Tenant-boundary tests
- Status-transition tests
- Concurrency tests
- Audit-log tests

### Gate K4 — First-page configuration

Required outcomes:

- Provider and active offering selection precede offering-specific keywords.
- Sector selection precedes domain selection.
- Domain selection precedes domain-specific activity selection.
- Every selected domain presents its own activity and keyword group.
- Final review shows every active profile and version.
- Generate Leads remains disabled until the definition is valid.

Gate evidence:

- Component tests
- Accessibility tests
- Responsive tests
- End-to-end configuration scenarios
- Invalid and contradictory definition tests

### Gate K5 — Query preview and composition

Required outcomes:

- Source-specific positive and negative queries are composed from approved versions.
- Query breadth and source limits are enforced.
- Term provenance is visible.
- Operators can test sample queries before activation.
- Sensitive queries require the configured review level.

Gate evidence:

- Query snapshot tests
- Golden test cases
- Negative-query tests
- Source-policy tests
- Locale-pack tests
- Cost-limit tests

### Gate K6 — Match evidence and classification

Required outcomes:

- Every match records profile, term, match mode, source, query, language, context, time, and classifier version.
- Context assessment remains separate from the raw match.
- Entity resolution occurs before responsible-role and contact resolution.
- Domain, activity, and signal confidence remain separate.
- Contradictory and stale evidence is retained and evaluated.

Gate evidence:

- Evidence persistence tests
- Context-classification tests
- Duplicate-origin tests
- Freshness tests
- Contradiction tests
- Traceability tests

### Gate K7 — Opportunity and contact-readiness integration

Required outcomes:

- Only active selected offerings participate.
- Keyword evidence alone cannot create an opportunity.
- Existing-solution terms permit replacement, integration, migration, optimization, support, expansion, or no-opportunity outcomes.
- Qualified opportunity and contact readiness remain separate.
- Consent, suppression, source-purpose, channel, and jurisdiction policies are enforced.

Gate evidence:

- Offering-eligibility tests
- Opportunity-decision tests
- Contact-policy tests
- Sensitive-sector tests
- Suppression tests
- Explanation tests

### Gate K8 — Feedback and governance

Required outcomes:

- Operators can report false positives, missing aliases, source mismatch, stale profiles, and negative-context failures.
- Feedback enters a review queue.
- Approved corrections create a new profile version.
- Historical jobs remain unchanged.
- Rollback restores a prior approved version.

Gate evidence:

- Feedback workflow tests
- Version-diff tests
- Activation tests
- Rollback tests
- Historical reproducibility tests

### Gate K9 — Production readiness

Required outcomes:

- Complete local-equivalent verification passes.
- Complete CI passes against the exact latest commit.
- Security and privacy review passes.
- Performance budgets pass.
- Import counts and profile references reconcile.
- Operator workflow is validated.
- No known unresolved release blocker remains.

---

## 4. Required benchmark set

Before production activation, Harvester must maintain a reviewed benchmark set containing:

- Clear positive domain examples
- Ambiguous domain examples
- Clear negative domain examples
- Activity-positive and activity-negative examples
- Offering-intent examples
- Existing-solution examples
- Replacement and integration examples
- Procurement open, amended, cancelled, closed, and awarded examples
- Job-posting examples that do and do not indicate relevant operational signals
- Current and stale event examples
- Duplicate-source-origin examples
- Sensitive-sector examples
- Urdu and Roman Urdu locale examples where the locale pack is activated

The benchmark must preserve source class, expected classification, expected exclusions, expected confidence dimensions, and reviewer rationale.

---

## 5. Minimum quality metrics

The implementation must report, by profile and source class where meaningful:

- Precision on reviewed samples
- False-positive rate
- Reviewed false-negative findings
- Ambiguous-term rate
- Negative-context catch rate
- Stale-event catch rate
- Duplicate-origin suppression rate
- Query yield
- Resolved-organization yield
- Supported-opportunity yield
- Contact-ready yield
- Reviewer agreement
- Average review age
- Profile version age
- Rollback frequency

No metric becomes an automatic self-modification trigger.

---

## 6. Migration and rollout strategy

Recommended rollout:

```text
Documentation baseline
→ schema behind feature flag
→ canonical import in non-production
→ read-only profile inspection
→ tenant draft overrides
→ query preview without acquisition
→ limited approved-source acquisition
→ evidence-only shadow mode
→ human-reviewed opportunity mode
→ bounded production activation
```

Shadow mode must not publish, export, contact, or automatically qualify targets.

Production activation should begin with a limited number of:

- Providers
- Offerings
- Sectors
- Domains
- Activities
- Sources
- Languages
- Query families

Expansion requires reviewed evidence rather than enthusiasm produced by one promising demo.

---

## 7. Definition of done

The keyword-profile runtime may be called **Complete** only when:

- The approved scope is implemented.
- All affected layers agree.
- All canonical imports reconcile.
- All acceptance criteria pass.
- Security and sensitive-sector controls pass.
- The actual operator workflow passes.
- Exact-head CI is green.
- No known unresolved issue remains.
- Production behavior is verified where production activation is in scope.

A Markdown registry, imported row count, successful API response, or visually convincing interface is not independently evidence of completion. Software has repeatedly demonstrated an ability to look organized while quietly doing the wrong thing.

---

## 8. Delivery boundary

This file adds delivery sequencing to the existing plan.

It does not authorize implementation, change the 64-module count, alter runtime behavior, or declare any gate passed.
