#!/usr/bin/env python3
"""Fixed-schema trusted NGINX root broker.

This program has two intentionally separate phases.  ``prepare-candidate``
runs without privilege in the immutable broker workflow and turns a narrow
caller manifest plus trusted build outputs into declarative data.  Every
privileged action reads that data as data only, copies verified artifacts into
a root-owned per-run root, and then accepts only a closed action allowlist.

It never sources shell, evaluates a command string, or accepts a program path
from the caller.  The root process can execute only the NGINX binary copied
from the broker workflow's verified protected build output.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import grp
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import signal
import socket
import stat
import subprocess
import sys
import time
from typing import Any, Iterable


SCHEMA_VERSION = 1
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
WORKER_NAME_RE = re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")
LOOPBACKS = {"127.0.0.1", "::1"}
ALLOWED_VARIANTS = {"no-crs", "with-crs"}
ALLOWED_ACTIONS = {
    "validate-manifest",
    "config-test",
    "start",
    "verify-master-worker-identity",
    "project-evidence",
    "stop",
    "cleanup-status",
}
IDENTITY_EVIDENCE_FILENAME = "identity.json"
RUNTIME_EVIDENCE_FILENAME = "runtime.json"
ACCESS_LOG_FILENAME = "nginx-access.log"
ERROR_LOG_FILENAME = "nginx-error.log"
EXPECTED_EVIDENCE = (
    IDENTITY_EVIDENCE_FILENAME,
    RUNTIME_EVIDENCE_FILENAME,
    ACCESS_LOG_FILENAME,
    ERROR_LOG_FILENAME,
)
ROOT_PARENT_NAME = "msconnector-nginx-root-broker"
ROOT_STATE_BASE = Path("/var/lib")
ROOT_PARENT = ROOT_STATE_BASE / ROOT_PARENT_NAME
ROOT_PARENT_MODE = 0o710
CALLER_MANIFEST_LABEL = "caller manifest"
CANDIDATE_LABEL = "broker candidate"
CANDIDATE_STAGING_LABEL = "candidate staging root"
TRUSTED_BUILD_ROOT_LABEL = "trusted build root"
RUNTIME_SNAPSHOT_LABEL = "runtime environment snapshot"
TRUSTED_MODSECURITY_LIBRARY_LABEL = "trusted ModSecurity shared library"
BROKER_ROOT_PARENT_LABEL = "broker root parent"
CANDIDATE_DIRECTORY_NAME = "broker-candidate"
RUNTIME_REPORTS_RELATIVE = Path("build") / "runtime-component-reports"
ARTIFACT_BINARY_NAME = "nginx"
ARTIFACT_MODULE_NAME = "ngx_http_modsecurity_module.so"
ARTIFACT_LIBRARY_NAME = "libmodsecurity.so"
BROKER_RULES_FILENAME = "broker-rules.conf"
BROKER_CONFIG_FILENAME = "nginx.conf"
BROKER_ROOT_LABEL = "broker root"
PID_FILENAME = "nginx.pid"
STATE_FILENAME = "state.json"
ARTIFACT_DESTINATION_NAMES = {
    "binary": ARTIFACT_BINARY_NAME,
    "module": ARTIFACT_MODULE_NAME,
    "modsecurity_library": ARTIFACT_LIBRARY_NAME,
}
MAX_MANIFEST_BYTES = 64 * 1024
MAX_EVIDENCE_FILE_BYTES = 8 * 1024 * 1024
MAX_EVIDENCE_TOTAL_BYTES = 20 * 1024 * 1024
RUNTIME_EXPORT_RE = re.compile(r"^export (?P<key>[A-Z0-9_]+)='(?P<value>[^'\r\n]*)'$")


class BrokerError(RuntimeError):
    """Raised when a trust or containment invariant is not satisfied."""


def fail(message: str) -> None:
    raise BrokerError(message)


def require_commit(value: object, label: str) -> str:
    if not isinstance(value, str) or not COMMIT_RE.fullmatch(value):
        fail(f"{label} must be a lowercase full Git SHA")
    return value


def require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(f"{label} must be a lowercase SHA-256")
    return value


def require_run_id(value: object) -> str:
    if not isinstance(value, str) or not RUN_ID_RE.fullmatch(value):
        fail("run_id must be a safe opaque identifier")
    return value


def require_string(value: object, label: str, *, maximum: int = 256) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        fail(f"{label} must be a non-empty bounded string")
    if "\x00" in value or "\n" in value or "\r" in value:
        fail(f"{label} must not contain control characters")
    return value


def normalized_absolute(value: str | Path, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        fail(f"{label} must be absolute: {path}")
    if ".." in path.parts:
        fail(f"{label} must not contain parent traversal: {path}")
    normalized = Path(os.path.normpath(os.fspath(path)))
    if normalized == Path("/"):
        fail(f"{label} must not be the filesystem root")
    resolved = Path(os.path.realpath(normalized))
    if resolved != normalized:
        fail(f"{label} must not resolve through a symlink: {path}")
    return normalized


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def overlaps(left: Path, right: Path) -> bool:
    return is_within(left, right) or is_within(right, left)


def no_symlink_components(path: Path, label: str, *, allow_missing_tail: bool = False) -> None:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            if allow_missing_tail:
                return
            fail(f"{label} component is missing: {current}")
        if stat.S_ISLNK(metadata.st_mode):
            fail(f"{label} contains a symlink: {current}")
        if not stat.S_ISDIR(metadata.st_mode) and current != path:
            fail(f"{label} has a non-directory component: {current}")


def directory_metadata(path: Path, label: str, *, owner: int | None = None) -> os.stat_result:
    no_symlink_components(path, label)
    try:
        metadata = os.lstat(path)
    except FileNotFoundError:
        fail(f"{label} is missing: {path}")
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        fail(f"{label} must be a non-symlink directory: {path}")
    if owner is not None and metadata.st_uid != owner:
        fail(f"{label} has an unexpected owner: {path}")
    if stat.S_IMODE(metadata.st_mode) & 0o022:
        fail(f"{label} must not be group- or other-writable: {path}")
    return metadata


def regular_metadata(path: Path, label: str, *, owner: int | None = None) -> os.stat_result:
    no_symlink_components(path, label)
    try:
        metadata = os.lstat(path)
    except FileNotFoundError:
        fail(f"{label} is missing: {path}")
    if not stat.S_ISREG(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        fail(f"{label} must be a non-symlink regular file: {path}")
    if metadata.st_nlink != 1:
        fail(f"{label} must have exactly one link: {path}")
    if owner is not None and metadata.st_uid != owner:
        fail(f"{label} has an unexpected owner: {path}")
    if stat.S_IMODE(metadata.st_mode) & 0o022:
        fail(f"{label} must not be group- or other-writable: {path}")
    return metadata


def open_regular_no_follow(path: Path, label: str) -> tuple[int, os.stat_result]:
    try:
        before = os.lstat(path)
    except FileNotFoundError:
        fail(f"{label} is missing: {path}")
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode) or before.st_nlink != 1:
        fail(f"{label} must be a single-link regular file: {path}")
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        fail(f"cannot open {label}: {exc}")
    metadata = os.fstat(descriptor)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        os.close(descriptor)
        fail(f"{label} must be a single-link regular file: {path}")
    if (metadata.st_dev, metadata.st_ino, metadata.st_size) != (before.st_dev, before.st_ino, before.st_size):
        os.close(descriptor)
        fail(f"{label} changed while being opened: {path}")
    return descriptor, metadata


def sha256_fd(descriptor: int) -> str:
    digest = hashlib.sha256()
    os.lseek(descriptor, 0, os.SEEK_SET)
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
    os.lseek(descriptor, 0, os.SEEK_SET)
    return digest.hexdigest()


def sha256_file(path: Path, label: str) -> str:
    descriptor, _ = open_regular_no_follow(path, label)
    try:
        return sha256_fd(descriptor)
    finally:
        os.close(descriptor)


def json_load_bounded(path: Path, label: str) -> dict[str, Any]:
    descriptor, metadata = open_regular_no_follow(path, label)
    try:
        if metadata.st_size > MAX_MANIFEST_BYTES:
            fail(f"{label} exceeds the manifest size limit")
        raw = bytearray()
        while len(raw) <= MAX_MANIFEST_BYTES:
            chunk = os.read(descriptor, min(8192, MAX_MANIFEST_BYTES + 1 - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
        if len(raw) > MAX_MANIFEST_BYTES:
            fail(f"{label} exceeds the manifest size limit")
    finally:
        os.close(descriptor)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid UTF-8 JSON: {exc}")
    if not isinstance(parsed, dict):
        fail(f"{label} must be a JSON object")
    return parsed


def parse_runtime_snapshot(path: Path) -> dict[str, str]:
    """Read only three declarative exports; never source the snapshot shell."""

    descriptor, metadata = open_regular_no_follow(path, RUNTIME_SNAPSHOT_LABEL)
    try:
        if metadata.st_size > MAX_MANIFEST_BYTES:
            fail("runtime environment snapshot exceeds the size limit")
        raw = bytearray()
        while len(raw) <= MAX_MANIFEST_BYTES:
            chunk = os.read(descriptor, min(8192, MAX_MANIFEST_BYTES + 1 - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
    finally:
        os.close(descriptor)
    if len(raw) > MAX_MANIFEST_BYTES:
        fail("runtime environment snapshot exceeds the size limit")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"runtime environment snapshot is not UTF-8: {exc}")
    required = {"NGINX_BINARY", "NGINX_MODULE", "MODSECURITY_SHARED_PREFIX"}
    values: dict[str, str] = {}
    for line in lines:
        match = RUNTIME_EXPORT_RE.fullmatch(line)
        if match is None:
            continue
        key = match.group("key")
        if key not in required:
            continue
        value = match.group("value")
        if not value or "'\"'\"'" in value:
            fail(f"runtime environment snapshot {key} has an unsupported quoted value")
        values[key] = value
    if set(values) != required:
        fail("runtime environment snapshot lacks required trusted NGINX exports")
    return values


def write_private_json(path: Path, payload: dict[str, Any], *, owner: int | None = None, group: int | None = None) -> None:
    parent = path.parent
    directory_metadata(parent, "manifest parent")
    temporary = parent / f".{path.name}.tmp-{os.getpid()}"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    descriptor = os.open(temporary, flags, 0o600)
    try:
        data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
        os.write(descriptor, data)
        os.fsync(descriptor)
        if owner is not None and group is not None:
            os.fchown(descriptor, owner, group)
        os.fchmod(descriptor, 0o600)
    finally:
        os.close(descriptor)
    try:
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def require_exact_keys(payload: dict[str, Any], expected: set[str], label: str) -> None:
    unknown = sorted(set(payload) - expected)
    missing = sorted(expected - set(payload))
    if unknown:
        fail(f"{label} contains unknown fields: {', '.join(unknown)}")
    if missing:
        fail(f"{label} is missing fields: {', '.join(missing)}")


CALLER_FIELDS = {
    "schema_version",
    "run_id",
    "matrix_variant",
    "parent_head_sha",
    "framework_sha",
    "protected_broker_sha",
}


def validate_caller_manifest(payload: dict[str, Any]) -> dict[str, str]:
    require_exact_keys(payload, CALLER_FIELDS, CALLER_MANIFEST_LABEL)
    if payload.get("schema_version") != SCHEMA_VERSION:
        fail("caller manifest has an unsupported schema version")
    run_id = require_run_id(payload.get("run_id"))
    variant = payload.get("matrix_variant")
    if variant not in ALLOWED_VARIANTS:
        fail("caller manifest matrix_variant is not allowed")
    return {
        "run_id": run_id,
        "matrix_variant": str(variant),
        "parent_head_sha": require_commit(payload.get("parent_head_sha"), "parent_head_sha"),
        "framework_sha": require_commit(payload.get("framework_sha"), "framework_sha"),
        "protected_broker_sha": require_commit(
            payload.get("protected_broker_sha"), "protected_broker_sha"
        ),
    }


@dataclass(frozen=True)
class ArtifactInput:
    name: str
    source: Path
    expected_sha256: str
    destination_name: str


def copy_verified_artifact(item: ArtifactInput, destination: Path, trusted_build_root: Path) -> dict[str, str]:
    source = normalized_absolute(item.source, f"{item.name} source")
    if not is_within(source, trusted_build_root):
        fail(f"{item.name} source must be inside the {TRUSTED_BUILD_ROOT_LABEL}")
    metadata = regular_metadata(source, f"{item.name} source", owner=os.geteuid())
    if metadata.st_size <= 0:
        fail(f"{item.name} source must not be empty")
    source_fd, source_metadata = open_regular_no_follow(source, f"{item.name} source")
    try:
        digest = sha256_fd(source_fd)
        if digest != item.expected_sha256:
            fail(f"{item.name} source digest does not match the expected digest")
        destination_fd = os.open(
            destination,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
        try:
            while True:
                chunk = os.read(source_fd, 1024 * 1024)
                if not chunk:
                    break
                offset = 0
                while offset < len(chunk):
                    offset += os.write(destination_fd, chunk[offset:])
            os.fsync(destination_fd)
            copied = os.fstat(destination_fd)
        finally:
            os.close(destination_fd)
        after = os.fstat(source_fd)
        if (after.st_dev, after.st_ino, after.st_size) != (
            source_metadata.st_dev,
            source_metadata.st_ino,
            source_metadata.st_size,
        ):
            fail(f"{item.name} source changed while being copied")
        if copied.st_size != source_metadata.st_size:
            fail(f"{item.name} copy has an unexpected size")
    finally:
        os.close(source_fd)
    return {"path": str(destination), "sha256": digest}


def atomic_text(path: Path, text: str, mode: int = 0o600) -> None:
    temporary = path.parent / f".{path.name}.tmp-{os.getpid()}"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    try:
        os.write(descriptor, text.encode("utf-8"))
        os.fsync(descriptor)
        os.fchmod(descriptor, mode)
    finally:
        os.close(descriptor)
    try:
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def safe_mkdir(path: Path, mode: int, label: str) -> None:
    try:
        os.mkdir(path, mode)
    except FileExistsError:
        fail(f"{label} already exists: {path}")
    except OSError as exc:
        fail(f"cannot create {label}: {exc}")
    metadata = os.lstat(path)
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        fail(f"{label} was replaced during creation")
    os.chmod(path, mode)


def artifact_set_digest(records: Iterable[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda value: value["name"]):
        digest.update(record["name"].encode("ascii") + b"\0")
        digest.update(record["sha256"].encode("ascii") + b"\0")
    return digest.hexdigest()


def candidate_layout(staging_root: Path) -> dict[str, Path]:
    return {
        "artifacts": staging_root / "artifacts",
        "control": staging_root / "control",
    }


def render_nginx_config(
    *,
    module: Path,
    runtime_root: Path,
    logs_root: Path,
    state_root: Path,
    docroot: Path,
    rules: Path,
    worker_name: str,
    worker_group: str,
    loopback: str,
    port: int,
) -> str:
    return f'''load_module "{module}";
daemon off;
worker_processes 1;
user {worker_name} {worker_group};
pid "{runtime_root / "nginx.pid"}";
error_log "{logs_root / ERROR_LOG_FILENAME}" notice;

events {{
    worker_connections 64;
}}

http {{
    access_log "{logs_root / ACCESS_LOG_FILENAME}";
    client_body_temp_path "{state_root / "client_body"}";
    proxy_temp_path "{state_root / "proxy"}";
    fastcgi_temp_path "{state_root / "fastcgi"}";
    uwsgi_temp_path "{state_root / "uwsgi"}";
    scgi_temp_path "{state_root / "scgi"}";
    server {{
        listen {loopback}:{port};
        server_name localhost;
        modsecurity on;
        modsecurity_rules_file "{rules}";
        location = /__broker_ready {{
            modsecurity off;
            return 204;
        }}
        location = /blocked {{
            root "{docroot}";
            index index.html;
        }}
        location / {{
            root "{docroot}";
            index index.html;
        }}
    }}
}}
'''


def caller_manifest_from_arguments(arguments: argparse.Namespace) -> dict[str, str]:
    caller_path = normalized_absolute(arguments.caller_manifest, CALLER_MANIFEST_LABEL)
    return validate_caller_manifest(json_load_bounded(caller_path, CALLER_MANIFEST_LABEL))


def require_matching_caller_binding(
    caller: dict[str, str],
    *,
    value: object,
    caller_field: str,
    validator: Any,
) -> None:
    if value and caller[caller_field] != validator(value):
        fail(f"caller manifest {caller_field} does not match the workflow input")


def validate_caller_bindings(arguments: argparse.Namespace, caller: dict[str, str], broker_sha: str) -> None:
    if caller["protected_broker_sha"] != broker_sha:
        fail("caller manifest protected_broker_sha does not match broker_sha")
    require_matching_caller_binding(
        caller,
        value=getattr(arguments, "expected_parent_head", ""),
        caller_field="parent_head_sha",
        validator=lambda value: require_commit(value, "expected_parent_head"),
    )
    require_matching_caller_binding(
        caller,
        value=getattr(arguments, "expected_framework_sha", ""),
        caller_field="framework_sha",
        validator=lambda value: require_commit(value, "expected_framework_sha"),
    )
    require_matching_caller_binding(
        caller,
        value=getattr(arguments, "expected_run_id", ""),
        caller_field="run_id",
        validator=require_run_id,
    )
    require_matching_caller_binding(
        caller,
        value=getattr(arguments, "expected_matrix_variant", ""),
        caller_field="matrix_variant",
        validator=lambda value: str(value),
    )


def validated_worker(arguments: argparse.Namespace) -> pwd.struct_passwd:
    if arguments.nginx_version != "1.31.3":
        fail("broker supports only reviewed NGINX version 1.31.3")
    if arguments.loopback not in LOOPBACKS:
        fail("broker supports only loopback addresses")
    if not (1024 <= arguments.port <= 65535):
        fail("broker port must be non-privileged")
    if not WORKER_NAME_RE.fullmatch(arguments.worker_user):
        fail("worker_user is unsafe")
    try:
        worker = pwd.getpwnam(arguments.worker_user)
    except KeyError as exc:
        fail(f"configured worker account is missing: {exc}")
    if worker.pw_uid == 0:
        fail("configured worker uid must not be root")
    if worker.pw_uid == os.geteuid():
        fail("configured worker uid must differ from the workflow runner")
    return worker


def trusted_build_root_from_arguments(arguments: argparse.Namespace) -> Path:
    trusted_build_root = normalized_absolute(arguments.trusted_build_root, TRUSTED_BUILD_ROOT_LABEL)
    directory_metadata(trusted_build_root, TRUSTED_BUILD_ROOT_LABEL, owner=os.geteuid())
    return trusted_build_root


def create_candidate_staging(trusted_build_root: Path) -> tuple[Path, dict[str, Path]]:
    staging_root = trusted_build_root / CANDIDATE_DIRECTORY_NAME
    if staging_root.exists() or staging_root.is_symlink():
        fail(f"{CANDIDATE_STAGING_LABEL} must be fresh")
    safe_mkdir(staging_root, 0o700, CANDIDATE_STAGING_LABEL)
    layout = candidate_layout(staging_root)
    for label in ("artifacts", "control"):
        safe_mkdir(layout[label], 0o700, f"candidate {label} root")
    return staging_root, layout


def copy_candidate_artifacts(
    arguments: argparse.Namespace,
    layout: dict[str, Path],
    trusted_build_root: Path,
) -> list[dict[str, str]]:
    artifact_specs = (
        ("binary", arguments.binary, arguments.binary_sha256, ARTIFACT_BINARY_NAME),
        ("module", arguments.module, arguments.module_sha256, ARTIFACT_MODULE_NAME),
        ("modsecurity_library", arguments.modsecurity_library, arguments.library_sha256, ARTIFACT_LIBRARY_NAME),
    )
    records: list[dict[str, str]] = []
    for name, source, digest, destination_name in artifact_specs:
        result = copy_verified_artifact(
            ArtifactInput(name, Path(source), require_sha256(digest, f"{name}_sha256"), destination_name),
            layout["artifacts"] / destination_name,
            trusted_build_root,
        )
        result["name"] = name
        records.append(result)
    return records


def candidate_payload(
    arguments: argparse.Namespace,
    caller: dict[str, str],
    broker_sha: str,
    worker: pwd.struct_passwd,
    staging_root: Path,
    records: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": caller["run_id"],
        "matrix_variant": caller["matrix_variant"],
        "parent_head_sha": caller["parent_head_sha"],
        "framework_sha": caller["framework_sha"],
        "protected_broker_sha": broker_sha,
        "runner_uid": os.geteuid(),
        "runner_gid": os.getegid(),
        "worker": {"name": worker.pw_name, "uid": worker.pw_uid, "gid": worker.pw_gid},
        "network": {"address": arguments.loopback, "port": arguments.port},
        "staging_root": str(staging_root),
        "artifacts": {record["name"]: {"path": record["path"], "sha256": record["sha256"]} for record in records},
        "artifact_digest": artifact_set_digest(records),
        "nginx_version": arguments.nginx_version,
        "producer": {"source_commit": broker_sha, "workflow_commit": broker_sha},
    }


def prepare_candidate(arguments: argparse.Namespace) -> Path:
    caller = caller_manifest_from_arguments(arguments)
    broker_sha = require_commit(arguments.broker_sha, "broker_sha")
    validate_caller_bindings(arguments, caller, broker_sha)
    worker = validated_worker(arguments)
    trusted_build_root = trusted_build_root_from_arguments(arguments)
    staging_root, layout = create_candidate_staging(trusted_build_root)
    records = copy_candidate_artifacts(arguments, layout, trusted_build_root)
    output = layout["control"] / "candidate.json"
    write_private_json(output, candidate_payload(arguments, caller, broker_sha, worker, staging_root, records))
    return output


def runtime_snapshot_from_trusted_build(trusted_build_root: Path) -> Path:
    reports_root = trusted_build_root / RUNTIME_REPORTS_RELATIVE
    directory_metadata(reports_root, "trusted runtime reports root", owner=os.geteuid())
    snapshots = sorted(reports_root.glob("runtime-env-snapshot.*.sh"))
    if len(snapshots) != 1:
        fail("trusted build must provide exactly one runtime environment snapshot")
    snapshot = normalized_absolute(snapshots[0], RUNTIME_SNAPSHOT_LABEL)
    if not is_within(snapshot, trusted_build_root):
        fail("runtime environment snapshot is outside the trusted build root")
    regular_metadata(snapshot, RUNTIME_SNAPSHOT_LABEL, owner=os.geteuid())
    return snapshot


def shared_library_from_snapshot(values: dict[str, str], trusted_build_root: Path) -> Path:
    prefix = normalized_absolute(values["MODSECURITY_SHARED_PREFIX"], "ModSecurity shared prefix")
    library_root = prefix / "lib"
    if not is_within(library_root, trusted_build_root):
        fail("ModSecurity shared prefix is outside the trusted build root")
    directory_metadata(library_root, "ModSecurity shared library root", owner=os.geteuid())
    candidates = sorted(library_root.glob("libmodsecurity.so.*"))
    if len(candidates) != 1:
        fail("trusted build must provide exactly one non-symlink ModSecurity shared library")
    library = normalized_absolute(candidates[0], TRUSTED_MODSECURITY_LIBRARY_LABEL)
    regular_metadata(library, TRUSTED_MODSECURITY_LIBRARY_LABEL, owner=os.geteuid())
    return library


def prepare_candidate_from_snapshot(arguments: argparse.Namespace) -> Path:
    trusted_build_root = trusted_build_root_from_arguments(arguments)
    values = parse_runtime_snapshot(runtime_snapshot_from_trusted_build(trusted_build_root))
    library = shared_library_from_snapshot(values, trusted_build_root)
    arguments.binary = values["NGINX_BINARY"]
    arguments.module = values["NGINX_MODULE"]
    arguments.modsecurity_library = str(library)
    arguments.binary_sha256 = sha256_file(Path(arguments.binary), "trusted NGINX binary")
    arguments.module_sha256 = sha256_file(Path(arguments.module), "trusted NGINX module")
    arguments.library_sha256 = sha256_file(library, TRUSTED_MODSECURITY_LIBRARY_LABEL)
    return prepare_candidate(arguments)


FINAL_FIELDS = {
    "schema_version",
    "run_id",
    "matrix_variant",
    "parent_head_sha",
    "framework_sha",
    "protected_broker_sha",
    "runner_uid",
    "runner_gid",
    "worker",
    "network",
    "broker_root",
    "artifacts",
    "artifact_digest",
    "producer",
    "nginx_version",
    "runtime",
    "projection",
    "expected_evidence",
}
FINAL_RUNTIME_FIELDS = {"root", "config", "rules", "docroot", "pid", "access_log", "error_log", "state"}
FINAL_PROJECTION_FIELDS = {"source_root", "target_root"}


def validated_manifest_header(payload: dict[str, Any], expected_broker_sha: str | None) -> str:
    require_exact_keys(payload, FINAL_FIELDS, "trusted broker manifest")
    if payload.get("schema_version") != SCHEMA_VERSION:
        fail("trusted broker manifest has an unsupported schema version")
    require_run_id(payload.get("run_id"))
    if payload.get("matrix_variant") not in ALLOWED_VARIANTS:
        fail("trusted broker manifest matrix_variant is not allowed")
    require_commit(payload.get("parent_head_sha"), "parent_head_sha")
    require_commit(payload.get("framework_sha"), "framework_sha")
    broker_sha = require_commit(payload.get("protected_broker_sha"), "protected_broker_sha")
    if expected_broker_sha is not None and broker_sha != expected_broker_sha:
        fail("trusted broker manifest protected_broker_sha mismatch")
    return broker_sha


def validate_final_manifest_identities(payload: dict[str, Any]) -> None:
    if not isinstance(payload.get("runner_uid"), int) or payload["runner_uid"] <= 0:
        fail("trusted broker manifest runner_uid is invalid")
    if not isinstance(payload.get("runner_gid"), int) or payload["runner_gid"] < 0:
        fail("trusted broker manifest runner_gid is invalid")
    worker = payload.get("worker")
    if not isinstance(worker, dict) or set(worker) != {"name", "uid", "gid"}:
        fail("trusted broker manifest worker shape is invalid")
    if not WORKER_NAME_RE.fullmatch(str(worker["name"])):
        fail("trusted broker manifest worker name is invalid")
    if not isinstance(worker["uid"], int) or worker["uid"] <= 0:
        fail("trusted broker manifest worker uid is invalid")
    if not isinstance(worker["gid"], int) or worker["gid"] < 0:
        fail("trusted broker manifest worker gid is invalid")
    if worker["uid"] == payload["runner_uid"]:
        fail("trusted broker manifest worker uid must differ from runner uid")


def validate_final_manifest_network(payload: dict[str, Any]) -> None:
    network = payload.get("network")
    if not isinstance(network, dict) or set(network) != {"address", "port"}:
        fail("trusted broker manifest network shape is invalid")
    if network["address"] not in LOOPBACKS or not isinstance(network["port"], int) or not (1024 <= network["port"] <= 65535):
        fail("trusted broker manifest network is not a loopback non-privileged listener")
    if payload.get("nginx_version") != "1.31.3":
        fail("trusted broker manifest NGINX version is not approved")


def final_manifest_artifact_records(payload: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != {"binary", "module", "modsecurity_library"}:
        fail("trusted broker manifest artifacts are invalid")
    artifact_records: list[dict[str, str]] = []
    for name, record in artifacts.items():
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            fail(f"trusted broker manifest {name} record is invalid")
        normalized_absolute(str(record["path"]), f"trusted broker {name} path")
        artifact_records.append({"name": name, "path": str(record["path"]), "sha256": require_sha256(record["sha256"], f"trusted broker {name} digest")})
    return artifact_records


def validate_final_manifest_artifacts(payload: dict[str, Any]) -> None:
    records = final_manifest_artifact_records(payload)
    if artifact_set_digest(records) != require_sha256(payload.get("artifact_digest"), "trusted broker artifact_digest"):
        fail("trusted broker manifest artifact digest is invalid")


def validate_final_manifest_paths(payload: dict[str, Any]) -> None:
    runtime = payload.get("runtime")
    if not isinstance(runtime, dict) or set(runtime) != FINAL_RUNTIME_FIELDS:
        fail("trusted broker manifest runtime paths are invalid")
    projection = payload.get("projection")
    if not isinstance(projection, dict) or set(projection) != FINAL_PROJECTION_FIELDS:
        fail("trusted broker manifest projection paths are invalid")
    for label, value in {**runtime, **projection}.items():
        normalized_absolute(str(value), f"trusted broker {label} path")


def validate_final_manifest_producer(payload: dict[str, Any], broker_sha: str) -> None:
    producer = payload.get("producer")
    if not isinstance(producer, dict) or set(producer) != {"source_commit", "workflow_commit"}:
        fail("trusted broker manifest producer identity is invalid")
    if producer["source_commit"] != broker_sha or producer["workflow_commit"] != broker_sha:
        fail("trusted broker manifest producer is not bound to the broker SHA")
    if tuple(payload.get("expected_evidence", [])) != EXPECTED_EVIDENCE:
        fail("trusted broker manifest evidence allowlist is invalid")


def validated_final_manifest(path: Path, expected_broker_sha: str | None = None) -> dict[str, Any]:
    payload = json_load_bounded(path, "trusted broker manifest")
    broker_sha = validated_manifest_header(payload, expected_broker_sha)
    validate_final_manifest_identities(payload)
    validate_final_manifest_network(payload)
    validate_final_manifest_artifacts(payload)
    validate_final_manifest_paths(payload)
    validate_final_manifest_producer(payload, broker_sha)
    return payload


def require_root() -> None:
    if os.geteuid() != 0:
        fail("broker privileged action requires root")


def sudo_runner_uid() -> int:
    raw = os.environ.get("SUDO_UID", "")
    if not raw.isdecimal() or int(raw) <= 0:
        fail("broker requires a non-root sudo caller identity")
    return int(raw)


def sudo_runner_gid() -> int:
    raw = os.environ.get("SUDO_GID", "")
    if not raw.isdecimal():
        fail("broker requires a sudo caller group identity")
    return int(raw)


def secure_root_parent(runner_gid: int) -> Path:
    directory_metadata(ROOT_STATE_BASE, "broker state base", owner=0)
    if ROOT_PARENT.exists() or ROOT_PARENT.is_symlink():
        metadata = directory_metadata(ROOT_PARENT, BROKER_ROOT_PARENT_LABEL, owner=0)
    else:
        safe_mkdir(ROOT_PARENT, ROOT_PARENT_MODE, BROKER_ROOT_PARENT_LABEL)
        try:
            os.chown(ROOT_PARENT, 0, runner_gid)
            metadata = directory_metadata(ROOT_PARENT, BROKER_ROOT_PARENT_LABEL, owner=0)
        except Exception as original_error:
            try:
                remove_empty_new_root_parent()
            except Exception as cleanup_error:
                raise BrokerError(
                    f"broker root parent setup failed and its empty private state could not be removed: {cleanup_error}"
                ) from original_error
            raise
    if metadata.st_gid != runner_gid or stat.S_IMODE(metadata.st_mode) != ROOT_PARENT_MODE:
        fail("broker root parent ownership or mode is invalid")
    return ROOT_PARENT


def remove_empty_new_root_parent() -> None:
    metadata = directory_metadata(ROOT_PARENT, "new broker root parent", owner=0)
    if stat.S_IMODE(metadata.st_mode) != ROOT_PARENT_MODE:
        fail("new broker root parent mode is invalid")
    os.rmdir(ROOT_PARENT)


def copy_into_root(source: Path, destination: Path, expected_sha: str, label: str) -> None:
    source_fd, source_metadata = open_regular_no_follow(source, label)
    try:
        if sha256_fd(source_fd) != expected_sha:
            fail(f"{label} digest mismatch before root admission")
        destination_fd = os.open(destination, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
        try:
            while True:
                chunk = os.read(source_fd, 1024 * 1024)
                if not chunk:
                    break
                written = 0
                while written < len(chunk):
                    written += os.write(destination_fd, chunk[written:])
            os.fsync(destination_fd)
            if sha256_fd(destination_fd) != expected_sha:
                fail(f"{label} digest mismatch after root admission")
            os.fchown(destination_fd, 0, 0)
            os.fchmod(destination_fd, 0o500 if label == "NGINX binary" else 0o400)
        finally:
            os.close(destination_fd)
        after = os.fstat(source_fd)
        if (source_metadata.st_dev, source_metadata.st_ino, source_metadata.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            fail(f"{label} changed while being admitted")
    finally:
        os.close(source_fd)


def root_layout(root: Path) -> dict[str, Path]:
    return {
        "artifacts": root / "artifacts",
        "runtime": root / "runtime",
        "logs": root / "runtime" / "logs",
        "state": root / "runtime" / "state",
        "docroot": root / "runtime" / "docroot",
        "control": root / "control",
        "evidence_source": root / "evidence-source",
        "projection_target": root / "evidence-published",
    }


def cleanup_entry_metadata(directory_fd: int, name: str, expected_device: int, label: str) -> os.stat_result:
    if not name or name in {".", ".."} or "/" in name:
        fail(f"{label} contains an unsafe cleanup entry")
    metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    if metadata.st_dev != expected_device:
        fail(f"{label} contains an entry on another device: {name}")
    return metadata


def remove_cleanup_directory(
    directory_fd: int,
    name: str,
    metadata: os.stat_result,
    expected_device: int,
    label: str,
) -> None:
    try:
        child_fd = os.open(
            name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=directory_fd,
        )
    except OSError as exc:
        fail(f"cannot safely open cleanup directory {name}: {exc}")
    try:
        opened = os.fstat(child_fd)
        if (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
            fail(f"cleanup directory changed while being opened: {name}")
        remove_directory_contents_no_follow(child_fd, expected_device, f"{label}/{name}")
    finally:
        os.close(child_fd)
    after = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
    if (after.st_dev, after.st_ino) != (metadata.st_dev, metadata.st_ino):
        fail(f"cleanup directory changed before removal: {name}")
    os.rmdir(name, dir_fd=directory_fd)


def remove_directory_contents_no_follow(directory_fd: int, expected_device: int, label: str) -> None:
    """Remove a private tree without ever traversing a caller-controlled link.

    This is deliberately descriptor-relative rather than ``rmtree``: a
    stopped worker may have left arbitrary names in its writable log/state
    directories, but cleanup must never follow any of them out of the broker
    run root.
    """

    for name in os.listdir(directory_fd):
        metadata = cleanup_entry_metadata(directory_fd, name, expected_device, label)
        if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
            remove_cleanup_directory(directory_fd, name, metadata, expected_device, label)
        else:
            # ``unlink`` is descriptor-relative and removes a link/special
            # file itself.  It never follows it, which is precisely what the
            # root-owned cleanup needs.
            os.unlink(name, dir_fd=directory_fd)


def remove_broker_root(
    root: Path,
    run_id: str,
    runner_gid: int,
    *,
    allow_initial_root_group: bool = False,
) -> None:
    """Remove exactly one stopped broker run root with no path traversal."""

    root = normalized_absolute(root, "broker cleanup root")
    if root.name != run_id or root.parent != ROOT_PARENT:
        fail("broker cleanup root is not the fixed run-specific location")
    parent = root.parent
    parent_metadata = directory_metadata(parent, "broker cleanup parent", owner=0)
    if parent_metadata.st_gid != runner_gid or stat.S_IMODE(parent_metadata.st_mode) != ROOT_PARENT_MODE:
        fail("broker cleanup parent ownership or mode is invalid")
    parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        root_metadata = os.stat(root.name, dir_fd=parent_fd, follow_symlinks=False)
        allowed_groups = {runner_gid}
        if allow_initial_root_group:
            allowed_groups.add(0)
        if (
            not stat.S_ISDIR(root_metadata.st_mode)
            or stat.S_ISLNK(root_metadata.st_mode)
            or root_metadata.st_uid != 0
            or root_metadata.st_gid not in allowed_groups
            or stat.S_IMODE(root_metadata.st_mode) != 0o710
        ):
            fail("broker cleanup root metadata is invalid")
        root_fd = os.open(
            root.name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=parent_fd,
        )
        try:
            opened = os.fstat(root_fd)
            if (opened.st_dev, opened.st_ino) != (root_metadata.st_dev, root_metadata.st_ino):
                fail("broker cleanup root changed while being opened")
            remove_directory_contents_no_follow(root_fd, root_metadata.st_dev, "broker cleanup root")
        finally:
            os.close(root_fd)
        after = os.stat(root.name, dir_fd=parent_fd, follow_symlinks=False)
        if (after.st_dev, after.st_ino) != (root_metadata.st_dev, root_metadata.st_ino):
            fail("broker cleanup root changed before removal")
        os.rmdir(root.name, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


CANDIDATE_FIELDS = {
    "schema_version",
    "run_id",
    "matrix_variant",
    "parent_head_sha",
    "framework_sha",
    "protected_broker_sha",
    "runner_uid",
    "runner_gid",
    "worker",
    "network",
    "staging_root",
    "artifacts",
    "artifact_digest",
    "nginx_version",
    "producer",
}


def load_candidate_for_admission(
    arguments: argparse.Namespace,
    runner_uid: int,
    runner_gid: int,
) -> tuple[dict[str, Any], str, str, dict[str, Path]]:
    candidate_path = normalized_absolute(arguments.candidate, CANDIDATE_LABEL)
    regular_metadata(candidate_path, CANDIDATE_LABEL, owner=runner_uid)
    candidate = json_load_bounded(candidate_path, CANDIDATE_LABEL)
    require_exact_keys(candidate, CANDIDATE_FIELDS, CANDIDATE_LABEL)
    if candidate.get("runner_uid") != runner_uid or candidate.get("runner_gid") != runner_gid:
        fail("broker candidate runner identity does not match sudo caller")
    broker_sha = require_commit(arguments.broker_sha, "broker_sha")
    if candidate.get("protected_broker_sha") != broker_sha:
        fail("broker candidate protected_broker_sha mismatch")
    staging_root = normalized_absolute(str(candidate.get("staging_root", "")), CANDIDATE_STAGING_LABEL)
    directory_metadata(staging_root, CANDIDATE_STAGING_LABEL, owner=runner_uid)
    candidate_paths = candidate_layout(staging_root)
    directory_metadata(candidate_paths["artifacts"], "candidate artifact root", owner=runner_uid)
    directory_metadata(candidate_paths["control"], "candidate control root", owner=runner_uid)
    if candidate_path != candidate_paths["control"] / "candidate.json":
        fail("broker candidate must be in its declared staging control root")
    if candidate.get("schema_version") != SCHEMA_VERSION:
        fail("broker candidate schema version is invalid")
    run_id = require_run_id(candidate.get("run_id"))
    if candidate.get("matrix_variant") not in ALLOWED_VARIANTS:
        fail("broker candidate matrix variant is invalid")
    require_commit(candidate.get("parent_head_sha"), "candidate parent_head_sha")
    require_commit(candidate.get("framework_sha"), "candidate framework_sha")
    if candidate.get("nginx_version") != "1.31.3":
        fail("broker candidate NGINX version is invalid")
    return candidate, broker_sha, run_id, candidate_paths


def resolved_candidate_worker(
    candidate: dict[str, Any],
    runner_uid: int,
) -> tuple[dict[str, Any], pwd.struct_passwd, str]:
    worker_candidate = candidate.get("worker")
    if not isinstance(worker_candidate, dict) or set(worker_candidate) != {"name", "uid", "gid"}:
        fail("broker candidate worker identity is invalid")
    if (
        not WORKER_NAME_RE.fullmatch(str(worker_candidate["name"]))
        or not isinstance(worker_candidate["uid"], int)
        or not isinstance(worker_candidate["gid"], int)
        or worker_candidate["uid"] <= 0
        or worker_candidate["gid"] < 0
        or worker_candidate["uid"] == runner_uid
    ):
        fail("broker candidate worker identity is malformed")
    try:
        account = pwd.getpwnam(str(worker_candidate["name"]))
        group_name = grp.getgrgid(int(worker_candidate["gid"])).gr_name
    except KeyError as exc:
        fail(f"broker candidate worker account is unavailable: {exc}")
    if account.pw_uid != worker_candidate["uid"] or account.pw_gid != worker_candidate["gid"] or account.pw_uid <= 0:
        fail("broker candidate worker identity no longer matches the local account")
    return worker_candidate, account, group_name


def validated_candidate_network(candidate: dict[str, Any]) -> dict[str, Any]:
    network_candidate = candidate.get("network")
    if not isinstance(network_candidate, dict) or set(network_candidate) != {"address", "port"}:
        fail("broker candidate network is invalid")
    if (
        network_candidate["address"] not in LOOPBACKS
        or not isinstance(network_candidate["port"], int)
        or not (1024 <= network_candidate["port"] <= 65535)
    ):
        fail("broker candidate network is not loopback/non-privileged")
    return network_candidate


def validate_candidate_producer(candidate: dict[str, Any], broker_sha: str) -> dict[str, Any]:
    producer_candidate = candidate.get("producer")
    if not isinstance(producer_candidate, dict) or set(producer_candidate) != {"source_commit", "workflow_commit"}:
        fail("broker candidate producer identity is invalid")
    if producer_candidate["source_commit"] != broker_sha or producer_candidate["workflow_commit"] != broker_sha:
        fail("broker candidate producer is not bound to the protected broker SHA")
    return producer_candidate


def validated_candidate_artifacts(
    candidate: dict[str, Any],
    candidate_paths: dict[str, Path],
    runner_uid: int,
) -> dict[str, dict[str, str]]:
    artifacts = candidate.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != set(ARTIFACT_DESTINATION_NAMES):
        fail("broker candidate artifacts are invalid")
    candidate_artifacts: dict[str, dict[str, str]] = {}
    for name, destination_name in ARTIFACT_DESTINATION_NAMES.items():
        record = artifacts[name]
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            fail(f"broker candidate {name} record is invalid")
        source = normalized_absolute(str(record["path"]), f"candidate {name} path")
        if source != candidate_paths["artifacts"] / destination_name:
            fail(f"candidate {name} path is not the fixed staging artifact path")
        regular_metadata(source, f"candidate {name} path", owner=runner_uid)
        candidate_artifacts[name] = {
            "path": str(source),
            "sha256": require_sha256(record["sha256"], f"candidate {name} digest"),
        }
    records = [dict(name=name, **record) for name, record in candidate_artifacts.items()]
    if artifact_set_digest(records) != require_sha256(candidate.get("artifact_digest"), "candidate artifact_digest"):
        fail("broker candidate artifact digest is invalid")
    return candidate_artifacts


def create_admitted_root(root: Path, runner_gid: int) -> None:
    safe_mkdir(root, 0o710, "broker run root")
    try:
        os.chown(root, 0, runner_gid)
    except Exception as original_error:
        try:
            remove_broker_root(
                root,
                root.name,
                runner_gid,
                allow_initial_root_group=True,
            )
        except Exception as cleanup_error:
            raise BrokerError(
                f"broker run root setup failed and its private state could not be removed: {cleanup_error}"
            ) from original_error
        raise


def create_admitted_layout(root: Path, worker_gid: int) -> dict[str, Path]:
    layout = root_layout(root)
    for key in ("artifacts", "runtime", "logs", "state", "docroot", "control", "evidence_source"):
        safe_mkdir(layout[key], 0o700, f"broker {key}")
        os.chown(layout[key], 0, 0)
    os.chown(layout["runtime"], 0, worker_gid)
    os.chmod(layout["runtime"], 0o710)
    for key in ("logs", "state", "docroot"):
        os.chown(layout[key], 0, worker_gid)
        os.chmod(layout[key], 0o730 if key in {"logs", "state"} else 0o710)
    return layout


def admit_candidate_artifacts(
    candidate_artifacts: dict[str, dict[str, str]],
    layout: dict[str, Path],
) -> dict[str, dict[str, str]]:
    admitted: dict[str, dict[str, str]] = {}
    for name, destination_name in ARTIFACT_DESTINATION_NAMES.items():
        record = candidate_artifacts[name]
        destination = layout["artifacts"] / destination_name
        copy_into_root(
            Path(record["path"]),
            destination,
            record["sha256"],
            "NGINX binary" if name == "binary" else name,
        )
        admitted[name] = {"path": str(destination), "sha256": record["sha256"]}
    return admitted


def admitted_runtime(
    layout: dict[str, Path],
    account: pwd.struct_passwd,
    group_name: str,
    network: dict[str, Any],
    worker_gid: int,
) -> dict[str, str]:
    rules = layout["runtime"] / BROKER_RULES_FILENAME
    index = layout["docroot"] / "index.html"
    config = layout["runtime"] / BROKER_CONFIG_FILENAME
    atomic_text(rules, 'SecRuleEngine On\nSecRule REQUEST_URI "@streq /blocked" "id:941001,phase:1,deny,status:403,log"\n', 0o400)
    atomic_text(index, "trusted nginx root broker\n", 0o640)
    atomic_text(
        config,
        render_nginx_config(
            module=layout["artifacts"] / ARTIFACT_MODULE_NAME,
            runtime_root=layout["runtime"],
            logs_root=layout["logs"],
            state_root=layout["state"],
            docroot=layout["docroot"],
            rules=rules,
            worker_name=account.pw_name,
            worker_group=group_name,
            loopback=str(network["address"]),
            port=int(network["port"]),
        ),
        0o400,
    )
    for path, mode in ((rules, 0o400), (config, 0o400), (index, 0o640)):
        os.chown(path, 0, worker_gid)
        os.chmod(path, mode)
    return {
        "root": str(layout["runtime"]),
        "config": str(config),
        "rules": str(rules),
        "docroot": str(layout["docroot"]),
        "pid": str(layout["runtime"] / PID_FILENAME),
        "access_log": str(layout["logs"] / ACCESS_LOG_FILENAME),
        "error_log": str(layout["logs"] / ERROR_LOG_FILENAME),
        "state": str(layout["control"] / STATE_FILENAME),
    }


def admitted_manifest_payload(
    candidate: dict[str, Any],
    broker_sha: str,
    runner_uid: int,
    runner_gid: int,
    root: Path,
    artifacts: dict[str, dict[str, str]],
    runtime: dict[str, str],
    layout: dict[str, Path],
    network: dict[str, Any],
    producer: dict[str, Any],
    worker: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": candidate["run_id"],
        "matrix_variant": candidate["matrix_variant"],
        "parent_head_sha": candidate["parent_head_sha"],
        "framework_sha": candidate["framework_sha"],
        "protected_broker_sha": broker_sha,
        "runner_uid": runner_uid,
        "runner_gid": runner_gid,
        "worker": worker,
        "network": network,
        "broker_root": str(root),
        "artifacts": artifacts,
        "artifact_digest": candidate["artifact_digest"],
        "producer": producer,
        "nginx_version": candidate["nginx_version"],
        "runtime": runtime,
        "projection": {
            "source_root": str(layout["evidence_source"]),
            "target_root": str(layout["projection_target"]),
        },
        "expected_evidence": list(EXPECTED_EVIDENCE),
    }


def admit_candidate(arguments: argparse.Namespace) -> Path:
    require_root()
    runner_uid = sudo_runner_uid()
    runner_gid = sudo_runner_gid()
    candidate, broker_sha, run_id, candidate_paths = load_candidate_for_admission(arguments, runner_uid, runner_gid)
    worker, account, group_name = resolved_candidate_worker(candidate, runner_uid)
    network = validated_candidate_network(candidate)
    producer = validate_candidate_producer(candidate, broker_sha)
    candidate_artifacts = validated_candidate_artifacts(candidate, candidate_paths, runner_uid)
    root = secure_root_parent(runner_gid) / run_id
    if root.exists() or root.is_symlink():
        fail("broker run root already exists")
    root_created = False
    try:
        create_admitted_root(root, runner_gid)
        root_created = True
        layout = create_admitted_layout(root, int(worker["gid"]))
        artifacts = admit_candidate_artifacts(candidate_artifacts, layout)
        runtime = admitted_runtime(layout, account, group_name, network, int(worker["gid"]))
        manifest = layout["control"] / "manifest.json"
        payload = admitted_manifest_payload(
            candidate,
            broker_sha,
            runner_uid,
            runner_gid,
            root,
            artifacts,
            runtime,
            layout,
            network,
            producer,
            worker,
        )
        write_private_json(manifest, payload, owner=0, group=0)
        return manifest
    except Exception as original_error:
        if root_created:
            try:
                remove_broker_root(root, run_id, runner_gid)
            except Exception as cleanup_error:
                raise BrokerError(
                    f"root admission failed and its private run root could not be removed: {cleanup_error}"
                ) from original_error
        raise


def manifest_paths(payload: dict[str, Any]) -> tuple[Path, dict[str, Path]]:
    root = normalized_absolute(str(payload["broker_root"]), BROKER_ROOT_LABEL)
    if root.parent != ROOT_PARENT or root.name != payload["run_id"]:
        fail("broker root is not the fixed run-specific location")
    layout = root_layout(root)
    expected_artifacts = {
        "binary": layout["artifacts"] / ARTIFACT_BINARY_NAME,
        "module": layout["artifacts"] / ARTIFACT_MODULE_NAME,
        "modsecurity_library": layout["artifacts"] / ARTIFACT_LIBRARY_NAME,
    }
    for name, expected in expected_artifacts.items():
        if Path(str(payload["artifacts"][name]["path"])) != expected:
            fail(f"manifest {name} path is not the fixed broker artifact path")
    expected_runtime = {
        "root": layout["runtime"],
        "config": layout["runtime"] / BROKER_CONFIG_FILENAME,
        "rules": layout["runtime"] / BROKER_RULES_FILENAME,
        "docroot": layout["docroot"],
        "pid": layout["runtime"] / PID_FILENAME,
        "access_log": layout["logs"] / ACCESS_LOG_FILENAME,
        "error_log": layout["logs"] / ERROR_LOG_FILENAME,
        "state": layout["control"] / STATE_FILENAME,
    }
    for name, expected in expected_runtime.items():
        if Path(str(payload["runtime"][name])) != expected:
            fail(f"manifest {name} path is not the fixed broker runtime path")
    if Path(str(payload["projection"]["source_root"])) != layout["evidence_source"]:
        fail("manifest evidence source is not the fixed broker evidence root")
    if Path(str(payload["projection"]["target_root"])) != layout["projection_target"]:
        fail("manifest evidence target is not the fixed broker projection root")
    for path in [*layout.values(), *expected_artifacts.values(), *expected_runtime.values()]:
        normalized = normalized_absolute(path, "manifest path")
        if not is_within(normalized, root):
            fail(f"manifest path escapes broker root: {normalized}")
    return root, layout


def require_directory_layout(path: Path, *, owner: int, group: int, mode: int, label: str) -> None:
    metadata = directory_metadata(path, label, owner=owner)
    if metadata.st_gid != group or stat.S_IMODE(metadata.st_mode) != mode:
        fail(f"{label} ownership or mode changed")


def require_file_layout(path: Path, *, owner: int, group: int, mode: int, label: str) -> None:
    metadata = regular_metadata(path, label, owner=owner)
    if metadata.st_gid != group or stat.S_IMODE(metadata.st_mode) != mode:
        fail(f"{label} ownership or mode changed")


def validate_root_layout(payload: dict[str, Any]) -> tuple[Path, dict[str, Path]]:
    root, layout = manifest_paths(payload)
    require_directory_layout(
        root,
        owner=0,
        group=int(payload["runner_gid"]),
        mode=0o710,
        label=BROKER_ROOT_LABEL,
    )
    for key in ("artifacts", "control", "evidence_source"):
        require_directory_layout(layout[key], owner=0, group=0, mode=0o700, label=f"broker {key}")
    require_directory_layout(
        layout["runtime"],
        owner=0,
        group=int(payload["worker"]["gid"]),
        mode=0o710,
        label="broker runtime",
    )
    for key in ("logs", "state"):
        require_directory_layout(
            layout[key],
            owner=0,
            group=int(payload["worker"]["gid"]),
            mode=0o730,
            label=f"broker {key}",
        )
    require_directory_layout(
        layout["docroot"],
        owner=0,
        group=int(payload["worker"]["gid"]),
        mode=0o710,
        label="broker docroot",
    )
    for name, mode in (("binary", 0o500), ("module", 0o400), ("modsecurity_library", 0o400)):
        require_file_layout(
            Path(str(payload["artifacts"][name]["path"])),
            owner=0,
            group=0,
            mode=mode,
            label=f"admitted {name}",
        )
    runtime = payload["runtime"]
    for key in ("config", "rules"):
        require_file_layout(
            Path(str(runtime[key])),
            owner=0,
            group=int(payload["worker"]["gid"]),
            mode=0o400,
            label=f"admitted NGINX {key}",
        )
    require_file_layout(
        layout["docroot"] / "index.html",
        owner=0,
        group=int(payload["worker"]["gid"]),
        mode=0o640,
        label="admitted NGINX document",
    )
    projection = layout["projection_target"]
    if projection.exists() or projection.is_symlink():
        require_directory_layout(
            projection,
            owner=0,
            group=int(payload["runner_gid"]),
            mode=0o750,
            label="broker evidence projection",
        )
    return root, layout


def validate_runtime_config(payload: dict[str, Any]) -> None:
    runtime = payload["runtime"]
    config = Path(str(runtime["config"]))
    descriptor, metadata = open_regular_no_follow(config, "admitted NGINX configuration")
    try:
        if metadata.st_uid != 0 or stat.S_IMODE(metadata.st_mode) != 0o400:
            fail("admitted NGINX configuration ownership or mode changed")
        raw = bytearray()
        while True:
            chunk = os.read(descriptor, 8192)
            if not chunk:
                break
            raw.extend(chunk)
    finally:
        os.close(descriptor)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"admitted NGINX configuration is not UTF-8: {exc}")
    try:
        worker_group = grp.getgrgid(int(payload["worker"]["gid"])).gr_name
    except KeyError as exc:
        fail(f"broker worker group is unavailable: {exc}")
    _, layout = manifest_paths(payload)
    expected = render_nginx_config(
        module=Path(str(payload["artifacts"]["module"]["path"])),
        runtime_root=Path(str(runtime["root"])),
        logs_root=layout["logs"],
        state_root=layout["state"],
        docroot=Path(str(runtime["docroot"])),
        rules=Path(str(runtime["rules"])),
        worker_name=str(payload["worker"]["name"]),
        worker_group=worker_group,
        loopback=str(payload["network"]["address"]),
        port=int(payload["network"]["port"]),
    )
    if text != expected:
        fail("broker configuration differs from the fixed root-generated configuration")


def clean_environment(library_dir: Path) -> dict[str, str]:
    return {
        "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
        "HOME": "/nonexistent",
        "LANG": "C",
        "LC_ALL": "C",
        "LD_LIBRARY_PATH": str(library_dir),
    }


def state_path(payload: dict[str, Any]) -> Path:
    return Path(str(payload["runtime"]["state"]))


def read_state(payload: dict[str, Any]) -> dict[str, Any]:
    path = state_path(payload)
    return json_load_bounded(path, "broker state")


def write_state(payload: dict[str, Any], state: dict[str, Any]) -> None:
    write_private_json(state_path(payload), state, owner=0, group=0)


def open_verified_artifact(payload: dict[str, Any], name: str, mode: int) -> int:
    path = Path(str(payload["artifacts"][name]["path"]))
    descriptor, metadata = open_regular_no_follow(path, f"admitted {name}")
    digest = sha256_fd(descriptor)
    if digest != payload["artifacts"][name]["sha256"]:
        os.close(descriptor)
        fail(f"admitted {name} digest changed")
    if metadata.st_uid != 0 or metadata.st_gid != 0 or stat.S_IMODE(metadata.st_mode) != mode:
        os.close(descriptor)
        fail(f"admitted {name} ownership or mode changed")
    return descriptor


def verify_admitted_artifact(payload: dict[str, Any], name: str, mode: int) -> None:
    descriptor = open_verified_artifact(payload, name, mode)
    os.close(descriptor)


def nginx_command(payload: dict[str, Any], *arguments: str) -> list[str]:
    descriptor = open_verified_artifact(payload, "binary", 0o500)
    # Keep the descriptor open across subprocess execution so `/proc/self/fd`
    # continues to bind the executable to the verified inode.
    return [f"/proc/self/fd/{descriptor}", *arguments]


def run_nginx(payload: dict[str, Any], *arguments: str, wait: bool) -> subprocess.Popen[bytes] | subprocess.CompletedProcess[bytes]:
    validate_root_layout(payload)
    verify_admitted_artifact(payload, "module", 0o400)
    verify_admitted_artifact(payload, "modsecurity_library", 0o400)
    command = nginx_command(payload, *arguments)
    descriptor = int(command[0].rsplit("/", 1)[1])
    runtime = payload["runtime"]
    library = Path(str(payload["artifacts"]["modsecurity_library"]["path"])).parent
    try:
        if wait:
            return subprocess.run(
                command,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=clean_environment(library),
                pass_fds=(descriptor,),
            )
        return subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(runtime["root"]),
            env=clean_environment(library),
            pass_fds=(descriptor,),
            start_new_session=True,
        )
    finally:
        os.close(descriptor)


def config_test(payload: dict[str, Any]) -> None:
    validate_runtime_config(payload)
    runtime = payload["runtime"]
    version = run_nginx(payload, "-v", wait=True)
    assert isinstance(version, subprocess.CompletedProcess)
    version_output = version.stdout.decode("utf-8", errors="replace")
    if version.returncode != 0 or f"nginx/{payload['nginx_version']}" not in version_output:
        fail("admitted NGINX version readback does not match the manifest")
    result = run_nginx(payload, "-t", "-p", str(runtime["root"]), "-c", str(runtime["config"]), wait=True)
    assert isinstance(result, subprocess.CompletedProcess)
    if result.returncode != 0:
        output = result.stdout.decode("utf-8", errors="replace")[-2000:]
        fail(f"NGINX configuration test failed: {output}")


def read_bound_pid_file(path: Path) -> int:
    descriptor, metadata = open_regular_no_follow(path, "broker NGINX PID file")
    try:
        if metadata.st_uid != 0 or metadata.st_size <= 0 or metadata.st_size > 32:
            fail("broker NGINX PID file metadata is invalid")
        raw = os.read(descriptor, 33)
    finally:
        os.close(descriptor)
    if len(raw) > 32:
        fail("broker NGINX PID file is too large")
    try:
        value = raw.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        fail(f"broker NGINX PID file is not ASCII: {exc}")
    if not value.isdecimal() or int(value) <= 1:
        fail("broker NGINX PID file is not a valid process identifier")
    return int(value)


def process_group_exists(process_group: int) -> bool:
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    return True


def process_uses_admitted_binary(pid: int, payload: dict[str, Any]) -> bool:
    binary = Path(str(payload["artifacts"]["binary"]["path"]))
    try:
        binary_metadata = os.stat(binary)
        process_metadata = os.stat(f"/proc/{pid}/exe")
    except FileNotFoundError:
        return False
    return (process_metadata.st_dev, process_metadata.st_ino) == (
        binary_metadata.st_dev,
        binary_metadata.st_ino,
    )


def wait_for_process_group_exit(process_group: int, *, timeout_seconds: float = 10) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if not process_group_exists(process_group):
            return
        time.sleep(0.1)
    fail("NGINX process group did not stop")


def terminate_new_process_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate a group that was just created by this process, if necessary."""

    if process.poll() is not None:
        return
    if os.getpgid(process.pid) != process.pid:
        fail("new NGINX process did not retain its dedicated process group")
    os.killpg(process.pid, signal.SIGTERM)
    try:
        wait_for_process_group_exit(process.pid, timeout_seconds=5)
    except BrokerError:
        os.killpg(process.pid, signal.SIGKILL)
        wait_for_process_group_exit(process.pid, timeout_seconds=5)


