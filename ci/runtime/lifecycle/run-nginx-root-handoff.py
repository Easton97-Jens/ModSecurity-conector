#!/usr/bin/env python3
"""Run only a prepared NGINX host stage through a narrow root handoff.

The normal connector lifecycle prepares and verifies NGINX artifacts as the
unprivileged runner.  This helper then elevates only the configuration/start/
No-CRS host phases that need a root-owned harness and a distinct non-root
worker.  It never sources the runner-produced runtime snapshot: the snapshot
is parsed as data, reduced to a small allowlist, and the elevated Framework
runner receives a newly constructed environment.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import grp
import os
from pathlib import Path
import pwd
import re
import secrets
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Mapping


ALLOWED_STAGES = frozenset({"config_load", "start_smoke", "minimal_runtime_smoke"})
ALLOWED_NGINX_ENV = frozenset(
    {
        "NGINX_ROOT_HANDOFF",
        "NGINX_PHASE4_MODE",
        "NGINX_DOCROOT_PROJECTION",
        "NGINX_DOCROOT_PROJECTION_PARENT",
        "NGINX_DOCROOT_PROJECTION_ROOT",
        "NGINX_HARNESS_PARENT",
        "NGINX_HARNESS_WORK_ROOT",
    }
)
SNAPSHOT_KEY = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
SAFE_CASE_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")
SAFE_CASE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SNAPSHOT_ALLOWED_KEYS = frozenset(
    {
        "CONNECTOR_COMPONENT_CACHE",
        "SOURCE_ROOT",
        "MODSECURITY_SOURCE_URL",
        "MODSECURITY_SOURCE_REF",
        "MODSECURITY_SOURCE_SHA",
        "MODSECURITY_BUILD_FLAGS",
        "MODSECURITY_DEPENDENCY_HASH",
        "MODSECURITY_BUILD_ID",
        "MODSECURITY_SOURCE_DIR",
        "MODSECURITY_V3_SOURCE_DIR",
        "MODSECURITY_V3_ROOT",
        "CRS_SOURCE_DIR",
        "APACHE_DOWNLOAD_DIR",
        "NGINX_DOWNLOAD_DIR",
        "HAPROXY_SOURCE_ROOT",
        "HAPROXY_DOWNLOAD_DIR",
        "HAPROXY_SOURCE_DIR",
        "NGINX_BUILD_DIR",
        "NGINX_BUILD_OWNER_ROOT",
        "NGINX_CONNECTOR_BUILD_ID",
        "NGINX_PREFIX",
        "NGINX_PROTOCOL_PROFILE",
        "MODSECURITY_PREFIX",
        "MODSECURITY_SHARED_PREFIX",
        "MODSECURITY_INCLUDE_DIR",
        "MODSECURITY_LIB_DIR",
        "MODSECURITY_PKG_CONFIG_PATH",
        "EXPAT_PREFIX",
        "CPPFLAGS",
        "LDFLAGS",
        "LIBS",
        "PKG_CONFIG_PATH",
        "LD_LIBRARY_PATH",
        "MRTS_NATIVE_NGINX_BIN",
        "MRTS_NATIVE_NGINX_MODULE_DIR",
        "MRTS_NATIVE_NGINX_MODULE_FILE",
        "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR",
        "MSCONNECTOR_COMMON_SRC",
        "RUNTIME_BUILD_CACHE_MANIFEST",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET",
    }
)
SNAPSHOT_REQUIRED_KEYS = frozenset(
    {
        "CONNECTOR_COMPONENT_CACHE",
        "MODSECURITY_SOURCE_DIR",
        "MODSECURITY_V3_SOURCE_DIR",
        "NGINX_BUILD_DIR",
        "NGINX_PREFIX",
        "NGINX_PROTOCOL_PROFILE",
        "MODSECURITY_LIB_DIR",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET",
    }
)
SNAPSHOT_FORWARD_KEYS = (
    "MODSECURITY_SOURCE_DIR",
    "MODSECURITY_V3_SOURCE_DIR",
    "MODSECURITY_V3_ROOT",
    "NGINX_BUILD_DIR",
    "NGINX_BUILD_OWNER_ROOT",
    "NGINX_CONNECTOR_BUILD_ID",
    "NGINX_PREFIX",
    "NGINX_PROTOCOL_PROFILE",
    "MODSECURITY_PREFIX",
    "MODSECURITY_SHARED_PREFIX",
    "MODSECURITY_INCLUDE_DIR",
    "MODSECURITY_LIB_DIR",
)
SYSTEM_WRITE_PREFIXES = (Path("/etc"), Path("/usr"), Path("/bin"), Path("/sbin"), Path("/lib"), Path("/lib64"), Path("/opt"), Path("/root"))
PROJECTION_FILENAMES = frozenset({"index.html", "__modsec_smoke_ready"})
FIXED_WORKER_USER = "nobody"


class HandoffError(ValueError):
    """The root handoff contract was not met."""


@dataclass(frozen=True)
class HandoffRequest:
    connector_root: Path
    framework_root: Path
    verified_run_root: Path
    build_root: Path
    cache_root: Path
    component_cache: Path
    tmp_root: Path
    log_root: Path
    results_dir: Path
    report_output_root: Path
    snapshot: Path
    python: Path
    stage: str
    run_one_case: str
    test_case: str
    smoke_cases: str
    selected_case_ids: str
    rule_preamble: Path | None
    phase4_mode: str
    docroot_projection: bool
    nginx_harness_parent: Path
    nginx_harness_work_root: Path | None
    runtime_root: Path | None
    runtime_base: Path | None
    evidence_root: Path | None
    connector_run_root: Path | None
    connector_log_root: Path | None


def fail(message: str) -> None:
    raise HandoffError(message)


def clean_absolute(raw: str | Path, label: str, *, required: bool = True) -> Path | None:
    text = str(raw)
    if not text:
        if required:
            fail(f"{label} is required")
        return None
    if text != text.strip() or "\x00" in text:
        fail(f"{label} is malformed")
    path = Path(text)
    if not path.is_absolute() or ".." in path.parts:
        fail(f"{label} must be an absolute path without traversal: {path}")
    return Path(os.path.abspath(os.path.normpath(os.fspath(path))))


def ensure_no_symlink_prefix(path: Path, label: str, *, require_leaf: bool) -> None:
    current = Path("/")
    for component in path.parts[1:]:
        current /= component
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            if require_leaf:
                fail(f"{label} is missing: {path}")
            return
        if stat.S_ISLNK(metadata.st_mode):
            fail(f"{label} contains a symbolic link: {current}")
        if current != path and not stat.S_ISDIR(metadata.st_mode):
            fail(f"{label} has a non-directory ancestor: {current}")
    if require_leaf and not path.exists():
        fail(f"{label} is missing: {path}")


def resolved(path: Path, label: str, *, require_leaf: bool = True) -> Path:
    ensure_no_symlink_prefix(path, label, require_leaf=require_leaf)
    return path.resolve(strict=require_leaf)


def strict_descendant(path: Path, root: Path, label: str) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise HandoffError(f"{label} must be inside its authorized root: {path}") from exc
    if relative == Path("."):
        fail(f"{label} must be a strict descendant of its authorized root: {path}")


def overlaps(left: Path, right: Path) -> bool:
    try:
        left.relative_to(right)
        return True
    except ValueError:
        pass
    try:
        right.relative_to(left)
        return True
    except ValueError:
        return False


def reject_system_write_path(path: Path, label: str) -> None:
    for prefix in SYSTEM_WRITE_PREFIXES:
        if path == prefix or prefix in path.parents:
            fail(f"{label} must not be under a system root: {path}")


def validate_mutable_path(path: Path, verified_root: Path, label: str) -> Path:
    candidate = resolved(path, label, require_leaf=False)
    reject_system_write_path(candidate, label)
    strict_descendant(candidate, verified_root, label)
    return candidate


def validate_fixed_file(path: Path, label: str) -> Path:
    candidate = resolved(path, label)
    metadata = candidate.lstat()
    if not stat.S_ISREG(metadata.st_mode):
        fail(f"{label} must be a regular file: {candidate}")
    return candidate


def split_safe_tokens(value: str, label: str, pattern: re.Pattern[str]) -> list[str]:
    tokens = value.split()
    if not tokens:
        return []
    for token in tokens:
        if not pattern.fullmatch(token) or token.startswith("/") or ".." in token.split("/"):
            fail(f"{label} contains an unsafe token: {token!r}")
    return tokens


def validate_stage_arguments(request: HandoffRequest) -> None:
    if request.stage not in ALLOWED_STAGES:
        fail(f"root handoff refuses unsupported stage: {request.stage}")
    if request.phase4_mode != "safe":
        fail(f"root handoff permits only NGINX_PHASE4_MODE=safe, got {request.phase4_mode!r}")
    if request.stage in {"config_load", "start_smoke"}:
        if request.run_one_case != "1" or request.test_case != "allow_without_marker":
            fail("config/start root handoff requires the fixed allow_without_marker case")
        if request.smoke_cases or request.selected_case_ids:
            fail("config/start root handoff does not accept selected case lists")
    else:
        if request.run_one_case != "0" or request.test_case:
            fail("minimal-runtime root handoff requires RUN_ONE_CASE=0 and no TEST_CASE")
        smoke_cases = split_safe_tokens(request.smoke_cases, "SMOKE_CASES", SAFE_CASE_TOKEN)
        if not {"allow_without_marker.yaml", "deny_header_marker_403.yaml"}.issubset(smoke_cases):
            fail("minimal-runtime root handoff requires the selected allow and deny No-CRS cases")
        split_safe_tokens(request.selected_case_ids, "NO_CRS_SELECTED_CASE_IDS", SAFE_CASE_ID)


def validate_nginx_environment(environment: Mapping[str, str]) -> None:
    unknown = sorted(key for key in environment if key.startswith("NGINX_") and key not in ALLOWED_NGINX_ENV)
    if unknown:
        fail(f"root handoff rejects unapproved NGINX environment keys: {', '.join(unknown)}")
    if environment.get("NGINX_ROOT_HANDOFF") != "1":
        fail("NGINX_ROOT_HANDOFF=1 is required")
    for key in ("NGINX_DOCROOT_PROJECTION_PARENT", "NGINX_DOCROOT_PROJECTION_ROOT"):
        if environment.get(key, ""):
            fail(f"caller-supplied {key} is not accepted by the root handoff")


def parse_runtime_snapshot(path: Path) -> dict[str, str]:
    snapshot = validate_fixed_file(path, "runtime environment snapshot")
    metadata = snapshot.lstat()
    if metadata.st_nlink != 1:
        fail(f"runtime environment snapshot must have one link: {snapshot}")
    values: dict[str, str] = {}
    for line_number, line in enumerate(snapshot.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.startswith("export "):
            fail(f"runtime environment snapshot line {line_number} is not an export assignment")
        try:
            tokens = shlex.split(line[len("export ") :], posix=True, comments=False)
        except ValueError as exc:
            raise HandoffError(f"runtime environment snapshot line {line_number} is malformed") from exc
        if len(tokens) != 1 or "=" not in tokens[0]:
            fail(f"runtime environment snapshot line {line_number} is not one assignment")
        key, value = tokens[0].split("=", 1)
        if not SNAPSHOT_KEY.fullmatch(key) or key not in SNAPSHOT_ALLOWED_KEYS:
            fail(f"runtime environment snapshot exports an unapproved key: {key!r}")
        if key in values:
            fail(f"runtime environment snapshot exports duplicate key: {key}")
        if any(character in value for character in ("\x00", "\r", "\n", "`", "$")):
            fail(f"runtime environment snapshot contains unsafe value characters for {key}")
        values[key] = value
    missing = sorted(SNAPSHOT_REQUIRED_KEYS - values.keys())
    if missing:
        fail(f"runtime environment snapshot omits required keys: {', '.join(missing)}")
    return values


def validate_snapshot(request: HandoffRequest, values: Mapping[str, str]) -> dict[str, str]:
    snapshot = resolved(request.snapshot, "runtime environment snapshot")
    report_root = validate_mutable_path(request.report_output_root, request.verified_run_root, "RUNTIME_REPORT_OUTPUT_ROOT")
    strict_descendant(snapshot, report_root, "runtime environment snapshot")
    component_cache = resolved(request.component_cache, "CONNECTOR_COMPONENT_CACHE")
    if values["CONNECTOR_COMPONENT_CACHE"] != str(component_cache):
        fail("runtime environment snapshot cache does not match CONNECTOR_COMPONENT_CACHE")
    if values["RUNTIME_COMPONENT_ENV_SNAPSHOT"] != str(snapshot):
        fail("runtime environment snapshot does not bind itself")
    if values["RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE"] != str(component_cache):
        fail("runtime environment snapshot metadata cache mismatch")
    if values["RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET"] != "nginx":
        fail("runtime environment snapshot target must be nginx")
    if values["RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA"] != "1":
        fail("runtime environment snapshot schema is unsupported")
    if values["NGINX_PROTOCOL_PROFILE"] != "h1":
        fail("root handoff permits only the reviewed h1 NGINX profile")

    cache_path_keys = (
        "MODSECURITY_SOURCE_DIR",
        "MODSECURITY_V3_SOURCE_DIR",
        "MODSECURITY_V3_ROOT",
        "NGINX_BUILD_DIR",
        "NGINX_BUILD_OWNER_ROOT",
        "NGINX_PREFIX",
        "MODSECURITY_PREFIX",
        "MODSECURITY_SHARED_PREFIX",
        "MODSECURITY_INCLUDE_DIR",
        "MODSECURITY_LIB_DIR",
        "MRTS_NATIVE_NGINX_BIN",
        "MRTS_NATIVE_NGINX_MODULE_DIR",
        "MRTS_NATIVE_NGINX_MODULE_FILE",
        "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR",
    )
    for key in cache_path_keys:
        value = values.get(key, "")
        if not value:
            continue
        candidate = resolved(clean_absolute(value, f"snapshot {key}"), f"snapshot {key}")
        strict_descendant(candidate, component_cache, f"snapshot {key}")

    nginx_prefix = resolved(clean_absolute(values["NGINX_PREFIX"], "snapshot NGINX_PREFIX"), "snapshot NGINX_PREFIX")
    nginx_build = resolved(clean_absolute(values["NGINX_BUILD_DIR"], "snapshot NGINX_BUILD_DIR"), "snapshot NGINX_BUILD_DIR")
    lib_dir = resolved(clean_absolute(values["MODSECURITY_LIB_DIR"], "snapshot MODSECURITY_LIB_DIR"), "snapshot MODSECURITY_LIB_DIR")
    for path, label in (
        (nginx_prefix / "sbin/nginx", "prepared NGINX binary"),
        (nginx_prefix / "modules/ngx_http_modsecurity_module.so", "prepared NGINX module"),
        (nginx_build / "connector-src/materialized-source.json", "prepared NGINX source manifest"),
        (nginx_build / "nginx-protocol-build-provenance.txt", "prepared NGINX protocol provenance"),
        (lib_dir / "libmodsecurity.so", "prepared libmodsecurity"),
    ):
        validate_fixed_file(path, label)
    if not os.access(nginx_prefix / "sbin/nginx", os.X_OK):
        fail("prepared NGINX binary is not executable")
    return {key: values[key] for key in SNAPSHOT_FORWARD_KEYS if values.get(key, "")}


def validate_python_tool(python: Path) -> Path:
    candidate = clean_absolute(python, "selected Python interpreter").resolve(strict=True)
    metadata = candidate.stat()
    if not stat.S_ISREG(metadata.st_mode):
        fail(f"selected Python interpreter must be a regular file: {candidate}")
    if metadata.st_uid != 0 or metadata.st_mode & 0o022:
        fail("selected Python interpreter must be root-owned and not group/other writable")
    return candidate


def validate_worker() -> tuple[str, str]:
    if os.geteuid() != 0:
        fail("elevated root handoff requires effective uid 0")
    try:
        account = pwd.getpwnam(FIXED_WORKER_USER)
        group = grp.getgrgid(account.pw_gid)
    except KeyError as exc:
        raise HandoffError(f"required NGINX worker account is unavailable: {FIXED_WORKER_USER}") from exc
    if account.pw_uid == 0:
        fail("NGINX worker account must not be root")
    runuser = shutil.which("runuser")
    if not runuser or not Path(runuser).is_file() or not os.access(runuser, os.X_OK):
        fail("root handoff requires the local runuser verifier")
    return account.pw_name, group.gr_name


def validate_request(request: HandoffRequest) -> tuple[HandoffRequest, dict[str, str]]:
    validate_stage_arguments(request)
    verified_root = resolved(request.verified_run_root, "VERIFIED_RUN_ROOT")
    reject_system_write_path(verified_root, "VERIFIED_RUN_ROOT")
    connector_root = resolved(request.connector_root, "CONNECTOR_ROOT")
    framework_root = resolved(request.framework_root, "FRAMEWORK_ROOT")
    if framework_root != connector_root / "modules" / "ModSecurity-test-Framework":
        fail("FRAMEWORK_ROOT must be the fixed direct Parent submodule path")
    runner = validate_fixed_file(framework_root / "ci/runtime/run-nginx-smoke.sh", "fixed Framework NGINX runner")
    if runner.parent.parent != framework_root / "ci":
        fail("fixed Framework NGINX runner path is invalid")

    build_root = validate_mutable_path(request.build_root, verified_root, "BUILD_ROOT")
    cache_root = validate_mutable_path(request.cache_root, verified_root, "CACHE_ROOT")
    component_cache = validate_mutable_path(request.component_cache, verified_root, "CONNECTOR_COMPONENT_CACHE")
    strict_descendant(component_cache, cache_root, "CONNECTOR_COMPONENT_CACHE")
    if overlaps(build_root, component_cache):
        fail("BUILD_ROOT and CONNECTOR_COMPONENT_CACHE must not overlap")
    for path, label in (
        (request.tmp_root, "TMP_ROOT"),
        (request.log_root, "LOG_ROOT"),
        (request.results_dir, "RESULTS_DIR"),
        (request.report_output_root, "RUNTIME_REPORT_OUTPUT_ROOT"),
        (request.nginx_harness_parent, "NGINX_HARNESS_PARENT"),
    ):
        validate_mutable_path(path, verified_root, label)
    for path, label in (
        (request.nginx_harness_work_root, "NGINX_HARNESS_WORK_ROOT"),
        (request.runtime_root, "RUNTIME_ROOT"),
        (request.runtime_base, "RUNTIME_BASE"),
        (request.evidence_root, "EVIDENCE_ROOT"),
        (request.connector_run_root, "CONNECTOR_RUN_ROOT"),
        (request.connector_log_root, "CONNECTOR_LOG_ROOT"),
    ):
        if path is not None:
            validate_mutable_path(path, verified_root, label)
    if request.rule_preamble is not None:
        rule_preamble = validate_fixed_file(request.rule_preamble, "MODSECURITY_RULE_PREAMBLE_FILE")
        strict_descendant(rule_preamble, framework_root, "MODSECURITY_RULE_PREAMBLE_FILE")
    else:
        rule_preamble = None
    validate_python_tool(request.python)
    snapshot_values = parse_runtime_snapshot(request.snapshot)
    forwarded = validate_snapshot(request, snapshot_values)
    normalized = HandoffRequest(
        connector_root=connector_root,
        framework_root=framework_root,
        verified_run_root=verified_root,
        build_root=build_root,
        cache_root=cache_root,
        component_cache=component_cache,
        tmp_root=resolved(request.tmp_root, "TMP_ROOT", require_leaf=False),
        log_root=resolved(request.log_root, "LOG_ROOT", require_leaf=False),
        results_dir=resolved(request.results_dir, "RESULTS_DIR", require_leaf=False),
        report_output_root=resolved(request.report_output_root, "RUNTIME_REPORT_OUTPUT_ROOT", require_leaf=False),
        snapshot=resolved(request.snapshot, "runtime environment snapshot"),
        python=validate_python_tool(request.python),
        stage=request.stage,
        run_one_case=request.run_one_case,
        test_case=request.test_case,
        smoke_cases=request.smoke_cases,
        selected_case_ids=request.selected_case_ids,
        rule_preamble=rule_preamble,
        phase4_mode=request.phase4_mode,
        docroot_projection=request.docroot_projection,
        nginx_harness_parent=resolved(request.nginx_harness_parent, "NGINX_HARNESS_PARENT", require_leaf=False),
        nginx_harness_work_root=(resolved(request.nginx_harness_work_root, "NGINX_HARNESS_WORK_ROOT", require_leaf=False) if request.nginx_harness_work_root else None),
        runtime_root=(resolved(request.runtime_root, "RUNTIME_ROOT", require_leaf=False) if request.runtime_root else None),
        runtime_base=(resolved(request.runtime_base, "RUNTIME_BASE", require_leaf=False) if request.runtime_base else None),
        evidence_root=(resolved(request.evidence_root, "EVIDENCE_ROOT", require_leaf=False) if request.evidence_root else None),
        connector_run_root=(resolved(request.connector_run_root, "CONNECTOR_RUN_ROOT", require_leaf=False) if request.connector_run_root else None),
        connector_log_root=(resolved(request.connector_log_root, "CONNECTOR_LOG_ROOT", require_leaf=False) if request.connector_log_root else None),
    )
    return normalized, forwarded


def create_projection_parent(verified_root: Path) -> tuple[Path, os.stat_result]:
    base = verified_root.parent
    ensure_no_symlink_prefix(base, "NGINX projection base", require_leaf=True)
    reject_system_write_path(base, "NGINX projection base")
    parent = Path(tempfile.mkdtemp(prefix="msconnector-nginx-projection-", dir=str(base)))
    created_metadata = parent.lstat()
    try:
        descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            opened_metadata = os.fstat(descriptor)
            if (
                opened_metadata.st_dev != created_metadata.st_dev
                or opened_metadata.st_ino != created_metadata.st_ino
                or not stat.S_ISDIR(opened_metadata.st_mode)
                or opened_metadata.st_uid != 0
            ):
                fail("created NGINX projection parent changed before permission setup")
            os.fchmod(descriptor, 0o711)
            metadata = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            fail("created NGINX projection parent is not a directory")
        if metadata.st_uid != 0 or metadata.st_mode & 0o066:
            fail("created NGINX projection parent has unsafe ownership or permissions")
        return parent, metadata
    except Exception:
        try:
            current = parent.lstat()
            if current.st_dev == created_metadata.st_dev and current.st_ino == created_metadata.st_ino:
                parent.rmdir()
        except OSError:
            pass
        raise


def remove_projection_parent(parent: Path, expected: os.stat_result) -> None:
    """Remove only the exact root-owned projection tree created by this helper."""

    current = parent.lstat()
    if current.st_dev != expected.st_dev or current.st_ino != expected.st_ino:
        fail("NGINX projection parent changed before cleanup")
    if not stat.S_ISDIR(current.st_mode) or stat.S_ISLNK(current.st_mode) or current.st_uid != 0:
        fail("NGINX projection parent is unsafe at cleanup")
    descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        names = set(os.listdir(descriptor))
        if names - {"docroot"}:
            fail("NGINX projection parent has unexpected entries; refusing cleanup")
        if "docroot" in names:
            child_metadata = os.stat("docroot", dir_fd=descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(child_metadata.st_mode) or stat.S_ISLNK(child_metadata.st_mode):
                fail("NGINX projection child is unsafe at cleanup")
            child_fd = os.open("docroot", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            try:
                child_names = set(os.listdir(child_fd))
                if child_names - PROJECTION_FILENAMES:
                    fail("NGINX projection child has unexpected entries; refusing cleanup")
                for name in child_names:
                    file_metadata = os.stat(name, dir_fd=child_fd, follow_symlinks=False)
                    if not stat.S_ISREG(file_metadata.st_mode) or stat.S_ISLNK(file_metadata.st_mode):
                        fail("NGINX projection child has unsafe file at cleanup")
                    os.unlink(name, dir_fd=child_fd)
            finally:
                os.close(child_fd)
            os.rmdir("docroot", dir_fd=descriptor)
    finally:
        os.close(descriptor)
    parent.rmdir()


def build_environment(
    request: HandoffRequest,
    snapshot: Mapping[str, str],
    *,
    worker_user: str,
    worker_group: str,
    projection_parent: Path | None,
) -> dict[str, str]:
    environment = {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "CONNECTOR_ROOT": str(request.connector_root),
        "FRAMEWORK_ROOT": str(request.framework_root),
        "VERIFIED_RUN_ROOT": str(request.verified_run_root),
        "VERIFIED_BUILD_ROOT": str(request.build_root),
        "BUILD_ROOT": str(request.build_root),
        "CACHE_ROOT": str(request.cache_root),
        "VERIFIED_COMPONENT_CACHE": str(request.component_cache),
        "CONNECTOR_COMPONENT_CACHE": str(request.component_cache),
        "TMP_ROOT": str(request.tmp_root),
        "LOG_ROOT": str(request.log_root),
        "RESULTS_DIR": str(request.results_dir),
        "RUNTIME_REPORT_OUTPUT_ROOT": str(request.report_output_root),
        "RUNTIME_COMPONENT_TARGET": "nginx",
        "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(request.snapshot),
        "PYTHON": str(request.python),
        "PYTHON_BIN": str(request.python),
        "NO_CRS_BASELINE": "1",
        "MODSECURITY_TEST_VARIANT": "no-crs",
        "MODSECURITY_MRTS_VARIANT": "no-mrts",
        "MSCONNECTOR_SMOKE_STAGE": request.stage,
        "RUN_ONE_CASE": request.run_one_case,
        "TEST_CASE": request.test_case,
        "SMOKE_CASES": request.smoke_cases,
        "NO_CRS_SELECTED_CASE_IDS": request.selected_case_ids,
        "NGINX_PHASE4_MODE": request.phase4_mode,
        "NGINX_HARNESS_PARENT": str(request.nginx_harness_parent),
        "NGINX_WORKER_USER": worker_user,
        "NGINX_WORKER_GROUP": worker_group,
        "BUILD_NGINX_FROM_SOURCE": "0",
        "AUTO_FETCH_SMOKE_SOURCES": "0",
        "AUTO_REFRESH_STALE_BUILD": "0",
        "REFRESH": "0",
        **snapshot,
    }
    if request.rule_preamble is not None:
        environment["MODSECURITY_RULE_PREAMBLE_FILE"] = str(request.rule_preamble)
    if request.nginx_harness_work_root is not None:
        environment["NGINX_HARNESS_WORK_ROOT"] = str(request.nginx_harness_work_root)
    if request.runtime_root is not None:
        environment["RUNTIME_ROOT"] = str(request.runtime_root)
    if request.runtime_base is not None:
        environment["RUNTIME_BASE"] = str(request.runtime_base)
    if request.evidence_root is not None:
        environment["EVIDENCE_ROOT"] = str(request.evidence_root)
        environment["VERIFIED_EVIDENCE_ROOT"] = str(request.evidence_root.parent)
    if request.connector_run_root is not None:
        environment["CONNECTOR_RUN_ROOT"] = str(request.connector_run_root)
    if request.connector_log_root is not None:
        environment["CONNECTOR_LOG_ROOT"] = str(request.connector_log_root)
    if projection_parent is not None:
        environment["NGINX_DOCROOT_PROJECTION"] = "1"
        environment["NGINX_DOCROOT_PROJECTION_PARENT"] = str(projection_parent)
        environment["NGINX_DOCROOT_PROJECTION_ROOT"] = str(projection_parent / "docroot")
    else:
        environment["NGINX_DOCROOT_PROJECTION"] = "0"
    return environment


def execute_elevated(request: HandoffRequest, snapshot: Mapping[str, str]) -> int:
    worker_user, worker_group = validate_worker()
    projection_parent: Path | None = None
    projection_metadata: os.stat_result | None = None
    if request.docroot_projection:
        projection_parent, projection_metadata = create_projection_parent(request.verified_run_root)
    try:
        environment = build_environment(
            request,
            snapshot,
            worker_user=worker_user,
            worker_group=worker_group,
            projection_parent=projection_parent,
        )
        runner = request.framework_root / "ci/runtime/run-nginx-smoke.sh"
        completed = subprocess.run(["/bin/sh", str(runner)], cwd=request.connector_root, env=environment, check=False)
        result = completed.returncode
    finally:
        if projection_parent is not None and projection_metadata is not None:
            remove_projection_parent(projection_parent, projection_metadata)
    return result


def make_request(args: argparse.Namespace) -> HandoffRequest:
    return HandoffRequest(
        connector_root=clean_absolute(args.connector_root, "CONNECTOR_ROOT"),
        framework_root=clean_absolute(args.framework_root, "FRAMEWORK_ROOT"),
        verified_run_root=clean_absolute(args.verified_run_root, "VERIFIED_RUN_ROOT"),
        build_root=clean_absolute(args.build_root, "BUILD_ROOT"),
        cache_root=clean_absolute(args.cache_root, "CACHE_ROOT"),
        component_cache=clean_absolute(args.component_cache, "CONNECTOR_COMPONENT_CACHE"),
        tmp_root=clean_absolute(args.tmp_root, "TMP_ROOT"),
        log_root=clean_absolute(args.log_root, "LOG_ROOT"),
        results_dir=clean_absolute(args.results_dir, "RESULTS_DIR"),
        report_output_root=clean_absolute(args.report_output_root, "RUNTIME_REPORT_OUTPUT_ROOT"),
        snapshot=clean_absolute(args.snapshot, "RUNTIME_COMPONENT_ENV_SNAPSHOT"),
        python=clean_absolute(args.python, "PYTHON"),
        stage=args.stage,
        run_one_case=args.run_one_case,
        test_case=args.test_case,
        smoke_cases=args.smoke_cases,
        selected_case_ids=args.selected_case_ids,
        rule_preamble=clean_absolute(args.rule_preamble, "MODSECURITY_RULE_PREAMBLE_FILE", required=False),
        phase4_mode=args.phase4_mode,
        docroot_projection=args.docroot_projection == "1",
        nginx_harness_parent=clean_absolute(args.nginx_harness_parent, "NGINX_HARNESS_PARENT"),
        nginx_harness_work_root=clean_absolute(args.nginx_harness_work_root, "NGINX_HARNESS_WORK_ROOT", required=False),
        runtime_root=clean_absolute(args.runtime_root, "RUNTIME_ROOT", required=False),
        runtime_base=clean_absolute(args.runtime_base, "RUNTIME_BASE", required=False),
        evidence_root=clean_absolute(args.evidence_root, "EVIDENCE_ROOT", required=False),
        connector_run_root=clean_absolute(args.connector_run_root, "CONNECTOR_RUN_ROOT", required=False),
        connector_log_root=clean_absolute(args.connector_log_root, "CONNECTOR_LOG_ROOT", required=False),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--elevated", action="store_true")
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--verified-run-root", required=True)
    parser.add_argument("--build-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--component-cache", required=True)
    parser.add_argument("--tmp-root", required=True)
    parser.add_argument("--log-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--report-output-root", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--run-one-case", required=True)
    parser.add_argument("--test-case", default="")
    parser.add_argument("--smoke-cases", default="")
    parser.add_argument("--selected-case-ids", default="")
    parser.add_argument("--rule-preamble", default="")
    parser.add_argument("--phase4-mode", required=True)
    parser.add_argument("--docroot-projection", choices=("0", "1"), required=True)
    parser.add_argument("--nginx-harness-parent", required=True)
    parser.add_argument("--nginx-harness-work-root", default="")
    parser.add_argument("--runtime-root", default="")
    parser.add_argument("--runtime-base", default="")
    parser.add_argument("--evidence-root", default="")
    parser.add_argument("--connector-run-root", default="")
    parser.add_argument("--connector-log-root", default="")
    return parser.parse_args(argv)


def elevate(argv: list[str]) -> int:
    command = ["/usr/bin/sudo", "-n", "--", *argv]
    return subprocess.run(command, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    original_argv = list(sys.argv[1:] if argv is None else argv)
    args = parse_args(original_argv)
    try:
        if not args.elevated:
            validate_nginx_environment(os.environ)
        request = make_request(args)
        request, snapshot = validate_request(request)
        if not args.elevated:
            elevated_argv = [
                str(request.python),
                str(Path(__file__).resolve()),
                "--elevated",
                *[argument for argument in original_argv if argument != "--elevated"],
            ]
            return elevate(elevated_argv)
        return execute_elevated(request, snapshot)
    except (HandoffError, OSError) as exc:
        print(f"FAIL: NGINX root handoff: {exc}", file=sys.stderr)
        return 77


if __name__ == "__main__":
    raise SystemExit(main())
