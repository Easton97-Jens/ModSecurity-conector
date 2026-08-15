#!/usr/bin/env python3
"""Read and validate the HAProxy HTX overlay version contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
PATCH_RE = re.compile(r"^[A-Za-z0-9._-]+\.patch$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_contract(path: Path | None = None) -> dict[str, str | int]:
    contract_path = path or Path(__file__).with_name("version-contract.json")
    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
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
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise ValueError("contract version must be a semantic numeric version")
    if version_file != "VERSION":
        raise ValueError("contract source_version_file must be VERSION")
    if not isinstance(patch, str) or not PATCH_RE.fullmatch(patch):
        raise ValueError("contract makefile_patch must be a safe .patch filename")
    series = ".".join(version.split(".")[:2])
    expected_url = f"https://www.haproxy.org/download/{series}/src/haproxy-{version}.tar.gz"
    if source_url != expected_url:
        raise ValueError("contract source_url does not match the selected HAProxy version")
    if not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256):
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
