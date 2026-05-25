# Product requirements

## Training decks for Azure quota and capacity management

### Summary

Create a set of five training decks based on the content in this repository. The intended audience is SaaS ISVs operating workloads in ISV-owned Azure subscriptions. The decks must explain, peer-to-peer, how ISVs can use Azure estate-level controls to manage quota, capacity, and deployment stamps. Content must align with the voice, scope, and terminology in AGENTS.md.

### Functional requirements

- FR-1: Kick-off overview deck
  - The system shall provide a kick-off deck that introduces the training series, the audience, the scope boundaries, and the five-deck structure.

- FR-2: Planning and forecasting deck
  - The system shall provide a Planning & Estimating and Forecasting deck that explains how capacity estimates and forecasts feed quota, reservations, and release gates.

- FR-3: Workload placement deck
  - The system shall provide an Architecting & Workload Placement deck that explains region access, zonal enablement, per-subscription quota constraints, and quota groups.

- FR-4: Usage and rate optimization deck
  - The system shall provide a Usage Optimization and Rate Optimization deck that explains capacity reservation groups, sharing constraints, and how capacity guarantees interact with billing constructs.

- FR-5: Governance and automation deck
  - The system shall provide a Governance, Policy & Risk and Automation, Tools & Services deck that explains quota alerts, reservation monitoring, budget signals, and CI/CD capacity gates.

### Non-functional requirements

- NFR-1: Slide count
  - Each deck shall contain 20–30 slides.

- NFR-2: Citations
  - Each slide shall include at least one citation to an authoritative source, preferring Microsoft Learn. Use a consistent format in speaker notes: a final section named "Sources" with URL links.

- NFR-2.1: Speaker notes
  - Each slide shall include speaker notes that provide a talk track for presenters. Use a consistent structure in speaker notes:
    - Key points
    - Talk track
    - Sources

- NFR-3: Microsoft style and AGENTS.md compliance
  - Deck content shall follow sentence-style capitalization, direct technical tone, and the word-choice rules in AGENTS.md and the Microsoft Writing Style Guide.

- NFR-4: Output location
  - The decks shall be saved under `vbd/openwork/`.

- NFR-5: Starting points
  - The decks must be net-new. Do not copy, edit, reference, or derive content from any existing PowerPoint files under `vbd/`.

- NFR-7: Cowork folder is off limits
  - Content under `vbd/cowork/` is off limits. Do not open, copy, edit, or use it as a source for decks.

- NFR-6: Audience alignment
  - Content shall be written for ISV platform teams. Remove references to Microsoft field personas (for example, SE, CSAM, and CSA), and avoid implying Microsoft-run processes outside of what Azure enforces.

## Hands-on lab modules for decks 02–05

### Summary

Create a set of hands-on lab modules that pair with decks 02–05 (planning and forecasting, workload placement, usage and rate optimization, and governance and automation). The labs must show how to use Azure estate-level controls and surfaces (portal, CLI, ARM, REST) so ISV platform teams can validate behaviors and failure modes.

### Functional requirements

- FR-6.1: Planning and forecasting lab
  - The system shall provide a planning and forecasting lab that walks through building a capacity-and-limits inventory across compute and selected PaaS services, and producing a forecast-ready dataset.

- FR-6.2: Workload placement lab
  - The system shall provide a workload placement lab that walks through validating region access, zonal enablement, per-subscription quota constraints, and quota groups for compute.

- FR-6.3: Usage and rate optimization lab
  - The system shall provide a usage and rate optimization lab that walks through creating and operating capacity reservation groups, including sharing constraints and zone-mapping considerations.

- FR-6.4: Governance and automation lab
  - The system shall provide a governance and automation lab that walks through turning on quota monitoring, creating quota alerts, and deploying budget and anomaly-alert guardrails using the scripts in this repository.

### Non-functional requirements

- NFR-6.1: Output location
  - The lab modules shall be saved under `docs/operations/labs/` and surfaced in `docs/toc.yml`.

- NFR-6.2: Citations
  - Each lab section shall include citations to authoritative sources, preferring Microsoft Learn.

- NFR-6.3: Microsoft style and AGENTS.md compliance
  - Lab content shall follow sentence-style capitalization, direct technical tone, and the word-choice rules in AGENTS.md and the Microsoft Writing Style Guide.

