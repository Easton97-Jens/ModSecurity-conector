#!/usr/bin/env python3
"""Constrained Base-owned supervisor for an exact-head NGINX runtime cell.

Only the protected Base checkout supplies this launcher, its shell helper and
the final collector.  A candidate checkout is never mounted as executable
source: its NGINX binary, module and libModSecurity image are admitted through
single-link descriptors and run only below a disposable user/mount/pid/network
namespace.  Scratch evidence is untrusted until this supervisor has stopped
the namespace, checked kernel process identity and atomically published a
small root-owned allowlist for the independent collector.
"""

from __future__ import annotations

import argparse
import ctypes
from dataclasses import dataclass
import functools
import hashlib
import json
import os
from pathlib import Path
import pwd
import grp
import re
import resource
import select
import shutil
import signal
import stat
import subprocess
import sys
import time
from typing import Any, Callable


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ROOT_RUN_NAME = "ModSecurity-conector-nginx-exact-head"
CELL_NAME = "root-launcher-cell"
APPARMOR_PROFILE_NAME = "msconnector-nginx-exact-head-userns"
APPARMOR_PROFILE_PATH = Path("/etc/apparmor.d") / APPARMOR_PROFILE_NAME
APPARMOR_PROFILE_TEXT = """abi <abi/4.0>,
include <tunables/global>

profile msconnector-nginx-exact-head-userns flags=(unconfined) {
  userns,
}
"""
SUPERVISOR_TIMEOUT = 90.0
POLL_INTERVAL = 0.05
MAX_MANIFEST_BYTES = 64 * 1024
MAX_SNAPSHOT_BYTES = MAX_MANIFEST_BYTES
MAX_READY_BYTES = 4096
MAX_RUNTIME_LOG_BYTES = 2 * 1024 * 1024
MAX_GENERATED_CONFIG_BYTES = 128 * 1024
MAX_PROC_STATUS_BYTES = 64 * 1024
MAX_SANDBOX_FILE_BYTES = 16 * 1024 * 1024
MAX_SANDBOX_ADDRESS_SPACE_BYTES = 1536 * 1024 * 1024
MAX_SANDBOX_PROCESSES = 128
MAX_SANDBOX_OPEN_FILES = 256
MAX_ADMITTED_ARTIFACT_BYTES = 256 * 1024 * 1024
PR_SET_CHILD_SUBREAPER = 36
TX_RE = re.compile(r"^nginx-exact-head-[0-9]+-[0-9]+-[0-9]+$")
CALLBACK_TX_RE = re.compile(
    r"\bmodsecurity_transaction_id=(nginx-exact-head-[0-9]+-[0-9]+-[0-9]+)\b"
)
RULE_1000001_RE = re.compile(r"(?<![0-9])1000001(?![0-9])")
FORBIDDEN_MARKERS = re.compile(r"canary|query[-_ ]?secret|password|token", re.IGNORECASE)
BASE_DRIVER_RELATIVE = Path("ci/runtime/broker/run_nginx_exact_head_cells.sh")
SANDBOX_BASE_HELPER = Path("/run/nginx-exact-head-base-helper.sh")
SANDBOX_TMPDIR = Path("/run/nginx-exact-head-tmp")
EXPECTED_NGINX_VERSION = "1.31.4"
EXPECTED_NGINX_SOURCE_DIGEST = "e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3"
DISPATCHER_FIELDS = frozenset({
    "schema_version", "trusted_dispatcher_base_sha", "run_id", "pr_number",
    "tested_pr_head", "tested_pr_head_ref", "tested_pr_head_repository",
    "tested_pr_base", "tested_pr_base_ref", "tested_pr_base_repository",
    "draft", "state", "merged",
})
CANDIDATE_MANIFEST_FIELDS = frozenset({
    "schema_version", "run_id", "tested_pr_head", "trusted_dispatcher_base_sha",
    "nginx_version", "nginx_source_digest", "artifacts", "producer",
})
ARTIFACT_RECORD_FIELDS = frozenset({"filename", "sha256", "size"})
ROOT_EVIDENCE_FILES = frozenset({
    "identity.json", "runtime.json", "on.jsonl", "off.jsonl", "exit.json",
})
HELPERS = {
    "sh": "/bin/sh",
    "git": "/usr/bin/git",
    "setpriv": "/usr/bin/setpriv",
    "unshare": "/usr/bin/unshare",
    "bwrap": "/usr/bin/bwrap",
    "newuidmap": "/usr/bin/newuidmap",
    "newgidmap": "/usr/bin/newgidmap",
    "aa-exec": "/usr/bin/aa-exec",
    "aa-status": "/usr/sbin/aa-status",
    "curl": "/usr/bin/curl",
    "groupadd": "/usr/sbin/groupadd",
    "useradd": "/usr/sbin/useradd",
    "userdel": "/usr/sbin/userdel",
    "groupdel": "/usr/sbin/groupdel",
    "id": "/usr/bin/id",
    "usermod": "/usr/sbin/usermod",
}


class LauncherError(RuntimeError):
    """A controlled refusal or failed runtime control."""


@dataclass(frozen=True)
class IdentityExpectations:
    runner_uid: int
    runner_gid: int
    worker_uid: int
    worker_gid: int


@dataclass
class SubordinateMapping:
    runner_name: str
    runner_uid: int
    worker_uid: int
    worker_gid: int
    uid_added: bool = False
    gid_added: bool = False


@dataclass(frozen=True)
class ProcessHandle:
    pid: int
    pidfd: int


# Commands are always executed without a shell.  Keep a second, explicit
# boundary here because several arguments are derived from filesystem metadata
# and are later forwarded through the namespace helper and its shell script.
COMMAND_FORBIDDEN_CHARS = frozenset("\x00\n\r;&|$`<>()")


def fail(message: str) -> None:
    raise LauncherError(message)


def validated_command(argv: list[str]) -> list[str]:
    """Return an argv list safe for the fixed no-shell execution boundary."""
    if not argv or any(type(argument) is not str or not argument for argument in argv):
        fail("checked command contains an invalid argument")
    if not os.path.isabs(argv[0]) or any(
        character in COMMAND_FORBIDDEN_CHARS
        for argument in argv
        for character in argument
    ):
        fail("checked command contains an unsafe executable or argument")
    return list(argv)


def open_regular_no_follow(path: Path, label: str) -> int:
    """Open a regular file by descriptor-walking from the trusted root."""
    path = no_symlink_path(path, label)
    try:
        descriptor = os.open(
            path.root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
        )
    except OSError as exc:
        fail(f"unable to open trusted filesystem root for {label}: {exc}")
    try:
        parts = path.parts[1:]
        if not parts:
            fail(f"{label} is not a regular file")
        for index, part in enumerate(parts):
            flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
            if index != len(parts) - 1:
                flags |= os.O_DIRECTORY
            next_descriptor = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
            fail(f"unsafe regular-file requirement: {path.name}")
        result = descriptor
        descriptor = -1
        return result
    except OSError as exc:
        fail(f"unable to safely open {label}: {exc}")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def bounded_file(path: Path, limit: int) -> bytes:
    try:
        descriptor = open_regular_no_follow(path, "bounded input")
    except LauncherError:
        raise
    try:
        initial = os.fstat(descriptor)
        if initial.st_nlink != 1 or initial.st_size > limit:
            fail(f"bounded input too large: {path.name}")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 64 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        final = os.fstat(descriptor)
        if len(data) > limit or (
            initial.st_dev, initial.st_ino, initial.st_size, initial.st_mtime_ns,
            initial.st_nlink,
        ) != (
            final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns,
            final.st_nlink,
        ):
            fail(f"bounded input grew while being read: {path.name}")
        return data
    finally:
        os.close(descriptor)


def admitted_artifact_identity(descriptor: int, label: str) -> dict[str, int | str]:
    """Read one already-open regular artifact into a stable bounded identity."""
    try:
        initial = os.fstat(descriptor)
        if (
            not stat.S_ISREG(initial.st_mode)
            or initial.st_nlink != 1
            or initial.st_size <= 0
            or initial.st_size > MAX_ADMITTED_ARTIFACT_BYTES
        ):
            fail(f"{label} exceeds the admitted artifact bound")
        digest = hashlib.sha256()
        os.lseek(descriptor, 0, os.SEEK_SET)
        remaining = MAX_ADMITTED_ARTIFACT_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            digest.update(chunk)
            remaining -= len(chunk)
        if remaining == 0:
            fail(f"{label} grew beyond the admitted artifact bound")
        final = os.fstat(descriptor)
        if (
            initial.st_dev,
            initial.st_ino,
            initial.st_size,
            initial.st_mtime_ns,
        ) != (
            final.st_dev,
            final.st_ino,
            final.st_size,
            final.st_mtime_ns,
        ):
            fail(f"{label} changed while its identity was admitted")
        return {
            "device": initial.st_dev,
            "inode": initial.st_ino,
            "sha256": digest.hexdigest(),
            "size": initial.st_size,
        }
    except OSError as exc:
        fail(f"unable to admit {label}: {exc}")


def admitted_artifact(path: Path, label: str) -> dict[str, int | str]:
    """Return a stable, bounded identity for an admitted regular artifact."""
    descriptor = open_regular_no_follow(path, f"admitted {label}")
    try:
        return admitted_artifact_identity(descriptor, label)
    finally:
        os.close(descriptor)


def admitted_artifact_descriptor(path: Path, label: str) -> tuple[int, dict[str, int | str]]:
    """Retain an admitted artifact descriptor for a race-free sandbox bind."""
    descriptor = open_regular_no_follow(path, f"admitted {label}")
    try:
        return descriptor, admitted_artifact_identity(descriptor, label)
    except BaseException:
        os.close(descriptor)
        raise


def bounded_proc_file(path: Path, limit: int) -> bytes:
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    except OSError as exc:
        fail(f"unable to open kernel evidence: {path.name}: {exc}")
    try:
        data = os.read(descriptor, limit + 1)
        if len(data) > limit:
            fail(f"kernel evidence exceeds bound: {path.name}")
        return data
    finally:
        os.close(descriptor)


