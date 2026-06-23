# Compile Lighttpd

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

Document the repository-supported build or prepare path for Lighttpd without adding unverified production claims. This guide is operator-facing and ties build, runtime, and smoke statements to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Open connector runtime path under `connectors/lighttpd/` using Phase 1 `sidecar_proxy`. Lighttpd is built locally from a pinned source tarball when runtime builds are allowed. There is no native Lighttpd ModSecurity connector. Production ready, full matrix ready, CRS complete, and response-body verified are all false.

## What This Builds / Prepares

a pinned Lighttpd source tarball/build/install under the component cache and generated sidecar_proxy smoke artifacts.

## What This Does Not Prove

It does not prove a native Lighttpd module, FastCGI/SCGI/mod_magnet/Lua integration, production readiness, full CRS coverage, full matrix coverage, or response-body support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/lighttpd/src/`, `connectors/lighttpd/harness/`, `connectors/lighttpd/docs/`, `examples/lighttpd/`, `ci/`, and generated reports.

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

`LIGHTTPD_BIN`, `LIGHTTPD_DECISION_BACKEND`, `DECISION_BACKEND`, `ALLOW_RUNTIME_BUILDS`, `CONNECTOR_COMPONENT_CACHE`, `SKIP_RUNTIME_COMPONENT_PREPARE`, `RUNTIME_COMPONENT_STRICT_VERIFY`, and `KEEP_RUNTIME_ARTIFACTS` are present in Makefile exports or harnesses. Version/checksum values are sourced from framework `common.sh` when present. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

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

Lighttpd-specific commands:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
make smoke-lighttpd-modsecurity
make smoke-lighttpd-crs
make smoke-lighttpd-crs-secondary
```

Open connector batch tests:

```sh
make smoke-new-connectors
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

## Production / Production-Style Integration

This is production-style only, not production-ready. A comparable deployment would need the pinned/staged runtime, the `sidecar_proxy` integration path, libmodsecurity for the libmodsecurity backend, ModSecurity rules and optional CRS, and runtime plus sidecar decision/audit logs. Do not treat smoke evidence as production readiness.

## Production / Production-Style Commands

Repository preparation/smoke commands:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
make smoke-lighttpd-modsecurity
make smoke-lighttpd-crs
```

Example config command with placeholder binary:

```sh
<lighttpd-bin> -tt -f examples/lighttpd/lighttpd-sidecar-proxy.conf
<lighttpd-bin> -D -f examples/lighttpd/lighttpd-sidecar-proxy.conf
```

The Lighttpd command flags above are placeholders for operator verification with the staged binary before use. There is no native Lighttpd ModSecurity connector. The current path is sidecar_proxy / Phase 1. FastCGI/SCGI/mod_magnet/Lua are not implemented here.

Expected outputs / evidence:

- `result.json` when produced by the runtime harness.
- `runtime-result.json` when produced by the runtime harness.
- `targeted-result.json` when the targeted libmodsecurity smoke runs.
- `crs-result.json` when the CRS smoke runs.
- `crs-secondary-result.json` when the secondary CRS smoke runs.
- Decision/audit logs when the selected backend supports them.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Run `ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build`, prepare libmodsecurity through `make prepare-runtime-components` when the libmodsecurity backend is used, prepare the `sidecar_proxy` path, then run `make smoke-lighttpd` or the libmodsecurity/CRS variants. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/lighttpd/README.md](examples/lighttpd/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Runtime Evidence Paths

Runtime result/log roots from framework `common.sh` when available and generated reports under `reports/testing/generated/`.

## Logs

Runtime logs when configured plus sidecar or decision-service logs for the libmodsecurity path. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

If the pinned runtime, integration service wiring, libmodsecurity, or CRS is absent, treat the run as blocked or runtime evidence only, not success.

## Common Failures

Missing runtime build permission, missing local Lighttpd binary, missing sidecar wiring, missing libmodsecurity backend, or assuming a native connector exists.

## Cleanup

The repository Makefile writes runtime/build state under `VERIFIED_RUN_ROOT` and related roots, not global install prefixes. Remove the chosen run root only after preserving logs and JSON summaries needed for evidence.

## Best Practices

- Keep build and runtime artifacts outside the git checkout.
- Pin source/runtime versions through existing framework variables; do not introduce undocumented versions in operator docs.
- Treat force-all FAIL rows as evidence of boundaries, not production support.
- Keep request-only operation as the conservative baseline unless generated evidence proves a more specific behavior.

## Related Docs / Examples

- [examples/lighttpd/README.md](examples/lighttpd/README.md)
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
- `reports/testing/generated/`
