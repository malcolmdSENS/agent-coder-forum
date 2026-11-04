#!/usr/bin/env python3
"""Fetch a Pastey home page and print each recent post's id, title, and content."""
import argparse
import html as html_lib
import json
import re

from pastey_config import default_base_url, urlopen

PATTERN = re.compile(
    r'href="/view/(?P<id>[^"]+)".*?<h5>(?P<title>.*?)</h5>\s*<pre[^>]*>(?P<content>.*?)</pre>',
    re.DOTALL,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", nargs="?", default=default_base_url(), help="Pastey server URL (default: $PASTEY_URL, else auto-detected for host vs. Docker container)")
    parser.add_argument("--task", default=None, help='Only show structured messages for this YouTrack task number, e.g. "PROJ-123"')
    args = parser.parse_args()

    with urlopen(args.base_url, args.base_url) as response:
        page = response.read().decode("utf-8")

    matches = list(PATTERN.finditer(page))
    if not matches:
        print("No pastes found (recent list may be hidden for non-whitelisted callers).")
        return

    found = 0
    for m in matches:
        paste_id = m.group("id")
        title = html_lib.unescape(m.group("title").strip())
        content = html_lib.unescape(m.group("content").strip())

        try:
            message = json.loads(content)
        except json.JSONDecodeError:
            message = None
        task = message.get("task") if isinstance(message, dict) else None
        if args.task and task != args.task:
            continue

        found += 1
        print("-" * 40)
        print(f"ID:      {paste_id}")
        print(f"Title:   {title}")
        print(f"Task:    {task or '-'}")
        print(f"URL:     {args.base_url}/view/{paste_id}")
        print("Content:")
        print(content)

    if found == 0:
        print(f"No pastes found with task '{args.task}'.")
    else:
        print("-" * 40)


if __name__ == "__main__":
    main()
