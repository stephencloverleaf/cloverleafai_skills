# cloverleafai_skills

A Claude Code plugin marketplace holding Cloverleaf AI's connector skills: skills that call the
Cloverleaf AI MCP server to find pre-RFP buying signals in government meetings, enrich them
into opportunities, present them, and write the outreach. That is the whole scope. One plugin,
`cloverleaf-sales`, carries 13 skills. `scripts/check_tool_drift.py` fails the build when a
skill names a tool that `connectors/*.tools.json` does not list for that snapshot date.

Ten skills needing brand, copy, playbook, Gmail, or browser automation, or a personal Obsidian
vault, moved to `~/Developer/skills-personal/` on Stephen's Mac. `MERGE-NOTES.md` lists them.

## Prerequisites

- The Cloverleaf AI MCP connector must be attached. Every skill in this plugin depends on it.
- Apollo.io is optional, for enrichment in `opportunity-enrichment`, `vendor-profile`, and
  `government-entity-profile`.
- A CRM connector is optional, for `police-chief-transitions` to check contacts.

## Colleague access

The repo is private, so each colleague needs read access on GitHub before any install below
will succeed: run `gh auth login`, or store credentials in the system keychain.

## Install in Claude Code

```
/plugin marketplace add stephencloverleaf/cloverleafai_skills
/plugin install cloverleaf-sales@cloverleafai-skills
```

## Install in the Claude desktop app or Cowork

Go to **Customize > Plugins > Personal plugins > + > Add marketplace > Add from a repository**
and paste the GitHub URL. Repeat on each machine; the marketplace is saved locally.

## Install on claude.ai

claude.ai does not sync from GitHub. Skills go up as zips:

1. Run `scripts/package_skills.sh` to write one zip per skill to `dist/`.
2. Upload zips at **Settings > Capabilities > Skills** for personal use, or hand them to an
   org admin to upload at **Organization settings > Skills** for org-wide use.
3. After a change, the admin re-uploads the affected zips. There is no automatic path.

## How updates reach users

Claude Code resolves a git-based marketplace by commit, so every merge to `main` is a new
version. Nothing declares a version number.

- **Auto-update is off by default for third-party marketplaces.** Turn it on once through
  **/plugin > Marketplaces > cloverleafai-skills > Enable auto-update**, or in `~/.claude/settings.json`:

  ```json
  {
    "extraKnownMarketplaces": {
      "cloverleafai-skills": {
        "source": { "source": "github", "repo": "stephencloverleaf/cloverleafai_skills" },
        "autoUpdate": true
      }
    },
    "enabledPlugins": { "cloverleaf-sales@cloverleafai-skills": true }
  }
  ```

- **A private repo added over HTTPS will not auto-update**, because background auto-update
  disables git credential helpers for its `git pull`. Add the marketplace with the SSH URL
  instead, `/plugin marketplace add git@github.com:stephencloverleaf/cloverleafai_skills.git`,
  with an SSH key loaded in `ssh-agent`, or update by hand: `/plugin marketplace update
  cloverleafai-skills` then `/plugin update cloverleaf-sales`.
- Anyone who accepts manual updates can use the HTTPS form instead, with `gh auth login` or
  keychain credentials.
- claude.ai users get changes only when an admin re-uploads the zips.

## Skills

The `cloverleaf-sales` plugin ships 13 skills, grouped by role:

| Skill | Group | What it does |
|---|---|---|
| `cloverleaf-mcp-operations` | Reference | The verified tool reference for the Cloverleaf AI MCP connector: tool names, parameters, limits, and response shapes. |
| `cloverleaf-signal-search` | Discovery | Finds pre-RFP buying signals in live government meeting transcripts and qualifies them against the guardrails. |
| `document-signal-search` | Discovery | Mines meeting documents, state legislation, and federal award records for procurement-stage signals. |
| `territory-monitor` | Discovery | Runs a recurring, territory-scoped sweep and produces a what's-new-since-last-time digest. |
| `rfp-timeline` | Discovery | Traces a contract award backward to its originating RFP and first spoken pain signal. |
| `government-entity-profile` | Discovery | Builds a deep account profile for one named government entity, seen through the lens of one vendor. |
| `police-chief-transitions` | Discovery | Finds newly appointed or interim police chiefs and checks them against a CRM, when one is attached. |
| `vendor-profile` | Vendor and enrichment | Researches a vendor company and produces a ready-to-run Cloverleaf search plan. |
| `opportunity-enrichment` | Vendor and enrichment | Turns one Cloverleaf signal into a workable opportunity using web search and Apollo.io. |
| `signal-dashboard` | Presentation and outreach | Turns Cloverleaf signals into a self-contained, sortable HTML dashboard that opens offline. |
| `signal-outreach` | Presentation and outreach | Turns an enriched signal into copy-paste-ready email, LinkedIn, and call-script outreach. |
| `demo-mcp` | Umbrella | Runs the whole seller workflow live from one company name or topic, chaining the other skills. |
| `refresh-connectors` | Maintenance | Re-snapshots the connector tool manifests in `connectors/` and reconciles the skills against them. |

## Add or change a skill

1. Edit `plugins/cloverleaf-sales/skills/<name>/SKILL.md`. Skills are auto-discovered; a new
   one needs a `name` and `description` in its frontmatter.
2. Run `python3 scripts/check_tool_drift.py`. It must report `0 FAIL`.
3. Run `claude plugin validate ./plugins/cloverleaf-sales` as the local lint.
4. Add a `CHANGELOG.md` entry and open a pull request. Merging to `main` is the release.

## Connector drift

Skills name MCP tools in backticks, and MCP servers change under them. Three things guard it:

- `connectors/*.tools.json` holds a dated snapshot per server. `connectors/retired.json` holds
  names that must never appear in a skill, with what replaced them.
- `scripts/check_tool_drift.py` fails on a retired name, an unknown tool in a connector's
  family, or a hard-coded `mcp__<server-id>__` prefix (server IDs differ per account). It
  warns about unused manifest tools and snapshots older than 45 days.
- The `refresh-connectors` skill re-snapshots the manifests and reconciles the skills, per the
  weekly prompt in `routines/skills-connector-refresh.md`. CI cannot do this part: reading a
  live tool list needs a signed-in Claude session.

## Repo map

```
.claude-plugin/marketplace.json     Marketplace definition
plugins/cloverleaf-sales/
  .claude-plugin/plugin.json        Plugin manifest
  skills/<name>/SKILL.md            13 skills, with their references, scripts, and assets
connectors/*.tools.json             Dated tool snapshots per MCP server
connectors/retired.json             Tool names that must never appear in a skill
scripts/check_tool_drift.py         Drift check, exits 1 on FAIL
scripts/package_skills.sh           One zip per skill into dist/, for claude.ai uploads
routines/skills-connector-refresh.md  Weekly refresh prompt and registry row
.github/workflows/check.yml         JSON validation plus the drift check
MERGE-NOTES.md                      Which source copy won per skill, and what was ported
```
