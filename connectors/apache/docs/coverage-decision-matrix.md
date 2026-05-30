# Apache Coverage Decision Matrix

Status: partial

This file evaluates Apache coverage using repository evidence only. Generated
coverage reporting is not automatically runtime promotion.

Evidence sources:

- `TEST-COVERAGE-SUMMARY.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/summary.md`
- `reports/testing/generated/apache-runtime-results.generated.md`

## Status Vocabulary

- `framework-covered`: a YAML/framework case exists, but Apache is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete Apache command was executed and passed
  for the named case.
- `partial`: some structure or runtime evidence exists, but the minimum matrix
  is incomplete.
- `not-verified`: no sufficient Apache runtime evidence exists.
- `fail`: Apache runtime was executed and the expectation was not met.
- `blocked`: the test could not run because of environment, dependency, or
  harness prerequisites.

## Apache Current Status

- [x] Status: partial - Connector is `adapter-owned`.
- [x] Status: framework-covered - No local `connectors/apache/tests` folder.
- [x] Status: framework-covered - External framework test paths referenced.
- [x] Status: runtime-smoke-verified - `/src` `phase1_header_block` runtime
      smoke PASS documented.
- [x] Status: runtime-smoke-verified - Current `/src` common runtime run
      documented in `verified-runtime-run.md`.
- [x] Status: runtime-smoke-verified - Current `/src` No-CRS run documented:
      54 PASS, 0 FAIL, 0 BLOCKED.
- [ ] Status: fail - Current `/src` With-CRS run documented: 54 PASS,
      1 FAIL, 0 BLOCKED.
- [x] Status: runtime-smoke-verified - Current `/src` With-CRS
      `crs_sqli_anomaly_block` documented: expected 403, actual 403.
- [ ] Status: blocked - Default `make smoke-common` readiness in default
      buildroot.
- [ ] Status: partial - Phase 2 request-body matrix fully verified.
- [ ] Status: fail - Phase 3 response-header matrix fully verified.
- [ ] Status: not-verified - Phase 4 response-body matrix fully verified.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified.
- [ ] Status: not-verified - Audit/log evidence fully verified.
- [ ] Status: not-verified - Negative/pass-through matrix verified.
- [ ] Status: partial - Connector can be marked more than `partial`.

## Generated Coverage Snapshot

Evidence source: `TEST-COVERAGE-SUMMARY.md`.

- Total YAML cases: 140.
- Common YAML cases: 133.
- Apache-specific YAML cases: 0.
- NGINX-specific YAML cases: 7.
- `runtime_verified=true`: 0.
- RESPONSE_BODY cases: 24.
- Apache attempted YAML cases in latest runtime snapshot: 133.
- Apache runtime smoke snapshot: `FORCE_ALL_CASES=1 REFRESH=1 make smoke-apache`
  status FAIL, exit 2, PASS 87, FAIL 46, BLOCKED 0, XFAIL 0.
- Apache connector runtime availability: FAIL, per-case results available,
  attempted cases 133.
- RESPONSE_BODY status: not verified or promoted.

## Current Verified Runtime Run

Evidence source: `reports/template-verification-nginx-apache/verified-runtime-run.md`.

- Command: `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache`.
- Result: PASS, Make exit 0.
- Final `make smoke-common` Apache summary: PASS 54, FAIL 0, BLOCKED 0,
  XFAIL 0.
- Summary JSON: `/src/ModSecurity-conector-build/results/apache-summary.json`.
- `phase1_header_block`: PASS, expected 403, actual 403.
- Phase 1: 17 PASS.
- Phase 2: 34 PASS.
- Phase 3: 2 PASS.
- Phase 4: 1 PASS for `response_body_pass` only.
- Audit/log: 5 PASS.
- Negative/pass-through: 10 PASS.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed.
- RESPONSE_BODY blocking: not verified.

## CRS Variant Runtime Runs

Evidence source: `reports/template-verification-nginx-apache/verified-runtime-run.md`.

