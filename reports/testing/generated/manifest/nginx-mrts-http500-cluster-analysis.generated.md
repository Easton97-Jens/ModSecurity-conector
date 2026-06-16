> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T07:20:52Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Make target: `generate-nginx-mrts-http500-cluster-analysis`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `1e0c825de82d1325b5e7b070a4916de2f5af2207`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `complete`

# NGINX with-crs/with-mrts HTTP-500 Cluster Analysis

## Summary

- Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
- Job: `nginx:with-crs:with-mrts`
- Primary blocker: `nginx_with_crs_with_mrts_http500_cluster`
- HTTP-500 failures: `510`
- Likely cause: NGINX worker cannot traverse /root-owned BUILD_ROOT parent; generated docroot is inaccessible, and try_files /index.html loops into HTTP 500.
- Classification: `harness_environment_error`; secondary `nginx_config_error`
- Confidence: `high`

## Cluster Counts

| Group | Count | Classification | Representative Cases |
| --- | --- | --- | --- |
| Other MRTS | 236 | crs_mrts_rule_interaction_secondary_harness_environment_error | `mrts_100000_mrts_002_args_a_get_100000_1`<br>`mrts_100000_mrts_002_args_a_get_100000_2`<br>`mrts_100000_mrts_002_args_a_get_100000_3` |
| MRTS request cookie/name | 125 | crs_mrts_rule_interaction_secondary_harness_environment_error | `v3_request_cookies_names_pass_no_match`<br>`v3_request_cookies_pass_no_match`<br>`v3_request_cookies_block` |
| Transformations / operators | 35 | harness_environment_error | `tfn_chain_lowercase_trim_pass_through`<br>`tfn_chain_urldecode_compress_whitespace_gap`<br>`operator_beginswith_pass_no_match_phase2` |
| Response body / phase 4 | 27 | response_body_phase4_bug_secondary_harness_environment_error | `pr70_phase4_response_body_audit_xfail`<br>`nginx_phase4_content_type_out_of_scope`<br>`nginx_phase4_minimal_log_only` |
| Request filename | 16 | crs_mrts_rule_interaction_secondary_harness_environment_error | `mrts_100148_mrts_061_request_filename_100148_1`<br>`mrts_100148_mrts_061_request_filename_100148_2`<br>`mrts_100148_mrts_061_request_filename_100148_3` |
| Collections / name handling | 15 | harness_environment_error | `duplicate_args_encoded_separator_edge`<br>`duplicate_cookie_name_runtime_difference`<br>`duplicate_header_case_normalization_gap` |
| Intervention / actions | 11 | intervention_handling_bug_secondary_harness_environment_error | `v3_action_nolog_pass_no_audit`<br>`nginx_redirect_phase1_302`<br>`nginx_tx_scoring_absolute_block` |
| Unknown | 11 | harness_environment_error | `audit_log_phase1_block`<br>`request_body_json_block`<br>`phase2_args_block` |
| Audit / intervention | 9 | intervention_handling_bug_secondary_harness_environment_error | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap` |
| Multipart | 9 | multipart_handling_bug_secondary_harness_environment_error | `files_names_mixed_case_filename_gap`<br>`multipart_basic_block`<br>`multipart_duplicate_field_names_gap` |
| Request body / parsers | 9 | harness_environment_error | `parser_json_partial_body_connector_gap`<br>`json_duplicate_keys_runtime_difference`<br>`json_nested_object_future_compatibility` |
| MRTS XML | 6 | xml_handling_bug_secondary_harness_environment_error | `parser_xml_partial_body_future_target`<br>`xml_request_body_block`<br>`xml_request_body_malformed_connector_gap` |
| Response headers / phase 3 | 1 | harness_environment_error | `phase3_response_headers_missing_pass_through` |

## Error Patterns

| Error Pattern | Count | Example | Affected Cases |
| --- | --- | --- | --- |
| modsecurity_crs_warning | 510 | 2026/06/16 04:53:46 [info] 1839142#0: *2 ModSecurity: Warning. Matched "Operator `Rx' with parameter `(?:^([\d.]+\|\[[\da-f:]+\]\|[\da-f:]+)(:[\d]+)?$)' against variable `REQUEST_HEADERS:Host' (Value: `127.0.0.1:28000' ) [ | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |
| docroot_directory_permission_denied | 510 | 2026/06/16 04:53:46 [crit] 1839142#0: *2 stat() "/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/audit_log_empty_sections_future_tar | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |
| nginx_crit_permission_denied | 510 | 2026/06/16 04:53:46 [crit] 1839142#0: *2 stat() "/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/audit_log_empty_sections_future_tar | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |
| docroot_index_permission_denied | 510 | 2026/06/16 04:53:46 [crit] 1839142#0: *2 stat() "/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/runtime/audit_log_empty_sections_future_tar | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |
| rewrite_internal_redirect_cycle_to_index | 510 | 2026/06/16 04:53:46 [error] 1839142#0: *2 rewrite or internal redirection cycle while internally redirecting to "/index.html", client: 127.0.0.1, server: localhost, request: "GET /?a=block HTTP/1.1", host: "127.0.0.1:280 | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |
| modsecurity_mrts_warning | 445 | 2026/06/16 04:54:29 [info] 1840427#0: *2 ModSecurity: Warning. Matched "Operator `Lt' with parameter `2' against variable `ARGS_COMBINED_SIZE' (Value: `' ) [file "/root/.local/state/ModSecurity-conector-build/mrts/upstre | `duplicate_cookie_name_runtime_difference`<br>`duplicate_header_case_normalization_gap`<br>`parser_json_partial_body_connector_gap`<br>`parser_xml_partial_body_future_target` |
| modsecurity_case_warning | 67 | 2026/06/16 04:53:46 [info] 1839142#0: *2 ModSecurity: Warning. Matched "Operator `StrEq' with parameter `block' against variable `ARGS:a' (Value: `block' ) [file "/root/.local/state/ModSecurity-conector-build/tmp/nginx-h | `audit_log_empty_sections_future_target`<br>`audit_log_matched_var_encoded_value`<br>`audit_log_message_presence_connector_gap`<br>`audit_log_multiline_message_normalization` |

