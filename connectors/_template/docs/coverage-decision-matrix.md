# Coverage Decision Matrix

Status: suitable scaffold, not runtime-verified

Deutsch: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert.

This file is a generic coverage and promotion matrix for new connectors.
Framework coverage means a case or runner exists. Runtime verification means a
concrete connector command was executed and produced a documented result for
that connector.

New connectors must not add a local `connectors/<name>/tests` folder.
Executable tests are framework-owned.

Runtime evidence is not applicable to the Template itself. It must be supplied
by each concrete connector.

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
| Phase 1 / Request headers, URI, ARGS | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 2 / Request body, multipart, XML/JSON | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 3 / Response headers | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 4 / Response body | fill per connector | required per connector | required per connector | required per connector | RESPONSE_BODY blocking gate |
| RESPONSE_BODY blocking | fill per connector | runtime promotion gate | runtime promotion gate | required per connector | do not promote from pass-through/log-only |
| Negative/pass-through | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| Audit/log evidence | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| Startup/reload validation | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| CRS-specific behavior | fill per connector | not applicable | required per connector | required per connector | required for `crs-verified` |
| Promotion gate | fill per connector | required per connector | required per connector | required per connector | blocked until full matrix documented |

## Template checklist

- [x] Status: framework-covered - Framework test paths referenced.
- [x] Status: framework-covered - No local `connectors/<name>/tests` folder.
- [x] Status: intentionally external - Executable tests are framework-owned
      and must be referenced, not copied into `connectors/_template/tests`.
- [ ] Status: per-connector gate - Verified runtime run evidence file linked
      for the concrete connector.
- [ ] Status: per-connector gate - No-CRS result documented.
- [ ] Status: per-connector gate - With-CRS result documented.
- [ ] Status: per-connector gate - Phase 1 runtime evidence documented.
- [ ] Status: per-connector gate - Phase 2 request-body runtime evidence
      documented.
- [ ] Status: per-connector gate - Phase 3 response-header runtime evidence
      documented.
- [ ] Status: per-connector gate - Phase 4 response-body runtime evidence
      documented.
- [ ] Status: runtime promotion gate - RESPONSE_BODY blocking verified with
      command/result/log evidence.
- [ ] Status: per-connector gate - Audit/log evidence documented.
- [ ] Status: per-connector gate - Negative/pass-through case documented.
- [x] Status: suitable scaffold - Template remains not runtime-verified; each
      concrete connector remains `partial` until required matrix is complete.

## RESPONSE_BODY gate

Required before claiming RESPONSE_BODY blocking:

- [ ] framework testcase exists
- [ ] expected blocking trigger documented
- [ ] actual blocking result documented, for example HTTP 403
- [ ] log/report evidence documented
- [ ] command documented
- [ ] connector documented
- [ ] Apache and NGINX separately documented if a shared claim is made

This is not a Template failure. It is a runtime promotion gate for concrete
connectors.

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

## Decision

Das Template ist als Scaffold-Vorlage geeignet. Es ist bewusst nicht
runtime-verifiziert und enthält keine produktive Connector-Implementierung.
Neue Connectoren müssen die per-connector Gates für Origin, Metadata, Build,
No-CRS, With-CRS, Coverage Matrix und Runtime Evidence erfüllen, bevor sie über
partial hinaus bewertet werden können.
