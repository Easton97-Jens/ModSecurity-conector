#!/usr/bin/env python3
"""Bounded HTTP/1.1 qualification of a freshly built native Apache module.

Build first with the canonical ``make build-apache`` target. This runner uses
real httpd/libmodsecurity and its own loopback origin; it never substitutes a
simulated connector. Specialized late-commit/Strict and fault-injection gates
remain separate and are listed in the output, so success is not full B approval.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.client
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mmap
import os
from pathlib import Path
import re
import select
import signal
import socket
import stat
import subprocess
import sys
import threading
import time

GUARD = Path(__file__).with_name("apache_process_guard.py")
MAX_ARTIFACT = 8 * 1024 * 1024
LIMIT = 1024
LEGACY_CONNECTOR_LIMIT = 32
LOCAL_ERROR_BODY = b"qualification-apache-local-error-500"
ENGINE_REJECT_BODY = b"qualification-apache-engine-reject-403"
RULES = '''SecRuleEngine On
SecRequestBodyAccess On
SecRequestBodyLimit 1024
SecRequestBodyNoFilesLimit 1024
SecRequestBodyLimitAction Reject
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain
SecResponseBodyLimit 1024
SecResponseBodyLimitAction Reject
SecAuditEngine Off
SecRule REQUEST_HEADERS:X-Qualification-P1 "@streq deny" "id:991001,phase:1,deny,status:403,log"
SecRule REQUEST_BODY "@contains qualification-p2-deny" "id:991002,phase:2,deny,status:403,log"
SecRule RESPONSE_HEADERS:X-Qualification-P3 "@streq deny" "id:991003,phase:3,deny,status:403,log"
SecRule RESPONSE_BODY "@contains qualification-p4-deny" "id:991004,phase:4,deny,status:403,log"
'''


def load_guard():
    spec = importlib.util.spec_from_file_location("apache_process_guard", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reap_child(pid: int, timeout: float = 8) -> int:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        found, status = os.waitpid(pid, os.WNOHANG)
        if found == pid:
            return os.waitstatus_to_exitcode(status)
        time.sleep(0.02)
    raise RuntimeError("controller child did not exit within cleanup bound")


def fork_guard(action, guard) -> int:
    expected_parent = os.getpid()
    pid = os.fork()
    if pid == 0:
        try:
            guard._set_parent_death_signal(int(signal.SIGKILL))
            if os.getppid() != expected_parent:
                os._exit(77)
            result = action()
        except BaseException as error:
            print("apache qualification controller: " + str(error), file=sys.stderr, flush=True)
            os._exit(77)
        os._exit(result or 0)
    return pid


def terminate_controller_child(pid: int) -> None:
    """Signal only an unreaped direct child, whose PID cannot be reused."""
    os.kill(pid, signal.SIGTERM)
    try:
        reap_child(pid)
    except RuntimeError:
        os.kill(pid, signal.SIGKILL)
        reap_child(pid)


def observed_supervise(guard, httpd, root, state, pid_output):
    """Publish the real launch-bound HTTPD reap, including cleanup signals."""
    signals = []
    original_send = guard._send_child_signal
    original_session = guard._run_supervisor_session

    def send(pidfd, child, sig):
        signals.append(int(sig))
        return original_send(pidfd, child, sig)

    def session(child, *args):
        try:
            return original_session(child, *args)
        finally:
            private_write(root / "httpd-exit.json", json.dumps({
                "pid": child.pid, "exit_status": child.poll(), "signals": signals,
                "reaped": child.returncode is not None}) + "\n")

    guard._send_child_signal = send
    guard._run_supervisor_session = session
    return guard.supervise(httpd, root / "conf/httpd.conf", state, pid_output)


def assert_controlled_exit(value, pid):
    # HTTPD may handle TERM and exit zero, or retain the TERM exit status.
    # A supervisor zero exit alone does not certify either outcome.
    if (type(value.get("pid")) is not int or value["pid"] != pid
            or type(value.get("exit_status")) is not int
            or value["exit_status"] not in (0, -int(signal.SIGTERM))
            or value.get("signals") != [int(signal.SIGTERM)]
            or value.get("reaped") is not True):
        raise RuntimeError("HTTPD exit was not a controlled TERM reap")


def supervisor_controller(control_fd: int) -> int:
    """Keep guard launch and stop children under one stable RTK-launched parent.

    The only stop capability is an inherited private socket; there is no PID or
    executable selector. The guard retains every launch and peer-lineage check.
    Its functions run in forked children, without adding another RTK intermediary.
    """
    guard = load_guard()
    root = guard._runner_configured_path(guard.RUNNER_ARTIFACT_ROOT_ENV,
                                         guard.APACHE_ARTIFACT_ROOT_LABEL)
    httpd = guard._runner_configured_path(guard.RUNNER_HTTPD_ENV,
                                          guard.APACHE_EXECUTABLE_LABEL)
    state, pid_output = root / "supervisor.json", root / "child.pid"
    control = socket.socket(fileno=control_fd)
    if control.family != socket.AF_UNIX or control.type != socket.SOCK_STREAM:
        control.close()
        raise RuntimeError("controller requires an inherited private Unix stream")
    stopping = False

    def stop_requested(*_args):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop_requested)
    signal.signal(signal.SIGINT, stop_requested)
    expected_parent = os.getppid()
    guard._set_parent_death_signal()
    if os.getppid() != expected_parent:
        control.close()
        raise RuntimeError("controller launcher disappeared before start")
    supervisor = fork_guard(lambda: observed_supervise(guard, httpd, root, state, pid_output), guard)
    stopper = None
    try:
        deadline = time.monotonic() + 900
        while not stopping:
            if time.monotonic() >= deadline:
                raise RuntimeError("controller lifetime bound exceeded")
            readable, _, _ = select.select([control], [], [], 0.25)
            if readable:
                command = control.recv(32)
                if command not in (b"stop\n", b""):
                    raise RuntimeError("invalid controller control command")
                break
            child, status = os.waitpid(supervisor, os.WNOHANG)
            if child == supervisor:
                supervisor = None
                raise RuntimeError("supervisor exited before stop: " + str(os.waitstatus_to_exitcode(status)))
        stopper = fork_guard(lambda: guard.stop_supervisor(state, root), guard)
        stop_status = reap_child(stopper)
        stopper = None
        if stop_status != 0:
            raise RuntimeError("guard rejected controller stop")
        status = reap_child(supervisor)
        supervisor = None
        if status != 0:
            raise RuntimeError("supervisor cleanup failed")
        return 0
    finally:
        control.close()
        if stopper is not None:
            terminate_controller_child(stopper)
        if supervisor is not None:
            terminate_controller_child(supervisor)


def config_path(value: str) -> Path:
    if len(value) > 4096:
        raise ValueError("path exceeds configuration bound")
    if any(character in value for character in '\n\r"\\$'):
        raise ValueError("path contains Apache configuration metacharacters")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("path must be absolute and traversal-free")
    return path


def directory_fd(path: Path, private: bool = False) -> int:
    """Walk directories with pinned descriptors, never follow an ancestor link."""
    config_path(str(path))
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        traversed = Path("/")
        for name in path.parts[1:]:
            next_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=fd)
            os.close(fd)
            fd = next_fd
            traversed /= name
            info = os.fstat(fd)
            trusted_sticky = (traversed == Path("/var/tmp") and info.st_uid == 0
                              and bool(info.st_mode & stat.S_ISVTX))
            if info.st_uid not in (0, os.geteuid()) or (info.st_mode & 0o022 and not trusted_sticky):
                raise ValueError("directory ancestor has unsafe ownership or permissions")
        info = os.fstat(fd)
        if private and (info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700):
            raise ValueError("artifact root must be owned by the runner and mode 0700")
        return fd
    except BaseException:
        os.close(fd)
        raise


def file_fd(path: Path, maximum: int, evidence: bool = True) -> int:
    parent = directory_fd(path.parent)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     dir_fd=parent)
    finally:
        os.close(parent)
    try:
        info = os.fstat(fd)
        owners = (os.geteuid(),) if evidence else (0, os.geteuid())
        if not stat.S_ISREG(info.st_mode) or info.st_uid not in owners or info.st_nlink != 1:
            raise ValueError("file must be an owned, single-link regular file")
        if ((evidence and stat.S_IMODE(info.st_mode) not in (0o400, 0o600))
                or info.st_mode & (0o022 | stat.S_ISUID | stat.S_ISGID)):
            raise ValueError("file permissions violate the evidence/input contract")
        if info.st_size > maximum:
            raise RuntimeError(f"artifact exceeds bound: {path.name}")
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_fd(fd: int, maximum: int) -> bytes:
    with os.fdopen(fd, "rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise RuntimeError("artifact exceeds bound during read")
    return data


def bounded_read(path: Path, maximum: int = MAX_ARTIFACT) -> bytes:
    return read_fd(file_fd(path, maximum), maximum)


def proc_read(pid: int, name: str) -> bytes:
    if pid <= 0 or name not in ("maps", "mountinfo", "status"):
        raise ValueError("unsupported kernel observation")
    fd = os.open(f"/proc/{pid}/{name}", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise ValueError("kernel observation is not a regular proc file")
    return read_fd(fd, MAX_ARTIFACT)


def digest(path: Path) -> str:
    maximum = 256 * 1024 * 1024
    value = hashlib.sha256()
    total = 0
    with os.fdopen(file_fd(path, maximum, evidence=False), "rb") as stream:
        while chunk := stream.read(min(65536, maximum - total + 1)):
            total += len(chunk)
            if total > maximum:
                raise RuntimeError("input grew beyond the hashing bound")
            value.update(chunk)
    return value.hexdigest()


def input_identity(path: Path) -> dict:
    """Hash and identify one descriptor, rejecting concurrent input mutation."""
    maximum = 256 * 1024 * 1024
    fd = file_fd(path, maximum, evidence=False)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        value = hashlib.sha256()
        total = 0
        while chunk := stream.read(min(65536, maximum - total + 1)):
            total += len(chunk)
            if total > maximum:
                raise RuntimeError("input grew beyond the hashing bound")
            value.update(chunk)
        after = os.fstat(stream.fileno())
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
    if any(getattr(before, field) != getattr(after, field) for field in fields):
        raise RuntimeError("qualification input changed during hashing")
    return {**{field: getattr(after, field) for field in fields}, "sha256": value.hexdigest()}


def verify_input_identity(path: Path, expected: dict) -> None:
    if input_identity(path) != expected:
        raise RuntimeError("qualification input identity or digest changed: " + path.name)


def verify_inputs(args) -> None:
    for key, expected in args.input_pins.items():
        verify_input_identity(getattr(args, key), expected)


def reject_security_module_preload(output: bytes) -> None:
    if re.search(rb"module\s+security3_module\s+is\s+already\s+loaded", output, re.I):
        raise RuntimeError("security3 module was loaded more than once")


def mapping_identity(fields: list[str]) -> tuple[int, int]:
    try:
        major, minor = (int(value, 16) for value in fields[3].split(":"))
        return os.makedev(major, minor), int(fields[4])
    except (ValueError, OverflowError) as error:
        raise RuntimeError("malformed security3 module mapping") from error


def decode_mount_path(value: str) -> Path:
    escapes = {"040": " ", "011": "\t", "012": "\n", "134": "\\"}
    decoded = []
    index = 0
    while index < len(value):
        if value[index] != "\\":
            decoded.append(value[index])
            index += 1
            continue
        code = value[index + 1:index + 4]
        if len(code) != 3 or code not in escapes:
            raise RuntimeError("unsupported mountinfo path escape")
        decoded.append(escapes[code])
        index += 4
    path = Path("".join(decoded))
    if not path.is_absolute():
        raise RuntimeError("mountinfo path is not absolute")
    return path


def effective_mount(path: Path, mountinfo: str) -> tuple[int, str, Path, Path]:
    candidates = []
    for line in mountinfo.splitlines():
        fields = line.split()
        try:
            separators = [index for index, field in enumerate(fields) if field == "-"]
            if len(separators) != 1 or separators[0] < 6 or len(fields) != separators[0] + 4:
                raise RuntimeError("malformed mountinfo observation")
            separator = separators[0]
            if (not fields[0].isdecimal() or int(fields[0]) < 1
                    or not fields[1].isdecimal() or int(fields[1]) < 0):
                raise RuntimeError("malformed mountinfo observation")
            device_parts = fields[2].split(":")
            if len(device_parts) != 2 or not all(value.isdecimal() for value in device_parts):
                raise RuntimeError("malformed mountinfo observation")
            root = decode_mount_path(fields[3])
            mount = decode_mount_path(fields[4])
            filesystem = fields[separator + 1]
            major, minor = (int(value, 10) for value in device_parts)
            device = os.makedev(major, minor)
        except (IndexError, ValueError, OverflowError) as error:
            raise RuntimeError("malformed mountinfo observation") from error
        if path == mount or path.is_relative_to(mount):
            candidates.append((len(mount.parts), mount, device, filesystem, root))
    if not candidates:
        raise RuntimeError("pinned module has no covering mountinfo entry")
    mounts = [candidate[1] for candidate in candidates]
    if len(set(mounts)) != len(mounts):
        raise RuntimeError("pinned module mountinfo is ambiguous")
    depth = max(candidate[0] for candidate in candidates)
    selected = [candidate for candidate in candidates if candidate[0] == depth]
    if len(selected) != 1:
        raise RuntimeError("pinned module mountinfo is ambiguous")
    _, mount, device, filesystem, root = selected[0]
    return device, filesystem, root, mount


def proc_link_identity(pid: int, name: str) -> tuple[int, int]:
    """Open one controlled proc magic link and identify its kernel object."""
    if pid <= 0 or name not in ("ns/mnt", "root"):
        raise ValueError("unsupported kernel identity")
    flags = os.O_CLOEXEC | (os.O_RDONLY if name == "ns/mnt" else os.O_PATH | os.O_DIRECTORY)
    fd = os.open(f"/proc/{pid}/{name}", flags)
    try:
        info = os.fstat(fd)
        return info.st_dev, info.st_ino
    finally:
        os.close(fd)


def process_mount_context(pid: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return proc_link_identity(pid, "ns/mnt"), proc_link_identity(pid, "root")


def backing_mapping_identity(module: Path, expected: dict) -> tuple[int, int]:
    """Observe the kernel mapping tuple for the safely opened pinned DSO."""
    verify_input_identity(module, expected)
    fd = file_fd(module, 256 * 1024 * 1024, evidence=False)
    try:
        info = os.fstat(fd)
        fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
        if any(getattr(info, field) != expected[field] for field in fields) or info.st_size < 1:
            raise RuntimeError("pinned DSO changed before backing-map observation")
        with mmap.mmap(fd, 1, access=mmap.ACCESS_READ):
            maps = proc_read(os.getpid(), "maps").decode()
            identities = set()
            for line in maps.splitlines():
                mapping = line.split(maxsplit=5)
                if len(mapping) == 6 and mapping[5] == str(module):
                    identities.add(mapping_identity(mapping))
    finally:
        os.close(fd)
    if len(identities) != 1:
        raise RuntimeError("pinned DSO backing-map identity is missing or ambiguous")
    verify_input_identity(module, expected)
    return identities.pop()


def assert_mapped_module(maps: str, module: Path, expected: dict,
                         host_mountinfo: str | None = None) -> None:
    """Bind kernel map path/device/inode to the descriptor-hashed DSO input."""
    found = False
    identities = set()
    backing_identity = None
    for line in maps.splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) != 6:
            continue
        path = fields[5]
        if path != str(module) and "security3" not in Path(path).name:
            continue
        device, inode = mapping_identity(fields)
        if path != str(module) or inode != expected["st_ino"]:
            raise RuntimeError("loaded security3 module differs from pinned DSO")
        if device != expected["st_dev"]:
            if host_mountinfo is None:
                raise RuntimeError("loaded security3 module differs from pinned DSO")
            if backing_identity is None:
                backing_identity = backing_mapping_identity(module, expected)
            if (device, inode) != backing_identity:
                raise RuntimeError("loaded security3 module differs from pinned DSO")
            host_mount = effective_mount(module, host_mountinfo)
            runner_mount = effective_mount(module, proc_read(os.getpid(), "mountinfo").decode())
            if host_mount != runner_mount:
                raise RuntimeError("loaded security3 module differs from pinned DSO")
            mount_device, filesystem, _, _ = host_mount
            if not ((filesystem == "overlay" and mount_device == expected["st_dev"])
                    or (filesystem == "btrfs" and mount_device == backing_identity[0])):
                raise RuntimeError("loaded security3 module differs from pinned DSO")
        identities.add((device, inode))
        found = True
    if not found or len(identities) != 1:
        raise RuntimeError("pinned security3 module is absent from host mappings")
    verify_input_identity(module, expected)


def observed_module_maps(pid: int, module: Path, expected: dict) -> str:
    """Bind host maps to the runner's unchanged mount namespace and root."""
    runner_context = process_mount_context(os.getpid())
    host_context = process_mount_context(pid)
    if host_context != runner_context:
        raise RuntimeError("Apache host mount namespace or root differs from qualification runner")
    maps = proc_read(pid, "maps").decode()
    mountinfo = proc_read(pid, "mountinfo").decode()
    assert_mapped_module(maps, module, expected, mountinfo)
    if process_mount_context(os.getpid()) != runner_context:
        raise RuntimeError("qualification runner mount namespace or root changed during observation")
    if process_mount_context(pid) != host_context:
        raise RuntimeError("Apache host mount namespace or root changed during observation")
    return maps


