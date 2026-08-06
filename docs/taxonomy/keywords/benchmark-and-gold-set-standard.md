# Harvester Keyword Benchmark and Gold-Set Standard

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This standard defines the evidence required before a keyword, semantic, exclusion, role, source, or provider-offering profile may become active.

The current registries are comprehensive documentation candidates. They are not production-approved merely because all rows exist. Completion requires measured behaviour against reviewed examples.

## 1. Benchmark units

Benchmarks exist for:

- domain identity profiles;
- activity profiles;
- organization-cue profiles;
- exclusion and contradiction profiles;
- acronyms and ambiguous terms;
- semantic profiles;
- locale packs;
- lead-generation signals;
- provider-offering profiles;
- decision-role profiles;
- contact-route profiles;
- source-specific query families.

## 2. Minimum example classes

Every tested profile should include:

```text
TRUE_POSITIVE
TRUE_NEGATIVE
NEAR_POSITIVE
AMBIGUOUS
CONTRADICTORY
STALE
DUPLICATE_ORIGIN
WRONG_ENTITY
WRONG_SECTOR
WRONG_ACTIVITY
WRONG_GEOGRAPHY
SOURCE_UNSUITABLE
LOCALE_VARIANT
MALFORMED_OR_NOISY_TEXT
```

## 3. Recommended sample depth

| Profile risk | Positive | Negative | Ambiguous/near | Source-specific | Locale |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low-risk narrow identity | 10 | 10 | 5 | 5 | 0–5 |
| Broad or ambiguous identity | 25 | 25 | 20 | 10 | 5–10 |
| Activity profile | 20 | 20 | 10 | 10 | 5 |
| Offering signal profile | 30 | 30 | 20 | 15 | 5–10 |
| Sensitive or high-impact profile | 50 | 50 | 30 | 20 | 10–20 |
| Contact or role profile | 30 | 30 | 20 | 15 | 5–10 |

These are minimum planning targets, not a claim that every current profile already has this evidence.

## 4. Gold-set record

```text
example_id
profile_id and version
source class
source snapshot or immutable reference
language and locale
text span or structured record
resolved entity if applicable
event date and collection date
expected match mode
expected keyword or semantic match
expected exclusion or contradiction
expected evidence grade
expected disposition
reviewer and review date
sensitive-data classification
notes
```

## 5. Metrics

Measure at minimum:

- precision;
- recall estimate;
- false-positive rate;
- false-negative review rate;
- ambiguity rate;
- exclusion accuracy;
- contradiction detection rate;
- source acceptance rate;
- duplicate-origin suppression;
- stale-signal suppression;
- entity-resolution error rate;
- locale parity;
- human-review overturn rate;
- opportunity confirmation rate by signal type;
- contact-policy violation rate;
- downstream irrelevance and suppression rate.

## 6. Provisional activation thresholds

Thresholds must be calibrated by profile and risk. Suggested starting gates:

| Profile class | Precision | Critical false positives | Other requirements |
| --- | ---: | ---: | --- |
| High-precision domain identity | `>= 0.95` | `0` in sensitive examples | Recall sampled and documented |
| Broad/contextual identity | `>= 0.85` | `0` high-impact | Cannot qualify without corroboration |
| Activity confirmation | `>= 0.90` | `0` high-impact | Entity and domain context required |
| Provider direct-intent | `>= 0.95` | `0` fabricated intent | Source and event date verified |
| Operational pain | `>= 0.85` | `0` unsupported accusations | Corroboration or direct statement |
| Contact route | `>= 0.98` | `0` private or stale contacts | Policy and current-affiliation checks |
| Sensitive-sector signal | `>= 0.98` | `0` harmful inference | Human review required |

No aggregate average may hide one unsafe profile.

## 7. Evaluation splits

Use distinct:

- development set;
- validation set;
- holdout set;
- live shadow sample;
- post-activation audit sample.

Do not tune terms against the holdout set and then announce the resulting score as independent validation, a statistical costume party the software industry attends regularly.

## 8. Sector coverage

The benchmark programme must sample all 16 sectors and all major domain families. It must not validate only easy technology or retail profiles and assume healthcare, legal, government, and finance will behave similarly.

## 9. Locale evaluation

Locale packs require:

- native or professionally competent review;
- script, transliteration, and mixed-language examples;
- spelling variants;
- local trade terminology;
- ambiguous and culturally specific negatives;
- source-specific examples;
- parity checks against the canonical English profile.

## 10. Regression testing

Every profile revision must run:

- its own benchmark set;
- overlapping profile sets;
- sensitive-sector suite where applicable;
- malformed-token suite;
- acronym ambiguity suite;
- source-adapter suite;
- locale suite;
- prior false-positive regression cases.

A revision that improves recall but reintroduces a known harmful false positive must not activate.

## 11. Shadow and staged rollout

```text
OFFLINE_TEST
→ SHADOW_NO_DECISION
→ INTERNAL_RESEARCH_ONLY
→ LIMITED_WORKSPACE_ROLLOUT
→ CONTROLLED_PRODUCTION
→ FULLY_ACTIVE
```

Each stage defines monitoring, rollback thresholds, reviewer ownership, and permitted downstream actions.

## 12. Activation evidence record

```text
profile and version
benchmark-set version
metrics by example class
known limitations
sensitive-sector review
source and locale coverage
shadow-run results
approval identities
activation date
rollback version
post-activation review date
```

## 13. Completion rule

A registry may be described as:

- **Defined** when documentation and candidate profiles exist;
- **Repository-integrated** when the files are committed and indexed;
- **Benchmark-ready** when reviewed test sets exist;
- **Tested** when the latest candidate passes its benchmark suite;
- **Active** when approved and deployed under controlled rollout;
- **Complete** only when requirements, benchmarks, runtime integration, exact-head CI, operational verification, and no-known-issue requirements pass.
