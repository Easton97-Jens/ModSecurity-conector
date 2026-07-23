#!/usr/bin/env python3
"""Run local Envoy/Traefik/lighttpd runtime smokes without global dependencies."""

from __future__ import annotations

import argparse
import contextlib
from dataclasses import dataclass
import http.client
import http.server
import json
import os
import re
import shutil
import socket
import stat
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# CI helpers are shared from ci/lib even when this runner is executed directly.
_CI_LIB = Path(__file__).resolve().parents[2] / "ci" / "lib"
if str(_CI_LIB) not in sys.path:
    sys.path.insert(0, str(_CI_LIB))

from runtime_path_utils import is_safe_runtime_root, verified_runtime_paths


BLOCK_VALUES = {"1", "true", "block", "yes", "on"}
REQUEST_BODY_BLOCK_MARKER = "modsec-request-body-block"
REQUEST_BODY_ALLOW_BODY = b"payload=modsec-request-body-allow"
REQUEST_BODY_BLOCK_BODY = b"payload=modsec-request-body-block"
REQUEST_BODY_CONTENT_TYPE = "application/x-www-form-urlencoded"
TARGETED_SMOKE_CASES = {"targeted", "request_body"}
CRS_SETUP_TEMPLATE_NAME = "crs-setup.conf.example"
GENERATED_CRS_SMOKE_RULE_LABEL = "generated CRS smoke rule"
RUNTIME_OUTPUT_PATH_FIELDS = (
    ("evidence_root", "EVIDENCE_ROOT"),
    ("results_dir", "RESULTS_DIR"),
    ("tmp_root", "TMP_ROOT"),
    ("log_root", "LOG_ROOT"),
    ("log_dir", "LOG_DIR"),
    ("config_root", "CONFIG_ROOT"),
)
CRS_SMOKE_CASES = {
    "minimal": {
        "blocked_path": "/?id=1%20UNION%20SELECT%20password%20FROM%20users",
        "description": "existing CRS SQLi anomaly probe",
    },
    "secondary": {
        "blocked_path": "/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E",
        "description": "secondary CRS XSS query probe",
    },
}


class SmokeBlocked(RuntimeError):
    def __init__(self, reason: str, missing_dependencies: list[str]) -> None:
        super().__init__(reason)
        self.reason = reason
        self.missing_dependencies = missing_dependencies


@dataclass(frozen=True)
class RuntimeOutputPaths:
    runtime_root: Path
    evidence_root: Path
    results_dir: Path
    tmp_root: Path
    log_root: Path
    log_dir: Path
    config_root: Path


def require_verified_runtime_output_path(value: str, label: str, root: Path) -> Path:
    """Return one absolute CLI output path constrained to the verified run root."""

    configured = Path(value)
    if not configured.is_absolute():
        raise SmokeBlocked(f"{label} must be absolute: {configured}", ["runtime path"])
    component = Path(configured.anchor)
    for name in configured.parts[1:]:
        component /= name
        try:
            metadata = component.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            raise SmokeBlocked(
                f"{label} cannot inspect path component: {component}", ["runtime path"]
            ) from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise SmokeBlocked(
                f"{label} must not contain a symlink: {component}", ["runtime path"]
            )
    try:
        resolved = configured.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise SmokeBlocked(f"{label} cannot be resolved: {configured}", ["runtime path"]) from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SmokeBlocked(
            f"{label} is outside the verified runtime root: {resolved}", ["runtime path"]
        ) from exc
    return resolved


def validate_runtime_output_paths(args: argparse.Namespace) -> RuntimeOutputPaths:
    """Validate every direct CLI output destination before this runner writes."""

    try:
        verified = verified_runtime_paths(os.environ)
    except ValueError as exc:
        raise SmokeBlocked(f"invalid verified runtime paths: {exc}", ["runtime path"]) from exc
    runtime_root = Path(verified["VERIFIED_RUN_ROOT"]).resolve(strict=False)
    if not is_safe_runtime_root(runtime_root):
        raise SmokeBlocked(f"VERIFIED_RUN_ROOT is unsafe: {runtime_root}", ["runtime path"])

    values: dict[str, Path] = {}
    for field, label in RUNTIME_OUTPUT_PATH_FIELDS:
        configured = namespace_value(args, field)
        if not configured:
            raise SmokeBlocked(f"missing required {label}", ["runtime path"])
        values[field] = require_verified_runtime_output_path(configured, label, runtime_root)
        setattr(args, field, str(values[field]))
    return RuntimeOutputPaths(runtime_root=runtime_root, **values)


def namespace_value(args: argparse.Namespace, name: str, default: str = "") -> str:
    value = getattr(args, name, default)
    return "" if value is None else str(value)


def normalize_ruleset(value: str) -> str:
    normalized = (value or "targeted").strip().lower()
    if normalized in {"", "targeted", "modsecurity-targeted"}:
        return "targeted"
    if normalized in {"crs", "owasp-crs", "coreruleset"}:
        return "crs"
    raise SmokeBlocked(f"unsupported ModSecurity ruleset: {value}", ["modsecurity ruleset"])


def normalize_modsecurity_smoke_case(value: str) -> str:
    normalized = (value or "targeted").strip().lower().replace("-", "_")
    if normalized in TARGETED_SMOKE_CASES:
        return normalized
    raise SmokeBlocked(f"unsupported ModSecurity smoke case: {value}", ["modsecurity smoke case"])


def normalize_crs_smoke_case(value: str) -> str:
    normalized = (value or "minimal").strip().lower()
    if normalized in CRS_SMOKE_CASES:
        return normalized
    raise SmokeBlocked(f"unsupported CRS smoke case: {value}", ["crs smoke case"])


def crs_blocked_path(args: argparse.Namespace) -> str:
    return str(CRS_SMOKE_CASES[args.crs_smoke_case]["blocked_path"])


def is_crs_block_probe(path: str, smoke_case: str) -> bool:
    decoded = urllib.parse.unquote(path).lower()
    if smoke_case == "minimal":
        return "union" in decoded and "select" in decoded
    if smoke_case == "secondary":
        return "<script>" in decoded and "alert(" in decoded
    return False


def crs_probe_uri(headers: http.client.HTTPMessage, path: str) -> str:
    for header_name in ("x-forwarded-uri", "x-envoy-original-path", "x-original-uri"):
        value = headers.get(header_name)
        if value:
            return value
    return path


def crs_version_from_source(source_dir: Path, configured_ref: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_dir), "describe", "--tags", "--always", "--dirty"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if completed.returncode == 0 and completed.stdout.strip():
            return completed.stdout.strip()
    except OSError:
        pass
    changes = source_dir / "CHANGES.md"
    if changes.is_file():
        match = re.search(r"^## Version ([^ \n]+)", changes.read_text(encoding="utf-8", errors="replace"), re.M)
        if match:
            return match.group(1)
    return configured_ref


def bracket_value_text(text: str, key: str) -> str:
    match = re.search(rf'\[{re.escape(key)} "([^"]*)"\]', text)
    return match.group(1) if match else ""


def crs_detection_from_audit_log(audit_log_path: Path, fallback_rule_id: str, fallback_message: str) -> tuple[str, str]:
    if not audit_log_path.is_file():
        return fallback_rule_id, fallback_message
    try:
        text = audit_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return fallback_rule_id, fallback_message
    observed: list[tuple[str, str]] = []
    for line in text.splitlines():
        if "ModSecurity:" not in line:
            continue
        rule_id = bracket_value_text(line, "id")
        message = bracket_value_text(line, "msg")
        if rule_id:
            observed.append((rule_id, message))
    for rule_id, message in observed:
        if not rule_id.startswith("949"):
            return rule_id, message
    if observed:
        return observed[-1]
    return fallback_rule_id, fallback_message


def request_body_smoke_enabled(args: argparse.Namespace) -> bool:
    return (
        args.decision_backend == "libmodsecurity"
        and args.modsecurity_ruleset == "targeted"
        and args.modsecurity_smoke_case == "request_body"
    )


def request_body_headers() -> dict[str, str]:
    return {"Content-Type": REQUEST_BODY_CONTENT_TYPE}


def request_body_evidence(
    decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend,
) -> tuple[bool, bool, bool]:
    return (
        bool(getattr(decision_backend, "request_body_smoke_verified", False)),
        bool(getattr(decision_backend, "request_body_access_enabled", False)),
        bool(getattr(decision_backend, "request_body_rule_loaded", False)),
    )


def crs_source_candidate_roots(args: argparse.Namespace) -> list[Path]:
    """Return only explicitly selected CRS source candidates.

    Shared temporary locations are intentionally not consulted here. A
    direct caller must supply CRS_SOURCE_DIR or a runtime lookup root that the
    caller already selected for its run.
    """

    roots: list[Path] = []

    def add(path: Path) -> None:
        if path.is_absolute() and str(path) not in {str(existing) for existing in roots}:
            roots.append(path)

    if args.crs_source_dir:
        add(Path(args.crs_source_dir))
    for root_text in args.runtime_lookup_root:
        if not root_text:
            continue
        root = Path(root_text)
        add(root / "src/coreruleset")
        add(root / "coreruleset")
        add(root / "sources/coreruleset")
        add(root / "cache-v2/shared/sources/coreruleset")
    return roots


def is_trusted_crs_owner(path_stat: os.stat_result) -> bool:
    """Return whether the runner or root controls a selected CRS path."""

    return path_stat.st_uid in {os.geteuid(), 0}


