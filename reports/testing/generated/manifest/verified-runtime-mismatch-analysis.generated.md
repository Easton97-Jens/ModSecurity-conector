> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:47:45Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-verified-runtime-mismatch-analysis.py`
> Make target: `generate-verified-runtime-mismatch-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> Input status: `complete`

# Verified Runtime Mismatch Analysis

Verified run id: `2026-06-16T19-12-00Z-614c8049`

This report is generated only from verified runtime producer files. It does not invent missing PASS/FAIL values.

## Summary

| Field | Value |
|---|---|
| Mismatches | `836` |
| Critical mismatches | `264` |
| Full matrix complete | `true` |
| Full matrix runtime status | `completed_with_mismatches` |
| Full matrix jobs | `12/12` |
| Full matrix status | `complete` |
| Full matrix timeout | `false` |
| Full matrix refresh timeout | `false` |
| Evidence scope | `full` |

## Inputs

| Input | Status | SHA256 |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `8378473bbc7146a7ed3e077973aece4dc85d4b2ffce29cd77c39b5ea5c9b3362` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `a2e7af7da5e6fd2718f07fb2fed949d8a74e52b33dbe977e5599a422fe29e13a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `eb56f03b535595ee1a4849dc89166a318920bfefaac4539dff9db054a799bbb3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `97e2b1584a0e45a080adc9611b47a071c38d8edf9e7b7ad54e4eae4262ddfa79` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `d53014e2d1833d03c2fad718f38ac3f4ce2a1a38a3c36c28b1717cc218e2eb64` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `e90fd4aefa085251a2ecb602069c17d1fb91d02df867693d700caeafa8c169c1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `a2153f8b25a1c30ee814d87f1899ae1521e98f20ee095a552c463b368d5edc58` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `36406e6a7c2c5a2c79c54d0334ea71c52c5b338cdca893aa6db46101d47261ff` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `682c6766a313fa47720812649ef9055eb1131659e7227077bf7af2abde5ddb35` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `72f234c0e2fb6c20a9681140facf724c6977316fab4c74dbb633faf94ba112b9` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `360167461277beafb06af1ce4c27d4f3dfb4b876abea494f2ca1dc339e35df56` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `77be7ff6bb9437339ea31d60553db3f5116cee849e5f6313b2e81897a6c0683b` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `b879807daa3ac77b4e2dd6254233ffeaa4f46bd0ec76163d98ff2cd2590b3412` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `4a82546f163707fb800b44dcf86ecd7f1722f0e84428c1b41020d15f1d228dd2` |

## By Connector

| Connector | Count |
|---|---:|
| apache | 266 |
| haproxy | 266 |
| nginx | 304 |

## By Category

| Category | Count |
|---|---:|
| connector_capability_gap | 63 |
| expected_status_mismatch | 51 |
| framework_expected_behavior_gap | 24 |
| known_not_next | 102 |
| runtime_regression | 66 |
| timeout_or_incomplete | 48 |
| unknown | 12 |
| with_mrts_detection_only_overlay | 470 |

## Top Cases

| Case | Count |
|---|---:|
| `duplicate_args_encoded_separator_edge` | 12 |
| `duplicate_header_case_normalization_gap` | 12 |
| `edge_semicolon_query_args_names` | 12 |
| `files_empty_part_future_compatibility` | 12 |
| `files_names_mixed_case_filename_gap` | 12 |
| `json_empty_body_future_compatibility` | 12 |
| `multipart_duplicate_field_names_gap` | 12 |
| `parser_xml_partial_body_future_target` | 12 |
| `phase3_response_headers_server_presence_pending` | 12 |
| `phase4_auditlog_outbound_multiline_section_gap` | 12 |
| `phase4_response_body_empty_future_target` | 12 |
| `sqli_like_keyword_spacing_probe` | 12 |
| `unicode_double_encoded_uri_runtime_difference` | 12 |
| `unicode_whitespace_normalization_gap` | 12 |
| `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | 12 |
| `v3_request_cookies_names_case_runtime_difference` | 12 |
| `v3_request_headers_names_lowercase_runtime_difference` | 12 |
| `xml_deep_nesting_future_target` | 12 |
| `xml_namespace_edge_connector_gap` | 12 |
| `xml_request_body_malformed_connector_gap` | 12 |

## Mismatch Table

