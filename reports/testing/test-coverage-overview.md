Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Overview

## Summary
- Total cases: **161**
- Verified/pass count (`runtime_verified=true`): **0**
- Current XFAIL count: **0**
- Former XFAIL cases tracked: **80**
- Pending runtime verification count: **12**
- Connector-gap count: **12**
- Runtime-difference count: **13**
- Future/experimental count: **17**
- RESPONSE_BODY cases: **25** (still **not verified/promoted**)
- Mapped-only import inventory entries: **10**

## MRTS Source Summary
- Total MRTS imported cases: **20**
- Active MRTS cases: **19**
- Pending MRTS cases: **1**
- Unclassified MRTS cases: **0**
- Phase 4 / RESPONSE_BODY MRTS cases: **1**
- Runtime-executable MRTS cases: **19**
- MRTS overlay classifications: **active(16), harness-incompatibility(2), importer-mapping-issue(1), non-promoted(1)**
- Apache observed classifications: **active(1), connector-gap(1), harness-incompatibility(2), importer-mapping-issue(1), non-promoted(1)**
- NGINX observed classifications: **active(1), harness-incompatibility(3), importer-mapping-issue(1), non-promoted(1)**
- HAProxy observed classifications: **active(2), harness-incompatibility(2), importer-mapping-issue(1), non-promoted(1)**

## Coverage By Variable / Collection
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 21 |
| `ARGS:q` | 18 |
| `ARGS` | 16 |
| `REQUEST_BODY` | 11 |
| `REQUEST_URI` | 8 |
| `ARGS_NAMES` | 7 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `XML` | 5 |
| `ARGS:a` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `ARGS:param1` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `ARGS:probe` | 4 |
| `MULTIPART_FILENAME` | 3 |
| `ARGS:chain_a` | 3 |
| `ARGS:chain_b` | 3 |
| `FILES` | 2 |
| `FILES_NAMES` | 2 |
| `TX:SCORE` | 2 |

## Coverage By Phase
| Phase | Count |
|---|---:|
| 1 | 39 |
| 2 | 89 |
| 3 | 13 |
| 4 | 21 |

## Coverage By Status
| Status | Count |
|---|---:|
| active | 27 |
| imported | 133 |
| pending | 1 |

## Coverage By Scope
| Scope | Count |
|---|---:|
| common | 154 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Runtime Matrix Status
- Default runtime-executable YAML cases: **80**
- Force-all runtime-executable YAML cases: **161**
- Apache attempted YAML cases from default summary: **73**
- NGINX attempted YAML cases from default summary: **79**
- HAProxy attempted YAML cases from default summary: **73**
- Apache attempted YAML cases from force-all summary: **153**
- NGINX attempted YAML cases from force-all summary: **160**
- HAProxy attempted YAML cases from force-all summary: **133**
- Apache force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **117** / **30** / **0** / **6**
- NGINX force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **113** / **41** / **0** / **6**
- HAProxy force-all raw runtime PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **104** / **23** / **0** / **6**
| Status | Apache | NGINX | HAProxy |
|---|---:|---:|---:|
| PASS | 59 | 62 | 68 |
| FAIL | 14 | 17 | 5 |
| NOT_EXECUTABLE | 7 | 0 | 7 |
| NOT EXECUTED | 81 | 82 | 81 |
| MAPPED_ONLY | 10 | 10 | 10 |
- Details: `reports/testing/generated/runtime-matrix.generated.md`
- HAProxy per-case results: `reports/testing/generated/haproxy-runtime-results.generated.md`

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
- Snapshot: **2026-06-07** (2026-06-07 23:18:49 CEST)
- Git: branch `integrate-new-connectors-local`, commit `4c40cba`
- BUILD_ROOT: `/src/ModSecurity-conector-build`
- Snapshot file: `reports/testing/runtime-validation-snapshot.json`

### Default Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | make smoke-apache | FAIL | 2 | 73 | 59 | 14 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json |
| nginx | make smoke-nginx | FAIL | 2 | 79 | 62 | 17 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json |
| haproxy | MODSECURITY_MRTS_VARIANT=with-mrts make smoke-haproxy | FAIL | 2 | 73 | 68 | 5 | 0 | 0 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json |
| all | REFRESH=1 make smoke-all | NOT_RUN | not_run | 0 | unknown | unknown | unknown | unknown | not available |

### Force-All Runtime Smoke Status
| Connector | Command | Status | Exit | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| apache | FORCE_ALL_CASES=1 make smoke-apache | FAIL | 1 | 153 | 117 | 30 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/apache-summary.json |
| nginx | FORCE_ALL_CASES=1 make smoke-nginx | FAIL | 1 | 160 | 113 | 41 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/nginx-summary.json |
| haproxy | FORCE_ALL_CASES=1 make smoke-haproxy | FAIL | 1 | 133 | 104 | 23 | 0 | 6 | /src/ModSecurity-conector-build/results/force-all/haproxy-summary.json |

