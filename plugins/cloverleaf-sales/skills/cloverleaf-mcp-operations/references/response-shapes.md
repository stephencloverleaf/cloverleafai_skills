# Response shapes

Top level and per row fields as the connector actually returned them. Every shape here
was read off a live call on 2026-11-13. A field not listed here was not present in that
response, so do not write code or a template that depends on it. Budget tool shapes are
in `budget-tools.md`.

Contents: get-signals-feed, search-insights, search-meetings,
run-meeting-keyword-search, search-documents, run-document-keyword-search,
get-document, the legislation searches, the bill tools, the purchase searches,
lookup-organization, list-organization-meetings and get-meeting,
get-meeting-transcripts, list-contacts, search-verified-speakers, search-campaigns,
territory and Salesforce lists, and the parsing note for offloaded payloads.

## get-signals-feed

Top level: `signals[]`, `page`, `per_page`, `total`, `hidden_total`, `facets`.

Per signal: `id`, `score` (integer 0 to 10), `title`, `summary`, `result`,
`content_type` ("meeting"), `meeting_id`, `meeting_document_id`, `organization_id`,
`organization_name`, `state_id`, `state_name`, `meeting_date`, `completed_at`, `seen`,
`hidden`, `product_type`, `saved_item_id`, `campaign_id`, `cloverleaf_url`.
`result_truncated: true` is added on cut rows.

- `facets` is `{organizations, states, campaigns}`, each a list of `{id, name}`.
- `cloverleaf_url` is the meeting's insights page and can carry `?campaign-id=<id>`.
- `campaign_id` and `meeting_document_id` can be null.
- No city, county, creator, or prompt fields. Those exist only on `search-insights`.

## search-insights

Top level: `insights[]`, `total`.

Per insight: `id`, `meeting_id`, `organization_name`, `city_name`, `county_name`,
`state_name`, `prompt_name`, `creator_email`, `created_at`, `summary`, `result`,
`cloverleaf_url`. `result_truncated: true` is present only on cut rows.

- `cloverleaf_url` is `https://app.cloverleaf.ai/meetings/<meeting_id>/insights`.
- `summary` carries the "Signal Match: X/10" line, sometimes written "[X]/10". There is
  no numeric score field.
- `summary` and `result` are both null on rows that have not produced a result.
- `result` embeds relative deep links of the form
  `/meetings/<id>?start-time=<seconds>`. Those are relative paths, not citable URLs.
- There is no `state` code field, only `state_name`. State, city, and county can each
  be null.

## search-meetings

Top level: `total_hits` (chunks, caps at 100), `total_meeting_hits` (meetings inside
those chunks), `meeting_hits[]`, `meetings[]`. Join the two arrays on `id`.

Per `meeting_hits[]` row: `id`, `hits`, `time` (epoch ms), `best_score`,
`already_viewed`, `speakers[]`, `transcripts[]`.

Per `transcripts[]` entry: `id` (`<meeting_id>-<chunk>`), `text` (500 character
preview), `start_time` (seconds, float), `score`, `cloverleaf_url`. **No `person`
block.**

Per `speakers[]` entry: `person_id`, `contact_id`, `first_name`, `last_name`,
`organization_name`, `title`. The array is usually empty. It describes the meeting, not
the excerpt.

Per `meetings[]` row: `id`, `cloverleaf_url`, `title`, `organization_id`,
`organization_name`, `created_at`, `description`, `published_at`, `source_video_url`,
`city`, `county`, `state`, `country_code`, `important_words`, `duration_seconds`,
`word_error_rate`, `discarded_at`, `is_spam`, `needs_run`, `spam_certainty`,
`thumbnail_url`, `updated_at`, `user_marked_spam`.

- Excerpt link: `https://app.cloverleaf.ai/meetings/<id>?nls-query=<query>&transcript_id=<chunk id>&start-time=<seconds>`.
  The meeting level link stops after `nls-query`.
- `state` is a full name ("Texas"), not a code. `city` is null on county meetings.
  `country_code` and `word_error_rate` were null on every row.
- `title` can carry stray HTML fragments. Strip markup before rendering.
- `spam_certainty` ran 0.75 to 0.95 on clean meetings, so it is not a quality filter.
- `description` is often the publisher's own video description and sometimes carries a
  full agenda with timestamps, which is useful corroboration for a jurisdiction check.

## run-meeting-keyword-search

Top level: `total_hits` (matching lines), `total_meeting_hits` (true count, caps at
1,000), `meeting_hits[]`, `meetings[]`.

Per `meeting_hits[]` row: `id`, `hits`, `time` (epoch ms), `already_viewed`, `terms[]`,
`transcripts[]`. No `best_score` and no `speakers`.

