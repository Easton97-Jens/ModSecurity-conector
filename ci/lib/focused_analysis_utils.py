#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from generated_report_utils import utc_now
from report_path_safety import read_json_file as read_json
from report_path_safety import read_text_file as read_text
from report_path_safety import safe_existing_file
from report_path_safety import write_json_file as write_json


def as_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return [] if value in (None, "") else [str(value)]
    return [str(item) for item in value if str(item).strip()]


def refresh_connector_queue_totals(data: dict[str, Any]) -> None:
    entries = [entry for entry in data.get("entries", []) if isinstance(entry, dict)]
    non_pass = [entry for entry in entries if entry.get("runtime_status") != "PASS"]
    priority_counts = Counter(str(entry.get("priority") or "-") for entry in non_pass)
    totals = data.setdefault("totals", {})
    totals["entries"] = len(entries)
    totals["failures"] = sum(1 for entry in entries if entry.get("runtime_status") == "FAIL")
    totals["priority"] = dict(sorted(priority_counts.items()))


def import_script(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def sanitize_path(value: Any, connector_root: Path, framework_root: Path) -> str:
    text = str(value or "")
    if not text:
        return "-"
    path = safe_existing_file(text)
    if path is None:
        leaf = text.replace("\\", "/").rstrip("/").split("/")[-1] or "-"
        return f"<runtime-artifact>/{leaf}"
    for root, prefix in ((connector_root, "connector"), (framework_root, "framework")):
        try:
            return f"{prefix}:{path.resolve().relative_to(root.resolve())}"
        except (OSError, ValueError):
            continue
    return f"<runtime-artifact>/{path.name}"


def _next_quote(quote: str | None, char: str) -> str | None:
    if char not in {"'", '"'}:
        return quote
    if quote is None:
        return char
    return None if quote == char else quote


def _append_action_part(parts: list[str], characters: list[str]) -> None:
    part = "".join(characters).strip()
    if part:
        parts.append(part)


def action_parts(action_text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in action_text:
        quote = _next_quote(quote, char)
        if char == "," and quote is None:
            _append_action_part(parts, current)
            current.clear()
        else:
            current.append(char)
    _append_action_part(parts, current)
    return parts
