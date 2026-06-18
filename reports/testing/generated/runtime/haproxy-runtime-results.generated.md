> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:37:01Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `framework:ci/generate-case-matrix.py`
> Make target: `generate-test-matrix`
> Owner: `runtime`
> Severity: `informational`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Generated HAProxy Runtime Results

- Command: `MODSECURITY_MRTS_VARIANT=with-mrts make smoke-haproxy`
- Status: **FAIL**
- Exit code: `2`
- Build status: `unknown`
- Per-case results: `available`
- Summary evidence: `/src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json`
- Attempted YAML cases in default runtime snapshot: **54**
- Runtime evidence is current local snapshot evidence only.
- RESPONSE_BODY remains non-verified/non-promoted.
- Bounded Phase 4 / strict-abort evidence remains experimental/non-promoted; pass-through rows do not prove full RESPONSE_BODY support.

## Raw Smoke Summary
| Status | Count |
|---|---:|
| PASS | 10 |
| FAIL | 44 |
| BLOCKED | 0 |
| NOT_EXECUTABLE | 0 |
| SKIPPED | 0 |

## Semantic Status Counts
| Status | Count |
|---|---:|
| PASS | 10 |
| FAIL | 44 |
| NOT_EXECUTABLE | 87 |

## HAProxy PASS Details
| Case | Variant | Expected | Actual | Evidence |
|---|---|---:|---:|---|
| action_allow_phase1_pass | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_allow_phase1_pass/result.json |
| phase2_args_pass | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase2_args_pass/result.json |
| response_body_pass | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/response_body_pass/result.json |
| rule_chain_first_only_pass | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_first_only_pass/result.json |
| rule_chain_second_only_pass | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_second_only_pass/result.json |
| v2_transformation_url_decode_pass_no_match | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_pass_no_match/result.json |
| v3_args_names_get_pass_no_match | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_args_names_get_pass_no_match/result.json |
| v3_request_cookies_names_pass_no_match | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_pass_no_match/result.json |
| v3_request_cookies_pass_no_match | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_pass_no_match/result.json |
| v3_request_headers_names_pass_no_match | no-crs | 200 | 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_pass_no_match/result.json |

## HAProxy FAIL Details
| Case | Variant | Expected | Actual | Assessment | Evidence |
|---|---|---:|---:|---|---|
| action_deny_phase1 | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_deny_phase1/result.json |
| action_deny_phase2 | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_deny_phase2/result.json |
| action_status_401_phase1_block | no-crs | 401 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/action_status_401_phase1_block/result.json |
| audit_log_phase1_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/audit_log_phase1_block/result.json |
| collection_args_combined_size_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_combined_size_block/result.json |
| collection_args_get_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_get_block/result.json |
| collection_args_names_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/collection_args_names_block/result.json |
| json_request_body_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/json_request_body_block/result.json |
| multipart_basic_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_basic_block/result.json |
| multipart_filename_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_filename_block/result.json |
| multipart_files_combined_size | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_combined_size/result.json |
| multipart_files_names_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_names_block/result.json |
| multipart_files_value_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_files_value_block/result.json |
| phase1_header_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase1_header_block/result.json |
| phase2_args_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase2_args_block/result.json |
| pr70_phase1_audit_request_header | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase1_audit_request_header/result.json |
| pr70_phase2_audit_urlencoded_body | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase2_audit_urlencoded_body/result.json |
| pr70_phase3_audit_response_header | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/pr70_phase3_audit_response_header/result.json |
| request_body_args_post_names_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_args_post_names_block/result.json |
| request_body_json_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_json_block/result.json |
| request_body_raw_text_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_raw_text_block/result.json |
| request_body_urlencoded_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/request_body_urlencoded_block/result.json |
| response_header_basic | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/response_header_basic/result.json |
| rule_chain_both_match_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/rule_chain_both_match_block/result.json |
| v2_operator_begins_with_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_begins_with_block/result.json |
| v2_operator_contains_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_contains_block/result.json |
| v2_operator_contains_word_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_contains_word_block/result.json |
| v2_operator_ends_with_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_ends_with_block/result.json |
| v2_operator_pm_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_pm_block/result.json |
| v2_operator_streq_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_operator_streq_block/result.json |
| v2_transformation_html_entity_decode_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_html_entity_decode_block/result.json |
| v2_transformation_lowercase_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_lowercase_block/result.json |
| v2_transformation_trim_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_trim_block/result.json |
| v2_transformation_url_decode_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_block/result.json |
| v3_args_names_get_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_args_names_get_block/result.json |
| v3_auditlog_serial_fields_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_auditlog_serial_fields_block/result.json |
| v3_operator_pm_digit_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_operator_pm_digit_block/result.json |
| v3_operator_rx_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_operator_rx_block/result.json |
| v3_request_cookies_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_block/result.json |
| v3_request_cookies_names_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_block/result.json |
| v3_request_headers_names_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_block/result.json |
| v3_secaction_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_secaction_block/result.json |
| v3_transformation_trim_block | no-crs | 403 | 200 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_transformation_trim_block/result.json |
| xml_request_body_block | no-crs | 403 | 501 | live HAProxy runtime result mismatch | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_request_body_block/result.json |

