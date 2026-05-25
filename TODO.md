# Backlog

## Sprint 1: Create training decks in vbd/openwork

- [x] T-1: Create `vbd/openwork/` output folder and baseline files (FR-1–FR-5, NFR-4)
- [x] T-2: Produce kick-off overview deck (FR-1, NFR-1–NFR-3, NFR-5)
- [x] T-3: Produce forecasting deck (FR-2, NFR-1–NFR-3)
- [x] T-4: Produce allocation deck (FR-3, NFR-1–NFR-3, NFR-5)
- [x] T-5: Produce procurement deck (FR-4, NFR-1–NFR-3, NFR-5)
- [x] T-6: Produce monitoring and governance deck (FR-5, NFR-1–NFR-3, NFR-5)
- [x] T-7: QA: validate slide count and per-slide sources across all decks (TC-1–TC-3)

## Sprint 2: Create lab modules for decks 02–05

- [ ] T-8: Create lab module skeletons under `docs/operations/labs/` and add them to `docs/toc.yml` (FR-6.1–FR-6.4, NFR-6.1)
- [ ] T-9: Write lab 02 forecasting module (FR-6.1, NFR-6.2–NFR-6.5)
- [ ] T-10: Write lab 03 allocation module (FR-6.2, NFR-6.2–NFR-6.5)
- [ ] T-11: Write lab 04 procurement module (FR-6.3, NFR-6.2–NFR-6.5)
- [ ] T-12: Write lab 05 monitoring and governance module (FR-6.4, NFR-6.2–NFR-6.5)
- [ ] T-13: QA: validate citations, style, and service coverage across all lab modules (TC-6.1–TC-6.5)

## Sprint 3: Azure CLI variant of quota analysis script

- [x] T-14: Implement `scripts/quota/Get-AzVMQuotaUsageCli.ps1` (FR-7.1, FR-7.2, NFR-7.1–NFR-7.3)
  - AC-1: Script uses `az` CLI commands exclusively—no `Az` PowerShell module cmdlets
  - AC-2: Parameter block is identical to original (same names, types, defaults, help messages)
  - AC-3: CSV output format is column-identical to the original (same header string)
  - AC-4: Multi-threading via `ForEach-Object -Parallel` is preserved
  - AC-5: Physical zone mapping (`-UsePhysicalZones`) works using `az rest`
  - AC-6: Error handling follows same patterns (try/catch, colored warnings, timing)
  - AC-7: `.SYNOPSIS`, `.DESCRIPTION`, `.NOTES` updated to reference Azure CLI (not Az module)
  - AC-8: `az` JSON output correctly parsed via `ConvertFrom-Json` pipeline
  - AC-9: Auto-thread-detection uses cross-platform `[Environment]::ProcessorCount` (not WMI)
  - AC-10: (Red-team F-19) Sovereign cloud URI uses `TrimEnd('/')` to prevent malformed URL when resource manager endpoint lacks trailing slash
  - AC-11: (Red-team F-20) `$UsePhysicalZones` passed into parallel runspace via `$using:` and forwarded to `Get-QuotaDetails` as parameter
  - AC-12: (Red-team F-1/F-25) `locationInfo[0]` access guarded with `.Count -gt 0` check to prevent throw on empty array
- [x] T-15: Update `scripts/quota/README.md` with CLI variant documentation (FR-7.3)
  - AC-1: README lists the new script with Azure CLI prerequisites (`az` install + `az login`)
  - AC-2: README provides download URL and usage examples for the CLI variant
  - AC-3: "What you'll need" section updated to cover both Az module and CLI paths

Notes:
- Do not use `vbd/cowork/*.pptx` as a starting point. All decks must be created net-new under `vbd/openwork/`.

## Sprint 4: Azure SRE Agent capacity manager plugin

