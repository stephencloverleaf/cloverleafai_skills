# Parameter recipes

Exact call shapes per tool, with the verified behavior that changes what you get back.
The ten rules in SKILL.md apply to every recipe here.

Contents: insights, semantic transcript search, lexical transcript search, the document
layer, the purchases layer, the legislation layer, contacts, campaigns, single entity
walks.

## search-insights

```python
search-insights(searchTerm = "cyber", limit = 20)                    # user scoped
search-insights(searchTerm = "cyber", states = ["FL"], limit = 20)   # territory filter
search-insights(searchTerm = "cyber", userId = 12020)                # a teammate
```

- Free. Run it before any keyword or semantic sweep, every time.
- Insights generate nationwide, so a territory rep always passes `states`.
- `limit` maxes at 200. No date filter exists; filter `created_at` yourself.
- One meeting yields several insights with different scores and different facts. There
  is no single insight for a meeting, so read every variant before quoting one.
- Scores compress at the top and do not bottom out. Across one 200 signal digest, none
  scored below 6 and 52% scored 9 or 10, and campaigns emitted exactly one insight per
  ingested meeting. The score labels everything ingested; it is not a selection
  threshold, and it tracks how loud the problem is, never whether it is yours.
- Skip 0/10 "gate excluded" rows rather than re-litigating them.
- Never work a digest from the summary email. It has promoted a 0/10 item while five
  9/10 signals in the same feed never surfaced. Pull the tool and sort by score.

## search-meetings (semantic transcripts)

```python
search-meetings(
    query    = "city or county asking for money to replace old firewalls or aging network equipment",
    states   = ["TX"],
    daysBack = 120,          # or startDate/endDate
    perPage  = 10,           # default 20, max 100; page for more
)
```

- Write the query as a full sentence describing the buyer's situation the way an
  official would live it. Intent matching is strong: the query above surfaced budget
  workshops discussing pen testing, Windows 10 end of life, and aging switches with
  almost no keyword overlap.
- Hits are multi paragraph chunks with ids like `20204912-12`, each carrying a `score`,
  plus a per meeting `best_score`. Treat 0.80 or higher as strong and read 0.75 to 0.80
  before trusting it.
- Excerpts carry `id`, `text`, `start_time`, and `score` and no speaker information at
  all. Every name you attach is reconstructed. See rule 9.
- Semantic search does not reliably find a meeting you already know exists. For a known
  meeting, go `lookup-organization`, then `list-organization-meetings` with the `title`
  filter, then `get-meeting-transcripts`. Reserve semantic and keyword search for open
  ended discovery.

## run-meeting-keyword-search (lexical transcripts)

```python
run-meeting-keyword-search(
    terms            = ["Fortinet", "FortiGate", "firewall"],
    mustIncludeTerms = ["renew", "expire", "replace"],
    proximity        = 50,
    states           = ["TX", "OK"],
    daysBack         = 120,
    perPage          = 50,     # max 100; page for more
)
```

- `terms` is an array and the terms are OR'd. `mustIncludeTerms` plus `proximity`
  require a search term to appear near an anchor term.
- Anchoring is lexical co-occurrence, not semantic. Anchor only with unambiguous words
  (vendor names, ransomware, SCADA). For fuzzy intent use `search-meetings`.
- `proximity` units are undocumented. 30 to 50 behaves as a loose window, and the org's
  saved campaigns use 30 to 180.
- The per line `person` block is `{name, organization, title}` only. Email and phone come
  from `list-contacts`.
- Hit counts undercount. On one meeting the tool reported 1 hit for a term the full
  transcript carries 3 times. The error runs toward manufacturing a false "not in the
  transcript", so verify a disconfirmation against the full transcript.

### Vendor search discipline

Three rules turn a vendor count into something you can say out loud.

1. **One vendor term per query.** In a batched `terms` array a high frequency term
   consumes the ranking and every other vendor reports `count: 0` for the returned page
   only. Batching six audit vendors let "teammate" swamp the ranking, so Workiva showed
   0 while it actually has 45 meetings.