## HAProxy BLOCKED Details
| Status | Count | Note |
|---|---:|---|
| BLOCKED | 0 | No HAProxy BLOCKED rows were reported in the current matrix. |

## HAProxy NOT_EXECUTABLE Details
| Status | Count | Note |
|---|---:|---|
| NOT_EXECUTABLE | 0 | No HAProxy NOT_EXECUTABLE rows were reported in the current matrix. |

## HAProxy MAPPED_ONLY Details
| Status | Count | Note |
|---|---:|---|
| MAPPED_ONLY | 0 | No HAProxy mapped-only import inventory entries were reported in the current matrix. |

## HAProxy Force-All Runtime Details
- Runtime mode: `force-all`
- Command: `FORCE_ALL_CASES=1 make smoke-haproxy`
- Status: **FAIL**
- Exit code: `1`
- Attempted YAML cases: **133**
- Total cases in summary: **133**
- Evidence root: `/src/ModSecurity-conector-build/results/force-all`
- JSONL evidence: `/src/ModSecurity-conector-build/results/force-all/haproxy-results.jsonl`
- Per-case result root: `/src/ModSecurity-conector-build/logs/haproxy-runtime`

| Status | Count |
|---|---:|
| PASS | 104 |
| FAIL | 23 |
| BLOCKED | 0 |
| NOT_EXECUTABLE | 6 |
| SKIPPED | 0 |

- Force-all exited nonzero because live-executed rows mismatched expected runtime outcomes.

