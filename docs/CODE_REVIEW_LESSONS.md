# Engineering lessons from Codex review (PR #1)

This document distills recurring bug classes surfaced by automated (Codex) code review across
the ~18 review rounds of the Entity Resolution / Source Connectors PR. Each pattern below caused
a real, shipped bug at least once in this codebase — usually more than once, in different files,
before the underlying class of mistake was recognized. The goal is to catch these *before*
review next time, not just after.

This is a living document. When a future review round (Codex or human) surfaces a bug that fits
an existing pattern below, add it as another example under that pattern instead of writing a new
one — that's the signal the pattern is real and worth remembering. When it's a genuinely new
class of mistake, add a new pattern.

## 1. Ordering: durable state before permanent-exclusion side effects

**The mistake:** writing an external, hard-to-reverse "this is done" marker (a visited-URL log,
a cookie file, a processed flag) *before* the corresponding database write that the marker is
supposed to represent has actually succeeded. If the DB write then fails, the marker says "done"
forever, and no rerun can recover the work — the marker itself excludes it from ever being
retried.

**Rule:** when an operation has both (a) a durable database write and (b) an external/local
side-effect that some other code path treats as a permanent exclusion (breadth tracker visit
logs, session cookie state, a "processed" file), perform (a) first. Only record the exclusion
once the data it protects is confirmed durable.

