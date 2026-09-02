# Dashboard input shapes

The build script dispatches on the top-level key of the JSON you hand it. Shapes for
`search-meetings`, `search-insights`, and `search-documents` were verified against live
connector output on 2026-09-02. The `run-document-keyword-search` reader was not re-verified on
that date, because the tool needs an array `terms` parameter the probe harness could not
send. `cloverleaf-mcp-operations` carries the canonical field lists in
`references/response-shapes.md`; read it when a field here is not enough.

## 1. search-meetings, `{"meeting_hits": [...], "meetings": [...]}`

Two parallel arrays joined on `id`.

- `meeting_hits[]`: `id`, `time` (epoch ms), `hits`, `best_score`, `already_viewed`, and
  `transcripts[]` where each chunk has `id`, `text`, `start_time`, `score`.
- `meetings[]`: `id`, `cloverleaf_url`, `title`, `organization_id`, `organization_name`,
  `city`, `county`, `state` (full name, for example "Colorado"), `published_at`,
  `source_video_url`, `duration_seconds`, `is_spam`, `spam_certainty`, `user_marked_spam`,
  `thumbnail_url`.

The reader takes the highest-scoring chunk per meeting as the quote, drops spam rows, maps
the full state name to a two-letter code, and builds the jurisdiction as
"<organization_name>, <ST>". **There is no speaker or contact block on this tool**, so cards
are speaker-blank until a person is attached from `list-contacts` or enrichment.

`total_hits` caps at 100 on the semantic tools; read it as "100 or more".
`total_meeting_hits` is the true entity count.

## 2. search-insights, `{"insights": [...], "total": N}`

Each insight carries `cloverleaf_url` (the meeting's insights page), `organization_name`,
`state_name`, `county_name`, `city_name`, `meeting_id`, `creator_email`, `created_at`,
`prompt_name`, `summary`, and `result` (markdown). A long `result` comes back truncated with
`result_truncated: true`.

The reader pulls the "Signal Match: X/10" score from the summary, rescales it to 0 to 100,
and drops rows scored 0/10, which are relevance-gate rejects from the insight's own prompt.
Those are common: all five rows returned on 2026-09-02 were 0/10.

A Signal Match score measures how loud the pain is, never whether it is yours. It is not
pre-filtered for your rules.

## 3. search-documents, `{"documents": [...]}`

Each document carries `document_id`, `cloverleaf_url` (a documents page, not a meetings
page), `index`, `hits`, `best_score`, `chunks[]` with `id`, `text`, and `score`,
`organization_id`, `source`, `document_type` (agenda, packet, minutes), and `meeting_date`
(ISO string).

There is **no organization name**, so the reader writes "Org #<id>" as the jurisdiction.
Resolve the name and set `jurisdiction` on a normalized signal for any card that matters.

Chunk text is OCR'd agenda text, so two unrelated line items often share one block. That is
why vendor and amount extraction stays conservative.

## 4. run-document-keyword-search, `{"object_api_response": {...}}`

Two envelopes have been reported for this tool and the reader accepts both: an
Elasticsearch-style `hits.hits[]` with `_source` and `highlight.plain_text[]`, or a flat
list of hit records carrying `organization_id`, `document_type`, `meeting_date`,
`term_frequencies`, `highlights[]`, and `cloverleaf_url` inline. Passages arrive with
`<mark>` tags, which the reader strips.

The reader keeps only documents where a non-boilerplate term hit, so matches on procurement
language alone are dropped. Neither envelope was re-verified on 2026-09-02, because the tool
needs an array `terms` parameter the probe harness could not send.

## 5. Normalized signals, `{"signals": [...]}` or a bare list

Every field is optional except `quote` and `jurisdiction`.

```jsonc
{
  "signal_type": "discussion",          // "discussion" (default) or "procurement"
  "jurisdiction": "City of Spokane Valley, WA",   // the ", ST" suffix drives the state filter
  "meeting_id": "18214101",
  "meeting_title": "City Council Budget Workshop",
  "date": "2026-06-09",                 // or epoch ms in "time"
  "quote": "…",
  "start_time": 18451.04,               // seconds into the meeting
  "speaker_name": "",                   // only when confirmed against minutes or a roster
  "speaker_title": "",
  "email": "",
  "phone": "",
  "terms": ["ransomware"],
  "cloverleaf_url": "https://app.cloverleaf.ai/meetings/18451",  // copied verbatim
  "fit": "one line on why this is real",
  "next_action": "one line on the move",
  "contacts": [ { "name": "", "title": "", "email": "", "phone": "" } ],
  "score": 88,                          // optional; computed when omitted

  // procurement only
  "vendor": "Bitdefender",
  "amount": "$10,803.80",
  "procurement_stage": "Renewal",       // Renewal | Award | Agreement | RFP | Budget item
  "doc_type": "agenda",
  "org_id": 500
}
```

## Mixing types on one board

Concatenate discussion and procurement signals into one `{"signals": [...]}` list. When both
types are present the dashboard shows a Discussion/Procurement filter and a Procurement
count stat. With one type, those hide themselves.

## Timestamp hint

When `start_time` is present the card shows a readable "quote ~5:07 in" hint. Offsets carried
over from a search payload have been observed wrong by 40 to 65 seconds, so re-derive the
offset from the transcript before featuring a card in front of a customer.

## Not a dashboard input: purchase records

`search-purchases` and `run-purchase-keyword-search` rows do not belong on a signal board.
They carry no `cloverleaf_url`, so a card could not cite one, and their `organization_ids`
and `organization_names` are identical on every row (the whole federal organization list),
so `department` is the only real buyer field. Use them in `opportunity-enrichment` as an
award-stage cross-check instead. Coverage beyond federal is unverified as of 2026-09-02.