def crs_directory_entry_is_protected(
    parent_stat: os.stat_result, child_stat: os.stat_result
) -> bool:
    """Return whether an ancestor prevents a different user replacing its child."""

    if not stat.S_ISDIR(parent_stat.st_mode):
        return False
    parent_mode = stat.S_IMODE(parent_stat.st_mode)
    if parent_mode & (stat.S_IWGRP | stat.S_IWOTH) == 0:
        return True
    return (
        bool(parent_mode & stat.S_ISVTX)
        and is_trusted_crs_owner(parent_stat)
        and is_trusted_crs_owner(child_stat)
    )


def assert_crs_path_has_no_symlink_components(path: Path, label: str) -> Path:
    """Return an absolute existing path after rejecting every symlink component."""

    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        try:
            current_stat = current.lstat()
        except OSError as exc:
            raise SmokeBlocked(f"{label} is unavailable: {current}", ["crs"]) from exc
        if stat.S_ISLNK(current_stat.st_mode):
            raise SmokeBlocked(f"{label} must not contain a symlink: {current}", ["crs"])
    return absolute


def assert_crs_path_ancestors_are_safe(path: Path, label: str) -> None:
    """Reject a CRS path replaceable through a different user's writable ancestor."""

    child = path
    while child != child.parent:
        try:
            child_stat = child.lstat()
            parent_stat = child.parent.lstat()
        except OSError as exc:
            raise SmokeBlocked(f"{label} ancestor is unavailable: {child.parent}", ["crs"]) from exc
        if not crs_directory_entry_is_protected(parent_stat, child_stat):
            raise SmokeBlocked(
                f"{label} has an ancestor that permits cross-user replacement: {child.parent}",
                ["crs"],
            )
        child = child.parent


def require_trusted_crs_path(path: Path, label: str, *, directory: bool) -> Path:
    """Require one non-replaceable selected CRS directory or configuration file."""

    if not path.is_absolute():
        raise SmokeBlocked(f"{label} must be absolute: {path}", ["crs"])
    trusted_path = assert_crs_path_has_no_symlink_components(path, label)
    if trusted_path == Path(trusted_path.anchor):
        raise SmokeBlocked(f"{label} is too broad: {trusted_path}", ["crs"])
    try:
        path_stat = trusted_path.lstat()
    except OSError as exc:
        raise SmokeBlocked(f"{label} is unavailable: {trusted_path}", ["crs"]) from exc
    expected_type = stat.S_ISDIR if directory else stat.S_ISREG
    expected_name = "directory" if directory else "regular file"
    if not expected_type(path_stat.st_mode):
        raise SmokeBlocked(f"{label} must be a {expected_name}: {trusted_path}", ["crs"])
    if not is_trusted_crs_owner(path_stat):
        raise SmokeBlocked(f"{label} must be owned by the runner or root: {trusted_path}", ["crs"])
    if stat.S_IMODE(path_stat.st_mode) & (stat.S_IWGRP | stat.S_IWOTH):
        raise SmokeBlocked(f"{label} must not be group or world writable: {trusted_path}", ["crs"])
    assert_crs_path_ancestors_are_safe(trusted_path, label)
    return trusted_path


def require_safe_crs_config_path(path: Path, label: str) -> Path:
    """Reject a filesystem path that would change a quoted ModSecurity directive."""

    value = str(path)
    if any(
        character in value
        for character in ('"', "\\", "\r", "\n", "\0", "*", "?", "[", "]", "{", "}")
    ):
        raise SmokeBlocked(
            f"{label} contains unsupported characters for a ModSecurity directive",
            ["crs"],
        )
    return path


def require_trusted_crs_output_parent(path: Path, label: str) -> Path:
    """Validate an existing directory that may safely receive a runner-owned child."""

    if not path.is_absolute():
        raise SmokeBlocked(f"{label} must be absolute: {path}", ["crs"])
    trusted_path = assert_crs_path_has_no_symlink_components(path, label)
    try:
        path_stat = trusted_path.lstat()
    except OSError as exc:
        raise SmokeBlocked(f"{label} is unavailable: {trusted_path}", ["crs"]) from exc
    if not stat.S_ISDIR(path_stat.st_mode):
        raise SmokeBlocked(f"{label} must be a directory: {trusted_path}", ["crs"])
    if not is_trusted_crs_owner(path_stat):
        raise SmokeBlocked(f"{label} must be owned by the runner or root: {trusted_path}", ["crs"])
    mode = stat.S_IMODE(path_stat.st_mode)
    if mode & (stat.S_IWGRP | stat.S_IWOTH) and not mode & stat.S_ISVTX:
        raise SmokeBlocked(f"{label} must not be group or world writable: {trusted_path}", ["crs"])
    assert_crs_path_ancestors_are_safe(trusted_path, label)
    return trusted_path


def ensure_trusted_crs_output_directory(path: Path, label: str) -> Path:
    """Safely create or validate a private generated-CRS output directory."""

    if not path.is_absolute():
        raise SmokeBlocked(f"{label} must be absolute: {path}", ["crs"])
    absolute = Path(os.path.abspath(path))
    if absolute == Path(absolute.anchor):
        raise SmokeBlocked(f"{label} is too broad: {absolute}", ["crs"])

    missing: list[Path] = []
    current = absolute
    while True:
        try:
            current_stat = current.lstat()
        except FileNotFoundError:
            missing.append(current)
            current = current.parent
            continue
        except OSError as exc:
            raise SmokeBlocked(f"{label} is unavailable: {current}", ["crs"]) from exc
        if stat.S_ISLNK(current_stat.st_mode):
            raise SmokeBlocked(f"{label} must not contain a symlink: {current}", ["crs"])
        break

    if missing:
        require_trusted_crs_output_parent(current, f"{label} parent")
    for missing_directory in reversed(missing):
        try:
            missing_directory.mkdir(mode=0o700)
        except FileExistsError:
            pass
        except OSError as exc:
            raise SmokeBlocked(
                f"could not create {label}: {missing_directory}", ["crs"]
            ) from exc
        require_trusted_crs_path(missing_directory, label, directory=True)
    return require_trusted_crs_path(absolute, label, directory=True)


def secure_crs_output_file(path: Path, label: str) -> int:
    """Open one generated CRS artifact without following a stale symlink."""

    parent = require_trusted_crs_path(path.parent, f"{label} parent", directory=True)
    target = parent / path.name
    if target.exists() or target.is_symlink():
        require_trusted_crs_path(target, label, directory=False)
        try:
            target.unlink()
        except OSError as exc:
            raise SmokeBlocked(f"could not replace {label}: {target}", ["crs"]) from exc
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    if no_follow == 0:
        raise SmokeBlocked("secure CRS output creation requires O_NOFOLLOW", ["crs"])
    try:
        return os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow,
            stat.S_IRUSR | stat.S_IWUSR,
        )
    except OSError as exc:
        raise SmokeBlocked(f"could not create {label}: {target}", ["crs"]) from exc


def write_trusted_crs_output(path: Path, label: str, content: str) -> Path:
    """Write one generated text artifact and verify it before later use."""

    descriptor = secure_crs_output_file(path, label)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
    except OSError as exc:
        raise SmokeBlocked(f"could not write {label}: {path}", ["crs"]) from exc
    return require_trusted_crs_path(path, label, directory=False)


def copy_trusted_crs_output(source: Path, destination: Path, label: str) -> Path:
    """Copy a validated source file into a generated CRS artifact safely."""

    descriptor = secure_crs_output_file(destination, label)
    try:
        with os.fdopen(descriptor, "wb") as output_handle:
            with source.open("rb") as input_handle:
                shutil.copyfileobj(input_handle, output_handle)
    except OSError as exc:
        raise SmokeBlocked(f"could not write {label}: {destination}", ["crs"]) from exc
    return require_trusted_crs_path(destination, label, directory=False)


def validate_crs_source_dir(candidate: Path) -> Path:
    """Validate every CRS path that the generated smoke config can include."""

    source_dir = require_trusted_crs_path(candidate, "CRS source directory", directory=True)
    setup_template = require_trusted_crs_path(
        source_dir / CRS_SETUP_TEMPLATE_NAME, "CRS setup template", directory=False
    )
    require_safe_crs_config_path(setup_template, "CRS setup template")
    rules_dir = require_trusted_crs_path(
        source_dir / "rules", "CRS rules directory", directory=True
    )
    require_safe_crs_config_path(rules_dir, "CRS rules directory")
    try:
        rule_files = sorted(path for path in rules_dir.iterdir() if path.name.endswith(".conf"))
    except OSError as exc:
        raise SmokeBlocked(f"CRS rules directory is unavailable: {rules_dir}", ["crs"]) from exc
    if not rule_files:
        raise SmokeBlocked(f"missing CRS rule files: {rules_dir}/*.conf", ["crs"])
    for rule_file in rule_files:
        trusted_rule_file = require_trusted_crs_path(rule_file, "CRS rule file", directory=False)
        require_safe_crs_config_path(trusted_rule_file, "CRS rule file")

    plugins_dir = source_dir / "plugins"
    if plugins_dir.exists() or plugins_dir.is_symlink():
        plugins_dir = require_trusted_crs_path(plugins_dir, "CRS plugins directory", directory=True)
        require_safe_crs_config_path(plugins_dir, "CRS plugins directory")
        plugin_files: list[Path] = []
        for pattern in ("*-config.conf", "*-before.conf", "*-after.conf"):
            plugin_files.extend(plugins_dir.glob(pattern))
        for plugin_file in sorted(set(plugin_files)):
            trusted_plugin_file = require_trusted_crs_path(
                plugin_file, "CRS plugin file", directory=False
            )
            require_safe_crs_config_path(trusted_plugin_file, "CRS plugin file")
    return source_dir