**Example:** `sources/account_farm.py::AccountFarm.run()` used to call `_record_farm_visits`
(writes to `breadth_log.json`, which `assign_partitions` treats as a permanent "never visit this
URL again" record) before `_persist_profiles` (writes to `RawSourceRecord`). A transient DB error
during persistence left every scraped profile's URL marked visited but the profile itself never
reached the database — permanently unrecoverable. Fixed in `ce8abe1` by swapping the order.

## 2. Key consistency: the same conceptual value must be derived the same way everywhere

**The mistake:** two different code paths each independently compute what's supposed to be the
same identity/grouping/comparison key, using similar-but-not-identical logic (different fallback
chains, different normalization, different sources for the same "city" concept). They silently
diverge, and a check that depends on both sides matching (a ceiling, a dedup, an exact-match
comparison) becomes permanently inert or wrong.

**Rule:** when a value is used as a key for comparison across two different call sites, compute
it *once* and thread it through, or extract a single shared function — never let a second call
site "reconstruct" the same key from source data using its own fallback logic. If a fallback
chain changes at one call site, grep for every other place that claims to derive "the same" key.

**Examples:**
- `sources/account_farm.py::_record_farm_visits` recorded each visit's "city" from the scraped
  profile's raw free-text location (`"Karachi, Sindh, Pakistan"`), while
  `is_breadth_exceeded()`/`assign_partitions()` compared against the run's declared
  `target_city` (`"karachi"`) — the two never matched, so the 30-day breadth ceiling never
  actually engaged no matter how many profiles were scraped. Fixed in `93ce49e`.
- `sources/authorized_imports.py`'s grouping loop computed an institution's grouping key via a
  website → address → city → row_number fallback chain, but the `source_id` property
  independently recomputed its own signal from `self.website`/`self.address` only — which,
  because those fields get backfilled by a later row *after* grouping, produced a different
  digest than the one the row was actually grouped under. Fixed in `a1aa4d4` by freezing the
  actual key-suffix used at grouping time into a field (`identity_key_suffix`) and having
  `source_id` read that instead of recomputing.

## 3. Batch isolation: one record's failure must not corrupt the whole batch

**The mistake:** processing N independent records inside one shared session/transaction with no
isolation between them. If record 7 of 50 triggers a genuine database-level error (a constraint
violation, a deliberately-invalid query), the whole transaction enters an aborted state and every
subsequent record in the batch fails too, even though nothing about them was wrong.

**Rule:** when a loop processes independent units of work against a shared `AsyncSession`, wrap
each unit's work in its own savepoint (`async with session.begin_nested():`) so a failure rolls
back only that unit, not the surrounding transaction.

**Example:** `intelligence/researcher.py::_research_record` — fixed in `fc2ef7d`.

## 4. Concurrency: claim work atomically, not "check then act"

**The mistake:** a "find pending work, process it" loop that selects candidate rows, then
processes them one at a time without ever locking them for the duration. Two overlapping
invocations of the same job (a cron overlap, a manual rerun while one is still going) each select
the same "pending" rows and do the same work twice.

**Rule:** claim rows with `SELECT ... FOR UPDATE SKIP LOCKED` inside the transaction that will
process them, so a second concurrent claimant skips whatever the first is already holding, and
dedupe within a single call using the item's own stable identity — not the ephemeral row PK the
call happens to touch (see also pattern 6, below).

**Examples:** `outreach/automator.py`'s draft claiming (round 10); `resolution/orchestrator.py`
via `resolve_incoming_record`; `intelligence/researcher.py::process_all_pending` (`8bf3c2c`);
`sources/linkedin_stealth.py`'s daily action-budget reservation (round 14).

## 5. Don't discard partial results on abort

**The mistake:** a loop that scrapes/processes N items, hits an error on item K (a CAPTCHA, a
budget exhaustion, a crash), and re-raises — losing everything already collected for items
`1..K-1` even though that work genuinely succeeded and is safe to keep.

**Rule:** when an in-progress collection loop can abort partway through for a reason unrelated to
the data already collected, attach what's been collected so far to the exception before
re-raising (`e.partial_profiles = results; raise`) so the caller can recover it, rather than
changing the exception's type/message or swallowing the error.

**Example:** `sources/linkedin_stealth.py`'s crawl loop — fixed in `4aaba92`.

## 6. Stable identity, not ordinal position or ephemeral row id

**The mistake:** using a row's position in a list, or its own newly-generated primary key, as the
identity used for deduplication/exclusion across separate runs. A later run with reordered or
appended input, or a record that gets re-scraped into a brand-new row, silently evades the
dedup/exclusion check because the "identity" it's checked against was never actually stable.

**Rule:** derive a stable `source_id` from content that identifies *the real-world thing* (a
profile URL, a normalized name+domain digest) — never from row order or from a freshly-minted
UUID that will differ across every reprocessing of logically the same record.

**Examples:** `sources/authorized_imports.py` (`source_id` from row ordinal → content digest,
round 15); `intelligence/researcher.py` deduping/excluding LinkedIn profiles by profile URL
instead of the raw record's own UUID (round 11, round 14).

## 7. Shared guards belong in one place, used by every path that needs them

**The mistake:** a safety check exists on one write path (e.g. the human-reviewer decision path)
but a second path that can reach the same dangerous state (e.g. an automated auto-merge path)
doesn't call it — usually because the check started life as a private method on a
service class the second path doesn't import, and duplicating the query felt like the easy
option, or got skipped entirely.

**Rule:** when two different entry points can both trigger the same class of unsafe state
transition, extract the guard into a shared, importable location both can call — don't duplicate
the query logic, and don't leave one path unguarded. Check for import cycles before choosing
where the shared function lives; it's fine for it to live in whichever module is lower in the
dependency graph, imported by the other.

**Example:** `_has_other_pending_candidate` existed only in `services/resolution_service.py`
(guarding the human-decision path) until `bc6cb93` moved it into `resolution/orchestrator.py` so
the automated `resolve_incoming_record` auto-merge path could use the identical guard instead of
silently canonicalizing a target that still had its own unresolved conflict.

## 8. Merges and updates must preserve existing state, not overwrite it

**The mistake:** an "attach new evidence" or "update on rerun" code path that only ever writes
fields on first creation, or derives a combined value from a single record instead of every
contributing record — so a second/later write silently drops previously-recorded state instead of
enriching it.

**Rule:** whenever code re-processes an entity that may already have data attached, check what's
already there and merge/enrich rather than assume you're always writing from scratch. This
applies at every layer: a single field on a row (`ContactPoint.person_name`/`role`,
`last_captcha_at` in a cookie payload), a derived value across multiple related rows (an
institution's overall status derived from *all* its branches, not just the one branch being
updated), and whole-entity re-import (an authorized-import row that fills in previously-blank
contact metadata for an institution that already exists).

**Examples:** `canonical/merger.py::_add_contact_if_present` (enrich existing `ContactPoint`
rather than only writing on creation); `canonical/merger.py::attach_record_to_institution`'s
multi-branch status guard (`6bf84fd`); `sources/session_manager.py::save_cookies` preserving
`last_captcha_at` (`f208958`); `pipeline.py`'s authorized-import evidence-merge path (`a242995`,
`200aad4`).

