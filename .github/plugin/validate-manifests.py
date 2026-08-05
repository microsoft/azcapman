#!/usr/bin/env python3
"""Structural checks for the plugin manifests and custom agent files."""
import json
import pathlib
import sys

def _repo_root():
    for candidate in pathlib.Path(__file__).resolve().parents:
        if (candidate / ".claude-plugin").is_dir():
            return candidate
    return pathlib.Path.cwd()


ROOT = _repo_root()

PLUGIN_MANIFESTS = [
    ".github/plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
]
MARKETPLACE_MANIFESTS = [
    ".github/plugin/marketplace.json",
    ".claude-plugin/marketplace.json",
]
AGENT_MAX_CHARS = 30000
# Keys that belong to another harness's agent format and are not part of the
# GitHub Copilot custom agent schema.
FOREIGN_AGENT_KEYS = {"skills", "allowed-tools", "argument-hint"}

errors = []


def fail(msg):
    errors.append(msg)


def load(rel):
    path = ROOT / rel
    if not path.is_file():
        fail(f"{rel}: missing")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{rel}: invalid JSON - {exc}")
        return None


def as_list(value):
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def norm_paths(value):
    return sorted(p.rstrip("/").removeprefix("./") for p in as_list(value))


def check_paths(rel, declared, field):
    for raw in as_list(declared):
        target = ROOT / raw.removeprefix("./").rstrip("/")
        if not target.exists():
            fail(f"{rel}: {field} points at '{raw}', which doesn't exist")


# Portability rules recreated from the observed behavior of
# `claude plugin validate --strict` (claude-code 2.1.218, checked 2026-07-30), so
# CI keeps this coverage without fetching and executing that tool:
#   - 'agents' paths must be './'-prefixed, and must name a *.agent.md file; a bare
#     directory is rejected, even though Copilot CLI accepts one
#   - Claude's marketplace plugin entry schema has no 'agents' field at all
#
# 'skills' is exempt from the './' rule, because it names a *container* directory
# whose immediate children are the skill directories - not a skill directory
# itself. Copilot CLI documents the field as "Path(s) to skill directories
# (SKILL.md files)", defaulting to 'skills/', with the example
# '"skills": ["skills/", "extra-skills/"]':
# https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
# Claude Code documents the matching 'skills/<name>/SKILL.md' layout:
# https://code.claude.com/docs/en/plugins-reference
# All seven plugins in Microsoft's reference marketplace Azure/sre-agent-plugins
# declare exactly ["skills/"]. Azure SRE Agent, whose plugin component model is at
# https://learn.microsoft.com/en-us/azure/sre-agent/plugin-marketplace, returned
# 'no_skills_found' for the './'-prefixed skill-directory form when measured
# against a live agent on 2026-08-05.
#
# Claude Code discovers agents from the agents/ directory, not from the manifest.
# Measured on claude-code 2.1.218 (2026-07-31) by installing four probe plugins that
# differed only in this field: with 'agents' naming a file the plugin installs and
# reports Agents (0), and with the field absent the same file loads as Agents (1).
# Pointing 'agents' at a directory is rejected outright, so for Claude there is no
# form of this field that works - it either validates and silently drops the agent,
# or fails validation. Copilot CLI does consume its own manifest's 'agents' array,
# so the field stays in .github/plugin/plugin.json and is banned here.
CLAUDE_MARKETPLACE = ".claude-plugin/marketplace.json"
CLAUDE_PLUGIN = ".claude-plugin/plugin.json"


def check_component_shape(rel, declared, field):
    for raw in as_list(declared):
        target = ROOT / raw.removeprefix("./").rstrip("/")
        if field == "agents":
            if not raw.startswith("./"):
                fail(f"{rel}: {field} '{raw}' must start with './'")
            if not raw.endswith(".agent.md"):
                fail(f"{rel}: agents '{raw}' must name a *.agent.md file - a "
                     f"directory is rejected by Claude's schema")
            elif target.exists() and not target.is_file():
                fail(f"{rel}: agents '{raw}' is not a file")
        elif field == "skills" and target.exists() and not target.is_dir():
            fail(f"{rel}: skills '{raw}' must be a directory")


plugins = {rel: load(rel) for rel in PLUGIN_MANIFESTS}
markets = {rel: load(rel) for rel in MARKETPLACE_MANIFESTS}

# Shared fields must agree across every plugin manifest.
for field in ("name", "version", "description"):
    seen = {rel: m.get(field) for rel, m in plugins.items() if m}
    if len(set(seen.values())) > 1:
        fail(f"plugin manifests disagree on '{field}': {seen}")

skill_sets = {rel: norm_paths(m.get("skills")) for rel, m in plugins.items() if m}
if len(set(map(tuple, skill_sets.values()))) > 1:
    fail(f"plugin manifests disagree on 'skills': {skill_sets}")

# Only manifests that declare 'agents' are compared; Codex has no agent concept.
agent_sets = {rel: norm_paths(m.get("agents"))
              for rel, m in plugins.items() if m and "agents" in m}
