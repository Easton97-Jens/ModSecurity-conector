#!/usr/bin/env python3
"""Enforce Apache/Common SDK structure-level adoption without runtime claims."""
from pathlib import Path
import re
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
APACHE = ROOT / "connectors/apache"
SRC = APACHE / "src"

checks: list[tuple[bool, str]] = []

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

config_h = read(SRC / "mod_security3.h")
config_c = read(SRC / "msc_config.c")
filters_c = read(SRC / "msc_filters.c")
module_c = read(SRC / "mod_security3.c")
utils_c = read(SRC / "msc_utils.c")
mapper_h = read(SRC / "msc_apache_mapper.h") if (SRC / "msc_apache_mapper.h").exists() else ""
mapper_c = read(SRC / "msc_apache_mapper.c") if (SRC / "msc_apache_mapper.c").exists() else ""
apache_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in SRC.glob("*.c")) + "\n" + "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in SRC.glob("*.h"))
docs_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in [APACHE / "README.md", APACHE / "README.de.md", ROOT / "docs/connectors/apache.md", ROOT / "reports/audits/architecture-and-evidence.md"] if p.exists())


def source_section(text: str, start: str, end: str) -> str:
    """Return one intentional C source region, or an empty string if absent.

    The Apache event writer is shared by the phase-3 and phase-4 wrappers.
    Keeping these checks scoped to their respective functions prevents a
    similarly named token elsewhere in the file from satisfying the adoption
    contract accidentally.
    """
    begin = text.find(start)
    if begin < 0:
        return ""
    finish = text.find(end, begin + len(start))
    if finish < 0:
        return ""
    return text[begin:finish]


