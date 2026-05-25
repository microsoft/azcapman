<!-- T-28: RTM NFR-11.2, NFR-8.7 -->
# Set up the capacity management lab

Use this guide to deploy the lab infrastructure, add the capacity management skill and subagent to Azure SRE Agent, configure notifications, and validate the end-to-end path described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview).

## Prerequisites

Before you deploy the lab, confirm that your team has an Azure subscription where you can create resources and assign roles for Azure SRE Agent, as described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview). Deploy the lab in East US 2, Sweden Central, or Australia East, which are the current preview regions listed in [supported regions for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions).

You'll also need the following tools installed before you run the scripts:

- Azure CLI, following [How to install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- PowerShell 7 or later, following [Installing PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell)
- Access to the Azure portal and the Builder experience described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview)

## Deploy the lab

The deployment flow uses Bicep to create the lab resources, which follows the Azure resource deployment model described in [What is Bicep?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview). For this lab, the deployment creates an Azure SRE Agent instance, a Log Analytics workspace, an Application Insights component, an AKS cluster, and Azure Managed Grafana, which gives the agent the observability and execution surfaces described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview).

1. Open PowerShell in the repo root.
2. Run the deployment script with a supported location.

   ```powershell
   ./sre-agent/scripts/deploy.ps1 -Location "East US 2"
   ```

3. Record the resource group name, the SRE Agent name, and the managed identity details that the script returns.

If your team uses one of the other supported regions, replace the location value with `Sweden Central` or `Australia East`, as listed in [supported regions for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/supported-regions).

## Configure permissions

Azure SRE Agent uses its managed identity to inspect resources, query logs, and propose or perform actions through attached tools and connectors, as described in [Connectors in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/connectors). After the deployment finishes, run the RBAC script to assign the baseline roles required for this lab.

```powershell
./sre-agent/scripts/configure-rbac.ps1
```

The script assigns the following roles for the lab scope, which align with the resource access model used by Azure SRE Agent connectors and tools in [Connectors in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/connectors):

- Reader
- Contributor
- Log Analytics Reader

If your environment uses stricter RBAC boundaries, keep the same role set, and change only the assignment scope.

## Upload the capacity management skill

Skills let Azure SRE Agent attach domain-specific instructions and tool access, as described in [Skills in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/skills). Upload the capacity management skill from the repo so the agent can activate it for quota, reservation, and capacity planning prompts.

1. Go to **Builder** > **Skills**.
2. Select the option to create or import a skill.
3. Upload `sre-agent/skill/skill-manifest.yaml`.
4. Upload `sre-agent/skill/SKILL.md` when the Builder flow asks for the skill content.
5. Save the skill, and confirm that the attached tools match the configuration described in [Skills in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/skills).

## Create the capacity-manager subagent

Subagents let you keep a focused specialist available for explicit handoff paths, which is the pattern described in [Subagents in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents). Import the capacity manager definition from this repo so platform teams can call it on demand.

1. Go to **Builder** > **Sub-agents**.
2. Select the option to create or import a subagent.
3. Upload `sre-agent/subagent/capacity-manager.yaml`.
4. Review the imported tools, permissions, and handoff description.
5. Save the subagent, and confirm that it stays in Review mode, as described in [Subagents in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents).

## Configure notifications

Azure SRE Agent can send notifications through supported connectors, including Microsoft Teams and Outlook, as described in [Send notifications in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications). Configure both connectors so the lab can send interactive alerts to Teams and summary reports through email.

1. Go to **Builder** > **Connectors**.
2. Add the Microsoft Teams connector, sign in, and select the target team and channel.
3. Add the Office 365 Outlook connector, sign in, and select the sending mailbox or account.
4. Save both connectors, and confirm that they're available to the skill and subagent flows described in [Send notifications in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).

## Validate the deployment

Before you start using the lab, validate that the core resources and agent wiring are healthy, which matches the readiness checks implied by the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview).

```powershell
./sre-agent/scripts/validate-deployment.ps1
```

Treat the deployment as ready only after the script confirms the Azure SRE Agent instance, Log Analytics workspace, and Application Insights component are healthy, and the supporting observability resources still match the deployed state described in [What is Bicep?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview).

## Clean up

When you're done with the lab, remove the deployed resources to stop further infrastructure charges. This follows the same resource lifecycle model used for Bicep-managed environments in [What is Bicep?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview).

```powershell
./sre-agent/scripts/destroy.ps1
```

If your team keeps the SRE Agent instance for follow-on testing, remove only the temporary lab resources you no longer need, and keep the remaining state aligned with the deployment model described in the [Azure SRE Agent overview](https://learn.microsoft.com/en-us/azure/sre-agent/overview).

## Cost estimate

For the lab shape in this repo, plan for about $22–28 per day without Azure SRE Agent, and about $32–38 per day with Azure SRE Agent enabled. Treat that range as a planning estimate, then compare it with the billing model in [Billing for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/billing) and the current meter details on the [Azure SRE Agent pricing page](https://azure.microsoft.com/en-us/pricing/details/sre-agent/).

The largest moving parts are the AKS cluster, the observability resources, Azure Managed Grafana, and the always-on Azure SRE Agent charge described in [Billing for Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/billing). If you change node count, region, or retention settings, recalculate the estimate before you share it with the rest of the platform team.
