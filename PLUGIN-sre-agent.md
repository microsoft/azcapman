## Azure SRE Agent

### Source documents

- [Plugin Marketplace in Azure SRE Agent (Microsoft Learn; ms.date: 2026-06-02; git_commit_id: f85079a3a3df6f64ede19ec060b0fc465d43cf65)](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- [Custom agents in Azure SRE Agent (Microsoft Learn; ms.date: 2026-03-18; git_commit_id: 734020337b79230be3cbfc48b30b9c47aad18eca)](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)
- [Skills in Azure SRE Agent (Microsoft Learn; ms.date: 2026-03-18; git_commit_id: 734020337b79230be3cbfc48b30b9c47aad18eca)](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

### Plugin scope

Azure SRE Agent's plugin marketplace page defines a plugin as a portable, installable package of agent capabilities stored in a GitHub repository, and its component table lists only **Skills** and **MCP servers** as plugin contents. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The same table says skills add investigation runbooks, troubleshooting playbooks, and operational procedures, while MCP servers add tool integrations that configure as connectors with pre-filled endpoints and authentication. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

These three pages don't document custom agents as a plugin component; instead, the custom-agents page documents custom agents separately under **Builder > Agent Canvas**. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)

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

### Version pinning and public marketplaces

The plugin marketplace page says each installation is pinned to a specific git commit, and it later says each plugin installation is pinned to the exact git commit at install time. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The same page says changes to the source repository after installation have no effect until you explicitly update. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The page lists two well-known public marketplaces: [Azure SRE Agent Plugins](https://github.com/Azure/sre-agent-plugins) and [Claude Plugins](https://github.com/anthropics/claude-plugins-official). [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

The live page's only explicit cross-format naming is the **GitHub Copilot** versus **Other formats** distinction in the **Marketplace formats** table. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)

### Custom-agent YAML and authoring surface

Across the live custom-agent examples on the custom-agents and skills pages, the documented top-level YAML fields are `name`, `system_prompt`, `handoff_description`, `tools`, `connectors`, `enable_skills`, and `allowed_skills`. [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

Both examples are flat top-level mappings, and neither page shows an `api_version` or `kind` envelope around the YAML. [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

The custom-agents page says to create custom agents in **Builder > Agent Canvas**, and its portal flow is **Agent Canvas** tab > **Create** > **Custom Agent**. [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)

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

### Symlink handling

None of these three Microsoft Learn pages mentions symlink handling for plugin content, custom-agent content, skill content, or manifest resolution. [Plugin marketplace, 2026-06-02, f85079a3a3df6f64ede19ec060b0fc465d43cf65](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Custom agents, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) [Skills, 2026-03-18, 734020337b79230be3cbfc48b30b9c47aad18eca](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

### REST deployment verification

On 2026-08-06, `sre-agent/scripts/deploy-capacity-manager.sh` deployed the
`azure-capacity-management` skill and `capacity-manager` custom agent to the
live non-production `azcapman-sre` agent through the documented v2 data plane.
The script uses `PUT /api/v2/extendedAgent/skills/{name}` and
`PUT /api/v2/extendedAgent/agents/{name}` and receives its data-plane token for
the `https://azuresre.dev` audience. [Azure SRE Agent API
reference](https://learn.microsoft.com/en-us/azure/sre-agent/api-reference)

The subsequent `GET` responses returned `Skill` and `ExtendedAgent` resources
with the expected tool lists. The skill contained 1,523 characters of
`skillContent`; the custom agent contained 1,753 characters of instructions,
enabled `azure-capacity-management`, and returned a 307-character
`handoffDescription`.

This test deployed a skill and custom agent directly. It did not validate a
plugin marketplace install. The plugin marketplace remains limited to skills and
MCP integrations, while custom agents use the separate data-plane `agents`
resource. [Plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) [Azure SRE Agent API reference](https://learn.microsoft.com/en-us/azure/sre-agent/api-reference)

### Live marketplace and plugin verification

On 2026-08-06, the non-production `azcapman-sre` agent accepted a marketplace
registration at `POST /api/v2/plugins/marketplaces` with
`metadata.name` and `spec.sourceUrl: "microsoft/azcapman"`. Its clone state changed
from `Cloning` to `Ready`. Item `GET` and `DELETE` returned the registered record and
removed it; both item `PATCH` and `PUT` returned HTTP 405. The [plugin marketplace
documentation](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
describes marketplace registration and commit-pinned plugin installations.

The same agent accepted `POST /api/v2/plugins/install-direct` with
`sourceUrl: "microsoft/azcapman"` and `pathInRepo: ""`, importing one skill under the
generated name `azure-capacity-management-azure-capacity-management`. The installation
record retained the source commit and the imported skill's
`sourcePluginInstallation` reference. The [standalone installation
documentation](https://learn.microsoft.com/en-us/azure/sre-agent/install-plugin-from-url)
documents the direct-install request shape.

The imported skill initially had an empty `tools` array, even with a `tools` YAML
front-matter field in `SKILL.md`. Sending the complete imported skill resource through
`PATCH /api/v2/extendedAgent/skills/{name}` with the three Azure CLI tools persisted
`RunAzCliReadCommands`, `RunAzCliWriteCommands`, and `GetAzCliHelp`. The
[skills documentation](https://learn.microsoft.com/en-us/azure/sre-agent/skills)
lists those Azure CLI tools as attachable skill tools. `sre-agent-plugin.sh` performs
that post-install PATCH when invoked with `--tool`.

`DELETE /api/v2/plugins/installations/{name}` removed the installation and caused its
imported skill to return HTTP 404. The final test cleanup deleted the separately
deployed `azure-capacity-management` skill and `capacity-manager` custom agent, then
confirmed that the skills, agents, plugin-installation, and marketplace-registration
lists contained none of the test resources. This test did not validate a
marketplace-selected plugin installation because the current REST documentation
exposes marketplace registration and listing but not a marketplace-install request.
