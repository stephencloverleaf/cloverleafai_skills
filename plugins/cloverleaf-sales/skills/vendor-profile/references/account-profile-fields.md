# Cloverleaf Account Profile fields

The platform's Account Profile settings page is a form, not a report. It has six fields:
Job title, Industry, Focus Area, Competitor, Products/Services You Offer, and Pain Points
Your Product Solves. Focus Area, Competitor, Products/Services, and Pain Points are
repeaters: a plus button adds another box.

So this block gives one short, literal value per line, numbered, ready to paste into
consecutive boxes. No paragraphs, except in Focus Area, where the field expects a
directive.

Produce it as a second block after the main profile document.

```markdown
## Cloverleaf Account Profile: copy and paste fields

**Job title:**
<role> - <Vendor>

**Industry:**
<two to five words, lowercase, terse. Mirror the platform's own style, for example
"cybersecurity", not a sentence.>

**Focus Area** (one box each)
1. Identify the top 3 opportunities for <category>. Score them 1 through 10 for how relevant they are.
2. In the 3 opportunities, summarize who spoke, their role, the main quote that proves there is an opportunity with a timestamp, what the suggested next step is, and how far along in the opportunity it is (awareness, initial research, seeking funding, going to RFP, vendor chosen).

**Competitor** (one box each)
1. <competitor 1>
2. <competitor 2>
3. <competitor 3>

**Products/Services You Offer** (one box each, five to eight items)
1. <product or service>
2. <product or service>

**Pain Points Your Product Solves** (one box each)
1. <pain point>
2. <pain point>
```

## Rules for this block

- **Focus Area 2 is boilerplate.** Reuse it verbatim for every vendor. Only Focus Area 1
  changes, and only the category name inside it. Add a third Focus Area only when the user
  asks for an extra cut, such as federal versus SLED or a named territory.
- **Industry is a label, not a sentence.** A couple of words, lowercase.
- **Job title is a placeholder persona**, not a researched fact. Flag it so the user knows
  to swap in their own title when they are the one logging in.
- **Competitor values must match** the "Competitors and incumbents to hunt" list in the main
  profile. Reuse that list rather than deriving a second one.
- **Products/Services are concrete noun phrases.** "firewalls", "wireless access points",
  not "we sell firewalls to protect networks".
- **Pain Points use the official's language**, the same translation the search plan uses,
  not the vendor's outcome marketing.
- **Same honesty rule as the rest of the profile.** No invented line items to fill boxes.
  A short list beats a padded one.
