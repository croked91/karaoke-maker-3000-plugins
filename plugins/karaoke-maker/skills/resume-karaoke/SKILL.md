---
name: resume-karaoke
description: Continue an existing Quick karaoke project, retry an eligible failed stage, cancel when requested, or hand the same project to Studio for manual correction.
---

Find the known project with `get_karaoke`, or use `list_karaokes` if its ID is
unknown. Prefer the same project over preparing another copy of its MP3.

- For work still processing, report its actual stage. Do not issue another start.
- For `awaiting_start`, show the current quote and saved or requested visual brief
  before `start_karaoke`. Pass the returned `quote_id`, `project_revision` as
  `expected_revision`, the final `visual_preferences`, and a stable idempotency
  key only after the user authorizes those terms. Renew an expired quote with
  `refresh_karaoke_quote` and show its new terms before starting.
- Use `retry_karaoke` only when requested and `can_retry` is true. It resumes the
  eligible failed stage and keeps completed work and the saved visual brief;
  retry is not a request to generate a different background.
- Use `cancel_karaoke` when requested and `can_cancel` is true. It stops successor
  stages; do not promise that already completed or running work is undone or free.
- Use `open_in_studio` when the user requests detailed correction and `can_handoff`
  is true. This stops Quick automation and hands the same project to Studio; it is
  an intentional workflow change, not a read-only preview link.

Treat `needs_lyrics_review` as correction work. Offer the Studio handoff when
appropriate; do not call an ASR draft final lyrics or bypass the review via export.
For ready work, use its current authorized media links. Preserve identical
arguments and idempotency keys after lost responses; check status before another
mutation. Changed creative wishes are not a transport retry.