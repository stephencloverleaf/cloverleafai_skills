# Parameter recipes

Exact call shapes per tool, with the verified behavior that changes what you get back.
The twelve rules in SKILL.md apply to every recipe here. Everything was re-verified on
2026-11-13 unless a line gives another date. Budget tools have their own file,
`budget-tools.md`.

Contents: shared filters and errors, signals feed, insights, semantic transcript search,
lexical transcript search, the document layer, the purchases layer, the legislation
layer, contacts and speakers, campaigns and territory, single entity walks.

## Shared filters and errors

`search-meetings`, `run-meeting-keyword-search`, `search-documents`, and
`run-document-keyword-search` take the same scope parameters:

```python
states          = ["TX", "Ontario"]      # codes or full names
counties        = ["Travis"]             # "County" suffix optional
cities          = ["Austin"]             # pass states too, to disambiguate
channelTypes    = ["City Council"]       # names, case insensitive
organizationIds = [1242]                 # numbers, from lookup-organization
snippetsPerHit  = 5                      # 1 to 50, default 5
```

- A meeting matches when it is in any listed county or any listed city. The filter is
  on where the body sits, not which government it is: `cities = ["Austin"]` returned
  the same meetings as `counties = ["Travis"]`, and document hits came from other
  bodies in the city. Use `organizationIds` for one government.
- Valid `channelTypes`: Broadband Office, Budget and Finance Committee, City Council,
  County Commissioner, Department of Natural Resources, Education, Environmental Agency,
  Federal Agency, Federal Committee, Fire/Police Board, Higher Education, Other, Parks
  and Recreation, Planning Commission, Port Authority, State Agency, State Executive
  Offices, State Health Department, State Legislature, Transportation, Water District.
- Errors you can act on, verbatim:
  - `daysBack cannot be combined with startDate/endDate. Provide either daysBack or a date range.`
  - `endDate is only accepted together with startDate.`
  - `Validation failed: states.0: Unknown state or province`
  - `Cloverleaf has no coverage for: Guam. Remove these from states, or omit states to search everywhere.`
  - `Cloverleaf has no coverage for cities: NAME. Check spelling, or add states to disambiguate names shared across states.`
  - `Unknown channel types: NAME. Valid values: ...` (lists every valid name)
  - `Validation failed: terms: Invalid input: expected array, received string`
  - `Validation failed: perPage: Too big: expected number to be <=100`
- `Tool "search-meetings" timed out after 60000ms` is rule 11, not an empty result.
  Shrink the window or the scope and retry.

## get-signals-feed

```python
get-signals-feed(states = ["NC"], perPage = 25)                 # user's threshold applies
get-signals-feed(minScore = 0, sort = "recent", startDate = "2026-10-01")
get-signals-feed(unseen = True, campaignIds = [27880], organizationIds = [6113])
```

- Returns only scored signals from the user's feed products and campaigns. `score` is
  an integer, and the default sort is score, then newest.
- The threshold is the user's notification setting (default 7). `minScore` overrides
  it: one account held 54 signals at the default and 313 at `minScore = 0`.
- The date range filters on when the signal was generated, not the meeting date, and
  defaults to the last 30 days.
- `perPage` defaults to 5 and maxes at 25. `total` counts every match across pages.
- `facets` lists the organizations, states, and campaigns in the feed as `{id, name}`.
  It is feed wide and does not narrow with your filters. Take `campaignIds` and
  `organizationIds` from it.
- No text search, and no `userId`: it reads the authenticated user's feed only. Use
  `search-insights` for a text filter or a teammate.
- Reading a signal here does not mark it seen. `hidden` signals are left out unless
  `showHidden` is set.
- A feed signal's `id` can differ from the `search-insights` id for the same meeting.
  `save-signal-to-tasks` takes the feed `id`.

`save-signal-to-tasks(insightId, title, notes)` writes a to-do to the user's Tasks. It
is idempotent per signal, and channel or territory analysis signals cannot be saved.
Call it only on request. It was not called during verification.

