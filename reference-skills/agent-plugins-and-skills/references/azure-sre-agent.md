# Azure SRE Agent plugin marketplace

Source: [Plugin Marketplace in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace).
Every claim below traces to that page unless noted otherwise.

## What a plugin and a marketplace are

A plugin is a portable, installable package of agent capabilities stored in a
GitHub repository. A plugin can contain skills (investigation runbooks,
troubleshooting playbooks, operational procedures) and MCP servers (tool
integrations that configure as connectors with pre-filled endpoints and auth).

A marketplace is a GitHub repo that bundles multiple plugins under a single
`marketplace.json` manifest. Teams publish a marketplace, and other teams browse
and install from it, with each plugin installed independently and pinned to a
specific version.

## Registering and installing from a marketplace

A marketplace is registered by adding its URL under **Builder > Plugins > Add
marketplace**; the repository clones in the background, tracked by a status
banner, with a completion toast once plugins are ready to browse. Two public
marketplaces the source names by way of example: [Azure SRE Agent
Plugins](https://github.com/Azure/sre-agent-plugins) (official SRE Agent skills
and integrations) and [Claude Plugins](https://github.com/anthropics/claude-plugins-official)
(Anthropic's reference Claude plugins).

Marketplaces can also be hosted in private GitHub repos, including GitHub
Enterprise, authenticated the same way as the GitHub Connector; authentication is
configured once per marketplace and every plugin in it inherits that credential.

**Install from URL** is a separate path: installing a plugin directly from a
GitHub repo URL without registering a marketplace, useful for one-off plugins or
quick testing. It's installed as a standalone with the same version pinning and
authentication support as a marketplace install.

### Shared credential boundary for private marketplaces

The credential provided when registering a private marketplace (OAuth token, PAT,
or GitHub App) is stored at the marketplace level and shared across all installs
from it:

- Every install from that marketplace clones the repo using the stored
  credential, not the installing user's own personal GitHub identity.
- GitHub validates that the stored credential can read the repo; SRE Agent
  doesn't separately re-check each individual user's GitHub permissions at
  install time.
- SRE Agent RBAC controls who can install: any user with the **Author** or
  **Administrator** role on the agent can browse and install from any registered
  marketplace.

The source gives a concrete example of the consequence: if User A registers a
private marketplace with their own PAT, User B (who has the Author role on the
agent but no personal access to that GitHub repo) can still install plugins from
it, because the install uses User A's stored PAT — removing User B's Author role
on the agent is what prevents that.

## Version pinning

Each plugin installation is pinned to the exact git commit at install time.
Changes to the source repository after installation have no effect until an
explicit update is made.

## Manifest locations

To author a marketplace, the manifest file goes in one of these locations in the
GitHub repository:

| File path |
| --- |
| `marketplace.json` (root) |
| `.plugin/marketplace.json` |
| `.github/plugin/marketplace.json` |
| `.claude-plugin/marketplace.json` |

For single-plugin repositories, a `plugin.json` file works at the same set of
locations (`plugin.json` at root, `.plugin/plugin.json`,
`.github/plugin/plugin.json`, or `.claude-plugin/plugin.json`).

Separately, the source also describes marketplace manifests in terms of two
named formats and their file paths:

| Format | File path |
| --- | --- |
| GitHub Copilot | `.github/plugin/marketplace.json` |
| Other formats | `.claude-plugin/marketplace.json` |

## MCP server configuration for plugins

A plugin that integrates with an external tool server (the source gives Datadog,
Dynatrace, and Elasticsearch as examples) includes an `.mcp.json` file describing
the server; a plugin that only contains skills doesn't need this file. The agent
records these requirements at install time and surfaces a non-blocking
**Connector setup required** banner on the plugin's detail page when a required
server has no matching connector yet — matching is loose, associating a connector
with a plugin by URL/command (or, for legacy entries, by name), so renaming a
connector keeps the link as long as the endpoint stays the same.

`.mcp.json` resolves from the same conventional locations as the manifest file:

| File path |
| --- |
| `.mcp.json` (root) |
| `.plugin/.mcp.json` |
| `.github/plugin/.mcp.json` |
| `.claude-plugin/.mcp.json` |

Two formats are supported, and the portal detects both automatically.

**Nested format** (standard) wraps server definitions inside an `mcpServers`
object:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

**Flat format** omits the wrapper:

```json
{
  "my-server": {
    "command": "node",
    "args": ["server.js"],
    "env": { "API_KEY": "${API_KEY}" }
  }
}
```

`env` values in `.mcp.json` are placeholder references — users configure actual
secrets when setting up the connector, and the source explicitly warns never to
commit real API keys or secrets to marketplace repositories.

MCP servers are classified as **supported** (has a command for stdio, or a URL
with authentication headers) or **unsupported** (anything else — no command and
no URL-plus-headers combination).
