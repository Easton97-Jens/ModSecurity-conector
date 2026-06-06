Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Overview

## Summary
- Total cases: **141**
- Verified/pass count (`runtime_verified=true`): **0**
- XFAIL count: **80**
- Pending runtime verification count: **91**
- Connector-gap count: **11**
- Runtime-difference count: **13**
- Future/experimental count: **17**
- RESPONSE_BODY cases: **24** (still **not verified/promoted**)
- Mapped-only import inventory entries: **10**

## Coverage By Variable / Collection
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 20 |
| `ARGS:q` | 18 |
| `REQUEST_BODY` | 10 |
| `ARGS_NAMES` | 7 |
| `REQUEST_URI` | 7 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `ARGS:a` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `XML` | 4 |
| `ARGS:param1` | 4 |
| `ARGS` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `ARGS:probe` | 4 |
| `MULTIPART_FILENAME` | 3 |
| `ARGS:chain_a` | 3 |
| `ARGS:chain_b` | 3 |
| `FILES_NAMES` | 2 |
| `TX:SCORE` | 2 |
| `REQUEST_COOKIES:USER_TOKEN` | 2 |

## Coverage By Phase
| Phase | Count |
|---|---:|
| 1 | 36 |
| 2 | 74 |
| 3 | 12 |
| 4 | 20 |

## Coverage By Status
| Status | Count |
|---|---:|
| active | 8 |
| imported | 53 |
| xfail | 80 |

## Coverage By Scope
| Scope | Count |
|---|---:|
| common | 134 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Runtime Matrix Status
- Default runtime-executable YAML cases: **61**
- Force-all runtime-executable YAML cases: **141**
- Apache attempted YAML cases from default summary: **133**
- NGINX attempted YAML cases from default summary: **140**
- HAProxy attempted YAML cases from default summary: **55**
- HAProxy attempted YAML cases from force-all summary: **133**
| Status | Apache | NGINX | HAProxy |
|---|---:|---:|---:|
| PASS | 53 | 56 | 54 |
| RESPONSE_BODY_PASS_THROUGH | 1 | 4 | 1 |
| XFAIL_PASS | 16 | 16 | 0 |
| XFAIL_FAIL | 20 | 21 | 0 |
| PENDING_FAIL | 1 | 1 | 0 |
| FUTURE_PASS | 6 | 6 | 0 |
| FUTURE_RESPONSE_BODY_PASS_THROUGH | 1 | 1 | 0 |
| FUTURE_FAIL | 10 | 10 | 0 |
| CONNECTOR_GAP_PASS | 4 | 5 | 0 |
| CONNECTOR_GAP_FAIL | 7 | 6 | 0 |
| RUNTIME_DIFFERENCE_PASS | 6 | 6 | 0 |
| RUNTIME_DIFFERENCE_FAIL | 8 | 8 | 0 |
| NOT_EXECUTABLE | 8 | 1 | 86 |
| MAPPED_ONLY | 10 | 10 | 10 |
- Details: `reports/testing/generated/runtime-matrix.generated.md`
- HAProxy per-case results: `reports/testing/generated/haproxy-runtime-results.generated.md`

