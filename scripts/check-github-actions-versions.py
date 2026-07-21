#!/usr/bin/env python3
"""Read-only compatibility wrapper for the Parent CI-tool update check."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_updater_module():
    script = Path(__file__).with_name("update-github-actions-versions.py")
    spec = importlib.util.spec_from_file_location("update_github_actions_versions", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    module = load_updater_module()
    arguments = list(argv if argv is not None else sys.argv[1:])
    if "--apply" in arguments or "--validate" in arguments:
        raise SystemExit("the check wrapper permits only read-only updater modes")
    if "--check" not in arguments and "--verify" not in arguments and "--resolve" not in arguments:
        arguments.insert(0, "--check")
    return module.main(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
