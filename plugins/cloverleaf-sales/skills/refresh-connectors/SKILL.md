---
name: refresh-connectors
description: >-
  Re-snapshot the MCP connector tool manifests in this repo and reconcile the skills
  against them. Use when the user says "refresh connectors", "check connector drift",
  "did the Cloverleaf MCP add tools", "are the tool manifests current", "the connector
  changed", or when a skill calls a tool the server no longer has. Reads the live tool
  list for each connector in `connectors/`, rewrites the manifests with today's date,
  runs the drift script, and reports new and removed tools without rewriting workflow
  skills unprompted.
---

# Refresh the connector manifests

The manifests in `connectors/` record what each MCP server offered on the snapshot date.
Skills are written against those names. When a server adds, renames, or drops a tool, the
skills drift, and the failure is quiet: a call to a name the server no longer has returns
nothing rather than an error.

Run this procedure in a session that has the connectors attached. Without them you cannot
see the live tool list, and you must stop rather than guess.

## Before you start

Confirm two things:

- The connectors named in `connectors/*.tools.json` are attached to this session. In
  Claude Code they appear in the deferred-tool list; in the Claude desktop app they appear
  under the connector's own tool list.
- You are working in a clone of this repo and the working tree is clean.

**Never fabricate a tool description.** If a description is not visible, leave the field
as it is and say so in the report.

## Procedure

1. **Enumerate the live tools for each connector.** In Claude Code, read the deferred-tool
   list and use ToolSearch to pull each tool's schema, which carries its description. In
   the desktop app, read the connector's tool list. Record the bare tool name (drop the
   `mcp__<server-id>__` prefix, which differs per account) and the description verbatim.

2. **Rewrite each manifest.** For every file in `connectors/`, set `snapshot` to today's
   date, set `snapshot_source` to how you observed the list, and write the full tool array
   sorted by name. Keep any description you already have when the live list does not
   supply one. Do not drop a description to replace it with an empty string.

3. **Run the drift script.**

   ```bash
   python3 scripts/check_tool_drift.py
   ```

   It exits non-zero on any FAIL. Fix every FAIL before you go further. WARN lines about
   unused tools and stale snapshots are information, not blockers.

4. **Document each new tool.** For every tool in the live list that was not in the previous
   snapshot, append a row to the tool matrix in the connector's reference skill:
   `cloverleaf-mcp-operations` for the Cloverleaf connector, or the analogous reference
   skill for another connector. Format the row as
   `| <tool> | New since <previous snapshot date> (seen <today>) | <description> |`, using
   the server's own description. Then list, in your report, which workflow skills could use
   it and why. **Do not rewrite a workflow skill to adopt a new tool unless the user asks.**

5. **Fix every reference to a removed tool.** For each tool that disappeared, add it to
   `connectors/retired.json` with `retired_on`, `replaced_by`, and a note that says what to
   use instead. Then grep the skills for the name and rewrite each mention to the correct
   current tool, judging by the surrounding context. Re-run the drift script.

6. **Commit on a branch.** Add a dated entry to `CHANGELOG.md` describing what the
   connector changed and what you edited. Do not add or bump a `version` field in
   `plugin.json` or `.claude-plugin/marketplace.json`: Claude Code resolves a git-based
   marketplace by commit, so every merge to `main` is a new version, and a declared version
   that nobody bumps freezes users on the cached copy. Commit on branch
   `connector-refresh/<YYYY-MM-DD>`.

7. **Open a pull request, or report the branch.** Run `gh auth status`. If it succeeds,
   push the branch and open a PR whose body lists new tools, removed tools, and the files
   you touched. If it fails, leave the branch local and report its name so the user can
   push it.

## Report format

Close with a short report:

- Connectors checked, and the snapshot date you wrote.
- New tools, one line each: name, description, and the skills that could use it.
- Removed or renamed tools, and every file you edited for each.
- The final drift-script output.
- The branch name, and the PR link when there is one.
