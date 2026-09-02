# Pattern catalog

Detection reference for the humanizer skill. These are detectors, not a substitution table: the fix for a hit is restructuring the sentence per the six mechanisms in SKILL.md, never a synonym swap.

Patterns 1-33 are adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup) via [blader/humanizer](https://github.com/blader/humanizer) v2.9.1, MIT License, Copyright (c) 2025 Siqi Chen. Patterns 34-41 are additions in this fork targeting drafting-time and conversational-model tells. Patterns 42-43 are adapted from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop), MIT License, Copyright (c) 2026 Peter Yang.

## Contents

- Content patterns: §1-6
- Language and grammar: §7-13
- Style: §14-19
- Communication artifacts: §20-22
- Filler, hedging, rhetoric: §23-33
- Additions in 3.0: §34-41
- Additions in 3.1: §42-43
- What NOT to flag (false positives)
- Signs of human writing (preserve these)

---

## Content patterns

### 1. Inflated significance, legacy, and broader trends

**Watch:** stands/serves as, is a testament/reminder, vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its enduring/lasting, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted
**Problem:** LLMs puff up importance by declaring that arbitrary details represent or contribute to something larger.
**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.
**After:**
> The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization of administrative functions in Spain.

### 2. Notability and media-coverage padding

**Watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence
**Problem:** Lists of citations or follower counts asserted as importance, without context.
**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
**After:**
> Her views have been cited in The New York Times and the BBC.

Keep the one citation the source gives real context for; drop the rest. Don't invent context to justify the trim.

### 3. Superficial analyses with -ing endings

**Watch:** highlighting..., underscoring..., ensuring..., reflecting..., symbolizing..., contributing to..., fostering..., encompassing..., showcasing...
**Problem:** Present-participle trailers tacked onto sentences to add fake depth.
**Before:**
> The temple's color palette resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
**After:**
> The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

### 4. Promotional and advertisement-like language

**Watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, breathtaking, must-visit, stunning
**Problem:** Neutral topics rendered as travel brochures.
**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### 5. Vague attributions and weasel words

**Watch:** industry reports, observers have cited, experts argue/believe, some critics argue, several sources
**Problem:** Opinions attributed to unnamed authorities.
**Before:**
> Experts believe it plays a crucial role in the regional ecosystem.
**After:**
> Researchers and conservationists study the Haolai River for its unusual characteristics.

If a real source exists, name it. An unsupported claim gets cut, not decorated.

### 6. Formulaic "challenges and future prospects" sections

**Watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook
**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, Korattur continues to thrive as an integral part of Chennai's growth.
**After:**
> Korattur has recurring traffic congestion and water shortages.

---

## Language and grammar

### 7. High-frequency AI vocabulary

**Watch:** actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), leverage, pivotal, robust, seamless, showcase, streamline, tapestry (abstract), testament, underscore (verb), unlock, valuable, vibrant
**Problem:** These words spike in post-2023 text and co-occur. One is nothing; a cluster is a confession.
**Before:**
> An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
**After:**
> Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

### 8. Copula avoidance

**Watch:** serves as, stands as, marks, represents [a], boasts/features/offers [a]
**Problem:** Elaborate constructions where "is" or "has" belongs.
**Before:**
> Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet.
**After:**
> Gallery 825 is LAAA's exhibition space, with four rooms totaling 3,000 square feet.

### 9. Negative parallelisms and tailing negations

**Problem:** "Not only... but...", "It's not just about X, it's Y", and clipped tailing fragments ("no guessing", "no wasted motion") tacked onto sentence ends.
**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression. It's not merely a song, it's a statement.
**After:**
> The heavy beat adds to the aggressive tone.

Register exception: a brand voice guide may endorse this rhythm for marketing copy. There it's voice; follow the brand guide. Everywhere else it's a tell.

### 10. Rule-of-three overuse

**Problem:** Ideas forced into triads to appear comprehensive.
**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
**After:**
> The event includes talks and panels, with time for informal networking between sessions.

