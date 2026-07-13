#!/usr/bin/env python3
"""Validate and atomically publish Bear-captured C/C++ compilation databases."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


class CompilationDatabaseError(RuntimeError):
    """Raised for a compilation-database contract violation."""


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def external_output_path(value: str, repository_root: Path) -> Path:
    output = Path(value)
    if not output.is_absolute():
        raise CompilationDatabaseError(f"COMPDB_OUTPUT must be an absolute path: {value}")
    resolved = output.resolve(strict=False)
    if is_within(resolved, repository_root):
        raise CompilationDatabaseError(
            f"COMPDB_OUTPUT must be outside the checkout: {resolved}"
        )
    return resolved


def load_database(path: Path) -> list[Any]:
    if not path.is_file():
        raise CompilationDatabaseError(f"compilation database is missing: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CompilationDatabaseError(f"invalid compilation database JSON at {path}: {error}") from error
    if not isinstance(value, list):
        raise CompilationDatabaseError(f"compilation database root must be a JSON array: {path}")
    return value


def tracked_sources(repository_root: Path) -> set[Path]:
    completed = subprocess.run(
        ["git", "-C", str(repository_root), "ls-files", "-z"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise CompilationDatabaseError(f"cannot enumerate tracked checkout sources: {detail}")
    return {
        (repository_root / item.decode("utf-8", "surrogateescape")).resolve(strict=False)
        for item in completed.stdout.split(b"\0")
        if item
    }


def source_path(entry: dict[str, Any]) -> Path:
    directory = entry.get("directory")
    file_name = entry.get("file")
    if not isinstance(directory, str) or not directory:
        raise CompilationDatabaseError("entry has no non-empty directory")
    if not isinstance(file_name, str) or not file_name:
        raise CompilationDatabaseError("entry has no non-empty file")
    directory_path = Path(directory)
    if not directory_path.is_absolute():
        raise CompilationDatabaseError(f"entry directory is not absolute: {directory}")
    file_path = Path(file_name)
    if not file_path.is_absolute():
        file_path = directory_path / file_path
    return file_path.resolve(strict=False)


def output_path(entry: dict[str, Any]) -> Path:
    output = entry.get("output")
    if not isinstance(output, str) or not output:
        raise CompilationDatabaseError("entry has no non-empty output path")
    path = Path(output)
    if not path.is_absolute():
        raise CompilationDatabaseError(f"entry output is not absolute: {output}")
    return path.resolve(strict=False)


def collect_entries(
    entries: list[Any],
    repository_root: Path,
    tracked: set[Path],
) -> tuple[dict[Path, dict[str, Any]], list[str]]:
    """Allow only tracked C/C++ sources and retain Bear's command records unchanged."""

    accepted: dict[Path, dict[str, Any]] = {}
    filtered: list[str] = []
    for index, raw_entry in enumerate(entries):
        if not isinstance(raw_entry, dict):
            filtered.append(f"entry {index} is not an object")
            continue
        entry = dict(raw_entry)
        try:
            source = source_path(entry)
        except CompilationDatabaseError as error:
            filtered.append(f"entry {index}: {error}")
            continue
        try:
            output = output_path(entry)
        except CompilationDatabaseError as error:
            filtered.append(f"entry {index}: {error}")
            continue
        if source.suffix not in {".c", ".cc"}:
            filtered.append(f"entry {index} is not a supported C/C++ translation unit: {source}")
            continue
        if source not in tracked or not is_within(source, repository_root) or not source.is_file():
            filtered.append(f"entry {index} is not a tracked checkout source: {source}")
            continue
        if is_within(output, repository_root):
            filtered.append(f"entry {index} writes inside the checkout: {output}")
            continue
        if source in accepted:
            filtered.append(f"duplicate translation unit: {source}")
            continue
        accepted[source] = entry
    return accepted, filtered


def command_arguments(entry: dict[str, Any], source: Path) -> list[str]:
    arguments = entry.get("arguments")
    if isinstance(arguments, list) and arguments and all(isinstance(arg, str) for arg in arguments):
        return arguments
    command = entry.get("command")
    if isinstance(command, str) and command:
        try:
            return shlex.split(command)
        except ValueError as error:
            raise CompilationDatabaseError(
                f"cannot parse command for {source}: {error}"
            ) from error
    raise CompilationDatabaseError(
        f"entry for {source} has neither a valid arguments array nor command string"
    )


