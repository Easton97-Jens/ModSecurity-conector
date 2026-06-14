# lighttpd Connector

Status: bridge-starter
Runtime status: not-verified
Template alignment: bridge-starter, not runtime-verified

This connector now contains a repository-owned decision-service bridge starter
for lighttpd. It is the smallest local next step after the metadata/probe
build-starter: it defines local request/decision data flow, compiles a CLI
self-test, and reuses connector-neutral `common/` status, origin, intervention,
and capability helpers.

The bridge starter is not a lighttpd module, not a FastCGI/SCGI implementation,
not a runtime harness, and not a libmodsecurity integration. It does not include
lighttpd headers, call lighttpd APIs, call ModSecurity APIs, process real
lighttpd traffic, load CRS, or write framework result JSON.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

The shared rules, gates, status vocabulary, No-CRS/With-CRS separation,
coverage matrix requirements, runtime evidence requirements, and RESPONSE_BODY
minimum evidence are defined globally and are not duplicated here.

## lighttpd-specific State

- Origin/license: documented for current repo-owned bridge starter; no upstream
  lighttpd source imported.
- Metadata: `metadata.c` / `metadata.h` present for bridge-starter status.
- Metadata/probe build: `build/build_starter.sh` compile-checkable.
- Bridge starter: local decision-service starter with CLI self-test.
- Native lighttpd module: not implemented.
- FastCGI/SCGI bridge: not implemented.
- Harness: contract only.
- No-CRS runtime: not run.
- With-CRS runtime: not run.
- RESPONSE_BODY blocking: not verified.

## Build and Self-Test Starters

Local starter commands:

```sh
make -C connectors/lighttpd build-starter
make -C connectors/lighttpd self-test
make -C connectors/lighttpd build-bridge-starter
make -C connectors/lighttpd self-test-bridge
```

The bridge starter sources are:

- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`

A PASS from these commands proves only local compile/self-test behavior for the
repo-owned starter. It is not a lighttpd module build and is not runtime
validation.

## Chosen Minimal Next Step

Native lighttpd module, FastCGI, and SCGI integration are deferred because this
repository does not currently contain selected lighttpd headers/SDK/source,
module build configuration, FastCGI/SCGI protocol adapter code, or a lighttpd
runtime harness.

The chosen next step is a local decision-service bridge starter. It is a future
bridge integration point only. It intentionally evaluates a local probe request
as `blocked` because no real lighttpd runtime hook, FastCGI/SCGI protocol
adapter, or libmodsecurity integration exists yet.

## Tests

No local `connectors/lighttpd/tests` folder is used. Executable tests are
framework-owned.

Framework-owned paths and targets to use when a real lighttpd build and harness
exist:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No lighttpd runtime result is claimed by this bridge starter. No-CRS and
With-CRS must be validated separately before promotion, and RESPONSE_BODY
blocking remains not verified.
