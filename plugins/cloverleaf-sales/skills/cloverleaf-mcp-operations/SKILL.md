---
name: cloverleaf-mcp-operations
description: "Verified operating manual for every tool on the Cloverleaf AI MCP server, live-tested August 2026, covering the new legislation layer (search-legislation, run-legislation-keyword-search, get-bill, get-bill-documents, get-bill-events, get-bill-status-changes), the new search-documents semantic document search, plus exact parameter recipes, hard limits, fixed bugs, and workarounds for the full 18-tool set. ALWAYS consult this before calling ANY Cloverleaf AI MCP tool: keyword or semantic transcript searches, document/agenda searches, legislation and bill tracking, jurisdiction lookups, meeting walks, contact roster pulls, or campaign and insight retrieval. Load it even for a single quick search, because it prevents silent failures (the 7-day default date window, the 100-chunk semantic cap, per-user insight scoping) that make results look wrong or incomplete."
---

# Cloverleaf AI MCP Operations Reference

Verified live on 2026-08-18. Companion to `cloverleaf-signal-search` (search
strategy and signal scoring), `document-signal-search`, `signal-dashboard`,
`opportunity-enrichment`, and `signal-outreach`. This file is the tool-level
ground truth. Where older notes conflict with this file, this file wins.

**What changed since the July 2026 pass** (all re-verified live): the `states`
crash on document search is FIXED; the 25-meeting cap is GONE (real pagination
everywhere); a whole LEGISLATION layer shipped (2 search tools + 4 bill
tools); `search-documents` (semantic) shipped; `search-insights` is now scoped
to the authenticated user and takes `states`; every entity now carries a
`cloverleaf_url` that is the required citation link; date ranges
(`startDate`/`endDate`) and Canadian provinces are supported everywhere.

---

## Tool matrix (20 tools)