def start(payload: dict[str, Any]) -> None:
    config_test(payload)
    runtime = payload["runtime"]
    process = run_nginx(payload, "-p", str(runtime["root"]), "-c", str(runtime["config"]), wait=False)
    assert isinstance(process, subprocess.Popen)
    pid_path = Path(str(runtime["pid"]))
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if pid_path.exists() and not pid_path.is_symlink():
                break
            if process.poll() is not None:
                fail("NGINX root master exited before creating its PID file")
            time.sleep(0.1)
        else:
            fail("NGINX root master did not create its PID file")
        if read_bound_pid_file(pid_path) != process.pid:
            fail("NGINX PID file does not bind the current root master")
        if not process_uses_admitted_binary(process.pid, payload):
            fail("started NGINX root master is not the admitted binary")
        if os.getpgid(process.pid) != process.pid:
            fail("started NGINX root master did not retain its dedicated process group")
    except Exception:
        terminate_new_process_group(process)
        raise
    write_state(payload, {"master_pid": process.pid, "process_group": process.pid, "started": True})


def proc_uid_gid(pid: int) -> tuple[int, int]:
    metadata = os.stat(f"/proc/{pid}")
    return metadata.st_uid, metadata.st_gid


def process_children(pid: int) -> list[int]:
    raw = Path(f"/proc/{pid}/task/{pid}/children").read_text(encoding="ascii").strip()
    return [int(item) for item in raw.split() if item.isdecimal()]


