---
name: reference-parity-qa
description: Forensic section-by-section comparison between live reference URLs and library.supercraft.my Elementor builds (scroll scrub, sticky stages, blur/masks, hover states, and Elementor CSS cache purge).
---

# Forensic Reference Parity QA

Use this workflow when auditing and fixing `library.supercraft.my` sections against live reference URLs (e.g., from the Task List Google Sheet).

## 1. Read Target Rows
- Fetch the target `T###` rows (`URL`, `Section` in Column C, `Tag`) from the Task List spreadsheet via `gsheets`.

## 2. Batch Browser Inspection (2–5 Sections per Pass)
Never skim 10 sections in one static pass. For each batch:
1. Open the `library.supercraft.my` page and test every interactive control (accordions, tabs, hover cards) + scroll through each section.
2. Open each reference URL, jump directly to its Column C section, and compare at **matching scroll keyframes (`0% → 25% → 50% → 75% → 100%`)**:
   - **Layout & Sticky Stages:** Check for isolated `100vh` sticky title stages, full-bleed vs. boxed widths, card stacking, and `overflow-x: clip` (avoid `overflow: hidden` on sticky ancestors).
   - **Motion Type:** Distinguish **scroll-scrubbed** transforms (`supercraft_scroll_scrub: "yes"`) from one-shot `scroll_into_view` entrances.
   - **Optical Layers:** Inspect `filter: blur(...)`, `backdrop-filter`, `mask-image`, gradient overlays, and `::before`/`::after` pseudo-elements (remember Elementor optimized markup omits `.elementor-widget-container` on headings).
   - **Interactive States:** Verify accordion open/close transitions, icon rotation, hover color shifts, and cursor styles.

## 3. Patch via Novamira Pro
- Apply fixes via `novamira/elementor-edit-element` / `add-element` / `delete-element`.
- Leave duplicate placeholder copy untouched unless instructed otherwise; prioritize **structure, layout, optical effects, and scroll/hover behavior**.

## 4. Purge Elementor CSS Cache & Re-Verify
`novamira/elementor-clear-document-cache` alone does not regenerate Elementor's compiled `post-<ID>.css` file when `had_cache` is false. Always run:
```php
delete_post_meta($post_id, '_elementor_css');
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}
```
Then hard-reload in Chrome and verify at the **exact same scroll position** as the reference.

