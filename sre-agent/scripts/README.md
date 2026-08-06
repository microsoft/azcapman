# Azure SRE Agent REST helpers

These scripts call the Azure SRE Agent v2 data plane documented in the [Azure SRE Agent API reference](https://learn.microsoft.com/en-us/azure/sre-agent/api-reference). They require Azure CLI, `curl`, `python3`, and a signed-in Azure CLI identity.

`sre-agent-rest.sh` verifies that the supplied subscription belongs to the supplied tenant, obtains `properties.agentEndpoint` from the `Microsoft.App/agents` resource, requests a `https://azuresre.dev` bearer token, and sends one data-plane request.

```bash
./sre-agent/scripts/sre-agent-rest.sh list \
  --tenant <tenant-id> \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --agent <agent-name> \
  --kind skills
```

Use `--kind` for `/api/v2/extendedAgent/<kind>` resources. Use `--path` for other documented data-plane paths, such as `/api/v2/plugins/marketplaces` and `/api/v2/plugins/installations`.

`sre-agent-plugin.sh` covers the tested plugin lifecycle. The [plugin marketplace documentation](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) describes marketplace registration, and [Install a plugin from a URL](https://learn.microsoft.com/en-us/azure/sre-agent/install-plugin-from-url) documents direct installation with `sourceUrl` and `pathInRepo`.

```bash
./sre-agent/scripts/sre-agent-plugin.sh marketplace-add \
  --tenant <tenant-id> \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --agent <agent-name> \
  --name <marketplace-name> \
  --source-url microsoft/azcapman

./sre-agent/scripts/sre-agent-plugin.sh plugin-install-direct \
  --tenant <tenant-id> \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --agent <agent-name> \
  --source-url microsoft/azcapman \
  --tool RunAzCliReadCommands \
  --tool RunAzCliWriteCommands \
  --tool GetAzCliHelp
```

The direct-install endpoint imports the skill without tool bindings in the tested service. `plugin-install-direct` reads each imported skill and sends the complete resource through `PATCH` with the supplied tool list. The [skills documentation](https://learn.microsoft.com/en-us/azure/sre-agent/skills) identifies Azure CLI tools as attachable skill tools. `marketplace-get`, `marketplace-delete`, `plugin-get`, `plugin-delete`, and the two `*-list` commands read or remove the returned resource names. The tested marketplace item endpoint returns `405` for both `PATCH` and `PUT`, so the helper doesn't expose an update command.

`deploy-capacity-manager.sh` creates the v2 envelopes for this repository's skill and subagent, then sends both `PUT` requests:

```bash
./sre-agent/scripts/deploy-capacity-manager.sh \
  --tenant <tenant-id> \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --agent <agent-name>
```

The Azure SRE Agent [plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) imports skills and MCP integrations. The custom agent is deployed separately through the `agents` data-plane resource.