def no_symlink_path(path: Path, label: str) -> Path:
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        fail(f"{label} must be an absolute normalized path")
    path = Path(os.path.normpath(os.fspath(path)))
    current = Path(path.root)
    for part in path.parts[1:]:
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            fail(f"{label} component is missing")
        if stat.S_ISLNK(mode):
            fail(f"{label} contains a symbolic link")
    return path


def contained(path: Path, root: Path, label: str) -> Path:
    path = no_symlink_path(path, label)
    root = no_symlink_path(root, "runner temporary root")
    try:
        path.relative_to(root)
    except ValueError:
        fail(f"{label} escapes runner temporary root")
    return path


def duplicate_safe(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            fail("duplicate JSON key in data-only manifest")
        value[key] = item
    return value


def json_object(path: Path, label: str, limit: int = MAX_MANIFEST_BYTES) -> dict[str, Any]:
    try:
        value = json.loads(
            bounded_file(path, limit).decode("utf-8"), object_pairs_hook=duplicate_safe
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not valid UTF-8 JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def require_sha40(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA_RE.fullmatch(value) is None:
        fail(f"{label} must be a lowercase 40-character SHA")
    return value


def require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        fail(f"{label} must be a lowercase SHA-256")
    return value


def require_exact_fields(value: dict[str, Any], expected: frozenset[str], label: str) -> None:
    if frozenset(value) != expected:
        fail(f"{label} fields do not match the fixed schema")


def dispatcher_manifest(path: Path, trusted_base_sha: str) -> dict[str, Any]:
    """Validate the immutable PR decision again at the privilege boundary."""
    value = json_object(path, "dispatcher manifest")
    require_exact_fields(value, DISPATCHER_FIELDS, "dispatcher manifest")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        fail("dispatcher manifest schema is unsupported")
    if type(value.get("pr_number")) is not int or value["pr_number"] <= 0:
        fail("dispatcher manifest PR number is invalid")
    if not isinstance(value.get("run_id"), str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value["run_id"]
    ):
        fail("dispatcher manifest run ID is invalid")
    if require_sha40(value.get("trusted_dispatcher_base_sha"), "dispatcher base SHA") != trusted_base_sha:
        fail("dispatcher manifest does not bind this Base revision")
    require_sha40(value.get("tested_pr_head"), "tested PR head SHA")
    require_sha40(value.get("tested_pr_base"), "tested PR base SHA")
    if (
        value.get("tested_pr_base_ref") != "master"
        or value.get("tested_pr_base_repository") != "Easton97-Jens/ModSecurity-conector"
        or value.get("tested_pr_head_repository") != "Easton97-Jens/ModSecurity-conector"
        or value.get("state") != "open"
        or value.get("draft") is not True
        or value.get("merged") is not False
    ):
        fail("dispatcher manifest does not represent an eligible canonical draft")
    if not isinstance(value.get("tested_pr_head_ref"), str) or not value["tested_pr_head_ref"]:
        fail("dispatcher manifest head ref is invalid")
    return value


def candidate_manifest(path: Path, dispatcher: dict[str, Any]) -> dict[str, Any]:
    """Bind untrusted artifacts to the previously admitted PR decision."""
    value = json_object(path, "candidate artifact manifest")
    require_exact_fields(value, CANDIDATE_MANIFEST_FIELDS, "candidate artifact manifest")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        fail("candidate artifact manifest schema is unsupported")
    if value.get("run_id") != dispatcher["run_id"]:
        fail("candidate artifact manifest run ID does not match dispatcher")
    if value.get("tested_pr_head") != dispatcher["tested_pr_head"]:
        fail("candidate artifact manifest head does not match dispatcher")
    if value.get("trusted_dispatcher_base_sha") != dispatcher["trusted_dispatcher_base_sha"]:
        fail("candidate artifact manifest Base revision does not match dispatcher")
    if (
        value.get("nginx_version") != EXPECTED_NGINX_VERSION
        or value.get("nginx_source_digest") != EXPECTED_NGINX_SOURCE_DIGEST
    ):
        fail("candidate artifact manifest does not bind pinned NGINX 1.31.4")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, dict) or frozenset(artifacts) != {"nginx", "module", "library"}:
        fail("candidate artifact manifest has an invalid artifact set")
    expected_names = {
        "nginx": "nginx",
        "module": "ngx_http_modsecurity_module.so",
        "library": "libmodsecurity.so.3",
    }
    for key, name in expected_names.items():
        record = artifacts[key]
        if not isinstance(record, dict):
            fail("candidate artifact record is not an object")
        require_exact_fields(record, ARTIFACT_RECORD_FIELDS, "candidate artifact record")
        if record.get("filename") != name or type(record.get("size")) is not int:
            fail("candidate artifact record has an invalid name or size")
        if record["size"] <= 0 or record["size"] > MAX_ADMITTED_ARTIFACT_BYTES:
            fail("candidate artifact record size is outside the allowed bound")
        require_sha256(record.get("sha256"), "candidate artifact digest")
    producer = value.get("producer")
    if not isinstance(producer, dict) or frozenset(producer) != {"kind", "runner_uid", "runner_gid"}:
        fail("candidate producer record is invalid")
    if producer.get("kind") != "unprivileged-exact-head-build":
        fail("candidate producer kind is invalid")
    if type(producer.get("runner_uid")) is not int or type(producer.get("runner_gid")) is not int:
        fail("candidate producer identity is invalid")
    return value


def validate_admitted_artifacts(
    manifest: dict[str, Any], admitted: dict[str, dict[str, int | str]]
) -> None:
    for key, identity in admitted.items():
        record = manifest["artifacts"][key]
        if (
            identity["sha256"] != record["sha256"]
            or identity["size"] != record["size"]
        ):
            fail("admitted artifact does not match its candidate manifest digest")


def run_checked(
    argv: list[str],
    *,
    env: dict[str, str] | None = None,
    timeout: float = 10.0,
    capture: bool = True,
    pass_fds: tuple[int, ...] = (),
    preexec_fn: Callable[[], None] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(validated_command(argv), check=True, env=env, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None,
                          timeout=timeout, pass_fds=pass_fds,
                          preexec_fn=preexec_fn)


def validate_exit_status(status: int) -> None:
    if status == 77:
        fail("Exit 77 is a fatal runtime failure")
    if status != 0:
        fail(f"trusted exact-head helper failed with status {status}")


def runner_checked(argv: list[str], runner_uid: int, runner_gid: int,
                   *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    command = [
        HELPERS["setpriv"], f"--reuid={runner_uid}", f"--regid={runner_gid}",
        "--clear-groups", "--no-new-privs", "--inh-caps=-all",
        "--ambient-caps=-all", "--bounding-set=-all", "--", *argv,
    ]
    return run_checked(command, env=env)


def runner_checked_bytes(
    argv: list[str], runner_uid: int, runner_gid: int, *, env: dict[str, str]
) -> subprocess.CompletedProcess[bytes]:
    """Run a fixed command as the runner without decoding trusted Git bytes."""
    command = [
        HELPERS["setpriv"],
        f"--reuid={runner_uid}",
        f"--regid={runner_gid}",
        "--clear-groups",
        "--no-new-privs",
        "--inh-caps=-all",
        "--ambient-caps=-all",
        "--bounding-set=-all",
        "--",
        *argv,
    ]
    return subprocess.run(
        validated_command(command),
        check=True,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15,
    )


def base_git_environment() -> dict[str, str]:
    return {
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "HOME": "/nonexistent",
    }


def trusted_base_file_descriptor(
    repo: Path,
    expected_sha: str,
    relative: Path,
    runner_uid: int,
    runner_gid: int,
    label: str,
) -> tuple[int, bytes]:
    """Bind one Base source file to its exact Git blob and a retained FD."""
    if relative.is_absolute() or any(part in {".", ".."} for part in relative.parts):
        fail(f"{label} has an unsafe Base-relative path")
    env = base_git_environment()
    fixed = [
        HELPERS["git"],
        "-c",
        "core.hooksPath=/nonexistent",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "diff.external=false",
        "-C",
        str(repo),
    ]
    try:
        expected = runner_checked_bytes(
            [*fixed, "show", f"{expected_sha}:{relative.as_posix()}"],
            runner_uid,
            runner_gid,
            env=env,
        ).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"could not read exact Base blob for {label}: {exc}")
    if not expected or len(expected) > MAX_ADMITTED_ARTIFACT_BYTES:
        fail(f"exact Base blob for {label} has an unsafe size")
    path = contained(repo / relative, repo, label)
    descriptor, identity = admitted_artifact_descriptor(path, label)
    expected_digest = hashlib.sha256(expected).hexdigest()
    if identity["sha256"] != expected_digest or identity["size"] != len(expected):
        os.close(descriptor)
        fail(f"{label} does not match the checked-out exact Base blob")
    return descriptor, expected


def verify_checkout(repo: Path, expected: str, runner_uid: int, runner_gid: int) -> None:
    """Bind the runner-owned worktree to one clean exact Git checkout."""
    env = base_git_environment()
    fixed = [
        HELPERS["git"], "-c", "core.hooksPath=/nonexistent", "-c",
        "core.fsmonitor=false", "-c", "diff.external=false", "-C", str(repo),
    ]
    top_level = runner_checked(
        [*fixed, "rev-parse", "--show-toplevel"], runner_uid, runner_gid, env=env
    )
    if top_level.stdout.strip() != str(repo):
        fail("repository root is not the canonical checked-out worktree")
    head = runner_checked(
        [*fixed, "rev-parse", "--verify", "HEAD"], runner_uid, runner_gid, env=env
    )
    if head.stdout.strip() != expected:
        fail("repository HEAD does not match expected exact SHA")
    status_result = runner_checked(
        [*fixed, "status", "--porcelain=v1", "--untracked-files=all",
         "--ignore-submodules=none"],
        runner_uid,
        runner_gid,
        env=env,
    )
    if status_result.stdout:
        fail("exact-head worktree or gitlink state is not clean")


def verify_helper(path: str) -> None:
    helper = Path(path)
    st = helper.stat()
    if st.st_uid != 0 or st.st_mode & 0o022 or not stat.S_ISREG(st.st_mode):
        fail(f"sandbox helper is not root-owned and nonwritable: {helper.name}")


def verify_helpers() -> None:
    for path in HELPERS.values():
        verify_helper(path)
    for name in ("newuidmap", "newgidmap"):
        st = Path(HELPERS[name]).stat()
        if not st.st_mode & stat.S_ISUID:
            fail(f"subordinate mapping helper is not setuid root: {name}")


def verify_apparmor_profile() -> None:
    st = APPARMOR_PROFILE_PATH.lstat()
    if (stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode) or st.st_uid != 0
            or st.st_mode & 0o022):
        fail("exact-head AppArmor profile is unsafe")
    if bounded_file(APPARMOR_PROFILE_PATH, 4096).decode("utf-8") != APPARMOR_PROFILE_TEXT:
        fail("exact-head AppArmor profile content is not the approved userns policy")
    try:
        run_checked([HELPERS["aa-status"], "--enabled"], capture=False)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        fail(f"AppArmor is not enabled: {exc}")


def apparmor_label(pid: int) -> str:
    try:
        return bounded_proc_file(
            Path(f"/proc/{pid}/attr/current"), 4096
        ).decode("ascii").strip()
    except OSError as exc:
        fail(f"unable to read AppArmor kernel evidence: {exc}")


def verify_runner_owned_directory(path: Path, expected_uid: int, expected_gid: int,
                                  label: str) -> None:
    st = path.lstat()
    if (stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode)
            or st.st_uid != expected_uid or st.st_gid != expected_gid
            or st.st_mode & 0o022):
        fail(f"{label} is not an exact nonwritable runner-owned directory")


def create_runner_owned_directory(path: Path, uid: int, gid: int) -> None:
    path.mkdir(mode=0o700)
    os.chown(path, uid, gid)
    os.chmod(path, 0o700)


def apply_sandbox_limits() -> None:
    """Bound only the child before it executes the trusted namespace chain."""
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (int(SUPERVISOR_TIMEOUT), int(SUPERVISOR_TIMEOUT)))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_SANDBOX_FILE_BYTES, MAX_SANDBOX_FILE_BYTES))
    resource.setrlimit(
        resource.RLIMIT_AS,
        (MAX_SANDBOX_ADDRESS_SPACE_BYTES, MAX_SANDBOX_ADDRESS_SPACE_BYTES),
    )
    resource.setrlimit(resource.RLIMIT_NPROC, (MAX_SANDBOX_PROCESSES, MAX_SANDBOX_PROCESSES))
    resource.setrlimit(resource.RLIMIT_NOFILE, (MAX_SANDBOX_OPEN_FILES, MAX_SANDBOX_OPEN_FILES))


