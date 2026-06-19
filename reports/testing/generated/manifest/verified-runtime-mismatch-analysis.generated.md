> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:51:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-verified-runtime-mismatch-analysis.py`
> Make target: `generate-verified-runtime-mismatch-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# Verified Runtime Mismatch Analysis

Verified run id: `2026-06-16T19-12-00Z-614c8049`

This report is generated only from verified runtime producer files. It does not invent missing PASS/FAIL values.

## Summary

| Field | Value |
|---|---|
| Mismatches | `771` |
| Critical mismatches | `0` |
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
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `bca8c97edc4f6d5bab304488e596af2a047b9f5f17994cf72ef64ae748430ff8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `1717c2a630321e9b7bf04cadd161eac0c164673442e843c2bd291994f0a1038c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `d20599aa223dad587761dd10551cb44fdbc00b83165baa7071c8d159ecc1ea04` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `949e28d7142459e86e0cb9ec1fad12b8b7172a5681039421e4075087d6c3de82` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `0a7ac7b47460d1aece31e5a5cce68ff254229b0d8da71644dd06d92739113aa6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `af1020b64ee7d12bd6580aafa92e5182aaacaf27dd8599991cfdf6cf161deabe` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `213018f411175c07f783a4ab48618a52e54b07f2be1d36543a18096b3c6013ef` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `2ad3431b993b3b1bd376f883bf7e4e92a69190a88685056a58dd8072e1ed181e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `af547bfca06e171781dee73eb432942ce47189d9ab8363fa7c694ed0cd994fda` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `fd4de70202d5780055fc4d4ad076133078c876970cf21cf54023d18139dd9fa4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `6f93aac6466c0e301e3bd6dfc3c4bbab4f5955ec884cd28eb28ba6821ab1ba0a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `1ff741bf7a50983b1d2e403206f2a75ba4cc21e43a45b0dd530f49cd3b344f46` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `efc447466ad8121a9316477b087e74a7155148082320a9cd57805aa3327f675e` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | present | `9167164893422a4ebf6587db8d70a96a61f169b49766a2abca2279126459a8d3` |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | present | `97a35281bbe37a2d08df5962b766ed71be05dd4dcb0673d275a0596d16650820` |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260619T063228Z-xml_request_body_malformed_connector_gap/native-case-run.json` | present | `38964013ce0ab0541e763b0472694e0123e70d8c55e609fb961c290064cee1a5` |

## By Connector

| Connector | Count |
|---|---:|
| apache | 243 |
| haproxy | 243 |
| nginx | 285 |

## By Category

| Category | Count |
|---|---:|
| known_not_next | 102 |
| libmodsecurity_collection_name_case_semantics | 36 |
| libmodsecurity_collection_semantics | 24 |
| libmodsecurity_transformation_semantics | 24 |
| libmodsecurity_xml_parser_semantics | 12 |
| nginx_phase4_response_body_enforcement_gap | 22 |
| nolog_expected_no_audit | 6 |
| phase4_rule_match_no_disruptive_intervention | 6 |
| secaction_detection_only_overlay | 6 |
| with_mrts_detection_only_overlay | 533 |

## Top Cases

| Case | Count |
|---|---:|
| `duplicate_args_encoded_separator_edge` | 12 |
| `duplicate_header_case_normalization_gap` | 12 |
| `edge_semicolon_query_args_names` | 12 |
| `files_empty_part_future_compatibility` | 12 |
| `parser_xml_partial_body_future_target` | 12 |
| `unicode_double_encoded_uri_runtime_difference` | 12 |
| `unicode_whitespace_normalization_gap` | 12 |
| `v3_request_cookies_names_case_runtime_difference` | 12 |
| `v3_request_headers_names_lowercase_runtime_difference` | 12 |
| `xml_deep_nesting_future_target` | 12 |
| `xml_request_body_malformed_connector_gap` | 12 |
| `phase4_auditlog_outbound_escaped_value_gap` | 8 |
| `phase4_auditlog_outbound_matched_var_future` | 8 |
| `phase4_auditlog_outbound_message_connector_gap` | 8 |
| `phase4_auditlog_outbound_multiline_section_gap` | 8 |
| `phase4_auditlog_outbound_rule_id_runtime_difference` | 8 |
| `phase4_response_body_buffering_order_future_target` | 8 |
| `phase4_response_body_chunk_assumption_connector_gap` | 8 |
| `phase4_response_body_compressed_assumption_experimental` | 8 |
| `phase4_response_body_empty_future_target` | 8 |

## Mismatch Table

| Connector | Variant | Case | Expected | Actual | Status | Classification | Evidence File |
|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | no-crs/no-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | no-crs/no-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/no-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/no-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | libmodsecurity_xml_parser_semantics | `full-matrix/no-crs/no-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
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
| apache | no-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | no-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | no-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | no-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | no-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | no-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | no-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | no-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
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
| apache | no-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | no-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_encoded_value_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_encoded_value_future_target/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_location_encoded_runtime_diff` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_location_encoded_runtime_diff/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_mixed_case_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_mixed_case_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_multi_value_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_multi_value_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase3_response_headers_set_cookie_multi_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_set_cookie_multi_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_escaped_value_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_escaped_value_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_matched_var_future` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_matched_var_future/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_message_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_message_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_auditlog_outbound_rule_id_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_rule_id_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_buffering_order_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_buffering_order_future_target/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_chunk_assumption_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_chunk_assumption_connector_gap/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_compressed_assumption_experimental` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_compressed_assumption_experimental/result.json` |
| apache | no-crs/with-mrts | `phase4_response_body_empty_future_target` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
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
| apache | no-crs/with-mrts | `sqli_like_keyword_spacing_probe` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_keyword_spacing_probe/result.json` |
| apache | no-crs/with-mrts | `sqli_like_quote_encoding_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/sqli_like_quote_encoding_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `tfn_chain_urldecode_compress_whitespace_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_chain_urldecode_compress_whitespace_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_compress_whitespace_runtime_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_compress_whitespace_runtime_gap/result.json` |
| apache | no-crs/with-mrts | `tfn_none_exact_block_phase2` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_none_exact_block_phase2/result.json` |
| apache | no-crs/with-mrts | `tfn_urldecodeuni_future_target_phase1` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/tfn_urldecodeuni_future_target_phase1/result.json` |
| apache | no-crs/with-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
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
| apache | no-crs/with-mrts | `v2_transformation_url_decode_invalid_sequence_mapped_candidate` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v2_transformation_url_decode_invalid_sequence_mapped_candidate/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_duplicate_query_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_duplicate_query_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_args_names_get_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_args_names_get_block/result.json` |
| apache | no-crs/with-mrts | `v3_auditlog_serial_fields_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_auditlog_serial_fields_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_pm_digit_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_pm_digit_block/result.json` |
| apache | no-crs/with-mrts | `v3_operator_rx_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_operator_rx_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_block/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_duplicate_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_duplicate_connector_gap/result.json` |
| apache | no-crs/with-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | no-crs/with-mrts | `v3_secaction_block` | `403` | `200` | fail | secaction_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_secaction_block/result.json` |
| apache | no-crs/with-mrts | `v3_transformation_trim_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/v3_transformation_trim_block/result.json` |
| apache | no-crs/with-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | no-crs/with-mrts | `xml_namespace_edge_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_namespace_edge_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_block/result.json` |
| apache | no-crs/with-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | libmodsecurity_xml_parser_semantics | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
| apache | no-crs/with-mrts | `xss_like_encoded_angles_normalization_probe` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_encoded_angles_normalization_probe/result.json` |
| apache | no-crs/with-mrts | `xss_like_mixed_case_script_token_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/no-crs/with-mrts/apache/logs/apache-runtime/xss_like_mixed_case_script_token_gap/result.json` |
| apache | with-crs/no-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/no-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/no-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/no-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/no-mrts | `parser_xml_partial_body_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/parser_xml_partial_body_future_target/result.json` |
| apache | with-crs/no-mrts | `unicode_double_encoded_uri_runtime_difference` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/unicode_double_encoded_uri_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `unicode_whitespace_normalization_gap` | `403` | `200` | fail | libmodsecurity_transformation_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/unicode_whitespace_normalization_gap/result.json` |
| apache | with-crs/no-mrts | `v3_action_nolog_pass_no_audit` | `200` | `200` | fail | nolog_expected_no_audit | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_action_nolog_pass_no_audit/result.json` |
| apache | with-crs/no-mrts | `v3_request_cookies_names_case_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_request_cookies_names_case_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `v3_request_headers_names_lowercase_runtime_difference` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/v3_request_headers_names_lowercase_runtime_difference/result.json` |
| apache | with-crs/no-mrts | `xml_deep_nesting_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xml_deep_nesting_future_target/result.json` |
| apache | with-crs/no-mrts | `xml_request_body_malformed_connector_gap` | `403` | `200` | fail | libmodsecurity_xml_parser_semantics | `full-matrix/with-crs/no-mrts/apache/logs/apache-runtime/xml_request_body_malformed_connector_gap/result.json` |
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
| apache | with-crs/with-mrts | `crs_sqli_anomaly_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/crs_sqli_anomaly_block/result.json` |
| apache | with-crs/with-mrts | `duplicate_args_encoded_separator_edge` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_args_encoded_separator_edge/result.json` |
| apache | with-crs/with-mrts | `duplicate_cookie_name_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_cookie_name_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `duplicate_header_case_normalization_gap` | `403` | `200` | fail | libmodsecurity_collection_name_case_semantics | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/duplicate_header_case_normalization_gap/result.json` |
| apache | with-crs/with-mrts | `edge_plus_vs_space_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_plus_vs_space_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `edge_semicolon_query_args_names` | `403` | `200` | fail | libmodsecurity_collection_semantics | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/edge_semicolon_query_args_names/result.json` |
| apache | with-crs/with-mrts | `files_empty_part_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_empty_part_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `files_names_mixed_case_filename_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json` |
| apache | with-crs/with-mrts | `json_duplicate_keys_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_duplicate_keys_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `json_empty_body_future_compatibility` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_empty_body_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_nested_object_future_compatibility` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_nested_object_future_compatibility/result.json` |
| apache | with-crs/with-mrts | `json_request_body_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/json_request_body_block/result.json` |
| apache | with-crs/with-mrts | `multipart_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_basic_block/result.json` |
| apache | with-crs/with-mrts | `multipart_duplicate_field_names_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json` |
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
| apache | with-crs/with-mrts | `phase1_vs_phase2_request_body_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase1_vs_phase2_request_body_gap/result.json` |
| apache | with-crs/with-mrts | `phase2_args_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase2_args_block/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_content_type_charset_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_content_type_charset_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_duplicate_value_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_duplicate_value_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_encoded_value_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_encoded_value_future_target/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_location_encoded_runtime_diff` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_location_encoded_runtime_diff/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_mixed_case_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_mixed_case_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_multi_value_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_multi_value_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase3_response_headers_set_cookie_multi_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase3_response_headers_set_cookie_multi_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_auditlog_outbound_escaped_value_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_escaped_value_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_auditlog_outbound_matched_var_future` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_matched_var_future/result.json` |
| apache | with-crs/with-mrts | `phase4_auditlog_outbound_message_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_message_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_auditlog_outbound_multiline_section_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_auditlog_outbound_rule_id_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_auditlog_outbound_rule_id_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_buffering_order_future_target` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_buffering_order_future_target/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_chunk_assumption_connector_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_chunk_assumption_connector_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_compressed_assumption_experimental` | `403` | `200` | fail | known_not_next | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_compressed_assumption_experimental/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_empty_future_target` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_empty_future_target/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_html_entity_decode_gap` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_entity_decode_gap/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_html_text_normalization_probe` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_html_text_normalization_probe/result.json` |
| apache | with-crs/with-mrts | `phase4_response_body_unicode_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/phase4_response_body_unicode_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `pr70_phase1_audit_request_header` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/pr70_phase1_audit_request_header/result.json` |
| apache | with-crs/with-mrts | `pr70_phase2_audit_urlencoded_body` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/pr70_phase2_audit_urlencoded_body/result.json` |
| apache | with-crs/with-mrts | `pr70_phase3_audit_response_header` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/pr70_phase3_audit_response_header/result.json` |
| apache | with-crs/with-mrts | `pr70_phase4_response_body_audit_xfail` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/pr70_phase4_response_body_audit_xfail/result.json` |
| apache | with-crs/with-mrts | `request_body_args_post_names_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/request_body_args_post_names_block/result.json` |
| apache | with-crs/with-mrts | `request_body_json_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/request_body_json_block/result.json` |
| apache | with-crs/with-mrts | `request_body_json_invalid_runtime_difference` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/request_body_json_invalid_runtime_difference/result.json` |
| apache | with-crs/with-mrts | `request_body_raw_text_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/request_body_raw_text_block/result.json` |
| apache | with-crs/with-mrts | `request_body_urlencoded_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/request_body_urlencoded_block/result.json` |
| apache | with-crs/with-mrts | `response_body_basic_block` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/response_body_basic_block/result.json` |
| apache | with-crs/with-mrts | `response_header_basic` | `403` | `200` | fail | with_mrts_detection_only_overlay | `full-matrix/with-crs/with-mrts/apache/logs/apache-runtime/response_header_basic/result.json` |
| ... | ... | `571 more rows in JSON` | ... | ... | ... | ... | ... |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `bca8c97edc4f6d5bab304488e596af2a047b9f5f17994cf72ef64ae748430ff8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | `97a35281bbe37a2d08df5962b766ed71be05dd4dcb0673d275a0596d16650820` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | `9167164893422a4ebf6587db8d70a96a61f169b49766a2abca2279126459a8d3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260619T063228Z-xml_request_body_malformed_connector_gap/native-case-run.json` | `38964013ce0ab0541e763b0472694e0123e70d8c55e609fb961c290064cee1a5` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172142Z-unicode_double_encoded_uri_runtime_difference/native-case-run.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260618T172131Z-unicode_whitespace_normalization_gap/native-case-run.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/native-case-runs/20260619T063228Z-xml_request_body_malformed_connector_gap/native-case-run.json` | present | input file available |
