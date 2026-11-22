# Product Requirements Document (PRD)
**Project:** Supercraft Autonomous Web Design & Build Harness (`supercraft-wp-harness`)  
**Version:** 1.0  
**Owner:** Lyness Lim (Founder & Creative Director, Supercraft Studio)  
**Target Users:** Internal Production Team (Winson Tan – UI/UX Lead, Edmund Chin – Web Dev, Yin Yin – PM/Strategist)  
**Primary Tech Stack:** Claude Code (CLI/IDE) + Novamira Pro + WordPress + Elementor Pro + ACF + CPT UI + Custom Internal Elementor Plugin + Playwright MCP  

---

## 1. Executive Summary & Objective
Build an internal, repository-based **Agent Harness** on top of **Claude Code** and **Novamira Pro** that enables Supercraft’s team to execute an end-to-end website build from a single command (`/build-page`). 

Instead of letting an AI generate generic, unstyled layouts from scratch, the harness enforces **Supercraft’s design taste, strategy-first conversion hierarchy, and proprietary 200-component library** (plus our internal custom Elementor plugin), pushes builds directly to a temporary staging WordPress URL via Novamira Pro, and runs an autonomous **Playwright visual self-critique loop** until desktop and mobile quality standards pass.

---

## 2. Goals & Success Metrics
* **Single-Command Orchestration:** Trigger the full workflow (*Art Direction Spec → Component Retrieval → Staging Build → Custom Motion/CSS → Visual QA & Self-Healing*) via one slash command (`/build-page`).
* **Design Taste Fidelity:** ≥80% of page sections assembled from Supercraft’s approved 200-component library or internal Elementor plugin rather than raw hallucinated widgets.
* **Autonomous Visual QA:** Zero horizontal mobile overflow (`390px`), zero broken Elementor JSON structures, and full adherence to global typography/color tokens before human review.
* **Team Portability & Subscription Efficiency:** Distributed via a private Git template repo; authenticates via individual/Team Claude Code seats (zero shared logins, zero surprise API spikes).

---

## 3. System Architecture & Stack

| Layer | Technology / Tool | Role in the Harness |
| :--- | :--- | :--- |
| **Orchestration Harness** | **Claude Code** (`CLAUDE.md`, `.claude/skills/`, `.claude/agents/`) | Reads client briefs/mockups, enforces agency rules, queries the 200-component index, and orchestrates subagents. |
| **WordPress Bridge** | **Novamira Pro** (Plugin + Novamira CLI / HQ) | Connects Claude Code over HTTPS to Hostinger temporary staging URLs; executes WP-CLI, edits child-theme PHP/CSS, manages ACF/CPT UI, and assembles Elementor V3/V4 layouts. |
| **Design Memory** | `library/components-index.json` + Thumbnail Previews | Lightweight metadata index of Supercraft’s 200 Elementor components so the agent selects exact layout matches without blowing up context tokens. |
| **Internal Plugin Bridge** | Novamira Skill (`supercomponent-guide.md`) + PHP Abilities | Documents our custom internal Elementor plugin widgets/controls and exposes safe insertion hooks. |
| **Visual Eyes & QA** | **Playwright MCP** + `visual-critic` Subagent | Renders the live staging URL at `1440px` and `390px`, captures screenshots, checks console errors, and grades visual craft in an isolated context. |

---

## 4. Repository Structure (Deliverable 1)
The developer must initialize a private Git template repository (`supercraft-wp-harness`) with the exact structure below:

```text
supercraft-wp-harness/
├── CLAUDE.md                          # Global Supercraft agency rules, design taste & coding standards
├── .mcp.json                          # MCP config for Playwright MCP (Novamira connects via CLI/MCP)
├── library/
│   ├── components-index.json          # Searchable metadata manifest of the 200 Elementor components
│   └── components/                    # Raw Elementor JSON exports + 1440px reference screenshots
│       ├── hero-split-vsl.json
│       ├── hero-split-vsl.png
│       └── ...
├── scripts/
│   ├── index-components.js            # Script to validate/update components-index.json
│   └── staging-preflight.sh           # Checks staging URL HTTPS, REST API reachability, and Novamira status
└── .claude/
    ├── agents/
    │   └── visual-critic.md           # Isolated subagent for ruthless desktop/mobile visual QA
    └── skills/
        ├── build-page/
        │   └── SKILL.md               # Master 1-command workflow (/build-page)
        ├── supercomponent-guide/
        │   └── SKILL.md               # Auto-generated schema & usage rules for our custom Elementor plugin
        └── audit-plugin/
            └── SKILL.md               # Utility skill to inspect/refresh custom plugin widget definitions
```

