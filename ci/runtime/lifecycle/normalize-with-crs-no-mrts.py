#!/usr/bin/env python3
"""Normalize one real Parent CRS/no-MRTS host run.

The connector harnesses are the host evidence producers.  This program only
reads their bounded output, correlates the request identities, and writes the
four compatibility records consumed by the unchanged Framework contract.
The Framework's ``UNATTESTED`` compatibility result is deliberately not used
as the Parent runtime verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any

CONNECTORS = {
    "envoy": ("envoy-ext-proc-service", "ext_proc", "event"),
    "traefik": ("traefik-native-middleware", "native-traefik-middleware", "event"),
    "lighttpd": ("lighttpd-patched-native-module", "patched-native-lighttpd", "audit"),
}
PROFILE = "five-connectors-with-crs-no-mrts"
RULE_FILE = "rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf"
RULE_ID = 942270
SUMMARY_FILE = "runtime-summary.txt"
RESULT_FILE = "result.json"
EVENTS_FILE = "events.jsonl"
COMPLETION_EVENTS_FILE = "completion-events.jsonl"
NO_MRTS_FIELDS = (
    "runner_invoked",
    "case_inventory_loaded",
    "process_started",
    "socket_or_listener_created",
    "artifact_used",
)
CLEANUP_COUNTERS = (
    "processes_remaining",
    "host_processes_remaining",
    "helper_processes_remaining",
    "listeners_remaining",
    "sockets_remaining",
    "pid_files_remaining",
    "runtime_fixtures_remaining",
    "temporary_paths_remaining",
)
MAX_FILE_BYTES = 2 * 1024 * 1024
TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
LIGHTTPD_RESPONSE_TRANSACTION_HEADER = "X-Msconnector-Host-Transaction-Id"
LIGHTTPD_HOST_TRANSACTION = re.compile(r"^lighttpd-[1-9][0-9]{0,18}-[1-9][0-9]{0,18}$")
CURL_TRACE_SEND_HEADER = re.compile(r"^=> Send header, ([0-9]{1,10}) bytes \(0x[0-9a-fA-F]{1,8}\)$")
CURL_TRACE_DATA_ROW = re.compile(r"^([0-9a-fA-F]{1,16}): ?([ -~]{0,256})$")
CURL_TRACE_INFO_LINE = re.compile(r"^== Info: [ -~]{1,256}$")


def file_identity(details: os.stat_result) -> tuple[int, int, int, int]:
    """Return the stable identity and type/size checked across an open."""
    return (
        details.st_dev,
        details.st_ino,
        stat.S_IFMT(details.st_mode),
        details.st_size,
    )


def fail(message: str) -> None:
    raise RuntimeError(message)


def safe_token(value: str, label: str) -> str:
    if not TOKEN.fullmatch(value):
        fail(f"unsafe {label}")
    return value


def root_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or path == Path("/"):
        fail(f"{label} must be an absolute non-root path")
    current = path
    while not current.exists():
        current = current.parent
    for ancestor in (current, *current.parents):
        info = ancestor.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            fail(f"{label} has an unsafe ancestor")
        if info.st_uid != os.geteuid() and stat.S_IMODE(info.st_mode) & (stat.S_IWGRP | stat.S_IWOTH):
            fail(f"{label} has a writable foreign ancestor")
    return path


def contained(path: Path, root: Path, label: str) -> Path:
    candidate = Path(os.path.abspath(path))
    base = Path(os.path.abspath(root))
    if base.is_symlink():
        fail(f"{label} base is a symlink")
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        fail(f"{label} escapes its runtime root")
        raise AssertionError from exc
    current = base
    for part in candidate.relative_to(base).parts:
        current /= part
        if current.is_symlink():
            fail(f"{label} contains a symlink")
    return candidate


def open_trusted_directory(root: Path, label: str) -> int:
    """Open a previously validated, non-symlink directory as the walk root."""
    checked = root_path(str(root), label)
    if Path(os.path.realpath(checked)) != checked:
        fail(f"{label} resolves through a symlink")
    pre_open = checked.lstat()
    if not stat.S_ISDIR(pre_open.st_mode):
        fail(f"{label} is not a directory")
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    directory_fd = os.open(checked, flags)
    details = os.fstat(directory_fd)
    if (
        not stat.S_ISDIR(details.st_mode)
        or (details.st_dev, details.st_ino, stat.S_IFMT(details.st_mode))
        != (pre_open.st_dev, pre_open.st_ino, stat.S_IFMT(pre_open.st_mode))
    ):
        os.close(directory_fd)
        fail(f"{label} changed between validation and open")
    return directory_fd


def open_contained_regular(path: Path, root: Path) -> tuple[int, Path]:
    """Open a regular evidence file by no-follow directory descriptors."""
    candidate = contained(path, root, "runtime evidence")
    base = Path(os.path.abspath(root))
    relative = candidate.relative_to(base)
    if not relative.parts:
        fail("runtime evidence must name a file below its root")
    pre_open = candidate.lstat()
    if not stat.S_ISREG(pre_open.st_mode):
        fail(f"evidence is not a regular file: {candidate}")
    if pre_open.st_size > MAX_FILE_BYTES:
        fail(f"evidence exceeds {MAX_FILE_BYTES} bytes: {candidate}")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        fail("platform cannot open runtime evidence without following symlinks")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | no_follow
    directory_fd = open_trusted_directory(base, "runtime evidence root")
    try:
        for component in relative.parts[:-1]:
            next_fd = os.open(component, directory_flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        file_fd = os.open(relative.parts[-1], os.O_RDONLY | no_follow, dir_fd=directory_fd)
    finally:
        os.close(directory_fd)
    try:
        opened = os.fstat(file_fd)
    except BaseException:
        os.close(file_fd)
        raise
    if file_identity(opened) != file_identity(pre_open):
        os.close(file_fd)
        fail(f"evidence changed between validation and open: {candidate}")
    return file_fd, candidate


def read_bounded(path: Path, root: Path) -> bytes:
    try:
        fd, candidate = open_contained_regular(path, root)
    except FileNotFoundError:
        return b""
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            fail(f"evidence is not a regular file: {candidate}")
        if opened.st_size > MAX_FILE_BYTES:
            fail(f"evidence exceeds {MAX_FILE_BYTES} bytes: {candidate}")
        with os.fdopen(fd, "rb", closefd=False) as handle:
            data = handle.read(MAX_FILE_BYTES + 1)
        final = os.fstat(fd)
        if (final.st_dev, final.st_ino, final.st_size) != (opened.st_dev, opened.st_ino, opened.st_size):
            fail(f"evidence changed while reading: {candidate}")
    finally:
        os.close(fd)
    if len(data) > MAX_FILE_BYTES:
        fail(f"evidence grew beyond bound: {path}")
    return data


def atomic_write(path: Path, data: bytes, root: Path) -> None:
    contained(path, root, "normalized evidence")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        fail(f"refusing to overwrite evidence: {path}")
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
        temporary_path.unlink()
        directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def create_run_directory(path: Path, root: Path) -> None:
    """Reserve a run leaf exactly once; never reuse another run's evidence."""
    contained(path, root, "run evidence directory")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        fail(f"evidence run directory already exists: {path}")
    os.mkdir(path, 0o700)
    fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try: os.fsync(fd)
    finally: os.close(fd)


