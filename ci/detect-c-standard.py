#!/usr/bin/env python3
"""Detect a compiler flag for a logical C standard profile."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROFILES = {
    "c17": ("-std=c17", "-std=c18"),
    "c23": ("-std=c23", "-std=c2x"),
    "c2y": ("-std=c2y", "-std=gnu2y"),
}
INVALID = {
    "c20": "c20 is not a portable ISO C compiler mode; use c23/c2x for C or c++20 for C++.",
    "c26": "c26 is not the current GCC C mode; use c2y/gnu2y for future C or c++26 for C++.",
}
ALLOWED_STANDARD_FLAGS = frozenset(
    {
        "-std=c17",
        "-std=c18",
        "-std=c23",
        "-std=c2x",
        "-std=c2y",
        "-std=gnu2y",
    }
)
COMPILER_BASENAME_RE = re.compile(r"^(cc|gcc|clang)(-[0-9]+(\.[0-9]+)*)?$")
COMPILER_PROBE_TIMEOUT_SECONDS = 10


class CompilerValidationError(ValueError):
    """Raised when a requested compiler command is not a safe C compiler name."""


def validate_standard_flag(flag: str) -> str:
    """Return a known C standard flag or reject it.

    The script has no raw CLI option for arbitrary compiler flags. This helper
    still validates each internally mapped flag before it reaches subprocess.run.
    """

    if flag not in ALLOWED_STANDARD_FLAGS:
        raise ValueError(f"unsupported C standard flag: {flag!r}")
    return flag


def compiler_basename_is_allowed(path: str) -> bool:
    """Return whether the executable basename is an allow-listed compiler."""

    return COMPILER_BASENAME_RE.fullmatch(Path(path).name) is not None


def resolve_compiler(cc: str) -> str:
    """Resolve and validate the compiler executable.

    This intentionally rejects arbitrary commands. The script only needs a C
    compiler probe, not a general command runner. Plain compiler names are
    resolved through PATH. Absolute paths are accepted only when their basename
    still matches the strict compiler allow-list. Relative paths are rejected to
    avoid path traversal and wrapper ambiguity.
    """

    if cc == "" or cc.strip() != cc:
        raise CompilerValidationError(f"unsafe compiler command {cc!r}")
    if any(character.isspace() for character in cc):
        raise CompilerValidationError(f"unsafe compiler command {cc!r}")

    compiler_path = Path(cc)
    if compiler_path.is_absolute():
        if not compiler_basename_is_allowed(cc):
            raise CompilerValidationError(f"compiler not found or not allowed: {cc!r}")
        if not os.access(cc, os.X_OK):
            raise CompilerValidationError(f"compiler not found or not allowed: {cc!r}")
        return str(compiler_path)

    if compiler_path.parent != Path("."):
        raise CompilerValidationError(f"unsafe compiler command {cc!r}")
    if not compiler_basename_is_allowed(cc):
        raise CompilerValidationError(f"compiler not found or not allowed: {cc!r}")

    resolved = shutil.which(cc)
    if resolved is None or not compiler_basename_is_allowed(resolved):
        raise CompilerValidationError(f"compiler not found or not allowed: {cc!r}")
    return resolved


def compiler_supports(compiler_path: str, flag: str) -> bool:
    validated_flag = validate_standard_flag(flag)
    env = {"PATH": os.environ.get("PATH", ""), "LC_ALL": "C"}

    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "detect.c"
        binary = Path(tmp) / "detect"
        source.write_text("int main(void) { return 0; }\n", encoding="utf-8")
        try:
            result = subprocess.run(
                [compiler_path, validated_flag, str(source), "-o", str(binary)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=COMPILER_PROBE_TIMEOUT_SECONDS,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0


def run_self_test() -> int:
    validate_standard_flag("-std=c17")
    validate_standard_flag("-std=c2x")

    for rejected_flag in ("-std=c20", "-std=c26"):
        try:
            validate_standard_flag(rejected_flag)
        except ValueError:
            pass
        else:
            print(f"self-test failed: accepted {rejected_flag}", file=sys.stderr)
            return 1

    for rejected_compiler in (
        "sh",
        "bash",
        "cc;rm -rf /",
        "cc -bad",
        "/bin/sh",
        "python3",
        "../cc",
        "",
    ):
        try:
            resolve_compiler(rejected_compiler)
        except CompilerValidationError:
            pass
        else:
            print(f"self-test failed: accepted compiler {rejected_compiler!r}", file=sys.stderr)
            return 1

    try:
        resolve_compiler("cc")
    except CompilerValidationError as exc:
        print(f"self-test notice: cc unavailable or not allowed: {exc}", file=sys.stderr)

    print("detect-c-standard self-test: pass")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile")
    parser.add_argument("--cc", default="cc")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.profile is None:
        print("INVALID: --profile is required unless --self-test is used", file=sys.stderr)
        return 2

    profile = args.profile.lower()
    if profile in INVALID:
        print(f"INVALID: {INVALID[profile]}", file=sys.stderr)
        return 2

    flags = PROFILES.get(profile)
    if flags is None:
        print(f"INVALID: unknown C standard profile {args.profile!r}", file=sys.stderr)
        return 2

    try:
        compiler_path = resolve_compiler(args.cc)
    except CompilerValidationError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2

    for flag in flags:
        if compiler_supports(compiler_path, flag):
            print(flag)
            return 0

    print(
        f"SKIPPED: optional {profile} check — compiler does not support {' or '.join(flags)}",
        file=sys.stderr,
    )
    return 77


if __name__ == "__main__":
    raise SystemExit(main())
