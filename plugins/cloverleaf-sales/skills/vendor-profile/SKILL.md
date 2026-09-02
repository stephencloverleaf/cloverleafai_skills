---
name: vendor-profile
description: >-
  Pre-research a vendor company (and optionally a named contact) from nothing but a
  name or website, and build a sales-ready VENDOR PROFILE whose main payoff is a
  ready-to-run Cloverleaf search plan: the pain-point keywords government officials
  actually say out loud, the named competitors/incumbents worth hunting for
  displacement deals, the jurisdiction types and buyer roles that fit, and the
  funding/grant hooks. Use this BEFORE running cloverleaf-signal-search whenever you
  are handed a new vendor/prospect/company to build pipeline for — e.g. "research
  GitLab," "build a profile for this company or website," "who would buy this and what
  do I search," "set me up to prospect for this vendor," or any new logo before the
  first signal sweep. This is the VENDOR side and the step-0 that makes signal search
  actually hit. It is distinct from opportunity-enrichment, which researches the
  GOVERNMENT buyer AFTER a signal is found.
---

# Vendor Profile (step 0 — research the company you're prospecting for)

## Why this skill exists

`cloverleaf-signal-search` only works if you search the **pain, not the product** —
officials never say "CrowdStrike" or "GitLab" in a council meeting; they say "we got
hit by ransomware," "our deployments take three weeks," "the audit found gaps." So the
quality of every signal sweep is capped by how well you've translated *what this vendor
sells* into *the language a government official would use to describe the problem it
solves.*

