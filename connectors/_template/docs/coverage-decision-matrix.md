# Coverage Decision Matrix

Status: template

This file is a generic coverage and promotion matrix for new connectors.
Framework coverage means a case or runner exists. Runtime verification means a
concrete connector command was executed and produced a documented result for
that connector.

New connectors must not add a local `connectors/<name>/tests` folder.
Executable tests are framework-owned.

## Evidence sources to fill in

- Framework cases:
  `modules/ModSecurity-test-Framework/tests/cases/`
- Connector-specific cases:
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- Runner:
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Runtime report:
  `reports/template-verification-nginx-apache/verified-runtime-run.md` or a
  connector-specific equivalent
- Summary JSON:
  `<BUILD_ROOT>/results/.../<connector>-summary.json`

## Status vocabulary

- `framework-covered`: a YAML/framework case exists, but the connector is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete command was executed and passed for the
  named connector and case.
- `crs-verified`: With-CRS command/case has CRS evidence and a passing result.
- `partial`: some structure or runtime evidence exists, but the minimum matrix
  is incomplete.
- `not-verified`: no sufficient runtime evidence exists.
- `fail`: runtime was executed and the expectation was not met.
- `blocked`: the test could not run because of environment, dependency, or
  harness prerequisites.

## Connector variant matrix

| Phase / Gate | Framework cases present | No-CRS status | With-CRS status | Evidence path | Decision |
| --- | --- | --- | --- | --- | --- |
| Phase 1 / Request headers, URI, ARGS | open | not-verified | not-verified | open | partial until executed |
| Phase 2 / Request body, multipart, XML/JSON | open | not-verified | not-verified | open | partial until executed |
| Phase 3 / Response headers | open | not-verified | not-verified | open | partial until executed |
| Phase 4 / Response body | open | not-verified | not-verified | open | RESPONSE_BODY blocking gate required |
| RESPONSE_BODY blocking | open | not-verified | not-verified | open | do not promote from pass-through/log-only |
| Negative/pass-through | open | not-verified | not-verified | open | required before more than partial |
| Audit/log evidence | open | not-verified | not-verified | open | required before more than partial |
| Startup/reload validation | open | not-verified | not-verified | open | required before more than partial |
| CRS-specific behavior | open | not applicable | not-verified | open | required for `crs-verified` |
| Promotion gate | open | not-verified | not-verified | open | blocked until full matrix documented |

## Template checklist

- [x] Status: framework-covered - Framework test paths referenced.
- [x] Status: framework-covered - No local `connectors/<name>/tests` folder.
- [ ] Status: not-verified - Verified runtime run evidence file linked for the
      concrete connector.
- [ ] Status: not-verified - No-CRS result documented.
- [ ] Status: not-verified - With-CRS result documented.
- [ ] Status: not-verified - Phase 1 runtime evidence documented.
- [ ] Status: not-verified - Phase 2 request-body runtime evidence documented.
- [ ] Status: not-verified - Phase 3 response-header runtime evidence
      documented.
- [ ] Status: not-verified - Phase 4 response-body runtime evidence
      documented.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified with
      command/result/log evidence.
- [ ] Status: not-verified - Audit/log evidence documented.
- [ ] Status: not-verified - Negative/pass-through case documented.
- [x] Status: partial - Connector remains `partial` until required matrix is
      complete.

## RESPONSE_BODY gate

Required before claiming RESPONSE_BODY blocking:

- [ ] framework testcase exists
- [ ] expected blocking trigger documented
- [ ] actual blocking result documented, for example HTTP 403
- [ ] log/report evidence documented
- [ ] command documented
- [ ] connector documented
- [ ] Apache and NGINX separately documented if a shared claim is made

## Minimum evidence for more than `partial`

- [ ] No-CRS PASS for the claimed connector/scope.
- [ ] With-CRS PASS for the claimed connector/scope.
- [ ] `phase1_header_block` or equivalent Phase 1 command/result/report path.
- [ ] Request-body blocking command/result/report path.
- [ ] Response-header blocking command/result/report path when framework
      support exists.
- [ ] Response-body blocking command/result/log evidence.
- [ ] Audit/log evidence.
- [ ] Startup/reload validation.
- [ ] Negative/pass-through case evidence.
- [ ] No unresolved FAIL/BLOCKED rows in the claimed minimum matrix.