### 11. Elegant variation (synonym cycling)

**Problem:** Repetition-penalty behavior produces "the protagonist... the main character... the central figure... the hero" for one referent.
**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs.
**After:**
> The protagonist faces many challenges but eventually triumphs.

### 12. False ranges

**Problem:** "From X to Y" where X and Y aren't on a scale.
**Before:**
> Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the enigmatic dance of dark matter.
**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Actor-hiding passives and subjectless fragments

**Problem:** The actor disappears ("The results are preserved automatically") or the subject drops ("No configuration file needed"). Rewrite when knowing the actor matters or the fragment reads clipped for its register. Terse fragments are legitimate in reference docs and UI text; don't inflate them there.
**Before:**
> The results are preserved automatically.
**After:**
> The system preserves the results automatically.

---

## Style

### 14. Em dashes and en dashes: cut them

**Rule:** The final output contains no em dashes (—) or en dashes (–). This is a hard constraint, not a preference; it is the most recognized AI tell in circulation. Replace each, in rough order: a period, a comma, a colon, parentheses, or restructure. Catch spaced dashes (` — `) and double hyphens (` -- `) too. Never fix by comma-splicing two independent clauses; restructure instead.
**Before:**
> The new policy — announced without warning — affects thousands of workers.
**After:**
> The new policy, announced without warning, affects thousands of workers.

Only exception: a user-provided writing sample that uses them. Match the sample's frequency.

### 15. Boldface overuse

**Before:**
> It blends **OKRs**, **KPIs**, and visual tools such as the **Business Model Canvas**.
**After:**
> It blends OKRs, KPIs, and visual tools like the Business Model Canvas.

### 16. Inline-header vertical lists

**Problem:** Bulleted lists of **Header:** sentence pairs where a paragraph belongs.
**Before:**
> - **User Experience:** The interface has been significantly improved.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with encryption.
**After:**
> The update improves the interface, speeds up load times, and adds end-to-end encryption.

### 17. Title Case in headings

Use sentence case unless the destination's style says otherwise.

### 18. Emojis

No decorative emojis on headings or bullets unless the register or the user's sample uses them.

### 19. Quotation mark consistency

Mixed curly and straight quotes in one document is an assembly artifact. Pick one style (straight by default for anything technical) and hold it.

---

## Communication artifacts

### 20. Chatbot correspondence residue

**Watch:** I hope this helps, Of course!, Certainly!, You're absolutely right, Would you like..., Want me to...?, Should I continue?, let me know, here is a...
**Problem:** Assistant-to-user chatter pasted as content.
**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 21. Knowledge-cutoff disclaimers and speculative gap-filling

**Watch:** as of [date], up to my last training update, while specific details are limited, based on available information, maintains a low profile, keeps personal details private, likely [grew up/studied/began], it is believed that
**Problem:** Narrating the absence of a source, then papering over it with stock guesses.
**Before:**
> Information about her early life is not publicly available, suggesting she maintains a low profile. She likely grew up in a middle-class household, which shaped her later interest in education reform.
**After:**
> Her early life is not documented in the available sources.

Or cut the sentence. State facts only when a source provides them.

### 22. Sycophantic and servile tone

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
**After:**
> The economic factors you mentioned are relevant here.

---

## Filler, hedging, rhetoric

### 23. Filler phrases

- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "has the ability to process" → "can process"
- "It is important to note that the data shows" → "The data shows"
- "It's worth noting that" → (delete)

### 24. Hedging stacks

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.
**After:**
> The policy may affect outcomes.

One qualifier per claim, and only when the uncertainty is information.

### 25. Generic positive conclusions

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.
**After:**
> (Cut the paragraph. End on the last concrete fact. If the source states real plans, use those.)

### 26. Uniform compound hyphenation

**Problem:** Hyphenating pairs identically everywhere, including predicate position. Keep attributive hyphens ("a high-quality report"); drop them after the noun ("the report is high quality").

### 27. Persuasive authority tropes

