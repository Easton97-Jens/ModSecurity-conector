> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T12:42:40Z`
> Verified run id: `2026-06-16-614c804`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `062e5ef84bcb3e385ac7b5335129eb578fe30833`
> Framework SHA: `3e7a08507b7fdb48565047470a3164a872fb15b5`
> Input status: `complete`

# Generated Connector Gap Summary

**Language:** English | [Deutsch](connector-gap-summary.generated.de.md)

| case_id | path | status | classification | tags | variables | source/provenance | notes |
|---|---|---|---|---|---|---|---|
| audit_log_message_presence_connector_gap | `tests/cases/audit-log/audit_log_message_presence_connector_gap.yaml` | imported | active | connector-gap | ARGS:a | unknown | - |
| audit_log_rule_id_presence_runtime_difference | `tests/cases/audit-log/audit_log_rule_id_presence_runtime_difference.yaml` | imported | active | runtime-difference | ARGS:a | unknown | - |
| duplicate_cookie_name_runtime_difference | `tests/cases/audit-log/duplicate_cookie_name_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_COOKIES_NAMES | unknown | - |
| parser_json_partial_body_connector_gap | `tests/cases/audit-log/parser_json_partial_body_connector_gap.yaml` | imported | active | connector-gap | REQUEST_BODY | unknown | - |
| json_duplicate_keys_runtime_difference | `tests/cases/body/json/json_duplicate_keys_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_BODY | unknown | - |
| request_body_json_invalid_runtime_difference | `tests/cases/body/json/request_body_json_invalid_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_BODY | unknown | - |
| multipart_empty_filename_connector_gap | `tests/cases/body/multipart/multipart_empty_filename_connector_gap.yaml` | imported | active | connector-gap | MULTIPART_FILENAME | unknown | - |
| multipart_encoded_filename_runtime_difference | `tests/cases/body/multipart/multipart_encoded_filename_runtime_difference.yaml` | imported | active | runtime-difference | MULTIPART_FILENAME | unknown | - |
| xml_namespace_edge_connector_gap | `tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml` | imported | active | connector-gap | REQUEST_HEADERS:Content-Type, XML:/* | unknown | - |
| xml_request_body_malformed_connector_gap | `tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml` | imported | active | connector-gap | REQUEST_HEADERS:Content-Type, XML | unknown | - |
| v3_args_names_duplicate_query_connector_gap | `tests/cases/future-gap/v3_args_names_duplicate_query_connector_gap.yaml` | imported | active | connector-gap | ARGS_NAMES | unknown | - |
| v3_request_cookies_names_case_runtime_difference | `tests/cases/request/cookies/v3_request_cookies_names_case_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_COOKIES_NAMES | unknown | - |
| v3_request_headers_names_duplicate_connector_gap | `tests/cases/request/headers/v3_request_headers_names_duplicate_connector_gap.yaml` | imported | active | connector-gap | REQUEST_HEADERS_NAMES | unknown | - |
| v3_request_headers_names_lowercase_runtime_difference | `tests/cases/request/headers/v3_request_headers_names_lowercase_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_HEADERS_NAMES | unknown | - |
| edge_plus_vs_space_runtime_difference | `tests/cases/request/uri/edge_plus_vs_space_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_URI | unknown | - |
| unicode_double_encoded_uri_runtime_difference | `tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml` | imported | active | runtime-difference | REQUEST_URI | unknown | - |
| phase4_auditlog_outbound_message_connector_gap | `tests/cases/response/body/phase4_auditlog_outbound_message_connector_gap.yaml` | imported | active | connector-gap | RESPONSE_BODY | unknown | - |
| phase4_auditlog_outbound_rule_id_runtime_difference | `tests/cases/response/body/phase4_auditlog_outbound_rule_id_runtime_difference.yaml` | imported | active | runtime-difference | RESPONSE_BODY | unknown | - |
| phase4_response_body_chunk_assumption_connector_gap | `tests/cases/response/body/phase4_response_body_chunk_assumption_connector_gap.yaml` | imported | active | connector-gap | RESPONSE_BODY | unknown | - |
| phase4_response_body_unicode_runtime_difference | `tests/cases/response/body/phase4_response_body_unicode_runtime_difference.yaml` | imported | active | runtime-difference | RESPONSE_BODY | unknown | - |
| phase3_response_headers_duplicate_value_runtime_difference | `tests/cases/response/headers/phase3_response_headers_duplicate_value_runtime_difference.yaml` | imported | active | runtime-difference | RESPONSE_HEADERS:Set-Cookie | unknown | - |
| phase3_response_headers_mixed_case_connector_gap | `tests/cases/response/headers/phase3_response_headers_mixed_case_connector_gap.yaml` | imported | active | connector-gap | RESPONSE_HEADERS:content-type | unknown | - |
| phase3_response_headers_multi_value_connector_gap | `tests/cases/response/headers/phase3_response_headers_multi_value_connector_gap.yaml` | imported | active | connector-gap | RESPONSE_HEADERS:Set-Cookie | unknown | - |
| sqli_like_quote_encoding_runtime_difference | `tests/cases/security/sql/sqli_like_quote_encoding_runtime_difference.yaml` | imported | active | runtime-difference | ARGS:q | unknown | - |
| request_body_limit_exceeded | `tests/cases/security-data-flow/body-limits/request_body_limit_exceeded.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| response_body_truncation_event | `tests/cases/security-data-flow/body-limits/response_body_truncation_event.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| decision_jsonl_no_body_payload | `tests/cases/security-data-flow/events/decision_jsonl_no_body_payload.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| event_jsonl_no_body_payload | `tests/cases/security-data-flow/events/event_jsonl_no_body_payload.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| integrity_event_hash_chain_tamper_detected | `tests/cases/security-data-flow/events/integrity_event_hash_chain_tamper_detected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| integrity_event_hash_chain_valid | `tests/cases/security-data-flow/events/integrity_event_hash_chain_valid.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| conflicting_content_length_rejected | `tests/cases/security-data-flow/headers/conflicting_content_length_rejected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| header_count_limit_exceeded | `tests/cases/security-data-flow/headers/header_count_limit_exceeded.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| header_value_limit_exceeded | `tests/cases/security-data-flow/headers/header_value_limit_exceeded.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| log_control_chars_sanitized | `tests/cases/security-data-flow/log-safety/log_control_chars_sanitized.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| log_secret_like_payload_redacted | `tests/cases/security-data-flow/log-safety/log_secret_like_payload_redacted.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| duplicate_mutating_phase_rejected | `tests/cases/security-data-flow/phase-order/duplicate_mutating_phase_rejected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| phase_skip_rejected | `tests/cases/security-data-flow/phase-order/phase_skip_rejected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| transaction_id_control_char_rejected | `tests/cases/security-data-flow/transaction-id/transaction_id_control_char_rejected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| transaction_id_too_long_rejected | `tests/cases/security-data-flow/transaction-id/transaction_id_too_long_rejected.yaml` | connector-gap | active | connector-gap | - | unknown | - |
| tests/cases/connector-specific/nginx/nginx_redirect_phase1_302.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX redirect behavior is not yet proven against Apache. |
| tests/cases/connector-specific/nginx/nginx_tx_scoring_absolute_block.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX TX scoring import is not yet proven against Apache. |
| tests/cases/connector-specific/nginx/nginx_tx_scoring_iterative_block.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX TX scoring import is not yet proven against Apache. |
| tests/cases/connector-specific/nginx/nginx_phase4_content_type_out_of_scope.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX-specific phase-4 log-only probe observed PASS in the latest local NGINX source-built smoke after the harness permission fix; this is connector-specific runtime evidence and not RESPONSE_BODY promotion. |
| tests/cases/connector-specific/nginx/nginx_phase4_minimal_log_only.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX-specific phase-4 minimal log-only probe observed PASS in the latest local NGINX source-built smoke after the harness permission fix; this is connector-specific runtime evidence and not RESPONSE_BODY promotion. |
| tests/cases/connector-specific/nginx/nginx_phase4_safe_log_only.yaml | `config/testing/import-status.json` | connector_specific | - | - | unknown | NGINX-specific phase-4 safe log-only probe observed PASS in the latest local NGINX source-built smoke after the harness permission fix; this is connector-specific runtime evidence and not RESPONSE_BODY promotion. |
| ModSecurity-apache/tests/regression/rule/10-xml.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-apache/tests/regression/rule/10-xml.t | XML parser cases require explicit fixture/schema support before active import. |
| ModSecurity-apache/tests/regression/misc/00-multipart-parser.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-apache/tests/regression/misc/00-multipart-parser.t | Multipart parser error and file collection branches exceed the current minimal multipart smoke. |
| ModSecurity-nginx/tests/nginx-tests-cvt.pl | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-nginx/tests/nginx-tests-cvt.pl | Converter tooling is build-runtime support, not a portable rule case. |
| ModSecurity_V2/tests/tfn/urlDecode.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity_V2/tests/tfn/urlDecode.t | Full-byte, NUL, and invalid-encoding urlDecode branches are mapped only; active smoke imports only source-confirmed text-safe Test+Case -> Test Case. |
| ModSecurity_V2/tests/tfn/htmlEntityDecode.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity_V2/tests/tfn/htmlEntityDecode.t | NUL, nbsp, non-ASCII, and invalid entity branches are mapped only; active smoke imports only the text-safe &lt;&gt; -> <> fragment. |
| ModSecurity_V2/tests/op/pm.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity_V2/tests/op/pm.t | Long phrase-list and no-match branches are mapped only; active smoke imports the source-confirmed param abc/input abcdefghi match. |
| ModSecurity_V2/tests/op/containsWord.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity_V2/tests/op/containsWord.t | Negative word-boundary branches are mapped only; active smoke imports the source-confirmed param abc/input abc def ghi match. |
| ModSecurity-nginx PR #377 tests/modsecurity-phase4-invalid-config.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-nginx PR #377 tests/modsecurity-phase4-invalid-config.t | Invalid config tests require config-test expected-failure assertions rather than HTTP smokes. |
| ModSecurity-nginx PR #377 tests/modsecurity-phase4-regression.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-nginx PR #377 tests/modsecurity-phase4-regression.t | Large-response phase-4 regression needs dedicated large fixture/log-leak coverage before active import. |
| ModSecurity-nginx PR #377 tests/modsecurity-response-body.t | `config/testing/import-status.json` | mapped_only | - | - | ModSecurity-nginx PR #377 tests/modsecurity-response-body.t | Response-body blocking remains non-promoted/mapped-only and is not promoted without stable real HTTP blocking semantics. |
| ModSecurity-nginx/tests/modsecurity-request-body-h2.t | `config/testing/import-status.json` | blocked | - | - | ModSecurity-nginx/tests/modsecurity-request-body-h2.t | HTTP/2 is outside the current HTTP/1.1 smoke harness. |
| ModSecurity-nginx/tests/modsecurity-h2.t | `config/testing/import-status.json` | blocked | - | - | ModSecurity-nginx/tests/modsecurity-h2.t | HTTP/2 is outside the current HTTP/1.1 smoke harness. |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-16-614c804` | present |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `d3017f038a44a5f5596e36e3482f92cd93ce6f2173bb958da98cddc05884cd8f` | `2026-06-16-614c804` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
