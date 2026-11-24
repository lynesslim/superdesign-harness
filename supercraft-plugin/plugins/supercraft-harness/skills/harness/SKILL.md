---
name: harness
description: Supercraft Studio's mandatory screenshot-to-Elementor build workflow. Use whenever building, rebuilding or editing a WordPress + Elementor page or section from a brief, reference screenshot, wireframe or URL via Novamira Pro — it sets discovery, design-system-first approval, section build plan, asset sourcing, the strict 4-tier build ladder, Elementor V3 styling rules, design guardrails, and the visual-critic QA loop.
---

# Supercraft Autonomous Web Design & Build Harness

## Mission
Convert client briefs and reference screenshots into production-grade WordPress + Elementor pages via **Novamira Pro** while enforcing Supercraft Studio's design taste, layout-first engineering, custom plugins, and independent visual QA.

## Target Environment
- The target WordPress site is whatever the current project's `CLAUDE.md` or `.mcp.json` names (a local Docker site from `setup-project`, or a remote Novamira site). If none is set, ask which site to build on.
- **Expected plugins:** `elementor`, `pro-elements`, `supercomponent-studio`, `supercraft-animation-plugin`, `supercraft-master-plugin`, `novamira`, `novamira-pro`. **Theme:** `hello-elementor`.

---

## Mandatory Workflow: Discovery → Design System → Build → QA

### Step 1: Clarify Gaps, Visual Direction & Load Guides
1. **Clarify Ambiguities Before Starting:** If the user's request is ambiguous or has gaps, ask **one concise batch of questions** before proposing the design system or touching the site:
   - **Theme Polarity:** Light, Dark, or Hybrid (e.g., light body with dark hero/footer or scroll-triggered dark spotlight section).
   - **Layout Width:** Full-width (edge-to-edge) or Boxed — **Narrow (`1280px`)**, **Medium (`1400px`)**, or **Wide (`1600px`)**.
   - **Awwwards-Winning Animated Sections (Include?):** Ask the user whether to include **Awwwards-winning animated sections** (1–2 signature moments so the page has pacing, rather than animating everything).
     - **If yes:** Query `library.supercraft.my` (`novamira --site library.supercraft.my`) for `component` posts with `style_tier = "awwwards"` (filtered by `theme_polarity` and relevant `component-category` / `motion_patterns`) and **propose 1–2 specific sections from the library** with their `preview_image` / `preview_video`, `layout_pattern`, and `ai_summary` (covering patterns like *Sticky Stage / Card Stacking*, *Horizontal Scroll*, *Scroll-Scrubbed Media/Parallax*, *Scroll Background Shift*, *Scroll-Fill Typography*, *Cinematic Section Transitions*, or *Cross-Element Choreography*).
   - **Visual Direction (Show Samples/References, Not Just Text):** When clarifying or proposing visual direction (typography tone, asset style, spacing density, accent/surface mood, navigation/CTA style), **show visual samples or reference screenshots** rather than text-only descriptions. When `library.supercraft.my` is accessible (`novamira --site library.supercraft.my`), query `component` posts by `style_tier` (`awwwards` / `enhanced` / `standard`), `motion_patterns`, `theme_polarity`, and `component-category` to pull real `preview_image` / `preview_video` samples. When asked for options or suggestions, list/show them and leave the page alone until the user chooses.
2. **Load Supporting Skills:**
   - Load `superanimation-guide` (Tier 1 interactive & scroll choreography).
   - Load `supercomponent-guide` only if Tier 3 custom widgets are needed.
3. **Examine Every Reference:** Inspect all reference screenshots, wireframes, and URLs before building.

### Step 2: Design System First (Visual Approval Gate → Elementor Kit)
1. **Present Visual Swatches & Live Font Specimens (Never Just Hex/Names):**
   - Show **rendered colour swatches** (with role labels: background, surface, primary text, muted text, accent, border, and text-on-background contrast pairs) and **live Google Font-pairing specimens** (`H1`, `H2`, `Eyebrow`, `Body`, `Button`) using an inline visual preview or rendered screenshot — never just raw hex codes in plain text.
   - **Banned fonts:** Never use `Inter` or `Arial`. Pair expressive display + readable body fonts with tight display tracking (`-0.02em` to `-0.04em`) and `clamp()` fluid display sizing.
   - **Wait for explicit user approval** before building. Keep the approved palette and fonts fixed unless the user asks to change them.
