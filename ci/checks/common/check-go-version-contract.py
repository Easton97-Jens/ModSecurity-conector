#!/usr/bin/env python3
"""Fail closed on drift in the Parent CodeQL Go toolchain selector."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


CANONICAL_VERSION_FILE = ".go-version"
CODEQL_WORKFLOW = Path(".github/workflows/ci-security-codeql.yml")
SETUP_GO_REFERENCE = "actions/setup-go@b7ad1dad31e06c5925ef5d2fc7ad053ef454303e # v7.0.0"
EXPECTED_JOBS = frozenset({"envoy-go", "traefik-go"})
VERSION_RE = re.compile(r"^1\.26\.(?:0|[1-9]\d*)$", re.ASCII)
JOB_HEADER = re.compile(r"^ {2}(?P<name>[A-Za-z0-9_-]+):\s*$")
SETUP_GO_PREFIX = "      - uses: actions/setup-go@"
EXPECTED_SETUP_GO_BODY = "\n".join(
    (
        "        with:",
        "          go-version-file: .go-version",
        "          check-latest: false",
    )
)


class ContractError(ValueError):
    """Raised when an input does not satisfy the narrow static contract."""


@dataclass(frozen=True)
class Result:
    version: str
    violations: tuple[str, ...]


@dataclass(frozen=True)
class SetupGoStep:
    """One exact-indentation setup-go step and its indented body."""

    reference: str
    body: str


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_canonical_version(root: Path) -> str:
    try:
        root_stat = os.lstat(root)
    except OSError as error:
        raise ContractError("repository root cannot be inspected safely") from error
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise ContractError("repository root must be a real directory")
    target = root / CANONICAL_VERSION_FILE
    try:
        before_open = os.lstat(target)
    except OSError as error:
        raise ContractError("root .go-version cannot be inspected safely") from error
    if not stat.S_ISREG(before_open.st_mode):
        raise ContractError("root .go-version must be a regular non-symlink file")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ContractError("platform cannot safely open .go-version without following symlinks")
    descriptor: int | None = None
    try:
        descriptor = os.open(target, os.O_RDONLY | nofollow)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(before_open, opened):
            raise ContractError("root .go-version changed while being opened")
        body = os.read(descriptor, 65)
    except ContractError:
        raise
    except OSError as error:
        raise ContractError("root .go-version cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if len(body) > 64:
        raise ContractError("root .go-version is unexpectedly large")
    try:
        value = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError("root .go-version is not UTF-8") from error
    if value.endswith("\n"):
        value = value[:-1]
    if not VERSION_RE.fullmatch(value):
        raise ContractError("root .go-version must be an exact stable Go 1.26 patch")
    return value


def job_blocks(text: str) -> dict[str, str]:
    """Split the small stable top-level jobs mapping without YAML execution."""

    blocks: dict[str, list[str]] = {}
    current: str | None = None
    in_jobs = False
    for line in text.splitlines():
        if line == "jobs:":
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            break
        match = JOB_HEADER.match(line)
        if match:
            current = match.group("name")
            blocks[current] = [line]
        elif current is not None:
            blocks[current].append(line)
    return {name: "\n".join(lines) for name, lines in blocks.items()}


def setup_go_blocks(job: str) -> list[SetupGoStep]:
    """Extract setup-go steps without multiline-regex boundary ambiguity."""

    lines = job.splitlines()
    steps: list[SetupGoStep] = []
    for index, line in enumerate(lines):
        if not line.startswith(SETUP_GO_PREFIX):
            continue
        body_lines: list[str] = []
        for body_line in lines[index + 1 :]:
            if body_line.startswith("      - "):
                break
            body_lines.append(body_line)
        steps.append(
            SetupGoStep(
                reference=line.removeprefix("      - uses: ").strip(),
                body="\n".join(body_lines),
            )
        )
    return steps


def job_violations(job_name: str, job: str) -> list[str]:
    violations: list[str] = []
    setup_steps = setup_go_blocks(job)
    if len(setup_steps) != 1:
        return [f"{job_name} must contain exactly one actions/setup-go step"]
    setup = setup_steps[0]
    reference = setup.reference
    if reference != SETUP_GO_REFERENCE:
        violations.append(f"{job_name} must use exactly {SETUP_GO_REFERENCE}")
    body = setup.body
    if body != EXPECTED_SETUP_GO_BODY:
        violations.append(
            f"{job_name} must use only the exact central .go-version selector inputs"
        )
    return violations


def evaluate(root: Path) -> Result:
    version = read_canonical_version(root)
    workflow_path = root / CODEQL_WORKFLOW
    try:
        workflow_stat = os.lstat(workflow_path)
        if not stat.S_ISREG(workflow_stat.st_mode):
            raise ContractError("CodeQL workflow must be a regular non-symlink file")
        text = workflow_path.read_text(encoding="utf-8")
    except ContractError:
        raise
    except (OSError, UnicodeDecodeError) as error:
        raise ContractError("CodeQL workflow cannot be read safely") from error

    blocks = job_blocks(text)
    violations: list[str] = []
    for job_name in sorted(EXPECTED_JOBS):
        job = blocks.get(job_name)
        if job is None:
            violations.append(f"CodeQL workflow lacks expected Go job {job_name}")
            continue
        violations.extend(job_violations(job_name, job))
    for job_name, job in sorted(blocks.items()):
        if "actions/setup-go@" in job and job_name not in EXPECTED_JOBS:
            violations.append(f"unlisted CodeQL Go selector job: {job_name}")
    return Result(version=version, violations=tuple(violations))


def emit(payload: dict[str, object], output: TextIO) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=output)


def main(argv: list[str] | None = None, *, output: TextIO | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit a stable JSON result")
    args = parser.parse_args(argv)
    stream = sys.stdout if output is None else output
    try:
        result = evaluate(repository_root())
    except ContractError as error:
        payload = {"status": "error", "error": str(error)}
        if args.json:
            emit(payload, stream)
        else:
            print(payload["error"], file=stream)
        return 2
    payload: dict[str, object] = {
        "status": "passed" if not result.violations else "failed",
        "version": result.version,
        "violations": list(result.violations),
    }
    if args.json:
        emit(payload, stream)
    else:
        for violation in result.violations:
            print(violation, file=stream)
    return 0 if not result.violations else 2


if __name__ == "__main__":
    raise SystemExit(main())
