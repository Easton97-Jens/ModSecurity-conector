# lighttpd Connector

Status: bridge-starter plus sidecar_proxy runtime-smoke path
Runtime status: locally verifiable with a staged lighttpd binary
Template alignment: bridge-starter, sidecar_proxy runtime-smoke only

This connector now contains a repository-owned decision-service bridge starter
for lighttpd. It is the smallest local next step after the metadata/probe
build-starter: it defines local request/decision data flow, compiles a CLI
self-test, and reuses connector-neutral `common/` status, origin, intervention,
and capability helpers.

The bridge starter is not a lighttpd module, not a FastCGI/SCGI implementation,
not a runtime harness, and not a libmodsecurity integration. It does not include
lighttpd headers, call lighttpd APIs, call ModSecurity APIs, process real
lighttpd traffic, load CRS, or write framework result JSON. Runtime evidence is
handled separately by the Phase 1 `sidecar_proxy` smoke.

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
- Harness: sidecar_proxy runtime-smoke entrypoint.
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

## Chosen Phase 1 Runtime Path

Native lighttpd module, FastCGI, and SCGI integration are deferred because this
repository does not currently contain selected lighttpd headers/SDK/source,
module build configuration, FastCGI/SCGI protocol adapter code, or a lighttpd
runtime module harness.

The chosen Phase 1 runtime path is `sidecar_proxy`. The smoke starts a local
lighttpd upstream and a local sidecar decision proxy. The sidecar allows a
normal request through to lighttpd and blocks `X-Modsec-Smoke: block` with HTTP
403 before the request reaches the upstream. This proves only the local
sidecar/proxy boundary; it is not native-module, FastCGI/SCGI, CRS, production,
or response-body verification.

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

## Parallel Runtime-Smoke Phase

Phase 1 uses `integration_mode=sidecar_proxy`. Native module, FastCGI/SCGI, and
mod_magnet/Lua remain deferred.

The lighttpd connector-specific surface is limited to:

- documenting the native module, FastCGI/SCGI, sidecar/proxy, and
  mod_magnet/Lua tradeoff;
- generated local lighttpd configuration for the sidecar_proxy smoke;
- lighttpd smoke harness entrypoint and common result evidence.

Shared request, response, intervention, status, logging, capabilities, origin,
and transaction concepts come from `common/include/msconnector/`. Runtime smoke
evidence is written through `common/scripts/write_smoke_result.py`, so lighttpd
does not maintain its own JSON result writer.

`make smoke-lighttpd` sources the framework common smoke wrapper, which sources
`modules/ModSecurity-test-Framework/ci/common.sh`. Runtime dependencies are not
installed globally and the harness does not assume `lighttpd` exists in the
global `PATH`.

Lighttpd binary lookup uses:

1. `LIGHTTPD_BIN`;
2. local common.sh-managed paths such as `$CONNECTOR_COMPONENT_CACHE`,
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
   `$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`;
3. Exit 77 with BLOCKED evidence if no local binary is found or the local
   sidecar smoke cannot complete.

Example:

```sh
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```

Local staging helper:

```sh
make prepare-lighttpd-runtime
```

The helper prepares `$CONNECTOR_COMPONENT_CACHE/lighttpd/bin` and reports
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd` when present. If the binary is
missing and `ALLOW_RUNTIME_DOWNLOADS=1` is not set, it exits 77 without
installing or downloading lighttpd. With explicit download opt-in, it downloads
the pinned lighttpd source tarball, verifies `LIGHTTPD_SHA256`, and stages source
under `$CONNECTOR_COMPONENT_CACHE/lighttpd/src/lighttpd-$LIGHTTPD_VERSION`.
With explicit build opt-in, it configures, builds, and installs only under
`$CONNECTOR_COMPONENT_CACHE/lighttpd`:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
```

The optional targeted backend is available through:

```sh
DECISION_BACKEND=libmodsecurity make smoke-lighttpd
make smoke-lighttpd-modsecurity
```

That mode may set `modsecurity_backend_verified=true` only when local
common.sh-managed libmodsecurity headers/libraries are available and rule
`1000001` returns a 403 intervention for `X-Modsec-Smoke: block`.
When it passes, the Lighttpd result records `decision_backend=libmodsecurity`,
`modsecurity_rule_loaded=true`, `modsecurity_rule_id=1000001`,
`allowed_request_status=200`, `blocked_request_status=403`, and
`modsecurity_backend_verified=true`.

The minimal CRS smoke keeps Lighttpd in Phase 1 `sidecar_proxy` mode and uses
the same local libmodsecurity backend with CRS selected:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-lighttpd
make smoke-lighttpd-crs
make smoke-lighttpd-crs-secondary
```

The CRS source-of-truth remains `common.sh` (`CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR`, and `CRS_RUNTIME_DIR`). The smoke writes a connector-local
CRS config under `$LIGHTTPD_RESULT_ROOT/crs-smoke`, sends a normal allowed
request and the existing minimal SQLi CRS probe
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`, and requires CRS-backed
HTTP 403 evidence. Successful CRS evidence may set only
`crs_minimal_smoke_verified=true`; it still keeps `crs_complete=false`,
`production_ready=false`, `full_matrix_ready=false`, and
`response_body_verified=false`. CRS evidence is also copied to
`$LIGHTTPD_RESULT_ROOT/crs-result.json` with logs in
`$LIGHTTPD_LOG_ROOT/crs-decision.log` and
`$LIGHTTPD_LOG_ROOT/crs-request-transcript.jsonl`.

The secondary CRS smoke reuses the same Phase 1 `sidecar_proxy` CRS resolver
and runtime path with `CRS_SMOKE_CASE=secondary`. It sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`, writes
`$LIGHTTPD_RESULT_ROOT/crs-secondary-result.json`, and records
`$LIGHTTPD_LOG_ROOT/crs-secondary-decision.log`,
`$LIGHTTPD_LOG_ROOT/crs-secondary-audit.log`, and
`$LIGHTTPD_LOG_ROOT/crs-secondary-request-transcript.jsonl`. A PASS may set
only `crs_secondary_smoke_verified=true` after extracting the actual CRS rule
ID/message from evidence. If CRS, libmodsecurity, and Lighttpd are present but
the secondary probe is not blocked, the result is FAIL, not PASS or BLOCKED.

All open connector CRS smokes can be run with:

```sh
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

This remains a sidecar/proxy proof. It is not a native lighttpd ModSecurity
module, not CRS-complete, not production-ready, and not response-body
verification.

lighttpd source metadata is centralized in `common.sh`: `LIGHTTPD_VERSION=1.4.84`,
the official 1.4.x release index, the latest URL used only for pinning,
the fixed tar.xz download URL, `LIGHTTPD_SHA256_URL`, and the pinned SHA256.
The machine-readable mirror is
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
Downloads and builds are not executed by default. When opted in, source, build,
binary, and logs stay under common.sh-managed runtime/component paths.

When no local binary is found, `missing_dependencies` includes `lighttpd`.
Evidence is written to `$VERIFIED_RUN_ROOT/lighttpd-smoke/`; if
`VERIFIED_RUN_ROOT` is not set, the fallback is
`$BUILD_ROOT/results/lighttpd-smoke/`.

Successful simple sidecar evidence may set `runtime_verified=true`,
`lighttpd_binary_verified=true`, `lighttpd_http_verified=true`, and
`sidecar_proxy_verified=true`. It still must not set production readiness, full
matrix readiness, CRS completeness, or response-body verification.
