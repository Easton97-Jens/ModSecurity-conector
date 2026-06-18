> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:48:09Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Remaining Full-Matrix Failure Analysis

Generated at: `2026-06-18T17:48:09Z`

## Scope
- Connector Full-Matrix evidence is separate from Native MRTS infrastructure evidence.
- Native Apache/NGINX evidence is reported in the `mrts-native-*` reports and does not replace connector PASS/FAIL values.
- Native `100003-1` remains classified as `native_modsecurity_semantics / phase4_native_limitation`.
- This report is analysis-only; runtime PASS/FAIL and expected statuses are not changed by classification metadata.

## Summary
- Attempted/pass/fail/blocked/not executable: **3928 / 3141 / 775 / 0 / 12**
- Pending metadata rows observed: **2298**
- Unique remaining failure cases: **118**
- MRTS imported connector failures: **0**
- Non-MRTS framework failures: **775**

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
| with_mrts_detection_only_non_disruptive | 513 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay makes disruptive request-side rules non-blocking | low; report-only and not a connector blocking bug | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 72 | apache, nginx | fixable only through real strict abort/log evidence, not status-only changes | high if promoted without transport proof | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay suppresses disruptive action | low; report-only if kept separate from PASS promotion | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector capability gap unless a real abort mechanism is implemented and evidenced | high if faked; low if reported as gap | document connector gap unless implementation can prove a real hard abort |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | metadata-only semantic split; needs native/libmodsecurity comparison before any fix | medium to high | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 24 | apache, haproxy, nginx | classification-only; XML body exists but the fixture does not enable the XML request body processor | low if kept report-only; high if treated as connector runtime evidence | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| transformation_semantics | 12 | apache, haproxy, nginx | not a harness quick win; needs semantic comparison against libmodsecurity expectations | high | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| multipart_files | 6 | apache, haproxy, nginx | possibly fixable; likely connector/body parser evidence work | medium | compare multipart variable population across connectors with one representative request |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | classification-only; nolog/pass rule is absent from audit evidence and CRS noise is unrelated | low; no runtime or expected-status change | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report-only unless the case is meant to exercise strict hard abort | low if reported honestly, high if promoted as hard abort | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| connector_gap | 3 | apache, haproxy, nginx | unknown; review required | unknown | manual review |
| unknown_requires_review | 1 | haproxy | unknown; review required | unknown | manual review |

## Top 10 Overall Failure Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 66 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |

## Top 10 Apache Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | apache / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 22 | apache / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 16 | apache / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | apache / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | apache / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | apache / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | apache / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | apache / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 12 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |

## Top 10 NGINX Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 30 | nginx / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 24 | nginx / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | - | - |
| 22 | nginx / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | - | - |
| 22 | nginx / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | - | - |
| 20 | nginx / phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 16 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | - | - |
| 16 | nginx / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | - | - |
| 14 | nginx / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | - | - |
| 12 | nginx / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | - | - |

## Top 10 HAProxy Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 22 | haproxy / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 22 | haproxy / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 16 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | haproxy / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 16 | haproxy / phase4_connector_gap / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | haproxy / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 12 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |

## Top MRTS Imported Failures
- None.

## Top Non-MRTS Framework Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 66 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |

## Top Phase4 / Response-Body Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 28 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 22 | phase4_connector_gap / response-body / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_chunk_assumption_connector_gap | - | - |
| 20 | phase4_connector_gap / audit-log / phase:4 / 403→200 | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_message_connector_gap | - | - |
| 6 | phase4_log_only_no_abort / response-body / phase:4 / 200→200 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | - | - |

## Top Intervention / Blocking Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 72 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 66 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_empty_part_future_compatibility | 4706 | FILES |
| 66 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 48 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 44 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | - | - |
| 42 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 42 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 36 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 36 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |

## Top Cross-Connector Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4608 | ARGS_NAMES |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4607 | REQUEST_HEADERS_NAMES |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4513 | ARGS_NAMES |
| 12 | files_empty_part_future_compatibility | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_files | {'403→200': 12} | 4706 | FILES |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 12} | 4610 | XML |
| 12 | unicode_double_encoded_uri_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4707 | REQUEST_URI |
| 12 | unicode_whitespace_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 12} | 4708 | ARGS:q |
| 12 | v3_request_cookies_names_case_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4403 | REQUEST_COOKIES_NAMES |
| 12 | v3_request_headers_names_lowercase_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 12} | 4401 | REQUEST_HEADERS_NAMES |
| 12 | xml_deep_nesting_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 12} | 4712 | XML |

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
| 1 | operator_endswith_pass_no_match_phase2 | haproxy | with-crs/no-mrts | unknown_requires_review | {'200→503': 1} | 4503 | ARGS:q |

## Recommendation
- Empfohlener nächster Fix-Cluster: `multipart_files`
- Begründung: remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil large count but likely semantic; needs native/libmodsecurity comparison before fixes.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil classification-only: explicit nolog means the matching rule should not emit audit evidence.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action.
- Nicht als nächstes bearbeiten: `with_mrts_detection_only_non_disruptive`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action.
- Nicht als nächstes bearbeiten: `xml_processor_activation_missing`, weil classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML.
- Nicht als nächstes bearbeiten: `multipart_processor_activation_missing`, weil classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections.
- Nicht als nächstes bearbeiten: `collection_name_normalization_semantics`, weil metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `890da243b91305746a7f8658e29fd2e9f814b10a001885be834c69bed542dba2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `c1f815e949464f1ba593aaee1b2c5651739506c91f657fd9bc60ce817c76c73d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `a563b592cfaa69eba42d56c8653fdf35dabd612afed049e7a44125eed2ee2975` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `755c309851358ba542c968738f1aa22892b600fab94b6c7f44ef1181b4021f5a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `940591881d51212ec497a44480db3a4afa312e9f07dbeac2513fafd31865422b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `48f9f3e71041a9a865f438af408bf5196f56184aa0d07f60bab5e7b5c1e42a87` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `03bb0aefae70d11b6fdf0c7bdbf372bdfce9285c160a675deadc08ff526a01d3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `425f99fe2b96bf291a2c688f8dd34a4eb756f8c496aecb909b8ce996f616f5a8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
