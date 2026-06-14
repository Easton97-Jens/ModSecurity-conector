#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SAFE_ROOTS: set[Path] = set()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def add_safe_roots(*roots: Path | str | None) -> None:
    for root in roots:
        if root is None:
            continue
        root_text = str(root)
        if not root_text or "\0" in root_text:
            continue
        try:
            SAFE_ROOTS.add(Path(root_text).expanduser().resolve(strict=False))
        except OSError:
            continue


def add_full_matrix_roots(full_matrix: dict[str, Any]) -> None:
    for key in ("build_root", "log_root"):
        value = full_matrix.get(key)
        if value:
            add_safe_roots(str(value))
    manifest = full_matrix.get("manifest")
    if manifest:
        add_safe_roots(Path(str(manifest)).parent)
    for run in full_matrix.get("runs", []):
        if not isinstance(run, dict):
            continue
        for key in ("log_path", "runtime_summary_path"):
            value = run.get(key)
            if value:
                add_safe_roots(Path(str(value)).parent)


def add_report_roots(report_dir: Path) -> None:
    add_safe_roots(report_dir)
    matrix_path = safe_existing_file(report_dir / "full-runtime-matrix.generated.json")
    if matrix_path is None:
        return
    matrix = read_json_file(matrix_path)
    if isinstance(matrix, dict):
        add_full_matrix_roots(matrix)


def safe_path(path: Path | str | None, *, must_exist: bool) -> Path | None:
    if path is None:
        return None
    path_text = str(path)
    if not path_text or "\0" in path_text:
        return None
    try:
        resolved = Path(path_text).expanduser().resolve(strict=False)
    except OSError:
        return None
    if SAFE_ROOTS and not any(_is_relative_to(resolved, root) for root in SAFE_ROOTS):
        return None
    if must_exist and not resolved.is_file():
        return None
    return resolved


def safe_existing_file(path: Path | str | None) -> Path | None:
    return safe_path(path, must_exist=True)


def read_json_file(path: Path | str | None) -> dict[str, Any]:
    resolved = safe_existing_file(path)
    if resolved is None:
        return {}
    try:
        loaded = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def read_text_file(path: Path | str | None) -> str:
    resolved = safe_existing_file(path)
    if resolved is None:
        return ""
    try:
        return resolved.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def write_json_file(path: Path | str, value: dict[str, Any]) -> None:
    resolved = safe_path(path, must_exist=False)
    if resolved is None:
        raise ValueError(f"unsafe output path: {path}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text_file(path: Path | str, text: str) -> None:
    resolved = safe_path(path, must_exist=False)
    if resolved is None:
        raise ValueError(f"unsafe output path: {path}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(text, encoding="utf-8")
