# Azure capacity management plugin

Plugin for Azure capacity and quota management, built for the azcapman repository. It packages for Claude Code, GitHub Copilot, and [Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview).

## Distribution targets

### Claude Code

Packages a Claude Code plugin with the `azure-capacity-manager` agent and the `azure-capacity-management` skill for operational analysis, planning, and engagement preparation.

**What's included:**
- Agent (`agents/azure-capacity-manager.md`) for quota, capacity reservation, and quota group tasks
- Skill (`skills/azure-capacity-management/SKILL.md`) for Azure capacity evidence mapped to FinOps Framework capabilities
- Plugin manifest (`.claude-plugin/plugin.json`) for the Claude Code distribution package

### GitHub Copilot

Packages the same `azure-capacity-management` skill as a standalone GitHub Copilot distribution target, so you can reuse the repository references without the Claude Code agent wrapper.

**What's included:**
- Skill (`skills/azure-capacity-management/`) with `SKILL.md` and `references/`
- Reference symlinks (`skills/azure-capacity-management/references/`) to `docs/` and `scripts/`

<!-- T-23: RTM NFR-8.1 -->
### Azure SRE Agent

The plugin also packages as an [Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview) skill and subagent for operational capacity management in production Azure environments.

**What's included:**
- Skill (`sre-agent/skill/`) that auto-activates during capacity-related incidents and attaches Azure CLI tools through [skills in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/skills)
- Subagent (`sre-agent/subagent/`) that you can invoke through `/agent capacity-manager`, and that runs in [Review mode](https://learn.microsoft.com/en-us/azure/sre-agent/sub-agents)
- Knowledge files (`sre-agent/knowledge/`) with reference docs for quota operations, capacity reservations, and quota groups, aligned with [knowledge uploads](https://learn.microsoft.com/en-us/azure/sre-agent/upload-knowledge-document)
- Deployment guide (`sre-agent/README.md`) with setup instructions for the Builder UI flow described in [skills in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/skills)

**Notifications:** Supports Teams and Outlook email notifications for capacity alerts and reports through [SRE Agent connectors](https://learn.microsoft.com/en-us/azure/sre-agent/send-notifications).

## How references work

The skill uses symlinks to reference the full repository documentation without duplication:

```
skills/azure-capacity-management/references/
  docs -> ../../../docs           # All operational docs, billing, deployment patterns
  scripts -> ../../../scripts     # PowerShell and Python tools with READMEs
```

This keeps the skill in sync with the source documentation, and avoids duplicate copies to maintain.

## Integration

### Azure CLI

The agent uses `az` commands for live Azure operations including quota queries, CRG management, AKS operations, billing, and estate enumeration. No additional tooling is required beyond an authenticated Azure CLI session, as described in [Azure CLI quota commands](https://learn.microsoft.com/en-us/cli/azure/quota?view=azure-cli-latest).

### maenifold

When available, the agent uses maenifold skills for knowledge graph operations and context engineering across conversations.

### Microsoft Docs MCP

The agent can pull the latest Microsoft Learn content through `microsoft_docs_search` and `microsoft_docs_fetch` when repository documentation doesn't cover a specific scenario.

## Repository structure

```
.claude-plugin/plugin.json                                # Claude Code plugin manifest
agents/azure-capacity-manager.md                          # Claude Code agent definition
skills/azure-capacity-management/SKILL.md                 # Shared skill definition
skills/azure-capacity-management/references/              # Symlinks to docs and scripts
sre-agent/README.md                                       # Azure SRE Agent deployment guide
sre-agent/skill/                                          # Azure SRE Agent skill package
sre-agent/subagent/                                       # Azure SRE Agent subagent package
sre-agent/knowledge/                                      # Azure SRE Agent knowledge files
```
