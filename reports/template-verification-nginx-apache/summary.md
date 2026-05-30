# Verification Summary

Status: reviewed

## Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked unless dependencies are prepared in
  the default build root.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` `make smoke-common` evidence: Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make smoke-nginx` all-scope evidence: NGINX 60 PASS,
  0 FAIL, 0 BLOCKED.
- Current `/src` `make test-no-crs`: PASS.
- Current `/src` `make test-with-crs`: FAIL.
- RESPONSE_BODY blocking: not verified.
- Vollstaendige Runtime-Verifikation: nein.
- Current With-CRS 401/403 mismatch analysis:
  `crs-action-status-401-analysis.md`.
- Cause for `action_status_401_phase1_block`: not definitive. The most likely
  classification from reviewed evidence is a With-CRS expected-status/context
  mismatch, likely involving CRS/default-action interaction or testcase
  expectation. A connector-specific issue is not evidenced because Apache and
  NGINX show the same result.

## Current Repo State Captured

- Parent working directory: `/root/git/ModSecurity-conector`.
- Parent commit: `e795c9b feat(apache): add modsecurity_use_error_log directive`.
- Parent status before documentation edits: clean.
- Framework submodule commit:
  `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18`.
- Framework submodule status before documentation edits: clean.

## New Test Targets

| Target | Found | Purpose found in repo | Current `/src` result |
| --- | --- | --- | --- |
| `make test-no-crs` | yes | Runs Apache and NGINX connector smokes with `MODSECURITY_TEST_VARIANT=no-crs`, local YAML rules only, `CASE_SCOPE=all`, and results under `$BUILD_ROOT/results/no-crs`. | PASS: Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `make test-with-crs` | yes | Runs Apache and NGINX connector smokes with `MODSECURITY_TEST_VARIANT=with-crs`, fetches/prepares CRS, injects `$CRS_RUNTIME_DIR/modsecurity-crs-preamble.conf`, and writes results under `$BUILD_ROOT/results/with-crs`. | FAIL: Apache 54 PASS / 1 FAIL; NGINX 60 PASS / 1 FAIL. |

## CRS Result

- CRS source path observed: `/src/coreruleset`.
- CRS runtime preamble observed:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- CRS version pin found in framework `ci/common.sh`: `v4.26.0`.
- `crs_sqli_anomaly_block`: PASS for Apache and NGINX, expected 403 and
  actual 403.
- Overall `make test-with-crs`: FAIL because `action_status_401_phase1_block`
  returned 403 instead of expected 401 for both connectors.
- Detailed analysis:
  `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## Decisions

| Target | Decision | Reason |
| --- | --- | --- |
| Scaffold rules | documented | `connector-scaffold-decisions.md` separates accepted and deferred decisions. |
| `connectors/_template` | partially suitable | Structure and warnings exist; local Template tests were removed; concrete runtime claims remain external evidence only. |
| `connectors/nginx` | partial | Adapter-owned structure exists; local tests were removed; No-CRS and common smokes passed; With-CRS currently has one FAIL; full matrix and RESPONSE_BODY blocking are not verified. |
| `connectors/apache` | partial | Adapter-owned structure exists; local tests were removed; No-CRS and common smokes passed; With-CRS currently has one FAIL; Apache-specific YAML files were not found; RESPONSE_BODY blocking is not verified. |

## Current Runtime Evidence

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` | PASS | Apache source-build smoke completed before later result refreshes. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | FAIL | Apache 54 PASS / 1 FAIL; NGINX 60 PASS / 1 FAIL; both fail `action_status_401_phase1_block`, expected 401 and actual 403. |

Evidence files:

- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

## Removed Local Test Folders

- `connectors/_template/tests/`
- `connectors/nginx/tests/`
- `connectors/apache/tests/`

Executable connector tests are framework-owned and are not maintained in local
`connectors/*/tests` directories.

## Checks

| Check | Result | Note |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; no runtime PASS claim. |
| `make check-test-matrix` | PASS | Matrix check exited 0. |
| `test ! -d connectors/_template/tests` | PASS | Template test folder is absent. |
| `test ! -d connectors/apache/tests` | PASS | Apache test folder is absent. |
| `test ! -d connectors/nginx/tests` | PASS | NGINX test folder is absent. |
| `make lint` | PASS | `actionlint unavailable` was informational; command exited 0. |
| `make quick-check` | PASS | Sequential rerun exited 0. An earlier parallel run collided with `make lint` on a helper-smoke artifact and exited with `Text file busy`; it was not used as the final status. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |

## Not Verified

- RESPONSE_BODY blocking for Apache and NGINX.
- Full runtime matrix promotion beyond `partial`.
- Apache-specific connector YAML cases under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there during this verification.
- NGINX-specific `nginx_phase4_strict_connection_abort` runtime result in the
  current No-CRS/With-CRS summaries; the YAML file exists but was not present
  in those summaries.
- Default `make smoke-common` without preparing the default build root.

## Report Files

- `connector-scaffold-decisions.md`
- `template-evaluation.md`
- `nginx-evaluation.md`
- `apache-evaluation.md`
- `component-download-check.md`
- `runtime-test-run-src.md`
- `verified-runtime-run.md`
- `nginx-build-fail-analysis.md`
- `nginx-docroot-permission-analysis.md`
- `nginx-blocked-runtime-cases.md`
- `crs-action-status-401-analysis.md`
- `summary.md`
- `findings.md`
- `files-reviewed.md`
- `open-questions.md`
