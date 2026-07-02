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

STD_C17 = "-std=c17"
STD_C18 = "-std=c18"
STD_C23 = "-std=c23"
STD_C2X = "-std=c2x"
STD_C2Y = "-std=c2y"
STD_GNU2Y = "-std=gnu2y"

PROFILE_C17 = "c17"
PROFILE_C23 = "c23"
PROFILE_FUTURE_C = "c2y"

COMPILER_CC = "cc"
COMPILER_GCC = "gcc"
COMPILER_CLANG = "clang"

PROFILES = {
    PROFILE_C17: (STD_C17, STD_C18),
    PROFILE_C23: (STD_C23, STD_C2X),
    PROFILE_FUTURE_C: (STD_C2Y, STD_GNU2Y),
}
INVALID = {
    "c20": "c20 is not a portable ISO C compiler mode; use c23/c2x for C or c++20 for C++.",
    "c26": "c26 is not the current GCC C mode; use c2y/gnu2y for future C or c++26 for C++.",
}
ALLOWED_STANDARD_FLAGS = frozenset(
    {
        STD_C17,
        STD_C18,
        STD_C23,
        STD_C2X,
        STD_C2Y,
        STD_GNU2Y,
    }
)
ALLOWED_COMPILER_IDS = frozenset({COMPILER_CC, COMPILER_GCC, COMPILER_CLANG})
COMPILER_ID_PATTERN = re.compile(r"^(cc|gcc|clang|gcc-\d+(\.\d+)*|clang-\d+(\.\d+)*)$")
COMPILER_PROBE_TIMEOUT_SECONDS = 10


class CompilerValidationError(ValueError):
    """Raised when a requested compiler id is not safe or available."""


def validate_standard_flag(flag: str) -> str:
    """Return a known C standard flag or reject it."""

    if flag not in ALLOWED_STANDARD_FLAGS:
        raise ValueError(f"unsupported C standard flag: {flag!r}")
    return flag


def validate_compiler_id(compiler_id: str) -> str:
    """Return an allow-listed compiler id or reject it.

    The CLI accepts compiler ids only, not executable paths or command strings.
    This keeps the compile probe from becoming a general command runner.
    """

    if not COMPILER_ID_PATTERN.fullmatch(compiler_id):
        raise CompilerValidationError(f"compiler id is not allowed: {compiler_id!r}")
    return compiler_id


def resolve_compiler_id(compiler_id: str) -> str:
    """Resolve an allow-listed compiler id through PATH."""

    validated_id = validate_compiler_id(compiler_id)
    resolved = shutil.which(validated_id)
    if resolved is None:
        raise CompilerValidationError(f"compiler id is not available on PATH: {validated_id!r}")
    return resolved


def compiler_probe_environment() -> dict[str, str]:
    return {"PATH": os.environ.get("PATH", ""), "LC_ALL": "C"}


def compiler_supports(compiler_path: str, flag: str) -> bool:
    validated_flag = validate_standard_flag(flag)

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
                env=compiler_probe_environment(),
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0


def run_self_test() -> int:
    validate_standard_flag(STD_C17)
    validate_standard_flag(STD_C2X)
    validate_compiler_id(COMPILER_GCC)
    validate_compiler_id(COMPILER_CLANG)
    validate_compiler_id("gcc-13")
    validate_compiler_id("clang-18")

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
        "clang -bad",
        "/bin/sh",
        "/usr/bin/clang",
        "python3",
        "../cc",
        "",
    ):
        try:
            validate_compiler_id(rejected_compiler)
        except CompilerValidationError:
            pass
        else:
            print(f"self-test failed: accepted compiler {rejected_compiler!r}", file=sys.stderr)
            return 1

    try:
        resolve_compiler_id(COMPILER_CC)
    except CompilerValidationError as exc:
        print(f"self-test notice: cc unavailable: {exc}", file=sys.stderr)

    print("detect-c-standard self-test: pass")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile")
    parser.add_argument(
        "--compiler",
        default=COMPILER_CC,
        help="Allowed compiler id, not an arbitrary command path.",
    )
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
        compiler_path = resolve_compiler_id(args.compiler)
    except CompilerValidationError as exc:
        print(f"SKIPPED: optional {profile} check — {exc}", file=sys.stderr)
        return 77

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