- [x] T-16: Create `sre-agent/` directory structure with `skill/`, `subagent/`, `knowledge/` subdirectories and setup README (FR-8, NFR-8.1, NFR-8.7)
- [x] T-17: Write SRE Agent skill manifest YAML with tool declarations for Azure CLI (FR-8.1)
- [x] T-18: Adapt SKILL.md for SRE Agent with Azure CLI procedures for quota analysis, CRG management, quota groups, and supply chain phases (FR-8.2, NFR-8.2)
- [x] T-19: Write subagent YAML definition — `capacity-manager` with system prompt, tools, handoff description, Review mode (FR-9.1, FR-9.2, NFR-8.3)
- [x] T-20: Write notification procedures in SKILL.md — Teams channel alerts and email report templates with HTML formatting (FR-10.1, FR-10.2, NFR-8.4)
- [x] T-21: Write knowledge base reference doc for quota operations — quota analysis, quota increases, region access, zonal enablement (FR-8.2)
- [x] T-22: Write knowledge base reference doc for capacity reservations and quota groups — CRG lifecycle, sharing, overallocation, quota group management (FR-8.2)
- [x] T-23: Update `README-plugin.md` to document SRE Agent as third distribution target alongside Claude Code and GitHub Copilot (NFR-8.1)
- [x] T-24: Update `.github/workflows/release.yml` to build SRE Agent plugin artifact zip (NFR-8.1)
- [x] T-25: QA: validate all SRE Agent artifacts against SRE Agent schema, AGENTS.md style, and Microsoft Learn citation requirements (TC-8.1–TC-8.6, TC-9.1–TC-9.2, TC-10.1–TC-10.2)

## Sprint 5: SRE Agent sandbox lab integration

- [x] T-26: Fork Bicep modules from azure-sre-agent-sandbox into `sre-agent/infra/bicep/` with MIT attribution (FR-11.1, NFR-11.1, NFR-11.3)
- [x] T-27: Fork deploy, destroy, validate, and RBAC scripts into `sre-agent/scripts/` (FR-11.2, FR-11.3)
- [x] T-28: Write setup guide at `sre-agent/docs/setup-guide.md` — AGENTS.md compliant (NFR-11.2, NFR-8.7)
- [x] T-29: Write capacity management prompt guide at `sre-agent/docs/prompts-guide.md` — AGENTS.md compliant (FR-12.1, NFR-11.2)
- [x] T-30: Fork dev container config into `sre-agent/.devcontainer/` (NFR-11.4)
- [x] T-31: Update `sre-agent/README.md` with automated deployment path alongside manual Builder UI (NFR-8.7)
- [x] T-32: QA: validate all Sprint 5 artifacts against AGENTS.md style, citations, and traceability (TC-11.1–TC-11.9, TC-12.1)

## Sprint 6: One-click SRE Agent deployment with azd

- [ ] T-33: Convert 5 Claude Code agent definitions to SRE Agent YAML (azuresre.ai/v2) under `sre-agent/sre-config/agents/` (FR-13.1, NFR-13.1, NFR-13.2)
- [ ] T-34: Adapt 3 skills for SRE Agent format under `sre-agent/sre-config/skills/` (FR-14.1)
- [ ] T-35: Write Kusto MCP connector YAML for FinOps Hub ADX at `sre-agent/sre-config/connectors/finops-hub-kusto.yaml` (FR-15.1)
- [ ] T-36: Write `sre-agent/scripts/post-provision.sh` — srectl init + apply all agents, skills, docs, connector (FR-16.2)
- [ ] T-37: Write `sre-agent/azure.yaml` — azd template with postprovision hook (FR-16.1)
- [ ] T-38: Add Bicep module for ADX AllDatabasesViewer role assignment to SRE Agent managed identity (FR-15.2)
- [ ] T-39: Update `sre-agent/README.md` with Deploy to Azure button and azd up instructions (FR-16.3, NFR-13.3)
- [ ] T-40: QA: validate all Sprint 6 artifacts (TC-13.1, TC-14.1, TC-15.1–TC-15.2, TC-16.1–TC-16.3)
