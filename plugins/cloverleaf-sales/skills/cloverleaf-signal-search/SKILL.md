---
name: cloverleaf-signal-search
description: "Find pre-RFP buying signals in live government meeting transcripts with Cloverleaf, qualify them against the guardrails that keep bad leads off a board, and pull the decision maker roster for every jurisdiction that survives. Use this any time the task involves searching Cloverleaf, finding leads or signals in public meetings, council or board discussions, or building public sector pipeline (federal, state, local, or education) from meeting intelligence, including when the user only says find me some signals, search for ransomware discussions, what are cities saying about X, or names a jurisdiction. This is the first step of the demo workflow: signal-dashboard, opportunity-enrichment, and signal-outreach all build on what it produces. Tool parameters live in cloverleaf-mcp-operations; this skill owns strategy, scoring, and the guardrails."
---

# Cloverleaf signal search

## What you are working with

Cloverleaf processes full, unedited live meeting audio and video from tens of thousands
of government organizations, not scraped written minutes. A search returns the words an
official said and when they said it, and `list-contacts` returns the verified roster for
that jurisdiction. Find the signal, then pull the roster: that two step pattern is the
fastest path to an outreach ready lead in this kit.

Coverage is the whole public sector. Cities, counties, school boards, special districts,
state agencies, and federal departments are all in scope, across US states and
territories and Canadian provinces. Federal is a thinner source than state and local
because local bodies argue in open session repeatedly, but it is covered. Never write
that it is not.

Tool parameters, limits, and response shapes live in `cloverleaf-mcp-operations`. Load it
before calling anything. This skill owns what to search for, what to reject, and how to
rank what is left.

## Search order

**Step 1. `search-insights(searchTerm, states)`.** Cloverleaf already runs an automated
insights pass on the account, so checking it costs no search credit and often surfaces a
scored signal a manual sweep would take several calls to rediscover. Pass `states`,
because insights generate nationwide. Read the Signal Match score and the summary, but
treat the score as a label on everything ingested rather than a selection threshold, and
skip 0/10 gate excluded rows without re-litigating them. If the rep you are working for
is not the authenticated account, pass their numeric `userId`.

**Step 2. Fall back to a fresh sweep** only when insights are absent, stale (call it more
than 90 days), or fail the guardrails below. Use `run-meeting-keyword-search` for precise
vocabulary and `search-meetings` for open ended intent.

**`get-meeting-transcripts` is never part of discovery.** It belongs to
`opportunity-enrichment`, on the three to five signals that already cleared scoring. If
you are calling it before you have a shortlist, you are on the wrong step.

## Write queries that hit

Officials describe problems and projects, not vendor names. Search the pain. The same
term list works as `searchTerm` for `search-insights` and as `terms` for
`run-meeting-keyword-search`; for `search-meetings`, turn the theme into a sentence
describing the buyer's situation.

Run two focused searches rather than one combined query, because the signal to noise
ratio is much better. Prefer compound terms over ambiguous single words: a bare firewall
sweep returns fire rated walls from zoning boards.

Read `references/query-craft.md` for the cybersecurity and network term banks, the
anchoring recipe, and the vendor name rules that decide whether a zero result means
anything.

## The four guardrails

Apply these in order, to every result, from every source including `search-insights`. A
high Signal Match score says nothing about whether a signal passes them.

### Guardrail 0: own vendor

Does the transcript or insight name the vendor you are prospecting for as already
contacted, demoed, or quoted? Check against the `own_vendor_names` list `vendor-profile`
produces, company name and product name both, because officials say either.

If yes, reject outright, whatever the budget, authority, or recency looks like. That
jurisdiction is not a discovery for that vendor's sales org; their own rep already has
visibility, the sales cycle is already open, and presenting it as newly found pre-RFP
pain undercuts the entire pitch.

A competitor or incumbent named as the system currently in use, with no replacement
chosen, is a different thing and is often the best signal you can find.

This is also why you never build a signal by searching a vendor's own company name. That
returns footprint mentions: their name in a payment register, an approved vendor list, a
contract amendment log, or a signed agreement. The vendor's name belongs in this
exclusion check and nowhere else in a discovery query.

### Guardrail 1: stage, pain over procurement

The product is the spoken window before a jurisdiction has decided what to do. Once an
RFI or RFP is posted, a hearing is called, or a contract is awarded, the opportunity is
public, contested, and available on procurement portals to everyone who pulled the same
feed.

- **Early stage pain, the target.** An official voicing a problem, a failing system, a
  compliance gap, or an incident, with no solution chosen. Up-rank hard.
- **Mid stage, marginal.** "We are forming a committee to look at options", "we should
  budget for this next year". Keep only when the pain is specific and you can get in
  before requirements lock.
- **Late stage, reject.** An RFI or RFP issued, a hearing scheduled, a contract awarded,
  a vendor already selected, or a project in kickoff. Do not feature these as
  opportunities, even with a named speaker and a full roster attached.

