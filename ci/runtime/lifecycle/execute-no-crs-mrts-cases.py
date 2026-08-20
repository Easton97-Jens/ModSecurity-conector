#!/usr/bin/env python3
"""Execute a bounded no-CRS/with-MRTS plan against a real host endpoint."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, NoReturn

MAX_BYTES = 1_048_576
SHA256_RE = set("0123456789abcdef")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"FAIL: {message}")


def safe_root(value: str, label: str) -> Path:
    root = Path(value).expanduser()
    if not root.is_absolute() or ".." in root.parts:
        fail(f"{label} must be an absolute traversal-free path")
    component = Path(root.anchor)
    for part in root.parts[1:]:
        component /= part
        if component.exists() and component.is_symlink():
            fail(f"{label} contains a symlink component")
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    root = root.resolve(strict=True)
    if root.is_symlink() or os.stat(root).st_uid != os.getuid():
        fail(f"{label} is not a private owner-controlled directory")
    os.chmod(root, 0o700)
    return root


def confined(path: str, root: Path, label: str, *, regular: bool = True) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{label} is not absolute and traversal-free")
    try:
        resolved = candidate.resolve(strict=regular)
        if not regular:
            resolved.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        fail(f"{label} escapes its private root: {exc}")
    if candidate.is_symlink() or any(part.is_symlink() for part in candidate.parents if part.exists()):
        fail(f"{label} contains a symlink component")
    if regular and not resolved.is_file():
        fail(f"{label} is not a regular file")
    return resolved


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")


def atomic_json(path: Path, value: Any, root: Path) -> None:
    if path.parent != root and root not in path.parents:
        fail("output is outside private runtime root")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    if len(data) > MAX_BYTES:
        fail("result exceeds bounded size")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def event_ids(event_log: Path, correlation_id: str, connector: str, uri: str) -> set[str]:
    found: set[str] = set()
    if not event_log.exists():
        return found
    if event_log.stat().st_size > MAX_BYTES:
        fail("event log exceeds bounded size")
    for line in event_log.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line, object_pairs_hook=reject_duplicates)
        except (UnicodeError, json.JSONDecodeError) as exc:
            fail(f"event log is not duplicate-safe JSONL: {exc}")
        if not isinstance(item, dict):
            fail("event log entries must be JSON objects")
        if item.get("transaction_id") != correlation_id:
            continue
        if item.get("connector") != connector or item.get("uri") != uri:
            continue
        def walk(value: Any) -> None:
            if isinstance(value, dict):
                for key, nested in value.items():
                    if key in {"rule_id", "ruleId", "rule_ids", "matched_rule_ids", "matchedRuleIds", "expect_ids"}:
                        values = nested if isinstance(nested, list) else [nested]
                        found.update(str(entry) for entry in values if entry is not None)
                    else:
                        walk(nested)
            elif isinstance(value, list):
                for nested in value:
                    walk(nested)
        walk(item)
    return found


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise urllib.error.HTTPError(request.full_url, code, "redirect refused", headers, fp)


def request(url: str, method: str, headers: dict[str, str], timeout: float, context: ssl.SSLContext | None) -> int:
    req = urllib.request.Request(url, method=method, headers=headers)
    handlers: list[Any] = [NoRedirect]
    if context is not None:
        handlers.append(urllib.request.HTTPSHandler(context=context))
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(req, timeout=timeout) as response:
            response.read(MAX_BYTES)
            return int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read(MAX_BYTES)
        return int(exc.code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True, choices=("envoy", "traefik", "lighttpd"))
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--load-file", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--event-log", required=True)
    parser.add_argument("--scheme", choices=("http", "https"), default="http")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--tls-insecure", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-" for ch in args.host):
        fail("invalid host or port")
    if args.host != "127.0.0.1":
        fail("MRTS runtime endpoint must be 127.0.0.1")
    root = safe_root(args.runtime_root, "runtime root")
    plan_path = confined(args.plan, root, "plan")
    result_path = Path(args.result)
    if not result_path.is_absolute() or ".." in result_path.parts:
        fail("result is not traversal-free")
    result_path = result_path.resolve(strict=False)
    if root not in result_path.parents:
        fail("result escapes runtime root")
    if result_path.exists():
        fail("result already exists; recycled runtime evidence is forbidden")
    event_path = confined(args.event_log, root, "event log", regular=False)
    plan = load_json(plan_path)
    if not isinstance(plan, dict) or plan.get("profile") != "no-crs/with-mrts" or plan.get("connector") != args.connector:
        fail("plan profile or connector is not closed")
    cases = plan.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("plan has no cases")
    executor_record = plan.get("executor")
    executor_path = Path(__file__).resolve()
    if not isinstance(executor_record, dict) or executor_record.get("path") != str(executor_path):
        fail("plan executor path does not match the trusted executor")
    executor_sha = executor_record.get("sha256")
    if not isinstance(executor_sha, str) or len(executor_sha) != 64 or any(char not in SHA256_RE for char in executor_sha):
        fail("plan executor digest is invalid")
    if hashlib.sha256(executor_path.read_bytes()).hexdigest() != executor_sha:
        fail("executor digest mismatch")
    build_root = root.parent.parent.parent.parent
    load_path = Path(str(plan.get("load_file", "")))
    load_path = confined(str(load_path), build_root, "MRTS load file")
    supplied_load_path = confined(args.load_file, build_root, "supplied MRTS load file")
    if supplied_load_path != load_path:
        fail("supplied MRTS load file does not match the plan")
    load_sha = plan.get("load_file_sha256")
    if not isinstance(load_sha, str) or hashlib.sha256(load_path.read_bytes()).hexdigest() != load_sha:
        fail("MRTS load file digest mismatch")
    if "crs" in load_path.read_text(encoding="utf-8").lower():
        fail("CRS reference found in MRTS load file")
    inventory_root = confined(str(plan.get("inventory_root", "")), build_root, "MRTS inventory root", regular=False)
    if inventory_root.is_symlink() or not inventory_root.is_dir():
        fail("MRTS inventory root is not a regular contained directory")
    case_hashes = plan.get("case_hashes")
    if not isinstance(case_hashes, dict):
        fail("MRTS case hash map is missing")
    for relative, expected_hash in case_hashes.items():
        case_path = confined(str(inventory_root / str(relative)), inventory_root, "MRTS case")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64 or any(char not in SHA256_RE for char in expected_hash) or hashlib.sha256(case_path.read_bytes()).hexdigest() != expected_hash:
            fail(f"MRTS case digest mismatch: {relative}")
    for case in cases:
        if isinstance(case, dict) and case.get("source") not in (None, "") and str(case["source"]) not in case_hashes:
            fail("plan case references an unverified MRTS source")
    run_id = secrets.token_hex(12)
    tls_context = ssl._create_unverified_context() if args.tls_insecure else None
    observed: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or case.get("kind") not in {"control", "detection", "bypass"}:
            fail("invalid case kind")
        correlation_id = f"{run_id}-{index:04d}"
        # The current host adapters derive transaction_id from X-Request-ID.
        # Use one observable correlation value for both receipt identities;
        # inventing a second header would make raw event correlation fail.
        request_id = correlation_id
        transaction_id = correlation_id
        uri = case.get("uri")
        if not isinstance(uri, str) or len(uri) > 2048 or not uri.startswith("/") or any(ord(char) < 0x20 or ord(char) == 0x7F for char in uri):
            fail("invalid case URI")
        status = request(f"{args.scheme}://{args.host}:{args.port}{uri}", "GET", {
            "Host": args.host,
            "X-MRTS-Request-ID": request_id,
            "X-MRTS-Transaction-ID": transaction_id,
            "X-Request-ID": correlation_id,
            "User-Agent": "MRTS-runtime/1",
        }, 15.0, tls_context)
        raw_expected_ids = case.get("expect_ids", [])
        if not isinstance(raw_expected_ids, list) or any(not str(value).isdigit() or len(str(value)) > 12 for value in raw_expected_ids):
            fail("invalid expected rule ID")
        expected_ids = {str(value) for value in raw_expected_ids}
        matched = event_ids(event_path, correlation_id, args.connector, uri)
        if status != 200:
            fail(f"{case.get('id', index)} returned HTTP {status}, expected DetectionOnly 200")
        if case["kind"] == "detection" and not expected_ids.issubset(matched):
            fail(f"{case.get('id', index)} did not correlate expected rule IDs")
        if case["kind"] in {"control", "bypass"} and matched:
            fail(f"{case.get('id', index)} unexpectedly matched rules: {sorted(matched)}")
        observed.append({"case_id": case.get("id", str(index)), "kind": case["kind"], "uri": uri, "connector": args.connector, "correlation_id": correlation_id, "request_id": request_id, "transaction_id": transaction_id, "status": status, "expected_rule_ids": sorted(expected_ids), "observed_rule_ids": sorted(matched)})
    if not {item["kind"] for item in observed} >= {"control", "detection", "bypass"}:
        fail("plan must contain control, detection, and bypass cases")
    receipt = {"connector": args.connector, "profile": "no-crs/with-mrts", "run_id": run_id, "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(), "cases": observed, "status": "passed"}
    atomic_json(result_path, receipt, root)
    return 0


if __name__ == "__main__":
    main()