def trusted_file(value: str) -> Path:
    path = config_path(value)
    if not path.is_absolute() or path.resolve(strict=True) != path:
        raise ValueError("input must be an absolute canonical file without symlinks")
    fd = file_fd(path, 256 * 1024 * 1024, evidence=False)
    os.close(fd)
    return path


def private_write(path: Path, data: str) -> None:
    if len(data.encode("utf-8")) > MAX_ARTIFACT:
        raise RuntimeError("generated artifact exceeds evidence bound")
    parent = directory_fd(path.parent)
    try:
        fd = os.open(path.name, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     0o600, dir_fd=parent)
    finally:
        os.close(parent)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(data)


def private_mkdir(path: Path) -> None:
    parent = directory_fd(path.parent)
    try:
        os.mkdir(path.name, 0o700, dir_fd=parent)
    finally:
        os.close(parent)
    os.close(directory_fd(path, private=True))


def serving_identity(status: str, expected_uid: int, expected_gid: int) -> dict:
    if expected_uid <= 0 or expected_gid <= 0:
        raise RuntimeError("qualification requires an unprivileged non-root serving profile")
    result = {}
    for field, expected in (("Uid", expected_uid), ("Gid", expected_gid)):
        match = re.search(rf"^{field}:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$", status, re.M)
        if match is None or any(int(value) != expected for value in match.groups()):
            raise RuntimeError("serving UID/GID differs from the unprivileged runner profile")
        result[field.lower()] = list(map(int, match.groups()))
    capabilities = re.search(r"^CapEff:\s+([0-9a-fA-F]+)\s*$", status, re.M)
    groups = re.search(r"^Groups:[ \t]*(.*)$", status, re.M)
    if capabilities is None or int(capabilities[1], 16) != 0:
        raise RuntimeError("serving profile has effective capabilities or missing evidence")
    if groups is None or "0" in groups[1].split():
        raise RuntimeError("serving profile has root supplementary group or missing evidence")
    result.update(capabilities_effective=0, groups=list(map(int, groups[1].split())))
    return result


