# Findings

All findings below are based on files, paths, commands, or local `/src`
runtime results reviewed in this repository.

## Repository And Framework State

- Parent repository path: `/root/git/ModSecurity-conector`.
- Framework submodule path: `modules/ModSecurity-test-Framework`.
- Framework submodule base commit:
  `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18`.
- Framework submodule working tree is modified for the CRS expectation work.
- No Apache or NGINX adapter source files were changed for this task.

## CRS Expectation Change

- Testcase path:
  `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`.
- Base expectation remains No-CRS: expected 401.
- With-CRS expectation is now variant-specific:
  `expect.variants.with-crs.status: 403`.
- Framework runner paths updated to resolve variant expectations:
  `modules/ModSecurity-test-Framework/tests/runners/runner_core.py` and
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Framework docs updated:
  `modules/ModSecurity-test-Framework/tests/README.md` and
  `modules/ModSecurity-test-Framework/tests/runners/README.md`.

## Current Runtime Results

| Command | Result | Evidence |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | PASS | Matrix check exited 0. |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Framework-local lint exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Framework-local matrix check exited 0 with a warning about missing `config/testing/import-status.json`. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS; NGINX 61 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |

Evidence files:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/nginx-summary.txt`

## Action Status 401 Case

- No-CRS Apache: `action_status_401_phase1_block` PASS, expected 401, actual
  401.
- No-CRS NGINX: `action_status_401_phase1_block` PASS, expected 401, actual
  401.
- With-CRS Apache: `action_status_401_phase1_block` PASS, expected 403, actual
  403.
- With-CRS NGINX: `action_status_401_phase1_block` PASS, expected 403, actual
  403.

Detailed report:
`reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## CRS Evidence

- Framework `ci/common.sh` pins CRS to `CRS_GIT_REF=v4.26.0`.
- Current With-CRS run observed CRS source at `/src/coreruleset`.
- Current With-CRS run observed CRS preamble at
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
  exists.
- `crs_sqli_anomaly_block` PASS for Apache and NGINX in the current With-CRS
  run, expected 403 and actual 403.

## Template

- `connectors/_template/README.md` now documents a repeatable connector flow,
  required evidence, No-CRS/With-CRS validation, coverage matrix, promotion
  gates, and claims that must not be made.
- `connectors/_template/TODO.md` is organized into phases 0 through 7.
- `connectors/_template/docs/coverage-decision-matrix.md` separates framework
  cases, No-CRS status, With-CRS status, evidence path, and decision.
- `connectors/_template/tests` is absent. Executable Template tests are not
  maintained connector-locally.

## External Tests

- Framework testcases are under `modules/ModSecurity-test-Framework/tests/cases/`.
- Connector-specific framework paths are under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`.
- NGINX-specific YAML files exist under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Apache-specific YAML files were not found under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- New connector scaffolds must not create local `connectors/<name>/tests`
  directories.

## NGINX

- `connectors/nginx/` is present and adapter-owned.
- `connectors/nginx/tests` is absent.
- Current `/src` NGINX common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX No-CRS target passed: 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX With-CRS target passed: 61 PASS, 0 FAIL, 0 BLOCKED.
- `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` remains the accepted
  NGINX build include contract.
- RESPONSE_BODY blocking remains not verified for NGINX. Current response-body
  rows are pass-through or log-only evidence.

## Apache

- `connectors/apache/` is present and adapter-owned.
- `connectors/apache/tests` is absent.
- Current `/src` Apache common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache No-CRS target passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache With-CRS target passed: 55 PASS, 0 FAIL, 0 BLOCKED.
- Apache-specific framework YAML files were not found.
- RESPONSE_BODY blocking remains not verified for Apache. `response_body_pass`
  is pass-through evidence only.

## Decisions

- `connectors/_template`: suitable scaffold, not runtime-verified; not a
  productive connector implementation.
- `connectors/apache`: aligned with current Template gates for scaffold,
  origin/license, metadata, build, harness, external tests, and executed
  No-CRS/With-CRS scope; runtime status remains partial. See
  `apache-template-alignment.md`.
- `connectors/nginx`: aligned with current Template gates for scaffold,
  origin/license, metadata, build, harness, external tests, and executed
  No-CRS/With-CRS scope; runtime status remains partial. See
  `nginx-template-alignment.md`.
- No-CRS runtime evidence: PASS for both connectors in current `/src` run.
- With-CRS runtime evidence: PASS for both connectors in current `/src` run.
- CRS SQLi anomaly case: PASS for both connectors.
- RESPONSE_BODY blocking: not verified.
- Full runtime verification: no.

## Envoy Scaffold Finding

- `connectors/envoy` exists as a sidecar/HTTP bridge-starter connector.
- Envoy follows global/shared connector gates from
  `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
  and references `connectors/_template/docs/coverage-decision-matrix.md` for
  shared matrix semantics.
- No local `connectors/envoy/tests` folder exists.
- No Envoy runtime evidence, productive adapter-owned source, production build
  evidence, or harness implementation is documented.
- Envoy runtime status is `not-verified`; promotion beyond bridge-starter
  is not allowed without future evidence.

## Envoy Build-Starter Finding

- Envoy has `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h`, a local
  `Makefile`, `build/build_metadata.sh`, and `src/envoy_bridge*` for local
  bridge-starter compilation.
- The bridge starter uses `common/include/msconnector/request.h`,
  `intervention.h`, `status.h`, `origin.h`, and `capabilities.h`, plus the
  corresponding common helper sources.
