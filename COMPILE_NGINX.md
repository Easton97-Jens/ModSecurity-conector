# Compile NGINX

## Purpose

This guide documents the repository-supported NGINX build and runtime-smoke
path from a clean clone. It covers the dynamic-module flow used by
`make smoke-nginx`, supported variables, and the evidence paths used by the
generated reports.

## Current Connector Status

- Connector: adapter-owned NGINX dynamic module under `connectors/nginx/`.
- Default runtime evidence: 60 attempted / 60 PASS.
- Force-all runtime evidence: 140 attempted / 95 PASS / 39 FAIL / 0 BLOCKED / 6 NOT_EXECUTABLE.
- Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is documented as runtime evidence only.

## What This Builds

- libmodsecurity v3 under `BUILD_ROOT`.
- A local NGINX source/build tree when `BUILD_NGINX_FROM_SOURCE=1`.
- The repo-owned `ngx_http_modsecurity_module.so` dynamic module.
- Per-case local NGINX runtime directories and smoke evidence under `BUILD_ROOT`.

## What Not Prove

- It does not prove every NGINX release, distro package, module set, or production configuration.
- It does not promote force-all FAIL rows or former expected-failure rows.
- It does not promote full RESPONSE_BODY support.
- Generated markdown is reporting only; runtime proof comes from smoke summary JSON and per-case logs.

## Repository Layout

| Path | Meaning |
|---|---|
| `connectors/nginx/` | NGINX connector source, module `config`, metadata, and harness |
| `connectors/nginx/src/` | Productive NGINX adapter source |
| `connectors/nginx/harness/` | Runtime smoke config template and runner |
| `common/` | Connector-neutral metadata and helper shapes |
| `modules/ModSecurity-test-Framework/` | YAML cases, runners, generators, and smoke orchestration |
| `reports/testing/` | Parent-repository generated runtime reports |

## Prerequisites

- POSIX shell, `make`, C/C++ build tools, `git`, `curl`, `python3`.
- Python dependencies from `make setup-dev`.
- Network access only when fetching libmodsecurity, NGINX, or CRS.
- A writable absolute `BUILD_ROOT` outside the git checkout.

## Required Submodules

```sh
git clone <repo-url> ModSecurity-conector
cd ModSecurity-conector
git submodule update --init --recursive
make setup-dev
```

Use `FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework` only when using a separate framework checkout.

## Build Variables

The supported variables below are consumed by the current Makefile or shell helpers.

## Full Variable Reference Table

| Variable | Required | Default | Example | Used by | Meaning | Notes |
|---|---|---|---|---|---|---|
| `FRAMEWORK_ROOT` | No | `$(CURDIR)/modules/ModSecurity-test-Framework` | `/work/ModSecurity-test-Framework` | Makefile, framework scripts | Test framework checkout | Must contain `ci/` and `tests/runners/` |
| `CONNECTOR_ROOT` | No | current repo | `/work/ModSecurity-conector` | Makefile, harnesses | Connector repository root | Root Makefile exports this as `$(CURDIR)` |
| `BUILD_ROOT` | No | `/src/ModSecurity-conector-build` | `/tmp/mscon-build` | all build/smoke helpers | Generated build, runtime, logs, and results root | Must be absolute and outside the checkout |
| `SOURCE_ROOT` | No | `/src` | `/src` | fetch/build helpers | Source checkout root | The helpers keep fetched sources under this root |
| `MODSECURITY_GIT_REF` | No | `v3/master` | `v3.0.15` | fetch helpers | libmodsecurity git ref | Alias for `MODSECURITY_V3_GIT_REF` |
| `MODSECURITY_SOURCE_DIR` | No | `$SOURCE_ROOT/ModSecurity_V3` | `/src/ModSecurity_V3` | build helpers | Existing libmodsecurity source tree | Also feeds `MODSECURITY_V3_SOURCE_DIR` |
| `REFRESH` | No | unset | `1` | prepare/fetch helpers | Recreate generated source/build trees | Use intentionally; it refreshes generated state |
| `FORCE_ALL_CASES` | No | unset | `1` | case discovery, smoke runners | Attempt materializable former-XFAIL/future/gap rows | Evidence only; does not promote support |
| `SMOKE_CASES` | No | unset | `phase1_header_block phase2_args_block` | case discovery | Limit smoke to named cases | Space-separated case names or paths |
| `BUILD_NGINX_FROM_SOURCE` | No | unset | `1` | NGINX prepare helper | Build local NGINX runtime/module | Recommended for reproducible local smoke |
| `NGINX_BINARY` | No | `$NGINX_PREFIX/sbin/nginx` | `/usr/sbin/nginx` | NGINX harness/prepare helper | NGINX executable | Use with a matching module path |
| `NGINX_SOURCE_DIR` | No | resolved by prepare helper | `/src/nginx` | NGINX prepare helper | Existing NGINX source tree | Used when providing source directly |
| `MODSECURITY_NGINX_SOURCE_DIR` | No | `$CONNECTOR_ROOT/connectors/nginx` | `/src/ModSecurity-nginx` | NGINX prepare helper | NGINX connector source input | Repo-local source is the default |
| `NGINX_PREFIX` | No | `$BUILD_ROOT/nginx-runtime/nginx` | `/tmp/mscon-build/nginx-runtime/nginx` | NGINX harness | Runtime prefix | Generated |
| `NGINX_MODULE` | No | `$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so` | `/tmp/mscon-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` | NGINX harness | Dynamic module path | Supported variable is `NGINX_MODULE`, not `NGINX_MODULE_PATH` |
| `NGINX_HARNESS_PARENT` | No | `$BUILD_ROOT` | `/tmp/mscon-build` | NGINX harness | Parent for generated runtime work dirs | Generated |
| `LOG_DIR` | No | `$NGINX_HARNESS_WORK_ROOT/logs` | `/tmp/mscon-build/nginx-runtime/logs` | NGINX harness | Per-run/per-case log root | Generated |
| `RESULTS_DIR` | No | `$BUILD_ROOT/results` | `/tmp/mscon-build/results` | NGINX harness | Summary JSON/TXT output root | Force-all defaults to `$BUILD_ROOT/results/force-all` |
| `RUNTIME_BASE` | No | `$NGINX_HARNESS_WORK_ROOT/runtime` | `/tmp/mscon-build/nginx-runtime/runtime` | NGINX harness | Per-case runtime root parent | Generated |
| `RUNTIME_ROOT` | No | `$RUNTIME_BASE/<case>` | `/tmp/mscon-build/nginx-runtime/runtime/phase1_header_block` | NGINX harness | One case runtime root | Used for selected-case runs |
| `PORT` | No | `18081` | `19081` | NGINX harness | Local listener base port | Harness searches for a free port |
| `MODSECURITY_RULE_PREAMBLE_FILE` | No | unset | `$BUILD_ROOT/crs/modsecurity-crs-preamble.conf` | CRS variant smoke | Rules prepended before generated case rules | Required for `MODSECURITY_TEST_VARIANT=with-crs` |

