---
name: supercomponent-guide
description: Tier 3 guide for authoring custom SuperComponent Studio widgets (widgetType "supercomponent") in Elementor via Novamira Pro.
---

# SuperComponent Studio — Custom Widget Authoring Guide (Tier 3)

Use this guide **only when Tier 1 (Native Elementor + Add-ons + Supercraft Animation) and Tier 2 (Native Elementor + Custom CSS/JS) cannot cleanly achieve the required component**.

Your goal is to author a **custom, designer-editable `supercomponent`** from scratch (`schema` + Mustache `html` + scoped `css` + scoped `js`)—not to rely on static presets.

---

## 1. Elementor Widget Structure (`widgetType: "supercomponent"`)

When adding a `supercomponent` widget via Novamira Pro (`add-element` / `edit-element`), populate these `settings` keys:

* `active_schema_id` *(string)* — Sanitized kebab-case version of `schema.id` (lowercase, non-alphanumeric → `-`, e.g. `"pricing-toggle"`). **Must match `schema.id`.**
* `schema` *(JSON string)* — Defines the Elementor sidebar controls:
  ```json
  {
    "id": "pricing-toggle",
    "name": "Pricing Toggle",
    "settings": [
      {
        "tab": "content",
        "section": "Header",
        "id": "heading",
        "label": "Heading",
        "type": "text",
        "default": "Simple, transparent pricing"
      },
      {
        "tab": "style",
        "section": "Colors",
        "id": "accent_color",
        "label": "Accent Color",
        "type": "color",
        "default": "#FF3B26"
      }
    ]
  }
  ```
* `html` *(Mustache HTML string)* — Markup with `{{variable}}` / `{{{raw_html}}}` / `{{#repeater}}...{{/repeater}}` tags.
* `css` *(CSS string)* — Scoped styles referencing `var(--control_id)` CSS variables and `.sc-{typography_id}` classes.
* `js` *(JS string)* — Optional interactive script scoped to `instanceId`.
* **Dynamic Control Values:** Every control in `schema.settings` is stored in Elementor `settings` under the **scoped key**:
  ```text
  sc_{active_schema_id}_{control.id}
  ```
  Example: `"sc_pricing-toggle_heading": "Simple, transparent pricing"`.

---

## 2. Supported Schema Control Types & Rendering

Common control properties: `id` (required), `type` (required), `label` (required), `tab` (`"content"` | `"style"` | `"advanced"`), `section` (default `"Component Settings"`), `default`, `description`, `condition` (`{ "other_id": "yes" }` — PHP auto-prefixes with `sc_{active_schema_id}_`).

| `type` | Default Format in `schema` & `settings` | HTML (Mustache) | CSS Variable / Class Emitted |
| :--- | :--- | :--- | :--- |
| `text` | `"string"` | `{{id}}` (escaped) / `{{{id}}}` (raw) | `--{id}: {val};` |
| `textarea` | `"string"` (also for inline `<svg>`) | `{{{id}}}` (raw) / `{{id}}` | `--{id}: {val};` |
| `richtext` | `"<p>HTML</p>"` | `{{{id}}}` | `--{id}: {val};` |
| `switcher` | `"yes"` or `"no"` | `{{#id}}...{{/id}}` / `{{^id}}...{{/id}}` | `--{id}: {val};` |
| `select` | `"val"` + `"options": [{"value":"val","label":"Label"}]` | `{{id}}` | `--{id}: {{VALUE}};` |
| `color` | `"#111827"` | `{{id}}` | `--{id}: {{VALUE}};` + `.sc-{id} { color: {{VALUE}} !important; }` |
| `number` | `12` (`min`, `max`, `step`) | `{{id}}` | `--{id}: {{VALUE}};` |
| `slider` | `{"size": 16, "unit": "px"}` (`min`, `max`, `step`, `unit`) | `{{id.size}}` | `--{id}: {{SIZE}}{{UNIT}};` |
| `dimensions` | `{"top":"20","right":"20","bottom":"20","left":"20","unit":"px"}` | — | `--{id}: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};` |
| `typography` | *(no default needed)* | Add class `sc-{id}` to HTML tag | `{{WRAPPER}} .sc-{id}` (stores `sc_{schema_id}_{id}_font_family`, etc.) |
| `image` | `{"url": "https://..."}` | `{{id.url}}`, `{{#id.url}}...{{/id.url}}` | `null` |
| `video` | `{"url": "https://..."}` | `{{id.url}}` | `null` |
| `media` | `{"url": "https://..."}` | `{{id.url}}` | `null` |
| `url` | `{"url": "https://...", "is_external": false}` | `{{id.url}}` *(see gotcha)* | `null` |
| `icons` / `icon` | `{"value": "fas fa-star", "library": "fa-solid"}` | `{{{id}}}` or `{{id}}` | `null` |
| `repeater` | Array of row objects (`fields`, `title_field`) | `{{#id}}...{{/id}}` | `null` |

---

## 3. Authoring Rules & Critical Gotchas
1. **Always Scope CSS:** CSS variables (`--{id}`) are automatically scoped to `.elementor-element-{id}`, but your custom `css` block is **not** auto-scoped. Prefix all selectors with a unique component class (e.g., `.sc-pt-wrap .sc-pt-card { ... }`) so styles never leak onto the rest of the page.
2. **Always Scope JS to `instanceId`:** The plugin wraps `js` in `(function() { var instanceId = '{id}'; ... })();`. Always query inside `const root = document.getElementById('supercomponent-' + instanceId); if (!root) return;` rather than `document.querySelector(...)`, so multiple instances on one page never collide.
3. **Make It Truly Editable:** Expose headlines, body copy, button labels/links, images, colors, padding/gaps, and repeater items in `schema.settings`—never hardcode client copy or colors in `html`/`css` without controls.
4. **Root-Level `url` Ternary Gotcha:** `{{link.is_external ? '_blank' : '_self'}}` and `{{link.target}}` work inside `{{#repeater}}...{{/repeater}}` loops, **not** at the root level. For root-level links, use a separate `switcher` if you need conditional `target="_blank"`.
5. **Font Awesome:** Font Awesome 6.5.1 is auto-enqueued on the frontend; `icons` controls render via `{{{id}}}`.
6. **License Gate:** `supercomponent_is_validated()` must be active in WordPress for the widget to register and render.
