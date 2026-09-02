---
name: territory-monitor
description: >-
  Run a RECURRING, territory-scoped sweep of Cloverleaf and produce a "what's new
  since last time" digest — the standing habit a rep runs weekly to stay on top of a
  book of business, not a one-off search. Use this whenever the task is about ongoing
  coverage of a territory or account list rather than a single lookup: "what's new in
  my territory," "catch me up on TX this week," "weekly cyber digest for the Carolinas,"
  "monitor these jurisdictions," "anything new since last Monday," or "set up a recurring
  scan." It scopes by state, sweeps both spoken and procurement signals, drops what's
  already been seen, and emits a tight digest plus an updated seen-list for the next run.
  Hands the new signals to `signal-dashboard` and `signal-outreach`.
---

# Territory Monitor (recurring "what's new" sweep)

This is the recurring-sweep mode of the Cloverleaf search engine. The full
mechanics — monitor config, freshness model, dual-layer sweep, and digest format
— live in **`cloverleaf-signal-search` → "Recurring territory sweep (monitor
mode)"**. Use that section; this skill routes you there when the task is standing
territory coverage rather than a one-off search.

The shape in one glance:

1. **Config:** `{ territory, terms, since, seen_meeting_ids, seen_document_ids }`.
2. **Freshness:** date window first (`daysBack` covers `now - since`), then seen-id
   dedup, then `already_viewed` as a soft down-rank only.
3. **Dual sweep:** Layer 1 `run-meeting-keyword-search` (states + terms + window);
   Layer 2 `run-document-keyword-search` (solution terms, and pass `states` — the old
   500 bug is fixed). Walk any watchlist orgs with `list-organization-meetings`.
4. **Output:** a ranked digest + an updated seen-list and `since` date to carry forward.

Apply the three guardrails from `cloverleaf-signal-search` to everything before it
lands in the digest. Hand off to `signal-dashboard` and `signal-outreach`.
