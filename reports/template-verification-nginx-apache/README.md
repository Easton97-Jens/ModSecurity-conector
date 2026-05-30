# Template Verification: NGINX and Apache

Status: reviewed

This report folder documents the verification work for turning the connector
template into Apache and NGINX connector documentation, external-test rules,
runtime evidence, CRS/No-CRS test-target results, and scaffold decisions.

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
- Current `/src` `make test-no-crs`: PASS; Apache 54 PASS and NGINX 60 PASS.
- Current `/src` `make test-with-crs`: FAIL; Apache and NGINX each have one
  failing case, `action_status_401_phase1_block`, expected 401 and actual 403.
- `action_status_401_phase1_block` cause: not definitive. Current evidence
  points to a With-CRS expected-status/context mismatch rather than a
  connector-specific issue.
- Current With-CRS `crs_sqli_anomaly_block`: PASS for Apache and NGINX.
- Historical NGINX 11 BLOCKED rows were a docroot permission/environment
  blocker and are resolved in the current `/src` runs.
- RESPONSE_BODY blocking remains not verified.
- Full runtime verification remains no.

## Key Reports

- `connector-scaffold-decisions.md`: accepted and deferred scaffold decisions.
- `template-evaluation.md`: Template suitability evaluation.
- `apache-evaluation.md`: Apache connector evaluation.
- `nginx-evaluation.md`: NGINX connector evaluation.
- `verified-runtime-run.md`: current `/src` runtime evidence, including
  No-CRS and With-CRS sections.
- `nginx-docroot-permission-analysis.md`: NGINX docroot blocker cause and fix.
- `nginx-blocked-runtime-cases.md`: historical 11 BLOCKED rows and current
  resolution.
- `crs-action-status-401-analysis.md`: current With-CRS 401/403 mismatch
  analysis for `action_status_401_phase1_block`.
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

## CRS And No-CRS

No-CRS and With-CRS results are documented separately:

- No-CRS: current `/src` target PASS for Apache and NGINX.
- With-CRS: current `/src` target FAIL for Apache and NGINX because
  `action_status_401_phase1_block` returned 403 instead of expected 401.
- Detailed 401/403 analysis: `crs-action-status-401-analysis.md`.
- CRS SQLi anomaly: current With-CRS case PASS for both connectors.

The With-CRS target result is not blocked. It ran and failed.

## RESPONSE_BODY

RESPONSE_BODY blocking is not verified. The current `response_body_pass` rows
are pass-through evidence only, and NGINX-specific phase-4 rows in the current
summaries are pass-through/log-only evidence. A blocking claim still requires a
real response-body blocking testcase, expected blocking trigger, actual
blocking result such as HTTP 403, logs/reports, command, and per-connector
evidence.
