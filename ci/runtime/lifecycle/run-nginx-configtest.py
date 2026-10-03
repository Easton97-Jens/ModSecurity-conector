#!/usr/bin/env python3
"""Run one closed, configuration-only NGINX rejection contract.

This does not start a daemon, bind a listener, send HTTP, or create native
transaction events. Unit tests use controlled executables, not runtime proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import stat
import subprocess
import time


CAPTURE_LIMIT = 65536
TIMEOUT_SECONDS = 10
ARTIFACT_LIMIT = 64 * 1024 * 1024
CONFIGTEST_CONTRACTS = {
    "invalid_boolean": {
        "operation": "configtest", "directive": "modsecurity", "value": "maybe",
        "expected_exit_code": 1, "expected_outcome": "config_rejected",
        "error_class": "invalid_boolean",
        "diagnostic_fragments": ['"modsecurity" directive', "invalid boolean value"],
    },
    "invalid_size": {
        "operation": "configtest", "directive": "modsecurity_phase4_body_limit", "value": "maybe",
        "expected_exit_code": 1, "expected_outcome": "config_rejected",
        "error_class": "invalid_size",
        "diagnostic_fragments": ['"modsecurity_phase4_body_limit" directive',
                                 "invalid value for modsecurity_phase4_body_limit"],
    },
}
PARENT_ROOT = Path(__file__).resolve().parents[3]


def absolute_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or not re.fullmatch(r"/[A-Za-z0-9_./-]+", value):
        raise ValueError("paths must be absolute and configuration-safe")
    if any(part in (".", "..") for part in value.split("/")):
        raise ValueError("paths must not contain traversal components")
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError("symlink paths are not authorized")
    return path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_checkout(path: Path) -> bool:
    """A protected placeholder .git directory alone is not a checkout."""
    marker = path / ".git"
    return marker.is_file() or (marker / "HEAD").is_file()


def snapshot_artifact(path: Path, destination: Path, *, executable: bool) -> str:
    """Retain and hash bounded regular-file bytes via non-following descriptors."""
    result = hashlib.sha256()
    source_fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(source_fd, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > ARTIFACT_LIMIT:
            raise ValueError("artifact must be a regular file no larger than 64 MiB")
        destination_fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o700 if executable else 0o600)
        with os.fdopen(destination_fd, "wb") as retained:
            total = 0
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                total += len(chunk)
                if total > ARTIFACT_LIMIT:
                    raise ValueError("artifact grew beyond the 64 MiB limit")
                result.update(chunk)
                retained.write(chunk)
    return result.hexdigest()


def invoke(argv: list[str], environment: dict[str, str]) -> tuple[int, bytes, bytes, str | None]:
    """Capture both streams with a hard combined byte limit and deadline."""
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    failure = None
    with subprocess.Popen(argv, env=environment, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        deadline = time.monotonic() + TIMEOUT_SECONDS
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, "stdout")
            selector.register(process.stderr, selectors.EVENT_READ, "stderr")
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    failure = "configtest_timeout"
                    break
                for key, _ in selector.select(min(remaining, 0.2)):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    capacity = CAPTURE_LIMIT - sum(map(len, captured.values()))
                    captured[key.data].extend(chunk[:capacity])
                    if len(chunk) > capacity:
                        failure = "configtest_capture_limit"
                        break
                if failure:
                    break
        if failure:
            process.kill()
        try:
            exit_code = process.wait(timeout=max(0.01, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            process.kill()
            exit_code = process.wait()
            failure = "configtest_timeout"
    return exit_code, bytes(captured["stdout"]), bytes(captured["stderr"]), failure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True, choices=CONFIGTEST_CONTRACTS)
    for name in ("nginx-binary", "module", "output-root", "run-id", "parent-sha",
                 "framework-sha", "mrts-sha"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--library-dir")
    args = parser.parse_args()
    contract = CONFIGTEST_CONTRACTS[args.case_id]
    try:
        binary, module, output = map(absolute_path, (args.nginx_binary, args.module, args.output_root))
        if not binary.is_file() or not os.access(binary, os.X_OK) or not module.is_file():
            raise ValueError("an executable binary and regular module are required")
        storage_root = Path("/var/tmp/codex/ModSecurity-conector")
        if storage_root not in output.parents:
            raise ValueError("output must be under the authorized external task storage")
        if (output == PARENT_ROOT or PARENT_ROOT in output.parents
                or any(is_checkout(ancestor) for ancestor in output.parents
                       if ancestor != storage_root and storage_root in ancestor.parents)):
            raise ValueError("output must be outside the checkout")
        if output.exists() or not output.parent.is_dir():
            raise ValueError("output must be a fresh child of an existing external parent")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", args.run_id):
            raise ValueError("run identity must be bounded and path-safe")
        for sha in (args.parent_sha, args.framework_sha, args.mrts_sha):
            if not re.fullmatch(r"[0-9a-f]{40}", sha):
                raise ValueError("exact source identities must be 40-character lowercase SHAs")
        environment = {"PATH": os.defpath, "LANG": "C", "LC_ALL": "C"}
        if args.library_dir:
            library = absolute_path(args.library_dir)
            if not library.is_dir():
                raise ValueError("library directory must exist")
            environment["LD_LIBRARY_PATH"] = str(library)
        output.mkdir(mode=0o700)
        retained_binary = output / "nginx-binary"
        retained_module = output / "nginx-module.so"
        binary_sha = snapshot_artifact(binary, retained_binary, executable=True)
        module_sha = snapshot_artifact(module, retained_module, executable=False)
        configuration = (
            f'load_module "{retained_module}";\n'
            f'pid "{output}/nginx.pid";\n'
            f'error_log "{output}/nginx-error.log";\n'
            "events {}\nhttp {\n"
            f"  {contract['directive']} {contract['value']};\n"
            "}\n"
        ).encode("utf-8")
        config_path = output / "nginx.conf"
        config_path.write_bytes(configuration)
        try:
            exit_code, stdout, stderr, failure = invoke(
                [str(retained_binary), "-e", "stderr", "-t", "-c", str(config_path), "-p", str(output) + "/"], environment,
            )
        except OSError:
            exit_code, stdout, stderr, failure = -1, b"", b"", "configtest_exec_error"
        (output / "stdout.log").write_bytes(stdout)
        (output / "stderr.log").write_bytes(stderr)
        text = stderr.decode("utf-8", errors="replace")
        fragments = contract["diagnostic_fragments"]
        matched = [fragment for fragment in fragments if fragment in text]
        expected_exit = contract["expected_exit_code"]
        passed = not failure and exit_code == expected_exit and matched == fragments
        receipt = {
            "schema_version": 1, "case_id": args.case_id, "connector": "nginx",
            "operation": "configtest", "run_id": args.run_id,
            "integration_mode": "native-nginx-http-module", "parent_sha": args.parent_sha,
            "framework_sha": args.framework_sha, "mrts_sha": args.mrts_sha,
            "binary_sha256": binary_sha, "module_sha256": module_sha,
            "config_path_identity": "sha256:" + digest(configuration),
            "directive": contract["directive"], "value": contract["value"],
            "expected_outcome": contract["expected_outcome"],
            "expected_exit_code": expected_exit, "observed_exit_code": exit_code,
            "observed_outcome": contract["expected_outcome"] if exit_code == expected_exit and not failure else "unexpected_outcome",
            "error_class": contract["error_class"] if passed else failure or "unexpected_config_error",
            "diagnostic_fragments": matched, "stdout_sha256": digest(stdout),
            "stderr_sha256": digest(stderr), "process_started": False, "listener_created": False,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        result = {"cases": [{"case_id": args.case_id, "status": "PASS" if passed else "FAIL",
                             "live_executed": failure != "configtest_exec_error",
                             "actual_status": exit_code, "observed_result": receipt["observed_outcome"],
                             "run_id": args.run_id, "integration_mode": receipt["integration_mode"],
                             "artifacts": {"configtest_dir": str(output)},
                             "configtest_receipt": receipt}]}
        (output / "source-result.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        (output / "source-result.jsonl").write_text(
            json.dumps(result["cases"][0], sort_keys=True) + "\n", encoding="utf-8",
        )
        return 0 if passed else 1
    except (ValueError, OSError) as error:
        parser.exit(2, "configtest input/output rejected: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
