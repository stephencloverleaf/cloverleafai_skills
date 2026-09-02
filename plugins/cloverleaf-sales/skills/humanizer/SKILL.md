---
name: humanizer
description: |
  Write and edit prose that reads like a skilled human wrote it, free of AI
  tells. Use for EVERY prose deliverable, both when DRAFTING new text and when
  editing existing text: emails, cold outreach, LinkedIn posts, blog posts,
  essays, reports, one-pagers, landing pages, scripts, and documentation.
  Always use when the user says "humanize", "make it sound natural", "this
  sounds like AI", "remove AI patterns", "de-slop", or complains that writing
  feels generic or robotic. Also use when the user asks whether a piece reads
  as AI, or wants a draft audited, scanned, or flagged for AI patterns without
  rewriting (detect mode). Fixes structural tells (hedging, symmetry, uniform
  rhythm, inflated significance, ritual openers and closers), not just banned
  words, and includes the full Wikipedia signs-of-AI-writing catalog. Do not
  apply to code, config, data files, or verbatim quotes.
license: MIT
metadata:
  version: "3.1.0"
  lineage: "fork of blader/humanizer 2.9.1; detect mode and §42-43 adapted from petergyang/no-ai-slop"
---

# Humanizer

AI-flavored writing is detectable through repeated mechanisms, not vocabulary. A text that avoids "delve" and "tapestry" but keeps hedged claims, symmetric triads, uniform 20-word sentences, and a recap closer still reads as machine output. So this skill works at the mechanism level. The word and phrase lists in `references/patterns.md` are detectors; the fix is always restructuring the sentence, never swapping a synonym.

Three modes. Mode A governs how to write in the first place. Mode B governs rewriting text that already exists. Mode C reports AI patterns in a text without changing it.

## Mode A: Drafting new prose

Use this mode whenever producing a prose deliverable, even if nobody said "humanize."

1. **Fix the register first.** Who reads this, where, and what is the one thing it must do? Read the matching section of `references/registers.md` before writing anything customer-facing. Register decides which rules bend (fragments are voice in marketing copy, a tell in essays).
2. **Draft with the six mechanisms below active.** Do not draft slop and plan to clean it later; a sentence built wrong stays wrong-shaped after cleanup.
3. **Never invent facts.** No name, number, date, quote, or citation that didn't come from the user, the source material, or verified research. If a sentence needs a specific to work and none exists, use a bracketed placeholder like `[specific detail from the meeting]` and say so, or write the plain version without it.
4. **Run the verification pass** before delivering. Rewrite flagged sentences from scratch rather than patching them.

## Mode B: Editing existing text ("humanize this")

1. **Read the full catalog** in `references/patterns.md` and scan the input against it.
2. **Preserve the information, not the shape.** Every claim in the original survives, but depth need not be uniform: compress the dull parts, dwell where a human would, merge or split paragraphs freely.
3. **Never invent facts** (same rule as Mode A). Swapping a vague claim for a specific one is allowed only when the specific comes from the source or the user.
4. **Match the voice.** If the user provides a sample of their own writing, analyze it first: sentence lengths, vocabulary, punctuation habits, recurring phrases. Match those habits instead of merely deleting AI patterns. A sample outranks this skill's style rules, including the em dash rule; if the sample uses em dashes, keep them at roughly the sample's frequency.
5. **Cut in proportion to the actual slop.** When the input is a human's draft rather than machine output, the minimum effective edit wins over restructuring: fix the tells, errors, and tangles, and leave strong human sentences alone. A rough draft with a real voice should still sound like the same person afterward; don't make every paragraph equally tidy or rewrite a distinctive line for consistency.
6. **Rewrite at the sentence level.** A flagged phrase marks a broken sentence. Replacing the phrase keeps the break.
7. **Run the verification pass**, then deliver the final rewrite plus a short note on the main changes. Skip draft-plus-audit ceremony unless the user asks to see the work.
8. When editing a file, humanize the prose only: leave code blocks, frontmatter, data, and link targets untouched.