| Gate | No-CRS Status | With-CRS Status | Evidence | Decision |
| --- | --- | --- | --- | --- |
| Basic target | PASS: 54 PASS, 0 FAIL, 0 BLOCKED | FAIL: 54 PASS, 1 FAIL, 0 BLOCKED | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`, `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json` | No-CRS verified for executed scope; With-CRS not fully passing. |
| CRS loading | not applicable | PASS for setup evidence and CRS case; overall target FAIL | `/src/coreruleset`, `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`, `crs_sqli_anomaly_block` | CRS case may be cited as PASS; target remains FAIL. |
| Phase 1 | 17 PASS | 16 PASS, 1 FAIL | Summary JSON | Partial; With-CRS fail is `action_status_401_phase1_block`, expected 401 and actual 403. |
| Phase 2 | 34 PASS | 35 PASS | Summary JSON | Partial; includes `crs_sqli_anomaly_block` PASS under With-CRS. |
| Phase 3 | 2 PASS | 2 PASS | Summary JSON | Partial for executed scope. |
| Phase 4 | 1 PASS | 1 PASS | Summary JSON | `response_body_pass` only; RESPONSE_BODY blocking not promoted. |
| Request body | 12 PASS | 12 PASS | Summary JSON | Runtime-smoke-verified for executed scope only. |
| RESPONSE_BODY | 1 PASS | 1 PASS | Summary JSON | Pass-through only; blocking not verified. |
| Negative/pass-through | 10 PASS | 10 PASS | Summary JSON | Runtime-smoke-verified for executed scope only. |
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
  evidenced as Apache-specific because NGINX shows the same result.

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

## Apache Phase Matrix

| Phase / Bereich | Coverage Summary Evidence | Apache Runtime Evidence | Status | Decision |
| --- | --- | --- | --- | --- |
| Phase 1 / Request headers, URI, ARGS | Phase 1 count 36; `REQUEST_HEADERS` 5; `REQUEST_URI` 7; `ARGS` 49 | Current run: 17 Phase 1 PASS; `/src phase1_header_block`: PASS with HTTP 403 | runtime-smoke-verified for current common scope | Apache remains partial |
| Phase 2 / Request body, multipart, XML/JSON | Phase 2 count 73; `REQUEST_BODY` 10; `FILES` 2; `FILES_NAMES` 2; `XML` 5 | Current run: 34 Phase 2 PASS; generated force-all snapshot still has FAIL evidence | partial | Do not promote beyond partial |
| Phase 3 / Response headers | Phase 3 count 12; `RESPONSE_HEADERS` 11 | Current run: 2 Phase 3 PASS; generated force-all snapshot still has response-header FAIL evidence | partial | Do not promote beyond partial |
| Phase 4 / Response body | Phase 4 count 20; `RESPONSE_BODY` 20; RESPONSE_BODY cases 24 | Current run: `response_body_pass` PASS only; `response_body_basic_block` not executed | not-verified for blocking | Do not promote |
| Audit/log evidence | Audit-log probes 24; `AUDIT_LOG` collection count 0 | Current run: 5 audit/log PASS rows | partial | Need complete log evidence |
| Negative/pass-through | Pass-through classes exist in generated runtime matrix; RESPONSE_BODY pass-through is non-promotable | Current run: 10 pass-through PASS rows | partial | Need complete PASS evidence across required matrix |

## Runtime Matrix Status Snapshot

Evidence source: `TEST-COVERAGE-SUMMARY.md`.

| Status | Apache |
| --- | ---: |
| PASS | 53 |
| RESPONSE_BODY_PASS_THROUGH | 1 |
| XFAIL_PASS | 16 |
| XFAIL_FAIL | 20 |
| PENDING_FAIL | 1 |
| FUTURE_PASS | 6 |
| FUTURE_RESPONSE_BODY_PASS_THROUGH | 1 |
| FUTURE_FAIL | 10 |
| CONNECTOR_GAP_PASS | 4 |
| CONNECTOR_GAP_FAIL | 7 |
| RUNTIME_DIFFERENCE_PASS | 6 |
| RUNTIME_DIFFERENCE_FAIL | 8 |
| NOT_EXECUTABLE | 7 |
| MAPPED_ONLY | 10 |

PASS/FAIL values are snapshot evidence only. XFAIL, pending, future,
connector-gap, runtime-difference, pass-through, and mapped-only rows are not
promoted.

## Decision

Apache remains `partial`. The current `/src` common and No-CRS runs are PASS
for their executed scopes, including `phase1_header_block`. The current
With-CRS run is FAIL because `action_status_401_phase1_block` returned 403
instead of expected 401, even though `crs_sqli_anomaly_block` is PASS. The
exact cause is not proven and the current evidence does not show an
Apache-specific connector bug. The current runs do not execute
`response_body_basic_block`, do not verify
RESPONSE_BODY blocking, and do not prove the full minimum matrix.