def digest(path: Path, root: Path) -> str:
    return hashlib.sha256(read_bounded(path, root)).hexdigest()


def jsonl(path: Path, runtime_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in read_bounded(path, runtime_root).decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"malformed host event JSON: {path}")
            raise AssertionError from exc
        if isinstance(value, dict):
            records.append(value)
    return records


def summary_values(path: Path, runtime_root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in read_bounded(path, runtime_root).decode("utf-8", "replace").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", key):
                values[key] = value
    return values


def private_wire_input(path_value: str, runtime_root: Path, label: str) -> tuple[Path, bytes]:
    """Read one harness-owned wire artifact without trusting its path or mode."""
    if not path_value:
        fail(f"Lighttpd {label} path is missing")
    path = contained(Path(path_value), runtime_root, f"Lighttpd {label}")
    parent = path.parent
    parent_details = parent.lstat()
    if not stat.S_ISDIR(parent_details.st_mode) or stat.S_IMODE(parent_details.st_mode) & 0o077:
        fail(f"Lighttpd {label} directory is not private")
    details = path.lstat()
    if not stat.S_ISREG(details.st_mode) or stat.S_IMODE(details.st_mode) & 0o077:
        fail(f"Lighttpd {label} is not a private regular file")
    return path, read_bounded(path, runtime_root)


def curl_send_header(trace_lines: list[str], case: str) -> tuple[int, int]:
    send_headers: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(trace_lines):
        declaration = CURL_TRACE_SEND_HEADER.fullmatch(line)
        if declaration is not None:
            send_headers.append((index, declaration))
    completed_lines = {
        "* Request completely sent off",
        "== Info: Request completely sent off",
    }
    if len(send_headers) != 1 or sum(line in completed_lines for line in trace_lines) != 1:
        fail(f"Lighttpd {case} trace does not contain exactly one request exchange")
    start_index, declaration = send_headers[0]
    return start_index, int(declaration.group(1))


def curl_header_rows(trace_lines: list[str], start_index: int, case: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for line in trace_lines[start_index + 1:]:
        if line in {"* Request completely sent off", "== Info: Request completely sent off"}:
            if rows:
                return rows
            fail(f"Lighttpd {case} trace has no completed outgoing-header block")
        # curl 8.18 can emit informational records with an ``== Info:``
        # prefix while flushing the header (older builds use ``*``).  These
        # records contain no request bytes; every byte row remains subject to
        # the contiguous-offset and declared-length checks below.
        if CURL_TRACE_INFO_LINE.fullmatch(line):
            continue
        row = CURL_TRACE_DATA_ROW.fullmatch(line)
        if row is None:
            fail(f"Lighttpd {case} trace has an unexpected outgoing-header row")
        offset = int(row.group(1), 16)
        fragment = row.group(2)
        if not fragment.isascii() or any(not 0x20 <= ord(character) <= 0x7E for character in fragment):
            fail(f"Lighttpd {case} trace has a non-ASCII outgoing-header fragment")
        rows.append((offset, fragment))
    fail(f"Lighttpd {case} trace has no completed outgoing-header block")


def curl_logical_header_lines(rows: list[tuple[int, str]], declared_length: int, case: str) -> list[str]:

    logical_lines: list[str] = []
    current_line = ""
    expected_offset = 0
    for index, (offset, fragment) in enumerate(rows):
        if offset != expected_offset:
            fail(f"Lighttpd {case} trace has a non-contiguous outgoing-header offset")
        next_offset = rows[index + 1][0] if index + 1 < len(rows) else declared_length
        span = next_offset - offset
        visible_length = len(fragment)
        if span == visible_length:
            current_line += fragment
        elif span == visible_length + 2:
            current_line += fragment
            logical_lines.append(current_line)
            current_line = ""
        else:
            fail(f"Lighttpd {case} trace has an invalid outgoing-header byte span")
        expected_offset = next_offset
    if expected_offset != declared_length or current_line or not logical_lines or logical_lines[-1] != "":
        fail(f"Lighttpd {case} trace has an unterminated outgoing-header block")
    return logical_lines


def lighttpd_request_lines(trace: str, case: str) -> list[str]:
    """Parse curl's real, offset-wrapped outbound HTTP/1.1 header block."""
    trace_lines = trace.splitlines()
    start_index, declared_length = curl_send_header(trace_lines, case)
    rows = curl_header_rows(trace_lines, start_index, case)
    return curl_logical_header_lines(rows, declared_length, case)


def require_single_lighttpd_request_header(lines: list[str], case: str, name: str, value: str) -> None:
    values = []
    for line in lines[1:-1]:
        header_name, separator, header_value = line.partition(":")
        if separator and header_name.lower() == name.lower():
            values.append(header_value.strip())
    if values != [value]:
        fail(f"Lighttpd {case} trace has an invalid {name} request header")


def decode_lighttpd_wire(trace_bytes: bytes, headers_bytes: bytes, case: str) -> tuple[str, str]:
    try:
        return trace_bytes.decode("ascii"), headers_bytes.decode("ascii")
    except UnicodeDecodeError as exc:
        fail(f"Lighttpd {case} wire evidence is not ASCII HTTP/curl output")
        raise AssertionError from exc


def validate_lighttpd_request(
    trace: str, case: str, uri: str, run_id: str, request_id: str
) -> None:
    request_lines = lighttpd_request_lines(trace, case)
    if request_lines[0] != f"GET {uri} HTTP/1.1":
        fail(f"Lighttpd {case} trace has an unexpected request line")
    require_single_lighttpd_request_header(request_lines, case, "Host", "crs-runtime.test")
    require_single_lighttpd_request_header(request_lines, case, "X-Framework-Run-ID", run_id)
    require_single_lighttpd_request_header(request_lines, case, "X-Framework-Request-ID", request_id)
    transaction_headers = {
        "x-modsec-transaction-id",
        "x-msconnector-host-transaction-id",
    }
    if any(line.partition(":")[0].lower() in transaction_headers for line in request_lines[1:-1]):
        fail(f"Lighttpd {case} trace supplied a client transaction id")
    if trace.count("*   Trying 127.0.0.1:") != 1 or trace.count("* Established connection to 127.0.0.1") != 1:
        fail(f"Lighttpd {case} trace does not prove one private loopback connection")


def lighttpd_response_lines(headers: str, case: str) -> list[str]:
    if not headers.endswith("\r\n\r\n") or headers.count("\r\n\r\n") != 1:
        fail(f"Lighttpd {case} response does not contain one complete HTTP header block")
    lines = headers[:-4].split("\r\n")
    if len(lines) < 2 or any(not line or line[:1] in (" ", "\t") for line in lines):
        fail(f"Lighttpd {case} response headers are malformed or folded")
    return lines


def lighttpd_response_status(lines: list[str], case: str, expected_status: int) -> None:
    status_line = lines[0]
    status_prefix = "HTTP/1.1 "
    status_text = status_line[len(status_prefix) :]
    status_code, separator, reason = status_text.partition(" ")
    if (
        not status_line.startswith(status_prefix)
        or len(status_code) != 3
        or not status_code.isdecimal()
        or not separator
        or not reason
        or len(reason) > 64
        or any(not 0x20 <= ord(character) <= 0x7E for character in reason)
        or int(status_code) != expected_status
    ):
        fail(f"Lighttpd {case} response status does not match the observed request status")


def lighttpd_response_header_values(lines: list[str], header_name: str, case: str) -> list[str]:
    values: list[str] = []
    for line in lines[1:]:
        name, separator, value = line.partition(":")
        if not separator or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name):
            fail(f"Lighttpd {case} response header syntax is invalid")
        if name.lower() == header_name.lower():
            values.append(value.strip())
    return values


def lighttpd_response_transaction_id(
    headers: str, case: str, expected_status: int, header_name: str, request_id: str
) -> str:
    lines = lighttpd_response_lines(headers, case)
    lighttpd_response_status(lines, case, expected_status)
    values = lighttpd_response_header_values(lines, header_name, case)
    if len(values) != 1 or not LIGHTTPD_HOST_TRANSACTION.fullmatch(values[0]):
        fail(f"Lighttpd {case} response lacks one safe server-generated transaction id")
    if values[0] == request_id:
        fail(f"Lighttpd {case} response transaction id reused its client request label")
    return values[0]


def lighttpd_wire_transaction(
    *,
    runtime_root: Path,
    case: str,
    trace_value: str,
    headers_value: str,
    request_id: str,
    run_id: str,
    uri: str,
    expected_status: int,
    header_name: str,
) -> tuple[str, Path, Path]:
    """Bind a local request label to Lighttpd's server-generated response ID.

    The client label is evidence-only.  It never becomes a Common Runtime
    transaction ID: the real response header must carry the host-generated
    ID that is later matched against the Common event and raw CRS log.
    """
    if header_name != LIGHTTPD_RESPONSE_TRANSACTION_HEADER:
        fail("Lighttpd response transaction header name is not the fixed server header")
    trace_path, trace_bytes = private_wire_input(trace_value, runtime_root, f"{case} request trace")
    headers_path, headers_bytes = private_wire_input(headers_value, runtime_root, f"{case} response headers")
    if trace_path == headers_path:
        fail(f"Lighttpd {case} request and response wire artifacts are the same file")
    if trace_path.parent != headers_path.parent or trace_path.parent.name != "crs-request-evidence":
        fail(f"Lighttpd {case} wire artifacts do not share the private evidence root")
    trace, headers = decode_lighttpd_wire(trace_bytes, headers_bytes, case)
    validate_lighttpd_request(trace, case, uri, run_id, request_id)
    transaction_id = lighttpd_response_transaction_id(
        headers, case, expected_status, header_name, request_id
    )
    return transaction_id, trace_path, headers_path


def correlated_trigger(log_text: str, transaction_id: str) -> int:
    matches: list[int] = []
    for line in log_text.splitlines():
        if f'[unique_id "{transaction_id}"]' not in line:
            continue
        marker = '[id "'
        start = line.find(marker)
        if start < 0:
            continue
        value_start = start + len(marker)
        value_end = line.find('"', value_start)
        if value_end < 0 or line[value_end : value_end + 2] != '"]':
            continue
        value = line[value_start:value_end]
        if value.isdecimal() and int(value) == RULE_ID:
            matches.append(RULE_ID)
    if len(matches) != 1:
        fail(f"CRS trigger {RULE_ID} is not uniquely correlated to {transaction_id}: {len(matches)} matches")
    return matches[0]


def envoy_deny_event(event: dict[str, Any], transaction_id: str) -> bool:
    return (
        event.get("connector") == "envoy"
        and event.get("integration_mode") == "ext_proc"
        and str(event.get("transaction_id")) == transaction_id
        and event.get("actual_action") == "deny"
        and int(event.get("visible_http_status", 0)) == 403
        and event.get("transport_result") == "http_status"
    )


def envoy_interventions(events: list[dict[str, Any]], transaction_ids: tuple[str, str]) -> dict[str, int]:
    interventions: dict[str, int] = {}
    for transaction_id in transaction_ids:
        matches = [event for event in events if envoy_deny_event(event, transaction_id)]
        if len(matches) != 1:
            fail(f"Envoy Common event lacks correlated 949110 intervention for {transaction_id}")
        try:
            rule_id = int(matches[0]["rule_id"])
        except (KeyError, TypeError, ValueError) as exc:
            fail(f"Envoy intervention rule is malformed for {transaction_id}")
            raise AssertionError from exc
        if rule_id != 949110:
            fail(f"Envoy intervention rule is not 949110 for {transaction_id}")
        interventions[transaction_id] = rule_id
    return interventions


def envoy_allow_completion(event: dict[str, Any], request_id: str) -> bool:
    return (
        event.get("event") == "ext_proc_stream_complete"
        and event.get("integration_mode") == "ext_proc"
        and str(event.get("transaction_id")) == request_id
        and event.get("evaluation_mode") == "common_libmodsecurity_nonpromoted"
        and event.get("rule_evaluation") == "libmodsecurity"
        and event.get("late_action") == "none"
        and event.get("close_reason") == "response_end_of_stream"
        and int(event.get("response_body_bytes", 0)) > 0
    )


def require_traefik_matching_event(
    events: list[dict[str, Any]], case: dict[str, Any], transaction_id: str
) -> None:
    observed_event = case.get("observed_event")
    if not isinstance(observed_event, dict):
        fail("Traefik result case lacks observed_event")
    matches = [
        event
        for event in events
        if event == observed_event
        and event.get("connector") == "traefik"
        and event.get("integration_mode") == "native-traefik-middleware"
        and str(event.get("transaction_id")) == transaction_id
        and event.get("actual_action") == "deny"
        and int(event.get("visible_http_status", 0)) == 403
        and event.get("transport_result") == "http_status"
        and str(event.get("rule_id")) == "949110"
    ]
    if len(matches) != 1:
        fail(f"Traefik result event is not uniquely correlated for {transaction_id}")


def observed_traefik(runtime_root: Path, run_id: str) -> dict[str, Any]:
    result = json.loads(read_bounded(runtime_root / RESULT_FILE, runtime_root).decode())
    if result.get("status") != "PASS" or result.get("connector") != "traefik" or result.get("integration_mode") != "native-traefik-middleware" or result.get("run_id") != run_id:
        fail("Traefik completion identity is not a PASS native run")
    block = result.get("block")
    bypass = result.get("bypass")
    allow = result.get("allow")
    if not isinstance(block, dict) or not isinstance(bypass, dict) or not isinstance(allow, dict):
        fail("Traefik result lacks observed allow/block/bypass records")
    if (int(allow.get("status", 0)), int(block.get("status", 0)), int(bypass.get("status", 0))) != (200, 403, 403):
        fail("Traefik result statuses are not 200/403/403")
    block_id = str(block.get("request_id", ""))
    bypass_id = str(bypass.get("request_id", ""))
    if not block_id or not bypass_id or block_id == bypass_id:
        fail("Traefik result lacks distinct transaction identities")
    engine_text = read_bounded(runtime_root / "logs" / "engine.stderr.log", runtime_root).decode("utf-8", "replace")
    block_trigger = correlated_trigger(engine_text, block_id)
    correlated_trigger(engine_text, bypass_id)
    try:
        actual_intervention = int(block.get("intervention_rule_id", block.get("observed_rule_id")))
    except (TypeError, ValueError) as exc:
        fail("Traefik intervention rule is malformed")
        raise AssertionError from exc
    if actual_intervention != 949110:
        fail("Traefik block does not retain the actual 949110 intervention")
    events = jsonl(runtime_root / "logs" / EVENTS_FILE, runtime_root)
    require_traefik_matching_event(events, block, block_id)
    require_traefik_matching_event(events, bypass, bypass_id)
    return {"allow": allow, "block": block, "bypass": bypass, "actual_intervention": actual_intervention, "canonical_trigger": block_trigger, "request_id": block_id, "transaction_id": block_id}


def observed_envoy(runtime_root: Path, run_id: str) -> dict[str, Any]:
    """Validate Envoy's probes, final host action, and ext-proc completion."""
    summary = summary_values(runtime_root / SUMMARY_FILE, runtime_root)
    if (
        summary.get("status") != "PASS"
        or summary.get("connector") != "envoy"
        or summary.get("integration_mode") != "ext_proc"
        or summary.get("run_id") != run_id
    ):
        fail("Envoy completion identity is not a PASS ext_proc run")
    block_value = json.loads(read_bounded(runtime_root / "crs-block-probe.json", runtime_root).decode())
    bypass_value = json.loads(read_bounded(runtime_root / "crs-bypass-probe.json", runtime_root).decode())
    allow_value = json.loads(read_bounded(runtime_root / "crs-allow-probe.json", runtime_root).decode())
    if (
        int(block_value.get("http_status", 0)) != 403
        or int(bypass_value.get("http_status", 0)) != 403
        or int(allow_value.get("http_status", 0)) != 200
    ):
        fail("Envoy probe statuses are not 200/403/403")
    block_id = summary.get("block_request_id", "")
    bypass_id = summary.get("bypass_request_id", "")
    allow_id = summary.get("allow_request_id", "")
    service_text = read_bounded(runtime_root / "ext-proc.stderr.log", runtime_root).decode("utf-8", "replace")
    block_trigger = correlated_trigger(service_text, block_id)
    if not block_trigger:
        fail("Envoy raw ModSecurity evidence is not correlated to the block request")
    bypass_trigger = correlated_trigger(service_text, bypass_id)
    if not bypass_trigger:
        fail("Envoy raw ModSecurity evidence is not correlated to the bypass request")
    if block_id == bypass_id:
        fail("Envoy block and bypass reused a transaction id")
    interventions = envoy_interventions(jsonl(runtime_root / EVENTS_FILE, runtime_root), (block_id, bypass_id))
    if not allow_id:
        fail("Envoy summary lacks allow transaction identity")
    completion_events = jsonl(runtime_root / COMPLETION_EVENTS_FILE, runtime_root)
    if len([event for event in completion_events if envoy_allow_completion(event, allow_id)]) != 1:
        fail("Envoy allow request lacks one correlated ext_proc completion event")
    for value, request_id in (
        (allow_value, allow_id),
        (block_value, block_id),
        (bypass_value, bypass_id),
    ):
        value["request_id"] = request_id
        value["transaction_id"] = request_id
    return {
        "allow": allow_value,
        "block": block_value,
        "bypass": bypass_value,
        "actual_intervention": interventions[block_id],
        "canonical_trigger": block_trigger,
        "request_id": block_id,
        "transaction_id": block_id,
    }


def lighttpd_summary_correlation(summary: dict[str, str], run_id: str) -> tuple[dict[str, str], dict[str, str]]:
    if (
        summary.get("status") != "PASS"
        or summary.get("connector") != "lighttpd"
        or summary.get("integration_mode") != "patched-native-lighttpd"
        or summary.get("run_id") != run_id
    ):
        fail("Lighttpd completion identity is not a PASS patched-native run")
    if summary.get("response_transaction_header_name") != LIGHTTPD_RESPONSE_TRANSACTION_HEADER:
        fail("Lighttpd summary does not identify the fixed response transaction header")
    if summary.get("response_transaction_header_origin") != "server_generated_lighttpd_host":
        fail("Lighttpd summary does not identify a server-generated response transaction header")
    request_ids = {case: summary.get(f"{case}_request_id", "") for case in ("allow", "block", "bypass")}
    uris = {case: summary.get(f"{case}_request_uri", "") for case in ("allow", "block", "bypass")}
    if not all((*request_ids.values(), *uris.values())):
        fail("Lighttpd summary lacks a complete request correlation tuple")
    for case, request_id in request_ids.items():
        safe_token(request_id, f"Lighttpd {case} request id")
    if len(set(request_ids.values())) != len(request_ids):
        fail("Lighttpd requests reused a client correlation label")
    return request_ids, uris


def lighttpd_wire_for(
    runtime_root: Path,
    summary: dict[str, str],
    run_id: str,
    case: str,
    request_id: str,
    uri: str,
    expected_status: int,
) -> tuple[str, Path, Path]:
    response_transaction_id, trace_path, headers_path = lighttpd_wire_transaction(
        runtime_root=runtime_root,
        case=case,
        trace_value=summary.get(f"{case}_request_trace", ""),
        headers_value=summary.get(f"{case}_response_headers", ""),
        request_id=request_id,
        run_id=run_id,
        uri=uri,
        expected_status=expected_status,
        header_name=summary.get("response_transaction_header_name", ""),
    )
    if summary.get(f"{case}_response_transaction_id", "") != response_transaction_id:
        fail(f"Lighttpd {case} summary response transaction id differs from its raw response header")
    if summary.get(f"{case}_transaction_id", "") != response_transaction_id:
        fail(f"Lighttpd {case} Common transaction id differs from its raw response header")
    return response_transaction_id, trace_path, headers_path


def lighttpd_deny_event(event: dict[str, Any], transaction_id: str, uri: str) -> bool:
    return (
        event.get("connector") == "lighttpd"
        and event.get("integration_mode") == "patched-native-lighttpd"
        and str(event.get("transaction_id")) == transaction_id
        and event.get("method") == "GET"
        and event.get("actual_action") == "deny"
        and int(event.get("http_status", 0)) == 403
        and int(event.get("visible_http_status", 0)) == 403
        and event.get("transport_result") == "http_status"
        and str(event.get("uri")) == uri
        and str(event.get("rule_id")) == "949110"
    )


def lighttpd_intervention_event(
    events: list[dict[str, Any]], case: str, transaction_id: str, uri: str
) -> dict[str, Any]:
    matches = [event for event in events if lighttpd_deny_event(event, transaction_id, uri)]
    if len(matches) != 1:
        fail(f"Lighttpd {case} lacks one correlated 949110 intervention for {transaction_id}")
    return matches[0]


def observed_lighttpd(runtime_root: Path, run_id: str) -> dict[str, Any]:
    """Validate Lighttpd's private wire evidence and correlated host events."""
    event_path = runtime_root / EVENTS_FILE
    events = jsonl(event_path, runtime_root)
    summary = summary_values(runtime_root / SUMMARY_FILE, runtime_root)
    request_ids, uris = lighttpd_summary_correlation(summary, run_id)
    allow_id, allow_trace, allow_headers = lighttpd_wire_for(runtime_root, summary, run_id, "allow", request_ids["allow"], uris["allow"], 200)
    block_id, block_trace, block_headers = lighttpd_wire_for(runtime_root, summary, run_id, "block", request_ids["block"], uris["block"], 403)
    bypass_id, bypass_trace, bypass_headers = lighttpd_wire_for(runtime_root, summary, run_id, "bypass", request_ids["bypass"], uris["bypass"], 403)
    wire_artifacts = {
        "allow_request_trace": allow_trace,
        "allow_response_headers": allow_headers,
        "block_request_trace": block_trace,
        "block_response_headers": block_headers,
        "bypass_request_trace": bypass_trace,
        "bypass_response_headers": bypass_headers,
    }
    if len(set(wire_artifacts.values())) != len(wire_artifacts):
        fail("Lighttpd requests reused a raw wire-evidence artifact")
    if len({allow_id, block_id, bypass_id}) != 3:
        fail("Lighttpd requests reused a server-generated host transaction id")
    block = lighttpd_intervention_event(events, "block", block_id, uris["block"])
    bypass = lighttpd_intervention_event(events, "bypass", bypass_id, uris["bypass"])
    if any(
        event.get("connector") == "lighttpd"
        and event.get("integration_mode") == "patched-native-lighttpd"
        and event.get("actual_action") == "deny"
        and str(event.get("uri")) == uris["allow"]
        for event in events
    ):
        fail("Lighttpd allow URI has a correlated deny event")
    allow = {"request_id": request_ids["allow"], "transaction_id": allow_id, "status": 200}
    server_text = read_bounded(runtime_root / "runtime-smoke.stderr", runtime_root).decode("utf-8", "replace")
    block_trigger = correlated_trigger(server_text, block_id)
    correlated_trigger(server_text, bypass_id)
    try: actual_intervention = int(block["rule_id"])
    except (KeyError, TypeError, ValueError): fail("Lighttpd intervention rule is malformed")
    if actual_intervention != 949110: fail("Lighttpd intervention is not 949110")
    return {"allow": allow, "block": block, "bypass": bypass, "actual_intervention": actual_intervention, "canonical_trigger": block_trigger, "request_id": request_ids["block"], "transaction_id": block_id, "bypass_request_id": request_ids["bypass"], "wire_artifacts": wire_artifacts}


def observed_runtime(runtime_root: Path, connector: str, run_id: str) -> dict[str, Any]:
    """Return only facts bound to this connector's fixed attack transaction."""
    if connector == "envoy":
        return observed_envoy(runtime_root, run_id)
    if connector == "traefik":
        return observed_traefik(runtime_root, run_id)
    if connector == "lighttpd":
        return observed_lighttpd(runtime_root, run_id)
    fail(f"unsupported connector runtime evidence: {connector}")
    raise AssertionError


def repository_root(path: Path, label: str) -> Path:
    root = root_path(str(path), f"{label} repository root")
    details = root.lstat()
    if not stat.S_ISDIR(details.st_mode) or stat.S_ISLNK(details.st_mode):
        fail(f"{label} repository root is not a safe directory")
    return root


def commit_identity(root: Path, label: str) -> str:
    repository = repository_root(root, label)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env={"PATH": os.defpath, "LC_ALL": "C"},
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve {label} commit")
        raise AssertionError from exc
    value = result.stdout.strip()
    if not COMMIT.fullmatch(value):
        fail(f"invalid {label} commit")
    return value


def framework_pins(framework_root: Path) -> tuple[str, str, str, str]:
    framework = repository_root(framework_root, "Framework")
    common = contained(framework / "ci/lib/common.sh", framework, "Framework common.sh")
    values: dict[str, str] = {}
    assignment = re.compile(r"^(CRS_APPROVED_REPO_URL|CRS_RELEASE_TAG|CRS_APPROVED_COMMIT|CRS_RULE_FILE_SHA256)=(?:\"([^\"]*)\"|'([^']*)')$")
    for line in read_bounded(common, framework).decode("utf-8", "strict").splitlines():
        match = assignment.fullmatch(line.strip())
        if match:
            values[match.group(1)] = match.group(2) or match.group(3)
    names = ("CRS_APPROVED_REPO_URL", "CRS_RELEASE_TAG", "CRS_APPROVED_COMMIT", "CRS_RULE_FILE_SHA256")
    if set(values) != set(names):
        fail("Framework CRS pin tuple is incomplete or duplicated")
    if not COMMIT.fullmatch(values[names[2]]) or not re.fullmatch(r"[0-9a-f]{64}", values[names[3]]):
        fail("Framework CRS pin tuple is malformed")
    return tuple(values[name] for name in names)  # type: ignore[return-value]


def record_json(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()


def framework_raw_value(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def framework_raw_record(record: dict[str, Any]) -> bytes:
    """Encode Framework's strict, non-normalized key=value evidence format."""
    lines: list[str] = []
    for name, value in record.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", name):
            fail(f"unsafe Framework raw-record key: {name}")
        encoded = framework_raw_value(value)
        if not encoded or "\r" in encoded or "\n" in encoded:
            fail(f"unsafe Framework raw-record value for {name}")
        lines.append(f"{name}={encoded}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def clean_runtime_observation(
    observation: dict[str, Any], connector: str, integration_mode: str
) -> tuple[dict[str, bool], dict[str, Any]]:
    expected_dispatch = {
        "source": "parent-runner",
        "connector": connector,
        "integration_mode": integration_mode,
        "test_variant": "with-crs",
        "mrts_variant": "no-mrts",
    }
    if observation.get("dispatch") != expected_dispatch:
        fail("runner dispatch identity is not the exact Parent with-crs/no-mrts dispatch")
    if connector == "traefik" and observation.get("external_socket_parent_cleanup") != "verified":
        fail("Traefik external socket parent cleanup was not verified")
    no_mrts = observation.get("no_mrts")
    if observation.get("status") != "PASS" or not isinstance(no_mrts, dict):
        fail("runner-written cleanup/no-MRTS observation is not a clean PASS")
    if any(no_mrts.get(name) is not False for name in NO_MRTS_FIELDS):
        fail("runner-written cleanup/no-MRTS observation is not a clean PASS")
    cleanup = observation.get("cleanup")
    if not isinstance(cleanup, dict):
        fail("runner-written cleanup scan is not empty")
    cleanup_scan = dict(cleanup)
    if any(name not in cleanup_scan for name in CLEANUP_COUNTERS):
        fail("runner cleanup scan is missing required counters")
    if any(int(cleanup_scan[name]) != 0 for name in CLEANUP_COUNTERS):
        fail("runner-written cleanup scan is not empty")
    listener_records = cleanup_scan.get("listener_records")
    residue_paths = cleanup_scan.get("paths")
    if not isinstance(listener_records, list) or not isinstance(residue_paths, list):
        fail("runner cleanup diagnostics are missing bounded arrays")
    if len(listener_records) > 1024 or len(residue_paths) > 4096:
        fail("runner cleanup diagnostics exceed bounds")
    if len(listener_records) != int(cleanup_scan["listeners_remaining"]):
        fail("runner listener counter does not match listener diagnostics")
    if residue_paths:
        fail("runner cleanup reports residue paths despite zero counters")
    return {name: no_mrts[name] for name in NO_MRTS_FIELDS}, cleanup_scan


def host_raw_inputs(runtime_root: Path, connector: str, observed: dict[str, Any]) -> dict[str, str]:
    raw_names = {
        "envoy": (SUMMARY_FILE, "crs-allow-probe.json", "crs-block-probe.json", "crs-bypass-probe.json", EVENTS_FILE, COMPLETION_EVENTS_FILE, "ext-proc.stderr.log"),
        "traefik": (RESULT_FILE, "logs/events.jsonl", "logs/engine.stderr.log"),
        "lighttpd": (SUMMARY_FILE, EVENTS_FILE, "runtime-smoke.stderr"),
    }[connector]
    raw_inputs: dict[str, str] = {}
    for name in raw_names:
        raw_path = contained(runtime_root / name, runtime_root, "raw host evidence")
        if not raw_path.is_file():
            fail(f"missing raw host evidence: {name}")
        raw_inputs[name] = digest(raw_path, runtime_root)
    if connector != "lighttpd":
        return raw_inputs
    wire_artifacts = observed.get("wire_artifacts")
    expected_wire_names = {
        "allow_request_trace",
        "allow_response_headers",
        "block_request_trace",
        "block_response_headers",
        "bypass_request_trace",
        "bypass_response_headers",
    }
    if not isinstance(wire_artifacts, dict) or set(wire_artifacts) != expected_wire_names:
        fail("Lighttpd observed runtime lacks the exact wire-evidence inventory")
    for name, raw_path_value in wire_artifacts.items():
        if not isinstance(raw_path_value, Path):
            fail(f"Lighttpd wire artifact is not a verified path: {name}")
        raw_path = contained(raw_path_value, runtime_root, f"Lighttpd {name}")
        if not raw_path.is_file():
            fail(f"Lighttpd wire artifact is absent: {name}")
        raw_inputs[str(raw_path.relative_to(runtime_root))] = digest(raw_path, runtime_root)
    return raw_inputs


def normalize(args: argparse.Namespace) -> Path:
    connector = args.connector
    adapter, mode, evidence_type = CONNECTORS[connector]
    run_id = safe_token(args.run_id, "run id")
    runtime_root = root_path(args.runtime_root, "runtime root")
    evidence_root = root_path(args.evidence_root, "evidence root")
    source_root = root_path(args.source_root, "CRS source root")
    source_checkout = contained(source_root / "coreruleset", source_root, "CRS source")
    crs_repository, crs_release, crs_commit, rule_sha256 = framework_pins(args.framework_root)
    rule_path = contained(source_checkout / RULE_FILE, source_checkout, "CRS rule")
    rule_data = read_bounded(rule_path, source_checkout)
    if hashlib.sha256(rule_data).hexdigest() != rule_sha256:
        fail("canonical CRS rule digest mismatch")
    if b"id:942270" not in rule_data:
        fail("canonical CRS rule fingerprint is absent")
    completion = runtime_root / (SUMMARY_FILE if connector != "traefik" else RESULT_FILE)
    if not completion.is_file():
        fail("host harness completion record is missing")
    observation_path = runtime_root / "runtime-observation.json"
    observation = json.loads(read_bounded(observation_path, runtime_root).decode())
    if not isinstance(observation, dict):
        fail("runner observation is not a JSON object")
    no_mrts, cleanup_scan = clean_runtime_observation(observation, connector, mode)
    parent_commit = commit_identity(args.connector_root, "Parent")
    framework_commit = commit_identity(args.framework_root, "Framework")
    observed = observed_runtime(runtime_root, connector, run_id)
    allow = observed["allow"]
    block = observed["block"]
    bypass = observed["bypass"]
    request_id = str(observed["request_id"])
    transaction_id = str(observed["transaction_id"])
    canonical_trigger = int(observed["canonical_trigger"])
    if canonical_trigger != RULE_ID:
        fail("correlated CRS trigger does not match the Framework contract")
    raw_inputs = host_raw_inputs(runtime_root, connector, observed)
    safe_token(request_id, "block request id")
    safe_token(transaction_id, "block transaction id")
    run_dir = contained(evidence_root / "raw" / connector / run_id, evidence_root, "raw evidence")
    normalized_dir = contained(evidence_root / "normalized" / connector / run_id, evidence_root, "normalized evidence")
    host_file = run_dir / "host-configuration.log"
    allow_file = run_dir / "allow-request.log"
    block_file = run_dir / "block-audit.log"
    cleanup_file = run_dir / "cleanup.log"
    create_run_directory(run_dir, evidence_root)
    create_run_directory(normalized_dir, evidence_root)
    config = {"schema_version": 1, "record_type": "host_configuration", "profile": PROFILE, "connector": connector, "integration_mode": mode, "run_id": run_id, "config_test_status": "passed", "host_start_status": "passed"}
    allow_record = {"schema_version": 1, "record_type": "allow_request", "profile": PROFILE, "connector": connector, "integration_mode": mode, "fixture_id": "crs_sqli_anomaly_block:allow", "run_id": run_id, "request_id": str(allow.get("request_id", allow.get("transaction_id", "allow"))), "transaction_id": str(allow.get("transaction_id", allow.get("request_id", "allow"))), "method": "GET", "path": "/?id=42", "correlation_header": "X-Framework-Run-ID", "correlation_value": run_id, "payload_length": 0, "status": 200}
    block_record = {"schema_version": 1, "record_type": "block_audit", "profile": PROFILE, "connector": connector, "integration_mode": mode, "fixture_id": "crs_sqli_anomaly_block", "run_id": run_id, "request_id": request_id, "transaction_id": transaction_id, "method": "GET", "path": "/?id=1%20UNION%20SELECT%20password%20FROM%20users", "correlation_header": "X-Framework-Run-ID", "correlation_value": run_id, "payload_length": 0, "expected_rule_id": RULE_ID, "observed_rule_id": RULE_ID, "expected_status": 403, "observed_status": 403, "intervention": "deny", "evidence_type": evidence_type}
    block_record["observed_rule_id"] = canonical_trigger
    cleanup_record = {"schema_version": 1, "record_type": "cleanup", "profile": PROFILE, "connector": connector, "run_id": run_id, "status": "passed", "host_processes_remaining": int(cleanup_scan["host_processes_remaining"]), "helper_processes_remaining": int(cleanup_scan["helper_processes_remaining"]), "listeners_remaining": int(cleanup_scan["listeners_remaining"]), "sockets_remaining": int(cleanup_scan["sockets_remaining"]), "pid_files_remaining": int(cleanup_scan["pid_files_remaining"]), "runtime_fixtures_remaining": int(cleanup_scan["runtime_fixtures_remaining"]), "temporary_paths_remaining": int(cleanup_scan["temporary_paths_remaining"]), "mrts_runner_invoked": no_mrts["runner_invoked"], "mrts_case_inventory_loaded": no_mrts["case_inventory_loaded"], "mrts_process_started": no_mrts["process_started"], "mrts_socket_or_listener_created": no_mrts["socket_or_listener_created"], "mrts_artifact_used": no_mrts["artifact_used"]}
    atomic_write(host_file, framework_raw_record(config), evidence_root)
    atomic_write(allow_file, framework_raw_record(allow_record), evidence_root)
    atomic_write(block_file, framework_raw_record(block_record), evidence_root)
    atomic_write(cleanup_file, framework_raw_record(cleanup_record), evidence_root)
    event = {"schema_version": 1, "profile": PROFILE, "connector": connector, "adapter_id": adapter, "integration_mode": mode, "fixture_id": "crs_sqli_anomaly_block", "run_id": run_id, "framework_commit": framework_commit, "connector_commit": parent_commit, "request_id": request_id, "transaction_id": transaction_id, "evidence_type": evidence_type, "evidence_origin": "connector-host", "crs_repository": crs_repository, "crs_release_tag": crs_release, "crs_commit": crs_commit, "crs_rule_file": RULE_FILE, "crs_rule_file_sha256": rule_sha256, "crs_source_kind": "fresh", "crs_git_ref": crs_release, "expected_rule_id": RULE_ID, "observed_rule_id": RULE_ID, "expected_status": 403, "observed_status": 403, "intervention": "deny", "allow_case": {"fixture_id": "crs_sqli_anomaly_block:allow", "run_id": run_id, "request_id": allow_record["request_id"], "transaction_id": allow_record["transaction_id"], "expected_status": 200, "observed_status": 200, "observed_rule_id": None, "evidence_path": f"raw/{connector}/{run_id}/allow-request.log", "evidence_sha256": digest(allow_file, evidence_root)}, "host_configuration": {"config_test_status": "passed", "host_start_status": "passed", "evidence_path": f"raw/{connector}/{run_id}/host-configuration.log", "evidence_sha256": digest(host_file, evidence_root)}, "block_evidence": {"evidence_path": f"raw/{connector}/{run_id}/block-audit.log", "evidence_sha256": digest(block_file, evidence_root)}, "no_mrts": {name: no_mrts[name] for name in ("runner_invoked", "case_inventory_loaded", "process_started", "socket_or_listener_created", "artifact_used")}, "cleanup": {"status": "passed", "host_processes_remaining": 0, "helper_processes_remaining": 0, "listeners_remaining": 0, "sockets_remaining": 0, "pid_files_remaining": 0, "runtime_fixtures_remaining": 0, "temporary_paths_remaining": 0, "evidence_path": f"raw/{connector}/{run_id}/cleanup.log", "evidence_sha256": digest(cleanup_file, evidence_root)}, "status": "PASS", "failure_count": 0, "mismatch_count": 0}
    event["cleanup"].update({key: cleanup_record[key] for key in ("host_processes_remaining", "helper_processes_remaining", "listeners_remaining", "sockets_remaining", "pid_files_remaining", "runtime_fixtures_remaining", "temporary_paths_remaining")})
    event["observed_rule_id"] = canonical_trigger
    event_path = normalized_dir / "event.json"
    atomic_write(event_path, record_json(event), evidence_root)
    parent_record = {
        "schema_version": 1,
        "record_type": "parent_runtime_attestation",
        "connector": connector,
        "run_id": run_id,
        "runtime_status": "PASS",
        "actual_intervention_rule_id": observed["actual_intervention"],
        "canonical_trigger_rule_id": canonical_trigger,
        "block_request_id": request_id,
        "block_transaction_id": transaction_id,
        "bypass_request_id": str(observed.get("bypass_request_id", "")),
        "raw_runtime_root": str(runtime_root),
        "raw_evidence_sha256": {
            "runtime_summary": digest(completion, runtime_root),
            "runtime_observation": digest(observation_path, runtime_root),
            "block_audit": digest(block_file, evidence_root),
        },
        "raw_inputs": raw_inputs,
        "observed_statuses": {
            "allow": int(allow.get("status", allow.get("http_status", allow.get("visible_http_status", allow.get("observed_status", 0))))),
            "block": int(block.get("status", block.get("http_status", block.get("visible_http_status", block.get("observed_status", 0))))),
            "bypass": int(bypass.get("status", bypass.get("http_status", bypass.get("visible_http_status", bypass.get("observed_status", 0))))),
        },
        "no_mrts": {name: no_mrts[name] for name in ("runner_invoked", "case_inventory_loaded", "process_started", "socket_or_listener_created", "artifact_used")},
        "cleanup_scan": cleanup_scan,
    }
    parent_dir = contained(evidence_root / "runtime" / connector / run_id, evidence_root, "Parent runtime evidence")
    create_run_directory(parent_dir, evidence_root)
    atomic_write(parent_dir / "runtime.json", record_json(parent_record), evidence_root)
    return event_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", choices=sorted(CONNECTORS), required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--connector-root", type=Path, required=True)
    parser.add_argument("--framework-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        path = normalize(args)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=os.sys.stderr)
        return 1
    print(json.dumps({"status": "PASS", "runtime_status": "PASS", "framework_compatibility": "UNATTESTED", "event_path": str(path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
