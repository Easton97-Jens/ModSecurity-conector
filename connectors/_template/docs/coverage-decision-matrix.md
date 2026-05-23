# Coverage Decision Matrix

Status: template

This file is a generic coverage and decision pattern for new connectors.

Framework coverage means that YAML cases or framework probes exist. Runtime
verification means that a concrete connector command was executed and produced
a documented result for that connector. New connectors start without runtime
claims and must not add a local `connectors/<name>/tests` folder.

`TEST-COVERAGE-SUMMARY.md` is generated reporting. It can be cited as snapshot
coverage evidence, but it is not by itself runtime proof.

A connector-specific verified runtime claim must link to
`reports/template-verification-nginx-apache/verified-runtime-run.md` or an
equivalent evidence file that records command, result, exit code, and report
paths.

## Status Vocabulary

- `framework-covered`: a YAML/framework case exists, but the connector is not
  runtime-verified by that fact alone.
- `runtime-smoke-verified`: a concrete command was executed and passed for the
  named connector and case.
- `partial`: some structure or runtime evidence exists, but the minimum matrix
  is incomplete.
- `not-verified`: no sufficient runtime evidence exists.
- `fail`: runtime was executed and the expectation was not met.
- `blocked`: the test could not run because of environment, dependency, or
  harness prerequisites.

## Template Checklist

- [x] Status: framework-covered - Framework test paths referenced.
- [x] Status: framework-covered - No local `connectors/<name>/tests` folder.
- [ ] Status: not-verified - Verified runtime run evidence file linked for the
      concrete connector.
- [ ] Status: not-verified - Phase 1 runtime evidence documented.
- [ ] Status: not-verified - Phase 2 request-body runtime evidence documented.
- [ ] Status: not-verified - Phase 3 response-header runtime evidence documented.
- [ ] Status: not-verified - Phase 4 response-body runtime evidence documented.
- [ ] Status: not-verified - RESPONSE_BODY blocking verified with
      command/result/log evidence.
- [ ] Status: not-verified - Audit/log evidence documented.
- [ ] Status: not-verified - Negative/pass-through case documented.
- [x] Status: partial - Connector remains `partial` until required matrix is
      complete.

## Generated Coverage Snapshot

Evidence source: `TEST-COVERAGE-SUMMARY.md`.

- Total YAML cases: 140.
- Common YAML cases: 133.
- Apache-specific YAML cases: 0.
- NGINX-specific YAML cases: 7.
- `runtime_verified=true`: 0.
- RESPONSE_BODY cases: 24.
- RESPONSE_BODY status: not verified or promoted.

## Generic Phase Matrix

| Phase / Bereich | Framework coverage | Runtime evidence required | Template default | Required evidence |
| --- | --- | --- | --- | --- |
| Phase 1 / Request headers, URI, ARGS | framework-covered if cases exist; generated snapshot records Phase 1 count 36 | yes | not-verified | Command, result, report path |
| Phase 2 / Request body, cookies, files, XML/JSON/multipart | framework-covered if cases exist; generated snapshot records Phase 2 count 73 | yes | not-verified | Command, result, report path |
| Phase 3 / Response headers | framework-covered if cases exist; generated snapshot records Phase 3 count 12 | yes | not-verified | Command, result, report path |
| Phase 4 / Response body / outbound | framework-covered if cases exist; generated snapshot records Phase 4 count 20 and RESPONSE_BODY count 20 by collection | yes | not-verified | Blocking evidence, logs, report path |
| Audit/log evidence | framework-covered only if probes exist; generated snapshot records Audit-log probes 24 and `AUDIT_LOG` collection count 0 | yes | not-verified | Audit/log report evidence |
| Negative/pass-through | framework-covered if case exists; generated snapshot includes RESPONSE_BODY pass-through classes but no promotion | yes | not-verified | Expected non-blocking result |

## Minimum Evidence For More Than `partial`

- [ ] `phase1_header_block` or equivalent Phase 1 command/result/report path.
- [ ] Request-body blocking command/result/report path.
- [ ] Response-header blocking command/result/report path when framework
      support exists.
- [ ] Response-body blocking command/result/log evidence.
- [ ] Audit/log evidence.
- [ ] Startup/reload validation.
- [ ] Negative/pass-through case evidence.
- [ ] Connector-specific result recorded separately for each claimed connector.
