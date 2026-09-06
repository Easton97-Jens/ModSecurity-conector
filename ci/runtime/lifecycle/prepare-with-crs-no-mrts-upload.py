#!/usr/bin/env python3
"""Validate generic CRS/no-MRTS evidence or publish a bounded failure receipt.

The receipt contains workflow metadata only.  It is deliberately not a
replacement for runtime evidence: a failed runtime remains a failed job.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path


GENERIC_CONNECTORS = frozenset(("envoy", "lighttpd", "traefik"))
FAILURE_RECEIPT_CONNECTORS = GENERIC_CONNECTORS | frozenset(("apache",))
OUTCOMES = frozenset(("success", "failure", "cancelled", "skipped"))
MAX_RECORD_BYTES = 65536
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,47}$")


def sha(value: str) -> bool:
    return len(value) == 40 and all(char in "0123456789abcdef" for char in value)


def identity(details: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        details.st_dev,
        details.st_ino,
        stat.S_IFMT(details.st_mode),
        details.st_size,
        details.st_nlink,
        details.st_uid,
        stat.S_IMODE(details.st_mode),
    )


def require_safe_directory(details: os.stat_result, label: str) -> None:
    if (
        not stat.S_ISDIR(details.st_mode)
        or details.st_uid != os.geteuid()
        or stat.S_IMODE(details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
    ):
        raise ValueError(f"{label} is not a private current-user directory")


def require_safe_regular(details: os.stat_result, label: str) -> None:
    if (
        not stat.S_ISREG(details.st_mode)
        or details.st_uid != os.geteuid()
        or details.st_nlink != 1
        or stat.S_IMODE(details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
        or details.st_size > MAX_RECORD_BYTES
    ):
        raise ValueError(f"{label} is not a bounded private regular file")


def require_verified_root(path: Path) -> Path:
    root = Path(os.path.abspath(path))
    if not root.is_absolute() or root == Path("/"):
        raise ValueError("verified root is not an absolute non-root path")
    before = root.lstat()
    if stat.S_ISLNK(before.st_mode):
        raise ValueError("verified root is a symlink")
    require_safe_directory(before, "verified root")
    return root


def open_private_directory(path: Path, label: str) -> int:
    before = path.lstat()
    if stat.S_ISLNK(before.st_mode):
        raise ValueError(f"{label} is a symlink")
    require_safe_directory(before, label)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory is None:
        raise ValueError("safe evidence access requires no-follow directory support")
    descriptor = os.open(path, os.O_RDONLY | directory | no_follow)
    try:
        opened = os.fstat(descriptor)
        if identity(opened) != identity(before):
            raise ValueError(f"{label} changed between validation and open")
        require_safe_directory(opened, label)
    except BaseException:
        os.close(descriptor)
        raise
    return descriptor


def read_evidence(root: Path, components: tuple[str, ...], label: str) -> bytes:
    if not components:
        raise ValueError("evidence path is empty")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if no_follow is None or directory is None or nonblock is None:
        raise ValueError("safe evidence access requires no-follow non-blocking support")
    directory_descriptor = open_private_directory(root, "verified root")
    try:
        for component in components[:-1]:
            before = os.stat(component, dir_fd=directory_descriptor, follow_symlinks=False)
            require_safe_directory(before, label)
            next_descriptor = os.open(
                component,
                os.O_RDONLY | directory | no_follow,
                dir_fd=directory_descriptor,
            )
            try:
                opened = os.fstat(next_descriptor)
                if identity(opened) != identity(before):
                    raise ValueError(f"{label} directory changed between validation and open")
                require_safe_directory(opened, label)
            except BaseException:
                os.close(next_descriptor)
                raise
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        before = os.stat(
            components[-1], dir_fd=directory_descriptor, follow_symlinks=False
        )
        require_safe_regular(before, label)
        file_descriptor = os.open(
            components[-1], os.O_RDONLY | no_follow | nonblock, dir_fd=directory_descriptor
        )
    finally:
        os.close(directory_descriptor)
    try:
        opened = os.fstat(file_descriptor)
        if identity(opened) != identity(before):
            raise ValueError(f"{label} changed between validation and open")
        require_safe_regular(opened, label)
        chunks: list[bytes] = []
        remaining = MAX_RECORD_BYTES + 1
        while remaining:
            chunk = os.read(file_descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        after = os.fstat(file_descriptor)
        if identity(after) != identity(opened):
            raise ValueError(f"{label} changed while reading")
        require_safe_regular(after, label)
    finally:
        os.close(file_descriptor)
    if len(data) > MAX_RECORD_BYTES:
        raise ValueError(f"{label} exceeds its bound")
    return data


def load_pass_evidence(root: Path, connector: str, run_id: str, parent_sha: str) -> None:
    record = json.loads(
        read_evidence(
            root,
            ("evidence", "runtime", connector, run_id, "runtime.json"),
            "runtime evidence",
        ).decode("utf-8")
    )
    event = json.loads(
        read_evidence(
            root,
            ("evidence", "normalized", connector, run_id, "event.json"),
            "normalized event evidence",
        ).decode("utf-8")
    )
    observation_data = read_evidence(
        root,
        (
            "evidence",
            "normalized",
            connector,
            run_id,
            "runtime-observation.json",
        ),
        "normalized observation evidence",
    )
    if not isinstance(record, dict) or not isinstance(event, dict):
        raise ValueError("runtime evidence is not an object")
    if (
        record.get("record_type") != "parent_runtime_attestation"
        or record.get("connector") != connector
        or record.get("run_id") != run_id
        or record.get("runtime_status") != "PASS"
    ):
        raise ValueError("runtime evidence binding or status is invalid")
    if (
        event.get("connector") != connector
        or event.get("run_id") != run_id
        or event.get("connector_commit") != parent_sha
        or event.get("status") != "PASS"
    ):
        raise ValueError("normalized evidence binding or status is invalid")
    canonical_observation = record.get("canonical_observation")
    expected_path = f"normalized/{connector}/{run_id}/runtime-observation.json"
    if (
        not isinstance(canonical_observation, dict)
        or canonical_observation.get("validation_status") != "CONTRACT_VALIDATED"
        or canonical_observation.get("evidence_path") != expected_path
        or canonical_observation.get("evidence_sha256")
        != hashlib.sha256(observation_data).hexdigest()
    ):
        raise ValueError("runtime observation binding is invalid")


def write_receipt(
    root: Path, connector: str, run_id: str, parent_sha: str, outcome: str, reason: str
) -> None:
    document = {
        "schema_version": 1,
        "record_type": "crs_no_mrts_runtime_failure_receipt",
        "connector": connector,
        "run_id": run_id,
        "connector_commit": parent_sha,
        "runtime_outcome": outcome,
        "evidence_status": "not_available",
        "reason": reason[:128],
    }
    data = (
        json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    if len(data) > 4096:
        raise ValueError("failure receipt exceeds its bound")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise ValueError("safe receipt publication requires no-follow support")
    root_descriptor = open_private_directory(root, "verified root")
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow
        descriptor = os.open("failure-receipt.json", flags, 0o600, dir_fd=root_descriptor)
        try:
            remaining = memoryview(data)
            while remaining:
                written = os.write(descriptor, remaining)
                if written <= 0:
                    raise OSError("short failure-receipt write")
                remaining = remaining[written:]
            os.fsync(descriptor)
            require_safe_regular(os.fstat(descriptor), "failure receipt")
        finally:
            os.close(descriptor)
        os.fsync(root_descriptor)
    finally:
        os.close(root_descriptor)


def receipt_exists(root: Path) -> bool:
    descriptor = open_private_directory(root, "verified root")
    try:
        try:
            os.stat("failure-receipt.json", dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return True
    finally:
        os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--parent-sha", required=True)
    parser.add_argument("--verified-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--runtime-outcome", required=True)
    args = parser.parse_args()
    if (
        args.connector not in FAILURE_RECEIPT_CONNECTORS
        or not RUN_ID.fullmatch(args.run_id)
        or not sha(args.parent_sha)
    ):
        return 2
    if args.runtime_outcome not in OUTCOMES:
        return 2
    try:
        verified_root = require_verified_root(args.verified_root)
        expected_receipt = verified_root / "failure-receipt.json"
        if Path(os.path.abspath(args.receipt)) != expected_receipt:
            raise ValueError("failure receipt escapes the verified runtime root")
    except (OSError, ValueError) as exc:
        print(f"FAIL: unsafe runtime evidence root: {exc}", file=os.sys.stderr)
        return 1
    if args.runtime_outcome != "success":
        try:
            write_receipt(
                verified_root,
                args.connector,
                args.run_id,
                args.parent_sha,
                args.runtime_outcome,
                "runtime did not complete successfully",
            )
        except (FileExistsError, OSError, ValueError) as receipt_error:
            print(
                f"FAIL: unable to retain bounded runtime failure receipt: {receipt_error}",
                file=os.sys.stderr,
            )
            return 1
        return 0
    if args.connector not in GENERIC_CONNECTORS:
        return 2
    try:
        load_pass_evidence(verified_root, args.connector, args.run_id, args.parent_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: runtime evidence validation failed: {exc}", file=os.sys.stderr)
        return 1
    if receipt_exists(verified_root):
        print("FAIL: unexpected failure receipt accompanies PASS evidence", file=os.sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