2. **Save to Elementor Kit (`manage-global-styles-v3`):**
   - **Merge** into the active Kit's settings — **never replace** them.
   - Save Global Colors, a **small role-based Global Typography preset set** (`H1`, `H2`, `H3`, `Body`, `Caption`, `Eyebrow`, `Button` — merge near-duplicates instead of adding one preset per size), and the global body font.
   - Set the approved boxed `container_width` (if boxed) globally in Site Settings, and set the Kit's default container padding to `0` so padding does not stack at every nesting level.
   - Zero the last paragraph's bottom margin once globally so container gaps control spacing.

### Step 3: Section Build Plan (With Visuals) & Asset Prep
1. **Section-by-Section Build Plan:**
   - Decompose every section into Elementor V3 **Flexbox Containers**, **CSS Grid Containers**, and **nested containers** (`elType: "container"`). Spot "fake complexity" (overlapping cards, floating badges, split heroes, layered images) that is **Tier 1 Native Elementor** using nested containers, negative margins, or `position: absolute` + `z-index`.
   - Assign a **Build Tier (1 → 4)** and any scroll/motion pattern to every section.
   - **Show a section-by-section visual reference** (cropped/annotated region of the reference screenshot, or a matching `library.supercraft.my` `component` `preview_image` / `preview_video` + `ai_summary` matched by `style_tier`, `motion_patterns`, `theme_polarity`, and `component-category`, or a wireframe visual) alongside each section's planned layout and tier. For any approved Awwwards sections drawn from `library.supercraft.my`, inspect the component's linked `elementor_template_id` (`_elementor_data`) as the structural/animation blueprint and adapt its tokens, copy, and media to the project's approved Design System. Get user sign-off before building.
2. **Visual Asset Extraction & Sourcing:**
   - Cut a **placeholder logo** from brand assets first and swap in the real one later.
   - **Stock Photography & General Scenes → Instant Images (WP Plugin):** Search and import high-resolution stock photos directly into the Media Library.
   - **Bespoke / Non-Stock / Brand Visuals → Higgsfield Connector / Image Tool (Images Only):** Brief image generation with the layout in mind (e.g., clear side for headline text), **review every generated image visually** before uploading, and use background-removed transparent files for product shots.
   - **Videos → Placeholder Video Only (NEVER Generate Video):** Use a Pexels, YouTube, or Vimeo URL.
   - **UI Icons & Simple Marks:** Use Elementor's native Icon Library, Skyboot Icons, Font Awesome, or clean inline SVGs.
   - Upload assets through Novamira into the Media Library and **record all media IDs in one shared helper file**.

### Step 4: Build Section by Section (Strict 4-Tier Ladder via Novamira Pro)
Work **section by section** and keep pages as **drafts** until the user says to publish.

#### 4-Tier Build Priority Ladder
Always use the **lowest-complexity tier** that achieves full fidelity. **Exhaust Tier 1 before Tier 2, and Tier 2 before Tier 3.**
- **Tier 1 — Native Elementor + Installed Add-on Widgets + Supercraft Animation *(Default)***
  - Flexbox/Grid/nested Containers + native Elementor widgets (`heading`, `text-editor`, `image`, `button`, `icon-list`, `video`, etc.) + installed add-on widgets.
  - Exhaust `Supercraft Animation Plugin` (`supercraft_advanced_animations`, `supercraft_named_enabled`, `hover`, `click`, `idle_loop`, `scroll_into_view`, `static_state`, cross-element triggers, section transitions) before custom JS or `supercomponent`.
  - Use Elementor Pro motion effects for parallax, and **disable parallax on mobile**.
- **Tier 2 — Native Elementor + Custom CSS/JS**
  - Use minimal, commented per-element `custom_css` (`selector { ... }`) or a small JS enhancement **only** where Elementor V3 lacks native controls (e.g., `backdrop-filter`, looping marquees, inline highlights, `clamp()` fluid typography, mixed-track `grid-template-columns`, `position: sticky` + `top`, multi-layer gradient+image backgrounds, `:hover` image zoom/card lift). Never use a page-wide `<style>` HTML widget.
