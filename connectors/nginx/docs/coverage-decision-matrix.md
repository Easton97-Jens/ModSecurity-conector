# NGINX Coverage Decision Matrix

Status: partial

This file evaluates NGINX coverage using repository evidence only. Generated
coverage reporting is not automatically runtime promotion.

Evidence sources:

- `TEST-COVERAGE-SUMMARY.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- `reports/template-verification-nginx-apache/nginx-docroot-permission-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`

## Status Vocabulary

- `framework-covered`: a YAML/framework case exists, but NGINX is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete NGINX command was executed and passed
  for the named case.
- `partial`: some structure or runtime evidence exists, but the minimum matrix
  is incomplete.
- `not-verified`: no sufficient NGINX runtime evidence exists.
- `fail`: NGINX runtime was executed and the expectation was not met.
- `blocked`: the test could not run because of environment, dependency, or
  harness prerequisites.

## NGINX Current Status

- [x] Status: partial - Connector is `adapter-owned`.
- [x] Status: framework-covered - No local `connectors/nginx/tests` folder.
- [x] Status: framework-covered - External framework test paths referenced.
- [x] Status: partial - `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`
      build contract documented.
- [x] Status: runtime-smoke-verified - `/src` `phase1_header_block` runtime
      smoke PASS documented.
- [x] Status: runtime-smoke-verified - Current `/src` common run has 54 PASS,
      0 FAIL, and 0 BLOCKED for NGINX.
- [x] Status: runtime-smoke-verified - Current `/src` NGINX all-scope smoke
      has 60 PASS, 0 FAIL, and 0 BLOCKED.
- [x] Status: runtime-smoke-verified - Current `/src` No-CRS run documented:
      60 PASS, 0 FAIL, 0 BLOCKED.
- [ ] Status: fail - Current `/src` With-CRS run documented: 60 PASS,
      1 FAIL, 0 BLOCKED.
- [x] Status: runtime-smoke-verified - Current `/src` With-CRS
      `crs_sqli_anomaly_block` documented: expected 403, actual 403.
- [x] Status: partial - The historical 11 BLOCKED rows were environment/docroot
      blockers and are resolved in the current run.
- [ ] Status: blocked - Default `make smoke-common` readiness in the default
      buildroot remains blocked unless dependencies are fetched there.
- [ ] Status: partial - Phase 2 request-body matrix fully verified.
- [ ] Status: partial - Phase 3 response-header matrix fully verified.
- [ ] Status: not-verified - Phase 4 response-body matrix fully verified.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified.
- [ ] Status: not-verified - Audit/log evidence fully verified.
- [ ] Status: partial - Negative/pass-through matrix verified only for current
      common/all smoke scope.
- [ ] Status: partial - Connector can be marked more than `partial`.

## Generated Coverage Snapshot

Evidence source: `TEST-COVERAGE-SUMMARY.md`.

- Total YAML cases: 140.
- Common YAML cases: 133.
- Apache-specific YAML cases: 0.
- NGINX-specific YAML cases: 7.
- `runtime_verified=true`: 0.
- RESPONSE_BODY cases: 24.
- NGINX attempted YAML cases in latest generated runtime snapshot: 140.
- Generated NGINX runtime snapshot: `FORCE_ALL_CASES=1 REFRESH=1 make smoke-nginx`
  status FAIL, exit 2, PASS 94, FAIL 46, BLOCKED 0, XFAIL 0.
- Generated snapshot evidence is not the same as the current `/src` smoke run.
- RESPONSE_BODY status: not verified or promoted.

## Current Verified Runtime Run

Evidence source: `reports/template-verification-nginx-apache/verified-runtime-run.md`.

- Command: `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx`.
- Result: PASS, NGINX 60 PASS, 0 FAIL, 0 BLOCKED.
- Command: `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common`.
- Result: PASS, Apache 54 PASS and NGINX 54 PASS.
- Final `make smoke-common` NGINX summary: PASS 54, FAIL 0, BLOCKED 0, XFAIL 0.
- Summary JSON: `/src/ModSecurity-conector-build/results/nginx-summary.json`.
- `phase1_header_block`: PASS, expected 403, actual 403.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed.
- RESPONSE_BODY blocking: not verified.

## CRS Variant Runtime Runs

Evidence source: `reports/template-verification-nginx-apache/verified-runtime-run.md`.

| Gate | No-CRS Status | With-CRS Status | Evidence | Decision |
| --- | --- | --- | --- | --- |
| Basic target | PASS: 60 PASS, 0 FAIL, 0 BLOCKED | FAIL: 60 PASS, 1 FAIL, 0 BLOCKED | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`, `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json` | No-CRS verified for executed scope; With-CRS not fully passing. |
| CRS loading | not applicable | PASS for setup evidence and CRS case; overall target FAIL | `/src/coreruleset`, `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`, `crs_sqli_anomaly_block` | CRS case may be cited as PASS; target remains FAIL. |
| Phase 1 | 18 PASS | 17 PASS, 1 FAIL | Summary JSON | Partial; With-CRS fail is `action_status_401_phase1_block`, expected 401 and actual 403. |
| Phase 2 | 36 PASS | 37 PASS | Summary JSON | Partial; includes `crs_sqli_anomaly_block` PASS under With-CRS. |
| Phase 3 | 2 PASS | 2 PASS | Summary JSON | Partial for executed scope. |
| Phase 4 | 4 PASS | 4 PASS | Summary JSON | Pass-through/log-only rows plus `response_body_pass`; RESPONSE_BODY blocking not promoted. |
| Request body | 12 PASS | 12 PASS | Summary JSON | Runtime-smoke-verified for executed scope only. |
| RESPONSE_BODY | 4 PASS | 4 PASS | Summary JSON | Pass-through/log-only only; blocking not verified. |
| Negative/pass-through | 13 PASS | 13 PASS | Summary JSON | Runtime-smoke-verified for executed scope only. |
| Audit/log | 5 PASS | 5 PASS | Summary JSON | Partial; complete audit/log matrix not proven. |

