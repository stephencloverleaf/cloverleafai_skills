# Merge notes

How the 24 skills in `plugins/cloverleaf-sales/skills/` were assembled on 2026-09-02, and
every edit made to the source files along the way. Source files were copied, never moved or
modified.

## Sources

| Source | Path | Synced | User-created skills |
|---|---|---|---|
| Personal library (stephengwhite94@gmail.com) | `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/4e130dd6-.../skills/` | 2026-09-02 | 16 |
| Work library (stephen@cloverleaf.ai) | `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/1eb59d7c-.../skills/` | 2026-08-27 | 15 |
| Claude Code user skills | `~/.claude/skills/` | live | 3 (`notebooklm` excluded as third-party) |

Every `creatorType: "anthropic"` skill was excluded: `consolidate-memory`, `docx`,
`explain-usage`, `import-memory`, `mcp-builder`, `morning`, `pdf`, `pptx`, `schedule`,
`setup-cowork`, `skill-creator`, `slack-gif-creator`, `web-artifacts-builder`, `xlsx`.

The union of user-created skills is 20, not 24: 5 exist only in the personal library
(`cloverleaf-profile-setup`, `government-entity-profile`, `humanizer`, `rfp-timeline`,
`territory-monitor`), 4 only in the work library (`cloverleaf-ai-profile`, merged into
`vendor-profile` on 2026-09-02 and deleted, see "Optimization pass, 2026-09-02" below;
`cloverleaf-mcp-operations`, `cloverleaf-signals-email`, `police-chief-transitions`), and
**11 in both**. The build brief expected 13 in both; the manifests say 11. Adding the 3
Claude Code skills and the new `refresh-connectors` gives 24. No user-created skill in either
manifest was left out.

## Base selection for the 11 skills in both libraries

Base chosen by the newer `updatedAt` in the manifests. Every pair differed, so the SKILL.md
mtime tie-break never applied. Note that all work-library files carry the same mtime
(2026-08-27 10:13, the sync time), so mtime is meaningless there. Two personal files were
edited locally after their manifest `updatedAt` (`opportunity-enrichment` on 2026-08-11,
`demo-mcp` on 2026-07-10); the rule still put the work copy first in both cases, and the
content those local edits carried was ported in by hand.

| Skill | Personal `updatedAt` | Work `updatedAt` | Base | Ported from the older copy |
|---|---|---|---|---|
| cloverleaf-copy-editor | 2026-07-15 | 2026-07-31 | work | Nothing. |
| cloverleaf-signal-search | 2026-07-15 | 2026-08-18 | work | 6 blocks, listed later. |
| demo-mcp | 2026-07-02 17:31 | 2026-07-02 18:16 | work | Nothing. |
| document-signal-search | 2026-07-15 | 2026-08-18 | work | Nothing. |
| logo-usage-guidelines | 2026-07-15 | 2026-06-10 | personal | 2 asset files plus the Assets section rewrite. |
| opportunity-enrichment | 2026-07-02 17:31 | 2026-07-02 18:17 | work | The whole Apollo.io section. |
| product-marketing-framing | 2026-07-15 | 2026-05-11 | personal | Nothing. |
| signal-dashboard | 2026-07-15 | 2026-07-02 | personal | 2 hand-off bullets. |
| signal-outreach | 2026-06-15 | 2026-07-02 | work | The "Brand voice" section. |
| typography-brand-guidelines | 2026-06-25 | 2026-05-06 | personal | Files are byte-identical. |
| vendor-profile | 2026-07-07 | 2026-07-02 | personal | `references/term-banks.md`, which the personal copy cites but does not carry. |

Skills taken whole from one source: `cloverleaf-profile-setup`, `government-entity-profile`,
`humanizer`, `rfp-timeline`, `territory-monitor` (personal); `cloverleaf-ai-profile` (work,
merged into `vendor-profile` on 2026-09-02 and deleted, see "Optimization pass, 2026-09-02"
below), `cloverleaf-mcp-operations`, `cloverleaf-signals-email`, `police-chief-transitions`
(work); `enrichment-provider`, `sales-communication`, `profile-account` (Claude Code).

## Per-skill detail

### cloverleaf-signal-search (base: work, 2026-08-18)

The work copy is a later rewrite: it carries the legislation layer, `search-documents`, the
fixed `states` behavior on document search, the August 2026 result shape, and the fact that
transcript hits no longer carry contact blocks. The personal copy holds material the work
copy dropped, all of it cited by other skills, so six blocks were ported in:

