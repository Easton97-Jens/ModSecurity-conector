# Compile HAProxy Connector

This document describes the repository-supported local HAProxy build and
runtime-smoke path. It follows the same root-documentation pattern as
`COMPILE_APACHE.md` and `COMPILE_NGINX.md`: connector source is repo-local,
the framework owns reusable runtime machinery, and build/runtime evidence is
local evidence only.

The current HAProxy path is a diagnostic SPOA/SPOP runtime plus a local
libmodsecurity binding. It is not a productive full HAProxy adapter and it is
not full-matrix verified.

## Status

- HAProxy local build: available.
- HAProxy runtime smoke: partial.
- Verified cases:
  - `haproxy_phase1_header_block`
  - `haproxy_crs_sqli_anomaly_block`
- CRS verified: scoped only to `haproxy_crs_sqli_anomaly_block`.
- RESPONSE_BODY: not verified.
- Full matrix: partial / not fully verified.

## Source of Truth

- Versions, URLs, tags, and checksums:
  `modules/ModSecurity-test-Framework/ci/common.sh`
- Coverage summary:
  `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Do not duplicate HAProxy source pins, release tags, URLs, or checksums in this
document or in connector-local docs. Update `common.sh` first when a source pin
needs to change.

## Local Build Roots

- `SOURCE_ROOT=/src`
- `BUILD_ROOT=/src/ModSecurity-conector-build`
- Results:
  `$BUILD_ROOT/results`
- Logs:
  `$BUILD_ROOT/logs`
- Temp/runtime:
  `$BUILD_ROOT/tmp`

Sources stay under `/src`. All builds, logs, runtime files, PIDs, sockets, and
results stay under `/src/ModSecurity-conector-build`. No generated build or
runtime artifacts should be written into `connectors/haproxy`.

## No Global Install

The repository-supported HAProxy path is local-only:

- no `sudo`
- no system `make install`
- no writes to `/usr`
- no writes to `/usr/local`
- no writes to `/etc`
- no writes to `/opt`

## Build Steps

Build and self-test the minimal diagnostic SPOP runtime:

```bash
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
```

Build and self-test the local libmodsecurity binding:

```bash
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

These commands prove only the local diagnostic components. They do not claim a
complete SPOA service, a native HAProxy module/filter, broader CRS behavior,
RESPONSE_BODY handling, or full framework matrix support.

## Runtime Smoke

Run the current narrow live HAProxy smoke:

```bash
make smoke-haproxy
```

Expected current status:

- No-CRS block probe: `403`
- No-CRS pass probe: `200`
- With-CRS block probe: `403`
- With-CRS pass probe: `200`

The No-CRS smoke verifies the diagnostic alias
`haproxy_phase1_header_block`. The With-CRS smoke verifies
`haproxy_crs_sqli_anomaly_block`, which maps to the existing framework YAML
case `crs_sqli_anomaly_block`.

## Runtime Matrix

Run the HAProxy matrix targets:

```bash
make runtime-matrix-haproxy
make test-haproxy-no-crs
make test-haproxy-with-crs
```

Status meanings:

- `PASS` only means live HAProxy execution.
- `FAIL` only means live HAProxy execution with the wrong result.
- `BLOCKED` means relevant, but the current HAProxy harness cannot execute it.
- `NOT_EXECUTABLE` means outside the current HAProxy scope.
- `MAPPED_ONLY` is import inventory, not runtime execution.
- RESPONSE_BODY is not verified.

Current combined HAProxy matrix evidence records 1 PASS, 0 FAIL, 59 BLOCKED,
81 NOT_EXECUTABLE, and 10 MAPPED_ONLY rows. The only YAML PASS is
`crs_sqli_anomaly_block`; the No-CRS header smoke remains an alias and is not
promoted to the framework `phase1_header_block` YAML row.

## Matrix Row Count Notes

HAProxy `141` means matrix rows enumerated / YAML rows considered. It does not
mean 141 live executed PASS/FAIL attempts. The HAProxy writer enumerates all
current framework YAML rows and then classifies unsupported rows as `BLOCKED`
or `NOT_EXECUTABLE`.

Apache `133` comes from the latest Apache runtime snapshot attempted count.
These numbers are only comparable when the report distinguishes:

- enumerated rows
- live attempted rows
- live executed rows
- blocked rows
- not executable rows

For HAProxy today, the combined matrix enumerates 141 YAML rows, live-executes
only the current narrow With-CRS YAML case, and records the rest as PASS,
BLOCKED, or NOT_EXECUTABLE according to the evidence rules above.

## Evidence Paths

- `/src/ModSecurity-conector-build/results/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/haproxy-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

## Current Open Areas

- broader HAProxy runtime harness
- broader No-CRS YAML execution
- broader With-CRS YAML execution
- request body
- multipart
- JSON
- XML
- response headers
- response body
- audit/log evidence
- RESPONSE_BODY blocking
- Full Matrix
- promotion beyond partial

## Commands For Local Verification

```bash
test ! -d connectors/haproxy/tests
make smoke-haproxy
make runtime-matrix-haproxy || true
make test-haproxy-no-crs || true
make test-haproxy-with-crs || true
make generate-test-matrix
make check-test-matrix
make lint
make quick-check
git diff --check
```
