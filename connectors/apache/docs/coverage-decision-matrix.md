# Apache Coverage Decision Matrix

Status: partial

This file evaluates Apache coverage using repository evidence only. Generated
coverage reporting is not automatically runtime promotion.

Template alignment report:
`reports/template-verification-nginx-apache/apache-template-alignment.md`.

Apache is aligned with the current Template for scaffold, metadata, build,
harness, No-CRS, and With-CRS executed runtime scope. It remains `partial`
because RESPONSE_BODY blocking and the full minimum matrix are not verified.

Evidence sources:

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/template-verification-nginx-apache/apache-template-alignment.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/apache-summary.json`

## Status Vocabulary

- `framework-covered`: a YAML/framework case exists, but Apache is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete Apache command was executed and passed
  for the named case.
- `crs-verified`: With-CRS command/case has CRS evidence and a passing result.
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
- [x] Status: runtime-smoke-verified - Current `/src` common runtime run:
      54 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: runtime-smoke-verified - Current `/src` No-CRS run:
      54 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: crs-verified - Current `/src` With-CRS run:
      55 PASS, 0 FAIL, 0 BLOCKED.
- [x] Status: crs-verified - `crs_sqli_anomaly_block`: expected 403,
      actual 403.
- [x] Status: runtime-smoke-verified - No-CRS
      `action_status_401_phase1_block`: expected 401, actual 401.
- [x] Status: crs-verified - With-CRS `action_status_401_phase1_block`:
      expected 403, actual 403.
- [ ] Status: blocked - Default `make smoke-common` readiness in default
      buildroot.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified.
- [ ] Status: partial - Full Phase 1/2/3/4 matrix verified.
- [ ] Status: not-verified - Audit/log evidence fully verified.
- [ ] Status: not-verified - Negative/pass-through matrix fully verified.
- [ ] Status: partial - Connector can be marked more than `partial`.

## Current Runtime Counts

| Target | PASS | FAIL | BLOCKED | Evidence |
| --- | ---: | ---: | ---: | --- |
| `make smoke-common` | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.txt` |
| `make test-no-crs` | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt` |
| `make test-with-crs` | 55 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt` |

## CRS Variant Runtime Runs

| Gate | Framework cases present | No-CRS status | With-CRS status | Evidence | Decision |
| --- | --- | --- | --- | --- | --- |
| Basic target | yes | PASS: 54/0/0 | PASS: 55/0/0 | no-crs and with-crs Apache summaries | Verified for executed scope only. |
| CRS loading | yes | not applicable | PASS | `/src/coreruleset`, CRS preamble, `crs_sqli_anomaly_block` | CRS behavior verified for executed cases. |
| Phase 1 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 2 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 3 | yes | PASS for executed rows | PASS for executed rows | summary JSON | Partial until full matrix is complete. |
| Phase 4 | yes | PASS for `response_body_pass` | PASS for `response_body_pass` | summary JSON | Pass-through only; RESPONSE_BODY blocking not verified. |
| RESPONSE_BODY | yes | not-verified for blocking | not-verified for blocking | `response_body_pass` only | Do not promote. |
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

## Minimum Evidence For More Than `partial`

- [x] No-CRS PASS for executed Apache scope.
- [x] With-CRS PASS for executed Apache scope.
- [x] `phase1_header_block` executed in current summaries.
- [x] Request-body blocking rows executed in current summaries.
- [x] Response-header blocking rows executed in current summaries.
- [ ] Response-body blocking command/result/log evidence.
- [ ] Full audit/log matrix evidence.
- [ ] Startup/reload validation.
- [ ] Complete negative/pass-through matrix evidence.
- [ ] No unresolved gap in the claimed minimum matrix.

## Decision

Apache remains `partial`. Current `/src` No-CRS, With-CRS, and common targets
pass for their executed scope. RESPONSE_BODY blocking is still not verified,
Apache-specific YAML cases were not found, and the complete promotion matrix is
not proven.
