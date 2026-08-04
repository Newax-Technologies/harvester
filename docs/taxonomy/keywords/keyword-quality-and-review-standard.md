# Harvester Keyword Quality and Review Standard

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This standard governs creation, review, activation, feedback, and retirement of domain, activity, signal, role, exclusion, and locale keyword profiles.

## 1. Mandatory review dimensions

Every profile must be reviewed for:

- semantic precision;
- recall value;
- ambiguity and homonyms;
- sector and activity context;
- organization-type compatibility;
- source suitability;
- language and locale;
- sensitive-data risk;
- prohibited or regulated use;
- freshness requirements;
- evidence threshold;
- negative and contradictory context;
- duplicate profile overlap;
- malformed stems and unsafe automatic variants.

## 2. Prohibited generation shortcuts

The following must not enter an approved profile without manual review:

- blind singularization or pluralization;
- truncated stems such as `manufactur`, `formulat`, or `franchis`;
- uncontrolled substring replacement;
- acronyms with several common meanings and no context rule;
- generic buzzwords such as `AI`, `platform`, `solution`, `digital`, or `innovation` without corroboration;
- a sector name used as a complete domain profile;
- a job title treated as proof of purchase authority;
- a public contact treated as consent;
- a missing website feature treated as confirmed operational absence;
- translations generated without locale review.

## 3. Profile lifecycle

```text
DRAFT
→ LEXICAL_REVIEW
→ DOMAIN_REVIEW
→ SOURCE_REVIEW
→ COMPLIANCE_REVIEW where required
→ READY_FOR_TEST
→ APPROVED
→ ACTIVE
→ SUPERSEDED or REVOKED
→ ARCHIVED
```

Production must never use a draft or unapproved profile.

## 4. Test set requirements

Every material profile should have:

- positive examples;
- near-positive examples;
- negative examples;
- ambiguous examples;
- source-specific examples;
- locale examples where supported;
- expected match mode;
- expected evidence state;
- expected exclusion behavior.

High-risk profiles require a reviewed benchmark set before activation.

## 5. Quality metrics

Recommended offline metrics include:

- precision by profile;
- recall by profile;
- false-positive rate;
- false-negative sample rate;
- ambiguity rate;
- source yield;
- evidence acceptance rate;
- duplicate-origin rate;
- stale-signal rate;
- human-review overturn rate;
- lead qualification rate after verification;
- downstream complaint, suppression, or irrelevance rate.

No single metric authorizes activation.

## 6. Feedback controls

1. User feedback creates a proposed revision, not a silent production mutation.
2. Rejected leads must record a structured reason such as wrong domain, wrong activity, stale event, weak evidence, wrong geography, no fit, duplicate, or contact restriction.
3. Converted or useful leads may support profile evaluation but do not prove every matched keyword was correct.
4. Profile changes require versioning, review, testing, approval, and rollback capability.
5. Completed Harvest Jobs retain the exact profile versions used.

## 7. Sensitive-sector controls

Healthcare, legal, finance, public-sector, employment, security, and nonprofit-beneficiary profiles require stricter review when keywords could reveal or imply sensitive facts.

Prohibited outcomes include:

- inferring a medical diagnosis;
- accusing an organization or person of crime or misconduct;
- inferring financial distress from weak evidence;
- collecting private beneficiary or patient data;
- targeting political beliefs or protected characteristics;
- bypassing procurement, referral, consent, or professional rules.

## 8. Acceptance checklist

```text
Canonical purpose defined: Yes
Active offering dependency defined: Yes where applicable
Positive examples reviewed: Yes
Negative and ambiguous examples reviewed: Yes
Source suitability reviewed: Yes
Freshness policy defined: Yes
Evidence threshold defined: Yes
Exclusion and contradiction rules defined: Yes
Sensitive-data risk reviewed: Yes
Locale reviewed or explicitly unsupported: Yes
Malformed variants absent: Yes
Duplicate overlap assessed: Yes
Version and rollback defined: Yes
```

## 9. Delivery boundary

This standard defines documentation and governance requirements. It does not implement profile storage, evaluation tooling, benchmark runners, approval workflows, search execution, classifiers, or release automation.
