# Compile NGINX

## Inhaltsverzeichnis

- [Purpose](#purpose)
- [Current Connector Status](#current-connector-status)
- [What This Builds / Prepares](#what-this-builds--prepares)
- [What This Does Not Prove](#what-this-does-not-prove)
- [Repository Layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [Required Submodules](#required-submodules)
- [Command Quickstart](#command-quickstart)
- [Build / Prepare Variables](#build--prepare-variables)
- [Testing Commands](#testing-commands)
- [Production / Production-Style Integration](#production--production-style-integration)
- [Production / Production-Style Commands](#production--production-style-commands)
- [End-to-End Flow](#end-to-end-flow-fetch-components--build-modsecurity--buildprepare-connector--run-integrated-smoke)
- [Example Configs](#example-configs)
- [Runtime Evidence Paths](#runtime-evidence-paths)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)
- [Common Failures](#common-failures)
- [Cleanup](#cleanup)
- [Best Practices](#best-practices)
- [Related Docs / Examples](#related-docs--examples)


## Purpose

Document the repository-supported build or prepare path for Nginx without adding unverified production claims. This guide is operator-facing and ties build, runtime, and smoke statements to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Adapter-owned NGINX dynamic module under `connectors/nginx/`; request phases are the production-style baseline. Default generated evidence currently reports 60/60 PASS, while force-all evidence still contains FAIL and NOT_EXECUTABLE rows and must not be promoted.

## What This Builds / Prepares

libmodsecurity v3, a local NGINX runtime/module when `BUILD_NGINX_FROM_SOURCE=1`, and `ngx_http_modsecurity_module.so` from `connectors/nginx/`.

## What This Does Not Prove

It does not prove every NGINX release, distro build, module ABI, packaging layout, or complete RESPONSE_BODY support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/nginx/src/`, `connectors/nginx/config`, `connectors/nginx/harness/`, `connectors/nginx/docs/`, `examples/nginx/`, `common/`, `ci/`, and `reports/testing/generated/`.

## Prerequisites

POSIX shell, `make`, Python 3, Git, C/C++ build tools where a native build is performed, network only when explicitly fetching pinned sources/runtime components, and writable runtime roots outside the checkout.

## Required Submodules

```sh
git submodule update --init --recursive
make setup-dev
```

`FRAMEWORK_ROOT` defaults to `modules/ModSecurity-test-Framework`. If the submodule is absent, targets that require `check-framework` block before runtime work starts.

## Command Quickstart

Use this copy/paste baseline for local verification before connector-specific commands:

```sh
git submodule update --init --recursive
make setup-dev
make doctor-quick
make lint
git diff --check
```

Use an isolated local run root when you do not want build/test artifacts under the default `/var/tmp/ModSecurity-conector-verified` tree:

```sh
export VERIFIED_RUN_ROOT=/tmp/modsecurity-conector-verified
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build"
export SOURCE_ROOT="$VERIFIED_RUN_ROOT/src"
export TMP_ROOT="$VERIFIED_RUN_ROOT/tmp"
export LOG_ROOT="$VERIFIED_RUN_ROOT/logs"
```

These are local build/test paths only. They are not global production install paths. Preserve logs, summary JSON, and any generated evidence you need before cleanup.


## Build / Prepare Variables

`BUILD_NGINX_FROM_SOURCE`, `NGINX_BINARY`, `NGINX_MODULE`, `NGINX_PREFIX`, `NGINX_BUILD_DIR`, `NGINX_SOURCE_DIR`, `MODSECURITY_NGINX_SOURCE_DIR`, `MRTS_NATIVE_NGINX_BIN`, and `MRTS_NATIVE_NGINX_MODULE_DIR` are present in the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

## Testing Commands

Common repository checks:

```sh
make quick-check
make smoke-all
make test-no-crs
make test-with-crs
make runtime-matrix
make check-test-matrix
```

Expensive or long-running jobs:

```sh
make runtime-matrix-all-runtime
make full-matrix-parallel-runtime
```

NGINX-specific commands:

```sh
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
FORCE_ALL_CASES=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
CASE=phase1_header_block CRS=no-crs MRTS=no-mrts BUILD_NGINX_FROM_SOURCE=1 make verified-nginx-case
CASE=phase1_header_block CRS=with-crs MRTS=no-mrts BUILD_NGINX_FROM_SOURCE=1 make verified-nginx-case
```

## Production / Production-Style Integration

A production-style NGINX deployment needs libmodsecurity v3 libraries, `ngx_http_modsecurity_module.so` compiled for the deployed NGINX ABI, a top-level `load_module` directive, NGINX `modsecurity on;` and `modsecurity_rules_file` directives in the intended scope, optional CRS includes, and writable NGINX/ModSecurity logs. The repository does not prove every NGINX version or distro build.

## Production / Production-Style Commands

Repository preparation/smoke commands:

```sh
make prepare-runtime-components
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

Operator install example with placeholders:

```sh
sudo install -d -m 0755 /etc/modsecurity /var/log/modsecurity
sudo install -m 0755 <built-ngx_http_modsecurity_module.so> /usr/lib/nginx/modules/ngx_http_modsecurity_module.so
sudo install -m 0644 examples/nginx/modsecurity-request-only.conf /etc/modsecurity/modsecurity-request-only.conf
sudo install -m 0644 examples/nginx/nginx-modsecurity-request-only.conf /etc/nginx/conf.d/modsecurity.conf
sudo nginx -t
sudo nginx -s reload
sudo tail -f /var/log/nginx/error.log /var/log/modsecurity/nginx-audit.log
```

`<built-ngx_http_modsecurity_module.so>` must be compiled for the deployed NGINX ABI. `load_module` placement is top-level NGINX config, not arbitrary nested scope. Replacing the module may require restart depending on packaging and process policy.

Expected outputs / evidence:

- Summary JSON under `BUILD_ROOT` results.
- NGINX access/error logs.
- ModSecurity audit log when enabled.
- Generated NGINX report path under `reports/testing/generated/`.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity through that target, build the dynamic module, then run `BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx` for integrated evidence. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/nginx/README.md](examples/nginx/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Runtime Evidence Paths

`BUILD_ROOT/results/.../nginx`, `NGINX_HARNESS_PARENT`, `LOG_ROOT`, NGINX runtime logs, audit logs, and generated report files under `reports/testing/generated/`.

## Logs

NGINX access/error logs from the harness runtime plus ModSecurity audit logs when enabled. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check missing submodule, NGINX module ABI mismatch, worker traversal permissions for runtime roots, missing libmodsecurity libraries, CRS include paths, and non-promoted phase-4 rows.

## Common Failures

NGINX worker permissions can block generated docroots; a module built for a different NGINX can fail to load; force-all rows may fail without changing production support status.

## Cleanup

The repository Makefile writes runtime/build state under `VERIFIED_RUN_ROOT` and related roots, not global install prefixes. Remove the chosen run root only after preserving logs and JSON summaries needed for evidence.

## Best Practices

- Keep build and runtime artifacts outside the git checkout.
- Pin source/runtime versions through existing framework variables; do not introduce undocumented versions in operator docs.
- Treat force-all FAIL rows as evidence of boundaries, not production support.
- Keep request-only operation as the conservative baseline unless generated evidence proves a more specific behavior.

## Related Docs / Examples

- [examples/nginx/README.md](examples/nginx/README.md)
- `connectors/nginx/README.md`
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
- `reports/testing/generated/`
