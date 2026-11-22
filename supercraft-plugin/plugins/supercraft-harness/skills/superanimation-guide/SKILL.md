---
name: superanimation-guide
description: Exhaustive Tier 1 guide for Supercraft Animation Plugin—including hover/click cross-element triggers, static_state, scroll transforms, text reveals, and section transitions in Elementor.
---

# Supercraft Animation Plugin — Exhaustive Tier 1 Guide

**Exhaust this plugin's capabilities before escalating to Tier 2 (Custom CSS/JS) or Tier 3 (`supercomponent`).**
`Supercraft Animation Plugin` can build rich, interactive UI choreography—including **hovering Element A to reveal or animate Element B**, **click-triggered state changes**, **scroll-scrubbed parallax/transforms**, **split-text reveals**, and **section transitions**—directly on native Elementor Containers and Widgets.

---

## 1. Golden Rules
1. **Containers & Widgets Only:** Frontend `supercraft_apply_attrs` is **only** hooked to `container` and `widget` elements (excluding `tabs` and `nested-tabs`). **Never** put Supercraft animation settings on legacy `section` or `column` elements—always use `elType: "container"`.
2. **Never Inject Duplicate GSAP / Lenis / SplitType:** The plugin already loads GSAP (`3.12.4`), ScrollTrigger (`3.12.5`), SplitType (`0.3.3`), and Lenis (`1.1.20`) globally when validated.
3. **Server-Side Attribute Rendering:** All controls have `frontend_available => false` and are emitted server-side by `render-attributes.php` onto `_wrapper`. Setting the control keys via Novamira Pro (`add-element` / `edit-element`) is all that is needed.
4. **License Gate:** `supercraft_is_validated()` (or `SUPERCRAFT_ALLOW_UNVALIDATED`) must be true in WordPress.

---

## 2. Complex UI Choreography (Cross-Element Triggers & `static_state`)

You do **not** need custom JS or `supercomponent` for interactive hover reveals, floating card overlays, or click-triggered animations. Combine **Named Elements** + **`supercraft_advanced_animations`**:

### How Named Elements Work
1. On any Container or Widget you want to reference as a **trigger** or **target**, enable:
   ```json
   {
     "supercraft_named_enabled": "yes",
     "supercraft_named_label": "card-preview"
   }
   ```
   *(PHP slugifies `supercraft_named_label` to lowercase kebab-case, e.g., `"Card Preview"` → `"card-preview"`.)*
2. On the target element (or a host container), use `supercraft_advanced_animations` (repeater):
   * Set `"trigger": "static_state"` to define its **initial resting state** (e.g., hidden with `custom_opacity: 0`, `custom_y: 16`, `custom_scale: 0.96`).
   * Set `"trigger": "hover"` (or `"click"`) with:
     * `"trigger_element_mode": "named"`, `"trigger_named_element": "trigger-card"`
     * `"animated_element_mode": "named"`, `"animated_named_element": "card-preview"`
     * `"hover_effect": "custom-transform"` (or `"focus-reveal"`, `"soft-elevate"`, etc.)
     * `custom_start_*` → `custom_*` (e.g., `custom_opacity: 1`, `custom_y: 0`, `custom_scale: 1`).

### Example: Hover Element A (`trigger-card`) → Reveal & Slide-Up Element B (`preview-badge`)
**On Element A (Trigger Container/Widget):**
```json
{
  "supercraft_named_enabled": "yes",
  "supercraft_named_label": "trigger-card"
}
```
**On Element B (Target Container/Widget — initially hidden, revealed on Element A hover):**
```json
{
  "supercraft_named_enabled": "yes",
  "supercraft_named_label": "preview-badge",
  "supercraft_advanced_animations": [
    {
      "_id": "init_hidden_1",
      "label": "Initial Hidden State",
      "trigger": "static_state",
      "custom_x": 0,
      "custom_y": 16,
      "custom_rotate": 0,
      "custom_blur": 0,
      "custom_scale": 0.96,
      "custom_opacity": 0
    },
    {
      "_id": "hover_reveal_1",
      "label": "Reveal on Trigger Hover",
      "trigger": "hover",
      "hover_effect": "custom-transform",
      "hover_duration": 0.3,
      "delay": 0,
      "ease": "power2.out",
      "intensity": 1,
      "speed": 1,
      "trigger_element_mode": "named",
      "trigger_named_element": "trigger-card",
      "animated_element_mode": "named",
      "animated_named_element": "preview-badge",
      "custom_start_x": 0,
      "custom_start_y": 16,
      "custom_start_rotate": 0,
      "custom_start_blur": 0,
      "custom_start_scale": 0.96,
      "custom_start_opacity": 0,
      "custom_x": 0,
      "custom_y": 0,
      "custom_rotate": 0,
      "custom_blur": 0,
      "custom_scale": 1,
      "custom_opacity": 1
    }
  ]
}
```