| Connector | Variant | Case | Expected | Actual | Status | Classification | Evidence File |
|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/no-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | no-crs/no-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | no-crs/no-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | no-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | no-crs/no-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | no-crs/no-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | no-crs/no-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | no-crs/no-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | no-crs/no-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | no-crs/no-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | no-crs/no-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/no-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | no-crs/no-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | no-crs/no-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `action_deny_phase1` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase1/result.json` |
| apache | no-crs/with-mrts | `action_deny_phase2` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase2/result.json` |
| apache | no-crs/with-mrts | `action_status_401_phase1_block` | `401` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/action_status_401_phase1_block/result.json` |
| apache | no-crs/with-mrts | `audit_log_empty_sections_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_empty_sections_future_target/result.json` |
| apache | no-crs/with-mrts | `audit_log_matched_var_encoded_value` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_matched_var_encoded_value/result.json` |
| apache | no-crs/with-mrts | `audit_log_message_presence_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_message_presence_connector_gap/result.json` |
| apache | no-crs/with-mrts | `audit_log_multiline_message_normalization` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_multiline_message_normalization/result.json` |
| apache | no-crs/with-mrts | `audit_log_phase1_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_phase1_block/result.json` |
| apache | no-crs/with-mrts | `audit_log_rule_id_presence_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/audit_log_rule_id_presence_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `collection_args_combined_size_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_combined_size_block/result.json` |
| apache | no-crs/with-mrts | `collection_args_get_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_get_block/result.json` |
| apache | no-crs/with-mrts | `collection_args_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/collection_args_names_block/result.json` |
| apache | no-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | no-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | no-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | no-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | no-crs/with-mrts | `multipart_empty_filename_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | no-crs/with-mrts | `multipart_encoded_filename_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_encoded_filename_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `multipart_filename_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_filename_block/result.json` |
| apache | no-crs/with-mrts | `multipart_files_combined_size` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_combined_size/result.json` |
| apache | no-crs/with-mrts | `multipart_files_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_names_block/result.json` |
| apache | no-crs/with-mrts | `multipart_files_value_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_files_value_block/result.json` |
| apache | no-crs/with-mrts | `multipart_invalid_boundary_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_invalid_boundary_future_target/result.json` |
| apache | no-crs/with-mrts | `parser_json_partial_body_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/parser_json_partial_body_connector_gap/result.json` |
| apache | no-crs/with-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | no-crs/with-mrts | `phase1_header_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase1_header_block/result.json` |
| apache | no-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | no-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_encoded_value_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_encoded_value_future_target/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_location_encoded_runtime_diff` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_location_encoded_runtime_diff/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_mixed_case_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_mixed_case_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_multi_value_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_multi_value_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_set_cookie_multi_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_set_cookie_multi_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_escaped_value_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_escaped_value_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_matched_var_future` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_matched_var_future/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_message_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_message_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_rule_id_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_rule_id_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_buffering_order_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_buffering_order_future_target/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_chunk_assumption_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_chunk_assumption_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_compressed_assumption_experimental` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_compressed_assumption_experimental/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_html_entity_decode_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_entity_decode_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_html_text_normalization_probe` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_text_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_unicode_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_unicode_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `pr70_phase1_audit_request_header` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase1_audit_request_header/result.json` |
| apache | no-crs/with-mrts | `pr70_phase2_audit_urlencoded_body` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase2_audit_urlencoded_body/result.json` |
| apache | no-crs/with-mrts | `pr70_phase3_audit_response_header` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase3_audit_response_header/result.json` |
| apache | no-crs/with-mrts | `pr70_phase4_response_body_audit_xfail` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/pr70_phase4_response_body_audit_xfail/result.json` |
| apache | no-crs/with-mrts | `request_body_args_post_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_args_post_names_block/result.json` |
| apache | no-crs/with-mrts | `request_body_json_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_json_block/result.json` |
| apache | no-crs/with-mrts | `request_body_json_invalid_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_json_invalid_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `request_body_raw_text_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_raw_text_block/result.json` |
| apache | no-crs/with-mrts | `request_body_urlencoded_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/request_body_urlencoded_block/result.json` |
| apache | no-crs/with-mrts | `response_body_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_body_basic_block/result.json` |
| apache | no-crs/with-mrts | `response_header_basic` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_header_basic/result.json` |
| apache | no-crs/with-mrts | `response_headers_multi_value_runtime_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/response_headers_multi_value_runtime_gap/result.json` |
| apache | no-crs/with-mrts | `rule_chain_both_match_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/rule_chain_both_match_block/result.json` |
| apache | no-crs/with-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | no-crs/with-mrts | `sqli_like_quote_encoding_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_quote_encoding_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `tfn_chain_urldecode_compress_whitespace_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_chain_urldecode_compress_whitespace_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_compress_whitespace_runtime_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_compress_whitespace_runtime_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_none_exact_block_phase2` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_none_exact_block_phase2/result.json` |
| apache | no-crs/with-mrts | `tfn_urldecodeuni_future_target_phase1` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_urldecodeuni_future_target_phase1/result.json` |
| apache | no-crs/with-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | runtime_regression | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | no-crs/with-mrts | `v2_operator_begins_with_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_begins_with_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_contains_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_contains_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_contains_word_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_contains_word_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_ends_with_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_ends_with_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_pm_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_pm_block/result.json` |
| apache | no-crs/with-mrts | `v2_operator_streq_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_operator_streq_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_html_entity_decode_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_html_entity_decode_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_lowercase_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_lowercase_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_remove_nulls_future_target` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_remove_nulls_future_target/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_trim_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_trim_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_trim_tab_future_compatibility` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_trim_tab_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_url_decode_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_block/result.json` |
| apache | no-crs/with-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_duplicate_query_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_duplicate_query_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_get_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_get_block/result.json` |
| apache | no-crs/with-mrts | `v3_auditlog_serial_fields_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_auditlog_serial_fields_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_pm_digit_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_pm_digit_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_rx_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_rx_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_duplicate_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_duplicate_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_secaction_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_secaction_block/result.json` |
| apache | no-crs/with-mrts | `v3_transformation_trim_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_transformation_trim_block/result.json` |
| apache | no-crs/with-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/with-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_block/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `xss_like_mixed_case_script_token_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_mixed_case_script_token_gap/result.json` |
| apache | with-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/no-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | with-crs/no-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | with-crs/no-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | with-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | with-crs/no-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | with-crs/no-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | with-crs/no-mrts | `phase4_response_body_empty_future_target` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | with-crs/no-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | framework_expected_behavior_gap | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
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
| apache | with-crs/with-mrts | `action_deny_phase1` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase1/result.json` |
| apache | with-crs/with-mrts | `action_deny_phase2` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_deny_phase2/result.json` |
| apache | with-crs/with-mrts | `action_status_401_phase1_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/action_status_401_phase1_block/result.json` |
| apache | with-crs/with-mrts | `audit_log_empty_sections_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_empty_sections_future_target/result.json` |
| apache | with-crs/with-mrts | `audit_log_matched_var_encoded_value` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_matched_var_encoded_value/result.json` |
| apache | with-crs/with-mrts | `audit_log_message_presence_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_message_presence_connector_gap/result.json` |
| apache | with-crs/with-mrts | `audit_log_multiline_message_normalization` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_multiline_message_normalization/result.json` |
| apache | with-crs/with-mrts | `audit_log_phase1_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_phase1_block/result.json` |
| apache | with-crs/with-mrts | `audit_log_rule_id_presence_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/audit_log_rule_id_presence_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `collection_args_combined_size_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_combined_size_block/result.json` |
| apache | with-crs/with-mrts | `collection_args_get_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_get_block/result.json` |
| apache | with-crs/with-mrts | `collection_args_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/collection_args_names_block/result.json` |
| apache | with-crs/with-mrts | `crs_sqli_anomaly_block` | `403` | `200` | fail | expected_status_mismatch | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/crs_sqli_anomaly_block/result.json` |
| apache | with-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | runtime_regression | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | with-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | with-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | with-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
| apache | with-crs/with-mrts | `multipart_empty_filename_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_empty_filename_connector_gap/result.json` |
| apache | with-crs/with-mrts | `multipart_encoded_filename_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_encoded_filename_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `multipart_filename_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_filename_block/result.json` |
| apache | with-crs/with-mrts | `multipart_files_combined_size` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_combined_size/result.json` |
| apache | with-crs/with-mrts | `multipart_files_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_names_block/result.json` |
| apache | with-crs/with-mrts | `multipart_files_value_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_files_value_block/result.json` |
| apache | with-crs/with-mrts | `multipart_invalid_boundary_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_invalid_boundary_future_target/result.json` |
| apache | with-crs/with-mrts | `parser_json_partial_body_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/parser_json_partial_body_connector_gap/result.json` |
| apache | with-crs/with-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | with-crs/with-mrts | `phase1_header_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase1_header_block/result.json` |
| apache | with-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | connector_capability_gap | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | with-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_encoded_value_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_encoded_value_future_target/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_location_encoded_runtime_diff` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_location_encoded_runtime_diff/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_mixed_case_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_mixed_case_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_multi_value_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_multi_value_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_server_presence_pending` | `200` | `http_status` | not_executable | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_server_presence_pending/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_set_cookie_multi_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_set_cookie_multi_gap/result.json` |
| ... | ... | `636 more rows in JSON` | ... | ... | ... | ... | ... |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `4a82546f163707fb800b44dcf86ecd7f1722f0e84428c1b41020d15f1d228dd2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `8378473bbc7146a7ed3e077973aece4dc85d4b2ffce29cd77c39b5ea5c9b3362` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
