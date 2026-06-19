> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:47:21Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-critical-batch-analysis.py`
> Make target: `generate-remaining-critical-batch-analysis`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# Remaining Critical Batch Analysis

## Official Before / After

| Metric | Before | After |
| --- | --- | --- |
| Total mismatches | 787 | 774 |
| Critical mismatches | 83 | 46 |
| Merge readiness | FAIL | FAIL |

## Cluster Ranking

| Rank | Cluster | Count | Connectors | Cases |
| --- | --- | --- | --- | --- |
| 1 | connector_capability_gap / phase-handling | 9 | apache, haproxy, nginx | phase1_vs_phase2_request_body_gap |
| 2 | expected_status_mismatch / actions | 6 | apache, haproxy, nginx | v3_secaction_block |
| 3 | expected_status_mismatch / response-body | 6 | nginx | phase4_response_body_empty_future_target, phase4_response_body_html_text_normalization_probe, response_body_basic_block |
| 4 | unknown / response-body | 6 | nginx | nginx_phase4_content_type_out_of_scope, nginx_phase4_minimal_log_only, nginx_phase4_safe_log_only |
| 5 | connector_capability_gap / audit-log | 4 | nginx | phase4_auditlog_outbound_escaped_value_gap, phase4_auditlog_outbound_message_connector_gap |
| 6 | expected_status_mismatch / audit-log | 4 | nginx | phase4_auditlog_outbound_multiline_section_gap, pr70_phase4_response_body_audit_xfail |
| 7 | runtime_regression / response-body | 4 | nginx | phase4_response_body_html_entity_decode_gap, phase4_response_body_unicode_runtime_difference |
| 8 | expected_status_mismatch / crs | 3 | apache, haproxy, nginx | crs_sqli_anomaly_block |
| 9 | runtime_regression / audit-log | 2 | nginx | phase4_auditlog_outbound_rule_id_runtime_difference |
| 10 | connector_capability_gap / response-body | 2 | nginx | phase4_response_body_chunk_assumption_connector_gap |

## Decisions

| Cluster | Decision | Rows | New Classification | Native Comparison | Full-Matrix Refresh Needed | Repro |
| --- | --- | --- | --- | --- | --- | --- |
| connector_capability_gap / body-processors / xml_namespace_edge_connector_gap | FIX_INPUT_REFRESH_REQUIRED | 12 | - | full_matrix_refresh_needed | no | `make verified-case CONNECTOR=nginx CASE=xml_namespace_edge_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / body-processors / xml_request_body_malformed_connector_gap | RECLASSIFY | 12 | libmodsecurity_xml_parser_semantics | native_comparison_complete | no | `make verified-case CONNECTOR=nginx CASE=xml_request_body_malformed_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / transformations / unicode_whitespace_normalization_gap | DEFER | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=unicode_whitespace_normalization_gap CRS=no-crs MRTS=no-mrts` |
| runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference | DEFER | 12 | - | native_comparison_missing | no | `make verified-case CONNECTOR=nginx CASE=unicode_double_encoded_uri_runtime_difference CRS=no-crs MRTS=no-mrts` |
| timeout_or_incomplete / transformations / v2_transformation_url_decode_invalid_sequence_mapped_candidate | FIX_INPUT_REFRESH_REQUIRED | 12 | - | runtime_reached_actual_match | no | `make verified-case CONNECTOR=haproxy CASE=v2_transformation_url_decode_invalid_sequence_mapped_candidate CRS=no-crs MRTS=no-mrts` |

## Native Comparison

| Case | Status | Evidence |
| --- | --- | --- |
| unicode_double_encoded_uri_runtime_difference | native_comparison_complete | native actual=200, expected=403; targeted connectors=apache:-, nginx:-, haproxy:-. |
| unicode_whitespace_normalization_gap | native_comparison_complete | native actual=200, expected=403; targeted connectors=apache:-, nginx:-, haproxy:-. |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | native_comparison_complete | native actual=403, expected=403; targeted connectors=apache:403, nginx:403, haproxy:403. |
| xml_namespace_edge_connector_gap | full_matrix_refresh_needed | native_comparison_complete: native actual=403, expected=403; targeted connectors=apache:403, nginx:403, haproxy:403; XML processor control present and XML:/* target matches. |
| xml_request_body_malformed_connector_gap | native_comparison_complete | runtime_reached_actual_mismatch: native actual=200, expected=403; targeted connectors=apache:200, nginx:200, haproxy:200; XML processor control present, but no native rule match/parser-error evidence, so malformed XML parser semantics remain deferred. |

## Targeted Repros

| Phase | Cluster | Case | Connector | Variant | Status | Runtime Classification | Actual | Rule | Matched Data | XML Processor Evidence | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-apache-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-nginx-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-haproxy-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-apache-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-nginx-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | /var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-haproxy-result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174008Z-apache-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174019Z-nginx-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4406 | - | - | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T174031Z-haproxy-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T175804Z-apache-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T175812Z-nginx-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4711 | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260618T175824Z-haproxy-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260619T062614Z-apache-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260619T062638Z-nginx-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | /var/tmp/ModSecurity-conector-verified/case-runs/20260619T062637Z-haproxy-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |

## Notes

- Full-matrix refresh needed: **False**.

- Reason: all affected Full-Matrix jobs ended after the YAML/input fixes

- Current official top critical cluster: `connector_capability_gap / phase-handling` (9).

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6934388824f6a335f3ffb3e8282b0c0ec98d28b3e466b9bce7266e9db3b5fcd4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `c8f7955fa9cad007f033b6c9a0aa8497595be59f409105d5f6cd74a35efa3c4a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `3f11d1fce15cdfa561cc96ef730cbd1b5604528e8f8a7fa8b2e7209629377e3b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `fdaa878e3a9e246ae057fe7b46c2208f20c4aa87cc7fbf1e679467bfcfe69d25` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f264523d6bb83b4a3382d4871099d221aac496d36dc8697548b4bba10fd2e52a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `e90c02f636c5b356c7db009eb39b4997c83b6db20d64fc90f796fec9ff3083e8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
