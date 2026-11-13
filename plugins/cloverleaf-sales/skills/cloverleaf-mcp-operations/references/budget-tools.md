# Budget tools

Six tools read line items that Cloverleaf extracted from a government's own budget book.
Everything here was observed on live calls on 2026-11-13, mostly against the City of
Austin and City of Raleigh books. A field or behavior not listed here was not observed.

Contents: call sequence, coverage, parameters that matter, response shapes, accuracy
limits, errors.

## Call sequence

Every budget tool except `list-budget-books` needs both `organizationId` and
`meetingDocumentId`, so the chain always starts the same way:

```python
lookup-organization(query = "City of Austin, TX")                  # org id 2167
list-budget-books(organizationId = 2167)                           # meeting_document_id 355426998
list-budget-departments(organizationId = 2167, meetingDocumentId = 355426998)
list-budget-categories(organizationId = 2167, meetingDocumentId = 355426998)
budget-rollup(organizationId = 2167, meetingDocumentId = 355426998,
              by = "category", amountType = "approved", top = 10)
search-budget-line-items(organizationId = 2167, meetingDocumentId = 355426998,
                         query = "cybersecurity", amountType = "approved", limit = 20)
get-budget-line-item(organizationId = 2167, lineItemId = "355426998:4b30...a55b")
```

Read `years[].amount_types` from `list-budget-books` before you choose `fiscalYear` and
`amountType`. It shows which year columns the book prints and how many lines each
amount type holds.

## Coverage

- Of 12 organizations tried across cities, counties, school districts, and a utility,
  5 had a book. Of 13 organizations with a budget typed document in `search-documents`,
  9 had a book. The two school districts tried had none.
- Every organization had zero or one book. Extraction is recent (the Austin book is
  dated 2026-11-10), so re-check an empty result later.
- `{"books": []}` means no extraction, or a wrong org id: a nonexistent id returns the
  same empty list with no error. One government often has two org records, and the
  book can sit on the sibling (Dallas City Council had one, City of Dallas did not).
- `current: true` was set on every book seen, including one whose fiscal year had
  ended and one biennial book whose labeled year had not started. Check `fiscal_year`
  and `fiscal_year_label` yourself before calling a book the budget in force.

## Parameters that matter

- `by` on `budget-rollup`: department, category, fund, or division.
- `lineType`: expenditure (default), revenue, or all.
- `amountType`: names one column. Type names are not normalized across books. Seen:
  adopted, approved, appropriated, amended, proposed, planned, recommended, requested,
  projected, actual, estimated_actual, ytd_actual, final_adopted, current, change, and
  unknown. Pass a name the book's `years` lists.
- `fiscalYear`: the label year (FY2026-27 is 2027). Defaults to the book's own year.
- `department` takes a key from `list-budget-departments` ("information technology").
  `categories` takes keys from `list-budget-categories` ("information_technology").
  `fund` takes a fund code or name.
- `includeTotals`: leave it off. It adds total and subtotal lines, which multiplied a
  grand total 14 to 16 times.
- `top` on the rollup: default 50, max 200. `grand_total` always sums every group.
- `search-budget-line-items`: `limit` max 50 (default 20), `skip` for paging, and
  `has_more` instead of a total. `query` needs at least 2 characters. `kCategories`
  (default 5) sets how many nearest categories seed the results; 0 searches printed
  labels only.
- `kind` on `list-budget-categories` is an exact match on a field whose values are
  `both` or `revenue`, so `kind = "expenditure"` returns nothing. Omit it.

## Response shapes