def proc_status_text(pid: int) -> str:
    if pid <= 1:
        fail("invalid process identifier for kernel evidence")
    try:
        return bounded_proc_file(
            Path(f"/proc/{pid}/status"), MAX_PROC_STATUS_BYTES
        ).decode("ascii")
    except OSError as exc:
        fail(f"unable to read /proc identity evidence: {exc}")


def status(pid: int) -> dict[str, int]:
    values: dict[str, int] = {}
    for line in proc_status_text(pid).splitlines():
        key, _, raw = line.partition(":")
        if key in {"Uid", "Gid", "PPid"}:
            fields = raw.split()
            if key == "PPid":
                values["ppid"] = int(fields[0])
            else:
                values[key.lower() + "_real"] = int(fields[0])
                values[key.lower() + "_effective"] = int(fields[1])
    if len(values) != 5:
        fail("incomplete /proc identity evidence")
    return values


def namespace_process_ids(pid: int) -> list[int]:
    for line in proc_status_text(pid).splitlines():
        if line.startswith("NSpid:"):
            try:
                values = [int(value) for value in line.split()[1:]]
            except ValueError as exc:
                fail(f"invalid NSpid kernel evidence: {exc}")
            if values and all(value > 0 for value in values):
                return values
    fail("missing NSpid kernel evidence")


def is_descendant_of(pid: int, ancestor: int) -> bool:
    seen: set[int] = set()
    current = pid
    while current > 1 and current not in seen:
        if current == ancestor:
            return True
        seen.add(current)
        current = status(current)["ppid"]
    return False


def enable_child_subreaper() -> None:
    """Adopt descendants that outlive their direct namespace supervisor."""
    libc = ctypes.CDLL(None, use_errno=True)
    result = libc.prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0)
    if result != 0:
        fail(f"unable to enable child subreaper: {os.strerror(ctypes.get_errno())}")


def snapshot_supervisor_descendants(supervisor_pid: int) -> list[ProcessHandle]:
    """Capture stable handles for every currently live supervisor descendant."""
    handles: list[ProcessHandle] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        candidate = int(entry.name)
        if candidate == supervisor_pid:
            continue
        try:
            if not is_descendant_of(candidate, supervisor_pid):
                continue
            handles.append(ProcessHandle(candidate, os.pidfd_open(candidate)))
        except (LauncherError, OSError):
            # A process can exit between proc enumeration and pidfd admission.
            continue
    return handles


def pidfd_exited(pidfd: int) -> bool:
    poller = select.poll()
    poller.register(pidfd, select.POLLIN | select.POLLHUP | select.POLLERR)
    return bool(poller.poll(0))


def join_network_namespace_from_pidfd(pidfd: int) -> None:
    """Enter the validated master's network namespace without resolving a PID.

    Linux permits ``setns`` to receive a pidfd since kernel 5.8.  In that
    form the kernel binds the operation to the admitted process rather than a
    later lookup of its numeric PID, so a process exit or PID reuse cannot
    redirect the root-side client into another namespace.
    """
    if pidfd < 0:
        raise OSError("invalid master pidfd")
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        setns = libc.setns
    except AttributeError as exc:
        raise OSError("libc does not provide setns") from exc
    setns.argtypes = [ctypes.c_int, ctypes.c_int]
    setns.restype = ctypes.c_int
    clone_newnet = 0x40000000
    if setns(pidfd, clone_newnet) != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number))


def terminate_runtime_process(process: subprocess.Popen[bytes]) -> None:
    """Terminate and reap every descendant through the subreaper boundary."""
    handles: dict[int, ProcessHandle] = {}
    errors: list[str] = []
    deadline = time.monotonic() + 10.0
    empty_scans = 0
    try:
        while time.monotonic() < deadline:
            # The launcher is a child subreaper, so this finds both live
            # supervisor children and any descendants reparented after the
            # outer process exits. Repeating the capture closes a fork race.
            for handle in snapshot_supervisor_descendants(os.getpid()):
                if handle.pid in handles:
                    os.close(handle.pidfd)
                else:
                    handles[handle.pid] = handle
            if process.poll() is None:
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
                except BaseException as exc:
                    errors.append(f"supervisor: {exc}")
            for handle in handles.values():
                if not pidfd_exited(handle.pidfd):
                    try:
                        signal.pidfd_send_signal(handle.pidfd, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    except BaseException as exc:
                        errors.append(f"descendant {handle.pid}: {exc}")
            for handle in handles.values():
                if handle.pid == process.pid or not pidfd_exited(handle.pidfd):
                    continue
                try:
                    os.waitpid(handle.pid, os.WNOHANG)
                except ChildProcessError:
                    pass
                except OSError as exc:
                    errors.append(f"descendant {handle.pid} reap: {exc}")
            process.poll()
            current = snapshot_supervisor_descendants(os.getpid())
            for handle in current:
                if handle.pid in handles:
                    os.close(handle.pidfd)
                else:
                    handles[handle.pid] = handle
            if not current and all(pidfd_exited(handle.pidfd) for handle in handles.values()):
                empty_scans += 1
                if empty_scans >= 2:
                    if errors:
                        fail("runtime process cleanup failed: " + "; ".join(errors))
                    return
            else:
                empty_scans = 0
            time.sleep(POLL_INTERVAL)
        remaining = snapshot_supervisor_descendants(os.getpid())
        for handle in remaining:
            os.close(handle.pidfd)
        fail("runtime process cleanup left live supervisor descendants")
    finally:
        for handle in handles.values():
            os.close(handle.pidfd)


def dedicated_worker_process_ids(worker_uid: int) -> list[int]:
    pids: list[int] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        pid = int(entry.name)
        try:
            observed = status(pid)
        except LauncherError:
            continue
        if (observed["uid_real"], observed["uid_effective"]) == (worker_uid, worker_uid):
            pids.append(pid)
    return pids


def require_no_dedicated_worker_processes(worker_uid: int) -> None:
    """Refuse account cleanup when an unowned same-UID process survives.

    Runtime descendants are owned and terminated through the launcher's
    subreaper/PIDFD boundary.  A numeric UID alone never authorizes signalling
    another host process, because system-UID reuse can otherwise cross the
    runtime-cell boundary.
    """
    if dedicated_worker_process_ids(worker_uid):
        fail("dedicated worker identity still owns an unbound host process")


def host_pid_for_namespace_pid(namespace_pid: int, supervisor_pid: int) -> int:
    candidates: list[int] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        host_pid = int(entry.name)
        try:
            process_ids = namespace_process_ids(host_pid)
            descendant = is_descendant_of(host_pid, supervisor_pid)
        except LauncherError:
            # Processes can legitimately exit while /proc is enumerated.  A
            # live candidate must still be uniquely observable below.
            continue
        if process_ids[-1] == namespace_pid and descendant:
            candidates.append(host_pid)
    if len(candidates) != 1:
        fail("namespace PID does not resolve to one supervisor descendant")
    return candidates[0]


def namespace_link(pid: int, namespace: str) -> str:
    try:
        return os.readlink(f"/proc/{pid}/ns/{namespace}")
    except OSError as exc:
        fail(f"unable to read {namespace} namespace evidence: {exc}")


def require_sandbox_security_state(pid: int) -> None:
    fields: dict[str, str] = {}
    for line in proc_status_text(pid).splitlines():
        key, _, value = line.partition(":")
        if key in {"NoNewPrivs", "CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb"}:
            fields[key] = value.strip()
    if fields.get("NoNewPrivs") != "1":
        fail("master did not retain no-new-privileges")
    allowed = (1 << 0) | (1 << 6) | (1 << 7)
    for field in ("CapInh", "CapAmb"):
        try:
            value = int(fields[field], 16)
        except (KeyError, ValueError) as exc:
            fail(f"invalid {field} kernel evidence: {exc}")
        if value != 0:
            fail(f"master retained unexpected {field} capabilities")
    for field in ("CapPrm", "CapEff", "CapBnd"):
        try:
            value = int(fields[field], 16)
        except (KeyError, ValueError) as exc:
            fail(f"invalid {field} kernel evidence: {exc}")
        if value & ~allowed:
            fail(f"master retained a capability outside the runtime minimum: {field}")


def validate_identity(ready: dict[str, object], expected: IdentityExpectations,
                      binary_identity: dict[str, int | str],
                      supervisor_pid: int) -> dict[str, int]:
    try:
        master_namespace_pid = int(ready["master_pid"])
        worker_namespace_pid = int(ready["worker_pid"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"supervisor readiness lacks PIDs: {exc}")
    if (master_namespace_pid <= 1 or worker_namespace_pid <= 1
            or master_namespace_pid == worker_namespace_pid):
        fail("invalid distinct master/worker PIDs")
    master = host_pid_for_namespace_pid(master_namespace_pid, supervisor_pid)
    worker = host_pid_for_namespace_pid(worker_namespace_pid, supervisor_pid)
    m, w = status(master), status(worker)
    if w["ppid"] != master:
        fail("worker is not a direct child of master")
    if (m["uid_real"], m["uid_effective"], m["gid_real"], m["gid_effective"]) != (expected.runner_uid, expected.runner_uid, expected.runner_gid, expected.runner_gid):
        fail("master identity is not the namespace-root identity")
    if (w["uid_real"], w["uid_effective"]) != (expected.worker_uid, expected.worker_uid) or (w["gid_real"], w["gid_effective"]) != (expected.worker_gid, expected.worker_gid):
        fail("worker identity does not match the dedicated account")
    master_stat = os.stat(f"/proc/{master}/exe")
    try:
        admitted_binary = (int(binary_identity["device"]), int(binary_identity["inode"]))
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"admitted NGINX artifact identity is invalid: {exc}")
    if (master_stat.st_dev, master_stat.st_ino) != admitted_binary:
        fail("master executable does not match admitted NGINX artifact")
    for namespace in ("user", "mnt", "pid", "net", "ipc", "uts"):
        if namespace_link(master, namespace) == namespace_link(os.getpid(), namespace):
            fail(f"master did not enter an isolated {namespace} namespace")
    if not apparmor_label(master).startswith(APPARMOR_PROFILE_NAME + " "):
        fail("master did not retain the approved AppArmor profile")
    require_sandbox_security_state(master)
    master_pidfd = -1
    try:
        master_pidfd = os.pidfd_open(master)
        if pidfd_exited(master_pidfd):
            fail("validated master exited before pidfd admission completed")
    except (AttributeError, OSError) as exc:
        fail(f"could not admit a stable master pidfd: {exc}")
    except BaseException:
        if master_pidfd >= 0:
            os.close(master_pidfd)
        raise
    return {
        "master_pid": master,
        "master_pidfd": master_pidfd,
        "worker_pid": worker,
        "master_namespace_pid": master_namespace_pid,
        "worker_namespace_pid": worker_namespace_pid,
        "master_uid": m["uid_real"],
        "master_gid": m["gid_real"],
        "worker_uid": expected.worker_uid,
        "worker_gid": expected.worker_gid,
    }


def _control_file_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_nlink,
        metadata.st_uid,
        metadata.st_gid,
        stat.S_IMODE(metadata.st_mode),
    )


