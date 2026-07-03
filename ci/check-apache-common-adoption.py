#!/usr/bin/env python3
"""Enforce Apache/Common SDK structure-level adoption without runtime claims."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APACHE = ROOT / "connectors/apache"
SRC = APACHE / "src"

checks: list[tuple[bool, str]] = []

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

config_h = read(SRC / "mod_security3.h")
config_c = read(SRC / "msc_config.c")
filters_c = read(SRC / "msc_filters.c")
mapper_h = read(SRC / "msc_apache_mapper.h") if (SRC / "msc_apache_mapper.h").exists() else ""
mapper_c = read(SRC / "msc_apache_mapper.c") if (SRC / "msc_apache_mapper.c").exists() else ""
apache_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in SRC.glob("*.c")) + "\n" + "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in SRC.glob("*.h"))
docs_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in [APACHE / "README.md", APACHE / "README.de.md", APACHE / "docs/architecture.md", ROOT / "reports/apache-common-adoption.md"] if p.exists())

checks.append(("msconnector_config common_config" in config_h, "Apache config embeds msconnector_config common_config"))
checks.append(("msconnector_config_init(&cnf->common_config)" in config_c, "Apache config init uses msconnector_config_init"))
checks.append(("msconnector_config_merge(&cnf_new->common_config" in config_c, "Apache config merge uses msconnector_config_merge"))
checks.append(("msconnector_config_validate(&cnf_new->common_config" in config_c, "Apache config validation path uses msconnector_config_validate"))
checks.append(("msconnector_parse_bool" in config_c, "Apache bool parsing uses Common parser"))
checks.append(("msconnector_parse_phase4_mode" in config_c, "Apache phase4 parsing uses Common parser"))
checks.append(("msconnector_parse_size" in config_c, "Apache size parsing uses Common parser"))
checks.append(("MSCONNECTOR_DIRECTIVE_" in config_c and "msconnector_directive_adapter_find" in config_c, "Apache directives reference Common directive names and adapter lookup"))
checks.append(("int msc_apache_map_request" in mapper_h + mapper_c and "request_rec *r" in mapper_h + mapper_c, "Apache request_rec mapper is present"))
checks.append(("msconnector_request_mapper_contract" in mapper_h + mapper_c and "msconnector_request_mapper_validate_output" in mapper_c, "Request mapper uses Common contract validation"))
checks.append(("int msc_apache_map_response" in mapper_h + mapper_c and "msconnector_response_mapper_contract" in mapper_h + mapper_c, "Apache response mapper is present"))
checks.append(("msconnector_response_mapper_validate_output" in mapper_c, "Response mapper uses Common contract validation"))
checks.append(("copy_apr_response_headers" in mapper_c and "err_headers_out" in mapper_c and "r->content_type" in mapper_c, "Response mapper includes err_headers_out and synthesized Content-Type"))
checks.append(("msconnector_headers_host" in mapper_c, "Apache mapper uses Common header helper"))
checks.append(("msconnector_event_write_jsonl_line" in filters_c and "msconnector_event_init" in filters_c, "Apache event JSONL uses Common event primitives"))
checks.append(("event.decision.status = MSCONNECTOR_STATUS_BLOCKED" in filters_c, "Phase4 intervention events set a non-OK status"))
checks.append(("event.meta.event = \"phase4_intervention\"" in filters_c, "Phase4 event key remains report-compatible"))
checks.append(("event serialization truncated" in filters_c and "event serialization failed" in filters_c and "apr_file_puts" in filters_c, "Truncated Phase4 events use a bounded fallback line"))
checks.append(("body_truncated" in filters_c and "json_truncated" in filters_c and "event.flags.truncated = msr->body_truncated" not in filters_c, "Response body truncation is separate from JSON serialization truncation"))
checks.append(("event.flags.headers_sent = msr->response_committed" in filters_c and "event.flags.body_started = msr->response_committed" in filters_c and "event.flags.late_intervention = msr->response_committed" in filters_c, "Buffered Phase4 denials are not marked sent before commit"))
checks.append(("strcmp(reason, \"buffered_before_commit\")" in filters_c and "event.http.visible_http_status = msr->last_intervention_status" in filters_c, "Pre-commit deny events report the deny status as visible"))
checks.append(("msconnector_rule_id_extract_from_message" in filters_c, "Apache rule-id extraction uses Common helper"))
checks.append(("apache_json_escape" not in apache_text, "Duplicate Apache JSON escape helper is removed"))
checks.append(("apache_phase4_rule_id" not in apache_text, "Duplicate Apache rule-id helper is removed"))
checks.append(("char *end = NULL" not in config_c and "strtoul" not in config_c, "Duplicate Apache size parser is removed"))
checks.append(("else if (cnf_new->common_config.transaction_id != NULL)" in config_c and "cnf_new->transaction_id_expr = NULL" in config_c, "Child static transaction IDs override parent expressions"))
checks.append(("MSCONNECTOR_COMMON_SOURCES" in (ROOT / "connectors/apache/build/apxs-wrapper.in").read_text(encoding="utf-8") and "common/src" in (ROOT / "connectors/apache/build/apxs-wrapper.in").read_text(encoding="utf-8"), "Apache APXS wrapper links Common SDK sources"))
for field in ["msc_state", "use_error_log;", "const char *transaction_id;", "int phase4_mode;", "const char *phase4_log_path;", "apr_size_t phase4_body_limit;"]:
    checks.append((field not in config_h, f"Duplicate config field removed: {field}"))

for forbidden in ["production-ready", "production ready", "runtime-verified", "full-matrix ready", "CRS PASS"]:
    checks.append((forbidden.lower() not in docs_text.lower(), f"No new forbidden claim: {forbidden}"))

ok = True
for passed, message in checks:
    if passed:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")
        ok = False

if not ok:
    sys.exit(1)
print("apache-common-adoption: structure-level Common SDK adoption checks passed")