def events(path: Path, token: str) -> list[dict]:
    if not path.exists():
        return []
    values = [json.loads(line) for line in bounded_read(path).splitlines() if line]
    return [value for value in values if value.get("transaction_id") == token]


def reconcile_final(root, cases, receipts, origin_errors):
    raw = bounded_read(root / "events.jsonl") if (root / "events.jsonl").exists() else b""
    if raw and not raw.endswith(b"\n"):
        raise RuntimeError("partial final event record")
    values = [json.loads(line) for line in raw.splitlines()]
    expected = [value for case in cases for value in case["events"]]
    # Concurrent requests may reorder records, but never change multiplicity,
    # correlation or any field after the per-request decision snapshot.
    canonical = lambda items: sorted(json.dumps(value, sort_keys=True) for value in items)
    if canonical(values) != canonical(expected):
        raise RuntimeError("late, uncorrelated or changed final event")
    wanted = {case["token"]: case["backend_delta"] for case in cases if case["backend_delta"]}
    if receipts != wanted or origin_errors:
        raise RuntimeError("final origin receipt/error reconciliation failed")


def reconcile_logs(root, cases=()):
    for path in root.glob("*.log"):
        data = bounded_read(path).decode("utf-8", errors="strict")
        for line in data.splitlines():
            if re.search(r"(?i)\b(?:fatal|crit(?:ical)?|panic|segfault|segmentation fault)\b|"
                         r"(?i:modsecurity|native|engine).*(?i:internal error|engine error|failed\b|failure\b)", line):
                raise RuntimeError("unexpected fatal/native engine log: " + path.name)