## Connector Runtime Availability
| Connector | Status | Build | Per-case results | Attempted cases | Summary evidence | Note |
|---|---|---|---|---:|---|---|
| Apache | FAIL | unknown | available | 73 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| NGINX | FAIL | unknown | available | 79 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json | Per-case results are copied from the local smoke summary JSON; they are runtime evidence only. |
| HAProxy | FAIL | unknown | available | 73 | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json | Default HAProxy evidence is the supported non-former-XFAIL subset of live HAProxy matrix evidence; force-all rows remain separate runtime evidence. |

## Runtime FAIL Details

### Apache FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| mrts_760012_mrts_050_json_request_body_760012_1 | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=mrts_760012_mrts_050_json_request_body_760012_1; status=fail; expected=403; actual=404 |
| mrts_760013_mrts_060_xml_760013_1 | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=mrts_760013_mrts_060_xml_760013_1; status=fail; expected=403; actual=404 |
| mrts_760016_mrts_090_multipart_files_760016_1 | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=mrts_760016_mrts_090_multipart_files_760016_1; status=fail; expected=403; actual=404 |
| mrts_760019_mrts_102_transform_compress_whitespace_760019_1 | 403 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=mrts_760019_mrts_102_transform_compress_whitespace_760019_1; status=fail; expected=403; actual=0 |
| phase2_args_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=phase2_args_pass; status=fail; expected=200; actual=403 |
| pr70_phase3_audit_response_header | 403 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=403 |
| response_body_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=response_body_pass; status=fail; expected=200; actual=403 |
| rule_chain_first_only_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=rule_chain_first_only_pass; status=fail; expected=200; actual=403 |
| rule_chain_second_only_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=rule_chain_second_only_pass; status=fail; expected=200; actual=403 |
| v2_transformation_url_decode_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v2_transformation_url_decode_pass_no_match; status=fail; expected=200; actual=403 |
| v3_args_names_get_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_args_names_get_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_cookies_names_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_names_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_cookies_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_cookies_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_headers_names_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/apache/apache-summary.json; case=v3_request_headers_names_pass_no_match; status=fail; expected=200; actual=403 |

### NGINX FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| mrts_760013_mrts_060_xml_760013_1 | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=mrts_760013_mrts_060_xml_760013_1; status=fail; expected=403; actual=404 |
| mrts_760014_mrts_070_response_headers_760014_1 | 403 | 405 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=mrts_760014_mrts_070_response_headers_760014_1; status=fail; expected=403; actual=405 |
| mrts_760016_mrts_090_multipart_files_760016_1 | 403 | 404 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=mrts_760016_mrts_090_multipart_files_760016_1; status=fail; expected=403; actual=404 |
| mrts_760019_mrts_102_transform_compress_whitespace_760019_1 | 403 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=mrts_760019_mrts_102_transform_compress_whitespace_760019_1; status=fail; expected=403; actual=0 |
| nginx_phase4_content_type_out_of_scope | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_content_type_out_of_scope; status=fail; expected=200; actual=403 |
| nginx_phase4_minimal_log_only | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_minimal_log_only; status=fail; expected=200; actual=403 |
| nginx_phase4_safe_log_only | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=nginx_phase4_safe_log_only; status=fail; expected=200; actual=403 |
| phase2_args_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=phase2_args_pass; status=fail; expected=200; actual=403 |
| pr70_phase3_audit_response_header | 403 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=403 |
| response_body_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=response_body_pass; status=fail; expected=200; actual=403 |
| rule_chain_first_only_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=rule_chain_first_only_pass; status=fail; expected=200; actual=403 |
| rule_chain_second_only_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=rule_chain_second_only_pass; status=fail; expected=200; actual=403 |
| v2_transformation_url_decode_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v2_transformation_url_decode_pass_no_match; status=fail; expected=200; actual=403 |
| v3_args_names_get_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_args_names_get_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_cookies_names_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_names_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_cookies_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_cookies_pass_no_match; status=fail; expected=200; actual=403 |
| v3_request_headers_names_pass_no_match | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/nginx/nginx-summary.json; case=v3_request_headers_names_pass_no_match; status=fail; expected=200; actual=403 |

### HAProxy FAIL Details
| Case | Expected | Actual | Assessment | Evidence |
|---|---|---|---|---|
| mrts_760013_mrts_060_xml_760013_1 | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=mrts_760013_mrts_060_xml_760013_1; status=fail; expected=403; actual=501 |
| mrts_760016_mrts_090_multipart_files_760016_1 | 403 | 501 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=mrts_760016_mrts_090_multipart_files_760016_1; status=fail; expected=403; actual=501 |
| mrts_760019_mrts_102_transform_compress_whitespace_760019_1 | 403 | 0 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=mrts_760019_mrts_102_transform_compress_whitespace_760019_1; status=fail; expected=403; actual=0 |
| pr70_phase3_audit_response_header | 403 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=pr70_phase3_audit_response_header; status=fail; expected=403; actual=403 |
| response_body_pass | 200 | 403 | runtime summary reported non-pass | /src/ModSecurity-conector-build/results/no-crs/with-mrts/haproxy/haproxy-summary.json; case=response_body_pass; status=fail; expected=200; actual=403 |

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
