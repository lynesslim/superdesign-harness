# supercraft-harness

Supercraft Studio's screenshot-to-Elementor build harness, packaged as a Claude Code plugin so it works in any project folder.

## What's inside
| Component | Use |
|---|---|
| `harness` skill | The mandatory build workflow: section build plan, design tokens, asset sourcing, 4-tier build ladder, Novamira Pro build rules, Elementor V3 styling rules, design guardrails, visual QA loop. |
| `setup-project` skill | Sets up a new project: project `CLAUDE.md`, optional local Docker WordPress with all harness plugins active, Novamira MCP instructions. |
| `superanimation-guide` skill | Tier 1 guide for Supercraft Animation Plugin. |
| `supercomponent-guide` skill | Tier 3 guide for SuperComponent Studio widgets. |
| `polish-design-tokens` skill | Fix only typography, spacing and colour on an existing page. |
| `visual-critic` agent | Independent visual QA at 1440px and 390px via Playwright. |
| Playwright MCP | Bundled for `visual-critic`. |

## Start a new project
In a new folder, ask Claude: "set up the Supercraft harness here" (or run `/supercraft-harness:setup-project`). Then share a reference screenshot and ask for the build.

Novamira site credentials are **not** bundled; each project adds its own Novamira server to its `.mcp.json`.

## Updating
Edit files in this folder, bump `version` in `.claude-plugin/plugin.json`, then run `claude plugin marketplace update supercraft` and `claude plugin update supercraft-harness@supercraft`.
