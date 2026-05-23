# Template Verification: NGINX and Apache

Status: reviewed

This report folder documents the verification work for turning the connector
template into Apache and NGINX connector documentation, external-test rules,
runtime evidence, and scaffold decisions.

## Current State

- Documentation/decision commit readiness: yes.
- Local connector test folders are absent:
  `connectors/_template/tests`, `connectors/apache/tests`, and
  `connectors/nginx/tests`.
- Executable connector tests are framework-owned, not connector-local.
- Current `/src` `make smoke-common`: Apache 54 PASS, 0 FAIL, 0 BLOCKED;
  NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make smoke-nginx` all-scope: NGINX 60 PASS, 0 FAIL,
  0 BLOCKED.
- Historical NGINX 11 BLOCKED rows were a docroot permission/environment
  blocker and are resolved in the current `/src` runs.
- RESPONSE_BODY blocking remains not verified.
- Full runtime verification remains no.

## Key Reports

- `connector-scaffold-decisions.md`: accepted and deferred scaffold decisions.
- `template-evaluation.md`: Template suitability evaluation.
- `apache-evaluation.md`: Apache connector evaluation.
- `nginx-evaluation.md`: NGINX connector evaluation.
- `verified-runtime-run.md`: current `/src` runtime evidence.
- `nginx-docroot-permission-analysis.md`: NGINX docroot blocker cause and fix.
- `nginx-blocked-runtime-cases.md`: historical 11 BLOCKED rows and current
  resolution.
- `nginx-build-fail-analysis.md`: earlier NGINX include-path build failure and
  build-contract verification.
- `summary.md`: final summary and readiness status.
- `findings.md`: repository-backed findings.
- `open-questions.md`: remaining deferred items.
- `files-reviewed.md`: reviewed files and evidence paths.

## Evaluation Results

| Target | Rating |
| --- | --- |
| `connectors/_template` | partially suitable |
| `connectors/apache` | partial |
| `connectors/nginx` | partial |

`partial` does not mean failed. It means some runtime evidence exists, but the
minimum matrix for promotion beyond partial is not complete.

## RESPONSE_BODY

RESPONSE_BODY blocking is not verified. The current `response_body_pass` rows
are pass-through evidence only. A blocking claim still requires a real
response-body blocking testcase, expected blocking trigger, actual blocking
result such as HTTP 403, logs/reports, command, and per-connector evidence.
