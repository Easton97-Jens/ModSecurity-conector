#!/usr/bin/env python3
"""Launch the No-CRS fixture through a trusted private namespace boundary.

Only pre-installed, root-owned system programs run before the connector
harness. ``/usr/bin/unshare`` first creates a one-identity user/mount/PID
namespace and makes its mount propagation private. A fixed ``dash`` command
then mounts a bounded ``nosuid,nodev,noexec`` tmpfs at ``/tmp`` *inside that
private namespace only*. ``/usr/bin/bwrap`` builds the final minimal filesystem
view, disables further user namespaces, and clears every capability set before
it invokes worktree code. The fixture is released by namespace teardown, never
by a host-side path-based directory deletion.

The launcher deliberately refuses a host-root or set-id caller. A missing
system binary, unavailable namespace primitive, malformed setup attestation,
or non-zero final capability state is a fail-closed ``BLOCKED`` condition.
There is no sudo route and no fallback to the former check-then-``rmdir``
cleanup design.
"""

from __future__ import annotations

import argparse
import ctypes
from dataclasses import dataclass
import errno
import json
import os
from pathlib import Path
import select
import signal
import stat
import sys
import time
from typing import Mapping, Sequence


EXIT_BLOCKED = 77
EXIT_TIMEOUT = 124
DEFAULT_TIMEOUT_SECONDS = 300.0
MAX_TIMEOUT_SECONDS = 900.0
SETUP_TIMEOUT_SECONDS = 10.0
CHILD_STOP_TIMEOUT_SECONDS = 5.0
MAX_ARGUMENTS = 64
MAX_ARGUMENT_LENGTH = 16384
SAFE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

TRUSTED_UNSHARE = Path("/usr/bin/unshare")
TRUSTED_BWRAP = Path("/usr/bin/bwrap")
TRUSTED_DASH = Path("/usr/bin/dash")
TRUSTED_MOUNT = Path("/usr/bin/mount")
TRUSTED_PYTHON = Path("/usr/bin/python3")
PRIVATE_TMPFS_MOUNT = Path("/tmp")
FIXTURE_ROOT = PRIVATE_TMPFS_MOUNT / "msconnector-lighttpd-no-crs-fixture"

# This string is passed as a single, immutable argv element to the root-owned
# shell. The unprivileged launcher never executes worktree code while the
# outer user namespace has CAP_SYS_ADMIN. This fixed command has no expansion
# of caller-controlled values: its only operation is the tmpfs mount, followed
# by an argv-preserving exec of bwrap.
PRIVATE_TMPFS_SETUP = (
    "set -eu; "
    "/usr/bin/mount -t tmpfs -o mode=0755,nosuid,nodev,noexec,size=64m tmpfs /tmp; "
    "exec \"$@\""
)

