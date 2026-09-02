---
name: rfp-timeline
description: "Use this skill whenever the user wants to trace government contract awards backward through meeting history to the originating RFP, bid announcement, or first pain signal. Triggers include: 'trace this contract back', 'when did they first talk about this?', 'show me the full procurement timeline', 'find recent awards and trace them back', 'what was the pain point before they awarded this contract?', 'who won and when did it start?', or any request to surface a procurement history rather than just a current signal. Also triggers when a user asks to find N recent contract awards in a given state. Use this skill instead of signal-dashboard when the goal is depth-over-time on procurement events (one award traced through its full history), not breadth across active pain signals."
---

# RFP Timeline

## Purpose

Surface recent government contract awards in one or more states, then trace each award backward through Cloverleaf to find (1) the first RFP or bid announcement, (2) the earliest underlying pain point, and (3) any vendor rep name mentioned in connection with the opportunity. Output is a visual timeline dashboard — one 3-node procurement arc per award — plus a contact layer for named reps.

**Read `cloverleaf-signal-search` before running any search in this skill.** Every tool call below assumes its rules (daysBack always set, no `states` on document search, 25-meeting cap, dedupe rules). Where this skill and that reference conflict, the reference wins.

**This skill is the deliberate exception to Guardrail 1 (pain-vs-procurement) in `cloverleaf-signal-search`.** That skill hunts for pre-decision pain and explicitly rejects anything at RFP/award stage. This skill *starts* at award stage on purpose — the point is to walk backward and show the history that led there. Do not apply Guardrail 1's stage filter here; it would reject every input by design. The vendor guardrail below is different and does apply — see Step 0.

---

## Step 0: Gather Inputs

Ask the user for the following before searching. If any are already present in the conversation, skip straight to Step 1.

**Required:**
1. **Target state(s)** — one state, a list, or "national"
2. **Number of leads (N)** — how many contract award timelines to surface (recommended 3–8; cap at 10)
3. **Vendor lens** — whose perspective is this for? (e.g. "Sophos," "our own pipeline," "no specific vendor — just show me who won"). This determines the guardrail in Step 2b.

**Optional but useful:**
- Product vertical or industry filter (e.g., "only cybersecurity," "only road infrastructure," "only waste management") — leave open if the user wants whatever comes up
- Time window for the award search (default: last 120 days)
- Minimum contract value

If a vertical filter is given, translate it into specific solution-noun search terms (not generic procurement words — see Step 1 and the term-bank guidance in `document-signal-search`). If no filter is given, run a broad award-language sweep and let results drive the industry coverage.

Do not default to a hardcoded state or skip the vendor-lens question — it changes what gets rejected in Step 2b.

---

## Step 1: Find Recent Contract Awards

Two independent sources can surface an award — run both, they catch different things:

**Source A — spoken record.** `run-meeting-keyword-search` for award language:

```python
run-meeting-keyword-search(
    terms            = ["awarded to", "contract award", "accept the bid",
                         "authorize the contract", "approve the contract"],
    mustIncludeTerms = [<vertical terms, if a filter was given>],
    states           = [<target state(s)>],   # omit if "national"
    daysBack         = <window from Step 0, default 120>,
)
```

**Source B — the written record, usually stronger for this job.** Officials rarely say a vendor name out loud, but agendas print it. `run-document-keyword-search` for the same window:

```python
run-document-keyword-search(
    terms    = [<vertical solution terms — see document-signal-search term bank>,
                "not to exceed", "award of contract"],
    daysBack = <window from Step 0, default 120>,
    perPage  = 10,
    # states = NEVER — 500s every time, see cloverleaf-signal-search Rule 2
)
```

If a state/territory scope is needed, resolve target jurisdictions to `organization_id`s first via `lookup-organization`, then post-filter document results by that ID set — do not attempt `states` on the document call.

**For each candidate from either source, before pulling any transcript:**
- Confirm ratification language is present (resolution, vote, motion to approve, "award of contract to," a dollar figure with a named vendor) — a mention or discussion is not an award.
- Note vendor name, contract value, project description, awarding agency, meeting/document date, and the source (`meeting` or `document`).
- Apply the dedup and noise rules from `cloverleaf-signal-search` Rule 4: drop `is_spam` rows (judged by content, not the flag alone), drop Federal rows unless federal is explicitly in scope, and dedupe on `organization_id` + title + date — never on ID alone.

**Only after an award is confirmed by title/highlight/excerpt text** — not before — pull `get-meeting-transcripts` (for a meeting-sourced award) or `get-document` (for a document-sourced one) to verify the full context. This keeps the expensive full-payload calls to the shortlist, matching how every other skill in this kit treats `get-meeting-transcripts`.

Collect the top N awards by recency (or contract value, if the user asked to prioritize by size). If more than N qualifying awards exist, keep the top N and tell the user how many additional candidates were set aside.

---

## Step 2a: Resolve the Organization

For each confirmed award:

```python
lookup-organization(query = "<Agency Name>, <ST>")
```

