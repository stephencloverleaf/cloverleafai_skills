---
name: refresh-connectors
description: "Re-snapshot the MCP connector tool manifests in this repo and reconcile the skills against them. Use when the user says refresh connectors, check connector drift, did the Cloverleaf MCP add tools, are the tool manifests current, the connector changed, or when a skill calls a tool the server no longer has. It reads the live tool list for each connector in the connectors directory, rewrites the manifests with today's date, runs the drift script, and reports new and removed tools without rewriting workflow skills unprompted."
---

# Refresh the connector manifests

The manifests in `connectors/` record what each MCP server offered on the snapshot date,
and the skills are written against those names. When a server adds, renames, or drops a
tool, the skills drift and the failure is quiet: a call to a name the server no longer has
returns nothing rather than an error.

Run this in a session that has the connectors attached. Without them you cannot see the
live tool list, and you stop rather than guess. Never fabricate a tool description; leave
the field as it is and say so in the report.

## How enumeration actually works

**In Claude Code, you get names but not descriptions.** The connector's tools arrive in
the deferred tool list under an `mcp__SERVER_ID__` prefix that differs per account.
Loading them with ToolSearch returns a schema of `{"type": "object"}` and a description
that is only the tool name repeated (verified for the Cloverleaf connector on 2026-09-02).
So enumerate by name from the deferred list, and get descriptions and parameters from one
of two places:

- The Claude desktop app's connector view, which shows the server's own descriptions.
- A live probe. Call the tool with one plausible parameter and read the validation error:
  the server names the failing parameter and its expected type. Passing a string where an
  array is expected returns "expected array, received string", which confirms both the
  parameter name and its type without spending a real query.
  In Claude Code sessions the harness sends every parameter as a string, so numeric and
  array parameters cannot be sent from there at all. A successful call proves only the
  string parameters; confirm the rest from validation errors or from the desktop app.

Record the bare tool name, dropping the server id prefix.

## Procedure

1. **Enumerate the live tools for each connector** by the method above. Note which names
   are new against the current manifest and which have disappeared.

2. **Rewrite each manifest.** For every file in `connectors/`, set `snapshot` to today's
   date, set `snapshot_source` to how you observed the list, and write the full tool array
   sorted by name. Keep an existing description when the live list does not supply one;
   never replace a real description with an empty string.

3. **Run the drift script** from the repo root:

   ```bash
   python3 scripts/check_tool_drift.py
   ```

   It exits non-zero on any FAIL, and every FAIL is fixed before you go further. WARN
   lines about unused tools and stale snapshots are information, not blockers.

4. **Document each new tool.** Append a row to the tool matrix in the connector's
   reference skill (`cloverleaf-mcp-operations` for Cloverleaf, the analogous skill for
   another connector), formatted `| TOOL_NAME | TODAY | DESCRIPTION |`. Then list
   in your report which workflow skills could use it and why. Do not rewrite a workflow
   skill to adopt a new tool unless the user asks.

5. **Fix every reference to a removed tool.** Add it to `connectors/retired.json` with
   `retired_on`, `replaced_by`, and a note saying what to use instead. Grep the skills for
   the name, rewrite each mention to the correct current tool by reading the surrounding
   context, and re-run the drift script.

6. **Commit on a branch** named `connector-refresh/DATE`, with a dated entry in
   `CHANGELOG.md` describing what the connector changed and what you edited. Do not add or
   bump a `version` field in `plugin.json` or the marketplace file: Claude Code resolves a
   git based marketplace by commit, so every merge to the default branch is a new version,
   and a declared version nobody bumps freezes users on the cached copy.

7. **Open a pull request, or report the branch.** Run `gh auth status`. If it succeeds,
   push and open a PR whose body lists new tools, removed tools, and the files you
   touched. If it fails, leave the branch local and report its name.

## Report format

- Connectors checked, and the snapshot date you wrote.
- New tools, one line each: name, description, and the skills that could use it.
- Removed or renamed tools, and every file you edited for each.
- The final drift script output.
- The branch name, and the PR link when there is one.