def resolve_crs_source_dir(args: argparse.Namespace) -> Path:
    for candidate in crs_source_candidate_roots(args):
        if (
            candidate.is_dir()
            and (candidate / CRS_SETUP_TEMPLATE_NAME).is_file()
            and (candidate / "rules").is_dir()
        ):
            return validate_crs_source_dir(candidate)
    configured = args.crs_source_dir or "<unset>"
    raise SmokeBlocked(f"missing CRS_SOURCE_DIR: {configured}; run make fetch-crs", ["crs"])


def free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class QuietHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        return


class UpstreamHandler(QuietHandler):
    def _answer(self) -> None:
        length = int(self.headers.get("content-length") or "0")
        if length > 0:
            self.rfile.read(length)
        body = b"msconnector upstream ok\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    do_GET = _answer
    do_POST = _answer
    do_HEAD = _answer


class SimpleDecisionBackend:
    decision_backend = "simple"
    modsecurity_backend_verified = False
    modsecurity_rule_loaded = False
    intervention_status: int | None = None
    last_error: str | None = None
    blocked_decision: dict[str, object] | None = None

    def decide(
        self,
        headers: http.client.HTTPMessage,
        path: str,
        method: str = "GET",
        body: bytes = b"",
    ) -> dict[str, object]:
        del path, method, body
        values = (
            headers.get("x-msconnector-block", ""),
            headers.get("x-modsec-smoke", ""),
        )
        if any(value.lower() in BLOCK_VALUES for value in values):
            return {
                "body": b"blocked by local msconnector decision service\n",
                "status": 403,
            }
        return {
            "body": b"allowed by local msconnector decision service\n",
            "status": 200,
        }


class ModSecurityDecisionBackend:
    decision_backend = "libmodsecurity"

    def __init__(
        self,
        helper: Path,
        rule_file: Path,
        decision_log_path: Path,
        env: dict[str, str],
        ruleset: str,
        crs_smoke_case: str,
        modsecurity_smoke_case: str,
    ) -> None:
        self.helper = helper
        self.rule_file = rule_file
        self.decision_log_path = decision_log_path
        self.env = env
        self.ruleset = ruleset
        self.crs_smoke_case = crs_smoke_case
        self.modsecurity_smoke_case = modsecurity_smoke_case
        self.modsecurity_backend_verified = False
        self.modsecurity_rule_loaded = False
        self.request_body_smoke_verified = False
        self.request_body_access_enabled = False
        self.request_body_rule_loaded = False
        self.intervention_status: int | None = None
        self.last_error: str | None = None
        self.blocked_decision: dict[str, object] | None = None
        self.allowed_decision: dict[str, object] | None = None
        self.crs_rule_id = ""
        self.crs_rule_message = ""

    def _evaluate(
        self,
        header_value: str,
        path: str,
        method: str = "GET",
        body: bytes = b"",
        content_type: str = "",
    ) -> dict[str, object]:
        if self.ruleset == "crs":
            self.rule_file = require_trusted_crs_path(
                self.rule_file, GENERATED_CRS_SMOKE_RULE_LABEL, directory=False
            )
            require_safe_crs_config_path(self.rule_file, GENERATED_CRS_SMOKE_RULE_LABEL)
        command = [
            str(self.helper),
            "--rule-file",
            str(self.rule_file),
            "--decision-log",
            str(self.decision_log_path),
            "--ruleset",
            self.ruleset,
            "--uri",
            path,
            "--smoke-case",
            self.modsecurity_smoke_case,
            "--method",
            method,
        ]
        if header_value:
            command.extend(["--header-value", header_value])
        if body:
            command.extend(["--body", body.decode("utf-8", errors="replace")])
            command.extend(["--content-type", content_type or REQUEST_BODY_CONTENT_TYPE])
            command.extend(["--request-body-marker", REQUEST_BODY_BLOCK_MARKER])
        completed = subprocess.run(
            command,
            check=False,
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"
            raise RuntimeError(f"libmodsecurity targeted evaluator failed: {detail}")
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"libmodsecurity targeted evaluator returned invalid JSON: {completed.stdout}") from exc
        if not payload.get("ok"):
            raise RuntimeError(str(payload.get("error") or "libmodsecurity targeted evaluator failed"))
        return payload

    def decide(
        self,
        headers: http.client.HTTPMessage,
        path: str,
        method: str = "GET",
        body: bytes = b"",
    ) -> dict[str, object]:
        if self.ruleset == "crs":
            header_value = ""
            evaluation_path = crs_probe_uri(headers, path)
            evaluation_body = b""
            content_type = ""
        elif self.modsecurity_smoke_case == "request_body":
            header_value = ""
            evaluation_path = path
            evaluation_body = body
            content_type = headers.get("content-type", REQUEST_BODY_CONTENT_TYPE)
        else:
            header_value = headers.get("x-modsec-smoke", "")
            evaluation_path = path
            evaluation_body = b""
            content_type = ""
        payload = self._evaluate(header_value, evaluation_path, method, evaluation_body, content_type)
        self.modsecurity_rule_loaded = bool(payload.get("modsecurity_rule_loaded"))
        self.request_body_access_enabled = bool(payload.get("request_body_access_enabled"))
        self.request_body_rule_loaded = bool(payload.get("request_body_rule_loaded"))
        disruptive = bool(payload.get("intervention_disruptive"))
        status = int(payload.get("intervention_status") or (403 if disruptive else 200))
        self.intervention_status = status
        if self.ruleset == "crs":
            is_block_probe = is_crs_block_probe(evaluation_path, self.crs_smoke_case)
            if is_block_probe:
                self.blocked_decision = payload
                self.crs_rule_id = str(payload.get("crs_rule_id") or payload.get("modsecurity_rule_id") or "")
                self.crs_rule_message = str(payload.get("crs_rule_message") or "")
                self.modsecurity_backend_verified = (
                    self.modsecurity_rule_loaded
                    and disruptive
                    and status == 403
                    and bool(self.crs_rule_id)
                    and self.crs_rule_id != "1000001"
                )
            else:
                self.allowed_decision = payload
            body = (
                b"blocked by libmodsecurity CRS smoke rule\n"
                if disruptive
                else b"allowed by libmodsecurity CRS smoke rule\n"
            )
            return {
                "body": body,
                "status": status if disruptive else 200,
            }
        if self.modsecurity_smoke_case == "request_body":
            body_has_marker = REQUEST_BODY_BLOCK_MARKER.encode("utf-8") in evaluation_body
            if body_has_marker:
                self.blocked_decision = payload
                self.request_body_smoke_verified = (
                    self.request_body_access_enabled
                    and self.request_body_rule_loaded
                    and disruptive
                    and status == 403
                    and payload.get("modsecurity_rule_id") == "1000002"
                )
                self.modsecurity_backend_verified = self.request_body_smoke_verified
            else:
                self.allowed_decision = payload
            response_body = (
                b"blocked by libmodsecurity request body smoke rule\n"
                if disruptive
                else b"allowed by libmodsecurity request body smoke rule\n"
            )
            return {
                "body": response_body,
                "status": status if disruptive else 200,
            }
        if header_value == "block":
            self.blocked_decision = payload
            self.modsecurity_backend_verified = (
                self.modsecurity_rule_loaded
                and disruptive
                and status == 403
                and payload.get("modsecurity_rule_id") == "1000001"
            )
        body = (
            b"blocked by libmodsecurity targeted smoke rule\n"
            if disruptive
            else b"allowed by libmodsecurity targeted smoke rule\n"
        )
        return {
            "body": body,
            "status": status if disruptive else 200,
        }


def read_request_body(handler: http.server.BaseHTTPRequestHandler) -> bytes:
    transfer_encoding = (handler.headers.get("transfer-encoding") or "").lower()
    if "chunked" in transfer_encoding:
        chunks: list[bytes] = []
        while True:
            line = handler.rfile.readline()
            if not line:
                break
            size_text = line.split(b";", 1)[0].strip()
            try:
                size = int(size_text, 16)
            except ValueError:
                break
            if size == 0:
                while True:
                    trailer = handler.rfile.readline()
                    if trailer in {b"\r\n", b"\n", b""}:
                        break
                break
            chunks.append(handler.rfile.read(size))
            handler.rfile.read(2)
        return b"".join(chunks)
    length = int(handler.headers.get("content-length") or "0")
    if length <= 0:
        return b""
    return handler.rfile.read(length)


def make_decision_handler(
    decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend,
    transcript_path: Path | None = None,
) -> type[QuietHandler]:
    class RuntimeDecisionHandler(QuietHandler):
        def _answer(self) -> None:
            try:
                request_body = read_request_body(self)
                decision = decision_backend.decide(self.headers, self.path, self.command, request_body)
                status = int(decision["status"])
                body = decision["body"]
            except Exception as exc:  # noqa: BLE001 - auth backend errors become smoke evidence.
                decision_backend.last_error = str(exc)
                status = 500
                body = f"decision backend error: {exc}\n".encode("utf-8")
                request_body = b""
            if transcript_path is not None:
                append_jsonl(
                    transcript_path,
                    {
                        "blocked_body_marker_present": REQUEST_BODY_BLOCK_MARKER.encode("utf-8") in request_body,
                        "body_length": len(request_body),
                        "content_length": self.headers.get("content-length"),
                        "decision_backend": decision_backend.decision_backend,
                        "method": self.command,
                        "path": self.path,
                        "response_status": status,
                        "transfer_encoding": self.headers.get("transfer-encoding"),
                    },
                )
            self.send_response(status)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        do_GET = _answer
        do_POST = _answer
        do_HEAD = _answer

    return RuntimeDecisionHandler


