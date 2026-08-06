# Claude Code plugin marketplaces

Source: [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).
Every claim below traces to that page unless noted otherwise.

## Two manifests, two locations

A Claude Code plugin distribution involves two separate JSON files:

- **`marketplace.json`**, the catalog. It goes in `.claude-plugin/marketplace.json` at
  the repository root and lists the plugins the marketplace makes available, along
  with where to fetch each one.
- **`plugin.json`**, the per-plugin manifest. It goes in `.claude-plugin/plugin.json`
  inside each individual plugin's own directory and describes that one plugin (name,
  description, version, author, and component configuration).

The example marketplace repository layout is:

```
my-marketplace/.claude-plugin/marketplace.json
my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json
my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md
```

## `marketplace.json` schema

Required top-level fields:

| Field     | Type   | Notes |
| :-------- | :----- | :---- |
| `name`    | string | Marketplace identifier, kebab-case, no spaces. It's public-facing — users see it in install commands such as `/plugin install my-tool@your-marketplace`. Each user can register only one marketplace per name; adding a second marketplace under the same name replaces the first. |
| `owner`   | object | Marketplace maintainer info: `name` (required), `email` and `url` (optional). |
| `plugins` | array  | The list of available plugins. |

A set of marketplace names is reserved for Anthropic's own official use (for
example, `claude-code-marketplace`, `claude-plugins-official`, `agent-skills`,
`anthropic-marketplace`) and can't be used by third-party marketplaces; names that
impersonate an official one, such as `official-claude-plugins`, are also blocked.
Claude Code re-checks reserved names every time it loads a marketplace, not only
when a user adds one, so a marketplace registered under a name that later becomes
reserved stops loading.

Optional top-level fields include `$schema` (ignored at load time, only used for
editor autocomplete), `description`, `version`, `metadata.pluginRoot` (a base
directory prepended to relative plugin source paths, so `"source": "formatter"`
can stand in for `"source": "./plugins/formatter"`), `allowCrossMarketplaceDependenciesOn`
(an array naming other marketplaces this marketplace's plugins may depend on —
dependencies on a marketplace not listed here are blocked at install time), and
`renames` (a map from a former plugin `name` to its current name, or to `null` if
the plugin was removed, so existing users migrate automatically; this field
requires Claude Code v2.1.193 or later).

## Plugin entries inside `marketplace.json`

Each entry in the `plugins` array can include any field from the plugin manifest
schema (`description`, `version`, `author`, `commands`, `hooks`, and so on), plus
marketplace-specific fields: `source`, `category`, `tags`, `strict`, and
`relevance`.

Required per entry:

| Field    | Type           | Notes |
| :------- | :------------- | :---- |
| `name`   | string         | Plugin identifier, kebab-case, no spaces — public-facing in install commands. |
| `source` | string\|object | Where to fetch the plugin from (see below). |

Other optional per-entry fields worth noting: `displayName` (a human-readable name
for UI, falling back to `name`; requires v2.1.143+), `version` (pins the plugin to
a fixed version string — omit it to fall back to the git commit SHA), `strict`
(boolean, default `true`, controls whether `plugin.json` is the sole authority for
component definitions), and `defaultEnabled` (boolean, default `true`; set to
`false` to install the plugin disabled until the user opts in — this field on the
marketplace entry takes precedence over the same field in the plugin's own
`plugin.json`, and requires v2.1.154+).

### Plugin component configuration fields

The plugin manifest schema (referenced from plugin entries and from `plugin.json`
itself) exposes these fields for declaring where a plugin's components live:

| Field        | Type           | Description |
| :----------- | :------------- | :---------- |
| `skills`     | string\|array  | Custom paths to skill directories, each containing `<name>/SKILL.md`. |
| `commands`   | string\|array  | Custom paths to flat `.md` skill files or directories. |
| `agents`     | string\|array  | Custom paths to agent files. |
| `hooks`      | string\|object | Custom hooks configuration, or a path to a hooks file. |
| `mcpServers` | string\|object | MCP server configurations, or a path to an MCP config file. |
| `lspServers` | string\|object | LSP server configurations, or a path to an LSP config file. |

If a plugin doesn't set `skills`, the default discovery convention is
`skills/<name>/SKILL.md` inside the plugin's own directory (as shown in the
walkthrough example above).

## Plugin sources

The `source` field on a plugin entry tells Claude Code where to fetch that plugin
from. After fetching, Claude Code copies the plugin into a local versioned cache at
`~/.claude/plugins/cache`.

| Source        | Shape                              | Fields                             | Notes |
| :------------ | :---------------------------------- | :---------------------------------- | :---- |
| Relative path | string, e.g. `"./my-plugin"`        | none                                | Must start with `./`. Resolves relative to the marketplace root (the directory containing `.claude-plugin/`), not to the `.claude-plugin/` directory itself. `../` is not allowed. |
| `github`      | object                              | `repo` (required), `ref?`, `sha?`   | `repo` is `owner/repo`. |
| `url`         | object                              | `url` (required), `ref?`, `sha?`    | Full git URL, `https://` or `git@`; the `.git` suffix is optional. |
| `git-subdir`  | object                              | `url`, `path`, `ref?`, `sha?`       | Points at a subdirectory inside a git repo; uses a sparse, partial clone so only that subdirectory is fetched. |
| `npm`         | object                              | `package`, `version?`, `registry?` | Installed via `npm install`. |

For the git-based source types (`github`, `url`, `git-subdir`), when both `ref`
(branch or tag) and `sha` (a full 40-character commit SHA) are set, `sha` is the
effective pin — Claude Code fetches and checks out that exact commit. On most git
hosts (GitHub, GitLab, Bitbucket) this means installation still succeeds even if
the branch or tag named by `ref` is later deleted, as long as the commit is still
reachable. Some hosts, such as AWS CodeCommit, don't support fetching by SHA
directly, so on those hosts the named `ref` must still exist and the pinned commit
must be reachable from it.

Marketplace sources (where the `marketplace.json` catalog itself is fetched from,
set via `/plugin marketplace add` or the `extraKnownMarketplaces` setting) and
plugin sources (the `source` field on each plugin entry) are distinct and pinned
independently: a marketplace source supports `ref` but not `sha`, while a plugin
source supports both.

## Namespacing, install, and updates

Plugin components are namespaced by the plugin's own name — for example, the
`quality-review` skill inside `quality-review-plugin` is invoked as
`/quality-review-plugin:quality-review`. Users add a marketplace with
`/plugin marketplace add <path-or-source>` and install a specific plugin with
`/plugin install <plugin-name>@<marketplace-name>`. Marketplace maintainers update
their catalog by pushing changes to the hosting repository; users pull those
changes into their local copy with `/plugin marketplace update`.

## Cache constraint: no `../` references, use symlinks

Because Claude Code copies each installed plugin directory into a cache location,
a plugin can't reference files outside its own directory with a path such as
`../shared-utils` — those files aren't copied along with it. Marketplace and
plugin authors who need to share files across multiple plugins in the same
repository need to use symlinks instead.