`document-signal-search` and `rfp-timeline` work the later stages on purpose. This skill
does not.

### Guardrail 2: minimum specificity

A signal needs at least one of: a named speaker with a title, a specific incident,
system, project, or capability gap, or a dollar figure, grant reference, or budget line
item. With none of the three it is noise. "Cybersecurity is important to our community"
is not a signal.

### Guardrail 3: who owns the problem

Name the buyer. Do the people speaking own the system that failed, and do they hold
budget for the category being sold? Legislators conducting oversight, public commenters,
and advocacy witnesses fail this test even when the quote is specific, recent, and
squarely on topic.

The test that catches it: could the rep's first email name a plausible recipient, and
would that person care? An oversight committee absorbing political backlash over an
agency's data exposure is not that agency's security buyer and holds no security budget.
If you cannot name who receives the email and why, demote the signal to background rather
than leading with it.

Watch two related traps. A signal can be filed under one organization while the pain
belongs to another (a commissioner's liaison report about a separate library
consortium's breach). And a same-name collision is not the same company: a tax penalty
item for an unrelated firm with a security vendor's name is not a signal.

## Scoring what survives

Once a result clears all four guardrails, rank it on:

1. **Named speaker with budget authority.** IT Director, CISO, City or County Manager,
   CFO. Pull their email and phone from `list-contacts`; transcript results do not carry
   contact details.
2. **Specificity of the pain.** A concrete failing system, incident, audit finding, or
   capability gap.
3. **Recency.** Inside 30 days is hot, 30 to 90 days is warm, 90 to 180 days is
   background.

Down-rank when `person` is null and the text is generic. Up-rank a named speaker plus a
specific unsolved problem plus a matching roster contact plus a recent date.

Verify the category, not only the facts, before featuring anything. A score measures how
loud the problem is, never whether it is yours: a well quoted, correctly transcribed
power supply failure is a 7/10 that no network security vendor can sell into.

## Contacts

Transcript results carry `{name, organization, title}` at most, so `list-contacts` is the
only path to an email or a phone number.

```
1. lookup-organization("Travis County, TX")   # read the whole list, check meeting_count
2. list-contacts(organizationId = 1242, limit = 50)
3. Filter on role: Head of IT, Head of Purchasing, Head of Finance, Top Appointed
   Executive, Top Elected Official
```

For a county wide sweep, skip the org id and pass `countyName` with `stateName`. Roster
coverage, deduping, empty rosters, and the jurisdiction contamination check are in
`cloverleaf-mcp-operations` under `references/recipes.md`.

## Territory sweep, one off

`run-meeting-keyword-search` with `states` and `terms` is the cleanest path for a rep's
territory. State is the finest geographic scope this tool has, so for county or city
targeting resolve the org with `lookup-organization` and walk it with
`list-organization-meetings`, or filter the `meetings[]` array client side on its
`county` field.

For standing weekly coverage, a seen-id ledger, and the digest format, use
`territory-monitor`. It owns the recurring form of this sweep and applies these same
guardrails.

## Before you present

The defect classes that survive into polished output are catalogued in
`cloverleaf-mcp-operations` (rules 5 through 9). The four that bite hardest here:

- **Confirm the jurisdiction from transcript content**, not the org label. Whole channels
  have been filed under the wrong city, and one meeting labeled Indiana was Tasmania.
- **Confirm every speaker name.** A populated `person` block is inference, not data. ASR
  mangles names ("Hellman Kava" for Helmin Caba, "Dela Flore" for Della Flora). Resolve
  the real name from the roster plus a quick web check before it reaches a rep, a call
  sheet, or outreach copy.
- **Re-derive deep link timestamps from the transcript.** Search payload timestamps have
  run 40 to 65 seconds off, which opens the link mid unrelated sentence in front of the
  customer.
- **An insight sentence is never a quote.** Corroborating one insight against another
  insight confirms nothing; only the transcript does.

Every signal you show carries org name, state, meeting date, a short verbatim quote, the
timestamp, and the `cloverleaf_url` as the link. Never construct a link yourself.

Read `references/worked-examples.md` for one clean pass and three rejects, each traced to
the guardrail that should have caught it. Read it when you are unsure whether a
borderline signal qualifies.

## Hand off

- `signal-dashboard` renders scored signals into a sortable board with contact cards.
- `opportunity-enrichment` fills in budget, timing, and buyer context, and is where
  `get-meeting-transcripts` gets pulled on the shortlist.
- `signal-outreach` drafts the message that quotes the official.
- `document-signal-search` pairs spoken pain with the procurement side evidence.
- `territory-monitor` turns a one off sweep into standing coverage.
- `vendor-profile` produces the term banks and the `own_vendor_names` list Guardrail 0
  depends on. Run it first on any new logo.
