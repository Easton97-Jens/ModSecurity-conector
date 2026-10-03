#!/usr/bin/env python3
"""Dispatch only explicitly selected, supported NGINX configuration contracts."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
DRIVER = Path(__file__).with_name("run-nginx-configtest.py")


def source_identity(root: Path, *arguments: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *arguments], check=True,
                            capture_output=True, text=True, timeout=10).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", result):
        raise ValueError("source identity must be an exact Git SHA")
    return result


def main() -> int:
    spec = importlib.util.spec_from_file_location("nginx_configtest_driver", DRIVER)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    try:
        framework = driver.absolute_path(os.environ["FRAMEWORK_ROOT"])
        selected = os.environ.get("NO_CRS_SELECTED_CASE_IDS", "").split()
        if len(selected) != len(set(selected)) or any(
                not re.fullmatch(r"[a-z][a-z0-9_]{0,127}", value) for value in selected):
            raise ValueError("selected case identities must be unique and path-safe")
        catalog_path = framework / "tests/cases/no-crs-baseline/catalog.json"
        driver.absolute_path(str(catalog_path))
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        records = catalog["cases"]
        invocations = []
        for case in records:
            if case["case_id"] not in selected:
                continue
            contract = case.get("config_invocations", {}).get("nginx")
            if contract is None:
                continue  # Never promote other selected cases or infer a runner.
            expected = driver.CONFIGTEST_CONTRACTS.get(case["case_id"])
            if (expected is None or contract != expected
                    or type(contract["expected_exit_code"]) is not int):
                raise ValueError("selected configuration invocation has no supported host driver")
            invocations.append(case["case_id"])
        if not invocations:
            return 0
        if len(invocations) != len(set(invocations)):
            raise ValueError("duplicate catalog configuration invocations")
        build = driver.absolute_path(os.environ["BUILD_ROOT"])
        results = driver.absolute_path(os.environ["RESULTS_DIR"])
        storage = driver.AUTHORIZED_STORAGE_ROOT
        if storage not in build.parents or any(driver.is_checkout(path) for path in (build, *build.parents)):
            raise ValueError("build output must be external authorized task storage")
        results.relative_to(build)
        if any(driver.is_checkout(path) for path in (results, *results.parents)):
            raise ValueError("results must be outside all source checkouts")
        if not build.is_dir():
            raise ValueError("build output root must already exist")
        driver.ensure_safe_runtime_directory(build)
        prefix = driver.absolute_path(os.environ["NGINX_PREFIX"])
        parent_sha = source_identity(ROOT, "rev-parse", "HEAD")
        framework_sha = source_identity(framework, "rev-parse", "HEAD")
        mrts_sha = source_identity(framework, "rev-parse", "HEAD:tools/MRTS")
        run_id = os.environ["NO_CRS_RUN_ID"]
        output_parent = driver.absolute_path(str(build / "configtests"))
        output_parent.mkdir(mode=0o700, exist_ok=True)
        driver.ensure_safe_runtime_directory(output_parent)
        driver.ensure_safe_runtime_directory(results.parent)
        results.mkdir(mode=0o700, exist_ok=True)
        driver.ensure_safe_runtime_directory(results)
        if any((output_parent / case_id).exists() or (output_parent / case_id).is_symlink()
               for case_id in invocations):
            raise ValueError("configuration output must be a fresh child")
        result_path = driver.absolute_path(str(results / "nginx-results.jsonl"))
        flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW
        with os.fdopen(os.open(result_path, flags, 0o600), "a+", encoding="utf-8") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 4 * 1024 * 1024:
                raise ValueError("existing result input must be a bounded regular file")
            if (metadata.st_uid != os.geteuid() or metadata.st_nlink != 1
                    or stat.S_IMODE(metadata.st_mode) & 0o022):
                raise ValueError("result input must be owned, single-link, and nonwritable by other users")
            stream.seek(0)
            previous = [json.loads(line) for line in stream if line.strip()]
            if any(row.get("case_id") in invocations for row in previous):
                raise ValueError("configuration invocation result already exists")
            failed = False
            for case_id in invocations:
                output = output_parent / case_id
                arguments = [sys.executable, str(DRIVER), "--case-id", case_id,
                             "--nginx-binary", str(prefix / "sbin/nginx"),
                             "--module", str(prefix / "modules/ngx_http_modsecurity_module.so"),
                             "--output-root", str(output), "--run-id", run_id,
                             "--parent-sha", parent_sha, "--framework-sha", framework_sha,
                             "--mrts-sha", mrts_sha]
                if os.environ.get("MODSECURITY_LIB_DIR"):
                    arguments += ["--library-dir", os.environ["MODSECURITY_LIB_DIR"]]
                completed = subprocess.run(arguments, check=False, timeout=30)
                source = driver.absolute_path(str(output / "source-result.jsonl"))
                if not source.is_file():
                    raise ValueError("configuration invocation produced no source result")
                if source.stat().st_size > 65536:
                    raise ValueError("configuration source result exceeds the receipt limit")
                rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
                if len(rows) != 1 or rows[0].get("case_id") != case_id:
                    raise ValueError("configuration invocation result identity mismatch")
                stream.write(json.dumps(rows[0], sort_keys=True) + "\n")
                stream.flush()
                failed = failed or completed.returncode != 0
            return 1 if failed else 0
    except (KeyError, ValueError, OSError, subprocess.SubprocessError) as error:
        print("selected NGINX configtests rejected: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