---

## 3. All Advanced Tab Options (`supercraft_advanced_animations`)
* **`trigger`:** `"scroll_into_view"`, `"click"`, `"idle_loop"`, `"hover"`, `"static_state"`
* **`hover_effect`** *(when `trigger: "hover"`)*:
  `"micro-scale"`, `"tactile-press"`, `"soft-elevate"`, `"3d-float"`, `"focus-reveal"`, `"float-blur"`, `"skew-press"`, `"magnetic-pull"`, `"cinematic-zoom"`, `"zoom-bg"`, `"scroll-zoom-bg-in"`, `"scroll-zoom-bg-out"`, `"custom-transform"`
* **`idle_effect`** *(when `trigger: "idle_loop"`)*:
  `"pulse"`, `"float"`, `"spin-continuous"`, `"spin-yoyo"`, `"breathe"`, `"swing"`, `"custom-transform"`
* **`animation_type`** *(when `trigger: "scroll_into_view"` or `"click"`)*:
  `"scroll-transform"`, `"image-reveal"`, `"container-reveal"`, `"split-text"`
* **`trigger_element_mode` / `animated_element_mode`:** `"self"` or `"named"` (with `trigger_named_element` / `animated_named_element` set to the slugified `supercraft_named_label`).
* **`hover_duration`:** number in seconds (default `0.1` for hover); **`duration`:** number in seconds (default `0.8` for other triggers); **`delay`:** seconds (default `0`); **`intensity` / `speed`:** numbers (default `1`).

---

## 4. Entrance Tab (`supercraft_anim_category`)

Set `"supercraft_anim_category"` to one of:
`""` (None), `"scroll-transform"`, `"split-text"`, `"image-reveal"`, `"container-reveal"`, `"scroll-fill-text"`, `"text-reveal"`, `"scroll-bg-color"`, `"video-gsap"`.

### A. `scroll-transform`
* `supercraft_scroll_preset`: `"fade-up"` *(default)*, `"fade-down"`, `"fade-left"`, `"fade-right"`, `"fade"`, `"zoom-in"`, `"zoom-out"`, `"blur-fade"`, `"blur-fade-up"`, `"blur-fade-down"`, `"blur-fade-left"`, `"blur-fade-right"`, `"blur-zoom-in"`, `"blur-zoom-out"`, `"scroll-zoom-bg-in"`, `"scroll-zoom-bg-out"`, `"custom"`
* **Preset mode:** `supercraft_trigger` (`"top 85%"`), `supercraft_preset_duration` (`1`), `supercraft_delay` (`0`), `supercraft_ease` (`"power2.out"`)
* **Scrub mode (`supercraft_scroll_scrub`: `"yes"`):** `supercraft_scrub_start` (`"top 85%"`), `supercraft_scrub_end` (`"top 15%"`), `supercraft_scrub_ease` (`"none"`), `supercraft_scrub_forward` (`"yes"`/`""`)
* **Custom mode (`supercraft_scroll_preset`: `"custom"`):** `supercraft_ct_start_x/y/rotate/blur` (`0`), `supercraft_ct_start_scale/opacity` (`1`), `supercraft_ct_end_x/y/rotate/blur` (`0`), `supercraft_ct_end_scale/opacity` (`1`). *(Gotcha: set `supercraft_ct_start_opacity: 0` explicitly for fade-ins; `""` or `null` forces `1`.)*

