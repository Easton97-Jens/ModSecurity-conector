#!/usr/bin/env python3
"""Fail-closed checks for a read-only submodule-update candidate.

The caller supplies the Parent baseline captured before the candidate runs.
Only the Framework worktree may differ from the Parent's recorded gitlink.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Sequence


FULL_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
FULL_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class ValidationError(RuntimeError):
    """An expected validation failure with a stable machine-readable code."""

    def __init__(self, code: str, details: dict[str, object] | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.details = details or {}


def _fail(code: str, **details: object) -> None:
    raise ValidationError(code, details)


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", os.fspath(root), *arguments],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if completed.returncode:
        _fail("GIT_COMMAND_FAILED")
    return completed.stdout


def _git_status(root: Path, *arguments: str) -> int:
    completed = subprocess.run(
        ["git", "-C", os.fspath(root), *arguments],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode


def _repository_root(root: Path, code: str) -> None:
    if not root.is_dir():
        _fail(code)
    try:
        actual = Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve(strict=True)
    except (OSError, ValidationError):
        _fail(code)
    if actual != root.resolve(strict=True):
        _fail(code)


def _hooks_digest(root: Path) -> str:
    hooks = Path(_git(root, "rev-parse", "--git-path", "hooks").strip())
    if not hooks.is_absolute():
        hooks = root / hooks
    try:
        metadata = os.lstat(hooks)
    except FileNotFoundError:
        _fail("PARENT_HOOKS_MISSING")
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        _fail("PARENT_HOOKS_UNSAFE")
    inventory: list[tuple[str, int, str]] = []

    def visit(directory: Path, relative: str) -> None:
        directory_metadata = os.lstat(directory)
        if not stat.S_ISDIR(directory_metadata.st_mode) or stat.S_ISLNK(directory_metadata.st_mode):
            _fail("PARENT_HOOKS_UNSAFE")
        inventory.append((relative, stat.S_IMODE(directory_metadata.st_mode), "directory"))
        for entry in sorted(os.scandir(directory), key=lambda candidate: candidate.name):
            path = Path(entry.path)
            child_relative = entry.name if relative == "." else f"{relative}/{entry.name}"
            metadata = os.lstat(path)
            if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                visit(path, child_relative)
            elif stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                inventory.append((child_relative, stat.S_IMODE(metadata.st_mode), hashlib.sha256(path.read_bytes()).hexdigest()))
            else:
                _fail("PARENT_HOOKS_UNSAFE")

    visit(hooks, ".")
    canonical = "".join(f"{name}\0{mode:o}\0{digest}\n" for name, mode, digest in inventory)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _head_gitlink(root: Path, submodule_path: str) -> str:
    """Return the Gitlink recorded by ``HEAD``, never an index-side value."""

    output = _git(root, "ls-tree", "HEAD", "--", submodule_path).splitlines()
    if len(output) != 1:
        _fail("PARENT_GITLINK_MISSING")
    fields = output[0].split(None, 3)
    if len(fields) != 4 or fields[0] != "160000" or fields[1] != "commit" or fields[3] != submodule_path:
        _fail("PARENT_GITLINK_INVALID")
    return fields[2]


def _relative_path(value: str, code: str) -> str:
    path = Path(value)
    if (
        not value
        or path.is_absolute()
        or os.path.normpath(value) != value
        or any(part in {"", ".", ".."} for part in path.parts)
        or value.startswith(":")
    ):
        _fail(code)
    return value


def _require_full_revision(value: str, code: str) -> str:
    if not FULL_SHA1.fullmatch(value):
        _fail(code)
    return value


def _diagnostic_paths(root: Path, arguments: Sequence[str]) -> list[str]:
    """Return a bounded list of Git paths only, never source-file content."""

    return [line for line in _git(root, *arguments).splitlines() if line][:20]


def _require_clean(
    root: Path,
    code: str,
    pathspec: Sequence[str] = (),
    *,
    scope: str,
    index_scope: str | None = None,
) -> None:
    suffix = ["--", *pathspec] if pathspec else []
    if _git_status(root, "diff", "--quiet", *suffix) != 0:
        _fail(
            code,
            scope=scope,
            state="worktree",
            paths=_diagnostic_paths(root, ("diff", "--name-only", *suffix)),
        )
    # The sole expected candidate difference is an *unstaged* Framework
    # worktree Gitlink divergence.  The index itself must be clean globally;
    # applying an exclusion here would permit a staged nested Gitlink bypass.
    if _git_status(root, "diff", "--cached", "--quiet") != 0:
        _fail(
            code,
            scope=index_scope or scope,
            state="index",
            paths=_diagnostic_paths(root, ("diff", "--cached", "--name-only")),
        )
    untracked_paths = _diagnostic_paths(root, ("ls-files", "--others", "--exclude-standard", *suffix))
    if untracked_paths:
        _fail(
            code,
            scope=scope,
            state="untracked",
            paths=untracked_paths,
        )


def _validate_gitmodules(root: Path, submodule_path: str) -> None:
    if not (root / ".gitmodules").is_file():
        _fail("PARENT_GITMODULES_MISSING", path=".gitmodules")
    paths = _git(root, "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$")
    configured = [line.split(None, 1)[1] for line in paths.splitlines() if " " in line]
    if configured.count(submodule_path) != 1:
        _fail("PARENT_GITMODULES_INVALID", path=".gitmodules", expected_path=submodule_path)


def _validate_parent(arguments: argparse.Namespace) -> Path:
    parent = Path(arguments.parent_root).resolve(strict=False)
    arguments.submodule_path = _relative_path(arguments.submodule_path, "SUBMODULE_PATH_INVALID")
    arguments.current_gitlink_sha = _require_full_revision(
        arguments.current_gitlink_sha, "CURRENT_GITLINK_SHA_INVALID"
    )
    arguments.candidate_sha = _require_full_revision(arguments.candidate_sha, "CANDIDATE_SHA_INVALID")
    arguments.expected_parent_head = _require_full_revision(
        arguments.expected_parent_head, "EXPECTED_PARENT_HEAD_INVALID"
    )
    if not FULL_SHA256.fullmatch(arguments.expected_parent_hooks_sha256):
        _fail("EXPECTED_PARENT_HOOKS_SHA256_INVALID")
    _repository_root(parent, "PARENT_ROOT_INVALID")
    actual_parent_head = _git(parent, "rev-parse", "HEAD").strip()
    if actual_parent_head != arguments.expected_parent_head:
        _fail(
            "PARENT_HEAD_CHANGED",
            expected_head=arguments.expected_parent_head,
            actual_head=actual_parent_head,
        )
    actual_hooks_digest = _hooks_digest(parent)
    if actual_hooks_digest != arguments.expected_parent_hooks_sha256:
        _fail(
            "PARENT_HOOKS_CHANGED",
            path=".git/hooks",
            expected_sha256=arguments.expected_parent_hooks_sha256,
            actual_sha256=actual_hooks_digest,
        )
    _validate_gitmodules(parent, arguments.submodule_path)
    actual_gitlink = _head_gitlink(parent, arguments.submodule_path)
    if actual_gitlink != arguments.current_gitlink_sha:
        _fail(
            "PARENT_GITLINK_CHANGED",
            path=arguments.submodule_path,
            expected_gitlink=arguments.current_gitlink_sha,
            actual_gitlink=actual_gitlink,
        )
    _require_clean(
        parent,
        "PARENT_OUTSIDE_SUBMODULE_DIRTY",
        (".", f":(exclude){arguments.submodule_path}"),
        scope="parent-outside-submodule",
        index_scope="parent-index",
    )
    return parent


def _submodule_paths(root: Path) -> list[str]:
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return []
    result = _git(root, "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$")
    paths = []
    for line in result.splitlines():
        key, separator, value = line.partition(" ")
        if not separator or not value or not key.endswith(".path"):
            _fail("FRAMEWORK_SUBMODULE_METADATA_INVALID")
        paths.append(_relative_path(value, "FRAMEWORK_SUBMODULE_METADATA_INVALID"))
    return paths


def _validate_nested(root: Path) -> None:
    paths = _submodule_paths(root)
    _require_clean(
        root, "FRAMEWORK_SUBMODULE_DIRTY",
        (".", *(f":(exclude){relative}" for relative in paths)),
        scope="framework-submodule-container",
    )
    for relative in paths:
        path = root / relative
        if not path.is_dir():
            _fail("FRAMEWORK_SUBMODULE_UNINITIALIZED")
        _repository_root(path, "FRAMEWORK_SUBMODULE_INVALID")
        expected_gitlink = _head_gitlink(root, relative)
        actual_head = _git(path, "rev-parse", "HEAD").strip()
        if expected_gitlink != actual_head:
            _fail(
                "FRAMEWORK_SUBMODULE_COMMIT_MISMATCH",
                path=relative,
                expected_gitlink=expected_gitlink,
                actual_head=actual_head,
            )
        _require_clean(
            path,
            "FRAMEWORK_SUBMODULE_DIRTY",
            scope=f"framework-submodule:{relative}",
            index_scope=f"framework-submodule-index:{relative}",
        )
        _validate_nested(path)


def _validate_framework(parent: Path, arguments: argparse.Namespace) -> None:
    framework = parent / arguments.submodule_path
    _repository_root(framework, "FRAMEWORK_ROOT_INVALID")
    actual_candidate_head = _git(framework, "rev-parse", "HEAD").strip()
    if actual_candidate_head != arguments.candidate_sha:
        _fail(
            "FRAMEWORK_CANDIDATE_MISMATCH",
            path=arguments.submodule_path,
            expected_candidate=arguments.candidate_sha,
            actual_head=actual_candidate_head,
        )
    paths = _submodule_paths(framework)
    _require_clean(
        framework, "FRAMEWORK_DIRTY",
        (".", *(f":(exclude){relative}" for relative in paths)),
        scope="framework-root",
        index_scope="framework-index",
    )
    _validate_nested(framework)


def capture_parent_baseline(arguments: argparse.Namespace) -> None:
    parent = Path(arguments.parent_root).resolve(strict=False)
    _repository_root(parent, "PARENT_ROOT_INVALID")
    environment = Path(arguments.github_env)
    if not environment.parent.is_dir() or environment.is_symlink():
        _fail("GITHUB_ENV_INVALID")
    head = _git(parent, "rev-parse", "HEAD").strip()
    digest = _hooks_digest(parent)
    try:
        with environment.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"EXPECTED_PARENT_HEAD={head}\n")
            stream.write(f"EXPECTED_PARENT_HOOKS_SHA256={digest}\n")
    except OSError:
        _fail("GITHUB_ENV_WRITE_FAILED")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    capture = modes.add_parser("capture-parent-baseline")
    capture.add_argument("--parent-root", required=True)
    capture.add_argument("--github-env", required=True)
    validate = modes.add_parser("validate")
    validate.add_argument("--parent-root", required=True)
    validate.add_argument("--submodule-path", required=True)
    validate.add_argument("--current-gitlink-sha", required=True)
    validate.add_argument("--candidate-sha", required=True)
    validate.add_argument("--expected-parent-head", required=True)
    validate.add_argument("--expected-parent-hooks-sha256", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    try:
        arguments = parse_args(argv)
        if arguments.mode == "capture-parent-baseline":
            capture_parent_baseline(arguments)
        else:
            parent = _validate_parent(arguments)
            _validate_framework(parent, arguments)
    except ValidationError as error:
        details = " ".join(
            f"{key}={json.dumps(value, ensure_ascii=True, separators=(',', ':'))}"
            for key, value in sorted(error.details.items())
        )
        print(f"ERROR:{error.code}" + (f" {details}" if details else ""), file=sys.stderr)
        return 1
    except (OSError, ValueError):
        print("ERROR:VALIDATOR_INTERNAL_ERROR", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
