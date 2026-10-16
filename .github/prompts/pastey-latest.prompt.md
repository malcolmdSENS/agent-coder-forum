---
mode: agent
description: Fetch and echo the most recent paste from the running Pastey server
---

Run `python scripts/pastey_recent.py [base_url]` to fetch and parse the Pastey home page (default base URL `http://localhost:5000`, or the port mapped in this repo's docker-compose.yml).

Steps:
1. Run the script. It only lists recent pastes if the caller is whitelisted or `PASTEY_FORCE_SHOW_RECENT=True` — if the output says no pastes were found, say so instead of guessing.
2. The first entry printed is the most recent paste.
3. Print that entry's ID, title, and content back to the user.

If the paste was created with encryption, its content will be ciphertext — note this instead of printing garbage text.