| Tool | Status | Job |
|---|---|---|
| `search-insights` | Verified, CHANGED | Already-generated AI insights with Signal Match scores. Free. **Always the first call.** Now scoped to the authenticated user (use `userId` for a teammate's insights); now accepts `states`. |
| `search-meetings` | Verified | Semantic natural-language transcript search. Fallback discovery tool when insights are thin. |
| `run-meeting-keyword-search` | Verified, CHANGED | Lexical transcript search with anchor terms (`mustIncludeTerms` + `proximity`). The old hard 25-meeting cap is gone: `perPage` up to 100 + `page` (verified 30 rows returned). |
| `run-document-keyword-search` | Verified, BUG FIXED | Agenda/packet/procurement text search. `states` now works (verified `["TX"]`, 186 hits, no 500). New `sortBy` (`hits` or `meeting_date`) + `direction`. |
| `search-documents` | NEW, verified | Semantic natural-language search over meeting documents. The intent-based procurement finder (a "contract award or renewal for firewall equipment" query surfaced a $4.86M DART Palo Alto award). |
| `search-legislation` | NEW, verified | Semantic search over state legislation documents. Returns `bill_id` for the bill tools. |
| `run-legislation-keyword-search` | NEW, verified | Lexical search over bill texts, amendments, supplements. |
| `get-bill` | NEW, verified | One bill: number, title, status + progress ("Engrossed"), chamber, session, sponsors with party/district. |
| `get-bill-documents` | NEW, verified | A bill's texts/amendments/supplements; each has a `meeting_document_id` readable via `get-document`. |
| `get-bill-events` | NEW, verified | Scheduled hearings and floor votes (date, time, room). |
| `get-bill-status-changes` | NEW, verified | Merged status timeline; filter `event_kind == "history"` for official status changes; `major: true` flags the big moves. |
| `list-contacts` | Verified | Role-keyed civic contact roster (name, title, email, direct phone) by org or geography. |
| `search-campaigns` | Verified, CHANGED | Saved campaigns as search-spec templates. Returned multiple users' campaigns in our org at test time (30 campaigns across 5 users); payload now arrives inline, not offloaded. |
| `lookup-organization` | Verified, CHANGED | Name → numeric org ID. Now returns `meeting_count` + `last_published_at` per match and a structured no-match result. Still embedding-ranked; read the whole list. |
| `list-organization-meetings` | Verified | Walk one jurisdiction's meetings newest-first. Preferred single-entity tool. |
| `get-meeting` | Verified | Metadata + video URL + `cloverleaf_url` for one meeting ID. |
| `get-meeting-transcripts` | Verified | Full transcript for one meeting. Large. **Reserved for `opportunity-enrichment` on shortlisted signals — not a discovery-phase call.** |
| `get-document` | Verified | One document by ID. Now also serves legislation documents (those have `organization_id: null` and a `bill_id`). |
| `search-purchases` | New since 2026-08-18 snapshot (seen 2026-09-02) | Semantic search over purchase and contract-award records. `purchase_dataset_id` 1 is federal contract awards with USAspending-style `CONT_AWD` ids; records carry `amount`, `vendor_name`, `department`, `purchase_description`, `transaction_date`, and `organization_ids`. Params: `query`, `daysBack`, `page`, `perPage` (numbers). Returns `total_hits`, `page`, `per_page`, `purchases[]`. |
| `run-purchase-keyword-search` | New since 2026-08-18 snapshot (seen 2026-09-02) | Lexical keyword search over the same purchase records. `terms` must be an array (same shape as `run-meeting-keyword-search`). The server did not publish a parameter schema as of 2026-09-02. |

**New since the 2026-08-18 verification pass:** the two purchases tools listed at the end of
the matrix appeared on the connector by 2026-09-02. No workflow skill uses them yet. The
obvious candidates are `document-signal-search` (award and renewal evidence) and
`rfp-timeline` (tracing an award back through its history). Verify the parameters live before
building either play on them.

---

## Eight rules that prevent bad results (all verified 2026-08-18)

1. **Always set a date window.** Meeting and document tools silently default
   to the last 7 days. Legislation tools default to the past 7 days through
   the NEXT 365 days (bills are future-dated). You now have two options:
   `daysBack`, OR `startDate`/`endDate` (ISO 8601; `endDate` requires
   `startDate`). `daysBack` cannot be combined with `startDate`/`endDate`.
   Omitting dates is still the number one cause of "no results" — a
   default-window `ransomware` legislation search returned 0; the same search
   with `daysBack = 180` returned 2,256.
2. **`states` now works on EVERY search tool** — the old
   `run-document-keyword-search` 500 is fixed (re-verified with `["TX"]`).
   Accepts 2-letter codes or full names, US states/territories AND Canadian
   provinces. States without coverage are rejected with an explicit error, not
   a silent empty result.
3. **Pagination is real now; the 25-meeting cap is gone.** All search tools
   take `page` + `perPage` (max 100; `search-insights` uses `limit`, max 200).
   Verified 30 meetings returned in one keyword-search call. Note the
   entity-count fields: `total_meeting_hits` / `total_document_hits` are the
   true entity counts; on the SEMANTIC tools `total_hits` (chunk count) caps
   at 100 — read "100" as "100+".
4. **Cite `cloverleaf_url`, never build links yourself.** Every meeting,
   document, insight, and bill now carries `cloverleaf_url` — that is the link
   to give users. NEVER construct or cite legiscan.com URLs. Only surface
   `state_url`/`external_url` when the user explicitly asks for the official
   state source. (This is a server-level instruction; treat it as policy.)
5. **Filter noise client-side. The API still does not.** Drop four things
   before presenting: (a) `is_spam: true` rows, (b) `state == "Federal"` rows
   unless federal is in scope, (c) duplicate uploads — the same meeting still
   appears under two meeting IDs (re-verified: Carroll ISD workshop, Navasota
   ZBA); dedupe on `organization_id` + title + published date, never on
   meeting ID alone — and (d) any result naming our own vendor as already
   contacted, demoed, or quoted (see `cloverleaf-signal-search` Guardrail 0).
   Lexical ambiguity is also alive and well: a "firewall" keyword sweep
   returned building firewalls from planning/zoning and a "firewall town
   center" in Garland. Meeting metadata now includes `spam_certainty` and
   `user_marked_spam` alongside `is_spam`; judge borderline rows by content.
6. **City metadata is still spotty.** County-level meetings carry
   `city: null`. Scope by `states` or `organizationId`; never rely on city
   fields for filtering.
7. **`lookup-organization` is embedding-ranked, not exact-match.**
   Re-verified: "Las Vegas, NV" returned Las Vegas City Council 9th of 13.
   Read the full list before choosing. NEW: each match now carries
   `meeting_count` and `last_published_at` — skip orgs with
   `meeting_count: 0` (no ingested meetings) before wasting calls, and use
   `last_published_at` to spot stale channels.
8. **`search-insights` is per-user now.** Results are scoped to the
   authenticated account (each insight carries `creator_email`); the old
   org-wide counts are gone. Pass `userId` to read a teammate's insights
   (same org only). No date filter exists on this tool — filter on
   `created_at` client-side.

---

## search-insights — free intel, the mandatory opening move

Returns AI insights ALREADY generated for the account (the "Sales Insights"
prompt runs on an automated cadence). Each record: full markdown `result`, a
`summary` with a "Signal Match: X/10" score, `organization_name`,
`state_name`/`county_name`/`city_name`, `meeting_id`, `creator_email`,
`created_at`, and `cloverleaf_url` (links to the meeting's insights page).

```python
search-insights(searchTerm = "cyber", limit = 20)                    # user-scoped
search-insights(searchTerm = "cyber", states = ["FL"], limit = 20)   # territory filter (verified)
search-insights(searchTerm = "cyber", userId = 12020)                # a teammate's insights
```

Rule: ALWAYS query this before running any keyword or semantic transcript
sweep. It costs nothing, prevents duplicate credit spend on meetings the
account has already analyzed, and is the fastest "what scored 7+ this week"
digest. Insights generate nationwide, so territory reps should always pass
`states`. It is not pre-filtered for our rules — every result still needs the
stage filter and the own-vendor guardrail from `cloverleaf-signal-search`
applied by hand. A high Signal Match score says nothing about whether the
named vendor is us, and the automated prompt applies ITS creator's relevance
gate, not necessarily yours (0/10 "gate excluded" rows are common — skip
them, don't re-litigate them).

---

## search-meetings (semantic) — the fallback discovery workhorse

Use when `search-insights` comes up thin and the target is an INTENT or
SITUATION rather than an exact phrase. Write the query as a full sentence
describing the buyer's situation, the way an official would live it.

```python
search-meetings(
    query    = "city or county asking for money to replace old firewalls or aging network equipment",
    states   = ["TX"],
    daysBack = 120,          # or startDate/endDate
    perPage  = 10,           # default 20, max 100; page for more
)
```

Verified behavior (2026-08-18):
- Excellent intent matching: the query above surfaced a Harlingen budget
  workshop covering pen-testing, Windows 10 EOL replacements, and aging
  network switches — mostly zero keyword overlap.
- Transcript hits are now multi-paragraph CHUNKS (IDs like `20204912-12`),
  each with a `score`, plus a per-meeting `best_score`. Calibration still
  holds: treat >= 0.80 as strong; read 0.75–0.80 before trusting it.
- No spam or federal filtering happens server-side. Apply Rule 5.
- Response shape: `meeting_hits[]` (chunked excerpts, scores, `best_score`,
  `already_viewed`) plus a parallel `meetings[]` metadata array
  (`organization_name`, `organization_id`, state, county, city,
  `cloverleaf_url`, `source_video_url`, `published_at`, `duration_seconds`,
  `is_spam`, `spam_certainty`, `user_marked_spam`, `thumbnail_url`). Join the
  two on `id`.
- `total_hits` caps at 100 (Rule 3); `total_meeting_hits` is the real
  meeting count.

---

## run-meeting-keyword-search — the precision and anchors tool

Use when you need exact, unambiguous vocabulary: vendor names, product names,
statutes, grant programs. `terms` are OR'd. `mustIncludeTerms` + `proximity`
require a search term to appear near an anchor term.

```python
run-meeting-keyword-search(
    terms            = ["Fortinet", "FortiGate", "firewall"],
    mustIncludeTerms = ["renew", "expire", "replace"],
    proximity        = 50,
    states           = ["TX", "OK"],
    daysBack         = 120,
    perPage          = 50,     # max 100; page for more — the 25 cap is gone
)
```

Verified behavior (2026-08-18):
- The 25-meeting cap is GONE. `perPage` up to 100 with `page` pagination
  (30 rows verified in one call). `total_meeting_hits` is the true count.
- Anchoring is LEXICAL co-occurrence, not semantic. Ambiguous anchors and
  terms still create false positives (building firewalls from zoning boards,
  a "firewall town center"). Anchor only with unambiguous words (vendor
  names, "ransomware", "SCADA"). For fuzzy intent, use `search-meetings`.
- `proximity` units are undocumented; 30–50 behaved as a loose window (the
  org's saved campaigns use 30–180).
- Results now include a full `meetings[]` metadata array (same shape as
  `search-meetings`, with `organization_name` and `cloverleaf_url`) — no more
  ID-only responses.
- CHANGED: the per-line `person` block is now `{name, organization, title}`
  only — email/phone are NO LONGER returned inline. Pull contact info with
  `list-contacts(organizationId)` instead.
- Speaker attribution quality varies; many lines have `person: null`.

---

## The document layer — search-documents (semantic) + run-document-keyword-search (lexical)

Transcripts show pain; documents show money moving. Use these for
procurement-stage evidence: contract awards, renewals, dollar line items, RFP
language, closed-session items. Real captures from the August pass: a DART
board packet awarding a 3-year, not-to-exceed **$4,859,039** Palo Alto
firewall contract to CDW-G, and Williamson County minutes renewing Palo
Alto/Prisma ($106,915.80) and Rubrik backup ($763,202) via DIR cooperative
contracts.

```python
search-documents(                       # NEW — intent-based
    query    = "contract award or renewal for firewall and network security equipment",
    states   = ["TX"],                  # works
    daysBack = 90,
    perPage  = 10,
)

run-document-keyword-search(            # lexical — exact vocabulary
    terms    = ["firewall", "network security", "cybersecurity"],
    states   = ["TX"],                  # FIXED — no longer 500s (verified)
    daysBack = 90,
    perPage  = 10,
    sortBy   = "hits",                  # or "meeting_date" (default); anything else silently falls back
)
```

Verified behavior:
- Both accept `states` normally now. The July "never pass states" rule is
  obsolete.
- `search-documents` response: `documents[]` with `chunks[]` (large text
  blocks + per-chunk `score`), `best_score`, `document_type` (agenda, packet,
  minutes), `meeting_date` (ISO), `cloverleaf_url`, and `organization_id`
  ONLY. `run-document-keyword-search` returns `highlights[]` with `<mark>`
  tags and `term_frequencies` per hit.
- Neither returns an org NAME — resolve `organization_id` yourself before
  presenting (via a meeting search on that org or `lookup-organization`).
- The old `docs_count_per_search_term` keyword-calibration aggregation did
  not appear in the August responses; don't rely on it.
- `meeting_date` is now an ISO string (was epoch ms); `created_at` is still
  epoch ms.

---

## The legislation layer (NEW) — bills as signals

Two search tools find legislation documents; four bill tools build the story.
The seller's use: track mandates that create budgets (cyber requirements for
utilities, modernization funds), watch hearings where agencies testify about
needs, and time outreach to statutory deadlines.

```python
search-legislation(                     # semantic
    query    = "cybersecurity requirements for critical infrastructure and utilities",
    daysBack = 180,                     # ALWAYS widen — default window is thin
    perPage  = 10,
)
run-legislation-keyword-search(         # lexical
    terms    = ["ransomware", "cyber incident reporting"],
    daysBack = 180,
)
```

Verified behavior:
- Date default is past 7 days through NEXT 365 days (calendar events are
  future-dated). In practice the default window is thin — 0 hits at default
  vs 2,256 at `daysBack = 180` for "cybersecurity". Always pass a wide
  window.
- Zero results for a state are often legitimate session-calendar gaps
  (biennial legislatures like Texas don't sit in even years). Widen dates and
  check the session before concluding "no coverage."
- Results carry `bill_id` (feed the four bill tools), `meeting_document_id`
  (feed `get-document` for full text), `document_type`, `ls_entity_type`,
  and `cloverleaf_url` (`app.cloverleaf.ai/legislation/...`). Older documents
  may lack `bill_id` — read the text via `get-document` to find it.
- `get-bill(billId)` → identity, status + `status_progress` (e.g.
  "Engrossed"), state, session, originating chamber, pending committee, and
  full sponsor list with party/district. `cloverleaf_url` can be null (no
  viewable page yet — say so, don't invent a link).
- `get-bill-status-changes(billId)` → one merged timeline; entries with
  `event_kind: "history"` are official status changes, `"calendar"` are
  hearings; `major: true` marks committee passage and floor votes.
- `get-bill-events(billId)` → upcoming/past hearings with date, time, room.
- `get-bill-documents(billId)` → Introduced/Amended versions with dates;
  read any version's full text via
  `get-document(documentId = meeting_document_id)`.
- Rule 4 applies hardest here: cite `cloverleaf_url`, NEVER legiscan.com;
  `state_url` only if the user explicitly asks for the official source.

---

## list-contacts — who to call

Role-keyed civic roster: Top Appointed Executive, Top Elected Official,
Governing Board Member, Head of IT, Head of Finance, Head of Purchasing, and
more. Each contact: name, title, role, email, phone (often direct), org, and
county FIPS/lat/long.

```python
list-contacts(organizationId = 1247, limit = 25)   # org ID from the signal
```

Verified behavior:
- Signal-to-buyer in two calls still works: the Hunt County firewall signal
  chained straight to the County Judge's direct line.
- Pass `organizationId` from the signal. `stateName`/`countyName`/`cityName`
  filters return ALPHABETICAL rosters, not signal-ranked; use them only for
  deliberate area-wide sweeps.
- Coverage is uneven: incorporated cities and counties are strong; special
  districts and utilities can return empty. When a roster is empty, SAY SO
  rather than skipping the org silently.
- Small orgs share inboxes across officials (all four Hunt County
  commissioners list `commissioner@huntcounty.net`) — dedupe by email and
  prefer the named-title contact when drafting outreach.
- This roster is separate from transcript speaker attribution;
  cross-reference both when a named speaker matters.

---

## search-campaigns — the saved-search template library (read-only)

Returns saved campaigns with their full search specs. At the August test it
returned 30 campaigns spanning five different users in our org, inline (no
file offload) — treat visibility as "your org's campaigns as exposed to your
account," and don't assume you're seeing every user's.

Each campaign: `searchTerms`, `mustIncludeTerms`, `exclude`, `proximity`, and
`filterParams` (`cities`/`counties`/`states`/`organizations` as internal
INTEGER IDs — not 2-letter codes — plus `channel_types`, `countries` (new,
e.g. `["US"]`), income/population ranges where `[-1, -1]` means unset,
`voice_ids`, `title_search_terms`, `organization_search_terms`, `person_ids`,
`user_ids`).

Use it as a template library: find a proven campaign, then translate its spec
into live search parameters by hand (integer geo IDs do not map to state
codes automatically). Campaigns named "Smart Search"/"SS" have EMPTY
`searchTerms` — they're semantic campaigns; adapt those into
`search-meetings` sentence queries instead of keyword lists. Beware corrupted
specs (searchTerms of `"0","1","2"...` were observed) — sanity-check before
copying. No create or update tool is exposed; campaign writes still happen in
the platform UI.

---

## lookup-organization and single-entity walks

- Combined query form verified: `lookup-organization(query = "Las Vegas, NV")`
  splits on the last comma; `name` + `state` also works; full names and
  2-letter codes both accepted, Canadian provinces included. Apply Rule 7 and
  read the whole list.
- NEW response shape: `{matched, organizations[], state}` where each org has
  `id`, `name`, `meeting_count`, `last_published_at`. Skip
  `meeting_count: 0` orgs; a structured no-match result distinguishes unknown
  state / no coverage / no name match.
- `list-organization-meetings(organizationId, perPage <= 100, title = "budget")`
  is the preferred single-entity walk: newest-first, optional case-insensitive
  title substring filter, NO date filter (paginate instead).
- `get-meeting-transcripts` returns transcript lines ordered by `start_time`
  with speaker info where known. Large payloads; pull only for context around
  a specific quote — during `opportunity-enrichment` on shortlisted signals,
  not during discovery.
- Watch for mis-attributed channels: a "Sealy City Council" meeting was filed
  under County of Austin's org. Verify org names against meeting titles
  before presenting.

---

## Standard plays

**1. Free intel first — always the opening move; every play below assumes this ran**
`search-insights(searchTerm = topic or vendor, states = territory)`. Surface
anything 7/10+ the rep hasn't acted on; skip 0/10 gate-excluded rows. Every
result still needs the stage filter and own-vendor guardrail from
`cloverleaf-signal-search` applied manually. Only move to plays 2–5 when
insights are absent, stale, or don't clear the guardrails.

**2. Discovery sweep (net-new pipeline)**
`search-meetings` with a sentence query, `states`, `daysBack` 90–180. Apply
Rule 5 (spam, Federal, dupes, own-vendor). Rank by `best_score`. For the top
orgs, call `list-contacts(organizationId)`. Hand off to `signal-dashboard` /
`signal-outreach`.

**3. Precision or competitor-displacement sweep**
`run-meeting-keyword-search` with vendor/product `terms`, unambiguous
`mustIncludeTerms` ("renew", "expire", "replace"), `proximity` ~50, `states`,
`daysBack`, `perPage` up to 100. Paginate freely — the cap is gone.

**4. Procurement sweep**
`search-documents` with an intent sentence, or `run-document-keyword-search`
with exact terms — both WITH `states` now — `daysBack` 60–120,
`sortBy = "hits"` when you want signal-dense documents first. Resolve
`organization_id`s, then pair each document hit with a transcript search on
that org for the narrative.

**5. Legislation watch (NEW)**
`search-legislation` / `run-legislation-keyword-search` with `daysBack` 180+,
then `get-bill` → `get-bill-status-changes` (filter `major: true`) →
`get-bill-events` for upcoming hearings. Sell against mandates and funding
programs the bill creates; time outreach to hearing dates and effective
dates.

**6. Account deep-dive (the "show me everything on City X" ask)**
`lookup-organization` (read the full list, check `meeting_count`) →
`list-organization-meetings` (paginate; optional `title` filter) → keyword or
semantic search within what you find → `get-meeting-transcripts` for quotes →
`list-contacts(organizationId)` for the roster. Enrich via
`opportunity-enrichment`.

**7. Campaign templating**
`search-campaigns`, filter names and terms for the vertical, adapt keyword
specs into `run-meeting-keyword-search` and "Smart Search" specs into
`search-meetings` sentence queries.

---

## Presentation hygiene

- Every signal presented to a rep or customer carries: org name, state,
  meeting date, a short verbatim quote, the timestamp, and the
  `cloverleaf_url` as the link (pair `start_time` seconds with
  `source_video_url` only when deep-linking the exact video moment).
- NEVER cite or construct legiscan.com URLs for legislation;
  `state_url`/`external_url` only when the user explicitly asks for the
  official state source.
- Flag `already_viewed: true` so reps know what they have seen.
- Never present spam or Federal rows to a customer without labeling them.
- State explicitly when a contact roster is empty for an org.
- Apply the pain-vs-procurement stage filter from `cloverleaf-signal-search`
  before featuring anything: early-stage spoken pain is the product;
  already-issued RFPs and awarded contracts are late-stage and available
  elsewhere. (Document and legislation hits are usually later-stage by
  nature — label the stage.)
- Apply Guardrail 0 from `cloverleaf-signal-search` before that: reject
  outright anything where our own vendor is already named as contacted,
  demoed, or quoted — that's a live deal, not a discovery, regardless of how
  well it would otherwise score.