def verify_master_worker_identity(payload: dict[str, Any]) -> dict[str, Any]:
    state = read_state(payload)
    master_pid = state.get("master_pid")
    if not isinstance(master_pid, int) or master_pid <= 1:
        fail("broker state lacks a valid master PID")
    master_uid, _ = proc_uid_gid(master_pid)
    if master_uid != 0:
        fail("NGINX master is not running as root")
    process_group = state.get("process_group")
    if not isinstance(process_group, int) or os.getpgid(master_pid) != process_group:
        fail("NGINX master process group does not match broker state")
    if not process_uses_admitted_binary(master_pid, payload):
        fail("NGINX master executable is not the admitted binary")
    children = process_children(master_pid)
    if len(children) != 1:
        fail("NGINX master has an unexpected number of direct children")
    worker_candidates: list[int] = []
    for child in children:
        uid, gid = proc_uid_gid(child)
        if uid == payload["worker"]["uid"] and gid == payload["worker"]["gid"]:
            if process_uses_admitted_binary(child, payload):
                worker_candidates.append(child)
    if len(worker_candidates) != 1:
        fail("NGINX worker identity is missing, duplicated, or has an unexpected executable")
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "run_id": payload["run_id"],
        "parent_head_sha": payload["parent_head_sha"],
        "framework_sha": payload["framework_sha"],
        "protected_broker_sha": payload["protected_broker_sha"],
        "nginx_binary_sha256": payload["artifacts"]["binary"]["sha256"],
        "nginx_module_sha256": payload["artifacts"]["module"]["sha256"],
        "nginx_version": payload["nginx_version"],
        "master_pid": master_pid,
        "master_uid": master_uid,
        "worker_pid": worker_candidates[0],
        "worker_uid": payload["worker"]["uid"],
        "worker_gid": payload["worker"]["gid"],
    }
    source = Path(str(payload["projection"]["source_root"]))
    write_private_json(source / IDENTITY_EVIDENCE_FILENAME, evidence, owner=0, group=0)
    return evidence


