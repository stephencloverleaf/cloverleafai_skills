# AI sales communication playbook

**Purpose:** Give people and AI a shared standard for producing sales communication that is relevant, credible, easy to act on, and worthy of an executive's attention.

**Research updated:** August 11, 2026

**Scope:** B2B and B2G prospecting, evaluation-stage communication, and decision-support materials. These guides are not a substitute for legal review, current platform rules, or account-specific research.

## The guides

1. [Email outreach](01-email-outreach.md): Cold email, no-response follow-up, post-meeting follow-up, evaluation communication, and executive updates.
2. [LinkedIn outreach](02-linkedin-outreach.md): Connection requests, direct messages, InMail, follow-up, executive outreach, and multichannel coordination.
3. [Executive sales materials](03-executive-sales-materials.md): Executive one-pagers, proposals, business cases, and PowerPoint presentations.

Each guide contains:

- A definition of excellence
- Stage-specific decision rules
- Structures and examples
- Failure modes
- A weighted quality rubric
- A final review checklist
- An annotated source list with evidence limitations

## How AI should use this playbook

Do not begin by writing. Begin by checking whether the inputs support a truthful, relevant message.

1. **Identify the audience and decision stage.** Cold prospecting, active discovery, technical evaluation, business approval, procurement, and renewal require different messages.
2. **Name the job of the asset.** Start a conversation, earn a reply, confirm commitments, resolve a risk, create consensus, or secure a decision. One asset should have one primary job.
3. **Collect the minimum evidence.** Use verified names, roles, dates, quotes, business priorities, decision criteria, proof, economics, and next steps. Never invent a personalization detail, quote, customer result, stakeholder, price, or deadline.
4. **Choose the relevant guide and format.** Do not force an email structure into LinkedIn or turn a live presentation into a text-heavy leave-behind.
5. **Draft from the buyer's world.** Lead with their priority, problem, consequence, or decision. Earn the right to introduce the seller and solution.
6. **Make the next action proportionate to the relationship.** A cold prospect has not earned a calendar request by default. An active buyer often benefits from a specific time, owner, and date.
7. **Score the draft.** Use the rubric in the relevant guide. Revise until it clears the publication threshold and contains no hard-fail condition.
8. **Run the truth and trust check.** Verify every factual claim and link. Confirm compliance, opt-out requirements, platform rules, accessibility, and brand rules.
9. **Ask for human review when risk is material.** Pricing, ROI, legal language, competitive claims, security claims, public quotes, procurement commitments, and executive recommendations require an accountable owner.

## Shared standard of excellence

World-class sales communication does seven things:

1. **It is specific.** A real priority, signal, quote, decision, number, or constraint replaces generic personalization.
2. **It creates relevance, not just familiarity.** Mentioning a college, hobby, or recent post proves research. Connecting a current business event to a meaningful consequence proves relevance.
3. **It makes the buyer's job easier.** The message reduces uncertainty, organizes a decision, offers useful evidence, or makes the next step simple.
4. **It is credible.** Claims have proof. Assumptions are labeled. Sources and dates are visible. Risks are addressed instead of hidden.
5. **It respects attention.** The main point appears first. The reader can understand the message by scanning headlines, opening sentences, and callouts.
6. **It fits the stage and channel.** Brevity, tone, evidence, and CTA change as the relationship develops.
7. **It preserves trust.** No fabricated research, fake familiarity, deceptive subject lines, surveillance language, hidden trade-offs, or pressure disguised as urgency.

## Evidence labels used in the guides

The source notes distinguish among three kinds of support:

- **Official or primary guidance:** Law, platform policy, standards, or a documented methodology. Strong for requirements and frameworks.
- **Original observational research:** Analysis of messages, buyers, or deals. Useful for directional patterns, but correlation does not prove causation and the sample may not represent Cloverleaf AI's market.
- **Practitioner standard:** A repeatable convention from experienced proposal, presentation, or sales practitioners. Useful as a default, not a universal law.

Exact word counts, send times, slide counts, and cadence lengths are defaults to test. They are not laws of persuasion.

The weighted rubrics and 80/90 thresholds are internal quality-control heuristics, not research findings or predicted conversion rates. Calibrate them with Cloverleaf AI's own qualified-outcome data.

## Cloverleaf AI application layer

Use the research guides together with the project's existing brand and voice references:

- [Stephen White email voice](../Cloverleaf_Email_Voice_Guide.md)
- [Product marketing framing](../Brand%20Guidelines/product-marketing-framing.md)
- [Cloverleaf AI copy editing](../Brand%20Guidelines/cloverleaf-copy-editor.md)
- [Logo usage](../Brand%20Guidelines/logo-usage-guidelines.md)
- [Typography](../Brand%20Guidelines/typography-brand-guidelines.md)

