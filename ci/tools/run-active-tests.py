#!/usr/bin/env python3
"""Run only selectors admitted by the complete Parent active-case inventory."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ci.lib.active_test_inventory import main


if __name__ == "__main__":
    raise SystemExit(main(root=ROOT))
