---
name: government-entity-profile
description: "Build a deep, trackable account profile for one named government entity (a city, county, school district, utility, special district, state agency, or federal department) seen through the lens of one vendor the user sells for. Use whenever the user wants to profile, build an account plan for, go deep on, get everything on, or asks what is happening at a single jurisdiction, or names one entity and one vendor and wants the opportunities, contacts, meetings, and budget in one place. This is the entity view: fix on one government body, mine its full Cloverleaf meeting history, cluster the discussion into named opportunities, enrich it, and render a dossier. Distinct from cloverleaf-signal-search, which sweeps a topic nationwide, and from opportunity-enrichment, which builds out one signal."
---

# Government entity profile

## What this is

The rest of the kit runs a vendor centric, nationwide funnel. This skill runs the other
axis: fix on one government entity, view it through one vendor's lens, and produce a
complete account picture of what is being discussed, who said it, what it might be worth,
and what to do next.

Tool parameters and limits are in `cloverleaf-mcp-operations`. Load it before searching.

## Inputs

Elicit two things and confirm both. Do not default either.

1. **The entity.** One named jurisdiction. Ask for the state when the name is ambiguous.
2. **The vendor lens.** The company the user is selling for on this account. The vendor
   decides which meeting topics count as opportunities.

Run `vendor-profile` on the vendor first, or pull its `references/term-banks.md`, so you
are searching the pain in the vendor's category rather than the vendor's name.

## Step 1: resolve the entity

`lookup-organization` is embedding ranked and name sensitive, so try several forms and
read the whole returned list.

- City: "Dallas City Council", "City of Dallas", "Dallas, TX"
- County: "Travis County", "Travis County Commissioners Court"
- District: the full legal name and the short form
- School: "<District> Independent School District", "<District> ISD"

Check `meeting_count` on each match and skip zero count orgs. When a place name misses,
the record is often filed under the body rather than the place. One org record can also be
a mixed feed of several governing bodies sharing a cable access channel, so confirm the
body from the meeting content before you build a profile on it.

## Step 2: walk the meeting history

`list-organization-meetings(organizationId)`, newest first and paginated, with the `title`
filter to jump to high value meetings: budget, workshop, finance, technology. Note the
coverage span and the meeting count; that becomes the coverage note in the output. A
channel with one or two ingested meetings cannot support a trend claim, and the rep should
be told not to expect follow up.

## Step 3: targeted passes

Run the vendor's pain terms through `run-meeting-keyword-search` with `states`, then keep
only hits on your org id. Run competitor and incumbent names second, one name per query,
for the displacement pass. Use `daysBack` 180 to 365 for an account profile.

Run `run-document-keyword-search` on the same terms (pass `states`) for dollar figures,
resolution language, and named vendor contract items. `document-signal-search` owns the
vocabulary rules that keep this from returning boilerplate.

Everything goes through the four guardrails in `cloverleaf-signal-search`: own vendor,
stage, minimum specificity, and who owns the problem.

## Step 4: go backward and find the influencers

Walk backward in time. A topic raised across three meetings over eight months is a live
initiative with a trajectory, not a one off comment. Collect recurring speakers: the
person who keeps raising the problem is your champion, and the budget line owner is your
economic buyer. Treat every name as unconfirmed until you check it against
`list-contacts`, published minutes, or a signature block.

## Step 5: enrich off platform

`opportunity-enrichment` carries the full enrichment procedure (jurisdiction profile,
budget and fiscal calendar, procurement stage, grants, decision makers). Follow it rather
than reinventing it.

Three Apollo tools cover the enrichment this skill needs directly:

- `apollo_organizations_enrich` for firmographics on the vendor side or a large agency.
- `apollo_mixed_people_api_search` to find people by title at an organization.
- `apollo_people_match` to confirm one named person and reveal contact details.

Two caveats. Apollo's usage stats tool misreports credit exhaustion, so check
`apollo_users_api_profile` before concluding a credit type is used up. And a phone reveal
resolves asynchronously, so the number may not be in the first response.

Apollo is the enrichment provider for this kit. ZoomInfo was retired on 2026-08-11 and its
server is disconnected; calls to it return nothing rather than failing, so any instruction
that still names it is stale.

For the government side, Cloverleaf's own `list-contacts` is usually better than Apollo:
it is role keyed to civic titles (Head of IT, Head of Purchasing, Top Appointed Executive)
and carries direct numbers. Check the roster for jurisdiction contamination before
presenting it; rosters have mixed two governments under one org id.

## Cluster into named opportunities

Group the matched discussion into threads and give each a plain name, for example
"Cybersecurity audit follow up and pen testing gap".

Each opportunity carries: its meetings as a timeline, the recurring speakers with their
role in the deal, a stage, the vendor fit, a next action, and a value estimate labeled as
an estimate.

- **Score** out of 100: named budget owning speaker (30), contact details (25), recency
  and an active decision (20), specificity and vendor fit (25).
- **Stage:** discovery, budgeting or pre-RFP, RFP imminent, RFP open, awarded, cold.

## Output

Assemble a profile object with `entity`, `vendor_lens`, `opportunities`, `contacts`,
`meetings`, `budget_findings`, `grants`, and `sources`, then render it.

Use `signal-dashboard` for the rendering and the brand palette, either through its bundled
build script for the signal cards or as a custom dossier with these sections: header and
coverage stats, an opportunity tracker as a stage column board of scored cards, a contacts
directory (name, title, role in the deal, email, phone, source), a meeting library (date,
title, key quote, link), and budget and funding with verified or unverified markers.

Cite `cloverleaf_url` on every meeting and document. Never construct a link.

## Honesty rules

- Never fabricate a contact, title, email, phone, budget figure, grant, RFP, or link.
- Mark every unverified item, and label deal value estimates as estimates.
- Say up front when coverage is thin.
- Keep three things visibly distinct: verbatim quotes from the public record, your own
  clustering and inference, and web sourced data such as budgets and directories.
- An insight sentence is never a quote. Anything in quotation marks comes from a
  transcript, read in context.

## Hand off

- `signal-outreach` drafts outreach quoting a recurring speaker.
- `signal-dashboard` renders the same signals as a card view if you widen to the vendor's
  whole territory.
- `territory-monitor` keeps the account under standing coverage after the profile ships.
