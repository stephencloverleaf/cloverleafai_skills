---
name: signal-dashboard
description: >-
  Turns Cloverleaf signals into one self-contained, sortable, filterable HTML sales
  dashboard branded in Cloverleaf navy and Sky, using the bundled build script. Reads live
  connector output directly from search-meetings, search-insights, search-documents, and
  run-document-keyword-search, or a normalized signals list, and handles both discussion
  signals (what officials say) and procurement signals (what they are buying) on one board.
  Trigger phrases: "build a dashboard", "show me these leads", "make this easy to sort
  through", "put the signals in a view", or right after a Cloverleaf search in a demo. Runs
  once signals exist, either as a fast triage board straight off the sweep or as the final
  board after opportunity-enrichment fills in budget, stage, and contacts. The output file
  opens offline, so it works in a room with no internet.
---

# Signal dashboard

## What it produces

One self-contained `.html` file with no external scripts, stylesheets, or images. Every
signal is a scannable card ranked by lead score, with live sort and filter. The reader sees
which jurisdictions are Hot, who said what, whether contact details exist, and what to do
next.

## Run the bundled script

`scripts/build_dashboard.py` does the rendering and accepts raw connector output directly,
so a live demo goes from search to dashboard in one step.

```bash
python3 scripts/build_dashboard.py INPUT.json -o signal_dashboard.html \
  --title "Cybersecurity signals: <Prospect>" \
  --subtitle "Pre-RFP buying signals from live government meetings"
```

`INPUT.json` can be the saved output of `search-meetings`, `search-insights`,
`search-documents`, or `run-document-keyword-search`, or a normalized `{"signals": [...]}`
list. The reader dispatches on the top-level key. For the field-by-field shape of each
input, the normalized signal schema, and which fields each card renders, read
**`references/input-shapes.md`**.

Then present the file so the user gets a clickable link, or open it in a browser.

## Rules the board depends on

- **Cite `cloverleaf_url`, never build a link.** Every meeting, document, and insight
  carries one. The script copies it verbatim and shows a plain meeting ID when it is
  missing. A link assembled from an ID can point at a page that does not exist.
- **Read the model into the flagship cards.** Auto-extraction of vendor, dollar amount, and
  stage from OCR'd agenda text is deliberately conservative: it leaves a field blank rather
  than guess, because a wrong dollar figure on a card is worse than none. For the handful of
  signals that matter, read the passage yourself and pass `vendor`, `amount`, and
  `procurement_stage` on a normalized signal. Use raw auto-ingest for fast triage of the
  whole result set.
- **`search-meetings` returns no speaker.** Verified live 2026-09-02: transcript chunks
  carry only an ID, text, start time, and score. Cards from that tool are speaker-blank by
  design. Fill the name from `list-contacts` or `opportunity-enrichment`, and only after
  confirming it, since speaker attribution anywhere in the platform is inference rather than
  data.
- **Documents carry no organization name.** `search-documents` and
  `run-document-keyword-search` return `organization_id` only, so those cards read
  "Org #<id>" until you resolve the name and set `jurisdiction`. Resolving it also turns the
  state filter back on for those cards.
- **Filter before you present.** Drop spam rows, drop duplicate uploads of the same meeting
  (dedupe on organization, title, and date, never on meeting ID alone), drop federal rows
  when federal is out of scope, and drop any signal naming the vendor you sell for as already
  contacted, demoed, or quoted. Label the stage on document hits, which are late-stage by
  nature.
- **The state filter needs a `, ST` suffix** on the jurisdiction. The script adds it from the
  meeting's state name; normalized signals you write by hand need it too.

## Lead scoring

If a signal has no explicit `score`, the script computes one from 0 to 100. The rubric
depends on signal type, because a procurement signal has no speaker.

**Discussion signals:**

- Named decision-maker attached: +30.
- Contact info attached: +25.
- Recency: +20 within 30 days, +12 within 90, +6 within 180.
- Substance: up to +25 from keyword density and quote length.
- Semantic relevance, only when no speaker is attached: +30 at a best score of 0.80 or
  above, +20 from 0.75, +10 from 0.70. This stands in for the missing person factors, since
  the discovery tool returns no speaker.

**Procurement signals:**

- Dollar figure present: +30.
- Named vendor or incumbent: +18.
- Stage: +25 for award, renewal, or agreement; +18 for RFP; +10 for a budget item.
- Recency: +22 within 30 days, +14 within 90, +7 within 180.
- Notice document: minus 8, since notices are usually publication boilerplate.

Tiers for both: **Hot at 70 or above, Warm 45 to 69, Cool below 45.** Set `score` explicitly
to override either rubric with human judgment.

## Brand

These values come from the Cloverleaf AI brand guidelines. The script bakes them in. Do not
invent others.

- **Ink Navy `#1B232E`:** primary dark surface for the header, stat numbers, and text
  accents.
- **Sky `#CCF1FD` and Sky-deep `#A9E3F4`:** the signature accent for badge fills, chips, and
  borders. Both are light, so use them as a background or border, never as text on white.
- Cream `#F3F1EA`, Near-Black `#16171B`, White `#FFFFFF`, Stone `#8C8A84`, Slate `#9AA1AA`.
- **There is no Cloverleaf green.** The old `#2E8B57` and navy `#1B2A4A` were fabricated and
  off-brand. Never reintroduce them.
- **Logo:** the official black or white lockup only, never recolored and never a stand-in
  shape. The script embeds the official white logo in the navy header.
- Badge fills: Hot uses a functional alert red, Warm uses Sky with navy text, Cool uses grey.

## Voice for anything you write on the board

The dashboard is customer-facing, so it is governed by the house sales-communication
standard. If a `sales-communication` or `humanizer` skill is available in this session, load
it first. Otherwise apply the checklist in `signal-outreach`'s
`references/outreach-checklist.md`. Beyond that:

- Direct and concrete. Real numbers, real names, real dates. No hedging, no generic SaaS
  verbs such as leverage, streamline, unlock, or harness.
- Short sentences. Active voice. Lead with the problem, not the product.
- The company name is always "Cloverleaf AI", never "Cloverleaf" alone.
- Oxford comma. No em dashes or en dashes. Use a period, comma, colon, or line break.
- Never print "45,000+ agencies". The website says 70,000+ agencies monitored continuously.
  Verify any platform figure before printing it.
- Lead with findings. No "what I cut", "what I could not verify", or standing-caveat
  sections. A single source and date line at the foot is fine.

## Watch-outs

- **Large raw results** get written to a file rather than returned inline. Point the script
  at that file path; it streams fine.
- **"Unknown jurisdiction"** means the payload carried no organization for that row. Those
  are low-value; drop them or set the jurisdiction yourself.

## Hand off

Upstream, the board ingests signals from `cloverleaf-signal-search` (discussion),
`document-signal-search` (procurement), and `territory-monitor` (a week across a territory).
From a chosen card, continue to `opportunity-enrichment` to deepen it, then
`signal-outreach` to draft the message.