- NFR-6.4: Script constraints
  - The labs shall not introduce new scripts. When the labs require automation, they shall reference only scripts that already exist in this repository and/or link to official Microsoft Learn procedures.

- NFR-6.5: Service coverage
  - The labs shall include guidance for, at minimum, Premium SSD v2, Azure App Service, Azure Database for PostgreSQL, Azure Database for MySQL, and Azure SQL Managed Instance.
  - The labs shall also cover five additional Azure PaaS services: Azure Storage, Azure Cosmos DB, Azure Service Bus, Azure Key Vault, and Azure Event Hubs.

### Constraints

- C-2: Cowork folder is off limits
  - Content under `vbd/cowork/` is off limits. Do not open, copy, edit, or use it as a source for lab modules.

## Azure CLI variant of quota analysis script

### Summary

Create an Azure CLI variant of the multi-threaded VM quota analysis script (`Get-AzVMQuotaUsage.ps1`) so ISV platform teams can run quota analysis without installing the Azure PowerShell module. The new script lives alongside the original and uses `az` CLI commands exclusively.

### Functional requirements

- FR-7: Azure CLI quota analysis script
  - FR-7.1: The system shall provide a PowerShell script (`Get-AzVMQuotaUsageCli.ps1`) that replaces all Azure PowerShell module cmdlets in `Get-AzVMQuotaUsage.ps1` with Azure CLI equivalents.
  - FR-7.2: The CLI variant shall preserve identical parameter interfaces, CSV output format, multi-threading support, and physical zone mapping feature.
  - FR-7.3: The README.md in `scripts/quota/` shall document the CLI variant with prerequisites, usage examples, and download instructions.

### Non-functional requirements

- NFR-7.1: The CLI variant shall require only Azure CLI (`az`) and PowerShell 7+—no Azure PowerShell module dependency.
- NFR-7.2: The CLI variant shall follow the same code structure, commenting style, and documentation conventions as the original.
- NFR-7.3: The CLI variant shall produce CSV output that is column-identical to the original script's output.

## Azure SRE Agent capacity manager plugin

### Summary

