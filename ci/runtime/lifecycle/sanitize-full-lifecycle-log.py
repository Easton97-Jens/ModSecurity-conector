#!/usr/bin/env python3
"""Copy a host log into canonical evidence without retaining request bodies.

The canonical full-lifecycle evidence root is intentionally useful after a
run, but it is not an audit-log archive.  In particular, a curl/debug trace
can otherwise reintroduce the test request or response body after the event
normalizer has carefully removed it.  This small filter preserves bounded
diagnostic lines and replaces known body sentinels and sensitive header
values.  It never treats a successful sanitization as runtime evidence.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re


BODY_SENTINELS = (
    "no-crs-request-body-marker",
    "no-crs-response-body-marker",
)
SENSITIVE_HEADER = re.compile(
    r"(?i)^(\s*(?:authorization|proxy-authorization|cookie|set-cookie)\s*:\s*).*$"
)
INLINE_SENSITIVE_HEADER = re.compile(
    r"(?i)(authorization|proxy-authorization|cookie|set-cookie)\s*:\s*[^\s,;]+"
)
MAX_LINE_CHARS = 2048


def sanitize_line(line: str) -> tuple[str, bool]:
    """Return a bounded, payload-free diagnostic line and whether it changed."""
    lowered = line.casefold()
    if any(marker in lowered for marker in BODY_SENTINELS):
        return "[body payload line omitted]", True
    match = SENSITIVE_HEADER.match(line)
    if match:
        return f"{match.group(1)}[redacted]", True
    cleaned = INLINE_SENSITIVE_HEADER.sub(r"\1: [redacted]", line)
    changed = cleaned != line
    if len(cleaned) > MAX_LINE_CHARS:
        cleaned = cleaned[:MAX_LINE_CHARS] + " [line truncated]"
        changed = True
    return cleaned, changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--label", default="host")
    args = parser.parse_args(argv)

    raw = args.input.read_bytes() if args.input.is_file() else b""
    text = raw.decode("utf-8", errors="replace")
    lines: list[str] = []
    redactions = 0
    for line in text.splitlines():
        safe, changed = sanitize_line(line)
        if changed:
            redactions += 1
        lines.append(safe)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"canonical_log_label={args.label}\n"
        f"source_sha256={hashlib.sha256(raw).hexdigest()}\n"
        f"source_bytes={len(raw)}\n"
        f"redacted_lines={redactions}\n"
    )
    args.output.write_text(header + "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
