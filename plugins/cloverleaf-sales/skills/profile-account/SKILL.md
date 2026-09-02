---
name: profile-account
description: >
  Capture or update government-account intelligence in the local Obsidian "Account
  Intelligence" vault from Cloverleaf AI data. Use whenever the user finds a signal worth
  keeping, preps a meeting/demo, or says "profile <jurisdiction>", "add this to the vault",
  "update my account file for X", or "what do we know about City/County of X". Insights-first,
  transcripts only when warranted; creates accounts/people/vendors if missing, appends new
  facts if present. Never fabricates — unknown stays blank.
---

# Profile Account → Account Intelligence Vault

Maintain the compounding knowledge base in the user's Public Sector Orgs Obsidian vault
(default `~/Documents/Public Sector Orgs`). The goal: every bit of meeting/demo prep the
user does gets **deposited** into durable, linked notes so profiles grow richer over time.

## Vault map (organized by GEOGRAPHY — three layers: State → Area → Org)
- `<State>/<Area>/<Entity>, <ST>/<Entity>, <ST>.md` — one folder per government entity; the
  AREA layer is the metro/region and holds every distinct org in it (city, county, transit
  authority, toll authority, school district). e.g.
  `Texas/Dallas/City of Dallas, TX/…`, `Texas/Dallas/Dallas Area Rapid Transit (DART)/…`
  - Choosing the area: use the metro/principal-city name (Dallas, San Antonio, Tampa Bay); for a
    standalone county with no obvious metro, use the county name (Culpeper). If genuinely
    ambiguous, ask the user.
- `<State>/<Area>/<Area> Area.md` — the area index note (create when creating a new area folder;
  copy the dataview blocks from an existing one, swapping the `area = "X"` and folder filters).
- `<State>/<Area>/<Entity>, <ST>/Contacts/<Name>.md` — decision-maker dossiers UNDER their account.
- `Vendors/<Name>.md` — incumbents & competitors (cross-cutting at vault root — a vendor spans
  multiple accounts, so it is NOT nested under one)
- `Home.md` — vault homepage (auto-populates; don't hand-edit its queries)

## Account frontmatter conventions
- `area:` — the area name exactly as the folder (drives area indexes)
- `location: [lat, long]` — stamp from Cloverleaf contact geo data (county_lat/county_long or
  city_lat/city_long) so the account pins on the Account Map dashboard
- Approximate renewal dates: set `renewal:` to the best-inference ISO date AND add
  `renewal_note: "approximate — <the wording actually heard>"`. Dashboards show ≈ for these.
  Only do this when a timeframe was actually stated — never invent one.
- `Dashboards/` — Dataview roll-ups (do not hand-edit; they query by tag)
- `Templates/` — Account.md, Person.md, Vendor.md (copy these when creating)

File naming — folder name always equals note name:
- Cities/counties: `<Entity>, <ST>` (e.g. `County of Culpeper, VA`)
- Authorities & special districts: their common name with acronym, NO state suffix
  (e.g. `Dallas Area Rapid Transit (DART)`, `North Texas Toll Association (NTTA)`)
- People by display name; vendors by brand. Spell the U.S. state folder in full (`Texas`,
  `Virginia`). Wikilinks resolve by note name regardless of folder — match them exactly
  (Obsidian is case- and punctuation-sensitive).

## Tagging (drives the dashboards)
- Account notes: `tags: [account, <ST>]`  ·  People: `tags: [person, ...]`  ·  Vendors: `tags: [vendor, ...]`
- Dashboards and cross-references use `FROM #account` / `#person` / `#vendor` — NOT folder paths —
  so a note works no matter which state folder it lives in. An account's own solution-stack table
  uses `FROM #account\nWHERE file.name = this.file.name`.

## Workflow

1. **Resolve the jurisdiction.** `lookup-organization` (Cloverleaf) → confirm the org id and
   exact name. If ambiguous, ask the user which match.

2. **Check the vault first.** Look for `<State>/<Area>/<Entity>, <ST>/<Entity>, <ST>.md`
   (search by note name — the area folder may vary).
   - **Missing** → determine the area, create `<State>/<Area>/<Entity>, <ST>/` and the note from
     `Templates/Account.md`; create `<Area> Area.md` too if the area folder is new.
   - **Exists** → read it; note what's already known so you only ADD new facts (never
     overwrite a confirmed value; if something changed, append a dated note rather than
     silently replacing).

3. **Insights-first (cheap).** `search-insights` with `searchTerm` = the distinctive token of
   the name (e.g. "Culpeper"). Match by `organization_name`. Parse the `Signal Match: N/10`
   score and the summary. Update `signal_strength` to the max score seen. Add a dated entry to
   the **Signal Log**.

4. **Only dig deeper when warranted.** Pull the full transcript (`get-meeting-transcripts`) or
   run `run-meeting-keyword-search` ONLY if: the insight is strong (≥6), or it names a vendor /
   dollar figure / renewal worth chasing, or the user asks. Don't burn calls on 0/10 meetings.

5. **Update the solution stack (dynamic fields).** In the account frontmatter `solutions:` list,
   add or update entries. Create a new `area` the moment you learn one (e.g. "Endpoint Protection"
   → vendor "CrowdStrike"). Fill `vendor`, `annual_spend`, `renewal`, `status`, `source`,
   `learned` **only when found — leave blank otherwise.** `status` is a short kebab-case state —
   common values: incumbent | evaluating | gap | end-of-life | forced-replacement | modernizing |
   unknown; richer values are fine when they say more (e.g. renewal-upcoming, rfp-imminent,
   funded-program, incumbent-under-scrutiny). Reuse an existing value when one fits rather than
   minting near-duplicates.
   A confirmed `renewal` date is what powers the Displacement Calendar — capture it whenever stated.

6. **People compound.** For each decision-maker learned (`list-contacts`, or named in a
   transcript): create `<the account's folder>/Contacts/<Name>.md` from the template if missing,
   else append. Add new **dated quotes** verbatim with source link; update priorities,
   `budget_authority`, `email`, `phone`, `last_seen`. Set the person's `account:` frontmatter to
   the `[[<Entity>, <ST>]]` wikilink, and link the person from the account's `people:` list and
   body. (Wikilinks resolve by note name, so nesting under `Contacts/` doesn't break them.)

7. **Vendors compound.** For each incumbent/competitor learned: create/append
   `Vendors/<Name>.md`. Record which account (dated), any **known weakness / displacement wedge**,
   and renewal/contract facts if found.

8. **Keep links tight.** Every person → `account:` wikilink; every account → `people:` wikilinks;
   solution `vendor` names should match a `Vendors/` note where one exists so the Graph View and
   vendor roll-ups connect.

## Hard rules
- **Never fabricate.** No invented budgets, renewal dates, emails, or quotes. Unknown = blank;
  it fills on a later visit. This is the whole point — the vault must be trustworthy in a demo.
- **Append, don't clobber.** Preserve prior dated entries; new visits add, they don't erase.
- **Attribute everything** to a source meeting link and a date.
- Convert relative dates to absolute (ISO) so Dataview can sort them.
- After updating, briefly tell the user what changed (new account? which fields/people/vendors
  added?) and point them to the Displacement Calendar if a renewal/trigger was captured.

## Trigger examples
- "Profile County of X" / "add City of Y to the vault"
- After a Workbench signal: "save this account"
- "What do we know about <jurisdiction>?" → read the note (and offer to refresh it)
- A recurring/scheduled territory sweep that profiles each account with a fresh signal
