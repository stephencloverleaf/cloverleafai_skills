---
name: cloverleaf-mcp-operations
description: "The verified tool-level reference for the Cloverleaf AI MCP connector: every live tool, its exact parameter names, hard limits, response shapes, and the rules that stop silent failures. Read this before calling any Cloverleaf tool, including one quick search. Triggers on: search Cloverleaf, find signals in government meetings, search meeting transcripts or agendas, look up a jurisdiction, pull a civic contact roster, track a state bill, find contract awards or purchase records, what parameters does this Cloverleaf tool take, and any Cloverleaf keyword, semantic, document, legislation, or purchase search. It carries the defaults that make results look wrong when you miss them: the 7 day date window, the 100 chunk semantic cap, per user insight scoping, and the spam, duplicate, and jurisdiction filtering the API does not do for you."
---

# Cloverleaf MCP operations reference

This file is the single source of tool-level truth for the Cloverleaf connector.
Workflow skills (`cloverleaf-signal-search`, `document-signal-search`,
`territory-monitor`, `rfp-timeline`, `government-entity-profile`,
`opportunity-enrichment`, `signal-dashboard`, `signal-outreach`, `vendor-profile`,
`demo-mcp`, `police-chief-transitions`) name the tools they use and point here for
parameters. Where a workflow skill disagrees with this file, this file wins.

Verification dates: the 18 tool pass ran 2026-08-18. The two purchase tools and the
response shapes in `references/response-shapes.md` were verified 2026-09-02.

## Tool matrix

| Tool | Verified | Job |
|---|---|---|
| `search-insights` | 2026-08-18 | Already generated AI insights carrying a Signal Match score. Costs no search credit. Always the first call. Scoped to the authenticated user (pass `userId` for a teammate) and accepts `states`. Also accepts `includeFullResult` (seen 2026-09-02; effect unverified). |
| `search-meetings` | 2026-09-02 | Semantic transcript search. The discovery workhorse when insights are thin. Excerpts carry no speaker block. |
| `run-meeting-keyword-search` | 2026-08-18 | Lexical transcript search with anchor terms (`mustIncludeTerms` plus `proximity`). Real pagination, `perPage` up to 100. |
| `search-documents` | 2026-09-02 | Semantic search over meeting documents. The intent based procurement finder. |
| `run-document-keyword-search` | 2026-08-18 | Lexical agenda, packet, and minutes search. `states` works. `sortBy` accepts `hits` or `meeting_date`. |
| `search-purchases` | 2026-09-02 | Semantic search over contract award records. Dataset 1 is federal awards with USAspending style `CONT_AWD` ids. Award stage, not open solicitations. |
| `run-purchase-keyword-search` | 2026-09-02 | Lexical search over the same award records. `terms` is an array, same shape as the meeting keyword tool. |
| `search-legislation` | 2026-08-18 | Semantic search over state legislation documents. Returns `bill_id`. |
| `run-legislation-keyword-search` | 2026-08-18 | Lexical search over bill texts, amendments, and supplements. |
| `get-bill` | 2026-08-18 | One bill: number, title, status and progress, chamber, session, sponsors with party and district. |
| `get-bill-documents` | 2026-08-18 | A bill's texts, amendments, and supplements. Each carries a `meeting_document_id`. |
| `get-bill-events` | 2026-08-18 | Scheduled hearings and floor votes with date, time, and room. |
| `get-bill-status-changes` | 2026-08-18 | Merged status timeline. Filter `event_kind == "history"` for official changes; `major: true` flags the big moves. |
| `lookup-organization` | 2026-09-02 | Resolve a jurisdiction name to a numeric org id. Returns `meeting_count` and `last_published_at` per match. Embedding ranked, so read the whole list. |
| `list-organization-meetings` | 2026-09-02 | Walk one jurisdiction's meetings newest first. The preferred single entity tool. `organizationId` is a number. |
| `get-meeting` | 2026-08-18 | Metadata, video URL, and `cloverleaf_url` for one meeting id. |
| `get-meeting-transcripts` | 2026-08-18 | Full transcript for one meeting. Large. Reserved for enrichment on a shortlisted signal, never for discovery. |
| `get-document` | 2026-08-18 | One document by id. Also serves legislation documents, which carry `organization_id: null` and a `bill_id`. |
| `list-contacts` | 2026-08-18 | Role keyed civic contact roster (name, title, email, direct phone) by organization or geography. The only contact path. |
| `search-campaigns` | 2026-08-18 | Saved campaigns as search spec templates. Read only, payload arrives inline. |

