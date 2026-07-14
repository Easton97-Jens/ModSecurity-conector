from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "ci" / "tooling" / "security-tools.lock.yml"


TOOL_NAME_CHARACTERS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789_")


def is_tool_header(line: str) -> bool:
    """Return whether a line starts a top-level tool record in the lock file."""
    if not line.startswith("  ") or not line.endswith(":"):
        return False
    name = line[2:-1]
    return bool(name) and all(character in TOOL_NAME_CHARACTERS for character in name)


def scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def map_value(lines: list[str], parent: str, key: str) -> str | None:
    marker = f"    {parent}:"
    try:
        start = lines.index(marker)
    except ValueError:
        return None
    for line in lines[start + 1 :]:
        if line.startswith("    ") and not line.startswith("      "):
            break
        if line.startswith(f"      {key}:"):
            return scalar(line.split(":", 1)[1])
    return None


def direct_value(lines: list[str], key: str) -> str | None:
    marker = f"    {key}:"
    for line in lines:
        if line.startswith(marker):
            return scalar(line.split(":", 1)[1])
    return None


def load_record(manifest_path: Path, name: str) -> dict[str, Any]:
    """Read just the binary-download fields from the stable lock-file shape.

    This avoids a runtime PyYAML dependency in the security workflows. The
    full manifest schema is independently validated by the repository check.
    """
    source = manifest_path.read_text(encoding="utf-8").splitlines()
    start = next(
        (index for index, line in enumerate(source) if line == f"  {name}:"), None
    )
    if start is None:
        raise ValueError(f"unknown security tool: {name}")
    end = len(source)
    for index in range(start + 1, len(source)):
        if is_tool_header(source[index]):
            end = index
            break
        if source[index] and not source[index].startswith(" "):
            end = index
            break
    lines = source[start + 1 : end]
    integration = direct_value(lines, "integration")
    if integration != "downloaded_binary":
        raise ValueError(f"{name} is not a downloaded binary")
    checksum = {
        key: map_value(lines, "checksum", key)
        for key in ("asset", "url", "sha256", "source", "executable")
    }
    upstream = {
        key: map_value(lines, "upstream", key)
        for key in ("owner", "repository", "url")
    }
    if any(value is None for value in checksum.values()) or any(
        value is None for value in upstream.values()
    ):
        raise ValueError(f"{name} lacks download metadata")
    owner = upstream["owner"]
    repository = upstream["repository"]
    expected_prefix = f"https://github.com/{owner}/{repository}/releases/download/"
    if not checksum["url"].startswith(expected_prefix):
        raise ValueError(f"{name} download URL is not an official release asset")
    return {"integration": integration, "checksum": checksum, "upstream": upstream}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(member: tarfile.TarInfo) -> bool:
    path = Path(member.name)
    return not path.is_absolute() and ".." not in path.parts and member.isfile()


def extract_executable(archive: Path, destination: Path, executable: str) -> Path:
    with tarfile.open(archive, mode="r:gz") as bundle:
        candidates = [
            member
            for member in bundle.getmembers()
            if safe_member(member) and Path(member.name).name == executable
        ]
        if len(candidates) != 1:
            raise ValueError(f"archive must contain exactly one {executable} executable")
        extracted = bundle.extractfile(candidates[0])
        if extracted is None:
            raise ValueError("archive executable cannot be read")
        target = destination / executable
        with target.open("wb") as stream:
            shutil.copyfileobj(extracted, stream)
    target.chmod(0o755)
    return target


def fetch(record: dict[str, Any], destination: Path) -> Path:
    checksum = record["checksum"]
    destination.mkdir(parents=True, exist_ok=True)
    asset = checksum["asset"]
    descriptor, archive_name = tempfile.mkstemp(
        prefix="security-tool-", suffix=".tar.gz", dir=destination
    )
    os.close(descriptor)
    archive = Path(archive_name)
    try:
        request = urllib.request.Request(checksum["url"], headers={"User-Agent": "ModSecurity-conector-security-tools"})
        with urllib.request.urlopen(request, timeout=60) as response:
            with archive.open("wb") as stream:
                shutil.copyfileobj(response, stream)
        actual = sha256(archive)
        if actual != checksum["sha256"]:
            raise ValueError(f"checksum mismatch for {asset}")
        return extract_executable(archive, destination, checksum["executable"])
    finally:
        archive.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a checksum-verified security-tool release asset."
    )
    parser.add_argument("--tool", required=True)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--validate-only", action="store_true")
    arguments = parser.parse_args()
    record = load_record(arguments.manifest.resolve(), arguments.tool)
    if arguments.validate_only:
        print(f"{arguments.tool}: manifest metadata valid")
        return
    if arguments.destination is None:
        parser.error("--destination is required unless --validate-only")
    else:
        binary = fetch(record, arguments.destination.resolve())
        print(binary)


if __name__ == "__main__":
    main()
