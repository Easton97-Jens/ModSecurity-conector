#!/usr/bin/env python3
"""Authenticate the small Parent-to-Framework bridge under the exact-Base gate."""
import hashlib
import os
from pathlib import Path
import stat
import sys

BRIDGE_SHA256 = "1ef4d6fb021605f52c63fef3bf522a325736ceb40457d48c94c091b1e3efc5eb"
TOOL = "exact-collector"


def collector_arguments():
    """Consume each source-binding option once, preserving the collector payload."""
    arguments = sys.argv[1:]
    bindings = {}
    consumed = set()
    for option in ("--base-repo-root", "--trusted-dispatcher-base-sha"):
        positions = [i for i, item in enumerate(arguments) if item == option]
        if len(positions) != 1 or positions[0] + 1 >= len(arguments):
            raise ValueError("protected Framework bridge requires exactly one " + option)
        index = positions[0]
        bindings[option] = arguments[index + 1]
        consumed.update((index, index + 1))
    return (Path(bindings["--base-repo-root"]), bindings["--trusted-dispatcher-base-sha"],
            [value for index, value in enumerate(arguments) if index not in consumed])


def main():
    root, revision, forwarded = collector_arguments()
    if not root.is_absolute() or ".." in root.parts:
        raise ValueError("protected base path must be absolute without traversal")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in (*root.parts[1:], "ci"):
            name = os.path.basename(component)
            if name in {"", ".", ".."} or name != component:
                raise ValueError("protected base components must be exact directory names")
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        source = os.open("run-trusted-framework.py", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(source, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size < 65536:
                raise ValueError("protected bridge source is not a bounded regular file")
            data = stream.read(65536)
        if hashlib.sha256(data).hexdigest() != BRIDGE_SHA256:
            raise ValueError("protected bridge does not match the trusted Parent source digest")
    finally:
        os.close(fd)
    namespace = {"__name__": "_authenticated_framework_bridge"}
    exec(compile(data, str(root / "ci/run-trusted-framework.py"), "exec"), namespace)
    return namespace["main"](["--tool", TOOL, "--connector-root", str(root),
                              "--connector-revision", revision, "--", *forwarded])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print("protected Framework bridge: " + str(error), file=sys.stderr)
        raise SystemExit(77)
