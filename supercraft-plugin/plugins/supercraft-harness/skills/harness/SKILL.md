---
name: harness
description: Supercraft Studio's mandatory screenshot-to-Elementor build workflow. Use whenever building, rebuilding or editing a WordPress + Elementor page or section from a brief, reference screenshot, wireframe or URL via Novamira Pro — it sets the section build plan, design tokens, asset sourcing, the strict 4-tier build ladder, Elementor V3 styling rules, design guardrails and the visual-critic QA loop.
---

# Supercraft Autonomous Web Design & Build Harness

## Mission
Convert client briefs and reference screenshots into production-grade WordPress + Elementor pages via **Novamira Pro** while enforcing Supercraft Studio's design taste, layout-first engineering, custom plugins, and independent visual QA.

## Target Environment
- The target WordPress site is whatever the current project's `CLAUDE.md` or `.mcp.json` names (a local Docker site from the `setup-project` skill, or a remote Novamira site). If none is set, ask which site to build on.
- **Expected plugins:** `elementor`, `pro-elements`, `supercomponent-studio`, `supercraft-animation-plugin`, `supercraft-master-plugin`, `novamira`, `novamira-pro`. **Theme:** `hello-elementor`.

---

## Mandatory Workflow: Screenshot-to-Elementor

### Step 1: Load Plugin Skills First
Before building anything, load these skills from this plugin:
- `superanimation-guide` (`Supercraft Animation Plugin` — Tier 1 interactive & scroll choreography)
- `supercomponent-guide` (`SuperComponent Studio` — Tier 3 custom widget authoring)

### Step 2: Visual & Structural Decomposition (Think Before Building)
Before calling any Novamira build tool, analyze the reference screenshot section-by-section and write a short **Section Build Plan**:
1. **Decompose into Elementor Layout Primitives:**
   - Think in terms of **Flexbox Containers**, **CSS Grid Containers**, and **nested containers** (`elType: "container"`).
   - **Spot "Fake Complexity":** Many seemingly complex sections (overlapping cards, floating badges, split/asymmetric heroes, offset grids, layered images) are **Tier 1 Native Elementor** using:
     - Nested containers (`flex-direction`, `gap`, `align-items`, `justify-content`)
     - **Negative margins** (e.g., pulling a card or image up over a hero)
     - **Absolute positioning** (`position: absolute` + `z-index` inside a `position: relative` parent container)
2. **Assign a Build Tier (1 → 4) to Every Section** using the strict priority ladder below.

### Step 2b: Visual Asset, Media & Typography Extraction
Before building sections, extract the **Design Tokens** and **Asset Manifest** from the screenshot:
1. **Typography (Elementor Google Fonts):**
   - Identify the screenshot's typographic character (e.g., editorial serif + grotesk sans, bold geometric display + clean sans/mono) and select a **suitable Google Font pairing** supported natively by Elementor.
   - Configure **Global Colors** (background, surface, primary text, muted text, accent) and **Global Typography** in Elementor via Novamira (`manage-global-styles-v3`) before assembling sections.
2. **Visual Asset Extraction & Sourcing:**
   - Inventory every image, illustration, and icon in the screenshot and route each to the proper source (never leave broken URLs or generic placeholder boxes):
     - **Stock Photography & General Scenes → Instant Images (WordPress Plugin):** Use the **Instant Images** plugin in WordPress to search and import high-resolution stock photos directly into the WordPress Media Library.
     - **Bespoke / Non-Stock / Brand-Specific Visuals → Higgsfield Connector (Images Only):** Pass the **reference screenshot** to the **Higgsfield connector** and instruct it to extract/recreate the specific bespoke visual/asset (e.g., custom 3D render, hero artwork, stylized illustration), then upload the resulting image into the WordPress Media Library via Novamira.
     - **Videos → Placeholder Video Only (NEVER Generate Video):** **Never** run AI video generation. For background videos, VSLs, or showreels, use a placeholder video (e.g., a Pexels video, YouTube, or Vimeo URL).
     - **UI Icons & Simple Marks:** Use Elementor's native Icon Library, the **Skyboot Icons** plugin in WordPress, Font Awesome, or clean inline SVGs.

### Step 3: Strict 4-Tier Build Priority Ladder
Always use the **lowest-complexity tier** that achieves full visual and interactive fidelity. **Exhaust Tier 1 before moving to Tier 2, and exhaust Tier 2 before moving to Tier 3.**

- **Tier 1 — Native Elementor + Installed Add-on Widgets + Supercraft Animation *(Default)***
  - Use Flexbox/Grid/nested Containers + native Elementor widgets (`heading`, `text-editor`, `image`, `button`, `icon-list`, `video`, etc.) + installed add-on widgets (Elementor Pro, Marquee, etc.).
  - **Exhaust Supercraft Animation first:** `Supercraft Animation Plugin` (`supercraft_advanced_animations` + `supercraft_named_enabled`) supports `hover`, `click`, `idle_loop`, `scroll_into_view`, `static_state`, and **cross-element triggers** (e.g., hover Component A → reveal/animate Component B). Use it for interactive cards, hover reveals, split-text entrances, image reveals, section transitions, and scroll background shifts before reaching for custom JS or `supercomponent`.
