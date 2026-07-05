# Traefik Connector

Status: decision-service-starter with conditional local runtime smoke
Runtime status: verified only when a local common.sh-managed Traefik binary runs the HTTP smoke
Template alignment: scaffold-aligned with local decision-service starter

This connector now contains a repo-owned local decision-service starter in
addition to the compile-time metadata starter. It still does not contain a
production Traefik adapter implementation. When a local Traefik binary is
provided through `TRAEFIK_BIN` or common.sh-managed caches, the runtime-smoke
harness starts a minimal upstream, a minimal forwardAuth decision service, and
Traefik with a generated local config to prove an allowed request and a blocked
HTTP 403 path.

The starter compiles only repository-owned C code and shared common helpers:

- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.*`
- shared helpers from `common/src/` and `common/include/msconnector/`

It does not include a Traefik API, Traefik plugin SDK, Go module,
libmodsecurity runtime integration, Traefik traffic handling, CRS execution,
RESPONSE_BODY handling, or a Traefik runtime harness.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Traefik-specific State

- Origin/license: documented for repo-owned starter; upstream Traefik source not selected
- Metadata: repo-owned compile-time metadata present
- Build: metadata and decision-service starter commands present
- Self-test: local decision-service starter self-test present
- Harness: conditional local Traefik forwardAuth smoke when a local binary is available
- No-CRS runtime: not run
- With-CRS runtime: not run
- RESPONSE_BODY blocking: not verified

## Build and Self-Test

Run the metadata build starter with:

```sh
connectors/traefik/build/build-starter.sh
```

Run the local decision-service starter self-test with:

```sh
make -C connectors/traefik self-test-decision-service
```

A successful self-test proves only local allow/block decision logic for in-memory
request structs. It is not a Traefik runtime, `forwardAuth`, CRS, or
libmodsecurity validation.

## Tests

No local `connectors/traefik/tests` folder is used. Executable tests are
framework-owned.

Framework-owned paths and targets to use after a real Traefik build and harness
are implemented:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, audit/log, or Traefik
runtime result is claimed for Traefik by this starter.

## Parallel Runtime-Smoke Phase

Phase 1 targets Traefik `forwardAuth`. A Go plugin is explicitly out of scope
for this phase.

The Traefik connector-specific surface is limited to:

- forwardAuth integration design and future Traefik configuration;
- Traefik smoke harness entrypoint;
- local decision-service starter code.

Shared request, response, intervention, status, logging, capabilities, origin,
and transaction concepts come from `common/include/msconnector/`. Runtime smoke
evidence is written through `common/scripts/write_smoke_result.py`, so Traefik
does not maintain its own JSON result writer.

`make smoke-traefik` sources the framework common smoke wrapper, which sources
`modules/ModSecurity-test-Framework/ci/common.sh`. Runtime dependencies are not
installed globally and the harness does not assume `traefik` exists in the
global `PATH`.

Traefik binary lookup uses:

1. `TRAEFIK_BIN`;
2. local common.sh-managed paths such as `$CONNECTOR_COMPONENT_CACHE`,
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
   `$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`;
3. Exit 77 with BLOCKED evidence if no local binary is found.

Example:

```sh
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
```

Local staging helper:

```sh
make prepare-traefik-runtime
```

The helper prepares `$CONNECTOR_COMPONENT_CACHE/traefik/bin` and reports
`$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik` when present. If the binary is
missing and `ALLOW_RUNTIME_DOWNLOADS=1` is not set, it exits 77 without
installing or downloading Traefik. With explicit opt-in, it downloads the
pinned Linux amd64 tarball, verifies `TRAEFIK_SHA256`, extracts only the
`traefik` binary, and stages it locally:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
make smoke-traefik
```

The default smoke proves the local Traefik runtime, generated forwardAuth
config, upstream, and simple decision-service 200/403 behavior. It is not a
libmodsecurity compatibility claim.

For the optional targeted libmodsecurity-backed smoke, keep the same local
Traefik binary and select the libmodsecurity decision backend:

```sh
DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-modsecurity
```

