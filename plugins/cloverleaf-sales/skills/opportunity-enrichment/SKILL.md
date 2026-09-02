---
name: opportunity-enrichment
description: >-
  Take a Cloverleaf signal and build it into a full government opportunity by filling
  gaps with web search and the Apollo.io MCP — jurisdiction profile, budget/fiscal
  timing, procurement stage, grants (e.g. SLCGP), and the decision-makers to sell into.
  Use this whenever the user wants to "flesh out," "research," "build out," "qualify,"
  or "add context to" a signal or lead, or asks "who do we call / what's their budget /
  is there an RFP." Step 3 of the demo workflow (search → dashboard → ENRICH → outreach).
  Focus is the GOVERNMENT buyer side. Outputs fields that drop straight back into the
  dashboard and feed the outreach skill.
---

# Opportunity Enrichment (government side)

## The job

A Cloverleaf signal tells you a jurisdiction has a need and (often) who raised it. To make
it a real opportunity a rep can work, you fill four gaps:

1. **Jurisdiction profile** — type (city / county / school district / utility / state agency), population, region, governing form.
2. **Money & timing** — budget size, IT/cyber budget if findable, **fiscal-year calendar** (when the budget is actually set — this is the clock), and any **grant** (especially **SLCGP**, the State and Local Cybersecurity Grant Program).
3. **Procurement stage** — pre-RFP discussion → budgeting → RFP imminent → awarded. This sets urgency.
4. **Decision-makers** — IT Director / CIO / CISO, City or County Manager, Finance Director, procurement officer, and the relevant elected committee. Names, titles, email, phone.

The signal already hands you some of this for free (the quote, the speaker, sometimes their
email/phone). Enrichment fills the rest.

## Source order: cheap and reliable first

Spend effort (and Apollo credits) in this order. Stop when the opportunity is workable.

### 1. Pull the full transcript, then mine it
This is where `get-meeting-transcripts(meetingId)` belongs in the workflow — not during
discovery, but here, first, on each of the 3–5 signals that already cleared scoring in
`cloverleaf-signal-search`. It's free, it's already-available data, and it's the
highest-signal-per-effort step in enrichment, so it comes before spending a web search or
an Apollo credit.

The excerpt that came back from discovery (`search-insights`, `run-meeting-keyword-search`,
or `search-meetings`) is a clipped window. The full transcript often adds a dollar figure
said a minute later, a second named speaker, or the fuller shape of the timeline that the
excerpt cut off. The `person.contact` block in the original result may already give you a
named decision-maker with email and phone — pull that plus whatever the full transcript
adds (project name, dollar figure, prior incident, timeline like "budget workshop" or
"audit last year") before searching anything else.

### 2. Web search — best for the jurisdiction and the project
For small and mid-size local governments, the open web beats any contact database, because
their budgets, agendas, staff directories, and grant awards are public. Run these (adapt the
jurisdiction name):

- `"<Jurisdiction>" adopted budget FY2027 cybersecurity OR information technology`
- `"<Jurisdiction>" CIP OR capital improvement information technology`
- `"<Jurisdiction>" RFP OR RFQ cybersecurity OR "managed security" OR "penetration testing"`
- `"<Jurisdiction>" SLCGP OR "cybersecurity grant" award`
- `"<Jurisdiction>" IT director OR CIO OR "information security" staff directory`
- `"<Jurisdiction>" ransomware OR data breach` (news — prior incident = urgency)
- `"<State>" fiscal year start local government` (to time the budget cycle)

Use `web_fetch` on the jurisdiction's `.gov` site for the staff directory, budget PDF, and
agenda/minutes pages. Pull names, titles, and the budget number from primary sources — do
not estimate them. If you can't verify a figure, say so and leave it for the rep to confirm.

### 3. Apollo.io MCP — best for the vendor side and for confirming named people
> **ZoomInfo was retired 2026-08-11 and its MCP is disconnected — calls to it return nothing,
> silently. Apollo.io replaced it. The `enrichment-provider` skill is the authority here and
> wins if this section is ever reverted by a plugin update.**

Apollo's strength is commercial firmographics. Government coverage is **thinner than ZoomInfo's
was**, and thinner for small jurisdictions than large ones — so on public-sector work the entity's
own staff directory and adopted budget usually beat it. Use Apollo for the vendor side of the deal,
for larger agencies and authorities, and to confirm a named person.

These tools are deferred in Claude Code — load them with ToolSearch before calling. Use the
bare tool names below. Every account gets its own Apollo server ID, so never hard-code an
account-specific MCP server prefix.

