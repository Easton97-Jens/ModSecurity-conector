#!/usr/bin/env python3
"""Detect a compiler flag for a logical C standard profile."""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

PROFILES = {
    "c17": ("-std=c17", "-std=c18"),
    "c23": ("-std=c23", "-std=c2x"),
    "c2y": ("-std=c2y", "-std=gnu2y"),
}
INVALID = {
    "c20": "c20 is not a portable ISO C compiler mode; use c23/c2x for C or c++20 for C++.",
    "c26": "c26 is not the current GCC C mode; use c2y/gnu2y for future C or c++26 for C++.",
}


def compiler_supports(cc: str, flag: str) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "detect.c"
        binary = Path(tmp) / "detect"
        source.write_text("int main(void) { return 0; }\n", encoding="utf-8")
        result = subprocess.run(
            [cc, flag, str(source), "-o", str(binary)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    parser.add_argument("--cc", default="cc")
    args = parser.parse_args()

    profile = args.profile.lower()
    if profile in INVALID:
        print(f"INVALID: {INVALID[profile]}", file=sys.stderr)
        return 2

    flags = PROFILES.get(profile)
    if flags is None:
        print(f"INVALID: unknown C standard profile {args.profile!r}", file=sys.stderr)
        return 2

    for flag in flags:
        if compiler_supports(args.cc, flag):
            print(flag)
            return 0

    print(
        f"SKIPPED: optional {profile} check — compiler does not support {' or '.join(flags)}",
        file=sys.stderr,
    )
    return 77


if __name__ == "__main__":
    raise SystemExit(main())
