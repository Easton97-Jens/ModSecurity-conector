"""Minimal shared runner core for connector tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex
from typing import Any, Iterable, Mapping

from adapter_interface import ConnectorAdapter


@dataclass
class RunnerResult:
    response: Any
    artifacts: Mapping[str, Any]
    passed: bool
    errors: tuple[str, ...]


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def _dedent_block(lines: Iterable[str]) -> str:
    collected = list(lines)
    indents = [
        len(line) - len(line.lstrip(" "))
        for line in collected
        if line.strip()
    ]
    if not indents:
        return ""
    margin = min(indents)
    return "\n".join(line[margin:] for line in collected).rstrip() + "\n"


def _load_yaml_with_pyyaml(path: Path) -> Mapping[str, Any] | None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return None
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, Mapping):
        raise ValueError(f"case file must contain a mapping: {path}")
    return loaded


def _load_minimal_yaml(path: Path) -> Mapping[str, Any]:
    """Parse the documented minimal case schema without external dependencies."""

    lines = path.read_text(encoding="utf-8").splitlines()
    case: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" "):
            raise ValueError(f"unexpected indented top-level line in {path}: {line}")
        if ":" not in line:
            raise ValueError(f"expected key/value line in {path}: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value == "|":
            block_lines: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line.startswith(" "):
                    break
                block_lines.append(next_line)
                index += 1
            case[key] = _dedent_block(block_lines)
            continue
        if raw_value:
            case[key] = _parse_scalar(raw_value)
            continue

        nested: dict[str, Any] = {}
        while index < len(lines):
            next_line = lines[index]
            if not next_line.strip() or next_line.lstrip().startswith("#"):
                index += 1
                continue
            if not next_line.startswith(" "):
                break
            index += 1
            nested_line = next_line.strip()
            if ":" not in nested_line:
                raise ValueError(f"expected nested key/value line in {path}: {next_line}")
            nested_key, nested_value = nested_line.split(":", 1)
            nested[nested_key.strip()] = _parse_scalar(nested_value)
        case[key] = nested
    return case


def load_case(path: str | Path) -> Mapping[str, Any]:
    case_path = Path(path)
    loaded = _load_yaml_with_pyyaml(case_path)
    case = dict(loaded if loaded is not None else _load_minimal_yaml(case_path))
    validate_case(case, case_path)
    return case


def validate_case(case: Mapping[str, Any], path: Path | None = None) -> None:
    where = f" in {path}" if path is not None else ""
    if not str(case.get("name", "")).strip():
        raise ValueError(f"case requires name{where}")
    if not str(case.get("rules", "")).strip():
        raise ValueError(f"case requires rules{where}")
    request = case.get("request")
    if not isinstance(request, Mapping):
        raise ValueError(f"case requires request mapping{where}")
    if not str(request.get("method", "")).strip():
        raise ValueError(f"case requires request.method{where}")
    if not str(request.get("path", "")).strip():
        raise ValueError(f"case requires request.path{where}")
    expect = case.get("expect")
    if not isinstance(expect, Mapping):
        raise ValueError(f"case requires expect mapping{where}")
    status = expect.get("status")
    if not isinstance(status, int):
        raise ValueError(f"case requires integer expect.status{where}")


def write_rules_file(case: Mapping[str, Any], path: str | Path) -> None:
    rules = str(case["rules"])
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rules if rules.endswith("\n") else f"{rules}\n", encoding="utf-8")


def write_shell_env(case: Mapping[str, Any], path: str | Path) -> None:
    request = case["request"]
    expect = case["expect"]
    values = {
        "CASE_NAME": case["name"],
        "REQUEST_METHOD": request["method"],
        "REQUEST_PATH": request["path"],
        "EXPECT_STATUS": expect["status"],
        "EXPECT_INTERVENTION": expect.get("intervention", ""),
        "EXPECT_RULE_ID": expect.get("rule_id", ""),
    }
    lines = ["# Generated from common test case. Do not edit.\n"]
    for key, value in values.items():
        lines.append(f"{key}={shlex.quote(str(value))}\n")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(lines), encoding="utf-8")


def response_status(response: Any) -> int | None:
    if isinstance(response, int):
        return response
    if isinstance(response, Mapping):
        status = response.get("status")
        return status if isinstance(status, int) else None
    status = getattr(response, "status", None)
    return status if isinstance(status, int) else None


def assert_case_response(case: Mapping[str, Any], response: Any) -> tuple[str, ...]:
    expect = case["expect"]
    expected_status = expect["status"]
    actual_status = response_status(response)
    if actual_status != expected_status:
        return (f"expected HTTP {expected_status}, observed {actual_status}",)
    return ()


class RunnerCore:
    """Minimal orchestration around a connector adapter."""

    def __init__(self, adapter: ConnectorAdapter) -> None:
        self.adapter = adapter

    def run_case(self, case: Mapping[str, Any]) -> RunnerResult:
        validate_case(case)
        self.adapter.prepare()
        try:
            self.adapter.apply_config(case.get("config", {}))
            self.adapter.apply_rules(str(case.get("rules", "")))
            self.adapter.start()
            response = self.adapter.send_request(case.get("request", {}))
            artifacts = self.adapter.collect_artifacts()
            errors = assert_case_response(case, response)
            return RunnerResult(
                response=response,
                artifacts=artifacts,
                passed=not errors,
                errors=errors,
            )
        finally:
            self.adapter.stop()
            self.adapter.cleanup()
