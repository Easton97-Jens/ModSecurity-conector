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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "ci" / "tooling" / "security-tools.lock.yml"
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def record(tool: str, lock_path: Path = LOCK) -> dict[str, str]:
    """Read the intentionally small downloaded-binary record without PyYAML."""
    text = lock_path.read_text(encoding="utf-8")
    match = re.search(rf"^  {re.escape(tool)}:\n(.*?)(?=^  [a-z][a-z0-9_]*:|^dispositions:|\Z)", text, re.MULTILINE | re.DOTALL)
    if match is None:
        raise ValueError(f"unknown security tool: {tool}")
    values = dict(re.findall(r"^    ([a-z0-9_]+): (.+)$", match.group(1), re.MULTILINE))
    required = {"asset", "url", "sha256", "executable", "upstream"}
    if set(values).intersection(required) != required:
        raise ValueError(f"{tool}: incomplete lock record")
    if not SHA256.fullmatch(values["sha256"]):
        raise ValueError(f"{tool}: malformed SHA-256")
    expected = values["upstream"].rstrip("/") + "/releases/download/"
    if not values["url"].startswith(expected):
        raise ValueError(f"{tool}: release asset is not from the recorded upstream")
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(member: tarfile.TarInfo) -> bool:
    path = Path(member.name)
    return member.isfile() and not path.is_absolute() and ".." not in path.parts


def fetch(tool: str, destination: Path, lock_path: Path = LOCK) -> Path:
    values = record(tool, lock_path)
    destination.mkdir(parents=True, exist_ok=True)
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--lock", type=Path, default=LOCK)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.validate_only:
        record(args.tool, args.lock)
        return 0
    if args.destination is None:
        parser.error("--destination is required unless --validate-only is used")
    print(fetch(args.tool, args.destination.resolve(), args.lock))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
