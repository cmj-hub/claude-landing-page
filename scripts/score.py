#!/usr/bin/env python3
"""Score a page: one URL, one offer, and one action. Refuse a sitemap.

Stdlib only. No network. Does not publish.

  python3 scripts/score.py --file draft.json
  python3 scripts/score.py --stdin
  python3 scripts/score.py --file draft.json --json

Exit codes: 0 the page passes, 1 the page fails, 2 the input is unusable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


MAX_INPUT_BYTES = 2_000_000
MAX_OFFER_CHARS = 200
MAX_ACTION_CHARS = 160

# Keys that mean the draft carries more than one of something.
SITEMAP_KEYS = ("urls", "pages", "sitemap")
EXTRA_OFFER_KEYS = ("offers", "offer_2", "second_offer")
EXTRA_ACTION_KEYS = ("actions", "ctas", "action_2", "second_action")

# A sentence end followed by more text. "e.g." and decimals do not split.
SENTENCE_BREAK = re.compile(r"(?<!\be\.g)(?<!\bi\.e)[.!?]+[\"')\]]*\s+(?=\S)")


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input("file not found")
        if not path.is_file():
            fail_input("not a file")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input("cannot read file")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("file is not UTF-8 text")


def load_payload(args: argparse.Namespace) -> object:
    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail_input("input is not UTF-8 text")
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")
    try:
        return json.loads(text)
    except (json.JSONDecodeError, RecursionError):
        fail_input("invalid JSON")


def nonempty_text(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return " ".join(value.split())
    return ""


def is_sitemap(data: dict) -> bool:
    kind = nonempty_text(data.get("kind")).lower()
    if kind == "sitemap":
        return True
    if any(isinstance(data.get(key), (list, dict)) for key in SITEMAP_KEYS):
        return True
    if isinstance(data.get("url"), list):
        return True
    url = nonempty_text(data.get("url")).lower()
    path = urlsplit(url).path if url else ""
    if "sitemap" in url or path.endswith(".xml"):
        return True
    return False


def has_any(data: dict, keys: tuple[str, ...]) -> bool:
    return any(data.get(key) not in (None, "", [], {}) for key in keys)


def sentence_count(text: str) -> int:
    return len(SENTENCE_BREAK.split(text.strip()))


def check_url(raw: object) -> list[str]:
    url = nonempty_text(raw)
    if not url:
        return ["url is missing"]
    if any(ch.isspace() for ch in url) or url.count("://") > 1:
        return ["url holds more than one address"]
    parts = urlsplit(url)
    if parts.scheme != "https":
        return ["url is not https"]
    if not parts.hostname or "." not in parts.hostname:
        return ["url has no host"]
    return []


def check_line(name: str, raw: object, extra: bool, limit: int) -> list[str]:
    if isinstance(raw, (list, dict)) or extra:
        return [f"more than one {name}"]
    text = nonempty_text(raw)
    if not text:
        return [f"{name} is missing"]
    problems = []
    if sentence_count(text) > 1:
        problems.append(f"{name} is more than one sentence")
    if len(text) > limit:
        problems.append(f"{name} is longer than {limit} characters")
    return problems


def score(data: dict) -> dict:
    if is_sitemap(data):
        return {"pass": False, "sitemap": True, "problems": ["a sitemap"]}
    problems = (
        check_url(data.get("url"))
        + check_line("offer", data.get("offer"), has_any(data, EXTRA_OFFER_KEYS), MAX_OFFER_CHARS)
        + check_line("action", data.get("action"), has_any(data, EXTRA_ACTION_KEYS), MAX_ACTION_CHARS)
    )
    result = {"pass": not problems, "sitemap": False, "problems": problems}
    if not problems:
        result.update(
            url=nonempty_text(data["url"]),
            offer=nonempty_text(data["offer"]),
            action=nonempty_text(data["action"]),
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a page draft: one https URL, one offer, one action. Refuses a sitemap."
    )
    parser.add_argument("--file", help="Path to a JSON object")
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    parser.add_argument("--json", action="store_true", help="Print the result as one JSON object")
    args = parser.parse_args()
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    result = score(data)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif result["sitemap"]:
        print("a sitemap")
    elif not result["pass"]:
        print("draft fails")
        for problem in result["problems"]:
            print(f"- {problem}")
    else:
        print(f"url: {result['url']}")
        print(f"offer: {result['offer']}")
        print(f"action: {result['action']}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
