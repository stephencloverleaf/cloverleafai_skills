---
name: signal-dashboard
description: >-
  Turn Cloverleaf signals (or raw `search-meetings` / `run-document-keyword-search` output)
  into a polished, sortable, filterable HTML sales dashboard branded in Cloverleaf
  navy and Sky accent. Handles BOTH discussion signals (what officials say, from transcripts)
  and procurement signals (what they're buying — vendors, dollar amounts, RFP/renewal
  stage, from documents), and can mix them on one board. Use this skill whenever the
  user has found signals and wants to SEE, sort, triage, or present them — phrases like
  "build a dashboard," "show me these leads," "make this easy to sort through," "put the
  signals in a view," or right after running a Cloverleaf search in a demo. This is step
  2 of the demo workflow (search → DASHBOARD → enrich → outreach). Produces one
  self-contained .html file that opens instantly offline — no internet needed in the room.
---

# Signal Dashboard

## What it produces

A single self-contained `.html` file (no CDNs, no internet — safe for a conference
room with bad wifi) that shows every signal as a scannable card, ranked by lead score,
with live sort and filter. The audience instantly sees: which jurisdictions are Hot,
who said what, whether you have their email/phone, and what to do next. This is the
"so it's not just a search box — it's a workflow" beat of the demo.

**Brand palette (official — from the Cloverleaf AI brand guidelines; this is the canonical list, do not invent values).** The script bakes these in:
- **Ink Navy `#1B232E`** — primary dark surface (header, stat numbers, text accents)
- **Sky `#CCF1FD` / Sky-deep `#A9E3F4`** — the signature accent (badge fills, chips, borders). It's *light*, so use it as a background/border, not as text on white.
- Cream `#F3F1EA`, Near-Black `#16171B`, White `#FFFFFF`, Stone `#8C8A84`, Slate `#9AA1AA`
- **There is NO Cloverleaf green.** The old `#2E8B57` (and navy `#1B2A4A`) were fabricated and off-brand — never reintroduce them.
- **Logo:** black or white official lockup only — never recolored, and never a stand-in shape like a colored dot. The script embeds the official white logo in the navy header.

## The fastest path: use the bundled script

`scripts/build_dashboard.py` does the rendering. It accepts raw Cloverleaf output
**directly**, so in a live demo you can go from search → dashboard in one step.

```bash
python3 scripts/build_dashboard.py INPUT.json -o signal_dashboard.html \
  --title "Cybersecurity Signals — <Prospect Name>" \
  --subtitle "Pre-RFP buying signals from live government meetings"
```

`INPUT.json` can be any of:

1. **Raw transcript `search-meetings` output** — the `{ "results": [...] }` from the connector. The
   script collapses each meeting to its single best signal line, prefers lines with a named
   speaker + contact info, and pulls the jurisdiction from the speaker's org. These are
   tagged `discussion` signals.
2. **Raw `run-document-keyword-search` output** — the `{ "object_api_response": {...} }`
   from the document tool. The script keeps only documents where a real topic term hit
   (dropping procurement-boilerplate-only matches, matching the `document-signal-search`
   rule) and tags them `procurement`. **Best-effort** extraction pulls a dollar amount,
   stage, and vendor from the highlight text — see the caveat below.
3. **A normalized signals list** — `{ "signals": [ {...}, ... ] }` (or a bare `[...]`). Use
   this for enriched or model-read signals. Set `signal_type` to `"discussion"` or
   `"procurement"`; for procurement cards add `vendor`, `amount`, `procurement_stage`,
   `doc_type`. Schema is documented at the top of `build_dashboard.py`.

A single board can mix discussion and procurement signals — concatenate them into one
`{"signals":[...]}` list, or build two and combine. When both types are present, the
dashboard shows a Discussion/Procurement filter and a Procurement count stat; with one
type, those hide themselves.

Then show it with `present_files` (preferred — gives Stephen a clickable card), or open it
in the browser.

### Procurement extraction: trust the model over the regex for flagship cards

