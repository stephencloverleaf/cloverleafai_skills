---
name: document-signal-search
description: "Mine Cloverleaf's meeting documents, state legislation, and federal award records for procurement stage buying signals: contract awards, renewals, RFP and solicitation releases, budget line items, named vendor dollar figures, and statutory mandates that create budgets. Use whenever the task is about what a jurisdiction is buying rather than what it is discussing, for example find RFPs for X, who is renewing a contract, search agendas or packets for procurement, any cybersecurity contracts on consent agendas, what is about to be awarded, find dollar amounts or not to exceed items, who won this federal contract, or what law is about to force this spend. This is the document side counterpart to cloverleaf-signal-search, which mines spoken transcripts. Feeds signal-dashboard, opportunity-enrichment, and signal-outreach."
---

# Document signal search

## What each source covers

`cloverleaf-signal-search` mines what officials say. This skill mines what they file and
what they sign. Pick the source by the stage you want, and label the stage on everything
you present.

| Source | Tools | Stage it covers |
|---|---|---|
| Legislation | `search-legislation`, `run-legislation-keyword-search`, `get-bill`, `get-bill-documents`, `get-bill-events`, `get-bill-status-changes` | Upstream mandate. A requirement or fund created before any agenda item exists. |
| Meeting documents | `search-documents`, `run-document-keyword-search`, `get-document` | Budget line item through solicitation, award, and renewal. The core of this skill. |
| Federal awards | `search-purchases`, `run-purchase-keyword-search` | Award already made. Who won, for how much, when. |