Unsupported as current repository variables: `VERBOSE`, `DEBUG`, `NGINX_PORT`, `NGINX_CONF`, `NGINX_LOG_DIR`, and `NGINX_MODULE_PATH`. Use `PORT`, generated config paths, `LOG_DIR`, and `NGINX_MODULE` instead.

## Minimal Local Build

```sh
git submodule update --init --recursive
make setup-dev
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Rebuild / Refresh

```sh
REFRESH=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

Use a separate build root for independent reproductions:

```sh
BUILD_ROOT=/tmp/mscon-nginx-build SOURCE_ROOT=/src REFRESH=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Manual Build Flow

The helper flow is the source of truth. A manual reproduction follows the same shape:

```sh
make fetch-deps
BUILD_NGINX_FROM_SOURCE=1 sh modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh
NGINX_BINARY=/path/to/nginx make smoke-nginx
```

## Production-Style Install / Deploy

- Install `ngx_http_modsecurity_module.so` into the NGINX modules directory.
- Load it from `/etc/nginx/nginx.conf` with `load_module`.
- Keep ModSecurity config in `/etc/modsecurity/`.
- Keep CRS in `/etc/modsecurity/crs/`.
- Write connector decisions under `/var/log/modsecurity/` and server logs under `/var/log/nginx/`.
- Reload/restart NGINX after changing loaded modules, ModSecurity config, CRS, or connector directives.

## Test / Smoke Validation

```sh
make quick-check
make smoke-nginx
FORCE_ALL_CASES=1 make smoke-nginx
make generate-test-matrix
make check-test-matrix
```

Expected current default evidence is 60 attempted / 60 PASS. Current force-all evidence contains expected FAIL and NOT_EXECUTABLE rows and is not a support promotion.

## Runtime Evidence Paths

| Evidence | Path |
|---|---|
| Default summary | `$BUILD_ROOT/results/nginx-summary.json` |
| Default JSONL | `$BUILD_ROOT/results/nginx-results.jsonl` |
| Force-all summary | `$BUILD_ROOT/results/force-all/nginx-summary.json` |
| Per-case logs | `$NGINX_HARNESS_WORK_ROOT/logs/<case>/` |
| Generated report | `reports/testing/generated/nginx-runtime-results.generated.md` |

## Generated Artifacts

- `$BUILD_ROOT/nginx-build/`
- `$BUILD_ROOT/nginx-runtime/`
- `$BUILD_ROOT/results/nginx-summary.json`
- `$BUILD_ROOT/logs/`

## Logs

Per-case logs include NGINX access/error logs, generated config, curl errors, `phase4.log`, `response-body.txt`, `audit.log`, and normalized `result.json`.

## Troubleshooting

- Missing framework: run `git submodule update --init --recursive` or set `FRAMEWORK_ROOT`.
- Module mismatch: rebuild NGINX and the dynamic module together.
- CRS run blocked: run `make prepare-crs` or use `make test-with-crs`.
- Port conflict: set `PORT` to another base port.

## Common Failures

- Build dependency missing: install compiler and NGINX build prerequisites or let the helper build locally.
- Generated path rejected: use absolute `BUILD_ROOT`, `LOG_DIR`, and `RUNTIME_ROOT` outside the checkout.
- Response-body mismatch: treat as bounded evidence only; do not promote RESPONSE_BODY.

## Cleanup

```sh
rm -rf /src/ModSecurity-conector-build/nginx-build
rm -rf /src/ModSecurity-conector-build/nginx-runtime
rm -rf /src/ModSecurity-conector-build/logs/nginx*
```

## Best Practices

- Prefer clean `BUILD_ROOT` values for evidence runs.
- Record exact commands and summary JSON paths in review notes.
- Keep generated runtime artifacts out of git.
- Stage generated markdown only after `make generate-test-matrix`.

## Related Docs / Examples

- `examples/nginx/README.md`
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`
