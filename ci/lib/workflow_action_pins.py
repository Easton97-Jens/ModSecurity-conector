"""Read exact setup-action references from the reviewed canonical lock block."""

from __future__ import annotations

import os
from pathlib import Path
import re
import stat


LOCK_PATH = Path("ci/tooling/security-tools.lock.yml")
PINNED_ACTIONS_HEADER = "pinned_actions:"
MAX_LOCK_BYTES = 65536
ACTION_NAME = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", re.ASCII)
# Same reviewed stable action-tag grammar as update-workflow-tools.py.
STABLE_TAG = re.compile(r"v\d+(?:\.\d+){0,3}", re.ASCII)
FULL_SHA = re.compile(r"[0-9a-f]{40}", re.ASCII)


class ActionPinsError(ValueError):
    """The setup-action lock is missing, ambiguous or malformed."""


def _validate_root_mapping(lines: list[str]) -> None:
    """Require the canonical closed top-level schema, without alternate YAML keys."""
    patterns = (
        r"schema_version: 1", r'''checked_at: (["'])\d{4}-\d{2}-\d{2}\1''',
        PINNED_ACTIONS_HEADER, r"tools:", r"dispositions:",
    )
    roots = [line for line in lines if line and not line[0].isspace() and not line.startswith("#")]
    if len(roots) != len(patterns) or any(
        re.fullmatch(pattern, line, re.ASCII) is None
        for pattern, line in zip(patterns, roots, strict=True)
    ):
        raise ActionPinsError("action lock must use the canonical unique top-level schema")
    first_mapping = lines.index(PINNED_ACTIONS_HEADER)
    if any(line.strip() and line[0].isspace() for line in lines[:first_mapping]):
        raise ActionPinsError("action lock has an unexpected top-level scalar extension")


def _read_lock_lines(root: Path) -> list[str]:
    """Read a bounded regular lock without following a substituted path."""
    for ancestor in LOCK_PATH.parents:
        if ancestor != Path(".") and (root / ancestor).is_symlink():
            raise ActionPinsError("action-lock directory must not be a symlink")
    try:
        descriptor = os.open(root / LOCK_PATH, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_LOCK_BYTES:
                raise ActionPinsError("action lock must be a bounded regular file")
            data = stream.read(MAX_LOCK_BYTES + 1)
        if len(data) > MAX_LOCK_BYTES:
            raise ActionPinsError("action lock exceeds the size limit")
        return data.decode("utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ActionPinsError("cannot read the regular UTF-8 action lock") from exc


def _action_mapping_lines(lines: list[str]):
    """Yield only non-comment lines in the one canonical action block."""
    if lines.count(PINNED_ACTIONS_HEADER) != 1:
        raise ActionPinsError("action lock must contain exactly one pinned_actions mapping")
    for line in lines[lines.index(PINNED_ACTIONS_HEADER) + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            break
        yield line


def _start_action_record(line: str, records: dict[str, dict[str, str]]) -> dict[str, str]:
    name = line[2:].removesuffix(":")
    if not line.endswith(":") or ACTION_NAME.fullmatch(name) is None or name in records:
        raise ActionPinsError("action lock has an invalid or duplicate action name")
    current: dict[str, str] = {}
    records[name] = current
    return current


def _add_action_field(line: str, current: dict[str, str] | None) -> None:
    if current is None or not line.startswith("    ") or line.startswith("     "):
        raise ActionPinsError("action lock has an unsupported mapping shape")
    key, separator, value = line[4:].partition(": ")
    if not separator or key not in {"version", "commit_sha", "upstream"} or key in current:
        raise ActionPinsError("action lock has an invalid or duplicate field")
    current[key] = value


def _parse_action_mapping(lines: list[str]) -> dict[str, dict[str, str]]:
    """Accept the canonical scalar mapping and reject duplicate or extended YAML."""
    records: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in _action_mapping_lines(lines):
        if line.startswith("  ") and not line.startswith("   "):
            current = _start_action_record(line, records)
        else:
            _add_action_field(line, current)
    if not records:
        raise ActionPinsError("action lock contains no pinned actions")
    return records


def _validate_action_records(records: dict[str, dict[str, str]]) -> None:
    """Require every action's stable tag, immutable SHA and canonical upstream."""
    for name, record in records.items():
        if (set(record) != {"version", "commit_sha", "upstream"}
                or STABLE_TAG.fullmatch(record["version"]) is None
                or FULL_SHA.fullmatch(record["commit_sha"]) is None
                or record["upstream"] != f"https://github.com/{name}"):
            raise ActionPinsError("action lock requires an exact stable tag, full SHA and canonical upstream")


def read_action_pins(root: Path) -> dict[str, dict[str, str]]:
    """Parse only the lock's fixed scalar action mapping; reject YAML extensions."""
    lines = _read_lock_lines(root)
    _validate_root_mapping(lines)
    records = _parse_action_mapping(lines)
    _validate_action_records(records)
    return records


def read_action_reference(root: Path, name: str) -> str:
    """Return the exact immutable reference and matching provenance comment."""
    record = read_action_pins(root).get(name)
    if record is None:
        raise ActionPinsError(f"action lock is missing {name}")
    return f"{name}@{record['commit_sha']} # {record['version']}"
