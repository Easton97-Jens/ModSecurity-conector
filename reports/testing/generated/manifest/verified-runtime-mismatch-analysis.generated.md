> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:20Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-verified-runtime-mismatch-analysis.py`
> Make target: `generate-verified-runtime-mismatch-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `complete`

# Verified Runtime Mismatch Analysis

Verified run id: `2026-06-16T16-57-44Z-b53340a8`

This report is generated only from verified runtime producer files. It does not invent missing PASS/FAIL values.

## Summary

| Field | Value |
|---|---|
| Mismatches | `586` |
| Critical mismatches | `524` |
| Full matrix complete | `true` |
| Full matrix runtime status | `runtime_completed_with_mismatches` |
| Full matrix jobs | `12/12` |
| Full matrix status | `FAIL` |
| Full matrix timeout | `false` |
| Full matrix refresh timeout | `false` |
| Evidence scope | `full` |

## Inputs

| Input | Status | SHA256 |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `808eb86b9a8c6b19093fc2daf965ca1fd031be11bfaba263f2988a910586c0bf` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `056fd01f02ef7665d48072916e692a369e993e423504ef8c19d5cdb05ae3f933` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `08652610c757311206bf4a3a33b79490dd3814a5891c61751bafc0e3ddac7d97` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `6b786b2af4a2058528b6f25c352773c3c7a540699888de46fbaa9a08ba5007ef` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `0b8eb3359e8f27a0941eb834026b92ea31730acb1c61882dc1429d82f7d60ebf` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `24ddaa455062edc3b5c5a112e72f2a00db41133f445de701d0c15d0af8ecdac2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `d72de57df3d0b25cd973e11de3f65b5dfce551ce31c7283404dc0b87f4072bc1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `44b196bb61b6b29157be63c7b2ef3f54fecc7db62d92ecb279514eaea261baa9` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `d424f4de305b39b5b75a023d407b5a2a49dac1d3c6941942370e79a3cfc0d8e6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `4332e809ba8efbb0fb5b7c87bd9ae94994edb77a4a68041214927ba23be10c87` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `ba3e820dd192da52ce9f7f59e894b809d66c536bf90cc2e670648c377f28d65d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `158169e9f708a0d2a23dfc2f81340778a6db6b0f78e3ff98ddc8ef60212b19b2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` |

## By Connector

| Connector | Count |
|---|---:|
| apache | 272 |
| haproxy | 4 |
| nginx | 310 |

## By Category

| Category | Count |
|---|---:|
| connector_capability_gap | 80 |
| expected_status_mismatch | 256 |
| framework_expected_behavior_gap | 16 |
| known_not_next | 62 |
| runtime_regression | 110 |
| timeout_or_incomplete | 52 |
| unknown | 10 |

## Top Cases

