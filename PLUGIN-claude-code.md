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
