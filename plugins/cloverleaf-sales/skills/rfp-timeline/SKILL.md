---
name: rfp-timeline
description: "Trace a government contract award backward through Cloverleaf to the originating RFP or bid announcement and to the first spoken pain signal, then render the procurement arc as a timeline with a contact layer. Use whenever the user says trace this contract back, when did they first talk about this, show me the full procurement timeline, find recent awards and trace them back, what was the pain point before they awarded this contract, who won and when did it start, or asks for N recent contract awards in a given state. Use this instead of signal-dashboard when the goal is depth over time on one procurement event rather than breadth across active pain signals. Award sources are meeting documents, transcripts, and the federal purchase records."
---

# RFP timeline

## Purpose

Surface recent contract awards, then walk each one backward to find when the procurement
was first opened publicly and when the underlying problem was first voiced. Output is a
three node arc per award (pain, first RFP signal, award) plus a contact layer.

Tool parameters and limits are in `cloverleaf-mcp-operations`. Load it before searching.

**This skill is the deliberate exception to Guardrail 1 in `cloverleaf-signal-search`.**
That skill hunts pre-decision pain and rejects anything at award stage. This one starts at
award stage on purpose, because the point is to show the history that led there. The
vendor guardrail in Step 2b is different and does apply.

## Step 0: inputs

Ask for these before searching, and skip ahead if the conversation already carries them.
Never default to a hardcoded state or skip the vendor lens; it decides what gets rejected.

Required: target state or states (or "national"), the number of timelines N (3 to 8
recommended, cap at 10), and the vendor lens (whose perspective this is for).

Optional: a product vertical, a time window for the award search (default 120 days), and a
minimum contract value.

If a vertical is given, translate it into solution nouns rather than generic procurement
words. `document-signal-search/references/procurement-vocabulary.md` carries the banks and
the phrases that flood a sort. With no vertical, run a broad award language sweep and let
the results set the coverage.

## Step 1: find recent awards

Three sources catch different things. Run the first two always, and the third when federal
is in scope.

**Source A, the written record.** Usually strongest, because officials rarely say a vendor
name out loud but agendas print it.

```python
run-document-keyword-search(
    terms    = [<solution terms>, "not to exceed", "award of contract"],
    states   = [<target states>],       # states works; pass it
    daysBack = <window, default 120>,
    sortBy   = "hits",
    perPage  = 10,
)
```

**Source B, the spoken record.**

```python
run-meeting-keyword-search(
    terms            = ["awarded to", "contract award", "accept the bid",
                        "authorize the contract", "approve the contract"],
    mustIncludeTerms = [<vertical terms, if given>],
    states           = [<target states>],
    daysBack         = <window>,
    perPage          = 50,              # max 100, paginate for more
)
```

**Source C, federal awards.** `search-purchases` with an intent sentence, or
`run-purchase-keyword-search` with exact terms. Verified 2026-09-02: dataset 1 is federal
contract awards with USAspending style `CONT_AWD` ids, carrying `amount`, `vendor_name`,
`department`, `purchase_description`, and `transaction_date`. Three caveats before you
build on it:

- Coverage beyond federal is unverified as of 2026-09-02. Every sampled row was a federal
  department. Do not claim state or local award coverage from this layer.
- `department` is the awarding body. Ignore `organization_names`, which came back
  identical on every row.
- There is no `cloverleaf_url` on a purchase row, so cite the award by `source_row_id`,
  department, vendor, and date. A federal award also has no Cloverleaf org id you can
  trust, so Step 2a resolution has to run off the department name, and the backward trace
  works only where that body's meetings are ingested. When it is not, say so and present
  the award as a single node.

**Qualify every candidate before pulling anything expensive.** Confirm ratification
language is present (a resolution, a vote, a motion to approve, an award of contract to a
named vendor with a dollar figure); a mention or a discussion is not an award. Record
vendor, value, project description, awarding body, date, and source. Drop spam rows,
federal rows when federal is out of scope, and duplicates (dedupe on `organization_id`
plus title plus date, never on id alone).

Only after an award is confirmed from title, highlight, or excerpt text do you pull
`get-meeting-transcripts` or `get-document`. Keep the full payload calls on the shortlist.

Take the top N by recency, or by value if the user asked to prioritise size, and say how
many qualifying candidates you set aside.

## Step 2a: resolve the organization

`lookup-organization(query = "<Agency Name>, <ST>")`. It is embedding ranked, so read the
whole list; the right org can sit well below the top hit, and many matches carry
`meeting_count: 0`. Large cities are often indexed as "{Name} City Council", and a place
name that misses is often filed under the body ("Victoria City Council"). Record the
`organization_id`; every downstream call uses it.

