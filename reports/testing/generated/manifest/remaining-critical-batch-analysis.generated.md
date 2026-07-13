> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:41:18Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-critical-batch-analysis.py`
> Make target: `generate-remaining-critical-batch-analysis`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
> Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
> Input status: `complete`

# Remaining Critical Batch Analysis

**Language:** English | [Deutsch](remaining-critical-batch-analysis.generated.de.md)

## Official Before / After

| Metric | Before | After |
| --- | --- | --- |
| Total mismatches | 787 | 771 |
| Critical mismatches | 83 | 0 |
| Merge readiness | FAIL | PASS |

## Cluster Ranking

| Rank | Cluster | Count | Connectors | Cases |
| --- | --- | --- | --- | --- |

_No rows available. Reason: no remaining critical mismatch clusters in the official report._

## Decisions

| Cluster | Decision | Rows | New Classification | Native Comparison | Full-Matrix Refresh Needed | Phase1 Body Gap | Phase2 Runtime | Connector Phase Gap | SecAction Runtime | SecAction Intervention | SecAction No Intervention | Native SecAction Same | Targeted Only | Repro |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| connector_capability_gap / phase-handling / phase1_vs_phase2_request_body_gap | FIX_INPUT_REFRESH_REQUIRED | 9 | - | native_phase_comparison_complete | no | yes | yes | no | - | - | - | - | yes | `make verified-case CONNECTOR=nginx CASE=phase1_vs_phase2_request_body_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / actions / v3_secaction_block | RECLASSIFY | 6 | secaction_detection_only_overlay | secaction_native_control_complete | no | - | - | - | yes | yes | yes | no-mrts only; with-mrts overlay intentionally differs | - | `make verified-case CONNECTOR=haproxy CASE=v3_secaction_block CRS=no-crs MRTS=with-mrts` |
| connector_capability_gap / body-processors / xml_namespace_edge_connector_gap | FIX_INPUT_REFRESH_REQUIRED | 12 | - | full_matrix_refresh_needed | no | - | - | - | - | - | - | - | - | `make verified-case CONNECTOR=nginx CASE=xml_namespace_edge_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / body-processors / xml_request_body_malformed_connector_gap | RECLASSIFY | 12 | libmodsecurity_xml_parser_semantics | native_comparison_complete | no | - | - | - | - | - | - | - | - | `make verified-case CONNECTOR=nginx CASE=xml_request_body_malformed_connector_gap CRS=no-crs MRTS=no-mrts` |
| expected_status_mismatch / transformations / unicode_whitespace_normalization_gap | DEFER | 12 | - | native_comparison_missing | no | - | - | - | - | - | - | - | - | `make verified-case CONNECTOR=nginx CASE=unicode_whitespace_normalization_gap CRS=no-crs MRTS=no-mrts` |
| runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference | DEFER | 12 | - | native_comparison_missing | no | - | - | - | - | - | - | - | - | `make verified-case CONNECTOR=nginx CASE=unicode_double_encoded_uri_runtime_difference CRS=no-crs MRTS=no-mrts` |
| timeout_or_incomplete / transformations / v2_transformation_url_decode_invalid_sequence_mapped_candidate | FIX_INPUT_REFRESH_REQUIRED | 12 | - | runtime_reached_actual_match | no | - | - | - | - | - | - | - | - | `make verified-case CONNECTOR=haproxy CASE=v2_transformation_url_decode_invalid_sequence_mapped_candidate CRS=no-crs MRTS=no-mrts` |

## Native Comparison

| Case | Status | Evidence |
| --- | --- | --- |
| phase1_vs_phase2_request_body_gap | native_phase_comparison_complete | native actual=403, expected=403; targeted connectors=apache:403, nginx:403, haproxy:403; phase 1 is a pass-only reachability marker and phase 2 REQUEST_BODY rule 4512 blocks. |
| unicode_double_encoded_uri_runtime_difference | native_comparison_complete | native actual=200, expected=403; targeted connectors=apache:-, nginx:-, haproxy:-. |
| unicode_whitespace_normalization_gap | native_comparison_complete | native actual=200, expected=403; targeted connectors=apache:-, nginx:-, haproxy:-. |
| v2_transformation_url_decode_invalid_sequence_mapped_candidate | native_comparison_complete | native actual=403, expected=403; targeted connectors=apache:403, nginx:403, haproxy:403. |
| v3_secaction_block | secaction_native_control_complete | native actual=403, expected=403; no-MRTS targeted connectors=apache:403, nginx:403, haproxy:403; with-MRTS targeted connectors=apache:200, nginx:200, haproxy:200. Native and no-MRTS block via SecAction rule 3312; with-MRTS loads MRTS_001_INIT ctl:ruleEngine=DetectionOnly, so disruptive SecAction is report-only. |
| xml_namespace_edge_connector_gap | full_matrix_refresh_needed | native_comparison_complete: native actual=403, expected=403; targeted connectors=apache:403, nginx:403, haproxy:403; XML processor control present and XML:/* target matches. |
| xml_request_body_malformed_connector_gap | native_comparison_complete | runtime_reached_actual_mismatch: native actual=200, expected=403; targeted connectors=apache:200, nginx:200, haproxy:200; XML processor control present, but no native rule match/parser-error evidence, so malformed XML parser semantics remain deferred. |

## Targeted Repros

| Phase | Cluster | Case | Connector | Variant | Status | Runtime Classification | Actual | Rule | Matched Data | XML Processor Evidence | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TARGETED | connector_capability_gap / phase-handling | phase1_vs_phase2_request_body_gap | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260619T101249Z-apache-phase1_vs_phase2_request_body_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / phase-handling | phase1_vs_phase2_request_body_gap | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260619T101257Z-nginx-phase1_vs_phase2_request_body_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / phase-handling | phase1_vs_phase2_request_body_gap | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4512 | - | - | <verified-run-root>/case-runs/20260619T101308Z-haproxy-phase1_vs_phase2_request_body_gap-no-crs-no-mrts/result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-apache-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-nginx-result.json |
| TARGETED | runtime_regression / transformations | unicode_double_encoded_uri_runtime_difference | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_double_encoded_uri_runtime_difference-haproxy-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-apache-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-nginx-result.json |
| TARGETED | expected_status_mismatch / transformations | unicode_whitespace_normalization_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/build/xml-unicode-transform-targeted-20260618/results/unicode_whitespace_normalization_gap-haproxy-result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260618T174008Z-apache-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260618T174019Z-nginx-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | timeout_or_incomplete / transformations | v2_transformation_url_decode_invalid_sequence_mapped_candidate | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4406 | - | - | <verified-run-root>/case-runs/20260618T174031Z-haproxy-v2_transformation_url_decode_invalid_sequence_mapped_candidate-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260619T102707Z-apache-v3_secaction_block-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | apache | no-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/case-runs/20260619T102710Z-apache-v3_secaction_block-no-crs-with-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | apache | with-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/case-runs/20260619T102721Z-apache-v3_secaction_block-with-crs-with-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260619T102731Z-nginx-v3_secaction_block-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | nginx | no-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/case-runs/20260619T102736Z-nginx-v3_secaction_block-no-crs-with-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | nginx | with-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | - | <verified-run-root>/case-runs/20260619T102747Z-nginx-v3_secaction_block-with-crs-with-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | - | <verified-run-root>/case-runs/20260619T102759Z-haproxy-v3_secaction_block-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | haproxy | no-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | 100028 | - | - | <verified-run-root>/case-runs/20260619T102801Z-haproxy-v3_secaction_block-no-crs-with-mrts/result.json |
| TARGETED | expected_status_mismatch / actions | v3_secaction_block | haproxy | with-crs/with-mrts | FAIL | runtime_reached_actual_mismatch | 200 | 920350 | - | - | <verified-run-root>/case-runs/20260619T102810Z-haproxy-v3_secaction_block-with-crs-with-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | apache | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260618T175804Z-apache-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | nginx | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | - | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260618T175812Z-nginx-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | connector_capability_gap / body-processors | xml_namespace_edge_connector_gap | haproxy | no-crs/no-mrts | PASS | runtime_reached_actual_match | 403 | 4711 | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260618T175824Z-haproxy-xml_namespace_edge_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | apache | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260619T062614Z-apache-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | nginx | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260619T062638Z-nginx-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |
| TARGETED | expected_status_mismatch / body-processors | xml_request_body_malformed_connector_gap | haproxy | no-crs/no-mrts | FAIL | runtime_reached_actual_mismatch | 200 | - | - | ctl:requestBodyProcessor=XML | <verified-run-root>/case-runs/20260619T062637Z-haproxy-xml_request_body_malformed_connector_gap-no-crs-no-mrts/result.json |

## Notes

- Full-matrix refresh needed: **False**.

- Reason: all affected Full-Matrix jobs ended after the YAML/input fixes

- Current official top critical cluster: `-` (-).

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `682daa5f4a31c9630b61a6bb5cc29090283acfdbfe6c37a3da83ce0008e437e1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `6a6d411311f909bc8dfa5b5f194ecffa5c41ac228894b68ca2d1b967469345f8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `401ad4822628cf5abd03471a376848f5bb77f4fab934c603cbcda42c89f60050` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `8e2d2ac2aff46856cd32e419ff73f333ce37a5321b15fad5f8b93bff85c1f16e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `cde00865dd00752f1a857c92f0f9db74adaa032921c7619bec174a9371034d23` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `2db466da1006f40605c3fbf9be46e8f370d486be124f3e288e573a1cff96a29f` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
