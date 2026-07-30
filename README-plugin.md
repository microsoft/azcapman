# Azure capacity management plugin

This repository packages its Azure capacity and quota content as an installable plugin
for five agentic harnesses. The skill content is authored once, in
`skills/azure-capacity-management/`, and every harness reads that same file.

## How one skill serves every target

`SKILL.md` follows [Agent Skills](https://agentskills.io/specification), an open
specification supported across multiple agents. `gh skill install --agent` accepts 47
agent targets, so the same skill directory is portable well beyond the five listed here.

The skill's `references/` directory uses symlinks to `docs/`, `scripts/`, and
`skills/vendor/`. Because those targets live in this same repository, they resolve
after a clone, and every install path below clones or fetches the repository.

## Install

### Claude Code

Add this repository as a marketplace, then install the plugin:

```
/plugin marketplace add microsoft/azcapman
/plugin install azure-capacity-management@azcapman
```

Manifests: `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`, per the
[Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference).

### GitHub Copilot

Install the skill with the [GitHub CLI](https://cli.github.com/manual/gh_skill_install)
(v2.90.0 or later):

```
gh skill install microsoft/azcapman azure-capacity-management
```

Preview it first without installing:

```
gh skill preview microsoft/azcapman azure-capacity-management
```

The custom agent at `.github/agents/azure-capacity-manager.agent.md` follows the
[custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration).
Its `target` property is unset, so it applies to both GitHub Copilot and VS Code.

### VS Code

VS Code reads [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
and the same `.github/agents/` custom agent as GitHub Copilot. Clone the repository, or
install the skill with `gh skill install` as shown above. No extension is required.

### Azure SRE Agent

In an existing agent, go to **Builder** > **Plugins** > **Install from URL** and enter
`microsoft/azcapman`, or add the repository as a marketplace. Azure SRE Agent accepts
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` as manifest locations,
per the [plugin marketplace documentation](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
and [install from a URL](https://learn.microsoft.com/en-us/azure/sre-agent/install-plugin-from-url).

Installation pins to the git commit at install time, so later changes to this repository
don't alter an installed agent until you update it.

### OpenAI Codex

Add the repository as a plugin marketplace, per the
[Codex plugin documentation](https://developers.openai.com/plugins/build/plugins):

```
codex plugin marketplace add microsoft/azcapman
```

Manifest: `.codex-plugin/plugin.json`. Codex also reads `AGENTS.md` from the repository
root, per [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Layout

```
.claude-plugin/plugin.json                     # Claude Code, Azure SRE Agent, VS Code
.claude-plugin/marketplace.json                # Marketplace manifest for the same three
.codex-plugin/plugin.json                      # OpenAI Codex
.github/agents/azure-capacity-manager.agent.md # GitHub Copilot and VS Code
agents/azure-capacity-manager.md               # Claude Code agent
skills/azure-capacity-management/SKILL.md      # Shared skill, Agent Skills specification
skills/azure-capacity-management/references/   # Symlinks to docs, scripts, and vendor
sre-agent/                                     # ExtendedAgent subagent YAML, a separate
                                               # in-portal mechanism, not plugin install
```

## Validation

Three first-party validators cover this packaging, and
`.github/workflows/validate-plugins.yml` runs all of them on every change:

| Command | Covers |
| --- | --- |
| `npx skills-ref validate skills/azure-capacity-management` | Agent Skills specification compliance |
| `gh skill publish --dry-run` | GitHub's skill naming, frontmatter, and metadata checks |
| `npx @anthropic-ai/claude-code plugin validate . --strict` | Claude Code plugin and marketplace manifests |

`gh skill publish --dry-run` validates without publishing and needs no write access, so
it runs as a plain lint step.

## Integration

The skill uses `az` CLI commands for live Azure operations, including quota queries,
capacity reservation group management, and estate enumeration. An authenticated Azure CLI
session is the only requirement, per the
[Azure CLI quota reference](https://learn.microsoft.com/en-us/cli/azure/quota).
