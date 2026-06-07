# Compile Apache

## Purpose

This guide documents the repository-supported Apache build and runtime-smoke
path from a clean clone. It covers the local source-build flow used by
`make smoke-apache`, the variables consumed by the current scripts, and where
to find runtime evidence.

## Current Connector Status

- Connector: adapter-owned Apache module under `connectors/apache/`.
- Default runtime evidence: 54 attempted / 54 PASS.
- Force-all runtime evidence: 133 attempted / 100 PASS / 27 FAIL / 0 BLOCKED / 6 NOT_EXECUTABLE.
- Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is documented as runtime evidence only.

## What This Builds

- libmodsecurity v3 under `BUILD_ROOT`.
- A local Apache httpd/APXS toolchain when `BUILD_HTTPD_FROM_SOURCE=1`, or a module against an explicit `APXS` and `APACHE_HTTPD`.
- The repo-owned Apache connector module `mod_security3.so`.
- Per-case local Apache runtime directories and smoke evidence under `BUILD_ROOT`.

## What Not Prove

- It does not prove every distribution Apache package, MPM, module mix, or production configuration.
- It does not promote force-all FAIL rows or former expected-failure rows.
- It does not promote full RESPONSE_BODY support.
- Generated markdown is reporting only; runtime proof comes from smoke summary JSON and per-case logs.

## Repository Layout

| Path | Meaning |
|---|---|
| `connectors/apache/` | Apache connector source, build inputs, metadata, and harness |
| `connectors/apache/src/` | Productive Apache adapter source |
| `connectors/apache/harness/` | Runtime smoke config template and runner |
| `common/` | Connector-neutral metadata and helper shapes |
| `modules/ModSecurity-test-Framework/` | YAML cases, runners, generators, and smoke orchestration |
| `reports/testing/` | Parent-repository generated runtime reports |

## Prerequisites

- POSIX shell, `make`, C/C++ build tools, `git`, `curl`, `python3`.
- Python dependencies from `make setup-dev`.
- Network access only when fetching libmodsecurity, Apache, APR/APR-util, PCRE2, or CRS.
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
| `BUILD_HTTPD_FROM_SOURCE` | No | unset | `1` | Apache prepare helper | Build httpd/APXS locally | Recommended for reproducible local smoke |
| `APXS` | No | generated APXS when building httpd | `/usr/bin/apxs2` | Apache harness/prepare helper | External APXS path | Must match `APACHE_HTTPD` if supplied |
| `APACHE_HTTPD` | No | generated httpd when building httpd | `/usr/sbin/apache2` | Apache harness/prepare helper | External Apache executable | Alias `APACHE` is also accepted by the harness |
| `MODSECURITY_APACHE_SOURCE_DIR` | No | `$CONNECTOR_ROOT/connectors/apache` | `/src/ModSecurity-apache` | Apache prepare helper | Apache connector source input | Repo-local source is the default |
| `APACHE_BUILD_ROOT` | No | `$BUILD_ROOT/apache-build` | `/tmp/mscon-build/apache-build` | Apache harness | Apache build staging root | Generated |
| `LOG_DIR` | No | `$BUILD_ROOT/logs/apache-runtime` | `/tmp/mscon-build/logs/apache-runtime` | Apache harness | Per-run/per-case log root | Generated |
| `RESULTS_DIR` | No | `$BUILD_ROOT/results` | `/tmp/mscon-build/results` | Apache harness | Summary JSON/TXT output root | Force-all defaults to `$BUILD_ROOT/results/force-all` |
| `RUNTIME_BASE` | No | `$BUILD_ROOT/apache-runtime` | `/tmp/mscon-build/apache-runtime` | Apache harness | Per-case runtime root parent | Generated |
| `RUNTIME_ROOT` | No | `$RUNTIME_BASE/<case>` | `/tmp/mscon-build/apache-runtime/phase1_header_block` | Apache harness | One case runtime root | Used for selected-case runs |
| `PORT` | No | `18080` | `19080` | Apache harness | Local listener base port | Harness searches for a free port |
| `MODSECURITY_RULE_PREAMBLE_FILE` | No | unset | `$BUILD_ROOT/crs/modsecurity-crs-preamble.conf` | CRS variant smoke | Rules prepended before generated case rules | Required for `MODSECURITY_TEST_VARIANT=with-crs` |

