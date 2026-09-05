#!/usr/bin/env python3
"""Read a Framework-generated NGINX case environment without shell evaluation.

The ordinary harness keeps compatibility with the Framework's shell fragment.
The GitHub-hosted functional-A root path instead reads each bounded value through
this parser so generated content is never sourced or passed to ``eval`` while
the NGINX master is being exercised as root.
"""

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path


_MAX_ENV_BYTES = 16 * 1024
_MAX_VALUE_BYTES = 4096
_ALLOWED_KEYS = frozenset(
    {
        "CASE_NAME",
        "REQUEST_METHOD",
        "REQUEST_PATH",
        "REQUEST_HAS_BODY",
        "REQUEST_HEADERS_FILE",
        "REQUEST_BODY_FILE",
        "AUDIT_LOG_FILE",
        "AUDIT_LOG_DIR",
        "EXPECT_STATUS",
        "EXPECT_INTERVENTION",
        "EXPECT_RULE_ID",
        "EXPECT_RESPONSE_CONTAINS",
        "EXPECT_TRANSPORT",
        "EXPECT_AUDIT_LOG_REQUIRED",
        "NGINX_PHASE4_MODE",
    }
)
_HEADER = "# Generated from common test case. Do not edit."


class CaseEnvironmentError(ValueError):
    """The generated case fragment is not a complete bounded data record."""


def _reject_control_characters(value: str, *, key: str) -> None:
    if any(character in value for character in ("\x00", "\r", "\n")):
        raise CaseEnvironmentError(f"{key} contains a forbidden control character")
    if len(value.encode("utf-8")) > _MAX_VALUE_BYTES:
        raise CaseEnvironmentError(f"{key} exceeds the bounded value size")


def read_case_environment(path: Path) -> dict[str, str]:
    """Return every expected value from one Framework ``case.env`` fragment.

    Framework writes one shell-quoted word per selected key.  ``shlex`` parses
    precisely that one word as data; callers receive its raw value and never
    ask a shell to re-interpret it.
    """

    try:
        raw = path.read_bytes()
    except OSError as error:
        raise CaseEnvironmentError(f"cannot read case environment: {error}") from error
    if len(raw) > _MAX_ENV_BYTES:
        raise CaseEnvironmentError("case environment exceeds the bounded file size")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CaseEnvironmentError("case environment is not UTF-8") from error

    values: dict[str, str] = {}
    saw_header = False
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line:
            raise CaseEnvironmentError(f"blank line at {line_number} is not permitted")
        if line.startswith("#"):
            if saw_header or line != _HEADER or line_number != 1:
                raise CaseEnvironmentError(f"unexpected comment at {line_number}")
            saw_header = True
            continue
        if "=" not in line:
            raise CaseEnvironmentError(f"missing assignment at {line_number}")
        key, rendered = line.split("=", 1)
        if key not in _ALLOWED_KEYS:
            raise CaseEnvironmentError(f"unexpected key at {line_number}: {key!r}")
        if key in values:
            raise CaseEnvironmentError(f"duplicate key at {line_number}: {key}")
        try:
            tokens = shlex.split(rendered, posix=True, comments=False)
        except ValueError as error:
            raise CaseEnvironmentError(
                f"invalid shell quoting for {key} at {line_number}"
            ) from error
        if len(tokens) != 1:
            raise CaseEnvironmentError(
                f"{key} at {line_number} must contain exactly one quoted value"
            )
        value = tokens[0]
        _reject_control_characters(value, key=key)
        values[key] = value

    if not saw_header:
        raise CaseEnvironmentError("case environment lacks the generated-file header")
    missing = sorted(_ALLOWED_KEYS.difference(values))
    if missing:
        raise CaseEnvironmentError(f"case environment is missing required keys: {', '.join(missing)}")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--key", required=True, choices=sorted(_ALLOWED_KEYS))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        value = read_case_environment(args.env_file)[args.key]
    except CaseEnvironmentError as error:
        print(f"nginx case environment rejected: {error}", file=sys.stderr)
        return 2
    print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