Create an [Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview) plugin that provides a capacity management [skill](https://learn.microsoft.com/en-us/azure/sre-agent/skills) and [subagent](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) for SaaS ISVs. The skill auto-activates during capacity-related incidents. The subagent provides on-demand capacity analysis via `/agent capacity-manager`. Both support [notifications](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications) to Microsoft Teams and Outlook email.

### Functional requirements

- FR-8: SRE Agent skill
  - FR-8.1: The system shall provide an SRE Agent [skill manifest](https://learn.microsoft.com/en-us/azure/sre-agent/skills) (YAML) that declares tool attachments (`RunAzCliReadCommands`, `RunAzCliWriteCommands`, `GetAzCliHelp`) and activation conditions for capacity management topics.
  - FR-8.2: The system shall provide a SKILL.md with procedural guidance for quota analysis, capacity reservation management, quota group operations, and Azure capacity evidence mapped to FinOps Framework capabilities, reusing content from the existing `azure-capacity-management` skill.

- FR-9: SRE Agent subagent
  - FR-9.1: The system shall provide a [subagent YAML definition](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) (`capacity-manager`) with system prompt, tool declarations, handoff description, and `Review` mode permissions.
  - FR-9.2: The subagent shall support Azure capacity evidence for Planning & Estimating, Forecasting, Architecting & Workload Placement, Usage Optimization, Rate Optimization, Governance, Policy & Risk, and Automation, Tools & Services via Azure CLI tools and Azure Resource Graph queries.

- FR-10: Notifications
  - FR-10.1: The skill and subagent shall include procedures for sending capacity alerts and reports to a configured [Microsoft Teams channel](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).
  - FR-10.2: The skill and subagent shall include procedures for sending capacity reports and recommendations via [Outlook email](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).

### Non-functional requirements

- NFR-8.1: SRE Agent artifacts shall live under `sre-agent/` in the repository root.
- NFR-8.2: SKILL.md content shall reuse existing `azure-capacity-management` skill content where applicable, adapted for SRE Agent's Azure CLI-based runtime.
- NFR-8.3: The subagent shall use `Review` [agent type](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) (proposes actions, requires human approval for write operations).
- NFR-8.4: Notification templates shall follow AGENTS.md style guide and use HTML format for Teams messages.
- NFR-8.5: All SRE Agent artifacts shall include [Microsoft Learn](https://learn.microsoft.com/) citations per AGENTS.md requirements.
- NFR-8.6: The plugin shall not require a custom MCP server—it shall use SRE Agent's [built-in tools](https://learn.microsoft.com/en-us/azure/sre-agent/tools) (Azure CLI, Resource Graph, Python code interpreter).
- NFR-8.7: A setup guide shall document how to deploy the skill, subagent, and connectors to an SRE Agent instance via the [Builder UI](https://learn.microsoft.com/en-us/azure/sre-agent/skills).

## SRE Agent sandbox lab

### Summary

Integrate the [azure-sre-agent-sandbox](https://github.com/matthansen0/azure-sre-agent-sandbox) infrastructure into this repository so ISV platform teams can deploy a complete SRE Agent instance with the capacity management skill and subagent using a single command. Includes Bicep IaC, deployment scripts, a setup guide, and a capacity management prompt guide.

### Functional requirements

- FR-11: Automated SRE Agent deployment
  - FR-11.1: The system shall provide [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) templates that deploy an SRE Agent instance, Log Analytics workspace, and Application Insights in a supported region.
  - FR-11.2: The system shall provide PowerShell deployment scripts (`deploy.ps1`, `destroy.ps1`, `validate-deployment.ps1`) that orchestrate the Bicep deployment and post-deployment configuration.
  - FR-11.3: The system shall provide an RBAC configuration script that grants the SRE Agent managed identity the permissions needed for capacity management operations.

- FR-12: Capacity management prompt guide
  - FR-12.1: The system shall provide a prompt guide with example prompts for quota analysis, capacity reservation operations, quota group management, and FinOps capability mapping.

### Non-functional requirements

- NFR-11.1: All sandbox artifacts shall live under `sre-agent/` in the repository.
- NFR-11.2: All Markdown content shall comply with AGENTS.md style requirements.
- NFR-11.3: Infrastructure code shall be adapted from [azure-sre-agent-sandbox](https://github.com/matthansen0/azure-sre-agent-sandbox) (MIT license) with attribution.
- NFR-11.4: A dev container configuration shall provide a consistent deployment experience.

## One-click SRE Agent deployment with azd

### Summary

Package all 5 subagents, 3 skills, knowledge docs, and a Kusto MCP connector as an [Azure Developer CLI (azd)](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview) template. Customers run `azd up` to deploy a fully configured SRE Agent instance that connects to their FinOps Hub.

### Functional requirements

- FR-13: Agent YAML conversion
  - FR-13.1: The system shall provide 5 subagent definitions in [SRE Agent YAML format](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents) (`api_version: azuresre.ai/v2`): `azure-capacity-manager`, `chief-financial-officer`, `finops-practitioner`, `ftk-database-query`, `ftk-hubs-agent`.

- FR-14: Skill packaging
  - FR-14.1: The system shall provide 3 skills adapted for SRE Agent: `azure-capacity-management`, `azure-cost-management`, `finops-toolkit`.

- FR-15: Kusto MCP connector
  - FR-15.1: The system shall provide a Kusto MCP connector YAML that connects to a customer's FinOps Hub ADX cluster using the SRE Agent's managed identity.
  - FR-15.2: The Bicep deployment shall assign `AllDatabasesViewer` at the ADX server scope to the SRE Agent managed identity.

- FR-16: Automated deployment
  - FR-16.1: The system shall provide an `azure.yaml` template that deploys the full stack via `azd up`.
  - FR-16.2: The system shall provide a `post-provision.sh` script that runs `srectl init`, uploads skills and knowledge docs, and applies all agent and connector YAML as an azd `postprovision` hook.
  - FR-16.3: The README shall include a "Deploy to Azure" button that links to the Azure Portal custom deployment UI.

### Non-functional requirements

- NFR-13.1: Agent YAML shall use `##param##` parameter format and include `target: dictionary:args:string` for all parameters.
- NFR-13.2: All SRE Agent YAML shall follow the [azuresre.ai/v2 schema](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents).
- NFR-13.3: All documentation shall comply with AGENTS.md style requirements.
