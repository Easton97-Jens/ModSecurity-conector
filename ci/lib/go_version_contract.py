"""Shared fail-closed reader for the repository's canonical Go version."""
from __future__ import annotations

import os
import re
import stat
from pathlib import Path


VERSION_RE = re.compile(r"1\.26\.(?:0|[1-9][0-9]*)\n?\Z", re.ASCII)
MAX_VERSION_BYTES = 64


class GoVersionContractError(ValueError):
    """Raised when the fixed repository Go-version contract is unsafe."""


def read_go_version_contract(root: Path) -> str:
    """Read one bounded, private, canonical .go-version file."""

    try:
        root_stat = os.lstat(root)
    except OSError as exc:
        raise GoVersionContractError("repository root cannot be inspected safely") from exc
    if (
        stat.S_ISLNK(root_stat.st_mode)
        or not stat.S_ISDIR(root_stat.st_mode)
        or root_stat.st_uid not in {0, os.getuid()}
        or root_stat.st_mode & 0o022
    ):
        raise GoVersionContractError("repository root must be a private real directory")
    target = root / ".go-version"
    current = Path(target.anchor)
    for part in target.parts[1:]:
        current /= part
        try:
            if current.is_symlink():
                raise GoVersionContractError(".go-version contains a symlink component")
        except OSError as exc:
            raise GoVersionContractError(".go-version cannot be inspected safely") from exc
    try:
        before_open = os.lstat(target)
    except OSError as exc:
        raise GoVersionContractError(".go-version cannot be inspected safely") from exc
    if (
        not stat.S_ISREG(before_open.st_mode)
        or before_open.st_uid not in {0, os.getuid()}
        or before_open.st_mode & 0o022
        or before_open.st_size > MAX_VERSION_BYTES
    ):
        raise GoVersionContractError(".go-version must be a bounded private regular file")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise GoVersionContractError("platform cannot safely open .go-version without following symlinks")
    descriptor: int | None = None
    try:
        descriptor = os.open(target, os.O_RDONLY | nofollow)
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or not os.path.samestat(before_open, opened)
            or opened.st_uid not in {0, os.getuid()}
            or opened.st_mode & 0o022
            or opened.st_size > MAX_VERSION_BYTES
        ):
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
    try:
        value = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GoVersionContractError(".go-version is not UTF-8") from exc
    if not VERSION_RE.fullmatch(value):
        raise GoVersionContractError(".go-version must be an exact stable Go 1.26 patch")
    return value[:-1] if value.endswith("\n") else value
