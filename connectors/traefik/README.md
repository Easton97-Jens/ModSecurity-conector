# Traefik Connector

**Language:** English | [Deutsch](README.de.md)

Status: forwardAuth compatibility smoke plus a non-promoted native local-plugin host probe
Runtime status: targeted local Traefik/Common-runtime allow 200/block 403
Verification status: not_verified / connector-gap

The selected connector architecture is an external HTTP `forwardAuth` service.
`src/traefik_forwardauth_service_main.c` registers a Traefik host profile with
the connector-neutral Common runtime, while `traefik_modsecurity_mapper.c`
provides real thin mapper functions. It remains the selected path and does not
establish production readiness.

The repository build surfaces compile only repository-owned C code and shared
Common helpers:

- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.*`
- `connectors/traefik/src/traefik_modsecurity_mapper.*`
- `connectors/traefik/src/traefik_forwardauth_service_main.c`
- `connectors/traefik/native_middleware/` (native local-plugin host source)
- shared helpers from `common/src/` and `common/include/msconnector/`
- shared runtime implementation from `common/runtime/`

The `forwardAuth` path remains the request-only compatibility path. The
repository-owned Go middleware under `native_middleware/` is selected by the
full-lifecycle runner through Traefik's local-plugin workspace, but it still
uses `PassthroughEngine`. That real host probe proves plugin loading and router
traffic only; it does not change rule-evaluation, response-intervention, or
verification state. Upstream response headers and bodies remain unsupported in
the `forwardAuth` compatibility protocol.

## Native Go streaming host probe (non-promoted)

`native_middleware/` implements Traefik-shaped `CreateConfig`, `New`, and
`ServeHTTP` entry points using the Go `net/http` interfaces. Its response
writer preserves `Flush`, `Hijack`, `Push`, `ReadFrom`, and `Unwrap`; it sends
bounded request and response body slices to an explicit engine seam and never
collects a whole response. The checked-in engine is deliberately pass-through,
not Common/libmodsecurity.

Run only the local source checks with:

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

These commands compile and unit-test repository source. The separate host
probe stages that source below a disposable `plugins-local` workspace, starts
the pinned Traefik binary, requires the plugin load confirmation, and sends a
body-bearing request through a router selecting the middleware:

```sh
TRAEFIK_BIN=/absolute/local/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absolute/runtime-root \
make -C connectors/traefik runtime-smoke-traefik-native
```

It records only status and byte/chunk counters. It does not call Common or
libmodsecurity, does not evaluate rules, and cannot promote P1–P4, safe,
strict, first-byte, or no-full-buffer capabilities. The C `forwardAuth`
commands remain the selected compatibility path.

## Connector Service Build

The real service build is compile/link-only and requires explicit local
libmodsecurity paths:

```sh
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik build-connector
```

Build, configuration validation, and process startup are separate operations:

```sh
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

`check-config` invokes `--check-config`; `start-smoke` invokes `--serve`, starts
a real local Traefik process with a temporary forwardAuth File Provider config,
proves that both processes remain alive, and stops them without sending a
request. Neither target silently rebuilds the service.

`runtime-smoke` is the separate traffic proof. It starts the built service, a
minimal upstream, and a local Traefik binary with a temporary File Provider
configuration. It requires an allowed request to return 200 and
`X-Modsec-Smoke: block` to return 403 through the Common runtime. Missing local
binaries return Exit 77; config, startup, mapping, or status errors return FAIL.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Traefik-specific State

- Origin/license: documented for repo-owned starter; upstream Traefik source not selected
- Metadata: repo-owned compile-time metadata present
- Build: C17 Common-runtime service plus legacy starter commands present
- Self-test: local decision-service starter self-test present
- Harness: conditional local Traefik forwardAuth smoke when a local binary is available
- Targeted No-CRS runtime: pass-local; full No-CRS matrix not run
- With-CRS runtime: not run
- RESPONSE_BODY blocking: `unsupported_by_host_model` for the selected
  `forwardAuth` integration

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

Phase 1 compatibility targets Traefik `forwardAuth`. The native Go middleware
has a separate pinned-host probe, but its passthrough engine has no runtime
promotion.

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
- Request and response mapper contracts use thin C17 functions in `connectors/traefik/src/traefik_modsecurity_mapper.*`; dead macro aliases are not used.
- The service host profile selects `integration_mode=forwardAuth`, prefers `X-Forwarded-Uri` then `X-Original-Uri`, and passes the mapper callbacks to the neutral HTTP authorization service.
- Runtime decisions use Common decision/intervention models; the targeted smoke verifies a Common blocked-event JSONL record without body payload fields.
- Connector-specific code remains responsible for the host profile, build glue, example configuration, and process entry point.
- Response mapping is linked for contract checking only; upstream response inspection is unsupported by `forwardAuth`.
- No production, CRS-complete, full-matrix, broad runtime, or RESPONSE_BODY verification is claimed.

## Canonical Phase-4 boundary

The selected host model is Traefik `forwardAuth`.  It executes before upstream
handling and cannot inspect the later upstream response body.  Consequently,
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are
`unsupported_by_host_model`, not merely absent from a local run.

The shared Phase-4 cases must therefore be `UNSUPPORTED` with the explicit
forwardAuth architecture reason.  A request-side 200 or 403 proves only the
pre-upstream authorization path; it neither proves response-body inspection
nor supplies original upstream status, post-commit visible status, or a late
action.  `UNSUPPORTED` is never a `PASS` and must not be changed to
`NOT_EXECUTED` merely because no response test was run.

No response-body payload belongs in an event or report.  A future Traefik
integration that observes upstream responses would be a different host model
and needs independent evidence.
