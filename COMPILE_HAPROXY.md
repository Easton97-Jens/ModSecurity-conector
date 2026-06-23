# Compile HAProxy

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

Document the repository-supported build or prepare path for Haproxy without adding unverified production claims. This guide is operator-facing and ties build, runtime, and smoke statements to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

SPOE/SPOP path using HAProxy plus `haproxy-modsecurity-spoa` and libmodsecurity. Default evidence reports 55/55 PASS; force-all evidence contains FAIL and NOT_EXECUTABLE rows. RESPONSE_BODY is not promoted.

## What This Builds / Prepares

a local HAProxy binary, `haproxy-modsecurity-spoa`, libmodsecurity binding/self-test pieces, SPOE config, decisions, audit logs, and smoke summaries under runtime roots.

## What This Does Not Prove

It does not prove OS-wide installation, every HAProxy build option, full RESPONSE_BODY support, or production support for force-all FAIL rows. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/haproxy/src/`, `connectors/haproxy/harness/`, `connectors/haproxy/docs/`, `connectors/haproxy/poc/spoe/`, `examples/haproxy/`, `ci/`, and `reports/testing/generated/`.

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

`HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_RUNTIME_DIR`, `HAPROXY_BIN`, `BUILD_ROOT`, `SOURCE_ROOT`, `LOG_ROOT`, and `RESULTS_DIR` are exported by the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

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

HAProxy-specific commands:

```sh
make smoke-haproxy
make test-haproxy-no-crs
make test-haproxy-with-crs
make runtime-matrix-haproxy
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
CASE=phase1_header_block CRS=no-crs MRTS=no-mrts make verified-haproxy-case
CASE=phase1_header_block CRS=with-crs MRTS=no-mrts make verified-haproxy-case
```

HAProxy local build/self-test commands:

```sh
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
```

## Production / Production-Style Integration

A production-style HAProxy deployment needs HAProxy, a running `haproxy-modsecurity-spoa` process, libmodsecurity accessible to that process, SPOE config loaded by HAProxy, a SPOA agent config pointing at ModSecurity rules, and writable decision/audit/agent logs. End-to-end: HAProxy starts, the SPOE filter sends request metadata to the SPOP backend, the SPOA runtime calls libmodsecurity, the agent writes decision/audit evidence, and HAProxy allows, denies, redirects, or drops according to returned transaction variables. Response-header checks are a separate path; RESPONSE_BODY remains bounded runtime evidence only.

## Production / Production-Style Commands

Repository preparation/smoke commands:

```sh
make prepare-runtime-components
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
make smoke-haproxy
```

Operator install example with placeholders:

```sh
sudo install -d -m 0755 /etc/haproxy /etc/modsecurity /var/log/haproxy-modsecurity
sudo install -m 0755 <built-haproxy-modsecurity-spoa> /usr/local/sbin/haproxy-modsecurity-spoa
sudo install -m 0644 examples/haproxy/spoe-modsecurity.conf /etc/haproxy/spoe-modsecurity.conf
sudo install -m 0644 examples/haproxy/modsecurity-agent.conf /etc/haproxy/modsecurity-agent.conf
sudo install -m 0644 examples/haproxy/haproxy-request-only.cfg /etc/haproxy/haproxy.cfg
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
sudo systemctl reload haproxy
sudo systemctl restart haproxy-modsecurity-spoa
sudo tail -f /var/log/haproxy-modsecurity/decision.jsonl /var/log/haproxy-modsecurity/audit.log
```

No systemd unit is added by these docs; `haproxy-modsecurity-spoa` service management is operator-provided unless a deployment supplies one. `<built-haproxy-modsecurity-spoa>` must be replaced with the verified built binary path. RESPONSE_BODY remains bounded runtime evidence only.

Expected outputs / evidence:

- Summary JSON under `BUILD_ROOT` results.
- `decision.jsonl`.
- `audit.log`.
- `spoa-agent.log` or agent diagnostic log when configured.
- Generated HAProxy runtime report under `reports/testing/generated/`.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity, build/prepare HAProxy and `haproxy-modsecurity-spoa`, then run `make smoke-haproxy`. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/haproxy/README.md](examples/haproxy/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Runtime Evidence Paths

HAProxy summaries under `BUILD_ROOT/results/.../haproxy`, SPOA `decision.jsonl`, audit logs, harness logs, and generated reports under `reports/testing/generated/`.

## Logs

HAProxy logs, SPOA agent logs, `decision.jsonl`, and ModSecurity audit logs. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check SPOP backend reachability, SPOE config syntax, frame/body limits, libmodsecurity library paths, writable log directories, and request/response phase assumptions.

## Common Failures

SPOE backend unavailable, HAProxy config validation failure, agent cannot open rules/logs, or phase-4 expectations exceeding non-promoted evidence.

## Cleanup

The repository Makefile writes runtime/build state under `VERIFIED_RUN_ROOT` and related roots, not global install prefixes. Remove the chosen run root only after preserving logs and JSON summaries needed for evidence.

## Best Practices

- Keep build and runtime artifacts outside the git checkout.
- Pin source/runtime versions through existing framework variables; do not introduce undocumented versions in operator docs.
- Treat force-all FAIL rows as evidence of boundaries, not production support.
- Keep request-only operation as the conservative baseline unless generated evidence proves a more specific behavior.

## Related Docs / Examples

- [examples/haproxy/README.md](examples/haproxy/README.md)
- `connectors/haproxy/README.md`
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `reports/testing/generated/`
