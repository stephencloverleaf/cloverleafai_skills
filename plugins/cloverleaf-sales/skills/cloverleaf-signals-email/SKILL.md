---
name: cloverleaf-signals-email
description: Fetch and parse the daily "Cloverleaf Signals" email from notifications@cloverleaf.ai. Use this skill whenever the user asks about their Cloverleaf Signals, daily signals email, signal digests, what signals came in today, signals for a specific campaign (like "my Sophos signals" or "what did the cybersecurity campaign find"), or any reference to cloverleaf signals, signal emails, or daily summaries from Cloverleaf. Also trigger when the user asks to "check my signals", "what came in today", "show me my Cloverleaf results", or "pull up the signals email". This skill handles all alias routing automatically — the alias tag (e.g., +sophos, +cybersecurity, +ai) maps directly to the campaign the signals were run for.
---

# Cloverleaf Signals Email Skill

Fetches the daily "Cloverleaf Signals" digest email from notifications@cloverleaf.ai and presents each campaign's signals clearly. One thread arrives each day containing separate messages, each addressed to a different email alias. The alias tag identifies the campaign.

---

## Alias → Campaign Mapping

Each message in the thread has a `toRecipients` field. Parse the alias tag to identify the campaign:

| Alias pattern | Campaign name |
|---|---|
| `stephen@cloverleaf.ai` (no tag) | General / default search |
| `stephen+sophos@cloverleaf.ai` | Sophos campaign |
| `stephen+cybersecurity@cloverleaf.ai` | Cybersecurity campaign |
| `stephen+ai@cloverleaf.ai` | AI campaign |
| `stephen+urbangrid@cloverleaf.ai` | Urban Grid / UrbanGrid campaign |
| `stephen+[tag]@cloverleaf.ai` | `[tag]` = campaign name (capitalize it) |

If no `+tag` is present, label it **"General"**.

**Capitalization exceptions**: Always uppercase known acronyms — `ai` → **AI**, `soc` → **SOC**, `edr` → **EDR**. Treat other tags as title case.

---

## Step-by-Step Instructions

### Step 1 — Search Gmail

Search for the most recent Cloverleaf Signals thread:

```
Gmail query: from:notifications@cloverleaf.ai subject:"Cloverleaf Signals" newer_than:3d
```

- Use `pageSize: 5` (the daily digest is one thread containing all campaigns)
- If the user asks for a specific date or "yesterday's signals", adjust the date filter accordingly
- If the user names a specific campaign (e.g., "my Sophos signals"), still pull the full thread — filter by alias after fetching

### Step 2 — Fetch the Full Thread

Take the most recent thread ID and call `get_thread` with `messageFormat: FULL_CONTENT`.

Each message in the thread = one campaign's signals.

### Step 3 — Parse Each Message

For each message, extract:

1. **Campaign name** — from `toRecipients[0]`, parse the `+tag` before `@`. If no tag, use "General".
2. **Summary paragraph** — the 2–4 sentence top-of-email narrative (appears before "DIG INTO THE DETAILS"). This is the AI-written overview of what signals were found.
3. **Search label** — the smart search name shown after "DIG INTO THE DETAILS ↓" (e.g., "Sophos - EDR/EMAIL/SOC" or "Smart Search - Washington - IT reseller")
4. **Stats line** — extract the 📅 Meetings, ⌛ Hours Analyzed, and 🎯/🔍 Hits or Keyword Mentions counts. The stats line ends just before the first signal card meeting name appears — trim anything after the last number/word pair in the stats block (i.e., stop at the first organization name that follows the counts).
5. **Individual signal cards** — each card contains:
   - Meeting name (e.g., "City of Amherst — Cherry Hill Working Group Jun 16, 2026")
   - Location (city, state)
   - Date
   - Signal Match score (e.g., "Signal Match: 9/10") — only present in some emails
   - Signal description paragraph

The body is HTML. Use text extraction — strip tags and look for these structural markers:
- Summary ends at "DIG INTO THE DETAILS"
- Search label appears right after "DIG INTO THE DETAILS ↓"
- Stats follow the search label (look for 📅, ⌛, 🎯/🔍 emoji)
- Signal cards follow the stats line and repeat until end of message

### Step 4 — Filter if Requested

If the user asked for a specific campaign (e.g., "show me the Sophos signals"), present only that campaign's message. Otherwise show all campaigns.

### Step 5 — Present the Output

Format the output clearly for each campaign. Use this structure:

---

## 📬 Cloverleaf Signals — [Date]

### 🏷️ Campaign: [Campaign Name]
**Search:** [Search label]  
**Coverage:** 📅 [X] Meetings · ⌛ [X] Hours · 🎯/🔍 [X] Hits/Mentions

**Summary:**
> [Summary paragraph verbatim or lightly cleaned]

**Signals:**

**1. [Meeting Name]**  
📍 [Location] · 📅 [Date] · Signal Match: [X/10 if available]  
[Signal description]

**2. [Meeting Name]**  
...

---

*(repeat for each campaign)*

---

## Edge Cases

- **No signals today**: If the search returns no results from the last 3 days, say "No Cloverleaf Signals email found in the last 3 days." Then offer to search further back.
- **Multiple threads found**: Always use the most recent one (sorted by date desc).
- **Non-"Cloverleaf Signals" subject emails** (e.g., "Cloverleaf AI Search Results Meta Analysis"): These are a different email type — do not parse them as daily signals. If the user specifically asks for one, retrieve it and summarize it separately.
- **Empty body**: Some messages may have only a snippet. If `htmlBody` and `plaintextBody` are both empty, use the `snippet` field to summarize what's available.
- **Campaign user asked for not found**: Say "[Campaign] signals were not found in today's email. Available campaigns today: [list aliases]."

## Quick Reference — Gmail Query Variants

| Intent | Query |
|---|---|
| Today's signals | `from:notifications@cloverleaf.ai subject:"Cloverleaf Signals" newer_than:1d` |
| Yesterday's signals | `from:notifications@cloverleaf.ai subject:"Cloverleaf Signals" newer_than:2d` |
| Last week | `from:notifications@cloverleaf.ai subject:"Cloverleaf Signals" newer_than:7d` |
| Specific campaign today | Pull full thread, filter by alias after fetching |
