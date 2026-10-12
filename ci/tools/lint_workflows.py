#!/usr/bin/env python3
"""Lint original workflows with compatibility for GitHub self-repository uses.

Actionlint 1.7.12 predates GitHub's $/ syntax. Translate only those uses values
to its equivalent local-path syntax in memory; security audits read originals.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess

import yaml
from yaml.tokens import KeyToken, ScalarToken, ValueToken

PATH_COMPONENT = re.compile(r"^[A-Za-z0-9_.-]+$", re.ASCII)


def actionlint_source(source: str) -> str:
    """Normalize safe self-repository references without changing other text."""

    try:
        tokens = list(yaml.scan(source))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid workflow YAML: {exc}") from exc
    replacements: list[int] = []
    for index in range(1, len(tokens) - 2):
        key, separator, value = tokens[index:index + 3]
        if not (
            isinstance(tokens[index - 1], KeyToken)
            and isinstance(key, ScalarToken) and key.value == "uses"
            and isinstance(separator, ValueToken)
            and isinstance(value, ScalarToken) and value.value.startswith("$/")
        ):
            continue
        reference = value.value
        parts = reference[2:].split("/")
        if any(
            part in {"", ".", ".."} or PATH_COMPONENT.fullmatch(part) is None
            for part in parts
        ):
            raise ValueError(f"unsafe self-repository reference: {reference!r}")
        start, end = value.start_mark.index, value.end_mark.index
        relative = source[start:end].find(reference)
        if relative < 0:
            raise ValueError("self-repository uses must contain its literal path")
        replacements.append(start + relative)
    for offset in reversed(replacements):
        source = source[:offset] + "." + source[offset + 1:]
    return source


def lint(actionlint: str, workflows: list[Path]) -> int:
    """Check every workflow using stdin while retaining its filename and location."""

    shellcheck = shutil.which("shellcheck") or ""
    status = 0
    for workflow in workflows:
        source = actionlint_source(workflow.read_text(encoding="utf-8"))
        result = subprocess.run(
            [actionlint, f"-shellcheck={shellcheck}", "-stdin-filename", str(workflow), "-"],
            input=source,
            text=True,
            check=False,
            timeout=120,
        )
        if result.returncode:
            status = result.returncode if result.returncode > 0 else 1
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actionlint", required=True)
    parser.add_argument("workflows", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        return lint(args.actionlint, args.workflows)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"workflow lint failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
