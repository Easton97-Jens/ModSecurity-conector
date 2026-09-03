#!/usr/bin/env python3
"""Linux-only identity, pidfd, and listener guards for the close harness."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import errno
import json
import os
from pathlib import Path
import resource
import re
import signal
import stat
import sys
import time


class GuardFailure(RuntimeError):
    """A process or listener cannot be safely attributed to this harness."""


class PidfdTargetExited(GuardFailure):
    """The pidfd target died or became a zombie before a pidfd was acquired."""


PIDFD_TARGET_EXIT_STATUS = 75


@dataclass(frozen=True)
class RegisteredSession:
    leader_pid: int
    leader_start_time: str
    session_id: int
    process_group: int


@dataclass
class OpenSessionMember:
    pid: int
    start_time: str
    session_id: int
    process_group: int
    pidfd: int


@dataclass(frozen=True)
class LeaderAnchor:
    is_live: bool
    is_registered_member: bool


MAX_PROC_SCAN_ENTRIES = 4096
MAX_SESSION_MEMBERS = 256
MAX_TASK_FD_ENTRIES = 4096
MAX_GUARD_ERRORS = 16
MAX_GUARD_ERROR_TEXT = 192
MAX_GUARD_ERROR_SUMMARY = 1024
MAX_RECORDED_MEMBER_IDS = 512
MAX_KILL_RESCANS = 64
MAX_SESSION_WAIT_RESCANS = 1024
MAX_SESSION_ABSENCE_RESCANS = 1024
MAX_ABORT_EVENT_RESCANS = 1024
MAX_TCP_LISTENER_LINES = 4096
MAX_TCP_LISTENER_LINE_BYTES = 4096
_ERROR_OVERFLOW = "additional task-guard errors suppressed"
MIN_BACKEND_READ_TIMEOUT_SECONDS = 1
MAX_BACKEND_READ_TIMEOUT_SECONDS = 30


def _private_artifact_path(path: Path) -> Path:
    """Validate a task-owned artifact path before any filesystem operation."""

    if not path.is_absolute() or path.name in ("", ".", ".."):
        raise GuardFailure("task artifact path must be absolute and have a filename")
    try:
        parent_mode = os.lstat(path.parent).st_mode
        target_mode = os.lstat(path).st_mode
    except FileNotFoundError:
        target_mode = None
        try:
            parent_mode = os.lstat(path.parent).st_mode
        except OSError as exc:
            raise GuardFailure("task artifact parent cannot be inspected") from exc
    except OSError as exc:
        raise GuardFailure("task artifact path cannot be inspected") from exc
    if not stat.S_ISDIR(parent_mode) or stat.S_ISLNK(parent_mode) or parent_mode & 0o077:
        raise GuardFailure("task artifact parent must be a private real directory")
    if target_mode is not None and stat.S_ISLNK(target_mode):
        raise GuardFailure("task artifact must not be a symbolic link")
    return path


def _proc_stat_path(pid: int) -> Path:
    if type(pid) is not int or not 1 <= pid <= 4_000_000_000:
        raise GuardFailure("process ID is outside the bounded Linux range")
    return Path("/proc") / str(pid) / "stat"


def _bounded_error_text(value: object) -> str:
    message = str(value)
    if len(message) > MAX_GUARD_ERROR_TEXT:
        return message[: MAX_GUARD_ERROR_TEXT - 3] + "..."
    return message


def _append_error(errors: list[str], value: object) -> None:
    """Retain bounded, deduplicated diagnostics without unbounded error text."""

    message = _bounded_error_text(value)
    if message in errors:
        return
    if len(errors) < MAX_GUARD_ERRORS:
        errors.append(message)
        return
    overflow_marker = _bounded_error_text(_ERROR_OVERFLOW)
    if errors and errors[-1] != overflow_marker:
        errors[-1] = overflow_marker


def _append_member_ids(
    destination: list[int],
    additions: list[int],
    errors: list[str],
    overflow_message: str,
) -> None:
    """Keep task-member receipts bounded while preserving fail-closed evidence."""

    for member_pid in additions:
        if member_pid in destination:
            continue
        if len(destination) >= MAX_RECORDED_MEMBER_IDS:
            _append_error(errors, overflow_message)
            return
        destination.append(member_pid)


def _error_summary(errors: list[str]) -> str:
    """Return a bounded error aggregate suitable for a fail-closed receipt."""

    summary = "; ".join(errors[:MAX_GUARD_ERRORS])
    if len(summary) > MAX_GUARD_ERROR_SUMMARY:
        return summary[: MAX_GUARD_ERROR_SUMMARY - 3] + "..."
    return summary


def _require_pidfd() -> None:
    if sys.platform != "linux" or not hasattr(os, "pidfd_open") or not hasattr(signal, "pidfd_send_signal"):
        raise GuardFailure("Linux os.pidfd_open and signal.pidfd_send_signal are required")
    self_pid = os.getpid()
    try:
        pidfd = os.pidfd_open(self_pid, 0)
    except OSError as exc:
        raise GuardFailure("Linux pidfd capability is unavailable or unusable") from exc
    try:
        _pidfd_matches_pid(pidfd, self_pid)
        # Signal 0 verifies the pidfd-backed signal path without changing state.
        signal.pidfd_send_signal(pidfd, 0)
    except (GuardFailure, OSError, TypeError) as exc:
        try:
            os.close(pidfd)
        except OSError:
            pass
        raise GuardFailure("Linux pidfd capability is unavailable or unusable") from exc
    try:
        os.close(pidfd)
    except OSError as exc:
        raise GuardFailure("Linux pidfd capability is unavailable or unusable") from exc


def _write_new(path: Path, payload: bytes) -> None:
    path = _private_artifact_path(path)
    try:
        parent_mode = os.lstat(path.parent).st_mode
        if not stat.S_ISDIR(parent_mode) or stat.S_ISLNK(parent_mode) or parent_mode & 0o077:
            raise GuardFailure("refusing to write outside a private real task directory")
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(descriptor, "wb") as output:
            output.write(payload)
    except OSError as exc:
        raise GuardFailure("cannot safely create a no-overwrite task artifact") from exc


def _lighttpd_string(path: str) -> str:
    if not path.startswith("/") or any(character in path for character in ("\x00", "\r", "\n")):
        raise GuardFailure("lighttpd config path is unsafe")
    return path.replace("\\", "\\\\").replace('"', '\\"')


def _runtime_config_path(path: str) -> str:
    if not path.startswith("/") or any(character in path for character in ("\x00", "\r", "\n", "=", "#", ";")):
        raise GuardFailure("runtime config path is unsafe")
    return path


def write_config(
    root: Path,
    rules_file: str,
    frontend_port: int,
    upstream_port: int,
    backend_read_timeout: int | None = None,
) -> None:
    try:
        root_mode = os.lstat(root).st_mode
    except OSError as exc:
        raise GuardFailure("runtime root cannot be inspected") from exc
    if not root.is_absolute() or not stat.S_ISDIR(root_mode) or stat.S_ISLNK(root_mode) or root_mode & 0o077:
        raise GuardFailure("runtime root must be a private real directory")
    if not 1024 <= frontend_port <= 65535 or not 1024 <= upstream_port <= 65535:
        raise GuardFailure("ports must be unprivileged")
    if backend_read_timeout is not None and (
        type(backend_read_timeout) is not int
        or not MIN_BACKEND_READ_TIMEOUT_SECONDS <= backend_read_timeout <= MAX_BACKEND_READ_TIMEOUT_SECONDS
    ):
        raise GuardFailure("backend read timeout must be an integer between 1 and 30 seconds")
    document_root = root / "document-root"
    upload_root = root / "upload"
    document_root.mkdir(mode=0o700)
    upload_root.mkdir(mode=0o700)
    runtime_config = root / "msconnector-runtime.conf"
    lighttpd_config = root / "lighttpd.conf"
    event_path = root / "events.jsonl"
    error_log = root / "lighttpd-error.log"
    pid_file = root / "lighttpd.pid"
    escaped = {name: _lighttpd_string(str(path)) for name, path in {
        "document_root": document_root,
        "upload_root": upload_root,
        "runtime_config": runtime_config,
        "event_path": event_path,
        "error_log": error_log,
        "pid_file": pid_file,
    }.items()}
    rules = _runtime_config_path(rules_file)
    runtime_event_path = _runtime_config_path(str(event_path))
    backend_read_timeout_setting = (
        f', "read-timeout" => {backend_read_timeout}' if backend_read_timeout is not None else ""
    )
    _write_new(
        runtime_config,
        (
            "enabled=on\n"
            f"rules_file={rules}\n"
            "transaction_id_header=x-modsec-transaction-id\n"
            "request_body_mode=none\n"
            "response_body_mode=streaming\n"
            "request_body_limit=1048576\n"
            "response_body_limit=1048576\n"
            "default_block_status=403\n"
            "default_error_status=500\n"
            "max_header_count=256\n"
            "max_header_name_size=256\n"
            "max_header_value_size=8192\n"
            "max_total_header_bytes=65536\n"
            "max_event_json_bytes=16384\n"
            f"event_path={runtime_event_path}\n"
        ).encode("utf-8"),
    )
    _write_new(
        lighttpd_config,
        (
            'server.compat-module-load = "disable"\n'
            'server.modules = ( "mod_proxy", "mod_msconnector" )\n'
            'server.stream-response-body = 1\n'
            f'server.document-root = "{escaped["document_root"]}"\n'
            'server.bind = "127.0.0.1"\n'
            f"server.port = {frontend_port}\n"
            f'server.errorlog = "{escaped["error_log"]}"\n'
            f'server.pid-file = "{escaped["pid_file"]}"\n'
            f'server.upload-dirs = ( "{escaped["upload_root"]}" )\n'
            'msconnector.enabled = "enable"\n'
            f'msconnector.config-file = "{escaped["runtime_config"]}"\n'
            'msconnector.expose-host-transaction-id = "enable"\n'
            "proxy.server = (\n"
            f'  "/p4/close/" => ( ( "host" => "127.0.0.1", "port" => {upstream_port}'
            f"{backend_read_timeout_setting} ) )\n"
            ")\n"
        ).encode("utf-8"),
    )


def _session_fields(pid: int) -> tuple[int, int]:
    try:
        stat_data = _proc_stat_path(pid).read_text(encoding="ascii")
        after_comm = stat_data.rsplit(")", 1)[1].split()
        return int(after_comm[2]), int(after_comm[3])
    except (OSError, IndexError, ValueError) as exc:
        raise GuardFailure(f"cannot parse /proc/{pid}/stat session fields") from exc


def _scan_session_members(session_id: int) -> tuple[list[int], list[str]]:
    """Return observable session members and every non-disappearance read failure.

    A `/proc` entry may disappear between directory enumeration and stat parsing.
    That one race is harmless.  Every other parse or inspection failure is retained
    so callers can fail closed after attempting containment of the members that
    were still provably in the registered task session.
    """

    members: list[int] = []
    errors: list[str] = []
    try:
        entries = Path("/proc").iterdir()
    except OSError:
        _append_error(errors, "cannot enumerate /proc for task session containment")
        return members, errors
    scanned_entries = 0
    try:
        for entry in entries:
            scanned_entries += 1
            if scanned_entries > MAX_PROC_SCAN_ENTRIES:
                _append_error(errors, "bounded /proc task-session scan limit exceeded")
                break
            if not entry.name.isdigit():
                continue
            try:
                _pgrp, member_session = _session_fields(int(entry.name))
            except GuardFailure as exc:
                try:
                    os.lstat(entry)
                except FileNotFoundError:
                    # The process exited while the scan was in flight; it cannot be
                    # signalled and does not make membership ambiguous.
                    continue
                except OSError as inspect_exc:
                    _append_error(errors, f"cannot revalidate /proc/{entry.name}: {inspect_exc}")
                    continue
                _append_error(errors, exc)
                continue
            if member_session == session_id:
                if len(members) >= MAX_SESSION_MEMBERS:
                    _append_error(errors, "bounded task-session member limit exceeded")
                    continue
                members.append(int(entry.name))
    except OSError:
        _append_error(errors, "cannot continue /proc task-session enumeration")
    return sorted(members), errors


def _session_members(session_id: int, strict: bool = False) -> list[int]:
    members, errors = _scan_session_members(session_id)
    if strict and errors:
        raise GuardFailure("cannot fully inspect task session membership: " + _error_summary(errors))
    return members


def _process_state(pid: int) -> str | None:
    try:
        stat_data = _proc_stat_path(pid).read_text(encoding="ascii")
    except OSError as exc:
        # Enumeration and the state read are separate operations.  ENOENT is
        # the expected process-exit race; all other read failures remain
        # fail-closed and are reported to the caller.
        if exc.errno == errno.ENOENT:
            return None
        raise GuardFailure(
            f"cannot read /proc/{pid}/stat process state (errno={exc.errno} {exc.strerror})"
        ) from exc
    try:
        return stat_data.rsplit(")", 1)[1].split()[0]
    except (IndexError, UnicodeError) as exc:
        raise GuardFailure(f"cannot parse /proc/{pid}/stat process state") from exc


def _active_session_members(session_id: int) -> tuple[list[int], list[str]]:
    members, errors = _scan_session_members(session_id)
    active: list[int] = []
    for member_pid in members:
        try:
            state = _process_state(member_pid)
        except GuardFailure as exc:
            _append_error(errors, exc)
            # An uninspectable member must not be mistaken for a clean exit.
            active.append(member_pid)
            continue
        if state not in (None, "Z"):
            active.append(member_pid)
    return active, errors


def _task_fd_entries(pid: int) -> list[Path]:
    entries: list[Path] = []
    try:
        for entry in Path(f"/proc/{pid}/fd").iterdir():
            if len(entries) >= MAX_TASK_FD_ENTRIES:
                raise GuardFailure("bounded task process FD inspection limit exceeded")
            entries.append(entry)
    except OSError as exc:
        raise GuardFailure("cannot inspect process file descriptors") from exc
    return entries


def assert_singleton_session(pid: int, expected_start: str, expected_exe: str) -> dict[str, object]:
    pidfd = _pidfd_for_identity(pid, expected_start, expected_exe)
    try:
        process_group, session_id = _session_fields(pid)
        if process_group != pid or session_id != pid:
            raise GuardFailure("task host is not its own session and process-group leader")
        members = _session_members(session_id, strict=True)
        if members != [pid]:
            raise GuardFailure("task session contains unexpected processes")
        fd_count = len(_task_fd_entries(pid))
        _validate_identity(pid, expected_start, expected_exe)
        return {"session_id": session_id, "members": members, "fd_count": fd_count}
    finally:
        os.close(pidfd)


def assert_session_absent(session_id: int, wait_seconds: float = 0.0) -> None:
    if not 0.0 <= wait_seconds <= 30.0:
        raise GuardFailure("session-absence wait bound is invalid")
    deadline = time.monotonic() + wait_seconds
    for _rescan_number in range(MAX_SESSION_ABSENCE_RESCANS):
        members, errors = _active_session_members(session_id)
        if errors:
            raise GuardFailure("cannot fully inspect task session membership: " + _error_summary(errors))
        if not members:
            return
        if time.monotonic() >= deadline:
            raise GuardFailure("task session still contains processes")
        time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))
    raise GuardFailure("bounded task-session absence rescan limit exceeded")


def assert_no_unix_sockets(root: Path) -> None:
    if not root.is_dir() or root.is_symlink():
        raise GuardFailure("runtime root is not a real directory")
    for parent, directories, files in os.walk(root, followlinks=False):
        for name in [*directories, *files]:
            candidate = Path(parent) / name
            if stat.S_ISSOCK(os.lstat(candidate).st_mode):
                raise GuardFailure("task runtime root retains a unix-domain socket")


def _receipt_abort_evidence(receipt_path: Path) -> tuple[str, int]:
    receipt_path = _private_artifact_path(receipt_path)
    try:
        receipt_mode = os.lstat(receipt_path).st_mode
        if stat.S_ISLNK(receipt_mode) or not stat.S_ISREG(receipt_mode) or receipt_mode & 0o077:
            raise GuardFailure("raw receipt is not a private regular task artifact")
        if os.stat(receipt_path).st_size > 65536:
            raise GuardFailure("raw receipt exceeds its bounded inspection limit")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        transaction_id = receipt["host_transaction_id"]
        status = receipt["frontend_status"]
        content_length = receipt["frontend_content_length"]
        body_bytes = receipt["frontend_body_bytes"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise GuardFailure("cannot read bounded host transaction ID from receipt") from exc
    if not isinstance(transaction_id, str) or not re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", transaction_id):
        raise GuardFailure("host transaction ID is unsafe or outside the bounded format")
    if (
        type(status) is not int
        or type(content_length) is not int
        or type(body_bytes) is not int
        or status != 200
        or content_length != 64
        or body_bytes != 5
    ):
        raise GuardFailure("raw receipt does not contain the correlated 200/64/5 fixture")
    return transaction_id, body_bytes


def assert_abort_event(receipt_path: Path, error_log: Path, max_bytes: int, wait_seconds: float = 0.0) -> None:
    if not 1 <= max_bytes <= 1024 * 1024:
        raise GuardFailure("error-log inspection bound is invalid")
    if not 0.0 <= wait_seconds <= 30.0:
        raise GuardFailure("abort-event wait bound is invalid")
    transaction_id, expected_offset = _receipt_abort_evidence(receipt_path)
    event_pattern = re.compile(
        r"msconnector event=upstream_eof response-body-abort host-transaction-id="
        + re.escape(transaction_id)
        + r" offset=[0-9]+"
    )
    expected_pattern = re.compile(
        r"msconnector event=upstream_eof response-body-abort host-transaction-id="
        + re.escape(transaction_id)
        + r" offset=" + str(expected_offset)
    )
    deadline = time.monotonic() + wait_seconds
    last_error = "matching upstream_eof response-body-abort event is missing"
    for _rescan_number in range(MAX_ABORT_EVENT_RESCANS):
        try:
            error_mode = os.lstat(error_log).st_mode
            if stat.S_ISLNK(error_mode) or not stat.S_ISREG(error_mode) or error_mode & 0o077:
                raise GuardFailure("host error log is not a private regular task artifact")
            if os.stat(error_log).st_size > max_bytes:
                raise GuardFailure("host error log exceeds its bounded inspection limit")
            log_text = error_log.read_text(encoding="utf-8", errors="strict")
            event_lines = [
                line
                for line in log_text.splitlines()
                if re.search(r"(?:^|\s)" + event_pattern.pattern + r"\s*$", line)
            ]
            if len(event_lines) == 1 and re.search(
                r"(?:^|\s)" + expected_pattern.pattern + r"\s*$", event_lines[0]
            ):
                return
            last_error = (
                "multiple upstream_eof response-body-abort events were recorded for the host transaction"
                if len(event_lines) > 1
                else "matching upstream_eof response-body-abort event is missing"
            )
        except FileNotFoundError:
            last_error = "task-owned host error log is missing"
        except OSError as exc:
            raise GuardFailure("cannot read task-owned host error log") from exc
        except UnicodeError as exc:
            raise GuardFailure("task-owned host error log is not valid UTF-8") from exc
        if time.monotonic() >= deadline:
            raise GuardFailure(last_error)
        time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))
    raise GuardFailure("bounded upstream_eof abort-event rescan limit exceeded")


def signal_singleton_session(pid: int, expected_start: str, expected_exe: str, signal_number: int) -> None:
    assert_singleton_session(pid, expected_start, expected_exe)
    signal_owned(pid, expected_start, expected_exe, signal_number)


def _register_session(path: Path) -> None:
    leader_pid = os.getpid()
    process_group, session_id = _session_fields(leader_pid)
    if process_group != leader_pid or session_id != leader_pid:
        raise GuardFailure("exec-session did not create a unique task SID/PGID")
    _write_new(
        path,
        (
            json.dumps(
                {
                    "leader_pid": leader_pid,
                    "leader_start_time": _start_time(leader_pid),
                    "process_group": process_group,
                    "session_id": session_id,
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8"),
    )


def _registered_session(path: Path) -> RegisteredSession:
    try:
        record_mode = os.lstat(path).st_mode
        if stat.S_ISLNK(record_mode) or not stat.S_ISREG(record_mode) or record_mode & 0o077:
            raise GuardFailure("session registration is not a private regular task artifact")
        if os.stat(path).st_size > 16384:
            raise GuardFailure("session registration exceeds its bounded inspection limit")
        value = json.loads(path.read_text(encoding="utf-8"))
        record = RegisteredSession(
            leader_pid=value["leader_pid"],
            leader_start_time=value["leader_start_time"],
            process_group=value["process_group"],
            session_id=value["session_id"],
        )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise GuardFailure("cannot read registered task session") from exc
    if (
        type(record.leader_pid) is not int
        or type(record.process_group) is not int
        or type(record.session_id) is not int
        or not isinstance(record.leader_start_time, str)
        or not record.leader_start_time.isdecimal()
        or record.leader_pid <= 0
        or record.session_id != record.leader_pid
        or record.process_group != record.leader_pid
    ):
        raise GuardFailure("registered task SID/PGID is invalid")
    return record


def write_json(path: Path, fields: list[str]) -> None:
    value: dict[str, str] = {}
    for field in fields:
        key, separator, item = field.partition("=")
        if not separator or not key or key in value:
            raise GuardFailure("JSON fields must be unique key=value pairs")
        value[key] = item
    _write_new(path, (json.dumps(value, sort_keys=True) + "\n").encode("utf-8"))


def _validated_executable(value: str) -> str:
    """Accept only an owner-controlled executable with stable path identity."""

    executable = Path(value)
    if not executable.is_absolute() or executable.name in ("", ".", ".."):
        raise GuardFailure("session executable must be an absolute path")
    try:
        resolved = executable.resolve(strict=True)
        metadata = os.lstat(executable)
    except OSError as exc:
        raise GuardFailure("session executable cannot be inspected") from exc
    if resolved != executable or stat.S_ISLNK(metadata.st_mode):
        raise GuardFailure("session executable path must not contain symbolic links")
    if not stat.S_ISREG(metadata.st_mode) or not os.access(executable, os.X_OK):
        raise GuardFailure("session executable must be an executable regular file")
    if metadata.st_uid != os.geteuid() or metadata.st_mode & 0o022:
        raise GuardFailure("session executable must be owned by the runner and not group/world writable")
    return str(executable)


def exec_session(file_limit_blocks: int, command: list[str], session_record: Path | None = None) -> None:
    if not command or not 1 <= file_limit_blocks <= 2048:
        raise GuardFailure("session command or file limit is invalid")
    command = [_validated_executable(command[0]), *command[1:]]
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit_blocks * 512, file_limit_blocks * 512))
        os.setsid()
        if session_record is not None:
            _register_session(session_record)
        os.execv(command[0], command)
    except OSError as exc:
        raise GuardFailure("cannot create task-owned session or exec host") from exc


def _start_time(pid: int) -> str:
    try:
        stat = _proc_stat_path(pid).read_text(encoding="ascii")
    except OSError as exc:
        raise GuardFailure(f"cannot read /proc/{pid}/stat") from exc
    try:
        after_comm = stat.rsplit(")", 1)[1].split()
        return after_comm[19]
    except (IndexError, ValueError) as exc:
        raise GuardFailure(f"cannot parse /proc/{pid}/stat start time") from exc


def _validate_identity(pid: int, expected_start: str, expected_exe: str) -> None:
    if _start_time(pid) != expected_start:
        raise GuardFailure("process start time changed")
    try:
        actual_exe = os.path.realpath(f"/proc/{pid}/exe")
    except OSError as exc:
        raise GuardFailure(f"cannot resolve /proc/{pid}/exe") from exc
    if actual_exe != os.path.realpath(expected_exe):
        raise GuardFailure("process executable changed")


def _pidfd_matches_pid(pidfd: int, pid: int) -> None:
    try:
        fdinfo = Path(f"/proc/self/fdinfo/{pidfd}").read_text(encoding="ascii")
    except OSError as exc:
        raise GuardFailure("cannot inspect pidfd identity") from exc
    if f"Pid:\t{pid}\n" not in fdinfo:
        raise GuardFailure("pidfd no longer refers to the expected live pid")


def _open_pidfd(pid: int) -> int:
    _require_pidfd()
    try:
        pidfd = os.pidfd_open(pid, 0)
    except OSError as exc:
        # Never fall back to a numeric signal.  A config-check can finish in
        # the small interval after its shell-side liveness check, but an open
        # failure for any target that remains live is ambiguous and must fail
        # closed.
        try:
            target_state = _process_state(pid)
        except GuardFailure as state_exc:
            raise GuardFailure("cannot classify pidfd target after open failure") from state_exc
        if target_state in (None, "Z"):
            raise PidfdTargetExited("pidfd target exited before it could be opened") from exc
        raise GuardFailure("cannot open pidfd for a live target") from exc
    try:
        _pidfd_matches_pid(pidfd, pid)
        return pidfd
    except BaseException:
        os.close(pidfd)
        raise


def _pidfd_for_identity(pid: int, expected_start: str, expected_exe: str) -> int:
    pidfd = _open_pidfd(pid)
    try:
        _validate_identity(pid, expected_start, expected_exe)
        return pidfd
    except BaseException:
        os.close(pidfd)
        raise


def signal_owned(pid: int, expected_start: str, expected_exe: str, signal_number: int) -> None:
    pidfd = _pidfd_for_identity(pid, expected_start, expected_exe)
    try:
        signal.pidfd_send_signal(pidfd, signal_number)
    except OSError as exc:
        raise GuardFailure("pidfd signal failed") from exc
    finally:
        os.close(pidfd)


def _member_snapshot(member_pid: int, session: RegisteredSession) -> tuple[str, int, int]:
    start_time = _start_time(member_pid)
    process_group, session_id = _session_fields(member_pid)
    if session_id != session.session_id or process_group <= 0:
        raise GuardFailure("session member SID/PGID does not match the registered task session")
    if member_pid == session.leader_pid:
        if start_time != session.leader_start_time:
            raise GuardFailure("registered task leader start time changed within the task session")
        if process_group != session.process_group:
            raise GuardFailure("registered task leader PGID changed within the task session")
    return start_time, process_group, session_id


def _open_verified_session_member(member_pid: int, session: RegisteredSession) -> OpenSessionMember:
    pidfd = _open_pidfd(member_pid)
    try:
        first = _member_snapshot(member_pid, session)
        second = _member_snapshot(member_pid, session)
        if first != second:
            raise GuardFailure("session member identity changed while opening its pidfd")
        return OpenSessionMember(
            pid=member_pid,
            start_time=second[0],
            process_group=second[1],
            session_id=second[2],
            pidfd=pidfd,
        )
    except BaseException:
        os.close(pidfd)
        raise


def _member_is_current(member: OpenSessionMember, session: RegisteredSession) -> bool:
    if _process_state(member.pid) in (None, "Z"):
        return False
    try:
        _pidfd_matches_pid(member.pidfd, member.pid)
        signal.pidfd_send_signal(member.pidfd, 0)
    except OSError as exc:
        if exc.errno == errno.ESRCH:
            return False
        raise GuardFailure("cannot probe a verified task-session pidfd") from exc
    snapshot = _member_snapshot(member.pid, session)
    if snapshot != (member.start_time, member.process_group, member.session_id):
        raise GuardFailure("session member identity changed before pidfd signal")
    return True


def _validate_registered_leader(session: RegisteredSession, expected_exe: str) -> LeaderAnchor:
    state = _process_state(session.leader_pid)
    if state in (None, "Z"):
        return LeaderAnchor(is_live=False, is_registered_member=False)
    pidfd = _pidfd_for_identity(session.leader_pid, session.leader_start_time, expected_exe)
    try:
        process_group, session_id = _session_fields(session.leader_pid)
        return LeaderAnchor(
            is_live=True,
            is_registered_member=(
                process_group == session.process_group and session_id == session.session_id
            ),
        )
    finally:
        os.close(pidfd)


def _signal_registered_leader_if_live(
    session: RegisteredSession,
    expected_exe: str,
    signal_number: int,
) -> tuple[list[int], list[str]]:
    """Contain an identity-verified leader that has left the recorded session.

    The normal member scan handles the common case.  This fallback is only for
    a still-live registered leader which was not in that scan (or changed its
    PGID): its pidfd and original start time/executable remain a stronger proof
    of task ownership than a later session-field mismatch.  The mismatch still
    makes the run fail closed after this repair attempt.
    """

    errors: list[str] = []
    try:
        leader_state = _process_state(session.leader_pid)
    except GuardFailure as exc:
        _append_error(errors, exc)
        return [], errors
    if leader_state in (None, "Z"):
        return [], []
    try:
        pidfd = _pidfd_for_identity(
            session.leader_pid,
            session.leader_start_time,
            expected_exe,
        )
    except GuardFailure as exc:
        _append_error(errors, exc)
        return [], errors
    try:
        process_group, session_id = _session_fields(session.leader_pid)
        if process_group != session.process_group or session_id != session.session_id:
            _append_error(errors, "registered task leader SID/PGID changed")
        signal.pidfd_send_signal(pidfd, signal_number)
        return [session.leader_pid], errors
    except OSError as exc:
        if exc.errno == errno.ESRCH:
            return [], errors
        _append_error(errors, "pidfd signal failed for the registered task leader")
        return [], errors
    except GuardFailure as exc:
        _append_error(errors, exc)
        return [], errors
    finally:
        os.close(pidfd)


def _add_errors(errors: list[str], additions: list[str]) -> None:
    for addition in additions:
        _append_error(errors, addition)


def _signal_current_session_members(
    session: RegisteredSession,
    signal_number: int,
    deadline: float,
    excluded_pids: frozenset[int] = frozenset(),
) -> tuple[list[int], list[str]]:
    """Signal every observable member one pidfd at a time before the deadline.

    Keeping only one pidfd open at a time gives every member a pidfd-bound
    signal path without turning an unexpected child population into an
    unbounded FD allocation.  Membership is read only after the pidfd is open
    and is checked again immediately before that pidfd is used.
    """

    member_pids, errors = _scan_session_members(session.session_id)
    signaled: list[int] = []
    for member_pid in member_pids:
        if member_pid in excluded_pids:
            continue
        if time.monotonic() >= deadline:
            _append_error(errors, "bounded task-session pidfd signal deadline expired")
            break
        try:
            member_state = _process_state(member_pid)
        except GuardFailure as exc:
            _append_error(errors, exc)
            continue
        if member_state in (None, "Z"):
            continue
        try:
            member = _open_verified_session_member(member_pid, session)
        except GuardFailure as exc:
            try:
                member_state = _process_state(member_pid)
            except GuardFailure as state_exc:
                _append_error(errors, state_exc)
            else:
                if member_state not in (None, "Z"):
                    _append_error(errors, exc)
            continue
        try:
            if _member_is_current(member, session):
                signal.pidfd_send_signal(member.pidfd, signal_number)
                if len(signaled) >= MAX_RECORDED_MEMBER_IDS:
                    _append_error(errors, "bounded recorded task-member signal limit exceeded")
                    break
                signaled.append(member.pid)
        except OSError as exc:
            if exc.errno != errno.ESRCH:
                _append_error(errors, "pidfd signal failed for a verified task-session member")
        except GuardFailure as exc:
            _append_error(errors, exc)
        finally:
            os.close(member.pidfd)
    return signaled, errors


KILL_RESCAN_SECONDS = 0.05
TERM_EMPTY_CONFIRMATION_RESCANS = 6


def _wait_for_no_active_session_members(
    session_id: int,
    deadline: float,
    maximum_wait_seconds: float | None = None,
    excluded_pids: frozenset[int] = frozenset(),
    minimum_empty_rescans: int = 1,
) -> tuple[bool, list[str]]:
    if minimum_empty_rescans < 1:
        raise GuardFailure("session-empty confirmation bound is invalid")
    wait_deadline = deadline
    if maximum_wait_seconds is not None:
        wait_deadline = min(wait_deadline, time.monotonic() + maximum_wait_seconds)
    errors: list[str] = []
    empty_rescans = 0
    for _rescan_number in range(MAX_SESSION_WAIT_RESCANS):
        active_members, scan_errors = _active_session_members(session_id)
        _add_errors(errors, scan_errors)
        active_members = [member_pid for member_pid in active_members if member_pid not in excluded_pids]
        if not active_members:
            empty_rescans += 1
            if empty_rescans >= minimum_empty_rescans:
                return True, errors
        else:
            empty_rescans = 0
        if time.monotonic() >= wait_deadline:
            return False, errors
        time.sleep(min(0.05, max(0.0, wait_deadline - time.monotonic())))
    _append_error(errors, "bounded task-session wait rescan limit exceeded")
    return False, errors


def _kill_until_no_active_session_members(
    session: RegisteredSession,
    deadline: float,
    excluded_pids: frozenset[int] = frozenset(),
) -> tuple[list[int], bool, list[str]]:
    """Repeat bounded pidfd KILL snapshots so forked late members are contained."""

    signaled: list[int] = []
    errors: list[str] = []
    for _rescan_number in range(MAX_KILL_RESCANS):
        round_signaled, round_errors = _signal_current_session_members(
            session,
            signal.SIGKILL,
            deadline,
            excluded_pids,
        )
        _append_member_ids(
            signaled,
            round_signaled,
            errors,
            "bounded recorded task-member signal limit exceeded",
        )
        _add_errors(errors, round_errors)
        stopped, wait_errors = _wait_for_no_active_session_members(
            session.session_id,
            deadline,
            KILL_RESCAN_SECONDS,
            excluded_pids,
        )
        _add_errors(errors, wait_errors)
        if stopped:
            return signaled, True, errors
        if time.monotonic() >= deadline:
            return signaled, False, errors
    _append_error(errors, "bounded task-session KILL rescan limit exceeded")
    return signaled, False, errors


def terminate_registered_session(
    session_record: Path,
    expected_leader_exe: str,
    timeout_seconds: float,
) -> dict[str, object]:
    if not 0.1 <= timeout_seconds <= 30.0:
        raise GuardFailure("session cleanup timeout is outside the bounded range")
    session = _registered_session(session_record)
    initial_members, initial_errors = _scan_session_members(session.session_id)
    observed_members: list[int] = []
    cleanup_errors: list[str] = []
    _append_member_ids(
        observed_members,
        initial_members,
        cleanup_errors,
        "bounded recorded task-member inventory limit exceeded",
    )
    _add_errors(cleanup_errors, initial_errors)
    excluded_pids: frozenset[int] = frozenset()
    leader_signal_allowed = True
    try:
        leader_anchor = _validate_registered_leader(session, expected_leader_exe)
    except GuardFailure as exc:
        # A live leader whose start time or executable no longer matches might
        # be a reused numeric PID.  Never signal that numeric PID.  Continue
        # with independently pidfd-verified members of the recorded SID/PGID so
        # a dead original leader cannot strand its real task children.
        leader_signal_allowed = False
        excluded_pids = frozenset((session.leader_pid,))
        try:
            leader_state = _process_state(session.leader_pid)
        except GuardFailure as state_exc:
            _append_error(cleanup_errors, "registered task leader state is not safely inspectable")
            _append_error(cleanup_errors, state_exc)
            leader_state = None
        if leader_state not in (None, "Z"):
            _append_error(
                cleanup_errors,
                "registered task leader identity is not pidfd-verifiable; "
                "containing other verified task-session members only",
            )
        else:
            _append_error(cleanup_errors, exc)
        leader_anchor = LeaderAnchor(is_live=False, is_registered_member=False)
    if leader_anchor.is_live and not leader_anchor.is_registered_member:
        _append_error(cleanup_errors, "registered task leader SID/PGID changed")
    term_deadline = time.monotonic() + timeout_seconds
    term_signaled, term_errors = _signal_current_session_members(
        session,
        signal.SIGTERM,
        term_deadline,
        excluded_pids,
    )
    _add_errors(cleanup_errors, term_errors)
    _append_member_ids(
        observed_members,
        term_signaled,
        cleanup_errors,
        "bounded recorded task-member inventory limit exceeded",
    )
    if leader_signal_allowed and session.leader_pid not in term_signaled:
        leader_signaled, leader_signal_errors = _signal_registered_leader_if_live(
            session,
            expected_leader_exe,
            signal.SIGTERM,
        )
        _append_member_ids(
            term_signaled,
            leader_signaled,
            cleanup_errors,
            "bounded recorded task-member signal limit exceeded",
        )
        _append_member_ids(
            observed_members,
            leader_signaled,
            cleanup_errors,
            "bounded recorded task-member inventory limit exceeded",
        )
        _add_errors(cleanup_errors, leader_signal_errors)
    term_stopped, term_wait_errors = _wait_for_no_active_session_members(
        session.session_id,
        term_deadline,
        excluded_pids=excluded_pids,
        minimum_empty_rescans=TERM_EMPTY_CONFIRMATION_RESCANS,
    )
    _add_errors(cleanup_errors, term_wait_errors)
    kill_signaled: list[int] = []
    if not term_stopped:
        kill_deadline = time.monotonic() + timeout_seconds
        kill_signaled, kill_stopped, kill_errors = _kill_until_no_active_session_members(
            session,
            kill_deadline,
            excluded_pids,
        )
        _add_errors(cleanup_errors, kill_errors)
        _append_member_ids(
            observed_members,
            kill_signaled,
            cleanup_errors,
            "bounded recorded task-member inventory limit exceeded",
        )
        if leader_signal_allowed and session.leader_pid not in kill_signaled:
            leader_signaled, leader_signal_errors = _signal_registered_leader_if_live(
                session,
                expected_leader_exe,
                signal.SIGKILL,
            )
            _append_member_ids(
                kill_signaled,
                leader_signaled,
                cleanup_errors,
                "bounded recorded task-member signal limit exceeded",
            )
            _append_member_ids(
                observed_members,
                leader_signaled,
                cleanup_errors,
                "bounded recorded task-member inventory limit exceeded",
            )
            _add_errors(cleanup_errors, leader_signal_errors)
    else:
        kill_stopped = True
    if not kill_stopped:
        raise GuardFailure("task session retains active members after bounded TERM/KILL containment")
    if cleanup_errors:
        raise GuardFailure(
            "task session membership could not be fully verified for cleanup: "
            + _error_summary(cleanup_errors)
        )
    return {
        "initial_members": initial_members,
        "kill_signaled": kill_signaled,
        "process_group": session.process_group,
        "session_id": session.session_id,
        "term_signaled": term_signaled,
        "unexpected_members": sorted(
            member_pid for member_pid in observed_members if member_pid != session.leader_pid
        ),
    }


def _listen_table_inodes(
    table_path: Path,
    expected_port: str,
    accepted_local_addresses: set[str] | None,
    table_name: str,
) -> set[str]:
    """Read one bounded kernel TCP table and return matching LISTEN inodes."""
    if table_path.name == "tcp":
        address_width = 8
    elif table_path.name == "tcp6":
        address_width = 32
    else:
        raise GuardFailure(f"{table_name} has an unknown TCP table family")
    inodes: set[str] = set()
    try:
        with table_path.open("r", encoding="ascii", errors="strict") as table:
            header = table.readline(MAX_TCP_LISTENER_LINE_BYTES + 1)
            header_fields = header.split()
            if (
                not header.endswith("\n")
                or len(header_fields) < 4
                or header_fields[:2] != ["sl", "local_address"]
                or header_fields[2] not in {"rem_address", "remote_address"}
                or header_fields[3] != "st"
                or "inode" not in header_fields
            ):
                raise GuardFailure(f"{table_name} contains an invalid or incomplete header")
            if len(header) > MAX_TCP_LISTENER_LINE_BYTES and not header.endswith("\n"):
                raise GuardFailure(f"{table_name} header exceeds the bounded inspection limit")
            for _line_number in range(MAX_TCP_LISTENER_LINES):
                line = table.readline(MAX_TCP_LISTENER_LINE_BYTES + 1)
                if not line:
                    break
                if len(line) > MAX_TCP_LISTENER_LINE_BYTES and not line.endswith("\n"):
                    raise GuardFailure(f"{table_name} entry exceeds the bounded inspection limit")
                fields = line.split()
                if len(fields) <= 9:
                    raise GuardFailure(f"{table_name} contains a malformed nonblank row")
                local_address, separator, local_port = fields[1].partition(":")
                if (
                    not separator
                    or len(local_address) != address_width
                    or len(local_port) != 4
                    or any(character not in "0123456789ABCDEFabcdef" for character in local_address + local_port)
                ):
                    raise GuardFailure(f"{table_name} contains an invalid local endpoint")
                remote_address, remote_separator, remote_port = fields[2].partition(":")
                if (
                    not remote_separator
                    or len(remote_address) != address_width
                    or len(remote_port) != 4
                    or any(character not in "0123456789ABCDEFabcdef" for character in remote_address + remote_port)
                ):
                    raise GuardFailure(f"{table_name} contains an invalid remote endpoint")
                state = fields[3]
                if len(state) != 2 or any(character not in "0123456789ABCDEFabcdef" for character in state):
                    raise GuardFailure(f"{table_name} contains an invalid state field")
                inode = fields[9]
                if not inode or not inode.isdecimal():
                    raise GuardFailure(f"{table_name} contains an invalid inode field")
                if (
                    separator
                    and (accepted_local_addresses is None or local_address in accepted_local_addresses)
                    and local_port == expected_port
                    and state == "0A"
                ):
                    inodes.add(inode)
            else:
                if table.read(1):
                    raise GuardFailure(f"bounded {table_name} listener scan limit exceeded")
    except (OSError, UnicodeError) as exc:
        raise GuardFailure(f"cannot inspect {table_name}") from exc
    return inodes


def _listen_inodes_snapshot(host: str, port: int, include_ipv6: bool = False) -> set[str]:
    """Return LISTEN inodes without using a bind/TIME_WAIT probe."""
    if host != "127.0.0.1":
        raise GuardFailure("listener guard supports only 127.0.0.1")
    expected_port = f"{port:04X}"
    tcp_inodes = _listen_table_inodes(
        Path("/proc/net/tcp"),
        expected_port,
        {"0100007F", "00000000"},
        "/proc/net/tcp",
    )
    if len(tcp_inodes) > 1:
        raise GuardFailure("expected exactly one frontend LISTEN inode for the task port")
    if not include_ipv6:
        return tcp_inodes
    # /proc/net/tcp6 prints IPv6 addresses as 32 lower-case hex digits.  The
    # wildcard and loopback forms cover [::]:PORT and [::1]:PORT, including
    # both IPV6_V6ONLY settings.  A matching IPv6 listener is relevant even
    # when the task itself uses IPv4, so absence is fail-closed on both tables.
    tcp6_inodes = _listen_table_inodes(
        Path("/proc/net/tcp6"),
        expected_port,
        None,
        "/proc/net/tcp6",
    )
    return tcp_inodes | tcp6_inodes


def _listen_inodes(host: str, port: int, include_ipv6: bool = False) -> set[str]:
    inodes = _listen_inodes_snapshot(host, port, include_ipv6=include_ipv6)
    if not inodes:
        raise GuardFailure("expected frontend listener is absent")
    return inodes


def assert_listener_absent(host: str, port: int) -> None:
    """Fail closed if any listener remains after cleanup."""

    inodes = _listen_inodes_snapshot(host, port, include_ipv6=True)
    if inodes:
        raise GuardFailure("frontend listener remains after cleanup")


def _owned_listener_inodes(pid: int, inodes: set[str]) -> set[str]:
    """Return listener inodes still held by the exact task process."""

    owned_inodes: set[str] = set()
    for entry in _task_fd_entries(pid):
        try:
            target = os.readlink(entry)
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise GuardFailure("cannot inspect process file descriptor") from exc
        for inode in inodes:
            if target == f"socket:[{inode}]":
                owned_inodes.add(inode)
    return owned_inodes


def assert_listener_owned(pid: int, expected_start: str, expected_exe: str, host: str, port: int) -> None:
    pidfd = _pidfd_for_identity(pid, expected_start, expected_exe)
    try:
        # An independently-held IPv6 listener on the same port is an
        # ambiguous active endpoint and must fail closed during attribution.
        before_inodes = _listen_inodes(host, port, include_ipv6=True)
        if _owned_listener_inodes(pid, before_inodes) != before_inodes:
            raise GuardFailure("a frontend listener inode is not exclusively owned by the task host")
        after_inodes = _listen_inodes(host, port, include_ipv6=True)
        if after_inodes != before_inodes:
            raise GuardFailure("frontend listener changed during task-FD attribution")
        if _owned_listener_inodes(pid, after_inodes) != after_inodes:
            raise GuardFailure("frontend listener inode is no longer held by the task host")
        _validate_identity(pid, expected_start, expected_exe)
    finally:
        os.close(pidfd)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(dest="command", required=True)
    command.add_parser("check-pidfd")
    config = command.add_parser("write-config")
    config.add_argument("--root", type=Path, required=True)
    config.add_argument("--rules-file", required=True)
    config.add_argument("--frontend-port", type=int, required=True)
    config.add_argument("--upstream-port", type=int, required=True)
    config.add_argument("--backend-read-timeout", type=int)
    writer = command.add_parser("write-json")
    writer.add_argument("--output", type=Path, required=True)
    writer.add_argument("--field", action="append", default=[])
    executor = command.add_parser("exec-session")
    executor.add_argument("--file-limit-blocks", type=int, required=True)
    executor.add_argument("--session-record", type=Path)
    executor.add_argument("exec_argv", nargs=argparse.REMAINDER)
    session = command.add_parser("assert-session")
    session.add_argument("--pid", type=int, required=True)
    session.add_argument("--start-time", required=True)
    session.add_argument("--exe", required=True)
    session.add_argument("--output", type=Path)
    session_signal = command.add_parser("signal-session")
    session_signal.add_argument("--pid", type=int, required=True)
    session_signal.add_argument("--start-time", required=True)
    session_signal.add_argument("--exe", required=True)
    session_signal.add_argument("--signal", choices=("TERM", "KILL"), required=True)
    absent = command.add_parser("assert-session-absent")
    absent.add_argument("--session", type=int, required=True)
    absent.add_argument("--wait-seconds", type=float, default=0.0)
    cleanup = command.add_parser("cleanup-session")
    cleanup.add_argument("--session-record", type=Path, required=True)
    cleanup.add_argument("--leader-exe", required=True)
    cleanup.add_argument("--timeout-seconds", type=float, required=True)
    cleanup.add_argument("--output", type=Path)
    cleanup.add_argument("--reject-unexpected-members", action="store_true")
    sockets = command.add_parser("assert-no-uds")
    sockets.add_argument("--root", type=Path, required=True)
    abort = command.add_parser("assert-abort-event")
    abort.add_argument("--receipt", type=Path, required=True)
    abort.add_argument("--error-log", type=Path, required=True)
    abort.add_argument("--max-bytes", type=int, required=True)
    abort.add_argument("--wait-seconds", type=float, default=0.0)
    for name in ("signal", "assert-listener"):
        subparser = command.add_parser(name)
        subparser.add_argument("--pid", type=int, required=True)
        subparser.add_argument("--start-time", required=True)
        subparser.add_argument("--exe", required=True)
        if name == "signal":
            subparser.add_argument("--signal", choices=("TERM", "KILL"), required=True)
        else:
            subparser.add_argument("--host", required=True)
            subparser.add_argument("--port", type=int, required=True)
    listener_absent = command.add_parser("assert-listener-absent")
    listener_absent.add_argument("--host", required=True)
    listener_absent.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    try:
        if args.command == "check-pidfd":
            _require_pidfd()
        elif args.command == "write-config":
            write_config(
                args.root,
                args.rules_file,
                args.frontend_port,
                args.upstream_port,
                args.backend_read_timeout,
            )
        elif args.command == "write-json":
            write_json(args.output, args.field)
        elif args.command == "exec-session":
            if args.exec_argv and args.exec_argv[0] == "--":
                args.exec_argv = args.exec_argv[1:]
            exec_session(args.file_limit_blocks, args.exec_argv, args.session_record)
        elif args.command == "assert-session":
            inventory = assert_singleton_session(args.pid, args.start_time, args.exe)
            if args.output is not None:
                _write_new(args.output, (json.dumps(inventory, sort_keys=True) + "\n").encode("utf-8"))
        elif args.command == "assert-session-absent":
            assert_session_absent(args.session, args.wait_seconds)
        elif args.command == "cleanup-session":
            inventory = terminate_registered_session(
                args.session_record,
                args.leader_exe,
                args.timeout_seconds,
            )
            if args.output is not None:
                _write_new(args.output, (json.dumps(inventory, sort_keys=True) + "\n").encode("utf-8"))
            if args.reject_unexpected_members and inventory["unexpected_members"]:
                raise GuardFailure("task session contained unexpected members during cleanup")
        elif args.command == "assert-no-uds":
            assert_no_unix_sockets(args.root)
        elif args.command == "assert-abort-event":
            assert_abort_event(args.receipt, args.error_log, args.max_bytes, args.wait_seconds)
        elif args.command == "signal-session":
            signal_singleton_session(args.pid, args.start_time, args.exe, getattr(signal, f"SIG{args.signal}"))
        elif args.command == "signal":
            signal_owned(args.pid, args.start_time, args.exe, getattr(signal, f"SIG{args.signal}"))
        elif args.command == "assert-listener-absent":
            assert_listener_absent(args.host, args.port)
        else:
            assert_listener_owned(args.pid, args.start_time, args.exe, args.host, args.port)
    except PidfdTargetExited as exc:
        print(f"lighttpd_backend_close_linux_guard: EXITED {exc}", file=sys.stderr)
        return PIDFD_TARGET_EXIT_STATUS
    except GuardFailure as exc:
        print(f"lighttpd_backend_close_linux_guard: FAIL {exc}", file=sys.stderr)
        return 1
    print(f"lighttpd_backend_close_linux_guard: PASS {args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