def assert_decision(values: list[dict], rule: str | None, phase: str | None,
                    status: int = 403, body_limit: bool = False) -> None:
    if rule is None and not body_limit:
        if values:
            raise RuntimeError("allow unexpectedly emitted an intervention")
        return
    if len(values) != 1:
        raise RuntimeError("expected exactly one correlated intervention")
    value = values[0]
    if str(value.get("rule_id")) != ("" if body_limit else rule) or value.get("phase") != phase:
        raise RuntimeError("intervention rule/phase mismatch")
    expected = {"connector": "apache", "integration_mode": "native-httpd-module",
                "action": "deny", "requested_action": "deny", "actual_action": "deny",
                "status": "blocked", "http_status": status, "visible_http_status": status,
                "transport_result": "http_status", "response_committed": False,
                "late_intervention": False, "headers_sent": False, "connection_aborted": False,
                "truncated": False, "body_truncated": body_limit and phase == "response_body"}
    if phase == "response_body" and "late_intervention_mode" in value:
        if type(value["late_intervention_mode"]) is not str or value["late_intervention_mode"] != "safe":
            raise RuntimeError("intervention late_intervention_mode mismatch")
    if body_limit:
        expected.update(event="body_limit", body_limit_outcome="reject")
    for field, wanted in expected.items():
        if type(value.get(field)) is not type(wanted) or value.get(field) != wanted:
            raise RuntimeError(f"intervention {field} mismatch")


def assert_phase4_safe(values: list[dict]) -> None:
    """Verify the progressive Safe result separately from ordinary Allow."""
    if len(values) != 1:
        raise RuntimeError("expected exactly one correlated Safe P4 intervention")
    expected = {"connector": "apache", "integration_mode": "native-httpd-module",
                "event": "phase4_intervention", "phase": "response_body", "rule_id": "991004",
                "status": "blocked", "requested_action": "deny", "action": "log_only",
                "actual_action": "log_only", "http_status": 403, "original_http_status": 200,
                "visible_http_status": 200, "transport_result": "log_only", "reason": "response_committed_safe",
                "late_intervention_mode": "safe", "late_intervention": True, "response_started": True,
                "response_committed": True, "headers_sent": True, "body_started": True, "eos_seen": True,
                "body_bytes_seen": 21, "body_bytes_inspected": 21, "body_truncated": False,
                "connection_aborted": False, "client_disconnected": False, "upstream_disconnected": False,
                "cancelled": False, "redacted": False, "truncated": False}
    for field, wanted in expected.items():
        if type(values[0].get(field)) is not type(wanted) or values[0].get(field) != wanted:
            raise RuntimeError(f"Safe P4 intervention {field} mismatch")


def assert_response_overlimit(values: list[dict], branch="after_commit") -> None:
    if len(values) != 1:
        raise RuntimeError("expected exactly one correlated native engine-limit intervention")
    if "body_limit_outcome" in values[0]:
        raise RuntimeError("native engine-limit intervention fabricated connector limit outcome")
    expected = {"connector": "apache", "integration_mode": "native-httpd-module",
                "message_id": "MSCONN_EVENT_PHASE4_LATE_INTERVENTION", "event": "phase4_intervention",
                "phase": "response_body", "rule_id": "", "status": "blocked",
                "requested_action": "deny", "action": "log_only",
                "actual_action": "log_only", "http_status": 403,
                "original_http_status": 200, "visible_http_status": 200,
                "transport_result": "log_only", "reason": "response_committed_safe",
                "method": "GET", "uri": "/response/1025", "content_type": "text/plain",
                "late_intervention_mode": "safe",
                "late_intervention": True, "response_started": True, "response_committed": True,
                "headers_sent": True, "body_started": True, "eos_seen": True,
                # Apache counts successful append calls here; this does not
                # assert that libModSecurity retained the rejected bucket.
                "body_bytes_seen": 1025, "body_bytes_inspected": 1025, "body_truncated": False,
                "connection_aborted": False, "client_disconnected": False,
                "upstream_disconnected": False, "cancelled": False, "redacted": False,
                "truncated": False}
    if branch == "before_commit":
        expected.update(message_id="MSCONN_EVENT_RESPONSE_BLOCKED", reason="response_not_committed",
                        action="deny", actual_action="deny", visible_http_status=403,
                        transport_result="http_status", late_intervention=False, response_started=False,
                        response_committed=False, headers_sent=False, body_started=False,
                        connection_aborted=False)
        del expected["late_intervention_mode"]
        if "late_intervention_mode" in values[0]:
            raise RuntimeError("precommit engine-limit unexpectedly reports late mode")
    elif branch != "after_commit":
        raise RuntimeError("unknown response-overlimit timing branch")
    for field, wanted in expected.items():
        if type(values[0].get(field)) is not type(wanted) or values[0].get(field) != wanted:
            raise RuntimeError(f"native engine-limit intervention {field} mismatch")


def response_framing(response: http.client.HTTPResponse, name: str) -> str:
    lengths = response.headers.get_all("Content-Length", [])
    encodings = response.headers.get_all("Transfer-Encoding", [])
    if len(lengths) > 1 or len(encodings) > 1 or (lengths and encodings):
        raise RuntimeError(f"ambiguous response framing: {name}")
    if lengths:
        if re.fullmatch(r"0|[1-9][0-9]*", lengths[0], re.ASCII) is None or response.chunked is not False:
            raise RuntimeError(f"invalid Content-Length framing: {name}")
        return "content-length"
    if encodings:
        if encodings[0].lower() != "chunked" or response.chunked is not True:
            raise RuntimeError(f"unsupported Transfer-Encoding framing: {name}")
        return "chunked"
    if response.will_close is not True or response.chunked is not False:
        raise RuntimeError(f"missing close-delimited response framing: {name}")
    return "close-delimited"


class StrictResponseLines:
    """Keep HTTPResponse's header parser, but require bounded wire CRLF."""
    def __init__(self, stream):
        self.stream = stream
        self.metadata = 0
        self.status_line = True
        self.headers_complete = False

    def readline(self, size=65537):
        line = self.stream.readline(min(size, 65537))
        self.metadata += len(line)
        if self.metadata > 65536 or not line.endswith(b"\r\n") or b"\n" in line[:-2] or b"\r" in line[:-2]:
            raise RuntimeError("invalid or truncated response wire framing")
        if self.status_line:
            self.status_line = False
        elif line == b"\r\n":
            self.headers_complete = True
        elif not self.headers_complete:
            # HTTP field names are ASCII tokens followed immediately by a
            # colon. Reject obs-fold and malformed lines before email's
            # permissive parser can turn framing fields into payload.
            if re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+:[\t\x20-\x7e\x80-\xff]*\r\n", line) is None:
                raise RuntimeError("invalid response header wire framing")
        return line

    def __getattr__(self, name):
        return getattr(self.stream, name)