def append_jsonl(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")


def make_sidecar_proxy_handler(
    decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend,
    upstream_port: int,
    transcript_path: Path,
) -> type[QuietHandler]:
    class LighttpdSidecarProxyHandler(QuietHandler):
        def _answer(self) -> None:
            decision_status = 500
            upstream_status: int | None = None
            forwarded = False
            request_body = b""
            try:
                request_body = read_request_body(self)
                decision = decision_backend.decide(self.headers, self.path, self.command, request_body)
                decision_status = int(decision["status"])
                if decision_status >= 400:
                    body = decision["body"]
                    status = decision_status
                else:
                    forwarded = True
                    url = f"http://127.0.0.1:{upstream_port}{self.path}"
                    forward_headers = {
                        key: value
                        for key, value in self.headers.items()
                        if key.lower() not in {"connection", "host", "proxy-connection"}
                    }
                    data = request_body if self.command not in {"GET", "HEAD"} else None
                    request = urllib.request.Request(url, data=data, headers=forward_headers, method=self.command)
                    try:
                        with urllib.request.urlopen(request, timeout=2) as response:
                            body = response.read()
                            status = int(response.status)
                    except urllib.error.HTTPError as exc:
                        body = exc.read()
                        status = int(exc.code)
                    upstream_status = status
            except Exception as exc:  # noqa: BLE001 - proxy errors become smoke evidence.
                decision_backend.last_error = str(exc)
                body = f"sidecar proxy error: {exc}\n".encode("utf-8")
                status = 500

            append_jsonl(
                transcript_path,
                {
                    "blocked_body_marker_present": REQUEST_BODY_BLOCK_MARKER.encode("utf-8") in request_body,
                    "body_length": len(request_body),
                    "content_length": self.headers.get("content-length"),
                    "decision_backend": decision_backend.decision_backend,
                    "decision_status": decision_status,
                    "forwarded_to_lighttpd": forwarded,
                    "method": self.command,
                    "path": self.path,
                    "response_status": status,
                    "transfer_encoding": self.headers.get("transfer-encoding"),
                    "upstream_status": upstream_status,
                },
            )
            self.send_response(status)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        do_GET = _answer
        do_POST = _answer
        do_HEAD = _answer

    return LighttpdSidecarProxyHandler


def start_http_server(handler: type[http.server.BaseHTTPRequestHandler], port: int) -> http.server.ThreadingHTTPServer:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def http_status(
    url: str,
    headers: dict[str, str] | None = None,
    method: str = "GET",
    data: bytes | None = None,
) -> int:
    request = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
            return int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        return int(exc.code)


def wait_for_proxy(url: str, process: subprocess.Popen[object], deadline: float, expected_status: int = 200) -> None:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"proxy exited early with code {process.returncode}")
        try:
            status = http_status(url)
            if status == expected_status:
                return
            last_error = RuntimeError(f"proxy returned {status}, expected {expected_status}")
        except Exception as exc:  # noqa: BLE001 - startup probes may fail many ways.
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"proxy did not become ready: {last_error}")


def wait_for_http_url(
    url: str,
    deadline: float,
    expected_status: int = 200,
    process: subprocess.Popen[object] | None = None,
    label: str = "service",
) -> None:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            raise RuntimeError(f"{label} exited early with code {process.returncode}")
        try:
            status = http_status(url)
            if status == expected_status:
                return
            last_error = RuntimeError(f"{label} returned {status}, expected {expected_status}")
        except Exception as exc:  # noqa: BLE001 - startup probes may fail many ways.
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"{label} did not become ready: {last_error}")


def local_library_env(base_env: dict[str, str], lib_dir: Path, runtime_lookup_roots: list[str]) -> dict[str, str]:
    env = dict(base_env)
    paths = [str(lib_dir)]
    for candidate in (
        lib_dir.parent.parent.parent / "expat/lib",
        lib_dir.parent.parent.parent / "pcre2/lib",
        lib_dir.parent.parent.parent / "yajl/lib",
    ):
        if candidate.is_dir():
            paths.append(str(candidate))
    for root_text in runtime_lookup_roots:
        root = Path(root_text)
        for candidate in (
            root / "prefix/expat/lib",
            root / "cache-v2/shared/prefix/expat/lib",
            root / "expat/lib",
        ):
            if candidate.is_dir():
                paths.append(str(candidate))
    existing = env.get("LD_LIBRARY_PATH", "")
    if existing:
        paths.append(existing)
    env["LD_LIBRARY_PATH"] = os.pathsep.join(dict.fromkeys(paths))
    return env


def prepare_crs_smoke_config(args: argparse.Namespace, log_dir: Path) -> tuple[Path, Path, str]:
    source_dir = resolve_crs_source_dir(args)
    args.effective_crs_source_dir = str(source_dir)
    setup_template = source_dir / CRS_SETUP_TEMPLATE_NAME
    rules_dir = source_dir / "rules"
    if not setup_template.is_file():
        raise SmokeBlocked(f"missing CRS setup template: {setup_template}", ["crs"])
    if not rules_dir.is_dir():
        raise SmokeBlocked(f"missing CRS rules directory: {rules_dir}", ["crs"])
    rule_files = sorted(rules_dir.glob("*.conf"))
    if not rule_files:
        raise SmokeBlocked(f"missing CRS rule files: {rules_dir}/*.conf", ["crs"])

    smoke_label = "crs-smoke" if args.crs_smoke_case == "minimal" else "crs-secondary-smoke"
    evidence_root = require_safe_crs_config_path(Path(args.evidence_root), "CRS evidence root")
    evidence_root = ensure_trusted_crs_output_directory(evidence_root, "CRS evidence root")
    runtime_dir = ensure_trusted_crs_output_directory(
        evidence_root / smoke_label, "CRS smoke runtime directory"
    )
    crs_setup = copy_trusted_crs_output(
        setup_template, runtime_dir / "crs-setup.conf", "generated CRS setup file"
    )
    require_safe_crs_config_path(crs_setup, "generated CRS setup file")

    audit_log_name = "crs-audit.log" if args.crs_smoke_case == "minimal" else "crs-secondary-audit.log"
    log_dir = require_safe_crs_config_path(log_dir, "CRS audit-log directory")
    log_dir = ensure_trusted_crs_output_directory(log_dir, "CRS audit-log directory")
    audit_log_path = write_trusted_crs_output(
        log_dir / audit_log_name, "generated CRS audit log", ""
    )
    require_safe_crs_config_path(audit_log_path, "generated CRS audit log")
    args.effective_audit_log_path = str(audit_log_path)
    if args.crs_smoke_case == "minimal":
        rule_file_name = "modsecurity-crs-smoke.conf"
    else:
        rule_file_name = "modsecurity-crs-secondary-smoke.conf"
    rule_file = runtime_dir / rule_file_name
    lines = [
        f"# Generated by run_local_runtime_smoke.py for the {args.crs_smoke_case} CRS smoke.",
        "SecRuleEngine On",
        "SecRequestBodyAccess On",
        "SecResponseBodyAccess Off",
        "SecAuditEngine RelevantOnly",
        "SecAuditLogType Serial",
        f'SecAuditLog "{audit_log_path}"',
        f'Include "{crs_setup}"',
    ]
    plugins_dir = source_dir / "plugins"
    if plugins_dir.is_dir():
        lines.extend(
            [
                f'Include "{plugins_dir}/*-config.conf"',
                f'Include "{plugins_dir}/*-before.conf"',
            ]
        )
    lines.append(f'Include "{rules_dir}/*.conf"')
    if plugins_dir.is_dir():
        lines.append(f'Include "{plugins_dir}/*-after.conf"')
    rule_file = write_trusted_crs_output(
        rule_file,
        GENERATED_CRS_SMOKE_RULE_LABEL,
        "\n".join(lines) + "\n",
    )
    require_safe_crs_config_path(rule_file, GENERATED_CRS_SMOKE_RULE_LABEL)

    version = crs_version_from_source(source_dir, args.crs_git_ref)
    payload_name = "crs-smoke-payload.txt" if args.crs_smoke_case == "minimal" else "crs-secondary-smoke-payload.txt"
    write_trusted_crs_output(
        log_dir / payload_name,
        "CRS smoke payload evidence",
        "\n".join(
            [
                "allowed_path=/allowed",
                f"blocked_path={crs_blocked_path(args)}",
                f"crs_smoke_case={args.crs_smoke_case}",
                f"crs_smoke_description={CRS_SMOKE_CASES[args.crs_smoke_case]['description']}",
                f"crs_source_dir={source_dir}",
                f"crs_runtime_dir={runtime_dir}",
                f"crs_git_ref={args.crs_git_ref}",
                f"crs_version={version}",
                f"audit_log_path={audit_log_path}",
            ]
        )
        + "\n",
    )
    return rule_file, runtime_dir, version


