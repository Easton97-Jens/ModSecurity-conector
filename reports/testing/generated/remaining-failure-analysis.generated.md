# Remaining Full-Matrix Failure Analysis

Generated at: `2026-06-13T13:49:37Z`

## Scope
- Connector Full-Matrix evidence is separate from Native MRTS infrastructure evidence.
- Native Apache/NGINX evidence is reported in the `mrts-native-*` reports and does not replace connector PASS/FAIL values.
- Native `100003-1` remains classified as `native_modsecurity_semantics / phase4_native_limitation`.
- This report is analysis-only; no connector/harness semantics were changed.

## Summary
- Attempted/pass/fail/blocked/not executable: **3928 / 3040 / 816 / 0 / 72**
- Pending metadata rows observed: **2298**
- Unique remaining failure cases: **113**
- MRTS imported connector failures: **0**
- Non-MRTS framework failures: **816**

## Regression Checks
| Check | Status | Count | Cases |
|---|---|---|---|
| Unexpected BLOCKED entries | clear | 0 | - |
| Apache expected 200 -> actual 404 | clear | 0 | - |
| HAProxy expected 200 -> actual 501 | clear | 0 | - |
| NGINX actual status 500 | clear | 0 | - |
| MRTS classification incomplete | clear | 0 | - |

## Category Rollup
| Category | Count | Connectors | Fixable | Risk | Next step |
|---|---|---|---|---|---|
| intervention_blocking | 261 | apache, haproxy, nginx | partly fixable; first split true connector gaps from future/native semantic cases | medium to high | sample high-count expected 403 -> actual 200 cases and decide semantic gap vs stale promoted expectation |
| transformation_semantics | 144 | apache, haproxy, nginx | not a harness quick win; needs semantic comparison against libmodsecurity expectations | high | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| phase4_response_body_non_promoted | 116 | apache, haproxy, nginx | not a quick connector fix; keep report-only until phase 4/RESPONSE_BODY promotion criteria are met | high for promotion, low for report-only | keep as non-promoted/report-only unless promotion policy changes |
| response_header_hook | 94 | apache, haproxy, nginx | possible connector/hook work; start with response-header capture evidence | medium | triage response-header phase 3 capture on Apache/NGINX first, then HAProxy |
| request_body_processor | 69 | apache, haproxy, nginx | possibly fixable after processor-specific triage | medium | split JSON, URL-encoded, and XML body processor cases before code changes |
| multipart_files | 66 | apache, haproxy, nginx | possibly fixable; likely connector/body parser evidence work | medium | compare multipart variable population across connectors with one representative request |
| xml_processor | 54 | apache, haproxy, nginx | possibly fixable, but high risk without XML processor parity checks | medium to high | verify XML processor enablement and malformed XML semantics |
| audit_log_evidence | 6 | apache, haproxy, nginx | fixable if audit-log assertion path is wrong; otherwise report/classification-only | low to medium | inspect `v3_action_nolog_pass_no_audit` audit expectation and report classification |
| rule_chain_semantics | 6 | apache, haproxy, nginx | small but semantic; requires focused rule-chain evidence | medium | single-case rule-chain triage with logs |

## Top 10 Overall Failure Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 82 | response_header_hook / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 58 | phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 52 | phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top 10 Apache Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | apache / transformation_semantics / transformations / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 30 | apache / response_header_hook / response-headers / phase:3 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 22 | apache / intervention_blocking / collections / phase:1 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | apache / multipart_files / multipart / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 18 | apache / intervention_blocking / collections / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | apache / xml_processor / body-processors / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 14 | apache / phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 14 | apache / transformation_semantics / transformations / phase:1 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | apache / phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | apache / intervention_blocking / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top 10 NGINX Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | nginx / transformation_semantics / transformations / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 30 | nginx / response_header_hook / response-headers / phase:3 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 30 | nginx / phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 24 | nginx / phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 22 | nginx / intervention_blocking / collections / phase:1 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | nginx / multipart_files / multipart / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 18 | nginx / intervention_blocking / collections / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | nginx / xml_processor / body-processors / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 14 | nginx / transformation_semantics / transformations / phase:1 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | nginx / intervention_blocking / operators / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top 10 HAProxy Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | haproxy / transformation_semantics / transformations / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | haproxy / intervention_blocking / collections / phase:1 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | haproxy / multipart_files / multipart / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 22 | haproxy / response_header_hook / response-headers / phase:3 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_multi_value_connector_gap | 4805 | RESPONSE_HEADERS:Set-Cookie |
| 18 | haproxy / intervention_blocking / collections / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | haproxy / xml_processor / body-processors / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 14 | haproxy / phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 14 | haproxy / transformation_semantics / transformations / phase:1 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | haproxy / phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | haproxy / intervention_blocking / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top MRTS Imported Failures
- None.

## Top Non-MRTS Framework Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 82 | response_header_hook / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 58 | phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 52 | phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top Phase4 / Response-Body Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 58 | phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 52 | phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 6 | phase4_response_body_non_promoted / response-body / phase:4 / 200→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | - | - |

## Top Intervention / Blocking Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 82 | response_header_hook / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 58 | phase4_response_body_non_promoted / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 52 | phase4_response_body_non_promoted / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | - | - |

## Top Cross-Connector Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4608 | ARGS_NAMES |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4607 | REQUEST_HEADERS_NAMES |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4513 | ARGS_NAMES |
| 12 | files_names_mixed_case_filename_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4705 | FILES_NAMES |
| 12 | multipart_duplicate_field_names_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4703 | ARGS_NAMES |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor | {'403→200': 12} | 4610 | XML |
| 12 | phase3_response_headers_multi_value_connector_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response_header_hook | {'403→200': 12} | 4805 | RESPONSE_HEADERS:Set-Cookie |
| 12 | phase3_response_headers_set_cookie_multi_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response_header_hook | {'403→200': 12} | 4904 | RESPONSE_HEADERS:Set-Cookie |
| 12 | phase4_auditlog_outbound_multiline_section_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_response_body_non_promoted | {'403→200': 12} | 4910 | RESPONSE_BODY |
| 12 | response_headers_multi_value_runtime_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response_header_hook | {'403→200': 12} | 4410 | RESPONSE_HEADERS:Set-Cookie |

## Top Connector-Only Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 2 | nginx_phase4_content_type_out_of_scope | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_response_body_non_promoted | {'200→200': 2} | - | - |
| 2 | nginx_phase4_minimal_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_response_body_non_promoted | {'200→200': 2} | - | - |
| 2 | nginx_phase4_safe_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_response_body_non_promoted | {'200→200': 2} | - | - |
| 2 | nginx_phase4_strict_connection_abort | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_response_body_non_promoted | {'403→200': 2} | - | - |
| 2 | nginx_redirect_phase1_302 | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'302→200': 2} | - | - |
| 2 | nginx_tx_scoring_absolute_block | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 2} | 3101 | ARGS |
| 2 | nginx_tx_scoring_iterative_block | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 2} | 3201 | ARGS |

## Recommendation
- Empfohlener nächster Fix-Cluster: `audit_log_evidence / v3_action_nolog_pass_no_audit`
- Begründung: HTTP behavior passes; remaining failure is evidence/assertion semantics
- Nicht als nächstes bearbeiten: `phase4_response_body_non_promoted`, weil known non-promoted/long-term surface; high risk to promote or force behavior prematurely.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil large count but likely semantic; needs native/libmodsecurity comparison before fixes.