# This verifier is executed by a root-owned system Python only *after* bwrap
# has created the private root, disabled new user namespaces, and dropped all
# capabilities. It is an enforcement boundary, not merely test evidence: no
# worktree harness command is exec'd until every final-state assertion passes.
FINAL_NAMESPACE_STATE_VERIFIER = r'''
import os
from pathlib import Path
import stat
import sys

def blocked(message):
    print(f"lighttpd_no_crs_fixture_namespace: BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(77)

try:
    inherited_descriptors = os.listdir("/proc/self/fd")
except OSError:
    blocked("namespace final verifier cannot inspect inherited descriptors")
for entry in inherited_descriptors:
    try:
        descriptor = int(entry, 10)
    except ValueError:
        continue
    if descriptor < 3:
        continue
    try:
        os.close(descriptor)
    except OSError as error:
        if error.errno != 9:
            blocked("namespace final verifier cannot close inherited descriptor")

if len(sys.argv) < 2 or not os.path.isabs(sys.argv[1]):
    blocked("namespace final verifier has no absolute harness command")

try:
    status = {}
    for row in Path("/proc/self/status").read_text(encoding="utf-8").splitlines():
        key, separator, value = row.partition(":")
        if separator:
            status[key] = value.strip()
except OSError:
    blocked("namespace final verifier cannot inspect process status")
for field in ("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb"):
    if status.get(field) != "0000000000000000":
        blocked(f"namespace final verifier retained {field}")
if status.get("NoNewPrivs") != "1":
    blocked("namespace final verifier requires no_new_privs")

try:
    rows = Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines()
except OSError:
    blocked("namespace final verifier cannot inspect mountinfo")
matches = []
for row in rows:
    before, separator, after = row.partition(" - ")
    fields = before.split()
    if separator and len(fields) >= 6 and fields[4] == "/tmp":
        matches.append((fields, after.split()))
if len(matches) != 1:
    blocked("namespace final verifier has no unique private tmpfs")
fields, after = matches[0]
if (
    not after
    or after[0] != "tmpfs"
    or not {"nosuid", "nodev", "noexec"}.issubset(set(fields[5].split(",")))
    or any(field.startswith(("shared:", "master:")) for field in fields[6:])
):
    blocked("namespace final verifier private tmpfs is unsafe")

try:
    details = os.lstat("/tmp/msconnector-lighttpd-no-crs-fixture")
except OSError:
    blocked("namespace final verifier fixture root is unavailable")
if (
    not stat.S_ISDIR(details.st_mode)
    or details.st_uid != os.geteuid()
    or stat.S_IMODE(details.st_mode) != 0o700
):
    blocked("namespace final verifier fixture root is unsafe")
os.environ["LIGHTTPD_NO_CRS_FIXTURE_ROOT_IDENTITY"] = f"{details.st_dev}:{details.st_ino}"
os.execvpe(sys.argv[1], sys.argv[1:], os.environ)
'''

SYSTEM_READONLY_BINDS = (
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/lib"),
    Path("/lib64"),
    Path("/etc"),
)
MAX_READONLY_BINDS = 16

PR_SET_PDEATHSIG = 1
LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.prctl.argtypes = [
    ctypes.c_int,
    ctypes.c_ulong,
    ctypes.c_ulong,
    ctypes.c_ulong,
    ctypes.c_ulong,
]
LIBC.prctl.restype = ctypes.c_int


class NamespaceUnavailable(RuntimeError):
    """The trusted private namespace boundary cannot be proved available."""


@dataclass(frozen=True)
class CallerIdentity:
    """The sole host identity eligible for the one-identity namespace map."""

    uid: int
    gid: int


