"""One reviewed classification contract for Sonar's actual test sources.

Classification never selects or executes a behavioral case. Product files and
mixed operational tooling are not tests merely because they live below ci/ or a
connector harness directory.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = "config/testing/sonar-source-roles.json"
MAX_BYTES = 16 * 1024 * 1024
BASE_PATTERNS = ("tests/**", "**/test_*.py", "**/*_test.py", "**/*_test.go")
RETAINED_EXACT = (
    "connectors/envoy/src/envoy_ext_authz_response_companion_test.c",
    "connectors/traefik/src/traefik_forwardauth_response_companion_test.c",
    "connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c",
    "fuzz/common_http_headers_fuzz.c",
)


class SourceRoleError(ValueError):
    """Source classification cannot be derived from the reviewed contract."""


@dataclass(frozen=True)
class SourceRoles:
    patterns: tuple[str, ...]
    exact_tests: frozenset[str]
    reviewed: tuple[dict[str, Any], ...]
    sha256: str

    def test_inclusions(self) -> str:
        return ",".join(self.patterns)


def canonical_relative(value: Any) -> PurePosixPath:
    if (not isinstance(value, str) or not value or "\\" in value or
            any(part in {"", ".", ".."} for part in value.split("/"))):
        raise SourceRoleError("source-role paths must be canonical relative POSIX paths")
    path = PurePosixPath(value)
    if path.is_absolute() or any(ord(character) < 32 for character in value):
        raise SourceRoleError("source-role paths must remain inside the repository")
    return path


def read_source(root: Path, relative: str) -> bytes:
    """Read an ordinary source without following symlinks in any component."""
    path = canonical_relative(relative)
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW,
                             dir_fd=directory)
        with os.fdopen(descriptor, "rb") as source:
            observed = os.fstat(source.fileno())
            if not stat.S_ISREG(observed.st_mode) or observed.st_size > MAX_BYTES:
                raise SourceRoleError("source-role input must be a bounded regular file")
            data = source.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise SourceRoleError("source-role input exceeds its size limit")
        return data
    except OSError as exc:
        raise SourceRoleError("source-role input requires existing non-symlink regular paths") from exc
    finally:
        os.close(directory)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for name, item in pairs:
        if name in value:
            raise SourceRoleError("source-role contract contains a duplicate JSON key")
        value[name] = item
    return value


def _keys(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise SourceRoleError(f"{label} must use the closed source-role schema")


def _evidence(root: Path, path: str, value: Any) -> None:
    _keys(value, {"line", "text"}, "source/caller evidence")
    line, text = value["line"], value["text"]
    if type(line) is not int or line < 1 or not isinstance(text, str) or not text.strip():
        raise SourceRoleError("source-role evidence requires an actual source line")
    lines = read_source(root, path).decode("utf-8").splitlines()
    if line > len(lines) or lines[line - 1] != text:
        raise SourceRoleError(f"reviewed source/caller evidence drifted: {path}:{line}")


def _reviewed_role(root: Path, value: Any) -> None:
    _keys(value, {"path", "role", "group", "rationale", "source_evidence", "caller_evidence"},
          "reviewed source role")
    path = str(canonical_relative(value["path"]))
    group = value["group"]
    if (value["role"] != "TEST" or not isinstance(group, str) or
            re.fullmatch(r"[a-z][a-z0-9-]*", group) is None):
        raise SourceRoleError("reviewed fixtures require the explicit TEST role and owning group")
    if not isinstance(value["rationale"], str) or not value["rationale"].strip():
        raise SourceRoleError("reviewed source role requires its actual purpose")
    _evidence(root, path, value["source_evidence"])
    callers = value["caller_evidence"]
    if not isinstance(callers, list) or not callers:
        raise SourceRoleError("reviewed fixture requires source-backed caller evidence")
    for caller in callers:
        _keys(caller, {"path", "line", "text"}, "caller evidence")
        _evidence(root, str(canonical_relative(caller["path"])),
                  {"line": caller["line"], "text": caller["text"]})


def load_roles(root: Path = ROOT) -> SourceRoles:
    if root.resolve(strict=True) != root:
        raise SourceRoleError("source-role repository root must be canonical")
    raw = read_source(root, CONTRACT)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SourceRoleError("source-role contract must be strict UTF-8 JSON") from exc
    _keys(value, {"schema_version", "standard_test_patterns", "existing_exact_test_sources",
                  "reviewed_test_sources"}, "source-role contract")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise SourceRoleError("unsupported source-role contract version")
    if value["standard_test_patterns"] != list(BASE_PATTERNS):
        raise SourceRoleError("source-role contract must preserve the standard test patterns")
    if value["existing_exact_test_sources"] != list(RETAINED_EXACT):
        raise SourceRoleError("source-role contract must preserve the existing exact native tests")
    reviewed = value["reviewed_test_sources"]
    if not isinstance(reviewed, list) or not reviewed:
        raise SourceRoleError("source-role contract requires individually reviewed fixture paths")
    for item in reviewed:
        _reviewed_role(root, item)
    names = [item["path"] for item in reviewed]
    if names != sorted(set(names)) or set(names).intersection(RETAINED_EXACT):
        raise SourceRoleError("reviewed fixture paths must be unique, sorted and distinct from retained tests")
    for path in RETAINED_EXACT:
        read_source(root, path)
    patterns = (*value["standard_test_patterns"], *value["existing_exact_test_sources"], *names)
    return SourceRoles(tuple(patterns), frozenset((*RETAINED_EXACT, *names)), tuple(reviewed),
                       hashlib.sha256(raw).hexdigest())


def _standard_match(relative: str, pattern: str) -> bool:
    # Sonar's leading **/ also matches zero directories; * never spans /.
    expression = re.escape(pattern).replace(r"\*\*/", r"(?:.*/)?")
    expression = expression.replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
    return re.fullmatch(expression, relative) is not None


def is_test_source(relativepath: str, roles: SourceRoles | None = None,
                   root: Path = ROOT) -> bool:
    relative = str(canonical_relative(relativepath))
    read_source(root, relative)
    contract = roles or load_roles(root)
    return (relative in contract.exact_tests or
            any(_standard_match(relative, pattern) for pattern in contract.patterns[:len(BASE_PATTERNS)]))