Unsupported as current repository variables: `VERBOSE`, `DEBUG`, `APACHE_PORT`, `APACHE_LISTEN`, `APACHE_MODULE_PATH`, `APACHE_LOG_DIR`, `APACHE_RUN_USER`, and `APACHE_RUN_GROUP`. Use the supported variables above, or production Apache configuration files, instead.

## Minimal Local Build

```sh
git submodule update --init --recursive
make setup-dev
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

## Rebuild / Refresh

```sh
REFRESH=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

Use a separate build root for independent reproductions:

```sh
BUILD_ROOT=/tmp/mscon-apache-build SOURCE_ROOT=/src REFRESH=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

## Manual Build Flow

The helper flow is the source of truth. A manual reproduction follows the same shape:

```sh
make fetch-deps
BUILD_HTTPD_FROM_SOURCE=1 sh modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh
APXS=/path/to/apxs APACHE_HTTPD=/path/to/httpd make smoke-apache
```

## Production-Style Install / Deploy

- Install the built `mod_security3.so` into the distribution module directory.
- Load it from `/etc/apache2/mods-available/` or the equivalent httpd config path.
- Keep ModSecurity config in `/etc/modsecurity/`.
- Keep CRS in `/etc/modsecurity/crs/`.
- Write audit and connector logs under `/var/log/modsecurity/` and server logs under `/var/log/apache2/` or `/var/log/httpd/`.
- Reload/restart Apache after changing loaded modules, ModSecurity config, CRS, or connector directives.

## Test / Smoke Validation

```sh
make quick-check
make smoke-apache
FORCE_ALL_CASES=1 make smoke-apache
make generate-test-matrix
make check-test-matrix
```

Expected current default evidence is 54 attempted / 54 PASS. Current force-all evidence contains expected FAIL and NOT_EXECUTABLE rows and is not a support promotion.

## Runtime Evidence Paths

| Evidence | Path |
|---|---|
| Default summary | `$BUILD_ROOT/results/apache-summary.json` |
| Default JSONL | `$BUILD_ROOT/results/apache-results.jsonl` |
| Force-all summary | `$BUILD_ROOT/results/force-all/apache-summary.json` |
| Per-case logs | `$BUILD_ROOT/logs/apache-runtime/<case>/` |
| Generated report | `reports/testing/generated/apache-runtime-results.generated.md` |

## Generated Artifacts

- `$BUILD_ROOT/apache-build/`
- `$BUILD_ROOT/apache-runtime/`
- `$BUILD_ROOT/results/apache-summary.json`
- `$BUILD_ROOT/logs/apache-runtime/`

## Logs

Per-case logs include Apache access/error logs, generated config, curl errors, `phase4.log`, `response-body.txt`, `audit.log`, and normalized `result.json`.

## Troubleshooting

- Missing framework: run `git submodule update --init --recursive` or set `FRAMEWORK_ROOT`.
- APXS/httpd mismatch: supply matching `APXS` and `APACHE_HTTPD`, or use `BUILD_HTTPD_FROM_SOURCE=1`.
- CRS run blocked: run `make prepare-crs` or use `make test-with-crs`.
- Port conflict: set `PORT` to another base port.

## Common Failures

- Build dependency missing: install compiler, APR/APR-util, PCRE2, and libtool/autotools prerequisites or let the helper build them.
- Generated path rejected: use absolute `BUILD_ROOT`, `LOG_DIR`, and `RUNTIME_ROOT` outside the checkout.
- Response-body mismatch: treat as bounded evidence only; do not promote RESPONSE_BODY.

## Cleanup

```sh
rm -rf /src/ModSecurity-conector-build/apache-build
rm -rf /src/ModSecurity-conector-build/apache-runtime
rm -rf /src/ModSecurity-conector-build/logs/apache-runtime
```

## Best Practices

- Prefer clean `BUILD_ROOT` values for evidence runs.
- Record exact commands and summary JSON paths in review notes.
- Keep generated runtime artifacts out of git.
- Stage generated markdown only after `make generate-test-matrix`.

## Related Docs / Examples

- `examples/apache/README.md`
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