def nginx_config_sources(repository_root: Path) -> set[Path]:
    config = repository_root / "connectors/nginx/config"
    try:
        text = config.read_text(encoding="utf-8")
    except OSError as error:
        raise CompilationDatabaseError(f"cannot read NGINX config source list: {error}") from error

    sources: set[Path] = set()
    for connector_source, common_source in re.findall(
        r"\$ngx_addon_dir/(src/[A-Za-z0-9_./-]+\.c)|\$MSCONNECTOR_COMMON_SRC/([A-Za-z0-9_./-]+\.c)",
        text,
    ):
        if connector_source:
            sources.add((repository_root / "connectors/nginx" / connector_source).resolve(strict=False))
        else:
            sources.add((repository_root / "common/src" / common_source).resolve(strict=False))
    if not sources:
        raise CompilationDatabaseError("NGINX config does not declare any C translation units")
    return sources


def expected_sources(repository_root: Path, requirements: list[str]) -> set[Path]:
    expected: set[Path] = set()
    if "nginx" in requirements:
        expected.update(nginx_config_sources(repository_root))
    if "cpp" in requirements:
        expected.add((repository_root / "common/scripts/modsecurity_targeted_eval.cc").resolve(strict=False))
    return expected


def validate_entries(
    entries: dict[Path, dict[str, Any]],
    repository_root: Path,
    requirements: list[str],
) -> None:
    if not entries:
        raise CompilationDatabaseError("compilation database has no accepted translation units")

    for source, entry in entries.items():
        arguments = command_arguments(entry, source)
        required_flags = ["-Wall", "-Wextra", "-Werror"]
        if source.suffix == ".c":
            required_flags.append("-std=c17")
        elif source.suffix == ".cc":
            required_flags.append("-std=c++17")
        missing = [flag for flag in required_flags if flag not in arguments]
        if missing:
            display = source.relative_to(repository_root)
            raise CompilationDatabaseError(
                f"translation unit {display} is missing required flags: {' '.join(missing)}"
            )

    expected = expected_sources(repository_root, requirements)
    missing_sources = sorted(expected.difference(entries), key=lambda path: path.as_posix())
    if missing_sources:
        names = ", ".join(str(path.relative_to(repository_root)) for path in missing_sources)
        raise CompilationDatabaseError(f"compilation database coverage is incomplete: {names}")


def atomic_write(path: Path, entries: dict[Path, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = [entries[source] for source in sorted(entries, key=lambda item: item.as_posix())]
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(ordered, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="validate and atomically publish a Bear-captured compilation database"
    )
    parser.add_argument("--repo-root", required=True, help="absolute checkout root")
    parser.add_argument("--output", required=True, help="absolute external compilation database path")
    parser.add_argument("--input", help="Bear JSON to filter and publish")
    parser.add_argument(
        "--require",
        choices=("nginx", "cpp"),
        action="append",
        default=[],
        help="translation-unit coverage required before success",
    )
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="retain an already-valid published database and replace matching captured units",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="validate an existing database without writing it",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    repository_root = Path(args.repo_root).resolve(strict=False)
    if not repository_root.is_dir() or not (repository_root / ".git").exists():
        raise CompilationDatabaseError(f"repo root is not a checkout: {repository_root}")
    output = external_output_path(args.output, repository_root)
    tracked = tracked_sources(repository_root)

    if args.verify_only:
        if args.input:
            raise CompilationDatabaseError("--input cannot be combined with --verify-only")
        existing, filtered = collect_entries(load_database(output), repository_root, tracked)
        if filtered:
            raise CompilationDatabaseError(
                "existing compilation database is invalid: " + "; ".join(filtered)
            )
        validate_entries(existing, repository_root, args.require)
        print(f"PASS: validated {len(existing)} unique translation units in {output}")
        return 0

    if not args.input:
        raise CompilationDatabaseError("--input is required unless --verify-only is used")

    captured, filtered = collect_entries(
        load_database(Path(args.input)), repository_root, tracked
    )
    if not captured:
        raise CompilationDatabaseError("Bear did not capture any tracked C/C++ translation units")

    published: dict[Path, dict[str, Any]] = {}
    if args.merge_existing and output.exists():
        existing, existing_filtered = collect_entries(
            load_database(output), repository_root, tracked
        )
        if existing_filtered:
            raise CompilationDatabaseError(
                "existing compilation database is invalid: " + "; ".join(existing_filtered)
            )
        validate_entries(existing, repository_root, [])
        published.update(existing)
    published.update(captured)
    validate_entries(published, repository_root, args.require)
    atomic_write(output, published)

    for reason in filtered:
        print(f"FILTERED: {reason}")
    print(f"PASS: atomically published {len(published)} unique translation units to {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CompilationDatabaseError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
