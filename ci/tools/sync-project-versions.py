#!/usr/bin/env python3
"""Check or regenerate fixed setup-action views from the central version lock."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from version_updater_common import (PROJECT_VERSION_LOCK, TOOLCHAIN_FIELDS, UpdaterError,
    project_lock_snapshot, read_current_version_with_stat, replace_project_files, version_target)


def synchronize(root: Path, *, sync: bool = False) -> list[str]:
    directory = version_target(root, PROJECT_VERSION_LOCK).parent
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        pins, lock_stat = project_lock_snapshot(root)
        updates = []
        for filename, field in TOOLCHAIN_FIELDS.items():
            view, metadata = read_current_version_with_stat(
                root, version_filename=filename, parse_stable_version=lambda value: value)
            if view != pins[field]:
                updates.append((filename, f"{pins[field]}\n".encode(), view, metadata, lambda value: value, 64))
        if sync and updates:
            # The unchanged lock is included as the final checked commit point;
            # this rejects concurrent lock replacement before view changes.
            from version_updater_common import _parse_project_lock
            updates.append((PROJECT_VERSION_LOCK, (json.dumps(pins, indent=2) + "\n").encode(),
                            pins, lock_stat, _parse_project_lock, 4096))
            replace_project_files(root, updates)
        return [item[0] for item in updates if item[0] != PROJECT_VERSION_LOCK]
    finally:
        os.close(descriptor)


def verify_toolchain_update(root: Path, language: str, previous: bytes) -> None:
    from version_updater_common import _parse_project_lock, TargetError
    before = _parse_project_lock(previous.decode("utf-8"))
    after, _ = project_lock_snapshot(root)
    field = f"{language}_version"
    if any(after[key] != before[key] for key in before if key != field):
        raise TargetError("toolchain update changed another central lock field")
    if synchronize(root):
        raise TargetError("toolchain update has stale generated views")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--sync", action="store_true")
    mode.add_argument("--verify-update", choices=("python", "go"))
    args = parser.parse_args(argv)
    try:
        if args.verify_update:
            previous = subprocess.run(
                ["git", "--no-replace-objects", "-C", str(ROOT), "show", f"HEAD:{PROJECT_VERSION_LOCK}"],
                check=True, capture_output=True, timeout=30,
            ).stdout
            verify_toolchain_update(ROOT, args.verify_update, previous)
            changed = []
        else:
            changed = synchronize(ROOT, sync=args.sync)
    except (UpdaterError, OSError, UnicodeError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2
    print(json.dumps({"status": "synchronized" if args.sync else "valid" if not changed else "drift", "changed": changed}))
    return int(bool(changed) and args.check)


if __name__ == "__main__":
    raise SystemExit(main())
