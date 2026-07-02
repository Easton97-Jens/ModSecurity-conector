#!/usr/bin/env python3
"""Conservative adapter contract scaffold check."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "common/include/msconnector/adapter_contract.h",
    ROOT / "common/src/adapter_contract.c",
]

missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.exists()]
if missing:
    for path in missing:
        print(f"missing adapter contract file: {path}")
    raise SystemExit(1)
print("adapter-contracts: common scaffolding present; connectors not yet adopted")
