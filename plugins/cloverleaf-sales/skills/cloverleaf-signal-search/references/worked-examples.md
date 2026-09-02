# Worked examples: one clean pass, four rejects

Each case is real and each reject is traced to the guardrail that should have caught it.
Read this when a borderline signal is hard to call.

## Clean pass: City of Snoqualmie, WA

A keyword sweep (security operations center, cybersecurity, incident response, scoped to
WA) surfaced a Finance and Administration Committee meeting where the IT Director told
the committee their five year old cybersecurity solution was expiring, it lacked a
security operations center, and they had evaluated six replacements.

`lookup-organization("City of Snoqualmie, WA")` resolved the org, and
`list-contacts(organizationId)` returned the full roster: IT Director, Finance Director,
City Administrator, and the council member chairing Finance, each with a direct email and
phone. Two tool calls after the signal, with no enrichment vendor and no guessing.

Why it passes:

- **Guardrail 0.** Six replacements evaluated, none named, and no mention of the vendor
  being prospected for.
- **Guardrail 1.** Expiring contract with no decision made. Early stage.
- **Guardrail 2.** Named speaker with a title, a specific failing capability, and a
  concrete timeline.
- **Guardrail 3.** The IT Director owns the system and sits in the budget conversation.
  The first email has an obvious recipient.

Note the division of labor: the transcript identified who spoke, and the roster supplied
the contact details. That split is mandatory now, because transcript results carry no
contact block.

## Reject 1: vendor already engaged (Guardrail 0)

A Samsara profile run surfaced a Clarksville, TN budget committee meeting where staff
said they had "gotten some additional quotes, one specifically with Samsara" and "we have
actually done some demos with them."

Quotes in hand and demos run is an open sales cycle, not pre-RFP pain. It scored highest
of the batch and led the board. The name match alone was disqualifying, before any
scoring ran.

## Reject 2: footprint mentions (Guardrail 0, then 1 and 2)

A 27 contact sequence was built by searching each prospect's own company name and taking
the top hit. Every result was a footprint mention: the vendor's name in a payment
register, an approved vendor list, a contract amendment log, or a signed agreement. The
whole batch was rejected.

It fails all three of the first guardrails at once. The name is the vendor's own (0), a
payment register is the far end of procurement (1), and most rows were accounts payable
line items with no speaker and no unsolved problem (2). The observed lows were a $135.72
child support services line and a $250 purchasing card line.

Three sub-failures worth naming, all from that one batch:

- **The recipient appeared in their own signal.** One contact was assigned an agenda that
  lists him by name; another got a quote from his own colleague.
- **Entity name collision.** A tax penalty waiver for an unrelated firm sharing a security
  vendor's name is not that vendor.
- **Non-government source.** A think tank is not a buyer, and a filler word fragment from
  one carries no meaning.

Also check the merge value itself. One record carried an acquired entity's old name and
would have opened the email wrong.

## Reject 3: wrong buyer (Guardrail 3)

A Trellix sweep led with a city council oversight hearing where the finance department
had published 959,710 names and addresses on a downloadable spreadsheet. Named council
members, verbatim quotes, one day old, squarely in the data loss prevention category.

Rejected on sight. The members were absorbing political backlash, not scoping a security
purchase. An oversight committee is not the agency's security buyer and holds no security
budget. It cleared Guardrails 0, 1, and 2, which is exactly why Guardrail 3 exists.

## Reject 4: the pain belongs to another organization (Guardrail 3)

The highest scoring signal in one feed, a 9/10 filed under a county, was a breach at a
separate multi-county library consortium the commissioner sits on as an outside board
liaison. The transcript is third person throughout, it runs six lines inside a round robin
liaison report, and the county's own network is never discussed. The insight's stated pain
point appears nowhere in 1,175 lines.

Check whether the entity in the insight is the entity that owns the meeting, especially
inside liaison and committee report segments.

## The pattern behind the scores

In the same feed, the two highest scored signals were another organization's breach and a
small city deciding not to buy hardware, while the strongest genuine opportunity, a county
with two email breaches, roughly $20,000 of deductibles already spent, and cybersecurity
named as a levy driver, scored 7/10 and never reached the summary email. Rank by the
guardrails, then by the three scoring factors. Never by the platform score alone.
