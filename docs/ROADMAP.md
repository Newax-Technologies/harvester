# Harvester module roadmap

Harvester is a universal market-intelligence and lead-discovery system — it finds, verifies,
enriches, scores, and ranks. It is explicitly **not** an emailing/sales-conversation system and
does not own canonical commercial identity. The three-way boundary:

```text
Harvester         Finds, verifies, enriches, scores, and ranks.
Engagement Engine  Contacts, follows up, receives, and responds.
Core / CRM          Owns canonical identity and the commercial relationship.
```

This doc is the planned module list. Nothing here is scheduled — modules get built when
explicitly requested, in whatever order is asked for. This is a reference, not a sprint plan.

## Tracked follow-ups from the core-newax sync integration

These are gaps identified while building the harvester → core-newax lead sync (`lead_sync_emitter.py`,
`manual_leads.py`'s webhook hook). Each was deliberately scoped out of that work, not forgotten:

1. **Outbox/retry durability. DONE (harvester side).** `LeadSyncEmitter.emit_institution_upserted`
   is still fire-and-forget on its own and stays that way (its public signature/behavior is
   relied on by its own existing test suite) — but `api/routes/manual_leads.py` and
   `integrations/lead_sync_resync.py` (the two production call sites) no longer call it
   directly. Both now go through `services/outbox_service.py::enqueue_and_attempt_delivery`,
   which persists an `EventOutbox` row (its `id` *is* the envelope's `eventId`, extracted once at
   enqueue time so every retry of that row reuses the identical id) before attempting delivery,
   so a failed delivery becomes a retryable PENDING row instead of a lost event. Retries use
   exponential backoff (`process_pending_deliveries`, claimed via `SELECT ... FOR UPDATE SKIP
   LOCKED` — the same pattern used everywhere else in this codebase — with each row's attempt
   isolated in its own savepoint) up to `MAX_ATTEMPTS` (6), after which a row moves to
   `DEAD_LETTER` and needs an explicit `requeue_dead_letter` call to try again. Invokable via the
   `process-outbox` CLI command or `GET/POST /api/v1/outbox/*`. An `event_id`-keyed inbox on
   core-newax's side for idempotent replay is still unbuilt — that half of this follow-up
   remains open.
2. **Wire up the dormant auto-resolution pipeline. DONE.** `resolution/orchestrator.py::resolve_incoming_record`
   now runs blocking + scoring for every `RawSourceRecord` created by `pipeline.py` (both
   `process_place` and `_run_web_crawler`), and decides: attach to an already-resolved
   institution, merge with an unresolved match, leave PENDING candidates for human review via
   the (now-fixed) `resolution-reviews` API, or give a confidently-distinct record its own
   institution. `canonical/merger.py` gained source-type-aware field extraction (it previously
   assumed every record was Google-Places-shaped), a same-location-aware branch-collapse path,
   and an `attach_record_to_institution` path for merging into an existing institution. Known v1
   limitation, documented in `resolution/orchestrator.py`'s docstring: two concurrent runs can
   each independently create a separate institution for what should be one, since resolution
   only sees records already committed by *other* completed runs, not concurrent in-flight ones
   — a full fix (advisory locks / per-record commits / a unique constraint) is separate follow-up
   work. This was module 5 ("Entity Resolution and Deduplication") above.
3. **Broader contact-type support.** Contact points outside phone/email/whatsapp/telegram (e.g.
   `linkedin`) are currently skipped-and-logged rather than synced, since core-newax's
   `ContactType` only supports that set. Expanding it is a joint harvester+core-newax change.
4. **Deletion/reconciliation.** The sync is currently append-and-update only; if a phone number
   or branch disappears from harvester, the previously-synced core-newax record isn't removed
   or expired. Full reconciliation is unbuilt.
5. **Cross-record person deduplication. Harvester side DONE, core-newax side still open.**
   `models/person.py`'s `PersonCandidate` (module 1, "Entity Registry") now gives harvester its
   own identity-clustering layer: `services/person_candidate_service.py::resolve_person_candidate`
   finds-or-creates one `PersonCandidate` per (institution, exact-after-`normalize_name` name),
   wired into every live `ContactPoint`-writing path (`canonical/merger.py`'s
   `_add_contact_if_present`, `api/routes/manual_leads.py`'s contact loop), so the same real
   person named on two different `contact_point` rows for one institution now converges onto one
   `ContactPoint.person_candidate_id` instead of staying two unrelated bare strings. What's still
   open: the lead-sync outbox/export layer doesn't use `person_candidate_id` as its `CorePerson`
   external-key namespace yet (it still keys by raw `contact_point.id`), so core-newax's own
   `CorePerson` de-dup gap is unchanged until that wiring is done as separate follow-up work.

## Planned modules

1. **Entity Registry** (`entities/`) — institution, branch, contact_point, person_candidate,
   source_record, signal. A `person_candidate` is a discovered *possible* contact, not a
   verified person, until resolved.
2. **Source Connectors** (`sources/`) — google_places, apple_maps, yandex_maps, web, search,
   telegram, authorized_imports. Unauthorized scraping/account automation is out of bounds;
   authorized imports and licensed/manual research are the accepted pattern.
3. **Collection and Crawling** (`ingestion/`) — source_scheduler, web_crawler, rate_limiter,
   page_fetcher, raw_snapshot, ingestion_job.
4. **Data Normalization** (`normalization/`) — organization_name, phone, email, website,
   social_handle, address, city, country.
5. **Entity Resolution and Deduplication** (`resolution/`) — exact/fuzzy/domain/phone/
   geographic matching, duplicate_candidates, merge_review, canonicalization.
6. **Enrichment** (`enrichment/`) — website_analyzer, contact_extractor, social_resolver,
   technology_detector, institution_classifier, location_enricher, decision_maker_discovery.
7. **Business Intelligence** (`intelligence/`) — opportunity_signals, pain_detection,
   size_estimation, operational_maturity, icp_matching, buying_signals, research_summary.
8. **Lead Scoring** (`scoring/`) — contactability/fit/opportunity/evidence/freshness/risk
   scores, score_explanation, score_history. Evidence-backed, not an opaque single number.
9. **Persistent Lead Profiles** (`profiles/`) — lead_profile, organization_summary,
   contactability, research_evidence, score_history, qualification_state, profile_history.
10. **Ranking and Daily Selection** (`allocation/`) — deterministic_ranking, eligibility_filter,
    daily_selection, reservation, duplicate_prevention, release_expired_reservations.
11. **Compliance and Source Governance** (`compliance/`) — source_policy, suppression,
    disqualification, consent_evidence, channel_eligibility, retention, deletion_requests.
    Harvester stores and obeys suppression; the Engagement Engine receives/processes opt-outs.
12. **Verification and Data Quality** (`verification/`) — evidence_validation,
    confidence_scoring, conflict_detection, freshness_checks, unreachable_contact_checks,
    source_comparison, review_queue.
13. **Export and Integration** (`exports/`, `integrations/`) — CSV/JSON export, core_sync,
    external_references, event_outbox, webhook_signing, delivery_status. Target pipeline:
    `harvester transaction → durable outbox → signed event delivery → Core inbox →
    idempotent processing → confirmed delivery` (the current `lead_sync_emitter.py` only
    implements the "signed event delivery" step — no outbox/inbox yet, tracked separately).
14. **Manual Lead Intake** (`manual_leads/`) — create_manual_lead, validate_submission,
    add_branch, add_contact_point, submit_for_resolution. Feeds the same normalization/
    resolution pipeline as scraped data, not a second-class path.
15. **Operations and Administration** (`operations/`) — job_management, source_health,
    failure_queue, configuration, audit, metrics, health_checks, admin_api.

## Explicitly not part of Harvester

Moved to the separate NEWAX Engagement Engine: email sending, WhatsApp sending, message
generation, approval workflow, follow-up sequences, reply monitoring/classification, automated
responses, meeting booking, bounce/complaint handling, communication timing, conversation
management.

Owned by NEWAX Core/CRM: canonical organizations, canonical people, users, memberships,
permissions, commercial lead stage, opportunity records, sales ownership, tasks, meetings,
authoritative CRM timeline.

## Current state vs. this plan (as of this doc's creation)

Roughly mapped against what exists in `src/lead_harvester/` today:

- **Entity Registry**: done for v1 scope. `models/canonical.py` has institution/branch/
  contact_point; `models/source.py` has source_record; `models/person.py`'s `PersonCandidate`
  and `models/signal.py`'s `Signal` are the two entities this module added. `PersonCandidate`
  is wired into every live `ContactPoint`-writing path via `services/person_candidate_service.py`
  (see the "cross-record person deduplication" tracked follow-up above for what it fixes and
  what's still open on the core-newax side). `Signal` is populated by
  `intelligence/researcher.py::_persist_findings`: each `pain_points`/`buying_signals` list item
  from the AI analysis becomes its own queryable/filterable `Signal` row (`PAIN_POINT`/
  `BUYING_SIGNAL`), alongside — not instead of — the existing `ResearchFinding` row that already
  holds the complete, unedited AI output as one JSON blob. Invokable via the
  `list-person-candidates`/`list-signals` CLI commands or `GET /api/v1/entities/*`. As part of
  this module, `intelligence/pain_detection.py` and `intelligence/scoring.py` were deleted:
  confirmed zero live callers, both existed only to consume the dead Phase-1 `entities/`
  dataclasses this doc's Lead Scoring note already flagged as superseded — leaving them in place
  next to the new, real `Signal` model would have been exactly the kind of shadow-implementation
  confusion `docs/CODE_REVIEW_LESSONS.md` pattern 2 warns about. The `entities/` dataclasses
  themselves (and `storage/sqlite.py`) were deliberately kept: the `migrate-phase1` CLI command
  is a real, still-needed one-time importer that depends on them. Known v1 limitation: no fuzzy/
  trigram matching for `PersonCandidate` (exact-after-`normalize_name` only, consistent with this
  codebase's other identity-matching v1 scopes); no automated merge/split UI for a
  `PersonCandidate` a human later decides was wrong.
- **Source Connectors**: done. `sources/` now has all seven: google_places, web,
  authorized_imports, plus `yandex_maps.py` (Yandex Maps Search API, mirrors
  google_places.py's shape), `apple_maps.py` (Apple MapKit Server API -- signs its own ES256
  developer JWT locally and exchanges it for a short-lived access token; known v1 limitation:
  Apple's `/v1/search` response has no phone/website field the way Google Places/Yandex do, so
  those stay blank for Apple-sourced records), and `telegram_channels.py` (fetches a channel's
  public `https://t.me/s/<channel>` preview page -- the page Telegram itself serves without
  authentication for anonymous/embed viewing; no login/MTProto/Bot-API involved, and no
  discovery -- job.yaml's `telegram_channels` list is the only input, since Telegram exposes no
  public search). `job.yaml`'s `places_provider` key (`google`/`apple`/`yandex`) selects which
  tile-based connector `LeadPipeline.run()` drives through the same
  `geographic_tiling.py` query machinery; `canonical/merger.py::display_fields` and
  `compliance/source_policy.py` were extended with a branch/entry per new SourceType (Yandex and
  Apple Maps are LICENSED_API; Telegram is PUBLIC_WEB_CRAWL, not ACCOUNT_AUTOMATION, since it's
  an unauthenticated page fetch). Also found and fixed: `sources/search.py`'s
  `BraveSearchSource` had zero callers anywhere in the codebase since it was written (a
  genuinely dead connector, not merely "partial") -- wired into `_run_web_crawler` as an
  optional seed-discovery step (`job.yaml`'s `search_queries` list; requires
  `BRAVE_SEARCH_API_KEY`), since its only purpose is discovering more seed URLs for the same web
  crawler that already exists, not a separate ingestion path.
- **Ingestion**: done for the pieces that were genuine gaps; the rest of this module's
  sub-concerns were already satisfied by existing code, just not living under a dedicated
  `ingestion/` directory -- moving already-correct, already-tested code into a new folder purely
  for naming purity would have been pure churn, not a real improvement, so it wasn't done.
  `web_crawler`/`page_fetcher`/`rate_limiter` are `sources/web.py`'s `WebCrawler`/`_fetch`/
  `DomainRateLimiter` (plus `RobotsCache` for robots.txt compliance); `ingestion_job` is
  `models/source.py`'s `SourceRun` (status/started_at/completed_at per run, already exposed via
  `services/operations_service.py`'s `list_source_runs`/`get_source_run_detail`);
  `source_scheduler` is intentionally external (an operator's cron/k8s CronJob/etc. invokes
  `lead-harvester run --config job.yaml` on a schedule) rather than an in-process scheduler --
  a deliberate, common architecture for this kind of tool, not a gap. What was genuinely
  missing: `raw_snapshot`. `RawSourceRecord.raw_payload` only ever stored the EXTRACTED lead
  fields for a domain (aggregated across every page that contributed to it) -- the actual
  fetched HTML was discarded, with no way to audit what a crawl actually saw, re-run extraction
  against historical pages without re-fetching, or tell "page had no useful data" apart from
  "page was skipped/failed and never really looked at". `models/source.py`'s new
  `RawPageSnapshot` is that record: one row per page a WEBSITE crawl attempted, success or
  failure (robots-disallowed/non-HTML/oversized/HTTP-error/decode-error all captured with a
  machine-readable `fetch_error` reason), accumulated on `WebCrawler` during `crawl()` (as a
  `self.snapshots` side channel, not part of `crawl()`'s return value, so no caller's signature
  had to change) and persisted by `pipeline.py::_run_web_crawler` once the run's `SourceRun`
  exists. Invokable via the `ops-page-snapshots` CLI command or
  `GET /api/v1/operations/page-snapshots` (excludes the stored HTML body from the response --
  query the database directly for that). Known v1 limitation: no separate retention/expiry
  policy for this table (`services/compliance_service.py::purge_expired_raw_records` only ever
  targeted `RawSourceRecord`).
- **Normalization**: partial, lives in `resolution/normalize.py` rather than its own module;
  covers phone/domain/name, plus `normalize_city` and `country_to_iso2` (a ~55-entry country
  name/alias -> ISO-2 table), the latter wired into `sources/authorized_imports.py` so a CSV row
  with a free-text `country` column but no explicit `country_code` still gets a real ISO-2 code
  instead of silently falling back to the import's default. No `website`/`social_handle`
  normalization yet.
- **Resolution**: done for the live ingestion paths. `resolution/orchestrator.py` wires
  blocking + scoring into `pipeline.py` (both Google Places and the web crawler), with a human
  review path for ambiguous (PENDING) matches via the `resolution-reviews` API. See tracked
  follow-up #2 above for the one documented v1 limitation (cross-run concurrency).
- **Enrichment**: done for the pieces that map onto live data. `enrichment/technology_detector.py`
  runs rule-based pain-point/buying-signal detection over each crawled page's visible text
  (`sources/web.py::_extract_lead`); `pipeline.py::_persist_detected_signals` materializes its
  output into real `models/signal.py` `Signal` rows once a page resolves to an institution,
  gated on `SourceType.WEBSITE`. Revives the intent of the deleted `intelligence/pain_detection.py`
  (dead Phase-1 code -- see `docs/CODE_REVIEW_LESSONS.md` pattern 2) with a real, wired
  implementation instead. contact_extractor/social_resolver are already covered by
  `extractors.py` (`extract_emails`/`extract_phones`/`extract_social_profiles`), reused by the
  crawler rather than duplicated. The dead, synchronous `enrichment/website_analyzer.py` (a
  superseded Phase-1 fetch helper with zero live callers) was removed. Known v1 limitation:
  text-pattern matching only, no HTML/DOM inspection -- can't fingerprint a specific CMS or
  booking widget by its markup. institution_classifier/location_enricher/
  decision_maker_discovery remain unbuilt.
- **Business Intelligence**: done for the pieces that map onto live data.
  `opportunity_signals`/`pain_detection`/`buying_signals` are covered by `models/signal.py`'s
  `Signal` table (module 1) fed from two sources: `intelligence/researcher.py`'s AI analysis
  (LinkedIn) and `enrichment/technology_detector.py`'s rule-based detection (module 6, website
  text). `research_summary` is `intelligence/research_summary.py::summarize_signals` -- composes
  a real summary from Signal evidence for every institution that has no AI-generated one, not a
  hardcoded "no summary yet" placeholder. `size_estimation` is
  `intelligence/size_estimation.py::estimate_size_tier` -- a branch-count/contact-count proxy
  (the only size signal this schema has; no headcount data exists). `operational_maturity` is
  `intelligence/operational_maturity.py::compute_operational_maturity` -- a 0-100 score from
  website presence and detected pain-point/buying-signal counts, distinct from the sales-facing
  lead score. `icp_matching` is `intelligence/icp_matching.py::score_icp_fit` -- a real,
  configurable weighted match (`Settings.icp_target_institution_types`/`icp_min_branch_count`)
  against operator-stated criteria, unlike `profiles/scoring.py`'s `category_fit` category
  (which only asks whether `institution_type` is known at all, not whether it matches anyone's
  target). All three are computed in `services/lead_profile_service.py::refresh_lead_profile`
  and stored on `LeadProfile` (`size_tier`/`operational_maturity_score`/`icp_match_score`),
  surfaced through the existing `GET /api/v1/lead-profiles*` API. Also fixed a real bug found in
  the same pass: `profiles/scoring.py`'s `research_signal` category and `organization_summary`
  previously only ever read `ResearchFinding` rows (LinkedIn-only) -- a website-crawled
  institution with real `technology_detector.py`-detected signals earned zero score credit and
  got a static "no summary yet" placeholder despite the evidence sitting in the `Signal` table
  the whole time. Both now read `Signal` directly (a strict superset of what `ResearchFinding`'s
  `pain_points`/`buying_signals` list findings held, since `researcher.py` already writes a
  `Signal` row for each of those items too -- reading both would have double-counted a
  LinkedIn-researched institution's evidence). `icp_matching`'s v1 limitation: only two criteria
  (institution type, minimum branch count) are configurable; geography/size-tier aren't yet.
  `operational_maturity`'s v1 limitation: every pain-point signal is weighted equally (no
  per-signal severity field exists on `Signal` to weight by).
- **Lead Scoring**: done against live data (`profiles/scoring.py::compute_lead_score`) --
  evidence-backed 0-100 score with a per-category breakdown (scale, contactability,
  category_fit, qualification, research_signal, freshness, confidence), not an opaque single
  number. `intelligence/scoring.py` (the older MVP referenced here previously) scores the dead
  Phase-1 `entities/` dataclasses that nothing in the live pipeline constructs -- superseded,
  not reused, per `docs/CODE_REVIEW_LESSONS.md` pattern 2 (don't let a second implementation of
  "the same" concept diverge from the live one).
- **Persistent Lead Profiles**: done. `models/profile.py`'s `LeadProfile` (current-state,
  one row per institution) and `LeadScoreSnapshot` (append-only score_history) are kept fresh
  by `services/lead_profile_service.py::refresh_lead_profile`, called from every path that
  changes score-relevant data: `resolution/orchestrator.py::resolve_incoming_record` (all three
  institution-producing branches), `intelligence/researcher.py::research_profile` (new AI
  findings), and `api/routes/manual_leads.py::create_manual_lead`. `qualification/agent.py`'s
  `QualificationAgent` (previously built but never called from any live path) is now wired in
  via `qualify_and_refresh`/`qualify_all_unassessed`, invokable through the `qualify-leads` CLI
  command or the `GET /api/v1/lead-profiles*` read API. Known v1 limitation: `qualify-leads`
  only ever assesses an institution once (no re-assessment policy for institutions whose data
  changed after their first qualification) -- revisiting that is separate follow-up work, not
  silently unhandled.
- **Ranking and Daily Selection**: done. `allocation/eligibility.py` states the eligibility rules
  (institution OPERATIONAL, never DISQUALIFIED, meets a minimum score, has a real contact method)
  and the deterministic ranking key (score desc, institution_id asc tiebreak) in Python;
  `services/daily_selection_service.py::select_daily_batch` implements the same rules again in
  SQL so the claim itself can filter/rank/lock atomically (kept in sync by hand, the same
  documented tradeoff `resolution/blocking.py::_predicted_decision` already accepts for its own
  duplication of `scoring.py`'s decision matrix). `models/allocation.py`'s `LeadReservation`
  claims an institution for a bounded TTL window via `SELECT ... FOR UPDATE SKIP LOCKED` (so two
  overlapping selection runs never claim the same institution), with a partial unique index
  (`WHERE status = 'RESERVED'`) as migration-level defense in depth. Expired reservations release
  automatically on the next `select_daily_batch` call; `mark_consumed`/`release_reservation`
  handle the other two lifecycle transitions. Invokable via the `select-daily-leads` CLI command
  or the `POST/GET /api/v1/daily-selection*` API. Known v1 limitation: nothing yet calls
  `mark_consumed` automatically -- `outreach/automator.py` still works off `OutreachDraft`/
  `AccountBrief`, not `LeadProfile`/`LeadReservation`, so wiring an actual outreach run to consume
  a reservation once it sends is separate, bigger integration work (see the existing
  boundary-conflict note on `outreach/` below), not silently unhandled.
- **Compliance and Source Governance**: done for v1 scope, with one deliberately unresolved
  tension surfaced rather than hidden. `compliance/source_policy.py` is a static, reviewed-by-
  people registry declaring each `SourceType`'s authorization basis -- and it states plainly
  that `SourceType.LINKEDIN` (`sources/linkedin_stealth.py`/`sources/account_farm.py`'s browser
  account automation) is the one source that does NOT meet this repo's own documented standard
  from module 2 above ("unauthorized scraping/account automation is out of bounds"). This module
  does not resolve that contradiction (disabling a relied-upon feature unilaterally is a business
  decision, not a data-model concern) -- it makes the contradiction impossible to miss: printed as
  a banner every time `LinkedInStealthCrawler.run()` actually executes, and queryable via
  `compliance/source_policy.py::contested_sources()`. `compliance/channel_eligibility.py` +
  `models/compliance.py`'s `SuppressionEntry` (optionally scoped to one channel, e.g. opted out of
  email but still callable) implement suppression -- wired as a real gate into
  `outreach/automator.py::run()`, which previously sent to any APPROVED draft with no compliance
  check at all. `DeletionRequest` implements a deliberately two-step right-to-erasure flow
  (`services/compliance_service.py::request_deletion` never deletes anything by itself;
  a separate `fulfill_deletion` call does). `purge_expired_raw_records` is v1's entire retention
  enforcement, narrowly scoped to `RawSourceRecord` rows with no `FieldProvenance` reference at
  all, to avoid corrupting data other live features (confidence scoring, conflict detection)
  still depend on. Invokable via `suppress-contact`/`purge-expired-records` CLI commands or
  `GET/POST /api/v1/compliance/*`. Known v1 limitations: a suppressed `OutreachDraft` stays
  APPROVED forever and is re-checked (and re-released) every automator run rather than moving to
  a dedicated terminal status -- adding one is separate follow-up work, deliberately avoided here
  to not widen `OutreachDraft`'s already carefully-claimed `SENDING`/`SENT` state machine for this
  fix; `consent_evidence` reuses the existing `ContactPoint.is_publicly_listed` flag rather than a
  new tracked field, since that's already the closest signal this codebase records.
- **Verification and Data Quality**: done for v1 scope. `verification/checks.py` states three
  checks as pure functions over already-loaded data: `check_confidence_drift` (does
  `CanonicalInstitution.confidence_score` still match what `verification/confidence.py`'s
  formula would compute from the institution's actual current `branch_membership`
  FieldProvenance count -- catches drift from anything that changes the source count without
  going through `canonical/merger.py`'s own increment), `check_stale_evidence` (no
  FieldProvenance/ResearchFinding recorded within a configurable freshness window), and
  `check_conflicting_canonical_name` (two sources asserting meaningfully different names for
  the same institution after `resolution/normalize.py`'s own `normalize_name` -- v1 scope is
  exact-after-normalization comparison, not fuzzy/trigram similarity). `services/
  verification_service.py::run_verification_checks`/`run_verification_sweep` run these and
  create `DataQualityFlag` rows (the review_queue), deduping against any already-OPEN flag of
  the same type so re-running a sweep doesn't spam duplicates; the sweep savepoint-isolates
  each institution (`docs/CODE_REVIEW_LESSONS.md` pattern 3) so one failing check doesn't
  abort the batch. Invokable via the `verify-data-quality` CLI command or
  `GET/POST /api/v1/verification/*`. Found and fixed a real pre-existing bug in the same pass:
  `CanonicalInstitution.confidence_score` is a 0-100 scale everywhere in `canonical/merger.py`
  (documented there as "an API/UI-facing percentage"), but `api/routes/manual_leads.py` set it
  to `0.7` (a 0-1 fraction -- effectively the *lowest* possible score, the opposite of its own
  "high base confidence" comment) and `profiles/scoring.py` (module 9) thresholded it at
  `>0.8`/`>0.5` (same wrong-scale assumption) -- both fixed, and `merger.py`'s own two inline
  copies of the "+10 per source, capped at 100" formula extracted into
  `verification/confidence.py` as a single source of truth. Known v1 limitations: conflict
  detection only covers `canonical_name` (not every field type); `unreachable_contact_checks`
  has no automated signal source (no email/phone verification API integration exists) and is
  only ever recorded manually via `flag_contact_unreachable`; `source_comparison` isn't a
  separate abstraction, it's what the conflicting-field check already does for the one field
  it covers.
- **Export and Integration**: mostly built. `lead_sync_emitter.py` implements signed delivery;
  `services/outbox_service.py` now sits in front of it (both live call sites route through it)
  giving harvester's side a durable, retried, dead-letterable delivery ledger (see the tracked
  follow-up above) — the still-missing piece is a core-newax-side `event_id`-keyed inbox for
  idempotent replay. `exports/lead_export.py` adds the CSV/JSON export piece: one row per
  `ContactPoint` (the actual contactable unit), carrying its institution's identity/score fields
  (reusing `LeadProfile` rather than recomputing) and an `is_suppressed` flag (reusing
  `services/compliance_service.py`'s suppression lookup) so a downstream consumer can't
  accidentally treat a suppressed contact as safe to message. Invokable via the `export-leads`
  CLI command or `GET /api/v1/exports/leads`. Known v1 limitation: a `ContactPoint` has no direct
  link to a specific `Branch` (contacts are institution-wide in this schema), so branch info is
  summarized per-institution (primary city/country, branch count) rather than joined per-row.
- **Manual Lead Intake**: exists and correctly scoped — `manual_leads.py::create_manual_lead`
  is the one connected, live write path today.
- **Operations and Administration**: done for v1 scope, as a read/aggregate layer over data
  every other module already writes -- no new tables. `services/operations_service.py`:
  `list_source_runs`/`get_source_run_detail` give `job_management` a real read API over the
  existing `SourceRun`/`RawSourceRecord` tables; `compute_source_health` reports each
  `SourceType`'s last run, last success, and 7-day failure count; `list_stranded_records` is
  read-only visibility into exactly the same "stranded" set `pipeline.py`'s
  `_retry_stranded_records` already self-heals every run (reuses its eligibility list directly
  rather than restating it, so the two can't drift), giving `failure_queue` an inspectable view
  without duplicating the retry logic that already exists; `list_audit_log` is the first read
  API over `AuditLog` (previously write-only -- populated by `resolution_service.py`/
  `draft_review_service.py` but nothing ever read it back); `get_sanitized_config` exposes an
  explicit allowlist of `Settings` fields (not a blocklist), so a future secret field can never
  leak through it just because nobody remembered to exclude it; `compute_operational_metrics`
  extends `DashboardService.get_summary` (reused, not recomputed) with outbox/data-quality/
  suppression counts from the modules that landed after the dashboard was built;
  `check_health` is a real check (an actual `SELECT 1`, plus detecting any `SourceRun` stuck in
  `STARTED` past a threshold -- a strong crashed-worker signal) rather than the trivial
  always-"ok" `/api/v1/health`. Invokable via the `ops-health`/`ops-metrics`/
  `ops-source-health` CLI commands or `GET /api/v1/operations/*`. Known v1 limitation: no
  `admin_api` write surface (e.g. manually cancelling a stuck run, editing `job_config`) --
  every endpoint here is read-only by design for this increment.

**Boundary conflict worth a decision, not silently resolved here**: `outreach/` (drafting +
`automator.py`, which sends LinkedIn messages and emails) and LinkedIn-stealth message-sending
capability currently live inside Harvester, but per the Harvester/Engagement-Engine boundary
above, sending and conversation-management belong to the Engagement Engine, not Harvester.
Whether that code moves to a separate service, gets deprecated, or is deliberately kept as an
interim capability until the Engagement Engine exists is an open decision, not resolved by this
document.