**Coverage note (don't treat Cloverleaf as SLED-only).** Cloverleaf indexes *any
publicly available public-sector meeting* — federal departments and agencies,
congressional and advisory committees, states, counties, cities, school boards, and
special districts. The "pain, not product" rule above holds for local meetings, but it
**relaxes at the federal level**: agency witnesses and committee members routinely say
the product category out loud ("DevSecOps," "software factory," "continuous ATO," "zero
trust"), so for federally-oriented vendors you can often search the category name
directly. The federal signal also reads differently — it is frequently *oversight
pressure* (a member of Congress saying an agency's systems are broken) rather than a
budget owner voicing intent. That still points you at an agency under pressure; you then
find the actual program office / CIO off-platform.

That translation is the job. A vendor profile is not a marketing summary — it is the
**input that makes the search hit.** The single most valuable thing this skill produces
is the **Cloverleaf search plan** at the end: term arrays, competitor terms, fit
filters, and funding hooks that drop straight into `run-meeting-keyword-search` /
`search-meetings`.

Everything else in the profile (what they sell, ICP, contact context) exists to make
that search plan correct and to give Stephen account context.

## Inputs

- **Required:** a vendor company name **or** website URL. That's enough to start.
- **Optional:** a named contact (person at the vendor) — if given, add the contact
  block. If not given, skip it; do not invent one.
- **Optional:** a territory. If Stephen names one (e.g. "TX only"), put it in the search
  plan's `states`. If he doesn't, leave `states` open — his default territory is the
  **entire U.S.**, and he narrows to a rep's territory only situationally. Don't assume
  Texas.

## Research workflow — cheap, authoritative sources first

Spend effort in this order. Stop when the search plan is solid; you do not need a
dossier, you need correct search terms.

### 1. The vendor's own website (authoritative for *what they sell*)
`web_fetch` the homepage, the product/solutions pages, and any "public sector,"
"government," "SLED," or "industries" page. Pull, in **plain language** (strip the
marketing):
- What category/categories they actually play in (e.g. "EDR/endpoint," "DevSecOps
  platform," "MDR/SOC-as-a-service," "GIS," "AI assistant for government").
- The concrete problems they claim to solve and the outcomes they sell on.
- Named **customers/case studies**, especially any government/SLED logos — these tell
  you which jurisdiction types already buy this.
- Any **compliance/authorization** posture relevant to gov buyers: FedRAMP (and level),
  StateRAMP, CJIS, FIPS, SOC 2, IL4/IL5. These are both credibility and search hooks.

### 2. Web search (competitors, news, gov footprint, triggers)
Run a few angles (adapt the name):
- `"<Vendor>" competitors OR alternatives` and `"<Vendor>" vs` — to build the
  **competitor/incumbent list** (you'll search these names too; a competitor named in a
  meeting = an active evaluation = a displacement opening).
- `"<Vendor>" government OR "public sector" OR SLED customers` — real gov footprint.
- `"<Vendor>" FedRAMP OR StateRAMP OR CJIS` — authorization status from primary sources.
- `"<Vendor>" cooperative contract OR NASPO OR Sourcewell OR GSA OR "state contract"` —
  how a government can actually buy them (lowers procurement friction = stronger plays).
- `"<Vendor>" funding OR acquisition OR layoffs OR breach` (news) — recent triggers that
  shape urgency or talk track.

Prefer the vendor's `.gov`-facing pages, the FedRAMP marketplace, and primary news over
aggregators. **If you can't verify something, say so** — an unverified FedRAMP claim is
worse than "not found; verify on marketplace.fedramp.gov."

### 3. Contact + firmographics via MCP (only if useful)
The Apollo.io connector is for **firmographics and the named contact**, not the product
research above. (Apollo.io replaced ZoomInfo on 2026-08-11; the `enrichment-provider`
skill carries the full tool mapping.)
- If a contact name was given: `apollo_people_match` to confirm role, seniority, and what
  they own (federal vs SLED, product line). This shapes the talk track, not the search terms.
- For company size, HQ, or employee count, a quick `apollo_organizations_enrich` on the
  domain is fine. Don't burn credits enriching things you don't need for the profile.
- **Note the boundary:** Apollo here describes the *vendor*, where its commercial
  firmographics are strongest. The same tools get used again later by
  `opportunity-enrichment` to describe the *government buyer* once a signal is found, where
  coverage is thinner. Don't confuse the two passes.

## The translation layer (the core deliverable)

Convert what the vendor sells into the four things the search plan needs. For the
category-by-category term banks, named competitors, and grant hooks, read
**`references/term-banks.md`** — it covers cyber sub-domains plus non-cyber categories
(DevSecOps, AI/automation, networking, ERP/GIS) so this works for GitLab and Anthropic,
not just security vendors.

The method (apply it even for a category not in the reference file):

1. **Pain terms** — what does an official *say* when they have this problem? Write the
   incident, the project, and the budget-line phrasings. "Endpoint protection" → officials
   say `ransomware`, `data breach`, `endpoint`, `device compromise`, `cybersecurity audit`.
   "DevSecOps platform" → `software development`, `application modernization`, `legacy
   system`, `IT modernization`, `developer`, `agile`. Always include 2–4 angles, not one
   perfect term. **Federal exception:** at the federal level the category vocabulary is
   spoken aloud, so add the product/category terms themselves (`DevSecOps`, `software
   factory`, `continuous ATO`, `zero trust`) to the federal term set — see the Federal
   vocabulary section of `references/term-banks.md`.
2. **Competitor terms** — the incumbents/products an official might name mid-evaluation.
   These are separate search runs (displacement plays), flagged as such.
3. **Funding/trigger terms** — the grant or budget language that signals money is moving:
   `SLCGP`, `cyber insurance`, `IT budget`, `cybersecurity grant`, `ARPA`, `bond`,
   `capital improvement`. Map to the vendor's category.
4. **Own-vendor names** — the exact strings that mean "this vendor is already in the
   room," not a discovery. Include the legal/brand name and any product name officials
   might say instead, if it differs from the company name (e.g., a platform name distinct
   from the corporate parent). This list feeds `cloverleaf-signal-search`'s Guardrail 0
   directly: any transcript or insight naming us as already contacted, demoed, or quoted
   gets auto-rejected before scoring, full stop — a live deal in our own pipeline is not
   a pre-RFP signal, no matter how good the budget or timing looks.

If the vendor spans multiple categories, produce a small term set per category rather
than one bloated query — broad/common terms over long windows blow past Cloverleaf's
context limit and the result gets dumped to a file.

## Output: the profile (use this exact structure)

Lead with substance, no warm-up. Markdown, with a fenced search-plan block at the end so
it round-trips into the next skill.

```markdown
# Vendor Profile — <Company>

## What they sell (plain)
<2–4 sentences: category(ies), the problem they solve, how a gov buyer would describe the need>

## Cloverleaf fit read
**<strong / medium / weak>** — <one line, stated up front before anyone burns sweeps:
is Cloverleaf the right channel for this vendor, and which level carries the signal
(federal / state / local / higher-ed)? E.g. "Strong, federal-led: agencies say the
category aloud in hearings; thinner at the local level where few entities write software.">

## Who buys it (ICP)
- **Jurisdiction types:** <federal dept/agency / congressional or advisory committee / state / county / city / K-12 / higher-ed / water-utility / special district>
- **Buyer roles (own the budget):** <agency CIO/CISO / program office / IT Director / CIO / CISO / City-County Manager / Finance / Superintendent / procurement>
- **Gov footprint / proof:** <named customers if found (note federal vs SLED), else "none verified">

## Buyability
- **Authorizations:** <FedRAMP level / StateRAMP / CJIS / IL4-5 / none found — cite source or mark unverified>
- **Contract vehicles:** <Carahsoft/aggregator / NASPO / Sourcewell / GSA / state contract — or "none found">
- **Procurement friction read:** <low / medium / high, one line why>

## Competitors / incumbents to hunt
<list — these become displacement search runs>

## Triggers (recent)
<funding, breach, acquisition, leadership change — or "none notable found">

## Contact (only if one was given)
- <name, title, what they own, email/phone if verified, source>

## Cloverleaf search plan  ← the payoff
```jsonc
{
  "primary_terms_sled": ["<pain term>", "<pain term>", "<project term>"],   // local: search the PAIN
  "primary_terms_federal": ["<category term>", "<pain term>"],              // federal: category spoken aloud, search it directly (omit if vendor isn't federal-relevant)
  "competitor_terms": ["<incumbent/product>", "..."],                      // separate displacement run
  "own_vendor_names": ["<Company>", "<product/brand name if different>"],  // reject list — feeds signal-search Guardrail 0, never mixed into a search query
  "funding_terms": ["SLCGP", "cyber insurance", "IT budget"],              // optional precision angle
  "states": [],                          // empty = full U.S. (Stephen's default); fill only if territory named
  "days_back": 90,                       // 30–90; never omit (no date silently = last 7 days only)
  "fit_filters": {                       // how to SCORE hits for this vendor
    "jurisdiction_types": ["federal agency", "state", "county", "city", "higher-ed"],
    "buyer_roles": ["agency CIO/CISO", "IT Director", "CISO", "City Manager"]
  },
  "notes": "Run primary first; if thin, widen days_back. Run competitor_terms as a 2nd pass. run-meeting-keyword-search caps at 25 results."
}
```
```

### Rules the search plan must respect (verified Cloverleaf behavior)
- `days_back` 30–90. **Never omit a date** — with no date the tools only look back 7 days.
- `states` empty = nationwide (Stephen's default). Only fill it if a territory was named.
- Keep terms **specific** ("ransomware resiliency," "security operations center") over
  generic ("technology," "security") — generic + wide window overflows context.
- Competitor terms are a **separate run**, not mixed into the pain query.
- `own_vendor_names` must cover every string an official might actually say for us — the
  company name and the product/brand name both, whenever they differ. This is a reject
  list, not a search list: never pass it as `terms` to a search tool.
- `run-meeting-keyword-search` returns at most **25 results, no pagination** — so precise
  terms beat broad ones. Use `mustIncludeTerms`/`proximity` if a query is too noisy.
- **Higher-ed-heavy vendors:** universities rarely surface in broad keyword sweeps the way
  city councils do. For these, name the target institutions and walk their meetings with
  `lookup-organization` → `list-organization-meetings` (board of regents / trustees, IT
  governance) instead of relying on a nationwide keyword sweep.

## Honesty rules (non-negotiable)
- Never fabricate a FedRAMP status, customer logo, competitor, contract vehicle, contact,
  or metric to fill the template. Mark unknowns "not found / verify."
- Distinguish what the vendor *claims* (their site) from what's *independently verified*
  (third-party, marketplace, news).
- If a section has nothing real, leave it short and say so. A thin profile with sourced
  facts beats a full one with fiction — and a wrong search term wastes a real sweep.

## Output 2 — Cloverleaf Account Profile fields (copy/paste into the platform)

Beyond the profile doc above, Stephen needs values that paste directly into Cloverleaf's
own **Account → Profile** settings page. That's a real form, not a report: Job title,
Industry, Focus Area, Competitor, Products/Services You Offer, and Pain Points Your
Product Solves — where Focus Area, Competitor, Products/Services, and Pain Points are each
**repeaters** (a `+` button adds another box). So this block gives **one short, literal
value per line, numbered**, ready to paste into consecutive boxes — no paragraphs, except
where the field itself expects a directive (Focus Area).

Always produce this as a second, separate block after the main profile doc.

```markdown
## Cloverleaf Account Profile — copy/paste fields

**Job title:**
<role> - <Vendor>
<!-- e.g. "Account Executive - Threefold AI." Placeholder seller persona — swap in
     Stephen's real title if this account represents him rather than a rep at the vendor. -->

**Industry:**
<2–5 words, lowercase, terse — mirror the platform's own style ("cybersecurity"), not a sentence>

**Focus Area** (one box each)
1. Identify the top 3 opportunities for <category>. Score them 1 through 10 for how relevant they are.
2. In the 3 opportunities, summarize who spoke, their role, the main quote that proves there is an opportunity with a timestamp, what the suggested next step is, and how far along in the opportunity it is (awareness, initial research, seeking funding, going to RFP, vendor chosen).

**Competitor** (one box each — identical to, or a subset of, "Competitors / incumbents to hunt" above; don't create a second, divergent list)
1. <competitor 1>
2. <competitor 2>
3. <competitor 3>

**Products/Services You Offer** (one box each — concrete noun phrases, matching the
platform's own terseness: "firewalls," "wireless access points," not "we sell firewalls
to protect networks")
1. <product/service>
2. <product/service>
(5–8 items)

**Pain Points Your Product Solves** (one box each — the official's language, the same
"pain, not product" translation used in the search plan, not the vendor's outcome-marketing copy)
1. <pain point>
2. <pain point>
(as many as genuinely verified — no padding to hit a round number)
```

### Rules for this block
- **Focus Area 2 is boilerplate.** Reuse it verbatim across every vendor profile. Only
  Focus Area 1 changes per vendor — just the category name gets swapped in. Add a third
  Focus Area only if Stephen wants an extra cut (e.g., federal vs. SLED, or a named
  territory) — don't invent one by default.
- **Industry is a label, not a sentence.** Match the terseness of the platform's own
  example — a couple of words, lowercase.
- **Job title is a placeholder persona**, not a researched fact — flag it as such so
  Stephen knows to swap in his own title if he's the one logging in as himself.
- **Products/Services and Pain Points follow the same honesty rule as the rest of the
  profile** — no invented line items to fill boxes. A short list beats a padded one.
- **Competitor list here must match** the "Competitors / incumbents to hunt" list in the
  main profile doc — reuse it, don't re-derive a different one.

## Hand off
Pass the **Cloverleaf search plan** to `cloverleaf-signal-search` (it maps directly onto
`terms` / `states` / `daysBack`). Run the primary terms first, then the competitor terms
as a displacement pass. `own_vendor_names` travels with it and feeds that skill's
Guardrail 0 automatically. The signal-search skill also handles document/procurement
searches and recurring territory sweeps — all three guardrails (own-vendor, stage filter,
minimum specificity) apply to every signal from every source.
From there the normal workflow continues: `signal-dashboard` ->
`opportunity-enrichment` (government side) -> `signal-outreach`.
