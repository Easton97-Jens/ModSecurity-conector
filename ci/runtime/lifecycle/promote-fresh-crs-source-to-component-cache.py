#!/usr/bin/env python3
"""Safely move one verified CRS checkout into a private component cache.

The caller must re-run the Framework CRS provenance verifier after this
filesystem-only transfer and before publishing the destination path.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import os
from pathlib import Path
import stat
import sys
from typing import Iterable


RENAME_NOREPLACE = 1


class Blocked(RuntimeError):
    """A required path or filesystem invariant failed."""


def block(message: str) -> None:
    raise Blocked(message)


def absolute_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        block(f"{label} must be absolute")
    if ".." in path.parts or "." in path.parts:
        block(f"{label} contains traversal segments")
    return path


def relative_parts(root: Path, child: Path, label: str) -> tuple[str, ...]:
    try:
        relative = child.relative_to(root)
    except ValueError:
        block(f"{label} must stay under CELL_ROOT")
    if not relative.parts:
        block(f"{label} must not equal CELL_ROOT")
    return relative.parts


def require_directory(info: os.stat_result, label: str, *, private: bool = False) -> None:
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        block(f"{label} must be a non-symlink directory")
    if info.st_uid != os.geteuid():
        block(f"{label} must be owned by the current runner user")
    if private and stat.S_IMODE(info.st_mode) & 0o077:
        block(f"{label} must be private to the current runner user")


def open_checked_child(parent_fd: int, name: str, label: str) -> int:
    try:
        before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError as exc:
        raise Blocked(f"{label} is missing") from exc
    require_directory(before, label)
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        child_fd = os.open(name, flags, dir_fd=parent_fd)
    except OSError as exc:
        raise Blocked(f"{label} could not be opened without following symlinks: {exc}") from exc
    after = os.fstat(child_fd)
    if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
        os.close(child_fd)
        block(f"{label} changed while being opened")
    require_directory(after, label)
    return child_fd


def open_existing_path(root_fd: int, parts: Iterable[str], label: str) -> int:
    current_fd = os.dup(root_fd)
    try:
        for part in parts:
            next_fd = open_checked_child(current_fd, part, label)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except BaseException:
        os.close(current_fd)
        raise


def ensure_private_path(root_fd: int, parts: Iterable[str], label: str) -> int:
    current_fd = os.dup(root_fd)
    try:
        for part in parts:
            try:
                os.mkdir(part, 0o700, dir_fd=current_fd)
            except FileExistsError:
                pass
            next_fd = open_checked_child(current_fd, part, label)
            require_directory(os.fstat(next_fd), label, private=True)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except BaseException:
        os.close(current_fd)
        raise


def require_absent(parent_fd: int, name: str, label: str) -> None:
    try:
        os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    block(f"{label} must not exist before promotion")


def rename_no_replace(source_parent_fd: int, destination_parent_fd: int) -> None:
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = libc.renameat2
    except AttributeError as exc:
        raise Blocked("renameat2 with RENAME_NOREPLACE is unavailable") from exc
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        source_parent_fd,
        b"crs-fresh-source",
        destination_parent_fd,
        b"sources",
        RENAME_NOREPLACE,
    )
    if result == 0:
        return
    error_number = ctypes.get_errno()
    if error_number == errno.EXDEV:
        block("fresh CRS promotion crosses filesystems; copy fallback is prohibited")
    if error_number == errno.EEXIST:
        block("component CRS sources root already exists")
    block(f"fresh CRS promotion failed: {os.strerror(error_number)}")


def promote(args: argparse.Namespace) -> None:
    cell_root = absolute_path(args.cell_root, "CELL_ROOT")
    verified_run_root = absolute_path(args.verified_run_root, "VERIFIED_RUN_ROOT")
    cache_root = absolute_path(args.cache_root, "CACHE_ROOT")
    component_cache = absolute_path(args.component_cache, "CONNECTOR_COMPONENT_CACHE")
    source_root = absolute_path(args.source_root, "SOURCE_ROOT")
    crs_source_dir = absolute_path(args.crs_source_dir, "CRS_SOURCE_DIR")

    if verified_run_root != cell_root / "verified":
        block("VERIFIED_RUN_ROOT must be the fixed private cell verified root")
    if cache_root != cell_root / "cache":
        block("CACHE_ROOT must be the fixed private cell cache root")
    if component_cache != cache_root / "shared":
        block("CONNECTOR_COMPONENT_CACHE must be the fixed private shared cache root")
    if source_root != verified_run_root / "crs-fresh-source":
        block("SOURCE_ROOT must be the fresh verified CRS root")
    if crs_source_dir != source_root / "coreruleset":
        block("CRS_SOURCE_DIR must be the fresh verified coreruleset root")

    if os.path.realpath(cell_root) != str(cell_root):
        block("CELL_ROOT must not resolve through a symlink")
    cell_info = os.lstat(cell_root)
    require_directory(cell_info, "CELL_ROOT", private=True)

    cell_fd = os.open(cell_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    descriptors: list[int] = [cell_fd]
    try:
        verified_fd = open_existing_path(
            cell_fd,
            relative_parts(cell_root, verified_run_root, "VERIFIED_RUN_ROOT"),
            "VERIFIED_RUN_ROOT",
        )
        descriptors.append(verified_fd)
        fresh_fd = open_checked_child(verified_fd, "crs-fresh-source", "fresh CRS source root")
        descriptors.append(fresh_fd)
        fresh_crs_fd = open_checked_child(fresh_fd, "coreruleset", "fresh CRS source directory")
        descriptors.append(fresh_crs_fd)

        cache_fd = ensure_private_path(
            cell_fd,
            relative_parts(cell_root, cache_root, "CACHE_ROOT"),
            "private cache path",
        )
        descriptors.append(cache_fd)
        component_fd = ensure_private_path(cache_fd, ("shared",), "private component cache")
        descriptors.append(component_fd)
        require_directory(os.fstat(component_fd), "private component cache", private=True)
        require_absent(component_fd, "sources", "component CRS sources root")

        rename_no_replace(verified_fd, component_fd)

        try:
            os.stat("crs-fresh-source", dir_fd=verified_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            block("fresh CRS source root remained after promotion")

        promoted_fd = open_checked_child(component_fd, "sources", "promoted CRS sources root")
        descriptors.append(promoted_fd)
        promoted_crs_fd = open_checked_child(promoted_fd, "coreruleset", "promoted CRS source directory")
        descriptors.append(promoted_crs_fd)
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell-root", required=True)
    parser.add_argument("--verified-run-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--component-cache", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--crs-source-dir", required=True)
    return parser.parse_args()


def main() -> int:
    try:
        promote(parse_args())
    except Blocked as exc:
        print(f"BLOCKED: fresh CRS cache promotion: {exc}", file=sys.stderr)
        return 77
    except OSError as exc:
        print(f"BLOCKED: fresh CRS cache promotion filesystem failure: {exc}", file=sys.stderr)
        return 77
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
