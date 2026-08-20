#!/usr/bin/env python3
"""Closed Parent route for the no-CRS/with-MRTS connector profile."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import secrets
import subprocess
import sys
import re
from pathlib import Path
from typing import Any, NoReturn

CONNECTORS = {"envoy", "traefik", "lighttpd"}
PROFILE = "no-crs/with-mrts"
MAX_PLAN_BYTES = 1_048_576
SHA256_RE = set("0123456789abcdef")
# The pinned CGo/libmodsecurity bridge observes the selected MRTS phase-1
# rule as Common request-body evidence. Retain that observed value as a single
# closed profile value rather than accepting either request phase.
RULE_MATCH_EVENT_PHASE = "request_body"


def stop(message: str) -> NoReturn:
    raise SystemExit(f"BLOCKED: {message}")


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


def select_cases(case_root: Path, framework_root: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    selected: list[dict[str, Any]] = []
    sources: list[Path] = []
    for source in sorted(case_root.glob("*.yaml")):
        if source.is_symlink() or not source.is_file() or case_root not in source.resolve(strict=True).parents:
            stop(f"generated MRTS case is not a contained regular file: {source}")
        document = load_framework_yaml(source, framework_root)
        meta = document.get("meta", {})
        metadata = document.get("metadata", {})
        upstream_file = metadata.get("upstream_file", "") if isinstance(metadata, dict) else ""
        is_args_get = (isinstance(meta, dict) and meta.get("name") == "MRTS_002_ARGS_A-GET.yaml") or str(upstream_file).endswith("MRTS_002_ARGS_A-GET.yaml")
        if not is_args_get:
            continue
        if metadata.get("phase") != 1:
            continue
        if isinstance(document.get("request"), dict):
            request = document["request"]
            expected = document.get("expect", {}).get("rule_id") if isinstance(document.get("expect"), dict) else None
            if document.get("portable") is not True or request.get("method") != "GET":
                continue
            uri = request.get("path")
            if isinstance(uri, str) and uri.startswith("/?") and expected is not None:
                selected.append({"id": source.stem, "source": source.name, "kind": "detection", "uri": uri, "expect_ids": [str(expected)], "expect_event_phase": RULE_MATCH_EVENT_PHASE})
                sources.append(source)
            continue
        tests = document.get("tests", [])
        if not isinstance(tests, list):
            stop(f"MRTS tests is not a list: {source}")
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
                if not isinstance(uri, str) or not uri.startswith("/?"):
                    continue
                expected = log.get("expect_ids", []) if isinstance(log, dict) else []
                if not isinstance(expected, list) or not expected:
                    continue
                selected.append({"id": f"{source.stem}:{item.get('test_id', len(selected))}", "source": source.name, "kind": "detection", "uri": uri, "expect_ids": [str(x) for x in expected], "expect_event_phase": RULE_MATCH_EVENT_PHASE})
                sources.append(source)
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


def validate_mrts_load_file(
    load_file: Path,
    rules_root: Path,
    no_crs_rules: Path,
    mrts_root: Path,
    runtime_root: Path,
) -> dict[str, str]:
    """Bind the generated load set byte-for-byte to the pinned MRTS rule corpus."""
    if any(not path.is_absolute() or ".." in path.parts for path in (load_file, rules_root, mrts_root, runtime_root)):
        stop("MRTS validation paths must be absolute and traversal-free")
    if any(has_symlink_component(path) for path in (load_file, rules_root, mrts_root, runtime_root)):
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
    canonical: dict[str, str] = {}
    for source in sorted(canonical_root.glob("MRTS_*.conf")):
        if source.is_symlink() or not source.is_file() or source.parent != canonical_root:
            stop("canonical MRTS rule is not a direct regular file")
        canonical[source.name] = hashlib.sha256(source.read_bytes()).hexdigest()
    if not canonical:
        stop("pinned MRTS checkout has no canonical generated rules")
    includes: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        match = re.fullmatch(r'\s*Include\s+"([^"\r\n]+)"\s*', line)
        if match is None:
            stop("MRTS load file has a non-canonical include line")
        candidate = Path(match.group(1))
        if not candidate.is_absolute() or ".." in candidate.parts:
            stop("MRTS load file include is not an absolute traversal-free path")
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
    if includes != canonical:
        stop("MRTS load file must include the complete canonical generated rule set")
    return includes


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
    except (UnicodeError, ValueError) as exc:
        stop(f"sealed MRTS plan is not valid JSON: {exc}")
    if not isinstance(plan, dict):
        stop("sealed MRTS plan root is not an object")
    return plan


def validate_plan_cases(cases: Any) -> None:
    if not isinstance(cases, list) or len(cases) < 3:
        stop("sealed MRTS plan must contain bounded control, detection, and bypass cases")
    kinds: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            stop("sealed MRTS plan case is not an object")
        case_id = case.get("id")
        uri = case.get("uri")
        kind = case.get("kind")
        expected_ids = case.get("expect_ids")
        if (
            not isinstance(case_id, str) or not case_id or len(case_id) > 255 or
            not isinstance(uri, str) or not uri.startswith("/") or len(uri) > 2048 or
            any(ord(character) < 0x20 or ord(character) == 0x7F for character in uri) or
            kind not in {"control", "detection", "bypass"} or
            case.get("expect_event_phase") != RULE_MATCH_EVENT_PHASE or
            not isinstance(expected_ids, list)
        ):
            stop("sealed MRTS plan case is outside the closed runtime profile")
        if any(
            not isinstance(rule_id, str) or not rule_id or len(rule_id) > 12 or
            rule_id[0] == "0" or any(character not in "0123456789" for character in rule_id)
            for rule_id in expected_ids
        ):
            stop("sealed MRTS plan case has an invalid expected rule ID")
        if kind == "detection" and not expected_ids:
            stop("sealed MRTS detection case has no expected rule ID")
        if kind != "detection" and expected_ids:
            stop("sealed MRTS control or bypass case expects a rule ID")
        kinds.add(kind)
    if kinds != {"control", "detection", "bypass"}:
        stop("sealed MRTS plan lacks a required case kind")


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

    case_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
    if has_symlink_component(case_root):
        stop("sealed MRTS case inventory contains a symlink component")
    try:
        case_root = case_root.resolve(strict=True)
    except OSError as exc:
        stop(f"sealed MRTS case inventory is unavailable: {exc}")
    expected_case_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
    if (
        case_root != expected_case_root
        or not case_root.is_dir()
        or case_root.stat().st_uid != os.getuid()
    ):
        stop("sealed MRTS case inventory is not the private generated directory")
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
    validate_plan_cases(plan.get("cases"))
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
    validation = plan.get("no_crs_validation")
    if not isinstance(validation, dict):
        stop("sealed MRTS plan lacks no-CRS validation")
    expected_validation = {
        "generated_rules_root": str(rules_root),
        "canonical_mrts_rules_root": str(mrts_root / "generated" / "rules"),
        "included_rule_sha256": included_rules,
    }
    if validation != expected_validation:
        stop("sealed MRTS plan no-CRS validation does not match loaded rules")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    parser.add_argument("--parent-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--execute-stage", action="store_true", help="required: run the real host stage")
    args = parser.parse_args()
    if args.connector not in CONNECTORS:
        stop("connector is outside the closed no-crs/with-mrts profile")
    if not args.execute_stage:
        stop("--execute-stage is mandatory; plan-only execution is not a runtime result")
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
    no_crs_rules = (framework / "tests" / "rules" / "no-crs-baseline.conf").resolve(strict=True)
    build = root / "build"
    build.mkdir(mode=0o700)
    stage_runtime = build / "stages" / args.connector / "no_crs_with_mrts" / "runtime"
    stage_runtime.mkdir(mode=0o700, parents=True, exist_ok=True)
    if stage_runtime.is_symlink() or stage_runtime.stat().st_uid != os.getuid():
        stop("stage runtime root is not a private owner-controlled directory")
    os.chmod(stage_runtime, 0o700)
    env = {key: os.environ[key] for key in ("PATH", "HOME", "LANG", "LC_ALL") if key in os.environ}
    env.update({"PYTHON": str(python_path), "PYTHON_BIN": str(python_path), "FRAMEWORK_ROOT": str(framework), "CONNECTOR_ROOT": str(parent), "VERIFIED_RUN_ROOT": str(root), "BUILD_ROOT": str(build), "MRTS_BUILD_ROOT": str(build / "mrts"), "TMP_ROOT": str(root / "tmp"), "LOG_ROOT": str(root / "logs"), "MODSECURITY_TEST_VARIANT": "no-crs", "MODSECURITY_MRTS_VARIANT": "with-mrts", "MODSECURITY_MRTS_PREPARED": "0", "MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO": "0", "GOTOOLCHAIN": "local"})
    env.update(provisioning_environment)
    prepare = '. "$FRAMEWORK_ROOT/ci/lib/common.sh"; . "$FRAMEWORK_ROOT/ci/lib/mrts-common.sh"; prepare_mrts_runtime_variant'
    subprocess.run(["sh", "-eu", "-c", prepare], env=env, cwd=parent, check=True)
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
    plan = {"schema": "no-crs-with-mrts-plan/v1", "profile": PROFILE, "connector": args.connector, "parent_commit": git_sha(parent), "framework_commit": git_sha(framework), "mrts_commit": git_sha(mrts), "provenance": provenance, "executor": {"path": str(executor), "sha256": executor_sha256}, "inventory_root": str(case_root), "inventory_hash": selected_case_inventory_hash(sources), "case_hashes": source_hashes, "load_file": str(load_file), "load_file_sha256": hashlib.sha256(load_file.read_bytes()).hexdigest(), "no_crs_rules_file": str(no_crs_rules), "no_crs_validation": {"generated_rules_root": str(build / "mrts" / "upstream-config-tests" / "rules"), "canonical_mrts_rules_root": str(mrts / "generated" / "rules"), "included_rule_sha256": included_rules}, "cases": cases}
    plan_path = stage_runtime / "mrts-runtime-plan.json"
    if plan_path.exists():
        stop("runtime plan already exists; use a fresh private runtime root")
    plan_sha256 = atomic_json(plan_path, plan)
    validate_sealed_plan(plan_path, root, framework, build / "mrts" / "upstream-config-tests" / "rules", load_file, plan_sha256)
    env.update({"MSCONNECTOR_MRTS_RUNTIME": "1", "MRTS_RUNTIME_PLAN": str(plan_path), "MRTS_RUNTIME_PLAN_SHA256": plan_sha256, "MRTS_RUNTIME_RESULT": str(stage_runtime / "mrts-runtime-result.json"), "MRTS_RUNTIME_EXECUTOR": str(executor), "MRTS_RUNTIME_EXECUTOR_SHA256": executor_sha256, "MRTS_RUNTIME_RULES_ROOT": str(build / "mrts" / "upstream-config-tests" / "rules"), "NO_CRS_RULES_FILE": str(no_crs_rules), "MSCONNECTOR_RULES_FILE": str(no_crs_rules), "MRTS_LOAD_FILE": str(load_file), "MRTS_CASE_ROOT": str(case_root), "EVENT_LOG": str(stage_runtime / "events.jsonl")})
    subprocess.run(["sh", str(Path(__file__).with_name("run-connector-stage.sh")), args.connector, "no_crs_with_mrts"], cwd=parent, env=env, check=True)
    print(plan_path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate-sealed-plan":
        raise SystemExit(validate_sealed_plan_command(sys.argv[2:]))
    raise SystemExit(main())