### HAProxy Force-All FAIL Rows
| Case | Expected | Observed | Reason | Evidence | Decision Log |
|---|---:|---:|---|---|---|
| duplicate_args_encoded_separator_edge | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/duplicate_args_encoded_separator_edge/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/duplicate_args_encoded_separator_edge/decision.jsonl |
| duplicate_header_case_normalization_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/duplicate_header_case_normalization_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/duplicate_header_case_normalization_gap/decision.jsonl |
| edge_semicolon_query_args_names | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/edge_semicolon_query_args_names/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/edge_semicolon_query_args_names/decision.jsonl |
| files_names_mixed_case_filename_gap | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/files_names_mixed_case_filename_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/files_names_mixed_case_filename_gap/decision.jsonl |
| multipart_duplicate_field_names_gap | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_duplicate_field_names_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_duplicate_field_names_gap/decision.jsonl |
| parser_xml_partial_body_future_target | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/parser_xml_partial_body_future_target/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/parser_xml_partial_body_future_target/decision.jsonl |
| phase1_vs_phase2_request_body_gap | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase1_vs_phase2_request_body_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase1_vs_phase2_request_body_gap/decision.jsonl |
| phase3_response_headers_multi_value_connector_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_multi_value_connector_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_multi_value_connector_gap/decision.jsonl |
| phase3_response_headers_set_cookie_multi_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_set_cookie_multi_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_set_cookie_multi_gap/decision.jsonl |
| phase4_auditlog_outbound_multiline_section_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase4_auditlog_outbound_multiline_section_gap/decision.jsonl |
| response_headers_multi_value_runtime_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/response_headers_multi_value_runtime_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/response_headers_multi_value_runtime_gap/decision.jsonl |
| sqli_like_keyword_spacing_probe | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/sqli_like_keyword_spacing_probe/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/sqli_like_keyword_spacing_probe/decision.jsonl |
| sqli_like_quote_encoding_runtime_difference | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/sqli_like_quote_encoding_runtime_difference/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/sqli_like_quote_encoding_runtime_difference/decision.jsonl |
| tfn_chain_lowercase_trim_pass_through | 200 | 0 | expected HTTP 200; observed HTTP 0 | /src/ModSecurity-conector-build/logs/haproxy-runtime/tfn_chain_lowercase_trim_pass_through/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/tfn_chain_lowercase_trim_pass_through/decision.jsonl |
| unicode_double_encoded_uri_runtime_difference | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/unicode_double_encoded_uri_runtime_difference/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/unicode_double_encoded_uri_runtime_difference/decision.jsonl |
| unicode_whitespace_normalization_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/unicode_whitespace_normalization_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/unicode_whitespace_normalization_gap/decision.jsonl |
| v3_request_cookies_names_case_runtime_difference | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_case_runtime_difference/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_cookies_names_case_runtime_difference/decision.jsonl |
| v3_request_headers_names_lowercase_runtime_difference | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/v3_request_headers_names_lowercase_runtime_difference/decision.jsonl |
| xml_deep_nesting_future_target | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_deep_nesting_future_target/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_deep_nesting_future_target/decision.jsonl |
| xml_namespace_edge_connector_gap | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_namespace_edge_connector_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_namespace_edge_connector_gap/decision.jsonl |
| xml_request_body_malformed_connector_gap | 403 | 501 | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_request_body_malformed_connector_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/xml_request_body_malformed_connector_gap/decision.jsonl |
| xss_like_encoded_angles_normalization_probe | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xss_like_encoded_angles_normalization_probe/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/xss_like_encoded_angles_normalization_probe/decision.jsonl |
| xss_like_mixed_case_script_token_gap | 403 | 200 | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/logs/haproxy-runtime/xss_like_mixed_case_script_token_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/xss_like_mixed_case_script_token_gap/decision.jsonl |

### HAProxy Force-All NOT_EXECUTABLE Rows
| Case | Reason | Evidence | Decision Log |
|---|---|---|---|
| files_empty_part_future_compatibility | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/files_empty_part_future_compatibility/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/files_empty_part_future_compatibility/decision.jsonl |
| json_empty_body_future_compatibility | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/json_empty_body_future_compatibility/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/json_empty_body_future_compatibility/decision.jsonl |
| multipart_empty_filename_connector_gap | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_empty_filename_connector_gap/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/multipart_empty_filename_connector_gap/decision.jsonl |
| phase3_response_headers_server_presence_pending | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_server_presence_pending/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase3_response_headers_server_presence_pending/decision.jsonl |
| phase4_response_body_empty_future_target | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase4_response_body_empty_future_target/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/phase4_response_body_empty_future_target/decision.jsonl |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | structurally not executable for this connector/runtime mode; see evidence_path and decision_log_path | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json | /src/ModSecurity-conector-build/logs/haproxy-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/decision.jsonl |

### HAProxy Force-All BLOCKED Rows
| Status | Count | Note |
|---|---:|---|
| BLOCKED | 0 | No rows were reported. |

