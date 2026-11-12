---
name: create-karaoke
description: Create a karaoke-maker-3000 Quick video from an MP3 after confirming its current quote and visual brief, including optional background and color wishes.
---

Use karaoke-maker-3000's MCP tools for the user's requested Quick project. The server performs audio processing, visual planning and MP4 rendering. Preserve explicit user choices; these instructions do not authorize a new paid run or regeneration.

- Use `get_account` when account linking or the connected identity needs checking. Follow the host's OAuth flow if linking is required.
- For a selected local MP3, follow [prepare-karaoke](../prepare-karaoke/SKILL.md): calculate its byte size and SHA-256, obtain a purpose-bound upload ticket with `create_local_upload`, stream raw file bytes to its exact same-origin upload URL, then read the returned project with `get_karaoke`. Keep file bytes and tickets out of chat. For a supported host-provided HTTPS URL, use `prepare_karaoke` with `download_url` and a stable idempotency key. A local path or attachment label is not a URL; do not invent URLs or use an unrelated public upload host. If this host supports neither delivery route, offer https://karaokemaker3000.art/maker?mode=quick for upload.
- Collect optional visual wishes as a concise `visual_preferences` string. Keep the user's concrete scene, colors and exclusions. An empty string lets the service choose. Only the project-relevant brief is sent, not the full conversation.
- Present the returned current terms and the brief before `start_karaoke`. Pass the returned `quote_id`, `project_revision` as `expected_revision`, the brief and a stable key once the user has authorized those terms. Do not turn upload or setup into implicit start authorization.
- Use `show_karaoke` to display the project's interactive card when helpful. For an unstarted project, pass the concise brief as `visual_preferences` so the card preserves wishes from this chat. An explicit empty string clears the presentation draft and lets Quick choose; omit the field for existing started work. The returned `presentation_visual_preferences` is an unsaved card draft; `start_karaoke` must receive the final brief to save it. If an unstarted quote has expired, use `refresh_karaoke_quote` and present the renewed terms before starting.
- Preserve the same command arguments and key when a response is lost. Check `get_karaoke` before deciding whether another action is needed. A changed instruction is not a transport retry.
- For an existing project, use `list_karaokes` or the known project ID, then `get_karaoke`. The list covers the connected account's Quick projects, not every legacy Studio project or unlinked email/Telegram identity. Use `can_start`, `can_retry`, `can_cancel` and `can_handoff` from the current result. Keep the same project rather than uploading another copy to repair an error.
- `retry_karaoke` resumes the failed stage with its saved visual brief. A request for a different generated background needs a supported explicit operation; do not use technical retry to imply regeneration.
- Treat `needs_lyrics_review` as a request for correction. Explain it and offer `open_in_studio`; do not bypass it with a direct export or call an ASR draft finished lyrics.
- Offer MP4 only when the service reports a current ready export and no lyrics review. Use returned authorized preview/download URLs. Refresh status for expired access; do not infer readiness from progress percentage.
- Use `cancel_karaoke` when requested. Use `open_in_studio` when the user requests detailed editing or unsupported Quick formatting, preserving the same project. Studio handoff stops Quick automation; it is not a read-only preview action.

Return the actual stage, result or required user action. Quick visual wishes guide the background and palette within supported settings; do not promise unsupported video layouts or typography. Never claim processing is complete until the service confirms it.
