# Roadmap

Status: scaffolded

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
  `docs/test-import-plan.md`.

## Planned

- Compile checks for common headers.
- Promote the documented YAML shape into a machine-readable schema.
- Promote imported NGINX-only TX scoring/redirect cases to common only after
  Apache equivalence is tested and documented.
- Add fixture support for external-file operators, multipart bodies, and
  connector-specific config matrices.

## Unknown

- HAProxy integration path: SPOE service, Lua, or native filter.
- Envoy integration path: native C++ filter, ext_authz, Lua, or Wasm.
- Lighttpd integration path: native plugin or `mod_magnet`.
- Traefik integration path: Yaegi middleware or Wasm middleware.

## Blocked

- Runtime claims are blocked until each connector has a build, test server,
  repeatable fixtures, and passing connector-specific tests.
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
