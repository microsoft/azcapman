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
