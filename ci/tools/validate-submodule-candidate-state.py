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
GITMODULES_FILENAME = ".gitmodules"


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
    inventory: list[tuple[str, int, str]] = []
    _inventory_hook_directory(_hooks_directory(root), ".", inventory)
    canonical = "".join(f"{name}\0{mode:o}\0{digest}\n" for name, mode, digest in inventory)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _hooks_directory(root: Path) -> Path:
    hooks = Path(_git(root, "rev-parse", "--git-path", "hooks").strip())
    if not hooks.is_absolute():
        hooks = root / hooks
    try:
        metadata = os.lstat(hooks)
    except FileNotFoundError:
        _fail("PARENT_HOOKS_MISSING")
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        _fail("PARENT_HOOKS_UNSAFE")
    return hooks


def _inventory_hook_directory(
    directory: Path, relative: str, inventory: list[tuple[str, int, str]]
) -> None:
    metadata = os.lstat(directory)
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        _fail("PARENT_HOOKS_UNSAFE")
    inventory.append((relative, stat.S_IMODE(metadata.st_mode), "directory"))
    for entry in sorted(os.scandir(directory), key=lambda candidate: candidate.name):
        child_relative = entry.name if relative == "." else f"{relative}/{entry.name}"
        _inventory_hook_entry(Path(entry.path), child_relative, inventory)


def _inventory_hook_entry(path: Path, relative: str, inventory: list[tuple[str, int, str]]) -> None:
    metadata = os.lstat(path)
    if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
        _inventory_hook_directory(path, relative, inventory)
    elif stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
        inventory.append((relative, stat.S_IMODE(metadata.st_mode), hashlib.sha256(path.read_bytes()).hexdigest()))
    else:
        _fail("PARENT_HOOKS_UNSAFE")


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


def _open_directory_without_symlinks(path: Path, code: str) -> int:
    if not path.is_absolute() or os.path.normpath(os.fspath(path)) != os.fspath(path):
        _fail(code)
    current = Path(path.anchor)
    try:
        descriptor = os.open(current, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        for component in path.parts[1:]:
            next_descriptor = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
    except OSError:
        try:
            os.close(descriptor)
        except UnboundLocalError:
            pass
        _fail(code)
    return descriptor


def _trusted_runner_directory(descriptor: int, code: str) -> None:
    metadata = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.geteuid()
        or metadata.st_mode & 0o022
    ):
        _fail(code)


def _open_github_environment_file(value: str) -> int:
    runner_temp = Path(os.environ.get("RUNNER_TEMP", ""))
    if runner_temp == Path("/"):
        _fail("GITHUB_ENV_INVALID")
    runner_descriptor = _open_directory_without_symlinks(runner_temp, "GITHUB_ENV_INVALID")
    directory_descriptor = -1
    environment_descriptor = -1
    try:
        _trusted_runner_directory(runner_descriptor, "GITHUB_ENV_INVALID")

        environment = Path(value)
        if not environment.is_absolute() or os.path.normpath(value) != value:
            _fail("GITHUB_ENV_INVALID")
        try:
            relative = environment.relative_to(runner_temp)
        except ValueError:
            _fail("GITHUB_ENV_INVALID")
        if not relative.parts:
            _fail("GITHUB_ENV_INVALID")
        directory_descriptor = runner_descriptor
        runner_descriptor = -1
        for component in relative.parts[:-1]:
            next_descriptor = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_descriptor,
            )
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
            _trusted_runner_directory(directory_descriptor, "GITHUB_ENV_INVALID")
        environment_descriptor = os.open(
            relative.parts[-1],
            os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=directory_descriptor,
        )
        os.close(directory_descriptor)
        directory_descriptor = -1
        metadata = os.fstat(environment_descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_uid != os.geteuid()
            or metadata.st_mode & 0o022
            or metadata.st_nlink != 1
        ):
            _fail("GITHUB_ENV_INVALID")
        result = environment_descriptor
        environment_descriptor = -1
        return result
    except OSError:
        _fail("GITHUB_ENV_INVALID")
    finally:
        if runner_descriptor >= 0:
            os.close(runner_descriptor)
        if directory_descriptor >= 0:
            os.close(directory_descriptor)
        if environment_descriptor >= 0:
            os.close(environment_descriptor)


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
    if not (root / GITMODULES_FILENAME).is_file():
        _fail("PARENT_GITMODULES_MISSING", path=GITMODULES_FILENAME)
    paths = _git(root, "config", "-f", GITMODULES_FILENAME, "--get-regexp", r"^submodule\..*\.path$")
    configured = [line.split(None, 1)[1] for line in paths.splitlines() if " " in line]
    if configured.count(submodule_path) != 1:
        _fail("PARENT_GITMODULES_INVALID", path=GITMODULES_FILENAME, expected_path=submodule_path)


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
    gitmodules = root / GITMODULES_FILENAME
    if not gitmodules.is_file():
        return []
    result = _git(root, "config", "-f", GITMODULES_FILENAME, "--get-regexp", r"^submodule\..*\.path$")
    paths = []
    for line in result.splitlines():
        key, separator, value = line.partition(" ")
        if not separator or not value or not key.endswith(".path"):
            _fail("FRAMEWORK_SUBMODULE_METADATA_INVALID")
        paths.append(_relative_path(value, "FRAMEWORK_SUBMODULE_METADATA_INVALID"))
    return paths


