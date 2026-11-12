---
name: prepare-karaoke
description: Import the user's selected MP3 into a free karaoke Quick draft, check the current price and capture visual wishes without starting paid processing.
---

Use the connected karaoke-maker-3000 MCP tools. Call `get_account` if the account
needs checking; use the host's OAuth flow when disconnected.

## Selected local MP3

When the agent can read the selected file, resolve this installed plugin's root
from the location of this skill, not a hardcoded cache version. Use the bundled
Python 3.10+ standard-library helper:

```sh
python <installed-plugin-root>/scripts/local_audio.py inspect <user-selected-MP3-path>
```

Safely quote the paths for the current shell. The result contains `filename`,
`byte_size` and lowercase `sha256`. Pass those to `create_local_upload` with a
stable `idempotency_key` and optional title, artist and language. Then run:

```sh
python <installed-plugin-root>/scripts/local_audio.py upload <same-MP3-path>
```

Pass the tool's structured result JSON through the process's **standard input**,
not argv or environment variables. The helper streams a raw PUT of the unchanged
file to `upload_url` using its `headers`, validates the file digest and size, and
requires HTTPS on https://karaokemaker3000.art with the exact path
`/api/agent/audio-upload`; do not follow redirects.

The Authorization header is a short-lived upload capability, not an OAuth token.
Do not log requests or bodies. Never read credential stores, print the capability, encode audio into
chat, place it in MCP JSON, or send the file to an unrelated public host.
Then call `get_karaoke` with the returned `project_id` to retrieve its quote.
If the upload result is lost, inspect that project before uploading again.
If the ticket expires, request a renewed ticket for the same file and key. If
Python or local streaming is unavailable, use the supported upload-page fallback
below; do not install unrelated dependencies or weaken upload checks.

## Host-provided download URL

If the host instead supplies a supported HTTPS file URL, use `prepare_karaoke`
with `download_url` and a stable `idempotency_key`. A local path, attachment label
or fabricated URL is not a download URL. If neither local streaming nor a supported
URL is available, offer https://karaokemaker3000.art/maker?mode=quick for upload.

## Quote and visual brief

Keep concrete background, color and exclusion wishes in a concise
`visual_preferences` brief. An empty brief lets the service choose. Only send the
project-relevant wishes, not the conversation history.

Show the returned current quote and the visual brief. Preparation imports audio
and creates a draft; it does not reserve funds or start processing. Keep the
project ID, `quote_id` and `project_revision` for an authorized start.
If useful, use `show_karaoke` with the brief to prefill its confirmation card.
The returned `presentation_visual_preferences` is an unsaved presentation draft;
it is saved only when passed to `start_karaoke`.

After a lost response, keep the same arguments and idempotency key. Refresh an
expired unstarted quote with `refresh_karaoke_quote` and show its renewed terms.
Do not call `start_karaoke` without authorization of the current terms.
