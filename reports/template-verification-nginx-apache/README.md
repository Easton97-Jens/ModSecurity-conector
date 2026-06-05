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
- `connectors/lighttpd` now has a repo-owned decision-service bridge starter,
  uses global/shared connector gates, has no runtime evidence, and has no local
  `connectors/lighttpd/tests` folder.

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
- `lighttpd-template-alignment.md`: lighttpd bridge-starter alignment against
  the current Template gates.
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
| `connectors/lighttpd` | bridge-starter only; runtime status not-verified |

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
## HAProxy Current Status

- `connectors/haproxy` now includes repo-authored metadata and a local SPOA
  agent starter under `connectors/haproxy/src/`.
- HAProxy current status: `spoa-agent-starter`.
- Build status: metadata build PASS; local SPOA starter build PASS; local
  ModSecurity binding self-test PASS; productive adapter build BLOCKED.
- Self-test status: local synthetic request-decision self-test PASS.
- Runtime status: `runtime-smoke-verified` for
  `haproxy_phase1_header_block` only.
- The starter uses shared request/intervention/status/origin shapes. The
  diagnostic path now also has live HAProxy to diagnostic SPOA to libmodsecurity
  enforcement evidence for the header-block case, but it does not implement
  full SPOE/SPOA compatibility, load CRS, or verify RESPONSE_BODY.
- No local `connectors/haproxy/tests` folder is used.
- Missing broader runtime evidence: full SPOA implementation, broader Framework
  case runtime, CRS runtime evidence, RESPONSE_BODY evidence, negative/pass-
  through evidence, and audit/log evidence.
- Alignment report: `reports/template-verification-nginx-apache/haproxy-template-alignment.md`.
## lighttpd Bridge-Starter

`connectors/lighttpd` contains repo-owned metadata/probe source plus a local
decision-service bridge starter. This starter uses shared `common/`
origin/status/intervention/capability helpers and does not include lighttpd
headers, call lighttpd APIs, implement FastCGI/SCGI, call ModSecurity APIs, or
provide runtime evidence. A real lighttpd adapter build remains blocked by
missing selected production integration path, lighttpd headers/SDK/source or
bridge dependencies, ModSecurity integration code, and a framework-owned runtime
harness.
## Traefik Decision-Service Starter

- `connectors/traefik` was advanced from metadata build-starter to a
  repo-owned local decision-service starter.
- Traefik follows the shared connector gates in `connector-scaffold-decisions.md`
  and `connectors/_template/docs/coverage-decision-matrix.md`.
- Traefik has local decision-service self-test evidence, no runtime evidence, and
  no local `connectors/traefik/tests` folder.
- Build/self-test commands: `connectors/traefik/build/build-starter.sh` and
  `make -C connectors/traefik self-test-decision-service`.
- Runtime integration path remains deferred until Traefik API/source/SDK or HTTP
  bridge runtime plus harness evidence are selected and documented.
- Detailed alignment: `traefik-template-alignment.md`.

## Framework Connector-Starter Checks

`make connector-starter-checks` runs the framework-owned starter check runner at
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
The command writes local evidence to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

These results are build/self-test evidence only. They are not Apache/NGINX-style
runtime smoke validation, do not install global artifacts, do not create local
`connectors/<name>/tests` directories, and leave runtime status
`not-verified` for starter evidence. RESPONSE_BODY remains not verified.

## New Connector Runtime-Smoke Entry Points

The framework now exposes runtime-smoke entrypoints for Envoy, HAProxy,
lighttpd, and Traefik through `make smoke-envoy`, `make smoke-haproxy`,
`make smoke-lighttpd`, and `make smoke-traefik`. These targets write runtime
evidence files under `/src/ModSecurity-conector-build/results/`.

Current status is PASS for HAProxy's single `haproxy_phase1_header_block`
runtime smoke and BLOCKED for Envoy, lighttpd, and Traefik. The aggregate
`make smoke-new-connectors` remains diagnostic and exits BLOCKED while any new
connector runtime remains unverified instead of summarizing blocked states as
PASS.
