"""Create Lighttpd harness outputs only below a verified private runtime root."""

from __future__ import annotations

import os
from pathlib import Path
import sys


_CI_LIB = Path(__file__).resolve().parents[3] / "ci" / "lib"
if str(_CI_LIB) not in sys.path:
    sys.path.insert(0, str(_CI_LIB))

from runtime_path_utils import (
    ensure_safe_runtime_directory,
    is_safe_runtime_root,
    is_under,
    read_runtime_artifact_text,
    runtime_artifact_path,
)


def verified_runtime_output_root(value: Path) -> Path:
    """Return one private runtime root, never a source or broad system path."""

    if not value.is_absolute():
        raise ValueError(f"runtime output root must be absolute: {value}")
    root = Path(os.path.abspath(value))
    if not is_safe_runtime_root(root):
        raise ValueError(f"runtime output root is unsafe for writes: {root}")
    return ensure_safe_runtime_directory(root)


def safe_output_path(root: Path, value: Path, label: str) -> Path:
    """Validate a regular output location strictly below the private root."""

    if not value.is_absolute():
        raise ValueError(f"{label} must be absolute: {value}")
    output = Path(os.path.abspath(value))
    if output == root or not is_under(output, root):
        raise ValueError(f"{label} must be below the runtime output root: {output}")
    if output.is_symlink():
        raise ValueError(f"{label} must not be a symbolic link: {output}")
    parent = ensure_safe_runtime_directory(output.parent)
    if not is_under(parent, root):
        raise ValueError(f"{label} parent escaped the runtime output root: {parent}")
    return output


def safe_input_path(root: Path, value: Path, label: str) -> Path:
    """Validate an existing regular runtime artifact before it is consumed."""

    return runtime_artifact_path(root, value, label, must_exist=True)


def read_runtime_input_text(root: Path, value: Path, label: str) -> str:
    """Read one validated runtime artifact without following symbolic links."""

    return read_runtime_artifact_text(root, value, label)


def write_text_atomic(root: Path, output: Path, content: str, label: str) -> Path:
    """Write one text artifact without following output or temporary-file links."""

    destination = safe_output_path(root, output, label)
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    if no_follow == 0:
        raise ValueError("safe runtime output creation requires O_NOFOLLOW")
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    descriptor = -1
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow,
            0o600,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination
