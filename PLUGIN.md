# Plugin and marketplace requirements

Per-harness canonical requirements for agent plugins and marketplaces, sourced from each vendor's live documentation. See AGENTS.md for citation and scope rules governing this document.

## Status

| Harness | Spec documented | Experiment status |
| --- | --- | --- |
| Claude Code | Done | Tested (2026-08-06) — real online install from `main`: `claude plugin marketplace add microsoft/azcapman`, `claude plugin install azure-capacity-management@azcapman`. Symlinks preserved as real relative symlinks with content correctly reachable through them. Cleaned up, no residue. See "Empirical test result" under Claude Code § Plugin caching and file resolution |
| GitHub Copilot CLI | Done | Tested (2026-08-06) — real online install directly from the repo: `copilot plugin install microsoft/azcapman`. Succeeds; symlinks dereferenced into real, fully-populated directories (not symlinks, not empty). CLI itself warns direct repo installs are deprecated in favor of marketplace installs. Cleaned up, no residue. See "Empirical test result" under GitHub Copilot CLI § Install cache and symlink handling |
| Codex | Done | Tested (2026-08-06) — real online install: `codex plugin marketplace add microsoft/azcapman --ref main`, `codex plugin add azure-capacity-management@azcapman`. Required restoring `.codex-plugin/plugin.json` (missing from `main`, restored in `2601b18`) in addition to the `marketplace.json` added in `5fd7364`. Marketplace clone preserves the symlinks intact; the plugin-install cache-copy step silently drops all three, leaving the reference content completely absent with no error. See "Empirical test result" under Codex § Symlink handling |
| Azure SRE Agent | Done | Tested (2026-08-06) — marketplace registration and standalone plugin import from `microsoft/azcapman` succeeded. The importer created one skill but no tool bindings; a complete-object data-plane PATCH attached the three Azure CLI tools. The imported workspace exposed only `SKILL.md`; all three linked reference paths returned empty data. Marketplace registrations, installations, imported skills, and direct-deployment test resources were removed afterward. See Azure SRE Agent § Live data-plane verification |

## Support matrix

The matrix separates **documented** capability from this repository's **recorded online-install result**. `Unknown` means this repository hasn't tested the behavior; it doesn't mean the harness rejects it.

| Harness | Skills | Plugin subagent | MCP configuration | This repo's `references/` symlinks | Skill tool binding after plugin import |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Yes; live marketplace install loaded the skill. [Plugins reference](https://code.claude.com/docs/en/plugins-reference#skills) | Yes; live install loaded the plugin agent after removing the incompatible `agents` manifest field. [Plugins reference](https://code.claude.com/docs/en/plugins-reference#agents) | Yes. [Plugins reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers) | Preserved as working relative symlinks. | Unknown |
| GitHub Copilot CLI | Yes; live install loaded one skill. [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) | Yes; plugin agents use `*.agent.md`. [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) | Yes. [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) | Dereferenced into populated directories. | Unknown |
| Codex | Yes; live install loaded the skill. [Build skills](https://learn.chatgpt.com/docs/build-skills) | No documented plugin-agent component; `agents/openai.yaml` is skill UI metadata, not a Codex subagent. [Build skills](https://learn.chatgpt.com/docs/build-skills) | Yes. [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Dropped silently from the installed cache. | Unknown |
| Azure SRE Agent | Yes; live standalone import loaded one skill. [Skills](https://learn.microsoft.com/en-us/azure/sre-agent/skills) | No; plugins contain skills and MCP integrations, while custom agents use a separate surface. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) | Yes; plugin installation records connector requirements, and connector setup is separate. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) | Only `SKILL.md` was exposed; reads of all three linked paths returned empty data. | Not automatic: import created an empty list; complete-object PATCH bound the three Azure CLI tools. |

## Claude Code

### Marketplace manifest

- The marketplace manifest is `.claude-plugin/marketplace.json` at the repository root ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#create-the-marketplace-file)).
- Its required top-level fields are `name` as a string, `owner` as an object, and `plugins` as an array ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)).
- `owner.name` is required, and `owner.email` and `owner.url` are optional ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#owner-fields)).
- Each `plugins[]` entry requires `name` and `source` ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#plugin-entries)).
- The marketplace `name` is the public-facing identifier, must be kebab-case with no spaces, and is unique per user registration, so adding another marketplace with the same name replaces the first ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)).
- A plugin entry `name` is also public-facing and is documented as kebab-case with no spaces ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#plugin-entries)).
- Reserved marketplace names are `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `claude-plugins-community`, `claude-community`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `knowledge-work-plugins`, `life-sciences`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins`, and `healthcare`, and the page also says names that impersonate official marketplaces, such as `official-claude-plugins` or `anthropic-plugins-v2`, are blocked ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)).
- The validator warnings say Claude Desktop accepts marketplace and plugin names only when they are at most 128 characters, contain letters, digits, `.`, `_`, and `-`, and start with a letter or digit, while the same warning also says Claude Code accepts other forms and Claude Desktop managed marketplace sync rejects names that fail that check ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#troubleshooting)).
- Optional top-level marketplace fields are `$schema` as a string, `description` as a string, `version` as a string, `metadata.pluginRoot` as a string, `allowCrossMarketplaceDependenciesOn` as an array, and `renames` as an object, and the page also says `description` and `version` are accepted under `metadata` for backward compatibility ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)).

