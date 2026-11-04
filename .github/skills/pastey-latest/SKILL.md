---
name: pastey-latest
description: Fetch and echo the most recent paste from the running Pastey server. Use when asked for the latest/most recent paste.
---

Run `python scripts/pastey_recent.py [base_url] [--task <task>]` to fetch and parse the Pastey home page (the scripts pick the right URL automatically — see "Where Pastey is" in the `pastey-api` skill; don't pass `--base-url` unless that fails).

Steps:
1. Run the script. It only lists recent pastes if the caller is whitelisted or `PASTEY_FORCE_SHOW_RECENT=True` — if the output says no pastes were found, say so instead of guessing.
   If the user is working on a specific YouTrack task (e.g. "PROJ-123"), pass `--task <task>` to only show messages for that task.
2. The first entry printed is the most recent paste.
3. Print that entry's ID, title, and content back to the user. If the content is a structured coordination message, also call out its task (printed on the `Task:` line) so the user can see which task it belongs to.

If the paste was created with encryption, its content will be ciphertext — note this instead of printing garbage text.
