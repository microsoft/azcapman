# Codex/ChatGPT CLI plugins

Source: [Plugins](https://learn.chatgpt.com/docs/plugins?surface=cli), viewed with
`surface=cli`. Every claim below traces to that page unless noted otherwise.

## Coverage note

This page documents how a user browses, installs, and uses plugins in Codex CLI and
ChatGPT. It explicitly defers manifest structure, packaging, and marketplace setup
to a separate page, [Build plugins](https://developers.openai.com/plugins/build/plugins),
which is **not** one of this skill's six canonical sources. Because of that, this
reference doesn't state a Codex plugin manifest filename, its location, or its
field list — those facts aren't present on the assigned canonical source, and this
skill's citation rule (cite every claim to one of the six fixed sources) means they
can't be included here without fabricating or inferring beyond what that source
states. What follows is a description of the parts of the system the canonical
source actually documents: what a plugin can contain, and how a user discovers,
installs, and removes one.

## Shared plugin directory

ChatGPT and Codex use one universal plugin directory (called the Plugins
Directory in the ChatGPT desktop app and web), so the same public plugins are
discoverable from both products' supported surfaces. The directory organizes
plugins into an **OpenAI** tab (plugins built by OpenAI), a workspace tab (plugins
provided by the user's workspace), and a **Personal** tab (personal marketplace
plugins, including ones created by or shared with the user), plus a separate
**Installed** row for plugins already installed.

## What a plugin can bundle

A plugin can contain one or more of these parts:

- **Skills** — reusable instructions for specific kinds of work, loaded by ChatGPT
  or Codex when needed so the right steps and references or helper scripts get
  used for a task.
- **Connectors** — connections to tools such as GitHub, Slack, or Google Drive, so
  ChatGPT and Codex can read information from those tools and take actions in
  them; connectors expose tools and can optionally include custom UI.
- **MCP servers** — services that give ChatGPT and Codex access to more tools or
  shared information, often from systems outside the local project; they're also
  the services behind connectors, and they define tools, enforce auth, return
  structured data, and perform actions against external systems.
- **Browser extensions** — browser capabilities a plugin needs for its workflow.
- **Hooks** — commands that run at configured lifecycle points; the source
  recommends reviewing and trusting plugin hooks before enabling them.
- **Scheduled task templates** — reusable starting points for recurring tasks,
  where scheduled tasks are available.

## Discovery and install in Codex CLI

In Codex CLI, entering `/plugins` opens the plugin browser. A plugin installs from
a configured marketplace, and a new session needs to start before its bundled
skills or tools become usable. Plugins aren't available in the IDE extension,
Chat, or mobile — only in ChatGPT Work on the web, ChatGPT Work or Codex in the
ChatGPT desktop app, and the Codex CLI plugin browser.

Once a plugin is installed, a user can either describe the task directly and let
ChatGPT or Codex choose the right installed tools, or type `@` to invoke a
specific plugin or one of its bundled skills explicitly.

## Distribution

A plugin owner can share plugins by publishing them through a marketplace source,
such as a repository marketplace scoped to a project or team. The canonical
source points to a separate page for the mechanics of that (packaging, manifest
fields, marketplace setup) rather than documenting them itself.

## Permissions

When a plugin capability runs through a Codex host, that host's sandbox and
approval policy applies. Connections to external services use that service's own
authentication and access controls, and when a plugin includes connectors, the
active product may prompt for install or sign-in to those connectors during setup
or on first use.

## Removing a plugin

Uninstalling is done from a supported plugin browser, by selecting **Uninstall
plugin** when that action is available; workspace-installed or default plugins
may not offer that action, since a workspace administrator controls those
instead. Uninstalling removes the plugin bundle from that ChatGPT or Codex
environment, but any bundled connectors stay connected until managed separately
in ChatGPT.
