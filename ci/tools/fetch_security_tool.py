#!/usr/bin/env python3
"""Download one checksum-verified CI security-tool release asset."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import stat
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
SHA256 = re.compile(r"^[a-f\d]{64}$")
RELEASE_TAG = re.compile(r"^v?[0-9]+(?:\.[0-9]+){0,3}$")
UPSTREAM = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def safe_component(value: str) -> bool:
    path = Path(value)
    return (
        bool(value)
        and "/" not in value
        and "\\" not in value
        and not path.is_absolute()
        and len(path.parts) == 1
        and path.parts[0] not in {".", ".."}
    )


def validate_record(tool: str, values: Mapping[str, str]) -> dict[str, str]:
    """Validate one Parent lock or normalized-candidate tool release tuple."""

    if not re.fullmatch(r"[a-z][a-z0-9_-]*", tool):
        raise ValueError("invalid security tool name")
    required = {"version", "asset", "url", "sha256", "executable", "upstream"}
    if not required.issubset(values) or not all(
        isinstance(key, str) and isinstance(value, str) and value
        for key, value in values.items()
    ):
        raise ValueError(f"{tool}: incomplete lock record")
    record = {key: values[key] for key in required}
    if not RELEASE_TAG.fullmatch(record["version"]):
        raise ValueError(f"{tool}: malformed release version")
    if not SHA256.fullmatch(record["sha256"]):
        raise ValueError(f"{tool}: malformed SHA-256")
    if not safe_component(record["asset"]) or not safe_component(record["executable"]):
        raise ValueError(f"{tool}: unsafe archive layout")
    if not UPSTREAM.fullmatch(record["upstream"]):
        raise ValueError(f"{tool}: upstream must be an exact HTTPS GitHub repository URL")
    expected_url = (
        f"{record['upstream']}/releases/download/{record['version']}/{record['asset']}"
    )
    if record["url"] != expected_url:
        raise ValueError(f"{tool}: release asset is not from the recorded upstream")
    return record


def record(tool: str) -> dict[str, str]:
    """Read the intentionally small downloaded-binary record without PyYAML."""
    text = LOCK.read_text(encoding="utf-8")
    match = re.search(rf"^ {{2}}{re.escape(tool)}:\n(.*?)(?=^ {{2}}[a-z][a-z\d_]*:|^dispositions:|\Z)", text, re.MULTILINE | re.DOTALL)
    if match is None:
        raise ValueError(f"unknown security tool: {tool}")
    values = dict(re.findall(r"^ {4}([a-z\d_]+): (.+)$", match.group(1), re.MULTILINE))
    return validate_record(tool, values)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(member: tarfile.TarInfo) -> bool:
    path = Path(member.name)
    return member.isfile() and not path.is_absolute() and ".." not in path.parts


def safe_destination(destination: Path) -> None:
    """Reject relative, traversal, and symlink destination components."""

    if not destination.is_absolute() or any(part == ".." for part in destination.parts):
        raise ValueError("security tool destination must be an absolute non-traversal path")
    current = Path(destination.anchor)
    for part in destination.parts[1:]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise ValueError("security tool destination must not traverse a symlink")


def fetch_record(tool: str, values: Mapping[str, str], destination: Path) -> Path:
    """Fetch one already-validated Parent release tuple without executing it."""

    values = validate_record(tool, values)
    safe_destination(destination)
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ValueError(f"{tool}: destination must be a directory") from exc
    if destination.is_symlink() or not destination.is_dir():
        raise ValueError(f"{tool}: destination must be a directory")
    with tempfile.TemporaryDirectory(prefix="security-tool-", dir=destination) as temp:
        archive = Path(temp) / values["asset"]
        request = urllib.request.Request(values["url"], headers={"User-Agent": "ModSecurity-conector-security-tools"})
        with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
        if sha256(archive) != values["sha256"]:
            raise ValueError(f"{tool}: SHA-256 mismatch")
        with tarfile.open(archive, "r:gz") as bundle:
            entries = [member for member in bundle.getmembers() if safe_member(member) and Path(member.name).name == values["executable"]]
            if len(entries) != 1:
                raise ValueError(f"{tool}: expected exactly one executable")
            source = bundle.extractfile(entries[0])
            if source is None:
                raise ValueError(f"{tool}: unreadable executable")
            target = destination / values["executable"]
            with target.open("wb") as output:
                shutil.copyfileobj(source, output)
    target.chmod(0o755)
    return target


def fetch(tool: str, destination: Path) -> Path:
    """Fetch the checked-in Parent lock record through the established CLI path."""

    return fetch_record(tool, record(tool), destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.validate_only:
        record(args.tool)
        return
    destination = args.destination
    if destination is None:
        parser.error("--destination is required unless --validate-only is used")
        return
    if not destination.is_absolute():
        destination = Path.cwd() / destination
    print(fetch(args.tool, destination))


if __name__ == "__main__":
    main()
