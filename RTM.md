# Requirements traceability matrix

## Training decks

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-1 | `vbd/openwork/01-Kickoff-Overview.pptx` | TC-1: Slide count 20–30 | Done |
| FR-1 | `vbd/openwork/01-Kickoff-Overview.pptx` | TC-2: Every slide has "Sources" in speaker notes | Done |
| FR-2 | `vbd/openwork/02-Forecasting.pptx` | TC-1: Slide count 20–30 | Done |
| FR-2 | `vbd/openwork/02-Forecasting.pptx` | TC-2: Every slide has "Sources" in speaker notes | Done |
| FR-3 | `vbd/openwork/03-Allocation.pptx` | TC-1: Slide count 20–30 | Done |
| FR-3 | `vbd/openwork/03-Allocation.pptx` | TC-2: Every slide has "Sources" in speaker notes | Done |
| FR-4 | `vbd/openwork/04-Procurement.pptx` | TC-1: Slide count 20–30 | Done |
| FR-4 | `vbd/openwork/04-Procurement.pptx` | TC-2: Every slide has "Sources" in speaker notes | Done |
| FR-5 | `vbd/openwork/05-Monitoring-Governance.pptx` | TC-1: Slide count 20–30 | Done |
| FR-5 | `vbd/openwork/05-Monitoring-Governance.pptx` | TC-2: Every slide has "Sources" in speaker notes | Done |
| NFR-3 | All five decks | TC-3: No title-case headings, and no prohibited words from AGENTS.md | Done |

## Hands-on lab modules (decks 02–05)

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-6.1 | `docs/operations/labs/lab-02-forecasting.md` | TC-6.1: Each section includes at least one Microsoft Learn citation | Not started |
| FR-6.2 | `docs/operations/labs/lab-03-allocation.md` | TC-6.2: Each section includes at least one Microsoft Learn citation | Not started |
| FR-6.3 | `docs/operations/labs/lab-04-procurement.md` | TC-6.3: Each section includes at least one Microsoft Learn citation | Not started |
| FR-6.4 | `docs/operations/labs/lab-05-monitoring-governance.md` | TC-6.4: Each section includes at least one Microsoft Learn citation | Not started |
| NFR-6.5 | All lab modules | TC-6.5: Required services and top 5 PaaS services are covered | Not started |

## Azure CLI variant of quota analysis script

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-7.1 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.1: Script contains no `Az` module cmdlets; all Azure calls use `az` CLI | Done |
| FR-7.2 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.2: Parameter block is identical to original (names, types, defaults) | Done |
| FR-7.2 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.3: CSV output columns match original exactly | Done |
| FR-7.2 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.4: Multi-threading via ForEach-Object -Parallel is preserved | Done |
| FR-7.2 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.5: Physical zone mapping (-UsePhysicalZones) works via `az rest` | Done |
| FR-7.3 | `scripts/quota/README.md` | TC-7.6: README documents CLI variant with prerequisites, examples, and download URL | Done |
| NFR-7.1 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.7: .NOTES references Azure CLI requirement, not Az module | Done |
| NFR-7.3 | `scripts/quota/Get-AzVMQuotaUsageCli.ps1` | TC-7.8: CSV header string is identical to original | Done |

## Constraints

- C-1: Decks are net-new
  - Do not copy, edit, reference, or derive content from any `vbd/cowork/*.pptx` file.