## Representative Cases

| Case | Expected | Actual | Access | Error Pattern | Classification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `audit_log_empty_sections_future_target` | 403 | 500 | 500 | modsecurity_crs_warning, modsecurity_case_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | intervention_handling_bug_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/audit_log_empty_sections_future_target/result.json |
| `action_allow_phase1_pass` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, modsecurity_case_warning, docroot_directory_permission_denied | intervention_handling_bug_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/action_allow_phase1_pass/result.json |
| `duplicate_args_encoded_separator_edge` | 403 | 500 | 500 | modsecurity_crs_warning, docroot_directory_permission_denied, nginx_crit_permission_denied, docroot_index_permission_denied | harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/duplicate_args_encoded_separator_edge/result.json |
| `multipart_basic_block` | 403 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, modsecurity_case_warning, docroot_directory_permission_denied | multipart_handling_bug_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/multipart_basic_block/result.json |
| `response_body_basic_block` | 403 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | response_body_phase4_bug_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/response_body_basic_block/result.json |
| `mrts_100000_mrts_002_args_a_get_100000_1` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | crs_mrts_rule_interaction_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/mrts_100000_mrts_002_args_a_get_100000_1/result.json |
| `mrts_100116_mrts_059_request_cookies_100116_2` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | crs_mrts_rule_interaction_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/mrts_100116_mrts_059_request_cookies_100116_2/result.json |
| `mrts_100132_mrts_060_request_cookies_names_100132_2` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | crs_mrts_rule_interaction_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/mrts_100132_mrts_060_request_cookies_names_100132_2/result.json |
| `mrts_100148_mrts_061_request_filename_100148_1` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | crs_mrts_rule_interaction_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/mrts_100148_mrts_061_request_filename_100148_1/result.json |
| `mrts_100154_mrts_110_xml_100154_1` | 200 | 500 | 500 | modsecurity_crs_warning, modsecurity_mrts_warning, docroot_directory_permission_denied, nginx_crit_permission_denied | xml_handling_bug_secondary_harness_environment_error | /root/.local/state/ModSecurity-conector-build/tmp/nginx-harness/ModSecurity-conector-full-matrix/with-crs-with-mrts-nginx-28000/logs/mrts_100154_mrts_110_xml_100154_1/result.json |

## Root Cause Evidence

- 510 HTTP-500 rows have 'rewrite or internal redirection cycle while internally redirecting to "/index.html"'.
- 510 HTTP-500 rows have htdocs/index.html Permission denied in final-run error logs.
- namei shows /root is 0700 while NGINX worker user is nobody; generated files below it are otherwise readable.
- No segfault/core/module-load error pattern was observed in the final-run cluster.

## Minimal Repro

- Minimal case: `mrts_100000_mrts_002_args_a_get_100000_1`
- Existing producer reproducer: `VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600 make verified-full-matrix-job CONNECTOR=nginx CRS=with-crs MRTS=with-mrts`
- Target to add: `make verified-nginx-mrts-case CASE=mrts_100000_mrts_002_args_a_get_100000_1 CRS=with-crs MRTS=with-mrts`
- Notes: The connector harness supports TEST_CASE internally, but the verified full-matrix path does not yet expose a single-case target with CRS/MRTS setup and isolated job metadata.

## Fix Plan

| Fix | File/Path | Risk | Expected Effect | Needs New Verified Run |
| --- | --- | --- | --- | --- |
| Move verified NGINX Full-Matrix harness roots out from under /root or avoid overriding NGINX_HARNESS_WORK_ROOT with BUILD_ROOT/tmp. | ci/run-full-matrix-parallel.sh / Makefile NGINX_HARNESS_PARENT | medium | Eliminates docroot Permission denied and the 510-case /index.html redirect-cycle 500 cluster. | True |
| Add a readiness/permission preflight that blocks NGINX jobs when worker user cannot traverse DOCROOT parents. | connectors/nginx/harness/run_nginx_smoke.sh | low | Classifies future inaccessible-docroot evidence as BLOCKED instead of runtime FAIL. | True |
| Add a verified single-case Full-Matrix target for NGINX with CRS/MRTS setup and job metadata. | Makefile / ci/run-full-matrix-job.py | low | Provides minimal repro without rerunning the 524-case NGINX job. | False |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/job.json` | `01a74cbafdd3ffdc001a0037435a2a9f8328e4e79f4a12f9d4762e80c398b171` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` | `4f0e9c8f457e28365c361cf25b5c2bfdb481625c22ffd4739c5e7434314f567e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `6c1859588a5d1cff7ee5a6fd1c347f4629381bd6c6221e0c7978f0f072ef989e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `8efbce6ae1454ca86ce4d7f5fde168a47b78743b9a8fad525e84c972f5cf7e47` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `739639a9e9ad53d7f2e1478080ed78f868ff440a65dc3466ba321bd0295a565f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `13a80bd86eb41c43a4567eeae5f18fee50e649bde9f14abefa5416b1a68d7923` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | input file available |