- **Tier 2 — Native Elementor + Custom CSS/JS**
  - Use when native widgets + Supercraft Animation cover the structure, but you need custom CSS (gradients, clip-paths, glassmorphism, pseudo-elements, custom grid spans) or a small JS enhancement.
- **Tier 3 — Custom `supercomponent` Widget (`SuperComponent Studio`)**
  - Use `widgetType: "supercomponent"` **only** when a section requires bespoke interactive DOM state, complex dynamic repeaters, or custom markup that Tier 1 and Tier 2 cannot cleanly achieve.
  - Author a **custom** `supercomponent` (`schema` JSON + Mustache `html` + scoped `css` + scoped `js` + `sc_{active_schema_id}_{field}` settings) so every text, image, color, and item remains editable in the Elementor sidebar.
- **Tier 4 — Custom WordPress / Elementor Plugin *(RESTRICTED)***
  - **NEVER** create a custom WordPress or Elementor plugin unless it is strictly impossible in Tiers 1–3.
  - **ALWAYS stop and ask the user for explicit permission** before creating any custom plugin.

### Step 4: Build via Novamira Pro (Never Hand-Write Raw `_elementor_data` JSON)
- **Do NOT** hand-craft or overwrite raw `_elementor_data` post meta JSON directly.
- Always build and edit through **Novamira Pro's Elementor abilities** (`check-setup`, `get-widget-schema`, `add-element`, `edit-element`, `delete-element`, `manage-global-styles-v3`, `clear-document-cache`) so Elementor's own schema validation, element IDs, and CSS/document cache are handled cleanly.
- Before using any unfamiliar widget (add-on or custom), call `get-widget-schema` via Novamira to inspect its exact control keys.

### Step 5: Independent Visual QA (`visual-critic` Subagent)
- After building, **always** spawn this plugin's `visual-critic` agent (`supercraft-harness:visual-critic`) as an **isolated subagent** (independent session with no builder bias).
- Pass it only: (1) the **file path** to the target reference screenshot (if the user pasted an image in chat, save a copy to disk first so `visual-critic` can `Read` it), (2) the live staging URL, and (3) any global design tokens used.
- If `visual-critic` returns `FAIL`, patch the exact defects via Novamira Pro and re-run `visual-critic` (up to **3 cycles**) until it returns `PASS`.

---

## Elementor V3 Native Styling & Global Layout Rules
- **Always Use V3 Containers & Widgets (Never V4 Atomic):** Always build with Elementor V3 (`elType: "container"`, `heading`, `text-editor`, `image`, `button`, etc.). **Never** use Elementor v4 atomic elements (`e-flexbox`, `e-div-block`, `e-heading`, `e-paragraph`, `e-image`, `e-button`).
- **Global Boxed Layout Width:** Always set the site's boxed `container_width` (e.g., `1280px`) globally in **Elementor Site Settings** (active Kit). On root section containers, set `content_width: "boxed"` and **omit** per-section `boxed_width` overrides so all sections inherit—and update together from—the global Site Settings width.
- **Native Elementor Controls First (No Global `<style>` Widgets):** Style every container and widget using native Elementor V3 sidebar controls (`flex_direction`, `flex_justify_content`, `flex_align_items`, `flex_wrap`, `flex_gap`, `padding`, `margin`, `width`/`_tablet`/`_mobile`, `min_height`, `overflow`, `_flex_size`, `_flex_align_self`, `_element_width`/`_element_custom_width`, `background_*`, `border_*`, `box_shadow_*`, `typography_*`, colors, `position: "absolute"` + `_offset_orientation_h/v` + `_offset_x/y/end`, `image` `object-fit`/`object-position`).
- **Minimal Per-Element `custom_css`:** Never use a page-wide `<style>` HTML widget. Use per-element `custom_css` (`selector { ... }`) **only** for CSS properties Elementor V3 lacks native controls for (e.g., mixed-track `grid-template-columns`, `grid-auto-rows`, `grid-column`/`grid-row` spans, `backdrop-filter`, `clamp()` fluid typography, `position: sticky` + `top`, multi-layer gradient+image backgrounds, and `:hover` image zoom/card lift). Omit redundant defaults like desktop `position: relative` on containers.
- **V3 Grid & Sticky Gotchas:**
  - On `container_type: "grid"` with custom `grid-template-columns`, add `selector::before, selector::after { content: none; display: none; }` and `selector { grid-template-rows: auto; --e-con-grid-template-rows: auto; }` so Elementor's default 2-row grid doesn't create an empty second row.
  - On `position: sticky` containers, keep `top` in `custom_css` (Elementor's `_offset_y` only applies to `absolute`/`fixed`) and ensure ancestor containers do not set `overflow: hidden`.

---

## Design Taste & Hard Guardrails
- **Banned AI Tropes:** Never generate generic 3-column boxy icon cards with thin borders or uninspired `Inter`/`Arial` typography pairings.
- **Typography & Rhythm:** Use expressive display + body pairings, `clamp()` fluid display sizing, and tight headline tracking (`-0.02em` to `-0.04em`).
- **Zero Mobile Regressions:** Zero horizontal overflow at `390px`, no clipped backgrounds, no overlapping text/buttons, and all tap targets `>= 44x44px`.
- **Clean DOM & Editor Stability:** Page must open cleanly in the Elementor visual editor and load with zero browser console errors.
