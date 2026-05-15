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
- Apache PoC source-built httpd path with local HTTP `403` smoke pass for all
  current shared minimal cases.
- NGINX PoC build helper and runtime harness using the same shared minimal cases
  and the official `nginx/nginx` GitHub release archive flow, with local HTTP
  `403` smoke pass observed for all current shared minimal cases.
- Formal smoke orchestration through `make smoke-apache`, `make smoke-nginx`,
  and `make smoke-all`.

## Planned

- Compile checks for common headers.
- Capability schema for portable vs connector-specific tests.
- Add capability tags to each shared YAML case.
- Add negative/pass-through cases after their source origins are mapped.

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