## search-insights

```python
search-insights(searchTerm = "cyber", limit = 20)                      # user scoped
search-insights(searchTerm = "cyber", states = ["FL"], limit = 50, page = 2)
search-insights(searchTerm = "cyber", userId = 12020)                  # a teammate
search-insights(searchTerm = "Bennettsville", limit = 1, includeFullResult = True)
```

- Run it, or the feed, before any keyword or semantic sweep.
- Insights generate nationwide, so a territory rep always passes `states`.
- `limit` defaults to 5 and maxes at 200. No date filter exists: rows come newest
  first, so page until `created_at` is older than the range you need.
- `result` is a 2,000 character preview. `result_truncated: true` appears only on cut
  rows. Pass `includeFullResult: true` for the whole text, on a small `limit`.
- There is no score field. Parse it from `summary` with a pattern that tolerates
  brackets, such as `Signal Match: \[?(\d+)\]?/10`. Rows with `summary: null` and
  `result: null` have no score yet (49 of 200 on one pull).
- One meeting yields several insights, one per prompt (Sales Insights, Sales Brief,
  Competitors, Competitor Contract Details), with different scores and different
  facts. Read every variant before quoting one.
- The score distribution depends on the account's campaigns. One digest never scored
  below 6. Another account's 200 newest insights held 105 rows at 0 or 1 and 27 at 7
  or higher. The score tracks how loud the problem is, never whether it is yours.
- Skip 0/10 rows rather than re-litigating them.
- Never work a digest from the summary email. It has promoted a 0/10 item while five
  9/10 signals in the same feed never surfaced. Pull `get-signals-feed` instead.

## search-meetings (semantic transcripts)

```python
search-meetings(
    query     = "city or county asking for money to replace old firewalls or aging network equipment",
    states    = ["TX"],
    startDate = "2026-08-15",   # state wide: 30 day slices (rule 11)
    endDate   = "2026-09-14",
    perPage   = 10,             # default 20, max 100
)
search-meetings(query = "...", organizationIds = [1242], daysBack = 365)   # narrow scope, long window
```

- Write the query as a full sentence describing the buyer's situation the way an
  official would live it. That query returned a county discussing end of life
  firewalls and a pending quote as its top hit.
- Hits are chunks with ids like `20204912-12` (meeting id, chunk number), each with a
  `score`, plus a per meeting `best_score`. Treat 0.80 or higher as strong and read
  0.75 to 0.80 before trusting it. Top hits on that query scored 0.84 and 0.80.
- Each excerpt is cut to a 500 character preview ending in "…". A chunk starts on a
  transcript line, and its `start_time` matches that line.
- Only the top 100 chunks come back (rule 3). To see more, slice the window or narrow
  the scope instead of paging.
- Semantic search does not reliably find a meeting you already know exists. For a known
  meeting, go `lookup-organization`, then `list-organization-meetings` with the `title`
  filter, then `get-meeting-transcripts`.

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

- `terms` is an array and the terms are OR'd. A multi word term matches as a phrase.
- `mustIncludeTerms` without `proximity` requires the meeting to contain an anchor term
  somewhere. Adding `proximity` requires a search term near an anchor: one probe fell
  from 94 meetings to 8 at `proximity = 50`.
- Anchoring is lexical co-occurrence, not semantic. Anchor only with unambiguous words
  (vendor names, ransomware, SCADA). For fuzzy intent use `search-meetings`.
- `proximity` units are undocumented. 30 to 50 behaves as a loose window, and saved
  campaigns use 30 to 180.
- An excerpt is one full transcript line, and its `id` is the transcript line id, so it
  joins to `get-meeting-transcripts` directly. Excerpts with a 20 character opaque id
  are summary text rather than a spoken line: do not quote them.
- The `person` block is `{name, first_name, last_name, organization, title}`. Email and
  phone come from `list-contacts`.
