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
import secrets
import signal
import stat
import time
from typing import Any


PROC = Path("/proc")
LISTEN = "0A"
MAX_PROC_ENTRIES = 4096
MAX_FD_ENTRIES = 4096
MAX_NET_ROWS = 4096
MAX_NET_BYTES = 4 * 1024 * 1024
MAX_NET_LINE = 4096
MAX_EVIDENCE_BYTES = 1024 * 1024
TERM_TIMEOUT = 2.0
KILL_TIMEOUT = 2.0
RECORD_FAILURE_CLEANED_EXIT = 74
TEMPORARY_ARTIFACT_ATTEMPTS = 16
RECORD_INSPECTION_ATTEMPTS = 8
RECORD_INSPECTION_RETRY_SECONDS = 0.01
RUNNER_DIRECTORY_ENV = "MSCONNECTOR_APACHE_GUARD_DIRECTORY"
RUNNER_ARTIFACT_ROOT_ENV = "MSCONNECTOR_APACHE_GUARD_ARTIFACT_ROOT"


class GuardError(RuntimeError):
    pass


class RecordFailureCleaned(GuardError):
    """Evidence publication failed after verified runtime cleanup."""


def _runner_configured_path(variable: str, capability: str) -> Path:
    """Read a path capability selected by the Apache smoke runner.

    The guard deliberately has no generic CLI root flag. Its root values are
    trusted smoke-runner configuration, not an authentication mechanism for a
    same-identity local caller; the guard still validates every resulting path
    before runtime creation or guard-evidence access.
    """
    raw_path = os.environ.get(variable)
    if not raw_path or "\x00" in raw_path:
        raise GuardError(f"{capability} must be supplied by the Apache smoke runner")
    return Path(raw_path)


def _directory_open_flags() -> int:
    """Return the descriptor flags required for race-safe directory walking."""
    directory = getattr(os, "O_DIRECTORY", None)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if directory is None or nofollow is None:
        raise GuardError("Apache runtime directory hardening is unavailable on this platform")
    flags = os.O_RDONLY | directory | nofollow
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    return flags


def _safe_runtime_ancestor(metadata: os.stat_result, path: Path) -> None:
    """Accept only stable ancestors for a later pathname-based harness use.

    A descriptor-relative create prevents a symlink insertion during setup.
    Once the descriptor is closed, however, the shell uses the resulting path
    again. Writable shared ancestors are therefore allowed only when the
    sticky-bit rule protects the task-owned child from another user renaming
    it (the normal /tmp and /var/tmp case).
    """
    if not stat.S_ISDIR(metadata.st_mode):
        raise GuardError(f"Apache runtime path must contain directories only: {path}")
    if metadata.st_uid not in (0, os.geteuid()):
        raise GuardError(
            f"Apache runtime path has an untrusted ancestor owner: {path}"
        )
    if metadata.st_mode & 0o022 and not (
        metadata.st_uid == 0 and metadata.st_mode & stat.S_ISVTX
    ):
        raise GuardError(
            f"Apache runtime path has an unsafe writable shared ancestor: {path}"
        )


