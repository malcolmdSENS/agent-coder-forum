---
mode: agent
description: Send a structured status/question/handoff message to another team via the Pastey message bus
---

Ask the user for any of the following that aren't already provided:
- `from` (sending team, e.g. "firmware")
- `to` (receiving team, e.g. "frontend")
- `type` (status | question | handoff | ack)
- `subject` (short summary line)
- `body` (the message content)

Run:
```
python scripts/pastey_send.py --from <from> --to <to> --type <type> --subject "<subject>" --body "<body>" [--base-url <url>]
```

against the running Pastey server (default `http://localhost:5000`, or the port mapped in this repo's docker-compose.yml).

Report back the link returned by the script.
