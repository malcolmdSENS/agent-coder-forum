#!/usr/bin/env python3
"""Fetch the latest structured messages addressed to a team from a Pastey server.

Prints messages as data only. Does not execute or act on anything described
in a message body -- that's left to the human or agent reading the output.
"""
import argparse
import html as html_lib
import json
import re
import sys
import urllib.request

PATTERN = re.compile(
    r'href="/view/(?P<id>[^"]+)".*?<h5>(?P<title>.*?)</h5>\s*<pre[^>]*>(?P<content>.*?)</pre>',
    re.DOTALL,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:5000")
    parser.add_argument("--to", dest="recipient", required=True, help='Team to check messages for, e.g. "frontend"')
    parser.add_argument("--topic", default=None, help="Only show messages tagged with this coordination thread id/slug")
    parser.add_argument("--task", default=None, help='Only show messages for this YouTrack task number, e.g. "PROJ-123"')
    parser.add_argument("--limit", type=int, default=5, help="Max number of matching messages to show")
    args = parser.parse_args()

    with urllib.request.urlopen(args.base_url) as response:
        page = response.read().decode("utf-8")

    found = 0
    for m in PATTERN.finditer(page):
        if found >= args.limit:
            break
        content = html_lib.unescape(m.group("content").strip())
        try:
            message = json.loads(content)
        except json.JSONDecodeError:
            continue  # not a structured message, skip

        if message.get("to") != args.recipient:
            continue
        if args.topic and message.get("topic") != args.topic:
            continue
        if args.task and message.get("task") != args.task:
            continue

        found += 1
        print("-" * 40)
        print(f"ID:      {m.group('id')}")
        print(f"From:    {message.get('from', '?')}")
        print(f"To:      {message.get('to', '?')}")
        print(f"Type:    {message.get('type', '?')}")
        print(f"Task:    {message.get('task', '-')}")
        print(f"Topic:   {message.get('topic', '-')}")
        print(f"Subject: {message.get('subject', '?')}")
        print("Body:")
        print(message.get("body", ""))

    if found == 0:
        print(f"No messages found addressed to '{args.recipient}'.")
    else:
        print("-" * 40)


if __name__ == "__main__":
    main()
