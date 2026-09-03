#!/usr/bin/env python3
"""Linux-only ownership guard for the Apache smoke host.

The guard deliberately uses a recorded /proc identity and listener inode.  A
numeric PID or a port is never sufficient to authorize a signal.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import select
import signal
from typing import Any


PROC = Path("/proc")
LISTEN = "0A"
MAX_PROC_ENTRIES = 4096
MAX_FD_ENTRIES = 4096
MAX_NET_ROWS = 4096
MAX_NET_BYTES = 4 * 1024 * 1024
MAX_NET_LINE = 4096
TERM_TIMEOUT = 2.0
KILL_TIMEOUT = 2.0


class GuardError(RuntimeError):
    pass


def _pidfd_available() -> bool:
    return callable(getattr(os, "pidfd_open", None)) and callable(
        getattr(signal, "pidfd_send_signal", None)
    )


def _pidfd_send_signal(fd: int, sig: int) -> None:
    signal.pidfd_send_signal(fd, sig)


def _pid_path(pid: int, name: str) -> Path:
    return PROC / str(pid) / name


def _stat(pid: int) -> dict[str, int]:
    raw = _pid_path(pid, "stat").read_text(encoding="ascii")
    close = raw.rfind(")")
    if close < 0:
        raise GuardError(f"malformed /proc/{pid}/stat")
    fields = raw[close + 2 :].split()
    # fields[0] is field 3 (state); pgrp/session/starttime are fields
    # 5/6/22, hence indexes 2/3/19 in this suffix.
    try:
        return {
            "pgrp": int(fields[2]),
            "session": int(fields[3]),
            "starttime": int(fields[19]),
        }
    except (IndexError, ValueError) as exc:
        raise GuardError(f"incomplete /proc/{pid}/stat") from exc


def _exe(pid: int) -> str:
    return os.path.realpath(os.readlink(_pid_path(pid, "exe")))


def _fd_inodes(pid: int) -> set[int]:
    result: set[int] = set()
    try:
        entries = os.scandir(_pid_path(pid, "fd"))
    except OSError as exc:
        raise GuardError(f"cannot inspect /proc/{pid}/fd: {exc}") from exc
    with entries:
        seen = 0
        for entry in entries:
            seen += 1
            if seen > MAX_FD_ENTRIES:
                raise GuardError("/proc fd scan exceeds bounded descriptor limit")
            try:
                target = os.readlink(entry.path)
            except OSError as exc:
                raise GuardError(f"cannot inspect {entry.path}: {exc}") from exc
            if target.startswith("socket:[") and target.endswith("]"):
                try:
                    result.add(int(target[8:-1]))
                except ValueError as exc:
                    raise GuardError(f"malformed socket descriptor {entry.path}") from exc
    return result


def _session_members(session: int, pgrp: int) -> list[int]:
    members: list[int] = []
    try:
        entries = os.scandir(PROC)
    except OSError as exc:
        raise GuardError(f"cannot scan {PROC}: {exc}") from exc
    with entries:
        seen = 0
        for entry in entries:
            seen += 1
            if seen > MAX_PROC_ENTRIES:
                raise GuardError("/proc scan exceeds bounded process-entry limit")
            if not entry.name.isdigit():
                continue
            candidate = int(entry.name)
            try:
                actual = _stat(candidate)
            except FileNotFoundError:
                continue
            except OSError as exc:
                raise GuardError(f"cannot inspect /proc/{candidate}/stat: {exc}") from exc
            if actual["session"] == session or actual["pgrp"] == pgrp:
                members.append(candidate)
    return members


def _listener_inodes(port: int) -> set[int]:
    if not 1 <= port <= 65535:
        raise GuardError("port is outside the TCP range")
    wanted = f"{port:04X}"
    result: set[int] = set()
    for name in ("net/tcp", "net/tcp6"):
        try:
            stream = (PROC / name).open(encoding="ascii")
        except OSError as exc:
            raise GuardError(f"cannot read {PROC / name}: {exc}") from exc
        with stream:
            try:
                next(stream)
                rows = 0
                total_bytes = 0
                for line in stream:
                    rows += 1
                    total_bytes += len(line)
                    if rows > MAX_NET_ROWS or total_bytes > MAX_NET_BYTES:
                        raise GuardError(f"{name} exceeds bounded listener scan")
                    if len(line) > MAX_NET_LINE:
                        raise GuardError(f"oversized listener row in {name}")
                    if not line.strip():
                        continue
                    fields = line.split()
                    # With whitespace tokenization, the kernel's listener
                    # inode is field 9. Require that field so timeout/ref
                    # values can never be mistaken for ownership.
                    if len(fields) < 10:
                        raise GuardError(f"malformed listener row in {name}")
                    address = fields[1]
                    if fields[3].upper() != LISTEN or ":" not in address:
                        continue
                    if address.rsplit(":", 1)[1].upper() != wanted:
                        continue
                    try:
                        result.add(int(fields[9]))
                    except ValueError as exc:
                        raise GuardError(f"invalid listener inode in {name}") from exc
            except (UnicodeError, StopIteration) as exc:
                raise GuardError(f"cannot parse {name}") from exc
    return result


def _bounded_net_header(name: str) -> None:
    try:
        with (PROC / name).open(encoding="ascii") as stream:
            header = stream.readline(MAX_NET_LINE + 1)
    except (OSError, UnicodeError) as exc:
        raise GuardError(f"cannot read {PROC / name}: {exc}") from exc
    if not header or len(header) > MAX_NET_LINE or not header.lstrip().startswith("sl "):
        raise GuardError(f"invalid or oversized header in {name}")


def _validated_artifact_path(path: Path) -> Path:
    """Return an absolute task artifact path with a trusted parent chain.

    Evidence is both security-sensitive input and a cleanup capability.  Do
    not follow links in any directory component, and require every existing
    directory in the chain to be owned by this process without group/world
    access.  The final file is protected separately with O_NOFOLLOW.
    """
    if not path.is_absolute():
        raise GuardError("Apache artifact path must be absolute")
    current = path.parent
    chain: list[Path] = []
    while True:
        chain.append(current)
        if current == current.parent:
            break
        current = current.parent
    private_directory_seen = False
    for directory in chain:
        try:
            info = directory.lstat()
        except OSError as exc:
            raise GuardError(f"cannot inspect Apache artifact directory {directory}: {exc}") from exc
        if not directory.is_dir() or directory.is_symlink():
            raise GuardError(f"Apache artifact directory is not a private directory: {directory}")
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            if not private_directory_seen:
                raise GuardError(f"Apache artifact directory is not private to the task: {directory}")
            break
        private_directory_seen = True
    return path


def _load(path: Path) -> dict[str, Any]:
    path = _validated_artifact_path(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, encoding="utf-8") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GuardError(f"cannot read guard evidence {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GuardError("guard evidence is not an object")
    return value


def _identity(evidence: dict[str, Any]) -> tuple[int, str, dict[str, int]]:
    try:
        pid = int(evidence["pid"])
        expected_exe = os.path.realpath(str(evidence["executable"]))
        expected = {
            key: int(evidence[key])
            for key in ("starttime", "session", "pgrp")
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise GuardError("guard evidence lacks a complete process identity") from exc
    if pid <= 1 or not expected_exe.startswith("/"):
        raise GuardError("invalid recorded process identity")
    return pid, expected_exe, expected


def _open_verified_pidfd(evidence: dict[str, Any]) -> tuple[int, int, str, dict[str, int]]:
    if not _pidfd_available():
        raise GuardError("Linux pidfd support is unavailable")
    pid, expected_exe, expected = _identity(evidence)
    try:
        fd = os.pidfd_open(pid)
    except OSError as exc:
        raise GuardError(f"cannot open Apache pidfd: {exc}") from exc
    try:
        if _pidfd_bound_pid(fd) != pid:
            raise GuardError("pidfd is not bound to the recorded PID")
    except (OSError, ValueError) as exc:
        os.close(fd)
        raise GuardError(f"cannot verify Apache pidfd binding: {exc}") from exc
    return fd, pid, expected_exe, expected


def _pidfd_bound_pid(fd: int) -> int:
    fdinfo = Path(f"/proc/self/fdinfo/{fd}").read_text(encoding="ascii")
    for line in fdinfo.splitlines():
        if line.startswith("Pid:"):
            return int(line.split(":", 1)[1].strip())
    raise GuardError("pidfd fdinfo has no PID binding")


def verify_running(evidence: dict[str, Any]) -> None:
    pid, expected_exe, expected = _identity(evidence)
    try:
        actual = _stat(pid)
        actual_exe = _exe(pid)
        fds = _fd_inodes(pid)
    except OSError as exc:
        raise GuardError(f"process identity is unavailable: {exc}") from exc
    if actual != expected or actual_exe != expected_exe:
        raise GuardError("Apache PID identity changed (possible PID reuse)")
    try:
        port = int(evidence["port"])
        recorded = {int(item) for item in evidence["listener_inodes"]}
    except (KeyError, TypeError, ValueError) as exc:
        raise GuardError("guard evidence lacks listener ownership") from exc
    current = _listener_inodes(port)
    if not recorded or not recorded.issubset(current) or not recorded.issubset(fds):
        raise GuardError("Apache listener ownership cannot be proven")


def verify_stopped(evidence: dict[str, Any], pidfile: str | None = None) -> None:
    pid, _, expected = _identity(evidence)
    if (_pid_path(pid, "stat")).exists():
        raise GuardError(f"Apache process still exists: {pid}")
    try:
        listeners = _listener_inodes(int(evidence["port"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise GuardError("guard evidence lacks a valid listener port") from exc
    if listeners:
        raise GuardError("a listener remains on the selected Apache port")
    members = _session_members(expected["session"], expected["pgrp"])
    if members:
        raise GuardError(f"Apache session/process-group members remain: {members}")
    if pidfile and Path(pidfile).exists():
        raise GuardError(f"Apache pidfile remains after cleanup: {pidfile}")


def record(pid: int, executable: str, port: int, output: Path) -> None:
    expected_exe = os.path.realpath(executable)
    try:
        stat = _stat(pid)
        actual_exe = _exe(pid)
        fds = _fd_inodes(pid)
        listeners = _listener_inodes(port)
    except OSError as exc:
        raise GuardError(f"cannot inspect Apache process: {exc}") from exc
    if actual_exe != expected_exe:
        raise GuardError("started process executable does not match Apache binary")
    owned = sorted(fds & listeners)
    if not owned:
        raise GuardError("started Apache process does not own the selected listener")
    payload = {
        "pid": pid,
        "executable": actual_exe,
        "starttime": stat["starttime"],
        "session": stat["session"],
        "pgrp": stat["pgrp"],
        "port": port,
        "listener_inodes": owned,
        "task_socket_inodes": sorted(fds),
        "pidfd_supported": _pidfd_available(),
    }
    output = _validated_artifact_path(output)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(output, flags, 0o600)
    except OSError as exc:
        raise GuardError(f"cannot create non-overwriting Apache evidence: {exc}") from exc
    try:
        os.write(fd, (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8"))
    finally:
        os.close(fd)


def signal_verified(evidence: dict[str, Any], sig: int) -> str:
    fd, _, _, _ = _open_verified_pidfd(evidence)
    try:
        verify_running(evidence)
        _pidfd_send_signal(fd, sig)
    finally:
        os.close(fd)
    return "pidfd"


def _poll_pidfd(fd: int, timeout: float) -> bool:
    poller = select.poll()
    poller.register(fd, select.POLLIN | select.POLLHUP)
    return bool(poller.poll(int(timeout * 1000)))


def terminate_verified(evidence: dict[str, Any]) -> str:
    fd, _, _, _ = _open_verified_pidfd(evidence)
    try:
        verify_running(evidence)
        _pidfd_send_signal(fd, int(signal.SIGTERM))
        if not _poll_pidfd(fd, TERM_TIMEOUT):
            _pidfd_send_signal(fd, int(signal.SIGKILL))
            if not _poll_pidfd(fd, KILL_TIMEOUT):
                raise GuardError("verified Apache process did not exit within bounded cleanup")
    finally:
        os.close(fd)
    return "pidfd-term-kill"


def verify_pidfile(evidence: dict[str, Any], pid: int) -> None:
    recorded, _, _ = _identity(evidence)
    if recorded != pid:
        raise GuardError("Apache pidfile PID does not match recorded evidence")


def preflight() -> None:
    if not PROC.is_dir():
        raise GuardError("/proc is unavailable")
    if not _pidfd_available():
        raise GuardError("Linux pidfd support is unavailable")
    try:
        fd = os.pidfd_open(os.getpid())
    except OSError as exc:
        raise GuardError(f"cannot open self pidfd: {exc}") from exc
    try:
        if _pidfd_bound_pid(fd) != os.getpid():
            raise GuardError("self pidfd binding is incorrect")
        _pidfd_send_signal(fd, 0)
    except (OSError, ValueError) as exc:
        raise GuardError(f"self pidfd validation failed: {exc}") from exc
    finally:
        try:
            os.close(fd)
        except OSError as exc:
            raise GuardError(f"cannot close self pidfd: {exc}") from exc
    for name in ("net/tcp", "net/tcp6"):
        _bounded_net_header(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--pid", type=int, required=True)
    rec.add_argument("--executable", required=True)
    rec.add_argument("--port", type=int, required=True)
    rec.add_argument("--output", type=Path, required=True)
    for name in ("verify-running", "signal", "terminate", "verify-stopped", "verify-pid", "preflight"):
        command = sub.add_parser(name)
        if name not in ("preflight",):
            command.add_argument("--evidence", type=Path, required=True)
        command.add_argument("--pidfile")
        if name in ("signal", "terminate"):
            command.add_argument("--signal", type=int, default=int(signal.SIGTERM))
        if name == "verify-pid":
            command.add_argument("--pid", type=int, required=True)
    args = parser.parse_args()
    try:
        if args.command == "record":
            record(args.pid, args.executable, args.port, args.output)
        elif args.command == "verify-running":
            verify_running(_load(args.evidence))
        elif args.command == "signal":
            print(signal_verified(_load(args.evidence), args.signal))
        elif args.command == "terminate":
            print(terminate_verified(_load(args.evidence)))
        elif args.command == "verify-pid":
            verify_pidfile(_load(args.evidence), args.pid)
        elif args.command == "preflight":
            preflight()
        else:
            verify_stopped(_load(args.evidence), args.pidfile)
    except GuardError as exc:
        print(f"apache_process_guard: blocked {exc}")
        return 77
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
