# Changelog

Claude Code resolves this marketplace by commit, so there are no version numbers. Every merge
to `main` is a release. Entries are newest first.

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