- No real Envoy API is used because no Envoy SDK/API dependency is present in
  this repository.
- ModSecurity bridge, Envoy runtime harness, No-CRS, With-CRS, and RESPONSE_BODY
  validation remain blocked/deferred.

## Envoy Build-Starter Result

- `make -C connectors/envoy build-starter` passed for bridge-starter compilation.
- `make -C connectors/envoy self-test` passed for local allow/block decision logic.
- The result does not use Envoy API and does not prove runtime compatibility.

## Envoy Bridge-Starter Finding

- The selected Envoy path is a sidecar/HTTP bridge starter, not a native Envoy
  filter, ext_proc service, or proxy-wasm module.
- The local bridge self-test can model request header and URI/query data and
  return a 403 `msconnector_intervention`.
- The self-test does not use Envoy API, libmodsecurity API, CRS, or framework
  YAML cases.
## HAProxy

- HAProxy implementation remains a starter, not a productive adapter.
- Current status is `spoa-agent-starter`; runtime status remains
  `not-verified`.
- The local SPOA agent starter compiles and self-tests synthetic
  request-decision logic using shared request/intervention/status data shapes.
- The starter does not include HAProxy headers, libmodsecurity headers, CRS
  loading, network handling, or a runtime harness.
- A separate minimal diagnostic SPOP handshake subset now self-tests local
  HELLO/AGENT-HELLO, NOTIFY-to-empty-ACK, and DISCONNECT handling. It is not a
  full SPOA agent implementation.
- Framework `ci/prepare-haproxy-runtime.sh` can now prepare HAProxy `3.2.19`
  locally under `/src/ModSecurity-conector-build` after verifying the official
  checksum and `TARGET=linux-glibc` support from the downloaded source Makefile.
- `make smoke-haproxy` is still BLOCKED, but now records granular prerequisite
  diagnostics in `/src/ModSecurity-conector-build/results/haproxy-summary.json`.
- Generated SPOE config is syntax-valid by `haproxy -c`, with
  `spoe_runtime_status: diagnostic-handshake-verified` when fresh agent-log
  evidence appears after the run marker.
- Current HAProxy runtime blocker is missing ModSecurity binding.
- Productive adapter build remains BLOCKED because the repository still lacks a
  full ModSecurity transaction binding, Framework-case runtime evidence, and
  libmodsecurity binding strategy.
- No local `connectors/haproxy/tests` folder is used.
- RESPONSE_BODY blocking remains not verified.
## lighttpd Bridge-Starter Finding

- `connectors/lighttpd` is bridge-starter only and runtime status is
  not-verified.
- Repo-owned metadata/probe source, bridge-starter source, `build/*.sh`, and
  local Make targets provide compile/self-test checks using shared `common/`
  helpers.
- `connectors/lighttpd/build/build_starter.sh`, `make -C connectors/lighttpd
  build-bridge-starter`, and `make -C connectors/lighttpd self-test-bridge`
  PASS prove only local starter compilation/self-test; the bridge probe reports
  a blocked local decision.
- The lighttpd docs reference global connector gates instead of copying status
  vocabulary, promotion gates, No-CRS/With-CRS separation, runtime evidence
  rules, and RESPONSE_BODY requirements into connector-specific docs.
- No local `connectors/lighttpd/tests` folder is present or required.
- No lighttpd API, FastCGI/SCGI protocol implementation, ModSecurity API,
  runtime harness, runtime evidence, adapter implementation, or runtime
  PASS/FAIL/BLOCKED count is claimed.
## Traefik Decision-Service Starter Finding

- `connectors/traefik` now has a repo-owned local decision-service starter.
- The Traefik docs reference shared connector gates and coverage rules instead
  of duplicating global rules locally.
- Traefik has local self-test evidence only, no implemented runtime harness, no
  production Traefik adapter build, and no local `connectors/traefik/tests`
  folder.
- Missing production dependencies include a selected Traefik API/source/SDK or
  HTTP bridge runtime strategy, libmodsecurity runtime integration point, Traefik
  configuration, and harness configuration/evidence paths.

## Connector-Starter Framework Finding

- `modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`
  provides a framework-owned local runner for Envoy, HAProxy, lighttpd, and
  Traefik starter build/self-test checks.
- `make connector-starter-checks` writes `summary.json`, `results.jsonl`, and
  per-check stdout/stderr logs under
  `/src/ModSecurity-conector-build/results/connector-starters/`.
- Each `results.jsonl` entry records `test_type: connector-starter`,
  `runtime_verified: false`, `runtime_status: not-verified`,
  `response_body_verified: false`, and `installs_global_artifacts: false`.
- The framework runner is not a server/proxy harness and does not prove No-CRS,
  With-CRS, CRS, RESPONSE_BODY, audit/log, or runtime-smoke behavior.

## New Connector Runtime-Smoke Finding

- The framework now has runtime-smoke entrypoints for Envoy, HAProxy, lighttpd,
  and Traefik.
- The Envoy/HAProxy/lighttpd/Traefik harness folders now contain executable
  `run_<name>_smoke.sh` entrypoints. They write BLOCKED diagnostic evidence
  with `runtime_verified: false` because real server/proxy harnesses are not
  implemented.
- `smoke-new-connectors` is not allowed to turn blocked diagnostics into PASS;
  with all four runtime harnesses missing, the aggregate status remains
  BLOCKED and `Runtime not verified`.
- All runtime-smoke evidence paths are under `/src/ModSecurity-conector-build`.
