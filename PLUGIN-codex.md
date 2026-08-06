## Codex

### Skill structure

A Codex skill is a directory with a `SKILL.md` file, and the `SKILL.md` file must include `name` and `description` in front matter. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The documented skill tree shows `scripts/`, `references/`, `assets/`, and `agents/openai.yaml` as optional directories or files alongside `SKILL.md`. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The manual `SKILL.md` example uses this front matter. [Build skills](https://learn.chatgpt.com/docs/build-skills)

```md
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---
```

The page says `agents/openai.yaml` can configure ChatGPT desktop app UI metadata, invocation policy, and tool dependencies. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The documented `interface` example includes `display_name`, `short_description`, `icon_small`, `icon_large`, `brand_color`, and `default_prompt`. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The documented `policy` example uses `allow_implicit_invocation`, and the page states its default is `true`; when the value is `false`, Codex won't implicitly invoke the skill, but explicit `$skill` invocation still works. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The documented `dependencies.tools` example is a list of records with `type`, `value`, `description`, `transport`, and `url`. [Build skills](https://learn.chatgpt.com/docs/build-skills)

### Skill discovery

Codex reads skills from repository, user, admin, and system locations, and for repositories it scans `.agents/skills` in every directory from the current working directory up to the repository root. [Build skills](https://learn.chatgpt.com/docs/build-skills)

| Scope | Documented location | Documented note |
| --- | --- | --- |
| `REPO` | `$CWD/.agents/skills` | Current working directory: where you launch Codex. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |
| `REPO` | `$CWD/../.agents/skills` | A folder above CWD when you launch Codex inside a Git repository. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |
| `REPO` | `$REPO_ROOT/.agents/skills` | The topmost root folder when you launch Codex inside a Git repository. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |
| `USER` | `$HOME/.agents/skills` | Any skills checked into the user's personal folder. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |
| `ADMIN` | `/etc/codex/skills` | Any skills checked into the machine or container in a shared, system location. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |
| `SYSTEM` | Bundled with Codex by OpenAI | The table does not list a filesystem path for this scope. ([Build skills](https://learn.chatgpt.com/docs/build-skills)) |

### Symlink handling

> "Codex supports symlinked skill folders and follows the symlink target when scanning these locations." ([Build skills](https://learn.chatgpt.com/docs/build-skills))

The documented wording is limited to symlinked skill folders while Codex scans the listed skill locations. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The page does not add a separate statement about symlinked files inside a skill directory. [Build skills](https://learn.chatgpt.com/docs/build-skills)

### Plugin and marketplace packaging

The plugin packaging page says packaging assembles skills and, when needed, an MCP server into the plugin people will install. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

Every plugin has a `.codex-plugin/plugin.json` manifest. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

Depending on the plugin's architecture, the folder can also include a `skills/` directory, an `.app.json` file for a registered MCP server connection, an `.mcp.json` file for a bundled MCP server, and optional assets and lifecycle hooks. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The plugin structure section says only `plugin.json` belongs inside `.codex-plugin/`, while `skills/`, `hooks/`, `assets/`, `.mcp.json`, and `.app.json` stay at the plugin root. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The skills page says plugins can include one or more skills, and it says plugins can also bundle registered MCP server connections, bundled MCP server configuration, and presentation assets in one package. [Build skills](https://learn.chatgpt.com/docs/build-skills)

The plugin page documents these top-level plugin manifest fields: `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `skills`, `mcpServers`, `apps`, `hooks`, and `interface`; it also says `.codex-plugin/plugin.json` is the required entry point, while the other manifest fields are optional. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The page documents repo and personal marketplace files at `$REPO_ROOT/.agents/plugins/marketplace.json` and `~/.agents/plugins/marketplace.json`. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The page defines a marketplace as a JSON catalog of plugins, and its example uses one object per plugin under `plugins`. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

In the documented marketplace format, the top-level `name` identifies the marketplace, `interface.displayName` sets the marketplace title, each plugin entry points at its source under `source`, and each plugin entry includes `policy.installation`, `policy.authentication`, and `category`. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

For local marketplace entries, the page says `source.path` stays relative to the marketplace root, starts with `./`, and stays inside that root, and it also allows a plain string path instead of an object for local sources. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The page also documents Git-backed plugin sources with `source: "url"` or `source: "git-subdir"`, and JavaScript package registry sources with `source: "npm"`, `package`, optional `version`, and optional `registry`. [Package your plugin](https://developers.openai.com/plugins/build/plugins)

The page documents `.codex-plugin/plugin.json` and `marketplace.json` through example JSON and field descriptions, and it does not publish a separate machine-readable JSON Schema on the page. [Package your plugin](https://developers.openai.com/plugins/build/plugins)
