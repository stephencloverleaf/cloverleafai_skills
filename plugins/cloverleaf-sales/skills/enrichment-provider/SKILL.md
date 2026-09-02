---
name: enrichment-provider
description: Names the current firmographic and contact enrichment provider for all account and opportunity research. Apollo.io replaced ZoomInfo on 2026-08-11; the ZoomInfo MCP is disconnected and any skill, spec, or habit that still calls it will silently return nothing. Load this whenever enriching a company, jurisdiction, or person — and specifically before running opportunity-enrichment, government-entity-profile, vendor-profile, or any account-research step that asks for firmographics, org size, budget, or contact details.
---

# Enrichment provider: Apollo.io

**ZoomInfo is gone.** Its MCP server is no longer connected.
It did not fail loudly — calls to it simply returned nothing, so enrichment steps that depended on it
produced output that looked *thin* rather than *broken*. Two shipped skills still name it:
`opportunity-enrichment` and `government-entity-profile`.

**Apollo.io is the replacement.** Its MCP server is connected. Call the tools by the bare
names in the mapping that follows. Every account gets its own Apollo server ID, so never
hard-code an account-specific MCP server prefix into a skill.

## Tool mapping

| What you needed ZoomInfo for | Use instead |
|---|---|
| Company firmographics from a domain | `apollo_organizations_enrich` (bulk: `apollo_organizations_bulk_enrich`) |
| Find companies matching criteria | `apollo_mixed_companies_search` |
| Find people by title / seniority / org | `apollo_mixed_people_api_search` |
| Confirm or enrich one known person | `apollo_people_match` (bulk: `apollo_people_bulk_match`) |
| Search contacts already in the CRM | `apollo_contacts_search` |
| Hiring signals as a budget/priority tell | `apollo_organizations_job_postings` |

In Claude Code the Apollo tools are deferred: load them with ToolSearch before calling, using
a `select:` query that names the tools you need (for example `apollo_organizations_enrich` and
`apollo_mixed_people_api_search`) with the prefix the session reports for the Apollo server.

## The coverage caveat that matters here

Apollo's strength is commercial firmographics. **Government coverage is thinner than ZoomInfo's was**,
and thinner for small jurisdictions than large ones. That changes the research order for public-sector
work — it does not just swap one tool for another:

1. **Cloverleaf first.** Meeting transcripts and documents are the primary source for a jurisdiction's
   priorities, budget language, and who actually speaks. No enrichment vendor substitutes for this.
2. **The entity's own web presence second.** Staff directories, adopted budget PDFs, org charts, and
   council rosters are more accurate for small and mid-size government than any commercial database.
3. **Apollo third**, for the things it is genuinely good at: the *vendor* side of a deal, larger
   agencies and authorities, and confirming a named person's title and contact details.

**Honesty rule (carried over from the skills this replaces):** if Apollo returns thin or no coverage
for a jurisdiction, say so plainly — "Apollo coverage is thin here; the staff directory is the better
source" — and use the web. Never present an absent enrichment result as a finding, and never fill the
gap with an inference. A blank field is a fact; a guess is a defect.

## Why this file exists at user level

The two affected skills ship inside a plugin whose files live in caches that a plugin update replaces
(`~/Library/Application Support/Claude/.../skills-plugin/...` and `~/.codex/plugins/cache/...`). Those
copies have been edited to point at Apollo, but **a plugin update will silently revert them.** This
file will not be reverted, and it wins on conflict. If you ever see a skill instructing you to call
ZoomInfo, that skill is stale — follow this file instead and re-apply the edit.

