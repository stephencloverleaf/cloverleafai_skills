---
name: typography-brand-guidelines
description: Apply Cloverleaf AI's official typography system and typeface rules to any design, code, or AI tool task. Use this skill whenever the user asks about fonts, typefaces, type hierarchy, or typescale for Cloverleaf AI. Trigger for any task involving UI design, marketing assets, presentations, code generation, or prompts for other AI tools (Midjourney, v0, Framer, Gamma, Canva AI, etc.) where Cloverleaf AI brand typography must be applied. Also trigger when user asks to "use brand fonts", "match the brand type", "what font do we use", "generate on-brand design", or any phrasing that implies visual consistency with Cloverleaf AI's identity. Always use this skill before writing any CSS, design specs, AI image prompts, or slide templates for Cloverleaf AI.
---

# Cloverleaf AI — Typography Brand Guidelines

Use this skill to apply the correct typefaces, weights, and typescale whenever producing design specs, UI code, AI tool prompts, or any visual asset for Cloverleaf AI.

---

## Typefaces

### Primary — Pangram Neue Montreal
- **Weight**: Medium only
- **Use for**: H1, H2, H3 (all primary display headlines and hero text)
- **Character**: Geometric, confident, modern
- **Do not use**: Light, Bold, or Black weights unless explicitly approved

### Secondary — Satoshi
- **Weights**: Medium (subheadings), Regular (body copy)
- **Use for**: H4 subheadings and all paragraph/body text
- **Character**: Clean grotesque, pairs with Neue Montreal
- **Do not use**: Satoshi Bold for headlines — that role belongs to Neue Montreal

### Tag Accent — B612 Mono
- **Weight**: Regular only
- **Use for**: Tags, badges, labels, UI metadata, data callouts
- **Character**: Monospaced, open-source, optimised for legibility at small sizes
- **Do not use**: For body copy, headings, or any running text

---

## Typescale

| Role | Font | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| H1 / H2 / H3 | Pangram Neue Montreal | Medium | 100% | 0% |
| H4 Subheading | Pangram Neue Montreal | Medium | 140% | 0% |
| Body Large | Satoshi | Regular | 120% | 0% |
| Body Default | Satoshi | Regular | 120% | -1% |
| Tags / Labels | B612 Mono | Regular | 95% | +4% |

---

## Core Rules

- Never mix Neue Montreal and Satoshi in the same heading
- B612 Mono is never used for body copy or headings
- Typographic hierarchy: Neue Montreal leads → Satoshi supports → B612 Mono accents
- **Sentence case** is the default for all headlines and subheads
- Title case is acceptable only where design balance clearly requires it

---

## Output by Context

When applying these rules, tailor the output format to the tool or task:

### UI / Web design tools (v0, Framer AI, Locofy, Builder.io)
Provide a structured token list:
```
Typography system:
- Headlines (H1–H3): Pangram Neue Montreal, Medium, line-height 100%, letter-spacing 0%
- Subheadings (H4): Pangram Neue Montreal, Medium, line-height 140%, letter-spacing 0%
- Body copy: Satoshi, Regular, line-height 120%, letter-spacing -1%
- Body large: Satoshi, Regular, line-height 120%, letter-spacing 0%
- Tags / labels: B612 Mono, Regular, line-height 95%, letter-spacing +4%
Sentence case for all headings. Do not substitute fonts.
```

### Image generation tools (Midjourney, Ideogram, Adobe Firefly)
Use descriptive style language (these tools cannot load fonts by name):
```
Typography style: clean geometric sans-serif headlines in the style of Pangram Neue Montreal Medium, supported by a neutral grotesque body font (Satoshi), with monospaced tag labels (B612 Mono). Modern, minimal, confident. No serif fonts. No decorative or script type.
```

### Presentation tools (Gamma, Beautiful.ai, Canva AI, PowerPoint Copilot)
```
Font rules:
- Slide titles: Pangram Neue Montreal Medium (or closest geometric sans-serif available)
- Body and bullets: Satoshi Regular (or closest grotesque sans-serif available)
- Data labels / tags / chips: B612 Mono Regular (monospace)
- Line height: 120–140% for body, 100% for display text
- Letter spacing: 0% default; -1% for body; +4% for monospaced tags
- Capitalisation: sentence case throughout
```

### Code generation (CSS / Tailwind / design tokens)
```css
/* Cloverleaf AI — Typography Tokens */
--font-primary:   'Neue Montreal', 'Pangram Neue Montreal', sans-serif;
--font-secondary: 'Satoshi', sans-serif;
--font-accent:    'B612 Mono', monospace;

--font-weight-display: 500;   /* Medium */
--font-weight-subhead: 500;   /* Medium */
--font-weight-body:    400;   /* Regular */

/* Typescale */
--text-h1: clamp(3rem, 6vw, 6rem);
--text-h2: clamp(2.25rem, 4.5vw, 4.5rem);
--text-h3: clamp(1.75rem, 3vw, 3rem);
--text-h4: clamp(1.25rem, 2vw, 1.75rem);
--text-body-lg: 1.125rem;
--text-body:    1rem;
--text-caption: 0.75rem;

/* Line heights */
--leading-display: 1;     /* 100% — H1/H2/H3 */
--leading-subhead: 1.4;   /* 140% — H4 */
--leading-body:    1.2;   /* 120% — Body */
--leading-caption: 0.95;  /* 95%  — Tags */

/* Letter spacing */
--tracking-display: 0em;
--tracking-body:   -0.01em;
--tracking-caption: 0.04em;
```

---

*Source: Cloverleaf AI Visual Guidelines, Typography section (Pages 56–61).*
