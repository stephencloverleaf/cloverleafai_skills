---
name: police-chief-transitions
description: >-
  Find newly appointed or incoming police chiefs in Cloverleaf government-meeting
  data and check them against the user's Salesforce contacts to surface people
  they already know who are changing jobs, plus warm paths into the agencies
  involved. Use this whenever the user wants to spot police-chief transitions,
  new/incoming/interim chiefs, leadership changes in law enforcement, or "people
  I know who are moving into new roles" as a prospecting signal — even if they
  don't name Cloverleaf or Salesforce explicitly. Trigger on phrases like "any
  new police chiefs", "who's starting a new chief role", "check for chief
  transitions in [states]", "are any of my contacts becoming chiefs", or "run
  the chief signal".
---

# Police Chief Transition Signals

## What this does and why it matters

The job is to answer: **which people the user already knows are moving into new
police-chief roles — and which agencies with a new chief are ones the user already
has a foot in?** A contact changing jobs (or a new chief at an agency where the user
knows someone) is a warm prospecting signal.

Two-sided flow:
1. **Cloverleaf** surfaces new/incoming/interim chief mentions in public government
   meetings.
2. **Salesforce** tells us whether each chief — or their new agency — connects to a
   known contact.

This skill is **read-only**: it reports findings and never writes to Salesforce.

## Inputs to gather first

- **Geographies.** State level for now (Cloverleaf's meeting search filters natively by
  state). Ask which states/provinces if the user hasn't said; accept 2-letter codes or
  full names. (City/county/agency-level targeting is a planned future iteration — don't
  promise it.)
- **Time window.** Default to the **last 14 days**. Mention the default when asking about
  geography so the user can override it in the same reply.

If the user already gave states and/or a window, don't re-ask — just confirm as you go.

## Step 1 — Find new-chief mentions in Cloverleaf

Use `Cloverleaf AI:run-meeting-keyword-search` scoped to the requested `states` and window
(`daysBack: 14` by default, or `startDate`/`endDate` for a range).

Starting terms (tune by result volume):

```
"new police chief", "police chief appointed", "police chief sworn in",
"incoming police chief", "interim police chief", "next chief of police",
"chief of police appointed", "named police chief"
```

Recall matters more than precision — Step 2 filters noise:
- Too few results → broaden to `"police chief"` / `"chief of police"` and lean on Step 2,
  or widen the window.
- Too many → tighten with `mustIncludeTerms: ["chief"]` and consider `proximity`.
- De-duplicate by person; one chief may appear in several meetings.

## Step 2 — Extract the chief's details

Names usually live in the transcript, not the search hit. Pull context and extract, per
candidate: **name** (note partial/first-only/truncated names explicitly), **jurisdiction
+ state** (from the meeting's organization), **status** (started vs. starting soon), and a
**meeting reference** (date + link).

Name-recovery rules learned the hard way:
- To enrich a name, use the **state-scoped** `run-meeting-keyword-search` or pull the
  **specific meeting's** transcript via `get-meeting-transcripts`. **Do NOT run an
  unscoped `search-meetings` for name recovery** — without `states` it floods with
  nationwide noise (unrelated people, even movie transcripts).
- Transcripts garble names. Expect first-only ("Ron"), surname-only ("Davila"), and
  truncated ("Gerald L.") forms. Surface the chief anyway; don't discard for a missing
  name — flag what's missing and let scoring handle the uncertainty.
- **Disambiguate police vs. fire/other chiefs.** "Chief [X]" hits include fire chiefs and
  assistant chiefs; require police/PD context before treating someone as a police chief.

Drop hits that aren't real transitions (a chief merely speaking, a budget line, a
nameless "we'll soon hire a chief"). Keep nameless-but-real transitions in a **separate
bucket** (Step 5) rather than mixing them into the matchable list.

## Step 3 — Cross-reference Salesforce

Resolve the org first: call `salesforce:get_username`. If no default target org resolves,
call it with `defaultTargetOrg: false` and `defaultDevHub: false` to use the allow-listed
org. **Tell the user which org/alias you're querying and why** (the connector requires
this). Never guess a username/alias. Pass the resolved `usernameOrAlias` and a working
`directory` to `run_soql_query`.

For each chief, look for **two kinds of signal** — both feed the score:

**(a) Person-level match** — a contact whose name plausibly matches the chief. This is the
primary goal: the contact may *be* the person taking the new role.
```sql
SELECT Id, Name, FirstName, LastName, Title, Account.Name, MailingCity, MailingState
FROM Contact WHERE LastName IN ('Davila','Harris',...)
```
Match on last name first; evaluate first name after. For first-only/truncated names, a
`FirstName` query is allowed but expect noise — cap confidence accordingly.

