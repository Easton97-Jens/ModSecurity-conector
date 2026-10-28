"""Launch one repository Stock profile with its installed native sidecar.

The executable has a fixed component path below --install-root. Profile records
are repository-owned; arbitrary executable paths and argv files are unsupported.
Run as the service UID; existing unsafe spool paths are rejected without chmod.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import stat

PROFILE_RECORDS = {
    "all": Path(__file__).resolve().parents[2] / "examples/lighttpd/stock/all/stock-sidecar.args",
    "off": Path(__file__).resolve().parents[2] / "examples/lighttpd/stock/off/stock-sidecar.args",
    "safe": Path(__file__).resolve().parents[2] / "examples/lighttpd/stock/safe/stock-sidecar.args",
    "strict": Path(__file__).resolve().parents[2] / "examples/lighttpd/stock/strict/stock-sidecar.args",
}
CONFIG_NAMES = {"all": "all", "off": "minimal", "safe": "safe", "strict": "strict"}
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC


def canonical_absolute(path: Path) -> None:
    if not path.is_absolute() or ".." in path.parts or str(path).startswith("//"):
        raise ValueError("installation and spool paths must be canonical and absolute")


def read_arguments(profile: str, install_root: Path = Path("/")) -> list[str]:
    canonical_absolute(install_root)
    if profile not in PROFILE_RECORDS:
        raise ValueError("unsupported Stock profile")
    arguments = shlex.split(PROFILE_RECORDS[profile].read_text(encoding="utf-8"), comments=True)
    if len(arguments) % 2 or len(set(arguments[::2])) != len(arguments) // 2:
        raise ValueError("argv record must contain unique option/value pairs")
    expected = {"--config": f"/etc/lighttpd/msconnector-stock-{CONFIG_NAMES[profile]}.conf",
                "--listen": "127.0.0.1:8080", "--upstream": "127.0.0.1:8081",
                "--spool-directory": f"/var/lib/msconnector/lighttpd-stock/{profile}"}
    numeric = {"--timeout-ms", "--spool-capacity-bytes", "--spool-free-reserve-bytes"}
    values = dict(zip(arguments[::2], arguments[1::2]))
    if expected.keys() - values.keys() or values.keys() - (expected.keys() | numeric):
        raise ValueError("argv record violates the closed Stock option contract")
    for option, expected_value in expected.items():
        if values[option] != expected_value:
            raise ValueError("argv record violates the selected Stock profile")
    for option in values.keys() & numeric:
        value = values[option]
        if not value.isascii() or not value.isdecimal() or not 0 < int(value) <= (1 << 64) - 1:
            raise ValueError("technical options require positive bounded decimal values")
    for option in ("--config", "--spool-directory"):
        index = arguments.index(option) + 1
        arguments[index] = str(install_root / Path(values[option]).relative_to("/"))
    return arguments


def check_parent(info: os.stat_result) -> None:
    if info.st_uid not in (0, os.geteuid()):
        raise ValueError("spool ancestors must belong to root or the effective UID")
    if info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX:
        raise ValueError("unsafe writable spool ancestor")


def check_child(parent: os.stat_result, info: os.stat_result, private: bool) -> None:
    if info.st_uid not in (0, os.geteuid()):
        raise ValueError("foreign directory owner")
    if parent.st_mode & 0o022 and info.st_uid != os.geteuid():
        raise ValueError("unsafe sticky directory child")
    if private and (info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700):
        raise ValueError("spool must belong to effective UID with mode 0700")


def open_child(parent_fd: int, component: str, private: bool, create: bool) -> int:
    parent = os.fstat(parent_fd)
    check_parent(parent)
    if create:
        try:
            os.mkdir(component, 0o700 if private else 0o755, dir_fd=parent_fd)
        except FileExistsError:
            pass
    child = os.open(component, DIRECTORY_FLAGS, dir_fd=parent_fd)
    try:
        check_child(parent, os.fstat(child), private)
    except BaseException:
        os.close(child)
        raise
    return child


def open_directory(path: Path, create: bool = False, private: bool = False) -> int:
    canonical_absolute(path)
    descriptor = os.open("/", DIRECTORY_FLAGS)
    try:
        for index, component in enumerate(path.parts[1:]):
            child = open_child(descriptor, component, private and index == len(path.parts) - 2, create)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def prepare_spool(path: Path) -> None:
    descriptor = open_directory(path, create=True, private=True)
    try:
        if os.fstatvfs(descriptor).f_flag & os.ST_RDONLY:
            raise ValueError("spool filesystem is read-only")
    finally:
        os.close(descriptor)


def open_component_binary(install_root: Path) -> int:
    directory = open_directory(install_root / "usr/libexec/msconnector")
    try:
        descriptor = os.open("lighttpd-stock-sidecar", os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                             dir_fd=directory)
    finally:
        os.close(directory)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_uid not in (0, os.geteuid()):
            raise ValueError("installed sidecar must be a trusted regular file")
        if info.st_mode & 0o022 or not info.st_mode & stat.S_IXUSR:
            raise ValueError("installed sidecar has unsafe permissions")
        if os.pread(descriptor, 4, 0) != b"\x7fELF":
            raise ValueError("installed Stock sidecar must be a native ELF artifact")
    except BaseException:
        os.close(descriptor)
        raise
    return descriptor


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=tuple(PROFILE_RECORDS))
    parser.add_argument("--install-root", type=Path, default=Path("/"))
    options = parser.parse_args()
    try:
        arguments = read_arguments(options.profile, options.install_root)
        descriptor = open_component_binary(options.install_root)
        try:
            prepare_spool(Path(arguments[arguments.index("--spool-directory") + 1]))
            # The validated pinned descriptor prevents executable pathname replacement.
            os.execve(descriptor, ["lighttpd-stock-sidecar", *arguments], os.environ.copy())
        finally:
            os.close(descriptor)
    except (OSError, ValueError) as error:
        parser.exit(78, f"Stock installation unavailable: {error}\n")


if __name__ == "__main__":
    main()