1. **Guardrail 2 (minimum specificity)**, plus a third litmus-test item. The work copy names
   only Guardrails 0 and 1, but `government-entity-profile`, `vendor-profile`, `demo-mcp`,
   and `territory-monitor` all refer to "the three guardrails".
2. **A "Known data defects" section**, from the personal copy's rules 5, 6, and 7: city
   metadata is roughly 28% populated, org names and states can be wrong (Greene Public
   Schools, City of Blue Ash), and `search-insights` can misattribute a speaker (Southampton,
   VA).
3. **The `search-campaigns` row** in the tool inventory, with the `filterParams` integer-geo-ID
   caveat and the two proven cyber campaign IDs. The work inventory omits the tool.
4. **Two `list-contacts` notes**: contacts can live under a different org ID than the meetings
   (Freeport, IL), and drop `removed_at` records and dedupe by email.
5. **The "Recurring territory sweep (monitor mode)" section.** `territory-monitor` is a router
   that points here for these mechanics, so without it that skill dangles.
6. **The "Presentation hygiene" section**, including the ASR-mangled speaker names (Helmin
   Caba, Kelly McNicholas Kury, Della Flora, Ptashnik).

Corrected while porting: the personal copy's "never pass `states` to
`run-document-keyword-search`" claim. The work copy verified on 2026-08-18 that the bug is
fixed, so the ported sweep passes `states`.

Not ported: the personal copy's "Seven rules" framing and its Recipes block (the work copy
carries equivalent examples inline), and its "Document signals (procurement-stage)" section
(superseded by the work `document-signal-search`, which is fuller and current).

### opportunity-enrichment (base: work, then fully re-pointed at Apollo)

The two copies differ only in the enrichment provider. The work copy is the ZoomInfo version;
the personal copy was edited on 2026-08-11 to replace ZoomInfo with Apollo.io. Because no
instruction to call ZoomInfo may survive, the whole `### 3. ZoomInfo MCP` section was replaced
with the personal copy's `### 3. Apollo.io MCP` section, and three ZoomInfo mentions in the
description and the source-order text were switched to Apollo. The three remaining mentions of
ZoomInfo are historical (it was retired, its coverage was better for government), which matches
`enrichment-provider`.

### signal-dashboard (base: personal)

The personal copy is the brand-corrected one: the official palette (Ink Navy `#1B232E`, Sky
`#CCF1FD` / `#A9E3F4`), the explicit "there is no Cloverleaf green", and a `build_dashboard.py`
that embeds the real white logo lockup as a data URI. The work copy still bakes in the
fabricated navy `#1B2A4A` and green `#2E8B57` and draws the logo as a green dot. Ported from
the work copy: the two hand-off bullets naming `document-signal-search` and `territory-monitor`,
both of which ship here as separate skills.

### logo-usage-guidelines (base: personal)

The personal SKILL.md is stronger (it forbids recreating the logo or substituting a stand-in
shape) but says the text-only wordmarks are "not yet bundled". The work copy bundles them, so
both SVGs were copied in and the Assets section now lists all four files while keeping the
personal copy's prohibitions.

### signal-outreach (base: work)

The work copy is the newer of the two by `updatedAt` and is otherwise identical to the personal
copy minus one section. The personal copy's "Brand voice (Cloverleaf AI tone)" section was
ported back in whole, with the stale agency count corrected (see "Stat corrections").

### vendor-profile (base: personal)

