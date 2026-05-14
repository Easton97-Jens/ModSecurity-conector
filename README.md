# ModSecurity Connector Monorepo

Status: scaffolded

This repository is a monorepo scaffold for future libmodsecurity v3 based
connectors.

Implemented now:

- Connector-neutral headers under `common/include/msconnector/`.
- Documentation that separates local v3/libmodsecurity facts from v2 historical
  and regression-test material.
- Connector directories for Apache, NGINX, HAProxy, Envoy, Lighttpd, and
  Traefik.
- Test layout, normalizer skeletons, runner skeletons, and CI structure checks.
- A connector-free libmodsecurity v3 C API smoke probe build harness under
  `src/v3-api-smoke/`; see `docs/v3-api-smoke-test.md`.
- A local `/src` default v3 smoke run has observed `primary_args_phase2`
  returning intervention status `403`.
- An Apache PoC build helper that can source-build httpd under `BUILD_ROOT`, plus
  a runtime smoke harness scaffold; see `docs/apache-poc.md`.
- A local source-built Apache PoC has observed HTTP `403` for the shared
  `phase2_args_block` case.

Not implemented:

- No complete connector runtime.
- No complete connector regression suite.
- No claim that any connector beyond the local Apache minimal PoC can load, run,
  block, log, or reload rules.
- No claim that the v3 API smoke probe passes until `primary_args_phase2`
  observes status `403`.
- No claim that the Apache PoC is complete beyond the documented minimal
  `ARGS:test` HTTP `403` smoke.

Observed local references:

- `/root/conecter/ModSecurity_V3`: `v3/master`, observed `v3.0.15`
- `/root/conecter/ModSecurity_V2`: `v2/master`, observed `v2.9.13`
- `/root/conecter/ModSecurity-apache`: observed `v0.0.9-beta1-26-g0488c77`
- `/root/conecter/ModSecurity-nginx`: observed `v1.0.4-14-g9eb44fd`

These paths are read-only references, not required build locations. Smoke
builds use `MODSECURITY_V3_SOURCE_DIR`, `MODSECURITY_V3_DIR`, `BUILD_ROOT`, and
`LOG_DIR`; local defaults build under `/src`, while CI can use `$RUNNER_TEMP`.

Apache PoC source-build defaults are also overrideable:

```sh
BUILD_HTTPD_FROM_SOURCE=1
HTTPD_VERSION=2.4.67
APR_VERSION=1.7.6
APR_UTIL_VERSION=1.6.3
BUILD_PCRE2_FROM_SOURCE=1
PCRE2_VERSION=10.47
```

Boundary rule:

- `common/` contains connector-neutral code only.
- `connectors/<name>/` contains server/proxy-specific integration only.
- `tests/common/` contains only portable engine/rule/behavior tests.
- `tests/<connector>/` contains connector-specific behavior tests.

See `docs/architecture.md`, `docs/compatibility.md`, and `docs/roadmap.md`.
See `docs/v3-api-smoke-test.md` for the minimal libmodsecurity v3 API smoke
probe status.
