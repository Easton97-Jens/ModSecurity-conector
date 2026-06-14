Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Overview

## Summary
- Total cases: **141**
- Verified/pass count (`runtime_verified=true`): **0**
- Current XFAIL count: **0**
- Former XFAIL cases tracked: **80**
- Pending runtime verification count: **11**
- Connector-gap count: **11**
- Runtime-difference count: **13**
- Future/experimental count: **17**
- RESPONSE_BODY cases: **24** (still **not verified/promoted**)
- Mapped-only import inventory entries: **10**

## Coverage By Variable / Collection
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 20 |
| `ARGS:q` | 18 |
| `REQUEST_BODY` | 10 |
| `ARGS_NAMES` | 7 |
| `REQUEST_URI` | 7 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `ARGS:a` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `XML` | 4 |
| `ARGS:param1` | 4 |
| `ARGS` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `ARGS:probe` | 4 |
| `MULTIPART_FILENAME` | 3 |
| `ARGS:chain_a` | 3 |
| `ARGS:chain_b` | 3 |
| `FILES_NAMES` | 2 |
| `TX:SCORE` | 2 |
| `REQUEST_COOKIES:USER_TOKEN` | 2 |

## Coverage By Phase
| Phase | Count |
|---|---:|
| 1 | 36 |
| 2 | 74 |
| 3 | 12 |
| 4 | 20 |

## Coverage By Status
| Status | Count |
|---|---:|
| active | 8 |
| imported | 133 |

## Coverage By Scope
| Scope | Count |
|---|---:|
| common | 134 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Runtime Matrix Status
- Default runtime-executable YAML cases: **61**
- Force-all runtime-executable YAML cases: **141**
- Apache attempted YAML cases from default summary: **54**
- NGINX attempted YAML cases from default summary: **60**
- HAProxy attempted YAML cases from default summary: **54**
- Apache attempted YAML cases from force-all summary: **516**
- NGINX attempted YAML cases from force-all summary: **140**
- HAProxy attempted YAML cases from force-all summary: **133**
- Apache force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **183** / **327** / **0** / **6**
- NGINX force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **67** / **67** / **0** / **6**
- HAProxy force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **104** / **23** / **0** / **6**
| Status | Apache | NGINX | HAProxy |
|---|---:|---:|---:|
| PASS | 10 | 10 | 10 |
| FAIL | 44 | 50 | 44 |
| NOT_EXECUTABLE | 87 | 81 | 87 |
| MAPPED_ONLY | 10 | 10 | 10 |
- Details: `reports/testing/generated/runtime-matrix.generated.md`
- HAProxy per-case results: `reports/testing/generated/haproxy-runtime-results.generated.md`

