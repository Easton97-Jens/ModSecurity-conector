"""Launch the Stock sidecar using a checked-in argv record and private spool.

Run as the sidecar service UID. Existing unsafe paths are rejected, never fixed
by chmod. --install-root relocates absolute config/spool paths for staged installs.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import stat


def read_arguments(record: Path, install_root: Path = Path("/")) -> list[str]:
    if not install_root.is_absolute() or ".." in install_root.parts:
        raise ValueError("install root must be canonical and absolute")
    arguments = shlex.split(record.read_text(encoding="utf-8"), comments=True)
    if len(arguments) % 2 or len(set(arguments[::2])) != len(arguments) // 2:
        raise ValueError("argv record must contain unique option/value pairs")
    allowed = {"--config", "--listen", "--upstream", "--timeout-ms",
               "--spool-directory", "--spool-capacity-bytes", "--spool-free-reserve-bytes"}
    if not set(arguments[::2]) <= allowed or not {"--config", "--listen", "--upstream", "--spool-directory"} <= set(arguments[::2]):
        raise ValueError("argv record lacks required options or contains unsupported options")
    for option in ("--config", "--spool-directory"):
        index = arguments.index(option) + 1
        path = Path(arguments[index])
        if not path.is_absolute() or ".." in path.parts or str(path) != arguments[index]:
            raise ValueError("config and spool paths must be canonical and absolute")
        arguments[index] = str(install_root / path.relative_to("/"))
    return arguments


def prepare_spool(path: Path) -> None:
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("spool path must be canonical and absolute")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    descriptor = os.open("/", flags)
    try:
        for index, component in enumerate(path.parts[1:]):
            final = index == len(path.parts) - 2
            parent_info = os.fstat(descriptor)
            if parent_info.st_uid not in (0, os.geteuid()) or (
                parent_info.st_mode & 0o022 and not parent_info.st_mode & stat.S_ISVTX
            ):
                raise ValueError("unsafe writable or foreign spool ancestor")
            try:
                os.mkdir(component, 0o700 if final else 0o755, dir_fd=descriptor)
            except FileExistsError:
                pass
            child = os.open(component, flags, dir_fd=descriptor)
            try:
                parent_info, info = os.fstat(descriptor), os.fstat(child)
                if parent_info.st_uid not in (0, os.geteuid()) or info.st_uid not in (0, os.geteuid()):
                    raise ValueError("spool ancestors must belong to root or the effective UID")
                if parent_info.st_mode & 0o022 and not (parent_info.st_mode & stat.S_ISVTX and info.st_uid == os.geteuid()):
                    raise ValueError("unsafe writable spool ancestor")
                if final and (info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700):
                    raise ValueError("spool must belong to effective UID with mode 0700")
            except BaseException:
                os.close(child)
                raise
            os.close(descriptor)
            descriptor = child
        filesystem = os.fstatvfs(descriptor)
        if filesystem.f_flag & os.ST_RDONLY:
            raise ValueError("spool filesystem is read-only")
    finally:
        os.close(descriptor)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--args-file", required=True, type=Path)
    parser.add_argument("--install-root", type=Path, default=Path("/"))
    options = parser.parse_args()
    try:
        arguments = read_arguments(options.args_file, options.install_root)
        prepare_spool(Path(arguments[arguments.index("--spool-directory") + 1]))
    except (OSError, ValueError) as error:
        parser.exit(78, f"private request spool unavailable: {error}\n")
    os.execv(str(options.binary), [str(options.binary), *arguments])


if __name__ == "__main__":
    main()
