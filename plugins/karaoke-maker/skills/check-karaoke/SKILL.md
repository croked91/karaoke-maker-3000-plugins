---
name: check-karaoke
description: Read the connected Karaoke account, balance, Quick projects or a project's processing status and current download links without starting or changing work.
---

Use `get_account` for the connected account and balance. Use `list_karaokes` to
find the account's Quick projects, then `get_karaoke` with the selected project
ID. This listing covers Quick projects; do not claim it includes every legacy
Studio project or merges different email and Telegram accounts.

Use the returned status, progress, warnings and `can_*` actions as authoritative.
`show_karaoke` can display the interactive result; omit `visual_preferences` when
checking existing work so no presentation brief is changed. If the host cannot
render a card, return a concise text status and supported links.

Offer the MP4 only when the current result reports a ready export and no
`needs_lyrics_review`. Use the returned authorized preview/download URLs. Refresh
status if a link expires; do not invent a persistent file URL or infer readiness
from a percentage. A lyrics review state needs correction, not an export bypass.

Checking status does not authorize preparing a new draft, renewing a quote,
starting, retrying, cancelling or handing a project to Studio. If an operation is
needed, explain it and follow the user's requested scope.