if len(set(map(tuple, agent_sets.values()))) > 1:
    fail(f"plugin manifests disagree on 'agents': {agent_sets}")

for rel, manifest in plugins.items():
    if not manifest:
        continue
    if not manifest.get("name"):
        fail(f"{rel}: 'name' is required")
    check_paths(rel, manifest.get("skills"), "skills")
    check_paths(rel, manifest.get("agents"), "agents")
    check_component_shape(rel, manifest.get("skills"), "skills")
    check_component_shape(rel, manifest.get("agents"), "agents")
    # Declaring this makes Claude Code load no agents at all. See the note above.
    if rel == CLAUDE_PLUGIN and "agents" in manifest:
        fail(f"{rel}: declares 'agents', which stops Claude Code discovering any "
             f"agent - remove the field and let it read the agents/ directory")

for rel, manifest in markets.items():
    if not manifest:
        continue
    for field in ("name", "owner", "plugins"):
        if not manifest.get(field):
            fail(f"{rel}: '{field}' is required")
    for entry in manifest.get("plugins", []):
        if not entry.get("source"):
            fail(f"{rel}: plugin '{entry.get('name')}' has no source")
        check_paths(rel, entry.get("source"), "source")
        check_paths(rel, entry.get("skills"), "skills")
        check_paths(rel, entry.get("agents"), "agents")
        check_component_shape(rel, entry.get("skills"), "skills")
        check_component_shape(rel, entry.get("agents"), "agents")
        # Claude's marketplace entry schema has no 'agents' field; declaring one
        # makes `claude plugin validate --strict` reject the whole marketplace.
        if rel == CLAUDE_MARKETPLACE and "agents" in entry:
            fail(f"{rel}: plugin '{entry.get('name')}' declares 'agents', which "
                 f"isn't in Claude's marketplace schema - Claude reads the "
                 f"agents/ directory, so no manifest here should declare it")

names = {rel: sorted(p.get("name", "") for p in m.get("plugins", []))
         for rel, m in markets.items() if m}
if len(set(map(tuple, names.values()))) > 1:
    fail(f"marketplace manifests list different plugins: {names}")

# Every declared plugin name must match a plugin manifest name.
manifest_names = {m.get("name") for m in plugins.values() if m}
for rel, listed in names.items():
    for name in listed:
        if name not in manifest_names:
            fail(f"{rel}: plugin '{name}' matches no plugin.json name {manifest_names}")

# Custom agent files.
agent_dir = ROOT / "agents"
agent_files = sorted(agent_dir.glob("*.agent.md")) if agent_dir.is_dir() else []
if not agent_files:
    fail("agents/: no *.agent.md files found; plugin agents won't load")

for path in agent_files:
    rel = path.relative_to(ROOT)
    text = path.read_text()
    if len(text) > AGENT_MAX_CHARS:
        fail(f"{rel}: {len(text)} chars exceeds the {AGENT_MAX_CHARS} limit")
    if not text.startswith("---\n"):
        fail(f"{rel}: missing YAML frontmatter")
        continue
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{rel}: unterminated YAML frontmatter")
        continue
    keys = {line.split(":", 1)[0].strip()
            for line in text[4:end].splitlines()
            if line.strip() and not line[0].isspace() and ":" in line}
    for required in ("name", "description"):
        if required not in keys:
            fail(f"{rel}: frontmatter is missing '{required}'")
    for foreign in sorted(keys & FOREIGN_AGENT_KEYS):
        fail(f"{rel}: frontmatter key '{foreign}' isn't in the Copilot agent schema")
    if f"{path.name.removesuffix('.agent.md')}" not in text[4:end]:
        fail(f"{rel}: frontmatter 'name' should match the file name")

# Each declared 'skills' path is a container directory; its immediate children are
# the published skill directories. Pin that published set, so a new directory under
# skills/ - vendored upstream material in particular - can't silently start shipping
# as a skill of this plugin.
PUBLISHED_SKILLS = ["azure-capacity-management"]

for rel, manifest in plugins.items():
    if not manifest:
        continue
    for skill in as_list(manifest.get("skills")):
        target = ROOT / skill.removeprefix("./").rstrip("/")
        if not target.is_dir():
            continue
        published = sorted(
            child.name
            for child in target.iterdir()
            if child.is_dir() and (child / "SKILL.md").is_file()
        )
        if not published:
            fail(f"{rel}: skills '{skill}' holds no <name>/SKILL.md skill directory")
        elif published != PUBLISHED_SKILLS:
            fail(f"{rel}: skills '{skill}' publishes {published}, "
                 f"expected {PUBLISHED_SKILLS}")

if errors:
    print("Manifest validation failed:\n")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print(f"Manifest validation passed "
      f"({len(PLUGIN_MANIFESTS)} plugin manifests, "
      f"{len(MARKETPLACE_MANIFESTS)} marketplace manifests, "
      f"{len(agent_files)} agent file(s)).")