`lookup-organization` is embedding-ranked, not exact-match — read the full returned list, the right org can sit well below the top hit (see the tool reference in `cloverleaf-signal-search`). Large cities are often indexed as "{Name} City Council."

Record the resolved `organization_id`. Every downstream call in this skill uses it.

---

## Step 2b: Vendor Guardrail

Check the confirmed vendor name on the award against the **vendor lens** named in Step 0.

- **If the awarded vendor IS the vendor lens** (we're running this for Sophos, and Sophos won) → **discard this award from the timeline set.** There's nothing to trace backward for — the deal is won, not a prospecting target. Note it was discarded and why, don't just silently drop it.
- **If the awarded vendor is a competitor, or no vendor lens was specified** → keep it. A competitor win is exactly the displacement intel this skill exists to produce.

This is narrower than Guardrail 0 in `cloverleaf-signal-search`. That skill rejects if the vendor is mentioned *anywhere* (contacted, demoed, quoted) because it's hunting pre-decision pain where any vendor contact taints the signal. Here the award has already happened by definition, so the only actionable reject condition is "the vendor we're running this for is the one who already won" — a competitor being named, discussed, or having lost is the product, not noise.

---

## Step 3: Trace Back to First RFP or Bid Announcement

For each award that cleared Step 2b, search backward through the same organization's history to find when the procurement was first opened publicly.

**Document search first — it's the better tool for this.** RFP/solicitation language is written, not spoken (same finding as `document-signal-search`: "documents name vendors, transcripts rarely do" — the same logic applies to RFP announcements).

```python
run-document-keyword-search(
    terms    = ["request for proposals", "invitation to bid", "solicitation",
                <project-specific keywords from the award, e.g. vendor's product category>],
    daysBack = <enough to precede the award — start at 365, widen if not found>,
    # states = NEVER
)
```
Post-filter to the resolved `organization_id` from Step 2a.

**If nothing surfaces in documents**, fall back to the spoken record:

```python
run-meeting-keyword-search(
    terms    = ["request for proposals", "RFP", "invitation to bid", "ITB",
                "scope of work", <project keywords>],
    states   = [<award's state>],
    daysBack = <same window>,
)
```
Post-filter to the same `organization_id` (this tool has no org-ID parameter directly, but `meetings[]` in the response carries `organization_id` — filter client-side). Respect the 25-meeting cap: if the window is wide and results are hitting the cap without surfacing the target org, narrow with more specific project keywords rather than paginating (there is no pagination on this tool).

Record the earliest hit where RFP/solicitation language appears in connection with the same project as the award.

**If no RFP signal is indexed for that organization in either source**, mark the node **"Signal Not Indexed"** with a dashed placeholder. This is not a failure state to hide — a coverage gap on a jurisdiction is itself worth surfacing to a Cloverleaf prospect (the "we'd have caught this earlier" value prop).

**Output fields per case:**
- First RFP/signal date
- Source (`meeting` or `document`) and ID
- Short excerpt or motion language
- Days elapsed from signal to award

---

## Step 4: Trace Back to First Pain Point

For each award with a confirmed RFP/signal date, continue scanning backward — same organization, earlier window — for the earliest mention of the underlying problem rather than the procurement process.

This is a spoken-record job. Pain is discussed before it's formalized; use `run-meeting-keyword-search` with problem-language terms derived from the project type, not generic ones:

```python
run-meeting-keyword-search(
    terms    = [<pain-adjacent terms for this project type — e.g. for a network
                 security award: "outage", "breach", "aging infrastructure",
                 "end of life", "audit finding">],
    states   = [<award's state>],
    daysBack = <window preceding the RFP date found in Step 3>,
)
```

Post-filter to the same `organization_id`. Same 25-cap caveat as Step 3 — narrow terms rather than expect pagination.

Record the earliest meeting where the pain is described in relation to the same project/location context as the eventual award. Capture speaker name and title where available (the `person.contact` block, when present, is a bonus — it may hand you a decision-maker contact for free).

**Output fields per case:**
- Pain point date (or "Not Indexed")
- Meeting ID
- Speaker name/title if available
- Excerpt or paraphrase of the pain, in your own words if quoting — see the copyright note below
- Total pain-to-award window in days

A full three-node timeline is the best output. Partial timelines (RFP + award, or award only) are still worth surfacing — mark the missing node clearly rather than dropping the case.

---

## Step 5: Pull Vendor Rep and Contact Names

Two separate things live here — don't conflate them:

**5a — Any named individual in the transcripts/documents.** Scan the text already pulled across all three nodes for a vendor rep mentioned by name: "the rep from [Vendor] explained...", "we met with [Name]", a name attached to a demo or presentation. If found, record name, title (if stated), and where it appeared. If not found in any node, the contact cell reads **"Not found in transcript"** — never fabricate a name.

**5b — The buyer-side roster.** Separately from any vendor rep, pull the actual decision-maker contacts at the awarding organization:

```python
list-contacts(organizationId = <id from Step 2a>, limit = 25)
```

This is the fast, reliable contact source — direct email/phone for IT Director, Head of Purchasing, Top Appointed Executive, etc. Filter out any record where `removed_at` is not null. If the roster comes back empty (special districts and utilities sometimes do), say so explicitly rather than skipping the org silently.

**Output fields per case (Contact Layer):**
- Vendor rep name (or "Not found in transcript") + title + source node
- Buyer-side roster: up to 3–5 relevant contacts (IT/Purchasing/Executive) from `list-contacts`, each with email/phone
- Action buttons: **Apollo lookup** (for the vendor rep, if named) | **Add buyer contact to outreach sequence**

---

## Step 6: Render the Procurement Timeline Dashboard

Use `visualize:show_widget` in HTML mode. Cloverleaf brand palette: use the official colors documented in `signal-dashboard` — Ink Navy `#1B232E`, Sky accent `#CCF1FD` / `#A9E3F4`, Cream `#F3F1EA`. **There is no brand green** (the old `#2E8B57`/`#1B2A4A` were off-brand); logo black or white only. Two tabs: **Timelines** and **Contacts**.

### Tab 1: Timelines

**Summary stat bar:**
- Awards surfaced (post-guardrail)
- Awards discarded by the vendor guardrail (Step 2b), with a one-line note why
- Full timelines (all 3 nodes) vs. partial
- Total contract value across all awards
- Max pain-to-award window in days
- State(s) covered

**Per-award timeline card**, horizontal 3-node arc:

```
[Pain Point]  ——  [First RFP/Bid Signal]  ——  [Contract Award]
```

Each node: label, date (or dashed-gray "Not Indexed"), one-sentence context, and a link. Use the same link convention as `signal-dashboard` — build `https://app.cloverleaf.ai/meetings/<meeting_id>` for meeting-sourced nodes so the viewer lands inside the Cloverleaf platform, not a raw source video. Document-sourced nodes link via `documentId` where the platform supports it; otherwise cite the document type and date plainly.

Between nodes: days-elapsed span, e.g. "47 days."

Below the arc: **Vendor:** [Name] · **Value:** $[Amount] · **Industry:** [Category], then **Vendor Contact:** [Name, Title] or "Not found in transcript," then the top 1–2 buyer-side contacts from `list-contacts`.

Node styling: confirmed = solid circle (Pain = amber, Signal = Ink Navy `#1B232E`, Award = Sky `#A9E3F4` with navy text); not-indexed = dashed gray. No brand green. Award node always renders — it's the anchor.

Card header: Agency, city, state (bold), project name in subhead.

### Tab 2: Contacts

One row per award:

| Agency | Project | Vendor | Rep Name | Buyer Contact | Source | Actions |
|---|---|---|---|---|---|---|

Actions: **Apollo lookup** (vendor rep, if named) · **Add to outreach sequence** (buyer contact, pre-filled from `list-contacts`).

If no rep was found in any transcript for a given award, note it plainly rather than leaving the cell ambiguous.

---

## Step 7: Offer Export and Next Steps

After rendering, offer:

1. **Export to CSV** — agency, project, vendor, value, all three dates, pain-to-award window, rep name, buyer contacts, source links
2. **Draft outreach** — hand qualifying timelines to `signal-outreach`; for competitor-won awards this is the displacement angle ("saw [Vendor] renewed with [Agency] — here's what we'd do differently")
3. **Coverage gaps** — for organizations where a node came back "Not Indexed," flag this as a `territory-monitor` candidate so future procurement activity on that org is caught earlier
4. **Expand** — rerun for additional states or a longer lookback window

---

## Key Rules

- Always gather state(s), lead count (N), and vendor lens before running any search. Never default to a hardcoded geography.
- Load `cloverleaf-signal-search` first, every time — the `states` bug on document search and the 25-meeting cap on keyword search will silently break this skill's backward-tracing logic if ignored.
- **This skill intentionally does not apply Guardrail 1 (pain-vs-procurement stage filter)** from `cloverleaf-signal-search`. Awards are the starting point here, not a rejected late-stage signal.
- **The vendor guardrail (Step 2b) is narrower than Guardrail 0** elsewhere in this kit: discard only when the awarded vendor is the vendor lens itself. A named competitor, at any stage, is the product — never discard for that reason.
- Cap at N timelines. If more qualifying awards exist, keep the top N and state how many were set aside.
- Never render a timeline card without at least one confirmed node (the award). No confirmable award, no card.
- Never fabricate a vendor name or contact — if not present in source text, the field reads "Not found in transcript."
- Missing nodes render with dashed placeholders and get called out explicitly as a coverage-gap finding, not hidden.
- Reserve `get-meeting-transcripts` / `get-document` for confirmed candidates only — never call them speculatively across a wide backward scan. This mirrors the enrichment-only rule for `get-meeting-transcripts` everywhere else in this kit.
- Never pass `states` to `run-document-keyword-search`. Scope by `organization_id` instead.
- If quoting a pain-point excerpt, keep it short and attributed (speaker + meeting), consistent with this kit's general copy conventions — this is sales intel for internal use, not a publishable transcript reproduction.
- No em dashes.
- Every confirmed node carries a meeting or document ID and, where the platform supports it, a direct link. Nothing confirmed should be undocumented.
