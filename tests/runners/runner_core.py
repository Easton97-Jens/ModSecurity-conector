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


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _load_minimal_yaml(path: Path) -> Mapping[str, Any]:
    """Parse the documented minimal case schema without external dependencies."""

    lines = path.read_text(encoding="utf-8").splitlines()

    def parse_mapping(index: int, indent: int) -> tuple[dict[str, Any], int]:
        parsed: dict[str, Any] = {}
        while index < len(lines):
            line = lines[index]
            if not line.strip() or line.lstrip().startswith("#"):
                index += 1
                continue
            current_indent = _indent_of(line)
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValueError(f"unexpected indentation in {path}: {line}")
            stripped = line.strip()
            if ":" not in stripped:
                raise ValueError(f"expected key/value line in {path}: {line}")
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value == "|":
                block_lines: list[str] = []
                while index < len(lines):
                    block_line = lines[index]
                    if block_line.strip() and _indent_of(block_line) <= current_indent:
                        break
                    block_lines.append(block_line)
                    index += 1
                parsed[key] = _dedent_block(block_lines)
                continue
            if raw_value:
                parsed[key] = _parse_scalar(raw_value)
                continue
            nested, index = parse_mapping(index, current_indent + 2)
            parsed[key] = nested
        return parsed, index

    case, final_index = parse_mapping(0, 0)
    while final_index < len(lines):
        trailing = lines[final_index]
        if trailing.strip() and not trailing.lstrip().startswith("#"):
            raise ValueError(f"unexpected trailing content in {path}: {trailing}")
        final_index += 1
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
    if str(request.get("method", "")).upper() not in {"GET", "POST"}:
        raise ValueError(f"case supports only GET or POST request.method{where}")
    if not str(request.get("path", "")).strip():
        raise ValueError(f"case requires request.path{where}")
    headers = request.get("headers", {})
    if headers is not None and not isinstance(headers, Mapping):
        raise ValueError(f"case request.headers must be a mapping{where}")
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


def request_headers(case: Mapping[str, Any]) -> Mapping[str, Any]:
    request = case["request"]
    headers = request.get("headers", {})
    if headers is None:
        return {}
    if not isinstance(headers, Mapping):
        raise ValueError("request.headers must be a mapping")
    return headers


def request_body(case: Mapping[str, Any]) -> str:
    request = case["request"]
    if "body" not in request or request.get("body") is None:
        return ""
    return str(request["body"])


def write_headers_file(case: Mapping[str, Any], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for name, value in request_headers(case).items():
        lines.append(f"{name}: {value}\n")
    output.write_text("".join(lines), encoding="utf-8")


def write_body_file(case: Mapping[str, Any], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(request_body(case), encoding="utf-8")


def write_shell_env(
    case: Mapping[str, Any],
    path: str | Path,
    headers_file: str | Path | None = None,
    body_file: str | Path | None = None,
) -> None:
    request = case["request"]
    expect = case["expect"]
    body = request_body(case)
    values = {
        "CASE_NAME": case["name"],
        "REQUEST_METHOD": str(request["method"]).upper(),
        "REQUEST_PATH": request["path"],
        "REQUEST_HAS_BODY": 1 if body else 0,
        "REQUEST_HEADERS_FILE": headers_file or "",
        "REQUEST_BODY_FILE": body_file or "",
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
