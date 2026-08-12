#!/usr/bin/env python3
"""Run the update-submodules candidate in a private Linux mount/PID namespace.

This is intentionally a small trusted, root-only launcher.  Candidate code is
never evaluated until after the namespace has been built and the process has
dropped to the dedicated validator account.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import grp
import os
from pathlib import Path
import pwd
import stat
import sys
from typing import Callable, Sequence


CLONE_NEWNS = 0x00020000
CLONE_NEWPID = 0x20000000
MS_RDONLY = 1
MS_NOSUID = 2
MS_NODEV = 4
MS_NOEXEC = 8
MS_BIND = 4096
MS_REC = 16384
MS_PRIVATE = 1 << 18
MS_REMOUNT = 32
PR_SET_NO_NEW_PRIVS = 38
LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.mount.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_void_p]
LIBC.mount.restype = ctypes.c_int
LIBC.umount2.argtypes = [ctypes.c_char_p, ctypes.c_int]
LIBC.umount2.restype = ctypes.c_int
LIBC.unshare.argtypes = [ctypes.c_int]
LIBC.unshare.restype = ctypes.c_int
LIBC.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
LIBC.prctl.restype = ctypes.c_int
SAFE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
PROCFS_TARGET = Path("/proc")
CandidateEntry = Callable[[Path, Path, Path, Path, Path, int, int], None]
CandidateArguments = tuple[Path, Path, Path, Path, Path, int, int]


class NamespaceUnavailable(RuntimeError):
    """The host kernel/container does not permit the required isolation."""


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--write-root", required=True)
    parser.add_argument("--external-root", required=True)
    parser.add_argument("--validator-user", required=True)
    parser.add_argument("--validator-group", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--namespace-parent", required=True)
    return parser.parse_args(argv)


def _absolute_existing_directory(value: str, label: str) -> Path:
    if not value or not os.path.isabs(value) or os.path.normpath(value) != value:
        raise ValueError(f"{label} must be a canonical absolute path")
    path = Path(value)
    current = Path("/")
    for part in path.parts[1:]:
        current /= part
        metadata = os.lstat(current)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"{label} must be an existing non-symlink directory")
    return path


def _strict_child(child: Path, parent: Path, label: str) -> None:
    try:
        child.relative_to(parent)
    except ValueError as exc:
        raise ValueError(f"{label} must be below source root") from exc
    if child == parent:
        raise ValueError(f"{label} must be a strict child of source root")


def _disjoint(first: Path, second: Path, first_label: str, second_label: str) -> None:
    for candidate, parent in ((first, second), (second, first)):
        try:
            candidate.relative_to(parent)
        except ValueError:
            continue
        raise ValueError(f"{first_label} and {second_label} must be disjoint")


def _identity(user: str, group: str) -> tuple[int, int]:
    try:
        account = pwd.getpwnam(user)
        group_entry = grp.getgrnam(group)
        primary_group = grp.getgrgid(account.pw_gid)
    except KeyError as error:
        raise ValueError("validator user and group must already exist") from error
    if (
        account.pw_uid == 0
        or account.pw_gid == 0
        or group_entry.gr_gid == 0
        or primary_group.gr_name == "root"
        or group_entry.gr_name == "root"
    ):
        raise ValueError("validator identity must be unprivileged")
    memberships = {entry.gr_name for entry in grp.getgrall() if user in entry.gr_mem}
    memberships.add(primary_group.gr_name)
    if group not in memberships or memberships & {"root", "sudo", "wheel", "admin"}:
        raise ValueError("validator identity is not a dedicated unprivileged account")
    return account.pw_uid, group_entry.gr_gid


def _mount(source: str | None, target: Path, flags: int, filesystem_type: str | None = None) -> None:
    result = LIBC.mount(
        ctypes.c_char_p(source.encode() if source is not None else None),
        ctypes.c_char_p(os.fsencode(target)),
        ctypes.c_char_p(filesystem_type.encode() if filesystem_type is not None else None),
        ctypes.c_ulong(flags), None,
    )
    if result != 0:
        error = ctypes.get_errno()
        if error in {errno.EPERM, errno.ENOSYS, errno.EINVAL}:
            raise NamespaceUnavailable(f"mount namespace operation unavailable: {os.strerror(error)}")
        raise OSError(error, os.strerror(error), target)


def _umount(target: Path) -> None:
    if LIBC.umount2(ctypes.c_char_p(os.fsencode(target)), 0) != 0:
        error = ctypes.get_errno()
        if error != errno.EINVAL:
            raise OSError(error, os.strerror(error), target)


def _mountinfo_for(path: Path) -> list[str]:
    target = str(path)
    return [
        line for line in Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines()
        if len(line.split(" - ", 1)[0].split()) > 4 and line.split(" - ", 1)[0].split()[4] == target
    ]


def _validate_namespace_parent(namespace_parent: Path, validator_gid: int) -> None:
    """Accept only a root-created private child of a trusted sticky directory."""
    namespace_ancestor = namespace_parent.parent
    if namespace_parent == namespace_ancestor:
        raise ValueError("namespace parent must have a trusted sticky ancestor")
    ancestor_metadata = os.lstat(namespace_ancestor)
    if (
        not stat.S_ISDIR(ancestor_metadata.st_mode)
        or stat.S_ISLNK(ancestor_metadata.st_mode)
        or ancestor_metadata.st_uid != 0
        or not ancestor_metadata.st_mode & stat.S_ISVTX
    ):
        raise ValueError("namespace parent requires a root-owned sticky ancestor")
    metadata = os.lstat(namespace_parent)
    if (
        not stat.S_ISDIR(metadata.st_mode)
        or stat.S_ISLNK(metadata.st_mode)
        or (metadata.st_uid, metadata.st_gid, stat.S_IMODE(metadata.st_mode))
        != (0, validator_gid, 0o750)
    ):
        raise ValueError("namespace parent must be root:validator mode 0750")
    if any(os.scandir(namespace_parent)):
        raise ValueError("namespace parent must be empty before mount layout creation")


def _create_mount_layout(namespace_parent: Path, validator_gid: int) -> Path:
    """Create and verify fixed root:validator traversal placeholders."""
    mount_root = namespace_parent / "mount-root"
    for path in (mount_root, mount_root / "source", mount_root / "external"):
        os.mkdir(path, mode=0o700)
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != 0:
                raise RuntimeError(f"unsafe namespace mount placeholder: {path}")
            os.fchown(descriptor, 0, validator_gid)
            os.fchmod(descriptor, 0o750)
        finally:
            os.close(descriptor)
    for path in (mount_root, mount_root / "source", mount_root / "external"):
        metadata = os.lstat(path)
        if (
            not stat.S_ISDIR(metadata.st_mode)
            or stat.S_ISLNK(metadata.st_mode)
            or metadata.st_uid != 0
            or metadata.st_gid != validator_gid
            or stat.S_IMODE(metadata.st_mode) != 0o750
        ):
            raise RuntimeError(f"unsafe namespace mount placeholder: {path}")
    return mount_root


def _verify_mount(target: Path, *, readonly: bool) -> None:
    rows = _mountinfo_for(target)
    if len(rows) != 1:
        raise RuntimeError(f"expected exactly one private bind mount for {target}")
    options = rows[0].split(" - ", 1)[0].split()[5].split(",")
    if ("ro" in options) != readonly or "nosuid" not in options or "nodev" not in options:
        raise RuntimeError(f"unsafe mount flags for {target}: {','.join(options)}")


def _verify_procfs(target: Path) -> None:
    """Require one fresh, hardened procfs layer over the literal proc target."""
    if target != PROCFS_TARGET:
        raise RuntimeError("procfs must be mounted at literal /proc")
    hardened_rows = []
    for row in _mountinfo_for(target):
        before_separator, separator, after_separator = row.partition(" - ")
        fields = before_separator.split()
        filesystem = after_separator.split()[0] if separator and after_separator else ""
        options = fields[5].split(",") if len(fields) > 5 else []
        if filesystem == "proc" and {"ro", "nosuid", "nodev", "noexec"}.issubset(options):
            hardened_rows.append(row)
    if len(hardened_rows) != 1:
        raise RuntimeError("expected exactly one hardened procfs mount at /proc")


def _unshare() -> None:
    if LIBC.unshare(ctypes.c_int(CLONE_NEWNS | CLONE_NEWPID)) != 0:
        error = ctypes.get_errno()
        if error in {errno.EPERM, errno.ENOSYS, errno.EINVAL}:
            raise NamespaceUnavailable(f"mount/PID namespace unavailable: {os.strerror(error)}")
        raise OSError(error, os.strerror(error))


def _set_no_new_privs() -> None:
    """Fail closed before candidate setup so setuid/file-cap binaries cannot elevate."""
    if LIBC.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        error = ctypes.get_errno()
        raise OSError(error, f"cannot set no_new_privs: {os.strerror(error)}")


def _candidate_environment(source: Path, framework_relative: Path, external: Path, guard: Path, python: Path) -> dict[str, str]:
    root = external
    return {
        "PATH": SAFE_PATH, "PYTHON": str(python), "HOME": str(root / "home"),
        "TMPDIR": str(root / "tmp"), "TMP": str(root / "tmp"), "TEMP": str(root / "tmp"),
        "XDG_CACHE_HOME": str(root / "xdg-cache"), "XDG_CONFIG_HOME": str(root / "xdg-config"),
        "XDG_DATA_HOME": str(root / "xdg-data"), "XDG_STATE_HOME": str(root / "xdg-state"),
        "PIP_CACHE_DIR": str(root / "pip-cache"), "PYTHONPYCACHEPREFIX": str(root / "pycache"),
        "PYTHONUSERBASE": str(root / "python-user-base"), "PYTHONPATH": str(root / "python-packages"),
        "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_GLOBAL": str(root / "gitconfig"),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0", "GITHUB_ACTIONS": "true",
        "GITHUB_WORKSPACE": str(source),
        "FRAMEWORK_ROOT": str(source / framework_relative), "VALIDATOR_EXTERNAL_ROOT": str(root),
        "BUILD_ROOT": str(root / "build"),
        "VALIDATION_WRITE_ROOT": str(guard), "VERIFIED_RUN_ROOT": str(root / "verified-run"),
        "VERIFIED_STATE_ROOT": str(root / "verified-run/state"), "VERIFIED_BUILD_ROOT": str(root / "verified-run/build"),
        "VERIFIED_SOURCE_ROOT": str(root / "verified-run/source"), "VERIFIED_TMP_ROOT": str(root / "verified-run/tmp"),
        "VERIFIED_LOG_ROOT": str(root / "verified-run/log"), "CACHE_ROOT": str(root / "cache"),
        "VERIFIED_COMPONENT_CACHE": str(root / "cache/shared"), "CONNECTOR_COMPONENT_CACHE": str(root / "cache/components"),
        "VERIFIED_EVIDENCE_ROOT": str(root / "evidence"), "EVIDENCE_ROOT": str(root / "evidence/no-crs"),
        "RUNTIME_EVIDENCE_ROOT": str(root / "evidence/runtime"), "RUNTIME_RUN_ROOT": str(root / "runtime"),
        "RUNTIME_LOG_ROOT": str(root / "runtime-log"), "SOURCE_ROOT": str(root / "source"),
        "TMP_ROOT": str(root / "tmp-root"), "LOG_ROOT": str(root / "log"), "MATRIX_ROOT": str(root / "matrix"),
    }


def _candidate_script() -> str:
    """Return the fixed, unprivileged candidate program; never accept source input."""
    return (
        'umask 077\n'
        'test "$(id -un)" = "modsecurity-validator"\n'
        'test "$PWD" = "$GITHUB_WORKSPACE"\n'
        'test "$(awk \'/^CapEff:/ {print $2}\' /proc/self/status)" = 0000000000000000\n'
        'test "$(awk \'/^NoNewPrivs:/ {print $2}\' /proc/self/status)" = 1\n'
        'test ! -w "$VALIDATION_WRITE_ROOT"; test ! -w "$GITHUB_WORKSPACE"; test ! -w "$GITHUB_WORKSPACE/.git"\n'
        'test ! -w "$GITHUB_WORKSPACE/.git/modules"; test ! -w "$FRAMEWORK_ROOT"; test ! -w "$FRAMEWORK_ROOT/.git"\n'
        'expect_blocked() { if "$@"; then echo "validator changed a protected path: $*" >&2; exit 1; fi; }\n'
        'for target in "$GITHUB_WORKSPACE/.readonly-validator-write-probe" "$FRAMEWORK_ROOT/.readonly-validator-write-probe" "$GITHUB_WORKSPACE/.git/index.lock" "$FRAMEWORK_ROOT/.git/index.lock" "$VALIDATION_WRITE_ROOT/.readonly-validator-guard-probe"; do expect_blocked touch "$target"; done\n'
        'for target in "$GITHUB_WORKSPACE/Makefile" "$FRAMEWORK_ROOT/Makefile" "$GITHUB_WORKSPACE/.git" "$FRAMEWORK_ROOT/.git"; do expect_blocked chmod 600 "$target"; done\n'
        'expect_blocked mv "$GITHUB_WORKSPACE/Makefile" "$GITHUB_WORKSPACE/.readonly-validator-rename-probe"\n'
        'expect_blocked mv "$FRAMEWORK_ROOT/Makefile" "$FRAMEWORK_ROOT/.readonly-validator-rename-probe"\n'
        'expect_blocked mv "$GITHUB_WORKSPACE/.git" "$GITHUB_WORKSPACE/.readonly-validator-git-rename-probe"\n'
        'expect_blocked mv "$FRAMEWORK_ROOT/.git" "$FRAMEWORK_ROOT/.readonly-validator-git-rename-probe"\n'
        'for target in "$GITHUB_WORKSPACE/Makefile" "$FRAMEWORK_ROOT/Makefile"; do expect_blocked rm "$target"; done\n'
        'if sudo -n true >/dev/null 2>&1 || /usr/bin/sudo -n true >/dev/null 2>&1; then echo "validator obtained sudo" >&2; exit 1; fi\n'
        'if /usr/bin/mount -o remount,rw "$GITHUB_WORKSPACE" >/dev/null 2>&1; then echo "validator remounted source" >&2; exit 1; fi\n'
        'mkdir -p "$HOME" "$TMPDIR" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" '
        '"$XDG_STATE_HOME" "$PIP_CACHE_DIR" "$PYTHONPYCACHEPREFIX" "$PYTHONUSERBASE" '
        '"$PYTHONPATH" "$VERIFIED_RUN_ROOT" "$VERIFIED_STATE_ROOT" "$VERIFIED_BUILD_ROOT" '
        '"$VERIFIED_SOURCE_ROOT" "$VERIFIED_TMP_ROOT" "$VERIFIED_LOG_ROOT" "$CACHE_ROOT" '
        '"$VERIFIED_COMPONENT_CACHE" "$CONNECTOR_COMPONENT_CACHE" "$VERIFIED_EVIDENCE_ROOT" '
        '"$EVIDENCE_ROOT" "$RUNTIME_EVIDENCE_ROOT" "$RUNTIME_RUN_ROOT" "$RUNTIME_LOG_ROOT" '
        '"$SOURCE_ROOT" "$TMP_ROOT" "$LOG_ROOT" "$MATRIX_ROOT" "$BUILD_ROOT"\n'
        'git config --global --add safe.directory "$GITHUB_WORKSPACE"\n'
        'git config --global --add safe.directory "$FRAMEWORK_ROOT"\n'
        'touch "$VALIDATOR_EXTERNAL_ROOT/write-probe"; test -f "$VALIDATOR_EXTERNAL_ROOT/write-probe"\n'
        '"$PYTHON" -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes '
        '--target "$PYTHONPATH" --requirement "$GITHUB_WORKSPACE/ci/requirements/update-submodules-validation-linux-x86_64.txt"\n'
        'exec make PYTHON="$PYTHON" quick-check'
    )


def _candidate_pid1(source: Path, framework_relative: Path, external: Path, guard: Path, python: Path, uid: int, gid: int) -> None:
    env = _candidate_environment(source, framework_relative, external, guard, python)
    os.setgroups([]); os.setgid(gid); os.setuid(uid); os.chdir(source)
    os.execve("/bin/bash", ["bash", "--noprofile", "--norc", "-ceu", _candidate_script()], env)


def _run_pid1_candidate(
    candidate_arguments: CandidateArguments,
    candidate_entry: CandidateEntry,
    proc_ready: tuple[int, int],
    before_proc: list[str],
) -> None:
    proc_ready_read, proc_ready_write = proc_ready
    os.close(proc_ready_read)
    proc_mounted = False
    ready_acknowledged = False
    try:
        _mount("proc", PROCFS_TARGET, MS_RDONLY | MS_NOSUID | MS_NODEV | MS_NOEXEC, "proc")
        proc_mounted = True
        _verify_procfs(PROCFS_TARGET)
        os.write(proc_ready_write, b"1")
        ready_acknowledged = True
        os.close(proc_ready_write)
        _set_no_new_privs()
        candidate_entry(*candidate_arguments)
    except Exception as error:
        print(f"readonly namespace candidate setup failed: {error}", file=sys.stderr)
        if proc_mounted and not ready_acknowledged:
            try:
                _umount(PROCFS_TARGET)
                if _mountinfo_for(PROCFS_TARGET) != before_proc:
                    print("readonly namespace candidate procfs restoration failed", file=sys.stderr)
            except Exception as cleanup_error:
                print(f"readonly namespace candidate procfs cleanup failed: {cleanup_error}", file=sys.stderr)
        try:
            os.close(proc_ready_write)
        except OSError:
            pass
        os._exit(127)


def _namespace_child(
    source: Path,
    framework: Path,
    external: Path,
    mount_root: Path,
    python: Path,
    uid: int,
    gid: int,
    candidate_entry: CandidateEntry = _candidate_pid1,
    close_parent_fds: Sequence[int] = (),
) -> int:
    _unshare()
    _mount(None, Path("/"), MS_REC | MS_PRIVATE)
    source_view, external_view = mount_root / "source", mount_root / "external"
    _mount(str(source), source_view, MS_BIND)
    _mount(None, source_view, MS_BIND | MS_REMOUNT | MS_RDONLY | MS_NOSUID | MS_NODEV)
    _mount(str(external), external_view, MS_BIND)
    _mount(None, external_view, MS_BIND | MS_REMOUNT | MS_NOSUID | MS_NODEV)
    _verify_mount(source_view, readonly=True); _verify_mount(external_view, readonly=False)
    framework_relative = framework.relative_to(source)
    before_proc = _mountinfo_for(PROCFS_TARGET)
    proc_ready_read, proc_ready_write = os.pipe()
    child = os.fork()
    if child == 0:
        _run_pid1_candidate(
            (source_view, framework_relative, external_view, mount_root, python, uid, gid),
            candidate_entry,
            (proc_ready_read, proc_ready_write),
            before_proc,
        )
    os.close(proc_ready_write)
    for descriptor in close_parent_fds:
        os.close(descriptor)
    proc_mounted = os.read(proc_ready_read, 1) == b"1"
    os.close(proc_ready_read)
    try:
        _pid, status = os.waitpid(child, 0)
    finally:
        if proc_mounted:
            _umount(PROCFS_TARGET)
            if _mountinfo_for(PROCFS_TARGET) != before_proc:
                raise RuntimeError("namespace runner did not restore inherited procfs")
        _umount(external_view); _umount(source_view)
    return os.waitstatus_to_exitcode(status)


def _validated_configuration(arguments: argparse.Namespace) -> tuple[Path, Path, Path, Path, Path, Path, int, int]:
    source = _absolute_existing_directory(arguments.source_root, "source root")
    framework = _absolute_existing_directory(arguments.framework_root, "framework root")
    write_root = _absolute_existing_directory(arguments.write_root, "write root")
    external = _absolute_existing_directory(arguments.external_root, "external root")
    _strict_child(framework, source, "framework root")
    _disjoint(source, write_root, "source root", "write root")
    if external != write_root / "external":
        raise ValueError("external root must be exactly the write root external child")
    namespace_parent = _absolute_existing_directory(arguments.namespace_parent, "namespace parent")
    python = Path(arguments.python)
    if not python.is_absolute() or not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError("python must be an executable absolute path")
    uid, gid = _identity(arguments.validator_user, arguments.validator_group)
    _validate_namespace_parent(namespace_parent, gid)
    write_metadata = os.stat(write_root, follow_symlinks=False)
    external_metadata = os.stat(external, follow_symlinks=False)
    if write_metadata.st_uid != 0 or write_metadata.st_gid != 0 or stat.S_IMODE(write_metadata.st_mode) != 0o711:
        raise ValueError("write root must be root-owned mode 0711")
    if (external_metadata.st_uid, external_metadata.st_gid, stat.S_IMODE(external_metadata.st_mode)) != (uid, gid, 0o700):
        raise ValueError("external root must be validator-owned mode 0700")
    return source, framework, write_root, external, namespace_parent, python, uid, gid


def run(arguments: argparse.Namespace) -> int:
    if os.name != "posix" or sys.platform != "linux" or os.geteuid() != 0:
        raise NamespaceUnavailable("readonly namespace runner requires Linux root")
    source, framework, _write_root, external, namespace_parent, python, uid, gid = _validated_configuration(arguments)
    mount_root = _create_mount_layout(namespace_parent, gid)
    before = _mountinfo_for(mount_root)
    try:
        child = os.fork()
        if child == 0:
            try: os._exit(_namespace_child(source, framework, external, mount_root, python, uid, gid))
            except NamespaceUnavailable as error: print(str(error), file=sys.stderr); os._exit(125)
            except Exception as error: print(f"readonly namespace setup failed: {error}", file=sys.stderr); os._exit(126)
        _pid, status = os.waitpid(child, 0)
        code = os.waitstatus_to_exitcode(status)
        if _mountinfo_for(mount_root) != before:
            raise RuntimeError("namespace runner leaked a host mount")
        if code == 0:
            print("READONLY_SUBMODULE_VALIDATION_NAMESPACE_COMPLETE")
        return code
    finally:
        # The bind mounts live only in the child mount namespace.  Do not use a
        # recursive cleanup: these are exact, trusted empty placeholders.
        if not _mountinfo_for(mount_root):
            for path in (mount_root / "source", mount_root / "external", mount_root):
                if path.exists():
                    os.rmdir(path)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return run(parse_args(sys.argv[1:] if argv is None else argv))
    except (ValueError, OSError, RuntimeError) as error:
        print(f"readonly namespace validation blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
