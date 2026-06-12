#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


COMPONENT_KEYS = ("apache_httpd", "nginx", "go_ftw", "albedo", "expat")
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


def normalize_native_remediation(text: str, components: dict[str, Any]) -> str:
    go_ftw = components.get("go_ftw", {})
    albedo = components.get("albedo", {})
    if go_ftw.get("status") in {"present", "built"}:
        text = re.sub(
            r"\n- nginx-pr24: `go-ftw` missing;[^\n]*",
            "\n- nginx-pr24: go-ftw is present; native execution reached go-ftw and failed during test execution.",
            text,
        )
        text = re.sub(
            r"\n- apache2_ubuntu: `go-ftw` missing;[^\n]*",
            "",
            text,
        )
    if albedo.get("status") in {"present", "built"}:
        text = re.sub(
            r"\n- nginx-pr24: `albedo` missing;[^\n]*",
            "",
            text,
        )
        text = re.sub(
            r"\n- apache2_ubuntu: `albedo` missing;[^\n]*",
            "",
            text,
        )
    return text


def runtime_components_markdown(components: dict[str, Any]) -> str:
    apache = components.get("apache_httpd", {})
    nginx = components.get("nginx", {})
    go_ftw = components.get("go_ftw", {})
    albedo = components.get("albedo", {})
    expat = components.get("expat", {})
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
        f"- Expat source: `{apache.get('expat_source') or '-'}`",
        f"- Expat release tag: `{apache.get('expat_release_tag') or '-'}`",
        f"- CPPFLAGS: `{apache.get('cppflags') or '-'}`",
        f"- LDFLAGS: `{apache.get('ldflags') or '-'}`",
        f"- LIBS: `{apache.get('libs') or '-'}`",
        f"- PKG_CONFIG_PATH: `{apache.get('pkg_config_path') or '-'}`",
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
        "### Expat",
        f"- Status: `{expat.get('status', '-')}`",
        f"- Blocker: `{expat.get('blocker_reason') or '-'}`",
        f"- Source: `{expat.get('source', '-')}`",
        f"- Release tag: `{expat.get('release_tag') or expat.get('expected_ref') or '-'}`",
        f"- Actual head: `{expat.get('actual_head') or '-'}`",
        f"- Prefix: `{expat.get('prefix') or '-'}`",
        f"- expat.h: `{expat.get('expat_h') or '-'}`",
        f"- lib dir: `{expat.get('lib_dir') or '-'}`",
        f"- Recursive submodules: `{expat.get('recursive_submodule_status') or '-'}`",
        "",
        "### go-ftw / albedo",
        "| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for item in (go_ftw, albedo):
        lines.append(
            "| {dep} | {status} | `{binary}` | `{env}` | `{source}` | `{ref}` | `{head}` | `{subs}` | {note} | {blocker} |".format(
                dep=item.get("dependency", "-"),
                status=item.get("status", "-"),
                binary=item.get("binary") or item.get("path") or "-",
                env=item.get("env_override", "-"),
                source=item.get("known_source") or "-",
                ref=item.get("release_tag") or item.get("known_ref") or "-",
                head=item.get("actual_head") or "-",
                subs=item.get("recursive_submodule_status") or "-",
                note=item.get("release_tag_deviation_note") or "-",
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
    if path.name == "mrts-native-full.generated.md":
        text = normalize_native_remediation(text, components)
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