2. **Spell names as ASR renders them.** The corpus is speech to text, so brand
   orthography does not survive. `CliftonLarsonAllen` returns 0 and `Clifton Larson
   Allen` returns 572. Confirmed manglings: KnowBe4 as "no before", Spillman as
   "Spellman", Eide Bailly as "Id Bailey", Purvis Gray as "Purvis Grain", Carahsoft as
   "Karasoff", PennDOT as "Pendot".
3. **Re-derive a zero in both layers.** Meetings and documents disagree. `AuditBoard`
   returns 0 meetings, because speech renders it "audit board", yet 37 real document
   hits. A wrong zero looks exactly like a right one, so never report a vendor absence
   until it has been run alone, in phonetic variants, and across both layers.

Watch for trap terms, which are ordinary words that are also product names (TeamMate,
Galvanize). Reach the product through the parent company instead. Watch too for acronym
collisions inside a jurisdiction: ERP in Cook County is the Early Resolution Program, an
eviction court legal aid program, and it outranked every genuine ERP system discussion in
Illinois. Anchor a bare acronym with a discriminating term.

## The document layer

```python
search-documents(                       # intent based, the better opening move
    query    = "contract award or renewal for firewall and network security equipment",
    states   = ["TX"],
    daysBack = 90,
    perPage  = 10,
)

run-document-keyword-search(            # lexical, exact vocabulary
    terms    = ["firewall", "network security", "cybersecurity"],
    states   = ["TX"],
    daysBack = 90,
    perPage  = 10,
    sortBy   = "hits",                  # or "meeting_date" (default)
    direction = "desc",
)
```

- `terms` is an array; a string fails validation (verified 2026-09-02). Multi word
  phrases match, for example "not to exceed".
- `sortBy` accepts only `hits` or `meeting_date`, and anything else silently falls back
  to `meeting_date`. Default sort is newest first, not relevance, so `sortBy = "hits"` is
  the fix for boilerplate flooding.
- Keep `perPage` small (5 to 10). Document highlights and chunks are long.
- Score calibration on documents runs lower than on transcripts. In a 2026-09-02 probe
  the top hit for a well formed procurement query scored 0.785 and was a real Fortinet
  award to CDW-G not to exceed $150,750. Read documents from about 0.75 up, and rank by
  `best_score` rather than applying the transcript threshold.
- Neither tool returns an org name. Resolve `organization_id` before presenting.
- The old `docs_count_per_search_term` calibration aggregation is gone. Calibrate a term
  with a cheap `perPage = 1` probe and read `total_document_hits`.

## The purchases layer

```python
search-purchases(                       # semantic
    query    = "firewall network security contract award",
    daysBack = 30,
    perPage  = 10,
)

run-purchase-keyword-search(            # lexical
    terms    = ["firewall", "Palo Alto"],
    daysBack = 30,
)
```

- Verified 2026-09-02: `query`, `daysBack`, `page`, and `perPage` are numbers where
  numeric; `states` validates as an array; `terms` on the keyword tool validates as an
  array.
- Dataset 1 is federal contract awards with USAspending style `CONT_AWD` ids. Every
  sampled row was a federal department (Government Accountability Office, Homeland
  Security, Transportation, Commerce, Smithsonian) dated within the prior week.
  Coverage beyond federal is unverified as of 2026-09-02.
- This is award stage data, not a feed of open solicitations. It answers who won, for how
  much, and when. It does not tell you what is currently biddable.
- `total_hits` capped at 100 on the probe, same as the other semantic tools.
- Rule 10 applies: read `department` as the buyer and ignore `organization_names`.

## The legislation layer

```python
search-legislation(                     # semantic
    query    = "cybersecurity requirements for critical infrastructure and utilities",
    daysBack = 180,                     # always widen; the default window is thin
    perPage  = 10,
)
run-legislation-keyword-search(         # lexical
    terms    = ["ransomware", "cyber incident reporting"],
    daysBack = 180,
)
```

- The default window runs the past 7 days through the next 365 days, because calendar
  events are future dated. In practice it is nearly empty: 0 hits at default against
  2,256 at `daysBack = 180`.