Per `terms[]` entry: `term`, `count`, `transcript_hits` (a map of transcript line id to
count). Anchor terms from `mustIncludeTerms` are listed here too.

Per `transcripts[]` entry: `id` (the transcript line id), `text` (the full line),
`start_time`, `person`, `cloverleaf_url`. `person` is null or
`{name, first_name, last_name, organization, title}`. A populated block is not evidence
(rule 9).

- Excerpt link: `https://app.cloverleaf.ai/meetings/<id>?search-terms=<term>&transcript_id=<line id>`.
- `meetings[]` has the same shape as in `search-meetings`.

## search-documents

Top level: `total_hits` (chunks, caps at 100), `total_document_hits` (documents inside
those chunks), `documents[]`.

Per document: `document_id`, `document_id_raw`, `cloverleaf_url`, `index`
("meeting-documents"), `hits`, `best_score`, `chunks[]`, `organization_id`, `source`
("scraping_agent"), `document_type` (agenda, packet, minutes, notice, or budget),
`meeting_date` (ISO string).

Per `chunks[]` entry: `id` (`<document_id>-<chunk>`), `text` (500 character preview of
raw PDF text with layout artifacts), `score`, `cloverleaf_url`.

- Document link: `https://app.cloverleaf.ai/documents/<id>?nls-query=<query>`. The
  chunk link adds `&chunk-id=<chunk id>`.
- No org name, no state field, no title, and no page number. Resolve `organization_id`
  before presenting.

## run-document-keyword-search

Top level: `total_hits` (true document count), `documents[]`.

Per document: `document_id`, `document_id_raw`, `cloverleaf_url` (carries
`?search-terms=`), `index`, `organization_id`, `meeting_date` (ISO string),
`created_at` (epoch ms), `highlights[]`, `term_frequencies`.

- `highlights[]` is a list of strings with matches wrapped in `<mark>` tags and embedded
  newlines.
- `term_frequencies` maps every search term to its count, including terms at 0.
- No org name and no `document_type`.

## get-document

`id`, `cloverleaf_url`, `organization_id`, `bill_id`, `document_type`, `document_url`,
`mime_type`, `document_type_guess`, `meeting_date`, `plain_text`, `storage_location`,
`failed`, `process_attempts`, `created_at`, `updated_at`.

- `plain_text` is the whole document, with form feed characters between pages.
- A legislation document has `organization_id: null`, a `bill_id`, `document_type`
  "bill", and a `document_url` on legiscan.com. Never cite that URL (rule 4).

## search-legislation and run-legislation-keyword-search

Semantic, top level: `total_hits` (caps at 100), `total_document_hits`, `documents[]`.
Per document: `document_id`, `document_id_raw`, `cloverleaf_url`, `index`
("legislation-documents"), `hits`, `best_score`, `chunks[]`, `legislative_body_id`,
`bill_id`, `source` ("legiscan"), `document_type` ("bill"), `meeting_date`. Chunks have
the same four fields as document chunks.

Keyword, top level: `total_hits` (true count), `documents[]`. Per document:
`document_id`, `document_id_raw`, `cloverleaf_url`, `index`, `bill_id`,
`legislative_body_id`, `ls_entity_type` ("bill_text"), `meeting_document_id`,
`document_type`, `meeting_date`, `created_at` (epoch ms), `highlights[]`,
`term_frequencies`.

- Link form: `https://app.cloverleaf.ai/legislation/<document_id>/search?nls-query=<query>`.
- `meeting_document_id` and `ls_entity_type` exist only on the keyword tool.

## Bill tools

**`get-bill`**: `bill`, `state`, `session`, `status_progress`, `pending_committee`,
`originating_body`, `type_record`, `subjects`, `sponsors[]`, `cloverleaf_url`. The
`bill` object holds `bill_id`, `bill_number`, `title`, `description`, `status_id`,
`status_date`, `state_url`, `body_id`, `bill_type_id`, `state_id`, `session_id`,
`pending_committee_id`. Each sponsor holds `sponsor_order`, a `person` with `name`,
`district`, `party`, and `role`, and a `sponsor_type`.

**`get-bill-documents`**: `documents[]`. Per row: `id`, `entity_type` (bill_text,
supplement, amendment), `title`, `description`, `document_type`, `date`, `state_url`,
`adopted`, `meeting_document_id`, `is_processed`, `supplement_category`, `body_abbr`,
`cloverleaf_url`.

**`get-bill-events`**: `calendar_events[]`. Per row: `date`, `time`, `location`,
`description`, `event_type`.

