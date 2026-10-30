#!/usr/bin/env python3
"""Authenticate the small Parent-to-Framework bridge under the exact-Base gate."""
import hashlib
import os
from pathlib import Path
import stat
import sys

BRIDGE_SHA256 = "60a3cddae2218ca3031240bfe6d3400ce9de39a94c609b53bf238f05e5bc4978"
TOOL = "exact-launcher"


def value(option):
    positions = [i for i, item in enumerate(sys.argv) if item == option]
    if len(positions) != 1 or positions[0] + 1 >= len(sys.argv):
        raise ValueError("protected Framework bridge requires exactly one " + option)
    return sys.argv[positions[0] + 1]


def main():
    root = Path(value("--base-repo-root"))
    revision = value("--trusted-dispatcher-base-sha")
    if not root.is_absolute() or ".." in root.parts:
        raise ValueError("protected base path must be absolute without traversal")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in (*root.parts[1:], "ci"):
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
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
    forwarded = sys.argv[1:]
    if TOOL == "exact-collector":
        for option in ("--base-repo-root", "--trusted-dispatcher-base-sha"):
            index = forwarded.index(option)
            del forwarded[index:index + 2]
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
