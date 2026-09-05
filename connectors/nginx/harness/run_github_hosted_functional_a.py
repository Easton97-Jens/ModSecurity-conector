#!/usr/bin/env python3
"""Launch the bounded GitHub-hosted NGINX functional-A root runtime.

This is deliberately not a broker or an adversarial attestation boundary.  It
only keeps the already-built, exact-head NGINX functional test from inheriting
the runner's ambient environment or re-running provisioning as root.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path
from typing import Mapping


_SAFE_PATH = "/usr/bin:/bin"
_SUDO = "/usr/bin/sudo"
_ENV = "/usr/bin/env"
_SHELL = "/bin/sh"
_PYTHON = "/usr/bin/python3"
_CURL = "/usr/bin/curl"
_WORKER_NAME_MAX = 64
_WORKER_NAME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-_")
_MODSECURITY_RUNTIME_LIBRARY = "libmodsecurity.so.3"
_FUNCTIONAL_PARENT_NAME = "ModSecurity-conector-nginx-functional-parent"
_FUNCTIONAL_ROOT_NAME = "nginx-hosted-functional-a"


class FunctionalALaunchError(ValueError):
    """The unprivileged preparation did not provide a bounded root input."""


def _has_unsafe_character(value: str) -> bool:
    return not value or any(character in value for character in ("\x00", "\r", "\n"))


def _require_worker_name(env: Mapping[str, str], name: str) -> str:
    value = str(env.get(name, ""))
    if (
        _has_unsafe_character(value)
        or len(value) > _WORKER_NAME_MAX
        or value[0] == "-"
        or any(character not in _WORKER_NAME_CHARS for character in value)
    ):
        raise FunctionalALaunchError(f"{name} is not a bounded local account name")
    return value


def _absolute_path(value: str, name: str) -> Path:
    if _has_unsafe_character(value):
        raise FunctionalALaunchError(f"{name} is empty or contains a control character")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise FunctionalALaunchError(f"{name} must be an absolute non-traversing path")
    return path


def _require_no_symlink_components(path: Path, name: str) -> Path:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        try:
            metadata = current.lstat()
        except OSError as error:
            raise FunctionalALaunchError(f"{name} is unavailable: {current}: {error}") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise FunctionalALaunchError(f"{name} contains a symbolic link: {current}")
    return path


def _require_under(path: Path, root: Path, name: str) -> Path:
    try:
        path.relative_to(root)
    except ValueError as error:
        raise FunctionalALaunchError(f"{name} must remain below VERIFIED_RUN_ROOT") from error
    return path


def _require_directory(path: Path, name: str) -> Path:
    _require_no_symlink_components(path, name)
    try:
        metadata = path.lstat()
    except OSError as error:
        raise FunctionalALaunchError(f"{name} is unavailable: {error}") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise FunctionalALaunchError(f"{name} must be a directory")
    return path


def _require_regular_executable(path: Path, name: str) -> Path:
    _require_no_symlink_components(path, name)
    try:
        metadata = path.lstat()
    except OSError as error:
        raise FunctionalALaunchError(f"{name} is unavailable: {error}") from error
    if not stat.S_ISREG(metadata.st_mode) or not os.access(path, os.X_OK):
        raise FunctionalALaunchError(f"{name} must be an executable regular file")
    return path


def _require_regular_file(path: Path, name: str) -> Path:
    _require_no_symlink_components(path, name)
    try:
        metadata = path.lstat()
    except OSError as error:
        raise FunctionalALaunchError(f"{name} is unavailable: {error}") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise FunctionalALaunchError(f"{name} must be a regular file")
    return path


def _require_worker_traversable_functional_parent(
    path: Path, verified_root: Path
) -> Path:
    """Accept only the workflow-created sibling for worker-visible runtime paths."""

    if path.name != _FUNCTIONAL_PARENT_NAME or path.parent != verified_root.parent:
        raise FunctionalALaunchError(
            "NGINX_FUNCTIONAL_A_PARENT_ROOT must be the designated sibling of VERIFIED_RUN_ROOT"
        )
    _require_directory(path, "NGINX_FUNCTIONAL_A_PARENT_ROOT")
    metadata = path.lstat()
    if metadata.st_uid != os.geteuid():
        raise FunctionalALaunchError(
            "NGINX_FUNCTIONAL_A_PARENT_ROOT must be owned by the workflow runner"
        )
    if stat.S_IMODE(metadata.st_mode) != 0o711:
        raise FunctionalALaunchError(
            "NGINX_FUNCTIONAL_A_PARENT_ROOT must be exactly non-enumerable mode 0711"
        )
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        if not current.lstat().st_mode & stat.S_IXOTH:
            raise FunctionalALaunchError(
                "NGINX_FUNCTIONAL_A_PARENT_ROOT has a worker-non-traversable ancestor"
            )
    return path


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_root_command(env: Mapping[str, str]) -> list[str]:
    """Validate fixed inputs and return the one explicit root command vector."""

    connector_root = _require_directory(repository_root(), "connector root")
    framework_root = _require_directory(
        connector_root / "modules" / "ModSecurity-test-Framework", "Framework root"
    )
    rule_preamble = _require_regular_file(
        framework_root / "tests" / "rules" / "no-crs-baseline.conf", "no-CRS rule preamble"
    )
    exact_script = _require_regular_file(
        connector_root / "connectors/nginx/harness/run_exact_head_use_error_log.sh",
        "exact functional-A script",
    )

    verified_root = _require_directory(
        _absolute_path(str(env.get("VERIFIED_RUN_ROOT", "")), "VERIFIED_RUN_ROOT"),
        "VERIFIED_RUN_ROOT",
    )
    functional_parent = _require_worker_traversable_functional_parent(
        _absolute_path(
            str(env.get("NGINX_FUNCTIONAL_A_PARENT_ROOT", "")),
            "NGINX_FUNCTIONAL_A_PARENT_ROOT",
        ),
        verified_root,
    )
    functional_root = functional_parent / _FUNCTIONAL_ROOT_NAME

    nginx_prefix = _require_under(
        _absolute_path(str(env.get("NGINX_PREFIX", "")), "NGINX_PREFIX"),
        verified_root,
        "NGINX_PREFIX",
    )
    nginx_build = _require_under(
        _absolute_path(str(env.get("NGINX_BUILD_DIR", "")), "NGINX_BUILD_DIR"),
        verified_root,
        "NGINX_BUILD_DIR",
    )
    modsecurity_lib = _require_under(
        _absolute_path(str(env.get("MODSECURITY_LIB_DIR", "")), "MODSECURITY_LIB_DIR"),
        verified_root,
        "MODSECURITY_LIB_DIR",
    )
    _require_directory(nginx_prefix, "NGINX_PREFIX")
    _require_directory(nginx_build, "NGINX_BUILD_DIR")
    _require_directory(modsecurity_lib, "MODSECURITY_LIB_DIR")
    nginx_binary = _require_regular_executable(nginx_prefix / "sbin/nginx", "NGINX binary")
    nginx_module = _require_regular_file(
        nginx_prefix / "modules/ngx_http_modsecurity_module.so", "NGINX module"
    )
    modsecurity_runtime_library = _require_regular_file(
        modsecurity_lib / _MODSECURITY_RUNTIME_LIBRARY,
        "libmodsecurity runtime library",
    )

    worker_user = _require_worker_name(env, "NGINX_FUNCTIONAL_WORKER_USER")
    worker_group = _require_worker_name(env, "NGINX_FUNCTIONAL_WORKER_GROUP")
    protocol = str(env.get("NGINX_PROTOCOL_PROFILE", "h1"))
    if protocol != "h1":
        raise FunctionalALaunchError("functional-A exact gate requires the h1 profile")

    root_environment = {
        "PATH": _SAFE_PATH,
        "HOME": "/nonexistent",
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
        "CONNECTOR_ROOT": str(connector_root),
        "FRAMEWORK_ROOT": str(framework_root),
        "NGINX_FUNCTIONAL_A_PARENT_ROOT": str(functional_parent),
        "VERIFIED_RUN_ROOT": str(functional_root),
        "NGINX_FUNCTIONAL_A_ROOT": str(functional_root),
        "NGINX_PREFIX": str(nginx_prefix),
        "NGINX_BUILD_DIR": str(nginx_build),
        "NGINX_BINARY": str(nginx_binary),
        "NGINX_MODULE": str(nginx_module),
        "MODSECURITY_LIB_DIR": str(modsecurity_lib),
        "NGINX_FUNCTIONAL_A_RUNTIME_LIBRARY": str(modsecurity_runtime_library),
        "MODSECURITY_RULE_PREAMBLE_FILE": str(rule_preamble),
        "MODSECURITY_TEST_VARIANT": "no-crs",
        "NO_CRS_BASELINE": "1",
        "NGINX_WORKER_USER": worker_user,
        "NGINX_WORKER_GROUP": worker_group,
        "NGINX_HOSTED_FUNCTIONAL_A": "1",
        "NGINX_LIFECYCLE_ENABLED": "1",
        "NGINX_PROTOCOL_PROFILE": "h1",
        "PYTHON": _PYTHON,
        "CURL": _CURL,
    }
    assignments = [f"{key}={value}" for key, value in root_environment.items()]
    return [_SUDO, "-n", _ENV, "-i", *assignments, _SHELL, str(exact_script)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="validate inputs and print the root command without executing it",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        command = build_root_command(os.environ)
    except FunctionalALaunchError as error:
        print(f"nginx hosted functional A blocked: {error}", file=sys.stderr)
        return 77
    if args.print_command:
        print(json.dumps(command))
        return 0
    # ``sudo`` itself receives only PATH.  Its child immediately replaces the
    # environment with the explicit allowlist above; no runner LD/Python/shell
    # startup variable crosses this privilege boundary.
    os.execve(_SUDO, command, {"PATH": _SAFE_PATH})
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
