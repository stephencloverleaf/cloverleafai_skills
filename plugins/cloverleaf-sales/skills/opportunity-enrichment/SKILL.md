---
name: opportunity-enrichment
description: >-
  Turns one Cloverleaf signal into a workable government opportunity by pulling the full
  meeting transcript, then filling the gaps with web search and Apollo.io: jurisdiction
  profile, budget and fiscal timing, procurement stage, grants such as SLCGP, and the
  decision-makers to sell into. Also verifies the signal before anyone acts on it, since
  speaker names, timestamps, and jurisdictions in search output are inferences. Trigger
  phrases: "flesh out this signal", "research this lead", "build out this opportunity",
  "qualify this", "add context to this signal", "who do we call", "what is their budget",
  "is there an RFP". Runs after the signal sweep and before signal-outreach, and its output
  drops straight back onto a signal-dashboard card. Focus is the government buyer side, not
  the vendor side, which vendor-profile covers.
---

# Opportunity enrichment (government side)

## The job

A Cloverleaf signal says a jurisdiction has a need and, often, who raised it. To make it an
opportunity a rep can work, you verify it and then fill four gaps:

1. **Jurisdiction profile.** Type (city, county, school district, utility, state or federal
   agency), population, region, governing form.
2. **Money and timing.** Budget size, IT or cyber budget when findable, the fiscal-year
   calendar, which is the clock, and any grant, especially the State and Local
   Cybersecurity Grant Program (SLCGP).
3. **Procurement stage.** Pre-RFP discussion, budgeting, RFP imminent, or awarded. This
   sets urgency, and it decides whether the lead is alive at all.
4. **Decision-makers.** IT Director, CIO, CISO, City or County Manager, Finance Director,
   procurement officer, and the relevant elected committee, with names, titles, email, and
   phone.

## Verify before you enrich

Everything in this section has been observed in real Cloverleaf output. Run these checks
first, because enrichment built on a defective signal looks complete and is wrong.

- **Confirm the jurisdiction from transcript content, not the organization label.** Org
  metadata can name the wrong place, including the wrong country. A meeting labeled "City
  of Hobart, Indiana" was Hobart, Tasmania, and it still scored 4/10.
- **Treat every speaker name as an inference.** `get-meeting-transcripts` returns
  `person: null` on essentially every line, and `run-meeting-keyword-search` populates a
  `person` block for the same lines, sometimes confidently wrong. Neither endpoint is
  authoritative. Confirm a name against published minutes, an official roster, or a
  signature block before putting it behind a quote.
- **Read a window, not a quote.** Quotes get spliced across timestamps and truncated right
  before the speaker disqualifies the claim. Read around the cited offset.
- **Re-derive timestamps from the transcript.** Deep-link offsets carried over from a search
  payload have been wrong by 40 to 65 seconds, which opens the link mid-unrelated-sentence.
- **Pull every session for the date.** The same meeting appears under several IDs, and long
  hearings split into morning and afternoon records. Check `is_spam`, `user_marked_spam`,
  `spam_certainty`, and whether `duration_seconds` matches the scheduled length.
- **Apply the buyer-ownership test.** Do the people speaking own the system that failed, and
  do they hold budget for this category? Legislators conducting oversight, public
  commenters, and advocacy witnesses fail this even when the quote is specific and recent.
  If you cannot name who receives the rep's first email and why they would care, demote the
  signal to background.
- **Check the stage before spending effort.** "Took quotes and awarded" or "the board
  approved" means the lead is gone. Cold outreach needs an open, pre-solicitation signal.
- **Verify the category fits what the vendor sells.** A well-quoted power-supply failure
  scores high and is unsellable for a network security vendor.

## Source order

Spend effort, and paid Apollo credits, in this order. Stop when the opportunity is workable.

### 1. Pull the full transcript

This is where `get-meeting-transcripts` belongs, on the three to five signals that already
cleared scoring, not during discovery. It is free and it is the highest-value step, so it
comes before any web search or Apollo call.

The discovery excerpt is a clipped window. The full transcript often adds a dollar figure
said a minute later, a second named speaker, or the shape of the timeline the excerpt cut
off. Pull the project name, dollar figure, prior incident, and timing language such as
"budget workshop" or "audit last year" before searching anything else.

For the buying group, call `list-contacts` with the signal's `organizationId`. Coverage is
uneven: incorporated cities and counties are strong, special districts and utilities can
return nothing. When a roster is empty, say so rather than dropping the org silently. Small
orgs share inboxes across officials, so dedupe by email and prefer the named-title contact.

For exact parameter names, limits, and response shapes, see `cloverleaf-mcp-operations`.

### 2. Search the web

For small and mid-size local governments the open web beats any contact database, because
budgets, agendas, staff directories, and grant awards are public. Adapt the jurisdiction
name and run:

- `"<Jurisdiction>" adopted budget FY2027 cybersecurity OR information technology`
- `"<Jurisdiction>" CIP OR capital improvement information technology`
- `"<Jurisdiction>" RFP OR RFQ cybersecurity OR "managed security" OR "penetration testing"`
- `"<Jurisdiction>" SLCGP OR "cybersecurity grant" award`
- `"<Jurisdiction>" IT director OR CIO OR "information security" staff directory`
- `"<Jurisdiction>" ransomware OR data breach` (news, since a prior incident means urgency)
- `"<State>" fiscal year start local government`

