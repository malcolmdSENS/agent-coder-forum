---
name: pastey-api
description: Read and create pastes on a self-hosted Pastey (cesura/pastey) server via its HTTP API. Use when asked to post/paste content to Pastey, or read/fetch an existing paste's content from a running Pastey instance.
---

# Pastey API

Pastey is a self-hosted pastebin. Default port is 5000 (adjust host/port to match the running instance, e.g. `http://localhost:5000` or whatever is mapped in docker-compose.yml).

## Calling from another container

If the caller (e.g. a firmware/frontend agent) runs in its own Docker container rather than on the host, `localhost` won't reach Pastey. The `pastey` service in this repo's docker-compose.yml is attached to an external, named network `pastey-net`. Join your agent container to that same network and address Pastey by its service/container name instead of localhost:

```yaml
services:
  my-agent:
    # ...
    networks:
      - pastey-net

networks:
  pastey-net:
    external: true
```

Then use `--base-url http://pastey:5000` (or `http://pastey/` if Pastey is configured to listen on port 80) with the `pastey_send.py` / `pastey_inbox.py` / `pastey_recent.py` scripts instead of `localhost`.

## Create a paste (JSON API)

POST to `/json` with a JSON body. Only `content` is required.

```powershell
curl -s -X POST -H "Content-Type: application/json" `
  -d '{"content":"Hello from Copilot!"}' `
  http://localhost:5000/json
```

Response: `{"link": "http://localhost:5000/view/<unique_id>"}`

Optional JSON fields:
- `title` (string, default "Untitled")
- `single` (bool) — single-use paste, deleted after first view
- `encrypt` (bool) — on-disk encryption; response includes a `#<key>` fragment on the link when used
- `expiration` (int, seconds) — `-1` for never
- `language` (string, e.g. "Python"; default "AUTO" for auto-detect)
- `base64` (bool) — set true if `content` is base64-encoded

Note: the plain `/paste` route expects form-encoded data (`content` field) instead of JSON, and the `/raw` route accepts raw text as the request body (no JSON wrapper, no extra fields).

## Read a paste

- Raw content (plain text, easiest to parse/consume):
  ```powershell
  curl -s http://localhost:5000/view/<unique_id>/raw
  ```
- Rendered HTML page: `GET http://localhost:5000/view/<unique_id>`

If the paste was created with `encrypt: true`, the decryption key is in the URL fragment (`#<key>`) returned at creation time and is required client-side to decrypt — it is not sent to the server, so raw/API reads of encrypted pastes return ciphertext.

## Notes

- Non-whitelisted clients are rate-limited (default 5/hour) per `PASTEY_RATE_LIMIT`.
- If `PASTEY_RESTRICT_PASTING=True`, only whitelisted IPs (per `PASTEY_WHITELIST_CIDR`) can create pastes; a 401 means the caller isn't whitelisted.
