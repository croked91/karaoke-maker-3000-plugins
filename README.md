# Karaoke Maker 3000 — Codex plugin

Create karaoke MP4 videos from an MP3, then check or continue the same project.
Includes preparation, creation, status, resume and setup skills plus the hosted MCP server.

## Install in Codex

```sh
codex plugin marketplace add https://github.com/croked91/karaoke-maker-3000-plugins.git
codex plugin add karaoke-maker-3000@karaoke
```

Complete browser sign-in for the bundled connection with your existing Karaoke
Maker account when prompted, then start a new chat. If Codex Desktop has not loaded
the new skills or tools, fully quit and reopen the app. Example:

> Create karaoke from this MP3 with a snowy forest background and blue accents.

The plugin includes its MCP connection. Do not add a duplicate standalone MCP server.
Installation and account connection do not start paid processing: the service returns
the current quote and requires your confirmation before creation starts.

Already configured this marketplace? Open the plugin using:
`codex://plugins/install/karaoke-maker-3000?marketplace=karaoke`.

## Links

- Setup: https://karaokemaker3000.art/agents
- Website: https://karaokemaker3000.art
- Privacy: https://karaokemaker3000.art/privacy.html
- MCP endpoint: https://karaokemaker3000.art/mcp

This repository distributes only the public Codex plugin, skills and metadata.
The application, processing workers and production credentials are hosted separately.
The native manifests follow the Codex marketplace layout. Portable manifests are
deliberately excluded from this distribution so Codex uses the bundled OAuth settings.