def _open_control_parent(path: Path) -> tuple[int, str]:
    """Bind a control-file parent before accepting its fixed leaf name."""
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        fail("root control file path must be absolute and normalized")
    path = Path(os.path.normpath(os.fspath(path)))
    if path.name in {"", ".", ".."}:
        fail("root control file path has no fixed leaf")
    parent = path.parent
    descriptor = -1
    try:
        descriptor = os.open(
            parent.root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
        )
        for component in parent.parts[1:]:
            before = os.stat(component, dir_fd=descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode) or stat.S_ISLNK(before.st_mode):
                fail("root control file parent has an unsafe component")
            child = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=descriptor,
            )
            opened = os.fstat(child)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                os.close(child)
                fail("root control file parent changed while opening")
            os.close(descriptor)
            descriptor = child
        result = descriptor
        descriptor = -1
        return result, path.name
    except OSError as exc:
        fail(f"could not open root control file parent: {exc}")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _require_root_control_file(metadata: os.stat_result) -> None:
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
        or metadata.st_uid != os.geteuid()
        or metadata.st_gid != os.getegid()
        or stat.S_IMODE(metadata.st_mode) != 0o400
    ):
        fail("root control file metadata is unsafe")


def _require_root_control_directory(path: Path) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        fail(f"root control directory is unavailable: {exc}")
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.geteuid()
        or metadata.st_gid != os.getegid()
        or stat.S_IMODE(metadata.st_mode) != 0o755
    ):
        fail("root control directory metadata is unsafe")


def atomic_json(path: Path, value: dict[str, object]) -> None:
    """Publish one root control file without following candidate path swaps."""
    parent_descriptor, name = _open_control_parent(path)
    temporary_name = f".{name}.tmp-{os.getpid()}"
    descriptor = -1
    published_descriptor = -1
    published = False
    success = False
    try:
        try:
            os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            fail("supervisor control file already exists")
        descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent_descriptor,
        )
        raw = (
            json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("ascii")
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                fail("could not write complete root control file")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o400)
        expected = os.fstat(descriptor)
        _require_root_control_file(expected)
        expected_identity = _control_file_identity(expected)
        os.close(descriptor)
        descriptor = -1
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        published = True
        os.fsync(parent_descriptor)
        published_descriptor = os.open(
            name,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
            dir_fd=parent_descriptor,
        )
        observed = os.fstat(published_descriptor)
        _require_root_control_file(observed)
        if _control_file_identity(observed) != expected_identity:
            fail("root control file changed while publishing")
        success = True
    except OSError as exc:
        fail(f"could not publish root control file: {exc}")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if published_descriptor >= 0:
            os.close(published_descriptor)
        if not success:
            for candidate_name in (
                temporary_name,
                name if published else None,
            ):
                if candidate_name is None:
                    continue
                try:
                    os.unlink(candidate_name, dir_fd=parent_descriptor)
                except FileNotFoundError:
                    pass
                except OSError:
                    pass
        os.close(parent_descriptor)


def root_owned_directory(path: Path, mode: int = 0o755) -> None:
    """Create one fresh non-writable-to-candidate runtime directory."""
    try:
        path.mkdir(mode=mode)
        os.chown(path, 0, 0)
        os.chmod(path, mode)
        metadata = path.lstat()
    except OSError as exc:
        fail(f"could not create root-owned runtime directory: {exc}")
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != 0
        or metadata.st_gid != 0
        or stat.S_IMODE(metadata.st_mode) != mode
    ):
        fail("root-owned runtime directory metadata is unsafe")


def root_owned_file(path: Path, content: bytes, mode: int = 0o444) -> None:
    """Create one fixed Base configuration or rule file."""
    descriptor = -1
    try:
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
            mode,
        )
        offset = 0
        while offset < len(content):
            written = os.write(descriptor, content[offset:])
            if written <= 0:
                fail("could not write complete root-owned runtime file")
            offset += written
        os.fsync(descriptor)
        os.fchown(descriptor, 0, 0)
        os.fchmod(descriptor, mode)
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or metadata.st_uid != 0
            or metadata.st_gid != 0
            or stat.S_IMODE(metadata.st_mode) != mode
        ):
            fail("root-owned runtime file metadata is unsafe")
    except OSError as exc:
        fail(f"could not create root-owned runtime file: {exc}")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def nginx_literal(value: Path | str, label: str) -> str:
    """Quote a Base-selected NGINX value without allowing a new directive."""
    raw = os.fspath(value)
    if (
        not raw
        or any(
            character == "\\"
            or ord(character) < 0x20
            or character in {'"', "'", ";", "{", "}", "#", "$"}
            for character in raw
        )
    ):
        fail(f"{label} cannot be represented safely in fixed NGINX configuration")
    return f'"{raw}"'


def prepare_trusted_cells(
    cell: Path,
    module: Path,
    worker_name: str,
    worker_group: str,
    runner_uid: int,
    runner_gid: int,
) -> None:
    """Construct immutable Base-owned config/rule inputs for both fresh cells.

    The candidate namespace can write only runtime and log subdirectories.
    Its NGINX process has no write permission to the parent cell, the
    configuration directory, the root-controlled synchronization directory,
    the rule file, or the document root. There are intentionally no NGINX
    include directives in this cell.
    """
    if not re.fullmatch(r"mscnxw_[0-9a-f]+", worker_name) or not re.fullmatch(
        r"mscnxg_[0-9a-f]+", worker_group
    ):
        fail("dedicated worker identity is not a launcher-generated value")
    nginx_literal(cell, "runtime cell path")
    module_literal = nginx_literal(module, "admitted module path")
    for mode in ("on", "off"):
        mode_root = cell / mode
        config_root = mode_root / "config"
        control_root = mode_root / "control"
        runtime_root = mode_root / "runtime"
        logs_root = mode_root / "logs"
        docroot = config_root / "docroot"
        root_owned_directory(mode_root)
        root_owned_directory(config_root)
        root_owned_directory(docroot)
        root_owned_directory(control_root, 0o755)
        create_runner_owned_directory(runtime_root, runner_uid, runner_gid)
        create_runner_owned_directory(logs_root, runner_uid, runner_gid)
        root_owned_file(docroot / "index.html", b"exact-head-ok\n")
        rules = (
            "SecRuleEngine On\n"
            'SecRule REQUEST_URI "@streq /exact-head" '
            '"id:1000001,phase:1,deny,status:403,log"\n'
        ).encode("utf-8")
        root_owned_file(config_root / "modsecurity.conf", rules)
        config = (
            f"load_module {module_literal};\n"
            "daemon off;\n"
            "worker_processes 1;\n"
            f"user {worker_name} {worker_group};\n"
            f"pid {nginx_literal(runtime_root / 'nginx.pid', 'PID path')};\n"
            f"error_log {nginx_literal(logs_root / 'error.log', 'error-log path')} notice;\n"
            "events { worker_connections 32; }\n"
            "http {\n"
            f"access_log {nginx_literal(logs_root / 'access.log', 'access-log path')};\n"
            "server {\n"
            "listen 127.0.0.1:18081;\n"
            "server_name exact-head.local;\n"
            "modsecurity on;\n"
            f"modsecurity_use_error_log {mode};\n"
            f"modsecurity_rules_file {nginx_literal(config_root / 'modsecurity.conf', 'rule path')};\n"
            f"modsecurity_phase4_log {nginx_literal(logs_root / 'events.jsonl', 'Phase-4 path')};\n"
            'modsecurity_transaction_id "nginx-exact-head-$pid-$connection-$connection_requests";\n'
            "location / {\n"
            f"root {nginx_literal(docroot, 'document-root path')};\n"
            "return 200 exact-head-ok;\n"
            "}\n"
            "}\n"
            "}\n"
        ).encode("utf-8")
        root_owned_file(config_root / "nginx.conf", config)


