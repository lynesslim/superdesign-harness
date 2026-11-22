# Token rules (defaults; the user's brand and explicit choices override them)

## Type
- Scale: base 16px (body 16-17px), ratio 1.25-1.333. 5-6 sizes total: caption/eyebrow 13-14, body 16-17, card title 20-26, section title 34-56 (fluid), hero 40-68 (fluid).
- Fluid display sizes with `clamp()`; example hero `clamp(2.5rem, 1rem + 4.1vw, 4.25rem)`.
- Line height: body 1.6-1.7, card titles 1.2, section titles 1.08-1.12, hero 1.04.
- Tracking: display serif -0.035em to -0.04em; sans titles -0.02em; body 0; eyebrows +0.1em uppercase 13px.
- Measure: body paragraphs max ~62ch.
- Two families max: one expressive display, one neutral UI/body. 2-3 weights. Never Inter/Arial.
- Don't use heavy weights on display serifs (400-500).

## Spacing
- 8px grid. One page gutter: `clamp(24px, 4.4vw, 64px)`. One section padding: `clamp(64px, 7vw, 104px)`.
- Space inside a group is about half the space between groups. Do not add vertical padding to hero/full-bleed media sections.

## Colour roles (derived from ONE brand colour)
- ink (very dark brand hue): headings on light, strong text.
- deep (dark navy of the brand hue): dark sections and dark overlays.
- body (muted ink, ~#2B3556 for blue): paragraph text, >= 4.5:1 on paper.
- paper (near white, tinted): default light background. mist (slightly deeper tint): alternate light background.
- sky (light tint of brand): chips, light buttons on dark, accent text on dark.
- brand: the single accent (<10% of the page). Replace mixed greys (#f8f8f8, #f5f5f5, white) with paper/mist alternating; replace pure black text with ink.

## Always verify
- Body contrast >= 4.5:1; large text >= 3:1.
- No horizontal overflow at 390; tap targets >= 44px; fonts actually loaded.