## Mode C: Detect ("is this AI?")

Use when the user asks whether a piece reads as AI-written, or wants an audit, scan, or flag pass without changes.

1. Read the full catalog in `references/patterns.md` and scan the input against it.
2. For each pattern found: name it with its § number, quote the offending line, and give the fix in a few words. Group repeat offenders under one heading with a count.
3. Do not rewrite the draft, assign a score, or state whether AI wrote it. AI detectors guess; named patterns are evidence the user can check themselves. Apply the "What NOT to flag" list: a single tell proves nothing, clusters are the signal.
4. If little or nothing turns up, say so plainly. Don't pad the report to look thorough.
5. Close by offering to edit (Mode B).

## The six mechanisms

### 1. Commit

Hedging stacks ("could potentially", "might arguably suggest") signal that nobody is home. One qualifier per claim, and only when the uncertainty is real information the reader needs. The paragraph-level version is worse: laying out both sides and closing with "ultimately it depends on your specific needs" is a refusal to do the job. Pick the side the evidence supports, or state the decision rule ("choose X if you need [condition]; otherwise Y"). Attribute opinions to named sources or own them; "experts argue" and "studies show" are laundering. Catalog: §5, §24, §34.

### 2. Let facts carry weight

Delete editorial inflation: pivotal, crucial, testament to, underscores, marks a significant shift, plays a vital role. If the fact matters, the reader can tell from the fact. Same for promotional adjectives (vibrant, stunning, renowned) and notability padding. Test each importance-claim with "so what?" — if the sentence can't answer concretely, cut the claim and keep the fact. Catalog: §1, §2, §4.

### 3. Break symmetry

The strongest structural tells are symmetric: "not just X, but Y" in any wording, rule-of-three lists, "No X. No Y. Just Z.", false ranges ("from X to Y"), and runs of staccato fragments engineered to sound quotable. Human writing is lopsided: it spends four sentences on one point and a clause on the next. Use three items only when exactly three things exist. One specific beats three generics. Catalog: §9, §10, §12, §31, §32.

### 4. Name the thing

Replace category nouns (landscape, ecosystem, journey, space, solution) with the actual noun. Replace "-ing" analysis trailers ("..., highlighting the growing importance of...") with the causal claim stated outright, or nothing. Prefer is/are/has over "serves as" and "boasts". Generic examples ("such as improved efficiency") are worse than no example. Catalog: §3, §7, §8, §11.

### 5. Vary rhythm

Uniform cadence is the most machine-readable signal there is, and word lists don't touch it. Operational targets:

- Sentence length should spread. In any ~150-word stretch, include at least one sentence under 8 words and one over 25. If three consecutive sentences land within ±20% of the same length, break one.
- Vary opening shapes. Three consecutive sentences starting subject-verb, or two starting with the same word, is a beat; interrupt it with a clause-first or fragment opening where register allows.
- Vary paragraph mass. All paragraphs at 2-4 sentences is a tell. Let one run long; let one be a single line.
- Read it aloud (internally). Anywhere the prose falls into a meter, break the meter.

A single short emphatic sentence is a tool. A run of them is §31. Catalog: §31, §39.

### 6. Kill the rituals

No throat-clearing: don't open by restating the request, the title, or a definition; open with the most specific claim in the piece. No signposting ("let's dive in", "here's what you need to know"). No fake-candid hooks ("Honestly?", "Here's the thing"). No transition theater, including questions asked only to answer them ("So what does this mean?"). No closers: recap paragraphs, "Ultimately," "In conclusion," upbeat send-offs, "challenges remain" padding. A fake-profound kicker (a final aphorism, metaphor, or mic-drop line) gets deleted, not rewritten into a better metaphor: end on the strongest concrete sentence, takeaway, or next action already in the piece. No chatbot residue ("I hope this helps", "Would you like me to..."). Formatting is not thinking: reasoning goes in prose; bullets are for genuinely enumerable items; no bold-for-emphasis mid-sentence; no header per two paragraphs; headings are plain claims, not "X: Why Y Matters." Start inside the point. Stop when the content stops. Catalog: §6, §16, §20, §22, §25, §27, §28, §29, §33, §35-38, §40, §41.