def require_root_owned_file(path: Path, mode: int, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        fail(f"{label} is unavailable: {exc}")
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
        or metadata.st_uid != 0
        or metadata.st_gid != 0
        or stat.S_IMODE(metadata.st_mode) != mode
    ):
        fail(f"{label} is not an immutable root-owned file")


def require_root_owned_directory(path: Path, mode: int, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        fail(f"{label} is unavailable: {exc}")
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != 0
        or metadata.st_gid != 0
        or stat.S_IMODE(metadata.st_mode) != mode
    ):
        fail(f"{label} is not an immutable root-owned directory")


def nginx_statements(text: str, label: str) -> list[str]:
    """Lex complete NGINX statements without confusing quoted semicolons."""
    statements: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False
    comment = False
    nesting = 0
    for character in text:
        if comment:
            if character == "\n":
                comment = False
            continue
        if quote is not None:
            current.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
            current.append(character)
        elif character == "#":
            comment = True
        elif character in {";", "{"}:
            statement = "".join(current).strip()
            if not statement:
                fail(f"{label} contains an empty NGINX statement")
            statements.append(statement + character)
            current.clear()
            if character == "{":
                nesting += 1
        elif character == "}":
            if "".join(current).strip():
                fail(f"{label} has an unterminated directive before a block close")
            if nesting <= 0:
                fail(f"{label} has an unmatched NGINX block close")
            statements.append("}")
            nesting -= 1
        else:
            current.append(character)
    if quote is not None:
        fail(f"{label} has an unterminated quoted value")
    if "".join(current).strip():
        fail(f"{label} has an unterminated NGINX statement")
    if nesting:
        fail(f"{label} has an unterminated NGINX block")
    return statements


def nginx_directive(statement: str) -> str:
    """Return one already-lexed directive or block keyword."""
    if statement == "}":
        return statement
    content = statement[:-1].strip()
    if not content:
        fail("empty NGINX statement has no directive")
    return content.split(None, 1)[0]


def validate_generated_config(
    ready: dict[str, object],
    cell: Path,
    mode: str,
    binary: Path,
    module: Path,
    worker_name: str,
    worker_group: str,
) -> None:
    raw_path = ready.get("config_path")
    raw_pid_path = ready.get("pid_path")
    if (type(ready.get("schema_version")) is not int
            or ready["schema_version"] != 1 or not isinstance(raw_path, str)
            or not isinstance(raw_pid_path, str)
            or ready.get("binary_path") != str(binary)):
        fail("supervisor readiness does not bind the admitted configuration")
    mode_root = cell / mode
    config_root = mode_root / "config"
    runtime_root = mode_root / "runtime"
    logs_root = mode_root / "logs"
    expected_config = config_root / "nginx.conf"
    expected_rules = config_root / "modsecurity.conf"
    expected_docroot = config_root / "docroot"
    config = contained(Path(raw_path), mode_root, "generated NGINX configuration")
    if config != expected_config:
        fail("supervisor readiness does not name the fixed root-owned configuration")
    text = bounded_file(config, MAX_GENERATED_CONFIG_BYTES).decode("utf-8")
    pid_path = contained(Path(raw_pid_path), mode_root, "generated NGINX PID file")
    if pid_path != runtime_root / "nginx.pid":
        fail("supervisor readiness does not name the fixed runtime PID path")
    require_root_owned_directory(mode_root, 0o755, "mode root")
    require_root_owned_directory(config_root, 0o755, "configuration root")
    require_root_owned_directory(expected_docroot, 0o755, "document root")
    require_root_owned_file(config, 0o444, "NGINX configuration")
    require_root_owned_file(expected_rules, 0o444, "ModSecurity rule file")
    require_root_owned_file(expected_docroot / "index.html", 0o444, "document")
    if bounded_file(expected_rules, 4096) != (
        b"SecRuleEngine On\n"
        b'SecRule REQUEST_URI "@streq /exact-head" '
        b'"id:1000001,phase:1,deny,status:403,log"\n'
    ):
        fail("root-owned ModSecurity rule file does not match the fixed cell")
    try:
        expected_namespace_pid = str(int(ready["master_pid"]))
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"supervisor readiness lacks the master namespace PID: {exc}")
    if bounded_file(pid_path, 128).decode("ascii").strip() != expected_namespace_pid:
        fail("generated NGINX PID file is not bound to the readiness master")
    statements = nginx_statements(text, "generated NGINX configuration")
    expected = {
        "load_module": f'load_module "{module}";',
        "user": f"user {worker_name} {worker_group};",
        "modsecurity_use_error_log": f"modsecurity_use_error_log {mode};",
        "daemon": "daemon off;",
        "worker_processes": "worker_processes 1;",
        "pid": f'pid "{pid_path}";',
        "error_log": f'error_log "{logs_root / "error.log"}" notice;',
        "access_log": f'access_log "{logs_root / "access.log"}";',
        "server_name": "server_name exact-head.local;",
        "modsecurity": "modsecurity on;",
        "modsecurity_rules_file": f'modsecurity_rules_file "{expected_rules}";',
        "modsecurity_phase4_log": f'modsecurity_phase4_log "{logs_root / "events.jsonl"}";',
        "modsecurity_transaction_id": (
            'modsecurity_transaction_id '
            '"nginx-exact-head-$pid-$connection-$connection_requests";'
        ),
        "root": f'root "{expected_docroot}";',
        "return": "return 200 exact-head-ok;",
    }
    forbidden_anywhere = {
        "env", "master_process", "stream", "mail", "proxy_pass",
        "fastcgi_pass", "uwsgi_pass", "scgi_pass", "resolver",
        "ssl_certificate_key", "include",
    }
    for statement in statements:
        directive = nginx_directive(statement)
        if directive in forbidden_anywhere:
            fail("generated NGINX configuration has an unsafe runtime directive")
    # The protected exact-head cell deliberately has no NGINX include
    # boundary at all.  Rejecting every include is stronger than admitting a
    # candidate-selected nested, absolute, or escaping include path.
    effective_lines = statements
    for directive, required in expected.items():
        matched = [line for line in effective_lines if nginx_directive(line) == directive]
        if matched != [required]:
            fail("generated NGINX configuration does not match the fixed runtime cell")
    listens = [line for line in effective_lines if nginx_directive(line) == "listen"]
    if len(listens) != 1 or not re.fullmatch(r"listen 127\.0\.0\.1:[0-9]+;", listens[0]):
        fail("generated NGINX configuration does not bind exactly one loopback listener")
    if any(nginx_directive(line) == "env" for line in effective_lines):
        fail("generated NGINX configuration does not match the fixed runtime cell")


def wait_mode(
    cell: Path,
    mode: str,
    expected: IdentityExpectations,
    binary: Path,
    binary_identity: dict[str, int | str],
    module: Path,
    worker_name: str,
    worker_group: str,
    supervisor: subprocess.Popen[bytes],
) -> dict[str, object]:
    mode_dir = contained(cell / mode, cell, "supervisor control directory")
    control_dir = contained(
        mode_dir / "control", mode_dir, "supervisor root control directory"
    )
    _require_root_control_directory(control_dir)
    runtime_dir = contained(mode_dir / "runtime", mode_dir, "supervisor runtime directory")
    ready_path = runtime_dir / "ready.json"
    release_path = control_dir / "release"
    completion_path = control_dir / "request-complete.json"
    if (
        release_path.exists()
        or release_path.is_symlink()
        or completion_path.exists()
        or completion_path.is_symlink()
    ):
        fail("supervisor control file was not fresh")
    deadline = time.monotonic() + SUPERVISOR_TIMEOUT
    while time.monotonic() < deadline:
        if supervisor.poll() is not None:
            fail(f"exact-head NGINX harness exited before {mode} readiness")
        contained(mode_dir, cell, "supervisor control directory")
        contained(control_dir, mode_dir, "supervisor root control directory")
        if ready_path.is_symlink():
            fail("supervisor readiness record is a symbolic link")
        if ready_path.exists():
            try:
                ready = json.loads(bounded_file(ready_path, MAX_READY_BYTES))
            except json.JSONDecodeError as exc:
                fail(f"supervisor readiness is not valid JSON: {exc}")
            if not isinstance(ready, dict) or ready.get("mode") != mode:
                fail("invalid supervisor readiness record")
            validate_generated_config(
                ready, cell, mode, binary, module, worker_name, worker_group
            )
            identity = validate_identity(ready, expected, binary_identity, supervisor.pid)
            try:
                atomic_json(release_path, {"mode": mode, "allow": True})
            except BaseException:
                close_identity_pidfd(identity)
                raise
            return {"mode": mode, **identity}
        time.sleep(POLL_INTERVAL)
    fail(f"supervisor readiness timeout for {mode}")


def close_identity_pidfd(identity: dict[str, object]) -> None:
    """Close and remove the internal master handle before evidence publication."""
    descriptor = identity.pop("master_pidfd", None)
    if type(descriptor) is not int or descriptor < 0:
        fail("validated identity lacks a safe master pidfd")
    try:
        os.close(descriptor)
    except OSError as exc:
        fail(f"could not close validated master pidfd: {exc}")


