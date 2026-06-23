# Compile Apache

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

Document the repository-supported build or prepare path for Apache without adding unverified production claims. This guide is operator-facing and ties build, runtime, and smoke statements to repository-owned Makefile targets, connector sources, harnesses, examples, or generated evidence.

## Current Connector Status

Adapter-owned Apache module under `connectors/apache/`; request phases are the production-style baseline. Default generated evidence currently reports 54/54 PASS, while force-all evidence still contains FAIL and NOT_EXECUTABLE rows and must not be promoted.

## What This Builds / Prepares

libmodsecurity v3, an Apache/APXS toolchain when `BUILD_HTTPD_FROM_SOURCE=1` or a module against explicit matching `APXS`/`APACHE_HTTPD`, and `mod_security3.so` from `connectors/apache/`.

## What This Does Not Prove

It does not prove every distribution Apache package, MPM combination, module mix, CRS deployment, or complete RESPONSE_BODY support. Generated markdown and smoke logs are evidence artifacts, not blanket support guarantees.

## Repository Layout

`connectors/apache/src/` (module source), `connectors/apache/harness/` (smoke harness), `connectors/apache/docs/`, `examples/apache/`, `common/`, `ci/`, and `reports/testing/generated/`.

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

`BUILD_HTTPD_FROM_SOURCE`, `APXS`, `APACHE_HTTPD`, `MODSECURITY_APACHE_SOURCE_DIR`, `MODSECURITY_V3_SOURCE_DIR`, `MODSECURITY_V3_ROOT`, `BUILD_ROOT`, `SOURCE_ROOT`, `LOG_ROOT`, `RESULTS_DIR`, `MODSECURITY_TEST_VARIANT`, and `MODSECURITY_MRTS_VARIANT` are present in the Makefile or preparation scripts. Do not invent additional variables; check `Makefile`, `ci/prepare-runtime-components.py`, connector Makefiles, and harness scripts before documenting new ones.

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

Apache-specific commands:

```sh
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
FORCE_ALL_CASES=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
CASE=phase1_header_block CRS=no-crs MRTS=no-mrts BUILD_HTTPD_FROM_SOURCE=1 make verified-apache-case
CASE=phase1_header_block CRS=with-crs MRTS=no-mrts BUILD_HTTPD_FROM_SOURCE=1 make verified-apache-case
```

## Production / Production-Style Integration

A production-style Apache deployment needs libmodsecurity v3 libraries, a `mod_security3.so` built for the exact Apache/APXS ABI, Apache config that loads the module, a ModSecurity rules file under an operator-chosen config directory such as `/etc/modsecurity`, optional CRS includes, and writable audit/error log locations. APXS and the Apache binary must come from the same Apache build or package family; this repository does not prove arbitrary distro/APXS/MPM combinations.

## Production / Production-Style Commands

Repository preparation/smoke commands:

```sh
make prepare-runtime-components
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

Operator install example with placeholders:

```sh
sudo install -d -m 0755 /etc/modsecurity /var/log/modsecurity
sudo install -m 0755 <built-mod_security3.so> /usr/lib/apache2/modules/mod_security3.so
sudo install -m 0644 examples/apache/modsecurity-request-only.conf /etc/modsecurity/modsecurity-request-only.conf
sudo install -m 0644 examples/apache/apache-modsecurity-request-only.conf /etc/apache2/mods-available/security3.conf
sudo apachectl configtest
sudo apachectl graceful
sudo tail -f /var/log/apache2/error.log /var/log/modsecurity/apache-audit.log
```

`<built-mod_security3.so>` must be replaced by the actual module built for the exact Apache/APXS ABI. The repository does not prove every distro package, MPM, or module layout. Use distro-specific paths when they differ.

Expected outputs / evidence:

- Summary JSON under `BUILD_ROOT` results.
- Apache access/error logs.
- ModSecurity audit log when enabled.
- Generated Apache report path under `reports/testing/generated/`.

## End-to-End Flow: Fetch Components → Build ModSecurity → Build/Prepare Connector → Run Integrated Smoke

Fetch components with `make prepare-runtime-components`, build/prepare libmodsecurity through that target, build the Apache module with the prepared APXS flow, and run `BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache` for integrated evidence. If a dependency is unavailable, document the result as blocked or not verified instead of treating it as a pass.

## Example Configs

See [examples/apache/README.md](examples/apache/README.md). Example configs are production-style illustrations. They must be reviewed and adapted before use; open connector examples are explicitly not production-ready proof.

## Runtime Evidence Paths

`BUILD_ROOT/results/.../apache`, `LOG_ROOT`, Apache runtime logs, audit logs, and generated report files under `reports/testing/generated/`.

## Logs

Apache access/error logs from the harness runtime plus ModSecurity audit logs when enabled. Preserve logs together with the exact command, connector, CRS variant, and MRTS variant.

## Troubleshooting

Check missing submodule, APXS/httpd mismatch, unwritable runtime roots, missing libmodsecurity headers/libraries, CRS include paths, and response-body tests that are intentionally non-promoted.

## Common Failures

Missing framework returns a blocked preflight; APXS from one Apache and httpd from another can produce an unusable module; force-all rows may fail without changing production support status.

## Cleanup

The repository Makefile writes runtime/build state under `VERIFIED_RUN_ROOT` and related roots, not global install prefixes. Remove the chosen run root only after preserving logs and JSON summaries needed for evidence.

## Best Practices

- Keep build and runtime artifacts outside the git checkout.
- Pin source/runtime versions through existing framework variables; do not introduce undocumented versions in operator docs.
- Treat force-all FAIL rows as evidence of boundaries, not production support.
- Keep request-only operation as the conservative baseline unless generated evidence proves a more specific behavior.

## Related Docs / Examples

- [examples/apache/README.md](examples/apache/README.md)
- `connectors/apache/README.md`
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
- `reports/testing/generated/`