| Case | Count |
|---|---:|
| `duplicate_args_encoded_separator_edge` | 8 |
| `duplicate_header_case_normalization_gap` | 8 |
| `edge_semicolon_query_args_names` | 8 |
| `files_empty_part_future_compatibility` | 8 |
| `files_names_mixed_case_filename_gap` | 8 |
| `json_empty_body_future_compatibility` | 8 |
| `multipart_duplicate_field_names_gap` | 8 |
| `multipart_empty_filename_connector_gap` | 8 |
| `parser_xml_partial_body_future_target` | 8 |
| `phase3_response_headers_server_presence_pending` | 8 |
| `phase4_auditlog_outbound_multiline_section_gap` | 8 |
| `phase4_response_body_empty_future_target` | 8 |
| `sqli_like_keyword_spacing_probe` | 8 |
| `sqli_like_quote_encoding_runtime_difference` | 8 |
| `unicode_double_encoded_uri_runtime_difference` | 8 |
| `unicode_whitespace_normalization_gap` | 8 |
| `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | 8 |
| `v3_request_cookies_names_case_runtime_difference` | 8 |
| `v3_request_headers_names_lowercase_runtime_difference` | 8 |
| `xml_deep_nesting_future_target` | 8 |

## Mismatch Table

| Connector | Variant | Case | Expected | Actual | Status | Classification | Evidence File |
|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/no-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | no-crs/no-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | no-crs/no-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | no-crs/no-mrts | `multipart_empty_filename_connector_gap` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | no-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | no-crs/no-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | no-crs/no-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | no-crs/no-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | no-crs/no-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | no-crs/no-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | no-crs/no-mrts | `sqli_like_quote_encoding_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/sqli_like_quote_encoding_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | no-crs/no-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/no-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | no-crs/no-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | no-crs/no-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | no-crs/no-mrts | `xss_like_mixed_case_script_token_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xss_like_mixed_case_script_token_gap/result.json` |
| apache | no-crs/with-mrts | `action_deny_phase1` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase1/result.json` |
| apache | no-crs/with-mrts | `action_deny_phase2` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase2/result.json` |
| apache | no-crs/with-mrts | `action_status_401_phase1_block` | `401` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_status_401_phase1_block/result.json` |
| apache | no-crs/with-mrts | `audit_log_empty_sections_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_empty_sections_future_target/result.json` |
| apache | no-crs/with-mrts | `audit_log_matched_var_encoded_value` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_matched_var_encoded_value/result.json` |
| apache | no-crs/with-mrts | `audit_log_message_presence_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_message_presence_connector_gap/result.json` |
| apache | no-crs/with-mrts | `audit_log_multiline_message_normalization` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_multiline_message_normalization/result.json` |
| apache | no-crs/with-mrts | `audit_log_phase1_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_phase1_block/result.json` |
| apache | no-crs/with-mrts | `audit_log_rule_id_presence_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_rule_id_presence_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `collection_args_combined_size_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_combined_size_block/result.json` |
| apache | no-crs/with-mrts | `collection_args_get_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_get_block/result.json` |
| apache | no-crs/with-mrts | `collection_args_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_names_block/result.json` |
| apache | no-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | no-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | no-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | no-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | no-crs/with-mrts | `multipart_empty_filename_connector_gap` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | no-crs/with-mrts | `multipart_encoded_filename_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_encoded_filename_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `multipart_filename_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_filename_block/result.json` |
| apache | no-crs/with-mrts | `multipart_files_combined_size` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_combined_size/result.json` |
| apache | no-crs/with-mrts | `multipart_files_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_names_block/result.json` |
| apache | no-crs/with-mrts | `multipart_files_value_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_value_block/result.json` |
| apache | no-crs/with-mrts | `multipart_invalid_boundary_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_invalid_boundary_future_target/result.json` |
| apache | no-crs/with-mrts | `parser_json_partial_body_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/parser_json_partial_body_connector_gap/result.json` |
| apache | no-crs/with-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | no-crs/with-mrts | `phase1_header_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase1_header_block/result.json` |
| apache | no-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | no-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_encoded_value_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_encoded_value_future_target/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_location_encoded_runtime_diff` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_location_encoded_runtime_diff/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_mixed_case_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_mixed_case_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_multi_value_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_multi_value_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_set_cookie_multi_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_set_cookie_multi_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_escaped_value_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_escaped_value_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_matched_var_future` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_matched_var_future/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_message_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_message_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_rule_id_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_rule_id_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_buffering_order_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_buffering_order_future_target/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_chunk_assumption_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_chunk_assumption_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_compressed_assumption_experimental` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_compressed_assumption_experimental/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_html_entity_decode_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_entity_decode_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_html_text_normalization_probe` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_text_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_unicode_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_unicode_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `pr70_phase1_audit_request_header` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase1_audit_request_header/result.json` |
| apache | no-crs/with-mrts | `pr70_phase2_audit_urlencoded_body` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase2_audit_urlencoded_body/result.json` |
| apache | no-crs/with-mrts | `pr70_phase3_audit_response_header` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase3_audit_response_header/result.json` |
| apache | no-crs/with-mrts | `pr70_phase4_response_body_audit_xfail` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase4_response_body_audit_xfail/result.json` |
| apache | no-crs/with-mrts | `request_body_args_post_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_args_post_names_block/result.json` |
| apache | no-crs/with-mrts | `request_body_json_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_json_block/result.json` |
| apache | no-crs/with-mrts | `request_body_json_invalid_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_json_invalid_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `request_body_raw_text_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_raw_text_block/result.json` |
| apache | no-crs/with-mrts | `request_body_urlencoded_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_urlencoded_block/result.json` |
| apache | no-crs/with-mrts | `response_body_basic_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_body_basic_block/result.json` |
| apache | no-crs/with-mrts | `response_header_basic` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_header_basic/result.json` |
| apache | no-crs/with-mrts | `response_headers_multi_value_runtime_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_headers_multi_value_runtime_gap/result.json` |
| apache | no-crs/with-mrts | `rule_chain_both_match_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/rule_chain_both_match_block/result.json` |
| apache | no-crs/with-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | no-crs/with-mrts | `sqli_like_quote_encoding_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_quote_encoding_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `tfn_chain_urldecode_compress_whitespace_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_chain_urldecode_compress_whitespace_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_compress_whitespace_runtime_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_compress_whitespace_runtime_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_none_exact_block_phase2` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_none_exact_block_phase2/result.json` |
| apache | no-crs/with-mrts | `tfn_urldecodeuni_future_target_phase1` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_urldecodeuni_future_target_phase1/result.json` |
| apache | no-crs/with-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | no-crs/with-mrts | `v2_operator_begins_with_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_begins_with_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_contains_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_contains_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_contains_word_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_contains_word_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_ends_with_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_ends_with_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_pm_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_pm_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_streq_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_streq_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_html_entity_decode_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_html_entity_decode_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_lowercase_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_lowercase_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_remove_nulls_future_target` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_remove_nulls_future_target/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_trim_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_trim_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_trim_tab_future_compatibility` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_trim_tab_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_url_decode_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_duplicate_query_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_duplicate_query_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_get_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_get_block/result.json` |
| apache | no-crs/with-mrts | `v3_auditlog_serial_fields_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_auditlog_serial_fields_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_pm_digit_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_pm_digit_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_rx_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_rx_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_duplicate_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_duplicate_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_secaction_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_secaction_block/result.json` |
| apache | no-crs/with-mrts | `v3_transformation_trim_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_transformation_trim_block/result.json` |
| apache | no-crs/with-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/with-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_block/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `xss_like_mixed_case_script_token_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_mixed_case_script_token_gap/result.json` |
| apache | with-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/no-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | with-crs/no-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | with-crs/no-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | with-crs/no-mrts | `multipart_empty_filename_connector_gap` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | with-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | with-crs/no-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | with-crs/no-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | with-crs/no-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | with-crs/no-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | with-crs/no-mrts | `sqli_like_quote_encoding_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/sqli_like_quote_encoding_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | with-crs/no-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | with-crs/no-mrts | `v3_action_nolog_pass_no_audit` | `200` | `200` | fail | unknown | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_action_nolog_pass_no_audit/result.json` |
| apache | with-crs/no-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | with-crs/no-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | with-crs/no-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | with-crs/no-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | with-crs/no-mrts | `xss_like_mixed_case_script_token_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xss_like_mixed_case_script_token_gap/result.json` |
| apache | with-crs/with-mrts | `action_deny_phase1` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase1/result.json` |
| apache | with-crs/with-mrts | `action_deny_phase2` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase2/result.json` |
| apache | with-crs/with-mrts | `action_status_401_phase1_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_status_401_phase1_block/result.json` |
| apache | with-crs/with-mrts | `audit_log_empty_sections_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_empty_sections_future_target/result.json` |
| apache | with-crs/with-mrts | `audit_log_matched_var_encoded_value` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_matched_var_encoded_value/result.json` |
| apache | with-crs/with-mrts | `audit_log_message_presence_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_message_presence_connector_gap/result.json` |
| apache | with-crs/with-mrts | `audit_log_multiline_message_normalization` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_multiline_message_normalization/result.json` |
| apache | with-crs/with-mrts | `audit_log_phase1_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_phase1_block/result.json` |
| apache | with-crs/with-mrts | `audit_log_rule_id_presence_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_rule_id_presence_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `collection_args_combined_size_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_combined_size_block/result.json` |
| apache | with-crs/with-mrts | `collection_args_get_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_get_block/result.json` |
| apache | with-crs/with-mrts | `collection_args_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_names_block/result.json` |
| apache | with-crs/with-mrts | `crs_sqli_anomaly_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/crs_sqli_anomaly_block/result.json` |
| apache | with-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | with-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | with-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | with-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | with-crs/with-mrts | `multipart_empty_filename_connector_gap` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | with-crs/with-mrts | `multipart_encoded_filename_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_encoded_filename_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `multipart_filename_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_filename_block/result.json` |
| apache | with-crs/with-mrts | `multipart_files_combined_size` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_combined_size/result.json` |
| apache | with-crs/with-mrts | `multipart_files_names_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_names_block/result.json` |
| apache | with-crs/with-mrts | `multipart_files_value_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_value_block/result.json` |
| apache | with-crs/with-mrts | `multipart_invalid_boundary_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_invalid_boundary_future_target/result.json` |
| apache | with-crs/with-mrts | `parser_json_partial_body_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/parser_json_partial_body_connector_gap/result.json` |
| apache | with-crs/with-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | with-crs/with-mrts | `phase1_header_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase1_header_block/result.json` |
| apache | with-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | with-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| ... | ... | `386 more rows in JSON` | ... | ... | ... | ... | ... |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `808eb86b9a8c6b19093fc2daf965ca1fd031be11bfaba263f2988a910586c0bf` | `2026-06-16T16-57-44Z-b53340a8` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