### B. `split-text` (Headlines & Editorial Typography)
* `supercraft_split_mode`: `"chars"` *(default)* or `"words"`
* `supercraft_split_variant_char` / `supercraft_split_variant_word`: `"fade-x"` *(default)*, `"fade-y"`, `"fade-blur"`, `"mask-up"`
* `supercraft_split_preset`: `"light"`, `"medium"` *(default)*, `"dramatic"`, `"custom"`
* `supercraft_split_delay`: `0`
* Optional scrub: `supercraft_split_scrub`: `"yes"`, `supercraft_split_scroll_start` (`"top 85%"`), `supercraft_split_scroll_end` (`"top 40%"`), `supercraft_split_forward` (`"yes"`/`""`)

### C. `image-reveal`
* `supercraft_image_preset`: `"left"`, `"right"`, `"top"`, `"bottom"`, `"envelope"`, `"envelope-single"`, `"custom"`
* `supercraft_image_color1` / `supercraft_image_color2` *(for `"envelope"` / `"envelope-single"`)*
* `supercraft_image_duration` (`1.5`), `supercraft_image_delay` (`0`), `supercraft_image_ease` (`"power2.out"`), `supercraft_image_trigger` (`"top 85%"`), `supercraft_image_scale` (`1.3`)

### D. `container-reveal`
* `supercraft_container_preset`: `"center"`, `"left"`, `"right"`, `"top"`, `"bottom"`, `"cinematic-gate"`, `"block-curtain"`, `"custom"`
* For `"block-curtain"`: `supercraft_container_block_color` (`"#ff3b26"`), `supercraft_container_block_count` (`5`), `supercraft_container_block_direction` (`"up"`/`"down"`/`"left"`/`"right"`), `supercraft_container_block_bg_effect` (`"none"`, `"zoom-out"`, `"zoom-in"`, `"blur"`, `"zoom-out-blur"`, `"zoom-in-blur"`)

### E. `text-reveal`, `scroll-fill-text`, `scroll-bg-color` & `video-gsap`
* **`text-reveal`:** `supercraft_text_reveal_preset` (`"envelope"`, `"envelope-single"`, `"decoder"`), `supercraft_text_reveal_duration` (`1`), `supercraft_text_reveal_delay` (`0`), `supercraft_text_reveal_trigger` (`"top 85%"`).
* **`scroll-fill-text`:** `supercraft_fill_start` (`"top 85%"`), `supercraft_fill_end` (`"top 60%"`), `supercraft_fill_base` (dim color), `supercraft_fill_line` (`"yes"`), `supercraft_fill_forward` (`""`).
* **`scroll-bg-color`:** `supercraft_bg_color_target` (hex), `supercraft_bg_color_scrub` (`"yes"` by default!), `supercraft_bg_color_start` (`"top 85%"`), `supercraft_bg_color_end` (`"top 50%"`), `supercraft_bg_color_forward` (`""`).
* **`video-gsap`:** `supercraft_video_preset` (`"scroll-scrub"`, `"horizontal-scrub"`), `supercraft_video_scroll_start` (`"top top"`), `supercraft_video_scroll_end` (`"bottom bottom"`), `supercraft_video_scrub_smoothing` (`0.5`).

---

## 5. Section Transitions (Container-Level)
* `supercraft_section_transition_enabled`: `"yes"`
* `supercraft_section_transition_preset`: `"vertical-shutter"`, `"liquid-curtain"`, `"diagonal-wipe"`, `"fade-blur"`
* `supercraft_section_transition_start`: `"bottom bottom+=20%"`, `supercraft_section_transition_end`: `"+=100%"`, `supercraft_section_transition_scrub`: `1`, `supercraft_section_transition_slats`: `16`, `supercraft_section_transition_fallback_color`: `"rgb(255,255,255)"`

---

## 6. Valid `$ease_options`
`"none"`, `"linear"`, `"power1.in"`, `"power1.out"`, `"power1.inOut"`, `"power2.in"`, `"power2.out"`, `"power2.inOut"`, `"power3.in"`, `"power3.out"`, `"power3.inOut"`, `"power4.in"`, `"power4.out"`, `"power4.inOut"`, `"expo.in"`, `"expo.out"`, `"expo.inOut"`, `"circ.in"`, `"circ.out"`, `"circ.inOut"`, `"back.in(1.7)"`, `"back.out(1.7)"`, `"back.inOut(1.7)"`, `"elastic.in(0.5,0.3)"`, `"elastic.out(0.5,0.3)"`, `"elastic.inOut(0.5,0.3)"`, `"bounce.in"`, `"bounce.out"`, `"bounce.inOut"`
