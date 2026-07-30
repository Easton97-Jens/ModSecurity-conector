#!/usr/bin/env python3
"""Generate connector-neutral block-status configuration sources."""

from __future__ import annotations

import argparse
import os
import secrets
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
PREPROCESSOR_ENDIF = "#endif"


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
        PREPROCESSOR_ENDIF,
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
            PREPROCESSOR_ENDIF,
            "",
            PREPROCESSOR_ENDIF,
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


GENERATED_FILES = (
    ("msconnector_block_statuses.generated.h", generated_header),
    ("msconnector_block_statuses.generated.c", generated_c),
)


def resolve_output_dir(out_dir: Path) -> tuple[Path, Path]:
    """Resolve a caller-selected output directory beneath the current directory."""
    if out_dir.is_absolute():
        raise ValueError("--out-dir must be a relative path beneath the current working directory")
    if ".." in out_dir.parts:
        raise ValueError("--out-dir must stay beneath the current working directory")

    try:
        output_root = Path.cwd().resolve(strict=True)
        resolved_out_dir = (output_root / out_dir).resolve(strict=False)
        resolved_out_dir.relative_to(output_root)
    except (OSError, ValueError) as exc:
        raise ValueError("--out-dir must stay beneath the current working directory") from exc
    return output_root, resolved_out_dir


def directory_open_flags() -> int:
    """Return the platform flags required to anchor writes below an opened directory."""
    required_flags = ("O_DIRECTORY", "O_NOFOLLOW")
    missing_flags = [name for name in required_flags if not hasattr(os, name)]
    if os.open not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd or missing_flags:
        raise ValueError("secure --out-dir handling is unavailable on this platform")
    return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)


def open_output_dir(output_root: Path, resolved_out_dir: Path) -> int:
    """Create and open the output directory without following path-component symlinks."""
    flags = directory_open_flags()
    current_fd = -1
    try:
        relative_out_dir = resolved_out_dir.relative_to(output_root)
        current_fd = os.open(output_root, flags)
        for component in relative_out_dir.parts:
            try:
                os.mkdir(component, mode=0o777, dir_fd=current_fd)
            except FileExistsError:
                pass
            next_fd = os.open(component, flags, dir_fd=current_fd)
            os.close(current_fd)
            current_fd = next_fd
        output_fd = current_fd
        current_fd = -1
        return output_fd
    except (OSError, ValueError) as exc:
        raise ValueError("--out-dir cannot be securely accessed beneath the current working directory") from exc
    finally:
        if current_fd != -1:
            os.close(current_fd)


def write_generated_file(output_fd: int, filename: str, content: str) -> None:
    """Atomically replace one generated file without following a final-component symlink."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    temporary_name = ""
    temporary_fd = -1
    try:
        for _ in range(16):
            temporary_name = f".{filename}.{secrets.token_hex(16)}.tmp"
            try:
                temporary_fd = os.open(temporary_name, flags, 0o666, dir_fd=output_fd)
                break
            except FileExistsError:
                continue
        else:
            raise ValueError(f"could not create a unique temporary output for {filename}")

        encoded_content = content.encode("utf-8")
        while encoded_content:
            written = os.write(temporary_fd, encoded_content)
            if written == 0:
                raise OSError("writing generated output returned zero bytes")
            encoded_content = encoded_content[written:]
        os.close(temporary_fd)
        temporary_fd = -1
        os.replace(temporary_name, filename, src_dir_fd=output_fd, dst_dir_fd=output_fd)
    except (NotImplementedError, OSError) as exc:
        raise ValueError(f"failed to write generated output safely: {filename}") from exc
    finally:
        if temporary_fd != -1:
            os.close(temporary_fd)
        if temporary_name:
            try:
                os.unlink(temporary_name, dir_fd=output_fd)
            except FileNotFoundError:
                pass
            except OSError:
                pass


def generate(connector: str, statuses: list[int], out_dir: Path) -> None:
    if connector not in SUPPORTED_CONNECTORS:
        supported = ", ".join(SUPPORTED_CONNECTORS)
        raise ValueError(f"unsupported connector: {connector!r}; expected one of: {supported}")

    output_root, resolved_out_dir = resolve_output_dir(out_dir)
    output_fd = open_output_dir(output_root, resolved_out_dir)
    try:
        for filename, render in GENERATED_FILES:
            write_generated_file(output_fd, filename, render(statuses))
        if connector == "haproxy":
            write_generated_file(
                output_fd,
                "haproxy-block-status-rules.generated.cfg",
                generated_haproxy_cfg(statuses),
            )
    finally:
        os.close(output_fd)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, help="connector name")
    parser.add_argument("--statuses", required=True, help="comma-separated HTTP statuses")
    parser.add_argument(
        "--out-dir",
        required=True,
        type=Path,
        help="relative output directory beneath the current working directory",
    )
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
