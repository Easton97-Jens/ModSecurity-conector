# Template Verification: NGINX and Apache

Status: reviewed

This report folder documents the verification work for turning the connector
template into Apache and NGINX connector documentation, external-test rules,
runtime evidence, CRS/No-CRS test-target results, and scaffold decisions.

## Current State

- Documentation/decision commit readiness: yes.
- Local connector test folders are absent:
  `connectors/_template/tests`, `connectors/apache/tests`, and
  `connectors/nginx/tests`, and `connectors/envoy/tests`.
- Executable connector tests are framework-owned, not connector-local.
- Actual framework path: `modules/ModSecurity-test-Framework`.
- Current framework commit referenced by the parent:
  `4bec4d960fea89525db9e439ea567df15943a2e7`.
- Framework-local `make lint`: PASS.
- Framework-local `make quick-check`: target not found; framework-local
  `make check-test-matrix` was run and exited 0.
- Current `/src` `make smoke-common`: Apache 54 PASS, 0 FAIL, 0 BLOCKED;
  NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make smoke-nginx` all-scope: NGINX 60 PASS, 0 FAIL,
  0 BLOCKED.
- Current `/src` `make test-no-crs`: PASS; Apache 54 PASS and NGINX 60 PASS.
- Current `/src` `make test-with-crs`: PASS; Apache 55 PASS and NGINX
  61 PASS, both 0 FAIL and 0 BLOCKED.
- `action_status_401_phase1_block`: resolved for current `/src` runs by a
  scoped With-CRS expectation. No-CRS remains 401/401 PASS; With-CRS is
  403/403 PASS.
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
- `apache-template-alignment.md`: Apache phase-by-phase alignment against the
  current Template gates.
- `nginx-template-alignment.md`: NGINX phase-by-phase alignment against the
  current Template gates.
- `envoy-template-alignment.md`: Envoy bridge-starter alignment against the
  current Template gates.
- `verified-runtime-run.md`: current `/src` runtime evidence, including
  No-CRS and With-CRS sections.
- `nginx-docroot-permission-analysis.md`: NGINX docroot blocker cause and fix.
- `nginx-blocked-runtime-cases.md`: historical 11 BLOCKED rows and current
  resolution.
- `crs-action-status-401-analysis.md`: resolved With-CRS 401/403 expectation
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
| `connectors/_template` | suitable scaffold, not runtime-verified |
| `connectors/apache` | aligned with Template gates for executed scope; runtime status partial |
| `connectors/nginx` | aligned with Template gates for executed scope; runtime status partial |
| `connectors/envoy` | bridge-starter; runtime status not-verified |

For the Template, `suitable scaffold, not runtime-verified` means it is a
usable scaffold for new connectors, not a productive connector implementation.
Origin, metadata, build, No-CRS, With-CRS, coverage matrix, and runtime
evidence are required per concrete connector. For Apache and NGINX, `partial`
does not mean failed. It means some runtime evidence exists, but the minimum
matrix for promotion beyond partial is not complete.

## CRS And No-CRS

No-CRS and With-CRS results are documented separately:

- No-CRS: current `/src` target PASS for Apache and NGINX.
- With-CRS: current `/src` target PASS for Apache and NGINX.
- Detailed 401/403 analysis: `crs-action-status-401-analysis.md`.
- CRS SQLi anomaly: current With-CRS case PASS for both connectors.

The former With-CRS status mismatch is not treated as an adapter bug. It is
resolved by variant-specific framework expectations.

## RESPONSE_BODY

RESPONSE_BODY blocking is not verified. The current `response_body_pass` rows
are pass-through evidence only, and NGINX-specific phase-4 rows in the current
summaries are pass-through/log-only evidence. A blocking claim still requires a
real response-body blocking testcase, expected blocking trigger, actual
blocking result such as HTTP 403, logs/reports, command, and per-connector
evidence.

## Envoy Scaffold Addendum

- `connectors/envoy` was advanced from metadata-only build starter to a local sidecar/HTTP bridge starter.
- Envoy follows the shared connector gates in
  `connector-scaffold-decisions.md` and the global matrix semantics in
  `connectors/_template/docs/coverage-decision-matrix.md`.
- Envoy has bridge-starter code and metadata, no runtime evidence yet, and no
  local `connectors/envoy/tests` folder.
- Envoy-specific files contain connector-specific bridge-starter status and
  references to global/shared rules instead of duplicating those rules.

## Envoy Build-Starter Addendum

- Envoy build status: `bridge-starter` for local sidecar/HTTP bridge compilation.
- Envoy runtime status: `not-verified`; no Envoy runtime harness has run.
- Selected minimal path: repository-local bridge decision model compiled with
  `common/` helper code.
- Deferred production paths: native Envoy HTTP filter, ext_proc service,
  proxy-wasm module, and sidecar/bridge integration until their real
  dependencies and harness evidence exist.

## Envoy Bridge-Starter Addendum

- Envoy bridge status: local CLI self-test PASS for allow/block decision logic.
- Envoy runtime status: `not-verified`; no Envoy runtime harness has run.
- Selected integration path: sidecar/HTTP bridge starter because native Envoy,
  ext_proc, and proxy-wasm dependencies are absent in this repository.
- Missing runtime evidence: Envoy config, bridge integration point, framework
  result JSON, No-CRS/With-CRS split, CRS effective evidence, and RESPONSE_BODY
  evidence.