- Hit counts undercount. On one meeting the tool reported 1 hit for a term the full
  transcript carries 3 times. Verify a disconfirmation against the full transcript.

### Vendor search discipline

Three rules turn a vendor count into something you can say out loud.

1. **One vendor term per query.** In a batched `terms` array a high frequency term
   consumes the ranking and every other vendor reports `count: 0` for the returned page.
   `["budget", "Workiva"]` showed Workiva at 0 on every returned meeting, while Workiva
   alone returned 16 meetings.
2. **Spell names as ASR renders them.** The corpus is speech to text, so brand
   orthography does not survive. `CliftonLarsonAllen` returns 0 and `Clifton Larson
   Allen` returns 450 meetings. Confirmed manglings: KnowBe4 as "no before", Spillman as
   "Spellman", Eide Bailly as "Id Bailey", Purvis Gray as "Purvis Grain", Carahsoft as
   "Karasoff", PennDOT as "Pendot".
3. **Re-derive a zero in both layers.** Meetings and documents disagree. `AuditBoard`
   returns 0 meetings, because speech renders it "audit board", yet real document hits.
   Never report a vendor absence until it has been run alone, in phonetic variants, and
   across both layers.

Watch for trap terms, which are ordinary words that are also product names (TeamMate,
Galvanize). Reach the product through the parent company instead. Watch too for acronym
collisions inside a jurisdiction: ERP in Cook County is the Early Resolution Program, an
eviction court legal aid program. Anchor a bare acronym with a discriminating term.

## The document layer

```python
search-documents(                       # intent based, the better opening move
    query         = "contract award or renewal for firewall and network security equipment",
    states        = ["TX"],
    daysBack      = 30,                 # state wide: 30 days at most (rule 11)
    documentTypes = ["agenda", "packet"],
    perPage       = 10,
)

run-document-keyword-search(            # lexical, exact vocabulary
    terms     = ["firewall", "network security", "cybersecurity"],
    states    = ["TX"],
    daysBack  = 90,
    perPage   = 10,
    sortBy    = "hits",                 # or "meeting_date" (default)
    direction = "desc",
)
```

- `documentTypes` accepts agenda, minutes, packet, notice, and budget. Budget books are
  searchable here as ordinary documents; for figures use the budget tools.
- `sortBy` accepts only `hits` or `meeting_date`. Anything else fails validation.
  Default sort is newest first, not relevance, so `sortBy = "hits"` is the fix for
  boilerplate flooding.
- Multi word phrases match exactly, for example "not to exceed".
- On the keyword tool `total_hits` is the true document count. Calibrate a term with a
  `perPage = 1` probe. It returns no `document_type`.
- Keep `perPage` small (5 to 10) on the keyword tool. Its highlights are long.
- Document scores run lower than transcript scores. Top hits for the semantic query here
  scored 0.77, and the first was a real Palo Alto licensing item not to exceed
  $114,757.70. Read documents from about 0.75 up and rank by `best_score`.
- Neither tool returns an org name. Resolve `organization_id` before presenting.
- `documentTypes = ["budget"]` has returned an upstream 500 and timeouts on wide
  windows. Narrow by `states` and a short date range.

## The purchases layer

```python
run-purchase-keyword-search(
    terms         = ["firewall", "Palo Alto"],
    states        = ["TX"],
    daysBack      = 365,
    organizations = [5012],             # org ids from lookup-organization
    vendorNames   = ["CDW"],            # partial match
    departments   = ["Purchasing"],
    amount        = {"min": 100000},
    sortBy        = "amount",           # score (default), date, transaction_date, department,
    direction     = "desc",             # category, purchase_name, vendor_name, amount, organization_names
)
```

- Use the keyword tool. `search-purchases` (semantic) takes the same filters but
  returned `total_hits: 0` on every probe on 2026-11-13. Treat a semantic zero as a
  tool gap, never as "no awards".
