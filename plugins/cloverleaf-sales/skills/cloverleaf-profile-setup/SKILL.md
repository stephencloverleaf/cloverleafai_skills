---
name: cloverleaf-profile-setup
description: Set up or update a user's Cloverleaf AI account profile and signal notification settings at app.cloverleaf.ai/account. Use when someone says "set up my Cloverleaf profile," "configure my profile," "update my focus areas / competitors / pain points," "I'm getting too many (or too few) signal emails," "change my score threshold," "why am I not getting good signals," or is onboarding a new Cloverleaf user or customer. Covers both the Profile tab (job title, industry, focus areas, competitors, products/services, pain points) and the Notifications tab (max results per campaign, score threshold, delivery window).
---

# Cloverleaf AI Profile Setup

The profile is what Cloverleaf uses to decide which government meeting discussions become signals for this user, and the notification settings control which of those signals actually reach their inbox. Both must be configured or the signal feed will be noisy or empty.

## Tooling

All steps happen in the browser at `https://app.cloverleaf.ai/account`. Use the **Claude in Chrome MCP** (`mcp__claude-in-chrome__*`), never host-level computer-use clicks. Load in one call:

```
ToolSearch select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__form_input
```

The user must already be logged in. If the page renders empty, wait a moment and re-read — the app hydrates after load.

## Step 1 — Gather the inputs before touching the UI

Do not guess these. Ask the user (AskUserQuestion) for anything missing:

| Field | What good looks like |
|---|---|
| Job title | e.g. "Business Development Director" |
| Industry | Specific, not generic. "public relations & issue advocacy" ✅ / "consulting" ❌ |
| Focus Areas | Instructions to the scanner, not keywords. One line describing the conversations that matter, plus a guardrail line. |
| Competitors | Named firms they lose deals to |
| Products/Services | 2–4 lines, what they actually sell |
| Pain Points | Phrased the way a government official would say it out loud |

If the user sells for a vendor you haven't profiled yet, run the `vendor-profile` skill first — it produces exactly these fields.

## Step 2 — Fill the Profile tab

Navigate to `https://app.cloverleaf.ai/account`, Profile tab.

Sections, each with a `+` to add another row and a `–` to remove one:

- **Job title** (single field)
- **Industry** (single field)
- **Focus Area** — the highest-leverage field. Example pair from a working profile:
  1. "Concise summary of conversations signaling a need for communications, public relations, crisis response, community engagement, or public-awareness campaigns. Summarize the top 3 by who spoke, what they said, and why it matters"
  2. "Make it very clear why there is a potential opportunity when you find one. Don't force find opportunities"
- **Competitor** — one per row
- **Products/Services You Offer** — one per row
- **Pain Points Your Product Solves** — written as first-person quotes, e.g. "We're getting negative press and need to fix our public image"

**Less is more.** Long, sprawling instructions degrade signal quality. Keep each field tight and specific.

**Click Save at the bottom.** The Save button is disabled until something changes and does not autosave. Every edit needs an explicit save.

## Step 3 — Configure the Notifications tab

Same page, Notifications tab:

- **Account** / **Signals** / **Missed Signals Recap** — checkboxes, leave on unless the user asks otherwise
- **Max Results Per Campaign** — default recommendation **3**. There's an "Unlimited" checkbox; avoid it unless the user explicitly wants firehose volume.
- **Score Threshold (0–10)** — default recommendation **7**. Only signals scoring at or above this send an email. Raise it if they complain about volume, lower it if the feed is dry.
- **Signals Delivery Window** — hour range + time zone. Default is 7:00–8:00 AM America/New_York.

**Click Save.** Same rule — no autosave.

## Step 4 — Verify

Re-read the page after saving and confirm the values persisted. Then report back the final profile and notification settings as a short summary so the user can sanity-check them.

## Troubleshooting

- "Too many low-quality signal emails" → raise Score Threshold, tighten Focus Areas, lower Max Results Per Campaign.
- "I'm not getting anything" → lower Score Threshold, check that Signals notifications are checked, and check the Territory tab is scoped correctly.
- "Signals are off-topic" → the Focus Areas are too broad or the Pain Points aren't phrased in officials' language. Fix those before touching the threshold.