- **Find the entity or vendor:** `apollo_mixed_companies_search` by name; or
  `apollo_organizations_enrich` when you already have the domain.
- **Get the right people:** `apollo_mixed_people_api_search` on the organization plus titles —
  "Chief Information Officer", "Chief Information Security Officer", "IT Director",
  "Information Technology", "Procurement" — and/or seniority filters. Per the territory playbook,
  run contact searches in **two passes** (one by department/level, one by title keyword);
  combined filters underperform.
- **Confirm one known person:** `apollo_people_match` (bulk: `apollo_people_bulk_match`).
- **Hiring as an urgency tell:** `apollo_organizations_job_postings`. An open security or network
  role is both a budget signal and a reason to reach out now. This is the nearest replacement for
  ZoomInfo's scoops/news feed — there is no direct equivalent, so do not promise one.
- **Check the CRM first:** `apollo_contacts_search` before spending anything new.

**Honesty rule:** if Apollo has thin coverage for a small jurisdiction, don't force it —
say "Apollo coverage is thin here; the city directory is the better source" and use the web.
Never invent a contact, title, or budget to fill the brief.

## Frame it the way the rep will use it (MEDDPIC)

Stephen qualifies on MEDDPIC. Map what you find so the brief is sales-ready, even if partial:

- **Metrics** — the cost of the pain (downtime, audit findings, ransom exposure).
- **Economic buyer** — usually the City/County Manager or Council; finance director controls the purse.
- **Decision criteria / process** — RFP vs. cooperative purchase (e.g. NASPO, Sourcewell), board vote cadence.
- **Identified pain** — the exact quote from the meeting (you already have it).
- **Champion** — the official who raised it (often your signal speaker).
- **Competition** — any incumbent or product named in the meeting (a named competitor = active evaluation).

Leave a field blank rather than guessing. A partial MEDDPIC with sourced facts beats a complete one full of fiction.

## Output: extend the signal (so it round-trips)

Append these fields to the signal object so the dashboard and outreach skills pick them up:

```jsonc
{
  // …original signal (jurisdiction, quote, speaker, email, phone, terms)…
  "jurisdiction_profile": { "type": "city", "population": "~107,000", "region": "Spokane County, WA", "fiscal_year": "Jan–Dec" },
  "money_timing": { "budget_notes": "FY budget workshop held Jun 2026 — funding being set now", "grant": "Check WA SLCGP sub-recipient list" },
  "procurement_stage": "Budgeting / pre-RFP",
  "contacts": [
    { "name": "Chad Knodel", "title": "IT Manager", "email": "cknodel@spokanevalleywa.gov", "phone": "509-720-5055", "source": "Cloverleaf signal" }
  ],
  "meddpic": { "identified_pain": "Ransomware resiliency audit found no network pen testing", "champion": "Chad Knodel", "economic_buyer": "City Manager / Council" },
  "fit": "Active cyber audit cycle with a named gap (pen testing) and budget being set this month.",
  "next_action": "Email Chad referencing the pen-testing gap; check SLCGP eligibility.",
  "sources": ["Cloverleaf meeting 18214101", "spokanevalleywa.gov budget page (verify)"]
}
```

`fit` and `next_action` are one line each and are exactly what the dashboard card and the
outreach draft need.

## Worked example (continuing the Spokane Valley signal)

**Known from the signal (verified):** City of Spokane Valley, WA, Jun 9 2026 Budget Workshop.
Chad Knodel (IT Manager, cknodel@spokanevalleywa.gov, 509-720-5055) said last year's
ransomware resiliency audit "did not include network penetration testing." Erik Lamb
(Deputy City Manager) framed ransomware as an existential operational risk.

**To verify by web (don't guess these):** population and FY calendar; whether Spokane Valley
is a WA SLCGP sub-recipient; the City Manager and Finance Director names; any open or planned
IT/security RFP. Queries: `"Spokane Valley" adopted budget 2026 information technology`,
`"Spokane Valley" SLCGP cybersecurity grant`, `spokanevalleywa.gov staff directory IT`.

**Read:** budgeting-stage opportunity, named champion, named gap, decision-makers in hand —
a clean pen-testing / endpoint / MSSP play. Hand to `signal-outreach`.

## Hand off
Pass the enriched signal to **`signal-outreach`** to draft the email / LinkedIn / call script,
and back to **`signal-dashboard`** so the card now shows budget, stage, contacts, and next step.
