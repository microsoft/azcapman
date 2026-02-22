# Azure Capacity Manager — VS Code extension

A GitHub Copilot Chat participant that brings Azure capacity, quota, and reservation expertise into \
VS Code — no local copy of the azcapman repository required.

Invoke with `@azure-capacity-manager` in any Copilot Chat conversation.

## What it does

The `@azure-capacity-manager` participant embeds the full azcapman domain knowledge as a bundled \
system prompt. It covers the complete capacity supply chain for SaaS ISVs operating workloads in \
ISV-owned Azure subscriptions under EA or MCA:

| Step | Coverage |
|------|---------|
| Forecast | Demand modeling, scale unit sizing, FinOps budget alignment |
| Procure | Region access, zonal enablement, quota increases, quota groups |
| Allocate | Capacity reservation group design, cross-subscription sharing, overallocation |
| Monitor | Quota alerts, budget alerts, anomaly detection, governance cadence |

## Slash commands

| Command | Use for |
|---------|---------|
| `/quota` | Quota analysis, increases, region/zone access workflows |
| `/reservation` | CRG design, cost modeling, sharing, overallocation |
| `/quotagroup` | Quota group architecture, ARM lifecycle, transfers |
| `/diagnose` | AKS scaling failures, quota blocks, capacity errors |
| `/workshop` | ISV capacity governance workshop preparation |

## Examples

```
@azure-capacity-manager Run a quota analysis for Standard_D16s_v5 in East US 2 across our subscriptions

@azure-capacity-manager /reservation Should we create a CRG for Standard_D16s_v5 in East US 2 zone 1?

@azure-capacity-manager /quotagroup Design a quota group strategy for 50 subscriptions across 3 management groups

@azure-capacity-manager /diagnose Our AKS node pool can't scale in East US zone 2 — what's blocking it?

@azure-capacity-manager /workshop Prepare materials for a capacity governance workshop with Contoso
```

## Requirements

- VS Code 1.95 or later
- GitHub Copilot extension installed and authenticated

## Build and install

```bash
cd vscode-extension
npm install
npm run package      # produces azure-capacity-manager-1.0.0.vsix
```

Install the `.vsix`:

```bash
code --install-extension azure-capacity-manager-1.0.0.vsix
```

Or drag the `.vsix` into the VS Code Extensions view.

## Publish to VS Code Marketplace

1. Create a publisher at https://marketplace.visualstudio.com/manage
2. Update `publisher` in `package.json`
3. `npx vsce publish`

## Reference documentation

Full operational documentation is at https://msbrett.github.io/azcapman/ — the participant cites \
these pages in every response.

Source repository: https://github.com/msbrett/azcapman
