---
applyTo: "**"
description: Keep a terse, timestamped LOG.md of every command run and every mutable action taken
---

# Agent action log (LOG.md)

Keep a running log in `LOG.md` at the workspace root. Create it if missing; only ever append — never rewrite or delete earlier lines.

Log **every** terminal command you run and **every** mutable action you take (file create/edit/delete, git commit/push/checkout, package installs, messages posted to Pastey or any other external service). Read-only tool use that isn't a terminal command (reading/searching files) does not need logging.

One line per item, terse, UTC timestamp:

```
- 2026-11-03 14:05:12Z | cmd    | python scripts/pastey_inbox.py --to frontend --task PROJ-123
- 2026-11-03 14:06:40Z | edit   | src/adc/voltage.c — scale string voltage by 1000
- 2026-11-03 14:07:02Z | create | docs/voltage-mapping.md
- 2026-11-03 14:08:15Z | git    | commit "PROJ-123 Fix string voltage scaling"
```

Kinds: `cmd`, `edit`, `create`, `delete`, `git`, `send`. Include the YouTrack task number when one is established, e.g. `| edit   | [PROJ-123] src/...`.

Use the real time, not a guess. The easiest way is to append with a shell command, which stamps it for you:

```bash
echo "- $(date -u '+%F %TZ') | edit   | src/adc/voltage.c — scale string voltage by 1000" >> LOG.md
```

Batching several items from the same step into one append is fine. Don't log the log appends themselves.

`scripts/pastey_send.py` logs its own `send` line (with the returned link) — don't log it a second time.
