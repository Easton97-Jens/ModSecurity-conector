#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COMPONENT_KEYS = ("apache_httpd", "nginx", "go_ftw", "albedo")
MARKER_START = "<!-- runtime-components:start -->"
MARKER_END = "<!-- runtime-components:end -->"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def component_inventory(report_dir: Path) -> dict[str, Any]:
    cache_report = read_json(report_dir / "runtime-component-cache.generated.json")
    return {key: cache_report.get(key, {}) for key in COMPONENT_KEYS}


def replace_marked_section(text: str, section: str) -> str:
    if MARKER_START in text and MARKER_END in text:
        prefix = text.split(MARKER_START, 1)[0].rstrip()
        suffix = text.split(MARKER_END, 1)[1].lstrip()
        return f"{prefix}\n\n{section}\n\n{suffix}".rstrip() + "\n"
    return text.rstrip() + "\n\n" + section + "\n"


def runtime_components_markdown(components: dict[str, Any]) -> str:
    apache = components.get("apache_httpd", {})
    nginx = components.get("nginx", {})
    go_ftw = components.get("go_ftw", {})
    albedo = components.get("albedo", {})
    lines = [
        MARKER_START,
        "## Runtime Components",
        "",
        "### Apache httpd",
        f"- Status: `{apache.get('status', '-')}`",
        f"- Blocker: `{apache.get('blocker_reason') or '-'}`",
        f"- Cache path: `{apache.get('cache_path', '-')}`",
        f"- Build path: `{apache.get('build_path', '-')}`",
        f"- apachectl/APACHECTL_BIN: `{apache.get('apachectl_bin', '-')}`",
        f"- Module file: `{apache.get('module_file', '-')}`",
        f"- Missing file: `{apache.get('missing_file') or '-'}`",
        f"- Build component: `{apache.get('build_component') or '-'}`",
        f"- Env variable to set: `{apache.get('env_variable_can_set') or apache.get('env_override') or '-'}`",
        "",
        "### NGINX",
        f"- Status: `{nginx.get('status', '-')}`",
        f"- Blocker: `{nginx.get('blocker_reason') or '-'}`",
        f"- Cache path: `{nginx.get('cache_path', '-')}`",
        f"- Build path: `{nginx.get('build_path', '-')}`",
        f"- MRTS_NATIVE_NGINX_BIN: `{nginx.get('nginx_bin', '-')}`",
        f"- MRTS_NATIVE_NGINX_MODULE_DIR: `{nginx.get('module_dir', '-')}`",
        f"- Module file: `{nginx.get('module_file', '-')}`",
        f"- Missing file: `{nginx.get('missing_file') or '-'}`",
        f"- Build component: `{nginx.get('build_component') or '-'}`",
        f"- Env variable to set: `{nginx.get('env_variable_can_set') or nginx.get('env_override') or '-'}`",
        "",
        "### go-ftw / albedo",
        "| Dependency | Status | Searched paths | Env override | Known source | Known ref | Can build locally | Blocker |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in (go_ftw, albedo):
        searched = "<br>".join(f"`{path}`" for path in item.get("searched_paths", [])) or "-"
        lines.append(
            "| {dep} | {status} | {searched} | `{env}` | `{source}` | `{ref}` | {can_build} | {blocker} |".format(
                dep=item.get("dependency", "-"),
                status=item.get("status", "-"),
                searched=searched,
                env=item.get("env_override", "-"),
                source=item.get("known_source") or "-",
                ref=item.get("known_ref") or "-",
                can_build="yes" if item.get("can_build_locally") else "no",
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.append(MARKER_END)
    return "\n".join(lines)


def update_report_json(path: Path, components: dict[str, Any]) -> None:
    if not path.is_file():
        return
    data = read_json(path)
    if not data:
        return
    data["runtime_components"] = components
    for key, value in components.items():
        data[key] = value
    write_json(path, data)


def update_report_md(path: Path, components: dict[str, Any]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    section = runtime_components_markdown(components)
    path.write_text(replace_marked_section(text, section), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", required=True)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    report_dir = connector_root / "reports/testing/generated"
    components = component_inventory(report_dir)
    for stem in ("mrts-native-full.generated", "full-run-evidence.generated"):
        update_report_json(report_dir / f"{stem}.json", components)
        update_report_md(report_dir / f"{stem}.md", components)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
