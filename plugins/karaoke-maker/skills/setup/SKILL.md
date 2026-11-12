---
name: setup
description: Connect the installed karaoke-maker-3000 plugin, verify its account, or diagnose missing karaoke tools. Stay in the user's current Codex or ChatGPT host.
---

# Connect karaoke-maker-3000

Identify the current host before choosing its connection controls. This plugin
bundles the remote MCP server and karaoke skills. Installation or reading this
skill does not authorize paid processing.

If this service's `get_account` tool is available, call it to verify the connected
identity. Reuse the connection. Never create or start a project as a setup test.

## Codex Desktop, CLI or IDE

When the user requests installation and this plugin is absent, use the published
marketplace commands once the distribution repository is available:

```sh
codex plugin marketplace add https://github.com/croked91/karaoke-maker-3000-plugins.git
codex plugin add karaoke-maker-3000@karaoke
```

Inspect `codex plugin list --marketplace karaoke --json` before adding an existing
install again. If the repository or package is unavailable, report that installation
has not completed; do not claim it is published or silently use another host.

Use the installed plugin's **karaoke-maker** MCP connection. Native configuration
is bundled in `.mcp.json`: HTTPS endpoint `https://karaokemaker3000.art/mcp`, public
OAuth client `karaoke-codex`, callback anchor `http://127.0.0.1/callback`.
Codex chooses an ephemeral local port. Scopes are `karaoke:read karaoke:write`.

Open the current Codex host's MCP/plugin controls and authenticate this connection.
The user signs into their existing Karaoke account and grants consent in the
browser. If the plugin was just installed and its tools are missing, ask the user
to fully quit and reopen Codex Desktop, then authenticate its bundled connection.
Use the host's reload controls when available. Do not register a duplicate server
with `codex mcp add` or manually rewrite `config.toml` for an installed plugin.

If installing, refreshing or authenticating needs the host's normal permission,
request that permission through its supported controls. A read-only configuration,
permission denial or unavailable CLI is a Codex setup limitation: stop this branch
and report the exact remaining Codex action. **Never switch a Codex user to ChatGPT
setup because Codex configuration is read-only.** Do not bypass host policy, read
credential stores, change global security or weaken production callback rules.

## ChatGPT

Only use this branch when the current host is ChatGPT. Use its available plugin
connection-management controls. The endpoint is the same; the predefined public
client is `karaoke-chatgpt`, its callback is
`https://chatgpt.com/connector_platform_oauth_redirect`, and no client secret is
required. Use scopes `karaoke:read karaoke:write`. A local Codex plugin install
does not install a ChatGPT web connection. If management controls are unavailable,
state that limitation and give the single remaining action in ChatGPT Plugins.

## Other hosts and verification

For another host, read https://karaokemaker3000.art/agents/connection.json and use
only an advertised compatible client. Stop if disabled. Do not infer a public
directory listing, DCR, CIMD or universal client support.

After the host loads the tools, call `get_account`. Report the actual connected
identity, or explicitly say installation succeeded but authentication/tool reload
remains. Distinguish **installed**, **needs restart**, **needs sign-in**, and
**verified**; only a successful tool call verifies the connection.
The account and existing wallet belong to that authenticated user;
different email and Telegram identities are not automatically merged. Never ask
for passwords, cookies, API keys or verification codes in chat.

Finish with one example: “Create karaoke from this MP3 with a snowy forest
background and blue accents.” Use the local-upload tool for a selected local MP3
when available; do not manufacture a public download URL.
