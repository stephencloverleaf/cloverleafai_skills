# cloverleafai_skills

A Claude Code plugin marketplace holding Cloverleaf AI's sales skills: finding pre-RFP
buying signals in government meetings, enriching them into opportunities, and writing the
outreach under the house sales-communication standard. One plugin, `cloverleaf-sales`,
carries 24 skills. `connectors/` records what the Cloverleaf AI and Apollo.io MCP servers
offered on the snapshot date, and `scripts/check_tool_drift.py` fails the build when a
skill names a tool that no longer exists.

Skills come from two claude.ai libraries (a personal account and a work account) plus three
Claude Code user skills. `MERGE-NOTES.md` records which copy won for each skill and what was
ported across.

## Install in Claude Code

```
/plugin marketplace add stephencloverleaf/cloverleafai_skills
/plugin install cloverleaf-sales@cloverleafai-skills
```

The repo is private, so the machine needs GitHub access first: run `gh auth login`, or store
credentials in the system keychain. Without it, the marketplace add fails.

## Install in the Claude desktop app or Cowork

Go to **Customize > Plugins > Personal plugins > + > Add marketplace > Add from a
repository** and paste the GitHub URL. The marketplace is saved locally on that computer, so
repeat this on each machine.

## Install on claude.ai

claude.ai does not sync from GitHub. Skills go up as zips:

1. Run `scripts/package_skills.sh`. It writes one zip per skill to `dist/`, each with the
   skill folder at the zip root.
2. Upload them at **Settings > Capabilities > Skills** for personal use, or hand them to an
   org admin, who uploads each zip at **Organization settings > Skills**
   (claude.ai/admin-settings/skills) to publish them org-wide.
3. After a change, the admin re-uploads the affected zips. There is no automatic path.

## How updates reach users

Claude Code resolves a git-based marketplace by commit, so every merge to `main` is a new
version. Nothing declares a version number.

- **Auto-update is off by default for third-party marketplaces.** Each user turns it on once,
  through **/plugin > Marketplaces > cloverleafai-skills > Enable auto-update**, or in
  `~/.claude/settings.json`:

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

- **A private repo added over HTTPS will not auto-update.** Background auto-update disables
  git credential helpers for its `git pull`. Either add the marketplace with the SSH URL,
  `/plugin marketplace add git@github.com:stephencloverleaf/cloverleafai_skills.git`, with an
  SSH key loaded in `ssh-agent`, or update by hand with `/plugin marketplace update
  cloverleafai-skills` followed by `/plugin update cloverleaf-sales`.
- Anyone who accepts manual updates can use the HTTPS form,
  `/plugin marketplace add stephencloverleaf/cloverleafai_skills`, with `gh auth login` or
  keychain credentials.
- claude.ai users get changes only when an admin re-uploads the zips.

## Add or change a skill

1. Edit `plugins/cloverleaf-sales/skills/<name>/SKILL.md`. A new skill needs a folder with a
   `SKILL.md` whose frontmatter carries `name` and `description`; skills are auto-discovered.
2. Run `python3 scripts/check_tool_drift.py`. It must report `0 FAIL`.
3. Run `claude plugin validate ./plugins/cloverleaf-sales` (or `/plugin validate` in a
   session) as the local lint.
4. Add a `CHANGELOG.md` entry and open a pull request. Merging to `main` is the release.

## Connector drift

Skills name MCP tools in backticks, and MCP servers change under them. Three things guard it:

- `connectors/*.tools.json` holds a dated snapshot of each server's tool list.
  `connectors/retired.json` holds names that must never appear in a skill, with what
  replaced them.
- `scripts/check_tool_drift.py` scans every skill markdown file and fails on a retired name,
  a name that matches a connector's family but is absent from its manifest, or a hard-coded
  `mcp__<server-id>__` prefix (server IDs differ per account). It warns about manifest tools
  no skill uses and about snapshots older than 45 days. `--json` prints machine output.
- The `refresh-connectors` skill re-snapshots the manifests from the live connectors and
  reconciles the skills. `routines/skills-connector-refresh.md` is the weekly prompt that
  runs it. CI cannot do this part: reading a live tool list needs a signed-in Claude session.

## Repo map

```
.claude-plugin/marketplace.json     Marketplace definition
plugins/cloverleaf-sales/
  .claude-plugin/plugin.json        Plugin manifest
  skills/<name>/SKILL.md            24 skills, with their references, scripts, and assets
connectors/*.tools.json             Dated tool snapshots per MCP server
connectors/retired.json             Tool names that must never appear in a skill
scripts/check_tool_drift.py         Drift check, exits 1 on FAIL
scripts/package_skills.sh           One zip per skill into dist/, for claude.ai uploads
routines/skills-connector-refresh.md  Weekly refresh prompt and registry row
.github/workflows/check.yml         JSON validation plus the drift check
MERGE-NOTES.md                      Which source copy won per skill, and what was ported
```