## MRTS Native Infrastructure Evidence
- Apache native: `reports/testing/generated/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | Repository lint checks passed |
| make generate-test-matrix | PASS | Generated coverage docs refreshed from current metadata |
| make check-test-matrix | FAIL | Exited 2 in this uncommitted working tree because generated reports differ from HEAD after the HAProxy matrix updates |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile modules/ModSecurity-test-Framework/tests/normalizers/*.py modules/ModSecurity-test-Framework/tests/runners/*.py modules/ModSecurity-test-Framework/ci/*.py | PASS | Framework Python files compiled through the connector module path |
| sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | POSIX shell syntax check passed for connector integration shell scripts |
| bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh | PASS | Bash syntax check passed for connector integration shell scripts |
| git diff --check | PASS | No whitespace errors reported |
| diff -u /tmp/pre-connector.diff /tmp/post-connector.diff | PASS | Connector source diff snapshot is unchanged; no new connector source changes were introduced |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | BLOCKED | Non-zero because connectors/apache/src/mod_security3.c had a pre-existing unrelated local change before this fix; the pre/post connector diff snapshot is unchanged |
| git ls-files .venv | PASS | No tracked .venv files |

## Readiness / Fetch Status
| Command | Status | Details |
|---|---|---|
| make fetch-deps | NOT_RUN | Not rerun during the framework-module migration; runtime-matrix-all used the configured local source tree and build output location |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity readiness remains diagnostic only and is not required for source-build smokes |
| make runtime-matrix-all | PASS | Force-all matrix orchestration completed and recorded Apache/NGINX per-case evidence; expected runtime FAILs remain evidence and are not PASS promotions |

## Runtime Smoke Status
- Snapshot: **2026-06-10** (2026-06-10 16:58:51 CEST)
- Git: branch `integrate-new-connectors-local`, commit `48bdd28`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- Snapshot file: `reports/testing/runtime-validation-snapshot.json`

### Default Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | make smoke-apache | FAIL | 2 | 54 | 10 | 44 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json |
| nginx | make smoke-nginx | FAIL | 2 | 60 | 10 | 50 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json |
| haproxy | MODSECURITY_MRTS_VARIANT=with-mrts make smoke-haproxy | FAIL | 2 | 54 | 10 | 44 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| all | REFRESH=1 make smoke-all | NOT_RUN | not_run | 0 | unknown | unknown | unknown | unknown | not available |

### Force-All Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | FORCE_ALL_CASES=1 make smoke-apache | FAIL | 2 | 516 | 183 | 327 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/apache-summary.json |
| nginx | FORCE_ALL_CASES=1 make smoke-nginx | FAIL | 2 | 140 | 67 | 67 | 0 | 6 | /root/.local/state/ModSecurity-conector-build/results/force-all/nginx-summary.json |
| haproxy | FORCE_ALL_CASES=1 make smoke-haproxy | FAIL | 1 | 133 | 104 | 23 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/haproxy-summary.json |

## Connector Runtime Availability
| Connector | Status | Build | Per-case results | Attempted cases | Summary evidence | Note |
|---|---|---|---|---:|---|---|
| Apache | FAIL | unknown | available | 54 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| NGINX | FAIL | unknown | available | 60 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| HAProxy | FAIL | unknown | available | 54 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json | Default HAProxy evidence is the supported non-former-XFAIL subset of live HAProxy matrix evidence; force-all rows remain separate runtime evidence. |

## Runtime FAIL Details

### Apache FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=json_request_body_block; status=fail; expected=403; actual=200 |
| multipart_basic_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=200 |
| multipart_filename_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=200 |
| multipart_files_combined_size | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=200 |
| multipart_files_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=200 |
| multipart_files_value_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=200 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=200 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=200 |
| request_body_json_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_json_block; status=fail; expected=403; actual=200 |
| request_body_raw_text_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=200 |
| request_body_urlencoded_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=200 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=404 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=404 |
| v3_operator_pm_digit_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=404 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=200 |

### NGINX FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=json_request_body_block; status=fail; expected=403; actual=405 |
| multipart_basic_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=405 |
| multipart_filename_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=405 |
| multipart_files_combined_size | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=405 |
| multipart_files_names_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=405 |
| multipart_files_value_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=405 |
| nginx_phase4_content_type_out_of_scope | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_content_type_out_of_scope; status=fail; expected=200; actual=200 |
| nginx_phase4_minimal_log_only | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_minimal_log_only; status=fail; expected=200; actual=200 |
| nginx_phase4_safe_log_only | 200 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_safe_log_only; status=fail; expected=200; actual=200 |
| nginx_redirect_phase1_302 | 302 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_redirect_phase1_302; status=fail; expected=302; actual=200 |
| nginx_tx_scoring_absolute_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_tx_scoring_absolute_block; status=fail; expected=403; actual=200 |
| nginx_tx_scoring_iterative_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_tx_scoring_iterative_block; status=fail; expected=403; actual=200 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=405 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=405 |
| request_body_json_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_json_block; status=fail; expected=403; actual=405 |
| request_body_raw_text_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=405 |
| request_body_urlencoded_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=405 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=404 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=404 |
| v3_operator_pm_digit_block | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=404 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=405 |

### HAProxy FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| action_deny_phase1 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase1; status=fail; expected=403; actual=200 |
| action_deny_phase2 | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_deny_phase2; status=fail; expected=403; actual=200 |
| action_status_401_phase1_block | 401 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=action_status_401_phase1_block; status=fail; expected=401; actual=200 |
| audit_log_phase1_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=audit_log_phase1_block; status=fail; expected=403; actual=200 |
| collection_args_combined_size_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_combined_size_block; status=fail; expected=403; actual=200 |
| collection_args_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_get_block; status=fail; expected=403; actual=200 |
| collection_args_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=collection_args_names_block; status=fail; expected=403; actual=200 |
| json_request_body_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=json_request_body_block; status=fail; expected=403; actual=501 |
| multipart_basic_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_basic_block; status=fail; expected=403; actual=501 |
| multipart_filename_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_filename_block; status=fail; expected=403; actual=501 |
| multipart_files_combined_size | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_combined_size; status=fail; expected=403; actual=501 |
| multipart_files_names_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_names_block; status=fail; expected=403; actual=501 |
| multipart_files_value_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=multipart_files_value_block; status=fail; expected=403; actual=501 |
| phase1_header_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase1_header_block; status=fail; expected=403; actual=200 |
| phase2_args_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=phase2_args_block; status=fail; expected=403; actual=200 |
| pr70_phase1_audit_request_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase1_audit_request_header; status=fail; expected=403; actual=200 |
| pr70_phase2_audit_urlencoded_body | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase2_audit_urlencoded_body; status=fail; expected=403; actual=501 |
| pr70_phase3_audit_response_header | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=200 |
| request_body_args_post_names_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_args_post_names_block; status=fail; expected=403; actual=501 |
| request_body_json_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_json_block; status=fail; expected=403; actual=501 |
| request_body_raw_text_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_raw_text_block; status=fail; expected=403; actual=501 |
| request_body_urlencoded_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=request_body_urlencoded_block; status=fail; expected=403; actual=501 |
| response_header_basic | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=response_header_basic; status=fail; expected=403; actual=200 |
| rule_chain_both_match_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=rule_chain_both_match_block; status=fail; expected=403; actual=200 |
| v2_operator_begins_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_begins_with_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_block; status=fail; expected=403; actual=200 |
| v2_operator_contains_word_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_contains_word_block; status=fail; expected=403; actual=200 |
| v2_operator_ends_with_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_ends_with_block; status=fail; expected=403; actual=200 |
| v2_operator_pm_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_pm_block; status=fail; expected=403; actual=200 |
| v2_operator_streq_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_operator_streq_block; status=fail; expected=403; actual=200 |
| v2_transformation_html_entity_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_html_entity_decode_block; status=fail; expected=403; actual=200 |
| v2_transformation_lowercase_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_lowercase_block; status=fail; expected=403; actual=200 |
| v2_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_trim_block; status=fail; expected=403; actual=200 |
| v2_transformation_url_decode_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v2_transformation_url_decode_block; status=fail; expected=403; actual=200 |
| v3_args_names_get_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_args_names_get_block; status=fail; expected=403; actual=200 |
| v3_auditlog_serial_fields_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_auditlog_serial_fields_block; status=fail; expected=403; actual=200 |
| v3_operator_pm_digit_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_pm_digit_block; status=fail; expected=403; actual=200 |
| v3_operator_rx_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_operator_rx_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_block; status=fail; expected=403; actual=200 |
| v3_request_cookies_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_cookies_names_block; status=fail; expected=403; actual=200 |
| v3_request_headers_names_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_request_headers_names_block; status=fail; expected=403; actual=200 |
| v3_secaction_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_secaction_block; status=fail; expected=403; actual=200 |
| v3_transformation_trim_block | 403 | 200 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=v3_transformation_trim_block; status=fail; expected=403; actual=200 |
| xml_request_body_block | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=xml_request_body_block; status=fail; expected=403; actual=501 |

## Runtime Verified Status
- Runtime matrix records current local Apache, NGINX, and HAProxy per-case smoke evidence when available.
- PASS in this snapshot means the case was executed by that connector's smoke harness and matched the case expectation in the summary JSON.
- Pending, connector-gap, runtime-difference, future, and mapped-only inventory are not promoted by this snapshot.
- FORCE_ALL_CASES=1 attempts all materializable YAML cases where they are applicable to the connector.
- HAProxy PASS is scoped to live HAProxy evidence only; current HAProxy coverage is partial request-side YAML execution.
- RESPONSE_BODY remains non-verified/non-promoted.
- Runtime passed, but this does not verify RESPONSE_BODY support.
- make smoke-all was not run by runtime-matrix; full-smoke PASS counts remain unknown.

## Open Runtime Issues
- Mapped-only import inventory entries are not executable YAML runtime cases.
- Pending/future/connector-gap/runtime-difference topics require live evidence before any support claim.
- RESPONSE_BODY remains experimental/non-verified.

## Open Areas / Gaps
- Runtime-verified means only cases explicitly classified as `runtime_verified=true`.
- Cases with `runtime_verified=false` or `runtime_verified=unknown` are not runtime PASS proof.
- See `reports/testing/generated/connector-gap-summary.generated.md` for detailed connector-gap entries.
- Phase 3/4 cases are visible in `reports/testing/generated/phase-coverage.generated.md` and in the runtime matrix.
- RESPONSE_BODY remains not verified and not promoted.
- GitHub/Codex checks are intentionally lightweight.
- Pending and gap topics need local runtime validation.
- `make smoke-all` is authoritative only if it was actually executed successfully.

## Commands
- `make quick-check`
- `make quick-all`
- `make cloud-quick-check`
- `make installed-readiness`
- `make runtime-matrix`
- `make runtime-matrix-all`
- `make runtime-matrix-haproxy`
- `make smoke-apache`
- `make smoke-nginx`
- `make smoke-haproxy`
- `make smoke-all`
- `make generate-test-matrix`
- `make check-test-matrix`

## Detail Reports
- `reports/testing/generated/case-matrix.generated.md`
- `reports/testing/generated/coverage-summary.generated.md`
- `reports/testing/generated/xfail-summary.generated.md`
- `reports/testing/generated/connector-gap-summary.generated.md`
- `reports/testing/generated/phase-coverage.generated.md`
- `reports/testing/generated/runtime-matrix.generated.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`

## Important Note
Generated coverage is reporting only; it is not runtime evidence by itself.
Full runtime validation is local and evidence-based.
GitHub/Codex checks are intentionally lightweight.
Pending, future, and gap topics need local runtime validation before promotion.
`make smoke-all` is authoritative only if it was actually executed successfully.
No PASS numbers are inferred from this file when `make smoke-all` was not run successfully.
Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is reported as runtime evidence only.
