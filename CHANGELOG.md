# Changelog

Claude Code resolves this marketplace by commit, so there are no version numbers. Every merge
to `main` is a release. Entries are newest first.

## 2026-09-02

Scope narrowed to MCP connector skills; optimization pass.

- Verified the claude.ai web app plugin install against this repo (Cloverleaf sales, version 1). Refresh behavior test commit.
- Merged `cloverleaf-ai-profile` into `vendor-profile` and deleted the `cloverleaf-ai-profile`
  folder. `vendor-profile` gained the predecessor's primary-industry line, products list,
  pain-points list, and `anchored_terms` mapping; fixed the stale 25-result cap claim
  (pagination is real); added vendor-search rules (one name per query, ASR spelling, re-derive
  across meeting and document layers); inlined Apollo tools with the credit caveat; moved the
  Account Profile form block to `references/account-profile-fields.md`. 289 to 259 lines.
- Moved 10 skills out of the plugin and out of this repo to `~/Developer/skills-personal/` on
  Stephen's Mac (not committed anywhere), because they cover brand, copy, playbook, Gmail,
  browser automation, or a personal vault rather than a Cloverleaf or Apollo MCP call:
  `cloverleaf-copy-editor`, `cloverleaf-profile-setup`, `cloverleaf-signals-email`,
  `enrichment-provider`, `humanizer`, `logo-usage-guidelines`, `product-marketing-framing`,
  `profile-account`, `sales-communication`, `typography-brand-guidelines`.
- `cloverleaf-mcp-operations`: moved recipes to `references/recipes.md` and added
  `references/response-shapes.md` with live field lists; folded purchase rows into the tool
  matrix with a `Verified` date column; kept rules 1 through 8 and added rule 9 (speaker
  attribution is inference, sanitize `person.organization`) and rule 10 (`department` is the
  buyer on a purchase row); absorbed vendor-search and acronym-collision rules that lived only
  in memory; cut the stale changelog section. 442 to 163 lines plus 2 references.
- `cloverleaf-signal-search`: dropped the duplicated tool matrix; restructured to four
  guardrails, adding guardrail 3 (who owns the problem); moved term banks, anchoring, and
  ambiguity traps to `references/query-craft.md` and worked examples to
  `references/worked-examples.md`; recurring-sweep mechanics now defer to `territory-monitor`
  instead of hosting them. 510 to 207 lines plus 2 references.
- `document-signal-search`: opens with a stage table (legislation, documents, purchases); added
  a federal-awards section noting award stage only, `department` is the buyer, no
  `cloverleaf_url`; moved vocabulary to `references/procurement-vocabulary.md`; added the 0.75
  document score calibration. 220 to 146 lines plus 1 reference.
- `rfp-timeline`: removed three stale rules (no `states` on document search, a 25-meeting cap,
  no pagination); added `search-purchases` and `run-purchase-keyword-search` as Source C; render
  section now points at `signal-dashboard` instead of restating hex codes. 264 to 220 lines.
- `government-entity-profile`: dropped the `enrichment-provider` dependency and inlined three
  Apollo tools with the credit-counter caveat and async phone reveal; added the
  mixed-governing-body, roster-contamination, and `meeting_count` coverage checks. 109 to 138
  lines.
- `territory-monitor`: was a redirect into `cloverleaf-signal-search`; now stands alone with a
  config block, a three-layer freshness model, four sweep layers, a digest template, and a
  carry-forward block; uses `list-organization-meetings` instead of
  `lookup-organization.last_published_at` for freshness. 34 to 119 lines.
- `refresh-connectors`: added a "How enumeration actually works" section documenting that
  Claude Code's deferred tool list gives names only and ToolSearch returns `{"type": "object"}`
  with the tool name as its description; updated the matrix row format to three columns.
  89 to 83 lines.
- `opportunity-enrichment`: added a "Verify before you enrich" section (speaker names are
  inference, re-derive timestamps, dedupe sessions, buyer-ownership test, awarded means dead);
  inlined the full Apollo mapping table and the async phone reveal, dropping the
  `enrichment-provider` reference; added purchases as an award-stage cross-check; output block
  now carries `speaker_confirmed` and cites `cloverleaf_url`.
- `signal-dashboard`: rewrote the script's reader for the live `search-meetings` shape
  (`meeting_hits[]` plus `meetings[]`, no `person` block) and added readers for
  `search-insights` and `search-documents`; removed link construction so cards cite
  `cloverleaf_url` verbatim; added a full-state-name to code map and a semantic-relevance
  scoring band; moved input shapes to `references/input-shapes.md`. 171 to 143 lines.
- `signal-outreach`: added four pre-draft kill checks (speaker confirmed, stage open, buyer
  owns the problem, quote read in context) that force NOT READY TO SEND when unmet; dropped
  `app.cloverleaf.ai` links from outbound in favor of a plain source line; rewrote Mode B to
  the three-move shape with the standard closer; added `references/outreach-checklist.md`.
- `demo-mcp`: chain is now the five plugin skills in order with `signal-outreach` as phase 5;
  removed the `cloverleaf-ai-profile` mention and local `/mnt` paths; added the guardrails
  inline (date window, never search the vendor's own name, buyer-ownership, cite
  `cloverleaf_url`).
- `police-chief-transitions`: checked the tool sequence against the ops reference (bare tool
  names, pagination, `startDate`/`endDate`, dedupe, cite `cloverleaf_url`); made the CRM step
  conditional on a connector being attached; added speaker-attribution and
  wrong-jurisdiction checks.
- Connector facts confirmed live on 2026-09-02: the Claude Code harness sends every MCP
  parameter as a string, so numeric and array parameters fail validation in a Claude Code
  session (verify parameter names and types from the resulting validation error); ToolSearch
  returns an empty `{"type": "object"}` schema and echoes the tool name as the description for
  this connector; `search-insights` accepts an undocumented `includeFullResult` parameter
  (effect unverified); purchase rows carry no `cloverleaf_url` and list the whole federal org
  list on every row, so `department`, not `organization_names`, is the buyer.

## 2026-09-02

Initial marketplace.

- Added the `cloverleaf-sales` plugin with 24 skills: 20 merged from the personal and work
  claude.ai skill libraries, 3 from `~/.claude/skills`, and `refresh-connectors`, written for
  this repo.
- Merged the 11 skills that exist in both libraries, choosing the base by manifest `updatedAt`
  and porting the content the older copy held. `MERGE-NOTES.md` records every choice and every
  edit.
- Removed every instruction to call ZoomInfo, retired on 2026-08-11, and repointed those steps
  at Apollo.io per the `enrichment-provider` skill.
- Replaced references to the retired Cloverleaf `search` tool with `search-meetings`, and
  rewrote account-specific `mcp__<server-id>__` prefixes to bare tool names.
- Vendored the AI Sales Communication Playbook into
  `sales-communication/references/playbook/` and rewrote the absolute paths in
  `sales-communication` and `profile-account`.
- Added `connectors/cloverleaf.tools.json` (20 tools, snapshot 2026-09-02, 18 descriptions from
  the `cloverleaf-mcp-operations` tool matrix), `connectors/apollo.tools.json` (73 tools, names
  only), and `connectors/retired.json`.
- Documented the purchases layer, `search-purchases` and `run-purchase-keyword-search`, in the
  `cloverleaf-mcp-operations` tool matrix. Both tools are live on the connector but no workflow
  skill uses them yet.
- Added `scripts/check_tool_drift.py` (fails on retired names, unknown family tools, and
  account-specific server prefixes), `scripts/package_skills.sh`, and a GitHub Actions workflow
  that runs the drift check and validates the manifests.