def build_modsecurity_evaluator(args: argparse.Namespace, log_dir: Path) -> tuple[Path, dict[str, str]]:
    include_dir = Path(args.modsecurity_include_dir) if args.modsecurity_include_dir else None
    lib_dir = Path(args.modsecurity_lib_dir) if args.modsecurity_lib_dir else None
    lib_file = Path(args.modsecurity_lib_file) if args.modsecurity_lib_file else None
    rule_file_text = namespace_value(args, "effective_modsecurity_rule_file", args.modsecurity_rule_file)
    rule_file = Path(rule_file_text) if rule_file_text else None
    if include_dir is None or lib_dir is None or lib_file is None or rule_file is None:
        raise RuntimeError("local libmodsecurity include dir, lib dir, lib file, and rule file are required")
    if args.modsecurity_ruleset == "crs":
        rule_file = require_trusted_crs_path(
            rule_file, GENERATED_CRS_SMOKE_RULE_LABEL, directory=False
        )
        require_safe_crs_config_path(rule_file, GENERATED_CRS_SMOKE_RULE_LABEL)
    for path, label in (
        (include_dir / "modsecurity/modsecurity.h", "modsecurity.h"),
        (include_dir / "modsecurity/rules_set.h", "rules_set.h"),
        (include_dir / "modsecurity/transaction.h", "transaction.h"),
        (lib_file, "libmodsecurity shared library"),
        (rule_file, "ModSecurity smoke rule"),
    ):
        if not path.exists():
            raise RuntimeError(f"missing {label}: {path}")

    cxx = os.environ.get("CXX") or shutil.which("c++") or shutil.which("g++")
    if not cxx:
        raise RuntimeError("missing C++ compiler for libmodsecurity smoke evaluator")

    source = Path(args.connector_root) / "common/scripts/modsecurity_targeted_eval.cc"
    if not source.is_file():
        raise RuntimeError(f"modsecurity evaluator source missing: {source}")

    build_dir = Path(args.tmp_root) / f"{args.connector}-modsecurity-{args.modsecurity_ruleset}-smoke"
    build_dir.mkdir(parents=True, exist_ok=True)
    output = build_dir / "modsecurity_targeted_eval"
    command = [
        cxx,
        "-std=c++17",
        "-I",
        str(include_dir),
        str(source),
        "-L",
        str(lib_dir),
        f"-Wl,-rpath,{lib_dir}",
        "-lmodsecurity",
        "-o",
        str(output),
    ]
    (log_dir / "modsecurity-evaluator-build-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
    completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    (log_dir / "modsecurity-evaluator-build.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (log_dir / "modsecurity-evaluator-build.stderr.log").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"
        raise RuntimeError(f"could not build libmodsecurity evaluator: {detail}")
    output.chmod(0o755)
    env = local_library_env(os.environ, lib_dir, args.runtime_lookup_root)
    return output, env


def envoy_config(listen_port: int, admin_port: int, upstream_port: int, auth_port: int) -> str:
    return f"""static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 127.0.0.1
        port_value: {listen_port}
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          route_config:
            name: local_route
            virtual_hosts:
            - name: local_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: upstream_service
          http_filters:
          - name: envoy.filters.http.ext_authz
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
              http_service:
                server_uri:
                  uri: http://127.0.0.1:{auth_port}
                  cluster: ext_authz
                  timeout: 0.5s
                path_prefix: /auth
                authorization_request:
                  allowed_headers:
                    patterns:
                    - exact: content-length
                    - exact: content-type
                    - exact: x-msconnector-block
                    - exact: x-modsec-smoke
              with_request_body:
                max_request_bytes: 4096
                allow_partial_message: false
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
  clusters:
  - name: upstream_service
    connect_timeout: 0.25s
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: upstream_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: 127.0.0.1
                port_value: {upstream_port}
  - name: ext_authz
    connect_timeout: 0.25s
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: ext_authz
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: 127.0.0.1
                port_value: {auth_port}
admin:
  access_log_path: /dev/null
  address:
    socket_address:
      address: 127.0.0.1
      port_value: {admin_port}
"""


def traefik_dynamic_config(upstream_port: int, auth_port: int) -> str:
    return f"""http:
  routers:
    msconnector:
      entryPoints:
      - web
      rule: PathPrefix(`/`)
      middlewares:
      - msconnector-auth
      service: upstream
  middlewares:
    msconnector-auth:
      forwardAuth:
        address: http://127.0.0.1:{auth_port}/auth
        trustForwardHeader: true
        authRequestHeaders:
        - Content-Length
        - Content-Type
        - X-Msconnector-Block
        - X-Modsec-Smoke
        forwardBody: true
        maxBodySize: 4096
        preserveRequestMethod: true
  services:
    upstream:
      loadBalancer:
        servers:
        - url: http://127.0.0.1:{upstream_port}
"""


def lighttpd_escape(value: Path | str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def lighttpd_config(
    document_root: Path,
    upload_root: Path,
    error_log_path: Path,
    pid_path: Path,
    upstream_port: int,
) -> str:
    return f"""server.document-root = "{lighttpd_escape(document_root)}"
server.bind = "127.0.0.1"
server.port = {upstream_port}
server.errorlog = "{lighttpd_escape(error_log_path)}"
server.pid-file = "{lighttpd_escape(pid_path)}"
server.upload-dirs = ( "{lighttpd_escape(upload_root)}" )
index-file.names = ( "index.txt" )
mimetype.assign = ( ".txt" => "text/plain" )
"""


def build_proxy_command(connector: str, binary: Path, work_dir: Path, listen_port: int, upstream_port: int, auth_port: int) -> list[str]:
    if connector == "envoy":
        admin_port = free_port()
        config_path = work_dir / "envoy.yaml"
        config_path.write_text(envoy_config(listen_port, admin_port, upstream_port, auth_port), encoding="utf-8")
        return [
            str(binary),
            "-c",
            str(config_path),
            "--base-id",
            str((listen_port + admin_port) % 100000),
            "--disable-hot-restart",
            "--log-level",
            "error",
        ]

    if connector == "traefik":
        dynamic_path = work_dir / "traefik-dynamic.yml"
        dynamic_path.write_text(traefik_dynamic_config(upstream_port, auth_port), encoding="utf-8")
        return [
            str(binary),
            "--entryPoints.web.address=127.0.0.1:%d" % listen_port,
            "--providers.file.filename=%s" % dynamic_path,
            "--providers.file.watch=false",
            "--api=false",
            "--log.level=ERROR",
            "--global.sendAnonymousUsage=false",
        ]

    raise ValueError(f"unsupported connector for local runtime smoke: {connector}")


def writer_args(
    args: argparse.Namespace,
    status: str,
    exit_code: int,
    runtime_verified: bool,
    allowed: int | None,
    blocked: int | None,
    skipped_reason: str,
    missing: list[str],
    modsecurity_backend_verified: bool = False,
    modsecurity_rule_loaded: bool = False,
    intervention_status: int | None = None,
    decision_log_path: str = "",
    audit_log_path: str = "",
    lighttpd_binary_verified: bool = False,
    lighttpd_http_verified: bool = False,
    sidecar_proxy_verified: bool = False,
    lighttpd_log_path: str = "",
    upstream_log_path: str = "",
    request_transcript_path: str = "",
    request_body_smoke_verified: bool = False,
    request_body_access_enabled: bool = False,
    request_body_rule_loaded: bool = False,
    crs_minimal_smoke_verified: bool = False,
    crs_secondary_smoke_verified: bool = False,
    crs_rule_id: str = "",
    crs_rule_message: str = "",
) -> list[str]:
    effective_rule_file = namespace_value(args, "effective_modsecurity_rule_file", args.modsecurity_rule_file)
    effective_crs_runtime_dir = namespace_value(args, "effective_crs_runtime_dir", args.crs_runtime_dir)
    effective_crs_source_dir = namespace_value(args, "effective_crs_source_dir", args.crs_source_dir)
    crs_version = namespace_value(args, "effective_crs_version", "")
    modsecurity_rule_id = ""
    if args.decision_backend == "libmodsecurity":
        if args.modsecurity_ruleset == "crs":
            modsecurity_rule_id = crs_rule_id
        elif args.modsecurity_smoke_case == "request_body":
            modsecurity_rule_id = "1000002"
        else:
            modsecurity_rule_id = "1000001"
    request_body_rule_file = ""
    request_body_rule_id = ""
    request_method = ""
    blocked_body_marker = ""
    if args.decision_backend == "libmodsecurity" and args.modsecurity_smoke_case == "request_body":
        request_body_rule_file = effective_rule_file
        request_body_rule_id = "1000002"
        request_method = "POST"
        blocked_body_marker = REQUEST_BODY_BLOCK_MARKER
    command = [
        sys.executable,
        str(Path(args.connector_root) / "common/scripts/write_smoke_result.py"),
        "--connector",
        args.connector,
        "--integration-mode",
        args.integration_mode,
        "--status",
        status,
        "--exit-code",
        str(exit_code),
        "--runtime-verified",
        "true" if runtime_verified else "false",
        "--response-body-verified",
        "false",
        "--allowed-request-status",
        str(allowed) if allowed is not None else "not-run",
        "--blocked-request-status",
        str(blocked) if blocked is not None else "not-run",
        "--decision-backend",
        args.decision_backend,
        "--modsecurity-ruleset",
        args.modsecurity_ruleset if args.decision_backend == "libmodsecurity" else "",
        "--modsecurity-smoke-case",
        args.modsecurity_smoke_case if args.decision_backend == "libmodsecurity" else "",
        "--crs-smoke-case",
        args.crs_smoke_case if args.modsecurity_ruleset == "crs" else "",
        "--modsecurity-backend-verified",
        "true" if modsecurity_backend_verified else "false",
        "--modsecurity-rule-file",
        effective_rule_file,
        "--modsecurity-rule-id",
        modsecurity_rule_id,
        "--modsecurity-rule-loaded",
        "true" if modsecurity_rule_loaded else "false",
        "--request-body-smoke-verified",
        "true" if request_body_smoke_verified else "false",
        "--request-body-access-enabled",
        "true" if request_body_access_enabled else "false",
        "--request-body-rule-file",
        request_body_rule_file,
        "--request-body-rule-id",
        request_body_rule_id,
        "--request-body-rule-loaded",
        "true" if request_body_rule_loaded else "false",
        "--request-method",
        request_method,
        "--blocked-body-marker",
        blocked_body_marker,
        "--intervention-status",
        str(intervention_status) if intervention_status is not None else "not-run",
        "--audit-log-path",
        audit_log_path,
        "--decision-log-path",
        decision_log_path,
        "--lighttpd-binary-verified",
        "true" if lighttpd_binary_verified else "false",
        "--lighttpd-http-verified",
        "true" if lighttpd_http_verified else "false",
        "--sidecar-proxy-verified",
        "true" if sidecar_proxy_verified else "false",
        "--lighttpd-log-path",
        lighttpd_log_path,
        "--upstream-log-path",
        upstream_log_path,
        "--request-transcript-path",
        request_transcript_path,
        "--modsecurity-include-dir",
        args.modsecurity_include_dir,
        "--modsecurity-lib-dir",
        args.modsecurity_lib_dir,
        "--modsecurity-lib-file",
        args.modsecurity_lib_file,
        "--modsecurity-pkg-config-path",
        args.modsecurity_pkg_config_path,
        "--modsecurity-prefix",
        args.modsecurity_prefix,
        "--modsecurity-manifest",
        args.modsecurity_manifest,
        "--evidence-root",
        args.evidence_root,
        "--results-dir",
        args.results_dir,
        "--connector-root",
        args.connector_root,
        "--source-root",
        args.source_root,
        "--build-root",
        args.build_root,
        "--tmp-root",
        args.tmp_root,
        "--log-root",
        args.log_root,
        "--log-dir",
        args.log_dir,
        "--harness-path",
        args.harness_path,
        "--skipped-reason",
        skipped_reason,
        "--resolved-runtime-binary",
        args.resolved_runtime_binary,
        "--runtime-binary-env-var",
        args.runtime_binary_env_var,
        "--runtime-binary-name",
        args.runtime_binary_name,
        "--architecture-decision",
        args.architecture_decision,
        "--crs-repo-url",
        args.crs_repo_url,
        "--crs-git-ref",
        args.crs_git_ref,
        "--crs-source-dir",
        effective_crs_source_dir,
        "--crs-runtime-dir",
        effective_crs_runtime_dir,
        "--crs-version",
        crs_version,
        "--crs-minimal-smoke-verified",
        "true" if crs_minimal_smoke_verified else "false",
        "--crs-secondary-smoke-verified",
        "true" if crs_secondary_smoke_verified else "false",
        "--crs-rule-id",
        crs_rule_id,
        "--crs-rule-message",
        crs_rule_message,
    ]
    for dependency in missing:
        command.extend(["--missing-dependency", dependency])
    for root in args.runtime_lookup_root:
        command.extend(["--runtime-lookup-root", root])
    return command


def write_result(
    args: argparse.Namespace,
    status: str,
    exit_code: int,
    runtime_verified: bool,
    allowed: int | None,
    blocked: int | None,
    skipped_reason: str,
    missing: list[str],
    modsecurity_backend_verified: bool = False,
    modsecurity_rule_loaded: bool = False,
    intervention_status: int | None = None,
    decision_log_path: str = "",
    audit_log_path: str = "",
    lighttpd_binary_verified: bool = False,
    lighttpd_http_verified: bool = False,
    sidecar_proxy_verified: bool = False,
    lighttpd_log_path: str = "",
    upstream_log_path: str = "",
    request_transcript_path: str = "",
    request_body_smoke_verified: bool = False,
    request_body_access_enabled: bool = False,
    request_body_rule_loaded: bool = False,
    crs_minimal_smoke_verified: bool = False,
    crs_secondary_smoke_verified: bool = False,
    crs_rule_id: str = "",
    crs_rule_message: str = "",
) -> None:
    subprocess.run(
        writer_args(
            args,
            status,
            exit_code,
            runtime_verified,
            allowed,
            blocked,
            skipped_reason,
            missing,
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            decision_log_path,
            audit_log_path,
            lighttpd_binary_verified,
            lighttpd_http_verified,
            sidecar_proxy_verified,
            lighttpd_log_path,
            upstream_log_path,
            request_transcript_path,
            request_body_smoke_verified,
            request_body_access_enabled,
            request_body_rule_loaded,
            crs_minimal_smoke_verified,
            crs_secondary_smoke_verified,
            crs_rule_id,
            crs_rule_message,
        ),
        check=True,
    )


def run_lighttpd_sidecar_smoke(
    args: argparse.Namespace,
    decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend,
    decision_log_path: Path | None,
) -> int:
    binary = Path(args.resolved_runtime_binary)
    work_dir = Path(args.config_root)
    log_dir = Path(args.log_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    upstream_port = args.upstream_port or free_port()
    listen_port = args.listen_port or free_port()
    document_root = work_dir / "docroot"
    upload_root = work_dir / "upload"
    document_root.mkdir(parents=True, exist_ok=True)
    upload_root.mkdir(parents=True, exist_ok=True)
    (document_root / "index.txt").write_text("msconnector lighttpd upstream ok\n", encoding="utf-8")
    (document_root / "allowed").write_text("msconnector lighttpd upstream allowed\n", encoding="utf-8")

    lighttpd_log_path = log_dir / "lighttpd-error.log"
    if args.modsecurity_ruleset == "crs" and args.crs_smoke_case == "secondary":
        upstream_log_name = "crs-secondary-lighttpd-upstream.log"
        transcript_name = "crs-secondary-request-transcript.jsonl"
    elif args.modsecurity_ruleset == "crs":
        upstream_log_name = "crs-lighttpd-upstream.log"
        transcript_name = "crs-request-transcript.jsonl"
    elif request_body_smoke_enabled(args):
        upstream_log_name = "request-body-lighttpd-upstream.log"
        transcript_name = "request-body-request-transcript.jsonl"
    else:
        upstream_log_name = "lighttpd-upstream.log"
        transcript_name = "request-transcript.jsonl"
    upstream_log_path = log_dir / upstream_log_name
    request_transcript_path = log_dir / transcript_name
    stdout_path = log_dir / "lighttpd.stdout.log"
    stderr_path = log_dir / "lighttpd.stderr.log"
    config_path = work_dir / "lighttpd.conf"
    pid_path = work_dir / "lighttpd.pid"
    version_path = log_dir / "lighttpd-version.txt"
    command_path = work_dir / "lighttpd-command.txt"

    allowed_status: int | None = None
    blocked_status: int | None = None
    direct_status: int | None = None
    lighttpd_binary_verified = False
    lighttpd_http_verified = False
    sidecar_proxy_verified = False
    process: subprocess.Popen[object] | None = None
    sidecar_server: http.server.ThreadingHTTPServer | None = None

    try:
        for stale_path in (lighttpd_log_path, upstream_log_path, request_transcript_path):
            if stale_path.exists():
                stale_path.unlink()
        if decision_log_path is not None and decision_log_path.exists():
            decision_log_path.unlink()

        version_completed = subprocess.run(
            [str(binary), "-v"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        version_output = (version_completed.stdout + version_completed.stderr).strip()
        version_path.write_text(version_output + "\n", encoding="utf-8")
        lighttpd_binary_verified = binary.is_file() and os.access(binary, os.X_OK)
        if version_completed.returncode != 0:
            raise RuntimeError(f"lighttpd -v failed with code {version_completed.returncode}: {version_output}")

        config_path.write_text(
            lighttpd_config(document_root, upload_root, lighttpd_log_path, pid_path, upstream_port),
            encoding="utf-8",
        )
        command = [str(binary), "-D", "-f", str(config_path)]
        command_path.write_text(" ".join(command) + "\n", encoding="utf-8")
        upstream_log_path.write_text(
            "\n".join(
                [
                    f"lighttpd_binary={binary}",
                    f"lighttpd_config={config_path}",
                    f"lighttpd_upstream_port={upstream_port}",
                    f"sidecar_listen_port={listen_port}",
                    f"decision_backend={args.decision_backend}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
            direct_url = f"http://127.0.0.1:{upstream_port}/allowed"
            wait_for_http_url(direct_url, time.monotonic() + 12, process=process, label="lighttpd")
            direct_status = http_status(direct_url)
            lighttpd_http_verified = direct_status == 200

            sidecar_server = start_http_server(
                make_sidecar_proxy_handler(decision_backend, upstream_port, request_transcript_path),
                listen_port,
            )
            sidecar_url = f"http://127.0.0.1:{listen_port}/allowed"
            wait_for_http_url(sidecar_url, time.monotonic() + 8, label="lighttpd sidecar proxy")
            if request_body_smoke_enabled(args):
                allowed_status = http_status(
                    sidecar_url,
                    request_body_headers(),
                    method="POST",
                    data=REQUEST_BODY_ALLOW_BODY,
                )
                blocked_path = "/blocked"
                blocked_headers = request_body_headers()
                blocked_method = "POST"
                blocked_body: bytes | None = REQUEST_BODY_BLOCK_BODY
            else:
                allowed_status = http_status(sidecar_url)
                blocked_path = crs_blocked_path(args) if args.modsecurity_ruleset == "crs" else "/blocked"
                blocked_headers = {} if args.modsecurity_ruleset == "crs" else {"X-Modsec-Smoke": "block"}
                blocked_method = "GET"
                blocked_body = None
            blocked_status = http_status(
                f"http://127.0.0.1:{listen_port}{blocked_path}",
                blocked_headers,
                method=blocked_method,
                data=blocked_body,
            )

        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        backend_error = getattr(decision_backend, "last_error", None)
        sidecar_proxy_verified = lighttpd_http_verified and allowed_status == 200 and blocked_status == 403
        (
            request_body_smoke_verified,
            request_body_access_enabled,
            request_body_rule_loaded,
        ) = request_body_evidence(decision_backend)
        crs_rule_id = str(getattr(decision_backend, "crs_rule_id", ""))
        crs_rule_message = str(getattr(decision_backend, "crs_rule_message", ""))
        if args.modsecurity_ruleset == "crs" and args.crs_smoke_case == "secondary":
            crs_rule_id, crs_rule_message = crs_detection_from_audit_log(
                Path(namespace_value(args, "effective_audit_log_path", "")),
                crs_rule_id,
                crs_rule_message,
            )
        crs_case_verified = (
            args.modsecurity_ruleset == "crs"
            and sidecar_proxy_verified
            and modsecurity_backend_verified
            and bool(crs_rule_id)
        )
        crs_minimal_smoke_verified = crs_case_verified and args.crs_smoke_case == "minimal"
        crs_secondary_smoke_verified = crs_case_verified and args.crs_smoke_case == "secondary"
        success = sidecar_proxy_verified
        if args.decision_backend == "libmodsecurity" and args.modsecurity_ruleset == "crs":
            success = success and crs_case_verified
        elif args.decision_backend == "libmodsecurity":
            success = success and modsecurity_backend_verified

        with upstream_log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"direct_upstream_status={direct_status}\n")
            handle.write(f"allowed_sidecar_status={allowed_status}\n")
            handle.write(f"blocked_sidecar_status={blocked_status}\n")
            handle.write(f"lighttpd_http_verified={str(lighttpd_http_verified).lower()}\n")
            handle.write(f"sidecar_proxy_verified={str(sidecar_proxy_verified).lower()}\n")

        if success:
            write_result(
                args,
                "PASS",
                0,
                True,
                allowed_status,
                blocked_status,
                "",
                [],
                modsecurity_backend_verified,
                modsecurity_rule_loaded,
                intervention_status,
                str(decision_log_path) if decision_log_path is not None else "",
                namespace_value(args, "effective_audit_log_path", ""),
                lighttpd_binary_verified,
                lighttpd_http_verified,
                sidecar_proxy_verified,
                str(lighttpd_log_path),
                str(upstream_log_path),
                str(request_transcript_path),
                request_body_smoke_verified,
                request_body_access_enabled,
                request_body_rule_loaded,
                crs_minimal_smoke_verified,
                crs_secondary_smoke_verified,
                crs_rule_id,
                crs_rule_message,
            )
            return 0

        reason = "lighttpd sidecar_proxy smoke did not produce expected direct 200 and sidecar 200/403 statuses"
        missing: list[str] = []
        if args.decision_backend == "libmodsecurity" and not modsecurity_backend_verified:
            if args.modsecurity_ruleset == "crs":
                reason = "lighttpd libmodsecurity CRS smoke did not verify a CRS-backed 403 intervention"
            else:
                reason = "lighttpd libmodsecurity targeted smoke did not verify a rule-backed 403 intervention"
            missing = ["libmodsecurity"] if backend_error else []
        if backend_error:
            reason = f"{reason}: {backend_error}"
        status = "BLOCKED"
        exit_code = 77
        runtime_verified = False
        if (
            args.decision_backend == "libmodsecurity"
            and args.modsecurity_ruleset == "crs"
            and allowed_status == 200
            and backend_error is None
        ):
            status = "FAIL"
            exit_code = 1
            runtime_verified = True
            reason = f"lighttpd CRS smoke case {args.crs_smoke_case} did not produce CRS-backed HTTP 403 evidence"
            missing = []
        write_result(
            args,
            status,
            exit_code,
            runtime_verified,
            allowed_status,
            blocked_status,
            reason,
            missing,
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
            namespace_value(args, "effective_audit_log_path", ""),
            lighttpd_binary_verified,
            lighttpd_http_verified,
            sidecar_proxy_verified,
            str(lighttpd_log_path),
            str(upstream_log_path),
            str(request_transcript_path),
            request_body_smoke_verified,
            request_body_access_enabled,
            request_body_rule_loaded,
            crs_minimal_smoke_verified,
            crs_secondary_smoke_verified,
            crs_rule_id,
            crs_rule_message,
        )
        return exit_code
    except Exception as exc:  # noqa: BLE001 - runtime startup failures become blocked evidence.
        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            f"lighttpd sidecar_proxy smoke could not be completed: {exc}",
            [args.runtime_binary_name],
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
            "",
            lighttpd_binary_verified,
            lighttpd_http_verified,
            sidecar_proxy_verified,
            str(lighttpd_log_path),
            str(upstream_log_path),
            str(request_transcript_path),
            *request_body_evidence(decision_backend),
        )
        return 77
    finally:
        if sidecar_server is not None:
            sidecar_server.shutdown()
            sidecar_server.server_close()
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def run_smoke(args: argparse.Namespace) -> int:
    try:
        runtime_output_paths = validate_runtime_output_paths(args)
    except SmokeBlocked as exc:
        print(f"BLOCKED runtime output path: {exc.reason}", file=sys.stderr)
        return 77
    try:
        args.modsecurity_ruleset = normalize_ruleset(args.modsecurity_ruleset)
        args.modsecurity_smoke_case = normalize_modsecurity_smoke_case(args.modsecurity_smoke_case)
        args.crs_smoke_case = normalize_crs_smoke_case(args.crs_smoke_case)
    except SmokeBlocked as exc:
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            None,
            None,
            exc.reason,
            exc.missing_dependencies,
        )
        return 77
    config_root = runtime_output_paths.config_root
    if args.modsecurity_ruleset == "crs":
        args.modsecurity_smoke_case = "targeted"
        config_suffix = "crs-smoke" if args.crs_smoke_case == "minimal" else "crs-secondary-smoke"
        try:
            config_root = require_verified_runtime_output_path(
                str(config_root / config_suffix),
                "CONFIG_ROOT",
                runtime_output_paths.runtime_root,
            )
        except SmokeBlocked as exc:
            print(f"BLOCKED runtime output path: {exc.reason}", file=sys.stderr)
            return 77
        args.config_root = str(config_root)
    binary = Path(args.resolved_runtime_binary)
    work_dir = config_root
    log_dir = runtime_output_paths.log_dir
    work_dir.mkdir(parents=True, exist_ok=True)
    if args.modsecurity_ruleset != "crs":
        log_dir.mkdir(parents=True, exist_ok=True)
    if args.modsecurity_ruleset == "crs" and args.crs_smoke_case == "secondary":
        decision_log_name = "crs-secondary-decision.log"
    elif args.modsecurity_ruleset == "crs":
        decision_log_name = "crs-decision.log"
    elif request_body_smoke_enabled(args):
        decision_log_name = "request-body-decision.log"
    else:
        decision_log_name = "modsecurity-decision.log"
    decision_log_path = log_dir / decision_log_name if args.decision_backend == "libmodsecurity" else None
    if (
        args.modsecurity_ruleset != "crs"
        and args.connector != "lighttpd"
        and decision_log_path is not None
        and decision_log_path.exists()
    ):
        decision_log_path.unlink()

    try:
        if args.modsecurity_ruleset == "crs" and args.decision_backend != "libmodsecurity":
            raise SmokeBlocked("CRS smoke requires DECISION_BACKEND=libmodsecurity", ["libmodsecurity"])
        if args.decision_backend == "libmodsecurity":
            if args.modsecurity_ruleset == "crs":
                rule_file, crs_runtime_dir, crs_version = prepare_crs_smoke_config(args, log_dir)
                args.effective_modsecurity_rule_file = str(rule_file)
                args.effective_crs_runtime_dir = str(crs_runtime_dir)
                args.effective_crs_version = crs_version
            else:
                args.effective_modsecurity_rule_file = args.modsecurity_rule_file
                args.effective_crs_runtime_dir = args.crs_runtime_dir
                args.effective_crs_version = ""
            if args.connector != "lighttpd" and decision_log_path is not None and decision_log_path.exists():
                decision_log_path.unlink()
            helper, helper_env = build_modsecurity_evaluator(args, log_dir)
            decision_backend: SimpleDecisionBackend | ModSecurityDecisionBackend = ModSecurityDecisionBackend(
                helper,
                Path(args.effective_modsecurity_rule_file),
                decision_log_path if decision_log_path is not None else log_dir / "modsecurity-decision.log",
                helper_env,
                args.modsecurity_ruleset,
                args.crs_smoke_case,
                args.modsecurity_smoke_case,
            )
        else:
            decision_backend = SimpleDecisionBackend()
    except SmokeBlocked as exc:
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            None,
            None,
            exc.reason,
            exc.missing_dependencies,
            False,
            False,
            None,
            str(decision_log_path) if decision_log_path is not None else "",
        )
        return 77
    except Exception as exc:  # noqa: BLE001 - dependency/build gaps become blocked evidence.
        missing_dependency = "crs" if args.modsecurity_ruleset == "crs" and "CRS" in str(exc) else "libmodsecurity"
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            None,
            None,
            f"{args.connector} libmodsecurity decision backend could not be prepared: {exc}",
            [missing_dependency],
            False,
            False,
            None,
            str(decision_log_path) if decision_log_path is not None else "",
        )
        return 77

    if args.connector == "lighttpd":
        return run_lighttpd_sidecar_smoke(args, decision_backend, decision_log_path)

    upstream_port = args.upstream_port or free_port()
    auth_port = args.authz_port or free_port()
    listen_port = args.listen_port or free_port()
    upstream_server: http.server.ThreadingHTTPServer | None = None
    auth_server: http.server.ThreadingHTTPServer | None = None
    stdout_path = log_dir / f"{args.connector}.stdout.log"
    stderr_path = log_dir / f"{args.connector}.stderr.log"
    request_transcript_path = log_dir / "request-body-request-transcript.jsonl"
    allowed_status: int | None = None
    blocked_status: int | None = None
    process: subprocess.Popen[object] | None = None

    try:
        upstream_server = start_http_server(UpstreamHandler, upstream_port)
        if request_body_smoke_enabled(args) and request_transcript_path.exists():
            request_transcript_path.unlink()
        auth_server = start_http_server(
            make_decision_handler(
                decision_backend,
                request_transcript_path if request_body_smoke_enabled(args) else None,
            ),
            auth_port,
        )
        command = build_proxy_command(args.connector, binary, work_dir, listen_port, upstream_port, auth_port)
        (work_dir / "proxy-command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
            wait_for_proxy(f"http://127.0.0.1:{listen_port}/allowed", process, time.monotonic() + 12)
            if request_body_smoke_enabled(args):
                allowed_status = http_status(
                    f"http://127.0.0.1:{listen_port}/allowed",
                    request_body_headers(),
                    method="POST",
                    data=REQUEST_BODY_ALLOW_BODY,
                )
                blocked_headers = request_body_headers()
                blocked_path = "/blocked"
                blocked_method = "POST"
                blocked_body: bytes | None = REQUEST_BODY_BLOCK_BODY
            elif args.decision_backend == "libmodsecurity" and args.modsecurity_ruleset == "crs":
                allowed_status = http_status(f"http://127.0.0.1:{listen_port}/allowed")
                blocked_headers = {}
                blocked_path = crs_blocked_path(args)
                blocked_method = "GET"
                blocked_body = None
            elif args.decision_backend == "libmodsecurity":
                allowed_status = http_status(f"http://127.0.0.1:{listen_port}/allowed")
                blocked_headers = {"X-Modsec-Smoke": "block"}
                blocked_path = "/blocked"
                blocked_method = "GET"
                blocked_body = None
            else:
                allowed_status = http_status(f"http://127.0.0.1:{listen_port}/allowed")
                blocked_headers = {"X-Msconnector-Block": "1"}
                blocked_path = "/blocked"
                blocked_method = "GET"
                blocked_body = None
            blocked_status = http_status(
                f"http://127.0.0.1:{listen_port}{blocked_path}",
                blocked_headers,
                method=blocked_method,
                data=blocked_body,
            )

        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        backend_error = getattr(decision_backend, "last_error", None)
        (
            request_body_smoke_verified,
            request_body_access_enabled,
            request_body_rule_loaded,
        ) = request_body_evidence(decision_backend)
        crs_rule_id = str(getattr(decision_backend, "crs_rule_id", ""))
        crs_rule_message = str(getattr(decision_backend, "crs_rule_message", ""))
        if args.modsecurity_ruleset == "crs" and args.crs_smoke_case == "secondary":
            crs_rule_id, crs_rule_message = crs_detection_from_audit_log(
                Path(namespace_value(args, "effective_audit_log_path", "")),
                crs_rule_id,
                crs_rule_message,
            )
        crs_case_verified = (
            args.modsecurity_ruleset == "crs"
            and allowed_status == 200
            and blocked_status == 403
            and modsecurity_backend_verified
            and bool(crs_rule_id)
        )
        crs_minimal_smoke_verified = crs_case_verified and args.crs_smoke_case == "minimal"
        crs_secondary_smoke_verified = crs_case_verified and args.crs_smoke_case == "secondary"
        success = allowed_status == 200 and blocked_status == 403
        if args.decision_backend == "libmodsecurity" and args.modsecurity_ruleset == "crs":
            success = success and crs_case_verified
        elif args.decision_backend == "libmodsecurity":
            success = success and modsecurity_backend_verified

        if success:
            write_result(
                args,
                "PASS",
                0,
                True,
                allowed_status,
                blocked_status,
                "",
                [],
                modsecurity_backend_verified,
                modsecurity_rule_loaded,
                intervention_status,
                str(decision_log_path) if decision_log_path is not None else "",
                namespace_value(args, "effective_audit_log_path", ""),
                False,
                False,
                False,
                "",
                "",
                str(request_transcript_path) if request_body_smoke_enabled(args) else "",
                request_body_smoke_verified,
                request_body_access_enabled,
                request_body_rule_loaded,
                crs_minimal_smoke_verified,
                crs_secondary_smoke_verified,
                crs_rule_id,
                crs_rule_message,
            )
            return 0

        reason = f"{args.connector} local runtime smoke did not produce expected 200/403 statuses"
        missing: list[str] = []
        if args.decision_backend == "libmodsecurity" and not modsecurity_backend_verified:
            if args.modsecurity_ruleset == "crs":
                reason = f"{args.connector} libmodsecurity CRS smoke did not verify a CRS-backed 403 intervention"
            else:
                reason = (
                    f"{args.connector} libmodsecurity targeted smoke did not verify "
                    "a rule-backed 403 intervention"
                )
            missing = ["libmodsecurity"] if backend_error else []
        if backend_error:
            reason = f"{reason}: {backend_error}"
        status = "BLOCKED"
        exit_code = 77
        runtime_verified = False
        if (
            args.decision_backend == "libmodsecurity"
            and args.modsecurity_ruleset == "crs"
            and allowed_status == 200
            and backend_error is None
        ):
            status = "FAIL"
            exit_code = 1
            runtime_verified = True
            reason = (
                f"{args.connector} CRS smoke case {args.crs_smoke_case} "
                "did not produce CRS-backed HTTP 403 evidence"
            )
            missing = []
        write_result(
            args,
            status,
            exit_code,
            runtime_verified,
            allowed_status,
            blocked_status,
            reason,
            missing,
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
            namespace_value(args, "effective_audit_log_path", ""),
            False,
            False,
            False,
            "",
            "",
            str(request_transcript_path) if request_body_smoke_enabled(args) else "",
            request_body_smoke_verified,
            request_body_access_enabled,
            request_body_rule_loaded,
            crs_minimal_smoke_verified,
            crs_secondary_smoke_verified,
            crs_rule_id,
            crs_rule_message,
        )
        return exit_code
    except Exception as exc:  # noqa: BLE001 - all runtime startup failures become blocked evidence.
        modsecurity_backend_verified = bool(
            getattr(decision_backend, "modsecurity_backend_verified", False)
        )
        modsecurity_rule_loaded = bool(getattr(decision_backend, "modsecurity_rule_loaded", False))
        intervention_status = getattr(decision_backend, "intervention_status", None)
        write_result(
            args,
            "BLOCKED",
            77,
            False,
            allowed_status,
            blocked_status,
            f"{args.connector} local runtime smoke could not be completed: {exc}",
            [args.runtime_binary_name],
            modsecurity_backend_verified,
            modsecurity_rule_loaded,
            intervention_status,
            str(decision_log_path) if decision_log_path is not None else "",
            "",
            False,
            False,
            False,
            "",
            "",
            str(request_transcript_path) if request_body_smoke_enabled(args) else "",
            *request_body_evidence(decision_backend),
        )
        return 77
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if upstream_server is not None:
            upstream_server.shutdown()
            upstream_server.server_close()
        if auth_server is not None:
            auth_server.shutdown()
            auth_server.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, choices=["envoy", "traefik", "lighttpd"])
    parser.add_argument("--integration-mode", required=True)
    parser.add_argument("--resolved-runtime-binary", required=True)
    parser.add_argument("--runtime-binary-env-var", required=True)
    parser.add_argument("--runtime-binary-name", required=True)
    parser.add_argument("--runtime-lookup-root", action="append", default=[])
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--build-root", required=True)
    parser.add_argument("--tmp-root", required=True)
    parser.add_argument("--log-root", required=True)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--config-root", required=True)
    parser.add_argument("--listen-port", type=int, default=0)
    parser.add_argument("--upstream-port", type=int, default=0)
    parser.add_argument("--authz-port", type=int, default=0)
    parser.add_argument("--harness-path", required=True)
    parser.add_argument("--architecture-decision", default="")
    parser.add_argument("--decision-backend", choices=["simple", "libmodsecurity"], default="simple")
    parser.add_argument("--modsecurity-ruleset", default=os.environ.get("MODSECURITY_RULESET", "targeted"))
    parser.add_argument("--modsecurity-smoke-case", default=os.environ.get("MODSECURITY_SMOKE_CASE", "targeted"))
    parser.add_argument("--crs-smoke-case", default=os.environ.get("CRS_SMOKE_CASE", "minimal"))
    parser.add_argument("--modsecurity-rule-file", default="")
    parser.add_argument("--modsecurity-include-dir", default="")
    parser.add_argument("--modsecurity-lib-dir", default="")
    parser.add_argument("--modsecurity-lib-file", default="")
    parser.add_argument("--modsecurity-pkg-config-path", default="")
    parser.add_argument("--modsecurity-prefix", default="")
    parser.add_argument("--modsecurity-manifest", default="")
    parser.add_argument("--crs-repo-url", default=os.environ.get("CRS_REPO_URL", ""))
    parser.add_argument("--crs-git-ref", default=os.environ.get("CRS_GIT_REF", ""))
    parser.add_argument("--crs-source-dir", default=os.environ.get("CRS_SOURCE_DIR", ""))
    parser.add_argument("--crs-runtime-dir", default=os.environ.get("CRS_RUNTIME_DIR", ""))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_smoke(args)


if __name__ == "__main__":
    raise SystemExit(main())
