---
name: document-signal-search
description: >-
  Mine Cloverleaf's government MEETING DOCUMENTS — agendas, packets, minutes,
  notices, resolutions — for PROCUREMENT-STAGE buying signals: contract awards,
  renewals, RFP/solicitation releases, budget line items, and named-vendor dollar
  figures, using both semantic (search-documents) and lexical
  (run-document-keyword-search) search. Use this whenever the task is about what a
  jurisdiction is actually BUYING rather than just discussing — e.g. "find RFPs for
  X," "who's renewing a contract," "search agendas/packets for procurement," "any
  cybersecurity contracts on consent agendas," "what's about to be awarded," or
  "find dollar amounts / not-to-exceed items." This is the DOCUMENT-side counterpart
  to `cloverleaf-signal-search` (which mines spoken transcripts): transcripts tell
  you about pain and discussion; documents tell you procurement is in motion. Feeds
  the same downstream skills — `signal-dashboard`, `opportunity-enrichment`,
  `signal-outreach`.
---

# Document Signal Search (procurement-stage signals)

## Why this is its own skill

`cloverleaf-signal-search` mines **spoken transcripts** — what officials *say*. This skill
mines **meeting documents** (agendas, packets, minutes, notices, resolutions) — what a
jurisdiction is *buying*. They are different funnel stages:

- A transcript line ("one ransomware attack and the city is shut down") is **pain** — early,
  pre-RFP, a discussion you can shape.