A transcript line ("one ransomware attack and the city is shut down") is pain. A document
line ("award a three year contract to CDW Government LLC for Palo Alto enterprise
firewall hardware and licensing, not to exceed $4,859,039") is procurement in motion: a
named vendor, a dollar figure, and a term length, closing on a consent agenda. Run both
sides when you want the full picture of a jurisdiction.

Parameters, limits, and response shapes are in `cloverleaf-mcp-operations`. Load it first.

## Procedure

1. **Open semantically.** `search-documents` with a sentence naming the deal type and the
   solution area, plus `states` and `daysBack` 60 to 120. This finds award and renewal
   language without you guessing the vocabulary. Rank by `best_score`.
2. **Go lexical for precision.** `run-document-keyword-search` with named vendors, product
   names, and rare procurement phrases. Set `sortBy = "hits"` so signal dense documents
   outrank whatever was published most recently.
3. **Filter on `term_frequencies`.** Keep only documents where a solution term hit. Discard
   anything that matched a procurement word alone.
4. **Resolve `organization_id` to a name** before presenting. Neither document tool returns
   one.
5. **Pair the document with the discussion.** Run the same solution term through
   `run-meeting-keyword-search` on that org to find who championed it, then
   `list-contacts(organizationId)` for email and direct phone.

Read `references/procurement-vocabulary.md` for the solution term banks, the procurement
phrases that are safe to pair, and the ones that flood a sort. It is the difference
between real line items and a page of website navigation menus.

## Score a document hit on deal mechanics

The value here is in the contract, not the speaker.

1. **A named vendor plus a dollar figure plus a term length.** "Palo Alto via CDW-G, 3
   year, not to exceed $4,859,039" names the incumbent, the spend, and the renewal
   horizon. That is a displacement play with a built in clock.
2. **Stage language.** "Consideration of an agreement", "renewal", "award", "not to
   exceed" means a decision is imminent. A real scope under "request for proposals" means
   an open competition you can still influence. A line item in a proposed budget means
   next fiscal year. Texas closed session items citing Government Code 551.089 (security
   devices) or 551.0761 (cybersecurity deliberations) are a strong procurement in motion
   tell.
3. **`document_type`.** An `agenda` consent or action item is a decision being made now.
   `minutes` record a vote that already happened, which is where incumbent and renewal
   date intel lives. A `packet` carries the scope, dollar amounts, and vendor terms. A
   `notice` is often publication boilerplate, so down-weight it unless it carries scope.
4. **Fiscal timing.** Map `meeting_date` to the jurisdiction's fiscal calendar; most local
   fiscal years start 1 July or 1 October, and budget season documents are the richest.

Down-weight website navigation menus, the standard competitive solicitation disclaimer,
and any document where every solution term scored 0.

**Documents name vendors, transcripts rarely do.** Officials do not say a security
vendor's name out loud, but a packet prints the vendor, the reseller, the cooperative
contract number, and the amount. That makes documents the best source for incumbent and
displacement intel: search the incumbent's product name here and read the renewal date off
the contract item.

## The federal awards layer

`search-purchases` (semantic) and `run-purchase-keyword-search` (lexical) search contract
award records. Verified 2026-09-02 against a live probe.

- Dataset 1 is federal contract awards with USAspending style `CONT_AWD` ids. Rows carry
  `amount`, `vendor_name`, `department`, `purchase_description`, `transaction_date`, and
  `source_row_id`.
- **Award stage, not open solicitations.** These tools answer who won and for how much.
  They do not list what is currently biddable, so never present a purchase row as an open
  opportunity.
- **Coverage beyond federal is unverified as of 2026-09-02.** Every sampled row was a
  federal department. Do not tell a customer this layer covers state or local awards
  until someone has confirmed it.
- **`department` is the buyer.** `organization_ids` and `organization_names` came back
  identical on every row (the whole federal org list), so they associate the dataset with
  Cloverleaf orgs rather than identify the awarding body.
- **No `cloverleaf_url` on a purchase row.** Cite the award by `source_row_id`,
  `department`, `vendor_name`, and `transaction_date` instead of building a link.
- `amount` can be 0 on a contract modification, and `start_date` and `end_date` were null
  on every sampled row.

Use it for displacement research on a federal target, for confirming who holds an
incumbent contract, and as the award anchor `rfp-timeline` traces backward from.

## The legislation layer

Procurement is sometimes created by statute before it reaches any agenda. A signed
mandate today is a consent agenda contract in 6 to 18 months, so use this layer to get
ahead of the documents this skill mines.

Search with `daysBack` 180 or more; the default window runs the past 7 days through the
next 365 and is nearly empty in practice. Zero results for a state are often a session
calendar gap rather than missing coverage, because biennial legislatures do not sit every
year. Cite each bill's `cloverleaf_url` and never a legiscan.com URL. Recipes are in
`cloverleaf-mcp-operations`.

## Territory scoping

Pass `states`; it works on both document tools and validates on `search-purchases`. State
is the finest geographic filter, and there is no county or city parameter. For a county or
a single account, resolve `organization_id`s with `lookup-organization` (skip orgs with
`meeting_count: 0`) and filter hits to that set.

Results carry `organization_id` only. Resolve the name from your territory map, or cross
reference a meeting side search on the same org, whose `meetings[]` array carries
`organization_name`, `state`, and `city`.

## Drill in

- `get-document(documentId)` pulls fuller content when the highlight or chunk is not
  enough. It also serves legislation documents, which carry `organization_id: null` and a
  `bill_id`.
- Cite `cloverleaf_url` on every document hit. Never build a document link yourself.
- Score calibration on documents runs lower than on transcripts. In a 2026-09-02 probe the
  top hit for a well formed procurement query scored 0.785 and was a real Fortinet award
  to CDW-G not to exceed $150,750. Read documents from about 0.75 up and rank by
  `best_score`.

## Hand off

- `signal-dashboard` renders contract and RFP hits into a sortable view by stage, dollar
  amount, vendor, and fiscal timing.
- `opportunity-enrichment` confirms budget, fiscal calendar, and the decision makers
  behind a contract item.
- `signal-outreach` drafts the message that references the actual line item.
- `rfp-timeline` takes an award from here and traces it back to the originating RFP and
  the first pain signal.
- `territory-monitor` folds this sweep into recurring coverage so new RFPs and renewals
  surface week over week.
