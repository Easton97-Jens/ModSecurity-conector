#!/usr/bin/env python3
"""Generate connector-neutral block-status configuration sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SUPPORTED_CONNECTORS = ("nginx", "apache", "haproxy", "envoy", "traefik", "lighttpd")

# Keep this list in sync with the global block-status contract implemented by
# common/src/block_statuses.c and exposed through common/include/msconnector/block_statuses.h.
# The generator intentionally does not import or compile C code.
ALLOWED_BLOCK_STATUSES = (
    400,
    401,
    403,
    404,
    405,
    406,
    408,
    409,
    410,
    413,
    415,
    418,
    422,
    425,
    429,
    451,
    500,
    501,
    502,
    503,
    504,
)

GENERATED_WARNING_C = "/* GENERATED FILE: do not edit by hand. */"
GENERATED_WARNING_CFG = "# GENERATED FILE: do not edit by hand."


def parse_statuses(raw_statuses: str) -> list[int]:
    if raw_statuses.strip() == "":
        raise ValueError("--statuses must not be empty")

    parsed: list[int] = []
    seen: set[int] = set()
    for raw_part in raw_statuses.split(","):
        part = raw_part.strip()
        if part == "":
            raise ValueError("--statuses contains an empty status entry")
        try:
            status = int(part, 10)
        except ValueError as exc:
            raise ValueError(f"status must be an integer: {part!r}") from exc
        if status in seen:
            raise ValueError(f"duplicate status is not allowed: {status}")
        seen.add(status)
        if status < 100 or status > 599:
            raise ValueError(f"status is outside the valid HTTP range 100-599: {status}")
        if status not in ALLOWED_BLOCK_STATUSES:
            raise ValueError(f"status is not allowed by the global block-status contract: {status}")
        parsed.append(status)

    if not parsed:
        raise ValueError("--statuses must not be empty")

    # Deterministic output: sort enabled statuses numerically so identical status
    # sets produce byte-for-byte identical files regardless of input ordering.
    return sorted(parsed)


def generated_header(enabled_statuses: list[int]) -> str:
    enabled = set(enabled_statuses)
    lines = [
        GENERATED_WARNING_C,
        "#ifndef MSCONNECTOR_BLOCK_STATUSES_GENERATED_H",
        "#define MSCONNECTOR_BLOCK_STATUSES_GENERATED_H",
        "",
        "#ifdef __cplusplus",
        'extern "C" {',
        "#endif",
        "",
    ]
    for status in ALLOWED_BLOCK_STATUSES:
        value = 1 if status in enabled else 0
        lines.append(f"#define MSCONNECTOR_ENABLE_BLOCK_STATUS_{status} {value}")
    lines.extend(
        [
            "",
            "const int *msconnector_generated_block_statuses(void);",
            "unsigned int msconnector_generated_block_status_count(void);",
            "int msconnector_generated_block_status_is_enabled(int status);",
            "",
            "#ifdef __cplusplus",
            "}",
            "#endif",
            "",
            "#endif",
            "",
        ]
    )
    return "\n".join(lines)


def generated_c(enabled_statuses: list[int]) -> str:
    statuses = ", ".join(str(status) for status in enabled_statuses)
    if not statuses:
        statuses = "0"
    lines = [
        GENERATED_WARNING_C,
        '#include "msconnector_block_statuses.generated.h"',
        "",
        f"static const int msconnector_generated_block_status_values[] = {{{statuses}}};",
        "",
        "const int *msconnector_generated_block_statuses(void) {",
        "    return msconnector_generated_block_status_values;",
        "}",
        "",
        "unsigned int msconnector_generated_block_status_count(void) {",
        "    return (unsigned int)(sizeof(msconnector_generated_block_status_values) / sizeof(msconnector_generated_block_status_values[0]));",
        "}",
        "",
        "int msconnector_generated_block_status_is_enabled(int status) {",
        "    unsigned int index;",
        "    for (index = 0; index < msconnector_generated_block_status_count(); ++index) {",
        "        if (msconnector_generated_block_status_values[index] == status) {",
        "            return 1;",
        "        }",
        "    }",
        "    return 0;",
        "}",
        "",
    ]
    return "\n".join(lines)


def generated_haproxy_cfg(enabled_statuses: list[int]) -> str:
    lines = [GENERATED_WARNING_CFG]
    for status in enabled_statuses:
        lines.append(f"http-request deny status {status} if {{ var(txn.modsec.status) -m int {status} }}")
        lines.append(f"http-response deny status {status} if {{ var(txn.modsec.status) -m int {status} }}")
    lines.append("")
    return "\n".join(lines)


def generate(connector: str, statuses: list[int], out_dir: Path) -> None:
    if connector not in SUPPORTED_CONNECTORS:
        supported = ", ".join(SUPPORTED_CONNECTORS)
        raise ValueError(f"unsupported connector: {connector!r}; expected one of: {supported}")

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "msconnector_block_statuses.generated.h").write_text(generated_header(statuses), encoding="utf-8")
    (out_dir / "msconnector_block_statuses.generated.c").write_text(generated_c(statuses), encoding="utf-8")
    if connector == "haproxy":
        (out_dir / "haproxy-block-status-rules.generated.cfg").write_text(
            generated_haproxy_cfg(statuses),
            encoding="utf-8",
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, help="connector name")
    parser.add_argument("--statuses", required=True, help="comma-separated HTTP statuses")
    parser.add_argument("--out-dir", required=True, type=Path, help="output directory")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        statuses = parse_statuses(args.statuses)
        generate(args.connector, statuses, args.out_dir)
    except ValueError as exc:
        print(f"generate-block-status-config: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