- **Tier 3 — Custom `supercomponent` Widget (`SuperComponent Studio`)**
  - Use `widgetType: "supercomponent"` only when bespoke interactive DOM state, complex dynamic repeaters, or custom markup cannot be achieved cleanly in Tiers 1–2. Follow `supercomponent-guide` (`schema` + Mustache `html` + scoped `css` + scoped `js`).
- **Tier 4 — Custom WordPress / Elementor Plugin *(RESTRICTED)***
  - **NEVER** create a custom plugin unless strictly impossible in Tiers 1–3, and **always ask the user for explicit permission first**.

#### Novamira Pro, Global Token & Elementor V3 Rules
- **Never hand-write raw `_elementor_data` JSON:** Always build and edit through Novamira Pro (`check-setup`, `get-widget-schema`, `add-element`, `edit-element`, `delete-element`, `manage-global-styles-v3`, `clear-document-cache`). Call `get-widget-schema` before using unfamiliar widgets.
- **V3 Only (Never V4 Atomic):** Always use V3 (`elType: "container"`, `heading`, `text-editor`, `image`, `button`, etc.). Never use v4 atomic elements (`e-flexbox`, `e-div-block`, `e-heading`, etc.).
- **Global & Reusable:** Every colour and text style must reference the global colours and typography presets (hard-code only what globals can't express, such as semi-transparent fills and shadows). If any part is generated from code, run a conversion step before publishing to turn literals into global references and compare computed values before/after to confirm the look is unchanged.
- **Boxed Inheritance:** On root section containers, set `content_width: "boxed"` and omit per-section `boxed_width` overrides so sections inherit the global Site Settings width.
- **Containers vs. Widgets:** Containers use `margin` and `padding`; widgets use `_margin` and `_padding`. Using the wrong one fails silently — verify that overlaps and offsets actually applied.
- **Flex & Typography Hygiene:**
  - Percentage widths plus gaps must total under `100%`, or the row wraps.
  - Set heading size, line height, and tracking explicitly, with tablet and mobile sizes.
  - Use explicit `<br>` line breaks sparingly and hide them on mobile so text flows.
- **V3 Grid & Sticky Gotchas:**
  - On `container_type: "grid"` with custom `grid-template-columns`, add `selector::before, selector::after { content: none; display: none; }` and `selector { grid-template-rows: auto; --e-con-grid-template-rows: auto; }`.
  - On `position: sticky` containers, keep `top` in `custom_css` and ensure ancestor containers do not set `overflow: hidden` (use `overflow-x: clip`).
- **Banned AI Tropes:** Never generate generic 3-column boxy icon cards with thin borders or uninspired `Inter`/`Arial` typography pairings.

### Step 5: Verify & Independent Visual QA (`visual-critic`)
1. **Runtime & Computed Verification:**
   - Explicitly set the preview viewport (**Desktop `1440px`**, **Mobile `390px`**, and **Tablet**) before judging layout; **reset to desktop** when finished.
   - Speed up animations before screenshots (e.g., `gsap.globalTimeline.timeScale(50)`), and also verify how motion actually behaves at runtime (loops, scroll-scrub, parallax disabled on mobile).
   - **Measure instead of guessing:** Read computed margins, sizes, and transforms in the page to diagnose spacing issues.
   - Verify zero horizontal overflow at `390px` (`scrollWidth <= innerWidth`), tap targets `>= 44x44px`, zero console/network errors, and **open the Elementor editor at the end** to confirm stability.
   - Report anything you could not verify.
2. **Independent `visual-critic` Subagent:**
   - Spawn `supercraft-harness:visual-critic` in an **isolated session** passing only: (1) the file path to the target reference screenshot (save pasted images to disk first), (2) the live staging URL, and (3) the global design tokens used.
   - If `visual-critic` returns `FAIL`, patch the exact defects via Novamira Pro, purge Elementor's CSS cache (`_elementor_css` + `files_manager->clear_cache()`), and re-run `visual-critic` (up to **3 cycles**) until it returns `PASS`.