def trusted_http_status(master_pidfd: int) -> int:
    """Make the only HTTP request through a fixed host-side client.

    The client enters the verified NGINX network namespace through its retained
    pidfd, never by resolving a numeric PID. Its output is retained in root
    memory rather than written into candidate-writable scratch, so a candidate
    cannot manufacture the 403 status evidence or redirect the client through
    PID reuse.
    """
    if master_pidfd < 0:
        fail("trusted HTTP client has no valid master pidfd")
    if pidfd_exited(master_pidfd):
        fail("validated master exited before the trusted HTTP request")
    env = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "LANG": "C", "LC_ALL": "C"}
    try:
        result = run_checked(
            [
                HELPERS["curl"],
                "--noproxy",
                "*",
                "--silent",
                "--show-error",
                "--max-time",
                "5",
                "--output",
                "/dev/null",
                "--write-out",
                "%{http_code}",
                "http://127.0.0.1:18081/exact-head",
            ],
            env=env,
            timeout=15,
            pass_fds=(master_pidfd,),
            preexec_fn=functools.partial(
                join_network_namespace_from_pidfd, master_pidfd
            ),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"trusted HTTP client failed: {exc}")
    if pidfd_exited(master_pidfd):
        fail("validated master exited during the trusted HTTP request")
    if result.stdout.strip() != "403":
        fail("trusted HTTP client did not observe the expected 403 response")
    return 403


def mark_request_complete(cell: Path, mode: str, status_code: int) -> None:
    """Release the Base helper only after the root-side HTTP observation."""
    if status_code != 403:
        fail("root-side HTTP observation cannot release a non-403 cell")
    mode_root = contained(cell / mode, cell, "root request-completion mode root")
    control_root = contained(
        mode_root / "control", mode_root, "root request-completion control root"
    )
    _require_root_control_directory(control_root)
    path = control_root / "request-complete.json"
    atomic_json(path, {"mode": mode, "http_status": status_code})


def mode_evidence(cell: Path, mode: str, status_code: int) -> dict[str, object]:
    """Derive one bounded cell decision from raw scratch evidence.

    The scratch directory is writable to the candidate namespace and is never
    uploaded or handed directly to the collector.  This routine reads fixed
    filenames only after the helper exits, rejects control-text injection and
    returns just the minimal facts that the root launcher publishes anew.  The
    callback and JSONL values remain explicitly labelled untrusted sandbox
    observations: schema/correlation checks cannot authenticate semantics
    emitted by the candidate process.
    """
    mode_root = cell / mode
    phase4 = contained(
        mode_root / "logs" / "events.jsonl", mode_root, "Phase-4 evidence"
    )
    error_log = contained(
        mode_root / "logs" / "error.log",
        mode_root,
        "native error-log evidence",
    )
    events: list[str] = []
    for line in bounded_file(phase4, MAX_RUNTIME_LOG_BYTES).decode("utf-8").splitlines():
        if "\x1b" in line or "::" in line:
            fail(f"{mode} Phase-4 evidence contains terminal or workflow control text")
        if FORBIDDEN_MARKERS.search(line):
            fail(f"{mode} Phase-4 evidence contains a forbidden marker")
        try:
            record = json.loads(line, object_pairs_hook=duplicate_safe)
        except json.JSONDecodeError as exc:
            fail(f"{mode} Phase-4 evidence is not JSONL: {exc}")
        if isinstance(record, dict):
            if (
                record.get("event") == "request_rule_match"
                and record.get("connector") == "nginx"
                and record.get("integration_mode") == "native-nginx-http-module"
                and record.get("rule_id") == "1000001"
            ):
                transaction_id = record.get("transaction_id")
                if not isinstance(transaction_id, str) or not TX_RE.fullmatch(transaction_id):
                    fail(f"{mode} event has an invalid deterministic transaction id")
                integrity = [
                    record.get(field)
                    for field in ("sequence", "previous_event_hash", "event_hash")
                ]
                if not all(type(value) is int and value >= 0 for value in integrity):
                    fail(f"{mode} event has invalid integrity representation")
                events.append(transaction_id)
    if status_code != 403:
        fail(f"{mode} trusted HTTP status was not 403")
    error = bounded_file(error_log, MAX_RUNTIME_LOG_BYTES).decode("utf-8")
    if FORBIDDEN_MARKERS.search(error):
        fail(f"{mode} native error-log evidence contains a forbidden marker")
    if len(events) != 1:
        fail(f"{mode} mode lacks exactly one correlated JSONL rule-match event")
    callback_transactions: list[str] = []
    for line in error.splitlines():
        if "\x1b" in line or "::" in line:
            fail(f"{mode} native error-log evidence contains terminal or workflow control text")
        if not RULE_1000001_RE.search(line):
            continue
        callback = CALLBACK_TX_RE.search(line)
        if callback is None:
            fail(f"{mode} native rule callback lacks an exact transaction id")
        callback_transactions.append(callback.group(1))
    if mode == "on":
        if callback_transactions != [events[0]]:
            fail("on mode lacks exactly one correlated native callback")
    elif callback_transactions or RULE_1000001_RE.search(error) or CALLBACK_TX_RE.search(error):
        fail("off mode contains native callback evidence")
    else:
        return {
            "callback_observed": False,
            "callback_observation_source": "candidate_scratch_untrusted",
            "http_status_observation_source": "root_pidfd_network_namespace",
            "mode": mode,
            "http_status": status_code,
            "jsonl_observed": True,
            "jsonl_observation_source": "candidate_scratch_untrusted",
            "waf_decision": "deny",
            "transaction_id": events[0],
        }
    return {
        "callback_observed": True,
        "callback_observation_source": "candidate_scratch_untrusted",
        "http_status_observation_source": "root_pidfd_network_namespace",
        "mode": mode,
        "http_status": status_code,
        "jsonl_observed": True,
        "jsonl_observation_source": "candidate_scratch_untrusted",
        "waf_decision": "deny",
        "transaction_id": events[0],
    }


def write_root_owned_json(path: Path, value: dict[str, Any], *, line_delimited: bool = False) -> None:
    """Atomically publish Base-derived data without copying raw candidate text."""
    if path.exists() or path.is_symlink():
        fail("root evidence destination is not fresh")
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if line_delimited:
        raw += b"\n"
    temporary = path.with_name("." + path.name + ".tmp")
    descriptor = -1
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
        )
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                fail("could not write complete root evidence")
            offset += written
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary, path)
        os.chmod(path, 0o600)
        final = path.lstat()
        if (
            stat.S_ISLNK(final.st_mode)
            or not stat.S_ISREG(final.st_mode)
            or final.st_nlink != 1
            or final.st_uid != 0
            or final.st_gid != 0
            or stat.S_IMODE(final.st_mode) != 0o600
        ):
            fail("published root evidence metadata is unsafe")
    except OSError as exc:
        fail(f"could not publish root evidence: {exc}")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            if temporary.exists() or temporary.is_symlink():
                temporary.unlink()
        except OSError:
            pass


def publish_evidence(
    evidence_root: Path,
    dispatcher: dict[str, Any],
    expected: IdentityExpectations,
    identities: list[dict[str, object]],
    artifacts: dict[str, dict[str, int | str]],
    modes: list[dict[str, object]],
) -> None:
    """Publish the exact fixed collector allowlist after the namespace drains."""
    metadata = evidence_root.lstat()
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != 0
        or metadata.st_gid != 0
        or stat.S_IMODE(metadata.st_mode) != 0o700
        or any(evidence_root.iterdir())
    ):
        fail("root evidence directory is not a fresh private root-owned directory")
    indexed_identity = {str(item["mode"]): item for item in identities}
    indexed_mode = {str(item["mode"]): item for item in modes}
    if set(indexed_identity) != {"on", "off"} or set(indexed_mode) != {"on", "off"}:
        fail("exact-head run does not contain both validated cells")
    for mode in ("on", "off"):
        if indexed_identity[mode]["master_pid"] == indexed_identity[mode]["worker_pid"]:
            fail("root identity evidence does not contain distinct processes")
        if indexed_mode[mode]["http_status"] != 403 or indexed_mode[mode]["waf_decision"] != "deny":
            fail("root mode evidence does not contain the expected WAF decision")
    on_identity = indexed_identity["on"]
    identity = {
        "schema_version": 1,
        "runner_uid": expected.runner_uid,
        "runner_gid": expected.runner_gid,
        "expected_worker_uid": expected.worker_uid,
        "expected_worker_gid": expected.worker_gid,
        "on": {
            "master_pid": on_identity["master_pid"],
            "worker_pid": on_identity["worker_pid"],
            "master_uid": on_identity["master_uid"],
            "master_gid": on_identity["master_gid"],
            "worker_uid": on_identity["worker_uid"],
            "worker_gid": on_identity["worker_gid"],
        },
        "off": {
            "master_pid": indexed_identity["off"]["master_pid"],
            "worker_pid": indexed_identity["off"]["worker_pid"],
            "master_uid": indexed_identity["off"]["master_uid"],
            "master_gid": indexed_identity["off"]["master_gid"],
            "worker_uid": indexed_identity["off"]["worker_uid"],
            "worker_gid": indexed_identity["off"]["worker_gid"],
        },
    }
    runtime = {
        "schema_version": 1,
        "tested_pr_head": dispatcher["tested_pr_head"],
        "trusted_dispatcher_base_sha": dispatcher["trusted_dispatcher_base_sha"],
        "candidate_run_id": dispatcher["run_id"],
        "nginx_version": EXPECTED_NGINX_VERSION,
        "nginx_source_digest": EXPECTED_NGINX_SOURCE_DIGEST,
        "connector_module_digest": artifacts["module"]["sha256"],
    }
    exit_status = {"schema_version": 1, "on_exit": 0, "off_exit": 0}
    for name, value, jsonl in (
        ("identity.json", identity, False),
        ("runtime.json", runtime, False),
        ("on.jsonl", indexed_mode["on"], True),
        ("off.jsonl", indexed_mode["off"], True),
        ("exit.json", exit_status, False),
    ):
        write_root_owned_json(evidence_root / name, value, line_delimited=jsonl)
    if {entry.name for entry in evidence_root.iterdir()} != ROOT_EVIDENCE_FILES:
        fail("root evidence allowlist publication is incomplete")