class StrictHTTPResponse(http.client.HTTPResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fp = StrictResponseLines(self.fp)

    def begin(self):
        super().begin()
        if self.headers.defects or any(getattr(value, "defects", ()) for value in self.headers.values()):
            raise RuntimeError("defective response header framing")


def strict_chunked_body(response, name):
    stream = response.fp
    received = bytearray()
    metadata = 0
    while True:
        line = stream.readline(8193)
        metadata += len(line)
        if metadata > 65536 or len(line) > 8192 or not line.endswith(b"\r\n"):
            raise RuntimeError(f"invalid chunk wire framing: {name}")
        # The controlled Apache profile emits plain hexadecimal sizes. Reject
        # extensions rather than inheriting stdlib's permissive split parser.
        if re.fullmatch(rb"[0-9a-fA-F]+\r\n", line) is None:
            raise RuntimeError(f"invalid chunk size framing: {name}")
        size = int(line[:-2], 16)
        if size == 0:
            # No trailers are generated by this profile. Require the actual
            # final empty CRLF; EOF and LF-only are never an EOS receipt.
            if stream.readline(8193) != b"\r\n":
                raise RuntimeError(f"invalid final chunk trailer framing: {name}")
            response._close_conn()
            response.chunk_left = None
            return bytes(received)
        if size > LIMIT + 4096 - len(received):
            raise RuntimeError(f"response exceeds framing bound: {name}")
        data = stream.read(size)
        if len(data) != size or stream.read(2) != b"\r\n":
            raise RuntimeError(f"invalid chunk data framing: {name}")
        received.extend(data)


def assert_response_complete(response: http.client.HTTPResponse, name: str) -> None:
    # read(amt) is bounded, but a premature fixed-length EOF can close fp while
    # leaving response.length positive. isclosed() alone is not completion.
    framing = response_framing(response, name)
    remaining = response.length
    valid_remaining = (type(remaining) is int and remaining == 0
                       if framing == "content-length" else remaining is None)
    if not response.isclosed() or not valid_remaining:
        raise RuntimeError(f"incomplete framing: {name}")


def bounded_response_body(response: http.client.HTTPResponse, name: str) -> bytes:
    framing = response_framing(response, name)
    received = (strict_chunked_body(response, name) if framing == "chunked"
                else response.read(LIMIT + 4097))
    if len(received) > LIMIT + 4096:
        raise RuntimeError(f"response exceeds framing bound: {name}")
    if framing == "close-delimited" and not response.isclosed():
        # A bounded read returning nonempty data may encounter EOF without
        # closing the stdlib stream. Prove EOF with at most one extra byte.
        if response.read(1):
            raise RuntimeError(f"incomplete close-delimited framing: {name}")
    assert_response_complete(response, name)
    return received


def bounded_overlimit_body(response: http.client.HTTPResponse, name: str) -> bytes:
    # Engine Reject is resolved at EOS. Before commit it produces a local
    # 403; Safe after commit forwards the complete original body and logs.
    # The wire branch must agree with its correlated native event.
    response.qualification_wire = {"status": response.status,
                                   "content_lengths": response.headers.get_all("Content-Length", []),
                                   "transfer_encodings": response.headers.get_all("Transfer-Encoding", []),
                                   "termination": "not_observed"}
    framing = response_framing(response, name)
    try:
        received = (response.read(LIMIT + 4097) if framing == "content-length"
                    else bounded_response_body(response, name))
    except (TimeoutError, ConnectionResetError) as error:
        response.qualification_wire["termination"] = ("timeout" if isinstance(error, TimeoutError) else "reset")
        raise
    response.qualification_wire.update(body_bytes=len(received), body_sha256=hashlib.sha256(received).hexdigest(),
                                       remaining_bytes=response.length,
                                       termination="complete" if response.isclosed()
                                       and response.length == 0 else "complete_or_unproven")
    if len(received) > LIMIT + 4096:
        raise RuntimeError("response-overlimit local ErrorDocument exceeds bound")
    if response.status == 200:
        if (framing != "content-length" or response.headers.get_all("Content-Length") != [str(LIMIT + 1)]
                or received != b"x" * (LIMIT + 1)):
            raise RuntimeError("postcommit engine-limit requires complete unmodified CL1025 body")
        assert_response_complete(response, name)
        response.qualification_wire.update(termination="safe_original_complete", branch="after_commit")
        return received
    assert_response_complete(response, name)
    if (response_framing(response, name) != "content-length" or response.status != 403
            or response.headers.get_all("Content-Length") != [str(len(ENGINE_REJECT_BODY))]
            or received != ENGINE_REJECT_BODY):
        raise RuntimeError("unexpected response-overlimit local ErrorDocument status/framing/body")
    response.qualification_wire.update(termination="local_error_document_complete", branch="before_commit")
    return received


class Origin(ThreadingHTTPServer):
    daemon_threads = True
    block_on_close = True

    def __init__(self):
        self.receipts: dict[str, int] = {}
        self.errors = []
        self.lock = threading.RLock()
        self.slots = threading.BoundedSemaphore(8)
        self.handlers: list[tuple[threading.Thread, socket.socket]] = []
        self.closing = False
        self.parallel_barrier = None
        self.parallel_secret = os.urandom(16).hex()
        self.parallel_active = 0
        self.parallel_peak = 0
        self.parallel_errors = []
        super().__init__(("127.0.0.1", 0), OriginHandler)

    def handle_error(self, request, client_address):
        with self.lock:
            self.errors.append("origin handler exception")

    def get_request(self):
        client, address = super().get_request()
        client.settimeout(2)
        return client, address

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            with self.lock:
                self.errors.append("origin concurrency bound exceeded")
            self.shutdown_request(request)
            return
        try:
            with self.lock:
                if self.closing or len(self.handlers) >= 128:
                    self.errors.append("origin request beyond closing/handler bound")
                    self.slots.release()
                    self.shutdown_request(request)
                    return
                worker = threading.Thread(target=self.process_request_thread,
                                          args=(request, client_address), daemon=True)
                self.handlers.append((worker, request))
                worker.start()
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def close_handlers(self, timeout: float = 3) -> None:
        with self.lock:
            self.closing = True
            handlers = list(self.handlers)
        for _worker, client in handlers:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            client.close()
        deadline = time.monotonic() + timeout
        for worker, _client in handlers:
            worker.join(timeout=max(0, deadline - time.monotonic()))
        if any(worker.is_alive() or client.fileno() != -1 for worker, client in handlers):
            raise RuntimeError("origin handler/socket cleanup could not be verified")


class OriginHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_args):
        pass

    def send_error(self, code, message=None, explain=None):
        with self.server.lock:
            self.server.errors.append("origin HTTP error: " + str(code))
        super().send_error(code, message, explain)

    def do_POST(self):
        self.do_GET()

    def do_GET(self):
        self.connection.settimeout(2)
        token = self.headers.get("X-Qualification-ID", "")
        if not re.fullmatch(r"q-[a-f0-9]{24}", token):
            with self.server.lock:
                self.server.errors.append("uncorrelated origin request")
            self.send_error(400)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            with self.server.lock:
                self.server.errors.append("invalid origin body length")
            self.send_error(400)
            return
        if not 0 <= length <= LIMIT:
            with self.server.lock:
                self.server.errors.append("out-of-bound origin body length")
            self.send_error(413)
            return
        if len(self.rfile.read(length)) != length:
            with self.server.lock:
                self.server.errors.append("partial origin body")
            return
        with self.server.lock:
            if token not in self.server.receipts and len(self.server.receipts) >= 128:
                self.send_error(503)
                return
            self.server.receipts[token] = self.server.receipts.get(token, 0) + 1
        parallel = self.path == "/parallel"
        if parallel:
            if (self.server.parallel_barrier is None or
                    self.headers.get("X-Qualification-Parallel") != self.server.parallel_secret):
                self.send_error(400)
                return
            with self.server.lock:
                self.server.parallel_active += 1
                self.server.parallel_peak = max(self.server.parallel_peak, self.server.parallel_active)
            try:
                self.server.parallel_barrier.wait(timeout=2)
                self.respond()
            except threading.BrokenBarrierError:
                self.server.parallel_errors.append("origin overlap barrier failed")
                self.send_error(503)
            finally:
                with self.server.lock:
                    self.server.parallel_active -= 1
            return
        self.respond()

    def respond(self):
        body = b"qualification-p4-deny" if self.path == "/p4" else b"qualification-ok"
        if self.path.startswith("/response/"):
            suffix = self.path.rsplit("/", 1)[1]
            if not suffix.isdecimal() or len(suffix) > 4 or int(suffix) > LIMIT + 1:
                self.send_error(400)
                return
            body = b"x" * int(suffix)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        if self.path == "/p3":
            self.send_header("X-Qualification-P3", "deny")
        self.end_headers()
        self.wfile.write(body)


