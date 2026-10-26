"""Admit the complete, expanded Parent test inventory before starting a child.

An execution is a selector, not a case. Its explicit cases include independently
exercised parameters and native fixture scenarios, even when a collector runs
them together. Source digests make changed collectors require reviewed expansion.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any
import unittest


HARD_CASE_LIMIT = 100
INVENTORY_PATH = Path("config/testing/active-cases.json")
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
IDENTIFIER = re.compile(r"[a-z][a-z0-9_.-]{0,127}", re.ASCII)
PYTHON_TARGET = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){2,}", re.ASCII)
GO_TEST = re.compile(r"Test\w+(?:/[A-Za-z0-9_.:=+-]+)*", re.ASCII)
GO_ALL_PACKAGES = "./..."
GO_MODULES = frozenset({
    "connectors/envoy/ext_proc", "connectors/traefik/native_middleware",
    "connectors/traefik/response_observer", "connectors/traefik/composite_middleware",
})
RUNTIME_CONNECTORS = ("apache", "haproxy", "envoy", "traefik", "lighttpd")
NATIVE_ARGUMENTS = {
    "ci/checks/common/run-active-authorization-timeout.sh": frozenset(
        (scenario,) for scenario in ("incomplete-headers", "incomplete-body")),
    "ci/runtime/lifecycle/run-active-no-crs-case.sh": frozenset(
        (connector,) for connector in RUNTIME_CONNECTORS),
    "ci/runtime/lifecycle/run-active-crs-case.sh": frozenset(
        (connector,) for connector in RUNTIME_CONNECTORS),
    "ci/runtime/lifecycle/run-connector-stage.sh": frozenset(
        (connector, stage) for connector in RUNTIME_CONNECTORS
        for stage in ("config_load", "start_smoke")),
    "ci/checks/security/check-workflow-fixture.sh": frozenset(
        (scenario,) for scenario in ("insecure", "safe", "permission-unsafe", "permission-safe")),
    "ci/checks/common/run-active-header-case.sh": frozenset(
        (scenario,) for scenario in ("valid-length", "duplicate-length", "overflow-length")),
    "connectors/nginx/harness/run-active-functional-a.sh": frozenset({()}),
    "ci/checks/common/run-active-targeted-evaluator.sh": frozenset({()}),
    "ci/checks/common/check-common-memory-safety.sh": frozenset({()}),
    "ci/checks/security/run-active-runtime-path-policy.sh": frozenset(
        (scenario,) for scenario in ("python-allowed", "python-blocked", "shell-allowed", "shell-blocked")),
}


class InventoryError(ValueError):
    """The complete active selection cannot be admitted safely."""


@dataclass(frozen=True)
class Inventory:
    root: Path
    digest: str
    executions: tuple[dict[str, Any], ...]
    case_ids: tuple[str, ...]
    path: Path | None = None
    offline_case_ids: tuple[str, ...] = ()

    @property
    def core_case_ids(self) -> tuple[str, ...]:
        exceptions = frozenset(self.offline_case_ids)
        return tuple(identifier for identifier in self.case_ids if identifier not in exceptions)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InventoryError("inventory contains a duplicate JSON key")
        result[key] = value
    return result


def _keys(value: Any, required: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != required:
        raise InventoryError(f"{label} must use the closed inventory schema")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None:
        raise InventoryError(f"{label} must be a stable nonempty identifier")
    return value


def _identifiers(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise InventoryError(f"{label} must be a nonempty unique identifier list")
    for item in value:
        _identifier(item, label)
    if len(value) != len(set(value)):
        raise InventoryError(f"{label} must be a nonempty unique identifier list")


def _relative_path(value: Any) -> PurePosixPath:
    if (not isinstance(value, str) or not value or "\\" in value or
            any(ord(character) < 32 or ord(character) == 127 for character in value)):
        raise InventoryError("source path must be a canonical relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in value.split("/")):
        raise InventoryError("source path must not traverse outside the repository")
    return path


def read_source(root: Path, relative: str) -> bytes:
    """Read a bounded regular source through non-symlink directory descriptors."""
    path = _relative_path(relative)
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        with os.fdopen(descriptor, "rb") as stream:
            observed = os.fstat(stream.fileno())
            if not stat.S_ISREG(observed.st_mode) or observed.st_size > MAX_SOURCE_BYTES:
                raise InventoryError("source must be a bounded regular non-symlink file")
            data = stream.read(MAX_SOURCE_BYTES + 1)
        if len(data) > MAX_SOURCE_BYTES:
            raise InventoryError("source exceeds the size limit")
        return data
    except OSError as exc:
        raise InventoryError("source must use existing non-symlink regular paths") from exc
    finally:
        os.close(directory)


def _validate_python_selector(selector: dict[str, Any], sources: dict[str, str]) -> None:
    _keys(selector, {"kind", "target"}, "Python selector")
    target = selector["target"]
    if not isinstance(target, str) or PYTHON_TARGET.fullmatch(target) is None:
        raise InventoryError("Python selector must name one exact module.Class.test_method")
    parts = target.split(".")
    if not parts[-1].startswith("test_") or "/".join(parts[:-2]) + ".py" not in sources:
        raise InventoryError("Python selector requires its exact test-module source binding")


def _go_package(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if value in {".", GO_ALL_PACKAGES}:
        return True
    return (value.startswith("./") and
            re.fullmatch(r"\./[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*", value, re.ASCII) is not None)


def _validate_go_selector(selector: dict[str, Any], sources: dict[str, str]) -> None:
    _keys(selector, {"kind", "module", "package", "test"}, "Go selector")
    if (not isinstance(selector["module"], str) or selector["module"] not in GO_MODULES or
            not _go_package(selector["package"])):
        raise InventoryError("Go selector requires one fixed Parent module and safe package")
    target = selector["test"]
    if not isinstance(target, str) or GO_TEST.fullmatch(target) is None:
        raise InventoryError("Go selector must name one exact TestName/subcase path")
    prefix = selector["module"] + "/"
    if not any(name.startswith(prefix) and name.endswith("_test.go") for name in sources):
        raise InventoryError("Go selector requires its test-source binding")


def _validate_native_selector(selector: dict[str, Any], sources: dict[str, str]) -> None:
    _keys(selector, {"kind", "script", "args"}, "native selector")
    script = str(_relative_path(selector["script"]))
    if not script.startswith(("ci/", "connectors/")) or not script.endswith(".sh"):
        raise InventoryError("native selector must name a bound Parent shell collector")
    if script not in sources or not _native_arguments(script, selector["args"]):
        raise InventoryError("native selector requires its source binding and closed arguments")


def _native_arguments(script: str, arguments: Any) -> bool:
    if not isinstance(arguments, list) or not all(isinstance(value, str) for value in arguments):
        return False
    return tuple(arguments) in NATIVE_ARGUMENTS.get(script, frozenset())


def _validate_selector(selector: Any, sources: dict[str, str]) -> None:
    if not isinstance(selector, dict):
        raise InventoryError("execution selector must be an object")
    kind = selector.get("kind")
    if not isinstance(kind, str):
        raise InventoryError("unknown execution selector kind")
    validator = {"python": _validate_python_selector, "go": _validate_go_selector,
                 "native": _validate_native_selector}.get(kind)
    if validator is None:
        raise InventoryError("unknown execution selector kind")
    validator(selector, sources)


def _source_bindings(sources: list[Any]) -> dict[str, str]:
    bindings = {}
    for source in sources:
        _keys(source, {"path", "sha256"}, "source binding")
        path, digest = source["path"], source["sha256"]
        _relative_path(path)
        if path in bindings:
            raise InventoryError("duplicate reviewed source path")
        if not isinstance(digest, str) or re.fullmatch(r"[a-f0-9]{64}", digest) is None:
            raise InventoryError("source SHA-256 must be an exact lowercase digest")
        bindings[path] = digest
    return bindings


def _expand_shared_sources(value: dict[str, Any], executions: list[Any]) -> None:
    """Validate the complete schema-3 pool/reference graph before expansion."""
    pool = value["source_bindings"]
    if not isinstance(pool, list) or not pool:
        raise InventoryError("shared source bindings must be a nonempty array")
    bindings = _source_bindings(pool)
    used = set()
    for execution in executions:
        references = execution.get("sources") if isinstance(execution, dict) else None
        if not isinstance(references, list) or not references:
            raise InventoryError("execution requires shared source references")
        local = set()
        for relative in references:
            _relative_path(relative)
            if relative not in bindings or relative in local:
                raise InventoryError("shared source references must be unique known paths")
            local.add(relative)
        used.update(local)
    if used != set(bindings):
        raise InventoryError("shared source bindings must not contain unused paths")
    for execution in executions:
        execution["sources"] = [{"path": relative, "sha256": bindings[relative]}
                                for relative in execution["sources"]]


def _validate_execution(execution: Any) -> None:
    required = {"id", "groups", "sources", "selector", "cases"}
    if isinstance(execution, dict) and "expected_subtests" in execution:
        required.add("expected_subtests")
    _keys(execution, required, "execution")
    _identifier(execution["id"], "execution ID")
    _identifiers(execution["groups"], "execution groups")
    sources = execution["sources"]
    if not isinstance(sources, list) or not sources:
        raise InventoryError("execution requires reviewed source SHA-256 bindings")
    bindings = _source_bindings(sources)
    # Keep a lookup map internally; the serialized contract explicitly names
    # the path and digest instead of treating source filenames as field names.
    execution["sources"] = bindings
    _validate_selector(execution["selector"], bindings)
    if not isinstance(execution["cases"], list) or not execution["cases"]:
        raise InventoryError("execution must explicitly enumerate its expanded cases")
    for case in execution["cases"]:
        _keys(case, {"id", "requirement", "profiles"}, "expanded case")
        _identifier(case["id"], "case ID")
        if not isinstance(case["requirement"], str) or not case["requirement"].strip():
            raise InventoryError("expanded case requires an observable requirement")
        _identifiers(case["profiles"], "case profiles")
    if "expected_subtests" in execution:
        expected = execution["expected_subtests"]
        if (execution["selector"]["kind"] != "python" or type(expected) is not int
                or not 0 <= expected <= len(execution["cases"])):
            raise InventoryError("expected subtests must match a bounded Python expansion")


def _read_inventory(path: Path) -> tuple[dict[str, Any], str]:
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as source:
        observed = os.fstat(source.fileno())
        if not stat.S_ISREG(observed.st_mode) or observed.st_size > MAX_INPUT_BYTES:
            raise InventoryError("inventory must be a bounded regular non-symlink file")
        data = source.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise InventoryError("inventory exceeds the size limit")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InventoryError("inventory must be strict UTF-8 JSON") from exc
    return value, hashlib.sha256(data).hexdigest()


def _python_definitions(relative: str, data: bytes) -> dict[tuple[str, str], int]:
    try:
        module = ast.parse(data, filename=relative)
    except (SyntaxError, UnicodeError) as exc:
        raise InventoryError("selected Python test source cannot be parsed") from exc
    definitions: dict[tuple[str, str], int] = {}
    for owner in module.body:
        if not isinstance(owner, ast.ClassDef):
            continue
        for method in owner.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                key = (owner.name, method.name)
                definitions[key] = definitions.get(key, 0) + 1
    return definitions


def _python_test_definition(selector: dict[str, Any], source_bytes: dict[str, bytes],
                            definitions_cache: dict[str, dict[tuple[str, str], int]]) -> None:
    parts = selector["target"].split(".")
    relative = "/".join(parts[:-2]) + ".py"
    if relative not in definitions_cache:
        definitions_cache[relative] = _python_definitions(relative, source_bytes[relative])
    if definitions_cache[relative].get((parts[-2], parts[-1]), 0) != 1:
        raise InventoryError("Python selector must resolve to one source-defined test method")


def _go_test_definition(root: Path, selector: dict[str, Any], source_bytes: dict[str, bytes]) -> None:
    name = selector["test"].split("/")[0]
    pattern = re.compile(rb"(?m)^func\s+" + name.encode("ascii") + rb"\s*\(")
    prefix = selector["module"] + "/"
    package = selector["package"]
    package_root = root / selector["module"]
    if package not in {".", GO_ALL_PACKAGES}:
        package_root /= package.removeprefix("./")
    candidates = (package_root.rglob("*_test.go") if package == GO_ALL_PACKAGES
                  else package_root.glob("*_test.go"))
    matches = [path.relative_to(root).as_posix() for path in candidates
               if pattern.search(read_source(root, path.relative_to(root).as_posix()))]
    if len(matches) != 1 or matches[0] not in source_bytes:
        raise InventoryError("Go selector must resolve to one bound test definition")
    if package != GO_ALL_PACKAGES:
        relative_package = "" if package == "." else package.removeprefix("./") + "/"
        if str(PurePosixPath(matches[0]).parent) + "/" != prefix + relative_package:
            raise InventoryError("Go selector package differs from its bound test definition")


def _validate_test_definition(root: Path, execution: dict[str, Any], source_bytes: dict[str, bytes],
                              definitions_cache: dict[str, dict[tuple[str, str], int]]) -> None:
    selector = execution["selector"]
    if selector["kind"] == "python":
        _python_test_definition(selector, source_bytes, definitions_cache)
    if selector["kind"] == "go":
        _go_test_definition(root, selector, source_bytes)


def _validate_source_definitions(root: Path, executions: list[dict[str, Any]]) -> None:
    # These caches live for this admission only. Every declared expected hash
    # is compared, even when another selector already used the same file.
    sources: dict[str, tuple[str, bytes]] = {}
    definitions_cache: dict[str, dict[tuple[str, str], int]] = {}
    for execution in executions:
        source_bytes = {}
        for relative, expected in execution["sources"].items():
            if relative not in sources:
                data = read_source(root, relative)
                sources[relative] = (hashlib.sha256(data).hexdigest(), data)
            actual, data = sources[relative]
            if actual != expected:
                raise InventoryError(f"reviewed source digest mismatch: {relative}")
            source_bytes[relative] = data
        _validate_test_definition(root, execution, source_bytes, definitions_cache)


def _validate_offline_exceptions(exceptions: list[dict[str, Any]]) -> None:
    for execution in exceptions:
        if (execution["selector"]["kind"] != "python" or
                "offline-unit" not in execution["groups"] or
                not execution["id"].startswith("offline.") or
                "expected_subtests" not in execution):
            raise InventoryError("offline exceptions require explicit source-bound Python unit selectors")


def load_inventory(root: Path, inventory_path: Path | None = None) -> Inventory:
    """Admit the entire expanded inventory, including unrequested groups."""
    root = root.resolve(strict=True)
    path = inventory_path or root / INVENTORY_PATH
    value, digest = _read_inventory(path)
    version = value.get("schema_version") if isinstance(value, dict) else None
    if type(version) is not int or version not in {1, 2, 3}:
        raise InventoryError("unsupported active-inventory schema version")
    keys = {"schema_version", "executions"}
    if version >= 2:
        keys.add("offline_unit_exceptions")
    if version == 3:
        keys.add("source_bindings")
    _keys(value, keys, "inventory")
    core = value["executions"]
    exceptions = value.get("offline_unit_exceptions", [])
    if not isinstance(core, list) or not core or not isinstance(exceptions, list):
        raise InventoryError("inventory must contain active executions")
    executions = core + exceptions
    if version == 3:
        _expand_shared_sources(value, executions)
    for execution in executions:
        _validate_execution(execution)
    core_count = sum(len(item["cases"]) for item in core)
    if core_count > HARD_CASE_LIMIT:
        raise InventoryError(f"expanded core active inventory has {core_count} cases; hard limit is 100")
    _validate_offline_exceptions(exceptions)
    case_ids = tuple(case["id"] for item in executions for case in item["cases"])
    if len(case_ids) != len(set(case_ids)):
        raise InventoryError("duplicate expanded case ID")
    execution_ids = [item["id"] for item in executions]
    selectors = [json.dumps(item["selector"], sort_keys=True) for item in executions]
    if len(execution_ids) != len(set(execution_ids)) or len(selectors) != len(set(selectors)):
        raise InventoryError("duplicate execution ID or selector; enumerate variants together")
    _validate_source_definitions(root, executions)
    offline_ids = tuple(case["id"] for item in exceptions for case in item["cases"])
    return Inventory(root, digest, tuple(executions), case_ids, path, offline_ids)


def _recheck_bindings(inventory: Inventory) -> None:
    if inventory.path is None or _read_inventory(inventory.path)[1] != inventory.digest:
        raise InventoryError("active inventory changed after admission")
    checked: dict[tuple[str, str], bytes] = {}
    for execution in inventory.executions:
        for relative, expected in execution["sources"].items():
            binding = (relative, expected)
            if binding in checked:
                continue
            data = read_source(inventory.root, relative)
            if hashlib.sha256(data).hexdigest() != expected:
                raise InventoryError(f"reviewed source digest mismatch before execution: {relative}")
            checked[binding] = data
        if execution["selector"]["kind"] == "go":
            # Go's uniqueness proof also includes current package membership:
            # a newly added, unbound *_test.go can introduce another definition.
            source_bytes = {relative: checked[(relative, expected)]
                            for relative, expected in execution["sources"].items()}
            _go_test_definition(inventory.root, execution["selector"], source_bytes)
    # Initial admission already resolved every definition. Exact unchanged
    # source bytes preserve that proof; repeated AST parsing adds no evidence.


def select_executions(inventory: Inventory, groups: tuple[str, ...] = (),
                      case_ids: tuple[str, ...] = (), module: str | None = None,
                      execution_ids: tuple[str, ...] = ()
                      ) -> tuple[dict[str, Any], ...]:
    """Select executions with closure over every explicitly expanded variant."""
    available = {group for item in inventory.executions for group in item["groups"]}
    if any(group not in available for group in groups):
        raise InventoryError("unknown or empty requested group")
    if any(case not in inventory.case_ids for case in case_ids):
        raise InventoryError("unknown requested case ID")
    if module is not None and module not in GO_MODULES:
        raise InventoryError("module filter must name a fixed Parent Go module")
    available_executions = {item["id"] for item in inventory.executions}
    if any(identifier not in available_executions for identifier in execution_ids):
        raise InventoryError("unknown requested execution ID")
    selected = tuple(item for item in inventory.executions if (
        (not groups and not case_ids and not execution_ids or
         set(groups).intersection(item["groups"]) or item["id"] in execution_ids or
         set(case_ids).intersection(case["id"] for case in item["cases"])) and
        (module is None or item["selector"].get("module") == module)))
    if not selected:
        raise InventoryError("requested selection has no active execution")
    return selected


def selection_summary(inventory: Inventory, selected: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    exceptions = frozenset(inventory.offline_case_ids)
    selected_ids = [case["id"] for item in selected for case in item["cases"]]
    return {"schema_version": 1, "inventory_sha256": inventory.digest,
            "active_case_count": len(inventory.case_ids), "hard_limit": HARD_CASE_LIMIT,
            "budget_scope": "core cases; additional reviewed offline units are separately counted",
            "core_case_count": len(inventory.core_case_ids),
            "offline_exception_case_count": len(exceptions),
            "selected_core_case_ids": [case for case in selected_ids if case not in exceptions],
            "selected_offline_exception_case_ids": [case for case in selected_ids if case in exceptions],
            "selected_case_ids": selected_ids,
            "selected_execution_ids": [item["id"] for item in selected]}


def python_child(target: str) -> int:
    """Run one exact Python selector and report its observed result."""
    import unittest

    if os.environ.get("ACTIVE_TEST_OFFLINE_I12") == "1":
        _guard_offline_test_effects()

    class Result(unittest.TextTestResult):
        subcases = 0

        def addSubTest(self, test, subtest, error):
            self.subcases += 1
            super().addSubTest(test, subtest, error)

    suite = unittest.defaultTestLoader.loadTestsFromName(target)
    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    summary = {"tests_run": result.testsRun, "subcases": result.subcases,
               "skips": len(result.skipped), "expected_failures": len(result.expectedFailures)}
    print("ACTIVE_TEST_RESULT=" + json.dumps(summary, sort_keys=True))
    return 0 if result.wasSuccessful() and result.testsRun == 1 and not result.expectedFailures else 1


def _guard_offline_test_effects() -> None:
    """Reject process and host-network effects in the reviewed offline child."""
    denied = frozenset({
        "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn",
        "os.fork", "os.forkpty", "os.kill", "os.killpg",
        "socket.connect", "socket.bind", "socket.getaddrinfo",
        "socket.gethostbyname", "socket.gethostbyaddr", "socket.sendto",
    })

    def check(event: str, _arguments: tuple) -> None:
        if event in denied:
            raise InventoryError("offline I12 unit cases prohibit this external effect: " + event)

    sys.addaudithook(check)


PYTHON_CHILD = ("import sys; from ci.lib.active_test_inventory import python_child; "
                "raise SystemExit(python_child(sys.argv[1]))")


def execution_command(root: Path, execution: dict[str, Any], race: bool = False
                      ) -> tuple[list[str], Path]:
    """Produce the exact admitted argv without a shell."""
    selector = execution["selector"]
    kind = selector["kind"]
    if kind == "python":
        return [sys.executable, "-c", PYTHON_CHILD, selector["target"]], root
    if kind == "native":
        return ["sh", str(root / selector["script"]), *selector["args"]], root
    pattern = "/".join("^" + re.escape(part) + "$" for part in selector["test"].split("/"))
    command = ["go", "test", "-json", "-mod=readonly", "-count=1", "-run", pattern]
    if race:
        command.append("-race")
    command.append(selector["package"])
    return command, root / selector["module"]


def _python_result(execution: dict[str, Any], text: str, strict_skips: bool) -> dict[str, Any]:
    records = [line.partition("=")[2] for line in text.splitlines()
               if line.startswith("ACTIVE_TEST_RESULT=")]
    if len(records) != 1:
        raise InventoryError("Python child must emit exactly one result record")
    result = json.loads(records[0])
    expected = execution.get("expected_subtests", len(execution["cases"]))
    if (("expected_subtests" in execution or result["subcases"]) and
            result["subcases"] != expected):
        raise InventoryError("observed Python subcases differ from the expanded inventory")
    if strict_skips and result["skips"]:
        raise InventoryError("selected Python execution skipped a required case")
    return result


def _go_result(execution: dict[str, Any], text: str, strict_skips: bool) -> dict[str, Any]:
    events = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
    names = {(event.get("Package"), event["Test"]) for event in events
             if event.get("Action") == "run" and "Test" in event}
    leaves = {(package, name) for package, name in names if not any(
        other_package == package and other_name.startswith(name + "/")
        for other_package, other_name in names)}
    skipped = sum(event.get("Action") == "skip" and "Test" in event for event in events)
    target = execution["selector"]["test"]
    if (len(leaves) != len(execution["cases"]) or
            any(not (name == target or name.startswith(target + "/") or target.startswith(name + "/"))
                for _, name in names)):
        raise InventoryError("observed Go leaf cases differ from the expanded inventory")
    if strict_skips and skipped:
        raise InventoryError("selected Go execution skipped a required case")
    return {"leaf_tests": [{"package": package, "test": name} for package, name in sorted(leaves)],
            "skips": skipped}


def _observed_result(execution: dict[str, Any], text: str, strict_skips: bool) -> dict[str, Any]:
    kind = execution["selector"]["kind"]
    if kind == "python":
        return _python_result(execution, text, strict_skips)
    if kind == "go":
        return _go_result(execution, text, strict_skips)
    return {"native_expansion": "reviewed-source-bound", "cases": len(execution["cases"])}


def validate_output_root(root: Path, output_root: Path) -> Path:
    """Validate an existing invocation-owned external parent before allocating."""
    if not output_root.is_absolute() or ".." in output_root.parts:
        raise InventoryError("test output root must be an existing absolute external directory")
    for component in [*reversed(output_root.parents), output_root]:
        observed = component.lstat()
        if not stat.S_ISDIR(observed.st_mode) or observed.st_uid not in {0, os.geteuid()}:
            raise InventoryError("test output ancestry must contain trusted non-symlink directories")
        public = component != output_root and observed.st_uid == 0 and observed.st_mode & stat.S_ISVTX
        if observed.st_mode & 0o022 and not public:
            raise InventoryError("test output ancestry must not be adversary-writable")
    if output_root == root or root in output_root.parents or output_root.stat().st_uid != os.geteuid():
        raise InventoryError("test output root must be external and invocation-owned")
    return output_root


def _output_directory(root: Path, output_root: Path) -> Path:
    return Path(tempfile.mkdtemp(prefix="active-tests-", dir=validate_output_root(root, output_root)))


def _process_group_exists(identifier: int) -> bool:
    try:
        os.killpg(identifier, 0)
    except ProcessLookupError:
        return False
    return True


def _signal_process_group(identifier: int, selected_signal: int) -> None:
    try:
        os.killpg(identifier, selected_signal)
    except ProcessLookupError:
        pass


def _terminate_process_group(process: subprocess.Popen) -> None:
    _signal_process_group(process.pid, signal.SIGTERM)
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        process.poll()
        if not _process_group_exists(process.pid):
            break
        time.sleep(0.05)
    if _process_group_exists(process.pid):
        _signal_process_group(process.pid, signal.SIGKILL)
    process.wait(timeout=5)


def _termination_requested(selected_signal: int, _frame: Any) -> None:
    raise SystemExit(128 + selected_signal)


def _run_child(command: list[str], working_directory: Path, environment: dict[str, str],
               stream: Any, timeout: float = 600) -> int:
    """Own one process group and reap it on timeout or interruption."""
    previous_termination = signal.signal(signal.SIGTERM, _termination_requested)
    try:
        process = subprocess.Popen(command, cwd=working_directory, env=environment,
                                   stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            returncode = process.wait(timeout=timeout)
        except BaseException as failure:
            try:
                _terminate_process_group(process)
            except (OSError, subprocess.SubprocessError) as cleanup_failure:
                failure.add_note("owned process-group cleanup failed: " + type(cleanup_failure).__name__)
            raise
        if returncode:
            _terminate_process_group(process)
        return returncode
    finally:
        signal.signal(signal.SIGTERM, previous_termination)


def execution_timeout(execution: dict[str, Any]) -> int:
    """Leave bounded provisioning time inside the existing 120-minute host jobs."""
    selector = execution["selector"]
    if selector["kind"] == "native" and selector["script"] in {
            "ci/runtime/lifecycle/run-active-crs-case.sh",
            "ci/runtime/lifecycle/run-active-no-crs-case.sh",
            "ci/runtime/lifecycle/run-connector-stage.sh"}:
        return 6000
    return 600


def run_execution(inventory: Inventory, execution: dict[str, Any], output: Path,
                  race: bool, strict_skips: bool) -> dict[str, Any]:
    """Run one admitted selector and retain its actual terminal result."""
    _recheck_bindings(inventory)
    log = output / (execution["id"] + ".log")
    command, working_directory = execution_command(inventory.root, execution, race)
    environment = dict(os.environ, GOTOOLCHAIN="local", PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    environment["ACTIVE_TEST_EXECUTION"] = execution["id"]
    environment["ACTIVE_TEST_INVENTORY_SHA256"] = inventory.digest
    environment.pop("ACTIVE_TEST_OFFLINE_I12", None)
    if {"offline-i12", "offline-unit"}.intersection(execution["groups"]):
        fixture = _output_directory(inventory.root, output)
        environment.update(I12_TEST_ROOT=str(fixture), CODEX_PROJECT_STATE=str(fixture),
                           I12_NGINX_LEDGER_TEST_ROOT=str(fixture),
                           CODEX_TEST_TMP_ROOT=str(fixture), CODEX_TEMP_ROOT=str(fixture),
                           TMPDIR=str(fixture), RUNNER_TEMP=str(fixture),
                           ACTIVE_TEST_OFFLINE_I12="1")
    with log.open("x", encoding="utf-8") as stream:
        returncode = _run_child(command, working_directory, environment, stream,
                                timeout=execution_timeout(execution))
    text = log.read_text(encoding="utf-8", errors="replace")
    print(text, end="", flush=True)
    if returncode:
        raise InventoryError(f"active execution {execution['id']} failed with exit {returncode}")
    _recheck_bindings(inventory)
    observed = _observed_result(execution, text, strict_skips)
    status = "blocked" if observed.get("skips") else "passed"
    return {"execution_id": execution["id"], "case_ids": [case["id"] for case in execution["cases"]],
            "status": status, "observed": observed, "log": log.name,
            "go_race": race and execution["selector"]["kind"] == "go"}


def execute_selected(inventory: Inventory, selected: tuple[dict[str, Any], ...], output_root: Path,
                     race: bool = False, strict_skips: bool = False) -> dict[str, Any]:
    output = _output_directory(inventory.root, output_root)
    summary = selection_summary(inventory, selected)
    summary["output_directory"] = str(output)
    summary["results"] = []
    destination = output / "summary.json"
    try:
        for execution in selected:
            summary["results"].append(run_execution(inventory, execution, output, race, strict_skips))
    finally:
        destination.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def _default_output_root() -> Path:
    selected = os.environ.get("RUNNER_TEMP") or os.environ.get("TMP_ROOT")
    if not selected:
        raise InventoryError("execution requires --output-root or an existing RUNNER_TEMP/TMP_ROOT")
    return Path(selected)


def canonical_test_id(test: Any, root: Path) -> str | None:
    """Bind a unittest instance to its actual source, including bare discovery imports."""
    if isinstance(test, OfflineInventoryCase):
        return test.id()
    owner = type(test)
    module = sys.modules.get(owner.__module__)
    filename = getattr(module, "__file__", None)
    if not isinstance(filename, str):
        return None
    try:
        source = Path(filename).resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        return None
    if source.suffix != ".py":
        return None
    identifier = test.id()
    prefix = owner.__module__ + "."
    if not isinstance(identifier, str) or not identifier.startswith(prefix):
        return None
    module_name = ".".join(source.with_suffix("").parts)
    return module_name + "." + identifier.removeprefix(prefix)


class OfflineInventoryCase(unittest.TestCase):
    """Keep offline discovery in the same guarded child as direct/CI selection."""

    def __init__(self, inventory: Inventory, execution: dict[str, Any]):
        super().__init__("test_admitted_execution")
        self.inventory = inventory
        self.execution = execution

    def id(self) -> str:
        return self.execution["selector"]["target"]

    def test_admitted_execution(self) -> None:
        execute_selected(self.inventory, (self.execution,), _default_output_root(), strict_skips=True)


def _offline_execution(execution: dict[str, Any]) -> bool:
    return bool({"offline-i12", "offline-unit"}.intersection(execution["groups"]))


def python_discovery_suite(inventory: Inventory, loader: Any):
    """Load core cases normally and defer offline imports to their guarded child."""
    suite = unittest.TestSuite()
    for execution in inventory.executions:
        if execution["selector"]["kind"] != "python":
            continue
        if _offline_execution(execution):
            suite.addTest(OfflineInventoryCase(inventory, execution))
        else:
            suite.addTests(loader.loadTestsFromName(execution["selector"]["target"]))
    return suite


def _suite_cases(suite: Any):
    import unittest

    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _suite_cases(item)
        else:
            yield item


def module_load_tests(_loader: Any, standard_tests: Any, pattern: Any):
    """Filter every Parent module's default discovery through the same admitted inventory."""
    import unittest

    if os.environ.get("ON_DEMAND_TESTS") == "1":
        return standard_tests
    root = Path(__file__).resolve().parents[2]
    inventory = load_inventory(root)
    allowed = {execution["selector"]["target"]: execution for execution in inventory.executions
               if execution["selector"]["kind"] == "python"}
    selected = {}
    for test in _suite_cases(standard_tests):
        if type(test).__module__ == "unittest.loader" and type(test).__name__ == "_FailedTest":
            raise InventoryError("default discovery encountered a test import failure")
        identifier = canonical_test_id(test, root)
        if identifier in allowed:
            execution = allowed[identifier]
            selected.setdefault(identifier, OfflineInventoryCase(inventory, execution)
                                if _offline_execution(execution) else test)
    if pattern is None and not selected:
        raise InventoryError("this test module is archived; explicit ON_DEMAND_TESTS=1 is required")
    return unittest.TestSuite(selected.values())


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--group", action="append", default=[])
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--execution", action="append", default=[])
    parser.add_argument("--module", choices=sorted(GO_MODULES))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--race", action="store_true")
    parser.add_argument("--strict-skips", action="store_true")
    parser.add_argument("--output-root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        inventory = load_inventory(root or Path(__file__).resolve().parents[2], arguments.inventory)
        if (not arguments.check and inventory.path is not None and
                inventory.path.absolute() != inventory.root / INVENTORY_PATH):
            raise InventoryError("alternate inventories are admission-only fixtures; execution requires the canonical inventory")
        selected = select_executions(inventory, tuple(arguments.group), tuple(arguments.case),
                                     arguments.module, tuple(arguments.execution))
        if arguments.check:
            summary = selection_summary(inventory, selected)
        else:
            output_root = arguments.output_root if arguments.output_root is not None else _default_output_root()
            summary = execute_selected(inventory, selected, output_root,
                                       arguments.race, arguments.strict_skips)
        print(json.dumps(summary, indent=2))
        return 0
    except (InventoryError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"ACTIVE_INVENTORY_REJECTED: {exc}", file=sys.stderr)
        return 2
