# Open Questions

This file separates resolved scaffold/runtime decisions from questions that
still need evidence. Full decision details are in
`connector-scaffold-decisions.md`.

## Current Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked until the default build root has
  ModSecurity V3 sources.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` `make smoke-common`: PASS; Apache 54 PASS and NGINX 54 PASS,
  both 0 FAIL and 0 BLOCKED.
- Current `/src` `make test-no-crs`: PASS; Apache 54 PASS and NGINX 60 PASS,
  both 0 FAIL and 0 BLOCKED.
- Current `/src` `make test-with-crs`: PASS; Apache 55 PASS and NGINX 61 PASS,
  both 0 FAIL and 0 BLOCKED.
- Current With-CRS CRS evidence: `crs_sqli_anomaly_block` PASS for Apache and
  NGINX, expected 403 and actual 403.
- RESPONSE_BODY blocking: not verified.
- Vollstaendige Runtime-Verifikation: nein.

## Resolved Decisions

- Parent connector documentation must reference
  `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md` when it
  points to the shared roadmap inventory. Framework-internal relative roadmap
  references are not changed.
- New connectors must not add a local `connectors/<name>/tests` folder.
  Executable tests are framework-owned and referenced through
  `modules/ModSecurity-test-Framework/tests/cases/`,
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`,
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`, and
  repository Make targets when present.
- NGINX-specific framework YAML cases are available under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- The current NGINX build contract is
  `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`.
- The current NGINX docroot work-parent contract is
  `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.
- Historical NGINX 11 BLOCKED rows are classified as an environment/docroot
  permission blocker and are resolved in current `/src` reruns.
- `make test-no-crs` is a documented target and currently passed for Apache
  and NGINX under `/src`.
- `make test-with-crs` is a documented target and currently passed for Apache
  and NGINX under `/src`.
