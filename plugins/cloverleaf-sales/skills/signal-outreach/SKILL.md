---
name: signal-outreach
description: >-
  Turn an enriched Cloverleaf signal into personalized, copy-paste-ready outreach —
  email, LinkedIn note, and a call/voicemail script — that quotes the actual official
  by name. Use this whenever the user wants to "write the email," "draft outreach,"
  "reach out," "turn this into a message," or "what would I send" off a signal or lead.
  Final step of the demo workflow (search → dashboard → enrich → OUTREACH). Two modes:
  vendor→government (the warm lead) and Stephen→vendor-prospect (proof-of-value). This
  is the "and it writes the outreach" mic-drop that shows the full workflow, not just search.
---

# Signal Outreach

## Why this lands

Cloverleaf's whole promise is that a rep can sound like an insider — referencing the exact
thing a named official said in a public meeting — instead of a data scraper blasting a
generic pitch. This skill produces that message. The power is in specificity: a real quote,
a real name, real timing. Never water it down into "I hope this email finds you well."

## Pick the mode

**Mode A — Vendor → government decision-maker (default).** The outreach a cyber vendor's rep
would send to the official from the signal (the warm lead). This is the demo payoff: "watch
Cloverleaf turn a council quote into the email your team sends Monday."

**Mode B — Stephen → vendor prospect (proof-of-value).** Stephen's own outreach selling
Cloverleaf, using a real signal from the prospect's SLED territory as undeniable proof. Great
as a live "and here's how I'd pitch *you* this capability" close, or as a leave-behind.

State which mode you're writing. When in doubt in a demo, do Mode A (it shows the product),
then offer Mode B as the kicker.

## Principles (both modes)

- **Open with their words, not your product.** Quote the official accurately — it's public
  record, so referencing it is fair game and credible. Get the quote right; don't paraphrase
  into something they didn't say.
- **One specific reason this is timely** — budget workshop happening now, audit follow-up,
  grant window (SLCGP), a prior incident. Timing is the reason they reply.
- **One CTA.** A 15-minute call before the budget locks. Not three asks.
- **Short.** Email body ≤ ~110 words. LinkedIn note ≤ 300 characters. Voicemail ≤ 20 seconds.
- **Plain language, peer tone.** Especially to government staff — respectful and helpful, not
  salesy. No hype words, no exclamation points.
- **Accuracy + opt-out** keep it effective and compliant: quote correctly, and honor
  unsubscribe/do-not-contact requests. That's it — no boilerplate disclaimers.

## Templates

### Mode A — Email (vendor rep → official)
```
Subject: <the specific thing they raised>

Hi <First> — I saw the <Mon DD> <meeting type> where you noted <short paraphrase or
direct quote of the pain/project>. <One sentence: why that gap matters / what usually
follows it.> We help <jurisdictions like theirs> <close that specific gap> — <one proof
point or relevant funding path, e.g. SLCGP>. Worth 15 minutes before <the budget /
RFP / next step> firms up?

<Name, title, company> · <phone>
```

### Mode A — LinkedIn connection note
```
Hi <First> — caught <Jurisdiction>'s <Mon DD> <meeting> and your point about
<the gap>. We help cities close exactly that. Would love to connect.
```

### Mode A — Voicemail / call opener (≤20 sec)
```
"Hi <First>, this is <Name> with <Company>. I was reviewing <Jurisdiction>'s
<Mon DD> budget workshop and heard your point that the resiliency audit skipped
<the gap>. That's the exact thing we help cities close, and there may be grant
dollars for it. I'll follow up by email — reach me at <phone>."
```

### Mode B — Email (Stephen → vendor BD/capture lead)
```
Subject: A <Jurisdiction> cyber budget signal in your <State> territory

Hi <First> — quick proof of concept. On <Mon DD>, <Jurisdiction>'s <official title>
said on the record that <the gap/pain> — during a budget workshop, i.e., as funding is
being set. We surface these pre-RFP, with the official's name and contact, months before
anything hits a bid portal. That's one of <N> cyber signals across your <State> territory
this quarter. Want me to show you the full set?

Stephen White · Cloverleaf AI
```

## Worked examples (real Spokane Valley signal)

**Mode A — to Chad Knodel, IT Manager, City of Spokane Valley (cknodel@spokanevalleywa.gov):**

> **Subject: The pen-testing gap from your June 9 budget workshop**
>
> Hi Chad — I caught the June 9 budget workshop where you noted last year's ransomware
> resiliency audit didn't include network penetration testing. That's exactly the gap that
> turns a "we're covered" into a breach six months later. We help WA municipalities close it
> with continuous pen testing and validation, and several have funded it through the state's
> SLCGP cybersecurity grant. Worth 15 minutes before the budget locks?
>
> — <Rep name, title, company> · <phone>

**Mode B — to a cyber vendor's SLED BD lead, using the same signal as proof:**

> **Subject: A Spokane Valley cyber budget signal you'd want**
>
> Hi <First> — quick proof of concept. On June 9, Spokane Valley's IT Manager said on the
> record that their ransomware resiliency audit skipped network pen testing — during a budget
> workshop, as funding is being set. We surface these pre-RFP, with the official's name and
> contact, months before an RFP. That's one of dozens of cyber signals across your SLED
> territory this quarter. Want me to show you the <state> set?
>
> Stephen White · Cloverleaf AI

Note how each email anchors on the **exact quote**, names a **specific timing reason**, and
ends with **one CTA**. That's the formula — keep it.

## Brand voice (Cloverleaf AI tone)

All outreach must match Cloverleaf AI's brand voice:

- **Direct and confident.** No hedging, no qualifiers like "might," "could
  potentially," "we believe." Urgency without alarm.
- **Never corporate.** No generic SaaS verbs: leverage, streamline, synergize,
  unlock, harness, enable, optimize. No hollow superlatives: innovative,
  cutting-edge, best-in-class, game-changing.
- **Short sentences are a feature.** Intentional fragments for emphasis are
  on-brand. Mix short punches with longer explanatory context.
- **Active voice throughout.** Lead with the problem, not the product.
- **Concrete specifics.** Use real numbers, names, dates. "70,000+ government
  agencies" beats "thousands of government agencies."
- **The company name is always "Cloverleaf AI"** — never "Cloverleaf" alone,
  never "CloverLeaf," never "Clover Leaf."
- **Oxford comma always. No em dashes** — use periods, colons, or line breaks.
- **Contractions encouraged** — they keep the tone human.

---

## Output

In a demo, show the drafts inline (that's the wow). For takeaways, save all variants per
signal to a `.md` file (e.g. `outreach_<jurisdiction>.md`) and present it so Stephen can
copy-paste. You can also write the chosen email's first line into the signal's `next_action`
so it shows on the dashboard card.

Pulls from the enriched signal produced by **`opportunity-enrichment`** (quote, speaker,
contacts, timing, grant). If those fields are thin, run enrichment first.
