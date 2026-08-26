#!/usr/bin/env python3
"""Seal the fixed Lighttpd runtime artifact set from a master-controlled job.

This module deliberately accepts no candidate-supplied manifest.  The caller
provides only a candidate root and an output path; the allowlisted layout and
the manifest are generated here.  Candidate files and output directories are
used through retained descriptors, so a replacement or symlink race cannot
turn the receipt into a statement about another file.  This protects the
sealed layout only: the protected caller must establish the candidate's
provenance independently.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import stat
from typing import Mapping


MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MANIFEST_NAME = "artifact-manifest.json"
SEALED_DIRECTORY_MODE = 0o710
SEALED_EXECUTABLE_FILE_MODE = 0o550
SEALED_READONLY_FILE_MODE = 0o440
CANDIDATE_ROOT_LABEL = "candidate root"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PROVENANCE_KEYS = frozenset({"parent_sha", "framework_sha", "mrts_sha"})


class SealerError(RuntimeError):
    """Raised when the candidate cannot be sealed fail-closed."""


def _fail(message: str) -> None:
    raise SealerError(message)


@dataclass(frozen=True)
class _SourceArtifact:
    """One already-opened, fixed-layout candidate artifact."""

    relative: str
    descriptor: int
    details: os.stat_result
    mode: int
    group: int


def _absolute(path: Path | str, label: str) -> Path:
    raw = os.fspath(path)
    if not raw or "\x00" in raw or not os.path.isabs(raw):
        _fail(f"{label} must be an absolute path")
    candidate = Path(raw)
    if any(part in {"", ".", ".."} for part in candidate.parts):
        _fail(f"{label} must not contain traversal")
    return Path(os.path.normpath(raw))


def _same_entry(before: os.stat_result, after: os.stat_result) -> bool:
    return (before.st_dev, before.st_ino, before.st_mode) == (after.st_dev, after.st_ino, after.st_mode)


def _entry_details(parent_descriptor: int, name: str, label: str) -> os.stat_result:
    try:
        return os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError as error:
        _fail(f"cannot inspect {label}: {error}")


def _open_directory_component(
    parent_descriptor: int,
    component: str,
    label: str,
    *,
    expected: os.stat_result | None = None,
) -> int:
    """Open one child directory without resolving an untrusted path twice."""

    if not component or component in {".", ".."} or "/" in component:
        _fail(f"{label} contains an unsafe directory component")
    try:
        descriptor = os.open(
            component,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=parent_descriptor,
        )
    except OSError as error:
        _fail(f"cannot open {label}: {error}")
    if expected is not None and not _same_entry(expected, os.fstat(descriptor)):
        os.close(descriptor)
        _fail(f"{label} changed during candidate enumeration")
    return descriptor


def _open_absolute_directory(path: Path, label: str) -> int:
    """Resolve an absolute directory through retained no-follow descriptors."""

    descriptor = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for component in path.parts[1:]:
            next_descriptor = _open_directory_component(descriptor, component, label)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


def _require_directory_descriptor(
    descriptor: int,
    label: str,
    *,
    owner: int | None = None,
    group: int | None = None,
    mode: int | None = None,
) -> None:
    details = os.fstat(descriptor)
    if not stat.S_ISDIR(details.st_mode):
        _fail(f"{label} must be a directory")
    if owner is not None and details.st_uid != owner:
        _fail(f"{label} must be owned by root")
    if group is not None and details.st_gid != group:
        _fail(f"{label} must use the configured runtime group")
    if mode is not None and stat.S_IMODE(details.st_mode) != mode:
        _fail(f"{label} did not receive the required mode")
    if details.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        _fail(f"{label} must not be group/world writable")


def _set_runtime_group(descriptor: int, label: str, runtime_gid: int) -> None:
    """Set the root/runtime-group ownership through an already-open descriptor."""

    try:
        os.fchown(descriptor, 0, runtime_gid)
    except OSError as error:
        _fail(f"cannot assign {label} to the configured runtime group: {error}")


def _set_required_mode(descriptor: int, label: str, required_mode: int) -> None:
    """Apply the exact mode through an already-open descriptor despite a restrictive umask."""

    try:
        os.fchmod(descriptor, required_mode)
    except OSError as error:
        _fail(f"cannot set the required mode on {label}: {error}")


def _directory_names(descriptor: int, label: str) -> set[str]:
    try:
        return set(os.listdir(descriptor))
    except OSError as error:
        _fail(f"cannot enumerate {label}: {error}")


def _open_regular_file(
    parent_descriptor: int,
    name: str,
    label: str,
    *,
    expected: os.stat_result | None = None,
) -> tuple[int, os.stat_result]:
    if not name or name in {".", ".."} or "/" in name:
        _fail(f"{label} must be a safe file name")
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=parent_descriptor,
        )
    except OSError as error:
        _fail(f"cannot open {label}: {error}")
    details = os.fstat(descriptor)
    if expected is not None and not _same_entry(expected, details):
        os.close(descriptor)
        _fail(f"{label} changed during candidate enumeration")
    mode = details.st_mode
    if not stat.S_ISREG(mode):
        os.close(descriptor)
        _fail(f"{label} must be a regular file")
    if details.st_nlink != 1:
        os.close(descriptor)
        _fail(f"{label} must not be hard-linked")
    if mode & (stat.S_IWGRP | stat.S_IWOTH):
        os.close(descriptor)
        _fail(f"{label} must not be group/world writable")
    if details.st_size <= 0:
        os.close(descriptor)
        _fail(f"{label} must not be empty")
    if details.st_size > MAX_FILE_BYTES:
        os.close(descriptor)
        _fail(f"{label} exceeds the size limit")
    return descriptor, details


def _source_file(root_descriptor: int, relative: str, label: str) -> tuple[int, os.stat_result]:
    """Open a candidate file below a retained root without following dirs."""

    components = relative.split("/")
    if not components or any(not component or component in {".", ".."} for component in components):
        _fail(f"{label} must be a safe relative path")
    directory = os.dup(root_descriptor)
    try:
        for component in components[:-1]:
            expected = _entry_details(directory, component, label)
            next_directory = _open_directory_component(directory, component, label, expected=expected)
            os.close(directory)
            directory = next_directory
        expected = _entry_details(directory, components[-1], label)
        return _open_regular_file(directory, components[-1], label, expected=expected)
    finally:
        os.close(directory)


def _copy_stable(source: _SourceArtifact, output_directory: int, output_name: str) -> tuple[str, int]:
    """Hash and copy one source inode, rejecting changes during the copy."""

    descriptor = source.descriptor
    before = source.details
    label = source.relative
    temporary_name = f".{output_name}.tmp-{os.getpid()}-{secrets.token_hex(8)}"
    try:
        try:
            out = os.open(
                temporary_name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                0o600,
                dir_fd=output_directory,
            )
        except OSError as error:
            _fail(f"cannot create sealed {label}: {error}")
        digest = hashlib.sha256()
        copied = 0
        try:
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                copied += len(chunk)
                if copied > MAX_FILE_BYTES:
                    _fail(f"{label} exceeds the size limit")
                digest.update(chunk)
                view = memoryview(chunk)
                while view:
                    written = os.write(out, view)
                    if written <= 0:
                        _fail(f"short write while sealing {label}")
                    view = view[written:]
            after = os.fstat(descriptor)
            if (
                (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
                != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
                or copied != before.st_size
            ):
                _fail(f"{label} changed while it was being sealed")
            _set_runtime_group(out, label, source.group)
            os.fchmod(out, source.mode)
            os.fsync(out)
        finally:
            os.close(out)
        os.replace(temporary_name, output_name, src_dir_fd=output_directory, dst_dir_fd=output_directory)
        return digest.hexdigest(), copied
    finally:
        try:
            os.unlink(temporary_name, dir_fd=output_directory)
        except FileNotFoundError:
            pass


def _new_sealed_directory(parent_descriptor: int, runtime_gid: int) -> tuple[str, int]:
    """Create one fresh output directory through its retained parent FD."""

    for _ in range(32):
        name = f".trusted-lighttpd-sealed-{secrets.token_hex(16)}"
        try:
            os.mkdir(name, SEALED_DIRECTORY_MODE, dir_fd=parent_descriptor)
        except FileExistsError:
            continue
        except OSError as error:
            _fail(f"cannot create sealed root: {error}")
        descriptor = _open_directory_component(parent_descriptor, name, "sealed temporary root")
        try:
            _set_required_mode(descriptor, "sealed temporary root", SEALED_DIRECTORY_MODE)
            _set_runtime_group(descriptor, "sealed temporary root", runtime_gid)
            _require_directory_descriptor(
                descriptor,
                "sealed temporary root",
                owner=0,
                group=runtime_gid,
                mode=SEALED_DIRECTORY_MODE,
            )
        except Exception:
            os.close(descriptor)
            try:
                os.rmdir(name, dir_fd=parent_descriptor)
            except OSError:
                pass
            raise
        return name, descriptor
    _fail("cannot allocate a fresh sealed root")


def _output_directory(root_descriptor: int, relative: str, runtime_gid: int) -> tuple[int, str]:
    """Create and return the retained output parent for one fixed role path."""

    components = relative.split("/")
    if len(components) < 2 or any(not component or component in {".", ".."} for component in components):
        _fail("sealed output path must be a fixed relative artifact path")
    directory = os.dup(root_descriptor)
    try:
        for component in components[:-1]:
            try:
                os.mkdir(component, SEALED_DIRECTORY_MODE, dir_fd=directory)
            except FileExistsError:
                pass
            except OSError as error:
                _fail(f"cannot create sealed output directory {component}: {error}")
            child = _open_directory_component(directory, component, f"sealed output directory {component}")
            os.close(directory)
            directory = child
            _set_required_mode(directory, f"sealed output directory {component}", SEALED_DIRECTORY_MODE)
            _set_runtime_group(directory, f"sealed output directory {component}", runtime_gid)
            _require_directory_descriptor(
                directory,
                f"sealed output directory {component}",
                owner=0,
                group=runtime_gid,
                mode=SEALED_DIRECTORY_MODE,
            )
        return directory, components[-1]
    except Exception:
        os.close(directory)
        raise


def _library_artifacts(directory_descriptor: int, prefix: str, runtime_gid: int) -> list[_SourceArtifact]:
    """Open every regular library from its retained parent directory."""

    artifacts: list[_SourceArtifact] = []
    try:
        for name in sorted(_directory_names(directory_descriptor, f"candidate {prefix} directory")):
            details = _entry_details(directory_descriptor, name, f"{prefix}/{name}")
            relative = f"{prefix}/{name}"
            if stat.S_ISLNK(details.st_mode):
                _fail(f"candidate library tree contains a symbolic link: {relative}")
            if stat.S_ISDIR(details.st_mode):
                child = _open_directory_component(directory_descriptor, name, relative, expected=details)
                try:
                    _require_directory_descriptor(child, relative)
                    artifacts.extend(_library_artifacts(child, relative, runtime_gid))
                finally:
                    os.close(child)
                continue
            if not stat.S_ISREG(details.st_mode):
                _fail(f"{relative} must be a regular file")
            descriptor, before = _open_regular_file(directory_descriptor, name, relative, expected=details)
            artifacts.append(
                _SourceArtifact(relative, descriptor, before, SEALED_READONLY_FILE_MODE, runtime_gid)
            )
        return artifacts
    except Exception:
        for artifact in artifacts:
            os.close(artifact.descriptor)
        raise


def _candidate_files(candidate_descriptor: int, runtime_gid: int) -> list[_SourceArtifact]:
    """Open and retain the fixed artifact set from one candidate root inode."""

    _require_directory_descriptor(candidate_descriptor, CANDIDATE_ROOT_LABEL)
    allowed_top = {"bin", "modules", "lib"}
    top = _directory_names(candidate_descriptor, CANDIDATE_ROOT_LABEL)
    if top != allowed_top:
        _fail("candidate contains an unlisted top-level entry")
    directories: dict[str, int] = {}
    artifacts: list[_SourceArtifact] = []
    try:
        for directory in sorted(allowed_top):
            expected = _entry_details(candidate_descriptor, directory, f"candidate {directory} directory")
            descriptor = _open_directory_component(
                candidate_descriptor,
                directory,
                f"candidate {directory} directory",
                expected=expected,
            )
            _require_directory_descriptor(descriptor, f"candidate {directory} directory")
            directories[directory] = descriptor
        for directory, expected in (("bin", {"lighttpd"}), ("modules", {"mod_msconnector.so", "mod_proxy.so"})):
            if _directory_names(directories[directory], f"candidate {directory} directory") != expected:
                _fail(f"candidate {directory} directory contains an unlisted entry")
        for descriptor, name, relative, mode in (
            (directories["bin"], "lighttpd", "bin/lighttpd", SEALED_EXECUTABLE_FILE_MODE),
            (
                directories["modules"],
                "mod_msconnector.so",
                "modules/mod_msconnector.so",
                SEALED_READONLY_FILE_MODE,
            ),
            (directories["modules"], "mod_proxy.so", "modules/mod_proxy.so", SEALED_READONLY_FILE_MODE),
        ):
            expected = _entry_details(descriptor, name, relative)
            file_descriptor, details = _open_regular_file(descriptor, name, relative, expected=expected)
            artifacts.append(_SourceArtifact(relative, file_descriptor, details, mode, runtime_gid))
        artifacts.extend(_library_artifacts(directories["lib"], "lib", runtime_gid))
        if len(artifacts) == 3:
            _fail("candidate lib directory must contain at least one file")
        return artifacts
    except Exception:
        for artifact in artifacts:
            os.close(artifact.descriptor)
        raise
    finally:
        for descriptor in directories.values():
            os.close(descriptor)


def _validate_provenance(provenance: Mapping[str, str] | None) -> dict[str, str]:
    if provenance is None:
        return {}
    if set(provenance) - _PROVENANCE_KEYS:
        _fail("provenance contains an unlisted key")
    result: dict[str, str] = {}
    for key in sorted(provenance):
        value = provenance[key]
        if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
            _fail(f"provenance {key} must be a lowercase SHA-256")
        result[key] = value
    return result


def _runtime_group(value: object) -> int:
    """Require the non-root group that will consume sealed runtime artifacts."""

    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("runtime GID must be a non-root integer")
    return value


def seal_candidate(
    candidate_root: Path | str,
    sealed_root: Path | str,
    *,
    runtime_gid: int,
    provenance: Mapping[str, str] | None = None,
) -> Path:
    """Create a fresh root-owned sealed tree and return its generated manifest."""

    if os.geteuid() != 0:
        _fail("artifact sealing requires a root-owned protected job")
    runtime_group = _runtime_group(runtime_gid)
    candidate = _absolute(candidate_root, CANDIDATE_ROOT_LABEL)
    destination = _absolute(sealed_root, "sealed root")
    if candidate == destination:
        _fail("candidate and sealed roots must be different")
    parent = destination.parent
    candidate_descriptor = _open_absolute_directory(candidate, CANDIDATE_ROOT_LABEL)
    parent_descriptor = _open_absolute_directory(parent, "sealed root parent")
    temporary_name = ""
    temporary_descriptor = -1
    entries: list[_SourceArtifact] = []
    try:
        _require_directory_descriptor(candidate_descriptor, CANDIDATE_ROOT_LABEL)
        _require_directory_descriptor(parent_descriptor, "sealed root parent", owner=0)
        try:
            os.stat(destination.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            _fail("sealed root must be fresh")
        temporary_name, temporary_descriptor = _new_sealed_directory(parent_descriptor, runtime_group)
        records: list[dict[str, object]] = []
        total = 0
        entries = _candidate_files(candidate_descriptor, runtime_group)
        for source in entries:
            output_directory, output_name = _output_directory(
                temporary_descriptor,
                source.relative,
                runtime_group,
            )
            try:
                digest, size = _copy_stable(source, output_directory, output_name)
            finally:
                os.close(output_directory)
            total += size
            if total > MAX_TOTAL_BYTES:
                _fail("candidate exceeds the total size limit")
            records.append({"path": source.relative, "sha256": digest, "size": size, "mode": source.mode})
        manifest = {
            "schema_version": 1,
            "artifact_layout": "lighttpd-fixed-v1",
            "runtime_gid": runtime_group,
            "provenance": _validate_provenance(provenance),
            "artifacts": records,
        }
        encoded = json.dumps(manifest, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
        descriptor = os.open(
            MANIFEST_NAME,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=temporary_descriptor,
        )
        try:
            view = memoryview(encoded.encode("utf-8"))
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    _fail("short write while creating the artifact manifest")
                view = view[written:]
            os.fchmod(descriptor, 0o400)
            os.fchown(descriptor, 0, 0)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.replace(
            temporary_name,
            destination.name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        return destination / MANIFEST_NAME
    except Exception:
        if temporary_name:
            shutil.rmtree(temporary_name, dir_fd=parent_descriptor, ignore_errors=True)
        raise
    finally:
        for source in entries:
            os.close(source.descriptor)
        if temporary_descriptor >= 0:
            os.close(temporary_descriptor)
        os.close(parent_descriptor)
        os.close(candidate_descriptor)


__all__ = ["MANIFEST_NAME", "MAX_FILE_BYTES", "MAX_TOTAL_BYTES", "SealerError", "seal_candidate"]
