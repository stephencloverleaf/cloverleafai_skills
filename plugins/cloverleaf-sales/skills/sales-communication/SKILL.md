---
name: sales-communication
description: The house standard for any external-facing sales communication — cold email, follow-up, nurture, sequence and cadence copy, subject lines, LinkedIn connection requests, DMs and InMail, call and voicemail scripts, executive one-pagers, proposals, business cases, ROI models, and executive decks. Use BEFORE drafting or editing anything a prospect, customer, or partner will read, and before running signal-outreach, cloverleaf-copy-editor, product-marketing-framing, or any routine that writes buyer-facing copy. Also use when reviewing, scoring, or rewriting existing outreach or sales collateral. Routes to the AI Sales Communication Playbook and enforces its gates.
---

# Sales communication standard

The playbook ships with this skill at `references/playbook/`. That copy is canonical for the
plugin: read it, not a local copy elsewhere on the machine. This skill is the router and the
gate. **It is not a substitute for reading the relevant guide.**

## Step 0 — do not start by writing

Before a single line of copy, answer four things. If you cannot, ask or stop.

1. **Audience and decision stage** — cold, active discovery, technical evaluation, business
   approval, procurement, renewal. These are different messages, not tone variants.
2. **The one job of this asset** — start a conversation, earn a reply, confirm commitments,
   resolve a risk, build consensus, secure a decision. One asset, one primary job.
3. **The evidence you actually hold** — verified names, roles, dates, quotes, priorities,
   decision criteria, proof, economics, next step. Anything you cannot verify does not go in.
4. **Which guide governs** — see the routing table. Read it before drafting.

## Route to the guide, then read it

| What you are producing | Read |
|---|---|
| Cold email, no-response follow-up, post-meeting recap, evaluation or executive update, proposal-delivery / pricing / stalled-deal email, subject lines, sequence + cadence design | `references/playbook/01-email-outreach.md` |
| Connection request, first message after acceptance, cold InMail, LinkedIn follow-up, executive LinkedIn outreach, multichannel coordination with email | `references/playbook/02-linkedin-outreach.md` |
| Executive one-pager, proposal, business case / ROI / TCO / NPV, executive PowerPoint or read-ahead deck | `references/playbook/03-executive-sales-materials.md` |
| Anything above, plus the shared standard, evidence labels, and the global hard fails | `references/playbook/README.md` |

Read the whole governing guide, not the section you think you need — the failure modes and the
rubric sit apart from the structure advice. For a mixed deliverable (an email that carries a
one-pager), read both and let the primary job pick the lead format.

## Gates that apply every time

Do not send, publish, or hand over an asset that contains any of these. This list is a copy of the
global hard fails in `references/playbook/README.md`; **if they ever diverge, the README wins.**

- A fabricated or weakly inferred fact presented as known
- Reused example names, dates, organizations, or metrics from a guide, treated as real evidence
- A quote without verified wording, speaker, source, date, and context
- A metric without a definition, time period, source, or relevant denominator
- A customer name, logo, or result without permission or an approved public source
- ROI that excludes material costs or hides assumptions
- A proposal that ignores stated evaluation criteria or submission instructions
- A message that violates an opt-out request, applicable law, or platform policy
- A CTA that asks for several unrelated actions
- Copy that could be sent unchanged to almost anyone in the target role

If a required input is missing, write the placeholder and label the draft **NOT READY TO SEND**.
Never close the gap with a plausible invention. A placeholder draft cannot pass the ship gate.

## Ship gate

Run the `humanizer` verification pass on the final draft first: an em dash, a "not just X"
construction, a ritual opener or closer, or uniform robotic rhythm that survives it is a
preflight failure, not a style preference. Then score the draft against the rubric in the
governing guide and run that guide's final preflight.

- **90+** and every factual detail verified → ship
- **80–89** → focused revision
- **below 80** → rebuild from the recipient's context, not from the draft
- **any mandatory / hard / critical gate failure** → do not send, whatever the score

These thresholds are house quality control, not predicted conversion. Calibrate against Stephen's
own qualified-outcome data as it accumulates.

**Escalate to a human owner** before sending anything containing pricing, ROI or economic claims,
legal or contractual language, competitive claims, security or compliance claims, a public-facing
quote, a procurement commitment, or an executive recommendation.

## Composing with the Cloverleaf skills

The playbook sets the floor. The Cloverleaf skills supply the account motion, the voice, and the
brand. Order matters:

1. **This skill** — stage, job, evidence, governing guide.
2. **The producing skill** — `signal-outreach` for signal-led messages, `vendor-profile` /
   `opportunity-enrichment` for the research behind them, `product-marketing-framing` for
   positioning and objection handling, `signal-dashboard` / brand skills for designed assets.
3. **`cloverleaf-copy-editor`** last, on the finished draft.
4. **`humanizer`** on any prose deliverable, before the ship gate.

Where a producing skill and the playbook conflict on structure, the playbook governs the standard
and the Cloverleaf skill governs the specifics — quote handling, signal framing, brand, and voice.
Neither one overrides the hard fails.

Cloverleaf-specific application rules — B2G framing, pain → impact → solution order, signal-led
openers, the exact "Cloverleaf AI" wordmark, stale-number discipline — live in the playbook
`references/playbook/README.md` under "Cloverleaf AI application layer" and in each guide's "Cloverleaf AI application
standard." Read those rather than reconstructing them here.

For Stephen's personal voice on his own outreach, consult
`references/Cloverleaf_Email_Voice_Guide.md` (shipped with this skill). It documents the
one sanctioned exception to house copy punctuation. Do not assume the exception; it applies only
when his personal voice is explicitly wanted. Do not lead with Fortinet in every message.

## When this does not apply

The playbook governs communication a buyer will read. It does not govern internal-only work, and
loading it there is noise: territory sweeps and signal searches, the `_wiki` compile layer, PSO
vault profiles, CRM field writes, call sheets and grids built for internal use, run logs, and
`_FLAGS.md` entries. The moment any of that output turns into a message or a deliverable someone
outside the company will read, this skill applies again.

## Maintenance

The playbook is reviewed at least twice a year, and sooner when LinkedIn changes its messaging
rules, mailbox providers change sender requirements, new internal win/reply data lands, or
Cloverleaf AI changes positioning, proof points, or product capabilities. Enforcement wiring — the
files that point sessions and routines here — is listed in `references/playbook/README.md` under
"How this is enforced."