**`list-budget-books`**: `books[]`. Per book: `meeting_document_id`, `title` (null on
every book seen), `url` (the government's PDF), `cloverleaf_url`
(`https://app.cloverleaf.ai/documents/<meeting_document_id>`), `fiscal_year`,
`fiscal_year_label`, `budget_stage` (adopted, approved, or null), `is_biennial`,
`line_item_count`, `extracted_at`, `current`, `years[]`. Each `years[]` entry is
`{fiscal_year, amount_types: {<type>: <line count>}}`.

**`list-budget-departments`**: `book`, `departments[]`. Per row: `key`, `name`,
`line_count`. Keys are lowercase with punctuation stripped. Near duplicate keys exist
(`parks` and `parks and recreation`, `city manager` and `city managers`), and some
"departments" are programs.

**`list-budget-categories`**: `book`, `categories[]`. Per row: `key`, `label`, `kind`,
`parent_key`, `description`, `line_count`. The taxonomy is the same for every book, so
categories with no lines are listed with `line_count: 0`. Parent rows hold no lines;
their lines sit on the children.

**`budget-rollup`**: `by`, `scope`, `rows[]`, `grand_total`, `truncated`. Per row:
`key`, `label`, `total`, `line_count`. Unassigned lines come back as a row with
`key: null` labeled "(no department)", "(no fund)", or "(no category)". `scope` holds
`fiscal_year`, `amount_type`, `amount_types`, `book`, and `note` when columns are mixed.

**`search-budget-line-items`**: `query`, `scope`, `categories`, `items[]`, `has_more`.
Per item: `id` (`<meeting_document_id>:<40 hex>`), `label`, `account_code`,
`department_key`, `department`, `division`, `fund_code`, `fund`, `category_key`,
`category`, `category_printed`, `line_type`, `is_total`, `summary_of`, `pdf_page`,
`cloverleaf_url` (`.../documents/<id>?page=<pdf_page>`), `meeting_document_id`,
`fiscal_year`, `amount_type`, `amount_label`, `amount`, `score`.

**`get-budget-line-item`**: `item`, `amounts[]`, `book`, `department`, `fund`,
`category`, `siblings[]`. Each `amounts[]` cell is `{fiscal_year, amount_type, label,
amount, primary, as_of_date, column_ordinal}`, oldest first, with `primary: true` on
the book's own figure. `siblings` holds up to 20 neighbouring lines of the same
department, including revenue lines, and is empty when the line has no department.

## Accuracy limits

- **Check `scope` before quoting a total.** When `scope.amount_type` is null the lines
  came from more than one column, and `scope.note` says so. Austin's default rollup
  mixed approved, appropriated, and planned lines into one 17.9 billion dollar figure.
  Re-run with `amountType` to read one column.
- **A rollup total is not the published budget.** Raleigh's adopted rollup summed to
  2.06 billion dollars against 1.77 billion in the book's own transmittal letter.
  Present a rollup as "extracted line items sum to", never as the city's budget.
- **Totals are consistent across groupings.** The grand total matched by department,
  category, fund, and division for the same book and column, so differences between
  groupings are not the error source.
- **Amounts and labels were accurate.** Two Austin lines checked against the book text
  matched on label and on all five year columns.
- **Department and category can be wrong.** A lift station project was filed under the
  Information Technology department and category, and a power plant security line
  under planning and zoning. Read the `label`, `division`, and page before you call a
  line an IT or security budget.
- **A topic query can fall back to label words.** `query = "cybersecurity"` seeded no
  category and returned lines with "security" in the label, including dam and
  substation security. Results sort by score tier and then by amount, so the largest
  loosely related line leads. A filter only call returns lines largest first.
- **Treat `pdf_page` as approximate.** On two lines it sat 4 and 10 pages from a page
  count taken on the extracted text. Cite the line's `cloverleaf_url`, and expect to
  scroll.
- **An empty result is not proof of no budget.** A query that matches nothing says so
  in `scope.note`, and many real line labels use wording the query will miss. Try the
  category key, or browse the department.

## Errors

A wrong key returns `{"error": "budget_not_found", "organization_id": N, "message": ...}`
and the message tells you how to recover:

- Wrong book id: "No budget book matches meeting_document_id 1. Books on record: Fiscal
  Year 2027 adopted (meeting_document_id 355629581)."
- Unknown department or fund: the message lists every department key or fund in the
  book. It can run to several kilobytes.
- Unknown year: "prints no figures for fiscal year 2031; its years are 2023, 2024, ..."
- Unknown or invalid amount type: "prints no actual figures for fiscal year 2026; that
  year's amount types are appropriated, approved, change, planned, proposed, unknown."
- Unknown line item, or a real id with the wrong organization: "No line item ID in
  this organization's budget books."

Validation errors use the standard form, for example "Validation failed: top: Too big:
expected number to be <=200" and "Validation failed: limit: Too big: expected number to
be <=50".
