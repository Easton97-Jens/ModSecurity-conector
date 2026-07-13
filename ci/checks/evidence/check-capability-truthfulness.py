#!/usr/bin/env python3
"""Check that the capability contract file exists without claiming connector pass status."""
from pathlib import Path
import json
ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
path = ROOT / "config/testing/capability-contract.json"
data = json.loads(path.read_text(encoding="utf-8"))
assert "capabilities" in data
print("capability-truthfulness: contract present; no connector pass claims")
