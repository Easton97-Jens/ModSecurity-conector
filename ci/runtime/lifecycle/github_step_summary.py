"""Safely append bounded content to a GitHub Actions step summary file."""

from __future__ import annotations

import os
import re
import stat
from collections.abc import Mapping
from pathlib import Path


SUMMARY_DIRECTORY_NAME = "_runner_file_commands"
SUMMARY_FILE_NAME = re.compile(r"^step_summary_[A-Za-z0-9_-]+$", re.ASCII)
UNSAFE_SUMMARY_PATH = "GitHub step summary path is unsafe"


def _write_summary(descriptor: int, content: str) -> None:
    data = content.encode("utf-8")
    while data:
        written = os.write(descriptor, data)
        if written <= 0:
            raise OSError("cannot append GitHub step summary")
        data = data[written:]


def _safe_open_flags() -> tuple[int, int, int, int]:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if (
        not isinstance(nofollow, int)
        or not isinstance(directory, int)
        or not isinstance(nonblock, int)
    ):
        raise ValueError("GitHub step summary safe-open capability is unavailable")
    return nofollow, directory, nonblock, getattr(os, "O_CLOEXEC", 0)


def _open_directory_without_symlinks(path: Path) -> int:
    if (
        not path.is_absolute()
        or path == Path("/")
        or os.path.normpath(os.fspath(path)) != os.fspath(path)
    ):
        raise ValueError(UNSAFE_SUMMARY_PATH)
    nofollow, directory, _nonblock, close_on_exec = _safe_open_flags()
    descriptor = -1
    try:
        descriptor = os.open(path.anchor, os.O_RDONLY | directory | close_on_exec)
        for component in path.parts[1:]:
            next_descriptor = os.open(
                component,
                os.O_RDONLY | directory | nofollow | close_on_exec,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
    except OSError as error:
        if descriptor >= 0:
            os.close(descriptor)
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    return descriptor


def _require_trusted_directory(descriptor: int) -> None:
    details = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(details.st_mode)
        or details.st_uid != os.geteuid()
        or details.st_mode & 0o022
    ):
        raise ValueError("GitHub step summary directory is unsafe")


def _open_github_step_summary(environment: Mapping[str, str]) -> int:
    runner_temp_value = environment.get("RUNNER_TEMP", "")
    summary_value = environment.get("GITHUB_STEP_SUMMARY", "")
    runner_temp = Path(runner_temp_value)
    runner_descriptor = -1
    summary_parent_descriptor = -1
    summary_descriptor = -1
    try:
        if not summary_value:
            raise ValueError("GitHub step summary path is unavailable")
        nofollow, directory, nonblock, close_on_exec = _safe_open_flags()
        runner_descriptor = _open_directory_without_symlinks(runner_temp)
        _require_trusted_directory(runner_descriptor)
        summary_path = Path(summary_value)
        if not summary_path.is_absolute() or os.path.normpath(summary_value) != summary_value:
            raise ValueError(UNSAFE_SUMMARY_PATH)
        try:
            relative = summary_path.relative_to(runner_temp)
        except ValueError as error:
            raise ValueError(UNSAFE_SUMMARY_PATH) from error
        if (
            len(relative.parts) != 2
            or relative.parts[0] != SUMMARY_DIRECTORY_NAME
            or not SUMMARY_FILE_NAME.fullmatch(relative.parts[1])
        ):
            raise ValueError(UNSAFE_SUMMARY_PATH)
        summary_parent_descriptor = os.open(
            SUMMARY_DIRECTORY_NAME,
            os.O_RDONLY | directory | nofollow | close_on_exec,
            dir_fd=runner_descriptor,
        )
        _require_trusted_directory(summary_parent_descriptor)
        summary_descriptor = os.open(
            relative.parts[1],
            os.O_WRONLY | os.O_APPEND | nofollow | nonblock | close_on_exec,
            dir_fd=summary_parent_descriptor,
        )
        details = os.fstat(summary_descriptor)
        if (
            not stat.S_ISREG(details.st_mode)
            or details.st_uid != os.geteuid()
            or details.st_mode & 0o022
            or details.st_nlink != 1
        ):
            raise ValueError("GitHub step summary file is unsafe")
        result = summary_descriptor
        summary_descriptor = -1
        return result
    except OSError as error:
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    finally:
        if runner_descriptor >= 0:
            os.close(runner_descriptor)
        if summary_parent_descriptor >= 0:
            os.close(summary_parent_descriptor)
        if summary_descriptor >= 0:
            os.close(summary_descriptor)


def append_github_step_summary(environment: Mapping[str, str], content: str) -> None:
    descriptor = _open_github_step_summary(environment)
    try:
        _write_summary(descriptor, content)
    finally:
        os.close(descriptor)
