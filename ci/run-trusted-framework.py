#!/usr/bin/env python3
"""Invoke a fixed Framework tool authenticated by an explicit trusted Parent base.

This source-integration entrypoint has no imports from either checkout. Protected
callers authenticate this file as a Parent Git blob before executing it as root.
The target implementation is read from the trusted base's exact Framework
gitlink; candidate-selected Framework revisions and modified files are rejected.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import stat
import subprocess
import sys

GIT = "/usr/bin/git"
GITLINK = "modules/ModSecurity-test-Framework"
MAX_SOURCE_BYTES = 2 * 1024 * 1024
PREFIX = "connector_suite/modsecurity_connector_ci/"
CELLS_SOURCE = PREFIX + "runtime/broker/run_nginx_exact_head_cells.sh"
TOOLS = {
    "connector-context": PREFIX + "tools/connector-context.py",
    "exact-dispatcher": PREFIX + "runtime/broker/protected_nginx_exact_head_dispatcher.py",
    "exact-preflight": PREFIX + "runtime/broker/protected_nginx_exact_head_runner_preflight.py",
    "exact-builder": PREFIX + "runtime/broker/protected_nginx_exact_head_builder.py",
    "exact-launcher": PREFIX + "runtime/broker/nginx_exact_head_root_launcher.py",
    "exact-collector": PREFIX + "runtime/broker/nginx_exact_head_result_collector.py",
    "broker-caller": PREFIX + "runtime/broker/protected_nginx_broker_caller.py",
    "root-broker": PREFIX + "runtime/broker/nginx_root_broker.py",
    "readonly-prepare": PREFIX + "tools/prepare-readonly-submodule-validation-sandbox.py",
    "readonly-namespace": PREFIX + "tools/run-readonly-submodule-validation-namespace.py",
    "python-interpreter": PREFIX + "checks/common/check-python-interpreter-contract.py",
}

# Only owned, sealed descriptors enter the interpreter's command line. Tool
# arguments remain data until the authenticated source receives its own argv.
INVOCATION_LAUNCHER = r'''
import fcntl,json,os,stat,sys
def read_sealed(descriptor):
    metadata = os.fstat(descriptor)
    required = fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
    if (not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.geteuid()
            or not 0 < metadata.st_size <= 2097152
            or fcntl.fcntl(descriptor, fcntl.F_GET_SEALS) & required != required):
        raise ValueError("invocation requires a bounded owned sealed regular descriptor")
    with os.fdopen(descriptor, 'rb') as stream:
        value = stream.read(2097153)
    if len(value) != metadata.st_size:
        raise ValueError("sealed invocation size differs from its descriptor")
    return value
source_fd, invocation_fd = map(int, sys.argv[1:])
source = read_sealed(source_fd)
invocation = json.loads(read_sealed(invocation_fd))
if (type(invocation) is not dict or set(invocation) != {'source_name', 'argv'}
        or type(invocation['source_name']) is not str or not invocation['source_name']
        or '\0' in invocation['source_name'] or type(invocation['argv']) is not list
        or any(type(value) is not str or '\0' in value for value in invocation['argv'])):
    raise ValueError("invocation envelope must contain an exact source name and string arguments")
name = invocation['source_name']
sys.argv = [name, *invocation['argv']]
globals()['__file__'] = name
exec(compile(source, name, 'exec'), globals())
'''


class TrustError(ValueError):
    """The requested invocation is not authenticated by the trusted base."""


def _sha(value: str) -> str:
    if not re.fullmatch(r"[a-f0-9]{40}", value):
        raise TrustError("trusted Connector revision must be an exact SHA-1")
    return value


def _absolute(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts or str(path) != value:
        raise TrustError("trusted Connector root must be a canonical absolute path")
    return path


def read_source(root: Path, relative: str) -> bytes:
    """Read bounded bytes through retained non-symlink descriptors."""
    parts = PurePosixPath(relative).parts
    if not parts or relative.startswith("/") or any(p in {".", ".."} for p in parts):
        raise TrustError("invalid fixed Framework source path")
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in (*root.parts[1:], *parts[:-1]):
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        source = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                         dir_fd=descriptor)
        with os.fdopen(source, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= MAX_SOURCE_BYTES:
                raise TrustError("Framework source must be a bounded regular file")
            data = stream.read(MAX_SOURCE_BYTES + 1)
            if len(data) != metadata.st_size:
                raise TrustError("Framework source changed while reading")
            return data
    finally:
        os.close(descriptor)


def _value(arguments: list[str], option: str) -> str:
    positions = [index for index, value in enumerate(arguments) if value == option]
    if len(positions) != 1 or positions[0] + 1 >= len(arguments):
        raise TrustError(f"protected root invocation requires exactly one {option}")
    return arguments[positions[0] + 1]


def _git(root: Path, *arguments: str, forwarded: list[str], data: bytes | None = None) -> bytes:
    environment = {
        "PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": "/dev/null",
        "GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "",
    }
    privilege_prefix = []
    if os.geteuid() == 0:
        try:
            uid, gid = (int(_value(forwarded, option)) for option in ("--runner-uid", "--runner-gid"))
        except ValueError as error:
            raise TrustError("root source verification requires explicit runner identity") from error
        if uid <= 0 or gid <= 0:
            raise TrustError("Git source verification must run without root")

        privilege_prefix = [
            "/usr/bin/setpriv", f"--reuid={uid}", f"--regid={gid}", "--clear-groups",
            "--no-new-privs", "--inh-caps=-all", "--ambient-caps=-all", "--bounding-set=-all", "--",
        ]

    def limit_output() -> None:
        _soft, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
        limit = MAX_SOURCE_BYTES + 1 if hard == resource.RLIM_INFINITY else min(hard, MAX_SOURCE_BYTES + 1)
        resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

    descriptor = os.memfd_create("trusted-git-output", os.MFD_CLOEXEC)
    try:
        input_options = {"stdin": subprocess.DEVNULL} if data is None else {"input": data}
        subprocess.run(
            [*privilege_prefix, GIT, "-c", "core.hooksPath=/nonexistent", "-c", "core.fsmonitor=false",
             "-c", "diff.external=false", "-C", str(root), *arguments],
            check=True, env=environment, **input_options,
            stdout=descriptor, stderr=subprocess.DEVNULL, timeout=15, preexec_fn=limit_output,
        )
        os.lseek(descriptor, 0, os.SEEK_SET)
        with os.fdopen(os.dup(descriptor), "rb") as source:
            data = source.read(MAX_SOURCE_BYTES + 1)
        if len(data) > MAX_SOURCE_BYTES:
            raise TrustError("trusted Git object output exceeds its bounded size")
        return data
    finally:
        os.close(descriptor)


def verified_object(root: Path, kind: str, oid: str, forwarded: list[str]) -> bytes:
    """Rehash raw Git bytes; object-store filenames and plumbing are not proof."""
    oid = _sha(oid)
    if kind not in {"commit", "tree", "blob"}:
        raise TrustError("only fixed Git object types may be authenticated")
    data = _git(root, "cat-file", kind, oid, forwarded=forwarded)
    # Git owns its object format and native object-identity implementation.
    # Rehash raw bytes without writing an object or consulting worktree filters.
    observed = _git(root, "hash-object", "--no-filters", "-t", kind, "--stdin",
                    forwarded=forwarded, data=data).decode("ascii").strip()
    if observed != oid:
        raise TrustError("trusted Git object bytes do not match their cryptographic identity")
    return data


def tree_entries(data: bytes) -> dict[bytes, tuple[str, str]]:
    entries, position = {}, 0
    while position < len(data):
        space = data.find(b" ", position)
        zero = data.find(b"\0", space + 1)
        if space <= position or zero <= space + 1 or zero + 21 > len(data):
            raise TrustError("malformed authenticated Git tree")
        mode, name = data[position:space], data[space + 1:zero]
        if (mode not in {b"40000", b"100644", b"100755", b"120000", b"160000"} or
                name in {b".", b".."} or b"/" in name or name in entries):
            raise TrustError("noncanonical or duplicate authenticated Git tree entry")
        entries[name] = (mode.decode("ascii"), data[zero + 1:zero + 21].hex())
        position = zero + 21
    return entries


def verified_path(root: Path, commit: str, relative: str, forwarded: list[str], *,
                  gitlink: bool = False) -> str:
    """Authenticate commit→trees→one fixed blob or gitlink without a read race."""
    body = verified_object(root, "commit", commit, forwarded)
    first = body.partition(b"\n")[0]
    match = re.fullmatch(rb"tree ([a-f0-9]{40})", first)
    if not match:
        raise TrustError("authenticated commit has no canonical root tree")
    oid = match[1].decode("ascii")
    components = PurePosixPath(relative).parts
    if not components or relative.startswith("/") or any(p in {".", ".."} for p in components):
        raise TrustError("authenticated source path must be canonical")
    for index, component in enumerate(components):
        entries = tree_entries(verified_object(root, "tree", oid, forwarded))
        entry = entries.get(component.encode("utf-8"))
        if entry is None:
            raise TrustError("trusted Git tree does not contain the fixed source path")
        mode, oid = entry
        allowed = {"160000"} if gitlink else {"100644", "100755"}
        if mode not in (allowed if index == len(components) - 1 else {"40000"}):
            raise TrustError("trusted Git source has the wrong object mode")
    return oid


def authenticated_source(connector: Path, revision: str, relative: str,
                         forwarded: list[str], *, object_only: bool = False) -> tuple[Path, bytes]:
    """Bind both roots and implementation bytes to the protected Parent gitlink."""
    if object_only and relative not in {TOOLS["readonly-prepare"], TOOLS["readonly-namespace"]}:
        raise TrustError("immutable object source is restricted to readonly validation helpers")
    revision = _sha(revision)
    if _git(connector, "rev-parse", "--show-toplevel", "HEAD", forwarded=forwarded).decode().splitlines() != [str(connector), revision]:
        raise TrustError("trusted Connector checkout does not match its explicit revision")
    framework_sha = verified_path(connector, revision, GITLINK, forwarded, gitlink=True)
    framework = connector / GITLINK
    identity = _git(framework, "rev-parse", "--show-toplevel", "HEAD", forwarded=forwarded).decode().splitlines()
    if (len(identity) != 2 or identity[0] != str(framework) or
            (not object_only and identity[1] != framework_sha)):
        raise TrustError("Framework checkout differs from the trusted Parent gitlink")
    blob = verified_path(framework, framework_sha, relative, forwarded)
    expected = verified_object(framework, "blob", blob, forwarded)
    if not 0 < len(expected) <= MAX_SOURCE_BYTES:
        raise TrustError("trusted Framework Git blob has an unsafe size")
    if object_only:
        # The updater deliberately has a candidate checked out here. Its files
        # are never read: only the immutable object selected by trusted Parent
        # is admitted. No other broker tool may opt into this acquisition mode.
        sys.audit("modsecurity.trusted_framework_source", "immutable-object",
                  revision, framework_sha, relative)
        return Path(f"git:{framework_sha}:{relative}"), expected
    actual = read_source(framework, relative)
    if len(expected) > MAX_SOURCE_BYTES or hashlib.sha256(actual).digest() != hashlib.sha256(expected).digest():
        raise TrustError("Framework implementation differs from the exact trusted Git blob")
    return framework / relative, actual


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOLS))
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--connector-revision", required=True)
    parser.add_argument("--source-reader-uid", type=int)
    parser.add_argument("--source-reader-gid", type=int)
    parser.add_argument("--trusted-framework-object", action="store_true")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    if (arguments.source_reader_uid is None) != (arguments.source_reader_gid is None):
        parser.error("--source-reader-uid and --source-reader-gid are required together")
    if arguments.trusted_framework_object and arguments.tool not in {"readonly-prepare", "readonly-namespace"}:
        parser.error("immutable Framework object acquisition is restricted to the readonly validation tools")
    forwarded = arguments.arguments
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]
    if any(value == "--trusted-cells-source-fd" or value.startswith("--trusted-cells-source-fd=") for value in forwarded):
        parser.error("trusted cells source descriptors are supplied only by the authenticated bridge")
    try:
        root = _absolute(arguments.connector_root)
        verification_arguments = forwarded
        if arguments.source_reader_uid is not None:
            if "--runner-uid" in forwarded or "--runner-gid" in forwarded:
                raise TrustError("source reader identity must have one explicit owner")
            verification_arguments = [*forwarded, "--runner-uid", str(arguments.source_reader_uid),
                                      "--runner-gid", str(arguments.source_reader_gid)]
        if arguments.trusted_framework_object:
            path, source = authenticated_source(root, arguments.connector_revision,
                                                TOOLS[arguments.tool], verification_arguments,
                                                object_only=True)
        else:
            path, source = authenticated_source(root, arguments.connector_revision,
                                                TOOLS[arguments.tool], verification_arguments)
        descriptors = []
        try:
            if arguments.tool == "exact-launcher":
                _cells_path, cells = authenticated_source(root, arguments.connector_revision,
                                                           CELLS_SOURCE, verification_arguments)
                cells_descriptor = sealed_source(cells)
                descriptors.append(cells_descriptor)
                forwarded = [*forwarded, "--trusted-cells-source-fd", str(cells_descriptor)]
            descriptor = sealed_source(source)
            descriptors.append(descriptor)
            invocation = json.dumps({"source_name": str(path), "argv": forwarded},
                                    ensure_ascii=True).encode("ascii")
            invocation_descriptor = sealed_source(invocation)
            descriptors.append(invocation_descriptor)
            # A fresh isolated interpreter retains ordinary __main__ semantics;
            # the command itself accepts only descriptors created above.
            return subprocess.run(
                [sys.executable, "-I", "-c", INVOCATION_LAUNCHER,
                 str(descriptor), str(invocation_descriptor)],
                pass_fds=tuple(descriptors), check=False,
            ).returncode
        finally:
            for owned in descriptors:
                os.close(owned)
    except (TrustError, OSError, subprocess.SubprocessError) as error:
        print(f"trusted Framework entrypoint: {error}", file=sys.stderr)
        return 77


def sealed_source(source: bytes) -> int:
    """Return a bounded immutable descriptor owned by this invocation."""
    if not 0 < len(source) <= MAX_SOURCE_BYTES:
        raise TrustError("trusted executable source has an unsafe size")
    descriptor = os.memfd_create("trusted-framework-source", os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
    try:
        with os.fdopen(os.dup(descriptor), "wb") as output:
            output.write(source)
        os.lseek(descriptor, 0, os.SEEK_SET)
        fcntl.fcntl(descriptor, fcntl.F_ADD_SEALS,
                    fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
