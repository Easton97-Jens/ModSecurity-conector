#!/usr/bin/env python3
"""Materialize connector build sources under BUILD_ROOT.

The materialized source tree is generated from the controlled upstream import
plus repo-owned adapter files. It is a build artifact and must never be written
inside the repository checkout or the read-only reference repositories.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from adapter_metadata import load_metadata


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_RELATIVE = "ci/materialize-connector-source.py"
EXCLUDED_DIRS = {
    ".deps",
    ".git",
    ".github",
    ".libs",
    "__pycache__",
    "autom4te.cache",
    "objs",
}
EXCLUDED_NAMES = {
    ".travis.yml",
}
EXCLUDED_PATTERNS = (
    "*.la",
    "*.lo",
    "*.log",
    "*.o",
    "*.so",
)
GENERATED_MANIFESTS = ("MATERIALIZED_SOURCE.md", "materialized-source.json")


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    source: str
    origin_path: str
    license: str
    commit: str
    version: str
    reason: str


def relative_or_absolute(path: Path) -> str:
    resolved = path.resolve(strict=False)
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def validate_source_dir(path: Path, label: str) -> Path:
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise SystemExit(f"{label} is not a directory: {resolved}")
    return resolved


def validate_destination(path: Path) -> Path:
    if not path.is_absolute():
        raise SystemExit(f"dest-dir must be absolute: {path}")
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        pass
    else:
        raise SystemExit(f"dest-dir must not be inside the checkout: {resolved}")
    try:
        resolved.relative_to(Path("/root/conecter"))
    except ValueError:
        pass
    else:
        raise SystemExit(f"dest-dir must not be inside /root/conecter: {resolved}")
    if resolved.exists() and any(resolved.iterdir()):
        raise SystemExit(f"dest-dir must be empty or absent: {resolved}")
    return resolved


def should_skip(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in relative_path.parts):
        return True
    name = relative_path.name
    if name in EXCLUDED_NAMES:
        return True
    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_PATTERNS)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        if should_skip(relative_path):
            continue
        files.append(relative_path)
    return sorted(files, key=lambda item: item.as_posix())


def copy_tree_files(
    source_root: Path,
    destination_root: Path,
    destination_prefix: Path,
    source_kind: str,
    metadata_license: str,
    metadata_commit: str,
    metadata_version: str,
    reason: str,
) -> dict[str, ManifestEntry]:
    entries: dict[str, ManifestEntry] = {}
    for relative_path in iter_files(source_root):
        destination_relative = destination_prefix / relative_path
        destination = destination_root / destination_relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_root / relative_path, destination)
        key = destination_relative.as_posix()
        entries[key] = ManifestEntry(
            path=key,
            source=source_kind,
            origin_path=relative_or_absolute(source_root / relative_path),
            license=metadata_license,
            commit=metadata_commit,
            version=metadata_version,
            reason=reason,
        )
    return entries


def manifest_payload(
    connector: str,
    destination: Path,
    entries: dict[str, ManifestEntry],
) -> dict[str, object]:
    metadata = load_metadata(connector)
    return {
        "connector": connector,
        "source_url": metadata.source_url,
        "source_commit": metadata.source_commit,
        "source_version": metadata.source_version,
        "license": metadata.license,
        "destination": str(destination),
        "entries": [asdict(entries[name]) for name in sorted(entries)],
    }


def write_markdown_manifest(destination: Path, payload: dict[str, object]) -> None:
    rows = [
        "# Materialized Connector Source",
        "",
        f"Connector: `{payload['connector']}`",
        f"Destination: `{payload['destination']}`",
        f"Upstream: {payload['source_url']}",
        f"Commit: `{payload['source_commit']}`",
        f"Version: `{payload['source_version']}`",
        f"License: {payload['license']}",
        "",
        "| File | Source | Origin | Reason |",
        "| --- | --- | --- | --- |",
    ]
    for entry in payload["entries"]:
        assert isinstance(entry, dict)
        rows.append(
            "| `{path}` | {source} | `{origin_path}` | {reason} |".format(**entry)
        )
    rows.append("")
    (destination / "MATERIALIZED_SOURCE.md").write_text("\n".join(rows), encoding="utf-8")


def materialize(connector: str, upstream_dir: Path, adapter_dir: Path, dest_dir: Path) -> None:
    upstream = validate_source_dir(upstream_dir, "upstream-dir")
    adapter = validate_source_dir(adapter_dir, "adapter-dir")
    destination = validate_destination(dest_dir)
    metadata = load_metadata(connector)

    destination.mkdir(parents=True, exist_ok=True)
    entries = copy_tree_files(
        upstream,
        destination,
        Path("."),
        "upstream-derived",
        metadata.license,
        metadata.source_commit,
        metadata.source_version,
        "Remaining imported connector source required by the current build.",
    )
    entries.update(
        copy_tree_files(
            adapter,
            destination,
            Path("src"),
            "adapter-owned",
            metadata.license,
            metadata.source_commit,
            metadata.source_version,
            "Repo-owned adapter source overlaid into the generated build tree.",
        )
    )

    for manifest_name in GENERATED_MANIFESTS:
        entries[manifest_name] = ManifestEntry(
            path=manifest_name,
            source="generated-overlay",
            origin_path=SCRIPT_RELATIVE,
            license=metadata.license,
            commit=metadata.source_commit,
            version=metadata.source_version,
            reason="Generated materialized-source manifest.",
        )

    payload = manifest_payload(connector, destination, entries)
    write_markdown_manifest(destination, payload)
    (destination / "materialized-source.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"materialized {connector} connector source at {destination}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, choices=("apache", "nginx"))
    parser.add_argument("--upstream-dir", required=True, type=Path)
    parser.add_argument("--adapter-dir", required=True, type=Path)
    parser.add_argument("--dest-dir", required=True, type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    materialize(args.connector, args.upstream_dir, args.adapter_dir, args.dest_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
