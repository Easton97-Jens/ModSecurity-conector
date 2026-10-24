#!/usr/bin/env python3
"""Reject HAProxy Makefiles whose overlay anchor would require an offset."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ANCHOR_LINE = 999
EXPECTED_LINES = (
    "        src/hpack-huff.o src/hpack-enc.o src/ebtree.o src/hash.o\t\\",
    "        src/version.o src/ncbmbuf.o",
    "",
    "ifneq ($(TRACE),)",
    "  OBJS += src/calltrace.o",
    "endif",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--makefile", type=Path, required=True)
    args = parser.parse_args()

    try:
        lines = args.makefile.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"cannot read HAProxy Makefile: {exc}", file=sys.stderr)
        return 1

    actual = tuple(lines[ANCHOR_LINE - 1 : ANCHOR_LINE - 1 + len(EXPECTED_LINES)])
    if actual != EXPECTED_LINES:
        print(
            "HAProxy Makefile does not match the exact 3.2.22 overlay anchor; "
            "refusing offset or fuzzy patch application",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