This mode resolves local libmodsecurity headers/libraries from common.sh-managed
component caches or explicit local `MODSECURITY_INCLUDE_DIR` /
`MODSECURITY_LIB_DIR` overrides, loads
`common/rules/modsecurity_targeted_smoke.conf`, and blocks
`X-Modsec-Smoke: block` with rule `1000001`. Missing local libmodsecurity
dependencies produce Exit 77/BLOCKED evidence with
`decision_backend=libmodsecurity` and `modsecurity_backend_verified=false`.

The minimal CRS smoke uses the same local Traefik runtime and libmodsecurity
backend, but switches the ruleset to CRS:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
make smoke-traefik-crs
make smoke-traefik-crs-secondary
```

The CRS source-of-truth remains `common.sh` (`CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR`, and `CRS_RUNTIME_DIR`). The smoke writes a connector-local
CRS config under `$TRAEFIK_RESULT_ROOT/crs-smoke`, sends a normal allowed
request and the existing minimal SQLi CRS probe
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`, and requires CRS-backed
HTTP 403 evidence. Successful CRS evidence may set only
`crs_minimal_smoke_verified=true`; it still keeps `crs_complete=false`,
`production_ready=false`, `full_matrix_ready=false`, and
`response_body_verified=false`. CRS evidence is also copied to
`$TRAEFIK_RESULT_ROOT/crs-result.json` with logs in
`$TRAEFIK_LOG_ROOT/crs-decision.log`.

The secondary CRS smoke reuses that same CRS resolver and runtime path with
`CRS_SMOKE_CASE=secondary`. It sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`, writes
`$TRAEFIK_RESULT_ROOT/crs-secondary-result.json`, and records
`$TRAEFIK_LOG_ROOT/crs-secondary-decision.log` plus
`$TRAEFIK_LOG_ROOT/crs-secondary-audit.log`. A PASS may set only
`crs_secondary_smoke_verified=true` after extracting the actual CRS rule
ID/message from evidence. If CRS, libmodsecurity, and Traefik are present but
the secondary probe is not blocked, the result is FAIL, not PASS or BLOCKED.

All open connector CRS smokes can be run with:

```sh
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

Traefik source metadata is centralized in `common.sh`: `TRAEFIK_VERSION=3.7.5`,
the official GitHub release URL, the install docs URL, the Linux amd64
download URL, `TRAEFIK_SHA256_URL`, and the pinned SHA256. The
machine-readable mirror is
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
Downloads are not executed by default and, when opted in, stage only under
`$CONNECTOR_COMPONENT_CACHE/traefik`.

Current missing-binary evidence uses
`skipped_reason="traefik runtime dependency not available in local common.sh-managed paths"`
and `missing_dependencies=["traefik"]`. Evidence is written to
`$VERIFIED_RUN_ROOT/traefik-smoke/`; if `VERIFIED_RUN_ROOT` is not set, the
fallback is `$BUILD_ROOT/results/traefik-smoke/`.

If a local binary is resolved, `make smoke-traefik` can return PASS only after a
real HTTP smoke observes an allowed request status of 200 and a blocked request
status of 403 through Traefik. That PASS still does not claim production
readiness, full matrix readiness, CRS completeness, or response-body
verification. `modsecurity_backend_verified=true` is claimed only by the
targeted libmodsecurity smoke when the decision log shows libmodsecurity loaded
the targeted rule and returned the 403 intervention.

## Common SDK adoption status

This connector is prepared for the Common SDK but remains `not_verified` / `connector-gap`.

- Common configuration is initialized through `traefik_modsecurity_config_init()` and maps to `msconnector_config`.
- Request and response mapper contracts use the Common generic mapper helper and live in `connectors/traefik/src/traefik_modsecurity_mapper.*` and are structure/compile-level only until host runtime callsites exist.
- Decisions use Common decision/intervention models; event, test-result, and artifact emission remain connector-gap until runtime integration exists.
- Connector-specific code remains responsible for host API glue, runtime lifecycle, build glue, and protocol/frame handling.
- No production, CRS, full-matrix, runtime, or RESPONSE_BODY verification is claimed.
