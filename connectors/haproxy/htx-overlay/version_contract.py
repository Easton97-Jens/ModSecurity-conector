#!/usr/bin/env python3
"""Read and validate the HAProxy HTX overlay version contract."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys


CONTRACT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONTRACT = CONTRACT_ROOT / "version-contract.json"


def _ascii_digits(value: str) -> bool:
    return bool(value) and all("0" <= character <= "9" for character in value)


def _valid_version(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value.split(".")) == 3
        and all(_ascii_digits(part) for part in value.split("."))
    )


def _valid_patch_name(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith(".patch"):
        return False
    stem = value[:-len(".patch")]
    return bool(stem) and Path(value).name == value and all(
        "A" <= character <= "Z"
        or "a" <= character <= "z"
        or "0" <= character <= "9"
        or character in "._-"
        for character in stem
    )


def _valid_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all("0" <= character <= "9" or "a" <= character <= "f" for character in value)
    )


def _read_contract(path: Path | None) -> object:
    requested = path or DEFAULT_CONTRACT
    root = CONTRACT_ROOT
    candidate = requested.absolute()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("HAProxy HTX version contract is outside the allowed root") from exc
    if candidate.is_symlink():
        raise ValueError("HAProxy HTX version contract must not be a symlink")
    resolved = candidate.resolve(strict=True)
    if resolved != candidate:
        raise ValueError("HAProxy HTX version contract resolves through a symlink")
    if not resolved.is_file():
        raise ValueError("HAProxy HTX version contract must be a regular file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as exc:
        raise ValueError(f"cannot open HAProxy HTX version contract: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("HAProxy HTX version contract must be a regular file")
        with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
            descriptor = -1
            return json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read HAProxy HTX version contract: {exc}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def load_contract(path: Path | None = None) -> dict[str, str | int]:
    try:
        raw = _read_contract(path)
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read HAProxy HTX version contract: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("HAProxy HTX version contract must be a JSON object")
    if raw.get("schema_version") != 1 or raw.get("component") != "haproxy-htx-overlay":
        raise ValueError("unsupported HAProxy HTX version-contract schema or component")
    version = raw.get("version")
    version_file = raw.get("source_version_file")
    patch = raw.get("makefile_patch")
    source_url = raw.get("source_url")
    sha256 = raw.get("sha256")
    if not _valid_version(version):
        raise ValueError("contract version must be a semantic numeric version")
    if version_file != "VERSION":
        raise ValueError("contract source_version_file must be VERSION")
    if not _valid_patch_name(patch):
        raise ValueError("contract makefile_patch must be a safe .patch filename")
    series = ".".join(version.split(".")[:2])
    expected_url = f"https://www.haproxy.org/download/{series}/src/haproxy-{version}.tar.gz"
    if source_url != expected_url:
        raise ValueError("contract source_url does not match the selected HAProxy version")
    if not _valid_sha256(sha256):
        raise ValueError("contract sha256 must be a SHA-256 digest")
    return {
        "schema_version": 1,
        "component": "haproxy-htx-overlay",
        "version": version,
        "source_url": source_url,
        "sha256": sha256,
        "source_version_file": version_file,
        "makefile_patch": patch,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--field", choices=("version", "source_url", "sha256", "source_version_file", "makefile_patch"), required=True)
    parser.add_argument("--contract", type=Path)
    args = parser.parse_args(argv)
    try:
        contract = load_contract(args.contract)
    except ValueError as exc:
        print(f"version-contract: {exc}", file=sys.stderr)
        return 1
    print(contract[args.field])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
