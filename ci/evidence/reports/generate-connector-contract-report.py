#!/usr/bin/env python3
"""Print a static connector contract skeleton without runtime claims."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
contract = json.loads((ROOT / "config/testing/capability-contract.json").read_text(encoding="utf-8"))
print(json.dumps({"runtime_verified": False, "capabilities": contract.get("capabilities", {}), "required_tests": contract.get("capabilities", {})}, sort_keys=True))
