---
name: polish-design-tokens
description: Polish an existing Elementor page by fixing ONLY typography (font pairing, size scale, tracking, line height), spacing (gutter, section rhythm) and colour roles. Never changes layout, copy, images or sections. Works on a safe unlisted clone via Novamira CLI. Use when the user says the page looks amateurish/unpolished/inconsistent and wants "just the design tokens fixed", asks for a "polished version" of a page, or invokes /polish-design-tokens.
---

# polish-design-tokens

> Paths like `scripts/…` and `references/…` are relative to this skill's base directory (shown when the skill loads). Use absolute paths when running them.

Fix the *design system* of an existing page without touching its structure.

**In scope:** font pairing, type scale, tracking, line height, body size, eyebrow and button type, one page gutter, one section rhythm, neutral and accent colour roles.
**Out of scope (never do):** moving, adding or removing sections/widgets, editing copy, swapping images, changing animations, changing the shared header/footer templates, changing site-wide Elementor global colours/typography (other pages use them).

## Inputs (ask only for what you cannot infer)
1. **Site** — a Novamira site profile (`novamira sites` lists them). Default to the site already in context.
2. **Target page** — page ID or URL.
3. **Brand colour** — optional. If omitted, `scripts/audit.js` infers it from the page; show the inferred value and confirm if it looks wrong.
4. **Font direction** — optional: a pairing id from `references/font-pairings.json`, or "pick for me" (choose by the brand character; say why).

## Connection
Prefer the Novamira CLI (OAuth, no stale sessions):
`novamira --site <profile> --json --yes run novamira/execute-php --input @file.json`
(`--yes` is required for execute-php; only run PHP you wrote and that is read-only or scoped to the clone.) If the CLI is not authorised, run `novamira auth login <site-url>` first, and `novamira --site <profile> doctor --json` to verify. Do not paste secrets in chat.
Only Elementor v3 container/widget pages are supported. If the page uses v4 atomic elements (`e-flexbox`, `e-heading`), stop and tell the user; v3 style CSS overrides will not map cleanly.

## Workflow
1. **Clone, never edit the original.** Copy the page (post + `_elementor_data`, `_elementor_page_settings`, `_wp_page_template`, edit-mode meta) into a new page titled "<Title> polished", published but with AIOSEO `robots: {index: noindex, follow: nofollow}`. Remember its ID. Never touch the original post.
2. **Audit the clone.** Navigate Playwright to the clone (use a cache-bust like `?qa=1`, never `?m=`/`?p=`), then call `browser_run_code_unsafe` with `filename` set to the absolute path of `scripts/audit.js` (there is no `require`/fs in that sandbox, so the result comes back inline). It sets 1440x900 and scrolls the page once itself. Write the returned JSON to a scratch file (e.g. `audit.json` in the session scratchpad). It reports fonts, sizes, section padding, background colours, an inferred brand colour, and a role map (hero title, section titles, card titles, sub-heads, lede, eyebrows, body, section backgrounds) keyed by Elementor element IDs.
3. **Show findings** to the user briefly (fonts in use, number of distinct sizes, gutter/padding spread, neutral greys) before changing anything. Flag any element the heuristics could not classify; do not guess.
4. **Derive tokens, do not hardcode.** Run:
   `python3 scripts/build_overrides.py --audit audit.json --page-id <CLONE_ID> --pairing <id|auto> [--brand #hex] --out overrides.css --tokens-out tokens.json`
   It derives ink/deep/paper/mist/sky/body from the brand colour, computes the type scale (see `references/token-rules.md`), and emits one scoped stylesheet (`body.page-id-<ID> …`) plus the Google Fonts link. Read `tokens.json` and sanity-check contrast and sizes; adjust flags (`--base`, `--ratio`, `--gutter`, `--section`) rather than editing the CSS by hand.
5. **Apply.** Inject the stylesheet as a single `html` widget in a new zero-padding root container at the end of the clone, using Novamira's `elementor-add-element` ability (never hand-write `_elementor_data`). `scripts/apply_overrides.py --page-id <ID> --css overrides.css --out apply.json` writes the `execute-php` payload (it is idempotent: it first deletes any earlier `polish-tokens` block and clears the Elementor cache); run it with the CLI.
6. **Verify.** Re-run the audit and a viewport scroll at 1440 and 390 (take JPEG viewport shots, not full-page: sticky cards and scroll animations make full-page captures misleading). Check: new fonts loaded (`document.fonts`), no leftover old font families, no horizontal overflow (scrollWidth vs innerWidth; a ~15px scrollbar gutter is fine), link/button heights ≥ 44px at 390, no clipped text. Fix by adjusting flags or adding a targeted rule, then re-run steps 4-5 (the previous block is replaced automatically). If leftover old fonts remain, they are usually custom-widget markup: add a targeted rule to `build_overrides.py` (generic, by widget class), not a one-off.
7. **Report honestly.** A before/after table (fonts, sizes, section padding, neutrals), the two URLs to compare, and an explicit list of: elements not classified, shared header/footer left untouched, items not verified (animations, tablet width), and pre-existing issues you did not fix (e.g. split-text animation glitches). Promoting the polished copy to the live page needs the user's explicit yes and is a separate step.

## Guardrails
- Original page and site-wide globals stay untouched unless the user explicitly asks.
- Use `-0.02em` to `-0.04em` tracking for display type, 0 for body; body ≥ 16px; tap targets ≥ 44px.
- Do not use Inter or Arial as the pairing (project rule).
- Screenshot fidelity and the user's brand beat these defaults; if the user names a font, colour or spacing, use it.
- Keep scratch files out of the project root (use the session scratchpad); delete screenshots when done if the user asks.

## Known limits
- Role detection is heuristic (heading size tiers, single-item icon-lists as eyebrows). Anything it cannot place is returned under `unclassified`; list it for the user.
- Sticky cards, split-text and scroll animations make full-page screenshots misleading; use scrolled viewport shots.
- Header/footer template roots are marked `template` and skipped for spacing/background.
- Tested on one Elementor v3 container page (IPEC home). Treat the first run on a new site as a trial and verify visually.