## Step 2b: vendor guardrail

Compare the awarded vendor against the vendor lens from Step 0.

- **The awarded vendor is the vendor lens.** Discard the award and say why. There is
  nothing to trace backward for; the deal is won, not a prospecting target.
- **The awarded vendor is a competitor, or no lens was given.** Keep it. A competitor win
  is the displacement intel this skill exists to produce.

This is narrower than Guardrail 0 in `cloverleaf-signal-search`, which rejects on any
mention. Here the award has already happened by definition, so a named competitor at any
stage is the product, not noise.

## Step 3: trace back to the first RFP or bid announcement

Documents first, because solicitation language is written rather than spoken.

```python
run-document-keyword-search(
    terms    = ["request for proposals", "invitation to bid", "solicitation",
                <project specific keywords from the award>],
    states   = [<award's state>],
    daysBack = 365,                     # widen if not found
    sortBy   = "hits",
)
```

Filter results to the `organization_id` from Step 2a. If nothing surfaces, fall back to
`run-meeting-keyword-search` with the same terms plus RFP, ITB, and scope of work, and
filter client side on the `organization_id` carried in the `meetings[]` array. Paginate
with `page` rather than narrowing prematurely.

Record the earliest hit where solicitation language attaches to the same project as the
award: date, source and id, a short excerpt, and days elapsed to the award.

If no RFP signal is indexed in either source, mark the node **Signal not indexed** with a
dashed placeholder. A coverage gap is a finding worth surfacing to a prospect, not
something to hide.

## Step 4: trace back to the first pain point

A spoken record job; pain is discussed before it is formalised.

```python
run-meeting-keyword-search(
    terms    = [<pain terms for this project type: "outage", "breach",
                "aging infrastructure", "end of life", "audit finding">],
    states   = [<award's state>],
    daysBack = <window preceding the RFP date from Step 3>,
    perPage  = 50,
)
```

Filter to the same `organization_id`. Record the earliest meeting describing the problem
in the same project context: date, meeting id, speaker name and title where available, a
short excerpt, and the total pain to award window in days.

Treat any speaker name as unconfirmed until you check it against the roster. The `person`
block is inference, and ASR mangles names.

A full three node timeline is the best output. A partial one is still worth showing with
the missing node marked, rather than dropped.

## Step 5: contacts

Two different things live here.

**5a, a named vendor rep.** Scan the text already pulled across all three nodes for a rep
named in connection with the opportunity. Record name, title if stated, and which node it
appeared in. If none, the cell reads **Not found in source text**. Never invent one.

**5b, the buyer side roster.** `list-contacts(organizationId, limit = 25)`. Drop records
where `removed_at` is set, check email domains and titles for jurisdiction contamination,
and say so explicitly when the roster comes back empty rather than skipping the org.

## Step 6: render the timeline

Hand the assembled cases to `signal-dashboard`, which owns the rendering and the brand
palette, or build one self contained HTML file with two tabs.

**Timelines tab.** A summary bar (awards surfaced, awards discarded by the vendor
guardrail with a one line reason, full versus partial timelines, total contract value, the
longest pain to award window, states covered), then one card per award:

```
[Pain point] --{days}--> [First RFP signal] --{days}--> [Contract award]
```

Each node carries a label, a date or a dashed "not indexed" marker, one sentence of
context, and its `cloverleaf_url`. Never build a link yourself; a federal purchase node has
no URL, so cite `source_row_id`, department, vendor, and date instead. Below the arc: the
vendor, value, and category, then the rep name or "Not found in source text", then the top
one or two buyer contacts. The award node always renders, because it is the anchor.

**Contacts tab.** One row per award: agency, project, vendor, rep name, buyer contact,
source, actions.

## Step 7: offer next steps

Export to CSV (agency, project, vendor, value, all three dates, the pain to award window,
rep name, buyer contacts, links). Hand competitor-won timelines to `signal-outreach` for
the displacement angle. Flag any org with a "not indexed" node to `territory-monitor` so
future activity is caught earlier. Offer to rerun for more states or a longer lookback.

## Key rules

- Gather states, N, and the vendor lens before any search.
- Do not apply Guardrail 1 from `cloverleaf-signal-search` here; awards are the input, not
  a rejected late stage signal. The Step 2b vendor guardrail is narrower and does apply.
- Never render a card without a confirmed award node.
- Never fabricate a vendor name, a rep, or a contact. Absent means "Not found in source
  text".
- Missing nodes render as dashed placeholders and get called out as a coverage finding.
- Reserve `get-meeting-transcripts` and `get-document` for confirmed candidates.
- Keep quoted excerpts short and attributed to the speaker and meeting.
- Every confirmed node carries a meeting, document, or award id.
