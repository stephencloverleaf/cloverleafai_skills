---
name: government-entity-profile
description: >-
  Build a deep, trackable ACCOUNT PROFILE for ONE named government entity — a city,
  county, school district, utility, special district, state agency, or federal
  department — seen through the lens of a specific vendor the user sells for. Use this
  whenever the user wants to "profile," "build an account plan for," "go deep on," "what's
  happening at," or "everything on" a single jurisdiction, or names one entity and one
  vendor and wants the opportunities, contacts, meetings, and budget in one place. This is
  the ENTITY/account view: pick one government body, mine its full Cloverleaf meeting
  history, cluster the discussion into named opportunities, enrich with web + Apollo.io, and
  render a branded HTML dossier. Distinct from `cloverleaf-signal-search` (nationwide topic
  sweep) and `opportunity-enrichment` (one signal).
---

# Government Entity Profile (single-account dossier)

## What this is

The rest of the suite runs a vendor-centric, nationwide funnel. This skill runs the
opposite axis: fix on **one government entity**, view it through **one vendor's** lens,
and produce a complete account picture — every relevant discussion, who said it, what it
might be worth, and what to do next.

## Inputs — elicit two things

1. **The government entity.** A single named jurisdiction. Ask for the state if ambiguous.
2. **The vendor lens** — the company the user is selling for on this account. Confirm
   explicitly; do not default.

### Get the vendor lens right
Run **`vendor-profile`** on the vendor first (or pull from
`vendor-profile/references/term-banks.md`). The vendor decides which meeting topics are
opportunities.

## The research spine

### Step 1 — Resolve the entity to an org ID
`lookup-organization` is embedding-ranked and name-sensitive. Try several forms:
- City: `"Dallas City Council"`, `"City of Dallas"`, `"Dallas, TX"`
- County: `"Travis County"`, `"Travis County Commissioners Court"`
- District: full legal name AND shortened form
- School: `"<District> Independent School District"`, `"<District> ISD"`

### Step 2 — Walk the entity's meeting history
`list-organization-meetings` (newest-first, paginated). Use `title` filter to jump to
high-value meetings: `"budget"`, `"workshop"`, `"finance"`, `"technology"`.
Note the coverage span — this becomes the "coverage_note."

### Step 3 — Targeted keyword passes
Layer the vendor's pain terms via `run-meeting-keyword-search` with `states` filter,
then keep only hits matching your org. Run pain terms first, competitor/incumbent names
second (displacement pass). Use `daysBack` 180-365 for account profiles.

All results go through the three guardrails from `cloverleaf-signal-search`:
Guardrail 0 (own-vendor), Guardrail 1 (stage filter), Guardrail 2 (specificity).

Also run `run-document-keyword-search` (pass `states`; the old 500 bug is fixed) for dollar
figures, RFP/resolution language, and named-vendor contract items.

### Step 4 — Deep dive: older meetings + key influencers
Walk backward in time. A topic raised across three meetings over eight months is a live
initiative with a trajectory. Collect recurring speakers — the person who keeps raising
cybersecurity is your champion; the budget-line owner is your economic buyer.

### Step 5 — Enrich off-platform
Reuse `opportunity-enrichment`'s method: web search for budget, fiscal calendar, grants,
staff directory; Apollo.io for the vendor side, larger agencies, and contact confirmation.
(ZoomInfo was retired 2026-08-11 and its MCP is disconnected — see the `enrichment-provider` skill.)

## Cluster meetings into named opportunities

Group matched discussion into opportunity threads:
- Plain name: "Cybersecurity audit follow-up & pen-testing gap"
- Attach meetings (timeline), recurring speakers (champion/buyer), stage, fit,
  next action, value estimate (labeled est.)
- **Score** 0-100: named budget-owning speaker (+30), contact info (+25),
  recency/active decision (+20), specificity & vendor fit (+25)
- **Stage**: Discovery -> Budgeting/pre-RFP -> RFP imminent -> RFP open ->
  Awarded -> Cold
- Map MEDDPIC where possible

## Output — profile JSON, then render

Assemble into a profile JSON with: `entity`, `vendor_lens`, `opportunities`,
`contacts`, `meetings`, `budget_findings`, `grants`, `sources`.

**Render** using `signal-dashboard`'s bundled `build_dashboard.py` for the signal
cards, or build a custom HTML dossier with these sections:
- Header + coverage stats
- Opportunity tracker (stage-column board with scored cards)
- Contacts directory (name, title, role-in-deal, email/phone, source)
- Meeting library (date, title, key quote, video deep-links)
- Budget & funding (with verified/unverified markers)

Brand palette: use the official Cloverleaf colors documented in `signal-dashboard` — Ink Navy `#1B232E`, Sky accent `#CCF1FD` / `#A9E3F4`, Cream `#F3F1EA`. **There is no brand green**, and the logo is black or white only (never recolored or a stand-in shape).

## Honesty rules (non-negotiable)
- Never fabricate a contact, title, email, phone, budget figure, grant, RFP,
  or meeting link.
- Mark every unverified item. Deal-value estimates must say "est."
- If coverage is thin, say so up front.
- Distinguish verbatim quotes (Cloverleaf, public record) from inference
  (your clustering) from web-sourced data (budget, directory).

## Hand off
- **`signal-outreach`** — draft outreach quoting a recurring speaker.
- **`signal-dashboard`** — if widening to the vendor's whole territory, the
  same signals render as the nationwide card view.
