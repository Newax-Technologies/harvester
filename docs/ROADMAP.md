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

1. **Outbox/retry durability.** `LeadSyncEmitter` is currently fire-and-forget: a failed webhook
   delivery is logged and lost, with no retry. The fix is a persisted delivery ledger in
   harvester (record every attempt, retry with backoff, dead-letter after a threshold) paired
   with an `event_id`-keyed inbox on core-newax's side for idempotent replay. This is the
   "Export and Integration" module's `event_outbox`/`delivery_status` pieces (see module 13
   above) — not yet built.
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
5. **Cross-record person deduplication.** The same real person named on two different
   `contact_point` rows for the same institution currently becomes two separate `CorePerson`
   records in core-newax. No identity resolution across contact points yet — relates to the
   `person_candidate` entity in module 1 above, which doesn't exist yet either.

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

- **Entity Registry**: partial. `models/canonical.py` has institution/branch/contact_point;
  `models/source.py` has source_record. No `person_candidate` (today `contact_point.person_name`
  is a bare string with no resolution state) or `signal` entity yet.
- **Source Connectors**: partial. `sources/` has google_places, web, search, and
  authorized_imports (CSV/bulk import of licensed or manually-sourced data, wired into
  `LeadPipeline`/`cli.py`'s `import-authorized` command, going through the same
  blocking/scoring resolution as every other connector). No apple_maps, yandex_maps, or
  telegram connectors yet.
- **Ingestion**: not modularized as its own layer; scheduling/rate-limiting logic is embedded
  in `pipeline.py`/`sources/web.py` rather than a distinct `ingestion/` module.
- **Normalization**: partial, lives in `resolution/normalize.py` rather than its own module;
  covers phone/domain, not yet a full city/country normalization layer.
- **Resolution**: done for the live ingestion paths. `resolution/orchestrator.py` wires
  blocking + scoring into `pipeline.py` (both Google Places and the web crawler), with a human
  review path for ambiguous (PENDING) matches via the `resolution-reviews` API. See tracked
  follow-up #2 above for the one documented v1 limitation (cross-run concurrency).
- **Enrichment**: partial (`enrichment/website_analyzer.py`); no contact_extractor/
  social_resolver/technology_detector/decision_maker_discovery as distinct pieces yet.
- **Business Intelligence**: partial (`intelligence/pain_detection.py`, `researcher.py`,
  `taxonomy.py`); not fully separated into the 7 planned sub-concerns.
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
- **Compliance and Source Governance**: principles only (README's "Compliance guardrails"),
  not implemented as code.
- **Verification and Data Quality**: doesn't exist as a distinct module.
- **Export and Integration**: partial. `lead_sync_emitter.py` implements signed delivery;
  no durable outbox, no core-side inbox yet (tracked follow-up, not forgotten).
- **Manual Lead Intake**: exists and correctly scoped — `manual_leads.py::create_manual_lead`
  is the one connected, live write path today.
- **Operations and Administration**: partial (`services/dashboard_service.py` and dashboard
  routes); no job_management/source_health/failure_queue as a distinct module.

**Boundary conflict worth a decision, not silently resolved here**: `outreach/` (drafting +
`automator.py`, which sends LinkedIn messages and emails) and LinkedIn-stealth message-sending
capability currently live inside Harvester, but per the Harvester/Engagement-Engine boundary
above, sending and conversation-management belong to the Engagement Engine, not Harvester.
Whether that code moves to a separate service, gets deprecated, or is deliberately kept as an
interim capability until the Engagement Engine exists is an open decision, not resolved by this
document.
