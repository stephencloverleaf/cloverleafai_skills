---
name: vendor-profile
description: >-
  Researches a vendor company from nothing but a name or website and produces a
  sales-ready vendor profile whose payoff is a ready-to-run Cloverleaf search plan: the
  pain-point keywords government officials say out loud, the anchor terms that cut noise,
  the competitors worth hunting for displacement deals, the jurisdiction types and buyer
  roles that fit, the funding hooks, and the own-vendor reject list. Also produces the
  copy-paste values for the Cloverleaf Account Profile settings page. Run this before
  cloverleaf-signal-search on any new vendor or prospect. Trigger phrases: "research
  GitLab", "profile Liquid Networx", "build a profile for this company or website", "who
  would buy this and what do I search", "what should we search for this vendor", "set me
  up to prospect for this vendor", or any new logo before the first signal sweep. This is
  the vendor side. opportunity-enrichment researches the government buyer after a signal
  is found.
---

# Vendor profile

## Why this skill exists

`cloverleaf-signal-search` only works if you search the pain, not the product. Officials
never say "CrowdStrike" or "GitLab" in a council meeting. They say "we got hit by
ransomware", "our deployments take three weeks", "the audit found gaps". The quality of
every sweep is capped by how well you translate what this vendor sells into the language
an official uses to describe the problem it solves.

That translation is the job. The most valuable output is the Cloverleaf search plan at
the end. Everything else exists to make that plan correct.

Two rules govern the plan before you write a single term:

- **Never put the vendor's own name in a discovery query.** Searching the vendor's name
  returns footprint mentions: their name in a payment register, an approved-vendor list, or
  a signed agreement. Those are existing business, not opportunities. The vendor's name
  belongs only in the `own_vendor_names` reject list.
- **Cloverleaf covers federal too.** It indexes any publicly available public-sector
  meeting: federal departments and agencies, congressional and advisory committees, states,
  counties, cities, school boards, and special districts. Never write that federal is
  uncovered. State and local carry more depth because those bodies argue things out in open
  session repeatedly. The pain-not-product rule also relaxes at the federal level, where
  witnesses say the category aloud ("DevSecOps", "zero trust", "continuous ATO"), so a
  federal term set can name the category directly.

## Inputs

- **Required:** a vendor company name or website URL.
- **Optional:** a named contact at the vendor. Add the contact block if one is given. Never
  invent one.
- **Optional:** a territory. Put it in the plan's `states`. With no territory named, leave
  `states` empty, which means nationwide.

If no company name or URL is given, ask for one before proceeding.

## Research workflow

Spend effort in this order and stop when the search plan is solid. You need correct search
terms, not a dossier.

### 1. Read the vendor's own website

Fetch the homepage, the product or solutions pages, and any public sector, government,
SLED, or industries page. Pull the following in plain language, with the marketing
stripped:

- The category or categories they play in, and the primary industry in two to five words.
- The concrete problems they solve and the outcomes they sell on.
- Five to eight named products or services.
- Named customers and case studies, especially government logos, which tell you which
  jurisdiction types already buy this.
- Compliance posture that matters to government buyers: FedRAMP and its level, StateRAMP,
  CJIS, FIPS, SOC 2, IL4 or IL5.

### 2. Search the web

Run a few angles, adapting the name:

- `"<Vendor>" competitors OR alternatives` and `"<Vendor>" vs`, to build the competitor
  list. A competitor named in a meeting means an active evaluation and a displacement
  opening.
- `"<Vendor>" government OR "public sector" OR SLED customers`, for real footprint.
- `"<Vendor>" FedRAMP OR StateRAMP OR CJIS`, for authorization status from primary sources.
- `"<Vendor>" cooperative contract OR NASPO OR Sourcewell OR GSA OR "state contract"`, for
  how a government can actually buy them. Low procurement friction makes a stronger play.
- `"<Vendor>" funding OR acquisition OR layoffs OR breach`, for recent triggers.