## 9. Multi-process/worker result completeness

**The mistake:** a worker (subprocess, async task) that crashes or times out simply never reports
back, and the aggregation code only ever sees the workers that *did* report — making "every
worker failed" indistinguishable from "there was nothing to report," since both look like an
empty or short result list.

**Rule:** track which units of work were actually dispatched (e.g. every key in the assignment
dict passed to workers), and after collecting results, synthesize an explicit failure entry for
every dispatched unit that never reported back, so downstream code can tell real success from
silent absence.

**Example:** `sources/account_farm.py::_fill_missing_worker_results` (`3757ba9`), feeding
`cli.py`'s exit-code derivation.

## 10. Record risk-mitigating state before attempting the risky action, not after

**The mistake:** a cooldown, rate-limit marker, or budget reservation gets recorded only *after*
an external, fallible action (a CAPTCHA solve attempt, an API call) completes — so a crash,
timeout, or exception during that action skips recording the very state meant to prevent
repeating it too soon.

**Rule:** when an action has a known failure mode that a subsequent retry-too-soon would make
worse, record the cooldown/reservation as soon as the *decision* to attempt the action is made,
before the attempt itself, not after it returns.

**Example:** `sources/linkedin_stealth.py` recording the CAPTCHA cooldown before attempting a
solve rather than after (`5626edf`).

## 11. Every terminal state is terminal, not just the most obvious one

**The mistake:** an immutability/terminal-state check is added for one state in a state machine
(e.g. `SENDING`, an in-flight status) but a later, also-terminal state (`SENT`) is left mutable,
because it was added at a different time or felt like "obviously done" and got overlooked.

**Rule:** when adding an immutability guard for a state machine, enumerate every state that
should be terminal, not just the one prompting the current fix — a status that "obviously"
shouldn't be mutated is exactly the one most likely to be silently missing a guard.

**Example:** `services/draft_review_service.py`/`api/errors.py` — `SENDING` was made immutable to
review mutations first (round 14), `SENT` was still mutable until round 16 (`5626edf`).

## 12. Normalize before you compare, every time a new writer appears

**The mistake:** a normalization step (E.164 phone formatting, domain lowercasing) is applied at
one write path, but a newly added write path (a new connector, an import format) writes the raw
value, so two representations of the same real-world value never dedup against each other.

**Rule:** whenever a new source of a normalized field is added, run it through the same
normalization function the rest of the pipeline already uses before it reaches storage — don't
assume "it'll get normalized somewhere downstream" without checking.

**Example:** `canonical/merger.py::_add_contacts_and_provenance` normalizing authorized-import
phone contacts via the existing `normalize_phone` (`5441bcb`), matching the E.164 normalization
already applied to Google Places phone numbers since round 10.

## 13. Migrations that add required columns must be staged

**The rule (already established, repeated here because it recurred):** adding a `NOT NULL`
column to a table that may already have rows must be staged: add nullable → backfill existing
rows → enforce `NOT NULL` in a later step (or a later revision). A single-step non-null add fails
outright against any non-empty table, in dev, staging, or prod alike.

**Examples:** `branches.city`/`country_code` (round 15); `outreach_drafts.version`/
`resolution_candidates.version` in `b007b9280dac` (`5c9178e`).

## How to use this document

- Before writing code that touches: multi-step external side effects, worker
  pools/subprocesses, dedup/grouping keys, entity merge/update paths, or anything with a
  cooldown/budget/rate-limit — skim the pattern list above first.
- When reviewing a Codex (or human) finding, check whether it matches an existing pattern before
  treating it as a one-off; if it does, the fix should follow that pattern's rule, and this doc
  gets a new example line, not a new section.
- When a genuinely new bug class shows up twice, add a new numbered pattern.