## Ten rules that prevent bad results

1. **Always set a date window.** Meeting, document, and purchase tools default to the
   last 7 days. Legislation tools default to the past 7 days through the next 365 days,
   because bills are future dated. Pass `daysBack`, or `startDate` with optional
   `endDate` (ISO 8601). You cannot combine `daysBack` with `startDate`. Omitting dates
   is the leading cause of a false "no results": a default window ransomware
   legislation search returned 0, and the same search at `daysBack = 180` returned
   2,256.
2. **Pass `states` on every search.** It works on all search tools, and it validates as an
   array of 2 letter codes or full names covering US states and territories plus Canadian
   provinces. A state with no coverage returns an explicit error rather than an empty
   result. State is the finest geographic filter; there is no county or city parameter.
3. **Pagination is real.** All search tools take `page` and `perPage` (max 100), and
   `search-insights` uses `limit` (max 200). Read the entity count fields, not
   `total_hits`: `total_meeting_hits` and `total_document_hits` are true counts, while
   `total_hits` on a semantic tool counts chunks and caps at 100. Read a `total_hits`
   of 100 as "100 or more".
4. **Cite `cloverleaf_url`, never build a link.** Meetings, documents, insights, and
   bills all carry it. Purchase rows do not, so cite an award by `source_row_id`,
   department, vendor, and date instead. Never construct or cite a legiscan.com URL.
   Surface `state_url` or `external_url` only when the user asks for the official state
   source.
5. **Filter noise client side, because the API does not.** Drop `is_spam: true` rows,
   `state == "Federal"` rows when federal is out of scope, duplicate uploads of one
   meeting under two ids (dedupe on `organization_id` plus title plus published date,
   never on meeting id alone), and any result naming your own vendor as already
   contacted, demoed, or quoted. `spam_certainty` runs 0.8 to 0.95 on clean meetings,
   so it is not usable as a quality filter. Lexical ambiguity is live: a firewall sweep
   returns fire rated walls from zoning boards.
