# Azure capacity management plugin

This repository packages its Azure capacity and quota content as an installable plugin
for Claude Code, OpenAI Codex, GitHub Copilot CLI, the GitHub Copilot cloud agent,
VS Code, and Azure SRE Agent. The skill content is authored once, in
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

### GitHub Copilot CLI

Add this repository as a plugin marketplace, then install the plugin:

```
copilot plugin marketplace add microsoft/azcapman
copilot plugin install azure-capacity-management@azcapman
```

Manifests: `.github/plugin/marketplace.json` and `.github/plugin/plugin.json`, per the
[CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
and [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace).

The plugin installs one skill and one custom agent. The agent is namespaced by plugin,
so address it as `azure-capacity-management:azure-capacity-manager`:

```
copilot --agent azure-capacity-management:azure-capacity-manager
```

Copilot CLI also accepts `copilot plugin install microsoft/azcapman` to install straight
from the repository, but the CLI reports that direct repository, URL, and local-path
installs are deprecated in favour of `plugin@marketplace`. Use the marketplace commands
above.

To install only the skill, without the plugin or its agent, use the
[GitHub CLI](https://cli.github.com/manual/gh_skill_install) (v2.90.0 or later):

```
gh skill install microsoft/azcapman azure-capacity-management
```

### GitHub Copilot cloud agent

The cloud agent installs plugins declaratively. Add the marketplace and the plugin to
`.github/copilot/settings.json` in the repository the agent works in, per
[About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins):

```json
{
  "extraKnownMarketplaces": {
    "azcapman": {
      "source": {
        "source": "github",
        "repo": "microsoft/azcapman"
      }
    }
  },
  "enabledPlugins": {
    "azure-capacity-management@azcapman": true
  }
}
```

### VS Code

VS Code reads [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
and auto-detects `.claude-plugin/plugin.json`. Clone the repository, or install the skill
with `gh skill install` as shown above. No extension is required.

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
.github/plugin/plugin.json                     # GitHub Copilot CLI and cloud agent
.github/plugin/marketplace.json                # Marketplace manifest for the same
.claude-plugin/plugin.json                     # Claude Code, Azure SRE Agent, VS Code
.claude-plugin/marketplace.json                # Marketplace manifest for the same three
.codex-plugin/plugin.json                      # OpenAI Codex, skills only
agents/azure-capacity-manager.agent.md         # Custom agent, shipped by the plugin
skills/azure-capacity-management/SKILL.md      # Shared skill, Agent Skills specification
skills/azure-capacity-management/references/   # Symlinks to docs, scripts, and vendor
sre-agent/                                     # ExtendedAgent subagent YAML, a separate
                                               # in-portal mechanism, not plugin install
```

Every manifest points at the same `agents/` directory and the same single skill
directory. Scoping `skills` to `./skills/azure-capacity-management` keeps the vendored
upstream skills under `skills/vendor/` out of the published set; they stay reachable only
through this skill's `references/vendor/` path, as `SKILL.md` describes.

## Validation

`.github/workflows/validate-plugins.yml` runs two checks on every change, and **neither
one downloads anything**:

| Command | Covers |
| --- | --- |
| `python3 .github/plugin/validate-manifests.py` | Cross-manifest agreement, path existence, component shape, agent frontmatter |
| `gh skill publish --dry-run` | GitHub's skill naming, frontmatter, and metadata checks |

The validator script is in this repository and uses only the Python standard library.
`gh skill` is a built-in command of the `gh` CLI, which is preinstalled on
GitHub-hosted runners, so the step installs no extension. `--dry-run` validates
without publishing, so it needs no write access.

A third workflow, `.github/workflows/supply-chain.yml`, enforces
[AGENTS.md §1.4](AGENTS.md#14-verified-pinned-dependencies) against this repository's
own CI: every action approved and pinned to a commit SHA, no fetch-and-execute, no
unpinned installs, and explicit token scopes on every job. It parses the workflow YAML
and walks `jobs` → `steps`, so a folded block scalar can't hide a piped installer
across a line break. `.github/scripts/test-supply-chain.py` runs alongside it and
proves the checker still rejects each class of bypass — folded-scalar pipes,
download-then-run, shell line continuations, mutable tags, unapproved publishers,
container tags, external reusable workflows, and checkout inputs that pull in another
repository.

On their own these checks would be tripwires rather than a root of trust, since a pull
request can edit them in the same diff that weakens a workflow. On `main` they're backed
by controls that sit outside the pull request:
[branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
makes `validate` and `check` required status checks and blocks force pushes, and the
repository
[actions permissions policy](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository)
requires every action to be pinned to a full-length commit SHA and allows only
GitHub-owned actions, which GitHub applies before a run starts.
[CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
on `.github/**` routes an outside contributor's CI change to the maintainer. Code
owner review isn't required on this repository, so it notifies rather than blocks.

CI previously fetched and ran `npx @anthropic-ai/claude-code plugin validate . --strict`.
That step is gone, per §1.4 — a package runner in CI is fetch-and-execute of third-party
code on every run. The rules that validator enforced were reproduced in
`validate-manifests.py` instead: component paths must be `./`-prefixed, `agents` must
name a `*.agent.md` file rather than a directory, and a Claude marketplace entry must
not declare `agents`.

The validator also parses all five manifests, checks that the fields they share agree,
confirms every path a manifest points at exists, and validates each `agents/*.agent.md`
file against the
[custom agent schema](https://docs.github.com/en/copilot/reference/custom-agents-configuration):
`name` and `description` present, no keys from other harnesses' formats, and a prompt
body under the 30,000-character limit.

## Integration

The skill uses `az` CLI commands for live Azure operations, including quota queries,
capacity reservation group management, and estate enumeration. An authenticated Azure CLI
session is the only requirement, per the
[Azure CLI quota reference](https://learn.microsoft.com/en-us/cli/azure/quota).
