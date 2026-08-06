---
name: agent-plugins-and-skills
description: Explains how plugin, skill, and marketplace systems work in Claude Code, Codex/ChatGPT CLI, GitHub Copilot CLI, and Azure SRE Agent, plus the vendor-neutral Agent Skills specification. Use when building or reviewing a plugin or skill package for any of these ecosystems, or when comparing their manifest formats, discovery conventions, or install and versioning models.
---

# Agent plugins and skills across ecosystems

This skill explains how four agentic-CLI ecosystems, plus one vendor-neutral
specification, structure plugins, skills, and marketplaces: where their manifest
files live, which fields are required or optional, how a marketplace registers
and installs a plugin, and how each system discovers a skill inside a plugin.
Use it to understand or check the shape of a plugin or skill package for any one
of these five surfaces.

This skill is purely descriptive. It states what each canonical source says
about its own ecosystem's mechanics, and it says so plainly when a source
doesn't cover something (see the Codex/ChatGPT CLI row below) rather than
filling the gap from an uncited source.

## Reference files

Each ecosystem has its own reference file with the full field-by-field detail,
loaded on demand:

- `references/claude-code.md` — [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- `references/codex-cli.md` — [Codex/ChatGPT CLI plugins](https://learn.chatgpt.com/docs/plugins?surface=cli)
- `references/github-copilot-cli.md` — [GitHub Copilot CLI plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) and [creating plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
- `references/azure-sre-agent.md` — [Plugin Marketplace in Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)
- `references/agent-skills-specification.md` — [Agent Skills specification](https://agentskills.io/specification)

## Shared foundation: the Agent Skills specification

The [Agent Skills specification](https://agentskills.io/specification) defines a
vendor-neutral skill shape that several of these ecosystems build on: a
directory holding a required `SKILL.md` file (YAML frontmatter, then Markdown
instructions), plus optional `scripts/`, `references/`, and `assets/`
subdirectories.

`SKILL.md` frontmatter has two required fields — `name` (max 64 characters,
lowercase letters/numbers/hyphens only, no leading, trailing, or consecutive
hyphens, and it must match the parent directory name) and `description` (max
1024 characters, non-empty) — plus optional `license`, `compatibility` (max 500
characters), `metadata` (a string-to-string map), and an experimental
`allowed-tools` field ([agentskills.io](https://agentskills.io/specification)).

The specification also defines progressive disclosure: an agent loads a skill's
`name` and `description` (~100 tokens) at startup, loads the full `SKILL.md`
body (recommended under 5000 tokens and 500 lines) only once the skill
activates, and loads anything in `scripts/`, `references/`, or `assets/` only as
a task needs it ([agentskills.io](https://agentskills.io/specification)). This
skill package follows that same split: this file is the always-loaded
foundation, and `references/*.md` are the on-demand, per-ecosystem detail.

Two of the four install ecosystems covered here confirm they use this same
individual-skill directory shape for a plugin's own skills: Claude Code's
default skill-discovery convention is `skills/<name>/SKILL.md` inside a plugin
directory ([Claude Code](https://code.claude.com/docs/en/plugin-marketplaces)),
and GitHub Copilot CLI's own worked example creates a skill at
`skills/deploy/SKILL.md` ([GitHub Copilot
CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)).
Azure SRE Agent's marketplace page also refers to "`SKILL.md` content" when
describing how a skill gets imported from a plugin ([Azure SRE
Agent](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace)).
Codex/ChatGPT CLI's canonical source describes skills only as a plugin
component type, without naming a file format for them — see the coverage note
in `references/codex-cli.md`.

## Comparison across the four install ecosystems

Facts in each row trace to the source linked in that row's ecosystem cell,
detailed further in the matching `references/*.md` file.

| Ecosystem | Marketplace manifest | Plugin manifest | Skill/component discovery | Install command | Version pinning |
| --- | --- | --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/plugin-marketplaces) | `marketplace.json` at `.claude-plugin/marketplace.json` (repo root); required `name`, `owner`, `plugins` | `plugin.json` at `<plugin-dir>/.claude-plugin/plugin.json` | Default `skills/<name>/SKILL.md`; overridable via the `skills` field (string or array of paths) | `/plugin marketplace add <path-or-source>`, then `/plugin install <plugin-name>@<marketplace-name>` | Per-plugin `source.sha` (exact commit) takes priority over `source.ref` (branch/tag) when both are set |
| [Codex/ChatGPT CLI](https://learn.chatgpt.com/docs/plugins?surface=cli) | Not specified by this canonical source (it covers install/use, not authoring; see `references/codex-cli.md`) | Not specified by this canonical source | `/plugins` browses and installs from a configured marketplace; a new session is needed to use newly installed capabilities | `/plugins` (Codex CLI plugin browser) | Not specified by this canonical source |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) | `marketplace.json` in `.github/plugin/` (also recognized in `.claude-plugin/`); required `plugins` array, each entry with `name`, `description`, `version`, `source` | `plugin.json` required at the plugin directory root; fields include `name`, `description`, `version`, `author`, `license`, `keywords`, `agents`, `skills`, `hooks`, `mcpServers` | `skills` field names one or more container paths (e.g. `["skills/", "extra-skills/"]`); each container's subdirectories are individual `NAME/SKILL.md` skills | `copilot plugin marketplace add owner/repo`; local dev: `copilot plugin install ./my-plugin` | Manifest carries a `version` string field; a local plugin's components are cached on install, and reinstalling (`copilot plugin install ./my-plugin`) is what picks up local changes — this source doesn't describe commit-level pinning the way Claude Code or Azure SRE Agent do |
| [Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace) | `marketplace.json` at repo root, `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, or `.claude-plugin/marketplace.json` | Single-plugin repos: `plugin.json` at the same four location patterns | Skills and MCP servers are the two component types; this source doesn't give an internal file-path convention for a plugin's own skill directories beyond referring to imported "`SKILL.md` content" | Builder > Plugins > Add marketplace (clones in background); "Install from URL" for a one-off install without registering a marketplace | Every install is pinned to the exact git commit at install time; changes to the source repo have no effect until an explicit update |

## Notes on scope

This skill only states what its six canonical sources say. Where a source is
silent on a detail — most notably, Codex/ChatGPT CLI's manifest schema — this
skill says so rather than inferring from a non-canonical page (such as
`developers.openai.com/plugins/build/plugins`, which the Codex/ChatGPT CLI
source itself points to for that detail). See `references/codex-cli.md` for the
full coverage note.
