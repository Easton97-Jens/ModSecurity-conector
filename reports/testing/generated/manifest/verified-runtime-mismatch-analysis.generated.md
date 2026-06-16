> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:56:32Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-verified-runtime-mismatch-analysis.py`
> Make target: `generate-verified-runtime-mismatch-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Verified Runtime Mismatch Analysis

Verified run id: `2026-06-15T21-01-39Z-9391a8d0`

This report is generated only from verified runtime producer files. It does not invent missing PASS/FAIL values.

## Summary

| Field | Value |
|---|---|
| Mismatches | `1733` |
| Critical mismatches | `1639` |
| Full matrix complete | `true` |
| Full matrix runtime status | `runtime_completed_with_mismatches` |
| Full matrix jobs | `12/12` |
| Full matrix status | `not_run` |
| Full matrix timeout | `false` |
| Full matrix refresh timeout | `false` |
| Evidence scope | `full` |

## Inputs

| Input | Status | SHA256 |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `f9634d21e3486bd05843bab0d423dd871d48edcfe6a2ec7a46cd5c694f3b54bb` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `c8402f160a295c0771a536254b82be01d30ee5ac6e889d3788831b61dcf71078` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `51ed44be35af5488aece950470f42c121296a25708f26d4abaf459fb621a084d` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `dfdc25be9e88791784904eee41e3f14c0963c4d3937ee02fd1d9f2b7d33cb001` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `0f3a0b511cc163d3528cd2a8a3e227445edf51b73131d7448aa6246a61c931cc` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `01bbff9b29b7ea6b99675661e94fda6bee0d82e80e60f84bfb779f99997d0e0f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `47b2bb86a5ba0352664796a58827a2310763b006085215914fc239bff9084757` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `3d78b7443596377e0edb3ee3ea18b1f35250a25205b0d2f74d2ca517bf3202f8` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `19d476da10b282fe0b3dda4e5b33f7d6af022291c556dd0c5cdd2fa2f45b12aa` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `33c1e28170576345db47af9fea8431d2838a7fe6105d9578d6e25593f8290b2a` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `8999743cd573a3fbb48273cacf45e6c9ea3da3abac769f47395c3d46aa49b424` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `d9dc4ab30c858f67255701c0ee2b7ee77d6ec1835b675cea43d796be29480083` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `0a23ef8755e377c3a1f02072a5ae0778000ba36a65fb0f1a4e03ec0b494ab0bb` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `4eeec4587355925ba8d7922e43436c5e7d60d17632c89848eda1e438cdc0954a` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `8b80105e55523c2dba26ee787c046e0dbac2318685ca4afe38ef01e5362d8e44` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `54b49ce81980fe2ee2679d87e94af43eb1a35bfd68f461465f57cba81216e3b7` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `38edd35d5d84110a318587bf1a5571d3eba41414c1b3693c8fb97ae744fde8b1` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `539e70cbe89c2d1c0ee010d3fa935294552f0d9ea8778e303ef1c8b9a6fa4610` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `af2f0b5878d7d5bb584f84b2c8d664008ef2f6f5f9ec767e5af2beb78748d202` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `1864576f38033a6e8ac8294a2532ffc0d82b2d6738988556928a11e8ad9ce03d` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `6ae8ee4339ffc6fe9aac0528e750685def7ee88df50e464f8b931b841b624be9` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `1e8998bdf289217d45a7df434310de0f91c3b6ef6d6785bb45ec3052e95e396f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `1bebe0cc629cf0f3d171f7147da0d3f1cdf5f75669ff7752327aa91f5e4ed4c3` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `6c1859588a5d1cff7ee5a6fd1c347f4629381bd6c6221e0c7978f0f072ef989e` |
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` |

## By Connector

| Connector | Count |
|---|---:|
| apache | 276 |
| haproxy | 276 |
| nginx | 1181 |

## By Category

| Category | Count |
|---|---:|
| connector_capability_gap | 117 |
| expected_status_mismatch | 244 |
| framework_expected_behavior_gap | 68 |
| known_not_next | 94 |
| runtime_regression | 1123 |
| timeout_or_incomplete | 83 |
| unknown | 4 |

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
| `multipart_empty_filename_connector_gap` | 12 |
| `parser_xml_partial_body_future_target` | 12 |
| `phase3_response_headers_server_presence_pending` | 12 |
| `phase4_auditlog_outbound_multiline_section_gap` | 12 |
| `phase4_response_body_empty_future_target` | 12 |
| `sqli_like_keyword_spacing_probe` | 12 |
| `sqli_like_quote_encoding_runtime_difference` | 12 |
| `unicode_double_encoded_uri_runtime_difference` | 12 |
| `unicode_whitespace_normalization_gap` | 12 |
| `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | 12 |
| `v3_request_cookies_names_case_runtime_difference` | 12 |
| `v3_request_headers_names_lowercase_runtime_difference` | 12 |
| `xml_deep_nesting_future_target` | 12 |

## Mismatch Table

| Connector | Variant | Case | Expected | Actual | Status | Classification | Evidence File |
|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | `__job__` | `complete` | `return_code=2` | blocked | timeout_or_incomplete | `full-matrix/no-crs/no-mrts/apache/job.json` |
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
| apache | no-crs/with-mrts | `__job__` | `complete` | `return_code=2` | blocked | timeout_or_incomplete | `full-matrix/no-crs/with-mrts/apache/job.json` |
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
| apache | with-crs/no-mrts | `__job__` | `complete` | `return_code=2` | blocked | timeout_or_incomplete | `full-matrix/with-crs/no-mrts/apache/job.json` |
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
| apache | with-crs/with-mrts | `__job__` | `complete` | `return_code=2` | blocked | timeout_or_incomplete | `full-matrix/with-crs/with-mrts/apache/job.json` |
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
| ... | ... | `1533 more rows in JSON` | ... | ... | ... | ... | ... |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | `f9634d21e3486bd05843bab0d423dd871d48edcfe6a2ec7a46cd5c694f3b54bb` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
