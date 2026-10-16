#!/usr/bin/env python3
"""Fetch a Pastey home page and print each recent post's id, title, and content."""
import re
import sys
import urllib.request
import html as html_lib

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"

PATTERN = re.compile(
    r'href="/view/(?P<id>[^"]+)".*?<h5>(?P<title>.*?)</h5>\s*<pre[^>]*>(?P<content>.*?)</pre>',
    re.DOTALL,
)


def main():
    with urllib.request.urlopen(BASE_URL) as response:
        page = response.read().decode("utf-8")

    matches = list(PATTERN.finditer(page))
    if not matches:
        print("No pastes found (recent list may be hidden for non-whitelisted callers).")
        return

    for m in matches:
        paste_id = m.group("id")
        title = html_lib.unescape(m.group("title").strip())
        content = html_lib.unescape(m.group("content").strip())

        print("-" * 40)
        print(f"ID:      {paste_id}")
        print(f"Title:   {title}")
        print(f"URL:     {BASE_URL}/view/{paste_id}")
        print("Content:")
        print(content)
    print("-" * 40)


if __name__ == "__main__":
    main()