### Plugin manifest

- The default plugin manifest location is `.claude-plugin/plugin.json`, and the manifest is optional because Claude Code auto-discovers components in default locations and derives the plugin name from the directory name when the file is omitted ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- If `plugin.json` is present, `name` is the only required field ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- The manifest `name` is a unique identifier documented as kebab-case with no spaces, and the same section says a marketplace entry name overrides it for `enabledPlugins` keys and `/plugin` lookup when the marketplace lists the plugin under a different name ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- Optional metadata fields are `$schema` as a string that Claude Code ignores at load time, `displayName` as a string that falls back to `name`, `version` as a string, `description` as a string, `author` as an object, `homepage` as a string, `repository` as a string, `license` as a string, `keywords` as an array, `metadata` as an object, and `defaultEnabled` as a boolean that defaults to `true` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- The `version` field pins updates to that version string, falls back to the git commit SHA when omitted, and wins over a `version` declared in `marketplace.json` when both are set ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- Optional component and configuration fields are `skills` as a string or array, `commands` as a string or array, `agents` as a string or array, `workflows` as a string or array, `hooks` as a string, array, or object, `mcpServers` as a string, array, or object, `outputStyles` as a string or array, `lspServers` as a string, array, or object, `experimental.themes` as a string or array, `experimental.monitors` as a string or array, `userConfig` as an object, `channels` as an array, and `dependencies` as an array ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)).
- The path-behavior rules say `skills` adds to the default `skills/` scan, `commands`, `agents`, `workflows`, `outputStyles`, `experimental.themes`, and `experimental.monitors` replace their default scans, and `hooks`, `mcpServers`, and `lspServers` follow component-specific merge rules ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#path-behavior-rules)).
- All custom manifest paths must be relative to the plugin root and start with `./`, except that the `skills` field also accepts `.` and `./` for the plugin root ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#path-behavior-rules)).

### Skills