def create_identity(suffix: str) -> tuple[str, str]:
    name = "mscnxw_" + suffix
    group = "mscnxg_" + suffix
    if name in {entry.pw_name for entry in pwd.getpwall()} or group in {entry.gr_name for entry in grp.getgrall()}:
        fail("dedicated NGINX identity already exists")
    run_checked([HELPERS["groupadd"], "--system", group], capture=False)
    try:
        run_checked([HELPERS["useradd"], "--system", "--no-create-home", "--shell", "/usr/sbin/nologin", "--gid", group, name], capture=False)
    except BaseException as primary:
        try:
            run_checked([HELPERS["groupdel"], group], capture=False)
        except BaseException as cleanup:
            fail(f"dedicated user creation failed: {primary}; group rollback failed: {cleanup}")
        raise
    return name, group


def cleanup_identity(name: str, group: str) -> None:
    errors: list[str] = []
    for label, command in (
        ("user", [HELPERS["userdel"], name]),
        ("group", [HELPERS["groupdel"], group]),
    ):
        try:
            run_checked(command, capture=False)
        except BaseException as exc:
            errors.append(f"{label}: {exc}")
    if errors:
        fail("dedicated identity cleanup failed: " + "; ".join(errors))


def subordinate_entries(path: Path, runner_name: str, runner_uid: int) -> list[tuple[str, int, int]]:
    st = path.lstat()
    if (stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode) or st.st_uid != 0
            or st.st_mode & 0o022):
        fail(f"unsafe subordinate identity file: {path.name}")
    entries: list[tuple[str, int, int]] = []
    for line in bounded_file(path, MAX_SNAPSHOT_BYTES).decode("ascii").splitlines():
        if not line:
            continue
        fields = line.split(":")
        if len(fields) != 3:
            fail(f"malformed subordinate identity record: {path.name}")
        principal, start, size = fields
        if principal not in {runner_name, str(runner_uid)}:
            continue
        if not start.isdecimal() or not size.isdecimal():
            fail(f"malformed runner subordinate identity record: {path.name}")
        entries.append((principal, int(start), int(size)))
    return entries


def require_no_subordinate_mapping(runner_name: str, runner_uid: int) -> None:
    for path in (Path("/etc/subuid"), Path("/etc/subgid")):
        if subordinate_entries(path, runner_name, runner_uid):
            fail("runner already has a subordinate identity delegation")


def require_exact_subordinate_mapping(mapping: SubordinateMapping) -> None:
    expected = {
        Path("/etc/subuid"): (mapping.worker_uid, 1),
        Path("/etc/subgid"): (mapping.worker_gid, 1),
    }
    for path, expected_entry in expected.items():
        entries = subordinate_entries(path, mapping.runner_name, mapping.runner_uid)
        if entries != [(mapping.runner_name, *expected_entry)]:
            fail("runner subordinate identity delegation is not exact")


def cleanup_subordinate_mapping(mapping: SubordinateMapping) -> None:
    errors: list[str] = []
    if mapping.gid_added:
        try:
            run_checked(
                [HELPERS["usermod"], "--del-subgids",
                 f"{mapping.worker_gid}-{mapping.worker_gid}", mapping.runner_name],
                capture=False,
            )
            mapping.gid_added = False
        except BaseException as exc:
            errors.append(f"gid mapping: {exc}")
    if mapping.uid_added:
        try:
            run_checked(
                [HELPERS["usermod"], "--del-subuids",
                 f"{mapping.worker_uid}-{mapping.worker_uid}", mapping.runner_name],
                capture=False,
            )
            mapping.uid_added = False
        except BaseException as exc:
            errors.append(f"uid mapping: {exc}")
    try:
        require_no_subordinate_mapping(mapping.runner_name, mapping.runner_uid)
    except BaseException as exc:
        errors.append(f"mapping state: {exc}")
    if errors:
        fail("subordinate mapping cleanup failed: " + "; ".join(errors))


def establish_subordinate_mapping(mapping: SubordinateMapping) -> None:
    require_no_subordinate_mapping(mapping.runner_name, mapping.runner_uid)
    try:
        run_checked(
            [HELPERS["usermod"], "--add-subuids",
             f"{mapping.worker_uid}-{mapping.worker_uid}", mapping.runner_name],
            capture=False,
        )
        mapping.uid_added = True
        run_checked(
            [HELPERS["usermod"], "--add-subgids",
             f"{mapping.worker_gid}-{mapping.worker_gid}", mapping.runner_name],
            capture=False,
        )
        mapping.gid_added = True
        require_exact_subordinate_mapping(mapping)
    except BaseException as primary:
        try:
            cleanup_subordinate_mapping(mapping)
        except BaseException as rollback:
            fail(f"subordinate mapping setup failed: {primary}; rollback failed: {rollback}")
        raise