Prefer the vendor's government-facing pages, the FedRAMP marketplace, and primary news over
aggregators. If you cannot verify something, say so. An unverified FedRAMP claim is worse
than "not found, verify on the FedRAMP marketplace".

### 3. Use Apollo.io for firmographics and the named contact only

Apollo.io replaced ZoomInfo on 2026-08-11. The ZoomInfo server is disconnected and returns
nothing rather than failing, so any instruction to call it is stale. Apollo tools are
deferred in Claude Code: load them with ToolSearch using a `select:` query before calling,
and use the bare tool names. Every account gets its own Apollo server ID, so never
hard-code a server prefix.

- `apollo_organizations_enrich` on the domain, for size, headquarters, and employee count.
- `apollo_mixed_companies_search` by name, when you do not have the domain.
- `apollo_people_match`, only when a contact name was given, to confirm role, seniority,
  and what the person owns. That shapes the talk track, not the search terms.

Apollo calls consume paid credits, so pull only what the profile needs. Apollo's strength
is commercial firmographics, which is what the vendor side of a profile needs. Its
government coverage is thinner, so do not reuse this pass for the buyer side.
`opportunity-enrichment` handles the buyer side and carries the coverage caveats. To check
remaining credits, read `apollo_users_api_profile`, not the usage-stats tool, which
misreports direct-dial credits as exhausted.

## The translation layer

Convert what the vendor sells into the five things the plan needs. For category term banks,
named competitors, funding hooks, and the federal vocabulary set, read
**`references/term-banks.md`**. It covers cyber sub-domains plus DevSecOps, AI, networking,
ERP, and GIS. Read it whenever the vendor fits one of those categories, or as a model for
writing a category it does not cover.

1. **Pain terms.** What an official says when they have this problem. Write the incident,
   the project, and the budget-line phrasings. "Endpoint protection" becomes `ransomware`,
   `data breach`, `endpoint`, `cybersecurity audit`. Give two to four angles, not one
   perfect term.
2. **Anchor terms.** A confirming word that must appear near the pain term, which is what
   `mustIncludeTerms` plus `proximity` enforce. Anchoring `firewall` to `outdated`,
   `replacement`, `renewal`, or `upgrade` keeps out the building firewalls that zoning
   boards discuss. Anchor only with unambiguous words.
3. **Competitor terms.** The incumbents or products an official might name mid-evaluation.
   These run as a separate displacement pass, never mixed into the pain query.
4. **Funding terms.** Grant or budget language that means money is moving: `SLCGP`, cyber
   insurance, IT budget, E-Rate, ARPA, bond, capital improvement.
5. **Own-vendor names.** Every string an official might say for us: the company name and
   any product or brand name that differs from it. This is a reject list, not a search list.

If the vendor spans several categories, produce a small term set per category rather than
one bloated query.

## Output 1: the profile

Lead with substance. Markdown, with a fenced search-plan block at the end so it round-trips
into the next skill.