When the communication is for Cloverleaf AI:

- Anchor the story in the buyer's B2G reality. Government deals are won long before the RFP.
- Prefer intelligence-led, territory-aware, relationship-driven language over generic sales-tech claims.
- Use pain, impact, and solution in that order.
- Open signal-led outreach with the verified official, statement, meeting, document, budget item, and date when available.
- Use **Cloverleaf AI** exactly. Never shorten or restyle the company name.
- Remove generic SaaS language and unsupported superlatives.
- Verify all company, product, coverage, customer, and performance figures at the time of use. Omit a stale number.
- Use the current brand-copy punctuation rules by default. If Stephen's personal email voice is explicitly requested, consult his email voice guide for the documented personal-style exception.
- For designed assets, use only the official black or white logo. Never recolor it or invent a substitute mark. Use the canonical brand palette in the current project skills.

## Global hard fails

Do not send or publish an asset that contains any of the following:

- A fabricated or weakly inferred fact presented as known
- Reusing a guide's fictional example names, dates, organizations, or metrics as evidence
- A quote without verified wording, speaker, source, date, and context
- A metric without a definition, time period, source, or relevant denominator
- A customer name, logo, or result without permission or an approved public source
- ROI that excludes material costs or hides assumptions
- A proposal that ignores stated evaluation criteria or submission instructions
- A message that violates opt-out requests, applicable law, or platform policy
- A CTA that asks for several unrelated actions
- Copy that could be sent unchanged to almost anyone in the target role

## How this is enforced

The playbook is not advisory. A skill carries it and a set of pointer files route every session and
routine into that skill. Nothing below restates the guides — each file points here.

| File | Role |
|---|---|
| `~/.claude/skills/sales-communication/SKILL.md` | **The enforcement point.** Loads from every folder. Routes to the right guide, carries the global hard fails and the ship gate, and sets the order in which the Cloverleaf skills compose with this standard. |
| `~/Documents/CLAUDE.md` | Standing rule for every session under `Documents/` — invoke the skill before drafting anything a buyer reads. Also states what is deliberately out of scope. |
| `~/Documents/Sales Resources/AGENTS.md` | Collateral production routes through the skill; guide 03 governs every document type in that folder. |
| `~/Documents/Customers/CLAUDE.md` | Step 4 of the pre-deliverable sequence. The wiki says what is true about the account; the playbook governs how it gets said. |
| `~/Documents/Claude/ROUTINES.md` | Registry rule 5 — binds existing and future routines. A new routine that writes buyer-facing copy without it is not ready to be listed. |
| `~/Documents/Claude/Scheduled/linkedin-customer-messages/SKILL.md` | Loads the skill before drafting; guide 02 governs. A lead whose data won't support an honest, specific message gets skipped and flagged, never softened into a generic one. |
| `~/Documents/Claude/Scheduled/daily-meeting-co-branded-signal-document/SKILL.md` | Named in the task's delegate-don't-duplicate block; guide 03 governs the brief. |
| `~/Documents/Claude/.claude/commands/pilot-spec.md` | The Proof Engine pilot factory. Loads the skill before stamping any prospect-facing paper (charter, manager packet, brief, readout, skeptic FAQ); guide 03 governs the packet and readout; the humanizer verification pass runs on every stamped file. Wired 2026-08-31. |

Those two scheduled specs are hard-linked into every past run directory — **edit them in place
(truncate-and-rewrite) or the links break and the spec silently forks.** See the note at the top of
`ROUTINES.md`.

Deliberately not wired, because their output is internal and loading the playbook there is noise:
territory sweeps (`duane-daily-territory-sweep`, `ibm-top20-ci-sweep`, `/fl-daily`, `/sophos-weekly`),
the `Customers/_wiki` compile layer, the Public Sector Orgs vault, CRM writes (`/disco`), and
internal call sheets (`/call-list`, `/grid`). Each of those specs already declares itself a working
brief rather than a customer-facing one. If any of them starts producing something a buyer reads,
wire it and add the row above.

The `anthropic-skills` plugin skills — `signal-outreach`, `cloverleaf-copy-editor`,
`product-marketing-framing`, and the brand skills — are **not** edited. They live in a versioned
plugin cache that a plugin update replaces. The `sales-communication` skill names them and sets the
composition order instead, so the wiring survives updates.

## Maintenance

Review this playbook at least twice a year, or sooner when:

- LinkedIn changes invitation, messaging, or automation rules
- Major mailbox providers change sender requirements
- New internal win/loss or reply data becomes available
- Cloverleaf AI changes positioning, proof points, brand guidance, or product capabilities

Internal performance data should eventually outrank broad market benchmarks. Segment results by persona, account type, signal type, stage, and channel. Optimize for positive conversations, qualified next steps, deal progression, and win quality, not vanity metrics.