Current With-CRS failing case:

- `action_status_401_phase1_block`
- Expected: 401
- Actual: 403
- Path:
  `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`
- Analysis:
  `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- Decision: exact cause not proven; likely With-CRS expected-status/context
  mismatch involving CRS/default-action behavior or testcase expectation. Not
  evidenced as NGINX-specific because Apache shows the same result.

NGINX-specific YAML note:

- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/nginx_phase4_strict_connection_abort.yaml`
  exists.
- That case was not present in the current No-CRS or With-CRS summary JSON
  files and is not counted as PASS here.

## Framework Coverage By Phase

| Phase | Count | Status |
| --- | ---: | --- |
| Phase 1 | 36 | framework-covered |
| Phase 2 | 73 | framework-covered |
| Phase 3 | 12 | framework-covered |
| Phase 4 | 20 | framework-covered |

## Framework Coverage By Variable / Collection

| Variable / Collection | Count |
| --- | ---: |
| `ARGS` | 49 |
| `ARGS_NAMES` | 7 |
| `REQUEST_HEADERS` | 5 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `REQUEST_COOKIES` | 2 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `REQUEST_URI` | 7 |
| `REQUEST_BODY` | 10 |
| `FILES` | 2 |
| `FILES_NAMES` | 2 |
| `XML` | 5 |
| `RESPONSE_HEADERS` | 11 |
| `RESPONSE_BODY` | 20 |
| `AUDIT_LOG` | 0 |

## NGINX Phase Matrix

| Phase / Area | Coverage Summary Evidence | Current NGINX Runtime Evidence | Status | Decision |
| --- | --- | --- | --- | --- |
| Phase 1 / Request headers, URI, ARGS | Phase 1 count 36; `REQUEST_HEADERS` 5; `REQUEST_URI` 7; `ARGS` 49 | Current `/src` common run PASS for executed common phase-1 cases; `phase1_header_block` PASS with HTTP 403 | partial / runtime-smoke-verified for executed smoke scope | NGINX remains partial |
| Phase 2 / Request body, multipart, XML/JSON | Phase 2 count 73; `REQUEST_BODY` 10; `FILES` 2; `FILES_NAMES` 2; `XML` 5 | Current `/src` common run PASS for executed common phase-2 cases | partial / runtime-smoke-verified for executed smoke scope | Do not promote |
| Phase 3 / Response headers | Phase 3 count 12; `RESPONSE_HEADERS` 11 | Current `/src` common run PASS for executed common phase-3 cases | partial / runtime-smoke-verified for executed smoke scope | Do not promote |
| Phase 4 / Response body | Phase 4 count 20; `RESPONSE_BODY` 20; RESPONSE_BODY cases 24 | `response_body_pass` PASS only; no blocking response-body testcase executed | pass-through only / not-verified for blocking | Do not promote |
| Audit/log evidence | Audit-log probes 24; `AUDIT_LOG` collection count 0 | Current `/src` common run PASS for executed common audit cases | partial | Need complete log evidence |
| Negative/pass-through | Pass-through classes exist in generated runtime matrix; RESPONSE_BODY pass-through is non-promotable | Current `/src` common run PASS for executed common pass-through cases | partial | Need broader matrix evidence |

## Historical BLOCKED Runtime Cases

The previous `/src` report state had 11 NGINX BLOCKED rows. The current reruns
resolved them. Details are in
`reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`.

## Runtime Matrix Status Snapshot

Evidence source: `TEST-COVERAGE-SUMMARY.md`.

| Status | NGINX |
| --- | ---: |
| PASS | 56 |
| RESPONSE_BODY_PASS_THROUGH | 4 |
| XFAIL_PASS | 16 |
| XFAIL_FAIL | 21 |
| PENDING_FAIL | 1 |
| FUTURE_PASS | 6 |
| FUTURE_RESPONSE_BODY_PASS_THROUGH | 1 |
| FUTURE_FAIL | 10 |
| CONNECTOR_GAP_PASS | 5 |
| CONNECTOR_GAP_FAIL | 6 |
| RUNTIME_DIFFERENCE_PASS | 6 |
| RUNTIME_DIFFERENCE_FAIL | 8 |
| NOT_EXECUTABLE | 0 |
| MAPPED_ONLY | 10 |

PASS/FAIL values are snapshot evidence only. XFAIL, pending, future,
connector-gap, runtime-difference, pass-through, and mapped-only rows are not
promoted.

## Decision

NGINX remains `partial`. The current `/src` smoke evidence is materially
better than the historical blocked run: NGINX now has 54 PASS / 0 BLOCKED in
common scope and 60 PASS / 0 BLOCKED in all and No-CRS scope. The current
With-CRS run is FAIL because `action_status_401_phase1_block` returned 403
instead of expected 401, even though `crs_sqli_anomaly_block` is PASS. The
exact cause is not proven and the current evidence does not show an
NGINX-specific connector bug. The connector is still not more than `partial`
because With-CRS is not fully passing, RESPONSE_BODY blocking and the complete
minimum matrix are not verified.
