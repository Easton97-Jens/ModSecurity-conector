"""Read ordinary Framework pins and bind them to independently recorded Git objects."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import subprocess


LOCK_RELATIVE_PATH = "ci/tooling/project-versions.lock.json"
MAX_LOCK_BYTES = 4096
FRAMEWORK_PATH = "modules/ModSecurity-test-Framework"
MRTS_PATH = "tools/MRTS"
HEX40 = re.compile(r"[0-9a-f]{40}", re.ASCII)
PYTHON_VERSION = re.compile(r"3\.14\.(?:0|[1-9][0-9]*)", re.ASCII)
GO_VERSION = re.compile(r"[1-9]\d*\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", re.ASCII)


class FrameworkRevisionPinsError(ValueError):
    """The lock or its independent repository provenance is invalid."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise FrameworkRevisionPinsError("duplicate revision-lock key")
        result[key] = value
    return result


def _sha(value: object, name: str) -> str:
    if not isinstance(value, str) or HEX40.fullmatch(value) is None:
        raise FrameworkRevisionPinsError(f"{name} must be a lowercase ASCII SHA-1")
    return value


def _version(value: object, name: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or len(value) > 32 or pattern.fullmatch(value) is None:
        raise FrameworkRevisionPinsError(f"{name} must be a supported stable ASCII release version")
    return value


def parse_framework_revision_pins(data: bytes) -> dict[str, int | str]:
    """Parse bounded UTF-8 JSON data without executing or inferring any values."""
    if len(data) > MAX_LOCK_BYTES:
        raise FrameworkRevisionPinsError("revision lock exceeds size limit")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise FrameworkRevisionPinsError("revision lock is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "framework_sha", "mrts_sha", "python_version", "go_version",
    }:
        raise FrameworkRevisionPinsError("project version lock must contain exactly the five approved keys")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise FrameworkRevisionPinsError("revision-lock schema_version must be integer 1")
    return {
        "schema_version": 1,
        "framework_sha": _sha(value["framework_sha"], "framework_sha"),
        "mrts_sha": _sha(value["mrts_sha"], "mrts_sha"),
        "python_version": _version(value["python_version"], "python_version", PYTHON_VERSION),
        "go_version": _version(value["go_version"], "go_version", GO_VERSION),
    }


def _read_lock(root: Path) -> bytes:
    relative = Path(LOCK_RELATIVE_PATH)
    try:
        for ancestor in relative.parents:
            if ancestor != Path(".") and (root / ancestor).is_symlink():
                raise FrameworkRevisionPinsError("revision-lock directory must not be a symlink")
        descriptor = os.open(root / relative, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode):
                raise FrameworkRevisionPinsError("revision lock must be a regular file")
            if metadata.st_size > MAX_LOCK_BYTES:
                raise FrameworkRevisionPinsError("revision lock exceeds size limit")
            data = stream.read(MAX_LOCK_BYTES + 1)
    except OSError as exc:
        raise FrameworkRevisionPinsError("cannot read regular, non-symlink revision lock") from exc
    return data


def load_framework_revision_pins(root: Path) -> dict[str, int | str]:
    """Load the fixed lock offline; this does not verify repository provenance."""
    return parse_framework_revision_pins(_read_lock(root))


def load_project_version_pins(root: Path) -> dict[str, int | str]:
    """Load shared toolchain and ordinary revision pins through the same strict parser."""
    return load_framework_revision_pins(root)


def parse_project_version_pins(data: bytes) -> dict[str, int | str]:
    """Parse the shared version lock with the same closed data contract."""
    return parse_framework_revision_pins(data)


def _git(root: Path, *arguments: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise FrameworkRevisionPinsError("cannot verify revision-lock Git provenance") from exc
    return result.stdout


def _repository_head(root: Path, expected: str, name: str) -> None:
    top_level = _git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    if Path(top_level).resolve() != root.resolve():
        raise FrameworkRevisionPinsError(f"{name} must be an initialized independent repository")
    head = _git(root, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    if head != expected:
        raise FrameworkRevisionPinsError(f"{name} HEAD disagrees with the expected revision")


def _gitlink(root: Path, commit: str, path: str, expected: str, name: str) -> None:
    entry = _git(root, "ls-tree", commit, "--", path)
    required = f"160000 commit {expected}\t{path}\n".encode("ascii")
    if entry != required:
        raise FrameworkRevisionPinsError(f"{name} recorded gitlink disagrees with the revision lock")


def read_framework_mrts_gitlink(framework_root: Path, framework_sha: str) -> str:
    """Read only the fixed MRTS gitlink from an exact candidate Framework object."""
    framework_sha = _sha(framework_sha, "framework_sha")
    entry = _git(framework_root, "ls-tree", framework_sha, "--", MRTS_PATH)
    match = re.fullmatch(rb"160000 commit ([0-9a-f]{40})\ttools/MRTS\n", entry)
    if match is None:
        raise FrameworkRevisionPinsError("candidate Framework must record an MRTS gitlink")
    return match.group(1).decode("ascii")


def verify_framework_revision_pins(root: Path, parent_sha: str) -> dict[str, int | str]:
    """Require the exact Parent lock blob, gitlinks, and materialized HEADs to agree."""
    parent_sha = _sha(parent_sha, "parent_sha")
    data = _read_lock(root)
    pins = parse_framework_revision_pins(data)
    _repository_head(root, parent_sha, "Parent")
    blob = f"{parent_sha}:{LOCK_RELATIVE_PATH}"
    lock_entry = _git(root, "ls-tree", parent_sha, "--", LOCK_RELATIVE_PATH)
    if re.fullmatch(rb"100644 blob [0-9a-f]{40}\tci/tooling/project-versions\.lock\.json\n", lock_entry) is None:
        raise FrameworkRevisionPinsError("recorded revision lock must be a regular non-executable blob")
    size = _git(root, "cat-file", "-s", blob).decode("ascii").strip()
    if not size.isdecimal() or int(size) > MAX_LOCK_BYTES:
        raise FrameworkRevisionPinsError("recorded revision-lock blob exceeds size limit")
    if _git(root, "cat-file", "blob", blob) != data:
        raise FrameworkRevisionPinsError("revision lock differs from the exact Parent commit blob")
    framework_sha = str(pins["framework_sha"])
    mrts_sha = str(pins["mrts_sha"])
    _gitlink(root, parent_sha, FRAMEWORK_PATH, framework_sha, "Framework")
    framework_root = root / FRAMEWORK_PATH
    _repository_head(framework_root, framework_sha, "Framework")
    _gitlink(framework_root, framework_sha, MRTS_PATH, mrts_sha, "MRTS")
    _repository_head(framework_root / MRTS_PATH, mrts_sha, "MRTS")
    return pins