- A document line ("award a three-year contract to CDW Government LLC for Palo Alto
  enterprise firewall hardware and licensing... not to exceed $4,859,039") is
  **procurement in motion** — a named vendor, a dollar figure, a term length. That is a
  deal closing on a consent agenda, possibly next week.

Run this when the question is about contracts, RFPs, renewals, awards, or budget line items
— the later-funnel signals transcript search can't see. Run both when you want the full
picture of a jurisdiction or territory.

**Availability note:** the connector now works in claude.ai chat, Cowork, and Claude Code
sessions alike.

## Two tools now (verified August 2026)

Tool-level ground truth lives in `cloverleaf-mcp-operations`; load it first. What matters
here:

### `search-documents` (NEW) — semantic, intent-first

Describe the *deal* you're hunting in natural language; it returns documents ranked by
semantic relevance with scored text chunks. This is now the best OPENING move for
procurement sweeps, because it finds award/renewal language without you guessing the
exact vocabulary:

```python
search-documents(
    query    = "contract award or renewal for firewall and network security equipment",
    states   = ["TX"],          # states WORKS now — see below
    daysBack = 90,              # or startDate/endDate — no date = last 7 days only
    perPage  = 10,
)
```

Live-verified catch: that exact query surfaced a DART board packet awarding a 3-year,
not-to-exceed **$4,859,039** Palo Alto firewall contract to CDW-G, plus Williamson
County minutes renewing Palo Alto/Prisma ($106,915.80) and Rubrik backup ($763,202) on
DIR cooperative contracts. Chunks carry per-chunk `score` and a per-document
`best_score` — the ≥0.80-is-strong calibration from meeting search applies here too.

### `run-document-keyword-search` — lexical, exact vocabulary

Use for named vendors, product names, statutes, and rare procurement phrases:

- `terms`: array of keywords/phrases. Multi-word phrases match (e.g. `"managed detection"`,
  `"not to exceed"`). Each result carries per-term `term_frequencies`.
- `daysBack`: integer window. **No date = last 7 days only** — always set it (30–90 for a
  sweep; 180+ if hunting renewal cycles). Or use `startDate`/`endDate` (ISO 8601);
  `daysBack` cannot be combined with them.
- `states`: **FIXED — works now.** (Re-verified August 2026: `["TX"]` returned 186 hits,
  no 500.) Accepts 2-letter codes or full names, US + Canadian provinces; uncovered
  states are rejected with an explicit error. The old "never pass states / post-filter
  nationally" workaround is obsolete — delete it from your muscle memory.
- `page` / `perPage` (max 100): keep `perPage` small (5–10) — document highlights are long
  and big pages blow up context fast.
- `sortBy`: only `"hits"` or `"meeting_date"` (default; anything else silently falls back
  to `meeting_date`). `direction` defaults to `desc`. **`sortBy="hits"` is the fix for
  boilerplate flooding** — it surfaces the documents where your terms actually
  concentrate instead of whatever was published most recently.

Result shape (per hit, August 2026): `organization_id`, `document_type`
(`agenda` | `packet` | `minutes` | `notice`), `meeting_date` (now an ISO string, no
longer epoch ms), `term_frequencies`, `highlights[]` (matched passages with `<mark>`
tags), and `cloverleaf_url` — **the link to cite; never build document links yourself.**
Two things that are NOT in the response: the org name (resolve `organization_id`
yourself before presenting) and the old `docs_count_per_search_term` aggregation
(don't rely on it; calibrate terms by running a cheap `perPage=1` probe and reading
`total_hits` instead).

## Write queries that surface procurement, not boilerplate

The single biggest failure mode: **searching procurement boilerplate alone.** "Request for
proposals" by itself returns thousands of documents — almost all website nav menus and the
standard agenda disclaimer about competitive solicitations, with zero buying substance.

The rule: **search solution- and product-level nouns, not generic procurement words** —
or skip the vocabulary problem entirely by opening with a `search-documents` intent
sentence ("renewal or award of endpoint protection or managed detection services") and
reserving keyword search for named vendors and rare phrases.

**Pattern that works:**
1. **Open with `search-documents`** using a sentence that names the deal type + solution
   area. Rank by `best_score`.
2. **Then go lexical for precision:** specific topic/solution terms on their own
   ("managed detection", "penetration testing", "firewall replacement") — they return
   real line items with vendor names and dollar amounts attached.
3. **Be careful adding procurement words to keyword search — most backfire.** The default
   sort is newest-first, NOT relevance, so a high-frequency procurement word floods the
   top page ("renewal" matches license renewals and building permits; "agreement",
   "award", "resolution" are the same). Two mitigations now exist: use `sortBy="hits"`,
   and/or only add **rare, specific phrases** — `"not to exceed"`, `"request for
   proposals"`, `"sole source"` — never the common ones.
4. **Always filter by `term_frequencies` after results return.** Keep only docs where a
   *solution* term hit; discard docs that matched only a procurement word.

**Procurement-language term bank** — use sparingly, only the rare phrases, and only paired
with topic terms (never solo, never the common ones):
*Safe to pair:* `not to exceed`, `request for proposals`, `request for qualifications`,
`invitation to bid`, `sole source`, `cooperative purchase`, `interlocal`.
*Avoid as terms (too common, will flood the sort):* `renewal`, `agreement`, `award`,
`resolution`, `consent agenda`. Read these as stage signals in the highlight text instead.

**Cyber/IT solution term bank** (the productive nouns — reuse from `cloverleaf-signal-search`
and `vendor-profile/references/term-banks.md`):
`managed detection`, `MDR`, `EDR`, `endpoint protection`, `firewall replacement`,
`penetration testing`, `security operations center`, `SIEM`, `zero trust`,
`multi-factor authentication`, `email security`, `backup and disaster recovery`,
`IT modernization`, `network upgrade`, `body-worn cameras`, `ERP`, `permitting system`.

Translate intent → query. *"Any cyber contracts about to be awarded in the next cycle?"* →
`search-documents(query="upcoming award or renewal of cybersecurity, endpoint, or managed
detection contracts", states=[...], daysBack=90)`, then read the chunks for
award/renewal/not-to-exceed language and keep the hits with real dollar figures.

## Read a document hit — what makes it STRONG

Score procurement signals differently from transcript signals — the value is in the **deal
mechanics**, not the speaker:

1. **A named vendor + a dollar figure + a term length** ("Palo Alto via CDW-G, 3-yr,
   NTE $4,859,039"). This is the jackpot: it names the incumbent, the spend, and the
   renewal horizon — a displacement play with a built-in clock.
2. **Stage language.** "Consideration of an agreement," "renewal," "award," "not to exceed"
   = a decision imminent. "RFP released" / "request for proposals" (with a real scope) = an
   open competition you can still influence. A line item in a proposed budget = next fiscal
   year. Texas closed-session items invoking Gov. Code 551.089 (security devices) or
   551.0761 (cybersecurity deliberations) are a strong "procurement in motion" tell.
3. **`document_type`.** An `agenda` consent/action item is a decision being made *now*;
   `minutes` record the vote that already happened (read for incumbent + renewal-date
   intel); a `packet` carries the detail (scope, dollar amounts, vendor terms); a `notice`
   is often just publication boilerplate — down-weight notices unless they carry scope.
4. **Recency / fiscal timing.** Map `meeting_date` to the jurisdiction's fiscal calendar
   (most local FYs start Jul 1 or Oct 1); budget-season documents are the richest.

**Down-weight:** website navigation menus, the standard "competitive solicitation"
disclaimer, and documents where only the procurement boilerplate term hit (`term_frequencies`
of every solution term = 0). These are noise, not deals.

**Note — documents name vendors, transcripts rarely do.** Officials don't say "CrowdStrike"
out loud, but a packet will print the vendor, reseller, cooperative contract number, and
dollar amount. That makes documents the **best source for incumbent/displacement intel** —
to time a takeout, search the incumbent's product name here and read the renewal date off
the contract item.

## Territory scoping — just pass `states` now

The old workaround section (run nationwide, post-filter by org ID) is retired: `states`
works on both document tools. What remains true:

- State is the finest geographic filter; there is no county/city parameter. For a county
  or single account, resolve `organization_id`s with `lookup-organization` (check the new
  `meeting_count` field to skip empty channels) and filter hits to those IDs.
- Results still carry `organization_id` ONLY — no org name. Resolve the ID before
  presenting (from your territory map, or cross-reference a meeting-side search on the
  same org, whose `meetings[]` array carries `organization_name`, `state`, `city`).

## The legislation angle (NEW)

Procurement is sometimes created by statute before it appears in any agenda. The new
legislation layer (`search-legislation`, `run-legislation-keyword-search`, plus
`get-bill`, `get-bill-documents`, `get-bill-events`, `get-bill-status-changes`) finds
bills that mandate spending — cyber requirements for utilities, modernization funds,
compliance deadlines. Use it to get ahead of the agendas this skill mines: a signed
mandate today is a consent-agenda contract in 6–18 months. Always search with wide
date windows (`daysBack` 180+; the default window is nearly empty), and cite each
bill's `cloverleaf_url` — never legiscan.com. Full recipes in
`cloverleaf-mcp-operations`.

## Drill in

A document hit gives you `organization_id`, `meeting_date`, and `cloverleaf_url` but not
the org name or video. To finish the lead:
- Resolve the org name (territory map, or a meeting-side search on the same org).
- `get-document(documentId)` pulls a single document's fuller content when the
  highlight/chunk isn't enough. (It now also serves legislation documents — those have
  `organization_id: null` and a `bill_id`.)
- To pair the contract with the *discussion* (who championed it, the spoken context), run
  the same solution term through `run-meeting-keyword-search` for that org — now you have
  both the deal and the decision-maker. Then `list-contacts(organizationId)` for email and
  direct phone (transcript results no longer carry contact info inline).

## Hand off

Procurement signals flow into the same downstream chain:

- **`signal-dashboard`** — render the contract/RFP hits into a sortable view (stage, dollar
  amount, vendor, fiscal timing). Link each row's `cloverleaf_url`.
- **`opportunity-enrichment`** — confirm budget, fiscal calendar, and the decision-makers
  behind a contract item via web + Apollo.io.
- **`signal-outreach`** — draft outreach that references the actual line item ("saw the
  Palo Alto renewal coming up on your consent agenda…").
- **`territory-monitor`** — fold this into a recurring sweep so new RFPs and renewals surface
  week over week, not just on a one-off pull.
