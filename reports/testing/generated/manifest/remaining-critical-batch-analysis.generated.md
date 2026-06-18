> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:49:20Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-critical-batch-analysis.py`
> Make target: `generate-remaining-critical-batch-analysis`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Remaining Critical Batch Analysis

## Official Before / After

| Metric | Before | After |
| --- | --- | --- |
| Total mismatches | 787 | 787 |
| Critical mismatches | 83 | 83 |
| Merge readiness | FAIL | FAIL |

## Cluster Ranking

| Rank | Cluster | Count | Connectors | Cases |
| --- | --- | --- | --- | --- |
| 1 | timeout_or_incomplete / transformations | 12 | apache, haproxy, nginx | v2_transformation_url_decode_invalid_sequence_mapped_candidate |
| 2 | connector_capability_gap / body-processors | 12 | apache, haproxy, nginx | xml_namespace_edge_connector_gap |
| 3 | expected_status_mismatch / body-processors | 12 | apache, haproxy, nginx | xml_request_body_malformed_connector_gap |
| 4 | connector_capability_gap / phase-handling | 9 | apache, haproxy, nginx | phase1_vs_phase2_request_body_gap |
| 5 | expected_status_mismatch / actions | 6 | apache, haproxy, nginx | v3_secaction_block |
| 6 | expected_status_mismatch / response-body | 6 | nginx | phase4_response_body_empty_future_target, phase4_response_body_html_text_normalization_probe, response_body_basic_block |
| 7 | unknown / response-body | 6 | nginx | nginx_phase4_content_type_out_of_scope, nginx_phase4_minimal_log_only, nginx_phase4_safe_log_only |
| 8 | connector_capability_gap / audit-log | 4 | nginx | phase4_auditlog_outbound_escaped_value_gap, phase4_auditlog_outbound_message_connector_gap |
| 9 | expected_status_mismatch / audit-log | 4 | nginx | phase4_auditlog_outbound_multiline_section_gap, pr70_phase4_response_body_audit_xfail |
| 10 | runtime_regression / response-body | 4 | nginx | phase4_response_body_html_entity_decode_gap, phase4_response_body_unicode_runtime_difference |
| 11 | expected_status_mismatch / crs | 3 | apache, haproxy, nginx | crs_sqli_anomaly_block |
| 12 | runtime_regression / audit-log | 2 | nginx | phase4_auditlog_outbound_rule_id_runtime_difference |
| 13 | connector_capability_gap / response-body | 2 | nginx | phase4_response_body_chunk_assumption_connector_gap |
| 14 | framework_expected_behavior_gap / operators | 1 | haproxy | operator_endswith_pass_no_match_phase2 |

## Decisions

| Cluster | Decision | Rows | New Classification | Native Comparison | Full-Matrix Refresh Needed | Repro |
| --- | --- | --- | --- | --- | --- | --- |
| connector_capability_gap / body-processors / xml_namespace_edge_connector_gap | DOCUMENT | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=xml_namespace_edge_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / body-processors / xml_request_body_malformed_connector_gap | DEFER | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=xml_request_body_malformed_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / transformations / unicode_whitespace_normalization_gap | DEFER | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=unicode_whitespace_normalization_gap CRS=no-crs MRTS=no-mrts` |
| runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference | DEFER | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=unicode_double_encoded_uri_runtime_difference CRS=no-crs MRTS=no-mrts` |
| timeout_or_incomplete / transformations / v2_transformation_url_decode_invalid_sequence_mapped_candidate | FIX_INPUT_REFRESH_REQUIRED | 12 | - | runtime_reached_actual_match | yes | `make verified-case CONNECTOR=haproxy CASE=v2_transformation_url_decode_invalid_sequence_mapped_candidate CRS=no-crs MRTS=no-mrts` |

## Native Comparison

| Case | Status | Evidence |
| --- | --- | --- |
| unicode_double_encoded_uri_runtime_difference | native_comparison_missing | Existing reports/testing/generated/mrts-native artifacts cover the MRTS native suite; no direct native/libmodsecurity control artifact exists for this framework case. |
| unicode_whitespace_normalization_gap | native_comparison_missing | Existing reports/testing/generated/mrts-native artifacts cover the MRTS native suite; no direct native/libmodsecurity control artifact exists for this framework case. |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | runtime_reached_actual_match | Targeted connector repros now execute to HTTP 403; native comparison is no longer blocked by fixture syntax. |
| xml_namespace_edge_connector_gap | native_comparison_missing | Existing reports/testing/generated/mrts-native artifacts cover the MRTS native suite; no direct native/libmodsecurity control artifact exists for this framework case. |
| xml_request_body_malformed_connector_gap | native_comparison_missing | Existing reports/testing/generated/mrts-native artifacts cover the MRTS native suite; no direct native/libmodsecurity control artifact exists for this framework case. |

## Targeted Repros

| Phase | Cluster | Case | Connector | Variant | Status | Runtime Classification | Actual | Rule | Matched Data | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-apache-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-nginx-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-haproxy-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-apache-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-nginx-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-haproxy-result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174008Z-apache-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174019Z-nginx-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4406 | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174031Z-haproxy-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_namespace_edge_connector_gap-apache-result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_namespace_edge_connector_gap-nginx-result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_namespace_edge_connector_gap-haproxy-result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_request_body_malformed_connector_gap-apache-result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_request_body_malformed_connector_gap-nginx-result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/xml_request_body_malformed_connector_gap-haproxy-result.json |

## Notes

- Full-matrix refresh needed: **True**.

- Reason: one or more affected Full-Matrix jobs are stale or missing

- Current official top critical cluster: `timeout_or_incomplete / transformations` (12).

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `06ccc48b304f836f75d06b5343edae8e966492cdc91bb13e3cfef4f62159bc49` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `d595d61d381d4fdf27481ac8ae6bf61f40a2070b6ef63b7c016b2a4923ca7ed8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `0df0accb88ed8f025ce283acc22ab0f792b49b29a74bdbc71b71edf35e764e4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `890da243b91305746a7f8658e29fd2e9f814b10a001885be834c69bed542dba2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `23d490410f677c4d0c3705b1a2315860fbb6c1275c94a8c085bc4c23c3918ca8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `dc80194255be5520bb8d5768e95f9b0990ae0256bf9264458ac1b5449be5e600` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