def prepare_runtime_directory(path: Path, label: str, private_mode: bool) -> None:
    """Create and validate a harness directory without pathname races.

    Every component is opened relative to an already verified descriptor with
    ``O_DIRECTORY|O_NOFOLLOW``. Missing components are created with
    ``mkdirat`` semantics, then reopened through that same parent descriptor.
    This rejects a symlink inserted between existence checking and creation.
    """
    raw_path = os.fspath(path)
    if not os.path.isabs(raw_path) or "\x00" in raw_path:
        raise GuardError(f"{label} must be an absolute path")
    components = Path(raw_path).parts
    if len(components) < 2 or components[0] != os.sep or any(
        component in ("", ".", "..") for component in components[1:]
    ):
        raise GuardError(f"{label} must not contain empty, dot, or parent components")

    flags = _directory_open_flags()
    try:
        current_fd = os.open(os.sep, flags)
    except OSError as exc:
        raise GuardError(f"cannot open Apache runtime filesystem root: {exc}") from exc

    current_path = Path(os.sep)
    try:
        for index, component in enumerate(components[1:], start=1):
            is_leaf = index == len(components) - 1
            child_path = current_path / component
            child_fd: int | None = None
            try:
                child_fd = os.open(component, flags, dir_fd=current_fd)
            except FileNotFoundError:
                # Newly created intermediate components stay private. A
                # non-private leaf preserves the previous output-root mode
                # contract while still denying group/world writes.
                mode = 0o700 if private_mode or not is_leaf else 0o755
                try:
                    os.mkdir(component, mode, dir_fd=current_fd)
                except FileExistsError:
                    pass
                except OSError as exc:
                    raise GuardError(
                        f"cannot create Apache runtime directory {child_path}: {exc}"
                    ) from exc
                try:
                    child_fd = os.open(component, flags, dir_fd=current_fd)
                except OSError as exc:
                    raise GuardError(
                        f"cannot reopen Apache runtime directory {child_path}: {exc}"
                    ) from exc
            except OSError as exc:
                raise GuardError(
                    f"cannot open Apache runtime directory {child_path}: {exc}"
                ) from exc

            try:
                metadata = os.fstat(child_fd)
                if is_leaf:
                    if not stat.S_ISDIR(metadata.st_mode):
                        raise GuardError(f"{label} must be a directory: {child_path}")
                    if metadata.st_uid != os.geteuid() or metadata.st_mode & 0o022:
                        raise GuardError(
                            f"{label} must be owned and not group/world writable: {child_path}"
                        )
                    if private_mode:
                        os.fchmod(child_fd, 0o700)
                        metadata = os.fstat(child_fd)
                        if stat.S_IMODE(metadata.st_mode) != 0o700:
                            raise GuardError(f"{label} must have private mode 0700: {child_path}")
                else:
                    _safe_runtime_ancestor(metadata, child_path)
            except OSError as exc:
                os.close(child_fd)
                raise GuardError(
                    f"cannot validate Apache runtime directory {child_path}: {exc}"
                ) from exc
            except GuardError:
                os.close(child_fd)
                raise
            try:
                os.close(current_fd)
            except OSError as exc:
                os.close(child_fd)
                raise GuardError(
                    f"cannot close Apache runtime directory {current_path}: {exc}"
                ) from exc
            current_fd = child_fd
            current_path = child_path
    finally:
        os.close(current_fd)


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


def _validated_artifact_path(path: Path, artifact_root: Path) -> Path:
    """Return an absolute task artifact path with a trusted parent chain.

    Evidence is both security-sensitive input and a cleanup capability.  Do
    not follow links in any directory component, and require every existing
    directory in the chain to be owned by this process without group/world
    access.  The final file is protected separately with O_NOFOLLOW.
    """
    if not path.is_absolute() or not artifact_root.is_absolute():
        raise GuardError("Apache artifact path must be absolute")
    if ".." in path.parts or "." in path.parts or ".." in artifact_root.parts or "." in artifact_root.parts:
        raise GuardError("Apache artifact path must not contain parent traversal")
    root = artifact_root
    try:
        if root.resolve(strict=True) != root:
            raise GuardError("trusted Apache artifact root must not contain symlinks")
    except OSError as exc:
        raise GuardError(f"cannot resolve trusted Apache artifact root {root}: {exc}") from exc
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise GuardError("Apache artifact path is outside the trusted artifact root") from exc
    if not relative.parts or relative.name in ("", ".", ".."):
        raise GuardError("Apache artifact path is not a file below the trusted artifact root")
    try:
        root_info = root.lstat()
    except OSError as exc:
        raise GuardError(f"cannot inspect trusted Apache artifact root {root}: {exc}") from exc
    if not root.is_dir() or root.is_symlink() or root_info.st_uid != os.getuid() or root_info.st_mode & 0o077:
        raise GuardError("trusted Apache artifact root is not a private directory")
    current = root
    for component in relative.parts[:-1]:
        current = current / component
        try:
            info = current.lstat()
        except OSError as exc:
            raise GuardError(f"cannot inspect Apache artifact directory {current}: {exc}") from exc
        if not current.is_dir() or current.is_symlink() or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise GuardError(f"Apache artifact directory is not a private directory: {current}")
    return path


