#!/usr/bin/env python3
"""Static contract checks for connector-neutral common SDK files."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "common"
CHECK_COMMON_HELPERS = ROOT / "ci" / "check-common-helpers.sh"
MAKEFILE = ROOT / "Makefile"
SEARCH_ROOTS = [COMMON / "include", COMMON / "src"]
FORBIDDEN_INCLUDES = (
    "#include <ngx_",
    "#include \"ngx_",
    "#include <httpd.h>",
    "#include \"httpd.h\"",
    "#include <haproxy",
    "#include \"haproxy",
    "#include <envoy",
    "#include \"envoy",
    "#include <traefik",
    "#include \"traefik",
    "#include <lighttpd",
    "#include \"lighttpd",
)
SERVER_TOKENS = ("nginx", "apache", "haproxy", "envoy", "traefik", "lighttpd")
NON_INTEGRATION_TERMS = ("not integrate", "not imply", "future", "separately", "no connector")


def fail(message: str) -> None:
    print(f"common-sdk-contract: {message}", file=sys.stderr)
    sys.exit(1)


def text_without_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//.*", "", text)


for header in (COMMON / "include" / "msconnector").glob("*.h"):
    text = header.read_text(encoding="utf-8")
    guard = "MSCONNECTOR_" + header.stem.upper() + "_H"
    if f"#ifndef {guard}" not in text or f"#define {guard}" not in text:
        fail(f"missing include guard {guard} in {header.relative_to(ROOT)}")

for source in (COMMON / "src").glob("*.c"):
    text = source.read_text(encoding="utf-8")
    expected = f'#include "msconnector/{source.stem}.h"'
    if expected not in text:
        fail(f"missing matching header include {expected} in {source.relative_to(ROOT)}")

for required_header in (
    "decision.h",
    "error.h",
    "rule_loader.h",
    "modsecurity_engine.h",
    "transaction_id.h",
    "adapter.h",
    "adapter_contract.h",
    "capability_matrix.h",
    "event_jsonl.h",
    "artifact_layout.h",
    "runtime_paths.h",
    "config_parser.h",
    "request_helpers.h",
    "response_helpers.h",
    "rule_merge.h",
    "rule_error.h",
    "rule_event.h",
    "test_result_json.h",
    "connector_manifest.h",
    "runtime_report.h",
    "origin_governance.h",
    "build_contract.h",
    "limits.h",
    "rule_id.h",
    "log_sanitize.h",
):
    if not (COMMON / "include" / "msconnector" / required_header).is_file():
        fail(f"missing common SDK header {required_header}")
    if not (COMMON / "src" / required_header.replace(".h", ".c")).is_file():
        fail(f"missing common SDK source {required_header.replace('.h', '.c')}")


for required_wrapper in (
    "request.hpp",
    "response.hpp",
    "transaction.hpp",
    "status.hpp",
    "capabilities.hpp",
    "origin.hpp",
    "logging.hpp",
):
    wrapper = COMMON / "include" / "msconnector" / required_wrapper
    if not wrapper.is_file():
        fail(f"missing C++ wrapper {required_wrapper}")
    wrapper_text = wrapper.read_text(encoding="utf-8")
    if "namespace msconnector" not in wrapper_text or "#include" not in wrapper_text:
        fail(f"C++ wrapper {required_wrapper} must be lightweight and include the C header")

for required_script in (
    "ci/check-origin-governance.py",
    "ci/check-build-contracts.py",
    "ci/generate-connector-contract-report.py",
):
    if not (ROOT / required_script).is_file():
        fail(f"missing common package script {required_script}")

for required_doc in (
    "docs/generated/connector-contract.md",
    "docs/generated/connector-contract.de.md",
    "docs/generated/origin-governance.md",
    "docs/generated/origin-governance.de.md",
):
    if not (ROOT / required_doc).is_file():
        fail(f"missing generated common package doc {required_doc}")

log_sanitize_source = (ROOT / "common" / "src" / "log_sanitize.c").read_text(encoding="utf-8")
if "redacted body" not in log_sanitize_source or "src;" not in log_sanitize_source:
    fail("body-snippet redaction must not copy payload bytes")

for root in SEARCH_ROOTS:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        uncommented = text_without_comments(text).lower()
        lowered = text.lower()
        for token in FORBIDDEN_INCLUDES:
            if token in lowered:
                fail(f"forbidden connector-specific include {token!r} in {path.relative_to(ROOT)}")
        for token in SERVER_TOKENS:
            if token in uncommented:
                fail(f"server-specific token {token!r} outside comments in {path.relative_to(ROOT)}")
            if token in lowered and not any(term in lowered for term in NON_INTEGRATION_TERMS):
                fail(f"server-specific token {token!r} lacks non-integration context in {path.relative_to(ROOT)}")

helper_text = CHECK_COMMON_HELPERS.read_text(encoding="utf-8")
makefile_text = MAKEFILE.read_text(encoding="utf-8")
combined_check_text = helper_text + "\n" + makefile_text
if "common/src/*.c" not in helper_text:
    fail("check-common-helpers.sh does not compile all common/src/*.c files")
if "-std=c99" in helper_text:
    fail("hardcoded -std=c99 remains in check-common-helpers.sh")
if "MSCONNECTOR_C_STD" not in helper_text or "MSCONNECTOR_CFLAGS" not in helper_text:
    fail("check-common-helpers.sh does not expose configurable common C standard flags")
if "MSCONNECTOR_C_STD ?= c17" not in makefile_text:
    fail("Makefile does not define c17 as the default common C standard")
if "-std=c20" in combined_check_text:
    fail("common C checks must not use -std=c20")
if "-std=c26" in combined_check_text:
    fail("common C checks must not use -std=c26")
if "--profile c23" not in makefile_text or "c2x" not in makefile_text:
    fail("optional c23/c2x common helper check is not wired")
if "--profile c2y" not in makefile_text or "gnu2y" not in makefile_text:
    fail("optional future-C c2y/gnu2y common helper check is not wired")

if "MSCONNECTOR_COMPILER_ID ?=" not in makefile_text:
    fail("Makefile must derive a common smoke compiler id for optional standard probes")
if '--compiler "$(MSCONNECTOR_COMPILER_ID)"' not in makefile_text:
    fail("optional C standard probes must use the same compiler id as the smoke")
if 'check-common-helpers CC="$(MSCONNECTOR_COMPILER_ID)"' not in makefile_text:
    fail("optional C standard smokes must compile with the probed compiler id")


detect_text = (ROOT / "ci" / "detect-c-standard.py").read_text(encoding="utf-8")
if "args.cc" in detect_text or 'parser.add_argument("--cc"' in detect_text:
    fail("detect-c-standard.py must not accept or use raw --cc command paths")
if "shell=True" in detect_text:
    fail("detect-c-standard.py must not use shell=True")
if "[0-9]" in detect_text:
    fail("detect-c-standard.py compiler regex must not use [0-9]")
if detect_text.count('"-std=c17"') > 1:
    fail("detect-c-standard.py duplicates the -std=c17 literal outside its constant")
if detect_text.count('"-std=c2x"') > 1:
    fail("detect-c-standard.py duplicates the -std=c2x literal outside its constant")
if "--compiler" not in detect_text or "COMPILER_ID_PATTERN" not in detect_text or "shutil.which" not in detect_text:
    fail("detect-c-standard.py must expose only a validated compiler-id selector")
if "gcc-\\d+" not in detect_text or "clang-\\d+" not in detect_text:
    fail("detect-c-standard.py must support safe versioned gcc/clang compiler ids")
if detect_text.count("subprocess.run(") != 1 or "def compiler_supports" not in detect_text:
    fail("detect-c-standard.py subprocess.run must appear only in the compiler probe helper")




def count_direct_fields(header_text: str, struct_name: str) -> int:
    match = re.search(
        rf"typedef\s+struct\s+{struct_name}\s*\{{(?P<body>.*?)\}}\s*{struct_name}\s*;",
        header_text,
        flags=re.S,
    )
    if match is None:
        fail(f"common event model is missing {struct_name}")
    body = text_without_comments(match.group("body"))
    return sum(1 for line in body.splitlines() if line.strip().endswith(";"))

def extract_http_status_table_statuses(source_text: str) -> set[int]:
    table_match = re.search(
        r"static\s+const\s+msconnector_http_status_info\s+http_statuses\[\]\s*=\s*\{(?P<body>.*?)\};",
        source_text,
        flags=re.S,
    )
    if table_match is None:
        fail("common/src/http_status.c does not expose a parseable http_statuses table")
    return {
        int(match.group(1))
        for match in re.finditer(r"\{\s*(\d{3})\s*,[^{}]*,\s*1\s*\}", table_match.group("body"))
    }


def extract_generator_statuses(source_text: str) -> set[int]:
    list_match = re.search(
        r"ALLOWED_BLOCK_STATUSES\s*=\s*\((?P<body>.*?)\)",
        source_text,
        flags=re.S,
    )
    if list_match is None:
        fail("ci/generate-block-status-config.py does not expose a parseable ALLOWED_BLOCK_STATUSES tuple")
    return {int(value) for value in re.findall(r"\b(\d{3})\b", list_match.group("body"))}


http_status_source = (ROOT / "common" / "src" / "http_status.c").read_text(encoding="utf-8")
block_status_source = (ROOT / "common" / "src" / "block_statuses.c").read_text(encoding="utf-8")
generator_source = (ROOT / "ci" / "generate-block-status-config.py").read_text(encoding="utf-8")
http_statuses = extract_http_status_table_statuses(http_status_source)
generator_statuses = extract_generator_statuses(generator_source)
if http_statuses != generator_statuses:
    fail(
        "HTTP status metadata and generator ALLOWED_BLOCK_STATUSES drift: "
        f"http_status.c={sorted(http_statuses)} generator={sorted(generator_statuses)}"
    )
if "case 400:" in block_status_source or "case 403:" in block_status_source:
    fail("common/src/block_statuses.c must delegate block status decisions instead of keeping a divergent switch list")
if "msconnector_http_status_is_block_response" not in block_status_source:
    fail("common/src/block_statuses.c does not delegate block status allow checks to HTTP status metadata")


headers_source = (ROOT / "common" / "src" / "headers.c").read_text(encoding="utf-8")
config_source = (ROOT / "common" / "src" / "config.c").read_text(encoding="utf-8")
path_policy_source = (ROOT / "common" / "src" / "path_policy.c").read_text(encoding="utf-8")
if "value_index" not in headers_source or "is_ows" not in headers_source or "header->value[suffix_index] == ';'" not in headers_source:
    fail("Content-Type matching must trim leading OWS and reject garbage after the media type")
if "msconnector_block_status_is_allowed" not in config_source or "validate_block_status_value" not in config_source:
    fail("default_block_status validation must use block-status allowance metadata")
if "merge_remote_rules_pair" not in config_source or "merge_transaction_id_pair" not in config_source:
    fail("config merge must preserve paired remote-rule and transaction-id fields")
if "is_path_separator" not in path_policy_source or "\\" not in path_policy_source:
    fail("path policy must treat backslash as a parent-traversal separator")

if "set-cookie" not in headers_source or "content-length" not in headers_source or "msconnector_headers_parse_content_length" not in headers_source:
    fail("headers.c must contain Set-Cookie and Content-Length duplicate-header policy")

adapter_metadata_source = (ROOT / "common" / "src" / "adapter_metadata.c").read_text(encoding="utf-8")
event_source = (ROOT / "common" / "src" / "event.c").read_text(encoding="utf-8")
if "string_is_nonempty" not in adapter_metadata_source or "imported_path" not in adapter_metadata_source:
    fail("adapter metadata completeness must reject empty required fields")
if "validate_error_status_value" not in config_source or "msconnector_http_status_is_error" not in config_source:
    fail("config validation must reject success/redirect default error and unsupported statuses")
if "format_event_json" not in event_source or "json_bool(was_truncated)" not in event_source:
    fail("event writer must recompute the truncation marker before final JSON output")
for required_doc in (
    "docs/architecture/common-sdk.de.md",
    "docs/connectors/new-connector-contract.md",
    "docs/connectors/new-connector-contract.de.md",
    "docs/generated/common-sdk.md",
    "docs/generated/common-sdk.de.md",
    "docs/generated/directives.md",
    "docs/generated/directives.de.md",
    "docs/generated/capabilities.md",
    "docs/generated/capabilities.de.md",
    "reports/sonar/pr27-issue-reduction.de.md",
):
    if not (ROOT / required_doc).is_file():
        fail(f"missing bilingual/common generated document {required_doc}")
for required_script in (
    "ci/common-harness.sh",
    "ci/port_allocator.py",
    "ci/process_helper.py",
    "ci/generate-common-docs.py",
    "ci/check-adapter-contracts.py",
    "ci/check-capability-truthfulness.py",
):
    if not (ROOT / required_script).is_file():
        fail(f"missing common helper script {required_script}")
if not (ROOT / "config/testing/capability-contract.json").is_file():
    fail("missing capability contract JSON")
event_jsonl_source = (ROOT / "common" / "src" / "event_jsonl.c").read_text(encoding="utf-8")
runtime_paths_source = (ROOT / "common" / "src" / "runtime_paths.c").read_text(encoding="utf-8")
if "msconnector_event_write_json_ex" not in event_jsonl_source or "request_body" in event_jsonl_source or "response_body" in event_jsonl_source:
    fail("event_jsonl writer must use event JSON and avoid body payload fields")
if "msconnector_path_is_absolute" not in runtime_paths_source or "msconnector_path_has_parent_reference" not in runtime_paths_source:
    fail("runtime path join must reject absolute and parent-traversal artifact names")
decision_source = (ROOT / "common" / "src" / "decision.c").read_text(encoding="utf-8")
error_source = (ROOT / "common" / "src" / "error.c").read_text(encoding="utf-8")
rule_loader_source = (ROOT / "common" / "src" / "rule_loader.c").read_text(encoding="utf-8")
engine_source = (ROOT / "common" / "src" / "modsecurity_engine.c").read_text(encoding="utf-8")
transaction_id_source = (ROOT / "common" / "src" / "transaction_id.c").read_text(encoding="utf-8")
if "msconnector_decision_to_event" not in decision_source:
    fail("decision.c must expose decision_to_event integration")
if "msconnector_error_to_event" not in error_source:
    fail("error.c must expose error_to_event integration")
if "backend.add_inline" not in rule_loader_source or "msconnector_rule_load_stats_add_inline" not in rule_loader_source:
    fail("rule_loader.c must use backend callbacks and rule_load_stats")
if "modsecurity/" in engine_source.lower() or "modsecurity.h" in engine_source.lower():
    fail("modsecurity_engine.c must not include libmodsecurity headers directly")
if "ops." not in engine_source or "msconnector_transaction_state_mark_phase" not in engine_source:
    fail("modsecurity_engine.c must use backend ops and mark transaction phases")
if "\\n" not in transaction_id_source and "< 32U" not in transaction_id_source:
    fail("transaction_id.c must reject CR/LF/control characters")
if "expr_eval" not in transaction_id_source:
    fail("transaction_id.c must support callback expression resolution")

event_header = (ROOT / "common" / "include" / "msconnector" / "event.h").read_text(encoding="utf-8")
if count_direct_fields(event_header, "msconnector_event") > 20:
    fail("top-level msconnector_event must not exceed 20 direct fields")
for nested_struct in (
    "msconnector_event_meta",
    "msconnector_event_decision",
    "msconnector_event_http",
    "msconnector_event_request",
    "msconnector_event_flags",
):
    if count_direct_fields(event_header, nested_struct) > 20:
        fail(f"{nested_struct} must not exceed 20 direct fields")
for required_field in (
    "message_id",
    "message",
    "requested_action",
    "actual_action",
    "http_reason_phrase",
    "http_default_message",
    "late_intervention",
    "connection_aborted",
    "truncated",
):
    if required_field not in event_header:
        fail(f"common event model must retain {required_field} metadata")
if "msconnector_event_set_phase4_hard_abort_after_200" not in event_header or "MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200" not in event_source:
    fail("common event model must expose the Phase 4 hard-abort-after-200 helper")
if "body_payload" in event_source or "request_body" in event_source or "response_body" in event_source:
    fail("common event JSON writer must not include request/response body payload fields")
if "event->meta.message_id" not in event_source or "event->decision.requested_action" not in event_source:
    fail("common event JSON writer must use nested event metadata")
if "truncated" not in event_header or "truncated" not in event_source:
    fail("common event JSON writer must expose truncation")
if "msconnector_event_write_json_ex" not in event_source or "return was_truncated ? 0 : 1" not in event_source:
    fail("common event JSON writer must fail success status when truncation is detected")
if "if ((dst_size == 0 || needed >= dst_size) && truncated != 0)" not in event_source:
    fail("common event JSON escaping helper must merge the truncation nested-if condition")
if '{200, "OK", "Request succeeded", MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, 0}' not in http_status_source:
    fail("common HTTP status metadata must include non-blocking 200 OK metadata")

print("common-sdk-contract: pass")
