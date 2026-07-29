"""Safely read and write HAProxy HTX runtime artifacts below one private root."""

from __future__ import annotations

import os
from pathlib import Path
import secrets
import stat
import sys


_CI_LIB = Path(__file__).resolve().parents[3] / "ci" / "lib"
if str(_CI_LIB) not in sys.path:
    sys.path.insert(0, str(_CI_LIB))

from runtime_path_utils import ensure_safe_runtime_directory, is_safe_runtime_root, is_under


def verified_runtime_root(value: str | Path) -> Path:
    """Return a private root that may contain this invocation's artifacts."""

    root = Path(value)
    if not root.is_absolute():
        raise ValueError(f"runtime root must be absolute: {root}")
    normalized = Path(os.path.abspath(root))
    if not is_safe_runtime_root(normalized):
        raise ValueError(f"runtime root is unsafe for writes: {normalized}")
    return ensure_safe_runtime_directory(normalized)


def artifact_path(root: Path, value: str | Path, label: str, *, must_exist: bool) -> Path:
    """Validate an artifact path before any filesystem access.

    The root and every opened parent are checked by descriptor, and the final
    file is rejected when it is a symbolic link.  This keeps a CLI-provided
    path from crossing into a checkout, system directory, or sibling run.
    """

    candidate = Path(value)
    if not candidate.is_absolute():
        raise ValueError(f"{label} must be absolute: {candidate}")
    normalized = Path(os.path.abspath(candidate))
    if normalized == root or not is_under(normalized, root):
        raise ValueError(f"{label} must be below the runtime root: {normalized}")
    if normalized.is_symlink():
        raise ValueError(f"{label} must not be a symbolic link: {normalized}")
    parent = ensure_safe_runtime_directory(normalized.parent)
    if not is_under(parent, root):
        raise ValueError(f"{label} parent escaped the runtime root: {parent}")
    if must_exist and (not normalized.is_file() or normalized.is_symlink()):
        raise ValueError(f"{label} must be an existing regular file: {normalized}")
    return normalized


def _open_parent(target: Path) -> int:
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory is None:
        raise ValueError("safe runtime artifacts require O_NOFOLLOW and O_DIRECTORY")
    return os.open(target.parent, os.O_RDONLY | directory | no_follow)


def _require_regular_file(descriptor: int, label: str) -> None:
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        raise ValueError(f"{label} must be a regular file")


def read_text(root: Path, value: str | Path, label: str, *, errors: str | None = None) -> str:
    """Read one verified regular artifact without following its final link."""

    target = artifact_path(root, value, label, must_exist=True)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise ValueError("safe runtime artifact reads require O_NOFOLLOW")
    parent_descriptor = _open_parent(target)
    try:
        descriptor = os.open(target.name, os.O_RDONLY | no_follow, dir_fd=parent_descriptor)
        try:
            _require_regular_file(descriptor, label)
            with os.fdopen(descriptor, "r", encoding="utf-8", errors=errors) as stream:
                descriptor = -1
                return stream.read()
        finally:
            if descriptor >= 0:
                os.close(descriptor)
    finally:
        os.close(parent_descriptor)


def append_text(root: Path, value: str | Path, text: str, label: str) -> Path:
    """Append one private text artifact through a no-follow descriptor."""

    target = artifact_path(root, value, label, must_exist=False)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise ValueError("safe runtime artifact writes require O_NOFOLLOW")
    parent_descriptor = _open_parent(target)
    try:
        descriptor = os.open(
            target.name,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND | no_follow,
            0o600,
            dir_fd=parent_descriptor,
        )
        try:
            _require_regular_file(descriptor, label)
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                descriptor = -1
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            if descriptor >= 0:
                os.close(descriptor)
    finally:
        os.close(parent_descriptor)
    return target


def write_text_atomic(root: Path, value: str | Path, text: str, label: str) -> Path:
    """Replace one private regular artifact atomically without following links."""

    target = artifact_path(root, value, label, must_exist=False)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise ValueError("safe runtime artifact writes require O_NOFOLLOW")
    parent_descriptor = _open_parent(target)
    temporary_name: str | None = None
    try:
        try:
            existing = os.stat(target.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None and not stat.S_ISREG(existing.st_mode):
            raise ValueError(f"{label} must be a regular file")

        for _ in range(100):
            temporary_name = f".{target.name}.{secrets.token_hex(16)}.tmp"
            try:
                descriptor = os.open(
                    temporary_name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow,
                    0o600,
                    dir_fd=parent_descriptor,
                )
            except FileExistsError:
                continue
            break
        else:
            raise ValueError(f"could not allocate a temporary {label}")

        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            existing = os.stat(target.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None and not stat.S_ISREG(existing.st_mode):
            raise ValueError(f"{label} must be a regular file")
        os.replace(
            temporary_name,
            target.name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        os.close(parent_descriptor)
    return target