def admit_candidate_bundle(
    root: Path, manifest: dict[str, Any]
) -> tuple[dict[str, dict[str, int | str]], dict[str, int]]:
    """Open exactly the fixed candidate payload and retain descriptors.

    The artifact directory is untrusted.  Its pathname is used only to open
    one fixed allowlist before namespace entry; the descriptors, rather than
    the pathnames, are then bound into bubblewrap.
    """
    root = no_symlink_path(root, "candidate artifact root")
    if not root.is_dir():
        fail("candidate artifact root is not a directory")
    fixed = {
        "nginx": "nginx",
        "module": "ngx_http_modsecurity_module.so",
        "library": "libmodsecurity.so.3",
    }
    expected_entries = set(fixed.values()) | {"artifact-manifest.json"}
    if {entry.name for entry in root.iterdir()} != expected_entries:
        fail("candidate artifact root does not contain exactly the approved payload")
    identities: dict[str, dict[str, int | str]] = {}
    descriptors: dict[str, int] = {}
    try:
        for key, filename in fixed.items():
            descriptor, identity = admitted_artifact_descriptor(
                contained(root / filename, root, f"candidate {key} artifact"),
                f"candidate {key} artifact",
            )
            identities[key] = identity
            descriptors[key] = descriptor
        validate_admitted_artifacts(manifest, identities)
        descriptor = open_regular_no_follow(
            contained(root / "artifact-manifest.json", root, "candidate artifact manifest"),
            "candidate artifact manifest",
        )
        descriptors["manifest"] = descriptor
        return identities, descriptors
    except BaseException:
        for descriptor in descriptors.values():
            os.close(descriptor)
        raise


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trusted-dispatcher-base-sha", required=True)
    parser.add_argument("--base-repo-root", required=True)
    parser.add_argument("--dispatcher-manifest", required=True)
    parser.add_argument("--candidate-manifest", required=True)
    parser.add_argument("--candidate-artifact-root", required=True)
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--runner-uid", required=True, type=int)
    parser.add_argument("--runner-gid", required=True, type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    primary: BaseException | None = None
    identity: tuple[str, str] | None = None
    mapping: SubordinateMapping | None = None
    worker_uid: int | None = None
    scratch_root: Path | None = None
    cell: Path | None = None
    evidence_root: Path | None = None
    process: subprocess.Popen[bytes] | None = None
    artifact_descriptors: dict[str, int] = {}
    trusted_base_descriptors: dict[str, int] = {}
    evidence_published = False
    try:
        if os.geteuid() != 0:
            fail("root launcher requires euid 0")
        args = parse_args(argv or sys.argv[1:])
        trusted_base_sha = require_sha40(
            args.trusted_dispatcher_base_sha, "trusted dispatcher Base SHA"
        )
        if args.runner_uid <= 0 or args.runner_gid <= 0:
            fail("runner identity must be nonroot")
        repo = no_symlink_path(Path(args.base_repo_root), "trusted Base repository root")
        if not repo.is_dir():
            fail("trusted Base repository root is not a directory")
        verify_runner_owned_directory(repo, args.runner_uid, args.runner_gid, "trusted Base repository root")
        raw_evidence = Path(args.evidence_root)
        if not raw_evidence.is_absolute() or any(part in {".", ".."} for part in raw_evidence.parts):
            fail("root evidence path must be an absolute normalized path")
        evidence_parent = no_symlink_path(raw_evidence.parent, "root evidence parent")
        verify_runner_owned_directory(evidence_parent, args.runner_uid, args.runner_gid, "root evidence parent")
        evidence_root = evidence_parent / raw_evidence.name
        if evidence_root.exists() or evidence_root.is_symlink():
            fail("root evidence path must be fresh")
        evidence_root.mkdir(mode=0o700)
        os.chown(evidence_root, 0, 0)
        os.chmod(evidence_root, 0o700)
        scratch_root = evidence_parent / ROOT_RUN_NAME
        if scratch_root.exists() or scratch_root.is_symlink():
            fail("exact-head scratch root must be fresh")
        create_runner_owned_directory(scratch_root, args.runner_uid, args.runner_gid)
        cell = scratch_root / CELL_NAME
        root_owned_directory(cell)
        dispatcher_path = no_symlink_path(Path(args.dispatcher_manifest), "dispatcher manifest")
        candidate_root = no_symlink_path(Path(args.candidate_artifact_root), "candidate artifact root")
        candidate_path = contained(
            Path(args.candidate_manifest), candidate_root, "candidate artifact manifest"
        )
        verify_helpers()
        verify_apparmor_profile()
        verify_checkout(repo, trusted_base_sha, args.runner_uid, args.runner_gid)
        helper_descriptor, _ = trusted_base_file_descriptor(
            repo,
            trusted_base_sha,
            BASE_DRIVER_RELATIVE,
            args.runner_uid,
            args.runner_gid,
            "trusted Base NGINX helper",
        )
        trusted_base_descriptors["helper"] = helper_descriptor
        dispatcher = dispatcher_manifest(dispatcher_path, trusted_base_sha)
        candidate = candidate_manifest(candidate_path, dispatcher)
        artifacts, artifact_descriptors = admit_candidate_bundle(candidate_root, candidate)
        suffix = f"{os.getpid():x}"
        identity = create_identity(suffix)
        worker_name, worker_group = identity
        worker = pwd.getpwnam(worker_name)
        worker_uid = worker.pw_uid
        runner = pwd.getpwuid(args.runner_uid)
        group = grp.getgrnam(worker_group)
        if worker.pw_uid in {0, args.runner_uid} or group.gr_gid in {0, args.runner_gid}:
            fail("dedicated identity collides with runner or root")
        mapping = SubordinateMapping(
            runner_name=runner.pw_name,
            runner_uid=args.runner_uid,
            worker_uid=worker.pw_uid,
            worker_gid=group.gr_gid,
        )
        establish_subordinate_mapping(mapping)
        binary = candidate_root / "nginx"
        module = candidate_root / "ngx_http_modsecurity_module.so"
        library = candidate_root / "libmodsecurity.so.3"
        prepare_trusted_cells(
            cell,
            module,
            worker_name,
            worker_group,
            args.runner_uid,
            args.runner_gid,
        )
        outer_env = {
            "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
            "LC_ALL": "C",
            "LANG": "C",
            "HOME": "/nonexistent",
        }
        sandbox_env = {
            **outer_env,
            "NGINX_EXACT_HEAD_IN_ROOT_LAUNCHER": "1",
            "NGINX_EXACT_HEAD_TRUSTED_BASE_ROOT": "/trusted-base",
            "NGINX_EXACT_HEAD_SCRATCH_ROOT": str(cell),
            "NGINX_BINARY": str(binary),
            "NGINX_MODULE": str(module),
            "MODSECURITY_LIB_DIR": str(candidate_root),
            # This path is entirely Base-selected and FD-backed below; it is
            # not inherited from the job or accepted from candidate metadata.
            "LD_LIBRARY_PATH": str(candidate_root),
            "NGINX_WORKER_USER": worker_name,
            "NGINX_WORKER_GROUP": worker_group,
            # Do not expose a conventional public temporary directory inside
            # the candidate sandbox.  The mount is fresh and private to this
            # one cell, while standard temporary-file consumers still receive
            # an explicit writable location.
            "TMPDIR": str(SANDBOX_TMPDIR),
        }
        # The outer transition intentionally does not set no_new_privs: the
        # trusted util-linux mapper must invoke the setuid uidmap helpers to
        # create the one explicit secondary identity map.  It changes to a
        # nonzero host UID without keep-caps and clears inheritable/ambient
        # sets before any checked-out command is reachable.  The inner
        # transition, after mapping, enables no_new_privs and narrows the
        # namespace capability set before bubblewrap can execute the harness.
        command = [HELPERS["aa-exec"], "-p", APPARMOR_PROFILE_NAME, "--", HELPERS["setpriv"], f"--reuid={args.runner_uid}", f"--regid={args.runner_gid}", "--clear-groups", "--inh-caps=-all", "--ambient-caps=-all",
                   "--", HELPERS["unshare"], "--user", "--map-user", "0", "--map-group", "0", "--map-users", f"{worker.pw_uid}:{worker.pw_uid}:1",
                   "--map-groups", f"{group.gr_gid}:{group.gr_gid}:1", "--setgroups", "allow", "--keep-caps", "--mount", "--pid", "--fork",
                   "--kill-child=SIGKILL", "--mount-proc=/proc", "--propagation", "private", HELPERS["setpriv"],
                   "--clear-groups", "--no-new-privs", "--inh-caps=-all", "--ambient-caps=-all",
                   "--bounding-set=-all,+chown,+setgid,+setuid,+sys_admin", "--", HELPERS["bwrap"],
                   "--die-with-parent", "--new-session", "--unshare-pid", "--unshare-net", "--unshare-ipc", "--unshare-uts",
                   "--disable-userns", "--assert-userns-disabled", "--tmpfs", "/", "--dir", "/proc", "--dir", "/dev",
                   "--dir", "/usr", "--dir", "/bin", "--dir", "/lib", "--dir", "/lib64",
                   "--dir", "/etc", "--dir", "/run", "--proc", "/proc", "--dev", "/dev", "--tmpfs", str(SANDBOX_TMPDIR),
                   "--ro-bind", "/usr", "/usr", "--ro-bind", "/bin", "/bin",
                   "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64", "--ro-bind", "/etc", "/etc",
                   "--ro-bind", str(scratch_root), str(scratch_root),
                   "--ro-bind", str(candidate_root), str(candidate_root),
                   "--ro-bind-fd", str(trusted_base_descriptors["helper"]), str(SANDBOX_BASE_HELPER),
                   "--ro-bind-fd", str(artifact_descriptors["nginx"]), str(binary),
                   "--ro-bind-fd", str(artifact_descriptors["module"]), str(module),
                   "--ro-bind-fd", str(artifact_descriptors["library"]), str(library),
                   "--ro-bind-fd", str(artifact_descriptors["manifest"]), str(candidate_path),
                   "--bind", str(cell), str(cell),
                   "--ro-bind", str(cell / "on" / "config"), str(cell / "on" / "config"),
                   "--ro-bind", str(cell / "off" / "config"), str(cell / "off" / "config"),
                   "--chdir", "/", "--clearenv", "--cap-drop", "ALL", "--cap-add", "CAP_CHOWN",
                   "--cap-add", "CAP_SETGID", "--cap-add", "CAP_SETUID"]
        for key, value in sorted(sandbox_env.items()):
            command.extend(("--setenv", key, value))
        command.extend(("--", HELPERS["sh"], str(SANDBOX_BASE_HELPER),
                        str(candidate_root), str(candidate_path), str(cell)))
        enable_child_subreaper()
        process = subprocess.Popen(
            validated_command(command),
            env=outer_env,
            pass_fds=tuple(artifact_descriptors.values()) + tuple(trusted_base_descriptors.values()),
            preexec_fn=apply_sandbox_limits,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        expected_identity = IdentityExpectations(args.runner_uid, args.runner_gid, worker.pw_uid, group.gr_gid)
        identity_evidence: list[dict[str, object]] = []
        observed_status: dict[str, int] = {}
        for mode in ("on", "off"):
            observed_identity = wait_mode(
                cell,
                mode,
                expected_identity,
                binary,
                artifacts["nginx"],
                module,
                worker_name,
                worker_group,
                process,
            )
            try:
                master_pidfd = observed_identity.get("master_pidfd")
                if type(master_pidfd) is not int:
                    fail("validated identity lacks a master pidfd")
                observed_status[mode] = trusted_http_status(master_pidfd)
            finally:
                close_identity_pidfd(observed_identity)
            identity_evidence.append(observed_identity)
            mark_request_complete(cell, mode, observed_status[mode])
        validate_exit_status(process.wait(timeout=SUPERVISOR_TIMEOUT))
        for key, descriptor in artifact_descriptors.items():
            if key == "manifest":
                continue
            if admitted_artifact_identity(descriptor, f"candidate {key} artifact") != artifacts[key]:
                fail(f"admitted candidate {key} artifact changed during isolated runtime")
        runtime_evidence = [
            mode_evidence(cell, mode, observed_status[mode]) for mode in ("on", "off")
        ]
        publish_evidence(evidence_root, dispatcher, expected_identity, identity_evidence,
                         artifacts, runtime_evidence)
        evidence_published = True
    except BaseException as exc:
        primary = exc
    finally:
        cleanup_errors: list[str] = []
        for key, descriptor in tuple(artifact_descriptors.items()):
            try:
                os.close(descriptor)
            except OSError as exc:
                cleanup_errors.append(f"{key} descriptor: {exc}")
        for key, descriptor in tuple(trusted_base_descriptors.items()):
            try:
                os.close(descriptor)
            except OSError as exc:
                cleanup_errors.append(f"trusted Base {key} descriptor: {exc}")
        runtime_quiescent = process is None
        if process is not None:
            try:
                terminate_runtime_process(process)
            except BaseException as exc:
                cleanup_errors.append(f"runtime process: {exc}")
            else:
                runtime_quiescent = True
        if runtime_quiescent and worker_uid is not None:
            try:
                require_no_dedicated_worker_processes(worker_uid)
            except BaseException as exc:
                cleanup_errors.append(f"dedicated worker processes: {exc}")
                runtime_quiescent = False
        identity_cleaned = identity is None
        if runtime_quiescent and identity is not None:
            try:
                cleanup_identity(*identity)
            except BaseException as exc:
                cleanup_errors.append(f"dedicated identity: {exc}")
            else:
                identity_cleaned = True
        if runtime_quiescent and mapping is not None and identity_cleaned:
            try:
                cleanup_subordinate_mapping(mapping)
            except BaseException as exc:
                cleanup_errors.append(f"subordinate mapping: {exc}")
        elif runtime_quiescent and mapping is not None:
            cleanup_errors.append("subordinate mapping retained because identity cleanup failed")
        if runtime_quiescent and scratch_root is not None and (scratch_root.exists() or scratch_root.is_symlink()):
            try:
                if scratch_root.is_symlink():
                    scratch_root.unlink()
                elif scratch_root.is_dir():
                    shutil.rmtree(scratch_root)
                else:
                    fail("root launcher scratch changed into an unsafe file")
            except BaseException as exc:
                cleanup_errors.append(f"runtime cell: {exc}")
        elif not runtime_quiescent:
            cleanup_errors.append(
                "runtime ownership was not quiescent; retained identity, mapping, and cell"
            )
        if (
            not evidence_published
            and evidence_root is not None
            and (evidence_root.exists() or evidence_root.is_symlink())
        ):
            try:
                metadata = evidence_root.lstat()
                if (
                    stat.S_ISLNK(metadata.st_mode)
                    or not stat.S_ISDIR(metadata.st_mode)
                    or metadata.st_uid != 0
                    or metadata.st_gid != 0
                ):
                    fail("failed-run evidence root changed into an unsafe path")
                shutil.rmtree(evidence_root)
            except BaseException as exc:
                cleanup_errors.append(f"failed-run evidence: {exc}")
        if cleanup_errors:
            cleanup_message = "; ".join(cleanup_errors)
            if primary is None:
                primary = LauncherError(f"cleanup failed: {cleanup_message}")
            else:
                primary = LauncherError(f"{primary}; cleanup failed: {cleanup_message}")
    if primary is not None:
        print(f"NGINX exact-head root launcher failed: {primary}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
