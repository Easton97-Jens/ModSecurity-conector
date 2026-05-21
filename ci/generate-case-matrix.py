#!/usr/bin/env python3
"""Compatibility wrapper for the external ModSecurity test framework generator."""

from __future__ import annotations

import os
import sys
from pathlib import Path


CONNECTOR_ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK_ROOT = Path(os.environ.get("FRAMEWORK_ROOT", CONNECTOR_ROOT.parent / "ModSecurity-test-Framework")).resolve()
TARGET = FRAMEWORK_ROOT / "ci" / "generate-case-matrix.py"

if not TARGET.exists():
    raise SystemExit(f"blocked: FRAMEWORK_ROOT does not contain {TARGET.relative_to(FRAMEWORK_ROOT)}: {FRAMEWORK_ROOT}")

os.execv(
    sys.executable,
    [
        sys.executable,
        str(TARGET),
        "--framework-root",
        str(FRAMEWORK_ROOT),
        "--connector-root",
        str(CONNECTOR_ROOT),
        "--output-root",
        str(CONNECTOR_ROOT),
        *sys.argv[1:],
    ],
)
