> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T11:29:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-critical-batch-analysis.py`
> Make target: `generate-remaining-critical-batch-analysis`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `1ed85089212c791958b5f09abf7b17d73bdfde91`
> Framework SHA: `9e2c82b829036d28f54459814773b92c801b6e24`
> Input status: `complete`

# Remaining Critical Batch Analysis

## Official Before / After

| Metric | Before | After |
| --- | --- | --- |
| Total mismatches | 824 | 808 |
| Critical mismatches | 216 | 152 |
| Merge readiness | FAIL | FAIL |

## Cluster Ranking

| Rank | Cluster | Count | Connectors | Cases |
| --- | --- | --- | --- | --- |
| 1 | connector_capability_gap / collections | 12 | apache, haproxy, nginx | duplicate_header_case_normalization_gap |
| 2 | timeout_or_incomplete / body-processors | 12 | apache, haproxy, nginx | json_empty_body_future_compatibility |
| 3 | timeout_or_incomplete / response-headers | 12 | apache, haproxy, nginx | phase3_response_headers_server_presence_pending |
| 4 | timeout_or_incomplete / response-body | 12 | apache, haproxy, nginx | phase4_response_body_empty_future_target |
| 5 | runtime_regression / transformations | 12 | apache, haproxy, nginx | unicode_double_encoded_uri_runtime_difference |
| 6 | connector_capability_gap / transformations | 12 | apache, haproxy, nginx | unicode_whitespace_normalization_gap |
| 7 | timeout_or_incomplete / transformations | 12 | apache, haproxy, nginx | v2_transformation_url_decode_invalid_sequence_mapped_candidate |
| 8 | connector_capability_gap / body-processors | 12 | apache, haproxy, nginx | xml_namespace_edge_connector_gap |
| 9 | expected_status_mismatch / body-processors | 12 | apache, haproxy, nginx | xml_request_body_malformed_connector_gap |
| 10 | connector_capability_gap / phase-handling | 9 | apache, haproxy, nginx | phase1_vs_phase2_request_body_gap |
| 11 | expected_status_mismatch / actions | 6 | apache, haproxy, nginx | v3_secaction_block |
| 12 | unknown / response-body | 6 | nginx | nginx_phase4_content_type_out_of_scope, nginx_phase4_minimal_log_only, nginx_phase4_safe_log_only |
| 13 | connector_capability_gap / audit-log | 4 | nginx | phase4_auditlog_outbound_escaped_value_gap, phase4_auditlog_outbound_message_connector_gap |
| 14 | expected_status_mismatch / audit-log | 4 | nginx | phase4_auditlog_outbound_multiline_section_gap, pr70_phase4_response_body_audit_xfail |
| 15 | runtime_regression / response-body | 4 | nginx | phase4_response_body_html_entity_decode_gap, phase4_response_body_unicode_runtime_difference |

## Decisions

| Cluster | Decision | Rows | New Classification | Full-Matrix Refresh Needed |
| --- | --- | --- | --- | --- |
| expected_status_mismatch / collections | RECLASSIFY | 24 | libmodsecurity_collection_name_case_semantics | no |
| multipart_files | FIX | 24 | - | no |
| runtime_regression / audit-log | FIX_AND_DOCUMENT | 14 | - | no |
| runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference | DEFER | 12 | - | no |
| unknown / actions / v3_action_nolog_pass_no_audit | RECLASSIFY | 6 | nolog_expected_no_audit | no |

## Targeted Repros

| Cluster | Case | Connector | Variant | Status | Actual | Rule | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| multipart_files | files_names_mixed_case_filename_gap | apache | no-crs/no-mrts | PASS | 403 | None | /var/tmp/ModSecurity-conector-verified/build/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json |
| multipart_files | files_names_mixed_case_filename_gap | nginx | no-crs/no-mrts | PASS | 403 | None | /var/tmp/ModSecurity-conector-verified/build/verified-nginx-case/no-crs-no-mrts-nginx/logs/files_names_mixed_case_filename_gap/result.json |
| multipart_files | files_names_mixed_case_filename_gap | haproxy | no-crs/no-mrts | PASS | - | - | command-output |
| multipart_files | multipart_duplicate_field_names_gap | apache | no-crs/no-mrts | PASS | 403 | None | /var/tmp/ModSecurity-conector-verified/build/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json |
| multipart_files | multipart_duplicate_field_names_gap | nginx | no-crs/no-mrts | PASS | 403 | None | /var/tmp/ModSecurity-conector-verified/build/verified-nginx-case/no-crs-no-mrts-nginx/logs/multipart_duplicate_field_names_gap/result.json |
| multipart_files | multipart_duplicate_field_names_gap | haproxy | no-crs/no-mrts | PASS | - | - | command-output |
| audit-log | phase4_auditlog_outbound_multiline_section_gap | apache | no-crs/no-mrts | PASS | 403 | 4910 | /var/tmp/ModSecurity-conector-verified/build/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json |
| audit-log | phase4_auditlog_outbound_multiline_section_gap | nginx | no-crs/no-mrts | FAIL | 200 | None | /var/tmp/ModSecurity-conector-verified/build/verified-nginx-case/no-crs-no-mrts-nginx/logs/phase4_auditlog_outbound_multiline_section_gap/result.json |
| audit-log | phase4_auditlog_outbound_multiline_section_gap | haproxy | no-crs/no-mrts | PASS | 403 | None | /var/tmp/ModSecurity-conector-verified/build/verified-haproxy-case/no-crs-no-mrts-haproxy/logs/haproxy-runtime/result.json |

## Notes

- Full-matrix refresh needed: **False**.

- Reason: Fresh Full-Matrix artifacts exist for the 12 affected connector/CRS/MRTS jobs; remaining rows are current official mismatches, not stale targeted-only evidence.

- Current official top critical cluster: `connector_capability_gap / collections` (12).

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `f0b86c64ce32e2bd1ff2a56c6242f01f8d01f8fa4af0fd2801772622c3b62d4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `e80586d1d046b64eea92983702e8affa4b1a75d646784b0699692e6ec4fd8e45` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `151fed6d47dda6380e0ece49684d4a9c333f464846e3810c5466cbdab5f72950` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `8cbf4ad7816be93d057616a8e2dba7146906c56f5e93e4202318b78607b91781` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `8199f2813c853163a3eddd848421bb327eacf6d75cc1a9e032d1943f5a2112fb` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
