> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:18:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-critical-batch-analysis.py`
> Make target: `generate-remaining-critical-batch-analysis`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
> Input status: `complete`

# Remaining Critical Batch Analysis

## Official Before / After

| Metric | Before | After |
| --- | --- | --- |
| Total mismatches | 808 | 787 |
| Critical mismatches | 152 | 107 |
| Merge readiness | FAIL | FAIL |

## Cluster Ranking

| Rank | Cluster | Count | Connectors | Cases |
| --- | --- | --- | --- | --- |
| 1 | runtime_regression / transformations | 12 | apache, haproxy, nginx | unicode_double_encoded_uri_runtime_difference |
| 2 | expected_status_mismatch / transformations | 12 | apache, haproxy, nginx | unicode_whitespace_normalization_gap |
| 3 | timeout_or_incomplete / transformations | 12 | apache, haproxy, nginx | v2_transformation_url_decode_invalid_sequence_mapped_candidate |
| 4 | connector_capability_gap / body-processors | 12 | apache, haproxy, nginx | xml_namespace_edge_connector_gap |
| 5 | expected_status_mismatch / body-processors | 12 | apache, haproxy, nginx | xml_request_body_malformed_connector_gap |
| 6 | connector_capability_gap / phase-handling | 9 | apache, haproxy, nginx | phase1_vs_phase2_request_body_gap |
| 7 | expected_status_mismatch / actions | 6 | apache, haproxy, nginx | v3_secaction_block |
| 8 | expected_status_mismatch / response-body | 6 | nginx | phase4_response_body_empty_future_target, phase4_response_body_html_text_normalization_probe, response_body_basic_block |
| 9 | unknown / response-body | 6 | nginx | nginx_phase4_content_type_out_of_scope, nginx_phase4_minimal_log_only, nginx_phase4_safe_log_only |
| 10 | connector_capability_gap / audit-log | 4 | nginx | phase4_auditlog_outbound_escaped_value_gap, phase4_auditlog_outbound_message_connector_gap |
| 11 | expected_status_mismatch / audit-log | 4 | nginx | phase4_auditlog_outbound_multiline_section_gap, pr70_phase4_response_body_audit_xfail |
| 12 | runtime_regression / response-body | 4 | nginx | phase4_response_body_html_entity_decode_gap, phase4_response_body_unicode_runtime_difference |
| 13 | expected_status_mismatch / crs | 3 | apache, haproxy, nginx | crs_sqli_anomaly_block |
| 14 | runtime_regression / audit-log | 2 | nginx | phase4_auditlog_outbound_rule_id_runtime_difference |
| 15 | connector_capability_gap / response-body | 2 | nginx | phase4_response_body_chunk_assumption_connector_gap |

## Decisions

| Cluster | Decision | Rows | New Classification | Full-Matrix Refresh Needed |
| --- | --- | --- | --- | --- |
| connector_capability_gap / collections / duplicate_header_case_normalization_gap | RECLASSIFY | 12 | libmodsecurity_collection_name_case_semantics | no |
| timeout_or_incomplete / body-processors / json_empty_body_future_compatibility | FIX | 12 | - | no |
| timeout_or_incomplete / response-headers / phase3_response_headers_server_presence_pending | FIX | 12 | - | no |
| timeout_or_incomplete / response-body / phase4_response_body_empty_future_target | FIX_AND_DOCUMENT | 12 | - | no |
| connector_capability_gap / transformations / unicode_whitespace_normalization_gap | FIX_INPUT_AND_DEFER_CLASSIFICATION | 12 | - | no |
| runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference | DEFER | 12 | - | no |

## Targeted Repros

| Phase | Cluster | Case | Connector | Variant | Status | Actual | Rule | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BEFORE | connector_capability_gap / collections | duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/duplicate_header_case_normalization_gap-apache.log |
| BEFORE | connector_capability_gap / collections | duplicate_header_case_normalization_gap | nginx | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/duplicate_header_case_normalization_gap-nginx.log |
| BEFORE | connector_capability_gap / collections | duplicate_header_case_normalization_gap | haproxy | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/duplicate_header_case_normalization_gap-haproxy.log |
| AFTER | targeted YAML/input fix | json_empty_body_future_compatibility | apache | no-crs/no-mrts | PASS | 403 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/json_empty_body_future_compatibility-apache-result.json |
| AFTER | targeted YAML/input fix | json_empty_body_future_compatibility | nginx | no-crs/no-mrts | PASS | 403 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/json_empty_body_future_compatibility-nginx-result.json |
| AFTER | targeted YAML/input fix | json_empty_body_future_compatibility | haproxy | no-crs/no-mrts | PASS | 403 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/json_empty_body_future_compatibility-haproxy-result.json |
| AFTER | targeted YAML/input fix | phase3_response_headers_server_presence_pending | apache | no-crs/no-mrts | PASS | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase3_response_headers_server_presence_pending-apache-result.json |
| AFTER | targeted YAML/input fix | phase3_response_headers_server_presence_pending | nginx | no-crs/no-mrts | PASS | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase3_response_headers_server_presence_pending-nginx-result.json |
| AFTER | targeted YAML/input fix | phase3_response_headers_server_presence_pending | haproxy | no-crs/no-mrts | PASS | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase3_response_headers_server_presence_pending-haproxy-result.json |
| AFTER | targeted YAML/input fix | phase4_response_body_empty_future_target | apache | no-crs/no-mrts | PASS | 403 | 4806 | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase4_response_body_empty_future_target-apache-result.json |
| AFTER | targeted YAML/input fix | phase4_response_body_empty_future_target | nginx | no-crs/no-mrts | FAIL | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase4_response_body_empty_future_target-nginx-result.json |
| AFTER | targeted YAML/input fix | phase4_response_body_empty_future_target | haproxy | no-crs/no-mrts | PASS | 403 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/phase4_response_body_empty_future_target-haproxy-result.json |
| AFTER | targeted YAML/input fix | unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | FAIL | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/unicode_whitespace_normalization_gap-apache-result.json |
| AFTER | targeted YAML/input fix | unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | FAIL | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/unicode_whitespace_normalization_gap-nginx-result.json |
| AFTER | targeted YAML/input fix | unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | FAIL | 200 | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after/unicode_whitespace_normalization_gap-haproxy-result.json |
| BEFORE | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/unicode_double_encoded_uri_runtime_difference-apache.log |
| BEFORE | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/unicode_double_encoded_uri_runtime_difference-nginx.log |
| BEFORE | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | FAIL_RC_2 | - | - | /var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted/unicode_double_encoded_uri_runtime_difference-haproxy.log |

## Notes

- Full-matrix refresh needed: **False**.

- Reason: all affected Full-Matrix jobs ended after the YAML/input fixes

- Current official top critical cluster: `runtime_regression / transformations` (12).

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `509bc6777259ded64851696daa44ebc1785e6850d74245f62002fca00b89d4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `3e783fdfa68caf8ca8bd1de7dc8cd107e2ac9b27e6d939f661137e574b081113` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `b9194afc316f2d929797e37a5101384b565efdb1809b7409d92866de4dfdd7cc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `94ef7376661e451a7c3a25bd98cb9b769096cd64fe85684fa62e6cef951a017e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `05bc958c83d0fba9f7991380580343ddbe984c2e25b5cd856adc79de70f55828` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `4aec42cd1ad41e7d8f3aeff9311774b32f29c12aca6fccc73468054dd890c6a2` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