**Watch:** the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter
**Problem:** Ceremony pretending to cut through to a deeper truth, followed by a restated ordinary point.
**Before:**
> At its core, what really matters is organizational readiness.
**After:**
> That mostly depends on whether the organization is ready to change its habits.

### 28. Signposting and announcements

**Watch:** let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado
**Problem:** Announcing what the text is about to do instead of doing it.
**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.
**After:**
> Next.js caches data at multiple layers: request memoization, the data cache, and the router cache.

### 29. Fragmented headers

**Problem:** A heading followed by a one-line paragraph restating the heading before real content begins. Delete the warm-up line.

### 30. Diff-anchored writing

**Problem:** Docs or comments narrating a change instead of describing the thing as it is. Outside changelogs and migration guides, text should read coherently without knowing what the last commit did.
**Before:**
> This function was added to replace the previous approach of iterating through all items.
**After:**
> This function uses a hash map for O(1) lookups.

### 31. Manufactured punchlines and staccato drama

**Problem:** Every sentence engineered to land like a quotable closer; runs of short declarative fragments stacked for drama. One short sentence for emphasis is a tool; a run of them is engineering.
**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
**After:**
> AlphaEvolve changed the search because it did not favor symmetry or human-looking designs, which made some older assumptions less useful.

### 32. Aphorism formulas

**Watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of
**Problem:** Ordinary claims dressed as reusable profundity. Replace with the concrete claim being gestured at.

### 33. Fake-candid rhetorical openers

**Watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk (as standalone hooks)
**Problem:** A theatrical pause-and-reveal before a routine point. A person being honest just says the thing.
**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.
**After:**
> Whether it's worth the price depends on how often you'll use it.

---

## Additions in 3.0

### 34. Paragraph-level equivocation

**Watch:** ultimately it depends, on the other hand, both approaches have merit, there's no one-size-fits-all answer, the right choice depends on your specific needs
**Problem:** Sentence-level hedging (§24) has a paragraph-level cousin: lay out both sides, then close without a position. This is the model refusing to do the reader's actual job. Commit to the side the evidence supports, or state the decision rule.
**Before:**
> Both approaches have their merits. Option A offers flexibility, while Option B provides simplicity. Ultimately, the right choice depends on your specific needs and use case.
**After:**
> Use Option A. B is faster to set up, but you'll hit its ceiling the first time you need custom routing, and migrating later costs more than the extra day now. The only case for B: a team that will never touch this again.

### 35. Question-as-transition

**Watch:** So what does this mean for...?, Why does this matter?, How did we get here?, The question then becomes...
**Problem:** Mid-document questions asked only so the next sentence can answer them. This is §33's cousin, moved from the opener into the body. Delete the question; state the answer.
**Before:**
> So what does this mean for school districts? It means budget season is the moment to act.
**After:**
> For school districts, budget season is the moment to act.

### 36. Colon-subtitle headings

**Watch:** X: Why Y Matters, X: A Deep Dive, X: What You Need to Know, X: The Complete Guide
**Problem:** The two-part headline formula reads as generated because it is the statistically safest headline shape. Make the heading a plain claim or a plain noun phrase.
**Before:**
> ## Network Segmentation: Why It Matters for Districts
**After:**
> ## Districts get breached through flat networks

### 37. Over-sectioning and formatting as thinking

**Problem:** A header every two paragraphs, reasoning fragmented into bullets, structure substituting for argument. If a bullet list contains full sentences whose commas and connectives are doing logical work, it is a paragraph wearing a costume. Prose carries reasoning; bullets carry genuinely enumerable items (steps, specs, options). Under ~600 words, a piece rarely needs headers at all.

### 38. Empty topic sentences and list preambles

**Watch:** There are several factors to consider., A few things stand out., This has a number of implications., Below are some key points:
**Problem:** A sentence that announces content instead of carrying any. Cut it, or make it carry the point.
**Before:**
> There are several factors to consider when timing outreach. First, budget cycles matter.
**After:**
> Timing outreach is mostly about budget cycles.

### 39. Uniform paragraph mass

