#!/usr/bin/env python3
"""Smoke checks for ci/tools/generate-block-status-config.py."""

from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
GENERATOR = REPO_ROOT / "ci" / "tools" / "generate-block-status-config.py"
HEADER = "msconnector_block_statuses.generated.h"
SOURCE = "msconnector_block_statuses.generated.c"
HAPROXY_CFG = "haproxy-block-status-rules.generated.cfg"


FULL_STATUS_LIST = "400,401,403,404,405,406,408,409,410,413,415,418,422,425,429,451,500,501,502,503,504"
FULL_STATUSES = tuple(int(value) for value in FULL_STATUS_LIST.split(","))
DEFAULT_WEB_SERVER_STATUSES = "403,501"

RUNS = (
    ("nginx", DEFAULT_WEB_SERVER_STATUSES),
    ("apache", DEFAULT_WEB_SERVER_STATUSES),
    ("haproxy", "401,403,406,429,501,503"),
    ("envoy", "403"),
    ("traefik", "403"),
    ("lighttpd", "403"),
)


def run_generator(connector: str, statuses: str, out_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--connector",
            connector,
            "--statuses",
            statuses,
            "--out-dir",
            str(out_dir),
        ],
        check=False,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_success(result: subprocess.CompletedProcess[str]) -> None:
    require(result.returncode == 0, f"expected success, got {result.returncode}: {result.stderr}")


def require_failure(result: subprocess.CompletedProcess[str], expected: str) -> None:
    require(result.returncode != 0, "expected generator to fail")
    require(expected in result.stderr, f"expected {expected!r} in stderr: {result.stderr!r}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_successful_runs(tmp: Path) -> None:
    for connector, statuses in RUNS:
        out_dir = tmp / connector
        require_success(run_generator(connector, statuses, out_dir))
        header = out_dir / HEADER
        source = out_dir / SOURCE
        haproxy_cfg = out_dir / HAPROXY_CFG
        require(header.is_file(), f"missing header for {connector}")
        require(source.is_file(), f"missing source for {connector}")
        require(haproxy_cfg.is_file() == (connector == "haproxy"), f"unexpected HAProxy cfg state for {connector}")

        header_text = read(header)
        requested = {int(value) for value in statuses.split(",")}
        has_501 = "#define MSCONNECTOR_ENABLE_BLOCK_STATUS_501 1" in header_text
        require(has_501 == (501 in requested), f"501 enablement mismatch for {connector}")
        if 501 not in requested:
            require("#define MSCONNECTOR_ENABLE_BLOCK_STATUS_501 0" in header_text, f"501 disabled macro missing for {connector}")
        require("#define MSCONNECTOR_ENABLE_BLOCK_STATUS_400 0" in header_text, f"disabled 400 macro missing for {connector}")

        source_text = read(source)
        require("#include \"msconnector_block_statuses.generated.h\"" in source_text, f"missing generated include for {connector}")
        require("msconnector_generated_block_status_is_enabled" in source_text, f"missing accessor for {connector}")

    haproxy_text = read(tmp / "haproxy" / HAPROXY_CFG)
    require("http-request deny status 501 if { var(txn.modsec.status) -m int 501 }" in haproxy_text, "missing HAProxy request 501 mapping")
    require("http-response deny status 501 if { var(txn.modsec.status) -m int 501 }" in haproxy_text, "missing HAProxy response 501 mapping")


def check_full_status_list(tmp: Path) -> None:
    out_dir = tmp / "full-haproxy"
    require_success(run_generator("haproxy", FULL_STATUS_LIST, out_dir))
    header_text = read(out_dir / HEADER)
    source_text = read(out_dir / SOURCE)
    haproxy_text = read(out_dir / HAPROXY_CFG)

    for status in FULL_STATUSES:
        require(
            f"#define MSCONNECTOR_ENABLE_BLOCK_STATUS_{status} 1" in header_text,
            f"full list did not enable {status}",
        )
        require(
            f"http-request deny status {status} if {{ var(txn.modsec.status) -m int {status} }}" in haproxy_text,
            f"full HAProxy config missing request mapping for {status}",
        )
        require(
            f"http-response deny status {status} if {{ var(txn.modsec.status) -m int {status} }}" in haproxy_text,
            f"full HAProxy config missing response mapping for {status}",
        )

    require("#define MSCONNECTOR_ENABLE_BLOCK_STATUS_200" not in header_text, "unexpected 200 generated macro")
    require("deny status 200" not in haproxy_text, "disabled 200 appeared in HAProxy config")
    require("501" in source_text, "501 should appear in generated source only when explicitly requested")


def check_failures(tmp: Path) -> None:
    require_failure(run_generator("nginx", "403,403", tmp / "duplicate"), "duplicate status")
    require_failure(run_generator("nginx", "99", tmp / "invalid-low"), "outside the valid HTTP range")
    require_failure(run_generator("nginx", "200", tmp / "unsupported"), "global block-status contract")
    require_failure(run_generator("not-a-connector", "403", tmp / "unknown"), "unsupported connector")
    require_failure(run_generator("nginx", "", tmp / "empty"), "must not be empty")
    require_failure(run_generator("nginx", "abc", tmp / "non-integer"), "must be an integer")


def check_deterministic(tmp: Path) -> None:
    first = tmp / "deterministic-a"
    second = tmp / "deterministic-b"
    require_success(run_generator("nginx", "501,403", first))
    require_success(run_generator("nginx", DEFAULT_WEB_SERVER_STATUSES, second))
    for filename in (HEADER, SOURCE):
        require(filecmp.cmp(first / filename, second / filename, shallow=False), f"non-deterministic {filename}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="msconnector-block-status-generator-") as raw_tmp:
        tmp = Path(raw_tmp)
        check_successful_runs(tmp)
        check_full_status_list(tmp)
        check_failures(tmp)
        check_deterministic(tmp)
    print("block_status_generator: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
