#!/usr/bin/env python3
"""Fail-closed runner preflight for the protected exact-head NGINX workflow.

This program is part of the protected Base.  It deliberately consumes no
candidate checkout and does not try to infer that a generic runner is safe.
Instead it validates the properties that can be observed locally before a
candidate build or a privileged cell starts: a fixed, scrubbed environment, a
private run directory, a checked-out Base revision, and the absence of common
host-control sockets.  Provisioning a disposable runner and a GitHub
Environment remains an external, reviewable prerequisite.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
ROLES = frozenset({"candidate-build", "privileged"})
REQUIRED_ENV = {
    "PATH": "/usr/bin:/bin",
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
}
OPTIONAL_ENV = frozenset({"RUNNER_TEMP"})
HOST_CONTROL_PATHS = (
    Path("/var/run/docker.sock"),
    Path("/run/docker.sock"),
    Path("/run/containerd/containerd.sock"),
    Path("/var/run/podman/podman.sock"),
    Path("/run/podman/podman.sock"),
)
# This executable is provisioned outside the checkout by the protected runner
# owner.  It must snapshot and verify the exact Base Git blob before invoking
# any checkout-resident code as root; a runner-local copy is not trusted.
HOST_GATE_PATH = Path(
    "/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher"
)


class PreflightError(RuntimeError):
    """The runner does not satisfy the protected-cell admission contract."""


def fail(message: str) -> None:
    raise PreflightError(message)


def require_sha40(value: str, label: str) -> str:
    if SHA40_RE.fullmatch(value) is None:
        fail(f"{label} must be a lowercase 40-character SHA")
    return value


def normalized_absolute(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        fail(f"{label} must be an absolute normalized path")
    result = Path(os.path.normpath(os.fspath(path)))
    if result == Path("/"):
        fail(f"{label} must not be filesystem root")
    return result


def no_symlink_chain(path: Path, label: str, *, missing_leaf: bool = False) -> Path:
    path = normalized_absolute(os.fspath(path), label)
    current = Path(path.root)
    for index, part in enumerate(path.parts[1:]):
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            if missing_leaf and index == len(path.parts) - 2:
                return path
            fail(f"{label} component is missing")
        if stat.S_ISLNK(metadata.st_mode):
            fail(f"{label} contains a symbolic link")
    return path


def require_scrubbed_environment() -> None:
    allowed = set(REQUIRED_ENV) | set(OPTIONAL_ENV)
    unexpected = set(os.environ) - allowed
    if unexpected:
        fail("runner environment contains a non-allowlisted variable")
    for key, expected in REQUIRED_ENV.items():
        if os.environ.get(key) != expected:
            fail(f"runner environment does not provide fixed {key}")
    runner_temp = os.environ.get("RUNNER_TEMP")
    if not runner_temp:
        fail("runner environment lacks RUNNER_TEMP")
    no_symlink_chain(Path(runner_temp), "RUNNER_TEMP")


def reject_host_control_sockets() -> None:
    for path in HOST_CONTROL_PATHS:
        try:
            path.lstat()
        except FileNotFoundError:
            continue
        except OSError as exc:
            fail(f"cannot inspect host-control path: {exc}")
        # Treat any pre-existing entry at one of these fixed control locations
        # as unsafe.  A non-socket replacement is not a harmless exception.
        fail("runner exposes a host-control socket path")


def require_private_task_root(value: str) -> Path:
    root = no_symlink_chain(Path(value), "task root", missing_leaf=True)
    runner_temp = no_symlink_chain(Path(os.environ["RUNNER_TEMP"]), "RUNNER_TEMP")
    try:
        root.relative_to(runner_temp)
    except ValueError:
        fail("task root must be below RUNNER_TEMP")
    if root.exists():
        metadata = root.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            fail("task root is not a non-symlink directory")
        if (
            metadata.st_uid != os.geteuid()
            or metadata.st_gid != os.getegid()
            or metadata.st_mode & 0o077
        ):
            fail("task root is not private to the invoking runner identity")
        if any(root.iterdir()):
            fail("task root must be fresh")
    else:
        try:
            root.mkdir(mode=0o700)
        except OSError as exc:
            fail(f"cannot create private task root: {exc}")
        metadata = root.lstat()
        if (
            stat.S_IMODE(metadata.st_mode) != 0o700
            or metadata.st_uid != os.geteuid()
            or metadata.st_gid != os.getegid()
        ):
            fail("new task root does not have private ownership or mode")
    return root


def require_base_checkout(value: str, expected_sha: str) -> Path:
    root = no_symlink_chain(Path(value), "trusted Base checkout")
    metadata = root.lstat()
    if not stat.S_ISDIR(metadata.st_mode) or metadata.st_mode & 0o022:
        fail("trusted Base checkout is not a safe directory")
    git = Path("/usr/bin/git")
    try:
        git_stat = git.lstat()
    except OSError as exc:
        fail(f"fixed git is unavailable: {exc}")
    if not stat.S_ISREG(git_stat.st_mode) or git_stat.st_mode & 0o022:
        fail("fixed git executable is unsafe")
    try:
        completed = subprocess.run(
            [os.fspath(git), "-C", os.fspath(root), "rev-parse", "HEAD^{commit}"],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=dict(REQUIRED_ENV),
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"cannot verify trusted Base checkout: {exc}")
    observed = completed.stdout.strip()
    if completed.returncode != 0 or observed != require_sha40(expected_sha, "trusted Base SHA"):
        fail("trusted Base checkout is not at the expected immutable revision")
    return root


def require_host_gate() -> Path:
    """Admit only the preinstalled, root-owned privilege bootstrap."""

    gate = no_symlink_chain(HOST_GATE_PATH, "protected host gate")
    try:
        metadata = gate.lstat()
    except OSError as exc:
        fail(f"protected host gate is unavailable: {exc}")
    if not stat.S_ISREG(metadata.st_mode):
        fail("protected host gate is not a regular file")
    if metadata.st_uid != 0 or metadata.st_gid != 0:
        fail("protected host gate is not root-owned")
    if stat.S_IMODE(metadata.st_mode) != 0o755:
        fail("protected host gate does not have mode 0755")
    return gate


def prepare(role: str, task_root: str, base_repo_root: str, trusted_base_sha: str) -> Path:
    if role not in ROLES:
        fail("runner role is unsupported")
    trusted_base_sha = require_sha40(trusted_base_sha, "trusted Base SHA")
    require_scrubbed_environment()
    reject_host_control_sockets()
    require_base_checkout(base_repo_root, trusted_base_sha)
    if role == "privileged":
        require_host_gate()
    root = require_private_task_root(task_root)
    # These paths are prepared before any candidate checkout/build and are
    # deliberately direct, private children of the fresh run root.
    for name in ("candidate", "artifacts", "evidence", "logs"):
        child = root / name
        try:
            child.mkdir(mode=0o700)
        except OSError as exc:
            fail(f"cannot create protected run directory: {exc}")
    return root


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=sorted(ROLES), required=True)
    parser.add_argument("--task-root", required=True)
    parser.add_argument("--base-repo-root", required=True)
    parser.add_argument("--trusted-base-sha", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = parse_args(argv)
        prepare(arguments.role, arguments.task_root, arguments.base_repo_root,
                arguments.trusted_base_sha)
    except PreflightError as exc:
        print(f"protected exact-head runner preflight: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