- CRS loading is evidenced for the current With-CRS run by `/src/coreruleset`,
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`, and
  `crs_sqli_anomaly_block` PASS for both connectors.
- `action_status_401_phase1_block` is now resolved for the current `/src`
  runs by a With-CRS-specific expectation: No-CRS remains expected/actual 401,
  With-CRS is expected/actual 403.
- Framework-local `make quick-check` is resolved as not available in the
  framework Makefile for this workspace; framework-local `make lint` and
  `make check-test-matrix` were run instead and exited 0.
- The shared scaffold status vocabulary is: `template`, `scaffolded`,
  `adapter-owned`, `runtime-smoke-verified`, `crs-verified`, `partial`, and
  `not-verified`.
- Template promotion gates are documented: `scaffolded`, `adapter-owned`,
  `runtime-smoke-verified`, `crs-verified`, and `more-than-partial`.
- Template status is normalized as suitable scaffold, not runtime-verified.
  Origin, metadata, build, No-CRS, With-CRS, coverage matrix, runtime evidence,
  and RESPONSE_BODY blocking are per-connector gates, not Template defects.
- Apache and NGINX phase-by-phase Template alignment reports were added:
  `apache-template-alignment.md` and `nginx-template-alignment.md`.
  Both are aligned for scaffold, origin/license, metadata, build, harness,
  external tests, and executed No-CRS/With-CRS scope; both remain `partial`.

## Still Open / Deferred

- Apache-specific YAML cases remain deferred. Needed evidence: YAML files under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
  plus runtime command output showing expected results. Currently only
  `README.md` was found there.
- RESPONSE_BODY blocking remains deferred. Needed evidence: a repository-backed
  runtime testcase, expected blocking response-body trigger, actual blocking
  result such as HTTP 403, log/report evidence, executed command, affected
  connector, and separate Apache/NGINX documentation for any shared claim.
- Exact CRS/default-action or ModSecurity action-merging cause for the
  With-CRS 403 response remains deferred. Needed evidence: per-connector audit
  evidence or targeted isolation proving the final disruptive rule/action
  mechanics. The runtime mismatch itself is resolved by scoped expectations.
- NGINX-specific `nginx_phase4_strict_connection_abort` runtime status remains
  deferred for the current target summaries. Needed evidence: a current
  summary/result entry for that case and its command result. The YAML file
  exists, but it was not present in the current No-CRS or With-CRS summaries.
- The alternative of generating a materialized `common/include` layout remains
  deferred. Needed evidence: implemented materialization behavior, generated
  path evidence, compiler lines using that path, and runtime smoke results.
- More-than-`partial` Apache/NGINX completeness remains deferred. Needed
  evidence: documented runtime results for `phase1_header_block`,
  request-body blocking, response-header blocking when framework-supported,
  response-body blocking, audit/log evidence, connector startup/reload
  validation, and a negative/pass-through case, with no open FAIL/BLOCKED rows
  in the claimed minimum matrix.
- Default `make smoke-common` without explicit `/src` environment remains
  deferred for this workspace. Needed evidence: run `make fetch-deps` for the
  default `BUILD_ROOT`/`SOURCE_ROOT`, or provide a valid
  `MODSECURITY_SOURCE_DIR`/`MODSECURITY_V3_SOURCE_DIR`, then rerun
  `make smoke-common` and record the result.

## Envoy Open Gates

Envoy bridge-starter work uses the existing global/shared connector gates rather
than copying them into Envoy-specific files. The following Envoy gates remain
open:

- Production upstream origin/license selection beyond local bridge starter.
- libmodsecurity headers/libs and Envoy bridge integration build/runtime logs.
- Harness implementation and evidence paths.
- Separate No-CRS and With-CRS runtime evidence.
- RESPONSE_BODY blocking evidence.
- Negative/pass-through and audit/log evidence.
- Promotion beyond bridge-starter.

## Envoy Build-Starter Open Dependencies

The bridge starter is available, but productive Envoy integration is
still blocked until one path supplies real dependencies:

- native Envoy HTTP filter: Envoy C++ SDK/API headers and build integration;
- external processing: ext_proc protobuf/gRPC generated code and service deps;
- proxy-wasm: proxy-wasm SDK and WASM build toolchain;
- sidecar/bridge: documented protocol, process contract, and runtime harness.

## Envoy Bridge-Starter Open Gates

- Define a real Envoy runtime integration point: sidecar HTTP route, ext_authz,
  ext_proc, native filter, or proxy-wasm.
- Add real libmodsecurity headers/libs and implement transaction lifecycle.
- Produce framework-owned No-CRS and With-CRS result JSON with PASS/FAIL/BLOCKED
  counts.
- Prove CRS loaded/effective behavior for Envoy.
- Keep RESPONSE_BODY as a separate unverified gate until a blocking runtime case
  passes.
## HAProxy Open Items

- Select and document an SPOP parser or SPOE/SPOA protocol library before the
  starter can become a compatible SPOA service.
- Add a HAProxy runtime harness that starts HAProxy with verified SPOE/SPOA
  configuration and the starter/agent endpoint.
- Select and implement the HAProxy-specific libmodsecurity binding strategy.
- Add runtime evidence for No-CRS, With-CRS, RESPONSE_BODY blocking,
  negative/pass-through behavior, and audit/log artifacts.
- Promote beyond `spoa-agent-starter` only after productive adapter build and
  runtime evidence are recorded.
## lighttpd Open Gates

The lighttpd bridge-starter is created/checked, but adapter and runtime gates
remain open or not verified:

- Upstream lighttpd source/version and a concrete integration path are not
  selected.
- Real native-module build is blocked by missing lighttpd headers/SDK/source.
- Real FastCGI/SCGI bridge is blocked by missing protocol adapter and lighttpd
  runtime configuration.
- ModSecurity integration code for lighttpd is not implemented.
- Harness is contract only.
- No-CRS and With-CRS runtime have not been run for lighttpd.
- RESPONSE_BODY blocking, negative/pass-through, and audit/log evidence are not
  verified for lighttpd.
- Promotion beyond bridge-starter/partial is not allowed without per-connector
  runtime evidence.
## Traefik Open Questions

- Which production Traefik integration approach, if any, will be implemented
  remains open.
- Traefik upstream origin/license, production build, harness, No-CRS, With-CRS,
  RESPONSE_BODY, negative/pass-through, and audit/log evidence remain open.
- The current decision-service starter does not select a Traefik plugin,
  middleware, sidecar/proxy, custom module, or Go-service path; `forwardAuth`
  remains starter-only without HTTP/Traefik runtime evidence.
- Traefik must not be promoted beyond decision-service-starter until connector-
  specific runtime evidence is produced and documented.
