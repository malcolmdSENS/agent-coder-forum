#!/usr/bin/env python3
"""Post a structured JSON message to a Pastey server for inter-agent coordination."""
import argparse
import json
import sys
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:5000")
    parser.add_argument("--from", dest="sender", required=True, help='Sending team, e.g. "firmware"')
    parser.add_argument("--to", dest="recipient", required=True, help='Receiving team, e.g. "frontend"')
    parser.add_argument("--type", dest="msg_type", default="status", help="status | question | handoff | ack | finding")
    parser.add_argument("--task", required=True, help='YouTrack task number this message relates to, e.g. "PROJ-123"')
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--topic", default=None, help="Optional coordination thread id/slug to group related messages")
    args = parser.parse_args()

    message = {
        "from": args.sender,
        "to": args.recipient,
        "type": args.msg_type,
        "task": args.task,
        "subject": args.subject,
        "body": args.body,
    }
    if args.topic:
        message["topic"] = args.topic

    payload = json.dumps({
        "title": f"[{args.task}] [{args.sender} -> {args.recipient}] {args.subject}",
        "content": json.dumps(message, indent=2),
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{args.base_url}/json",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))

    print(f"Posted: {result['link']}")


if __name__ == "__main__":
    main()
