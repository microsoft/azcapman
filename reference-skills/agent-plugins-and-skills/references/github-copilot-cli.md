# GitHub Copilot CLI plugins and marketplaces

Sources: [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
and [Creating a plugin for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating).
Every claim below traces to one of those two pages unless noted otherwise.

## Plugin structure

A plugin is a directory that must contain a `plugin.json` manifest file at its
root ([Creating a plugin](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)).
It can also contain any combination of agents, skills, hooks, and MCP server
configurations:

```
my-plugin/
├── plugin.json           # required manifest
├── agents/                # custom agents (optional)
│   └── helper.agent.md
├── skills/                # skills (optional)
│   └── deploy/
│       └── SKILL.md
├── hooks.json             # hook configuration (optional)
└── .mcp.json              # MCP server config (optional)
```

### `plugin.json` example

```json
{
  "name": "my-dev-tools",
  "description": "React development utilities",
  "version": "1.2.0",
  "author": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "license": "MIT",
  "keywords": ["react", "frontend"],
  "agents": "agents/",
  "skills": ["skills/", "extra-skills/"],
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

The fields shown here are `name`, `description`, `version`, `author`, `license`,
`keywords`, `agents`, `skills`, `hooks`, and `mcpServers`. The `skills` field can
take one or more container-directory paths (here, both `skills/` and
`extra-skills/`); each container's own subdirectories are the individual skills,
each holding its own `SKILL.md`.

### Adding an agent

An agent is a `NAME.agent.md` file inside an `agents/` subdirectory, with YAML
frontmatter such as `name`, `description`, and `tools`, followed by the agent's
instructions in the body.

### Adding a skill

A skill is a `skills/NAME/` subdirectory containing a `SKILL.md` file, with
frontmatter fields such as `name` and `description`, followed by the skill's
instructions in the body — for example, `skills/deploy/SKILL.md` for a "deploy"
skill.

## Local install, test, and iterate

1. Install a local plugin directory for testing: `copilot plugin install
   ./my-plugin`.
2. Confirm it loaded: `copilot plugin list`, or in an interactive session,
   `/plugin list`.
3. Confirm individual components loaded: `/agent` for custom agents, `/skills
   list` for skills.
4. **Caching:** a plugin's components are cached on install, and the CLI reads
   from that cache for subsequent sessions. To pick up changes made to a local
   plugin, install it again with `copilot plugin install ./my-plugin`.
5. Uninstall a local test install with `copilot plugin uninstall NAME`, using the
   plugin's `name` field from its `plugin.json`, not the path to its directory.

## Creating a marketplace

A `marketplace.json` file is the only required component of a plugin marketplace
([Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)).
Adding it to a repository lets Copilot CLI recognize that repository as a plugin
marketplace and lets users install plugins from it.

### `marketplace.json` example

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Organization",
    "email": "plugins@example.com"
  },
  "metadata": {
    "description": "Curated plugins for our team",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "frontend-design",
      "description": "Create a professional-looking GUI ...",
      "version": "2.1.0",
      "source": "./plugins/frontend-design"
    },
    {
      "name": "security-checks",
      "description": "Check for potential security vulnerabilities ...",
      "version": "1.3.0",
      "source": "./plugins/security-checks"
    }
  ]
}
```

The top-level `plugins` field is an array of plugin objects, each with metadata
including its name, description, version, and `source`. The `source` value is the
path to the plugin's directory relative to the repository root; a leading `./`
isn't required, so `"./plugins/plugin-name"` and `"plugins/plugin-name"` resolve
to the same directory.

### Location

`marketplace.json` goes in the `.github/plugin/` directory of a repository.
Copilot CLI also looks for it in the `.claude-plugin/` directory.

### Publishing plugin directories alongside the manifest

For each plugin listed in `marketplace.json`, the corresponding plugin directory
needs to exist at the path named in its `source` field — for example, a plugin
entry with `"source": "./plugins/frontend-design"` needs a `frontend-design`
plugin directory at `plugins/frontend-design` in the repository.

### Adding the marketplace as a user

Sharing a marketplace repository means giving users an add command such as:

```shell
copilot plugin marketplace add octo-org/octo-repo
```

## Distribution

Distributing a plugin means adding it to a marketplace, as described above.