**Problem:** Every paragraph 2-4 sentences, same visual weight, same internal shape. The paragraph-level version of uniform cadence. Merge, split, and let mass follow importance: a long paragraph where the argument lives, a one-line paragraph where a point lands.

### 40. Prompt-echo and definition openers

**Watch:** openers that rephrase the request or the title; "X is defined as", "X refers to", "In today's [adjective] world/landscape"
**Problem:** The first sentence is the highest-value real estate in the piece, and models spend it restating what the reader already knows. Open with the most specific claim available.
**Before:**
> Cybersecurity has become increasingly important for school districts in today's threat landscape.
**After:**
> Two of the district's neighbors got hit with ransomware last spring; the board's $1.2 million response tells you what they're afraid of.

(That specific must come from the source. If there is no specific, open with the plainest true claim, not an inflated one.)

### 41. Recap closers

**Watch:** In summary, In short, To sum up, In conclusion, final paragraphs that restate earlier points in compressed form
**Problem:** §25 covers upbeat send-offs; this is the neutral version. A closing paragraph that adds no new information exists only because the shape of an essay seemed to demand one. End on the last concrete point, a consequence, or the next action.

---

## Additions in 3.1

### 42. Faux-insight setups

**Watch:** what most people get wrong, here's what nobody tells you, the part everyone misses, most people don't realize, what they don't teach you, the secret is
**Problem:** The claim is dressed as contrarian secret knowledge, flattering the writer as the lone expert and the reader as the insider. The setup adds no information. Cut it and let the claim stand on its own.
**Before:**
> The part everyone misses: distribution is the real moat.
**After:**
> Distribution is the moat.

### 43. In-sentence colon reveals

**Watch:** a short noun phrase, a colon, then a dramatic payoff. "The best part: it learns." "The detail that makes it work: a separate agent grades it." "One problem: nobody asked."
**Problem:** §36 covers this shape in headings; in body text it is a theatrical pause before a routine point, and runs of it are among the strongest current tells. Colons are for lists, labels, ratios, and quotes. State the point as a plain sentence, and connect it causally where the source supports it.
**Before:**
> The best part: the whole thing runs offline.
**After:**
> It runs offline, so the demo doesn't depend on conference wifi.

---

## What NOT to flag (false positives)

Clean human writing can hit several patterns above. Before rewriting, check you aren't gutting legitimate prose. Not reliable indicators on their own:

- Perfect grammar and consistent style. Polish is not AI.
- Mixed casual and formal registers.
- Bland prose without specific tells. Generic dryness is just dry writing.
- Formal vocabulary generally. AI overuses the *specific* words in §7, not all brainy words; don't flatten "ostensibly" or "constituent."
- Salutations and sign-offs. They predate ChatGPT by centuries.
- Common transitions in isolation. One "however" is not a tell; a pileup of "additionally, moreover, consequently" is.
- Curly quotes alone (most editors auto-curl).
- Em dashes alone *in source text you're judging*. Many journalists use them. In your own output the ban in §14 still holds.
- One short emphatic sentence. Flag staccato only in runs (§31).
- Unsourced claims. Most of the web is unsourced.
- Watched phrases inside quotations, titles, or examples where the phrase is discussed rather than used.

Look for clusters. A single em dash means nothing; em dashes plus rule-of-three plus "vibrant tapestry" plus a Conclusion section is a confession.

## Signs of human writing (preserve these)

Lean toward leaving the prose alone when you see:

- Specific, unusual, hard-to-fabricate detail. Real addresses, weird quotes, "the lawyer who used to work upstairs from my dentist." Models round off specifics; humans hoard them.
- Mixed feelings and unresolved tension. "Mostly good, but it bothers me and I can't fully explain why."
- Dated, era-bound references and in-jokes.
- First-person editorial choices the writer can defend.
- Genuine sentence-length variety.
- Asides, parentheticals, self-corrections. "(I keep wanting to say 'almost' here, but it really was certain.)"
- Anything written before November 30, 2022.