The personal copy adds the "Cloverleaf Account Profile fields" block (the copy-and-paste values
for the platform's Account settings form) and a fuller hand-off. The work copy carries
`references/term-banks.md`, which the personal SKILL.md cites twice but does not ship, so that
file was copied in.

### demo-mcp, document-signal-search, cloverleaf-copy-editor (base: work)

Nothing to port. The personal `demo-mcp` is a July 10 condensation of the same material, and its
explicit three-guardrail enumeration is preserved through `cloverleaf-signal-search`. The
personal `document-signal-search` is a 2 KB stub that routes to `cloverleaf-signal-search`; the
work copy is the real skill. The personal `cloverleaf-copy-editor` lacks the work copy's current
platform stats, ROI figures, and customer quotes.

## Reference fixes

### Absolute and machine-specific paths

| File | Change |
|---|---|
| `sales-communication/SKILL.md` | The playbook's 4 markdown files were copied to `references/playbook/`. The absolute `/Users/swhite/Documents/Sales Resources/AI Sales Communication Playbook/` reference now says the repo copy ships with the skill and is canonical for the plugin. The 4 routing-table filenames, the hard-fails pointer, the application-layer pointer, and the enforcement pointer all became `references/playbook/...` paths. |
| `sales-communication/SKILL.md` | The absolute `/Users/swhite/Documents/Sales Resources/Cloverleaf_Email_Voice_Guide.md` became `Cloverleaf_Email_Voice_Guide.md` in the user's Sales Resources folder (default `~/Documents/Sales Resources/`). That file is outside the playbook folder and is not vendored here. |
| `profile-account/SKILL.md` | The absolute vault path became "the user's Public Sector Orgs Obsidian vault (default `~/Documents/Public Sector Orgs`)". |
| `demo-mcp/SKILL.md` | `/mnt/skills/user/signal-dashboard/scripts/build_dashboard.py` became `<path-to>/signal-dashboard/scripts/build_dashboard.py`. The claude.ai path is wrong for plugin installs, and the skill's own copy of the command is the reference. |
| `enrichment-provider/SKILL.md` | The trailing Obsidian wikilink `[[outbound-stack-gojiberry-hubspot]]` was dropped; it resolves only inside the vault. |

### Account-specific MCP server prefixes

| File | Change |
|---|---|
| `opportunity-enrichment/SKILL.md` | `Tool prefix mcp__ae38a734-...__` became an instruction to use the bare tool names, because every account gets its own Apollo server ID. |
| `enrichment-provider/SKILL.md` | The same prefix line, and the `select:mcp__ae38a734-...` ToolSearch example, were rewritten to name the bare tools and tell the reader to use the prefix their own session reports. The retired ZoomInfo server ID was dropped. |

### Retired tool names

The live Cloverleaf server offers exactly the 20 tools in `connectors/cloverleaf.tools.json`.
The bare `search` tool and the underscore spellings are gone.

| File | Was | Now | Why |
|---|---|---|---|
| `signal-dashboard/SKILL.md` (description) | raw `search` output | raw `search-meetings` output | Context is transcript search output feeding the dashboard. |
| `signal-dashboard/SKILL.md` (input list) | Raw transcript `search` output | Raw transcript `search-meetings` output | Same. |
| `signal-dashboard/scripts/build_dashboard.py` (header comment) | raw Cloverleaf transcript `search` output | raw Cloverleaf transcript `search-meetings` output | Same. |
| `vendor-profile/SKILL.md` | drops into `run-meeting-keyword-search` / `search` | `run-meeting-keyword-search` / `search-meetings` | The pair is lexical plus semantic transcript search. |
| `police-chief-transitions/SKILL.md` | "Do NOT use the bare `search` tool for name recovery, it has no state filter" | "Do NOT run an unscoped `search-meetings` for name recovery, without `states` it floods" | The replacement tool does accept `states`, so the warning had to move from the tool to the missing parameter. The lesson (nationwide noise, including movie transcripts) is unchanged. |

Left alone deliberately: `` `search` `` in `notebooklm` (excluded from this repo), and the
Apollo search tools, which are named in full and unambiguous.

### ZoomInfo to Apollo.io

ZoomInfo was retired on 2026-08-11 and its MCP server is disconnected, so no instruction to
call it survives. `enrichment-provider/SKILL.md` is the authority for the replacements.

| File | Change |
|---|---|
| `opportunity-enrichment/SKILL.md` | Description, source-order line, credit line, and the entire provider section (see above). |
| `demo-mcp/SKILL.md` | "a ZoomInfo credit" became "an Apollo credit"; "use ZoomInfo for larger agencies and contact confirmation" became "use Apollo.io". |
| `document-signal-search/SKILL.md` | Hand-off "via web + ZoomInfo" became "via web + Apollo.io". |
| `cloverleaf-signal-search/SKILL.md` | Hand-off "via web + ZoomInfo" became "via web + Apollo.io"; the worked example's "No ZoomInfo, no web search" became "No enrichment vendor, no web search". |
| `vendor-profile/SKILL.md` | The "Contact + firmographics via MCP" step named `contact_research` and `enrich_companies`. It now names `apollo_people_match` and `apollo_organizations_enrich`, points at `enrichment-provider`, and notes that Apollo's government coverage is thinner than its commercial coverage. |
| `rfp-timeline/SKILL.md` | Two "ZoomInfo lookup" action buttons became "Apollo lookup". |

`government-entity-profile/SKILL.md` already pointed at Apollo.io and needed no change.
All 11 retired ZoomInfo tool names are recorded in `connectors/retired.json`, so the drift
check fails if one reappears.

### Superseded tool behavior

The August 2026 verification pass fixed the `states` bug on `run-document-keyword-search`.
Three files still carried the old workaround and would have shipped a known-false instruction:

- `cloverleaf-signal-search/SKILL.md`, in the ported territory-sweep section.
- `territory-monitor/SKILL.md`, Layer 2 of the dual sweep.
- `government-entity-profile/SKILL.md`, the document-search step.

Each now says to pass `states` and notes that the old 500 error is fixed.

### Stat corrections

Stephen's standing rule is never to print "45,000+ agencies"; the site says 70K+, and the work
`cloverleaf-copy-editor` in this repo lists "70K+ agencies tracked" as current. Six occurrences
of `45,000+` were changed to `70,000+`: four in `product-marketing-framing/SKILL.md` (two
objection handles, the proof list, and the jargon-replacement list), and two in
`cloverleaf-copy-editor/SKILL.md` (the specificity example and the numerals example). The
"Brand voice" section ported into `signal-outreach` carried a seventh, corrected on the way in.
This is the only change made to skill prose that was not a path, tool name, or provider fix.
Revert it if the figure was deliberate.

### New content

- `cloverleaf-mcp-operations/SKILL.md`: two rows added to the end of the tool matrix for
  `search-purchases` and `run-purchase-keyword-search`, marked "New since 2026-08-18 snapshot
  (seen 2026-09-02)", with the live parameter details, plus a short note that no workflow skill
  uses them yet and which two are the obvious candidates. The heading count went from 18 to 20.
- `refresh-connectors`: a new skill, written for this repo. It has no source copy.

## Residual differences not carried over

- `cloverleaf-signal-search`: the personal copy's "Seven rules" framing, its Recipes code block,
  and its document-signals section.
- `demo-mcp`: the personal copy's condensed prose and its explicit three-guardrail enumeration.
- `cloverleaf-copy-editor`: the personal copy's step-3 cross-reference wording ("see Company Name
  Usage above").
- `product-marketing-framing`: the work copy's expanded acknowledge, reframe, bridge bullet
  formatting. The personal base states the same handles in prose.
- `signal-dashboard`: the work copy's `build_dashboard.py`, entirely. It is the off-brand
  version.
- `logo-usage-guidelines`: the work copy's softer Assets wording.
- Both libraries keep their own copies of everything. Nothing here was written back to them.

## Addendum, 2026-09-02 (post-build audit)

- `sales-communication`: `Cloverleaf_Email_Voice_Guide.md` was referenced by a local path that teammates do not have. The file is now vendored at `references/Cloverleaf_Email_Voice_Guide.md` and the reference points there. It describes Stephen's personal outreach voice; remove it from the plugin if that should stay personal.
- `scripts/check_tool_drift.py`: two em dashes in output strings replaced with colons.

## Optimization pass, 2026-09-02

Two agents split the 13 remaining connector skills and ran an optimization pass against the
live Cloverleaf AI MCP connector: one covered the search-layer skills, the other covered
vendor, enrichment, presentation, and outreach. `python3 scripts/check_tool_drift.py` exits 0,
0 FAIL, 62 WARN (all pre-existing unused Apollo tools), after both passes.

### Per-skill changes

**cloverleaf-mcp-operations**

- Moved recipes to `references/recipes.md` and added `references/response-shapes.md` with the
  live field lists from the verification calls below.
- Folded purchase rows into the tool matrix with a `Verified` date column.
- Kept rules 1 through 8 and added rule 9 (speaker attribution is inference from both
  endpoints, sanitize `person.organization`) and rule 10 (`department` is the buyer on a
  purchase row).
- Absorbed vendor-search, acronym-collision, insight-layer, timestamp-drift, and
  roster-contamination rules that previously lived only in Stephen's memory files.
- Cut the "what changed since July" changelog section and the fixed-`states`-500 framing.
- 442 to 163 lines plus 2 references.

**cloverleaf-signal-search**

- Dropped the duplicated 11-row tool matrix; the skill now names only the tools its procedure
  uses.
- Restructured guardrails to four: 0 own-vendor (with the footprint-mention trap folded in),
  1 stage, 2 specificity, 3 who owns the problem (new).
- Moved term banks, anchoring, ambiguity traps, and vendor-zero rules to
  `references/query-craft.md`, and worked examples to `references/worked-examples.md`.
- Recurring-sweep mechanics now defer to `territory-monitor` instead of being hosted here.
- 510 to 207 lines plus 2 references.

**document-signal-search**

- Opens with a stage table: legislation is the upstream mandate, documents are the line item
  through award, purchases are the award already made.
- Added a federal-awards section with four caveats: award stage only, coverage beyond federal
  unverified, `department` is the buyer, no `cloverleaf_url`.
- Moved vocabulary, boilerplate traps, and cooperative-vehicle names to
  `references/procurement-vocabulary.md`.
- Added the 0.75 document score calibration.
- 220 to 146 lines plus 1 reference.

**rfp-timeline**

- Removed three stale rules: never pass `states` on document search, a 25-meeting cap, and no
  pagination on the tool.
- Added `search-purchases` and `run-purchase-keyword-search` as Source C, noting a federal
  award has no trustworthy Cloverleaf org id.
- Trimmed the render section to point at `signal-dashboard` instead of restating hex codes.
- 264 to 220 lines.

**government-entity-profile**

- Removed the `enrichment-provider` dependency and inlined three Apollo tools
  (`apollo_organizations_enrich`, `apollo_mixed_people_api_search`, `apollo_people_match`)
  with the credit-counter caveat and the async phone reveal.
- Added the mixed-governing-body and roster-contamination checks, the `meeting_count` coverage
  check, and "an insight sentence is never a quote".
- 109 to 138 lines.

**territory-monitor**

- Was a pure redirect into a section of `cloverleaf-signal-search`; now stands alone.
- Added a config block, a three-layer freshness model, four sweep layers (insights first,
  spoken, procurement, watchlist orgs), a digest template, and a carry-forward block.
- Switched to `list-organization-meetings` rather than `lookup-organization.last_published_at`
  for freshness, per the verified defect.
- Added the recess and coverage-gap honesty rule.
- 34 to 119 lines.

**refresh-connectors**

- Added a "How enumeration actually works" section: in Claude Code the deferred list gives
  names only, and ToolSearch returns `{"type": "object"}` with the tool name echoed as the
  description, so descriptions come from the desktop connector view or a live validation
  probe.
- Updated the matrix row format to the three-column shape the ops file now uses.
- 89 to 83 lines.

**vendor-profile** (absorbed `cloverleaf-ai-profile`, folder deleted)

- Merged in the predecessor's primary-industry line, products list, pain-points list, and
  problem-anchored keyword pairs, now `anchored_terms` mapping to `mustIncludeTerms` plus
  `proximity`.
- Fixed a stale claim that `run-meeting-keyword-search` caps at 25 results with no pagination;
  pagination is real (`perPage` 100, `page`).
- Added vendor-search rules that make a zero publishable: one name per query, ASR spelling,
  re-derive across meeting and document layers.
- Inlined Apollo (`apollo_organizations_enrich`, `apollo_mixed_companies_search`,
  `apollo_people_match`) with the credit caveat and the `apollo_users_api_profile` fix; removed
  the `enrichment-provider` dependency.
- Moved the Account Profile form block to `references/account-profile-fields.md`.
- 289 to 259 lines.

**opportunity-enrichment**

- Added a "Verify before you enrich" section: jurisdiction from transcript content, speaker
  names as inference from both endpoints, read a window, re-derive timestamps, duplicate
  sessions, buyer-ownership test, awarded means dead.
- Inlined the full Apollo mapping table, credit caveat, two-pass rule, and async phone reveal;
  no `enrichment-provider` reference remains.
- Added purchases as an award-stage cross-check only, with `department` as the buyer,
  `organization_names` as the whole federal list on every row, no `cloverleaf_url`, `amount` 0
  on modifications, null dates, federal-only as of 2026-09-02.
- Output block now carries `speaker_confirmed` and cites `cloverleaf_url`.

**signal-dashboard**

- Rewrote the script's reader for the live `search-meetings` shape, `meeting_hits[]` plus
  `meetings[]` with no `person` block, replacing the `{"results": [...]}` shape it was written
  against. Added readers for `search-insights` and `search-documents`; kept the legacy path.
- Removed link construction; cards cite `cloverleaf_url` verbatim.
- Added a full-state-name to code map and a semantic-relevance scoring band, since live
  discussion signals arrive with no speaker.
- Tightened extraction after real-data false positives ("Master" as a vendor, "$0" amounts).
- Moved input shapes to `references/input-shapes.md`.
- 171 to 143 lines.

**signal-outreach**

- Added four pre-draft kill checks: speaker confirmed, stage open, buyer owns the problem,
  quote read in context. Unmet means NOT READY TO SEND.
- Dropped `app.cloverleaf.ai` links from outbound in favor of a plain source line, keeping
  `cloverleaf_url` as an internal citation. No early-signal claim without two dated meetings.
- Rewrote Mode B to the three-move shape with the standard closer ("Cloverleaf AI pulls leads
  like this every day...").
- Added `references/outreach-checklist.md` and the conditional `sales-communication` or
  `humanizer` load.

**demo-mcp**

- Chain is now the five plugin skills in order, with `signal-outreach` as phase 5 rather than
  an optional encore.
- Removed the `cloverleaf-ai-profile` mention and the `/mnt/user-data/outputs/` and other local
  paths.
- Added the guardrails inline: date window, never search the vendor's own name, reject awarded
  or out-to-bid, buyer-ownership, cite `cloverleaf_url`, never print 45,000+.

**police-chief-transitions**

- Checked the tool sequence against the ops reference: bare tool names (was
  "Cloverleaf AI:run-meeting-keyword-search"), pagination, `startDate`/`endDate` as the
  `daysBack` alternative, dedupe, cite `cloverleaf_url`.
- Made the Salesforce step conditional: without a CRM connector, it delivers the transition
  list with warm-path suggestions instead.
- Added the speaker-attribution and wrong-jurisdiction checks.

### Live verifications, 2026-09-02

15 live calls against the connected Cloverleaf AI account (a 15-call budget on one agent, plus
10 on the other), no transcript-content calls:

| Tool | Parameters | Result |
|---|---|---|
| `search-insights` | `searchTerm="cybersecurity"` | 4 insights, all 0/10 gate-excluded; envelope `{insights[], total}`; per row `cloverleaf_url`, `summary`, `result`, `state_name`, no state code. |
| `search-insights` | `searchTerm="firewall"` | `{insights: [], total: 0}`. |
| `search-insights` | `searchTerm="cyber"` | 5 rows, all 0/10 gate-excluded; `result_truncated: true` with an undocumented `includeFullResult` parameter. |
| `search-purchases` | `query="firewall network security contract award"` | `{total_hits:100, purchases[]}`, no `cloverleaf_url`; every row carried the identical whole federal `organization_ids`/`organization_names` list; `department` is the real buyer; `amount` 0 on modifications; `start_date`/`end_date` null. |
| `run-purchase-keyword-search` | `terms="firewall"` | "expected array, received string": confirms `terms` is an array. |
| `search-purchases` | `query`, `states="TX"` | "expected array, received string": confirms `states` exists and is an array. |
| `lookup-organization` | `query="Travis County, TX"` | `{matched, organizations[], state}`; one org showed `last_published_at: 2028-07-07`. |
| `search-documents` | `query="contract award or renewal for firewall and network security equipment"` | `{total_hits:100, total_document_hits:61, documents[]}` with `cloverleaf_url`, `chunks[]`; top hit 0.785, a real Fortinet/CDW-G award. |
| `search-documents` | query plus `startDate`/`endDate` window | 67 document hits; re-surfaced a $4,859,039 CDW-G Palo Alto award. |
| `search-meetings` | query re: replacing old firewalls | `{meeting_hits[], meetings[]}`; `transcripts[]` carries only `id, text, start_time, score`, no `person` block; `spam_certainty` 0.8-0.95 on clean meetings. |
| `search-meetings` | query plus `startDate` 2026-08-28, `endDate` 2026-09-02 | 62 meeting hits, same no-`person` shape; `state` is a full name. |
| `list-organization-meetings` | `organizationId="1242"` | "expected number, received string": confirms the parameter name and numeric type. |
| `run-document-keyword-search` | `terms="firewall"` | "expected array, received string": confirms `terms` is an array. |
| `perPage`, `states` on keyword-search tools | various | rejected as "expected number/array, received string": every parameter is sent as a string in this harness, so no array- or number-typed parameter is callable from it. |
| ToolSearch `select:` on 9 Cloverleaf tools | none | every schema returned `{"type": "object"}` and the description was the bare tool name. |

### Contradictions found and resolved

1. The `cloverleaf-rfp-data-gap` memory said the purchase tools were "not yet in
   `cloverleaf-mcp-operations`". Stale as of this pass's purchase-row edit; resolved in favor
   of the repo.
2. The ops file said `search-insights` is "always the first call, free"; a daily-summary defect
   note said never trust the feed. Both kept, scoped: free and first, but the score is a label
   on everything ingested, not a threshold, and an insight is a lead, not a citation.
3. The ops calibration said semantic score 0.80 or higher is strong. Live document and purchase
   hits top out at 0.785 and 0.789 on good queries. Calibration split: transcripts at 0.80,
   documents and purchases from about 0.75, ranked by `best_score`.
4. `cloverleaf-signal-search` claimed transcript results carry a `person` name, org, and title.
   True for `run-meeting-keyword-search`, false for `search-meetings`, which returns no
   `person` key at all. Recorded per tool in `references/response-shapes.md`.
5. `rfp-timeline` said document search 500s on `states` and keyword search has no pagination.
   Both contradicted by the ops reference and by live behavior; the ops reference won and
   `rfp-timeline` was corrected.
6. `signal-dashboard` and `opportunity-enrichment` each claimed a fixed step number (search,
   dashboard, enrich, outreach), conflicting with the `demo-mcp` chain order. Step numbers were
   removed: the dashboard runs whenever signals exist, enrichment runs between the sweep and
   outreach, and `demo-mcp` enriches before rendering so cards ship complete.
7. The ops reference's `references/response-shapes.md` describes the `run-document-keyword-search`
   envelope as flat hit records with `highlights[]` and `cloverleaf_url`; the shipped
   `signal-dashboard` script assumed an Elasticsearch `hits.hits[]` shape with
   `highlight.plain_text[]`. Neither agent could call the tool live, so the reader now accepts
   both shapes.
8. The 25-meeting cap claimed in `vendor-profile` contradicted the ops reference, which
   documents real pagination. The ops reference won.

### Open questions for Stephen

1. Does `search-purchases` hold anything but `purchase_dataset_id: 1` (federal)? Every sampled
   row was federal. If SLED award data exists, the skills should say so; until confirmed, they
   say the opposite.
2. Purchase rows have no `cloverleaf_url` and no per-award org id. Is there a platform page for
   an award, or is `source_row_id` genuinely the only citation?
3. `run-purchase-keyword-search` published no parameter schema. Confirmed `terms` is an array;
   does it also take `mustIncludeTerms`, `proximity`, `sortBy`?
4. One org in the Travis County probe returned `last_published_at: 2028-07-07`. Data defect
   worth logging in the wiki, or expected?
5. `territory-monitor` now owns the recurring sweep outright. Should the scheduled routines in
   `routines/` be repointed at it?
6. `search-insights` on the connected account returns only `stephen+airsight@cloverleaf.ai`
   counter-UAS insights, all 0/10. Is that the account colleagues will install against? If so,
   the "insights first" opening move will look empty in their first demo.
7. Mode A outreach (vendor rep to government buyer) has no standard closer, only the
   interest-oriented CTA from the playbook. The 8/24 closer is scoped to Mode B. Do you want a
   house closer for the vendor rep too?
8. `signal-dashboard` drops insight rows scored 0/10. Confirm that is right, since it is most
   of what the live feed returns.

## Skills moved out of the plugin

Ten skills moved out of the `cloverleaf-sales` plugin and out of this repo on 2026-09-02,
because they cover brand, copy, playbook, Gmail, browser automation, or a personal vault
rather than a call to the Cloverleaf AI or Apollo.io MCP connector. They now live at
`~/Developer/skills-personal/` on Stephen's Mac and are not committed anywhere:

- `cloverleaf-copy-editor`
- `cloverleaf-profile-setup`
- `cloverleaf-signals-email`
- `enrichment-provider`
- `humanizer`
- `logo-usage-guidelines`
- `product-marketing-framing`
- `profile-account`
- `sales-communication`
- `typography-brand-guidelines`
