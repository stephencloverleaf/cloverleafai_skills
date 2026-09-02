# Procurement vocabulary

The single biggest failure mode in document search is searching procurement boilerplate
alone. "Request for proposals" by itself returns thousands of documents, almost all
website navigation menus and the standard agenda disclaimer about competitive
solicitations, with no buying substance.

The rule: search solution and product nouns, not generic procurement words. Or skip the
vocabulary problem by opening with a `search-documents` intent sentence and reserving
lexical search for named vendors and rare phrases.

## Solution term banks

These are the productive nouns. They return line items with vendor names and dollar
amounts attached.

**Cyber and IT:** managed detection, MDR, EDR, endpoint protection, firewall replacement,
penetration testing, security operations center, SIEM, zero trust, multi-factor
authentication, email security, backup and disaster recovery, IT modernization, network
upgrade.

**Adjacent public sector systems:** body-worn cameras, license plate readers, ERP,
permitting system, computer aided dispatch, records management, fiber and broadband.

For any other category, `vendor-profile` produces the bank. Its `references/term-banks.md`
carries vocabulary per vertical, and `cloverleaf-signal-search/references/query-craft.md`
carries the transcript side equivalents.

## Procurement phrases

**Safe to pair with a solution term:** not to exceed, request for proposals, request for
qualifications, invitation to bid, sole source, cooperative purchase, interlocal.

**Avoid as search terms:** renewal, agreement, award, resolution, consent agenda. They are
too common, and because the default sort is newest first rather than relevance, one of
them floods the top page. "Renewal" matches license renewals and building permits equally.
Read these as stage signals in the highlight text instead of searching for them.

Two mitigations exist when you do need a procurement word: set `sortBy = "hits"`, and add
only the rare specific phrases from the safe list.

## Translating an intent into a query

*"Any cyber contracts about to be awarded in the next cycle?"*

```python
search-documents(
    query    = "upcoming award or renewal of cybersecurity, endpoint, or managed detection contracts",
    states   = ["TX"],
    daysBack = 90,
    perPage  = 10,
)
```

Then read the chunks for award, renewal, and not-to-exceed language, and keep the hits
carrying real dollar figures.

*"Who is the incumbent, and when does the contract come up?"*

```python
run-document-keyword-search(
    terms    = ["FortiGate"],          # one vendor or product term per query
    states   = ["TX"],
    daysBack = 365,
    sortBy   = "hits",
    perPage  = 10,
)
```

## Calibrating a term

The old `docs_count_per_search_term` aggregation is gone. Calibrate by running the term at
`perPage = 1` and reading `total_document_hits`, which is the true document count.
`total_hits` on the semantic tool counts chunks and caps at 100.

## Cooperative contract vehicles

Local governments buy through cooperatives more often than through their own
solicitations, so the vehicle name is frequently the only procurement language in the
document. Seen live in agendas: DIR (Texas), BuyBoard, TIPS, Omnia Partners, Sourcewell,
NASPO ValuePoint, E&I, and state term schedules. A cooperative purchase means no open
competition and a faster clock, so treat a named vehicle plus a solution term as a strong
hit rather than boilerplate.

## Vendor name spelling

Documents are written text, so brand orthography survives here. That is the opposite of
the transcript layer, where speech to text mangles names. A vendor returning zero in
meetings can return dozens of real document hits, which is why a zero must be re-derived
in both layers before it is spoken to a customer. The transcript side rules are in
`cloverleaf-signal-search/references/query-craft.md`.