Raw documents are OCR'd agenda text — often two unrelated line items in one block. The
script's auto-extraction is deliberately **conservative: it leaves `vendor`/`amount` blank
rather than guess wrong** (a wrong dollar figure on a card is worse than none). It reliably
catches clean phrasings ("Agreement with PKI Solutions LLC… Not-to-Exceed $337,500") but
will miss or blank a mangled one (e.g. a Bitdefender renewal interleaved with a paving
invoice — it'll get the vendor and stage but may blank the amount).

So for the **handful of signals that matter in a demo**, don't rely on the regex: read the
highlight passage yourself, pull the right `vendor` / `amount` / `procurement_stage`, and
pass them as a normalized `signals` entry (path 3). That's the reliable path and it takes
seconds for the top few. Use raw-document auto-ingest (path 2) for fast, rough triage of the
whole result set.

## Lead scoring (so Hot/Warm/Cool is consistent every demo)

If a signal has no explicit `score`, the script computes one 0–100. The rubric **depends on
signal type**, because a procurement signal has no speaker to score:

**Discussion signals** (transcripts) — the four factors the search skill uses:
- **Named decision-maker** (+30) — a real person, ideally one who owns budget.
- **Contact info present** (+25) — email or phone attached. This is the jackpot.
- **Recency** (+20 / +12 / +6) — within 30 / 90 / 180 days.
- **Substance** (up to +25) — keyword density (`hits`) and a specific, quotable statement.

**Procurement signals** (documents) — scored on deal mechanics, not people:
- **Dollar figure present** (+30) — a real line item, not a passing mention.
- **Named vendor/incumbent** (+18) — a displacement clock you can work.
- **Stage** (+25 award/renewal/agreement · +18 RFP · +10 budget item) — how close to closing.
- **Recency** (+22 / +14 / +7) — fiscal timing matters even more here.
- **Notice penalty** (−8) — `notice` docs are usually publication boilerplate.

Tiers (same for both): **Hot ≥ 70**, **Warm 45–69**, **Cool < 45**. Badge fills: Hot uses a functional alert red, Warm uses the Sky accent (navy text), Cool uses grey — not a brand green. A
contract about to be awarded ($ + vendor + "agreement") lands Hot with no named person —
which is correct. Override either rubric by setting `score` explicitly when you want to
reflect human judgment.

## Make the cards demo-ready (optional but worth it)

The raw search gives you quote + speaker + contacts. Two cheap upgrades make a card sing:

- **Watch link → the Cloverleaf platform:** every card automatically renders a
  "▶ Watch on Cloverleaf" link to `https://app.cloverleaf.ai/meetings/<meeting_id>` — the
  platform page where the video **and** the AI insights live. The script builds this from
  each signal's `meeting_id`, so you don't pass anything for it. A readable timestamp hint
  (e.g. "quote ~5:07 in") is shown next to the link so the rep knows where to scrub. This is
  the point: the rep lands inside Cloverleaf, not on a raw YouTube/source video. (If you ever
  need to point a card somewhere specific, set `cloverleaf_url` to override; the legacy
  `video_url` field still works as a last-resort fallback only when a signal has no
  `meeting_id`.)
- **`fit` and `next_action`:** one line each. `fit` = why this is a real opportunity;
  `next_action` = the move. These come for free if you run `opportunity-enrichment`
  first, but you can also write them inline.

When you hand enriched signals (with `contacts`, budget, timeline) to the dashboard,
keep the same `signals` schema and just add fields — the card shows what's present and
ignores what isn't.

## Watch-outs

- **Big raw results:** a broad search can exceed the context window and get saved to a
  file. Don't paste it — point the script at that file path directly; it streams fine.
- **"Unknown jurisdiction":** appears only when a meeting has no identified speaker
  anywhere (so search returned no org). Those are low-value anyway; drop them or infer
  the jurisdiction from context. The strong, named-speaker signals always carry their org.
- **Procurement signals show "Org #<id>", not a name.** `run-document-keyword-search`
  returns `organization_id` but no jurisdiction name. For the cards that matter, resolve the
  name (from your territory org-id map, or by cross-referencing a meeting-side hit for the
  same org) and set `jurisdiction` on the normalized signal so the card reads "City of X, ST"
  — that also re-enables the state filter for those cards.
- **State filter** auto-populates only when jurisdictions include a `, ST` suffix.
  `opportunity-enrichment` adds that; raw data may not have it, in which case the filter
  hides itself and the free-text search box still covers jurisdiction.

## Brand voice (Cloverleaf AI tone)

The dashboard is customer-facing. Apply these rules to any text you write
for cards, titles, subtitles, or annotations:

- **Direct and confident.** No hedging ("might," "could potentially"). No
  generic SaaS verbs (leverage, streamline, unlock, harness).
- **Concrete specifics beat vague claims.** Use real numbers, real names,
  real dates. "70,000+ government agencies" not "thousands."
- **Short sentences are a feature.** Mix short punches with longer context.
- **The company name is always "Cloverleaf AI"** — never "Cloverleaf" alone,
  never "CloverLeaf."
- **Oxford comma always.** No em dashes — use periods, colons, or line breaks.
- **Active voice.** Lead with the problem, not the product.

---

## Hand off

The dashboard is the spine of the demo. Upstream, it ingests signals from:
- **`cloverleaf-signal-search`** — discussion signals (transcripts), the guardrails, and
  the recurring territory sweep mechanics.
- **`document-signal-search`** — procurement signals (contracts, RFPs, renewals, dollars).
- **`territory-monitor`** — a week's worth of new signals across a territory.

From a chosen card, continue to:
- **`opportunity-enrichment`** — deepen a signal into a full opportunity (budget, timeline, decision-makers).
- **`signal-outreach`** — draft the email/LinkedIn/call script (quote the official for a
  discussion signal; reference the contract line item for a procurement signal).
