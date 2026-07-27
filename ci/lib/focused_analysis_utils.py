#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from report_path_safety import read_json_file, read_text_file, safe_existing_file, write_json_file


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Any) -> dict[str, Any]:
    return read_json_file(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_json_file(path, data)


def read_text(path: Path | None) -> str:
    return read_text_file(path)


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value)]


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


def action_parts(action_text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in action_text:
        if char in {"'", '"'}:
            quote = None if quote == char else char if quote is None else quote
        if char == "," and quote is None:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            continue
        current.append(char)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts
