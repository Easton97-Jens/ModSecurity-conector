> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T07:21:25Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `1e0c825de82d1325b5e7b070a4916de2f5af2207`
> Framework SHA: `unknown`
> Input status: `blocked`

# Remaining Full-Matrix Failure Analysis

Generated at: `2026-06-16T07:21:25Z`

## Scope
- Connector Full-Matrix evidence is separate from Native MRTS infrastructure evidence.
- Native Apache/NGINX evidence is reported in the `mrts-native-*` reports and does not replace connector PASS/FAIL values.
- Native `100003-1` remains classified as `native_modsecurity_semantics / phase4_native_limitation`.
- This report is analysis-only; runtime PASS/FAIL and expected statuses are not changed by classification metadata.

## Summary
- Attempted/pass/fail/blocked/not executable: **3928 / 2206 / 1650 / 0 / 72**
- Pending metadata rows observed: **2298**
- Unique remaining failure cases: **518**
- MRTS imported connector failures: **766**
- Non-MRTS framework failures: **884**

## Regression Checks
| Check | Status | Count | Cases |
|---|---|---|---|
| Unexpected BLOCKED entries | clear | 0 | - |
| Apache expected 200 -> actual 404 | clear | 0 | - |
| HAProxy expected 200 -> actual 501 | clear | 0 | - |
| NGINX actual status 500 | REGRESSION | 1138 | action_allow_phase1_pass, action_deny_phase1, action_deny_phase2, action_status_401_phase1_block, audit_log_empty_sections_future_target, audit_log_matched_var_encoded_value, audit_log_message_presence_connector_gap, audit_log_multiline_message_normalization, audit_log_phase1_block, audit_log_rule_id_presence_runtime_difference, collection_args_combined_size_block, collection_args_get_block, collection_args_names_block, crs_sqli_anomaly_block, duplicate_args_encoded_separator_edge, duplicate_cookie_name_runtime_difference, duplicate_header_case_normalization_gap, edge_missing_header_pass_through, edge_plus_vs_space_runtime_difference, edge_semicolon_query_args_names, files_names_mixed_case_filename_gap, json_duplicate_keys_runtime_difference, json_nested_object_future_compatibility, json_request_body_block, mrts_100000_mrts_002_args_a_get_100000_1 |
| MRTS classification incomplete | clear | 0 | - |

## Category Rollup
| Category | Count | Connectors | Fixable | Risk | Next step |
|---|---|---|---|---|---|
| unknown_requires_review | 665 | nginx | unknown; review required | unknown | manual review |
| with_mrts_detection_only_non_disruptive | 326 | apache, haproxy | classification-only; with-MRTS DetectionOnly overlay makes disruptive request-side rules non-blocking | low; report-only and not a connector blocking bug | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 294 | apache, nginx | fixable only through real strict abort/log evidence, not status-only changes | high if promoted without transport proof | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| transformation_semantics | 88 | apache, haproxy, nginx | not a harness quick win; needs semantic comparison against libmodsecurity expectations | high | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| response_header_mrts_detection_only | 56 | apache, haproxy, nginx | classification-only; with-MRTS DetectionOnly overlay suppresses disruptive action | low; report-only if kept separate from PASS promotion | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| multipart_files | 46 | nginx | possibly fixable; likely connector/body parser evidence work | medium | compare multipart variable population across connectors with one representative request |
| phase4_connector_gap | 46 | apache, haproxy, nginx | connector capability gap unless a real abort mechanism is implemented and evidenced | high if faked; low if reported as gap | document connector gap unless implementation can prove a real hard abort |
| xml_processor | 22 | nginx | possibly fixable, but high risk without XML processor parity checks | medium to high | verify XML processor enablement and malformed XML semantics |
| collection_name_normalization_semantics | 20 | apache, haproxy | metadata-only semantic split; needs native/libmodsecurity comparison before any fix | medium to high | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| request_body_processor | 20 | nginx | possibly fixable after processor-specific triage | medium | split JSON, URL-encoded, and XML body processor cases before code changes |
| xml_processor_activation_missing | 16 | apache, haproxy | classification-only; XML body exists but the fixture does not enable the XML request body processor | low if kept report-only; high if treated as connector runtime evidence | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| phase4_log_only_no_abort | 12 | nginx | report-only unless the case is meant to exercise strict hard abort | low if reported honestly, high if promoted as hard abort | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| response_header_backend_setup | 12 | nginx | likely harness/backend fix; add deterministic target response headers before judging connector parity | low to medium | add deterministic response headers to the Apache/NGINX harness/backend probes, then rerun targeted Phase 3 response-header cases |
| rule_chain_semantics | 10 | nginx | small but semantic; requires focused rule-chain evidence | medium | single-case rule-chain triage with logs |
| multipart_processor_activation_missing | 8 | apache, haproxy | classification-only; multipart body and boundary exist but the fixture does not enable request body access before expecting FILES/ARGS_NAMES collections | low if kept report-only; high if treated as connector multipart runtime evidence | keep Multipart processor activation-missing rows report-only; do not change bodies, rules, or Expected statuses |
| connector_gap | 5 | apache, haproxy, nginx | unknown; review required | unknown | manual review |
| nolog_expected_no_audit | 4 | apache, haproxy | classification-only; nolog/pass rule is absent from audit evidence and CRS noise is unrelated | low; no runtime or expected-status change | keep as classification-only evidence; do not add artificial audit logs |

## Top 10 Overall Failure Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 212 | phase4_missing_abort_evidence / mrts / phase:4 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | mrts_100003_mrts_002_args_a_get_100003_1 | 100003 | ARGS |
| 194 | unknown_requires_review / mrts / phase:2 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100001_mrts_002_args_a_get_100001_1 | 100001 | ARGS |
| 194 | unknown_requires_review / mrts / phase:3 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100002_mrts_002_args_a_get_100002_1 | 100002 | ARGS |
| 130 | unknown_requires_review / mrts / phase:1 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100000_mrts_002_args_a_get_100000_1 | 100000 | ARGS |
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 48 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 40 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 36 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 34 | transformation_semantics / transformations / phase:2 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | transformation_semantics | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 32 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |

## Top 10 Apache Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 20 | apache / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 18 | apache / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 16 | apache / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | apache / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | apache / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | apache / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | apache / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 12 | apache / with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 12 | apache / phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |

## Top 10 NGINX Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 212 | nginx / phase4_missing_abort_evidence / mrts / phase:4 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | mrts_100003_mrts_002_args_a_get_100003_1 | 100003 | ARGS |
| 194 | nginx / unknown_requires_review / mrts / phase:2 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100001_mrts_002_args_a_get_100001_1 | 100001 | ARGS |
| 194 | nginx / unknown_requires_review / mrts / phase:3 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100002_mrts_002_args_a_get_100002_1 | 100002 | ARGS |
| 130 | nginx / unknown_requires_review / mrts / phase:1 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100000_mrts_002_args_a_get_100000_1 | 100000 | ARGS |
| 34 | nginx / transformation_semantics / transformations / phase:2 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | transformation_semantics | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 28 | nginx / phase4_missing_abort_evidence / response-body / phase:4 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_strict_connection_abort | 910003 | RESPONSE_BODY |
| 22 | nginx / unknown_requires_review / collections / phase:1 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | runtime_difference | duplicate_header_case_normalization_gap | 4607 | REQUEST_HEADERS_NAMES |
| 22 | nginx / multipart_files / multipart / phase:2 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | multipart_files | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 20 | nginx / unknown_requires_review / operators / phase:2 / 200→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | operator_beginswith_pass_no_match_phase2 | 4502 | ARGS:q |
| 18 | nginx / unknown_requires_review / collections / phase:2 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | runtime_difference | duplicate_args_encoded_separator_edge | 4608 | ARGS_NAMES |

## Top 10 HAProxy Clusters
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 24 | haproxy / with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 20 | haproxy / with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 18 | haproxy / with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 16 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 16 | haproxy / response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 14 | haproxy / phase4_connector_gap / audit-log / phase:4 / 403→200 | haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 14 | haproxy / phase4_connector_gap / response-body / phase:4 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 14 | haproxy / with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 12 | haproxy / with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top MRTS Imported Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 212 | phase4_missing_abort_evidence / mrts / phase:4 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | mrts_100003_mrts_002_args_a_get_100003_1 | 100003 | ARGS |
| 194 | unknown_requires_review / mrts / phase:2 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100001_mrts_002_args_a_get_100001_1 | 100001 | ARGS |
| 194 | unknown_requires_review / mrts / phase:3 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100002_mrts_002_args_a_get_100002_1 | 100002 | ARGS |
| 130 | unknown_requires_review / mrts / phase:1 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100000_mrts_002_args_a_get_100000_1 | 100000 | ARGS |
| 8 | multipart_files / mrts / phase:1 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100148_mrts_061_request_filename_100148_1 | 100148 | - |
| 8 | multipart_files / mrts / phase:2 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100149_mrts_061_request_filename_100149_1 | 100149 | - |
| 8 | multipart_files / mrts / phase:3 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | operator_semantics | mrts_100150_mrts_061_request_filename_100150_1 | 100150 | - |
| 8 | phase4_missing_abort_evidence / mrts / phase:5 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | mrts_100153_mrts_069_response_body_100153_1 | 100153 | RESPONSE_BODY |
| 2 | xml_processor / mrts / phase:2 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | xml_processor | mrts_100154_mrts_110_xml_100154_1 | 100154 | XML |
| 2 | xml_processor / mrts / phase:3 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | runtime-difference | xml_processor | mrts_100155_mrts_110_xml_100155_1 | 100155 | XML |

## Top Non-MRTS Framework Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 48 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 40 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 36 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 34 | transformation_semantics / transformations / phase:2 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | runtime-difference | transformation_semantics | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 32 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 28 | phase4_missing_abort_evidence / response-body / phase:4 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_strict_connection_abort | 910003 | RESPONSE_BODY |
| 28 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 28 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 24 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |

## Top Phase4 / Response-Body Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 212 | phase4_missing_abort_evidence / mrts / phase:4 / 200→500 | nginx | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | mrts_100003_mrts_002_args_a_get_100003_1 | 100003 | ARGS |
| 28 | phase4_missing_abort_evidence / response-body / phase:4 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_strict_connection_abort | 910003 | RESPONSE_BODY |
| 18 | phase4_connector_gap / audit-log / phase:4 / 403→200 | apache, haproxy | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 16 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_matched_var_future | 4908 | RESPONSE_BODY |
| 16 | phase4_connector_gap / response-body / phase:4 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_chunk_assumption_connector_gap | 4808 | RESPONSE_BODY |
| 12 | phase4_log_only_no_abort / response-body / phase:4 / 200→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | nginx_phase4_content_type_out_of_scope | 920002 | RESPONSE_BODY |
| 12 | phase4_missing_abort_evidence / response-body / phase:4 / 403→200 | apache | no-crs/with-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_buffering_order_future_target | 4906 | RESPONSE_BODY |
| 10 | phase4_missing_abort_evidence / audit-log / phase:4 / 403→200 | apache | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_multiline_section_gap | 4910 | RESPONSE_BODY |
| 8 | phase4_connector_gap / audit-log / phase:4 / 403→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_auditlog_outbound_escaped_value_gap | - | - |
| 8 | phase4_missing_abort_evidence / response-body / phase:4 / 200→500 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | response-body-non-promoted | response_body_non_promoted | phase4_response_body_pass_no_match_experimental | 4905 | RESPONSE_BODY |

## Top Intervention / Blocking Failures
| Count | Cluster | Connectors | Variants | Classification | Work direction | Example | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|---|
| 48 | response_header_mrts_detection_only / response-headers / phase:3 / 403→200 | apache, haproxy, nginx | no-crs/with-mrts, with-crs/with-mrts | response-header-mrts-detection-only | response_header_mrts_detection_only | phase3_response_headers_content_type_charset_gap | 4902 | RESPONSE_HEADERS:Content-Type |
| 48 | with_mrts_detection_only_non_disruptive / transformations / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |
| 40 | with_mrts_detection_only_non_disruptive / body-processors / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | json_duplicate_keys_runtime_difference | 4710 | REQUEST_BODY |
| 36 | with_mrts_detection_only_non_disruptive / multipart / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | files_names_mixed_case_filename_gap | 4705 | FILES_NAMES |
| 32 | with_mrts_detection_only_non_disruptive / collections / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | duplicate_cookie_name_runtime_difference | 4606 | REQUEST_COOKIES_NAMES |
| 28 | with_mrts_detection_only_non_disruptive / collections / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | collection_args_combined_size_block | 2203 | ARGS_COMBINED_SIZE |
| 28 | with_mrts_detection_only_non_disruptive / operators / phase:2 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | v2_operator_begins_with_block | 3220 | ARGS:probe |
| 24 | with_mrts_detection_only_non_disruptive / audit-log / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | audit_log_empty_sections_future_target | 4605 | ARGS:a |
| 24 | with_mrts_detection_only_non_disruptive / transformations / phase:1 / 403→200 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with_mrts_detection_only_non_disruptive | classification_only | edge_plus_vs_space_runtime_difference | 4515 | REQUEST_URI |
| 20 | transformation_semantics / transformations / phase:2 / 403→200 | apache, haproxy | no-crs/no-mrts, with-crs/no-mrts | transformation_request_literal_no_match | transformation_semantics | sqli_like_keyword_spacing_probe | 4715 | ARGS:q |

## Top Cross-Connector Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 12 | duplicate_args_encoded_separator_edge | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 8, '403→500': 4} | 4608 | ARGS_NAMES |
| 12 | duplicate_header_case_normalization_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 8, '403→500': 4} | 4607 | REQUEST_HEADERS_NAMES |
| 12 | edge_semicolon_query_args_names | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | collection_name_normalization_semantics | {'403→200': 8, '403→500': 4} | 4513 | ARGS_NAMES |
| 12 | files_names_mixed_case_filename_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_processor_activation_missing | {'403→200': 8, '403→500': 4} | 4705 | FILES_NAMES |
| 12 | multipart_duplicate_field_names_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | multipart_processor_activation_missing | {'403→200': 8, '403→500': 4} | 4703 | ARGS_NAMES |
| 12 | parser_xml_partial_body_future_target | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | xml_processor_activation_missing | {'403→200': 8, '403→500': 4} | 4610 | XML |
| 12 | phase4_auditlog_outbound_multiline_section_gap | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→200': 8, '403→500': 4} | 4910 | RESPONSE_BODY |
| 12 | sqli_like_keyword_spacing_probe | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 8, '403→500': 4} | 4715 | ARGS:q |
| 12 | sqli_like_quote_encoding_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 8, '403→500': 4} | 4716 | ARGS:q |
| 12 | unicode_double_encoded_uri_runtime_difference | apache, haproxy, nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | transformation_semantics | {'403→200': 8, '403→500': 4} | 4707 | REQUEST_URI |

## Top Connector-Only Failures
| Count | Case | Connectors | Variants | Category | Status pairs | Rule ID | Variable/target |
|---|---|---|---|---|---|---|---|
| 4 | action_allow_phase1_pass | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 2103 | - |
| 4 | edge_missing_header_pass_through | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 4514 | REQUEST_HEADERS:X-Missing |
| 4 | nginx_phase4_content_type_out_of_scope | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→500': 4} | 920002 | RESPONSE_BODY |
| 4 | nginx_phase4_minimal_log_only | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→500': 4} | 910001 | RESPONSE_BODY |
| 4 | nginx_phase4_safe_log_only | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_log_only_no_abort | {'200→500': 4} | 910002 | RESPONSE_BODY |
| 4 | nginx_phase4_strict_connection_abort | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | phase4_missing_abort_evidence | {'403→500': 4} | 910003 | RESPONSE_BODY |
| 4 | operator_beginswith_pass_no_match_phase2 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 4502 | ARGS:q |
| 4 | operator_contains_pass_no_match_phase2 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 4501 | ARGS:q |
| 4 | operator_endswith_pass_no_match_phase2 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 4503 | ARGS:q |
| 4 | operator_rx_pass_no_match_phase2 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | unknown_requires_review | {'200→500': 4} | 4505 | ARGS:q |

## Recommendation
- Empfohlener nächster Fix-Cluster: `nginx_with_crs_with_mrts_http500_cluster`
- Begründung: largest verified Full-Matrix blocker; all HTTP-500 rows share the /index.html redirect-cycle/docroot-permission signature
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
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `9ba0e705e79616868c41e57959d7b80963efd1859039704bfa46aab2e9648fe5` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `58779ee2126c9f1c19a0b81db904eb56ecc73dd008f014bc2ec0e6ef83d96e81` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `e8549a2c62650e9b0ec761a461f61b7d2abb1af0be375f49116976f324bd35a3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `88ce8e4acd933ddb46d5f4f488190daf1de5c38dcdb6a2cd9cdb35b738c56e3e` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `3a396c14ab6c2d7e84b419d32fbc215193e99a47a6a37a5c7d1ea9a55482717e` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `54f4c92738c5271b21ac17bd65352499f65b467c8a0d4679e1ee331dbf81f897` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `95d3512364665627633d55db406e6d783652ac35f9a6ccad2cc08127c82dae78` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `be1eb6d091f6b266506cdbe9527f6b33f719d2b5772058e3fb616be78045a888` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
