---
name: setup-project
description: Set up a new project folder for the Supercraft build harness — writes a project CLAUDE.md that points at the harness skill, optionally starts a local Docker WordPress with Elementor, Pro Elements, the Supercraft plugins and Novamira already active, and explains how to connect a Novamira MCP server. Use when the user wants to start a new Supercraft/Elementor build project, "set up the harness here", or spin up a local WordPress for the harness.
---

# Set up a Supercraft harness project

Base directory for this skill is shown when it loads; `scripts/` and `templates/` below are relative to it. Work in the user's current project folder unless they name another.

## 1. Ask what is needed (one question, skip what the user already said)
- **Target site:** a new **local Docker WordPress** (default), or an **existing remote site** with Novamira.
- For local: a **port** (suggest the first free one from 8892 upward; check with `lsof -nP -iTCP:<port> -sTCP:LISTEN`).

## 2. Local Docker WordPress (if chosen)
1. Make sure Docker is running (`docker info`). On this machine Docker Desktop lives at `/Volumes/T7/Applications/Docker.app` (`open -a` that path, then wait for `docker info`).
2. Run `bash <skill-dir>/scripts/setup-local-wp.sh "<project-dir>" <port>` in the background-friendly way (it can take a few minutes on first image pull).
   - It writes `docker-compose.yml`, `.env`, `apache-limits.conf`, `wp-uploads/`, adds gitignore entries, starts the containers, installs WordPress with a generated test admin saved to `.wp-local-credentials` (mode 600), activates `hello-elementor` and the 7 harness plugins, and skips Elementor onboarding.
   - Plugin source folders default to the T7 SAAS layout. If it prints `MISSING <VAR>=<path>`, find the right folder and re-run with that env var set (e.g. `ELEMENTOR_DIR=/path/to/elementor`). Elementor/Pro Elements can be copied out of any running WordPress container with `docker cp <container>:/var/www/html/wp-content/plugins/elementor <dest>`.
3. Never echo the generated password in chat; point the user to `.wp-local-credentials`.

## 3. Write the project CLAUDE.md
Copy `templates/CLAUDE.md` into the project root, filling `{{PROJECT_NAME}}`, `{{SITE_URL}}` and `{{NOVAMIRA_SERVER}}` (use "not connected yet" if unknown). If a `CLAUDE.md` already exists, append the template's sections instead of overwriting.

## 4. Novamira MCP connection
The harness builds through a Novamira MCP server for the target site. Add one to the project's `.mcp.json` (and make sure `.mcp.json` is gitignored, since it holds an application password):

```json
{
  "mcpServers": {
    "novamira-<site>": {
      "command": "npx",
      "args": ["-y", "@automattic/mcp-wordpress-remote@latest"],
      "env": {
        "WP_API_URL": "<site-url>/wp-json/mcp/novamira",
        "WP_API_USERNAME": "<wp-user>",
        "WP_API_PASSWORD": "<application-password>"
      }
    }
  }
}
```

The application password must be created by the user in WordPress (Users → Profile → Application Passwords); ask them to paste it into the file themselves rather than into chat. Alternatively the `novamira` CLI skill can operate the site directly. Restart the session after editing `.mcp.json` so the server connects.

Playwright MCP (used by `visual-critic`) ships with this plugin; no setup needed.

## 5. Report
Tell the user the site URL, where the credentials file is, which files were created, and that the next step is to share a reference screenshot or brief to build with `supercraft-harness:harness`.
