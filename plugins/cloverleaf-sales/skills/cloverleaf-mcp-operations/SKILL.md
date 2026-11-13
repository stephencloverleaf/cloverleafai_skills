---
name: cloverleaf-mcp-operations
description: "The verified tool-level reference for the Cloverleaf AI MCP connector: every live tool, its exact parameter names, hard limits, response shapes, and the rules that stop silent failures. Read this before calling any Cloverleaf tool, including one quick search. Triggers on: search Cloverleaf, find signals in government meetings, search meeting transcripts or agendas, look up a jurisdiction, pull a civic contact roster, track a state bill, find contract awards or purchase records, read a budget book or budget line item, pull my signals feed, what parameters does this Cloverleaf tool take, and any Cloverleaf keyword, semantic, document, legislation, purchase, or budget search. It carries the defaults that make results look wrong when you miss them: the 7 day date window, the 100 chunk semantic cap, the 30 day ceiling on state wide semantic search, per user insight scoping, and the spam, duplicate, and jurisdiction filtering the API does not do for you."
---

# Cloverleaf MCP operations reference

This file is the single source of tool-level truth for the Cloverleaf connector.
Workflow skills (`cloverleaf-signal-search`, `document-signal-search`,
`territory-monitor`, `rfp-timeline`, `government-entity-profile`,
`opportunity-enrichment`, `signal-dashboard`, `signal-outreach`, `vendor-profile`,
`demo-mcp`, `police-chief-transitions`) name the tools they use and point here for
parameters. Where a workflow skill disagrees with this file, this file wins.

Verification: the connector exposes 31 tools. On 2026-11-13 every tool was checked
against the server's published parameter schema, and 30 were called live. That pass
replaces the 2026-08-18 and 2026-09-02 passes. `save-signal-to-tasks` writes to the
user's account, so it was checked by schema only. `list-territory-channels` and
`list-salesforce-account-mappings` returned empty lists on the test account, so their
row shapes are unobserved.

## Tool matrix

