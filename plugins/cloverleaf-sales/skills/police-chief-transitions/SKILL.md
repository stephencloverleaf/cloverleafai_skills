---
name: police-chief-transitions
description: >-
  Finds newly appointed, incoming, or interim police chiefs in Cloverleaf government-meeting
  data, then, when a CRM connector is attached, checks them against the user's contacts to
  surface people they already know who are changing jobs plus warm paths into the agencies
  involved. Read-only: it reports and never writes to a CRM. Trigger phrases: "any new
  police chiefs", "who is starting a new chief role", "check for chief transitions in
  STATE_CODES", "are any of my contacts becoming chiefs", "run the chief signal", or any ask
  about law-enforcement leadership changes as a prospecting signal, even without naming
  Cloverleaf or a CRM.
---

# Police chief transition signals

## What this does

It answers two questions: which people the user already knows are moving into new
police-chief roles, and which agencies with a new chief are ones the user already has a foot
in. A contact changing jobs, or a new chief at an agency where the user knows someone, is a
warm prospecting signal.

Cloverleaf surfaces the transition. A CRM tells you whether the chief or the new agency
connects to a known contact. The CRM half is optional: without one, deliver the transition
list with warm-path suggestions.

## Gather first

- **Geographies.** State level. Cloverleaf search filters natively by state and accepts
  two-letter codes or full names. Ask which states if the user has not said. City, county,
  and agency-level targeting is a future iteration; do not promise it.
- **Time window.** Default to the last 14 days. Mention the default when you ask about
  geography so the user can override it in the same reply.

If the user already gave states or a window, do not re-ask.

## Step 1: find new-chief mentions

Use `run-meeting-keyword-search` scoped to the requested `states` and window. Pass `daysBack`
of 14, or `startDate` and `endDate` for a range. The two cannot be combined. Never omit the
window: with no date the tool looks back seven days.

Starting terms, tuned by result volume:

```
"new police chief", "police chief appointed", "police chief sworn in",
"incoming police chief", "interim police chief", "next chief of police",
"chief of police appointed", "named police chief"
```

Recall matters more than precision, because Step 2 filters the noise.

- Too few results: broaden to "police chief" or "chief of police" and lean on Step 2, or
  widen the window.
- Too many: tighten with `mustIncludeTerms` of `["chief"]` and a `proximity` of about 50.
- `perPage` goes up to 100 with `page`, so paginate rather than accepting the first page as
  the whole answer.
- De-duplicate by person. One chief appears in several meetings. Also de-duplicate meetings
  on organization, title, and date, because the same meeting is ingested under more than one
  ID.

For parameters, limits, and response shapes, see `cloverleaf-mcp-operations`.

## Step 2: extract the chief's details

Names usually live in the transcript, not the search hit. Per candidate, extract the name,
the jurisdiction and state from the meeting's organization, the status (started or starting
soon), and the meeting reference: date plus the `cloverleaf_url` from the payload. Never
build a link yourself.

Name-recovery rules learned the hard way:

- To recover a name, use the state-scoped `run-meeting-keyword-search` or pull the specific
  meeting with `get-meeting-transcripts`. **Do not run an unscoped `search-meetings` for name
  recovery.** Without `states` it floods with nationwide noise.
- **Treat every name as unconfirmed until you check it.** `get-meeting-transcripts` returns
  no speaker on essentially every line, and `run-meeting-keyword-search` populates a person
  block that is sometimes confidently wrong. Confirm against minutes, an official roster, or
  a press release before presenting a name as fact.
- Speech-to-text garbles names. Expect first-only ("Ron"), surname-only ("Davila"), and
  truncated ("Gerald L.") forms. Surface the chief anyway. Flag what is missing and let
  scoring carry the uncertainty.
- **Separate police chiefs from fire and assistant chiefs.** "Chief TOPIC" hits include fire
  chiefs. Require police or PD context before treating someone as a police chief.
- Confirm the jurisdiction from transcript content, not the organization label, which can
  name the wrong place.

Drop hits that are not real transitions: a sitting chief merely speaking, a budget line, a
nameless "we will hire a chief soon". Keep nameless-but-real transitions in a separate bucket
for Step 5 rather than mixing them into the matchable list.

## Step 3: cross-reference the CRM, if one is attached

**This step is conditional.** Run it only when a Salesforce or other CRM connector is
attached to the session. Without one, skip to Step 5 and deliver the transition list with
warm-path suggestions: for each agency, name the roles a rep should approach and why the
transition opens the door.