---

## 5. Functional Requirements

### FR-1: Staging Environment & Novamira Pro Integration
* **Target Environment:** Hostinger temporary staging WordPress URL (`https://...`) pre-loaded with WordPress, Elementor Pro, ACF, CPT UI, Supercraft’s custom internal Elementor plugin, and **Novamira Pro**.
* **Connection Method:** Developers connect via **Novamira CLI** (`novamira connect <staging-url>`) or **Novamira HQ** so terminal sessions remain lightweight and resilient to connection drops.
* **Safety & Staging Hygiene:**
  * Staging sites must enforce `noindex, nofollow` (`blog_public = 0`) automatically.
  * Before modifying any existing page, the agent must trigger a backup/snapshot via Novamira.
  * Production sites must strictly use **Novamira Read Mode** if ever inspected.

### FR-2: Custom Internal Elementor Plugin Onboarding
* **Requirement:** Novamira Pro must understand and prioritize Supercraft’s custom internal Elementor plugin widgets and templates over generic Elementor widgets.
* **Implementation:**
  1. Run an initial filesystem & widget-registry scan of `/wp-content/plugins/<custom-plugin>/` via Novamira to extract every custom widget slug (`get_name()`), control keys, default values, and responsive settings.
  2. Compile this output into `.claude/skills/supercomponent-guide/SKILL.md` (and sync a copy into Novamira’s in-WordPress Skills) so every future session loads the exact schema automatically.
  3. *(Optional Enhancement)* Register two lightweight WordPress Abilities (`supercraft/list_components` and `supercraft/insert_component`) in sandboxed PHP via Novamira so Claude can insert complex multi-container templates with one deterministic call.

### FR-3: 200-Component Library Indexing & Retrieval
* **Problem:** Passing 200 raw Elementor JSON files into Claude’s context window causes token exhaustion and degraded reasoning.
* **Implementation:** Create `library/components-index.json` containing lightweight metadata for each of the 200 components:
  ```json
  [
    {
      "id": "sc-hero-014",
      "name": "Asymmetric Split Hero with VSL & Floating Proof Badge",
      "category": "hero",
      "conversion_role": "above-the-fold-value-prop",
      "visual_tags": ["editorial", "high-contrast", "split-60-40", "dark-mode"],
      "uses_custom_plugin": true,
      "json_path": "library/components/sc-hero-014.json",
      "preview_path": "library/components/sc-hero-014.png"
    }
  ]
  ```
* **Retrieval Rule:** When given a wireframe, client brief, or reference screenshot, the agent must query `components-index.json` first, shortlist the top 1–3 matching components per section, inspect their preview thumbnails if needed, and load **only** the selected `.json` files into context.

### FR-4: The Master 1-Command Workflow (`/build-page`)
Invoked via `/build-page <brief-or-url> [optional-mockup-image] <staging-url>`. Must execute these 5 stages autonomously:

1. **Stage 1 — Art Direction & Conversion Architecture:**
   * Analyze the client brief and optional reference mockup.
   * Output a temporary `build-plan.json` defining:
     * **Conversion Flow:** Current-to-Desired state narrative, above-the-fold CTA placement, social proof sequence.
     * **Design Tokens:** Display & body font pairings, `clamp()` fluid typography scale, tight headline tracking (`-0.02em` to `-0.04em`), surface/accent color tokens, and container max-width (`1280px` or `1360px`).
     * **Motion Spec:** Single animation stack (**Lenis** smooth scroll + **GSAP / ScrollTrigger** staggered reveals)—strictly banning conflicting animation libraries.
2. **Stage 2 — Component Matching & WordPress Setup:**
   * Configure Elementor Global Colors and Global Typography on staging via Novamira Pro to match `build-plan.json`.
   * Register any required Custom Post Types (CPT UI) and ACF field groups if dynamic content is needed.
   * Map every section of `build-plan.json` to an existing ID in `components-index.json` (or our internal Elementor plugin). Only build net-new Elementor containers if no suitable component exists in the 200-component library.