def _open_artifact_parent(path: Path, artifact_root: Path) -> tuple[int, str]:
    """Open an artifact's validated private parent and return its leaf name."""
    path = _validated_artifact_path(path, artifact_root)
    parent_flags = _directory_open_flags()
    try:
        parent_fd = os.open(artifact_root, parent_flags)
    except OSError as exc:
        raise GuardError(f"cannot open Apache artifact directory {path.parent}: {exc}") from exc
    try:
        relative = path.relative_to(artifact_root)
        for component in relative.parts[:-1]:
            next_fd = os.open(component, parent_flags, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = next_fd
        return parent_fd, relative.name
    except OSError as exc:
        os.close(parent_fd)
        raise GuardError(f"cannot open Apache artifact directory {path.parent}: {exc}") from exc


def _open_artifact(path: Path, artifact_root: Path, flags: int, mode: int = 0) -> int:
    """Open an already validated artifact relative to its private parent.

    Keeping the untrusted CLI value out of the final ``open`` call prevents
    path injection after the parent boundary has been checked.  ``O_NOFOLLOW``
    protects the artifact itself; the parent validation protects the directory
    namespace used by the guard.
    """
    parent_fd, name = _open_artifact_parent(path, artifact_root)
    try:
        return os.open(name, flags, mode, dir_fd=parent_fd)
    except OSError as exc:
        raise GuardError(f"cannot open Apache artifact {path}: {exc}") from exc
    finally:
        os.close(parent_fd)


def _load(path: Path, artifact_root: Path) -> dict[str, Any]:
    flags = os.O_RDONLY
    # O_NONBLOCK makes opening a FIFO or other special file non-blocking so
    # that the descriptor can be rejected after fstat().  It is harmless for
    # regular files and avoids trusting the path type before opening it.
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = _open_artifact(path, artifact_root, flags)
        try:
            metadata = os.fstat(fd)
            if not stat.S_ISREG(metadata.st_mode):
                raise GuardError("Apache guard evidence must be a regular file")
            if metadata.st_size > MAX_EVIDENCE_BYTES:
                raise GuardError("Apache guard evidence exceeds bounded size")
            payload = bytearray()
            while len(payload) <= MAX_EVIDENCE_BYTES:
                chunk = os.read(fd, min(65536, MAX_EVIDENCE_BYTES + 1 - len(payload)))
                if not chunk:
                    break
                payload.extend(chunk)
            if len(payload) > MAX_EVIDENCE_BYTES:
                raise GuardError("Apache guard evidence exceeds bounded size")
        finally:
            os.close(fd)
        value = json.loads(bytes(payload).decode("utf-8"))
    except (GuardError, OSError, UnicodeError, json.JSONDecodeError) as exc:
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
    except (GuardError, OSError, ValueError) as exc:
        try:
            os.close(fd)
        except OSError as close_exc:
            raise GuardError(
                f"cannot verify Apache pidfd binding and cannot close pidfd: {close_exc}"
            ) from exc
        if isinstance(exc, GuardError):
            raise
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


def _write_all(fd: int, payload: bytes) -> None:
    """Write a bounded evidence payload completely or fail closed."""
    view = memoryview(payload)
    offset = 0
    while offset < len(view):
        try:
            written = os.write(fd, view[offset:])
        except OSError as exc:
            raise GuardError(f"cannot write Apache guard evidence: {exc}") from exc
        if written <= 0:
            raise GuardError("cannot write Apache guard evidence: write made no progress")
        offset += written


def _record_failure_runtime_quiesced(
    evidence: dict[str, Any], leader_exit_confirmed: bool
) -> None:
    """Prove that a failed evidence publication retained no live runtime."""
    pid, _, expected = _identity(evidence)
    try:
        port = int(evidence["port"])
    except (KeyError, TypeError, ValueError) as exc:
        raise GuardError("record cleanup lacks a valid listener port") from exc
    if _listener_inodes(port):
        raise GuardError("Apache listener remains after failed evidence publication")
    members = _session_members(expected["session"], expected["pgrp"])
    if leader_exit_confirmed:
        members = [member for member in members if member != pid]
    elif _pid_path(pid, "stat").exists():
        raise GuardError("Apache process remains after failed evidence publication")
    if members:
        raise GuardError(
            f"Apache session/process-group members remain after failed evidence publication: {members}"
        )


def _terminate_after_record_failure(evidence: dict[str, Any]) -> None:
    """Use the in-memory verified identity when persistence itself fails."""
    leader_exit_confirmed = False
    termination_error: GuardError | None = None
    try:
        terminate_verified(evidence)
        leader_exit_confirmed = True
    except GuardError as exc:
        termination_error = exc
    try:
        _record_failure_runtime_quiesced(evidence, leader_exit_confirmed)
    except GuardError as exc:
        if termination_error is None:
            raise
        raise GuardError(
            f"cannot terminate Apache after failed evidence publication: "
            f"{termination_error}; {exc}"
        ) from exc


def _capture_record_payload(
    pid: int, expected_exe: str, port: int
) -> tuple[dict[str, Any], GuardError | OSError | None]:
    """Capture one stable ownership snapshot with bounded transient retries."""
    inspection_error: GuardError | OSError | None = None
    for attempt in range(RECORD_INSPECTION_ATTEMPTS):
        try:
            process_stat = _stat(pid)
            actual_exe = _exe(pid)
            fds = _fd_inodes(pid)
            listeners = _listener_inodes(port)
        except (GuardError, OSError) as exc:
            inspection_error = exc
        else:
            if actual_exe != expected_exe:
                raise GuardError("started process executable does not match Apache binary")
            owned = sorted(fds & listeners)
            if owned:
                return {
                    "pid": pid,
                    "executable": actual_exe,
                    "starttime": process_stat["starttime"],
                    "session": process_stat["session"],
                    "pgrp": process_stat["pgrp"],
                    "port": port,
                    "listener_inodes": owned,
                    "task_socket_inodes": sorted(fds),
                    "pidfd_supported": _pidfd_available(),
                }, inspection_error
            inspection_error = GuardError(
                "started Apache process does not own the selected listener"
            )
        if attempt + 1 < RECORD_INSPECTION_ATTEMPTS:
            time.sleep(RECORD_INSPECTION_RETRY_SECONDS)
    raise GuardError(
        f"cannot obtain stable Apache ownership evidence: {inspection_error}"
    ) from inspection_error


def _temporary_evidence_flags() -> int:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    return flags


def _open_temporary_evidence(parent_fd: int, flags: int) -> tuple[int, str]:
    for _ in range(TEMPORARY_ARTIFACT_ATTEMPTS):
        candidate = f".apache-process-guard-{secrets.token_hex(16)}.tmp"
        try:
            return os.open(candidate, flags, 0o600, dir_fd=parent_fd), candidate
        except FileExistsError:
            continue
    raise GuardError("cannot create a unique temporary Apache evidence file")


def _rollback_record_artifacts(
    parent_fd: int,
    output_name: str,
    temporary_fd: int,
    temporary_name: str | None,
    published: bool,
) -> list[str]:
    cleanup_errors: list[str] = []
    if temporary_fd >= 0:
        try:
            os.close(temporary_fd)
        except OSError as exc:
            cleanup_errors.append(f"temporary evidence close failed: {exc}")
    if parent_fd < 0:
        cleanup_errors.append("Apache evidence parent could not be opened")
        return cleanup_errors
    if temporary_name is not None:
        try:
            os.unlink(temporary_name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            cleanup_errors.append(f"temporary evidence removal failed: {exc}")
    if published:
        try:
            os.unlink(output_name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            cleanup_errors.append(f"published evidence rollback failed: {exc}")
    try:
        os.stat(output_name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    except OSError as exc:
        cleanup_errors.append(f"cannot verify evidence rollback: {exc}")
    else:
        cleanup_errors.append("Apache evidence path remains after rollback")
    return cleanup_errors


def _publish_record_payload(
    payload: dict[str, Any], output: Path, artifact_root: Path
) -> None:
    encoded = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
    flags = _temporary_evidence_flags()
    parent_fd = -1
    output_name = ""
    temporary_fd = -1
    temporary_name: str | None = None
    published = False
    try:
        parent_fd, output_name = _open_artifact_parent(output, artifact_root)
        temporary_fd, temporary_name = _open_temporary_evidence(parent_fd, flags)
        _write_all(temporary_fd, encoded)
        # This guard is Linux-only because its termination authority is pidfd.
        # Linux releases a descriptor before reporting any delayed close error;
        # relinquish the number first because retrying close could target a
        # descriptor that another thread or signal handler has already reused.
        closing_fd = temporary_fd
        temporary_fd = -1
        os.close(closing_fd)
        os.link(
            temporary_name,
            output_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
            follow_symlinks=False,
        )
        published = True
        os.unlink(temporary_name, dir_fd=parent_fd)
        temporary_name = None
    except (GuardError, OSError) as exc:
        cleanup_errors = _rollback_record_artifacts(
            parent_fd,
            output_name,
            temporary_fd,
            temporary_name,
            published,
        )
        try:
            _terminate_after_record_failure(payload)
        except GuardError as cleanup_exc:
            cleanup_errors.append(str(cleanup_exc))
        if cleanup_errors:
            raise GuardError(
                f"cannot publish non-overwriting Apache evidence: {exc}; "
                f"cleanup incomplete: {'; '.join(cleanup_errors)}"
            ) from exc
        raise RecordFailureCleaned(
            f"cannot publish non-overwriting Apache evidence: {exc}; "
            "verified Apache cleanup completed"
        ) from exc
    finally:
        if parent_fd >= 0:
            try:
                os.close(parent_fd)
            except OSError:
                pass


def record(pid: int, executable: str, port: int, output: Path, artifact_root: Path) -> None:
    payload, inspection_error = _capture_record_payload(
        pid, os.path.realpath(executable), port
    )
    if inspection_error is not None:
        try:
            _terminate_after_record_failure(payload)
        except GuardError as cleanup_exc:
            raise GuardError(
                f"Apache ownership inspection was unstable: {inspection_error}; "
                f"cleanup incomplete: {cleanup_exc}"
            ) from cleanup_exc
        raise RecordFailureCleaned(
            f"Apache ownership inspection was unstable: {inspection_error}; "
            "verified Apache cleanup completed"
        ) from inspection_error
    _publish_record_payload(payload, output, artifact_root)


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
    prepare = sub.add_parser("prepare-directory")
    prepare.add_argument("--label", required=True)
    prepare.add_argument("--private", action="store_true")
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
        if args.command == "prepare-directory":
            prepare_runtime_directory(
                _runner_configured_path(RUNNER_DIRECTORY_ENV, "Apache runtime directory"),
                args.label,
                args.private,
            )
        elif args.command == "record":
            record(
                args.pid,
                args.executable,
                args.port,
                args.output,
                _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
            )
        elif args.command == "verify-running":
            verify_running(
                _load(
                    args.evidence,
                    _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
                )
            )
        elif args.command == "signal":
            print(
                signal_verified(
                    _load(
                        args.evidence,
                        _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
                    ),
                    args.signal,
                )
            )
        elif args.command == "terminate":
            print(
                terminate_verified(
                    _load(
                        args.evidence,
                        _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
                    )
                )
            )
        elif args.command == "verify-pid":
            verify_pidfile(
                _load(
                    args.evidence,
                    _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
                ),
                args.pid,
            )
        elif args.command == "preflight":
            preflight()
        else:
            verify_stopped(
                _load(
                    args.evidence,
                    _runner_configured_path(RUNNER_ARTIFACT_ROOT_ENV, "Apache artifact root"),
                ),
                args.pidfile,
            )
    except RecordFailureCleaned as exc:
        print(f"apache_process_guard: blocked {exc}")
        return RECORD_FAILURE_CLEANED_EXIT
    except GuardError as exc:
        print(f"apache_process_guard: blocked {exc}")
        return 77
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
