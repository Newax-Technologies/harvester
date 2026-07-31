# Integration contract for Communicator

[Communicator](https://github.com/nadeemmurtaza/Communicator) is a separate
service that turns qualified Harvester leads into multi-channel outreach
(email/SMS/WhatsApp) and handles the resulting conversations. It integrates
with Harvester over this API only — it does not connect to Harvester's
Postgres database directly. Full design: see Communicator's
`docs/ARCHITECTURE.md`.

This doc tracks what Harvester needs to expose so that integration works.

## Already available

- `GET /api/v1/institutions` — paginated list, filterable by `city`
  (`src/lead_harvester/api/routes/institutions.py`).
- `GET /api/v1/institutions/{institution_id}` — full dossier including
  contact points and qualification data.
- `GET /api/v1/drafts` — drafts with `status == GENERATED`; combined with
  `POST /drafts/{id}/decision` this is how a first-touch message gets
  human-approved today.
- Bearer-token auth via `get_current_user` / `require_roles`.

## Needed for Communicator

1. **`qualified` and `updated_since` filters on `GET /api/v1/institutions`**
   so Communicator can do incremental sync of leads that passed
   `QualificationAssessment` without re-pulling the whole table each time.
2. **`POST /api/v1/outreach-outcomes`** — lets Communicator report
   conversation-level engagement (`opened`, `replied`, `positive_reply`,
   `closed_won`/`closed_lost`) back onto the existing `OutreachOutcome`
   model, keyed by the originating `OutreachDraft` (or a new
   `institution_id`-keyed outcome if the conversation didn't start from a
   Harvester draft). Today `OutreachOutcome` rows are only ever created by
   `OutreachAutomator._mark_sent` with all engagement fields defaulted to
   `False` — nothing currently updates them after send.
3. **A dedicated service-role API token** for Communicator, scoped to
   read `institutions`/`drafts` and write `outreach-outcomes` only (not the
   full `reviewer`/`admin` roles used by the dashboard).

## Out of scope for Harvester

SMS/WhatsApp sending, inbound message handling, AI reply generation, and
follow-up scheduling all live in Communicator. Harvester's existing
`OutreachAutomator` (LinkedIn + one-shot email) is not being extended for
this — Communicator's channel adapters supersede it for
email/SMS/WhatsApp going forward.