## Azure SRE Agent capacity manager plugin

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-8.1 | `sre-agent/skill/skill-manifest.yaml` | TC-8.1: Skill manifest declares `name`, `description`, `files`, and `tools` fields per SRE Agent schema | Done |
| FR-8.2 | `sre-agent/skill/SKILL.md` | TC-8.2: SKILL.md contains procedural guidance covering all four supply chain phases with Azure CLI examples | Done |
| FR-9.1 | `sre-agent/subagent/capacity-manager.yaml` | TC-9.1: Subagent YAML declares `api_version`, `kind`, `spec` with `system_prompt`, `handoff_description`, `tools`, and `agent_type: Review` | Done |
| FR-9.2 | `sre-agent/subagent/capacity-manager.yaml` | TC-9.2: Subagent tools include `RunAzCliReadCommands`, `RunAzCliWriteCommands`, and `execute_python` | Done |
| FR-10.1 | `sre-agent/skill/SKILL.md` | TC-10.1: SKILL.md includes Teams notification procedures with HTML-formatted capacity alert templates | Done |
| FR-10.2 | `sre-agent/skill/SKILL.md` | TC-10.2: SKILL.md includes email notification procedures with capacity report templates | Done |
| NFR-8.1 | `sre-agent/` | TC-8.3: All SRE Agent artifacts exist under `sre-agent/` directory | Done |
| NFR-8.3 | `sre-agent/subagent/capacity-manager.yaml` | TC-8.4: `agent_type` field is set to `Review` | Done |
| NFR-8.5 | All SRE Agent files | TC-8.5: Every procedural section includes at least one Microsoft Learn citation | Done |
| NFR-8.7 | `sre-agent/README.md` | TC-8.6: README provides step-by-step deployment instructions for Builder UI | Done |

## SRE Agent sandbox lab

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-11.1 | `sre-agent/infra/bicep/main.bicep` | TC-11.1: Bicep deploys SRE Agent, Log Analytics, and Application Insights resources | Done |
| FR-11.2 | `sre-agent/scripts/deploy.ps1` | TC-11.2: Deploy script accepts `-Location` parameter and orchestrates Bicep deployment | Done |
| FR-11.2 | `sre-agent/scripts/destroy.ps1` | TC-11.3: Destroy script removes the resource group and all resources | Done |
| FR-11.2 | `sre-agent/scripts/validate-deployment.ps1` | TC-11.4: Validate script checks SRE Agent, Log Analytics, and App Insights are healthy | Done |
| FR-11.3 | `sre-agent/scripts/configure-rbac.ps1` | TC-11.5: RBAC script assigns Reader, Contributor, and Log Analytics Reader roles | Done |
| FR-12.1 | `sre-agent/docs/prompts-guide.md` | TC-12.1: Prompt guide includes prompts for quota analysis, CRG operations, quota groups, and supply chain phases | Done |
| NFR-11.2 | `sre-agent/docs/setup-guide.md` | TC-11.6: Setup guide complies with AGENTS.md style (sentence case, contractions, no prohibited words, citations) | Done |
| NFR-11.2 | `sre-agent/docs/prompts-guide.md` | TC-11.7: Prompt guide complies with AGENTS.md style | Done |
| NFR-11.3 | `sre-agent/infra/` | TC-11.8: Bicep files include MIT license attribution comment referencing azure-sre-agent-sandbox | Done |
| NFR-11.4 | `sre-agent/.devcontainer/` | TC-11.9: Dev container configuration exists with Azure CLI and PowerShell tools | Done |

## One-click SRE Agent deployment with azd

| Requirement | Component (file) | Test case | Status |
|---|---|---|---|
| FR-13.1 | `sre-agent/sre-config/agents/*.yaml` | TC-13.1: All 5 agents use api_version azuresre.ai/v2 with spec containing instructions, handoffDescription, tools | Not started |
| FR-14.1 | `sre-agent/sre-config/skills/` | TC-14.1: All 3 skills have SKILL.md with frontmatter (name, description) | Not started |
| FR-15.1 | `sre-agent/sre-config/connectors/finops-hub-kusto.yaml` | TC-15.1: Connector YAML specifies Kusto type with managed identity | Not started |
| FR-15.2 | `sre-agent/infra/bicep/` | TC-15.2: Bicep assigns AllDatabasesViewer role at ADX server scope | Not started |
| FR-16.1 | `sre-agent/azure.yaml` | TC-16.1: azd template defines infra provider and postprovision hook | Not started |
| FR-16.2 | `sre-agent/scripts/post-provision.sh` | TC-16.2: Script runs srectl init, skill apply, agent apply, doc upload, connector apply | Not started |
| FR-16.3 | `sre-agent/README.md` | TC-16.3: README includes Deploy to Azure button with portal link | Not started |
