"""Shared fail-closed reader for the repository's canonical Go version."""
from __future__ import annotations

import os
import stat
from pathlib import Path


MAX_VERSION_BYTES = 64


class GoVersionContractError(ValueError):
    """Raised when the fixed repository Go-version contract is unsafe."""


def _private_regular_file(metadata: os.stat_result) -> bool:
    return (
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_uid in {0, os.getuid()}
        and not metadata.st_mode & 0o022
        and metadata.st_size <= MAX_VERSION_BYTES
    )


def _private_root(root: Path) -> None:
    try:
        metadata = os.lstat(root)
    except OSError as exc:
        raise GoVersionContractError("repository root cannot be inspected safely") from exc
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid not in {0, os.getuid()}
        or metadata.st_mode & 0o022
    ):
        raise GoVersionContractError("repository root must be a private real directory")


def _reject_symlink_components(target: Path) -> None:
    current = Path(target.anchor)
    for part in target.parts[1:]:
        current /= part
        try:
            linked = current.is_symlink()
        except OSError as exc:
            raise GoVersionContractError(".go-version cannot be inspected safely") from exc
        if linked:
            raise GoVersionContractError(".go-version contains a symlink component")


def _read_version_file(target: Path) -> bytes:
    try:
        before_open = os.lstat(target)
    except OSError as exc:
        raise GoVersionContractError(".go-version cannot be inspected safely") from exc
    if not _private_regular_file(before_open):
        raise GoVersionContractError(".go-version must be a bounded private regular file")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise GoVersionContractError("platform cannot safely open .go-version without following symlinks")
    descriptor: int | None = None
    try:
        descriptor = os.open(target, os.O_RDONLY | nofollow)
        opened = os.fstat(descriptor)
        if not _private_regular_file(opened) or not os.path.samestat(before_open, opened):
            raise GoVersionContractError(".go-version changed while being opened")
        body = os.read(descriptor, MAX_VERSION_BYTES + 1)
    except GoVersionContractError:
        raise
    except OSError as exc:
        raise GoVersionContractError(".go-version cannot be read safely") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if len(body) > MAX_VERSION_BYTES:
        raise GoVersionContractError(".go-version is unexpectedly large")
    return body


def _canonical_version(body: bytes) -> str:
    try:
        value = body.decode("utf-8").removesuffix("\n")
    except UnicodeDecodeError as exc:
        raise GoVersionContractError(".go-version is not UTF-8") from exc
    major, separator, patch = value.partition(".")
    minor, separator, patch = patch.partition(".") if separator else ("", "", "")
    if (
        major != "1"
        or minor != "26"
        or not separator
        or not patch.isascii()
        or not patch.isdecimal()
    ):
        raise GoVersionContractError(".go-version must be an exact stable Go 1.26 patch")
    if len(patch) > 1 and patch.startswith("0"):
        raise GoVersionContractError(".go-version must be an exact stable Go 1.26 patch")
    return value


def read_go_version_contract(root: Path) -> str:
    """Read one bounded, private, canonical .go-version file."""
    _private_root(root)
    target = root / ".go-version"
    _reject_symlink_components(target)
    return _canonical_version(_read_version_file(target))