## Latest Local Runtime Validation Snapshot
- Snapshot: **2026-06-06** (2026-06-06 22:19:59 CEST)
- Git: branch `integrate-new-connectors-local`, commit `1a09900`
- BUILD_ROOT: `/src/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Runtime matrix snapshot generated from local Apache, NGINX, and HAProxy summary JSON files when present.
- Per-case PASS/FAIL/BLOCKED/XFAIL values are runtime evidence for this local run only.
- No xfail/pending YAML case is promoted by this snapshot.
- RESPONSE_BODY remains non-verified/non-promoted, including pass-through response-body probes.
- Runtime-passing RESPONSE_BODY cases are marked non-promotable pass-through evidence.
- Mapped-only import inventory entries remain visible but are not executed runtime cases.
- make smoke-all is not implied by separate Apache/NGINX runtime matrix runs.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | Repository lint checks passed |
| make generate-test-matrix | PASS | Generated coverage docs refreshed from current metadata |
| make check-test-matrix | FAIL | Exited 2 in this uncommitted working tree because generated reports differ from HEAD after the HAProxy matrix updates |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile modules/ModSecurity-test-Framework/tests/normalizers/*.py modules/ModSecurity-test-Framework/tests/runners/*.py modules/ModSecurity-test-Framework/ci/*.py | PASS | Framework Python files compiled through the connector module path |
| sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | POSIX shell syntax check passed for connector integration shell scripts |
| bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | Bash syntax check passed for connector integration shell scripts |
| git diff --check | PASS | No whitespace errors reported |
| diff -u /tmp/pre-connector.diff /tmp/post-connector.diff | PASS | Connector source diff snapshot is unchanged; no new connector source changes were introduced |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | BLOCKED | Non-zero because connectors/apache/src/mod_security3.c had a pre-existing unrelated local change before this fix; the pre/post connector diff snapshot is unchanged |
| git ls-files .venv | PASS | No tracked .venv files |

## Readiness / Fetch Status
| Command | Status | Details |
|---|---|---|
| make fetch-deps | NOT_RUN | Not rerun during the framework-module migration; runtime-matrix-all used the configured local source tree and build output location |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity readiness remains diagnostic only and is not required for source-build smokes |
| make runtime-matrix-all | PASS | Force-all matrix orchestration completed and recorded Apache/NGINX per-case evidence; expected runtime FAILs remain evidence and are not PASS promotions |

## Default Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | XFAIL | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| apache | FORCE_ALL_CASES=1 REFRESH=1 make smoke-apache | FAIL | 2 | 133 | 87 | 46 | 0 | unknown | 0 | /src/ModSecurity-conector-build/results/apache-summary.json |
| nginx | FORCE_ALL_CASES=1 REFRESH=1 make smoke-nginx | FAIL | 2 | 140 | 94 | 46 | 0 | unknown | 0 | /src/ModSecurity-conector-build/results/nginx-summary.json |
| haproxy | make smoke-haproxy | PASS | 0 | 55 | 55 | 0 | 0 | 0 | 0 | /src/ModSecurity-conector-build/results/haproxy-summary.json |
| all | REFRESH=1 make smoke-all | NOT_RUN | not_run | 0 | unknown | unknown | unknown | unknown | unknown | not available |

## Force-All Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | XFAIL | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| apache | FORCE_ALL_CASES=1 REFRESH=1 make smoke-apache | NOT_AVAILABLE | not_run | 0 | unknown | unknown | unknown | unknown | unknown | /src/ModSecurity-conector-build/results/force-all/apache-summary.json |
| nginx | FORCE_ALL_CASES=1 REFRESH=1 make smoke-nginx | NOT_AVAILABLE | not_run | 0 | unknown | unknown | unknown | unknown | unknown | /src/ModSecurity-conector-build/results/force-all/nginx-summary.json |
| haproxy | FORCE_ALL_CASES=1 make smoke-haproxy | FAIL | 2 | 133 | 104 | 23 | 0 | 6 | 0 | /src/ModSecurity-conector-build/results/force-all/haproxy-summary.json |

## Connector Runtime Availability
| Connector | Status | Build | Per-case results | Attempted cases | Summary evidence | Note |
|---|---|---|---|---:|---|---|
| Apache | FAIL | unknown | available | 133 | /src/ModSecurity-conector-build/results/apache-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only and do not promote YAML xfail/pending status. |
| NGINX | FAIL | unknown | available | 140 | /src/ModSecurity-conector-build/results/nginx-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only and do not promote YAML xfail/pending status. |
| HAProxy | PASS | unknown | available | 55 | /src/ModSecurity-conector-build/results/haproxy-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only and do not promote YAML xfail/pending status. |

## Runtime FAIL Details

### Apache FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=duplicate_args_encoded_separator_edge; status=fail; expected=403; actual=200 |
| duplicate_header_case_normalization_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=duplicate_header_case_normalization_gap; status=fail; expected=403; actual=200 |
| edge_semicolon_query_args_names | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=edge_semicolon_query_args_names; status=fail; expected=403; actual=200 |
| files_empty_part_future_compatibility | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=files_empty_part_future_compatibility; status=fail; expected=403; actual=None |
| files_names_mixed_case_filename_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=files_names_mixed_case_filename_gap; status=fail; expected=403; actual=200 |
| json_empty_body_future_compatibility | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=json_empty_body_future_compatibility; status=fail; expected=403; actual=None |
| multipart_duplicate_field_names_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=multipart_duplicate_field_names_gap; status=fail; expected=403; actual=200 |
| multipart_empty_filename_connector_gap | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=multipart_empty_filename_connector_gap; status=fail; expected=403; actual=None |
| parser_xml_partial_body_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=parser_xml_partial_body_future_target; status=fail; expected=403; actual=200 |
| phase1_vs_phase2_request_body_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase1_vs_phase2_request_body_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_content_type_charset_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_content_type_charset_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_duplicate_value_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_duplicate_value_runtime_difference; status=fail; expected=403; actual=200 |
| phase3_response_headers_encoded_value_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_encoded_value_future_target; status=fail; expected=403; actual=200 |
| phase3_response_headers_location_encoded_runtime_diff | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_location_encoded_runtime_diff; status=fail; expected=403; actual=200 |
| phase3_response_headers_mixed_case_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_mixed_case_connector_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_multi_value_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_multi_value_connector_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_server_presence_pending | 200 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_server_presence_pending; status=fail; expected=200; actual=None |
| phase3_response_headers_set_cookie_multi_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase3_response_headers_set_cookie_multi_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_escaped_value_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_auditlog_outbound_escaped_value_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_matched_var_future | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_auditlog_outbound_matched_var_future; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_message_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_auditlog_outbound_message_connector_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_multiline_section_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_auditlog_outbound_multiline_section_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_rule_id_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_auditlog_outbound_rule_id_runtime_difference; status=fail; expected=403; actual=200 |
| phase4_response_body_buffering_order_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_buffering_order_future_target; status=fail; expected=403; actual=200 |
| phase4_response_body_chunk_assumption_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_chunk_assumption_connector_gap; status=fail; expected=403; actual=200 |
| phase4_response_body_compressed_assumption_experimental | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_compressed_assumption_experimental; status=fail; expected=403; actual=200 |
| phase4_response_body_empty_future_target | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_empty_future_target; status=fail; expected=403; actual=None |
| phase4_response_body_html_entity_decode_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_html_entity_decode_gap; status=fail; expected=403; actual=200 |
| phase4_response_body_html_text_normalization_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_html_text_normalization_probe; status=fail; expected=403; actual=200 |
| phase4_response_body_unicode_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=phase4_response_body_unicode_runtime_difference; status=fail; expected=403; actual=200 |
| pr70_phase4_response_body_audit_xfail | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=pr70_phase4_response_body_audit_xfail; status=fail; expected=403; actual=200 |
| response_body_basic_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=response_body_basic_block; status=fail; expected=403; actual=200 |
| response_headers_multi_value_runtime_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=response_headers_multi_value_runtime_gap; status=fail; expected=403; actual=200 |
| sqli_like_keyword_spacing_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=sqli_like_keyword_spacing_probe; status=fail; expected=403; actual=200 |
| sqli_like_quote_encoding_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=sqli_like_quote_encoding_runtime_difference; status=fail; expected=403; actual=200 |
| tfn_chain_lowercase_trim_pass_through | 200 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=tfn_chain_lowercase_trim_pass_through; status=fail; expected=200; actual=0 |
| unicode_double_encoded_uri_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=unicode_double_encoded_uri_runtime_difference; status=fail; expected=403; actual=200 |
| unicode_whitespace_normalization_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=unicode_whitespace_normalization_gap; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=v2_transformation_url_decode_invalid_sequence_mapped_candidate; status=fail; expected=403; actual=None |
| v3_request_cookies_names_case_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=v3_request_cookies_names_case_runtime_difference; status=fail; expected=403; actual=200 |
| v3_request_headers_names_lowercase_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=v3_request_headers_names_lowercase_runtime_difference; status=fail; expected=403; actual=200 |
| xml_deep_nesting_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=xml_deep_nesting_future_target; status=fail; expected=403; actual=200 |
| xml_namespace_edge_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=xml_namespace_edge_connector_gap; status=fail; expected=403; actual=200 |
| xml_request_body_malformed_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=xml_request_body_malformed_connector_gap; status=fail; expected=403; actual=200 |
| xss_like_encoded_angles_normalization_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=xss_like_encoded_angles_normalization_probe; status=fail; expected=403; actual=200 |
| xss_like_mixed_case_script_token_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/apache-summary.json; case=xss_like_mixed_case_script_token_gap; status=fail; expected=403; actual=200 |

### NGINX FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| duplicate_args_encoded_separator_edge | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=duplicate_args_encoded_separator_edge; status=fail; expected=403; actual=200 |
| duplicate_header_case_normalization_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=duplicate_header_case_normalization_gap; status=fail; expected=403; actual=200 |
| edge_semicolon_query_args_names | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=edge_semicolon_query_args_names; status=fail; expected=403; actual=200 |
| files_empty_part_future_compatibility | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=files_empty_part_future_compatibility; status=fail; expected=403; actual=None |
| files_names_mixed_case_filename_gap | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=files_names_mixed_case_filename_gap; status=fail; expected=403; actual=405 |
| json_empty_body_future_compatibility | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=json_empty_body_future_compatibility; status=fail; expected=403; actual=None |
| multipart_duplicate_field_names_gap | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=multipart_duplicate_field_names_gap; status=fail; expected=403; actual=405 |
| multipart_empty_filename_connector_gap | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=multipart_empty_filename_connector_gap; status=fail; expected=403; actual=None |
| nginx_phase4_strict_connection_abort | 403 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=nginx_phase4_strict_connection_abort; status=fail; expected=403; actual=0 |
| parser_xml_partial_body_future_target | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=parser_xml_partial_body_future_target; status=fail; expected=403; actual=405 |
| phase1_vs_phase2_request_body_gap | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase1_vs_phase2_request_body_gap; status=fail; expected=403; actual=405 |
| phase3_response_headers_content_type_charset_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_content_type_charset_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_duplicate_value_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_duplicate_value_runtime_difference; status=fail; expected=403; actual=200 |
| phase3_response_headers_encoded_value_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_encoded_value_future_target; status=fail; expected=403; actual=200 |
| phase3_response_headers_location_encoded_runtime_diff | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_location_encoded_runtime_diff; status=fail; expected=403; actual=200 |
| phase3_response_headers_multi_value_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_multi_value_connector_gap; status=fail; expected=403; actual=200 |
| phase3_response_headers_server_presence_pending | 200 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_server_presence_pending; status=fail; expected=200; actual=None |
| phase3_response_headers_set_cookie_multi_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase3_response_headers_set_cookie_multi_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_escaped_value_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_auditlog_outbound_escaped_value_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_matched_var_future | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_auditlog_outbound_matched_var_future; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_message_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_auditlog_outbound_message_connector_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_multiline_section_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_auditlog_outbound_multiline_section_gap; status=fail; expected=403; actual=200 |
| phase4_auditlog_outbound_rule_id_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_auditlog_outbound_rule_id_runtime_difference; status=fail; expected=403; actual=200 |
| phase4_response_body_buffering_order_future_target | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_buffering_order_future_target; status=fail; expected=403; actual=200 |
| phase4_response_body_chunk_assumption_connector_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_chunk_assumption_connector_gap; status=fail; expected=403; actual=200 |
| phase4_response_body_compressed_assumption_experimental | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_compressed_assumption_experimental; status=fail; expected=403; actual=200 |
| phase4_response_body_empty_future_target | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_empty_future_target; status=fail; expected=403; actual=None |
| phase4_response_body_html_entity_decode_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_html_entity_decode_gap; status=fail; expected=403; actual=200 |
| phase4_response_body_html_text_normalization_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_html_text_normalization_probe; status=fail; expected=403; actual=200 |
| phase4_response_body_unicode_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=phase4_response_body_unicode_runtime_difference; status=fail; expected=403; actual=200 |
| pr70_phase4_response_body_audit_xfail | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=pr70_phase4_response_body_audit_xfail; status=fail; expected=403; actual=200 |
| response_body_basic_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=response_body_basic_block; status=fail; expected=403; actual=200 |
| response_headers_multi_value_runtime_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=response_headers_multi_value_runtime_gap; status=fail; expected=403; actual=200 |
| sqli_like_keyword_spacing_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=sqli_like_keyword_spacing_probe; status=fail; expected=403; actual=200 |
| sqli_like_quote_encoding_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=sqli_like_quote_encoding_runtime_difference; status=fail; expected=403; actual=200 |
| tfn_chain_lowercase_trim_pass_through | 200 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=tfn_chain_lowercase_trim_pass_through; status=fail; expected=200; actual=0 |
| unicode_double_encoded_uri_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=unicode_double_encoded_uri_runtime_difference; status=fail; expected=403; actual=200 |
| unicode_whitespace_normalization_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=unicode_whitespace_normalization_gap; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | 403 | - | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=v2_transformation_url_decode_invalid_sequence_mapped_candidate; status=fail; expected=403; actual=None |
| v3_request_cookies_names_case_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=v3_request_cookies_names_case_runtime_difference; status=fail; expected=403; actual=200 |
| v3_request_headers_names_lowercase_runtime_difference | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=v3_request_headers_names_lowercase_runtime_difference; status=fail; expected=403; actual=200 |
| xml_deep_nesting_future_target | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=xml_deep_nesting_future_target; status=fail; expected=403; actual=405 |
| xml_namespace_edge_connector_gap | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=xml_namespace_edge_connector_gap; status=fail; expected=403; actual=405 |
| xml_request_body_malformed_connector_gap | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=xml_request_body_malformed_connector_gap; status=fail; expected=403; actual=405 |
| xss_like_encoded_angles_normalization_probe | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=xss_like_encoded_angles_normalization_probe; status=fail; expected=403; actual=200 |
| xss_like_mixed_case_script_token_gap | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/nginx-summary.json; case=xss_like_mixed_case_script_token_gap; status=fail; expected=403; actual=200 |

## HAProxy Runtime Matrix Details

### HAProxy PASS Details
| Case | Variant | Expected | Actual | Evidence |
|---|---|---:|---:|---|
| action_allow_phase1_pass | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_allow_phase1_pass/result.json |
| action_deny_phase1 | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_deny_phase1/result.json |
| action_deny_phase2 | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_deny_phase2/result.json |
| action_status_401_phase1_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_status_401_phase1_block/result.json |
| audit_log_phase1_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/audit_log_phase1_block/result.json |
| collection_args_combined_size_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_combined_size_block/result.json |
| collection_args_get_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_get_block/result.json |
| collection_args_names_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_names_block/result.json |
| crs_sqli_anomaly_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/crs_sqli_anomaly_block/result.json |
| json_request_body_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/json_request_body_block/result.json |
| multipart_basic_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_basic_block/result.json |
| multipart_filename_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_filename_block/result.json |
| multipart_files_combined_size | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_combined_size/result.json |
| multipart_files_names_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_names_block/result.json |
| multipart_files_value_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_value_block/result.json |
| phase1_header_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase1_header_block/result.json |
| phase2_args_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase2_args_block/result.json |
| phase2_args_pass | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase2_args_pass/result.json |
| pr70_phase1_audit_request_header | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase1_audit_request_header/result.json |
| pr70_phase2_audit_urlencoded_body | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase2_audit_urlencoded_body/result.json |
| pr70_phase3_audit_response_header | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase3_audit_response_header/result.json |
| request_body_args_post_names_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_args_post_names_block/result.json |
| request_body_json_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_json_block/result.json |
| request_body_raw_text_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_raw_text_block/result.json |
| request_body_urlencoded_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_urlencoded_block/result.json |
| response_header_basic | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/response_header_basic/result.json |
| rule_chain_both_match_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_both_match_block/result.json |
| rule_chain_first_only_pass | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_first_only_pass/result.json |
| rule_chain_second_only_pass | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_second_only_pass/result.json |
| v2_operator_begins_with_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_begins_with_block/result.json |
| v2_operator_contains_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_contains_block/result.json |
| v2_operator_contains_word_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_contains_word_block/result.json |
| v2_operator_ends_with_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_ends_with_block/result.json |
| v2_operator_pm_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_pm_block/result.json |
| v2_operator_streq_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_streq_block/result.json |
| v2_transformation_html_entity_decode_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_html_entity_decode_block/result.json |
| v2_transformation_lowercase_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_lowercase_block/result.json |
| v2_transformation_trim_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_trim_block/result.json |
| v2_transformation_url_decode_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_block/result.json |
| v2_transformation_url_decode_pass_no_match | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_pass_no_match/result.json |
| v3_args_names_get_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_args_names_get_block/result.json |
| v3_args_names_get_pass_no_match | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_args_names_get_pass_no_match/result.json |
| v3_auditlog_serial_fields_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_auditlog_serial_fields_block/result.json |
| v3_operator_pm_digit_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_operator_pm_digit_block/result.json |
| v3_operator_rx_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_operator_rx_block/result.json |
| v3_request_cookies_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_block/result.json |
| v3_request_cookies_names_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_block/result.json |
| v3_request_cookies_names_pass_no_match | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_pass_no_match/result.json |
| v3_request_cookies_pass_no_match | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_pass_no_match/result.json |
| v3_request_headers_names_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_block/result.json |
| v3_request_headers_names_pass_no_match | with-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_pass_no_match/result.json |
| v3_secaction_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_secaction_block/result.json |
| v3_transformation_trim_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_transformation_trim_block/result.json |
| xml_request_body_block | with-crs | 403 | 403 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_request_body_block/result.json |

### HAProxy FAIL Details
| Status | Count | Note |
|---|---:|---|
| FAIL | 0 | No live HAProxy runtime FAIL rows were reported in the current matrix. |

### HAProxy Non-PASS Summary
| Status | Count | Note |
|---|---:|---|
| FAIL | 0 | Live-executed HAProxy runtime mismatches only; PASS/FAIL require live execution. |
| BLOCKED | 0 | Relevant HAProxy rows blocked by current harness or prerequisites. |
| NOT_EXECUTABLE | 0 | Rows outside the current HAProxy runtime surface. |
| MAPPED_ONLY | 0 | Import inventory only; not runtime-executable YAML evidence. |

- Detailed BLOCKED, NOT_EXECUTABLE, and MAPPED_ONLY rows are reported in `reports/testing/generated/haproxy-runtime-results.generated.md`.
- BLOCKED, NOT_EXECUTABLE, and MAPPED_ONLY rows are not runtime FAIL rows.

## Runtime Verified Status
- Runtime matrix records current local Apache, NGINX, and HAProxy per-case smoke evidence when available.
- PASS in this snapshot means the case was executed by that connector's smoke harness and matched the case expectation in the summary JSON.
- XFAIL, pending, connector-gap, runtime-difference, future, and mapped-only inventory are not promoted by this snapshot.
- FORCE_ALL_CASES=1 attempts xfail/pending/future/gap YAML cases where they are applicable to the connector.
- HAProxy PASS is scoped to live HAProxy evidence only; current HAProxy coverage is partial request-side YAML execution.
- RESPONSE_BODY remains non-verified/non-promoted.
- Runtime passed, but this does not verify RESPONSE_BODY support.
- make smoke-all was not run by runtime-matrix; full-smoke PASS counts remain unknown.

## Open Runtime Issues
- Mapped-only import inventory entries are not executable YAML runtime cases.
- XFAIL/pending/future/connector-gap/runtime-difference cases require separate evidence before any status change.
- RESPONSE_BODY remains experimental/non-verified.

## Open Gaps
- See `reports/testing/generated/connector-gap-summary.generated.md` for detailed entries.

## Verified Runtime Coverage
- Runtime-verified means only cases explicitly classified as `runtime_verified=true`.

## Pending Runtime Verification
- Cases with `runtime_verified=false` or `runtime_verified=unknown` are not runtime PASS proof.

## XFAIL / Known Gap Coverage
- XFAIL, pending, future, and experimental cases are listed in the XFAIL summary.
- XFAIL, pending, and gap cases need local runtime validation before promotion.

## Connector Gap / Runtime Difference Coverage
- Connector-gap and runtime-difference classes are reported separately.

## Phase 3/4 Outbound Coverage
- Phase 3/4 cases are visible in `reports/testing/generated/phase-coverage.generated.md` and in the runtime matrix.

## RESPONSE_BODY Status
- RESPONSE_BODY remains not verified and not promoted.

## Cloud / Quick / Full Smoke Meaning
- Generated coverage is not runtime evidence by itself.
- Full runtime validation is local and evidence-based.
- GitHub/Codex checks are intentionally lightweight.
- XFAIL, pending, and gap cases need local runtime validation.
- `make smoke-all` is authoritative only if it was actually executed successfully.

## Generated Artifacts
- `reports/testing/generated/case-matrix.generated.md`
- `reports/testing/generated/coverage-summary.generated.md`
- `reports/testing/generated/xfail-summary.generated.md`
- `reports/testing/generated/connector-gap-summary.generated.md`
- `reports/testing/generated/phase-coverage.generated.md`

## Note
- Generated summaries do not replace full-smoke runtime evidence.
- No RESPONSE_BODY promotion is made without stable runtime evidence.