- Coverage is federal plus a growing set of local datasets. Dataset 1 is federal
  contract awards with `CONT_AWD` ids. Local datasets seen: Los Angeles MTA, Long
  Beach, Santa Clarita, County of Boone, County of Collin, City of Dallas, Miami-Dade,
  Detroit, and Washington DC. `purchaseDatasetIds` filters to specific ones.
- Rule 10 applies: on dataset 1 read `department` as the buyer; on local datasets read
  `organization_names`.
- Local rows often carry a contract term in `start_date` and `end_date` (a Dallas web
  application firewall contract ending 2029-05-31). An approaching `end_date` is a
  renewal signal. Federal rows leave both null.
- `daysBack` does not filter on `transaction_date`: a 30 day call returned rows dated a
  year earlier and rows with a null date. Read the dates on each row.
- `cities`, `counties`, and `channelTypes` take integer ids here, not names. `states`
  takes codes or names as usual.
- With `sortBy` set to anything but score, `score` comes back null.
- `total_hits` is a true count on the keyword tool. `perPage` defaults to 10.
- The same record can appear under two dataset ids. Dedupe on vendor, name, and amount.
- This is award and contract data, not a feed of open solicitations.

## The legislation layer

```python
run-legislation-keyword-search(         # lexical; handles long windows
    terms    = ["ransomware", "cyber incident reporting"],
    daysBack = 180,
    states   = ["TX"],
)
search-legislation(                     # semantic; 30 days at most (rule 11)
    query    = "cybersecurity requirements for critical infrastructure and utilities",
    daysBack = 30,
    perPage  = 10,
)
```

- The default window runs the past 7 days through the next 365 days. It is thin: 1
  keyword hit for "ransomware" at default against 68 at `daysBack = 180`.
- Zero results for a state are often a legitimate session calendar gap. Biennial
  legislatures do not sit every year, so widen the dates and check the session before
  concluding there is no coverage.
- Both tools return `bill_id` for the four bill tools. The keyword tool also returns
  `meeting_document_id` and `ls_entity_type`; on the semantic tool the document id is
  `document_id`. Older documents can lack `bill_id`; read the text through
  `get-document` to find it.
- Federal bills appear alongside state bills.
- The keyword tool takes `direction` but no `sortBy`. An unknown parameter is ignored
  without an error.
- `get-bill(billId)` returns identity, `status_progress`, state, session, originating
  chamber, pending committee, subjects, and sponsors with party and district.
  `cloverleaf_url` can be null, which means there is no viewable page yet. Say so
  rather than inventing a link.
- `get-bill-status-changes(billId)` merges one timeline under `history[]`. `event_kind`
  is "history" (official status changes), "calendar" (hearings), "amendment", or
  "supplement". `major: true` marks committee passage and floor votes.
- `get-bill-documents(billId)` lists Introduced, Comm Sub, Amendment, Chaptered, Fiscal
  Note, and Analysis documents with dates. Read any of them through
  `get-document(documentId = meeting_document_id)`. It has timed out once and worked on
  retry.
- `get-bill-events(billId)` returns `calendar_events[]`, often empty.

## Contacts and speakers

```python
list-contacts(
    organizationId = 2908,          # from lookup-organization, the most precise filter
    limit          = 50,            # default 20; 1,000 worked
    offset         = 0,
    # geography filters, exact match, no org id needed
    stateName      = ["Washington"],
    countyName     = ["King"],
    cityName       = ["Snoqualmie"],
)
search-verified-speakers(query = "Austin", limit = 20, offset = 0)
```

- Filter on `role`. Values include Top Elected Official, Top Appointed Executive, Deputy
  Top Appointed Executive, Governing Board Member, Head Clerk, and Head of IT, Finance,
  Purchasing, HR, Communications, Law Enforcement, Corrections, Fire Protection
  Services, Public Works, Water Supply, Facilities Management, Buildings,
  Planning/Zoning, Economic Development, Parks and Recreation, Health Services, and
  Geographic Information System.