- Plugin skills load from `skills/` or `commands/` in the plugin root, and a plugin with no `skills/` directory and no `skills` manifest field loads a root `SKILL.md` as a single skill ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#skills)).
- The plugin skills example uses `skills/<skill-name>/SKILL.md`, optional supporting files such as `reference.md`, and optional subdirectories such as `scripts/`, and the skills page says each skill directory requires `SKILL.md` and treats the other files as optional supporting files ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#skills)) ([Skills](https://code.claude.com/docs/en/skills#discovery-from-parent-and-nested-directories)).
- The skills page says `SKILL.md` is configured with YAML frontmatter between `---` markers followed by Markdown content, and its frontmatter reference says all frontmatter fields are optional while `description` is recommended so Claude knows when to use the skill ([Skills](https://code.claude.com/docs/en/skills#frontmatter-reference)).
- For the root-`SKILL.md` fallback, the plugins reference says to set frontmatter `name` if you need a stable invocation name, because otherwise Claude Code falls back to the install directory name, and marketplace-installed plugins use a version-string directory name that changes on every update ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#skills)).
- A folder under a skills directory that contains `.claude-plugin/plugin.json` loads as `<name>@skills-dir`, and the skills-directory section says this source is discovered in place rather than copied into the plugin cache ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#skills-directory-plugins)).

### Agents

- Plugin agents are Markdown files under the plugin-root `agents/` directory, and the file-locations reference lists `agents/` as the default location for subagent Markdown files ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#agents)) ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#file-locations-reference)).
- Plugin agent frontmatter supports `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, and `isolation`, and the only valid `isolation` value is `"worktree"` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#agents)).
- Plugin agent frontmatter does not support `hooks`, `mcpServers`, or `permissionMode`, and the page says those fields are excluded for security reasons ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#agents)).

### Hooks

- Plugin hooks live in `hooks/hooks.json` at the plugin root or inline in the `hooks` field of `plugin.json` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#hooks)).
- The hook format is JSON that maps lifecycle event names to arrays of matcher blocks, and each block contains a `matcher` plus a `hooks` array of actions ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#hooks)).
- The documented hook action types are `command`, `http`, `mcp_tool`, `prompt`, and `agent` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#hooks)).

### MCP servers

- Plugin MCP server configuration lives in `.mcp.json` at the plugin root or inline in the `mcpServers` field of `plugin.json` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers)).
- The page describes the format as standard MCP server configuration ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers)).
- Plugin MCP servers start automatically when the plugin is enabled, and `/reload-plugins` keeps live connections for servers whose configuration is unchanged ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers)).

### LSP servers

- Plugin LSP server configuration lives in `.lsp.json` at the plugin root or inline in the `lspServers` field of `plugin.json` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#lsp-servers)).
- Each LSP server configuration requires `command` and `extensionToLanguage` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#lsp-servers)).
- Optional LSP fields are `args`, `transport`, `env`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `shutdownTimeout`, `restartOnCrash`, `maxRestarts`, and `diagnostics`, with documented defaults of `transport: "stdio"`, `restartOnCrash: true`, and `diagnostics: true` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#lsp-servers)).
- The page also says the language-server binary is not bundled with the plugin and must be installed separately ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#lsp-servers)).

### Monitors

- Monitors are an experimental component that live in `monitors/monitors.json` at the plugin root, and inline declarations use `experimental.monitors` in `plugin.json`, either as the same JSON array or as a relative path string to a non-default file ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#monitors)).
- Each monitor entry requires `name`, `command`, and `description`, and the only documented optional field is `when`, which defaults to `"always"` and also accepts `"on-skill-invoke:<skill-name>"` ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#monitors)).
- Plugin monitors run only in interactive CLI sessions, run unsandboxed at the same trust level as hooks, and are skipped on hosts where the Monitor tool is unavailable ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#monitors)).

### Plugin caching and file resolution

- The caching section distinguishes session-only plugins loaded with `claude --plugin-dir` or `claude --plugin-url` from marketplace-installed plugins, and it says marketplace plugins are copied into the local plugin cache at `~/.claude/plugins/cache` for security and verification ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- Each installed version gets its own cache directory, update or uninstall marks the previous version as orphaned, orphaned versions are removed automatically after 14 days, and Claude's Glob and Grep tools skip orphaned directories during searches ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- Installed plugins cannot reference files outside their directory, so traversals such as `../shared-utils` fail after installation because those files are not copied into the cache ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- A symlink whose target resolves within the plugin's own directory is preserved as a relative symlink in the cache ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- A symlink whose target resolves elsewhere within the same marketplace is dereferenced, and Claude Code copies the target content into the cache in place of the link ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- A symlink whose target resolves outside the marketplace is skipped for security ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- For plugins installed with `--plugin-dir` or from a local path, only symlinks whose targets resolve within the plugin's own directory are preserved, and all others are skipped ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).
- The plugin-caching section documents these cache-copy cases and the local-path rule, and it does not document any additional symlink tiers or any exception that allows out-of-plugin-directory references after installation ([Plugins reference](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).

#### Empirical test result (2026-08-06)

Real online install from `main`: `claude plugin marketplace add microsoft/azcapman` (HTTPS clone), `claude plugin install azure-capacity-management@azcapman` (user scope). The plugin root recorded in `.claude-plugin/marketplace.json` is the whole repository, not just `skills/azure-capacity-management/`, so the three symlinks in `skills/azure-capacity-management/references/` (`docs`, `scripts`, `vendor`) all resolve to targets that are within that same copied root (`docs/`, `scripts/`, `skills/vendor/`). Observed result in `~/.claude/plugins/cache/azcapman/azure-capacity-management/1.0.0/`: all three are preserved as real relative symlinks (confirmed with `find -type l` and `readlink`), and each resolves to real, populated content copied alongside them in the same cache tree (confirmed by reading a file through the symlink path). This matches the first documented tier above, not the second — "plugin's own directory" is the whole copied plugin root here, not the individual skill subfolder. Cleaned up afterward: `claude plugin uninstall`, `claude plugin marketplace remove`, and the leftover `~/.claude/plugins/cache/azcapman` / `~/.claude/plugins/marketplaces/azcapman` directories were removed manually (uninstall does not delete them).

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

#### Empirical test result (2026-08-06)

This repo's case (real symlinks nested inside a skill directory: `skills/azure-capacity-management/references/{docs,scripts,vendor}`) is exactly the undocumented gap above. Real online test: `codex plugin marketplace add microsoft/azcapman --ref main`, then `codex plugin add azure-capacity-management@azcapman`. Result was split across two stages:

- Marketplace clone (`~/.codex/.tmp/marketplaces/azcapman`): the three symlinks are preserved intact as real symlinks (`git status --short` clean, `find -type l` matches all three, `readlink` returns the original relative targets, content is reachable).
- Plugin install/cache copy (`~/.codex/plugins/cache/azcapman/azure-capacity-management/1.0.0`): the same three symlinks are **silently dropped**. `references/docs`, `references/scripts`, and `references/vendor` do not exist at all in the installed copy — not as symlinks, not as dereferenced directories, not as broken links. No error or warning is printed. The installed `SKILL.md` still references this content, so an install via `codex plugin add` silently ships a skill missing all of its reference material. Confirmed the manifest itself (`.codex-plugin/plugin.json`) also has to exist for the install to succeed at all — restored from `449cf07^` in commit `2601b18` after it was found missing from `main` (it had not been restored in PR #30, only the marketplace pointer had been added). Cleaned up afterward: `codex plugin remove`, `codex plugin marketplace remove azcapman`, confirmed no residue in `codex plugin list` / `codex plugin marketplace list`.

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

## GitHub Copilot CLI

### Plugin manifest

A GitHub Copilot CLI plugin is a directory whose root contains `plugin.json`, and it can also contain agents, skills, hooks, and MCP server configurations. [Creating a plugin for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)

The creation guide's examples use agent files in `agents/` as `NAME.agent.md` files, and skill files in `skills/NAME/` as `SKILL.md`. [Creating a plugin for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)

#### Required field

| Field | Type | Default | Description | Source |
| --- | --- | --- | --- | --- |
| `name` | string | — | Kebab-case plugin name (letters, numbers, hyphens only). Max 64 chars. Plugins that opt into Open Plugin Spec support may also use dots, for example `acme.tools`. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |

#### Optional metadata fields

| Field | Type | Default | Description | Source |
| --- | --- | --- | --- | --- |
| `$schema` | string | — | Set to the canonical Agent Plugins (Open Plugin Spec) v1.0.0 schema URL to opt into spec semantics. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `description` | string | — | Brief description. Max 1024 chars. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `version` | string | — | Semantic version, for example `1.0.0`. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `author` | object | — | `name` is required; `email` and `url` are optional. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `homepage` | string | — | Plugin homepage URL. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `repository` | string | — | Source repository URL. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `license` | string | — | License identifier, for example `MIT`. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `keywords` | string[] | — | Search keywords. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `category` | string | — | Plugin category. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `tags` | string[] | — | Additional tags. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |

#### Optional component path fields

| Field | Type | Default | Description | Source |
| --- | --- | --- | --- | --- |
| `agents` | string \| string[] | `agents/` | Path or paths to agent directories that contain `.agent.md` files. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `skills` | string \| string[] | `skills/` | Path or paths to skill directories that contain `SKILL.md` files. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `commands` | string \| string[] | — | Path or paths to command directories. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `hooks` | string \| object | — | Path to a hooks configuration file, or an inline hooks object. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `extensions` | string \| string[] \| object | — | Path or paths to extension directories. Use `{ paths: [...], exclusive: true }` to suppress built-in extensions. In Open Plugin Spec mode, this field has a different meaning. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `mcpServers` | string \| object | — | Path to an MCP configuration file, for example `.mcp.json`, or inline server definitions. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |
| `lspServers` | string \| object | — | Path to an LSP configuration file, or inline server definitions. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson) |

### Manifest search order and locations

- `.plugin/plugin.json`, `plugin.json`, `.github/plugin/plugin.json`, or `.claude-plugin/plugin.json` (checked in this order). [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#file-locations)
- `marketplace.json`, `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, or `.claude-plugin/marketplace.json` (checked in this order). [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#file-locations)

### Marketplace manifest

A plugin marketplace is recognized by `marketplace.json`, and the marketplace guide says that `marketplace.json` is the only required component of a plugin marketplace. [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)

#### Top-level fields

| Field | Type | Default | Description | Source |
| --- | --- | --- | --- | --- |
| `name` | string | — | Kebab-case marketplace name. Max 64 chars. Dots are also accepted, for example `acme.tools`, for Open Plugin Spec plugins. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `owner` | object | — | Marketplace owner info in the form `{ name, email? }`. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `plugins` | array | — | List of plugin entries. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `metadata` | object | — | Optional marketplace metadata in the form `{ description?, version?, pluginRoot? }`. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |

#### Plugin entry fields

| Field | Type | Default | Description | Source |
| --- | --- | --- | --- | --- |
| `name` | string | — | Kebab-case plugin name. Max 64 chars. Dots are also accepted for Open Plugin Spec plugins. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `source` | string \| object | — | Where to fetch the plugin, as a relative path, GitHub source, or URL source. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `description` | string | — | Plugin description. Max 1024 chars. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `version` | string | — | Plugin version. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `author` | object | — | `name` is required; `email` and `url` are optional. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `homepage` | string | — | Plugin homepage URL. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `repository` | string | — | Source repository URL. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `license` | string | — | License identifier. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `keywords` | string[] | — | Search keywords. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `category` | string | — | Plugin category. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `tags` | string[] | — | Additional tags. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `commands` | string \| string[] | — | Path or paths to command directories. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `agents` | string \| string[] | — | Path or paths to agent directories. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `skills` | string \| string[] | — | Path or paths to skill directories. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `hooks` | string \| object | — | Path to hooks configuration, or inline hooks object. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `mcpServers` | string \| object | — | MCP servers to activate when the plugin is installed, as an inline server map or a path to a JSON configuration file. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `lspServers` | string \| object | — | Path to LSP configuration, or inline server definitions. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |
| `strict` | boolean | `true` | When `true`, plugins must conform to the full schema and validation rules. When `false`, relaxed validation is used, especially for direct installs or legacy plugins. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) |

The marketplace guide says that each plugin entry's `source` path is relative to the repository root, and that `./plugins/plugin-name` and `plugins/plugin-name` resolve to the same directory. [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)

The plugin reference says that `source` can also be an object describing a GitHub repository or Git URL source, and that both `github` and `url` source types accept an optional `sha` that must be a full 40-character commit SHA. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson)

### Install specification formats

| Format | Example | Meaning | Source |
| --- | --- | --- | --- |
| Marketplace | `plugin@marketplace` | Plugin from a registered marketplace. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#plugin-specification-for-install-command) |
| GitHub | `OWNER/REPO` | Root of a GitHub repository. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#plugin-specification-for-install-command) |
| GitHub subdir | `OWNER/REPO:PATH/TO/PLUGIN` | Subdirectory in a repository. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#plugin-specification-for-install-command) |
| Git URL | `https://github.com/o/r.git` | Any Git URL. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#plugin-specification-for-install-command) |
| Local path | `./my-plugin` or `/abs/path` | Local directory. | [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#plugin-specification-for-install-command) |

### Auto-update

First-party plugins, meaning plugins installed from the built-in `copilot-plugins` and `awesome-copilot` marketplaces, automatically update at the start of each session in a trusted working directory. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#copilot-plugins-update-options)

Set `autoUpdate` to `false`, or set `COPILOT_AUTO_UPDATE=false`, to disable that session-start auto-update behavior. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#copilot-plugins-update-options)

Auto-update is skipped by default in CI. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#copilot-plugins-update-options)

A marketplace added by the user can opt into the same session-start auto-update by setting `autoUpdate: true` on its `extraKnownMarketplaces` entry in user settings, and the same reference says that repository settings and managed settings cannot enable or redirect that auto-update behavior. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#copilot-plugins-update-options)

### Open Plugin Spec support

Declaring the canonical `$schema` in `plugin.json` opts a plugin into the Agent Plugins (Open Plugin Spec) v1.0.0 format, additively on top of standard plugin loading. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#open-plugin-spec-support)

In the plugin reference tables, Open Plugin Spec support allows dots in `plugin.json` plugin names, marketplace names, and marketplace plugin-entry names in addition to the standard kebab-case forms. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

The `extensions` field description says that Open Plugin Spec mode gives `extensions` a different meaning, but the same GitHub Copilot CLI reference page does not restate that alternate meaning in the component-path table. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

The same Open Plugin Spec section documents LSP server configuration in `lsp-config/servers.json`, or through `lspServers`, and says that an LSP server definition requires `fileExtensions` and at least one of `command`, `bash`, or `powershell`. [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#open-plugin-spec-support)

### Install cache and symlink handling

The plugin creation guide says that installed plugin components are cached, that subsequent sessions read from that cache, and that local plugin changes require reinstalling the plugin to pick them up. [Creating a plugin for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)

Across the GitHub Copilot CLI pages cited in this section, no page mentions symlink handling during plugin installation or plugin caching. [Creating a plugin for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)

#### Empirical test result (2026-08-06)

Real online install directly from the GitHub repo: `copilot plugin install microsoft/azcapman`. This printed `Plugin "azure-capacity-management" installed successfully. Installed 1 skill.` plus a live deprecation warning not covered by any cited doc page: `Direct plugin installs (repos, URLs, local paths) are deprecated. Only plugin@marketplace installs will be supported in a future release.` Installed at `~/.copilot/installed-plugins/_direct/microsoft--azcapman/`. The three symlinks (`skills/azure-capacity-management/references/{docs,scripts,vendor}`) are not present as symlinks at all (`find -type l` empty); each is a real directory containing the full, real dereferenced content of its target (confirmed populated, not empty or stubbed). This is dereference-and-copy, distinct from both Claude Code's symlink-preservation result and Codex's silent-drop result. Cleaned up afterward with `copilot plugin uninstall`.

## Azure SRE Agent

### Source documents

- [Plugin Marketplace in Azure SRE Agent (Microsoft Learn; ms.date: 2026-06-02; git_commit_id: f85079a3a3df6f64ede19ec060b0fc465d43cf65)](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- [Install a plugin from a URL in Azure SRE Agent (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/sre-agent/install-plugin-from-url)
- [Custom agents in Azure SRE Agent (Microsoft Learn; ms.date: 2026-03-18; git_commit_id: 734020337b79230be3cbfc48b30b9c47aad18eca)](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)
- [Skills in Azure SRE Agent (Microsoft Learn; ms.date: 2026-03-18; git_commit_id: 734020337b79230be3cbfc48b30b9c47aad18eca)](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

### Plugin scope

Azure SRE Agent's plugin marketplace page defines a plugin as a portable, installable package of agent capabilities stored in a GitHub repository, and its component table lists only **Skills** and **MCP servers** as plugin contents. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The same table says skills add investigation runbooks, troubleshooting playbooks, and operational procedures, while MCP servers add tool integrations that configure as connectors with pre-filled endpoints and authentication. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

These three pages don't document custom agents as a plugin component; instead, the custom-agents page documents custom agents separately under **Builder > Agent Canvas**. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)

For this repository, the Azure SRE Agent package boundary is therefore the `skills/azure-capacity-management/` skill content and an optional `.mcp.json` connector declaration. `sre-agent/subagent/capacity-manager.yaml` isn't imported by marketplace or standalone plugin installation; `deploy-capacity-manager.sh` deploys it separately through the v2 `extendedAgent/agents` endpoint. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Azure SRE Agent API reference](https://learn.microsoft.com/en-us/azure/sre-agent/api-reference)

### Manifest files and conventional locations

The plugin marketplace page lists these `marketplace.json` locations, in this order. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

- `marketplace.json` (root). [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.plugin/marketplace.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.github/plugin/marketplace.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.claude-plugin/marketplace.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

For single-plugin repositories, the same page says `plugin.json` works in these locations, in this order. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

- `.plugin/plugin.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `plugin.json` (root). [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.github/plugin/plugin.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.claude-plugin/plugin.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The page's later **Marketplace formats** table maps `.github/plugin/marketplace.json` to **GitHub Copilot** and `.claude-plugin/marketplace.json` to **Other formats**. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

### `.mcp.json` resolution and formats

The plugin marketplace page says plugins that integrate with an external tool server can include an `.mcp.json` file, and plugins that only contain skills don't need that file. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The same page says `.mcp.json` is resolved from these conventional locations, in this order. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

- `.mcp.json` (root). [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.plugin/.mcp.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.github/plugin/.mcp.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `.claude-plugin/.mcp.json`. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The page says the portal supports two `.mcp.json` formats: a nested format that wraps server definitions inside `mcpServers`, and a flat format that keeps server definitions at the root. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The page also says the portal detects both formats automatically. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

An installed plugin records MCP requirements but doesn't configure its connector. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

### Version pinning and public marketplaces

The plugin marketplace page says each installation is pinned to a specific git commit, and it later says each plugin installation is pinned to the exact git commit at install time. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The same page says changes to the source repository after installation have no effect until you explicitly update. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The page lists two well-known public marketplaces: [Azure SRE Agent Plugins](https://github.com/Azure/sre-agent-plugins) and [Claude Plugins](https://github.com/anthropics/claude-plugins-official). [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The live page's only explicit cross-format naming is the **GitHub Copilot** versus **Other formats** distinction in the **Marketplace formats** table. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

### Custom-agent deployment

Custom agents aren't an Azure SRE Agent plugin component. This repository deploys its `capacity-manager` custom agent separately as an `ExtendedAgent` through `PUT /api/v2/extendedAgent/agents/{name}`; its skill uses `PUT /api/v2/extendedAgent/skills/{name}`. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Azure SRE Agent API reference](https://learn.microsoft.com/en-us/azure/sre-agent/api-reference)

### Skills and skill constraints

The skills page says a skill combines `SKILL.md`, tools, and supporting files. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The same page says to create skills in **Builder > Skills**, and it says a skill includes a `SKILL.md` file with procedural guidance and optional tool attachments for execution. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The page's example skill structure uses `name`, `description`, `files`, and `tools`. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The page says attachable tool types include Azure CLI, Kusto or Log Analytics, Python, MCP, and Link. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The skills page lists a maximum of five concurrent active skills. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The same constraints table says the oldest active skill is autounloaded when the limit is exceeded. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The same constraints table says active skills clear on conversation compaction. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The same constraints table says skill-attached tools are available only while the skill is active. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The page also says that if the agent needs a skill's tools after the skill unloads, it re-reads `SKILL.md` to reactivate the skill. [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

### Live data-plane verification

On 2026-08-06, the non-production `azcapman-sre` agent accepted a marketplace registration with `spec.sourceUrl: "microsoft/azcapman"` and transitioned it from `Cloning` to `Ready`. Item `GET` and `DELETE` worked; item `PATCH` and `PUT` returned HTTP 405. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The agent also accepted the [documented direct-install request](https://learn.microsoft.com/en-us/azure/sre-agent/install-plugin-from-url) at `POST /api/v2/plugins/install-direct` with `sourceUrl: "microsoft/azcapman"` and `pathInRepo: ""`. The importer suffixed the skill name when a direct skill with the source name already existed; after that direct skill was removed, the focused reference test imported `azure-capacity-management`. Each installation was pinned to the tested commit and recorded its source installation on the imported skill.

The importer set the imported skill's `tools` array to empty even though `SKILL.md` contains a YAML `tools` field. A full-object `PATCH /api/v2/extendedAgent/skills/{name}` then persisted `RunAzCliReadCommands`, `RunAzCliWriteCommands`, and `GetAzCliHelp`. The [skills documentation](https://learn.microsoft.com/en-us/azure/sre-agent/skills) lists those Azure CLI tools as attachable skill tools. `sre-agent/scripts/sre-agent-plugin.sh plugin-install-direct --tool <tool-name>` implements that tested post-import binding.

`DELETE /api/v2/plugins/installations/{name}` removed the imported skill. Final cleanup also removed the separately deployed skill and custom agent, and list calls confirmed no test marketplace registration, plugin installation, imported skill, direct skill, or custom agent remained.

### Symlink handling

None of these three Microsoft Learn pages mentions symlink handling for plugin content, custom-agent content, skill content, or manifest resolution. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

#### Empirical test result (2026-08-06)

After a fresh standalone installation with no colliding direct skill, the authenticated Agent Canvas file-content endpoint returned one root file, `SKILL.md`. It returned `{ "data": [] }` for `references/docs/operations/capacity-and-quotas/README.md`, `references/scripts/quota/README.md`, and `references/vendor/MANIFEST.md`. The imported Azure SRE Agent plugin workspace therefore did not contain this repository's three linked `references/` roots. `sre-agent/scripts/sre-agent-plugin.sh skill-list-files` and `skill-read-file` reproduce the root listing and individual file reads. The [skills documentation](https://learn.microsoft.com/en-us/azure/sre-agent/skills) describes supporting files as a skill component, but it doesn't describe this importer behavior.