| Tool | Verified | Job |
|---|---|---|
| `get-signals-feed` | 2026-11-13 | The user's scored signals: insights at or above their score threshold (default 7) from their feed products and campaigns. Numeric `score`, sorted by score, date range on creation time (default 30 days), `perPage` max 25. The first call for "what are my signals". |
| `search-insights` | 2026-11-13 | Every insight the user owns, scored or not, newest first, with a `searchTerm` text filter. Costs no search credit. `limit` defaults to 5 (max 200) with `page`. No date filter. The score exists only as text inside `summary`. |
| `save-signal-to-tasks` | 2026-11-13 (schema only) | Write tool. Saves one feed signal to the user's Cloverleaf Tasks list. Call it only when the user asks. |
| `search-meetings` | 2026-11-13 | Semantic transcript search. Filters: `states`, `cities`, `counties`, `channelTypes`, `organizationIds`. Each excerpt is a 500 character preview with its own deep link. Excerpts carry no speaker. |
| `run-meeting-keyword-search` | 2026-11-13 | Lexical transcript search with anchor terms (`mustIncludeTerms` plus `proximity`). Same filters as `search-meetings`. Real pagination, `perPage` up to 100. |
| `search-documents` | 2026-11-13 | Semantic search over meeting documents. The intent based procurement finder. Adds a `documentTypes` filter (agenda, minutes, packet, notice, budget). |
| `run-document-keyword-search` | 2026-11-13 | Lexical agenda, packet, and minutes search. `sortBy` accepts `hits` or `meeting_date`; any other value is a validation error. |
| `search-purchases` | 2026-11-13 | Semantic search over purchase records. Returned zero rows on every probe on 2026-11-13 while the keyword tool returned rows for the same topics. Use the keyword tool. |
| `run-purchase-keyword-search` | 2026-11-13 | Lexical search over purchase records: federal awards plus local government contract and purchasing datasets. Filters for vendor, department, amount, dataset, state, and organization. |
| `search-legislation` | 2026-11-13 | Semantic search over legislation documents. Returns `bill_id`. `states` is the only geography filter. |
| `run-legislation-keyword-search` | 2026-11-13 | Lexical search over bill texts, amendments, and supplements. |
| `get-bill` | 2026-11-13 | One bill: number, title, status and progress, chamber, session, subjects, sponsors with party and district. |
| `get-bill-documents` | 2026-11-13 | A bill's texts, amendments, fiscal notes, and analyses. Each carries a `meeting_document_id`. |
| `get-bill-events` | 2026-11-13 | Scheduled hearings and floor votes, under the key `calendar_events`. |
| `get-bill-status-changes` | 2026-11-13 | Merged status timeline. Filter `event_kind == "history"` for official changes; `major: true` flags the big moves. |
| `lookup-organization` | 2026-11-13 | Resolve a jurisdiction name to a numeric org id. Returns `meeting_count` and `last_published_at` per match. Embedding ranked, so read the whole list. |
| `list-organization-meetings` | 2026-11-13 | Walk one jurisdiction's meetings newest first. The preferred single entity tool. Returns `total` and `has_more`. |
| `get-meeting` | 2026-11-13 | Metadata, video URL, and `cloverleaf_url` for one meeting id, under the key `meeting`. |
| `get-meeting-transcripts` | 2026-11-13 | Transcript lines for one meeting, paginated (`perPage` up to 500, default 200). Reserved for enrichment on a shortlisted signal, never for discovery. |
| `get-document` | 2026-11-13 | One document by id, full text in `plain_text`. Also serves legislation documents, which carry `organization_id: null` and a `bill_id`. |
| `list-contacts` | 2026-11-13 | Role keyed civic contact roster (name, title, email, phone) by organization or geography. The only path to email and phone. |
| `search-verified-speakers` | 2026-11-13 | People matched to a voice recording: name, organization, title. No email or phone. Use it to check a speaker name. |
| `search-campaigns` | 2026-11-13 | Saved campaigns as search spec templates. Read only, paginated. |
| `list-territory-channels` | 2026-11-13 (empty on test account) | The user's monitored organizations, filterable by name, state id, and source. |
| `list-salesforce-account-mappings` | 2026-11-13 (empty on test account) | Salesforce account to Cloverleaf organization mappings for the user's org. |
| `list-budget-books` | 2026-11-13 | The budget books extracted for one organization. The entry point for every budget tool. |
| `list-budget-departments` | 2026-11-13 | Department keys for one budget book. |
| `list-budget-categories` | 2026-11-13 | Category keys (public safety, information technology, and so on) for one budget book. |
| `budget-rollup` | 2026-11-13 | One book summed by department, category, fund, or division, with a grand total. |
| `search-budget-line-items` | 2026-11-13 | Line items about a topic in one budget book. |
| `get-budget-line-item` | 2026-11-13 | One line item with every printed year and column, plus neighbouring lines. |

## Twelve rules that prevent bad results

1. **Always set a date window.** Meeting, document, and purchase tools default to the
   last 7 days. Legislation tools default to the past 7 days through the next 365 days,
   because bills are future dated. Pass `daysBack`, or `startDate` with optional
   `endDate` (ISO 8601). `daysBack` cannot be combined with `startDate` or `endDate`,
   and `endDate` is rejected without `startDate`. With `startDate` alone, the end
   defaults to 365 days after it or after today, whichever is later. Omitting dates is
   the leading cause of a false "no results": on 2026-11-13 a ransomware legislation
   keyword search returned 1 hit at the default window and 68 at `daysBack = 180`.
2. **Scope geography with the narrowest filter that fits.** `states` works on every
   search tool and takes 2 letter codes or full names for US states, territories, and
   Canadian provinces. The four meeting and document search tools also take `cities`,
   `counties`, `channelTypes`, and `organizationIds`. A city or county filter matches
   every body located there (the school district, the utility, the county), so use
   `organizationIds` to scope to one government. Legislation tools take `states` only.
   Purchase tools take `states` plus integer id filters. An unknown or uncovered place
   returns an explicit error, not an empty result.
3. **Know which counts are true.** All search tools take `page` and `perPage` (max
   100), `search-insights` uses `limit` (max 200), and `get-signals-feed` caps
   `perPage` at 25. A semantic tool returns the top 100 chunks and nothing beyond:
   `total_hits` caps at 100, and `total_meeting_hits` or `total_document_hits` counts
   only the entities inside those chunks. When `total_hits` is 100, read both numbers
   as floors. Keyword tools give true counts: `total_meeting_hits` on meetings (caps
   at 1,000) and `total_hits` on documents, legislation, and purchases.
