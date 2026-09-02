# Response shapes

Top level and per row fields as the connector actually returned them. Every shape below
was read off a live call on the date given. A field not listed here was not present in
that response, so do not write code or a template that depends on it.

Contents: search-insights, search-meetings, run-meeting-keyword-search, search-documents,
run-document-keyword-search, search-purchases, lookup-organization,
list-organization-meetings, and the parsing note for offloaded payloads.

## search-insights (2026-09-02)

Top level: `insights[]`, `total`.

Per insight: `id`, `meeting_id`, `organization_name`, `city_name`, `county_name`,
`state_name`, `prompt_name`, `creator_email`, `created_at`, `summary`, `result`,
`result_truncated`, `cloverleaf_url`.

- `cloverleaf_url` points at the meeting's insights page,
  `https://app.cloverleaf.ai/meetings/<meeting_id>/insights`.
- `summary` carries the "Signal Match: X/10" line. `result` is the full markdown and
  arrives truncated with `result_truncated: true`; pass `includeFullResult: true` for the
  whole text.
- `result` embeds relative deep links of the form
  `/meetings/<id>?start-time=<seconds>`. Those are relative paths, not citable URLs.
- There is no `state` code field, only `state_name`, and city or county can be null.

## search-meetings (2026-09-02)

Top level: `total_hits` (chunk count, caps at 100), `total_meeting_hits` (true meeting
count), `meeting_hits[]`, `meetings[]`. Join the two arrays on `id`.

Per `meeting_hits[]` row: `id`, `hits`, `time` (epoch ms), `best_score`,
`already_viewed`, `transcripts[]`.

Per `transcripts[]` entry: `id` (formatted `<meeting_id>-<chunk>`), `text`, `start_time`
(seconds, float), `score`. **No `person` block.** Semantic excerpts carry no speaker
information at all.

Per `meetings[]` row: `id`, `cloverleaf_url`, `title`, `organization_id`,
`organization_name`, `created_at`, `description`, `published_at`, `source_video_url`,
`city`, `county`, `state`, `country_code`, `important_words`, `duration_seconds`,
`word_error_rate`, `discarded_at`, `is_spam`, `needs_run`, `spam_certainty`,
`thumbnail_url`, `updated_at`, `user_marked_spam`.

- `state` is a full name ("Texas"), not a code. `city` is null on county meetings.
- `spam_certainty` came back 0.8 to 0.95 on every clean meeting in the probe, so it is
  not a quality filter.
- `description` is often the publisher's own YouTube description and sometimes carries a
  full agenda with timestamps, which is useful corroboration for a jurisdiction check.

## run-meeting-keyword-search (2026-08-18)

Top level: `total_meeting_hits` (true count), `meeting_hits[]`, `meetings[]`.

Per `meeting_hits[]` row: `id`, `hits`, `time` (epoch ms), `already_viewed`, `terms[]`
(each `{term, count, ...}`), `transcripts[]`.

Per `transcripts[]` entry: `text`, `start_time`, `person`. The `person` block is
`{name, organization, title}` only; email and phone are not returned inline. Many lines
carry `person: null`, and a populated block is not evidence (rule 9).

`meetings[]` has the same shape as in `search-meetings`.

## search-documents (2026-09-02)

Top level: `total_hits` (chunk count, caps at 100), `total_document_hits` (true document
count), `documents[]`.

Per document: `document_id`, `document_id_raw`, `cloverleaf_url`
(`https://app.cloverleaf.ai/documents/<id>`), `index` ("meeting-documents"), `hits`,
`best_score`, `chunks[]`, `organization_id`, `source` ("scraping_agent"), `document_type`
(agenda, packet, minutes, notice), `meeting_date` (ISO string).

Per `chunks[]` entry: `id` (`<document_id>-<chunk>`), `text` (long, often hundreds of
characters of raw PDF text with layout artifacts), `score`.

- No org name and no state field. Resolve `organization_id` before presenting, and scope
  geography through the `states` request parameter.

## run-document-keyword-search (2026-08-18)

Per hit: `organization_id`, `document_type`, `meeting_date` (ISO string),
`term_frequencies`, `highlights[]` (matched passages wrapped in `<mark>` tags), and
`cloverleaf_url`. `created_at` is still epoch ms. No org name.

## search-purchases (2026-09-02)

Top level: `total_hits` (capped at 100), `page`, `per_page`, `purchases[]`.

Per purchase: `id` (`<dataset>:<source_row_id>`), `score`, `purchase_dataset_id`,
`source_row_id`, `organization_ids`, `organization_names`, `amount`, `purchase_name`,
`purchase_description`, `vendor_name`, `department`, `transaction_date`, `start_date`,
`end_date`.

- **No `cloverleaf_url`.** Cite the award by `source_row_id`, `department`, `vendor_name`,
  and `transaction_date`.
- `organization_ids` and `organization_names` were identical on every row (175 ids, 155
  names, the whole federal org list). They are a dataset level association, not the
  awarding body. Read `department` as the buyer.
- `amount` is a number and can be 0 on a contract modification. `start_date` and
  `end_date` were null on every sampled row. `transaction_date` is an ISO date string.
- `purchase_description` is upper case procurement prose, for example "THE PURPOSE OF
  THIS ACTION IS TO PROCURE ACF PALO ALTO FIREWALL REPLACEMENT."
- Scores on a good query ran 0.73 to 0.79, so calibrate purchases like documents rather
  than like transcripts.

## lookup-organization (2026-09-02)

Top level: `matched` (boolean), `organizations[]`, `state` (`{name, code}`).

Per organization: `id`, `name`, `meeting_count`, `last_published_at`.

- Embedding ranked. A "Travis County, TX" probe returned County of Travis first, then 49
  other Texas orgs including cities and a college district, many with
  `meeting_count: 0` and `last_published_at: null`.
- A `last_published_at` in the future has been observed. Treat the field as a hint and
  confirm freshness with `list-organization-meetings`.
- A no match returns a structured result that distinguishes an unknown state, no
  coverage, and no name match.

## list-organization-meetings (2026-09-02)

`organizationId` is a number; a string fails validation with "expected number, received
string". Rows carry the same meeting metadata shape as the `meetings[]` array in
`search-meetings`, newest first, with no date filter.

## Parsing an offloaded payload

Large results are written to a file and the tool result gives the path plus the schema.
Probe the structure with `jq` or Python before reading it, and extract slices rather than
loading the whole file. When a payload arrives inline but nested, the real content sits
at `inner['meeting_hits']` and `inner['meetings']` after a second JSON parse of the
`text` field. Build a metadata dict keyed on meeting id from `meetings` and join it
against `meeting_hits`.
