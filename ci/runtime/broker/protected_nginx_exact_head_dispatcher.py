#!/usr/bin/env python3
"""Base-owned PR identity gate for the protected exact-head NGINX run.

This module is intentionally data-only: it does not import candidate code or
invoke a shell.  GitHub is queried through a fixed, unauthenticated HTTPS
endpoint and the resulting identity is written as a private atomic manifest.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

CANONICAL_REPOSITORY = "Easton97-Jens/ModSecurity-conector"
API_ROOT = "https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/pulls/"
USER_AGENT = "ModSecurity-conector-protected-exact-head-dispatcher"
MAX_RESPONSE_BYTES = 64 * 1024
MAX_RUN_ID_BYTES = 128
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SCHEMA_VERSION = 1
MANIFEST_FIELDS = frozenset({
    "schema_version", "trusted_dispatcher_base_sha", "run_id", "pr_number",
    "tested_pr_head", "tested_pr_head_ref", "tested_pr_head_repository",
    "tested_pr_base", "tested_pr_base_ref", "tested_pr_base_repository",
    "draft", "state", "merged",
})


class ContractError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ContractError(message)


def sha40(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA40_RE.fullmatch(value) is None:
        fail(f"{label} must be exactly 40 lowercase hexadecimal characters")
    return value


def duplicate_safe(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode_json(raw: bytes, label: str) -> Any:
    if len(raw) > MAX_RESPONSE_BYTES:
        fail(f"{label} exceeds {MAX_RESPONSE_BYTES} bytes")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_safe)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid UTF-8 JSON: {exc}")


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str,
                         headers: Any, newurl: str) -> None:
        fail("GitHub API redirects are rejected")


def fetch_pr(pr_number: int) -> dict[str, Any]:
    if type(pr_number) is not int or not 1 <= pr_number <= 999999999:
        fail("PR number is invalid")
    url = f"{API_ROOT}{pr_number}"
    request = Request(url, method="GET", headers={"Accept": "application/vnd.github+json",
                                                    "User-Agent": USER_AGENT})
    try:
        with build_opener(RejectRedirects()).open(request, timeout=15) as response:
            length = response.headers.get("Content-Length")
            if length is not None and (not length.isdigit() or int(length) > MAX_RESPONSE_BYTES):
                fail("GitHub API response is oversized")
            final_url = response.geturl()
            if final_url != url:
                fail("GitHub API final URL does not match the fixed endpoint")
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except ContractError:
        raise
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        fail(f"GitHub API request failed: {exc}")
    payload = decode_json(raw, "GitHub PR response")
    if not isinstance(payload, dict):
        fail("GitHub PR response must be an object")
    return payload


def branch_ref(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 255:
        fail(f"{label} is invalid")
    if value.startswith("refs/") or value.startswith("/") or value.endswith("/"):
        fail(f"{label} must be a branch ref, not a qualified ref")
    if any(ord(char) < 0x20 or ord(char) == 0x7f for char in value):
        fail(f"{label} contains control characters")
    if "\\" in value or ".." in value or "@{" in value:
        fail(f"{label} is not a safe branch ref")
    if value.endswith(".") or value.endswith(".lock") or value.startswith("."):
        fail(f"{label} is not a safe branch ref")
    return value


def nested(payload: dict[str, Any], key: str, label: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def validate_identity(payload: dict[str, Any], pr_number: int, expected_head: str) -> dict[str, Any]:
    if payload.get("number") != pr_number:
        fail("GitHub PR number does not match the requested PR")
    if payload.get("state") != "open":
        fail("pull request is not open")
    if payload.get("merged_at") is not None:
        fail("pull request is merged")
    if type(payload.get("merged")) is not bool:
        fail("pull request merged field is not boolean")
    if payload["merged"]:
        fail("pull request is merged")
    if type(payload.get("draft")) is not bool:
        fail("pull request draft field is not boolean")
    base = nested(payload, "base", "base")
    head = nested(payload, "head", "head")
    base_ref = branch_ref(base.get("ref"), "base.ref")
    branch_ref(head.get("ref"), "head.ref")
    if base_ref != "master":
        fail("pull request base ref must be master")
    base_repo = nested(base, "repo", "base.repo")
    head_repo = nested(head, "repo", "head.repo")
    if base_repo.get("full_name") != CANONICAL_REPOSITORY:
        fail("base repository is not canonical")
    if head_repo.get("full_name") != CANONICAL_REPOSITORY:
        fail("head repository must not be a fork")
    base_sha = sha40(base.get("sha"), "base.sha")
    head_sha = sha40(head.get("sha"), "head.sha")
    expected_head = sha40(expected_head, "expected head SHA")
    if head_sha != expected_head:
        fail("pull request head SHA is stale or does not match expected SHA")
    return {"pr_number": pr_number, "tested_pr_base_ref": base_ref,
            "tested_pr_base": base_sha, "tested_pr_head_ref": head.get("ref"),
            "tested_pr_head": head_sha,
            "tested_pr_base_repository": CANONICAL_REPOSITORY,
            "tested_pr_head_repository": CANONICAL_REPOSITORY, "draft": payload["draft"],
            "state": "open", "merged": False}


def validate_run_id(value: str) -> str:
    if not isinstance(value, str) or len(value.encode()) > MAX_RUN_ID_BYTES or RUN_ID_RE.fullmatch(value) is None:
        fail("run ID is invalid")
    return value


def make_manifest(pr_number: int, expected_head: str, dispatcher_base_sha: str,
                  run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    identity = validate_identity(payload, pr_number, expected_head)
    return {"schema_version": SCHEMA_VERSION, "trusted_dispatcher_base_sha": sha40(dispatcher_base_sha, "dispatcher base SHA"),
            "run_id": validate_run_id(run_id), **identity}


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    if not path.is_absolute() or path.name in {"", ".", ".."}:
        fail("manifest path must be absolute")
    parent = path.parent
    try:
        metadata = parent.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            fail("manifest parent must be a directory")
        if stat.S_IMODE(metadata.st_mode) & 0o077:
            fail("manifest parent must not be accessible by group or other users")
        fd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            temp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            out = os.open(temp, flags, 0o600)
            try:
                data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
                offset = 0
                while offset < len(data):
                    written = os.write(out, data[offset:])
                    if written <= 0:
                        fail("could not write complete manifest")
                    offset += written
                os.fsync(out)
            finally:
                os.close(out)
            os.replace(temp, path)
            os.chmod(path, 0o600)
            os.fsync(fd)
        finally:
            os.close(fd)
    except ContractError:
        raise
    except OSError as exc:
        fail(f"could not write private manifest: {exc}")


def read_manifest(path: Path) -> dict[str, Any]:
    fd = -1
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode) != 0o600 or before.st_nlink != 1:
            fail("manifest permissions must be 0600")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, MAX_RESPONSE_BYTES + 1 - total)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_RESPONSE_BYTES:
                fail("manifest exceeds size limit")
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_nlink) != (
                after.st_dev, after.st_ino, after.st_size, after.st_nlink):
            fail("manifest changed while being read")
        raw = b"".join(chunks)
    except OSError as exc:
        fail(f"could not read manifest: {exc}")
    finally:
        if fd >= 0:
            os.close(fd)
    payload = decode_json(raw, "manifest")
    if not isinstance(payload, dict):
        fail("manifest must be an object")
    return payload


def verify_manifest(path: Path, *, pr_number: int | None = None,
                    expected_head_sha: str | None = None,
                    dispatcher_base_sha: str | None = None) -> dict[str, Any]:
    manifest = read_manifest(path)
    if frozenset(manifest) != MANIFEST_FIELDS:
        fail("manifest fields are not exactly the dispatcher schema")
    if (
        type(manifest.get("schema_version")) is not int
        or manifest["schema_version"] != SCHEMA_VERSION
    ):
        fail("unsupported manifest schema")
    manifest_pr_number = manifest.get("pr_number")
    if type(manifest_pr_number) is not int:
        fail("manifest PR number is invalid")
    if pr_number is not None and manifest_pr_number != pr_number:
        fail("manifest PR number does not match requested PR")
    expected = sha40(manifest.get("tested_pr_head"), "manifest tested PR head SHA")
    if expected_head_sha is not None and expected != sha40(expected_head_sha, "expected head SHA"):
        fail("manifest head SHA does not match requested head")
    trusted_base = sha40(manifest.get("trusted_dispatcher_base_sha"), "manifest dispatcher base SHA")
    if dispatcher_base_sha is not None and trusted_base != sha40(dispatcher_base_sha, "dispatcher base SHA"):
        fail("manifest dispatcher base SHA does not match requested base")
    current = make_manifest(manifest_pr_number, expected, trusted_base, manifest.get("run_id"), fetch_pr(manifest_pr_number))
    if current != manifest:
        fail("PR identity changed after dispatch (TOCTOU detected)")
    return current


def emit_outputs(path: Path, output_path: Path) -> None:
    """Write only validated scalar fields to the GitHub job-output file."""
    manifest = read_manifest(path)
    values = {
        "tested_pr_head": sha40(manifest["tested_pr_head"], "manifest tested PR head SHA"),
        "tested_pr_base": sha40(manifest["tested_pr_base"], "manifest tested PR base SHA"),
        "trusted_dispatcher_base_sha": sha40(
            manifest["trusted_dispatcher_base_sha"], "manifest dispatcher base SHA"
        ),
    }
    if not output_path.is_absolute():
        fail("output path must be absolute")
    data = "".join(f"{key}={value}\n" for key, value in values.items()).encode("ascii")
    try:
        fd = os.open(output_path, os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
        try:
            metadata = os.fstat(fd)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                fail("output path must be a regular non-hardlinked file")
            offset = 0
            while offset < len(data):
                offset += os.write(fd, data[offset:])
        finally:
            os.close(fd)
    except OSError as exc:
        fail(f"could not write job outputs: {exc}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    dispatch = sub.add_parser("dispatch")
    dispatch.add_argument("--pr-number", type=int, required=True)
    dispatch.add_argument("--expected-head-sha", required=True)
    dispatch.add_argument("--dispatcher-base-sha", required=True)
    dispatch.add_argument("--run-id", required=True)
    dispatch.add_argument("--output", type=Path, required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--pr-number", type=int)
    verify.add_argument("--expected-head-sha")
    verify.add_argument("--dispatcher-base-sha")
    emit = sub.add_parser("emit-outputs")
    emit.add_argument("--manifest", type=Path, required=True)
    emit.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "dispatch":
            payload = make_manifest(args.pr_number, args.expected_head_sha, args.dispatcher_base_sha,
                                    args.run_id, fetch_pr(args.pr_number))
            write_manifest(args.output, payload)
        else:
            if args.command == "verify":
                verify_manifest(args.manifest, pr_number=args.pr_number,
                                expected_head_sha=args.expected_head_sha,
                                dispatcher_base_sha=args.dispatcher_base_sha)
            else:
                emit_outputs(args.manifest, args.output)
        return 0
    except ContractError as exc:
        print(f"protected exact-head dispatcher: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