def unused_port() -> int:
    with socket.socket() as candidate:
        candidate.bind(("127.0.0.1", 0))
        return candidate.getsockname()[1]


def config(root: Path, module: Path, modules: Path, port: int, origin_port: int) -> str:
    for path in (root, module, modules):
        config_path(str(path))
    return f'''ServerRoot "{root}"
PidFile "{root}/httpd.pid"
DefaultRuntimeDir "{root}/run"
Listen 127.0.0.1:{port}
ServerName 127.0.0.1
LoadModule security3_module "{module}"
Include "{modules}"
ErrorLog "{root}/error.log"
LogLevel warn
ErrorDocument 500 "{LOCAL_ERROR_BODY.decode('ascii')}"
ErrorDocument 403 "{ENGINE_REJECT_BODY.decode('ascii')}"
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 2
LimitRequestFieldSize 256
ProxyRequests Off
ProxyPass / http://127.0.0.1:{origin_port}/
ProxyPassReverse / http://127.0.0.1:{origin_port}/
modsecurity on
modsecurity_transaction_id_expr "%{{req:X-Qualification-ID}}"
modsecurity_phase4_mode safe
modsecurity_phase4_body_limit {LEGACY_CONNECTOR_LIMIT}
modsecurity_phase4_log "{root}/events.jsonl"
modsecurity_rules_file "{root}/rules.conf"
'''


