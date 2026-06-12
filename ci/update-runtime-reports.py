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
DIAG_MARKER_START = "<!-- runtime-diagnostics:start -->"
DIAG_MARKER_END = "<!-- runtime-diagnostics:end -->"
POST_LIBCRYPT_MARKER_START = "<!-- post-libcrypt-native:start -->"
POST_LIBCRYPT_MARKER_END = "<!-- post-libcrypt-native:end -->"


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


def replace_named_section(text: str, section: str, start_marker: str, end_marker: str) -> str:
    if start_marker in text and end_marker in text:
        prefix = text.split(start_marker, 1)[0].rstrip()
        suffix = text.split(end_marker, 1)[1].lstrip()
        return f"{prefix}\n\n{section}\n\n{suffix}".rstrip() + "\n"
    return text.rstrip() + "\n\n" + section + "\n"


def read_text_if_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def collect_case_lines(log_text: str, case_id: str) -> list[str]:
    lines = log_text.splitlines()
    in_case = False
    case_lines: list[str] = []
    for line in lines:
        if f"{case_id}-" in line and "-s" in line:
            in_case = True
            case_lines.append(line)
            continue
        if in_case:
            case_lines.append(line)
            if f"{case_id}-" in line and "-e" in line:
                break
    return case_lines


def collect_actual_ids(case_lines: list[str]) -> list[str]:
    actual_ids: list[str] = []
    for line in case_lines:
        for match in re.findall(r'\[id "([0-9]+)"\]', line):
            if match not in actual_ids:
                actual_ids.append(match)
    return actual_ids


def collect_phase_hits(case_lines: list[str]) -> list[tuple[str, str]]:
    return [
        match
        for match in re.findall(r"\[id \"([0-9]+)\"].*?\[msg \"([^\"]*phase:[0-9][^\"]*)\"\]", "\n".join(case_lines))
    ]


def collect_run_counts(run_text: str) -> dict[str, Any]:
    return {
        "attempted": first_match(r"➕ run ([0-9]+) total tests", run_text) or "-",
        "passed": str(run_text.count("✔ passed")),
        "failed_cases": first_match(r"failed to run: \[(.*?)\]", run_text).replace('"', "") or "-",
    }


def collect_apache_100003_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    apache = components.get("apache_httpd", {})
    build_path = apache.get("build_path")
    if not build_path:
        return {}
    build_root = Path(build_path).resolve().parent
    native_root = build_root / "mrts-native"
    run_log = native_root / "apache2_ubuntu/run.log"
    error_log = native_root / "apache2_ubuntu/stage/infra/log/error.log"
    access_log = native_root / "apache2_ubuntu/stage/infra/log/access.log"
    audit_log = native_root / "apache2_ubuntu/stage/infra/log/modsec_audit.log"
    ftw_yaml = build_root / "mrts/upstream-config-tests/ftw/100003_MRTS_002_ARGS_A-GET.yaml"
    rule_file = build_root / "mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf"
    load_file = native_root / "apache2_ubuntu/stage/infra/mrts.load"
    module_load_file = native_root / "apache2_ubuntu/stage/infra/mods-enabled/security2.load"
    security_conf = native_root / "apache2_ubuntu/stage/infra/mods-enabled/security2.conf"

    run_text = read_text_if_file(run_log)
    if "100003-1 failed" not in run_text:
        return {}

    yaml_text = read_text_if_file(ftw_yaml)
    rule_text = read_text_if_file(rule_file)
    error_text = read_text_if_file(error_log)
    access_text = read_text_if_file(access_log)
    audit_text = read_text_if_file(audit_log)
    load_text = read_text_if_file(load_file)
    module_load_text = read_text_if_file(module_load_file)
    security_text = read_text_if_file(security_conf)

    case_lines = collect_case_lines(error_text, "100003-1")
    actual_ids = collect_actual_ids(case_lines)
    module_path = first_match(r"^LoadModule\s+security3_module\s+(\S*mod_security3\.so)", module_load_text)
    expected_id = first_match(r"expect_ids:\n\s+-\s+([0-9]+)", yaml_text) or "100003"
    method = first_match(r"^\s+method:\s+(\S+)", yaml_text)
    uri = first_match(r"^\s+uri:\s+(.+)$", yaml_text)
    rule_block = first_match(r'(SecRule ARGS "@contains attack" \\\n\s+"id:100003,\\\n\s+phase:4,[\s\S]*?ver:\'MRTS/0\.1\'")', rule_text)
    request_seen = 'POST /?foo=attack HTTP/1.1" 200' in access_text

    return {
        "target": "apache2_ubuntu",
        "case": "100003-1",
        "server_label": "Apache",
        "status": "fail",
        "diagnosis": "Apache/httpd started and reached go-ftw; expected phase 4 rule id 100003 was not logged.",
        "counts": collect_run_counts(run_text),
        "ftw_yaml": str(ftw_yaml),
        "rule_file": str(rule_file),
        "run_log": str(run_log),
        "error_log": str(error_log),
        "access_log": str(access_log),
        "audit_log": str(audit_log),
        "mrts_load": str(load_file),
        "module_conf": str(module_load_file),
        "module_path": module_path,
        "module_loaded": bool(module_path and Path(module_path).is_file()),
        "mrts_load_included": str(rule_file) in load_text and str(load_file) in security_text,
        "method": method or "POST",
        "uri": uri or "/?foo=attack",
        "body": "none",
        "port": "19080",
        "expected_status": "not specified in FTW YAML",
        "actual_status": "HTTP 200 observed in Apache access log" if request_seen else "not printed by go-ftw",
        "expected_result": f"log id {expected_id}",
        "actual_result": "missing expected log id 100003",
        "actual_logged_ids": actual_ids,
        "phase_hits": collect_phase_hits(case_lines),
        "request_reached_server": request_seen,
        "request_reached_modsecurity": bool(actual_ids),
        "request_reached_albedo": "Received default request to /?foo=attack" in run_text,
        "audit_evidence": "empty" if audit_log.is_file() and not audit_text.strip() else ("present" if audit_text else "missing"),
        "rule_excerpt": rule_block,
        "go_ftw_excerpt": "\n".join(line for line in run_text.splitlines() if "100003-1" in line or "failed" in line),
        "recommended_action": "No MRTS definition/result rewrite was made; investigate native phase 4 behavior separately.",
    }


