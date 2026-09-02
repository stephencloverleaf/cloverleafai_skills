---
name: signal-outreach
description: >-
  Turns an enriched Cloverleaf signal into copy-paste-ready outreach, an email plus a
  LinkedIn note plus a call and voicemail script, anchored on what a named official
  actually said in a public meeting. Runs in two modes: a vendor rep writing to the
  government decision-maker, and a Cloverleaf AI seller writing to a vendor prospect using
  a real signal from their territory as proof. Trigger phrases: "write the email", "draft
  outreach", "reach out to them", "turn this into a message", "what would I send". Final
  step of the demo workflow, after opportunity-enrichment. Carries the hard fails that stop
  a draft from shipping: no fabricated quote or personalization, no Cloverleaf app links in
  outbound, no early-signal claim without two dated meetings, and no awarded deal used as a
  lead.
---

# Signal outreach

## Load the writing standard first

If a `sales-communication` or `humanizer` skill is available in this session, load it first
and let it govern voice and structure. Otherwise apply the checklist in
**`references/outreach-checklist.md`**, which carries the hard fails and the preflight. Read
it before you write, and run it again before you ship.

## Why this lands

The promise is that a rep sounds like someone who was in the room, because they reference
the exact thing a named official said in a public meeting. The power is specificity: a real
quote, a real name, real timing. Never dilute it into "I hope this email finds you well".

## Pick the mode

**Mode A, vendor to government decision-maker.** What a vendor's rep sends to the official
from the signal. This is the warm lead the whole workflow produces.

**Mode B, Cloverleaf AI seller to vendor prospect.** Outreach selling Cloverleaf AI, using a
real signal from the prospect's own territory as proof. Say which mode you are writing.

## Before you write: four checks that kill drafts

1. **Is the speaker confirmed?** Speaker attribution in the platform is inference, not data,
   from both transcript endpoints. If the name has not been checked against minutes, a
   roster, or a signature block, do not put it behind the quote. Write the body or the role
   instead: "staff told the council", "the IT director said".
2. **Is the stage open?** "Took quotes and awarded" or "the board approved" means the lead is
   gone. Signals used in cold outreach must be open and pre-solicitation.
3. **Does the recipient own the problem?** The people speaking must own the failing system
   and hold budget for the category. Oversight hearings, public commenters, and advocacy
   witnesses fail this even when the quote is specific and recent.
4. **Is the quote read in context?** Quotes get spliced across timestamps and cut right
   before the speaker disqualifies the claim. Read a window around it.

If a check fails and you cannot fix it from the data, label the draft **NOT READY TO SEND**
and say which input is missing. Never fill the gap with an invention.

## Principles for both modes

- **Open with their words, not your product.** Quote accurately. It is public record, so
  referencing it is fair and credible.
- **One specific reason it is timely.** A budget workshop in progress, an audit follow-up, a
  grant window, a prior incident. Timing is why they reply.
- **One ask.** For a cold recipient, prefer an interest-oriented question over a calendar
  request. A meeting ask works only when the offer is concrete and the timing is real.
- **Short.** Email body 50 to 100 words, three or four short sentences. LinkedIn note under
  300 characters. Voicemail under 20 seconds.
- **Plain language, peer tone.** Especially to government staff: respectful and useful, not
  salesy. No hype words and no exclamation marks.
- **Write less technical.** The signal facts stay concrete. The commentary around them stays
  simple, and there is no interpretive paragraph telling the reader what to think.
- **Source without a link.** Never put an `app.cloverleaf.ai` link in outbound copy.
  Recipients have no account, so the link hits a login wall. Name the jurisdiction, the
  governing body, and the date in a plain source line instead. Keep the `cloverleaf_url`
  with the draft as an internal citation, clearly marked as not part of the message.
- **Never claim a decision started early without the earlier meeting.** The early-signal
  argument needs two dated meetings, the discussion and the later buy. With one, you have no
  argument, so do not make it.
- **No dashes.** No em dashes or en dashes anywhere in outbound copy. Use a period, comma,
  colon, or line break.
- **Accuracy and opt-out** are the whole compliance story here: quote correctly, and honor
  unsubscribe and do-not-contact requests. No boilerplate disclaimers.

## Templates

### Mode A, email to the official

```
Subject: <the specific thing they raised>

Hi <First>, I saw the <Mon DD> <meeting type> where <the speaker or body> noted <short
direct quote or close paraphrase of the pain or project>. <One sentence on why that gap
matters or what usually follows it.> We help <jurisdictions like theirs> <close that
specific gap>, and <one verified proof point or funding path>. <One interest-oriented
question.>

Source: <Jurisdiction> <governing body>, <Mon DD, YYYY>

<Name, title, company> · <phone>
```

### Mode A, LinkedIn connection note

```
Hi <First>, caught <Jurisdiction>'s <Mon DD> <meeting> and the point about <the gap>. We
help cities close exactly that. Would like to connect.
```

### Mode A, voicemail or call opener, under 20 seconds

```
Hi <First>, this is <Name> with <Company>. I was reviewing <Jurisdiction>'s <Mon DD>
<meeting> and heard the point that <the gap>. That is the exact thing we help cities close,
and there may be grant dollars for it. I will follow up by email. You can reach me at
<phone>.
```

### Mode B, email to a vendor prospect

Three moves and nothing else: the signal, one plain sentence on what Cloverleaf AI does, one
direct ask.

```
Subject: <Jurisdiction> <category> signal in your <State> territory

Hey <First>,

In <Jurisdiction>, <State> on <Mon DD>, <the speaker or body> <the concrete thing they said
or the numbers they laid out>.

We are helping public sector teams know about opportunities in their accounts well before
the word "RFP" is ever said.

Cloverleaf AI pulls leads like this every day. Want to see how it works using your
territory?

Best,
<Name>
```

Use "your accounts" instead of "your territory" for proposal-desk and contracts titles that
carry no territory. Every signal-led cold email or follow-up ends on that closer. Never end
on a bare "want the clip?" or "want the meeting detail?", which hides what Cloverleaf AI is
and has left a prospect thinking the sender was a reseller bringing them a deal.

## Output

Show the drafts inline. For a takeaway, save all variants per signal to a `.md` file, for
example `outreach_<jurisdiction>.md`, and present it. You can also write the chosen email's
first line into the signal's `next_action` so it shows on the dashboard card.

Lead with the drafts. Do not add a section explaining what you rejected, what you could not
verify, or standing caveats. A single source and date line at the foot is fine. If a draft
is not shippable, say so in one line at the top and name the missing input.

## Inputs

Pulls from the enriched signal produced by `opportunity-enrichment`: quote, speaker and
whether the name is confirmed, contacts, procurement stage, timing, grant, and
`cloverleaf_url` for internal citation. If those fields are thin, run enrichment first.