With Salesforce attached, resolve the org first by calling `get_username`. If no default
target org resolves, call it again with the default-target-org and default-dev-hub flags set
to false to use the allow-listed org. **Tell the user which org or alias you are querying and
why**, which the connector requires. Never guess a username or alias. Pass the resolved
username or alias and a working directory to `run_soql_query`.

For each chief, look for two kinds of signal. Both feed the score.

**(a) Person-level match:** a contact whose name plausibly matches the chief. The contact may
be the person taking the new role.

```sql
SELECT Id, Name, FirstName, LastName, Title, Account.Name, MailingCity, MailingState
FROM Contact WHERE LastName IN ('Davila','Harris')
```

Match on last name first, then evaluate first name. For first-only or truncated names a
first-name query is allowed, but expect noise and cap confidence accordingly.

**(b) Jurisdiction adjacency:** contacts at the chief's new agency regardless of name. That
is a warm path, and sometimes the chief themselves under a garbled name, such as an assistant
chief being promoted.

```sql
SELECT Id, Name, Title, Account.Name, MailingCity, MailingState
FROM Contact WHERE Account.Name LIKE '%Kerrville%'
```

Escape apostrophes in any name or token. Batch queries where possible.

Data reality in this org: `MailingCity` and `MailingState` are null on nearly all contacts.
The reliable corroborators are `Account.Name`, which encodes the jurisdiction, and `Title`,
which encodes the law-enforcement role. Treat location as a bonus, not a dependency.

## Step 4: confidence scoring

Score each chief-to-contact pair with three sub-scores from 0 to 100, then combine.

- **NameScore:** exact first and last is about 100; last plus first initial about 85;
  surname only about 55; phonetically near but uncertain about 40; first-only or truncated
  about 25; no overlap is 0, which is a pure adjacency row.
- **AccountTitleScore:** `Account.Name` corresponds to the chief's jurisdiction or to law
  enforcement generally, and `Title` is a law-enforcement role such as chief, deputy or
  assistant chief, sergeant, officer, or sheriff. An unrelated account or title pulls it down.
- **LocationScore:** mailing city or state matches the meeting jurisdiction. Almost always
  null, so it contributes 0 when absent rather than a penalty.

Combine, and state the weights when you present:

```
CorroborationScore = 0.7 * AccountTitleScore + 0.3 * LocationScore
FinalConfidence    = 0.55 * NameScore + 0.45 * CorroborationScore
```

**Promotion-pattern override.** The highest-value pattern is an internal promotion the name
match misses: a contact at the chief's new agency holding a deputy or assistant chief title
when that agency has just announced a new chief. Floor FinalConfidence at about 80 and label
the row "likely promotion", even when NameScore is low because the transcript garbled the
name. The linear blend under-rates this case, and it is the strongest "someone you know is
moving" signal the skill can produce. Note in the reasoning that the name is unconfirmed.

Two nuances:

- A person moving jobs usually still shows their old account and title in the CRM. For a
  person-level match, jurisdiction overlap with the new post is not expected. Title relevance
  is the real corroborator. Do not penalize a strong name match for sitting at a different
  agency; that is consistent with a move.
- For a jurisdiction-adjacency row, NameScore is low, so AccountTitleScore drives the result.
  Watch for a law-enforcement contact at the new agency whose name is phonetically near the
  garbled chief name. Flag that prominently.

Label every row "Person match" or "Jurisdiction adjacency", give a short concrete reason
citing the sub-scores, and sort by FinalConfidence descending.

## Step 5: present

Lead with one line: chiefs found across the states and window, how many produced a person
match, how many produced a jurisdiction adjacency. With no CRM attached, say so in that same
line and present the transitions with warm-path suggestions.

Then a table sorted by confidence:

| Confidence | Type | Chief (new role, state) | Status | Matched contact (title at account) | Why (sub-scores) | Meeting (date) |
|---|---|---|---|---|---|---|

- State the weights used so the user can recalibrate.
- Add a short bucket of nameless or non-transition mentions, by jurisdiction and state or as
  a count, so coverage is visible. Keep the spotlight on scored matches.
- Include the `cloverleaf_url` for every row so each signal is verifiable.

## Boundaries

- **Read-only.** No CRM writes: no contacts, tasks, or notes, unless the user explicitly asks
  in a later turn, and confirm before any write.
- **State level for now.** City, county, and agency targeting, natural-language search, and
  file export are future iterations. Do not imply they exist.
- **Handle failures gracefully.** A search can error or return nothing. Note it, fall back to
  different terms or a different source, and keep going rather than stalling.