4. **Cite `cloverleaf_url`, never build a link.** Meetings, documents, insights,
   signals, bills, budget books, and budget lines all carry it. Search excerpts and
   document chunks carry their own `cloverleaf_url` that opens the exact moment or
   chunk, so cite that one for a specific hit. Purchase rows do not carry one, so cite
   an award by `source_row_id`, buyer, vendor, and date. Never construct or cite a
   legiscan.com URL, including the `document_url` on a legislation document. Surface
   `state_url`, `external_url`, or a budget book's `url` only when the user asks for
   the official source.
5. **Filter noise client side, because the API does not.** Drop `is_spam: true` rows,
   `state == "Federal"` rows when federal is out of scope, duplicate uploads of one
   meeting under two ids (dedupe on `organization_id` plus title plus published date,
   never on meeting id alone), duplicate purchase rows filed under two dataset ids,
   and any result naming your own vendor as already contacted, demoed, or quoted.
   `spam_certainty` runs 0.75 to 0.95 on clean meetings, so it is not usable as a
   quality filter. Lexical ambiguity is live: a firewall sweep returns fire rated walls
   and a "firewall show" that is a fireworks show.
6. **Confirm the jurisdiction from content, not from the label.** Org metadata carries
   verified errors at meeting scale and at channel scale (a whole channel filed under a
   neighbouring city's name, a meeting labeled Indiana that is Tasmania). County
   meetings carry `city: null`, and `get-meeting` can return null geography that
   `list-organization-meetings` fills in. Scope by `states` or `organizationIds`, and
   read transcript nouns before you name a jurisdiction to a customer.
7. **`lookup-organization` is embedding ranked, not exact match.** A "Travis County, TX"
   query returns County of Travis first and then 49 other Texas orgs, half with
   `meeting_count: 0`. Read the whole list, skip zero count orgs, and use
   `last_published_at` to spot stale channels. One government often has two org
   records (City of Dallas and Dallas City Council), and meetings, contacts, and budget
   books can sit on different ones, so try the sibling id before reporting a gap. When
   a place name misses, the record is often named for the body ("Victoria City
   Council" rather than "Victoria, MN").
8. **Insights are per user, and an insight is a lead, not a citation.** Results are
   scoped to the authenticated account; pass `userId` to `search-insights` for a
   teammate in the same org. `search-insights` has no date filter and no numeric
   score, and it returns unscored and still generating rows. Use `get-signals-feed`
   when you need a score to sort or filter on. Verified insight defects include an
   invented product category, inverted causality, a dollar figure with no transcript
   antecedent, and a quoted sentence the named speaker never said. Anything going in
   quotation marks comes from a transcript or a keyword hit on raw text, read in
   context.
9. **Speaker attribution is inference.** `get-meeting-transcripts` returns
   `person: null` on most lines, `search-meetings` excerpts carry no `person` block,
   and `run-meeting-keyword-search` populates `person` inconsistently and sometimes
   wrongly with full confidence. The `speakers` array on a semantic meeting hit lists
   people attached to the meeting, not who said the excerpt. A populated field is not
   evidence. Confirm a name against `list-contacts`, `search-verified-speakers`,
   published minutes, or a signature block before it reaches a rep. Sanitize
   `person.organization` and meeting `title` before rendering: both have carried stray
   markup or model deliberation text.
10. **Find the buyer on a purchase row by dataset.** On federal rows
    (`purchase_dataset_id` 1, ids starting `CONT_AWD`) `department` is the buyer, and
    `organization_names` is the whole federal org list (175 ids, 155 names) on every
    row. On local dataset rows `organization_names` is the buyer and `department` is a
    division inside it or null. `amount` can be 0 or null, and `transaction_date` can
    be null. The date window does not track `transaction_date`, so check dates
    yourself.
11. **Keep state wide semantic searches to 30 days.** On 2026-11-13 `search-meetings`,
    `search-documents`, and `search-legislation` returned in seconds at 30 days and
    timed out at 60 seconds on every state wide or nationwide window of 60 days or
    more. A timeout is not an empty result. For a longer range, walk it in 30 day
    slices with `startDate` and `endDate`, or narrow the scope with `organizationIds`,
    `counties`, or `cities`, which returned at 365 days. Keyword tools handled a
    state wide 120 day window without trouble.
12. **Quote budget figures as returned, and label them.** Every budget figure comes
    from one extracted book. Never add lines by hand, and never present a rollup
    `grand_total` as the government's total budget: it did not match the published
    total on the books checked. Department and category assignments are machine made
    and can be wrong. Read `references/budget-tools.md` before the first budget call.

## Reference files

- `references/recipes.md`: exact parameter recipes per tool, with verified behavior and
  score calibration. Read it when you are about to call a tool and need the parameter
  names, or when a call returns fewer results than you expect.
- `references/response-shapes.md`: the top level and per row fields actually returned
  by each search, feed, entity, and contact tool. Read it before you write parsing or
  rendering code, or when you need to know whether a field exists.
- `references/budget-tools.md`: the six budget tools: call sequence, parameters,
  response shapes, coverage, and the accuracy limits found in testing. Read it before
  any budget call.

## Standard plays

1. **Stored intel first.** `get-signals-feed(states)` for scored signals, then
   `search-insights(searchTerm, states)` to text search everything the user owns. Every
   later play assumes this ran. Surface anything scoring 7 or higher that the rep has
   not acted on, skip the 0/10 rows, and apply the guardrails from
   `cloverleaf-signal-search` by hand. Move on only when stored intel is absent, stale,
   or fails those guardrails.
2. **Discovery sweep.** `search-meetings` with a sentence query and `states`, in 30 day
   slices (rule 11), or with `counties` or `organizationIds` and `daysBack` 90 to 180.
   Rank by `best_score`, then `list-contacts(organizationId)` for the top orgs.
3. **Precision or displacement sweep.** `run-meeting-keyword-search` with vendor and
   product `terms`, unambiguous `mustIncludeTerms` such as renew, expire, or replace,
   `proximity` around 50, and `perPage` up to 100.
4. **Procurement sweep.** `search-documents` with an intent sentence, or
   `run-document-keyword-search` with exact terms and `sortBy = "hits"`. Resolve each
   `organization_id`, then pair the document hit with a transcript search on that org
   for the narrative. `document-signal-search` owns this play.
5. **Award and contract check.** `run-purchase-keyword-search`. Federal rows answer who
   won and when. Local rows often carry a contract `end_date`, which is a renewal
   timing signal. `rfp-timeline` owns the backward trace.
6. **Legislation watch.** `run-legislation-keyword-search` at `daysBack` 180 or more,
   or `search-legislation` in 30 day slices, then `get-bill`,
   `get-bill-status-changes` filtered to `major: true`, and `get-bill-events` for
   hearings.
7. **Account deep dive.** `lookup-organization`, then `list-organization-meetings`
   (paginate, optional `title` filter), then a keyword or semantic search scoped with
   `organizationIds`, then `get-meeting-transcripts` for quotes, then
   `list-contacts(organizationId)`. `government-entity-profile` owns this play.
8. **Budget check.** `lookup-organization`, then `list-budget-books`, then
   `search-budget-line-items` for a topic or `budget-rollup` for the shape of the
   spend. About half the organizations tried had a book.
9. **Campaign templating.** `search-campaigns`, then translate a proven spec into live
   parameters by hand. Its geo filters are internal integer ids. State ids resolve to
   names through `facets.states` in `get-signals-feed`.

## Presentation hygiene

- Every signal you show carries org name, state, meeting date, a short verbatim quote,
  the timestamp, and a `cloverleaf_url`. For a specific quote, cite the excerpt's own
  `cloverleaf_url`. On 2026-11-13 excerpt `start_time` matched the transcript line
  exactly on eight of eight samples; the 40 to 65 second drift seen in August did not
  reproduce. If a link opens mid sentence, re-derive the timestamp from the transcript.
- Read a window around a quote, not the quote alone. Semantic excerpts are cut at 500
  characters, and a cut can land right before the clause that disqualifies the claim.
- Flag `already_viewed: true` so a rep knows what they have seen.
- Never present spam or Federal rows to a customer without labeling them.
- Say so explicitly when a contact roster or a budget book list comes back empty, and
  check roster records for a mismatched email domain or title: rosters have mixed two
  governments under one org id and returned out of state contacts.
- Apply Guardrail 0 (own vendor) and the stage filter from `cloverleaf-signal-search`
  before featuring anything. Document, legislation, purchase, and budget hits are later
  stage by nature, so label the stage.
- Cloverleaf covers federal agencies. They are a thinner source than state, county,
  municipal, K-12, higher education, and special districts, because those bodies argue
  in open session repeatedly. Never write that federal is uncovered.
