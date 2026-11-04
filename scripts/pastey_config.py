"""Shared helpers for the pastey_*.py scripts: default server URL and friendly connection errors.

Agents usually run inside a Docker container while Pastey is published on the
host machine at http://localhost:5000. Inside a container, "localhost" is the
container itself, so the host has to be reached via host.docker.internal.
"""
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

HOST_URL = "http://localhost:5000"
CONTAINER_URL = "http://host.docker.internal:5000"


def in_container():
    return os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")


def default_base_url():
    """PASTEY_URL if set, else host.docker.internal inside a container, else localhost."""
    return os.environ.get("PASTEY_URL") or (CONTAINER_URL if in_container() else HOST_URL)


def log_action(kind, text, path="LOG.md"):
    """Append a timestamped line to the agent's LOG.md (see .github/instructions/agent-log.instructions.md)."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"- {stamp} | {kind:<6} | {text}\n")


def urlopen(url_or_request, base_url):
    """urllib.request.urlopen that exits with a hint instead of a traceback when Pastey is unreachable."""
    try:
        return urllib.request.urlopen(url_or_request, timeout=15)
    except urllib.error.URLError as e:
        hint = (
            "Running inside a Docker container: Pastey runs on the host at http://localhost:5000, "
            f"which is reached from here as {CONTAINER_URL}. If that hostname doesn't resolve, the container "
            'needs `extra_hosts: ["host.docker.internal:host-gateway"]`, or join the `pastey-net` network '
            "and use --base-url http://pastey:5000. Override the default with the PASTEY_URL env var."
            if in_container()
            else "Is the Pastey container running (docker compose up -d in agent-coder-forum)?"
        )
        sys.exit(f"Could not reach Pastey at {base_url}: {e.reason}\n{hint}")