- There is no total count. Page with `offset` until a short page comes back.
- Geography filters return alphabetical rosters, not signal ranked.
- Dedupe by email: small orgs share one inbox across several officials. `email_address`
  can be null. There is no `removed_at` field to filter on.
- Coverage is uneven. Cities and counties are strong, special districts and utilities
  can return `{"contacts": []}`. Say so rather than skipping the org silently.
- Contacts can sit under a different org id than the meetings. When a roster comes back
  empty, try the sibling org record from `lookup-organization` before concluding there
  is no roster.
- Check the roster for jurisdiction contamination: one county org mixed township records
  with county records, and one state senate org returned contacts from two other states.
  Filter by email domain and title before presenting.
- `search-verified-speakers` matches `query` against first name, last name, and
  organization, sorted by last name, with a `total`. It returns name, organization, and
  title only. The same person can appear under two `person_id` values.

## Campaigns and territory

`search-campaigns(page, perPage)` is read only and returns `total_campaigns`. Each
campaign carries `searchTerms`, `exclude`, and `filterParams`, and some carry
`mustIncludeTerms` and `proximity`. `filterParams` holds cities, counties, states,
organizations, and `channel_types` as internal integer ids, plus `countries`,
`document_types`, income and population ranges where `-1` means unset, `voice_ids`,
`title_search_terms`, `organization_search_terms`, `person_ids`, and `user_ids`.

Use it as a template library and translate a spec into live parameters by hand. State
ids resolve to names through `facets.states` in `get-signals-feed`. Smart Search
campaigns have empty `searchTerms` (9 of 14 on one account): adapt those into
`search-meetings` sentence queries. Sanity check before copying, because junk specs
exist (`searchTerms` of "0", "1", "2", or "Test", "tst"). Visibility is your org's
campaigns as exposed to your account. There is no create or update tool.

`list-territory-channels(q, stateId, source, sortBy, sortOrder, page, perPage)` lists
the user's monitored organizations. `source` is all, manual, or auto. `perPage` above
100 is reduced to 100. An account with no territory returns `{"channels": [], "total": 0}`.

`list-salesforce-account-mappings(page, perPage)` returns `accounts[]` with
`total_count`. It is empty when the org has no Salesforce mapping.

## Single entity walks

- `lookup-organization(query = "Las Vegas, NV")` splits on the last comma. `name` plus
  `state` also works and ranks differently. A miss returns `matched: false` with a
  `reason` of `unknown_state`, `no_coverage_in_state`, or `no_match`.
- `list-organization-meetings(organizationId, perPage <= 100, title = "budget")` is the
  preferred walk: newest first, optional case insensitive title substring filter, no
  date filter, so paginate on `has_more`. `organizationId` is a number. Its `total` can
  differ from `meeting_count` in the lookup (166 against 160).
- Use this walk, not `lookup-organization.last_published_at`, to judge freshness. The
  lookup has returned a date in the future.
- Sessions split and duplicate. One budget hearing ingests as separate morning and
  afternoon records, and the same session has appeared under three ids. List every
  meeting for the date, pull all sessions, and pick the most complete.
- One org record can be a mixed feed of several governing bodies sharing a cable access
  channel. Confirm the governing body from the transcript, and check that the contacts
  you pull belong to it.
- `get-meeting-transcripts(meetingId, page, perPage)` returns lines ordered by
  `start_time`, 200 per page by default and 500 at most, with `total_transcripts`. Page
  until you have them all. A 500 line page can still exceed the tool output limit and
  be written to a file. Lines carry no `cloverleaf_url`: cite the search excerpt's link.
- `get-document(documentId)` returns the whole text in `plain_text`, with form feed
  characters as the only page breaks. An agenda packet ran to 950,000 characters and a
  budget book to 2.1 million, so the result is written to a file. Slice it with a
  script rather than reading it.
