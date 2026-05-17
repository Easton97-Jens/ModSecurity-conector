# Roadmap

Status: scaffolded

## Current Roadmap View

| Group | Items |
| --- | --- |
| Now | Keep Apache/NGINX real-world smokes stable; maintain docs/index/link hygiene; keep origin and license maps current |
| Next | Add machine-readable YAML schema; design fixture support for external files; prepare evidence-backed common helpers for config, logging/audit, request/response metadata, status/origin, and intervention representation |
| Later | Evaluate HAProxy, Envoy, Lighttpd, and Traefik only after Common stabilization and a real-world harness plan for each |
| Blocked | `RESPONSE_BODY` blocking common PASS, RAW-ARGS active cases until PR #3564 support is present locally, further upstream code reduction until functionality has a proven replacement |
| Evidence-only | Connector-free v3 API smoke, mapped-only V2/V3 cases, response-body blocking probe, RAW-ARGS PR #3564 evidence |

## Implemented

- Monorepo scaffold.
- Connector-neutral C-first common headers.
- Branch-aware source documentation.
- Test runner and normalizer skeletons.
- CI workflows for structure and documentation checks.
- Connector-free libmodsecurity v3 C API smoke probe source, Makefile runner,
  and prerequisite check.
- Portable `/src` default build flow for the v3 API smoke probe, with local
  `primary_args_phase2` pass observed against `/src/ModSecurity_V3_build`.
- Apache PoC build-preparation helper, runtime smoke harness scaffold, and
  shared minimal YAML cases.
- Apache PoC source-built httpd path with local expected HTTP behavior for all
  current shared minimal cases.
- NGINX PoC build helper and runtime harness using the same shared minimal cases
  and the official `nginx/nginx` GitHub release archive flow, with local
  expected HTTP behavior observed for all current shared minimal cases.
- Formal smoke orchestration through `make smoke-apache`, `make smoke-nginx`,
  `make smoke-common`, and `make smoke-all`.
- Shared YAML schema fields for `capabilities`, pass-through expectations,
  response body checks, and stable audit-log field checks.
- Source-derived imported YAML smoke cases from the local Apache and NGINX
  connector tests, with common vs connector-specific placement documented in
  `docs/testing/test-import-plan.md`.
- Deterministic multipart request materialization, per-case response fixtures,
  and active source-derived common cases for raw JSON body matching, simple
  multipart text-field blocking, and response-body pass-through.
- V2/V3-derived common smoke imports for initial operator, transformation,
  multipart FILES, XML body processor, v3 `@rx`, trim, and `SecAction`
  behavior.
- Capability validation/normalization in the shared runner for multipart,
  files, XML, JSON, response-body, audit-log, collections, operators,
  transformations, actions, rule-parser, and transaction-lifecycle metadata.
- `real-world-connector-path` result metadata for Apache and NGINX smokes,
  including server binary, connector module, libmodsecurity path, and verified
  variable families derived only from passing cases.
- Stabilized status/capability documentation in `docs/architecture/capability-model.md` and
  `docs/architecture/status-model.md`.
- Connector adapter responsibilities documented in
  `docs/architecture/connector-adapter-interface.md`.
- Case matrix generation through `make case-matrix` and
  `docs/testing/case-matrix.md`.
- Maintenance checks through `make lint` and summary rendering through
  `make summary`.
- SonarCloud remediation inventory in `docs/quality/sonarcloud-remediation-plan.md`.
- Controlled Apache and NGINX connector source imports with file-level origin
  maps, documented minimal upstream file sets, and central attribution under
  `licenses/`.
- First common refactor phase documented in `docs/architecture/refactor-phase-1-plan.md`,
  limited to connector-neutral data shapes and documentation.
- Phase 1 connector-neutral common foundation for status, intervention, and
  origin metadata without Apache/NGINX hook or filter extraction.
- C-first connector design decision documented; C++ is limited to thin wrappers,
  test/build tools, and optional helper programs.
- Harness result metadata aligned with common status, origin, and intervention
  models while preserving backward-compatible smoke summaries.
- Apache and NGINX smoke harnesses hardened for generated-runtime pid cleanup
  and deterministic localhost port selection.
- NGINX module source migrated to adapter-owned `connectors/nginx/src`, built
  through `$BUILD_ROOT/nginx-build/connector-src`, with retained upstream
  attribution and PR #377 phase-4 source provenance.

## Planned

- Promote the documented YAML shape into a machine-readable schema.
- Promote imported NGINX-only TX scoring/redirect cases to common only after
  Apache equivalence is tested and documented.
- Add fixture support for external-file operators and connector-specific config
  matrices.
- Promote multipart file-name/file-collection cases only after Apache and NGINX
  both pass them through the shared harness.
- Add a dedicated `smoke-api` target for API-only v3 public C API regression
  candidates; API-only cases are mapped today but not part of connector
  `smoke-all`.
- Expand V2/V3 imports beyond initial text-safe cases after fixture support for
  external files, schema/DTD files, and binary/NUL payload representation is
  designed.
- Re-run SonarCloud after the next CI analysis and close any remaining issues
  that the source-level refactor did not resolve.
- Continue reducing the remaining Apache `connectors/apache/upstream/` import
  only after the equivalent behavior exists in maintained project code,
  attribution remains under `licenses/` and `ORIGIN.md`, and smoke-all still
  passes. The former NGINX `upstream/` tree was removed in phase 10 after the
  adapter-owned source and durable attribution paths were validated.

## Unknown

- HAProxy integration path: SPOE service, Lua, or native filter.
- Envoy integration path: native C++ filter, ext_authz, Lua, or Wasm.
- Lighttpd integration path: native plugin or `mod_magnet`.
- Traefik integration path: Yaegi middleware or Wasm middleware.

These future connector decisions are intentionally deferred until Apache/NGINX
Common metadata and harness behavior remain stable.

## Blocked

- Runtime claims are blocked until each connector has a build, test server,
  repeatable fixtures, and passing connector-specific tests.
- Direct libmodsecurity API smoke is not connector proof; connector pass must
  come from the `real-world-connector-path`.
- v3 API smoke status is `pass` only when the primary `ARGS:test` scenario
  observes intervention status `403`; `fallback pass` is only a minimal API
  proof.
- Fresh environments remain blocked until
  `$MODSECURITY_V3_DIR/src/.libs/libmodsecurity.so` exists in a writable build
  copy.
- Apache PoC runtime is blocked in fresh environments until source downloads,
  PCRE/APR/httpd/libmodsecurity builds, and the module build complete.
- NGINX PoC runtime is blocked in fresh environments until GitHub release
  resolution/downloads, libmodsecurity v3 build, connector module build, and
  runtime smokes complete.
- Response-body blocking remains blocked/xfail for common import until both
  Apache and NGINX return stable HTTP 403 for the same YAML case. PR #377 source
  is applied to adapter-owned NGINX source, but it is not a verification result.
- RAW-ARGS cases remain mapped-only until the configured ModSecurity v3 source
  contains PR #3564 behavior and both Apache and NGINX pass real HTTP smokes.
- `v3_action_nolog_pass_no_audit` remains xfail/mapped-only for active common
  smoke status: local Apache/NGINX probes observed empty audit logs, but GitHub
  Actions observed unexpected audit output.
- XML schema/DTD validation, parser-error cases, file-backed operators,
  malformed multipart bodies, and streaming/body-buffering cases remain mapped
  until the shared harness has explicit fixture and transport support.
