# Remaining Full-Matrix Failure Analysis

Generated at: `2026-06-13T20:04:23Z`

## Scope
- Connector Full-Matrix evidence is separate from Native MRTS infrastructure evidence.
- Native Apache/NGINX evidence is reported in the `mrts-native-*` reports and does not replace connector PASS/FAIL values.
- Native `100003-1` remains classified as `native_modsecurity_semantics / phase4_native_limitation`.
- This report is analysis-only; runtime PASS/FAIL and expected statuses are not changed by classification metadata.

## Summary
- Attempted/pass/fail/blocked/not executable: **3928 / 3074 / 782 / 0 / 72**
- Pending metadata rows observed: **2298**
- Unique remaining failure cases: **113**
- MRTS imported connector failures: **0**
- Non-MRTS framework failures: **782**

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
| request_body_processor | 69 | apache, haproxy, nginx | possibly fixable after processor-specific triage | medium | split JSON, URL-encoded, and XML body processor cases before code changes |
| multipart_files | 66 | apache, haproxy, nginx | possibly fixable; likely connector/body parser evidence work | medium | compare multipart variable population across connectors with one representative request |
| phase4_missing_abort_evidence | 64 | apache, nginx | fixable only through real strict abort/log evidence, not status-only changes | high if promoted without transport proof | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay suppresses disruptive action | low; report-only if kept separate from PASS promotion | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| xml_processor | 54 | apache, haproxy, nginx | possibly fixable, but high risk without XML processor parity checks | medium to high | verify XML processor enablement and malformed XML semantics |
| phase4_connector_gap | 46 | apache, haproxy, nginx | connector capability gap unless a real abort mechanism is implemented and evidenced | high if faked; low if reported as gap | document connector gap unless implementation can prove a real hard abort |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | classification-only; nolog/pass rule is absent from audit evidence and CRS noise is unrelated | low; no runtime or expected-status change | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report-only unless the case is meant to exercise strict hard abort | low if reported honestly, high if promoted as hard abort | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| rule_chain_semantics | 6 | apache, haproxy, nginx | small but semantic; requires focused rule-chain evidence | medium | single-case rule-chain triage with logs |

## Top 10 Overall Failure Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 36 | intervention_blocking / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top 10 Apache Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | apache / transformation_semantics / transformations / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | apache / intervention_blocking / collections / phase:1 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | apache / multipart_files / multipart / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 18 | apache / intervention_blocking / collections / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | apache / xml_processor / body-processors / phase:2 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 16 | apache / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | apache / transformation_semantics / transformations / phase:1 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | apache / intervention_blocking / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | apache / intervention_blocking / audit-log / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 12 | apache / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |

## Top 10 NGINX Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | nginx / transformation_semantics / transformations / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 26 | nginx / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 22 | nginx / intervention_blocking / collections / phase:1 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | nginx / multipart_files / multipart / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 18 | nginx / intervention_blocking / collections / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | nginx / xml_processor / body-processors / phase:2 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 16 | nginx / phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_matched_var_future | 4908 | RESPONSE_BODY |
| 16 | nginx / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | nginx / transformation_semantics / transformations / phase:1 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | nginx / intervention_blocking / operators / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |

## Top 10 HAProxy Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 34 | haproxy / transformation_semantics / transformations / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | haproxy / intervention_blocking / collections / phase:1 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | haproxy / multipart_files / multipart / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 18 | haproxy / intervention_blocking / collections / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 18 | haproxy / xml_processor / body-processors / phase:2 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 16 | haproxy / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | haproxy / phase4_connector_gap / audit-log / phase:4 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 14 | haproxy / transformation_semantics / transformations / phase:1 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 14 | haproxy / phase4_connector_gap / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | haproxy / intervention_blocking / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |

## Top MRTS Imported Failures
- None.

## Top Non-MRTS Framework Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 36 | intervention_blocking / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top Phase4 / Response-Body Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 26 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 26 | phase4_connector_gap / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 20 | phase4_connector_gap / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_chunk_assumption_connector_gap | 4808 | RESPONSE_BODY |
| 6 | phase4_log_only_no_abort / response-body / phase:4 / 200→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | 920002 | RESPONSE_BODY |

## Top Intervention / Blocking Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 102 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | intervention_blocking / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 66 | multipart_files / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 54 | intervention_blocking / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |
| 54 | xml_processor / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | parser_xml_partial_body_future_target | 4610 | XML |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 42 | transformation_semantics / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | unicode_double_encoded_uri_runtime_difference | 4707 | REQUEST_URI |
| 42 | intervention_blocking / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 36 | intervention_blocking / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | intervention_blocking | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top Cross-Connector Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4608 | ARGS_NAMES |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4607 | REQUEST_HEADERS_NAMES |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 12} | 4513 | ARGS_NAMES |
| 12 | files_names_mixed_case_filename_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4705 | FILES_NAMES |
| 12 | multipart_duplicate_field_names_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4703 | ARGS_NAMES |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor | {'403→200': 12} | 4610 | XML |
| 12 | phase4_auditlog_outbound_multiline_section_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 12} | 4910 | RESPONSE_BODY |
| 12 | sqli_like_keyword_spacing_probe | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4715 | ARGS:q |
| 12 | sqli_like_quote_encoding_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4716 | ARGS:q |
| 12 | unicode_double_encoded_uri_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4707 | REQUEST_URI |

## Top Connector-Only Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 2 | nginx_phase4_content_type_out_of_scope | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | 920002 | RESPONSE_BODY |
| 2 | nginx_phase4_minimal_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | 910001 | RESPONSE_BODY |
| 2 | nginx_phase4_safe_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | 910002 | RESPONSE_BODY |
| 2 | nginx_phase4_strict_connection_abort | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 2} | 910003 | RESPONSE_BODY |
| 2 | nginx_redirect_phase1_302 | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'302→200': 2} | 3302 | ARGS |
| 2 | nginx_tx_scoring_absolute_block | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 2} | 3101 | ARGS |
| 2 | nginx_tx_scoring_iterative_block | nginx | no-crs/with-mrts, with-crs/with-mrts | intervention_blocking | {'403→200': 2} | 3201 | ARGS |

## Recommendation
- Empfohlener nächster Fix-Cluster: `request_body_processor / multipart_files / xml_processor`
- Begründung: high combined volume, but likely multiple true processor gaps
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil large count but likely semantic; needs native/libmodsecurity comparison before fixes.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil classification-only: explicit nolog means the matching rule should not emit audit evidence.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action.
