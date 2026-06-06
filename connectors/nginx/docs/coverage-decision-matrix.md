# NGINX Coverage Decision Matrix

Status: partial

This file evaluates NGINX coverage using repository evidence only. Generated
coverage reporting is not automatically runtime promotion.

Evidence sources:

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/template-verification-nginx-apache/nginx-template-alignment.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`

Template alignment report:
`reports/template-verification-nginx-apache/nginx-template-alignment.md`.

NGINX is aligned with the current Template for scaffold, metadata, build,
harness, No-CRS, and With-CRS executed runtime scope. It remains `partial`
because RESPONSE_BODY blocking and the full minimum matrix are not verified.

## Status Vocabulary

- `framework-covered`: a YAML/framework case exists, but NGINX is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete NGINX command was executed and passed
  for the named case.
- `crs-verified`: With-CRS command/case has CRS evidence and a passing result.
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
- [x] Status: runtime-smoke-verified - Current `/src` common runtime run:
      54 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: runtime-smoke-verified - Current `/src` No-CRS run:
      60 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: crs-verified - Current `/src` With-CRS run:
      61 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: crs-verified - `crs_sqli_anomaly_block`: expected 403,
      actual 403.
- [x] Status: runtime-smoke-verified - No-CRS
      `action_status_401_phase1_block`: expected 401, actual 401.
- [x] Status: crs-verified - With-CRS `action_status_401_phase1_block`:
      expected 403, actual 403.
- [x] Status: partial - Historical 11 BLOCKED rows were environment/docroot
      blockers and are resolved in current `/src` reruns.
- [ ] Status: blocked - Default `make smoke-common` readiness in default
      buildroot.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified.
- [ ] Status: partial - Full Phase 1/2/3/4 matrix verified.
- [ ] Status: not-verified - Audit/log evidence fully verified.
- [ ] Status: partial - Negative/pass-through matrix verified only for current
      smoke scope.
- [ ] Status: partial - Connector can be marked more than `partial`.

## Current Runtime Counts

| Target | PASS | FAIL | BLOCKED | Evidence |
| --- | ---: | ---: | ---: | --- |
| `make smoke-common` | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.txt` |
| `make test-no-crs` | 60 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt` |
| `make test-with-crs` | 61 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt` |

## CRS Variant Runtime Runs

| Gate | Framework cases present | No-CRS status | With-CRS status | Evidence | Decision |
| --- | --- | --- | --- | --- | --- |
| Basic target | yes | PASS: 60/0/0 | PASS: 61/0/0 | no-crs and with-crs NGINX summaries | Verified for executed scope only. |
| CRS loading | yes | not applicable | PASS | `/src/coreruleset`, CRS preamble, `crs_sqli_anomaly_block` | CRS behavior verified for executed cases. |
| Phase 1 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 2 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 3 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 4 | yes | PASS for pass-through/log-only rows | PASS for pass-through/log-only rows | summary JSON | RESPONSE_BODY blocking not verified. |
| RESPONSE_BODY | yes | not-verified for blocking | not-verified for blocking | `response_body_pass` and NGINX log-only rows | Do not promote. |
| Negative/pass-through | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until complete matrix is documented. |
| Audit/log | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until complete log evidence is documented. |
| Promotion | yes | partial | partial | this matrix | Not more than `partial`. |

## Important Cases

| Variant | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | `action_status_401_phase1_block` | 401 | 401 | PASS |
| With-CRS | `action_status_401_phase1_block` | 403 | 403 | PASS |
| With-CRS | `crs_sqli_anomaly_block` | 403 | 403 | PASS |
| No-CRS/With-CRS | `response_body_pass` | 200 | 200 | PASS, pass-through only |

## NGINX-Specific YAML Note

`modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
contains NGINX-specific YAML files. Current all-scope target summaries include
six NGINX-specific PASS rows. `nginx_phase4_strict_connection_abort.yaml`
exists but is not present in the current No-CRS or With-CRS summaries and is
not counted as PASS here.

## Minimum Evidence For More Than `partial`

- [x] No-CRS PASS for executed NGINX scope.
- [x] With-CRS PASS for executed NGINX scope.
- [x] `phase1_header_block` executed in current summaries.
- [x] Request-body blocking rows executed in current summaries.
- [x] Response-header blocking rows executed in current summaries.
- [ ] Response-body blocking command/result/log evidence.
- [ ] Full audit/log matrix evidence.
- [ ] Startup/reload validation.
- [ ] Complete negative/pass-through matrix evidence.
- [ ] No unresolved gap in the claimed minimum matrix.

## Decision

NGINX remains `partial`. Current `/src` No-CRS, With-CRS, and common targets
pass for their executed scope. RESPONSE_BODY blocking is still not verified and
the complete promotion matrix is not proven.