**(b) Jurisdiction adjacency (secondary signal)** — contacts at the chief's *new* agency,
regardless of name. A warm path into that agency, and — critically — sometimes the chief
themselves under a garbled/partial name (e.g., an "Assistant Police Chief" at the same
agency being promoted to Chief). Match the jurisdiction token against `Account.Name`:
```sql
SELECT Id, Name, Title, Account.Name, MailingCity, MailingState
FROM Contact WHERE Account.Name LIKE '%Kerrville%'
```
**Escape apostrophes** in any name/token (`O'Brien` → `O\'Brien`). Batch where possible.

Data reality in this org: `MailingCity`/`MailingState` are **null on nearly all
contacts**. The reliable corroborators are **`Account.Name`** (encodes the jurisdiction)
and **`Title`** (law-enforcement roles). Treat location as a bonus when present, not a
dependency.

## Step 4 — Confidence scoring

Score each surfaced (chief → contact) pair with three 0–100 sub-scores, then combine.

- **NameScore** — identity match. Exact first+last ≈ 100; last + first-initial ≈ 85;
  surname-only ≈ 55; first-only or truncated ≈ 25; phonetically-near but uncertain
  (e.g. "Gerald" vs "Jerel") ≈ 40; no name overlap = 0 (pure adjacency rows).
- **AccountTitleScore** — `Account.Name` corresponds to the chief's jurisdiction or to law
  enforcement generally (+), and `Title` is a law-enforcement role — chief, deputy/
  assistant chief, sergeant, officer, sheriff (+). Unrelated account/title pulls it down.
- **LocationScore** — `MailingCity`/`MailingState` matches the meeting jurisdiction. Almost
  always null here → contributes 0 when absent (do not penalize, just no boost).

Combine (all weights tunable — state them when presenting results):

```
CorroborationScore = 0.7 * AccountTitleScore + 0.3 * LocationScore
FinalConfidence     = 0.55 * NameScore + 0.45 * CorroborationScore
```

**Promotion-pattern boost (override).** The highest-value pattern is an internal
promotion the name match would otherwise miss: a contact **at the chief's new agency**
holding a **deputy or assistant chief** (or similar second-in-command) title, when that
agency has just sworn in / announced a new chief. When this pattern holds, **floor
FinalConfidence at ~80** and label the row **"likely promotion"** — even if NameScore is
low because the transcript garbled or truncated the chief's name. Rationale: the linear
blend under-rates this case (a garbled name drags NameScore down, location is usually
null), yet it's the strongest "someone you know is moving" signal the skill can produce.
Note explicitly in the "why" that the name is unconfirmed so the user can verify.

Crucial nuances:
- A person who is **moving jobs usually still shows their OLD account/title** in the CRM.
  So for a *person-level* match, jurisdiction overlap with the NEW post is NOT expected —
  **title relevance** (they're in law enforcement somewhere) is the real corroborator, not
  account-jurisdiction match. Don't penalize a strong name match for being at a different
  agency; that's consistent with a move.
- For a **jurisdiction-adjacency** row, NameScore is low/zero, so FinalConfidence is driven
  by AccountTitleScore. Watch for the high-value special case: a law-enforcement contact at
  the chief's new agency whose name is phonetically near the (garbled) chief name — that
  may be a real promotion the name match missed. Flag it prominently.

Label every surfaced row as **Person match** or **Jurisdiction adjacency**, give a short
concrete "why" citing the sub-scores, and **sort all rows by FinalConfidence descending**.

## Step 5 — Present the results

Lead with a one-line summary: chiefs found across the states/window, how many produced a
person match, how many produced a jurisdiction adjacency.

Then a markdown table sorted by confidence:

| Confidence | Type | Chief (new role, state) | Status | Matched contact (title @ account) | Why (sub-scores) | Meeting (date) |
|---|---|---|---|---|---|---|

- State the weights used so the user can recalibrate.
- Then a brief **bucket of nameless/non-transition mentions** (jurisdiction + state, or a
  count) so coverage is visible — but keep the spotlight on scored matches.
- Include meeting links so every signal is verifiable.

## Boundaries and future direction

- **Read-only.** No writes to Salesforce (no contacts, tasks, notes) unless the user
  explicitly asks in a later turn — and confirm before any write.
- **State-level for now.** City/county/agency targeting, natural-language search, and CSV/
  file export are expected future iterations — don't imply they exist yet.
- **Handle tool hiccups gracefully.** Searches can return errors (e.g. a 500 from document
  search) or empty sets; note it, fall back (different terms/source), and keep going rather
  than stalling.
