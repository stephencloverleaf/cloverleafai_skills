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
`territory-monitor`), 4 only in the work library (`cloverleaf-ai-profile`,
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
`humanizer`, `rfp-timeline`, `territory-monitor` (personal); `cloverleaf-ai-profile`,
`cloverleaf-mcp-operations`, `cloverleaf-signals-email`, `police-chief-transitions` (work);
`enrichment-provider`, `sales-communication`, `profile-account` (Claude Code).

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
