# Remaining Full-Matrix Failure Analysis

Generated at: `2026-06-14T19:39:20Z`

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
| with_mrts_detection_only_non_disruptive | 495 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay makes disruptive request-side rules non-blocking | low; report-only and not a connector blocking bug | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 68 | apache, nginx | fixable only through real strict abort/log evidence, not status-only changes | high if promoted without transport proof | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay suppresses disruptive action | low; report-only if kept separate from PASS promotion | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector capability gap unless a real abort mechanism is implemented and evidenced | high if faked; low if reported as gap | document connector gap unless implementation can prove a real hard abort |
| transformation_semantics | 36 | apache, haproxy, nginx | not a harness quick win; needs semantic comparison against libmodsecurity expectations | high | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | metadata-only semantic split; needs native/libmodsecurity comparison before any fix | medium to high | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 24 | apache, haproxy, nginx | classification-only; XML body exists but the fixture does not enable the XML request body processor | low if kept report-only; high if treated as connector runtime evidence | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| multipart_processor_activation_missing | 12 | apache, haproxy, nginx | classification-only; multipart body and boundary exist but the fixture does not enable request body access before expecting FILES/ARGS_NAMES collections | low if kept report-only; high if treated as connector multipart runtime evidence | keep Multipart processor activation-missing rows report-only; do not change bodies, rules, or Expected statuses |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | classification-only; nolog/pass rule is absent from audit evidence and CRS noise is unrelated | low; no runtime or expected-status change | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report-only unless the case is meant to exercise strict hard abort | low if reported honestly, high if promoted as hard abort | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| connector_gap | 3 | apache, haproxy, nginx | unknown; review required | unknown | manual review |

## Top 10 Overall Failure Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 54 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | - | - |

## Top 10 Apache Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 20 | apache / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 18 | apache / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 16 | apache / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 16 | apache / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 14 | apache / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 14 | apache / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 12 | apache / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |
| 12 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | - | - |
| 12 | apache / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |

## Top 10 NGINX Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 26 | nginx / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 24 | nginx / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 20 | nginx / phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 20 | nginx / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 18 | nginx / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 16 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 16 | nginx / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 12 | nginx / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |

## Top 10 HAProxy Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 20 | haproxy / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 18 | haproxy / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 16 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 16 | haproxy / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 14 | haproxy / phase4_connector_gap / audit-log / phase:4 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | - | - |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 14 | haproxy / phase4_connector_gap / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 12 | haproxy / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |

## Top MRTS Imported Failures
- None.

## Top Non-MRTS Framework Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 54 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | - | - |

## Top Phase4 / Response-Body Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 30 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | - | - |
| 22 | phase4_connector_gap / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_message_connector_gap | - | - |
| 20 | phase4_connector_gap / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_chunk_assumption_connector_gap | - | - |
| 6 | phase4_log_only_no_abort / response-body / phase:4 / 200→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | - | - |

## Top Intervention / Blocking Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 60 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 54 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | - | - |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 38 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | - | - |

## Top Cross-Connector Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | - | - |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | - | - |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | - | - |
| 12 | files_names_mixed_case_filename_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_processor_activation_missing | {'403→200': 12} | - | - |
| 12 | multipart_duplicate_field_names_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_processor_activation_missing | {'403→200': 12} | - | - |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 12} | - | - |
| 12 | phase4_auditlog_outbound_multiline_section_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 12} | - | - |
| 12 | sqli_like_keyword_spacing_probe | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | - | - |
| 12 | sqli_like_quote_encoding_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | - | - |
| 12 | unicode_double_encoded_uri_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | - | - |

## Top Connector-Only Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 2 | nginx_phase4_content_type_out_of_scope | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_minimal_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_safe_log_only | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→200': 2} | - | - |
| 2 | nginx_phase4_strict_connection_abort | nginx | no-crs/with-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 2} | - | - |
| 2 | nginx_redirect_phase1_302 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'302→200': 2} | - | - |
| 2 | nginx_tx_scoring_absolute_block | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'403→200': 2} | - | - |
| 2 | nginx_tx_scoring_iterative_block | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | {'403→200': 2} | - | - |

## Recommendation
- Empfohlener nächster Fix-Cluster: `none`
- Begründung: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil large count but likely semantic; needs native/libmodsecurity comparison before fixes.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil classification-only: explicit nolog means the matching rule should not emit audit evidence.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action.
- Nicht als nächstes bearbeiten: `with_mrts_detection_only_non_disruptive`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action.
- Nicht als nächstes bearbeiten: `xml_processor_activation_missing`, weil classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML.
- Nicht als nächstes bearbeiten: `multipart_processor_activation_missing`, weil classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections.
- Nicht als nächstes bearbeiten: `collection_name_normalization_semantics`, weil metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes.