- Zero results for a state are often a legitimate session calendar gap. Biennial
  legislatures do not sit every year, so widen the dates and check the session before
  concluding there is no coverage.
- Results carry `bill_id` for the four bill tools, `meeting_document_id` for
  `get-document`, `document_type`, `ls_entity_type`, and `cloverleaf_url`. Older
  documents can lack `bill_id`; read the text through `get-document` to find it.
- `get-bill(billId)` returns identity, `status_progress`, state, session, originating
  chamber, pending committee, and sponsors with party and district. `cloverleaf_url` can
  be null, which means there is no viewable page yet. Say so rather than inventing a link.
- `get-bill-status-changes(billId)` merges one timeline: `event_kind: "history"` entries
  are official status changes, `"calendar"` entries are hearings, and `major: true` marks
  committee passage and floor votes.
- `get-bill-documents(billId)` lists Introduced and Amended versions with dates; read any
  version through `get-document(documentId = meeting_document_id)`.

## list-contacts

```python
list-contacts(
    organizationId = 2908,          # from lookup-organization, the most precise filter
    limit          = 50,            # default 20
    offset         = 0,
    # geography filters, no org id needed
    stateName      = ["Washington"],
    countyName     = ["King"],
    cityName       = ["Snoqualmie"],
)
```

- Roles include Top Appointed Executive, Top Elected Official, Governing Board Member,
  Head of IT, Head of Finance, and Head of Purchasing. Filter on `role`.
- Geography filters return alphabetical rosters, not signal ranked. Use them for a
  deliberate area sweep, not to rank an account.
- Drop records where `removed_at` is set, and dedupe by email: small orgs share one inbox
  across several officials.
- Coverage is uneven. Cities and counties are strong, special districts and utilities can
  return nothing. When a roster is empty, say so rather than skipping the org silently.
- Contacts can sit under a different org id than the meetings. When a roster comes back
  empty, re-resolve the entity with `lookup-organization` and retry before concluding
  there is no roster.
- Check the roster for jurisdiction contamination: one county org mixed township records
  with county records, and one state senate org returned contacts from two other states.
  Filter by email domain and title before presenting.

## search-campaigns

Read only. Each campaign carries `searchTerms`, `mustIncludeTerms`, `exclude`,
`proximity`, and `filterParams` (cities, counties, states, and organizations as internal
integer ids, plus `channel_types`, `countries`, income and population ranges where
`[-1, -1]` means unset, `voice_ids`, `title_search_terms`, `organization_search_terms`,
`person_ids`, `user_ids`).

Use it as a template library and translate a spec into live parameters by hand, because
the integer geo ids do not map to state codes. Campaigns named "Smart Search" or "SS"
have empty `searchTerms`: adapt those into `search-meetings` sentence queries. Sanity
check before copying, because corrupted specs exist (`searchTerms` of "0", "1", "2").
Visibility is your org's campaigns as exposed to your account, so do not assume you see
every user's. There is no create or update tool; campaign writes happen in the platform.

## Single entity walks

- `lookup-organization(query = "Las Vegas, NV")` splits on the last comma. `name` plus
  `state` also works, and full names, 2 letter codes, and Canadian provinces are
  accepted.
- `list-organization-meetings(organizationId, perPage <= 100, title = "budget")` is the
  preferred walk: newest first, optional case insensitive title substring filter, no date
  filter, so paginate. `organizationId` is a number.
- Use this walk, not `lookup-organization.last_published_at`, to judge freshness. The org
  endpoint has reported a newer date than the channel actually held.
- Sessions split and duplicate. One budget hearing ingests as separate morning and
  afternoon records, and the same session has appeared under three ids. List every
  meeting for the date, pull all sessions, and pick the most complete.
- One org record can be a mixed feed of several governing bodies sharing a cable access
  channel (a city council, a county board, and a school board under one id). Confirm the
  governing body from the transcript, and check that the contacts you pull belong to it.
- `get-meeting-transcripts` returns lines ordered by `start_time`. Payloads are large, so
  pull only for context around a specific quote during enrichment on a shortlisted
  signal. On a long meeting the payload can exceed the tool output limit, and the
  fallback path produces insight text that reads like a quote but is not one.