Fetch the jurisdiction's own government site for the staff directory, the budget PDF, and
the agenda pages. Pull names, titles, and budget numbers from primary sources. Never
estimate a figure. If you cannot verify one, say so and leave it for the rep.

### 3. Use Apollo.io

Apollo.io replaced ZoomInfo on 2026-08-11. The ZoomInfo server is disconnected and returns
nothing rather than failing, so any instruction to call it is stale. Apollo tools are
deferred in Claude Code: load them with ToolSearch using a `select:` query before calling,
and use the bare tool names. Every account gets its own Apollo server ID, so never
hard-code a server prefix. Every Apollo call consumes paid credits.

| What you need | Tool |
|---|---|
| Company firmographics from a domain | `apollo_organizations_enrich` (bulk: `apollo_organizations_bulk_enrich`) |
| Find organizations matching criteria | `apollo_mixed_companies_search` |
| Find people by title, seniority, or org | `apollo_mixed_people_api_search` |
| Confirm or enrich one known person | `apollo_people_match` (bulk: `apollo_people_bulk_match`) |
| Search contacts already in the CRM | `apollo_contacts_search` |
| Hiring as a budget and urgency tell | `apollo_organizations_job_postings` |

Working notes:

- **Government coverage is thinner than ZoomInfo's was**, and thinner for small
  jurisdictions than large ones. That changes the research order rather than swapping one
  tool for another: Cloverleaf first, the entity's own web presence second, Apollo third.
  Use Apollo for larger agencies and authorities and to confirm a named person.
- Run people searches in two passes, one by department or level and one by title keyword.
  Combined filters underperform.
- Check `apollo_contacts_search` before spending anything new.
- Apollo has no scoops or news feed. `apollo_organizations_job_postings` is the nearest
  urgency tell. Do not promise an equivalent.
- Check remaining credits with `apollo_users_api_profile`, not
  `apollo_usage_stats_credit_usage_stats`, which has reported direct-dial credits as
  exhausted when thousands remained. Phone reveal is asynchronous: a bulk match with phone
  reveal returns a request ID, and the numbers arrive from polling
  `apollo_webhook_result_show`. Email comes back inline.
- **Honesty rule:** when Apollo coverage is thin for a small jurisdiction, say "Apollo
  coverage is thin here, the staff directory is the better source" and use the web. A blank
  field is a fact. A guess is a defect.

### 4. Optional: cross-check the award stage against purchase records

`search-purchases` (semantic) and `run-purchase-keyword-search` (lexical) read contract and
purchase records. Use them only to answer "has this already been bought", which sets the
stage field and can kill a lead.

Rules for reading a purchase row, verified live 2026-09-02:

- **`department` is the buyer.** Never present `organization_names` or `organization_ids`.
  Every row carries the same 175 ids and 155 names, the entire federal organization list, so
  those fields are a dataset-level association rather than the awarding body.
- **Purchase rows carry no `cloverleaf_url`.** Never build one. Cite the award by
  `source_row_id`, `department`, `vendor_name`, and `transaction_date`.
- **`amount` can be 0** on a contract modification, so a zero is not evidence of a small buy.
  `start_date` and `end_date` were null on every sampled row.
- Scores on a good query ran 0.73 to 0.79, so calibrate these like document hits rather than
  like transcript hits.

**Federal caveat:** `purchase_dataset_id` 1 is federal contract awards, with USAspending-style
award IDs. Coverage beyond federal is unverified as of 2026-09-02, so an absence here says
nothing about a city or county buy.

## Frame it as MEDDPIC

Map what you find so the brief is sales-ready even when partial:

- **Metrics:** the cost of the pain, such as downtime, audit findings, or ransom exposure.
- **Economic buyer:** usually the City or County Manager or the council. Finance controls
  the purse.
- **Decision criteria and process:** RFP versus cooperative purchase (NASPO, Sourcewell),
  and the board vote cadence.
- **Identified pain:** the exact quote from the meeting.
- **Champion:** the official who raised it, often your signal speaker.
- **Competition:** any incumbent or product named in the meeting, which means an active
  evaluation.

Leave a field blank rather than guessing.

## Output: extend the signal

Append these fields so the dashboard and outreach skills pick them up:

```jsonc
{
  // original signal fields: jurisdiction, quote, cloverleaf_url, meeting_id, terms
  "jurisdiction_profile": { "type": "city", "population": "", "region": "", "fiscal_year": "" },
  "money_timing": { "budget_notes": "", "grant": "" },
  "procurement_stage": "Budgeting / pre-RFP",
  "contacts": [
    { "name": "", "title": "", "email": "", "phone": "", "source": "list-contacts" }
  ],
  "meddpic": { "identified_pain": "", "champion": "", "economic_buyer": "" },
  "speaker_confirmed": false,
  "fit": "one line on why this is a real opportunity",
  "next_action": "one line on the move",
  "sources": ["Cloverleaf meeting <id>", "<jurisdiction> budget page"]
}
```

`fit` and `next_action` are one line each and are exactly what the dashboard card and the
outreach draft need. Set `speaker_confirmed` only when you checked the name against minutes,
a roster, or a signature block.

## Hand off

Pass the enriched signal to `signal-outreach` for the email, LinkedIn note, and call script,
and back to `signal-dashboard` so the card shows budget, stage, contacts, and next step.
