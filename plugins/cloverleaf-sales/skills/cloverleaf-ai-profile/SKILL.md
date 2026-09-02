---
name: cloverleaf-ai-profile
description: >-
  Research a vendor or technology company by name and build a sales-ready CLOVERLEAF AI PROFILE
  that translates what they sell into problem-based keywords government officials actually say
  in public meetings. The profile includes industry overview, competitors, service/product breakdown,
  pain points solved, and a ready-to-run Cloverleaf search plan with problem-based keywords,
  problem-anchored keywords, and competitor displacement terms. Use this whenever you need to
  research a vendor to build Cloverleaf signal pipeline — e.g. "profile Liquid Networx," "build a
  profile for this company," "what should we search for this vendor," or "set me up to prospect
  for this company." This is step-0 research that makes signal search actually hit.
---

# Cloverleaf AI Profile — SUPERSEDED, kept for reference only

> **Use `vendor-profile` instead.** Same job — vendor → Cloverleaf search plan — plus the
> federal/SLED vocabulary split, buyability/authorization research, higher-ed guidance,
> and an `own_vendor_names` field that `cloverleaf-signal-search`'s Guardrail 0 checks
> against to auto-reject signals where our own vendor is already engaged. `demo-mcp` now
> calls `vendor-profile` in Phase 1. This file is not deleted in case anything else still
> references it, but new work should not start here.

## Why this skill exists

The quality of every Cloverleaf signal sweep is capped by how well you've translated *what this
vendor sells* into *the language a government official would use to describe the problem it
solves.* Officials never say "Liquid Networx" or "Fortinet" in a city council meeting; they
say "we had a breach," "our phone system keeps dropping calls," "the audit found compliance gaps,"
or "we need to upgrade our firewall."

This skill takes a vendor company name, researches its primary industry, competitors, services,
pain points, and translates all of that into:

1. **Problem-based keywords** — the incidents and issues officials voice
2. **Problem-anchored keywords** — problem terms paired with confirming context (e.g., "dropped calls"
   + "VoIP" within 15 seconds)
3. **Competitor terms** — displacement search runs for incumbents/alternatives
4. **A ready-to-run Cloverleaf search plan** that drops straight into `cloverleaf-signal-search`

The single most valuable output is the **Cloverleaf search plan**: term arrays, competitor terms,
fit filters, and funding hooks that feed the search tool.

## Inputs

- **Required:** a vendor company name (or website URL). That's all you need.
- **Optional:** a territory. If named (e.g. "TX only"), it goes into the search plan's `states`.
  If not, search defaults to nationwide.

If the skill is called with **no company name given**, ask the user for one before proceeding.

## Research workflow — cheap, authoritative sources first

Spend effort in this order. Stop when the search plan is solid; you do not need a dossier,
you need correct search terms.

### 1. The vendor's own website (authoritative for *what they sell*)
`web_fetch` the homepage and products/services pages. Pull, in **plain language** (strip
marketing):
- **Primary industry** — the main category they operate in (e.g., "Telecommunications / Managed Services,"
  "Cybersecurity / MSP," "Cloud Infrastructure")
- **Products/services list** — concrete offerings (firewalls, VoIP, EDR, compliance audits, etc.)
- **What problems they solve** — outcomes, benefits, pain they address
- **Named customers/case studies** — especially any government/public-sector logos
- **Compliance posture** — FedRAMP, StateRAMP, SOC 2, etc. (if selling to government)

### 2. Web search (competitors, footprint, pain points)
Run a few angles:
- `"<Vendor>" competitors OR alternatives` — build the competitor/incumbent list
- `"<Vendor>" government OR "public sector" customers` — real gov footprint
- General web search to verify the company exists and understand its market position

### 3. Synthesize into search plan
Use web_search results and the company's own website to build pain-based keyword sets and
competitor lists that will feed Cloverleaf search.

## Output: the profile (use this exact structure)

Lead with substance, no warm-up. Markdown, with a fenced search-plan block at the end so
it round-trips into `cloverleaf-signal-search`.

```markdown
# Cloverleaf AI Profile — <Company>

## Primary industry
<one line: the main category they operate in>

## What they sell (plain)
<2–4 sentences: products/services, the problems they solve, how a government official would describe the need>

## Key services/products
- <product/service>
- <product/service>
- (list 5–8 concrete offerings)

## Pain points they solve
- <official's language for the problem>
- <official's language for the problem>
- (list the incidents, issues, and needs they address)

## Competitors / incumbents to hunt
<list — these become displacement search runs>

## Cloverleaf search plan  ← the payoff
```jsonc
{
  "primary_problem_keywords": [
    "data breach",
    "ransomware",
    "network outage",
    "dropped calls"
  ],
  "problem_anchored_keywords": [
    { "primary": "firewall", "anchor": "outdated | replacement | renewal | upgrade | next-gen" },
    { "primary": "network security", "anchor": "breach | incident | attack | vulnerability | threat" },
    { "primary": "VoIP", "anchor": "migration | replacement | outdated | modernize | upgrade" },
    { "primary": "compliance", "anchor": "audit | certification | PCI | SOC 2 | requirements" }
  ],
  "competitor_terms": ["<competitor>", "<incumbent>"],
  "states": [],
  "days_back": 90,
  "fit_filters": {
    "jurisdiction_types": ["city", "county", "state", "federal agency", "school district"],
    "buyer_roles": ["CIO", "CISO", "IT Director", "City Manager", "CFO"]
  },
  "notes": "Run primary_problem_keywords first. Use problem_anchored_keywords to narrow results to relevant conversations. Run competitor_terms as a separate displacement pass."
}
```
```

## Honesty rules (non-negotiable)
- Never fabricate a competitor, service, or pain point. If you can't verify it from the company's
  website or credible web search, say "not found" or "unverified."
- Distinguish what the vendor *claims* (their website) from what's *independently verified*
  (web search, third-party sources).
- A thin, accurate profile beats a full one with invented terms — wrong search keywords waste
  real Cloverleaf sweeps.

## Hand off
Pass the **Cloverleaf search plan** to `cloverleaf-signal-search`. Run the primary problem keywords
first. Use problem-anchored keywords to tighten results. Run competitor terms as a separate
displacement pass. From there: `signal-dashboard` → `opportunity-enrichment` → `signal-outreach`.