def collect_nginx_100003_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    nginx = components.get("nginx", {})
    build_path = nginx.get("build_path")
    if not build_path:
        return {}
    build_root = Path(build_path).resolve().parent
    native_root = build_root / "mrts-native"
    run_log = native_root / "nginx-pr24/run.log"
    error_log = native_root / "nginx-pr24/stage/infra/log/error.log"
    audit_log = native_root / "nginx-pr24/stage/infra/log/modsec_audit.log"
    ftw_yaml = build_root / "mrts/upstream-config-tests/ftw/100003_MRTS_002_ARGS_A-GET.yaml"
    rule_file = build_root / "mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf"
    load_file = native_root / "nginx-pr24/stage/infra/mrts.load"
    main_conf = native_root / "nginx-pr24/stage/infra/modsecurity/main.conf"
    module_conf = native_root / "nginx-pr24/stage/infra/modules-available/mod-http-modsecurity.conf"

    run_text = read_text_if_file(run_log)
    if "100003-1 failed" not in run_text:
        return {}

    yaml_text = read_text_if_file(ftw_yaml)
    rule_text = read_text_if_file(rule_file)
    error_text = read_text_if_file(error_log)
    audit_text = read_text_if_file(audit_log)
    load_text = read_text_if_file(load_file)
    main_text = read_text_if_file(main_conf)
    module_text = read_text_if_file(module_conf)

    case_lines = collect_case_lines(error_text, "100003-1")
    actual_ids = collect_actual_ids(case_lines)
    phase_hits = collect_phase_hits(case_lines)
    module_path = first_match(r"^load_module\s+([^;]+ngx_http_modsecurity_module\.so);", module_text)
    expected_id = first_match(r"expect_ids:\n\s+-\s+([0-9]+)", yaml_text) or "100003"
    method = first_match(r"^\s+method:\s+(\S+)", yaml_text)
    uri = first_match(r"^\s+uri:\s+(.+)$", yaml_text)
    port = first_match(r"^\s+port:\s+([0-9]+)", yaml_text)
    rule_block = first_match(r'(SecRule ARGS "@contains attack" \\\n\s+"id:100003,\\\n\s+phase:4,[\s\S]*?ver:\'MRTS/0\.1\'")', rule_text)

    return {
        "target": "nginx-pr24",
        "case": "100003-1",
        "server_label": "NGINX",
        "status": "fail",
        "diagnosis": "go-ftw expected phase 4 rule id 100003, but NGINX/ModSecurity logged only earlier phase matches for the request.",
        "counts": collect_run_counts(run_text),
        "ftw_yaml": str(ftw_yaml),
        "rule_file": str(rule_file),
        "run_log": str(run_log),
        "error_log": str(error_log),
        "audit_log": str(audit_log),
        "mrts_load": str(load_file),
        "module_conf": str(module_conf),
        "module_path": module_path,
        "module_loaded": bool(module_path and Path(module_path).is_file()),
        "mrts_load_included": str(rule_file) in load_text and "Include mrts.load" in main_text,
        "method": method or "POST",
        "uri": uri or "/?foo=attack",
        "body": "none",
        "port": port or "19081",
        "expected_status": "not specified in FTW YAML",
        "actual_status": "not printed by go-ftw; backend request was observed",
        "expected_result": f"log id {expected_id}",
        "actual_result": "missing expected log id 100003",
        "actual_logged_ids": actual_ids,
        "phase_hits": phase_hits,
        "request_reached_server": any('request: "POST /?foo=attack HTTP/1.1"' in line for line in case_lines),
        "request_reached_modsecurity": bool(actual_ids),
        "request_reached_albedo": "Received default request to /?foo=attack" in run_text,
        "audit_evidence": "empty" if audit_log.is_file() and not audit_text.strip() else ("present" if audit_text else "missing"),
        "rule_excerpt": rule_block,
        "go_ftw_excerpt": "\n".join(line for line in run_text.splitlines() if "100003-1" in line or "failed" in line),
        "recommended_action": "No MRTS definition/result rewrite was made; investigate NGINX/native phase 4 support separately.",
    }