class Host:
    def __init__(self, args, root: Path, origin: Origin):
        self.args, self.root, self.origin = args, root, origin
        self.port = unused_port()
        self.process = None
        self.pid = None
        self.resources = []
        self.resource_lock = threading.Lock()
        self.monitor_stop = threading.Event()
        self.monitor_failures = []
        self.library_identities = {}
        self.case_results = []
        self.probe_failures = []
        with origin.lock:
            self.origin_baseline = dict(origin.receipts)
            self.origin_error_baseline = len(origin.errors)
        self.env = dict(os.environ)
        self.env.update(MSCONNECTOR_APACHE_GUARD_ARTIFACT_ROOT=str(root),
                        MSCONNECTOR_APACHE_GUARD_HTTPD=str(args.httpd))
        self.env["LD_LIBRARY_PATH"] = str(args.library.parent) + os.pathsep + self.env.get("LD_LIBRARY_PATH", "")

    def guard(self, *arguments):
        return subprocess.run(["rtk", "proxy", sys.executable, "-I", str(GUARD), *arguments],
                              env=self.env, timeout=12, check=True, capture_output=True)

    def start(self):
        verify_inputs(self.args)
        private_mkdir(self.root)
        private_mkdir(self.root / "conf")
        private_mkdir(self.root / "run")
        private_write(self.root / "rules.conf", RULES)
        private_write(self.root / "conf/httpd.conf", config(self.root, self.args.module,
                      self.args.modules_config, self.port, self.origin.server_port))
        syntax = subprocess.run(["rtk", "proxy", str(self.args.httpd), "-t", "-f", str(self.root / "conf/httpd.conf")],
                                env=self.env, check=True, timeout=10, capture_output=True)
        reject_security_module_preload(syntax.stdout + syntax.stderr)
        verify_inputs(self.args)
        root_fd = directory_fd(self.root, private=True)
        try:
            launch_fd = os.open("launch.log", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                0o600, dir_fd=root_fd)
        finally:
            os.close(root_fd)
        self.launch_log = os.fdopen(launch_fd, "wb")
        self.control, child_control = socket.socketpair()
        try:
            self.process = subprocess.Popen(["rtk", "proxy", sys.executable, "-I", str(Path(__file__).resolve()),
                             "--supervisor-control-fd", str(child_control.fileno())],
                             pass_fds=(child_control.fileno(),), env=self.env,
                             stdout=self.launch_log, stderr=self.launch_log)
        finally:
            child_control.close()
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError("supervised Apache exited during startup")
            try:
                self.pid = int(bounded_read(self.root / "child.pid", 32))
                self.guard("record", "--pid", str(self.pid), "--executable", str(self.args.httpd),
                           "--port", str(self.port), "--output", str(self.root / "identity.json"))
                self.sample()
                verify_inputs(self.args)
                self.monitor = threading.Thread(target=self.monitor_resources, daemon=True)
                self.monitor.start()
                return
            except (OSError, ValueError, subprocess.CalledProcessError):
                time.sleep(0.05)
        raise RuntimeError("Apache readiness deadline exceeded")

    def sample(self):
        if self.pid is None:
            raise RuntimeError("missing native host PID")
        maps = observed_module_maps(self.pid, self.args.module, self.args.input_pins["module"])
        reject_security_module_preload(bounded_read(self.root / "launch.log"))
        candidates = {line.split()[-1] for line in maps.splitlines() if "libmodsecurity.so" in line}
        if not candidates:
            raise RuntimeError("loaded libmodsecurity does not match pinned library")
        for value in candidates:
            library = Path(value)
            info = library.stat()
            identity = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
            if self.library_identities.get(value) != identity:
                if digest(library) != self.args.library_sha256:
                    raise RuntimeError("loaded libmodsecurity does not match pinned library")
                self.library_identities[value] = identity
        status = proc_read(self.pid, "status").decode()
        self.serving_identity = serving_identity(status, os.geteuid(), os.getegid())
        rss = re.search(r"^VmRSS:\s+(\d+) kB$", status, re.M)
        if rss is None:
            raise RuntimeError("missing RSS observation")
        count = len(list(Path(f"/proc/{self.pid}/fd").iterdir()))
        with self.resource_lock:
            if len(self.resources) >= 4096:
                raise RuntimeError("resource sample limit exceeded")
            self.resources.append({"pid": self.pid, "rss_kib": int(rss[1]), "fd_count": count})
        if int(rss[1]) > 512 * 1024 or count > 512:
            raise RuntimeError("bounded host resource ceiling exceeded")
        return maps

    def monitor_resources(self):
        while not self.monitor_stop.wait(0.02):
            try:
                self.sample()
            except Exception as error:
                self.monitor_failures.append(str(error))
                return

    def request(self, name, expected=200, delta=1, body=b"", path="/", headers=None,
                rule=None, phase=None, connection=None, safe_postcommit=False, expected_body=None,
                response_overlimit=False):
        token = "q-" + os.urandom(12).hex()
        self.guard("verify-running", "--evidence", str(self.root / "identity.json"))
        selected = {"X-Qualification-ID": token, "Content-Type": "text/plain"}
        selected.update(headers or {})
        client = connection or http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        client.response_class = StrictHTTPResponse
        try:
            client.request("POST" if body else "GET", path, body=body, headers=selected)
            response = client.getresponse()
            received = (bounded_overlimit_body(response, name) if response_overlimit
                        else bounded_response_body(response, name))
            if not response_overlimit and response.status != expected:
                raise RuntimeError(f"unexpected bounded response: {name} {response.status}")
            if expected_body is not None and (received != expected_body or not response.isclosed()):
                raise RuntimeError(f"unexpected response body or incomplete framing: {name}")
            with self.origin.lock:
                reached = self.origin.receipts.get(token, 0)
            if reached != delta:
                raise RuntimeError(f"origin receipt multiplicity mismatch: {name}")
            observed = events(self.root / "events.jsonl", token)
            if response_overlimit:
                if (name != "response-body-1025" or path != "/response/1025"
                        or expected is not None or delta != 1 or body or connection is not None):
                    raise RuntimeError("response-overlimit requires exact one-bucket fixture")
                assert_response_overlimit(observed, response.qualification_wire["branch"])
            elif safe_postcommit:
                if expected != 200 or delta != 1 or expected_body != b"qualification-p4-deny":
                    raise RuntimeError("Safe P4 requires exact visible status, origin and body contract")
                assert_phase4_safe(observed)
            elif rule is not None or expected in (200, 400):
                # The HTTPD header parser's 400 is a host rejection before
                # connector evaluation. Its correlated event set must be
                # empty, just like a non-intervening Allow.
                assert_decision(observed, rule, phase, expected)
            elif expected == 413:
                assert_decision(observed, None, "request_body", expected, body_limit=True)
            else:
                raise RuntimeError("unsupported qualification decision status")
            self.sample()
            if self.monitor_failures:
                raise RuntimeError("resource monitor failed: " + self.monitor_failures[0])
            result = {"case": name, "token": token, "status": response.status, "backend_delta": reached,
                    "events": observed, "pid": self.pid, "response_body_bytes": len(received),
                    "response_body_sha256": hashlib.sha256(received).hexdigest(),
                    "response_framing_complete": response.isclosed() and response.length in (0, None)}
            if response_overlimit:
                result.update(response_declared_bytes=int(response.headers["Content-Length"]),
                              response_remaining_bytes=response.length,
                              response_termination=response.qualification_wire["termination"],
                              response_overlimit_branch=response.qualification_wire["branch"])
            with self.resource_lock:
                self.case_results.append(result)
            return result
        except Exception as error:
            diagnostic = {"case": name, "token": token, "failure": describe_failure(error)}
            if "response" in locals() and hasattr(response, "qualification_wire"):
                diagnostic["wire"] = response.qualification_wire
            # Retain observed attributable side effects of a failed attempt.
            # This never turns it into a successful case, and unknown/late
            # records remain fatal in the complete post-stop comparison.
            with self.origin.lock:
                diagnostic["backend_delta"] = self.origin.receipts.get(token, 0)
            diagnostic["events"] = []
            try:
                diagnostic["events"] = events(self.root / "events.jsonl", token)
            except Exception as observation_error:
                diagnostic["observation_failure"] = describe_failure(observation_error)
            with self.resource_lock:
                getattr(self, "probe_failures", []).append(diagnostic)
            raise
        finally:
            if connection is None:
                client.close()

    def stop(self):
        self.monitor_stop.set()
        if hasattr(self, "monitor"):
            self.monitor.join(timeout=2)
        try:
            if self.process is not None:
                liveness_error = None
                try:
                    if self.process.poll() is not None:
                        raise RuntimeError("Apache controller exited before controlled stop")
                    self.guard("verify-running", "--evidence", str(self.root / "identity.json"))
                    self.sample()
                    verify_inputs(self.args)
                except Exception as error:
                    liveness_error = error
                if (self.root / "supervisor.json").exists():
                    self.control.sendall(b"stop\n")
                if self.process.wait(timeout=12) != 0:
                    raise RuntimeError("Apache supervisor controller cleanup failed")
                if (self.root / "identity.json").exists():
                    self.guard("verify-stopped", "--evidence", str(self.root / "identity.json"))
                else:
                    raise RuntimeError("cleanup lacks launch-bound host identity")
                assert_controlled_exit(json.loads(bounded_read(self.root / "httpd-exit.json")), self.pid)
                if liveness_error is not None:
                    raise RuntimeError("host liveness/identity failed immediately before stop") from liveness_error
        finally:
            if hasattr(self, "launch_log"):
                self.launch_log.close()
            if hasattr(self, "control"):
                self.control.close()
        reconcile_logs(self.root, self.case_results)
        verify_inputs(self.args)
        with self.origin.lock:
            receipts = {key: value for key, value in self.origin.receipts.items()
                        if key not in self.origin_baseline}
            if any(self.origin.receipts.get(key) != value for key, value in self.origin_baseline.items()):
                raise RuntimeError("late origin receipt from prior start")
            errors = self.origin.errors[self.origin_error_baseline:]
        reconcile_final(self.root, self.case_results + self.probe_failures, receipts, errors)
        if self.monitor_failures:
            raise RuntimeError("resource monitor failed: " + self.monitor_failures[0])


def exercise_keepalive(host: Host) -> list[dict]:
    results = []
    client = http.client.HTTPConnection("127.0.0.1", host.port, timeout=3)
    try:
        client.connect()
        original = client.sock
        sequence = (("allow-before", {}),
                    ("p1-deny", {"expected": 403, "delta": 0,
                                 "headers": {"X-Qualification-P1": "deny"},
                                 "rule": "991001", "phase": "request_headers"}),
                    ("allow-after-p1", {}),
                    ("p2-deny", {"expected": 403, "delta": 0,
                                 "body": b"qualification-p2-deny",
                                 "rule": "991002", "phase": "request_body"}),
                    ("allow-after-p2", {}))
        for name, arguments in sequence:
            results.append(host.request("keepalive-" + name, connection=client, **arguments))
            if client.sock is not original or original.fileno() < 0:
                raise RuntimeError("keepalive reconnected or closed the original socket")
    finally:
        client.close()
    return results