## Results
| case_id | path | YAML status | runtime status | promotion | reason | evidence |
|---|---|---|---|---|---|---|
| audit_log_empty_sections_future_target | tests/cases/audit-log/audit_log_empty_sections_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| audit_log_matched_var_encoded_value | tests/cases/audit-log/audit_log_matched_var_encoded_value.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| audit_log_message_presence_connector_gap | tests/cases/audit-log/audit_log_message_presence_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| audit_log_multiline_message_normalization | tests/cases/audit-log/audit_log_multiline_message_normalization.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| audit_log_phase1_block | tests/cases/audit-log/audit_log_phase1_block.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| audit_log_rule_id_presence_runtime_difference | tests/cases/audit-log/audit_log_rule_id_presence_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| duplicate_args_encoded_separator_edge | tests/cases/audit-log/duplicate_args_encoded_separator_edge.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| duplicate_cookie_name_runtime_difference | tests/cases/audit-log/duplicate_cookie_name_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| duplicate_header_case_normalization_gap | tests/cases/audit-log/duplicate_header_case_normalization_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| parser_json_partial_body_connector_gap | tests/cases/audit-log/parser_json_partial_body_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| parser_xml_partial_body_future_target | tests/cases/audit-log/parser_xml_partial_body_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| pr70_phase1_audit_request_header | tests/cases/audit-log/pr70-phases/pr70_phase1_audit_request_header.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | tests/cases/audit-log/pr70-phases/pr70_phase2_audit_urlencoded_body.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=501 |
| pr70_phase3_audit_response_header | tests/cases/audit-log/pr70-phases/pr70_phase3_audit_response_header.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| pr70_phase4_response_body_audit_xfail | tests/cases/audit-log/pr70-phases/pr70_phase4_response_body_audit_xfail.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_chain_lowercase_trim_pass_through | tests/cases/audit-log/tfn_chain_lowercase_trim_pass_through.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_chain_urldecode_compress_whitespace_gap | tests/cases/audit-log/tfn_chain_urldecode_compress_whitespace_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v3_action_nolog_pass_no_audit | tests/cases/audit-log/v3_action_nolog_pass_no_audit.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v3_auditlog_serial_fields_block | tests/cases/audit-log/v3_auditlog_serial_fields_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=200 |
| json_duplicate_keys_runtime_difference | tests/cases/body/json/json_duplicate_keys_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| json_empty_body_future_compatibility | tests/cases/body/json/json_empty_body_future_compatibility.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| json_nested_object_future_compatibility | tests/cases/body/json/json_nested_object_future_compatibility.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| json_request_body_block | tests/cases/body/json/json_request_body_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=json_request_body_block; status=fail; expected=403; actual=501 |
| request_body_json_block | tests/cases/body/json/request_body_json_block.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_json_block; status=fail; expected=403; actual=501 |
| request_body_json_invalid_runtime_difference | tests/cases/body/json/request_body_json_invalid_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| files_empty_part_future_compatibility | tests/cases/body/multipart/files_empty_part_future_compatibility.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| files_names_mixed_case_filename_gap | tests/cases/body/multipart/files_names_mixed_case_filename_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| multipart_basic_block | tests/cases/body/multipart/multipart_basic_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=501 |
| multipart_duplicate_field_names_gap | tests/cases/body/multipart/multipart_duplicate_field_names_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| multipart_empty_filename_connector_gap | tests/cases/body/multipart/multipart_empty_filename_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| multipart_encoded_filename_runtime_difference | tests/cases/body/multipart/multipart_encoded_filename_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| multipart_filename_block | tests/cases/body/multipart/multipart_filename_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=501 |
| multipart_files_combined_size | tests/cases/body/multipart/multipart_files_combined_size.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=501 |
| multipart_files_names_block | tests/cases/body/multipart/multipart_files_names_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=501 |
| multipart_files_value_block | tests/cases/body/multipart/multipart_files_value_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=501 |
| multipart_invalid_boundary_future_target | tests/cases/body/multipart/multipart_invalid_boundary_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| xml_deep_nesting_future_target | tests/cases/body/xml/xml_deep_nesting_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| xml_namespace_edge_connector_gap | tests/cases/body/xml/xml_namespace_edge_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| xml_request_body_block | tests/cases/body/xml/xml_request_body_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=501 |
| xml_request_body_malformed_connector_gap | tests/cases/body/xml/xml_request_body_malformed_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| nginx_phase4_content_type_out_of_scope | tests/cases/connector-specific/nginx/nginx_phase4_content_type_out_of_scope.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_phase4_minimal_log_only | tests/cases/connector-specific/nginx/nginx_phase4_minimal_log_only.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_phase4_safe_log_only | tests/cases/connector-specific/nginx/nginx_phase4_safe_log_only.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_phase4_strict_connection_abort | tests/cases/connector-specific/nginx/nginx_phase4_strict_connection_abort.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_redirect_phase1_302 | tests/cases/connector-specific/nginx/nginx_redirect_phase1_302.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_tx_scoring_absolute_block | tests/cases/connector-specific/nginx/nginx_tx_scoring_absolute_block.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| nginx_tx_scoring_iterative_block | tests/cases/connector-specific/nginx/nginx_tx_scoring_iterative_block.yaml | imported | NOT_EXECUTABLE | - | nginx-specific case is not applicable to haproxy | - |
| v3_args_names_duplicate_query_connector_gap | tests/cases/future-gap/v3_args_names_duplicate_query_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| edge_missing_header_pass_through | tests/cases/negative-pass-through/edge_missing_header_pass_through.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| operator_beginswith_pass_no_match_phase2 | tests/cases/negative-pass-through/operator_beginswith_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| operator_contains_pass_no_match_phase2 | tests/cases/negative-pass-through/operator_contains_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| operator_endswith_pass_no_match_phase2 | tests/cases/negative-pass-through/operator_endswith_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| operator_rx_pass_no_match_phase2 | tests/cases/negative-pass-through/operator_rx_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| operator_streq_pass_no_match_phase2 | tests/cases/negative-pass-through/operator_streq_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase2_header_only_pass_through | tests/cases/negative-pass-through/phase2_header_only_pass_through.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_lowercase_pass_no_match_phase2 | tests/cases/negative-pass-through/tfn_lowercase_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_trim_pass_no_match_phase2 | tests/cases/negative-pass-through/tfn_trim_pass_no_match_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v2_transformation_url_decode_pass_no_match | tests/cases/negative-pass-through/v2_transformation_url_decode_pass_no_match.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_url_decode_pass_no_match; status=pass; expected=200; actual=200 |
| v3_args_names_get_pass_no_match | tests/cases/negative-pass-through/v3_args_names_get_pass_no_match.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_args_names_get_pass_no_match; status=pass; expected=200; actual=200 |
| v3_request_cookies_names_pass_no_match | tests/cases/negative-pass-through/v3_request_cookies_names_pass_no_match.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_names_pass_no_match; status=pass; expected=200; actual=200 |
| v3_request_cookies_pass_no_match | tests/cases/negative-pass-through/v3_request_cookies_pass_no_match.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_pass_no_match; status=pass; expected=200; actual=200 |
| v3_request_headers_names_pass_no_match | tests/cases/negative-pass-through/v3_request_headers_names_pass_no_match.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_headers_names_pass_no_match; status=pass; expected=200; actual=200 |
| action_allow_phase1_pass | tests/cases/phases/phase1/action_allow_phase1_pass.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_allow_phase1_pass; status=pass; expected=200; actual=200 |
| action_deny_phase1 | tests/cases/phases/phase1/action_deny_phase1.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | tests/cases/phases/phase1/action_status_401_phase1_block.yaml | imported | FAIL | not promoted | expected HTTP 401; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| phase1_vs_phase2_request_body_gap | tests/cases/phases/phase1/phase1_vs_phase2_request_body_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| action_deny_phase2 | tests/cases/phases/phase2/action_deny_phase2.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | tests/cases/phases/phase2/collection_args_combined_size_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | tests/cases/phases/phase2/collection_args_get_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | tests/cases/phases/phase2/collection_args_names_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| edge_semicolon_query_args_names | tests/cases/phases/phase2/edge_semicolon_query_args_names.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase2_args_block | tests/cases/phases/phase2/phase2_args_block.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| phase2_args_pass | tests/cases/phases/phase2/phase2_args_pass.yaml | active | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase2_args_pass; status=pass; expected=200; actual=200 |
| request_body_args_post_names_block | tests/cases/phases/phase2/request_body_args_post_names_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=501 |
| request_body_raw_text_block | tests/cases/phases/phase2/request_body_raw_text_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=501 |
| request_body_urlencoded_block | tests/cases/phases/phase2/request_body_urlencoded_block.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 501 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=501 |
| v3_args_names_get_block | tests/cases/phases/phase2/v3_args_names_get_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | tests/cases/phases/phase2/v3_secaction_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | tests/cases/request/cookies/v3_request_cookies_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | tests/cases/request/cookies/v3_request_cookies_names_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_case_runtime_difference | tests/cases/request/cookies/v3_request_cookies_names_case_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase1_header_block | tests/cases/request/headers/phase1_header_block.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | tests/cases/request/headers/v2_transformation_html_entity_decode_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | tests/cases/request/headers/v3_request_headers_names_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_duplicate_connector_gap | tests/cases/request/headers/v3_request_headers_names_duplicate_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v3_request_headers_names_lowercase_runtime_difference | tests/cases/request/headers/v3_request_headers_names_lowercase_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| edge_plus_vs_space_runtime_difference | tests/cases/request/uri/edge_plus_vs_space_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_urldecodeuni_future_target_phase1 | tests/cases/request/uri/tfn_urldecodeuni_future_target_phase1.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| unicode_double_encoded_uri_runtime_difference | tests/cases/request/uri/unicode_double_encoded_uri_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v2_transformation_remove_nulls_future_target | tests/cases/request/uri/v2_transformation_remove_nulls_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v2_transformation_url_decode_block | tests/cases/request/uri/v2_transformation_url_decode_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_auditlog_outbound_escaped_value_gap | tests/cases/response/body/phase4_auditlog_outbound_escaped_value_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_auditlog_outbound_matched_var_future | tests/cases/response/body/phase4_auditlog_outbound_matched_var_future.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_auditlog_outbound_message_connector_gap | tests/cases/response/body/phase4_auditlog_outbound_message_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_auditlog_outbound_multiline_section_gap | tests/cases/response/body/phase4_auditlog_outbound_multiline_section_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_auditlog_outbound_rule_id_runtime_difference | tests/cases/response/body/phase4_auditlog_outbound_rule_id_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_buffering_order_future_target | tests/cases/response/body/phase4_response_body_buffering_order_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_chunk_assumption_connector_gap | tests/cases/response/body/phase4_response_body_chunk_assumption_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_compressed_assumption_experimental | tests/cases/response/body/phase4_response_body_compressed_assumption_experimental.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_empty_future_target | tests/cases/response/body/phase4_response_body_empty_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_html_entity_decode_gap | tests/cases/response/body/phase4_response_body_html_entity_decode_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_html_text_normalization_probe | tests/cases/response/body/phase4_response_body_html_text_normalization_probe.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_pass_no_match_experimental | tests/cases/response/body/phase4_response_body_pass_no_match_experimental.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase4_response_body_unicode_runtime_difference | tests/cases/response/body/phase4_response_body_unicode_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| response_body_basic_block | tests/cases/response/body/response_body_basic_block.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| response_body_pass | tests/cases/response/body/response_body_pass.yaml | imported | PASS | RESPONSE_BODY non-verified; non-promotable | Runtime passed, but this does not verify RESPONSE_BODY support. | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=response_body_pass; status=pass; expected=200; actual=200 |
| phase3_response_headers_content_type_charset_gap | tests/cases/response/headers/phase3_response_headers_content_type_charset_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_duplicate_value_runtime_difference | tests/cases/response/headers/phase3_response_headers_duplicate_value_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_encoded_value_future_target | tests/cases/response/headers/phase3_response_headers_encoded_value_future_target.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_location_encoded_runtime_diff | tests/cases/response/headers/phase3_response_headers_location_encoded_runtime_diff.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_missing_pass_through | tests/cases/response/headers/phase3_response_headers_missing_pass_through.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_mixed_case_connector_gap | tests/cases/response/headers/phase3_response_headers_mixed_case_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_multi_value_connector_gap | tests/cases/response/headers/phase3_response_headers_multi_value_connector_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_server_presence_pending | tests/cases/response/headers/phase3_response_headers_server_presence_pending.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| phase3_response_headers_set_cookie_multi_gap | tests/cases/response/headers/phase3_response_headers_set_cookie_multi_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| response_header_basic | tests/cases/response/headers/response_header_basic.yaml | active | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| response_headers_multi_value_runtime_gap | tests/cases/response/headers/response_headers_multi_value_runtime_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| crs_sqli_anomaly_block | tests/cases/security/crs/crs_sqli_anomaly_block.yaml | active | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| rule_chain_both_match_block | tests/cases/security/rule-chain/rule_chain_both_match_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| rule_chain_first_only_pass | tests/cases/security/rule-chain/rule_chain_first_only_pass.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=rule_chain_first_only_pass; status=pass; expected=200; actual=200 |
| rule_chain_second_only_pass | tests/cases/security/rule-chain/rule_chain_second_only_pass.yaml | imported | PASS | promotion eligible | runtime summary result; classification=active | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=rule_chain_second_only_pass; status=pass; expected=200; actual=200 |
| sqli_like_keyword_spacing_probe | tests/cases/security/sql/sqli_like_keyword_spacing_probe.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| sqli_like_quote_encoding_runtime_difference | tests/cases/security/sql/sqli_like_quote_encoding_runtime_difference.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| xss_like_encoded_angles_normalization_probe | tests/cases/security/xss/xss_like_encoded_angles_normalization_probe.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| xss_like_mixed_case_script_token_gap | tests/cases/security/xss/xss_like_mixed_case_script_token_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_compress_whitespace_runtime_gap | tests/cases/transformations/tfn_compress_whitespace_runtime_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| tfn_none_exact_block_phase2 | tests/cases/transformations/tfn_none_exact_block_phase2.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| unicode_whitespace_normalization_gap | tests/cases/transformations/unicode_whitespace_normalization_gap.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v2_operator_begins_with_block | tests/cases/transformations/v2_operator_begins_with_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | tests/cases/transformations/v2_operator_contains_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | tests/cases/transformations/v2_operator_contains_word_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | tests/cases/transformations/v2_operator_ends_with_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | tests/cases/transformations/v2_operator_pm_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | tests/cases/transformations/v2_operator_streq_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | tests/cases/transformations/v2_transformation_lowercase_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | tests/cases/transformations/v2_transformation_trim_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_tab_future_compatibility | tests/cases/transformations/v2_transformation_trim_tab_future_compatibility.yaml | imported | NOT_EXECUTABLE | not promoted | no haproxy runtime evidence recorded for this executable YAML case | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| v3_operator_pm_digit_block | tests/cases/transformations/v3_operator_pm_digit_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=200 |
| v3_operator_rx_block | tests/cases/transformations/v3_operator_rx_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | tests/cases/transformations/v3_transformation_trim_block.yaml | imported | FAIL | not promoted | expected HTTP 403; observed HTTP 200 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `c8e7113e2b7d4982ad6817e9f3fd4387370db33224a0f14ec265126ec685f5f9` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
