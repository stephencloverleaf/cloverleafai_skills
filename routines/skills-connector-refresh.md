# Routine: skills connector refresh

A weekly check that the connector tool manifests in the `cloverleafai_skills` repo still
match the live MCP servers, and that no skill references a tool that moved or disappeared.

## Schedule

Mondays at 06:30 local time, in Claude Code or the Claude desktop app, in a session with the
Cloverleaf AI and Apollo.io connectors attached. A signed-in Claude session is required, so CI
cannot do this.

Claude Code and the desktop app enumerate differently, and the `refresh-connectors` skill
handles both. In Claude Code, the connector's tools arrive in the deferred tool list as names
only; loading one with ToolSearch returns a schema of `{"type": "object"}` and a description
that repeats the tool name. So enumeration there goes by tool name, and descriptions come
from the desktop app's connector view (it shows the server's own descriptions) or from a live
probe that calls the tool with one plausible parameter and reads the validation error. Claude
Code also sends every parameter as a string, so a tool with a numeric or array parameter cannot
be called there at all; the validation error itself ("expected array, received string") is how
you confirm the parameter's name and type without spending a real query.

## The prompt to paste into the scheduled task

Copy everything between the rules.

---

Work in the local repo at `~/Developer/cloverleafai_skills`. If it is missing, stop and
report that instead of cloning anything.

Check that the Cloverleaf AI and Apollo.io connectors are attached to this session. If
either is missing, stop and report which one, because the live tool list is the whole point
of this run.

Run the `refresh-connectors` skill from the `cloverleaf-sales` plugin (`/refresh-connectors`)
and follow it exactly. In short: snapshot the live tool names and descriptions for both
connectors into `connectors/cloverleaf.tools.json` and `connectors/apollo.tools.json` with
today's date, run `python3 scripts/check_tool_drift.py`, fix every FAIL, document each new
tool as a dated row in the tool matrix in `cloverleaf-mcp-operations`, and fix every
reference to a tool that disappeared. Never invent a tool description. Do not rewrite
workflow skills to adopt a new tool unless asked.

Write the run report to `reports/<YYYY-MM-DD>.md` in the repo, using today's date as the
filename. The report covers: connectors checked, new tools with their descriptions and the
skills that could use them, removed or renamed tools with every file edited, the verbatim
drift-script output, and the branch name.

Commit on branch `connector-refresh/<YYYY-MM-DD>`, including the report. Run `gh auth
status`: if it succeeds, push and open a pull request; if it fails, leave the branch local
and say so.

If nothing changed, say so in one line, write the report anyway, and skip the branch.

---

## Proposed entry for `Documents/Claude/ROUTINES.md`

Add this row by hand. This file does not edit the registry.

| Routine | Schedule | Spec | Deposits to | Status | Last verified |
|---|---|---|---|---|---|
| skills-connector-refresh | Mondays 06:30 local | `~/Developer/cloverleafai_skills/routines/skills-connector-refresh.md` | `~/Developer/cloverleafai_skills/reports/<date>.md` plus a `connector-refresh/<date>` branch | Not scheduled yet | 2026-09-02 |