def collect_runtime_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {}
    apache_diag = collect_apache_100003_diagnostics(components)
    if apache_diag:
        diagnostics["apache_100003_1"] = apache_diag
    nginx_diag = collect_nginx_100003_diagnostics(components)
    if nginx_diag:
        diagnostics["nginx_100003_1"] = nginx_diag
    return diagnostics


def post_libcrypt_native_summary(components: dict[str, Any], diagnostics: dict[str, Any]) -> dict[str, Any]:
    apache = components.get("apache_httpd", {})
    nginx = components.get("nginx", {})
    apache_diag = diagnostics.get("apache_100003_1", {})
    nginx_diag = diagnostics.get("nginx_100003_1", {})
    build_path = apache.get("build_path") or nginx.get("build_path") or ""
    build_root = str(Path(build_path).resolve().parent) if build_path else "-"
    return {
        "build_root": build_root,
        "apachectl_bin": apache.get("apachectl_bin") or "-",
        "apache_module": apache.get("module_file") or "-",
        "nginx_bin": nginx.get("nginx_bin") or "-",
        "nginx_module": nginx.get("module_file") or "-",
        "apache_result": "FAIL" if apache_diag else "-",
        "apache_counts": apache_diag.get("counts", {}),
        "nginx_result": "FAIL" if nginx_diag else "-",
        "nginx_counts": nginx_diag.get("counts", {}),
    }


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
        f"- crypt.h status: `{apache.get('crypt_h_status') or '-'}`",
        f"- crypt.h path: `{apache.get('crypt_h_path') or '-'}`",
        f"- libcrypt status: `{apache.get('libcrypt_status') or '-'}`",
        f"- libcrypt paths: `{', '.join(apache.get('libcrypt_paths', [])) or '-'}`",
        f"- crypt link mode: `{apache.get('crypt_link_mode') or '-'}`",
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


def post_libcrypt_native_markdown(summary: dict[str, Any]) -> str:
    apache_counts = summary.get("apache_counts", {})
    nginx_counts = summary.get("nginx_counts", {})
    lines = [
        POST_LIBCRYPT_MARKER_START,
        "## Post-libcrypt Native Rerun",
        "- Scope: requested native rerun after external `libcrypt-dev` availability; the earlier full-matrix sections in this file remain historical evidence from their original generation time.",
        "- Command: `FRAMEWORK_ROOT=/root/git/ModSecurity-test-Framework BUILD_ROOT=/tmp/modsec-native-after-libcrypt MRTS_NATIVE_TARGETS=\"apache2_ubuntu nginx-pr24\" CONNECTOR_COMPONENT_CACHE=/src/ModSecurity-conector-cache PYTHONDONTWRITEBYTECODE=1 make mrts-native-full-run`",
        f"- BUILD_ROOT: `{summary.get('build_root', '-')}`",
        f"- Apache wrapper: `{summary.get('apachectl_bin', '-')}`",
        f"- Apache module: `{summary.get('apache_module', '-')}`",
        f"- Apache native result: `{summary.get('apache_result', '-')}`; attempted `{apache_counts.get('attempted', '-')}`, passed `{apache_counts.get('passed', '-')}`, failed cases `{apache_counts.get('failed_cases', '-')}`",
        f"- NGINX binary: `{summary.get('nginx_bin', '-')}`",
        f"- NGINX module: `{summary.get('nginx_module', '-')}`",
        f"- NGINX native result: `{summary.get('nginx_result', '-')}`; attempted `{nginx_counts.get('attempted', '-')}`, passed `{nginx_counts.get('passed', '-')}`, failed cases `{nginx_counts.get('failed_cases', '-')}`",
        POST_LIBCRYPT_MARKER_END,
    ]
    return "\n".join(lines)