def _tree_metadata(root: Path, revision: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return the reviewed tree's gitlinks and ``.gitmodules`` blobs.

    This deliberately reads Git's object database only.  It never asks Git to
    initialise, fetch, or recurse into a candidate-controlled submodule.
    """

    output = _git(root, "ls-tree", "-r", "-z", "--full-tree", revision)
    gitlinks: dict[str, str] = {}
    gitmodules: dict[str, str] = {}
    for entry in output.split("\0"):
        if not entry:
            continue
        header, separator, path = entry.partition("\t")
        fields = header.split()
        if not separator or len(fields) != 3 or not path:
            _fail("FRAMEWORK_SUBMODULE_METADATA_INVALID")
        mode, object_type, object_id = fields
        safe_path = _relative_path(path, "FRAMEWORK_SUBMODULE_METADATA_INVALID")
        if mode == "160000":
            if object_type != "commit" or not FULL_SHA1.fullmatch(object_id):
                _fail("FRAMEWORK_SUBMODULE_METADATA_INVALID")
            gitlinks[safe_path] = object_id
        if safe_path == GITMODULES_FILENAME or safe_path.endswith(f"/{GITMODULES_FILENAME}"):
            if object_type != "blob" or not FULL_SHA1.fullmatch(object_id):
                _fail("FRAMEWORK_SUBMODULE_METADATA_INVALID")
            gitmodules[safe_path] = object_id
    return gitlinks, gitmodules


def _validate_candidate_submodule_metadata(
    root: Path, current_revision: str, candidate_revision: str
) -> None:
    """Reject candidate changes to nested-submodule topology or gitlinks."""

    current_gitlinks, current_gitmodules = _tree_metadata(root, current_revision)
    candidate_gitlinks, candidate_gitmodules = _tree_metadata(root, candidate_revision)
    if current_gitlinks != candidate_gitlinks or current_gitmodules != candidate_gitmodules:
        changed_paths = sorted(
            {
                *set(current_gitlinks) ^ set(candidate_gitlinks),
                *set(current_gitmodules) ^ set(candidate_gitmodules),
                *{
                    path
                    for path in set(current_gitlinks) & set(candidate_gitlinks)
                    if current_gitlinks[path] != candidate_gitlinks[path]
                },
                *{
                    path
                    for path in set(current_gitmodules) & set(candidate_gitmodules)
                    if current_gitmodules[path] != candidate_gitmodules[path]
                },
            }
        )[:20]
        _fail(
            "FRAMEWORK_SUBMODULE_METADATA_CHANGED",
            paths=changed_paths,
        )


def _validate_nested(root: Path) -> None:
    paths = _submodule_paths(root)
    _require_clean(
        root, "FRAMEWORK_SUBMODULE_DIRTY",
        (".", *(f":(exclude){relative}" for relative in paths)),
        scope="framework-submodule-container",
    )
    for relative in paths:
        path = root / relative
        # A candidate's nested submodule must not be fetched merely to prove
        # that the candidate is safe.  Its topology and gitlink were compared
        # against the reviewed commit above; an absent worktree is therefore
        # an accepted, intentionally uninitialised state.
        if not path.exists():
            continue
        if not path.is_dir():
            _fail("FRAMEWORK_SUBMODULE_INVALID")
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
    _validate_candidate_submodule_metadata(
        framework, arguments.current_gitlink_sha, arguments.candidate_sha
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
    head = _git(parent, "rev-parse", "HEAD").strip()
    digest = _hooks_digest(parent)
    environment_descriptor = _open_github_environment_file(arguments.github_env)
    try:
        with os.fdopen(environment_descriptor, "a", encoding="utf-8", newline="\n") as stream:
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
