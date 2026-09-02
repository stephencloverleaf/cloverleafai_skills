---
name: logo-usage-guidelines
description: Apply Cloverleaf AI's official logo guidelines to any design, marketing, or development task. Use this skill whenever the user asks about logos, logo files, logo placement, logo color, logo sizing, logo spacing, logo versions, or which logo file to use. Trigger for phrases like "which logo should I use", "can I use the logo on a dark background", "what's the clear space rule", "logo for a presentation", "logo file for the website", "logo on a t-shirt", "logo in an email signature", "minimum logo size", "can I change the logo color", "is this logo usage correct", or any request involving Cloverleaf AI's visual brand mark. Always use this skill before giving any guidance about logos or providing logo files — even if the question seems simple.
---

# Cloverleaf AI Logo Usage Guidelines

Use this skill to guide correct logo usage across all contexts — marketing, design, development, and merchandise.

---

## Logo Versions

Cloverleaf AI has **two structural versions**, each in **two color variants** = 4 files total.

| File | Description | When to use |
|---|---|---|
| `Cloverleaf_AI_full_black.svg` | Logomark (symbol) + wordmark, black | Default. Use on light/white/beige backgrounds |
| `Cloverleaf_AI_full_white.svg` | Logomark (symbol) + wordmark, white | Use on dark backgrounds (navy, dark brown, black, dark imagery) |
| `Cloverleaf_AI_black_logo_textonly.svg` | Wordmark only, black | Use when the logomark is not needed or would clutter the layout |
| `Cloverleaf_AI_white_logo_textonly.svg` | Wordmark only, white | Same as above, on dark backgrounds |

**The logomark** is the geometric four-petal circle symbol. It can also be used standalone (as a favicon, app icon, embossed graphic on merchandise) but only in black or white.

---

## Color Rule — Black or White Only

The logo must **always** appear in black or white. No exceptions.

- **Black logo** → use on light backgrounds (white, off-white/cream, light secondary colors like pale blue)
- **White logo** → use on dark backgrounds (navy, dark brown, black, dark gradient imagery)
- **Never** recolor the logo in brand colors, gradients, or any other hue
- **Never** apply drop shadows, glows, or effects to the logo

This preserves boldness, legibility, and timeless consistency across all applications.

---

## Clear Zone (Spacing)

Always maintain clear space equal to the width of the **"C" in the wordmark** on all four sides of the logo.

- This applies to **both versions** (with and without the logomark)
- No text, graphics, or other elements may enter this clear zone
- The clear zone ensures the logo reads with impact and is never visually crowded

---

## Correct vs. Incorrect Usage

### ✅ DO
- Use on solid brand-approved backgrounds (white, off-white/cream, navy, dark brown, black)
- Use on photography/imagery as long as contrast is sufficient (white logo on dark areas, black logo on light areas)
- Use the text-only version when the logomark would clutter a layout
- Use the logomark standalone for icons, favicons, or embossed/embroidered merchandise

### ❌ DO NOT
- Recolor the logo (no brand colors, no gradients, no custom tints)
- Stretch, squish, or distort the logo proportions
- Place the logo on busy, low-contrast backgrounds where it becomes hard to read
- Add effects (drop shadows, glows, outlines, transparency)
- Recreate the logo in a different typeface
- Use the logo at sizes so small it becomes illegible (the "C" clear zone rule implicitly sets a minimum — if the spacing can't be honored, the logo is too small)

---

## File Format Guidance

| Use case | Recommended format |
|---|---|
| Web, UI, email | SVG (scales perfectly, small file size) |
| Print, high-res marketing | SVG or export to high-res PNG/PDF |
| Presentations (Keynote, PowerPoint) | SVG preferred; PNG at 2x resolution if SVG isn't supported |
| Embroidery / merchandise | Provide SVG to vendor; they'll convert as needed |
| Favicon / app icon | Export logomark only at required pixel sizes (16px, 32px, 180px) |

Always provide files from the approved SVG source assets — never screenshot or re-export from a low-quality source.

---

## Co-Branding Rules

When a Cloverleaf AI logo and a partner's logo must appear on the same asset:

### Placement
- Place the two logos in **different corners** of the asset — never side-by-side or stacked in the same area
- Typical convention: Cloverleaf AI logo in one corner (e.g. top-left or bottom-right), partner logo in the opposite corner
- Neither logo should dominate — aim for visual parity in sizing unless the context clearly calls for one brand to lead (e.g. a partner-hosted event)

### Spacing
- The **clear zone rule applies independently to each logo** — maintain a full "C"-width buffer around the Cloverleaf AI logo regardless of where the partner logo sits
- Never allow the partner logo to encroach on Cloverleaf AI's clear zone, and vice versa

### Identity Integrity
- **Never merge, overlap, or combine** the Cloverleaf AI logo with another brand's logo or mark
- **Never place both logos inside a shared container**, badge, or lockup (e.g. no shared box, circle, or background shape that houses both marks together)
- **Never modify the Cloverleaf AI logo** to "match" a partner's brand color or style
- If a partner's brand uses a color background that conflicts with logo legibility, choose the appropriate black or white version of the Cloverleaf AI logo for contrast — do not alter the logo itself

### Example Scenarios
| Scenario | Correct approach |
|---|---|
| Co-branded event banner | Cloverleaf AI logo top-left (white on dark), partner logo bottom-right |
| Partner one-pager | Cloverleaf AI logo in header, partner logo in footer (or opposite corners) |
| Joint press release header | Logos separated by clear space, not merged into a single lockup |
| Co-branded merch | Logos on opposite sides or areas of the item; never combined into one graphic |

---

## Assets

Official logo files bundled in the `assets/` directory (full logomark + wordmark lockup):
- `assets/Cloverleaf_AI_full_black.svg` — use on light backgrounds
- `assets/Cloverleaf_AI_full_white.svg` — use on dark backgrounds (navy, black)

The text-only wordmark variants are bundled too:
- `assets/Cloverleaf_AI_black_logo_textonly.svg` — wordmark only, light backgrounds
- `assets/Cloverleaf_AI_white_logo_textonly.svg` — wordmark only, dark backgrounds

These four are the authoritative source SVGs — always embed or reference one of them; **never recreate the logo or substitute a stand-in shape (for example, a colored dot)**. To embed in a self-contained HTML build, read the SVG and inline it (or base64 it as a `data:` URI) — this is exactly what `signal-dashboard` does for its header.