## Hard rules

- **No em dashes (—) or en dashes (–) in the final output.** This is the single most reliable tell and both readers and detectors key on it. Replace with, in rough order: a period, a comma, a colon, parentheses, or restructure. Never fix by comma-splicing two independent clauses. Only exception: a user writing sample that uses them (match its frequency).
- **No emojis** unless the register or the user's sample uses them.
- **No invented facts, names, numbers, dates, quotes, or citations.** A fabricated specific is a defect even when it sounds more human than the vague original.
- **Don't rewrite quoted material**, titles, proper names, or text where a watched phrase is being discussed rather than used.

## Verification pass

Run mechanically on every deliverable in Modes A and B (Mode C delivers findings, not prose, so it skips this):

1. Search for `—`, `–`, ` -- `. Any hit: not done.
2. Search "not just", "isn't just", "more than just", "not only". Rewrite each hit.
3. Any exactly-three parallel list: justify or cut to one strong item.
4. First sentence: does it restate the prompt, the title, or a definition? Replace with a specific claim.
5. Last paragraph: does it summarize or send off? Delete it and end on the last concrete point.
6. Transplant test: any sentence that could sit unchanged in an unrelated document gets cut.
7. Sweep the high-frequency vocabulary in `references/patterns.md` §7. Restructure hits.
8. Scan three consecutive sentences anywhere: same length and same opening shape means rework (mechanism 5).
9. "Experts say / studies show / observers note": name the source or own the claim.
10. Read-aloud check: would this sound natural spoken to a sharp colleague? In Mode B, also: would the original writer recognize the result as their own voice?
11. Ask: "What still makes this read as AI-generated?" Fix what you find, then deliver.

## Over-correction traps

Humanizing is not flattening. Sterile, voiceless prose is as obvious as slop.

- Where the content calls for it (essays, opinion, personal writing), let the writer have stance, mixed feelings, humor, asides, and uneven rhythm. For encyclopedic, technical, or legal text, neutral and plain *is* the correct human voice.
- Never fake humanity: no inserted typos, forced slang, or manufactured idioms.
- Keep hedges where uncertainty is the content (forecasts, risk, medicine, legal exposure).
- Don't turn genuinely enumerable content (steps, specs, schedules) into prose.
- Use contractions wherever the register allows; their total absence is itself a tell.
- Polish, formality, common transitions, curly quotes, or a single em dash in *source* text are not proof of AI. Look for clusters of tells before rewriting hard. See "What not to flag" in `references/patterns.md`.

## Composing with brand-voice skills

If a brand or copy-editing skill also applies (e.g. a company voice guide), it wins on voice, terminology, claims, and any pattern it explicitly endorses. Concretely: if the brand guide endorses intentional fragments or rhythmic parallelism ("Not behind a login. Not in a dashboard."), those are voice in that register, not tells; do not "fix" them. This skill still governs everything the brand guide is silent on: hedging, inflation, ritual openers/closers, rhythm variance, invented facts, and chatbot residue. Both this skill and typical brand guides ban em dashes; that rule holds everywhere.

## References

- `references/patterns.md` — the full detector catalog: 33 patterns from Wikipedia's "Signs of AI writing" (via blader/humanizer, MIT) plus 10 additions targeting drafting-time tells, Claude-conversational tells, and faux-insight patterns (§42-43 via petergyang/no-ai-slop, MIT). Read in full for Modes B and C; consult by section number from the mechanisms above.
- `references/registers.md` — per-register playbook: cold outreach, LinkedIn, blog/essay, technical docs, reports/memos, internal chat. Read the matching section before drafting anything customer-facing.