3. **Stage 3 — Page Assembly & Custom Code Injection:**
   * Assemble the page on the staging URL via Novamira Pro, replacing placeholder copy with conversion-focused client copy and mapping dynamic ACF tags.
   * Write bespoke micro-interactions, custom hover states, and GSAP/Lenis scroll animations into Elementor Custom Code or child-theme assets via Novamira.
4. **Stage 4 — Autonomous Visual Audit (`visual-critic` Subagent):**
   * Spawn the isolated `visual-critic` subagent (`.claude/agents/visual-critic.md`).
   * Using **Playwright MCP**, open the live staging URL at **Desktop (`1440x900`)** and **Mobile (`390x844`)**.
   * Capture full-page screenshots, check browser console for JS/CSS errors, and evaluate against Supercraft’s Awwwards-grade rubric (Section 6).
5. **Stage 5 — Self-Healing Iteration Loop (Max 3 Cycles):**
   * If `visual-critic` returns `FAIL` with specific defects, the main agent patches the Elementor container settings or custom CSS via Novamira and re-triggers `visual-critic` (up to 3 loops) until it returns `PASS`.
   * Output a final build summary with the live staging preview link, components used, and any manual polish notes for Winson/Edmund.

---

## 6. Design Taste & Visual QA Guardrails (`CLAUDE.md` & `visual-critic.md`)
To prevent generic AI output, both `CLAUDE.md` and `visual-critic.md` must enforce these hard rules:

* **Banned AI Tropes:** Never generate generic 3-column boxy icon cards with thin borders, unstyled default Elementor padding (`10px` everywhere), or uninspired `Inter`/`Arial` typography pairings.
* **Typography & Rhythm:** Enforce clear visual hierarchy (`clamp()` fluid display headers, max 2–3 lines per hero headline on desktop, generous vertical section padding `96px–140px` desktop / `56px–72px` mobile).
* **Zero Mobile Regressions:** `visual-critic` must automatically `FAIL` any page exhibiting horizontal scrollbars at `390px`, overlapping text/buttons, clipped background images, or tap targets smaller than `44x44px`.
* **Clean DOM & Editor Stability:** Ensure pages open cleanly in the Elementor visual editor without JSON corruption and load with zero console errors.

---

## 7. Phased Implementation Plan for Developer

| Phase | Timeline | Key Deliverables & Validation Gate |
| :--- | :--- | :--- |
| **Phase 1: Core Connection & Benchmark** | Days 1–2 | • Set up `supercraft-wp-harness` Git repo with `CLAUDE.md` and `.mcp.json` (Playwright MCP).<br>• Install **Novamira Pro** + custom internal Elementor plugin on a Hostinger temp staging URL.<br>• Run the **3-Screenshot Validation Test** (Bento grid, Editorial typography, Custom plugin component) to verify clean Elementor JSON generation. |
| **Phase 2: Plugin Skill & Component Indexing** | Days 3–5 | • Run Novamira audit on Supercraft’s custom Elementor plugin and generate `.claude/skills/supercomponent-guide/SKILL.md`.<br>• Export and index the **top 30–50 signature components** into `library/components-index.json` + `.png` thumbnails (expand to all 200 after testing). |
| **Phase 3: `/build-page` & Visual QA Loop** | Days 6–8 | • Implement `.claude/skills/build-page/SKILL.md` and `.claude/agents/visual-critic.md`.<br>• Run 2 end-to-end test builds from real client briefs + mockup images and tune the visual-critic rubric. |
| **Phase 4: Team Rollout** | Day 9 | • Onboard Winson, Edmund, and Yin Yin via Claude Team seats + Novamira HQ/CLI.<br>• Document a 1-page team SOP (`README.md`) covering repo cloning, staging connection, and running `/build-page`. |

---

## 8. Immediate Next Action for Developer
1. Provision a blank Hostinger temporary staging WordPress site with **Elementor Pro, ACF, CPT UI, Novamira Pro, and Supercraft’s custom plugin** active.
2. Initialize the `supercraft-wp-harness` Git repository and connect **Novamira CLI** + **Playwright MCP** in Claude Code.
3. Run the **Phase 1 3-Screenshot Validation Test** and review the rendered Elementor output before indexing the full 200-component library.