def exercise(host: Host, extended: bool) -> list[dict]:
    results = [host.request("allow"), host.request("p1", 403, 0,
               headers={"X-Qualification-P1": "deny"}, rule="991001", phase="request_headers"),
               host.request("p2", 403, 0, body=b"qualification-p2-deny",
                            rule="991002", phase="request_body")]
    if not extended:
        return results
    for size in (LIMIT - 1, LIMIT, LIMIT + 1):
        results.append(host.request(f"request-body-{size}", 413 if size > LIMIT else 200,
                                    0 if size > LIMIT else 1, body=b"x" * size))
    results.append(host.request("error-followup-allow"))
    # HTTPD 2.4.68 server/protocol.c ap_get_mime_headers_core passes the
    # directive + 2 to ap_rgetline_core. Its CRLF completion strips both bytes
    # and permits LF beyond n when CR was buffered: directive 256 therefore
    # admits a 257-byte name/separator/value line (259 bytes including CRLF).
    # Probe that exact parser boundary, with a mandatory 258-byte rejection.
    for size in (256, 257, 258):
        boundary = host.request(f"header-line-{size}", 400 if size == 258 else 200,
                                0 if size == 258 else 1,
                                headers={"X-Boundary": "x" * (size - len("X-Boundary: "))})
        boundary.update(header_line_bytes_before_crlf=size, header_line_bytes_with_crlf=size + 2,
                        configured_field_size=256,
                        parser_contract="httpd-2.4.68-ap-rgetline-core-crlf")
        results.append(boundary)
    results.append(host.request("p3", 403, 1, path="/p3", rule="991003", phase="response_headers"))
    # Progressive Apache forwards the body prefix before evaluating P4 at EOS.
    # Safe therefore preserves the visible 200 and records the exact late deny.
    results.append(host.request("p4-safe-postcommit", 200, 1, path="/p4", safe_postcommit=True,
                                expected_body=b"qualification-p4-deny"))
    results.append(host.request("response-body-0", 200, path="/response/0", expected_body=b""))
    results.append(host.request("response-legacy-connector-budget-bypass",
                                path=f"/response/{LEGACY_CONNECTOR_LIMIT + 1}",
                                expected_body=b"x" * (LEGACY_CONNECTOR_LIMIT + 1)))
    for size in (LIMIT - 1, LIMIT, LIMIT + 1):
        results.append(host.request(f"response-body-{size}", None if size > LIMIT else 200,
                                    path=f"/response/{size}",
                                    expected_body=b"x" * size if size <= LIMIT else None,
                                    response_overlimit=size > LIMIT))
    results.append(host.request("response-error-followup-allow"))
    results.extend(exercise_keepalive(host))
    barrier = threading.Barrier(4, timeout=3)
    host.origin.parallel_barrier = threading.Barrier(4)

    def concurrent(index):
        barrier.wait()
        return host.request(f"parallel-{index}", path="/parallel",
                            headers={"X-Qualification-Parallel": host.origin.parallel_secret})

    with ThreadPoolExecutor(max_workers=4) as pool:
        results.extend(pool.map(concurrent, range(4)))
    if host.origin.parallel_peak < 4 or host.origin.parallel_errors:
        raise RuntimeError("four native requests did not overlap at the origin")
    return results


def describe_failure(error):
    if isinstance(error, BaseExceptionGroup):
        return type(error).__name__ + ": " + "; ".join(describe_failure(item) for item in error.exceptions)
    return type(error).__name__ + ": " + str(error)


def run_host_campaign(host, extended):
    primary = None
    results = None
    try:
        host.start()
        results = exercise(host, extended)
        private_write(host.root / "maps.txt", host.sample())
    except Exception as error:
        primary = error
    try:
        host.stop()
    except Exception as cleanup:
        if primary is not None:
            raise ExceptionGroup("Apache probe and cleanup both failed", [primary, cleanup])
        raise
    if primary is not None:
        raise primary
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--httpd", required=True, type=trusted_file)
    parser.add_argument("--module", required=True, type=trusted_file)
    parser.add_argument("--modules-config", required=True, type=trusted_file,
                        help="trusted build-owned native Apache module-load config")
    parser.add_argument("--library", required=True, type=trusted_file)
    parser.add_argument("--library-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if os.geteuid() == 0 or os.getegid() == 0:
        parser.error("run qualification under an approved unprivileged UID/GID; root cannot receive a pass")
    if not re.fullmatch(r"[0-9a-f]{64}", args.library_sha256) or digest(args.library) != args.library_sha256:
        parser.error("library digest mismatch")
    args.input_pins = {key: input_identity(getattr(args, key))
                       for key in ("httpd", "module", "modules_config", "library")}
    if args.input_pins["library"]["sha256"] != args.library_sha256:
        parser.error("library changed while pinning inputs")
    approved = Path("/var/tmp/codex/ModSecurity-conector")
    if not args.output.is_absolute() or args.output.parent.resolve() != args.output.parent or approved not in args.output.parents:
        parser.error("output must be a new canonical directory beneath the external project root")
    try:
        config_path(str(args.output))
        os.close(directory_fd(args.output.parent))
        os.close(directory_fd(approved))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    os.umask(0o077)
    private_mkdir(args.output)
    report = {"profile": "apache-native", "status": "failed", "full_b_acceptance": False,
              "remaining_gaps": ["late-commit-safe-and-strict", "engine-fault-injection", "full-security-error-matrix"],
              "build_target": "make build-apache", "starts": [], "cases": [], "cleanup_verified": False,
              "inputs": {key: {"path": str(getattr(args, key)), **identity}
                         for key, identity in args.input_pins.items()}}
    origin = Origin()
    thread = threading.Thread(target=origin.serve_forever, daemon=True)
    thread.start()
    hosts = []
    try:
        for index in range(4):
            host = Host(args, args.output / f"start-{index}", origin)
            hosts.append(host)
            if index == 3:
                host.port = restart_port
            report["cases"].extend(run_host_campaign(host, index == 2))
            report["starts"].append({"identity": json.loads(bounded_read(host.root / "identity.json")),
                                     "module_identity": args.input_pins["module"],
                                     "resources": host.resources, "serving_identity": host.serving_identity,
                                     "cleanup_verified": True})
            restart_port = host.port
        report["controlled_stop_start_verified"] = True
        report["restart_listener_port"] = restart_port
        verify_inputs(args)
        report["status"] = "passed"
    except Exception as error:
        report["failure"] = describe_failure(error)
    finally:
        origin_cleaned = False
        try:
            origin.shutdown()
            try:
                origin.close_handlers()
            finally:
                origin.server_close()
                thread.join(timeout=3)
            origin_cleaned = not thread.is_alive() and origin.socket.fileno() == -1
            # Reconcile again after every origin handler is reaped: a receipt
            # arriving after an earlier host stop must not escape acceptance.
            all_cases = [case for item in hosts for case in item.case_results + item.probe_failures]
            wanted = {case["token"]: case["backend_delta"] for case in all_cases if case["backend_delta"]}
            if origin.receipts != wanted or origin.errors or origin.parallel_errors:
                raise RuntimeError("post-cleanup origin reconciliation failed")
            for item in hosts:
                records = item.case_results + item.probe_failures
                selected = {case["token"]: origin.receipts[case["token"]]
                            for case in records if case["backend_delta"]}
                reconcile_final(item.root, records, selected, [])
                reconcile_logs(item.root, item.case_results)
            verify_inputs(args)
        except Exception as error:
            report["status"] = "failed"
            report["cleanup_failure"] = describe_failure(error)
        report["cases"] = [case for item in hosts for case in item.case_results]
        report["failed_probes"] = [probe for item in hosts for probe in item.probe_failures]
        report["origin_parallel_peak"] = origin.parallel_peak
        report["origin_cleanup_verified"] = origin_cleaned
        report["cleanup_verified"] = len(report["starts"]) == 4 and origin_cleaned
        private_write(args.output / "qualification.json", json.dumps(report, indent=2) + "\n")
    return 0 if report["status"] == "passed" and report["cleanup_verified"] else 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--supervisor-control-fd":
        raise SystemExit(supervisor_controller(int(sys.argv[2])))
    raise SystemExit(main())