6. **Confirm the jurisdiction from content, not from the label.** Org metadata carries
   verified errors at meeting scale and at channel scale (a whole channel filed under a
   neighbouring city's name, a meeting labeled Indiana that is Tasmania). County
   meetings carry `city: null`, and `get-meeting` can return null geography that
   `list-organization-meetings` fills in. Scope by `states` or `organizationId`, and
   read transcript nouns before you name a jurisdiction to a customer.
7. **`lookup-organization` is embedding ranked, not exact match.** A "Travis County, TX"
   query returns County of Travis first and then dozens of unrelated Texas counties,
   many with `meeting_count: 0` (verified 2026-09-02). Read the whole list, skip zero
   count orgs, and use `last_published_at` to spot stale channels. When a place name
   misses, the record is often named for the body ("Victoria City Council" rather than
   "Victoria, MN").
8. **`search-insights` is per user and has no date filter.** Results are scoped to the
   authenticated account, and each insight carries `creator_email` and `created_at`.
   Pass `userId` to read a teammate's insights in the same org. Filter on `created_at`
   yourself. An insight is a lead, not a citation: verified defects include an invented
   product category, inverted causality, a dollar figure with no transcript antecedent,
   and a quoted sentence the named speaker never said. Anything going in quotation marks
   comes from a transcript or a keyword hit on raw text, read in context.
9. **Speaker attribution is inference from both transcript endpoints.**
   `get-meeting-transcripts` returns `person: null` on most lines, `search-meetings`
   excerpts carry no `person` block at all, and `run-meeting-keyword-search` populates
   `person` inconsistently and sometimes wrongly with full confidence. A populated field
   is not evidence. Confirm a name against `list-contacts`, published minutes, or a
   signature block before it reaches a rep. Sanitize `person.organization` before
   rendering: it has been observed carrying model deliberation text with newline and
   brace characters intact.
10. **On a purchase row, `department` is the buyer, not `organization_names`.** Every row
    in a 2026-09-02 probe carried the same 175 `organization_ids` and 155
    `organization_names` (the whole federal org list), so those fields associate the
    dataset with Cloverleaf orgs rather than identify the awarding body. Present
    `department` with `vendor_name`. `amount` can be 0 on a modification, and
    `start_date` and `end_date` are often null.

## Reference files

- `references/recipes.md`: exact parameter recipes per tool, with verified behavior and
  score calibration. Read it when you are about to call a tool and need the parameter
  names, or when a call returns fewer results than you expect.
- `references/response-shapes.md`: the top level and per row fields actually returned by
  `search-insights`, `search-meetings`, `run-meeting-keyword-search`, `search-documents`,
  `run-document-keyword-search`, `search-purchases`, `lookup-organization`, and
  `list-organization-meetings`. Read it before you write parsing or rendering code, or
  when you need to know whether a field exists.

## Standard plays

1. **Free intel first.** `search-insights(searchTerm, states)`. Every play below assumes
   this ran. Surface anything scoring 7 or higher that the rep has not acted on, skip
   the 0/10 gate excluded rows, and apply the guardrails from `cloverleaf-signal-search`
   by hand. Move on only when insights are absent, stale, or fail those guardrails.
2. **Discovery sweep.** `search-meetings` with a sentence query, `states`, and `daysBack`
   90 to 180. Rank by `best_score`, then `list-contacts(organizationId)` for the top orgs.
3. **Precision or displacement sweep.** `run-meeting-keyword-search` with vendor and
   product `terms`, unambiguous `mustIncludeTerms` such as renew, expire, or replace,
   `proximity` around 50, and `perPage` up to 100.
4. **Procurement sweep.** `search-documents` with an intent sentence, or
   `run-document-keyword-search` with exact terms and `sortBy = "hits"`. Resolve each
   `organization_id`, then pair the document hit with a transcript search on that org for
   the narrative. `document-signal-search` owns this play.
5. **Award check.** `search-purchases` or `run-purchase-keyword-search`. Award stage, so
   it answers who won and when, not what is open. `rfp-timeline` owns the backward trace.
6. **Legislation watch.** `search-legislation` or `run-legislation-keyword-search` at
   `daysBack` 180 or more, then `get-bill`, `get-bill-status-changes` filtered to
   `major: true`, and `get-bill-events` for upcoming hearings.
7. **Account deep dive.** `lookup-organization`, then `list-organization-meetings`
   (paginate, optional `title` filter), then a keyword or semantic search inside what you
   find, then `get-meeting-transcripts` for quotes, then `list-contacts(organizationId)`.
   `government-entity-profile` owns this play.
8. **Campaign templating.** `search-campaigns`, then translate a proven spec into live
   parameters by hand. Its geo filters are internal integer ids that do not map to state
   codes.

## Presentation hygiene

- Every signal you show carries org name, state, meeting date, a short verbatim quote,
  the timestamp, and the `cloverleaf_url`. Re-derive a deep link timestamp from the
  transcript: timestamps taken from a search payload have run 40 to 65 seconds off.
- Read a window around a quote, not the quote alone. Excerpts get spliced across
  timestamps, and a cut can land right before the clause that disqualifies the claim.
- Flag `already_viewed: true` so a rep knows what they have seen.
- Never present spam or Federal rows to a customer without labeling them.
- Say so explicitly when a contact roster comes back empty, and check roster records for
  a mismatched email domain or title: rosters have mixed two governments under one org id
  and returned out of state contacts.
- Apply Guardrail 0 (own vendor) and the stage filter from `cloverleaf-signal-search`
  before featuring anything. Document, legislation, and purchase hits are later stage by
  nature, so label the stage.
- Cloverleaf covers federal agencies. They are a thinner source than state, county,
  municipal, K-12, higher education, and special districts, because those bodies argue in
  open session repeatedly. Never write that federal is uncovered.
