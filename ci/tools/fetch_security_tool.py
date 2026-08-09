#!/usr/bin/env python3
"""Download one checksum-verified CI security-tool release asset."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import tarfile
import tempfile
import urllib.request
from collections.abc import Mapping
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
SHA256 = re.compile(r"^[a-f\d]{64}$", re.ASCII)
VERSION = re.compile(r"^v?\d+(?:\.\d+){1,3}$", re.ASCII)
GITHUB_UPSTREAM = re.compile(
    r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
)
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9_.-]+$")
REQUIRED_FIELDS = frozenset({"version", "asset", "url", "sha256", "executable", "upstream"})


def record(tool: str) -> dict[str, str]:
    """Read the intentionally small downloaded-binary record without PyYAML."""
    text = LOCK.read_text(encoding="utf-8")
    match = re.search(rf"^ {{2}}{re.escape(tool)}:\n(.*?)(?=^ {{2}}[a-z][a-z\d_]*:|^dispositions:|\Z)", text, re.MULTILINE | re.DOTALL)
    if match is None:
        raise ValueError(f"unknown security tool: {tool}")
    values = dict(re.findall(r"^ {4}([a-z\d_]+): (.+)$", match.group(1), re.MULTILINE))
    return validated_record(tool, values)


def safe_component(value: str) -> bool:
    return bool(SAFE_COMPONENT.fullmatch(value)) and value not in {".", ".."}


def validated_record(tool: str, values: Mapping[str, object]) -> dict[str, str]:
    """Validate the precise immutable asset tuple before any download."""

    if not isinstance(tool, str) or not safe_component(tool):
        raise ValueError("security tool name is unsafe")
    missing = REQUIRED_FIELDS.difference(values)
    if missing:
        raise ValueError(f"{tool}: incomplete lock record")
    result = {field: values[field] for field in REQUIRED_FIELDS}
    if not all(isinstance(value, str) for value in result.values()):
        raise ValueError(f"{tool}: lock record fields must be strings")
    typed = {field: str(value) for field, value in result.items()}
    if not VERSION.fullmatch(typed["version"]):
        raise ValueError(f"{tool}: malformed release version")
    if not SHA256.fullmatch(typed["sha256"]):
        raise ValueError(f"{tool}: malformed SHA-256")
    if not safe_component(typed["asset"]) or not safe_component(typed["executable"]):
        raise ValueError(f"{tool}: asset or executable name is unsafe")
    if not GITHUB_UPSTREAM.fullmatch(typed["upstream"]):
        raise ValueError(f"{tool}: upstream must be an official GitHub repository")
    expected = (
        typed["upstream"]
        + "/releases/download/"
        + typed["version"]
        + "/"
        + typed["asset"]
    )
    if typed["url"] != expected:
        raise ValueError(f"{tool}: release asset is not the recorded upstream tuple")
    return typed


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(member: tarfile.TarInfo) -> bool:
    path = Path(member.name)
    return member.isfile() and not path.is_absolute() and ".." not in path.parts


def fetch_record(tool: str, values: Mapping[str, object], destination: Path) -> Path:
    """Fetch a validated on-disk or candidate asset tuple without executing it."""

    values = validated_record(tool, values)
    if destination.is_symlink():
        raise ValueError(f"{tool}: destination must not be a symlink")
    destination.mkdir(mode=0o700, parents=True, exist_ok=True)
    if destination.is_symlink() or not destination.is_dir():
        raise ValueError(f"{tool}: destination must be a directory")
    destination.chmod(0o700)
    target = destination / values["executable"]
    if target.exists() or target.is_symlink():
        raise ValueError(f"{tool}: destination executable already exists")
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
    """Fetch one existing on-disk lock record through the legacy CLI API."""

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
    print(fetch(args.tool, destination.resolve()))


if __name__ == "__main__":
    main()
