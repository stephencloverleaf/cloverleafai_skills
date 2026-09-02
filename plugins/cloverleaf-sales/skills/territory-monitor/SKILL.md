---
name: territory-monitor
description: "Run a recurring, territory scoped sweep of Cloverleaf and produce a what is new since last time digest, the standing habit a rep runs weekly to stay on top of a book of business rather than a one off search. Use whenever the task is ongoing coverage of a territory or account list: what is new in my territory, catch me up on TX this week, weekly cyber digest for the Carolinas, monitor these jurisdictions, anything new since last Monday, or set up a recurring scan. It scopes by state, sweeps insights, spoken signals, and procurement documents, drops what has already been seen, and emits a ranked digest plus the seen list and date to carry into the next run. Hands new signals to signal-dashboard and signal-outreach."
---

# Territory monitor

The recurring form of a Cloverleaf sweep. A one off search answers a question; this
answers "what changed", week after week, without re-surfacing what the rep already
worked.

Tool parameters and limits are in `cloverleaf-mcp-operations`. The guardrails and scoring
that decide what earns a place in the digest are in `cloverleaf-signal-search`; this skill
applies them unchanged rather than restating them.

## Monitor config

Carry this between runs. Ask for anything missing before sweeping, and never default to a
hardcoded geography.

```jsonc
{
  "territory": ["TX", "OK"],
  "terms": ["ransomware", "penetration testing", "security operations center"],
  "watchlist_orgs": [1242, 2908],        // optional named accounts
  "since": "2026-08-26",
  "seen_meeting_ids": [],
  "seen_document_ids": []
}
```

`terms` come from the vendor's term bank. `vendor-profile` produces it, and
`cloverleaf-signal-search/references/query-craft.md` carries the cyber and network banks.

## Freshness, in three layers

1. **Date window first.** Set `daysBack` to cover `now - since`, with a day or two of
   overlap, because ingestion lags the meeting. On the meeting tools you can pass
   `startDate` instead.
2. **Seen id dedupe.** Drop any hit whose meeting or document id is in the seen set. Then
   dedupe what is left on `organization_id` plus title plus published date, because the
   same meeting still appears under two ids.
3. **`already_viewed` as a soft signal only.** It means the rep opened it in the platform,
   not that it was worked. Down-rank, never hard filter.

## The sweep

**Layer 0, insights.** `search-insights(searchTerm, states = territory)`. Free, so it
always runs first. Filter on `created_at` yourself, because the tool has no date
parameter. Skip 0/10 gate excluded rows.

**Layer 1, spoken signals.** `run-meeting-keyword-search` with `terms`, `states`, the
window, and `perPage` up to 100. Paginate rather than narrowing when the first page fills.
Run one vendor term per query when you are sweeping for competitor names.

**Layer 2, procurement.** `run-document-keyword-search` with solution terms, `states`, the
window, `sortBy = "hits"`, and a small `perPage`. This is where renewals and awards
surface. `document-signal-search` owns the vocabulary rules.

**Layer 3, watchlist orgs.** For each org in `watchlist_orgs`, walk
`list-organization-meetings(organizationId)` and keep meetings published after `since`.
Use this walk, not `lookup-organization.last_published_at`, to judge whether a channel has
moved: the org endpoint has reported a newer date than the channel actually held.

Apply the four guardrails from `cloverleaf-signal-search` to everything before it reaches
the digest: own vendor, stage, minimum specificity, and who owns the problem. A recurring
digest is where an unqualified signal does the most damage, because nobody re-reads it.

## Digest format

```
TERRITORY DIGEST | {territory} | new since {since} | run {today}
{N} new signals ({n_hot} hot)

NEW AND NOTABLE (strongest first)
- {Jurisdiction, ST} | {one line on the unsolved problem} | {speaker and role} | {date}
  {cloverleaf_url}

PROCUREMENT MOVES
- {Jurisdiction, ST} | {RFP, renewal, or award, with the dollar figure} | {date}
  {cloverleaf_url}

WATCHLIST
- {Org} | {new meetings since last run, or "no new meetings"}

NOTHING FOUND
- {states or terms that returned zero, and whether that reads as real or as a coverage gap}
```

Keep it short enough to read on a phone. A digest that lists everything is a digest nobody
opens.

Two honesty rules. Say when a state or term returned zero, and say which reading applies:
a legitimately quiet week, a recess (many governing bodies go quiet in August), or thin
coverage on that channel. And check `meeting_count` before promising ongoing coverage on a
jurisdiction; a one meeting channel cannot support a trend.

## Carry forward

Close every run by emitting the state for the next one:

```
--- save for next run ---
seen_meeting_ids:  [... plus everything surfaced this run]
seen_document_ids: [... plus everything surfaced this run]
since: {today}
```

Add ids for everything you surfaced, including what you rejected, so a rejected signal
does not resurface every week.

## Hand off

- `signal-dashboard` renders the digest as a sortable board when the rep wants to triage
  rather than read.
- `opportunity-enrichment` builds out the two or three signals worth working.
- `signal-outreach` drafts the message.
- `rfp-timeline` traces any award that surfaces in the procurement section back to its
  origin.
