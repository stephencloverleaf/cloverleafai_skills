---
name: cloverleaf-signal-search
description: >-
  How to drive the Cloverleaf AI MCP connector to find pre-RFP buying signals in
  live government meeting transcripts, then immediately pull verified contact info
  (email + direct phone) for every relevant person at that jurisdiction. Use this
  skill ANY time the task involves searching Cloverleaf, finding leads/signals in
  public meetings, council or board discussions, or building public-sector pipeline
  (federal, state, local, or education — cybersecurity or any category) from meeting
  intelligence — even if the user just says "find me some signals," "search for
  ransomware discussions," "what are cities saying about X," or names a jurisdiction.
  This is the FIRST step of the demo workflow; the dashboard, enrichment, and
  outreach skills all build on the signals this produces.
---

# Cloverleaf Signal Search

## What this connector is (and why it wins)

Cloverleaf processes **full, unedited live meeting audio and video** from 30,000+
government organizations — not scraped written minutes. A single search returns the
**exact words an official said**, **who said it**, and **when**. And via
`list-contacts`, you can instantly pull the complete verified contact roster for any
jurisdiction — name, title, direct email, and phone.

That two-step pattern (find the signal → pull the org's contact list) is the
fastest path to a warm outreach-ready lead in the entire workflow.

**Coverage is the whole public sector, not just SLED.** Cities, counties, school
boards, special districts, state agencies, federal departments — all in scope. US
states/territories AND Canadian provinces are now accepted everywhere a `states`
filter exists.

**Where it runs (new):** the Cloverleaf MCP connector now works in claude.ai chat,
Cowork, AND Claude Code sessions. If the tools aren't visible in a session, the
connector just needs to be enabled for that chat — it's no longer a chat-only
integration.

**Citation rule (new, server-mandated):** every meeting, document, insight, and bill
now carries a `cloverleaf_url`. That is THE link to put on dashboards and in
outreach context. Never construct links yourself, and never cite legiscan.com.

---

## Full tool inventory (re-verified August 2026)

Tool-level ground truth (parameters, limits, bugs) lives in
`cloverleaf-mcp-operations` — load it before calling anything. Summary:

| Tool | Status | Use it for |
|---|---|---|
| `search-insights` | ✅ **Check FIRST** | Free, already-generated AI insights with a `Signal Match: X/10` score. **Now scoped to the authenticated user** (pass `userId` for a teammate) and **now accepts `states`** — territory reps should always pass it, since insights generate nationwide. Still apply every guardrail below to each result. |
| `run-meeting-keyword-search` | ✅ Fallback sweep | Territory-scoped lexical sweep when insights are thin or stale. `terms[]`, `states[]`, `daysBack` or `startDate`/`endDate`. **The old 25-meeting cap is GONE** — `perPage` up to 100 with real `page` pagination. |
| `search-meetings` | ✅ Fallback sweep | Natural-language semantic meeting search. Use when insights and keyword search come up short — good for open-ended intent discovery. Same pagination. |
| `lookup-organization` | ✅ Reliable, improved | Resolve any jurisdiction name → numeric org `id`. Now also returns `meeting_count` and `last_published_at` per match — skip `meeting_count: 0` orgs before wasting calls. Still embedding-ranked: read the WHOLE list. |
| `list-contacts` | ✅ Primary contact path | Complete verified contact roster for an org or geography. **Now the ONLY contact path** — transcript results no longer carry email/phone (see below). |
| `list-organization-meetings` | ✅ Reliable | Walk a jurisdiction's meetings newest-first. Optional `title` filter (e.g. `"budget"`, `"IT"`). Paginated, no date filter. |
| `get-meeting` | ✅ Reliable | Title, date, video URL, `cloverleaf_url` for a specific meeting ID. |
| `get-meeting-transcripts` | ⚠️ **Enrichment only — never discovery** | Full transcript for one meeting — large. Pull only for the 3–5 signals that already cleared scoring, during `opportunity-enrichment`. |
| `run-document-keyword-search` / `search-documents` | ✅ Procurement layer | Agenda/packet search — lexical and (new) semantic. **The `states` bug is FIXED; pass `states` normally now.** Owned by `document-signal-search`. |
| `search-campaigns` | ✅ Read-only template library | Every saved campaign as a search spec (`searchTerms`, `mustIncludeTerms`, `exclude`, `proximity`, `filterParams`). No create/update tool. `filterParams` uses internal **integer** geo IDs that don't map to 2-letter codes — translate a spec into live search params by hand. Proven cyber templates: 4553 "Cybersecurity SLED opportunities", 4511 "Thrive - Cybersecurity campaign". |
| `search-legislation` / `run-legislation-keyword-search` + `get-bill*` | ✅ NEW legislation layer | State bills, amendments, hearings, status timelines. Use for mandate-driven pipeline: laws that create budgets and requirements (cyber rules for utilities, modernization funds). Recipes in `cloverleaf-mcp-operations`. |

---

## Known data defects — verify before you present

Verified live and still true; each one survives into polished-looking output if you
don't check it.

- **City metadata is roughly 28% populated.** Scope by `states` or `organizationId`.
  Never rely on a city field for filtering.
- **Org names and states in metadata can be flat wrong.** Confirmed 2026-07-17:
  "Greene Public Schools (Virginia)" (meeting 19294024) is actually Greene County,
  GEORGIA; "City of Blue Ash" (org 577) meetings are actually Columbia Township, OH.
  Verify the entity and state from transcript content before presenting any signal.
- **`search-insights` quotes and titles can misattribute the speaker.** A Southampton,
  VA insight titled as an "IT Administrator server warning" was really a citizen
  describing a certificate warning on their personal phone. Verify every
  insight-sourced signal against the actual transcript before featuring it.

---

## Search order: insights first, transcripts are the fallback (and the enrichment tool)

Don't open with a fresh transcript sweep. Cloverleaf runs an automated insights pass on
every account already — checking it costs nothing and often surfaces a scored signal a
manual sweep would take several calls to rediscover.

**Step 1 — `search-insights(searchTerm = <vendor or topic>, states = <territory>)`.**
Run this before `run-meeting-keyword-search` or `search-meetings`, every time. Pass
`states` — insights generate nationwide and an unscoped read wastes the page on other
territories. Read the `Signal Match` score and the summary, but don't trust the score
alone — it's the insight prompt's scoring, not our rulebook. Skip `0/10` "gate
excluded" rows without re-litigating them. Every insight still gets the same guardrail
checks (below) a raw keyword hit would get before it's allowed on a board. Insights
are per-user now: if the rep you're working for isn't the authenticated account, pass
their numeric `userId`.

**Step 2 — fall back to a fresh sweep only when insights are absent, stale (call it
>90 days), or don't clear the guardrails.** That's `run-meeting-keyword-search` for
precision terms and `search-meetings` for open-ended semantic discovery — see
"Territory-scoped signal search" below.

**`get-meeting-transcripts` is not part of discovery, ever.** It's expensive to read and
belongs to `opportunity-enrichment`: once 3–5 signals have cleared scoring, pull the full
transcript on *those* to verify exact wording and surrounding context before a rep acts
on the quote. If you're calling `get-meeting-transcripts` before you've picked a
shortlist, stop — that's the wrong step.

---

## `list-contacts` — now the ONLY contact path

**Change from earlier versions of this skill:** transcript search results no longer
include speaker email/phone. The per-line `person` block is now just
`{name, organization, title}`. Every email and phone number now comes from
`list-contacts`. The two-step (signal → roster) isn't just the fastest path anymore;
it's the only one.

**Parameters:**

```python
list-contacts(
    organizationId = 2908,          # from lookup-organization — most precise
    limit          = 50,            # default 20; increase for large orgs
    offset         = 0,             # pagination
    # --- geography filters (no org ID needed) ---
    stateName      = ["Washington"],
    countyName     = ["King"],      # all orgs in King County, WA
    cityName       = ["Snoqualmie"] # all orgs in a specific city
)
```

**Key behaviors (verified August 2026):**
- `organizationId` is the most precise filter — use it after `lookup-organization`.
- `countyName` + `stateName` together sweep all orgs in a county; `cityName` works the
  same for city scope. Geography sweeps return ALPHABETICAL rosters, not signal-ranked.
- Contacts include a `role` field (e.g. `"Head of IT"`, `"Top Elected Official"`,
  `"Head of Purchasing"`) — filter on it for IT, finance, and executive contacts.
- Small orgs share inboxes across officials (all four Hunt County commissioners list
  the same `commissioner@` address) — dedupe by email and prefer the named-title
  contact when drafting outreach.
- Coverage is uneven: cities and counties are strong; special districts and utilities
  can return empty. When a roster is empty, SAY SO — never skip the org silently.
- The roster does **not** always include staff below director level. Transcript
  speaker attribution (name/title) still identifies who *spoke*; match them into the
  roster by name to get their email/phone.
- Contacts may live under a **different org ID than the meetings** (confirmed: Freeport,
  IL meetings under org 789, contacts under org 10511). When `list-contacts` returns
  empty, re-resolve the entity with `lookup-organization` and retry before concluding
  there's no roster.
- Drop records where `removed_at` is set. Small towns map one person to many roles, so
  dedupe by email.

**Workflow — named jurisdiction:**
```
1. lookup-organization("Travis County, TX")  →  id: 1242 (check meeting_count > 0)
2. list-contacts(organizationId=1242, limit=50)
3. Filter to role contains "IT", "Purchasing", "Finance", or top elected/appointed
```

**Workflow — county sweep (no specific org needed):**
```
1. list-contacts(countyName=["Travis"], stateName=["Texas"], limit=50)
   → returns all contacts across every org Cloverleaf tracks in Travis County
```

**Roles to prioritize for cyber/IT signals:**
- `Head of IT` — owns the buy
- `Head of Purchasing` / `Head of Finance` — controls the contract
- `Top Appointed Executive` (City/County Manager) — final authority on large deals
- `Top Elected Official` — needed for political champion outreach

---

## Territory-scoped signal search (fallback sweep — only after Step 1 comes up short)

### State-level sweep — `run-meeting-keyword-search`

The cleanest path for a rep's territory. Pass `states[]` and `terms[]` together:

```python
run-meeting-keyword-search(
    terms    = ["ransomware", "cybersecurity", "security operations center", "zero trust"],
    states   = ["TX"],
    daysBack = 90,          # or startDate/endDate (ISO 8601) — new option
    perPage  = 50,          # max 100; paginate with page= — the old 25 cap is gone
)
```

Results come back with `state`/`county`/`city` on every meeting. The **signal search
has no county filter** — state is the finest geographic scope for this tool. For
county targeting, use the org ID path below.

### County or city targeting

`run-meeting-keyword-search` cannot filter by county. To target a specific county:

```
1. lookup-organization("Travis County, TX")  →  id: 1242
2. list-organization-meetings(organizationId=1242)      # their recent meetings
3. list-contacts(organizationId=1242)                   # their full contact roster
```

Or if you want signals AND contacts across every org in a county (not just the county
government itself):
```
1. Run keyword search with states=["TX"], then filter meeting results by county field
2. list-contacts(countyName=["Travis"], stateName=["Texas"]) for the contact sweep
```

### One specific jurisdiction — deep dive

```
1. lookup-organization("City of Snoqualmie, WA")  →  id: 2908
2. list-organization-meetings(organizationId=2908, title="IT")   # IT-related meetings
3. list-contacts(organizationId=2908)                            # full contact roster
```

---

## Write queries that actually hit

Officials describe **problems and projects**, not vendor names. Search the pain. The
same term banks work as the `searchTerm` for `search-insights` and as `terms[]` for
`run-meeting-keyword-search` — build the list once, use it for both. For
`search-meetings`, convert the theme into a full sentence describing the buyer's
situation instead.

**Cybersecurity term bank:**
- *Threat/pain:* `ransomware`, `data breach`, `phishing`, `cyber attack`, `malware`
- *Project/initiative:* `cybersecurity audit`, `security operations center`, `zero trust`,
  `penetration testing`, `incident response`, `multi-factor authentication`,
  `endpoint protection`, `IT modernization`, `ransomware resiliency`
- *Budget/funding:* `SLCGP`, `cybersecurity grant`, `cyber insurance`, `MSSP`,
  `managed security`, `IT budget`
- *Sector:* `water system cybersecurity`, `K-12 cybersecurity`, `critical infrastructure`, `SCADA`

**Network infrastructure term bank:**
- `network infrastructure`, `network modernization`, `fiber`, `broadband`, `SD-WAN`,
  `network upgrade`, `managed services`, `software defined networking`, `bandwidth`

Run two separate thematically focused searches rather than one combined query — the
signal-to-noise ratio is much better. And remember lexical ambiguity is real: a bare
"firewall" sweep returns building firewalls from planning/zoning boards. Prefer
compound terms or pair with an unambiguous anchor.

### `mustIncludeTerms` + `proximity` for precision

Require a term to appear in close proximity to a must-include term:
```python
run-meeting-keyword-search(
    terms            = ["cybersecurity", "budget", "contract"],
    mustIncludeTerms = ["cybersecurity"],
    proximity        = 50,   # within ~50 tokens of "cybersecurity"
    states           = ["TX"],
    daysBack         = 90
)
```

---

## Scoring signals — what to prioritize

### Guardrail 0 — own-vendor check (apply first, to every signal, from every source)

Before stage-filtering or scoring anything, check one thing: **does the transcript or
insight name the vendor we're prospecting FOR as already contacted, demoed, or quoted?**
Check against the `own_vendor_names` list `vendor-profile` produces — company name and
product/brand name both, since officials may say either.

If yes — **automatic reject, full stop.** Doesn't matter how good the budget, authority,
or recency looks.

This is a different check from "is a vendor already named" in the stage filter below. A
**competitor or incumbent** named as the system currently in use, with no replacement
chosen yet, is a legitimate — often the *best* — displacement signal ("we're on Verizon
Connect and looking at what else is out there" is exactly what we want). But when **our
own vendor's name is already in the room** — a demo already run, a quote already on the
table — that jurisdiction isn't a discovery for that vendor's sales org. Their own rep
already has, or should have, visibility into it. Presenting it as newly-found pre-RFP
pain is wrong on the merits (the sales cycle is already open, this isn't early-stage) and
undercuts the whole pitch, which is *finding the pain before anyone else knows about it.*

**Failure mode, worked (do not repeat):** a Samsara profile run surfaced a Clarksville,
TN budget committee meeting where staff said they'd "gotten some additional quotes, one
specifically with Samsara... we've actually done some demos with them." That's a vendor
already engaged — demos run, quotes in hand — not a pre-RFP signal. It got scored highest
of the batch and led the board. It should have been rejected on sight: the name match
alone is disqualifying, before any scoring runs.

**This applies to `search-insights` results too**, not just raw transcript hits — an
insight can carry a `Signal Match: 9/10` on budget and recency while completely missing
that the named vendor is us. The guardrail is about the underlying meeting, not which
tool surfaced it.

### Guardrail 1 — stage filter (pain vs. procurement)

**The single most important rule after Guardrail 0: we are hunting for PAIN, not PROCUREMENT.**

Cloverleaf's unique value is the spoken-word transcript — officials describing a problem
*out loud, in a meeting, before they've decided what to do about it.* That early window —
"our system keeps going down," "we're still on paper," "the audit found gaps," "this thing
is end-of-life" — is the signal no one else can sell you. By the time a jurisdiction has
posted an RFI, called an RFP hearing, awarded a contract, or kicked off an implementation,
the opportunity is **already public, already contested, and already late.** RFI/RFP/award
data lives on procurement portals and bid-aggregator platforms; a rep who waits for it is
competing with everyone else who pulled the same feed. The whole point of mining transcripts
is to reach the official *before* that stage exists.

So **stage is the primary filter after the own-vendor check:**

- ✅ **Early-stage pain (the target).** An official voicing a problem, a frustration, a
  failing system, a compliance gap, an incident — with **no solution chosen yet.** This is
  the signal. Up-rank hard.
- ⚠️ **Mid-stage (marginal).** "We're forming a committee to look at options," "we should
  budget for this next year." Worth noting, but the problem is already on its way to a
  process. Keep only if the pain is specific and you can get in before requirements lock.
- ❌ **Late-stage (reject — this is NOT a Cloverleaf signal).** An RFI or RFP already
  issued, an RFP hearing scheduled, a contract awarded, a vendor already named, or a project
  in kickoff/implementation. The decision window has closed or is closing, and this
  information is available through better channels for that stage. **Do not feature these as
  opportunities,** even if a named speaker and full contacts are attached. A complete contact
  roster on a deal that's already moving is a polished card for a lead that's gone.

### Guardrail 2 — minimum specificity (reject generic noise)

A signal must have at least ONE of: (1) a named speaker with a title, (2) a specific
incident, system, project, or capability gap, or (3) a dollar figure, grant reference,
or budget line item. **Reject signals with none of the three.** "Cybersecurity is
important to our community," with no name, no system, and no dollars, is noise.

Once a result clears **all three** guardrails (not our vendor, early/mid-stage pain, and
minimum specificity), score it on:

1. **Named speaker with budget authority** — IT Director, CISO, City/County Manager,
   CFO. A named speaker with a title in the transcript is gold; pull their email/phone
   from `list-contacts` (transcript results no longer carry contact info inline).
2. **Specificity of the pain** — a concrete failing system, incident, audit finding, or
   capability gap. Generic "cybersecurity is important" commentary is noise.
3. **Recency** — within 30 days is hot; 30–90 days is warm; 90–180 days is background.

Down-rank: `person` is null AND text is generic. Reject outright: our own vendor already
named, or anything at RFI/RFP/award/kickoff stage. Up-rank: named speaker + specific
*unsolved* problem + matching roster contact + recent date.

**Litmus test before featuring any signal, in this order:**
1. **Is our own vendor already named as contacted, demoed, or quoted?** If yes — reject,
   stop here, don't bother scoring the rest.
2. **Has this jurisdiction already decided what they're doing?** If yes — even partially
   (RFI out, RFP hearing called, an incumbent vendor named as a done deal, project kicked
   off) — it fails. A named *competitor* with no decision made yet is fine and often
   exactly what you want; a named *us* at any stage is not.
3. **Does it carry a name, a specific gap, or a number?** If none of the three, it's
   generic noise — drop it.

---

## Result structure — `run-meeting-keyword-search` (August 2026 shape)

Returns two parallel arrays plus counts (`total_meeting_hits` is the true meeting
count):

**`meeting_hits[]`** — quotes + speaker attribution (NOTE: no more inline contact info):
```jsonc
{
  "id": 19286232,
  "hits": 25,
  "time": 1784219956000,
  "already_viewed": false,
  "terms": [{"term": "firewall", "count": 25, ...}],
  "transcripts": [{
    "text": "the amount of attacks that we have every day... our firewall is constantly battling",
    "start_time": 6756.72,
    "person": {                      // CHANGED: name/org/title only —
      "name": "Brandon Brand",       // email/phone come from list-contacts now
      "organization": "County of Hunt",
      "title": "IT Director"
    }
  }]
}
```

**`meetings[]`** — org metadata, join to `meeting_hits` by `id`:
```jsonc
{
  "id": 19286232,
  "cloverleaf_url": "https://app.cloverleaf.ai/meetings/19286232",   // NEW — the citation link
  "organization_name": "County of Hunt",
  "state": "Texas", "county": "Hunt", "city": null,
  "source_video_url": "http://youtube.com/watch?v=...",
  "published_at": "2026-07-16T16:39:16",
  "duration_seconds": 9970,
  "is_spam": false,
  "spam_certainty": 0.95,            // NEW
  "user_marked_spam": false          // NEW
}
```

**Parsing note:** When results are saved to a file (large payload), the actual payload
lives at `inner['meeting_hits']` and `inner['meetings']` after a second JSON parse of
the `text` field. Build a `meta` dict keyed on meeting ID from `inner['meetings']` and
join against `meeting_hits`.

**Noise is still yours to filter:** `is_spam` misfires both ways (judge by content),
Federal rows still rank high on cyber topics, and duplicate uploads of the same
meeting under two IDs are still common — dedupe on `organization_id` + title +
published date, never on meeting ID alone. Watch for mis-attributed channels too (a
"Sealy City Council" meeting was filed under County of Austin).

---

## Recurring territory sweep (monitor mode)

For standing coverage ("what's new since last time"), run a dual-layer sweep with a
freshness window. `territory-monitor` routes here for these mechanics.

```jsonc
{ "territory": ["TX","OK"], "terms": ["ransomware","penetration testing"],
  "since": "2026-06-09", "seen_meeting_ids": [], "seen_document_ids": [] }
```

**Freshness:** (1) date window — set `daysBack` to cover `now - since`; (2) seen-id list
— drop hits whose ID is in the seen set; (3) `already_viewed` flag — down-rank, don't
hard-filter (it means "the rep saw it in-platform," not ground truth).

**The sweep:** Layer 1 `run-meeting-keyword-search` (states + terms + window). Layer 2
`run-document-keyword-search` (solution terms, and pass `states` — the old 500 bug is
fixed). Watchlist orgs: walk each with `list-organization-meetings` and keep meetings
newer than `since`.

```
TERRITORY DIGEST — {territory} — new since {since} ({today})
{N} new signals ({n_hot} hot)
NEW & NOTABLE (strongest first)
- {Jurisdiction, ST} — {one-line} — {speaker/role or vendor+$}
PROCUREMENT MOVES
- {Jurisdiction} — {RFP/renewal/award, with $ if present}
--- save for next run ---
seen_meeting_ids / seen_document_ids / next "since": {today}
```

---

## Presentation hygiene

Every signal shown to a rep or customer carries: org name, state, meeting date, a short
verbatim quote, and the timestamp (pair `start_time` seconds with `source_video_url` for
the exact moment). Flag `already_viewed: true` so reps know what they've seen. Never
present spam or Federal rows unlabeled. State explicitly when a roster is empty.

**ASR mangles speaker names** — confirmed live: "Hellman Kava" = Helmin Caba, "Kelly
Curry" = Kelly McNicholas Kury, "Dela Flore" = Della Flora, "Tashnick" = Ptashnik.
Resolve the real name from the `list-contacts` roster plus a quick web check before
putting a name in front of a rep, on a call sheet, or in outreach.

---

## The drill-in kill shot

For a chosen meeting, cite its `cloverleaf_url` as the link. For the live-video
moment, pair the quote's `start_time` (seconds) with `source_video_url`. In a demo:
"Would you rather read a line in clerk-written minutes — or watch the IT Director say
it live?"

---

## Worked example (live-captured; pattern re-verified August 2026)

**City of Snoqualmie, WA — Finance & Admin Committee:**

Keyword search (`security operations center`, `cybersecurity`, `incident response`,
state=`WA`) surfaced a meeting where IT Director Fletcher LaCroix told the Finance
Committee their five-year-old cybersecurity solution was expiring, it lacked a SOC,
and they evaluated six replacements.

`lookup-organization("City of Snoqualmie, WA")` → ID 2908 (read the whole list; check
`meeting_count`). `list-contacts(organizationId=2908)` returned the full roster:

- **Fletcher LaCroix** · IT Director · flacroix@snoqualmiewa.gov · 425-888-8010
- **Drew Bouta** · Finance Director · dbouta@snoqualmiewa.gov · 425-888-1555
- **Mike Chambless** · City Administrator · mchambless@snoqualmiewa.gov · 425-888-8009
- **Jo Johnson** · Council Member (Finance Chair) · jjohnson@snoqualmiewa.gov

No enrichment vendor, no web search, no guessing — full contact roster from Cloverleaf in two
tool calls after the signal was found. (The transcript identified the speaker; the
roster supplied the email and phone — that division of labor is now mandatory, since
transcript results no longer carry contact blocks.)

Note this one clears Guardrail 0 cleanly: "six replacements" evaluated, none named,
including no mention of any vendor we'd be prospecting for. That's what a clean pass
looks like.

---

## Hand off

Once you have scored signals + contacts:

- **`signal-dashboard`** — render into a sortable, scannable dashboard with full
  contact cards per signal. Link each signal's `cloverleaf_url`.
- **`opportunity-enrichment`** — fill in budget, timeline, and decision-maker context
  via web + Apollo.io. This is also where `get-meeting-transcripts` gets pulled, on the
  shortlisted signals only — never during discovery.
- **`signal-outreach`** — draft personalized outreach quoting the official by name.
- **`document-signal-search`** — pair spoken pain with the procurement-side evidence
  (now with working `states` scoping and a semantic `search-documents` tool).
- For mandate-driven pipeline (laws that create budgets and requirements), use the new
  legislation layer — recipes in `cloverleaf-mcp-operations`, play 5.
