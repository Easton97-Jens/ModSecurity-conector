#!/usr/bin/env python3
"""Closed Parent route for the no-CRS/with-MRTS connector profile."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import secrets
import shutil
import stat
import subprocess
import sys
import re
import tempfile
from pathlib import Path
from typing import Any, NoReturn

LIB_ROOT = Path(__file__).resolve().parents[2] / "lib"
if str(LIB_ROOT) not in sys.path:
    sys.path.insert(0, str(LIB_ROOT))
from go_version_contract import GoVersionContractError, read_go_version_contract as read_shared_go_version_contract

CONNECTORS = {"envoy", "traefik", "lighttpd"}
PROFILE = "no-crs/with-mrts"
MAX_PLAN_BYTES = 1_048_576
MAX_RULE_ID_INVENTORY = 100_000
SHA256_RE = set("0123456789abcdef")
# The pinned CGo/libmodsecurity bridge observes the selected MRTS phase-1
# rule as Common request-body evidence. Retain that observed value as a single
# closed profile value rather than accepting either request phase.
RULE_MATCH_EVENT_PHASE = "request_body"
NO_CRS_RUN_ID_PREFIX = "mrts-"
NO_CRS_RUN_ID_HEX_LENGTH = 32
TRAEFIK_ENGINE_SOCKET_PARENT_PREFIX = "msct-"
TRAEFIK_ENGINE_SOCKET_PATH_MAX_BYTES = 100
TRAEFIK_ENGINE_SOCKET_CHILD_PREFIX = "msconnector-traefik-uds-"
TRAEFIK_ENGINE_SOCKET_CHILD_RANDOM_HEX_LENGTH = 16
TRAEFIK_ENGINE_SOCKET_FILENAME = "engine.sock"
NON_CANONICAL_GO_VERSION = "trusted Go binary returned a non-canonical version"


def _go_major_minor(version_output: str) -> str:
    fields = version_output.split()
    if len(fields) < 3 or fields[0:2] != ["go", "version"]:
        stop(NON_CANONICAL_GO_VERSION)
    if not fields[2].startswith("go"):
        stop(NON_CANONICAL_GO_VERSION)
    version = fields[2][2:]
    components = version.split(".")
    if len(components) not in {2, 3} or not all(
        component.isascii() and component.isdecimal() for component in components
    ):
        stop(NON_CANONICAL_GO_VERSION)
    return ".".join(components[:2])


def _canonical_rule_id(value: str) -> bool:
    return (
        bool(value)
        and len(value) <= 12
        and value[0] != "0"
        and value.isascii()
        and value.isdecimal()
    )


def stop(message: str) -> NoReturn:
    raise SystemExit(f"BLOCKED: {message}")


def new_no_crs_run_id() -> str:
    """Create the one invocation identity used across closed runtime hops."""

    return f"{NO_CRS_RUN_ID_PREFIX}{secrets.token_hex(NO_CRS_RUN_ID_HEX_LENGTH // 2)}"


def validate_no_crs_run_id(value: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != len(NO_CRS_RUN_ID_PREFIX) + NO_CRS_RUN_ID_HEX_LENGTH
        or not value.startswith(NO_CRS_RUN_ID_PREFIX)
        or any(character not in "0123456789abcdef" for character in value[len(NO_CRS_RUN_ID_PREFIX):])
    ):
        stop("NO_CRS_RUN_ID is not a canonical private run identity")
    return value


def private_root(value: str) -> Path:
    root = Path(value).expanduser()
    if not root.is_absolute() or ".." in root.parts:
        stop("runtime root must be absolute and traversal-free")
    component = Path(root.anchor)
    for part in root.parts[1:]:
        component /= part
        if component.exists() and component.is_symlink():
            stop("runtime root contains a symlink component")
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    root = root.resolve(strict=True)
    if root.is_symlink() or root.stat().st_uid != os.getuid():
        stop("runtime root is not owner-controlled")
    os.chmod(root, 0o700)
    return root


def _symlink_free_path(path: Path, label: str) -> None:
    """Reject symlink components in a task-created external boundary."""

    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        if current.is_symlink():
            stop(f"{label} contains a symlink component")


def create_private_traefik_engine_socket_parent() -> Path:
    """Allocate one short-lived private UDS parent for one Traefik run.

    The Traefik harness requires an existing parent because the actual socket
    child is allocated by its native runtime.  The canonical run root is too
    long for sockaddr_un on some hosts, so this intentionally uses a unique
    task-owned child allocated atomically by Python's secure temporary-
    directory API.  It is never shared with another connector or run and is
    removed by the caller.
    """

    try:
        path = Path(tempfile.mkdtemp(prefix=TRAEFIK_ENGINE_SOCKET_PARENT_PREFIX))
    except OSError as exc:
        stop(f"cannot allocate private Traefik engine socket parent: {exc}")
    try:
        _symlink_free_path(path, "Traefik engine socket parent")
        os.chmod(path, 0o700)
        selected = path.stat()
        if (
            selected.st_uid != os.geteuid()
            or (selected.st_mode & 0o777) != 0o700
            or not path.is_dir()
        ):
            stop("allocated Traefik engine socket parent is not private")
        socket_candidate = (
            path
            / f"{TRAEFIK_ENGINE_SOCKET_CHILD_PREFIX}{'f' * TRAEFIK_ENGINE_SOCKET_CHILD_RANDOM_HEX_LENGTH}"
            / TRAEFIK_ENGINE_SOCKET_FILENAME
        )
        if len(os.fsencode(str(socket_candidate))) > TRAEFIK_ENGINE_SOCKET_PATH_MAX_BYTES:
            stop("allocated Traefik engine socket path is too long")
    except BaseException:
        try:
            path.rmdir()
        except OSError:
            pass
        raise
    return path


def private_runtime_build(root: Path) -> Path:
    """Open the fixed runtime build child safely and idempotently.

    Framework preparation creates this directory before the target runner in
    hosted jobs.  Reopen only the literal direct child of the already-private
    root, then re-establish the exact owner/mode contract before it receives
    any further runtime artifact.
    """

    build = root / "build"
    try:
        build.mkdir(mode=0o700, exist_ok=True)
    except OSError as exc:
        stop(f"cannot create runtime build root: {exc}")
    if has_symlink_component(build):
        stop("runtime build root contains a symlink component")
    try:
        selected = build.lstat()
        resolved = build.resolve(strict=True)
    except OSError as exc:
        stop(f"runtime build root is unavailable: {exc}")
    if (
        not stat.S_ISDIR(selected.st_mode)
        or build.is_symlink()
        or resolved.parent != root
        or selected.st_uid != os.getuid()
    ):
        stop("runtime build root is not the private direct child")
    try:
        os.chmod(build, 0o700)
        selected = build.stat()
    except OSError as exc:
        stop(f"cannot secure runtime build root: {exc}")
    if selected.st_uid != os.getuid() or (selected.st_mode & 0o777) != 0o700:
        stop("runtime build root is not owner-private")
    return build


def remove_private_traefik_engine_socket_parent(path: Path) -> None:
    """Remove only the exact private parent allocated by this run."""

    _symlink_free_path(path, "Traefik engine socket parent")
    try:
        selected = path.lstat()
    except OSError as exc:
        stop(f"Traefik engine socket parent disappeared before cleanup: {exc}")
    if (
        not path.is_dir()
        or path.is_symlink()
        or selected.st_uid != os.geteuid()
        or (selected.st_mode & 0o777) != 0o700
    ):
        stop("Traefik engine socket parent changed before cleanup")
    if any(path.iterdir()):
        stop("Traefik engine socket parent contains artifacts after native cleanup")
    try:
        path.rmdir()
    except OSError as exc:
        stop(f"Traefik engine socket parent cleanup failed: {exc}")


def git_sha(path: Path) -> str:
    try:
        value = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        stop(f"cannot resolve git identity for {path}: {exc}")
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        stop(f"invalid git identity for {path}")
    return value


def git_output(path: Path, *arguments: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(path), *arguments], text=True, stderr=subprocess.STDOUT, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        stop(f"git provenance query failed for {path}: {exc}")


def repository_provenance(parent: Path, framework: Path, mrts: Path) -> dict[str, Any]:
    parent_link = git_output(parent, "ls-tree", "HEAD", "modules/ModSecurity-test-Framework").split()
    framework_link = git_output(framework, "ls-tree", "HEAD", "tools/MRTS").split()
    if len(parent_link) < 3 or len(framework_link) < 3:
        stop("required gitlink is missing or malformed")
    expected = {"parent_framework": parent_link[2], "framework_mrts": framework_link[2]}
    actual = {"parent_framework": git_sha(framework), "framework_mrts": git_sha(mrts)}
    if expected != actual:
        stop(f"gitlink mismatch: expected {expected}, checked out {actual}")
    repositories = {"parent": parent, "framework": framework, "mrts": mrts}
    origins: dict[str, dict[str, str]] = {}
    clean: dict[str, bool] = {}
    detached: dict[str, bool] = {}
    expected_origins = {
        "parent": "Easton97-Jens/ModSecurity-conector",
        "framework": "Easton97-Jens/ModSecurity-test-Framework",
        "mrts": "Easton97-Jens/MRTS",
    }
    for name, path in repositories.items():
        status = git_output(path, "status", "--porcelain=v1")
        clean[name] = not status
        if not clean[name]:
            stop(f"{name} checkout is dirty")
        branch = git_output(path, "rev-parse", "--abbrev-ref", "HEAD")
        detached[name] = branch == "HEAD"
        if name != "parent" and not detached[name]:
            stop(f"{name} checkout must be detached")
        remotes = {}
        remotes["fetch"] = git_output(path, "remote", "get-url", "origin")
        remotes["push"] = git_output(path, "remote", "get-url", "--push", "origin")
        for remote in ("fetch", "push"):
            normalized = remotes[remote].removesuffix(".git")
            owner, repository = expected_origins[name].split("/", 1)
            allowed = re.fullmatch(rf"(?:git@github\.com:{re.escape(owner)}/{re.escape(repository)}|https://github\.com/{re.escape(owner)}/{re.escape(repository)}|ssh://git@github\.com/{re.escape(owner)}/{re.escape(repository)})", normalized, re.IGNORECASE)
            if not allowed:
                stop(f"{name} origin {remote} does not match expected repository")
        origins[name] = remotes
    return {"gitlinks": expected, "checked_out": actual, "origins": origins, "clean": clean, "detached": detached}


def checked_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        stop(f"{label} must be absolute and traversal-free")
    if path.is_symlink() or any(part.is_symlink() for part in path.parents if part.exists()):
        stop(f"{label} contains a symlink component")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        stop(f"{label} is unavailable: {exc}")


def active_python_executable() -> Path:
    """Return the invocation path so a venv keeps its site-package context."""

    executable = Path(sys.executable)
    if not executable.is_absolute() or ".." in executable.parts:
        stop("trusted Python invocation must be absolute and traversal-free")
    parent = executable.parent
    while parent != parent.parent:
        if parent.is_symlink():
            stop("trusted Python invocation contains a symlinked parent")
        parent = parent.parent
    try:
        resolved = executable.resolve(strict=True)
    except OSError as exc:
        stop(f"trusted Python interpreter is unavailable: {exc}")
    if (
        not executable.is_file()
        or not os.access(executable, os.R_OK | os.X_OK)
        or not resolved.is_file()
        or not os.access(resolved, os.R_OK | os.X_OK)
    ):
        stop("trusted Python interpreter is unavailable")
    return executable


def read_go_version_contract(parent: Path) -> str:
    try:
        return read_shared_go_version_contract(parent)
    except GoVersionContractError as exc:
        stop(f"trusted Go version contract is invalid: {exc}")


def _go_directory_is_trusted(metadata: os.stat_result, *, hosted_toolcache: bool) -> bool:
    """Validate one directory on the selected Go binary's ancestry.

    ``actions/setup-go`` may provision its hosted-toolcache tree with the
    runner's primary group and group-write permission.  A root-owned component
    may also be group-writable by a group the unprivileged runner does not
    hold; it remains outside that runner's write authority.  World-writable
    components and group-write permissions for any other runner-held group
    remain rejected.  The fixed ``/usr/local/go`` contract keeps its stricter
    owner/non-writable rule.
    """

    mode = metadata.st_mode
    if not hosted_toolcache:
        return metadata.st_uid in {0, os.getuid()} and not mode & 0o022
    if metadata.st_uid == os.geteuid() and metadata.st_gid == os.getegid():
        return not mode & 0o002
    if metadata.st_uid == 0:
        if mode & 0o002:
            return False
        if not mode & 0o020:
            return True
        runner_groups = {os.getegid(), os.getgid(), *os.getgroups()}
        return metadata.st_gid == os.getegid() or metadata.st_gid not in runner_groups
    return False


def _validate_go_binary(executable: Path) -> Path:
    try:
        resolved = executable.resolve(strict=True)
    except OSError as exc:
        stop(f"trusted Go binary is unavailable: {exc}")
    if (
        not executable.is_file()
        or not os.access(executable, os.R_OK | os.X_OK)
        or not resolved.is_file()
        or not os.access(resolved, os.R_OK | os.X_OK)
    ):
        stop("trusted Go binary is unavailable")
    return resolved


def _validate_go_ancestry(executable: Path, hosted_toolcache: bool) -> None:
    hosted_toolcache_parent = Path("/opt/hostedtoolcache")
    for directory in (executable.parent, *executable.parents):
        try:
            metadata = directory.stat()
        except OSError as exc:
            stop(f"trusted Go binary parent is unavailable: {exc}")
        hosted_component = hosted_toolcache and (
            directory == hosted_toolcache_parent or hosted_toolcache_parent in directory.parents
        )
        if not _go_directory_is_trusted(metadata, hosted_toolcache=hosted_component):
            stop("trusted Go binary is not owner-controlled and non-writable")


def _read_go_binary_version(executable: Path) -> str:
    try:
        output = subprocess.check_output(
            [str(executable), "version"],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        stop(f"trusted Go binary cannot report its version: {exc}")
    return _go_major_minor(output)


def active_go_provenance(parent: Path) -> tuple[Path, str, str]:
    """Bind the existing setup-go binary to its approved root and version."""

    executable_raw = shutil.which("go")
    if not executable_raw:
        stop("trusted Go invocation is unavailable")
    executable = Path(executable_raw)
    if not executable.is_absolute() or ".." in executable.parts:
        stop("trusted Go invocation must be absolute and traversal-free")
    if has_symlink_component(executable) or executable.is_symlink() or parent in executable.parents:
        stop("trusted Go invocation contains a symlink component")
    hosted_toolcache_root = Path("/opt/hostedtoolcache/go")
    hosted_toolcache = hosted_toolcache_root == executable or hosted_toolcache_root in executable.parents
    if not any(root == executable or root in executable.parents for root in (Path("/usr/local/go"), hosted_toolcache_root)):
        stop("trusted Go invocation is outside the approved setup-go roots")
    _validate_go_binary(executable)
    _validate_go_ancestry(executable, hosted_toolcache)
    actual_major_minor = _read_go_binary_version(executable)
    expected_major_minor = read_go_version_contract(parent).rsplit(".", 1)[0]
    if expected_major_minor != actual_major_minor:
        stop("trusted Go binary does not satisfy the repository Go version contract")
    return executable, hashlib.sha256(executable.read_bytes()).hexdigest(), actual_major_minor


def active_go_executable(parent: Path | None = None) -> Path:
    """Compatibility accessor for tests and callers that only need the path."""

    if parent is None:
        parent = Path.cwd().resolve()
    return active_go_provenance(parent)[0]


def duplicate_safe_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def atomic_json(path: Path, value: Any) -> str:
    data = duplicate_safe_json(value).encode()
    if len(data) > MAX_PLAN_BYTES:
        stop("plan exceeds bounded size")
    digest = hashlib.sha256(data).hexdigest()
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return digest


def has_symlink_component(path: Path) -> bool:
    if not path.is_absolute():
        return True
    component = Path(path.anchor)
    for part in path.parts[1:]:
        component /= part
        try:
            if component.is_symlink():
                return True
        except OSError:
            return True
    return False


def load_framework_yaml(path: Path, framework_root: Path) -> dict[str, Any]:
    """Load a generated case through the exact checked-out Framework parser."""

    loader_path = framework_root / "ci" / "provisioning" / "import-mrts-cases.py"
    if has_symlink_component(loader_path):
        stop("Framework MRTS loader contains a symlink component")
    try:
        loader_path = loader_path.resolve(strict=True)
    except OSError as exc:
        stop(f"Framework MRTS loader is unavailable: {exc}")
    if (
        not loader_path.is_file()
        or loader_path.parent.parent.parent != framework_root
    ):
        stop("Framework MRTS loader escapes the exact Framework checkout")
    spec = importlib.util.spec_from_file_location("mrts_case_loader", loader_path)
    if spec is None or spec.loader is None:
        stop("Framework MRTS loader cannot be imported")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        parsed = module.load_yaml(path)
    except (OSError, ValueError) as exc:
        stop(f"generated MRTS case is invalid: {exc}")
    if not isinstance(parsed, dict):
        stop("generated MRTS case root is not a mapping")
    return parsed


def _select_direct_case(source: Path, document: dict[str, Any]) -> list[dict[str, Any]]:
    request = document.get("request")
    if not isinstance(request, dict) or document.get("portable") is not True:
        return []
    if request.get("method") != "GET":
        return []
    uri = request.get("path")
    expectation = document.get("expect")
    expected = expectation.get("rule_id") if isinstance(expectation, dict) else None
    if not isinstance(uri, str) or not uri.startswith("/?") or expected is None:
        return []
    return [{"id": source.stem, "source": source.name, "kind": "detection", "uri": uri, "expect_ids": [str(expected)], "expect_event_phase": RULE_MATCH_EVENT_PHASE}]


def _select_staged_cases(source: Path, document: dict[str, Any]) -> list[dict[str, Any]]:
    tests = document.get("tests", [])
    if not isinstance(tests, list):
        stop(f"MRTS tests is not a list: {source}")
    selected: list[dict[str, Any]] = []
    for item in tests:
        if not isinstance(item, dict):
            stop(f"MRTS test is not a mapping: {source}")
        for stage in item.get("stages", []):
            if not isinstance(stage, dict):
                continue
            request = stage.get("input", {})
            output = stage.get("output", {})
            log = output.get("log", {}) if isinstance(output, dict) else {}
            if not isinstance(request, dict) or request.get("method") != "GET":
                continue
            uri = request.get("uri")
            expected = log.get("expect_ids", []) if isinstance(log, dict) else []
            if not isinstance(uri, str) or not uri.startswith("/?") or not isinstance(expected, list) or not expected:
                continue
            selected.append({"id": f"{source.stem}:{item.get('test_id', len(selected))}", "source": source.name, "kind": "detection", "uri": uri, "expect_ids": [str(x) for x in expected], "expect_event_phase": RULE_MATCH_EVENT_PHASE})
    return selected


def _select_document_cases(source: Path, document: dict[str, Any]) -> list[dict[str, Any]]:
    meta = document.get("meta", {})
    metadata = document.get("metadata", {})
    upstream_file = metadata.get("upstream_file", "") if isinstance(metadata, dict) else ""
    is_args_get = (isinstance(meta, dict) and meta.get("name") == "MRTS_002_ARGS_A-GET.yaml") or str(upstream_file).endswith("MRTS_002_ARGS_A-GET.yaml")
    if not is_args_get or metadata.get("phase") != 1:
        return []
    if isinstance(document.get("request"), dict):
        return _select_direct_case(source, document)
    return _select_staged_cases(source, document)


def select_cases(case_root: Path, framework_root: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    selected: list[dict[str, Any]] = []
    sources: list[Path] = []
    for source in sorted(case_root.glob("*.yaml")):
        if source.is_symlink() or not source.is_file() or case_root not in source.resolve(strict=True).parents:
            stop(f"generated MRTS case is not a contained regular file: {source}")
        cases = _select_document_cases(source, load_framework_yaml(source, framework_root))
        selected.extend(cases)
        sources.extend(source for _ in cases)
    if not selected:
        stop("no applicable phase-1 GET ARGS MRTS cases were generated")
    # These controls are deliberately outside the imported attack cases and
    # use the same real host path. They prove DetectionOnly and bypass safety.
    selected.insert(0, {"id": "control-empty-args", "kind": "control", "uri": "/?mrts_control=1", "expect_ids": [], "expect_event_phase": RULE_MATCH_EVENT_PHASE})
    selected.append({"id": "bypass-safe-args", "kind": "bypass", "uri": "/?foo=benign-value", "expect_ids": [], "expect_event_phase": RULE_MATCH_EVENT_PHASE})
    return selected, sorted(set(sources))


def explicit_runtime_provisioning_environment(connector: str) -> dict[str, str]:
    """Allow only an explicit fixed opt-in for pinned runtime provisioning."""
    if connector not in CONNECTORS:
        stop("runtime provisioning connector is outside the closed profile")
    missing = [
        name
        for name in ("ALLOW_RUNTIME_DOWNLOADS", "ALLOW_RUNTIME_BUILDS")
        if os.environ.get(name) != "1"
    ]
    if missing:
        stop(f"real host provisioning requires explicit {' and '.join(missing)}=1")
    return {"ALLOW_RUNTIME_DOWNLOADS": "1", "ALLOW_RUNTIME_BUILDS": "1"}


def _validate_load_paths(load_file: Path, rules_root: Path, no_crs_rules: Path, mrts_root: Path, runtime_root: Path) -> tuple[Path, Path, Path, Path, list[str], dict[str, str]]:
    paths = (load_file, rules_root, mrts_root, runtime_root)
    if any(not path.is_absolute() or ".." in path.parts for path in paths):
        stop("MRTS validation paths must be absolute and traversal-free")
    if any(has_symlink_component(path) for path in paths):
        stop("MRTS validation path contains a symlink component")
    try:
        runtime_root = runtime_root.resolve(strict=True)
        rules_root = rules_root.resolve(strict=True)
        mrts_root = mrts_root.resolve(strict=True)
        no_crs_rules = no_crs_rules.resolve(strict=True)
        lines = load_file.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        stop(f"cannot inspect MRTS load file: {exc}")
    expected_rules_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "rules"
    if rules_root != expected_rules_root or not rules_root.is_dir():
        stop("MRTS rules root is not the expected private generated directory")
    canonical_root_raw = mrts_root / "generated" / "rules"
    if has_symlink_component(canonical_root_raw):
        stop("canonical MRTS rules root contains a symlink component")
    try:
        canonical_root = canonical_root_raw.resolve(strict=True)
    except OSError as exc:
        stop(f"canonical MRTS rules root is unavailable: {exc}")
    if canonical_root.parent.parent != mrts_root or not canonical_root.is_dir():
        stop("canonical MRTS rules root escapes the pinned MRTS checkout")
    canonical = _canonical_rules(canonical_root)
    return load_file, rules_root, no_crs_rules, mrts_root, lines, canonical


def _canonical_rules(canonical_root: Path) -> dict[str, str]:
    canonical: dict[str, str] = {}
    for source in sorted(canonical_root.glob("MRTS_*.conf")):
        if source.is_symlink() or not source.is_file() or source.parent != canonical_root:
            stop("canonical MRTS rule is not a direct regular file")
        canonical[source.name] = hashlib.sha256(source.read_bytes()).hexdigest()
    if not canonical:
        stop("pinned MRTS checkout has no canonical generated rules")
    return canonical


def _validate_load_include(line: str, allowed: dict[str, Path], rules_root: Path, no_crs_rules: Path, canonical: dict[str, str], includes: dict[str, str]) -> None:
    match = re.fullmatch(r'\s*Include\s+"([^"\r\n]+)"\s*', line)
    if match is None:
        stop("MRTS load file has a non-canonical include line")
    candidate = allowed.get(match.group(1))
    if candidate is None:
        stop("MRTS load file include is outside the generated pinned rule set")
    if candidate.parent != rules_root or has_symlink_component(candidate):
        stop("MRTS load file include is outside the private generated rules root")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        stop(f"MRTS load file include is unavailable: {exc}")
    if candidate.is_symlink() or resolved.is_symlink() or not resolved.is_file():
        stop("MRTS load file include is not a regular file")
    if resolved.parent != rules_root or not re.fullmatch(r"MRTS_[A-Z0-9_-]+\.conf", resolved.name):
        stop("MRTS load file include is outside the generated MRTS rules root")
    if resolved == no_crs_rules:
        stop("no-CRS baseline file is not a permitted MRTS include")
    if resolved.name in includes:
        stop("MRTS load file contains duplicate generated includes")
    observed_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if canonical.get(resolved.name) != observed_hash:
        stop("generated MRTS rule does not match the pinned canonical MRTS source")
    includes[resolved.name] = observed_hash


def validate_mrts_load_file(
    load_file: Path,
    rules_root: Path,
    no_crs_rules: Path,
    mrts_root: Path,
    runtime_root: Path,
) -> dict[str, str]:
    """Bind the generated load set byte-for-byte to the pinned MRTS rule corpus."""
    load_file, rules_root, no_crs_rules, mrts_root, lines, canonical = _validate_load_paths(
        load_file, rules_root, no_crs_rules, mrts_root, runtime_root
    )
    # Build candidates exclusively from the already validated pinned corpus.
    # The generated load file may name only one of these exact paths; never
    # construct a filesystem path from its untrusted include text.
    allowed_include_paths = {
        str(rules_root / name): rules_root / name for name in canonical
    }
    includes: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        _validate_load_include(line, allowed_include_paths, rules_root, no_crs_rules, canonical, includes)
    if includes != canonical:
        stop("MRTS load file must include the complete canonical generated rule set")
    return includes


def closed_connector_stage_command(connector: str) -> list[str]:
    """Build a fixed shell argv only for the three closed profile members."""

    stage_script_raw = Path(__file__).with_name("run-connector-stage.sh")
    if has_symlink_component(stage_script_raw):
        stop("connector stage runner contains a symlink component")
    try:
        stage_script = stage_script_raw.resolve(strict=True)
    except OSError as exc:
        stop(f"connector stage runner is unavailable: {exc}")
    if stage_script_raw.is_symlink() or not stage_script.is_file():
        stop("connector stage runner is not a regular file")
    if connector == "envoy":
        return ["sh", str(stage_script), "envoy", "no_crs_with_mrts"]
    if connector == "traefik":
        return ["sh", str(stage_script), "traefik", "no_crs_with_mrts"]
    if connector == "lighttpd":
        return ["sh", str(stage_script), "lighttpd", "no_crs_with_mrts"]
    stop("connector stage is outside the closed no-crs/with-mrts profile")


def rule_id_inventory(
    rules_root: Path, included_rules: dict[str, str]
) -> list[str]:
    """Extract the complete normalized ID inventory from the pinned rule load."""

    if len(included_rules) > MAX_RULE_ID_INVENTORY:
        stop("pinned MRTS rule corpus contains too many generated files")
    inventory: set[str] = set()
    id_marker = re.compile(r"\bid\s*:\s*([^,\s\\]+)")
    for name in sorted(included_rules):
        _add_rule_file_ids(rules_root, name, included_rules[name], id_marker, inventory)
        if len(inventory) > MAX_RULE_ID_INVENTORY:
            stop("pinned MRTS rule corpus contains too many rule IDs")
    if not inventory:
        stop("pinned MRTS rule corpus has an empty rule ID inventory")
    return sorted(inventory, key=lambda value: int(value))


def _add_rule_file_ids(
    rules_root: Path,
    name: str,
    expected_hash: str,
    id_marker: re.Pattern[str],
    inventory: set[str],
) -> None:
    path = rules_root / name
    if path.parent != rules_root or path.is_symlink() or has_symlink_component(path) or not path.is_file():
        stop("pinned MRTS rule inventory path is not a direct regular file")
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        stop(f"pinned MRTS rule cannot be parsed for ID inventory: {exc}")
    if len(data) > MAX_PLAN_BYTES:
        stop("pinned MRTS rule exceeds bounded size")
    if hashlib.sha256(data).hexdigest() != expected_hash:
        stop("pinned MRTS rule changed during ID inventory validation")
    found_in_file = 0
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        for match in id_marker.finditer(line):
            raw_id = match.group(1).strip("'\"")
            if not _canonical_rule_id(raw_id):
                stop(f"pinned MRTS rule has a non-canonical rule ID: {name}")
            if raw_id in inventory:
                stop(f"pinned MRTS rule corpus contains duplicate rule ID: {raw_id}")
            inventory.add(raw_id)
            found_in_file += 1
    if found_in_file == 0:
        stop(f"pinned MRTS rule has no canonical rule ID: {name}")


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            stop("sealed MRTS plan contains a duplicate JSON key")
        value[key] = item
    return value


def required_sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in SHA256_RE for character in value)
    ):
        stop(f"{label} must be a lowercase SHA-256 digest")
    return value


def load_sealed_plan(plan_path: Path, expected_plan_sha256: str) -> dict[str, Any]:
    """Load one bounded plan snapshot bound to the parent-held digest."""

    expected_plan_sha256 = required_sha256(
        expected_plan_sha256, "sealed MRTS plan digest"
    )
    try:
        data = plan_path.read_bytes()
    except OSError as exc:
        stop(f"sealed MRTS plan cannot be read: {exc}")
    if len(data) > MAX_PLAN_BYTES:
        stop("sealed MRTS plan exceeds bounded size")
    if hashlib.sha256(data).hexdigest() != expected_plan_sha256:
        stop("sealed MRTS plan digest does not match the parent-held value")
    try:
        plan = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicate_json_keys)
    except (UnicodeError, json.JSONDecodeError) as exc:
        stop(f"sealed MRTS plan is not valid JSON: {exc}")
    if not isinstance(plan, dict):
        stop("sealed MRTS plan root is not an object")
    return plan


def validate_plan_cases(cases: Any, allowed_rule_ids: set[str]) -> None:
    if not isinstance(cases, list) or len(cases) < 3:
        stop("sealed MRTS plan must contain bounded control, detection, and bypass cases")
    kinds: set[str] = set()
    for case in cases:
        kinds.add(_validate_plan_case(case, allowed_rule_ids))
    if kinds != {"control", "detection", "bypass"}:
        stop("sealed MRTS plan lacks a required case kind")


def _validate_plan_case(case: Any, allowed_rule_ids: set[str]) -> str:
    if not isinstance(case, dict):
        stop("sealed MRTS plan case is not an object")
    case_id = case.get("id")
    uri = case.get("uri")
    kind = case.get("kind")
    expected_ids = case.get("expect_ids")
    if (
        not isinstance(case_id, str) or not case_id or len(case_id) > 255
        or not isinstance(uri, str) or not uri.startswith("/") or len(uri) > 2048
        or any(ord(character) < 0x20 or ord(character) == 0x7F for character in uri)
        or kind not in {"control", "detection", "bypass"}
        or case.get("expect_event_phase") != RULE_MATCH_EVENT_PHASE
        or not isinstance(expected_ids, list)
    ):
        stop("sealed MRTS plan case is outside the closed runtime profile")
    _validate_expected_rule_ids(expected_ids, allowed_rule_ids, kind)
    return kind


def _validate_expected_rule_ids(expected_ids: list[Any], allowed_rule_ids: set[str], kind: str) -> None:
    for rule_id in expected_ids:
        if not isinstance(rule_id, str) or not rule_id or len(rule_id) > 12 or rule_id[0] == "0" or any(character not in "0123456789" for character in rule_id):
            stop("sealed MRTS plan case has an invalid expected rule ID")
        if rule_id not in allowed_rule_ids:
            stop("sealed MRTS plan case expects a rule ID outside the pinned corpus")
    if kind == "detection" and not expected_ids:
        stop("sealed MRTS detection case has no expected rule ID")
    if kind != "detection" and expected_ids:
        stop("sealed MRTS control or bypass case expects a rule ID")


def selected_case_hashes(case_root: Path, sources: list[Path]) -> dict[str, str]:
    """Return the exact generated sources that produced the selected cases."""

    return {
        str(path.relative_to(case_root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sources
    }


def selected_case_inventory_hash(sources: list[Path]) -> str:
    """Preserve the existing ordered inventory identity for the sealed plan."""

    return hashlib.sha256(b"".join(path.read_bytes() for path in sources)).hexdigest()


def validate_plan_case_binding(
    plan: dict[str, Any], runtime_root: Path, framework_root: Path
) -> None:
    """Reconstruct the exact selected cases before any connector can start.

    The case map in a plan is executable input, not merely descriptive
    metadata.  Reparse the generated Framework artifacts through the exact
    checked-out Framework loader so a syntactically valid plan cannot replace
    a pinned MRTS URI, rule expectation, selector, or phase after preparation.
    """

    case_root = _private_case_root(runtime_root)
    expected_cases, sources = select_cases(case_root, framework_root)
    expected_case_hashes = selected_case_hashes(case_root, sources)
    expected_inventory_hash = selected_case_inventory_hash(sources)
    if plan.get("inventory_root") != str(case_root):
        stop("sealed MRTS plan inventory root does not match")
    if plan.get("case_hashes") != expected_case_hashes:
        stop("sealed MRTS plan case-source hashes do not match")
    if plan.get("inventory_hash") != expected_inventory_hash:
        stop("sealed MRTS plan inventory hash does not match")
    if plan.get("cases") != expected_cases:
        stop("sealed MRTS plan cases do not match the pinned Framework inventory")


def _private_case_root(runtime_root: Path) -> Path:
    case_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
    if has_symlink_component(case_root):
        stop("sealed MRTS case inventory contains a symlink component")
    try:
        resolved = case_root.resolve(strict=True)
    except OSError as exc:
        stop(f"sealed MRTS case inventory is unavailable: {exc}")
    if resolved != case_root or not resolved.is_dir() or resolved.stat().st_uid != os.getuid():
        stop("sealed MRTS case inventory is not the private generated directory")
    return resolved


def validate_sealed_plan(
    plan_path: Path,
    runtime_root: Path,
    framework_root: Path,
    rules_root: Path,
    load_file: Path,
    expected_plan_sha256: str,
) -> None:
    """Revalidate the private plan and exact no-CRS rule binding before a host starts."""
    raw_paths = (plan_path, runtime_root, framework_root, rules_root, load_file)
    if any(not path.is_absolute() or ".." in path.parts for path in raw_paths):
        stop("sealed MRTS plan validation paths must be absolute and traversal-free")
    if any(has_symlink_component(path) for path in raw_paths):
        stop("sealed MRTS plan validation path contains a symlink component")
    try:
        plan_path = plan_path.resolve(strict=True)
        runtime_root = runtime_root.resolve(strict=True)
        framework_root = framework_root.resolve(strict=True)
        rules_root = rules_root.resolve(strict=True)
        load_file = load_file.resolve(strict=True)
    except OSError as exc:
        stop(f"sealed MRTS plan validation path is unavailable: {exc}")
    if plan_path.is_symlink() or not plan_path.is_file():
        stop("sealed MRTS plan is not a regular file")
    runtime_mode = runtime_root.stat().st_mode & 0o777
    if runtime_root.stat().st_uid != os.getuid() or runtime_mode != 0o700:
        stop("sealed MRTS plan runtime root is not private")
    plan = load_sealed_plan(plan_path, expected_plan_sha256)
    if plan.get("schema") != "no-crs-with-mrts-plan/v1":
        stop("sealed MRTS plan schema is invalid")
    if plan.get("profile") != PROFILE or plan.get("connector") not in CONNECTORS:
        stop("sealed MRTS plan profile is not closed")
    validation = plan.get("no_crs_validation")
    if not isinstance(validation, dict):
        stop("sealed MRTS plan lacks no-CRS validation")
    connector = plan["connector"]
    expected_plan = runtime_root / "build" / "stages" / connector / "no_crs_with_mrts" / "runtime" / "mrts-runtime-plan.json"
    expected_rules_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "rules"
    expected_load_file = runtime_root / "build" / "mrts" / "upstream-config-tests" / "mrts.load"
    if plan_path != expected_plan or rules_root != expected_rules_root or load_file != expected_load_file:
        stop("sealed MRTS plan paths do not match the closed private layout")
    validate_plan_case_binding(plan, runtime_root, framework_root)
    mrts_root = framework_root / "tools" / "MRTS"
    no_crs_rules = framework_root / "tests" / "rules" / "no-crs-baseline.conf"
    included_rules = validate_mrts_load_file(load_file, rules_root, no_crs_rules, mrts_root, runtime_root)
    inventory = rule_id_inventory(rules_root, included_rules)
    expected_validation = {
        "generated_rules_root": str(rules_root),
        "canonical_mrts_rules_root": str(mrts_root / "generated" / "rules"),
        "included_rule_sha256": included_rules,
        "rule_id_inventory": inventory,
    }
    if validation != expected_validation:
        stop("sealed MRTS plan no-CRS validation does not match loaded rules")
    validate_plan_cases(plan.get("cases"), set(inventory))
    if plan.get("load_file") != str(load_file):
        stop("sealed MRTS plan load-file path does not match")
    if plan.get("load_file_sha256") != hashlib.sha256(load_file.read_bytes()).hexdigest():
        stop("sealed MRTS plan load-file digest does not match")
    if plan.get("no_crs_rules_file") != str(no_crs_rules.resolve(strict=True)):
        stop("sealed MRTS plan no-CRS baseline identity does not match")


def validate_sealed_plan_command(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--rules-root", required=True)
    parser.add_argument("--load-file", required=True)
    parser.add_argument("--plan-sha256", required=True)
    args = parser.parse_args(arguments)
    validate_sealed_plan(
        Path(args.plan),
        Path(args.runtime_root),
        Path(args.framework_root),
        Path(args.rules_root),
        Path(args.load_file),
        args.plan_sha256,
    )
    return 0


def _parse_target_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    parser.add_argument("--parent-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--execute-stage", action="store_true", help="required: run the real host stage")
    return parser.parse_args(arguments)


def _validate_target_arguments(args: argparse.Namespace) -> None:
    if args.connector not in CONNECTORS:
        stop("connector is outside the closed no-crs/with-mrts profile")
    if not args.execute_stage:
        stop("--execute-stage is mandatory; plan-only execution is not a runtime result")
    if "NO_CRS_RUN_ID" in os.environ:
        stop("NO_CRS_RUN_ID must be generated by the closed target runner")


def _prepare_target_context(args: argparse.Namespace) -> dict[str, Any]:
    no_crs_run_id = validate_no_crs_run_id(new_no_crs_run_id())
    provisioning_environment = explicit_runtime_provisioning_environment(args.connector)
    root = private_root(args.runtime_root)
    parent = checked_path(args.parent_root, "Parent root")
    framework = checked_path(args.framework_root, "Framework root")
    expected_framework = (parent / "modules" / "ModSecurity-test-Framework").resolve(strict=True)
    if framework != expected_framework:
        stop("Framework root is not the exact Parent gitlink checkout")
    mrts = framework / "tools" / "MRTS"
    if not mrts.is_dir() or mrts.is_symlink():
        stop("MRTS checkout is missing or symlinked")
    provenance = repository_provenance(parent, framework, mrts)
    python_path = active_python_executable()
    go_path, go_sha256, go_version = active_go_provenance(parent)
    no_crs_rules = (framework / "tests" / "rules" / "no-crs-baseline.conf").resolve(strict=True)
    build = private_runtime_build(root)
    stage_runtime = build / "stages" / args.connector / "no_crs_with_mrts" / "runtime"
    stage_runtime.mkdir(mode=0o700, parents=True, exist_ok=True)
    if stage_runtime.is_symlink() or stage_runtime.stat().st_uid != os.getuid():
        stop("stage runtime root is not a private owner-controlled directory")
    os.chmod(stage_runtime, 0o700)
    env = {key: os.environ[key] for key in ("PATH", "HOME", "LANG", "LC_ALL") if key in os.environ}
    env.update({"PYTHON": str(python_path), "PYTHON_BIN": str(python_path), "MRTS_GO_BINARY": str(go_path), "MRTS_GO_BINARY_SHA256": go_sha256, "MRTS_GO_VERSION": go_version, "FRAMEWORK_ROOT": str(framework), "CONNECTOR_ROOT": str(parent), "VERIFIED_RUN_ROOT": str(root), "BUILD_ROOT": str(build), "MRTS_BUILD_ROOT": str(build / "mrts"), "TMP_ROOT": str(root / "tmp"), "LOG_ROOT": str(root / "logs"), "MODSECURITY_TEST_VARIANT": "no-crs", "MODSECURITY_MRTS_VARIANT": "with-mrts", "MODSECURITY_MRTS_PREPARED": "0", "MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO": "0", "GOTOOLCHAIN": "local", "NO_CRS_RUN_ID": no_crs_run_id})
    env.update(provisioning_environment)
    prepare = '. "$FRAMEWORK_ROOT/ci/lib/common.sh"; . "$FRAMEWORK_ROOT/ci/lib/mrts-common.sh"; prepare_mrts_runtime_variant'
    subprocess.run(["sh", "-eu", "-c", prepare], env=env, cwd=parent, check=True)
    return {"root": root, "parent": parent, "framework": framework, "mrts": mrts, "build": build, "stage_runtime": stage_runtime, "env": env, "no_crs_rules": no_crs_rules, "provenance": provenance, "python_path": python_path, "go_path": go_path, "go_sha256": go_sha256, "go_version": go_version}


def _create_runtime_plan(context: dict[str, Any], connector: str) -> tuple[Path, Path, dict[str, str], str]:
    root = context["root"]
    parent = context["parent"]
    framework = context["framework"]
    mrts = context["mrts"]
    build = context["build"]
    stage_runtime = context["stage_runtime"]
    no_crs_rules = context["no_crs_rules"]
    case_root = build / "mrts" / "upstream-config-tests" / "framework-cases"
    load_file = build / "mrts" / "upstream-config-tests" / "mrts.load"
    if not case_root.is_dir() or not load_file.is_file():
        stop("Framework did not produce MRTS case/load artifacts")
    cases, sources = select_cases(case_root, framework)
    for artifact in (case_root, load_file):
        resolved = artifact.resolve(strict=True)
        if artifact.is_symlink() or root not in resolved.parents:
            stop(f"MRTS artifact escapes private runtime root: {artifact}")
    included_rules = validate_mrts_load_file(
        load_file,
        build / "mrts" / "upstream-config-tests" / "rules",
        no_crs_rules,
        mrts,
        root,
    )
    source_hashes = selected_case_hashes(case_root, sources)
    executor = Path(__file__).with_name("execute-no-crs-mrts-cases.py").resolve(strict=True)
    if executor.is_symlink() or not executor.is_file() or not os.access(executor, os.R_OK):
        stop("MRTS executor is not a regular readable file")
    executor_sha256 = hashlib.sha256(executor.read_bytes()).hexdigest()
    rule_ids = rule_id_inventory(build / "mrts" / "upstream-config-tests" / "rules", included_rules)
    plan = {"schema": "no-crs-with-mrts-plan/v1", "profile": PROFILE, "connector": connector, "parent_commit": git_sha(parent), "framework_commit": git_sha(framework), "mrts_commit": git_sha(mrts), "provenance": context["provenance"], "executor": {"path": str(executor), "sha256": executor_sha256}, "inventory_root": str(case_root), "inventory_hash": selected_case_inventory_hash(sources), "case_hashes": source_hashes, "load_file": str(load_file), "load_file_sha256": hashlib.sha256(load_file.read_bytes()).hexdigest(), "no_crs_rules_file": str(no_crs_rules), "no_crs_validation": {"generated_rules_root": str(build / "mrts" / "upstream-config-tests" / "rules"), "canonical_mrts_rules_root": str(mrts / "generated" / "rules"), "included_rule_sha256": included_rules, "rule_id_inventory": rule_ids}, "cases": cases}
    plan_path = stage_runtime / "mrts-runtime-plan.json"
    if plan_path.exists():
        stop("runtime plan already exists; use a fresh private runtime root")
    plan_sha256 = atomic_json(plan_path, plan)
    validate_sealed_plan(plan_path, root, framework, build / "mrts" / "upstream-config-tests" / "rules", load_file, plan_sha256)
    return plan_path, executor, {"plan_sha256": plan_sha256, "load_file": str(load_file), "case_root": str(case_root), "rules_root": str(build / "mrts" / "upstream-config-tests" / "rules"), "no_crs_rules": str(no_crs_rules)}, executor_sha256


def _execute_target_stage(context: dict[str, Any], args: argparse.Namespace, plan_path: Path, executor: Path, metadata: dict[str, str], executor_sha256: str) -> None:
    env = context["env"]
    stage_runtime = context["stage_runtime"]
    parent = context["parent"]
    env.update({"MSCONNECTOR_MRTS_RUNTIME": "1", "MRTS_RUNTIME_PLAN": str(plan_path), "MRTS_RUNTIME_PLAN_SHA256": metadata["plan_sha256"], "MRTS_RUNTIME_RESULT": str(stage_runtime / "mrts-runtime-result.json"), "MRTS_RUNTIME_EXECUTOR": str(executor), "MRTS_RUNTIME_EXECUTOR_SHA256": executor_sha256, "MRTS_RUNTIME_RULES_ROOT": metadata["rules_root"], "NO_CRS_RULES_FILE": metadata["no_crs_rules"], "MSCONNECTOR_RULES_FILE": metadata["no_crs_rules"], "MRTS_LOAD_FILE": metadata["load_file"], "MRTS_CASE_ROOT": metadata["case_root"], "EVENT_LOG": str(stage_runtime / "events.jsonl")})
    traefik_socket_parent: Path | None = None
    try:
        if args.connector == "traefik":
            traefik_socket_parent = create_private_traefik_engine_socket_parent()
            env["TRAEFIK_ENGINE_SOCKET_PARENT"] = str(traefik_socket_parent)
        subprocess.run(
            closed_connector_stage_command(args.connector),
            cwd=parent,
            env=env,
            check=True,
        )
    finally:
        if traefik_socket_parent is not None:
            remove_private_traefik_engine_socket_parent(traefik_socket_parent)
    print(plan_path)


def main() -> int:
    args = _parse_target_arguments()
    _validate_target_arguments(args)
    context = _prepare_target_context(args)
    plan_path, executor, metadata, executor_sha256 = _create_runtime_plan(context, args.connector)
    _execute_target_stage(context, args, plan_path, executor, metadata, executor_sha256)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate-sealed-plan":
        raise SystemExit(validate_sealed_plan_command(sys.argv[2:]))
    raise SystemExit(main())
