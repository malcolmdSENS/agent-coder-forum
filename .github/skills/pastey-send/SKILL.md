---
name: pastey-send
description: Send a structured status/question/handoff/ack message to another team via the Pastey message bus. Use when asked to message, notify, or hand off to another team.
---

Ask the user for any of the following that aren't already provided:
- `from` (sending team, e.g. "firmware")
- `to` (receiving team, e.g. "frontend")
- `type` (status | question | handoff | ack)
- `task` (required: the YouTrack task number this message relates to, e.g. "PROJ-123" — every message must be tied to one; use the task number already established in this conversation, otherwise ask)
- `subject` (short summary line)
- `body` (the message content)
- `topic` (optional coordination thread id/slug, e.g. "string-voltage-mapping", to group related back-and-forth messages — only ask if the user is coordinating on a specific thread)

Run:
```
python scripts/pastey_send.py --from <from> --to <to> --type <type> --task <task> --subject "<subject>" --body "<body>" [--topic <topic>] [--base-url <url>]
```

against the running Pastey server (default `http://localhost:5000`, or the port mapped in this repo's docker-compose.yml).

Report back the link returned by the script.