def diagnostics_markdown(diagnostics: dict[str, Any]) -> str:
    lines = [DIAG_MARKER_START, "## Native Runtime Diagnostics"]
    if not diagnostics:
        lines.extend(["", "- No generated native runtime diagnostics were detected."])
    else:
        for key in ("apache_100003_1", "nginx_100003_1"):
            diag = diagnostics.get(key, {})
            if not diag:
                continue
            label = diag.get("server_label") or diag.get("target", "-")
            counts = diag.get("counts", {})
            lines.extend(
                [
                    "",
                    f"### {label} 100003-1",
                    f"- Status: `{diag.get('status', '-')}`",
                    f"- Target: `{diag.get('target', '-')}`",
                    f"- Run counts: attempted `{counts.get('attempted', '-')}`, passed `{counts.get('passed', '-')}`, failed cases `{counts.get('failed_cases', '-')}`",
                    f"- Diagnosis: {diag.get('diagnosis', '-')}",
                    f"- Generated YAML: `{diag.get('ftw_yaml', '-')}`",
                    f"- Generated rule file: `{diag.get('rule_file', '-')}`",
                    f"- Request: `{diag.get('method', '-')} {diag.get('uri', '-')} HTTP/1.1` on port `{diag.get('port', '-')}`; body `{diag.get('body', '-')}`",
                    f"- Expected status/result: `{diag.get('expected_status', '-')}` / `{diag.get('expected_result', '-')}`",
                    f"- Actual status/result: `{diag.get('actual_status', '-')}` / `{diag.get('actual_result', '-')}`",
                    f"- Actual logged IDs: `{', '.join(diag.get('actual_logged_ids', [])) or '-'}`",
                    f"- Module loaded: `{diag.get('module_loaded')}` from `{diag.get('module_path') or '-'}`",
                    f"- mrts.load included: `{diag.get('mrts_load_included')}`",
                    f"- Request reached {label}/ModSecurity/Albedo: `{diag.get('request_reached_server')}` / `{diag.get('request_reached_modsecurity')}` / `{diag.get('request_reached_albedo')}`",
                    f"- Audit/debug evidence: audit log `{diag.get('audit_evidence', '-')}`, error log `{diag.get('error_log', '-')}`, go-ftw log `{diag.get('run_log', '-')}`",
                    f"- Action: {diag.get('recommended_action', '-')}",
                ]
            )
    lines.append(DIAG_MARKER_END)
    return "\n".join(lines)


def update_report_json(path: Path, components: dict[str, Any], diagnostics: dict[str, Any]) -> None:
    if not path.is_file():
        return
    data = read_json(path)
    if not data:
        return
    data["runtime_components"] = components
    data["runtime_diagnostics"] = diagnostics
    if path.name == "full-run-evidence.generated.json":
        data["post_libcrypt_native_rerun"] = post_libcrypt_native_summary(components, diagnostics)
    for key, value in components.items():
        data[key] = value
    write_json(path, data)


def update_report_md(path: Path, components: dict[str, Any], diagnostics: dict[str, Any]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if path.name == "mrts-native-full.generated.md":
        text = normalize_native_remediation(text, components)
    if path.name == "full-run-evidence.generated.md":
        text = replace_named_section(
            text,
            post_libcrypt_native_markdown(post_libcrypt_native_summary(components, diagnostics)),
            POST_LIBCRYPT_MARKER_START,
            POST_LIBCRYPT_MARKER_END,
        )
    section = runtime_components_markdown(components)
    text = replace_marked_section(text, section)
    text = replace_named_section(text, diagnostics_markdown(diagnostics), DIAG_MARKER_START, DIAG_MARKER_END)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", required=True)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    report_dir = connector_root / "reports/testing/generated"
    components = component_inventory(report_dir)
    diagnostics = collect_runtime_diagnostics(components)
    update_report_json(report_dir / "runtime-component-cache.generated.json", components, diagnostics)
    update_report_md(report_dir / "runtime-component-cache.generated.md", components, diagnostics)
    for stem in ("mrts-native-full.generated", "full-run-evidence.generated"):
        update_report_json(report_dir / f"{stem}.json", components, diagnostics)
        update_report_md(report_dir / f"{stem}.md", components, diagnostics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