def write_runtime_evidence(payload: dict[str, Any]) -> None:
    source = Path(str(payload["projection"]["source_root"]))
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "run_id": payload["run_id"],
        "matrix_variant": payload["matrix_variant"],
        "parent_head_sha": payload["parent_head_sha"],
        "framework_sha": payload["framework_sha"],
        "protected_broker_sha": payload["protected_broker_sha"],
        "artifact_digest": payload["artifact_digest"],
        "nginx_binary_sha256": payload["artifacts"]["binary"]["sha256"],
        "nginx_module_sha256": payload["artifacts"]["module"]["sha256"],
        "nginx_version": payload["nginx_version"],
        "root_broker_status": "PASS",
        "scope": "root-broker-only; CRS validation is intentionally outside this protected broker",
    }
    write_private_json(source / RUNTIME_EVIDENCE_FILENAME, evidence, owner=0, group=0)


def copy_evidence_file(
    source: Path,
    target: Path,
    *,
    runner_gid: int,
    allowed_owners: set[int],
    expected_device: int,
    label: str,
) -> int:
    source_fd, source_metadata = open_regular_no_follow(source, label)
    try:
        if source_metadata.st_size > MAX_EVIDENCE_FILE_BYTES:
            fail(f"{label} exceeds the evidence file size limit")
        if source_metadata.st_uid not in allowed_owners:
            fail(f"{label} has an unexpected owner")
        if source_metadata.st_dev != expected_device:
            fail(f"{label} is on an unexpected device")
        if stat.S_IMODE(source_metadata.st_mode) & 0o022:
            fail(f"{label} is group- or other-writable")
        target_fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            remaining = source_metadata.st_size
            while remaining:
                chunk = os.read(source_fd, min(1024 * 1024, remaining))
                if not chunk:
                    fail(f"{label} was truncated during projection")
                offset = 0
                while offset < len(chunk):
                    offset += os.write(target_fd, chunk[offset:])
                remaining -= len(chunk)
            copied = os.fstat(target_fd)
            if copied.st_size != source_metadata.st_size:
                fail(f"{label} projection size mismatch")
            after = os.fstat(source_fd)
            if (after.st_dev, after.st_ino, after.st_size) != (
                source_metadata.st_dev,
                source_metadata.st_ino,
                source_metadata.st_size,
            ):
                fail(f"{label} changed during projection")
            os.fchown(target_fd, 0, runner_gid)
            os.fchmod(target_fd, 0o640)
        finally:
            os.close(target_fd)
    finally:
        os.close(source_fd)
    return source_metadata.st_size


