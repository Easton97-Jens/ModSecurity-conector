#!/usr/bin/env python3
"""Fail closed when a CI job is not running the requested Python interpreter."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Sequence


EXACT_PYTHON_313 = re.compile(r"3\.13\.(?:0|[1-9][0-9]*)\Z")
PROBE_SCRIPT = (
    "import sys; "
    "print(sys.executable); "
    "print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
)


class ContractInputError(ValueError):
    """Raised when a canonical-version input is missing or malformed."""


def exact_version(value: str, source: str) -> str:
    """Return an exact supported version or raise a deterministic input error."""

    if not EXACT_PYTHON_313.fullmatch(value):
        raise ContractInputError(
            f"{source} must contain an exact Python 3.13.N version; got {value!r}"
        )
    return value


def read_version_file(path: Path) -> str:
    """Read one exact version, permitting only the conventional final newline."""

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractInputError(f"cannot read version file {path}: {exc}") from exc

    if content.endswith("\n"):
        content = content[:-1]
    if "\n" in content or "\r" in content:
        raise ContractInputError(
            f"version file {path} must contain one exact version and an optional final newline"
        )
    return exact_version(content, f"version file {path}")


def version_from_info(info: object) -> str:
    """Format the public version fields without relying on implementation details."""

    return f"{info.major}.{info.minor}.{info.micro}"


def same_interpreter(left: str | Path, right: str | Path) -> bool:
    """Use samefile where possible, with a safe canonical-path fallback."""

    try:
        return os.path.samefile(left, right)
    except (AttributeError, OSError):
        return os.path.normcase(os.path.realpath(left)) == os.path.normcase(
            os.path.realpath(right)
        )


def executable_path(argument: str, label: str, violations: list[str]) -> Path | None:
    """Validate a caller-supplied executable path without invoking a shell."""

    candidate = Path(argument)
    if not candidate.is_absolute():
        violations.append(f"{label} must be an absolute path: {argument!r}")
        return None
    if not candidate.is_file():
        violations.append(f"{label} is not a regular file: {candidate}")
        return None
    if not os.access(candidate, os.X_OK):
        violations.append(f"{label} is not executable: {candidate}")
        return None
    return candidate


def probe_interpreter(
    executable: Path,
    label: str,
    expected_version: str,
    reference: Path,
    violations: list[str],
) -> None:
    """Run a bounded, argument-vector-only interpreter identity probe."""

    try:
        completed = subprocess.run(
            [str(executable), "-c", PROBE_SCRIPT],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        violations.append(f"{label} could not be executed safely: {exc}")
        return

    if completed.returncode != 0:
        violations.append(f"{label} probe exited with status {completed.returncode}")
        return

    lines = completed.stdout.splitlines()
    if len(lines) != 2:
        violations.append(f"{label} probe returned an unexpected identity record")
        return

    reported_executable, reported_version = lines
    if reported_version != expected_version:
        violations.append(
            f"{label} reports Python {reported_version}, expected {expected_version}"
        )
    if not reported_executable or not same_interpreter(reported_executable, reference):
        violations.append(
            f"{label} runs {reported_executable or '<empty>'}, not {reference}"
        )


def check_command_alias(
    command: str,
    expected_version: str,
    reference: Path,
    violations: list[str],
) -> None:
    """Verify that a PATH command points at and runs the current interpreter."""

    resolved = shutil.which(command)
    if not resolved:
        violations.append(f"{command} does not resolve on PATH after setup-python")
        return

    resolved_path = Path(resolved)
    if not same_interpreter(resolved_path, reference):
        violations.append(f"{command} resolves to {resolved_path}, not {reference}")
    probe_interpreter(resolved_path, command, expected_version, reference, violations)


def check_pip(reference: Path, violations: list[str]) -> None:
    """Require the selected interpreter's pip module without using a bare pip command."""

    try:
        completed = subprocess.run(
            [str(reference), "-m", "pip", "--version"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        violations.append(f"{reference} -m pip --version could not run: {exc}")
        return
    if completed.returncode != 0:
        violations.append(f"{reference} -m pip --version exited with status {completed.returncode}")


def evaluate_contract(expected_version: str, expected_python: str | None) -> list[str]:
    """Return every observed contract violation rather than stopping at the first."""

    violations: list[str] = []
    current = version_from_info(sys.version_info)
    if current != expected_version:
        violations.append(
            f"current sys.version is Python {current}, expected {expected_version}"
        )

    reference = executable_path(sys.executable, "sys.executable", violations)
    if reference is None:
        return violations

    for command in ("python", "python3"):
        check_command_alias(command, expected_version, reference, violations)

    if expected_python is not None:
        action_python = executable_path(expected_python, "--expected-python", violations)
        if action_python is not None:
            if not same_interpreter(action_python, reference):
                violations.append(
                    f"--expected-python is {action_python}, not the current {reference}"
                )
            probe_interpreter(
                action_python,
                "--expected-python",
                expected_version,
                reference,
                violations,
            )

    check_pip(reference, violations)
    return violations


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Verify the exact Python interpreter selected by actions/setup-python."
    )
    version_source = argument_parser.add_mutually_exclusive_group()
    version_source.add_argument(
        "--version-file",
        metavar="PATH",
        help="canonical exact Python version file (default: .python-version)",
    )
    version_source.add_argument(
        "--expected-version",
        metavar="3.13.N",
        help="validated exact version for the one candidate-validation workflow",
    )
    argument_parser.add_argument(
        "--expected-python",
        metavar="ABSOLUTE_PATH",
        help="actions/setup-python's python-path output to compare with sys.executable",
    )
    argument_parser.add_argument("--json", action="store_true", help="emit a JSON result")
    return argument_parser


def report(status: str, expected_version: str | None, violations: list[str], as_json: bool) -> None:
    """Write either compact machine-readable data or clear actionable diagnostics."""

    if as_json:
        print(
            json.dumps(
                {
                    "status": status,
                    "expected_version": expected_version,
                    "sys_executable": sys.executable,
                    "violations": violations,
                },
                sort_keys=True,
            )
        )
        return

    if status == "valid":
        print(
            "python-interpreter-contract: valid "
            f"(Python {expected_version}; sys.executable={sys.executable})"
        )
        return
    for violation in violations:
        print(f"python-interpreter-contract: {violation}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.expected_version is not None:
            expected_version = exact_version(args.expected_version, "--expected-version")
        else:
            version_file = Path(args.version_file or ".python-version")
            expected_version = read_version_file(version_file)
    except ContractInputError as exc:
        report("error", None, [str(exc)], args.json)
        return 2

    violations = evaluate_contract(expected_version, args.expected_python)
    if violations:
        report("violations", expected_version, violations, args.json)
        return 1
    report("valid", expected_version, [], args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
