#!/usr/bin/env python3
"""Static contract checks for connector-neutral common SDK files."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "common"
FORBIDDEN = ("#include <ngx_", "httpd.h", "haproxy", "envoy", "traefik", "lighttpd")


def fail(message: str) -> None:
    print(f"common-sdk-contract: {message}", file=sys.stderr)
    sys.exit(1)

for header in (COMMON / "include" / "msconnector").glob("*.h"):
    text = header.read_text(encoding="utf-8")
    guard = "MSCONNECTOR_" + header.stem.upper() + "_H"
    if f"#ifndef {guard}" not in text or f"#define {guard}" not in text:
        fail(f"missing include guard {guard} in {header.relative_to(ROOT)}")

for source in (COMMON / "src").glob("*.c"):
    text = source.read_text(encoding="utf-8")
    expected = f'#include "msconnector/{source.stem}.h"'
    if expected not in text:
        fail(f"missing matching header include {expected} in {source.relative_to(ROOT)}")

for path in list((COMMON / "include").rglob("*")) + list((COMMON / "src").rglob("*")):
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                fail(f"forbidden connector-specific token {token!r} in {path.relative_to(ROOT)}")

print("common-sdk-contract: pass")