def project_evidence(payload: dict[str, Any]) -> None:
    state = read_state(payload)
    if not state.get("stopped"):
        fail("evidence projection requires a stopped NGINX process group")
    write_runtime_evidence(payload)
    source_root = Path(str(payload["projection"]["source_root"]))
    target_root = Path(str(payload["projection"]["target_root"]))
    if target_root.exists() or target_root.is_symlink():
        fail("evidence projection target already exists")
    temporary = target_root.parent / f".{target_root.name}.tmp-{os.getpid()}"
    safe_mkdir(temporary, 0o700, "evidence projection staging root")
    total = 0
    try:
        names_to_sources = {
            IDENTITY_EVIDENCE_FILENAME: source_root / IDENTITY_EVIDENCE_FILENAME,
            RUNTIME_EVIDENCE_FILENAME: source_root / RUNTIME_EVIDENCE_FILENAME,
            ACCESS_LOG_FILENAME: Path(str(payload["runtime"]["access_log"])),
            ERROR_LOG_FILENAME: Path(str(payload["runtime"]["error_log"])),
        }
        if tuple(names_to_sources) != EXPECTED_EVIDENCE:
            fail("evidence projection allowlist changed unexpectedly")
        root_device = directory_metadata(Path(str(payload["broker_root"])), BROKER_ROOT_LABEL, owner=0).st_dev
        for name, source in names_to_sources.items():
            owners = {0} if name.endswith(".json") else {0, int(payload["worker"]["uid"])}
            total += copy_evidence_file(
                source,
                temporary / name,
                runner_gid=int(payload["runner_gid"]),
                allowed_owners=owners,
                expected_device=root_device,
                label=name,
            )
            if total > MAX_EVIDENCE_TOTAL_BYTES:
                fail("evidence projection exceeds total size limit")
        descriptor = os.open(temporary, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fchown(descriptor, 0, int(payload["runner_gid"]))
            os.fchmod(descriptor, 0o750)
        finally:
            os.close(descriptor)
        os.replace(temporary, target_root)
    finally:
        try:
            temporary.rmdir()
        except OSError:
            pass


def remove_bound_pid_file(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    descriptor, metadata = open_regular_no_follow(path, "broker NGINX PID file")
    try:
        if metadata.st_uid != 0:
            fail("broker NGINX PID file owner is invalid")
    finally:
        os.close(descriptor)
    os.unlink(path)


def stop(payload: dict[str, Any]) -> None:
    state_file = state_path(payload)
    if not state_file.exists() and not state_file.is_symlink():
        remove_bound_pid_file(Path(str(payload["runtime"]["pid"])))
        write_state(payload, {"started": False, "stopped": True})
        return
    state = read_state(payload)
    if state.get("stopped"):
        return
    master_pid = state.get("master_pid")
    process_group = state.get("process_group")
    if not isinstance(master_pid, int) or not isinstance(process_group, int) or process_group <= 1:
        fail("broker state lacks a valid live process group")
    if Path(f"/proc/{master_pid}").exists():
        master_uid, _ = proc_uid_gid(master_pid)
        if (
            master_uid != 0
            or os.getpgid(master_pid) != process_group
            or not process_uses_admitted_binary(master_pid, payload)
        ):
            fail("broker refuses to signal an unbound NGINX process group")
        os.killpg(process_group, signal.SIGTERM)
        try:
            wait_for_process_group_exit(process_group, timeout_seconds=5)
        except BrokerError:
            os.killpg(process_group, signal.SIGKILL)
            wait_for_process_group_exit(process_group, timeout_seconds=5)
    elif process_group_exists(process_group):
        fail("broker refuses to signal a process group without its bound master")
    pid_path = Path(str(payload["runtime"]["pid"]))
    remove_bound_pid_file(pid_path)
    write_state(payload, {"master_pid": master_pid, "process_group": process_group, "stopped": True})


def verify_listener_released(address: str, port: int) -> None:
    family = socket.AF_INET6 if address == "::1" else socket.AF_INET
    with socket.socket(family, socket.SOCK_STREAM) as probe:
        if family == socket.AF_INET6:
            probe.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        try:
            probe.bind((address, port))
        except OSError as exc:
            fail(f"cleanup found a remaining listener on the broker port: {exc}")


def cleanup_status(payload: dict[str, Any]) -> None:
    state = read_state(payload)
    if not state.get("stopped"):
        fail("cleanup requires a stopped NGINX process group")
    master_pid = state.get("master_pid")
    if isinstance(master_pid, int) and Path(f"/proc/{master_pid}").exists():
        fail("cleanup found a remaining NGINX master process")
    process_group = state.get("process_group")
    if isinstance(process_group, int) and process_group_exists(process_group):
        fail("cleanup found a remaining NGINX process group")
    pid_path = Path(str(payload["runtime"]["pid"]))
    try:
        if pid_path.exists() or pid_path.is_symlink():
            fail("cleanup found a remaining NGINX PID file")
    finally:
        verify_listener_released(str(payload["network"]["address"]), int(payload["network"]["port"]))
    remove_broker_root(
        Path(str(payload["broker_root"])),
        str(payload["run_id"]),
        int(payload["runner_gid"]),
    )


def execute_action(arguments: argparse.Namespace) -> None:
    if arguments.action not in ALLOWED_ACTIONS:
        fail("broker action is not allowed")
    if arguments.action == "validate-manifest":
        manifest = admit_candidate(arguments)
        print(manifest)
        return
    require_root()
    manifest_path = normalized_absolute(arguments.manifest, "broker manifest")
    payload = validated_final_manifest(manifest_path, require_commit(arguments.broker_sha, "broker_sha"))
    root, _ = manifest_paths(payload)
    directory_metadata(root, BROKER_ROOT_LABEL, owner=0)
    if arguments.action == "config-test":
        config_test(payload)
    elif arguments.action == "start":
        start(payload)
    elif arguments.action == "verify-master-worker-identity":
        verify_master_worker_identity(payload)
    elif arguments.action == "project-evidence":
        project_evidence(payload)
    elif arguments.action == "stop":
        stop(payload)
    elif arguments.action == "cleanup-status":
        cleanup_status(payload)


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare-candidate")
    prepare.add_argument("--caller-manifest", required=True)
    prepare.add_argument("--trusted-build-root", required=True)
    prepare.add_argument("--broker-sha", required=True)
    prepare.add_argument("--expected-parent-head", default="")
    prepare.add_argument("--expected-framework-sha", default="")
    prepare.add_argument("--expected-run-id", default="")
    prepare.add_argument("--expected-matrix-variant", default="")
    prepare.add_argument("--binary", required=True)
    prepare.add_argument("--binary-sha256", required=True)
    prepare.add_argument("--module", required=True)
    prepare.add_argument("--module-sha256", required=True)
    prepare.add_argument("--modsecurity-library", required=True)
    prepare.add_argument("--library-sha256", required=True)
    prepare.add_argument("--nginx-version", required=True)
    prepare.add_argument("--worker-user", default="www-data")
    prepare.add_argument("--loopback", default="127.0.0.1")
    prepare.add_argument("--port", type=int, required=True)

    snapshot = commands.add_parser("prepare-from-snapshot")
    snapshot.add_argument("--caller-manifest", required=True)
    snapshot.add_argument("--trusted-build-root", required=True)
    snapshot.add_argument("--broker-sha", required=True)
    snapshot.add_argument("--expected-parent-head", default="")
    snapshot.add_argument("--expected-framework-sha", default="")
    snapshot.add_argument("--expected-run-id", default="")
    snapshot.add_argument("--expected-matrix-variant", default="")
    snapshot.add_argument("--nginx-version", required=True)
    snapshot.add_argument("--worker-user", default="www-data")
    snapshot.add_argument("--loopback", default="127.0.0.1")
    snapshot.add_argument("--port", type=int, required=True)

    action = commands.add_parser("action")
    action.add_argument("--action", required=True, choices=sorted(ALLOWED_ACTIONS))
    action.add_argument("--broker-sha", required=True)
    action.add_argument("--candidate")
    action.add_argument("--manifest")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        if arguments.command == "prepare-candidate":
            print(prepare_candidate(arguments))
        elif arguments.command == "prepare-from-snapshot":
            print(prepare_candidate_from_snapshot(arguments))
        else:
            if arguments.action == "validate-manifest":
                if not arguments.candidate:
                    fail("validate-manifest requires --candidate")
            elif not arguments.manifest:
                fail(f"{arguments.action} requires --manifest")
            execute_action(arguments)
    except (BrokerError, OSError, ValueError, KeyError) as exc:
        print(f"BLOCKED: trusted NGINX root broker: {exc}", file=sys.stderr)
        return 77
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
