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
- A shared YAML case runner used by Apache and NGINX PoC smokes.
- A connector-free libmodsecurity v3 C API smoke probe build harness under
  `src/v3-api-smoke/`; see `docs/v3-api-smoke-test.md`.
- A local `/src` default v3 smoke run has observed `primary_args_phase2`
  returning intervention status `403`.
- An Apache PoC build helper that can source-build httpd under `BUILD_ROOT`, plus
  a runtime smoke harness scaffold; see `docs/apache-poc.md`.
- A local source-built Apache PoC has observed the YAML-expected HTTP behavior
  for all current shared minimal cases.
- A scaffolded NGINX PoC build helper and runtime harness use the same shared
  YAML case and source NGINX from the official `nginx/nginx` GitHub release
  archive flow.
- A local source-built NGINX PoC has observed the YAML-expected HTTP behavior
  for all current shared minimal cases.
- Formal connector smoke targets:
  `make smoke-apache`, `make smoke-nginx`, and `make smoke-all`.

Not implemented:

- No complete connector runtime.
- No complete connector regression suite.
- No claim that any connector is complete, reload-safe, production-ready, or
  covered beyond the documented local PoC smokes.
- No claim that the v3 API smoke probe passes until `primary_args_phase2`
  observes status `403`.
- No claim that the Apache PoC is complete beyond the documented shared
  minimal HTTP `403` smokes.
- No claim that the NGINX PoC is complete beyond the documented shared minimal
  HTTP `403` smokes.

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

NGINX PoC source-build defaults are overrideable:

```sh
BUILD_NGINX_FROM_SOURCE=1
NGINX_SOURCE_MODE=github-release
NGINX_GITHUB_REPO=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

When `NGINX_RELEASE_TAG=latest`, the actual tag is resolved at build time and
recorded under `$BUILD_ROOT/logs/nginx/`.

## Shared Smoke Targets

The connector smoke targets reuse build artifacts under `BUILD_ROOT` unless
`REFRESH=1` is set. They never write generated files into this checkout.

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-apache
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-nginx
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
```

`SMOKE_CASES` can restrict the run by case name or file path:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build \
SMOKE_CASES="phase1_header_block phase2_args_block request_body_json_block" \
make smoke-all
```

Current shared minimal cases:

| Case | Source-derived origin | Local Apache | Local NGINX |
| --- | --- | --- | --- |
| `audit_log_phase1_block.yaml` | Apache logging actions and NGINX serial audit-log tests | pass, HTTP 403, audit fields | pass, HTTP 403, audit fields |
| `phase1_header_block.yaml` | Apache request-header/JSON gating and NGINX phase-1 block tests | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_block.yaml` | Apache `00-basics.t` and NGINX `modsecurity.t` ARGS phase-2 tests | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_pass.yaml` | Apache non-matching ARGS rule and NGINX "nothing to detect" tests | pass, HTTP 200, origin body | pass, HTTP 200, origin body |
| `request_body_json_block.yaml` | Apache JSON/body handling and NGINX request-body tests | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_urlencoded_block.yaml` | Apache `ARGS_POST` and NGINX request-body/ARGS_POST tests | pass, HTTP 403 | pass, HTTP 403 |
| `response_header_basic.yaml` | Apache phase tests and NGINX header-filter path | pass, HTTP 403 | pass, HTTP 403 |

These pass observations were made locally on 2026-05-15 with
`BUILD_ROOT=/src/ModSecurity-conector-build`. Other environments must run the
same targets before claiming pass there.

Boundary rule:

- `common/` contains connector-neutral code only.
- `connectors/<name>/` contains server/proxy-specific integration only.
- `tests/common/` contains only portable engine/rule/behavior tests.
- `tests/<connector>/` contains connector-specific behavior tests.

See `docs/architecture.md`, `docs/compatibility.md`, and `docs/roadmap.md`.
See `docs/v3-api-smoke-test.md` for the minimal libmodsecurity v3 API smoke
probe status.
See `docs/nginx-poc.md` for the NGINX PoC build and smoke status rules.
