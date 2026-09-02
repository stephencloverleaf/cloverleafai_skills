# Query craft: term banks and anchoring

How to turn a vendor's product into the words an official actually says, and how to keep
a lexical search from returning noise. Parameter names and limits are in
`cloverleaf-mcp-operations`.

## Term banks

Build the list once and use it as `searchTerm` for `search-insights` and as `terms` for
`run-meeting-keyword-search`. For `search-meetings`, write the theme as a sentence
instead.

**Cybersecurity**

- Threat and pain: ransomware, data breach, phishing, cyber attack, malware
- Project and initiative: cybersecurity audit, security operations center, zero trust,
  penetration testing, incident response, multi-factor authentication, endpoint
  protection, IT modernization, ransomware resiliency
- Budget and funding: SLCGP, cybersecurity grant, cyber insurance, MSSP, managed
  security, IT budget
- Sector specific: water system cybersecurity, K-12 cybersecurity, critical
  infrastructure, SCADA

**Network infrastructure**

network infrastructure, network modernization, fiber, broadband, SD-WAN, network
upgrade, managed services, software defined networking, bandwidth

For any other category, `vendor-profile` produces the term bank; its
`references/term-banks.md` carries the vocabulary per vertical. Build the bank before the
sweep, not during it.

## Semantic queries

Write a full sentence describing the buyer's situation the way an official would live it,
not the way a vendor would market to it.

- Weak: "network security solutions for municipalities"
- Strong: "city or county asking for money to replace old firewalls or aging network
  equipment"

A 2026-09-02 probe of that strong query returned 78 meetings, led by a town board
itemising a $27,000 firewall and switch replacement into next year's budget, a school
board approving $63,064.63 for end of life switch and firewall replacement, and a county
IT director bringing an emergency router replacement after the manufacturer stopped
selling the model. None of those meetings would surface on the marketing phrasing.

## Anchoring a lexical search

`mustIncludeTerms` plus `proximity` require a search term to appear near an anchor term.

```python
run-meeting-keyword-search(
    terms            = ["cybersecurity", "budget", "contract"],
    mustIncludeTerms = ["cybersecurity"],
    proximity        = 50,
    states           = ["TX"],
    daysBack         = 90,
)
```

Anchoring is lexical co-occurrence, not semantic, so an ambiguous anchor produces
confident false positives. Anchor only with words that mean one thing: a vendor name,
ransomware, SCADA. For fuzzy intent, switch to `search-meetings`.

## Ambiguity traps

**Lexical false positives.** Firewall matches fire rated courthouse walls and a "firewall
town center" development. Pair the term with an unambiguous companion or use a compound
phrase.

**Acronym collisions inside a jurisdiction.** ERP in Cook County is the Early Resolution
Program, an eviction court legal aid program, and eleven hits in one meeting made it the
highest frequency ERP result in the state, above every genuine ERP system discussion.
Term frequency rewards this class, and the surrounding text reads as serious government
business rather than obvious noise. Confirmed members: ERP (Early Resolution Program), TCS
(911 telecommunicators), SAP in documents (Substance Abuse Professional, State Aid
Project, Service and Assessment Plan). Before trusting an acronym search, run it once
unfiltered and read the top hit by frequency. If it has a local program meaning, anchor
it with a discriminating term.

**Trap terms.** Ordinary English words that are also product names return essentially all
noise: TeamMate, Galvanize. Reach the product through the parent company instead, which
is how a $687,010.80 TeamMate line item surfaced under Wolters Kluwer. Pairing a trap term
with discriminators is a valid negative test: Galvanize plus internal audit terms
returning 0 is a genuine absence.

## Vendor names and the rules behind a zero

A "vendor X returns zero" claim shapes a customer's whole competitive picture, and a
wrong zero looks exactly like a right one. Three rules make a count trustworthy.

1. **One vendor term per query.** In a batched `terms` array one high frequency term
   consumes the ranking and every other vendor reports `count: 0` for the returned page
   only, which is a per page count and not a corpus count. Batching six audit vendors let
   "teammate" swamp the ranking, so Workiva reported 0 while it actually has 45 meetings
   and CaseWare 25.
2. **Spell names as ASR renders them.** The corpus is speech to text, so brand
   orthography does not survive. `CliftonLarsonAllen` returns 0; `Clifton Larson Allen`
   returns 572. Confirmed manglings: KnowBe4 as "no before", Spillman as "Spellman", Eide
   Bailly as "Id Bailey", Purvis Gray as "Purvis Grain", Carahsoft as "Karasoff".
3. **Re-derive a zero in both layers.** Meetings and documents disagree, because the
   brand and ASR forms differ. `AuditBoard` returns 0 meetings, since speech renders it
   "audit board", yet 37 real document hits including a live agenda item and a state code
   recommendation.

Prefer reporting what a competitor is doing over reporting that you found nothing.