**`get-bill-status-changes`**: `history[]`. Per row: `date`, `title`, `description`,
`action`, `body_abbr`, `external_url`, `event_kind` (history, calendar, amendment,
supplement), `major`, `adopted`.

## search-purchases and run-purchase-keyword-search

Keyword, top level: `total_hits` (true count), `purchases[]`. Semantic, top level:
`total_hits`, `page`, `per_page`, `purchases[]` (empty on every probe).

Per purchase: `id` (`<dataset>:<source_row_id>`), `score`, `purchase_dataset_id`,
`source_row_id`, `organization_ids`, `organization_names`, `amount`, `purchase_name`,
`purchase_description`, `vendor_name`, `department`, `transaction_date`, `start_date`,
`end_date`.

- **No `cloverleaf_url`.** Cite the award by `source_row_id`, buyer, `vendor_name`, and
  date.
- Federal rows: `id` like `1:CONT_AWD_...`, the full federal org list in
  `organization_ids` and `organization_names` on every row, the buyer in `department`,
  null `start_date` and `end_date`, upper case `purchase_description`.
- Local rows: `id` like `521:dataset-521-<hash>`, one or two entries in
  `organization_names` (the buyer), `department` a division or null, and often a
  contract term in `start_date` and `end_date`.
- `amount` is a number, 0, or null. `transaction_date`, `purchase_description`, and
  `department` can each be null.
- Keyword `score` is a lexical relevance number (11 to 14 on a good match), not a 0 to
  1 similarity. It is null when `sortBy` is not score.

## lookup-organization

Top level: `matched` (boolean), `organizations[]`, `state` (`{name, code}`).

Per organization: `id`, `name`, `meeting_count`, `last_published_at`. There is no
similarity score, and a match list runs to 50 rows.

A miss returns `matched: false` with a `reason` and a `message`:

- `unknown_state`: the state text is not a state or province.
- `no_coverage_in_state`: the state is real and has no organizations for this account.
- `no_match`: the state has coverage and no name matched. Carries `coverage_count`.

## list-organization-meetings and get-meeting

`list-organization-meetings` top level: `data[]`, `page`, `per_page`, `total`,
`has_more`. Rows use the `meetings[]` field names from `search-meetings`, without
`needs_run` and `user_marked_spam`, newest first. List rows are sparse: description,
video URL, duration, and spam fields came back null on a county walk, while `county`
and `state` were filled.

`get-meeting` wraps one full meeting row in `{"meeting": {...}}`. Its `city`, `county`,
and `state` can be null on a meeting whose list row has them.

## get-meeting-transcripts

Top level: `transcripts[]`, `total_transcripts`, `page`, `per_page`.

Per line: `id` (`<4 hex>_<meeting_id>_<index>`), `text`, `start_time`, `person`.
`person` was null on all 200 lines of the meeting sampled. Lines carry no
`cloverleaf_url`. The index in the id is not the line's position in the page.

## list-contacts

Top level: `contacts[]` only. There is no total.

Per contact: `id`, `first_name`, `last_name`, `title`, `role`, `email_address`,
`phone_number`, `organization_id`, `organization_name`, `state_name`, `county_name`,
`county_fips_code`, `county_lat`, `county_long`, `city_name`, `city_geoid`, `city_lat`,
`city_long`.

## search-verified-speakers

Top level: `persons[]`, `total`.

Per person: `person_id`, `contact_id`, `first_name`, `last_name`, `organization_name`
(can be null), `title`.

## search-campaigns

Top level: `campaigns[]`, `total_campaigns`, `page`, `per_page`.

Per campaign: `id`, `name`, `user_id`, `user_organization_id`, `searchTerms`,
`exclude`, `filterParams`, and on some campaigns `mustIncludeTerms` and `proximity`.
`filterParams` can be an empty object.

## Territory and Salesforce lists

Both were empty on the test account, so only the envelopes are known:

- `list-territory-channels`: `{"channels": [], "total": 0, "page": 0, "per_page": 25}`.
- `list-salesforce-account-mappings`:
  `{"accounts": [], "page": 1, "total_pages": 0, "total_count": 0}`.

## Parsing an offloaded payload

Large results are written to a file and the tool result gives the path plus the schema.
Probe the structure with `jq` or Python before reading it, and extract slices rather than
loading the whole file. When a payload arrives inline but nested, the real content sits
at `inner['meeting_hits']` and `inner['meetings']` after a second JSON parse of the
`text` field. Build a metadata dict keyed on meeting id from `meetings` and join it
against `meeting_hits`. Ids that are numbers inline can arrive as strings in a file
dump, so normalize the type before joining.
