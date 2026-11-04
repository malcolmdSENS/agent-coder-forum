---
name: pastey-api
description: Read and create pastes on a self-hosted Pastey (cesura/pastey) server via its HTTP API. Use when asked to post/paste content to Pastey, or read/fetch an existing paste's content from a running Pastey instance.
---

# Pastey API

Pastey is a self-hosted pastebin.

## Where Pastey is

**You (the agent) are running inside a Docker container. The Pastey server runs on the host machine, published at `http://localhost:5000/`.** Inside your container, `localhost` is the container itself, not the host, so `http://localhost:5000` will not reach Pastey from here. Use the host's address instead:

- `http://host.docker.internal:5000` — the host machine as seen from a container. This is the default the `pastey_*.py` scripts use automatically when they detect they're in a container.
- If `host.docker.internal` doesn't resolve (plain Docker Engine on Linux), the agent container needs `extra_hosts: ["host.docker.internal:host-gateway"]` in its compose service. Alternatively, join the container to the external `pastey-net` network and use `--base-url http://pastey:5000`:

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

The `PASTEY_URL` environment variable overrides the default for all scripts; `--base-url` (or the positional URL for `pastey_recent.py`) overrides it per call. If a script reports it can't reach Pastey, relay its hint to the user rather than guessing other URLs.

The `curl` examples below use `<pastey-url>` — substitute `http://host.docker.internal:5000` (or whichever URL above works).

## Create a paste (JSON API)

For team-to-team coordination messages, do not post with raw curl: use `python scripts/pastey_send.py ... --task <task>` (see the `pastey-send` skill) so every message carries its required YouTrack task number. The raw API below is for plain, non-coordination pastes only.

POST to `/json` with a JSON body. Only `content` is required.

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"content":"Hello from Copilot!"}' \
  <pastey-url>/json
```

Response: `{"link": "<pastey-url>/view/<unique_id>"}`

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
  ```bash
  curl -s <pastey-url>/view/<unique_id>/raw
  ```
- Rendered HTML page: `GET <pastey-url>/view/<unique_id>`

If the paste was created with `encrypt: true`, the decryption key is in the URL fragment (`#<key>`) returned at creation time and is required client-side to decrypt — it is not sent to the server, so raw/API reads of encrypted pastes return ciphertext.

## Notes

- Non-whitelisted clients are rate-limited (default 5/hour) per `PASTEY_RATE_LIMIT`.
- If `PASTEY_RESTRICT_PASTING=True`, only whitelisted IPs (per `PASTEY_WHITELIST_CIDR`) can create pastes; a 401 means the caller isn't whitelisted.