intervention_event_helper = source_section(
    filters_c,
    "static void apache_log_intervention_event",
    "static void apache_phase4_log_event",
)
phase4_event_wrapper = source_section(
    filters_c,
    "static void apache_phase4_log_event",
    "static void apache_phase3_log_event",
)
phase3_event_wrapper = source_section(
    filters_c,
    "static void apache_phase3_log_event",
    "static apr_status_t apache_phase4_append_bucket",
)

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
checks.append(("event.decision.status = MSCONNECTOR_STATUS_BLOCKED" in intervention_event_helper, "Apache P3/P4 intervention events set a non-OK status"))
checks.append((
    "event.meta.event = event_name" in intervention_event_helper
    and "\"phase4_intervention\"" in phase4_event_wrapper
    and "MSCONNECTOR_PHASE_RESPONSE_BODY" in phase4_event_wrapper
    and "\"phase3_intervention\"" in phase3_event_wrapper
    and "MSCONNECTOR_PHASE_RESPONSE_HEADERS" in phase3_event_wrapper
    and "\"response_headers_before_commit\"" in phase3_event_wrapper
    and "original_status, 0" in phase3_event_wrapper,
    "Apache P3 and P4 wrappers retain distinct event names, phases, and pre-commit P3 status context",
))
checks.append((
    "phase == MSCONNECTOR_PHASE_RESPONSE_BODY" in intervention_event_helper
    and "MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200" in intervention_event_helper
    and "MSCONN_EVENT_PHASE4_LATE_INTERVENTION" in intervention_event_helper
    and "MSCONN_EVENT_RESPONSE_BLOCKED" in intervention_event_helper
    and "msconnector_event_default_level(event.meta.message_id)" in intervention_event_helper
    and "msconnector_event_default_message(event.meta.message_id)" in intervention_event_helper,
    "Apache P3/P4 events select canonical message IDs and safe default messages by phase and action",
))
checks.append((
    "event serialization truncated" in intervention_event_helper
    and "event serialization failed" in intervention_event_helper
    and "apr_file_puts" in intervention_event_helper,
    "Apache P3/P4 events use bounded serialization fallback lines",
))
checks.append(("body_truncated" in filters_c and "json_truncated" in filters_c and "event.flags.truncated = msr->body_truncated" not in filters_c, "Response body truncation is separate from JSON serialization truncation"))
checks.append((
    "event.http.original_http_status = original_status" in intervention_event_helper
    and "event.http.visible_http_status = msr->last_intervention_status" in intervention_event_helper
    and "event.flags.late_intervention = response_committed" in intervention_event_helper
    and "event.flags.headers_sent = response_committed" in intervention_event_helper
    and "event.flags.body_started = phase == MSCONNECTOR_PHASE_RESPONSE_BODY" in intervention_event_helper
    and "response_committed;" in intervention_event_helper
    and "msr != NULL ? msr->response_committed : 0" in phase4_event_wrapper
    and "original_status, 0" in phase3_event_wrapper,
    "Apache P3/P4 events preserve original and visible status while deriving commit flags from the actual phase",
))
checks.append(("msconnector_late_intervention_policy_init" in filters_c and "msconnector_late_intervention_resolve" in filters_c and "msconnector_late_intervention_action_name" in filters_c, "Apache Phase4 handling uses the Common late-intervention policy"))
checks.append(("strcmp(actual, \"deny\")" in filters_c and "event.http.visible_http_status = msr->last_intervention_status" in filters_c and "response_not_committed" in filters_c, "Pre-commit deny events report the deny status as visible"))
checks.append((
    "apr_bucket_brigade *response_brigade;" in config_h
    and "response_body_scope_decided" not in config_h
    and "ap_save_brigade(f, &msr->response_brigade, &bb_in, r->pool)" in filters_c
    and "apache_phase4_release_response_brigade" in filters_c
    and "apache_phase4_normalize_response_brigade" in filters_c
    and "APR_BUCKET_IS_FLUSH(bucket)" in filters_c
    and "bucket->length == 0" in filters_c
    and "No later\n         * bucket belongs to this response" in filters_c
    and "msc_discard_response_brigade(msr);" in filters_c
    and "msc_discard_response_brigade(msr);" in utils_c
    and "MSCONNECTOR_BODY_LIMIT_ACTION_REJECT" in filters_c
    and "apache_phase4_in_scope" not in filters_c
    and "SecResponseBodyMimeType selection" in filters_c
    and "plan.append_size) != 1" in filters_c
    and "msc_process_response_body(msr->t) != 1" in filters_c
    and "r->bytes_sent > 0" in filters_c
    and "response_phase4_eos_released" in filters_c
    and "missing saved response brigade" in filters_c
    and "response_phase4_gate_failed" in filters_c
    and "r->connection->aborted = 1" in filters_c
    and "phase4_terminal_guard_filter" in filters_c
    and "apache_send_precommit_terminal_error" in filters_c
    and "msc_discard_response_brigade(msr);" in filters_c
    and "MSC_PHASE4_TERMINAL_OUTPUT_EMITTING" in filters_c
    and "MSC_PHASE4_TERMINAL_OUTPUT_SEALED" in filters_c
    and 'ap_register_output_filter("MODSECURITY_PHASE4_GUARD"' in module_c
    and 'ap_add_output_filter("MODSECURITY_PHASE4_GUARD"' in module_c
    and 'ap_add_output_filter("MODSECURITY_OUT", msr, r,' in module_c
    and "mandatory Phase 4 content filter; aborting request" in module_c
    and "ap_bucket_eoc_create" not in filters_c
    and "ap_flush_conn(r->connection)" not in filters_c
    and "if (!eos_seen)\n    {\n        return APR_SUCCESS;" in filters_c,
    "Apache Phase4 sets aside every response through EOS, treats C API failures as fail-closed, uses downstream-safe commit evidence, and seals terminal request output",
))
checks.append(("msc_finalize_request_body" in filters_c and "request_body_processed" in filters_c and "APR_BUCKET_REMOVE(pbktIn)" in filters_c, "Apache request chunks are borrowed and phase 2 finalizes once at EOS"))
input_filter_c = filters_c.split("apr_status_t input_filter", 1)[1].split("static const char *apache_response_content_type", 1)[0]
checks.append((input_filter_c.count("send_input_error_bucket") == 3 and "send_error_bucket(msr, f" not in input_filter_c, "Apache input-filter errors use the input-specific output-chain bridge"))
checks.append(("return pass_error_bucket(f, status, f->r->output_filters);" in utils_c and "return ap_pass_brigade(destination, brigade);" in utils_c, "Apache input-error bridge propagates the output-chain filter result"))
checks.append(("msc_process_request_body(msr->t)" not in module_c, "Apache does not finalize Phase 2 before the input filter reaches EOS"))
checks.append(("ap_request_has_body(r)" in module_c and "msc_finalize_request_body(msr, r)" in module_c, "Apache completes Phase 2 for a known empty request body"))
checks.append(("ap_discard_request_body(r)" in filters_c and "apache_finish_unread_request_body" in filters_c and "return APR_ECONNABORTED" in filters_c, "Apache drains an unread request body through the streaming input filter or aborts before Phase 3 when EOS is unavailable"))
checks.append(("wanted = msr->last_intervention_status" in filters_c and "\"redirect\" : \"deny\"" in filters_c, "Apache retains redirect as requested action"))
checks.append((
    "failed to open intervention log" in intervention_event_helper
    and "failed to write intervention log" in intervention_event_helper
    and "failed to write truncated intervention log" in intervention_event_helper
    and "failed to write failed intervention log" in intervention_event_helper
    and "failed to close intervention log" in intervention_event_helper
    and "apr_file_puts" in intervention_event_helper
    and "apr_file_close" in intervention_event_helper,
    "Apache reports open, write, fallback-write, and close failures for shared P3/P4 event logging",
))
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
