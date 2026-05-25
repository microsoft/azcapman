<!-- T-31: RTM NFR-8.7 -->
# Azure SRE Agent capacity manager plugin

## Overview

This plugin adds a capacity management [skill](https://learn.microsoft.com/en-us/azure/sre-agent/skills) and a `capacity-manager` [subagent](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) to [Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview). The skill supports automatic activation for quota, reservation, and capacity planning prompts, and the subagent gives you an explicit `/agent capacity-manager` handoff path in Review mode for focused investigations ([skill/skill-manifest.yaml](skill/skill-manifest.yaml), [subagent/capacity-manager.yaml](subagent/capacity-manager.yaml)).

## Quick start

Use the automated path first if you want the lab infrastructure, observability stack, and baseline RBAC configuration created through [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) and the repo scripts in one flow ([scripts/deploy.ps1](scripts/deploy.ps1), [scripts/configure-rbac.ps1](scripts/configure-rbac.ps1)).

1. Run `az login` to authenticate your Azure CLI session before you deploy the lab, as described in [Sign in with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli).
2. Run `.\sre-agent\scripts\deploy.ps1 -Location eastus2` to deploy the lab into a supported Azure SRE Agent region ([scripts/deploy.ps1](scripts/deploy.ps1), [supported regions for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions)).
3. Upload the skill and subagent through the Builder UI, then finish connector configuration by following the [setup guide](docs/setup-guide.md), which maps to the [skills](https://learn.microsoft.com/en-us/azure/sre-agent/skills), [subagents](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents), and [notifications](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications) flows in Azure SRE Agent.

## What's included

These artifacts package the plugin assets, the automation path, and the supporting docs you need for either deployment option ([Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview), [setup guide](docs/setup-guide.md)).

- `skill/`—Skill manifest and `SKILL.md` symlink to the shared capacity management skill source ([skill/skill-manifest.yaml](skill/skill-manifest.yaml), [skill/SKILL.md](skill/SKILL.md)).
- `subagent/`—`capacity-manager` subagent definition that stays in Review mode ([subagent/capacity-manager.yaml](subagent/capacity-manager.yaml), [Subagents in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)).
- `knowledge/`—Symlinks to the shared `docs/` and `scripts/` trees for knowledge uploads and operator references ([knowledge/docs](knowledge/docs), [knowledge/scripts](knowledge/scripts), [upload knowledge documents to Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/upload-knowledge-document)).
- `infra/bicep/`—Bicep templates for Azure SRE Agent, AKS, and observability resources ([infra/bicep/main.bicep](infra/bicep/main.bicep), [Bicep overview](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview)).
- `scripts/`—Deployment, delete, validation, and RBAC configuration scripts ([scripts/deploy.ps1](scripts/deploy.ps1), [scripts/destroy.ps1](scripts/destroy.ps1), [scripts/validate-deployment.ps1](scripts/validate-deployment.ps1), [scripts/configure-rbac.ps1](scripts/configure-rbac.ps1)).
- `docs/`—Setup and prompt guides for Builder upload steps and capacity workflows ([docs/setup-guide.md](docs/setup-guide.md), [docs/prompts-guide.md](docs/prompts-guide.md)).
- `.devcontainer/`—Dev container assets for a consistent deployment workspace ([.devcontainer/devcontainer.json](.devcontainer/devcontainer.json), [.devcontainer/.attribution](.devcontainer/.attribution)).

## Deployment options

Use the automated path when you need the full sandbox deployment. Use the manual path when you already have an Azure SRE Agent instance and only need to upload plugin assets through Builder ([docs/setup-guide.md](docs/setup-guide.md), [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview)).

| Path | What it covers | Best fit |
| --- | --- | --- |
| Automated | Run `deploy.ps1` to create the lab infrastructure with Bicep, then upload the skill and subagent through Builder, and configure connectors by following the [setup guide](docs/setup-guide.md) ([scripts/deploy.ps1](scripts/deploy.ps1), [Bicep overview](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview)). | Use this path for the primary end-to-end deployment flow. |
| Manual | Skip the infrastructure scripts, and use the Builder UI to upload the skill, create the Review-mode subagent, upload knowledge files, and configure Teams and Outlook connectors ([docs/setup-guide.md](docs/setup-guide.md), [skills](https://learn.microsoft.com/en-us/azure/sre-agent/skills), [subagents](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents), [Send notifications in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications)). | Use this path if your team already runs an Azure SRE Agent instance. |

## Region support

Deploy the automated lab in East US 2, Sweden Central, or Australia East, which align with the current Azure SRE Agent preview footprint described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview) and [supported regions for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions).

## Cost estimate

Plan for about $22–28 per day without Azure SRE Agent, and about $32–38 per day with Azure SRE Agent in the lab shape used by this repo ([docs/setup-guide.md](docs/setup-guide.md), [Billing for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/billing), [Azure SRE Agent pricing](https://azure.microsoft.com/en-us/pricing/details/sre-agent/)).

## Documentation

Use the repo docs for the Builder steps and day-two prompts that sit on top of the Azure SRE Agent platform docs ([Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview)).

- [Set up the capacity management lab](docs/setup-guide.md)—Automated deployment steps, Builder upload steps, connector configuration, validation, and cleanup.
- [Capacity management prompts for SRE Agent](docs/prompts-guide.md)—Prompt patterns for quota analysis, capacity reservations, quota groups, and supply chain workflows.

## Attribution

The infrastructure and supporting automation under `sre-agent/` are adapted from [azure-sre-agent-sandbox](https://github.com/matthansen0/azure-sre-agent-sandbox) under the MIT license, with repo-local attribution recorded in [.devcontainer/.attribution](.devcontainer/.attribution) and the adapted source headers in [infra/bicep/main.bicep](infra/bicep/main.bicep).
