#!/usr/bin/env python3
"""Emit ordinary revision pins only after exact-checkout provenance verification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ci/lib"))
from framework_revision_pins import (  # noqa: E402
    FrameworkRevisionPinsError,
    verify_framework_revision_pins,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--parent-sha", required=True)
    parser.add_argument("--format", choices=("json", "github-output"), default="json")
    arguments = parser.parse_args()
    try:
        pins = verify_framework_revision_pins(ROOT, arguments.parent_sha)
    except FrameworkRevisionPinsError as exc:
        parser.exit(1, f"Framework revision verification failed: {exc}\n")
    if arguments.format == "github-output":
        print(f"framework_sha={pins['framework_sha']}\nmrts_sha={pins['mrts_sha']}")
    else:
        print(json.dumps(pins, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
