#!/usr/bin/env python3
"""Common-only origin governance scaffold check."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "common/include/msconnector/origin_governance.h",
    ROOT / "common/src/origin_governance.c",
    ROOT / "docs/generated/origin-governance.md",
    ROOT / "docs/generated/origin-governance.de.md",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    for item in missing: print(f"missing origin governance scaffold: {item}")
    raise SystemExit(1)
for path in sorted((ROOT / "connectors").glob("*")):
    if path.is_dir(): print(f"INFO: {path.relative_to(ROOT)} not enforced; common origin governance not yet adopted")
print("origin-governance: common scaffold present")
