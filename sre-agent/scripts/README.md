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

`deploy-capacity-manager.sh` creates the v2 envelopes for this repository's skill and subagent, then sends both `PUT` requests:

```bash
./sre-agent/scripts/deploy-capacity-manager.sh \
  --tenant <tenant-id> \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --agent <agent-name>
```

The Azure SRE Agent [plugin marketplace](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) imports skills and MCP integrations. The custom agent is deployed separately through the `agents` data-plane resource.