```markdown
# Vendor profile: <Company>

## Primary industry
<two to five words, lowercase>

## What they sell (plain)
<two to four sentences: category, the problem they solve, how a government buyer would
describe the need>

## Cloverleaf fit read
**<strong / medium / weak>**: <one line, stated before anyone burns a sweep. Is Cloverleaf
the right channel for this vendor, and which level carries the signal: federal, state,
local, or higher education?>

## Key products and services
<five to eight concrete offerings>

## Who buys it
- **Jurisdiction types:** <federal agency, congressional or advisory committee, state,
  county, city, K-12, higher education, utility, special district>
- **Buyer roles that own the budget:** <agency CIO or CISO, program office, IT Director,
  CIO, CISO, City or County Manager, Finance, Superintendent, procurement>
- **Government footprint:** <named customers if found, noting federal versus SLED, else
  "none verified">

## Buyability
- **Authorizations:** <FedRAMP level, StateRAMP, CJIS, IL4 or IL5, or "none found". Cite
  the source or mark it unverified.>
- **Contract vehicles:** <aggregator, NASPO, Sourcewell, GSA, state contract, or "none
  found">
- **Procurement friction:** <low, medium, or high, and one line on why>

## Competitors and incumbents to hunt
<list. These become displacement search runs.>

## Pain points, in the official's language
<the incidents and problems an official voices, not the vendor's outcome marketing>

## Triggers (recent)
<funding, breach, acquisition, leadership change, or "none notable found">

## Contact (only if one was given)
<name, title, what they own, verified email or phone, source>

## Cloverleaf search plan
```jsonc
{
  "primary_terms_sled": ["<pain term>", "<pain term>", "<project term>"],
  "primary_terms_federal": ["<category term>", "<pain term>"],
  "anchored_terms": [
    { "primary": "firewall", "anchor": ["outdated", "replacement", "renewal", "upgrade"] }
  ],
  "competitor_terms": ["<incumbent or product>"],
  "own_vendor_names": ["<Company>", "<product or brand name if different>"],
  "funding_terms": ["SLCGP", "cyber insurance", "IT budget"],
  "states": [],
  "days_back": 90,
  "fit_filters": {
    "jurisdiction_types": ["federal agency", "state", "county", "city", "higher education"],
    "buyer_roles": ["agency CIO or CISO", "IT Director", "CISO", "City Manager"]
  },
  "notes": "Run primary terms first. If thin, widen the date window. Run competitor terms as a second pass."
}
```
```

### Rules the search plan must respect

- **Never omit a date window.** With no date, the meeting and document tools look back only
  seven days. Use a `daysBack` of 30 to 90, or `startDate` and `endDate`, which cannot be
  combined with `daysBack`.
- `states` empty means nationwide. Fill it only when a territory was named. It works on
  every search tool and accepts two-letter codes, full names, and Canadian provinces.
- Keep terms specific. "ransomware resiliency" and "security operations center" beat
  "technology" and "security". Broad terms over a wide window overflow the context limit
  and the result gets written to a file.
- Search one vendor name per query. In a batched `terms` array, one high-frequency term
  consumes the ranking and every other name reports zero for the returned page only, which
  is not a corpus count.
- Spell multi-word vendor names the way speech-to-text renders them, not the way the
  company brands itself. Spaced `Clifton Larson Allen` returns hundreds of meetings where
  `CliftonLarsonAllen` returns none. Watch for ordinary English words that are also product
  names, which return near-total noise on their own.
- Before claiming a competitor returns zero, re-run it alone, in spaced and phonetic
  variants, and across both the meeting and the document layers. A wrong zero looks exactly
  like a right one.
- Pagination is real. `perPage` goes up to 100 with `page`, and `search-insights` uses
  `limit` up to 200. The old 25-meeting cap is gone.
- `own_vendor_names` is never passed as `terms` to a search tool.
- **Higher-education-heavy vendors:** universities rarely surface in broad keyword sweeps.
  Name the target institutions and walk their meetings with `lookup-organization` and then
  `list-organization-meetings` (board of regents or trustees, IT governance) instead.

For parameter names, limits, and response shapes, see `cloverleaf-mcp-operations`.

## Output 2: Cloverleaf Account Profile fields

Produce a second block with the values that paste into the platform's Account Profile
settings page. The field list, the repeater behavior, and the boilerplate Focus Area text
are in **`references/account-profile-fields.md`**. Read it when you are ready to write this
block.

## Honesty rules

- Never fabricate a FedRAMP status, customer logo, competitor, contract vehicle, contact,
  or metric to fill the template. Mark unknowns "not found, verify".
- Separate what the vendor claims on its own site from what a third party verifies.
- Leave a thin section thin and say so. A wrong search term wastes a real sweep.
- Never print "45,000+ agencies". The Cloverleaf AI website says 70,000+ agencies monitored
  continuously. Verify any platform figure before using it.

## Hand off

Pass the search plan to `cloverleaf-signal-search`. It maps onto `terms`, `states`, and the
date window, and `own_vendor_names` feeds that skill's own-vendor guardrail. Run the primary
terms first, then the competitor terms as a displacement pass. From there the workflow
continues to `signal-dashboard`, `opportunity-enrichment`, and `signal-outreach`.