def _bounded_timeout(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("timeout must be numeric") from error
    if not 0 < parsed <= MAX_TIMEOUT_SECONDS:
        raise argparse.ArgumentTypeError(
            f"timeout must be in the range (0, {MAX_TIMEOUT_SECONDS:g}]"
        )
    return parsed


def _caller_identity() -> CallerIdentity:
    if os.name != "posix" or sys.platform != "linux":
        raise NamespaceUnavailable("No-CRS fixture namespace requires Linux")
    if os.geteuid() == 0 or os.getegid() == 0:
        raise NamespaceUnavailable("No-CRS fixture namespace launcher refuses a host-root caller")
    if os.getuid() != os.geteuid() or os.getgid() != os.getegid():
        raise NamespaceUnavailable("No-CRS fixture namespace launcher refuses set-id callers")
    return CallerIdentity(uid=os.geteuid(), gid=os.getegid())


def _require_trusted_system_executable(path: Path) -> None:
    """Accept only a root-owned, non-writable executable below trusted dirs."""

    if not path.is_absolute() or path.parent not in {Path("/usr/bin"), Path("/bin")}:
        raise NamespaceUnavailable(f"trusted namespace binary path is invalid: {path}")
    for directory in (Path("/"), Path("/usr"), Path("/usr/bin")):
        try:
            details = directory.lstat()
        except OSError as error:
            raise NamespaceUnavailable(f"cannot inspect trusted directory: {directory}") from error
        if (
            not stat.S_ISDIR(details.st_mode)
            or details.st_uid != 0
            or stat.S_IMODE(details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
        ):
            raise NamespaceUnavailable(f"trusted directory is unsafe: {directory}")
    try:
        details = path.lstat()
    except OSError as error:
        raise NamespaceUnavailable(f"trusted namespace binary is unavailable: {path}") from error
    if stat.S_ISLNK(details.st_mode):
        try:
            resolved = path.resolve(strict=True)
            resolved_details = resolved.lstat()
        except OSError as error:
            raise NamespaceUnavailable(f"trusted namespace binary symlink is unsafe: {path}") from error
        if (
            resolved.parent != Path("/usr/bin")
            or not stat.S_ISREG(resolved_details.st_mode)
            or resolved_details.st_uid != 0
            or stat.S_IMODE(resolved_details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
            or not resolved_details.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        ):
            raise NamespaceUnavailable(f"trusted namespace binary symlink is unsafe: {path}")
        return
    if (
        not stat.S_ISREG(details.st_mode)
        or details.st_uid != 0
        or stat.S_IMODE(details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
        or not details.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    ):
        raise NamespaceUnavailable(f"trusted namespace binary is unsafe: {path}")


def _require_trusted_system_binaries() -> None:
    for path in (
        TRUSTED_UNSHARE,
        TRUSTED_BWRAP,
        TRUSTED_DASH,
        TRUSTED_MOUNT,
        TRUSTED_PYTHON,
    ):
        _require_trusted_system_executable(path)


def _require_trusted_system_bind_root(path: Path) -> None:
    """Require a root-owned, non-writable system tree before ro-binding it."""

    try:
        source = path.resolve(strict=True)
    except OSError as error:
        raise NamespaceUnavailable(f"trusted system bind root is unavailable: {path}") from error
    if not source.is_absolute() or (
        source != Path("/etc") and not _is_beneath(source, Path("/usr"))
    ):
        raise NamespaceUnavailable(f"trusted system bind root is outside the fixed system roots: {path}")
    current = source
    while current != current.parent:
        try:
            details = current.lstat()
        except OSError as error:
            raise NamespaceUnavailable(f"cannot inspect trusted system bind root: {path}") from error
        if (
            not stat.S_ISDIR(details.st_mode)
            or details.st_uid != 0
            or stat.S_IMODE(details.st_mode) & (stat.S_IWGRP | stat.S_IWOTH)
        ):
            raise NamespaceUnavailable(f"trusted system bind root is unsafe: {path}")
        current = current.parent


def _validate_command(command: Sequence[str]) -> list[str]:
    if not command or len(command) > MAX_ARGUMENTS:
        raise NamespaceUnavailable("namespace harness command has an invalid argument count")
    result: list[str] = []
    for index, value in enumerate(command):
        if not isinstance(value, str) or not value or len(value) > MAX_ARGUMENT_LENGTH:
            raise NamespaceUnavailable("namespace harness command has an unsafe argument")
        if "\x00" in value or "\n" in value or "\r" in value:
            raise NamespaceUnavailable("namespace harness command has an unsafe argument")
        if index == 0 and not os.path.isabs(value):
            raise NamespaceUnavailable("namespace harness command must start with an absolute executable")
        result.append(value)
    return result


_FORWARDED_ENVIRONMENT = (
    "BUILD_ROOT",
    "CACHE_ROOT",
    "CONNECTOR_COMPONENT_CACHE",
    "CONNECTOR_ROOT",
    "FRAMEWORK_ROOT",
    "FULL_LIFECYCLE_EVIDENCE_OUTPUT",
    "FULL_LIFECYCLE_EXECUTED_TARGET",
    "FULL_LIFECYCLE_HOST_PROFILE",
    "HOME",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "LIGHTTPD_CONFIG_ROOT",
    "LIGHTTPD_CONNECTOR_BUILD_ROOT",
    "LIGHTTPD_EXPOSE_HOST_TRANSACTION_ID",
    "LIGHTTPD_INCLUDE_DIR",
    "LIGHTTPD_LOG_ROOT",
    "LIGHTTPD_MODULE_DIR",
    "LIGHTTPD_PATCHED_ROOT",
    "LIGHTTPD_PATCHED_SMOKE_DIR",
    "LIGHTTPD_RESULT_ROOT",
    "LIGHTTPD_SMOKE_PORT",
    "LOG_ROOT",
    "MODSECURITY_INCLUDE_DIR",
    "MODSECURITY_LIB_DIR",
    "MODSECURITY_PREFIX",
    "MSCONNECTOR_CRS_RUNTIME",
    "MSCONNECTOR_EXPECTED_RULE_ID",
    "MSCONNECTOR_RULES_FILE",
    "NO_CRS_ARTIFACT_PROFILE",
    "NO_CRS_RUN_ID",
    "NO_CRS_SELECTED_CASE_IDS",
    "PARENT_HOST_RUNTIME_ROOT",
    "PYTHON",
    "RESULTS_DIR",
    "RUNTIME_BASE",
    "RUNTIME_ROOT",
    "TMP_ROOT",
    "VERIFIED_RUN_ROOT",
)


def _child_environment(base: Mapping[str, str]) -> dict[str, str]:
    """Forward only bounded data values after bwrap clears the environment."""

    result = {
        "PATH": SAFE_PATH,
        "HOME": str(PRIVATE_TMPFS_MOUNT),
        "TMPDIR": str(PRIVATE_TMPFS_MOUNT),
        "TMP": str(PRIVATE_TMPFS_MOUNT),
        "TEMP": str(PRIVATE_TMPFS_MOUNT),
        "LIGHTTPD_NO_CRS_FIXTURE_ROOT": str(FIXTURE_ROOT),
        "LIGHTTPD_NO_CRS_FIXTURE_NAMESPACE_ACTIVE": "1",
    }
    for name in _FORWARDED_ENVIRONMENT:
        if name == "HOME":
            continue
        value = base.get(name)
        if value is None:
            continue
        if not isinstance(value, str) or len(value) > MAX_ARGUMENT_LENGTH:
            raise NamespaceUnavailable(f"namespace environment value for {name} is unsafe")
        if "\x00" in value or "\n" in value or "\r" in value:
            raise NamespaceUnavailable(f"namespace environment value for {name} is unsafe")
        result[name] = value
    return result


def _safe_production_writable_root(environment: Mapping[str, str]) -> Path:
    """Materialize exactly the Parent-owned Lighttpd host runtime root.

    bwrap presents the rest of the host root read-only. The one writable bind
    is intentionally the existing Parent runtime output root, never `/tmp`, a
    broad cache, or an arbitrary caller-selected directory.
    """

    runtime_root_value = environment.get("RUNTIME_ROOT")
    smoke_root_value = environment.get("LIGHTTPD_PATCHED_SMOKE_DIR")
    parent_host_value = environment.get("PARENT_HOST_RUNTIME_ROOT")
    verified_root_value = environment.get("VERIFIED_RUN_ROOT")
    evidence_value = environment.get("FULL_LIFECYCLE_EVIDENCE_OUTPUT")
    if not all((runtime_root_value, smoke_root_value, verified_root_value, evidence_value)):
        raise NamespaceUnavailable("No-CRS namespace requires Parent-owned Lighttpd runtime roots")
    runtime_root = Path(runtime_root_value)
    smoke_root = Path(smoke_root_value)
    parent_host = Path(parent_host_value) if parent_host_value else None
    verified_root = Path(verified_root_value)
    evidence = Path(evidence_value)
    if not all(path.is_absolute() for path in (runtime_root, smoke_root, verified_root, evidence)):
        raise NamespaceUnavailable("No-CRS namespace runtime roots must be absolute")
    with_crs_smoke = runtime_root / "host"
    no_crs_smoke = verified_root / "lighttpd-runtime"
    if parent_host is not None and not parent_host.is_absolute():
        raise NamespaceUnavailable("No-CRS namespace Parent host runtime root must be absolute")
    if smoke_root == with_crs_smoke and parent_host == with_crs_smoke:
        expected_smoke = with_crs_smoke
    elif smoke_root == no_crs_smoke and parent_host is None:
        expected_smoke = no_crs_smoke
    else:
        raise NamespaceUnavailable("No-CRS namespace writable root is not an exact Parent Lighttpd runtime root")
    if evidence != expected_smoke / "first-byte-evidence.json":
        raise NamespaceUnavailable("No-CRS namespace evidence output is not the exact Parent runtime artifact")
    patched_root_value = environment.get("LIGHTTPD_PATCHED_ROOT")
    if not patched_root_value:
        raise NamespaceUnavailable("No-CRS namespace requires the pinned patched Lighttpd root")
    _require_real_directory(Path(patched_root_value), "patched Lighttpd runtime root")
    try:
        script_directory = Path(__file__).resolve().parent
        if str(script_directory) not in sys.path:
            sys.path.insert(0, str(script_directory))
        from safe_runtime_output import verified_runtime_output_root

        verified_runtime_output_root(smoke_root)
    except (ImportError, OSError, ValueError) as error:
        raise NamespaceUnavailable("No-CRS namespace writable root is unsafe") from error
    if smoke_root == PRIVATE_TMPFS_MOUNT or PRIVATE_TMPFS_MOUNT in smoke_root.parents:
        raise NamespaceUnavailable("No-CRS namespace writable root must not overlay private /tmp")
    return smoke_root


def _require_production_harness(command: Sequence[str]) -> None:
    """Accept the one full-lifecycle entrypoint used by the Parent runner."""

    harness = _validate_command(command)
    expected = _repository_root() / "connectors/lighttpd/harness/run_patched_full_lifecycle.sh"
    if len(harness) != 2 or harness[0] != "/bin/sh" or Path(harness[1]) != expected:
        raise NamespaceUnavailable("No-CRS namespace command is not the pinned Parent lifecycle harness")


def _is_beneath(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _require_real_directory(path: Path, label: str) -> Path:
    """Return one absolute, non-symlink directory safe to ro-bind.

    These roots are selected before any capability-bearing setup begins. They
    can only become visible to the harness read-only, while the sole writable
    runtime output root is bound separately after them.
    """

    if not path.is_absolute() or path == Path("/"):
        raise NamespaceUnavailable(f"{label} must be one non-root absolute directory")
    if path == PRIVATE_TMPFS_MOUNT or PRIVATE_TMPFS_MOUNT in path.parents:
        raise NamespaceUnavailable(f"{label} must not use the private tmpfs path")
    try:
        details = path.lstat()
    except OSError as error:
        raise NamespaceUnavailable(f"{label} is unavailable") from error
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISDIR(details.st_mode):
        raise NamespaceUnavailable(f"{label} must be a real directory")
    return path


def _repository_root() -> Path:
    try:
        root = Path(__file__).resolve().parents[3]
    except (OSError, IndexError) as error:
        raise NamespaceUnavailable("cannot locate the Parent repository root") from error
    return _require_real_directory(root, "Parent repository root")


def _readonly_runtime_bind_roots(environment: Mapping[str, str]) -> list[Path]:
    """Build the minimum read-only view required by the full host lifecycle."""

    repository_root = _repository_root()
    connector_root = environment.get("CONNECTOR_ROOT")
    if connector_root is not None and Path(connector_root) != repository_root:
        raise NamespaceUnavailable("namespace CONNECTOR_ROOT is not the active Parent checkout")
    framework_root = Path(
        environment.get("FRAMEWORK_ROOT", str(repository_root / "modules/ModSecurity-test-Framework"))
    )
    if framework_root != repository_root / "modules/ModSecurity-test-Framework":
        raise NamespaceUnavailable("namespace FRAMEWORK_ROOT is not the Parent framework gitlink")

    candidate_roots = [repository_root]
    for name in ("LIGHTTPD_PATCHED_ROOT", "MODSECURITY_LIB_DIR", "MODSECURITY_PREFIX"):
        value = environment.get(name)
        if value:
            candidate_roots.append(Path(value))
    python_value = environment.get("PYTHON")
    if python_value and os.path.isabs(python_value):
        python_path = Path(python_value)
        try:
            resolved_python = python_path.resolve(strict=True)
        except OSError as error:
            raise NamespaceUnavailable("namespace PYTHON is unavailable") from error
        if not _is_beneath(resolved_python, Path("/usr")):
            candidate_roots.append(resolved_python.parent.parent)

    result: list[Path] = []
    trusted_roots = (*SYSTEM_READONLY_BINDS,)
    for candidate in candidate_roots:
        root = _require_real_directory(Path(os.path.abspath(candidate)), "namespace read-only runtime root")
        if any(_is_beneath(root, trusted) for trusted in trusted_roots):
            continue
        if any(_is_beneath(root, existing) for existing in result):
            continue
        result = [existing for existing in result if not _is_beneath(existing, root)]
        result.append(root)
    if len(result) > MAX_READONLY_BINDS:
        raise NamespaceUnavailable("namespace read-only runtime roots exceed the bounded limit")
    return result


def _namespace_bind_arguments(
    *,
    environment: Mapping[str, str],
    writable_roots: Sequence[Path],
) -> list[str]:
    """Return only fixed system, read-only runtime, tmpfs and output binds."""

    arguments: list[str] = []
    for system_root in SYSTEM_READONLY_BINDS:
        _require_trusted_system_bind_root(system_root)
        arguments.extend(("--ro-bind", str(system_root), str(system_root)))
    for runtime_root in _readonly_runtime_bind_roots(environment):
        arguments.extend(("--ro-bind", str(runtime_root), str(runtime_root)))
    # This is the noexec tmpfs created by the fixed outer system-binary setup,
    # not a host /tmp bind. The bwrap bind keeps its mount flags intact.
    arguments.extend(("--bind", str(PRIVATE_TMPFS_MOUNT), str(PRIVATE_TMPFS_MOUNT)))

    seen: set[Path] = set()
    for root in writable_roots:
        root = Path(root)
        if not root.is_absolute() or root in seen:
            raise NamespaceUnavailable("namespace writable bind root is invalid")
        _require_real_directory(root, "namespace writable runtime root")
        if root == PRIVATE_TMPFS_MOUNT or PRIVATE_TMPFS_MOUNT in root.parents:
            raise NamespaceUnavailable("namespace writable root must not use private /tmp")
        seen.add(root)
        arguments.extend(("--bind", str(root), str(root)))
    return arguments


def build_trusted_namespace_command(
    command: Sequence[str],
    *,
    environment: Mapping[str, str],
    writable_roots: Sequence[Path] = (),
    info_descriptor: int | None = None,
) -> list[str]:
    """Build the fixed system-binary-only setup chain.

    The outer ``unshare`` performs the explicit propagation change before it
    executes bwrap. bwrap owns the only capability-bearing inner setup and
    clears its bounding set before the supplied command is reached.
    """

    harness = _validate_command(command)
    child_environment = _child_environment(environment)
    binds = _namespace_bind_arguments(
        environment=environment,
        writable_roots=writable_roots,
    )
    if info_descriptor is None or info_descriptor < 3:
        raise NamespaceUnavailable("namespace setup attestation descriptor is invalid")

    bwrap = [
        str(TRUSTED_BWRAP),
        "--unshare-user",
        "--unshare-pid",
        "--disable-userns",
        "--assert-userns-disabled",
        "--die-with-parent",
        "--new-session",
        *binds,
        # bwrap creates the fixed root while it still owns the namespace
        # setup. Harness code receives only this private, mode-0700 child.
        "--dir",
        str(FIXTURE_ROOT),
        "--chmod",
        "0700",
        str(FIXTURE_ROOT),
        "--proc",
        "/proc",
        "--dev",
        "/dev",
        "--uid",
        "0",
        "--gid",
        "0",
        "--cap-drop",
        "ALL",
        "--info-fd",
        str(info_descriptor),
        "--clearenv",
    ]
    for name, value in sorted(child_environment.items()):
        bwrap.extend(("--setenv", name, value))
    bwrap.extend(("--", str(TRUSTED_PYTHON), "-c", FINAL_NAMESPACE_STATE_VERIFIER, *harness))
    return [
        str(TRUSTED_UNSHARE),
        "--user",
        "--map-root-user",
        "--mount",
        "--pid",
        "--fork",
        "--kill-child=SIGKILL",
        "--mount-proc=/proc",
        "--propagation",
        "private",
        str(TRUSTED_DASH),
        "-c",
        PRIVATE_TMPFS_SETUP,
        "lighttpd-no-crs-private-tmpfs",
        *bwrap,
    ]


def _linux_prctl(option: int, first: int, label: str) -> None:
    if LIBC.prctl(option, first, 0, 0, 0) == 0:
        return
    error = ctypes.get_errno()
    raise NamespaceUnavailable(f"{label} is unavailable: {os.strerror(error)}")


def _arm_parent_death_signal() -> None:
    """Reject the small parent-death setup race before execing unshare."""

    parent = os.getppid()
    if parent <= 1:
        raise NamespaceUnavailable("namespace supervisor has no live parent")
    _linux_prctl(PR_SET_PDEATHSIG, signal.SIGKILL, "parent-death signal setup")
    if os.getppid() != parent:
        raise NamespaceUnavailable("namespace supervisor disappeared during parent-death setup")


def _seal_inherited_descriptors(kept: set[int]) -> None:
    """Prevent caller-provided descriptors crossing the privileged setup edge."""

    try:
        entries = os.listdir("/proc/self/fd")
    except OSError as error:
        raise NamespaceUnavailable("cannot inspect inherited namespace descriptors") from error
    for entry in entries:
        try:
            descriptor = int(entry, 10)
        except ValueError:
            continue
        if descriptor in kept:
            continue
        try:
            os.set_inheritable(descriptor, False)
        except OSError as error:
            if error.errno != errno.EBADF:
                raise NamespaceUnavailable("cannot seal inherited namespace descriptor") from error


def _read_setup_attestation(descriptor: int, child: int) -> None:
    """Require bwrap's setup record before treating later exits as harness exits."""

    deadline = time.monotonic() + SETUP_TIMEOUT_SECONDS
    payload = bytearray()
    try:
        while time.monotonic() < deadline:
            ready, _write, _error = select.select([descriptor], [], [], 0.05)
            if not ready:
                try:
                    pid, _status = os.waitpid(child, os.WNOHANG)
                except ChildProcessError:
                    raise NamespaceUnavailable("namespace setup child disappeared") from None
                if pid == child:
                    raise NamespaceUnavailable("trusted namespace setup did not attest readiness")
                continue
            chunk = os.read(descriptor, 4096)
            if not chunk:
                break
            payload.extend(chunk)
            if len(payload) > 16384:
                raise NamespaceUnavailable("trusted namespace setup attestation is too large")
            try:
                record = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if (
                not isinstance(record, dict)
                or not isinstance(record.get("child-pid"), int)
                or record["child-pid"] <= 0
                or not isinstance(record.get("mnt-namespace"), int)
                or record["mnt-namespace"] <= 0
                or not isinstance(record.get("pid-namespace"), int)
                or record["pid-namespace"] <= 0
            ):
                raise NamespaceUnavailable("trusted namespace setup attestation is invalid")
            return
    finally:
        os.close(descriptor)
    raise NamespaceUnavailable("trusted namespace setup attestation timed out")


def _terminate_and_reap(child: int) -> None:
    """Bounded process-group cleanup for the direct trusted unshare child."""

    try:
        pid, _status = os.waitpid(child, os.WNOHANG)
    except ChildProcessError:
        return
    if pid == child:
        return
    for signum in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(child, signum)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + CHILD_STOP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            try:
                pid, _status = os.waitpid(child, os.WNOHANG)
            except ChildProcessError:
                return
            if pid == child:
                return
            time.sleep(0.05)
    raise NamespaceUnavailable("trusted namespace supervisor did not stop after bounded SIGTERM/SIGKILL")


def _wait_for_child(child: int, timeout_seconds: float) -> int:
    """Wait boundedly and preserve a caller signal as a regular cleanup case."""

    deadline = time.monotonic() + timeout_seconds
    interruption: list[int] = []

    def record_signal(signum: int, _frame: object) -> None:
        interruption.append(signum)

    previous = {
        signum: signal.signal(signum, record_signal)
        for signum in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)
    }
    try:
        while True:
            pid, status = os.waitpid(child, os.WNOHANG)
            if pid == child:
                return os.waitstatus_to_exitcode(status)
            if interruption:
                _terminate_and_reap(child)
                return 128 + interruption[0]
            if time.monotonic() >= deadline:
                _terminate_and_reap(child)
                return EXIT_TIMEOUT
            time.sleep(0.05)
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def run_isolated(
    command: Sequence[str],
    *,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    environment: Mapping[str, str] | None = None,
    writable_roots: Sequence[Path] = (),
) -> int:
    """Run after the trusted setup boundary as the invoking non-root identity."""

    _caller_identity()
    if not 0 < timeout_seconds <= MAX_TIMEOUT_SECONDS:
        raise NamespaceUnavailable("namespace timeout is invalid")
    _require_trusted_system_binaries()
    setup_read, setup_write = os.pipe()
    os.set_inheritable(setup_write, True)
    child = -1
    try:
        arguments = build_trusted_namespace_command(
            command,
            environment=os.environ if environment is None else environment,
            writable_roots=writable_roots,
            info_descriptor=setup_write,
        )
        child = os.fork()
        if child == 0:
            try:
                os.close(setup_read)
                os.setsid()
                _arm_parent_death_signal()
                _seal_inherited_descriptors({0, 1, 2, setup_write})
                os.execve(str(TRUSTED_UNSHARE), arguments, {"PATH": SAFE_PATH})
            except NamespaceUnavailable as error:
                print(f"No-CRS namespace blocked: {error}", file=sys.stderr)
                os._exit(EXIT_BLOCKED)
            except BaseException as error:
                print(f"No-CRS namespace setup failed: {error}", file=sys.stderr)
                os._exit(126)
        os.close(setup_write)
        setup_write = -1
        _read_setup_attestation(setup_read, child)
        setup_read = -1
        return _wait_for_child(child, timeout_seconds)
    except BaseException:
        if child > 0:
            _terminate_and_reap(child)
        raise
    finally:
        for descriptor in (setup_read, setup_write):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout-seconds", type=_bounded_timeout, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    if not arguments.command or arguments.command[0] != "--":
        parser.error("one absolute harness command must follow --")
    arguments.command = arguments.command[1:]
    if not arguments.command or not os.path.isabs(arguments.command[0]):
        parser.error("the harness command must be absolute")
    return arguments


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        writable_root = _safe_production_writable_root(os.environ)
        _require_production_harness(arguments.command)
        return run_isolated(
            arguments.command,
            timeout_seconds=arguments.timeout_seconds,
            writable_roots=(writable_root,),
        )
    except NamespaceUnavailable as error:
        print(f"lighttpd_no_crs_fixture_namespace: BLOCKED: {error}", file=sys.stderr)
        return EXIT_BLOCKED
    except (OSError, RuntimeError, ValueError) as error:
        print(f"lighttpd_no_crs_fixture_namespace: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
