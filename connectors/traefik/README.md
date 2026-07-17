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
repository-owned Go middleware under `native_middleware/` is selected by
`full-lifecycle-traefik-native` through Traefik's local-plugin workspace. Its
isolated host probe chooses `engineMode: uds`, so one persistent local
Common/libmodsecurity service is reused across one UDS session per host
request. It has targeted real-host P1--P4 evidence but does not change the
checked-in capability declaration, CRS state, Safe/Strict status, or production
readiness. Upstream response headers and bodies remain unsupported in the
separate `forwardAuth` compatibility protocol.

## Persistent native UDS engine service

`src/traefik_engine_service.c` and
`src/traefik_engine_protocol.h` add a persistent local Unix-domain-socket
Common/libmodsecurity service for the Yaegi-compatible Go bridge. It has
bounded metadata/chunk frames and explicit transaction EOS, finish, and destroy
operations. The native host probe supplies its private socket and run-local
event path; it records a host outcome only after the actual ResponseWriter
action succeeds. After response commitment, a P4 disruptive decision is
accepted only as `LOG_ONLY` with the actual visible status.

```sh
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik test-engine-service
```

The focused test starts only the local engine service and is not a Traefik
host-runtime test. See the [canonical Traefik guide](../../docs/connectors/traefik.md)
for lifecycle, configuration, canonical-rule selection, and outcome boundaries.
For a sandboxed local test only, `TRAEFIK_ENGINE_SOCKET_TEST_PARENT` can select
an existing current-user-owned `0700` parent instead of the generated
`/var/tmp` allocation root; it does not change the host-probe configuration.

## Native Go streaming host probe (non-promoted)

`native_middleware/` implements Traefik-shaped `CreateConfig`, `New`, and
`ServeHTTP` entry points using the Go `net/http` interfaces. Its response
writer preserves `Flush`, `Hijack`, `Push`, `ReadFrom`, and `Unwrap`; it sends
bounded request and response body slices to an explicit engine seam and never
collects a whole response. The source default is deliberately pass-through;
the isolated host probe selects the separately built persistent UDS
Common/libmodsecurity engine.

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
TRAEFIK_ENGINE_SOCKET_PARENT=/absolute/private/short-socket-parent \
MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
MSCONNECTOR_RULES_FILE=/absolute/no-crs-baseline.conf \
make -C connectors/traefik runtime-smoke-traefik-native
```

`TRAEFIK_ENGINE_SOCKET_PARENT` is the optional private parent for the native
probe's short-lived engine UDS child. The runner chooses this explicit value
first, then `TMPDIR`; when neither is set it creates a short, current-user
owned, `0700`-private fallback parent below `/var/tmp`. An explicit value or
`TMPDIR` must be an existing absolute, `0700`-private directory outside the
checkout with no symlink component; the broad roots `/`, `/tmp`, `/var`, and
`/var/tmp` are rejected as configured parents. Control characters are rejected
before path handling, and the generated YAML serializes the socket path as a
quoted scalar. The runner creates one unique private child below the selected
parent, enforces the 100-byte socket-path limit before and after allocation,
and removes that child after its host processes stop only if it is unchanged
and empty. Before reporting readiness on Linux, the engine makes a local
self-probe through the configured pathname and requires the accepted peer's
`SO_PEERCRED` PID and UID to identify the engine process. A replacement after
`bind` during that bounded pre-readiness capture sequence therefore fails
startup instead of being captured as service-owned. This capture does not bind
later middleware dials to the captured listener: a hostile process sharing the
UID can still replace the live pathname after readiness, so this path is not a
same-UID endpoint-integrity boundary. The engine checks the captured socket
identity at cleanup and reports an observed replacement as incomplete cleanup
instead of removing it. A private `0700` directory is a cross-UID boundary, not
isolation from a hostile process with the same UID: POSIX has no atomic
unlink-if-this-inode operation, and the runner's directory identity/emptiness
checks before `rmdir()` are likewise non-atomic. The native pathname listener
fails closed on a platform without the required Linux peer-credential
primitive. The runner never removes a caller-selected parent or accepts a
caller-selected socket pathname; it removes generated allocation directories
only after the documented checks, not under a same-UID race-proof guarantee.

The host probe records metadata only, never bodies. With the canonical rules
file it requires P1 allow `200`, P1 deny `403` (rule `1100001`), P2 deny `403`
(`1100101`), P3 pre-commit deny `403` (`1100201`), and P4 safe/log-only with
visible `200` (`1100301`). P4 strict is `NOT EXECUTED`. The host-confirmed
JSONL records use integration mode `native-traefik-middleware` and canonical
`transport_result` values `http_status` or `log_only`. This evidence does not
promote P1–P4, Safe/Strict, first-byte, no-full-buffer, CRS, or production
capabilities. The C `forwardAuth` commands remain the selected compatibility
path. The exact native transport/API boundary, including the non-promoting
keep-alive observation and Strict `NOT EXECUTED` rationale, is in the
[canonical Traefik guide](../../docs/connectors/traefik.md).

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

See the canonical [connector contract](../../docs/connectors/README.md) and
[testing/evidence guide](../../docs/testing-and-evidence.md).

## Traefik-specific State

- Origin/license: documented for repo-owned starter; upstream Traefik source not selected
- Metadata: repo-owned compile-time metadata present
- Build: C17 Common-runtime service plus legacy starter commands present
- Self-test: local decision-service starter self-test present
- Harness: conditional local Traefik forwardAuth smoke plus an isolated native
  UDS host probe when local Traefik and libmodsecurity inputs are available
- Targeted native No-CRS runtime: real local P1--P4-safe evidence; full matrix
  and capability promotion not run
- With-CRS runtime: not run
- RESPONSE_BODY blocking: `unsupported_by_host_model` for `forwardAuth`; the
  separate native UDS probe has only non-promoted P4 safe/log-only evidence

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

The starter itself claims no No-CRS, With-CRS, RESPONSE_BODY, negative/
pass-through, audit/log, or Traefik runtime result. The separate native UDS
host probe records only its targeted metadata-only evidence.

## Parallel Runtime-Smoke Phase

Phase 1 compatibility targets Traefik `forwardAuth`. The native Go middleware
has a separate pinned-host UDS probe with Common/libmodsecurity rule execution;
that targeted result has no runtime promotion.

The Traefik connector-specific surface is limited to:

- forwardAuth compatibility integration and configuration;
- native local-plugin UDS engine service and host harness;
- Traefik smoke harness entrypoints and local decision-service starter code.

Shared request, response, intervention, status, logging, capabilities, origin,
and transaction concepts come from `common/include/msconnector/`. Runtime smoke
evidence is written through `common/scripts/write_smoke_result.py`, so Traefik
does not maintain its own JSON result writer.

`make smoke-traefik` sources the framework common smoke wrapper, which sources
`modules/ModSecurity-test-Framework/ci/lib/common.sh`. Runtime dependencies are not
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
`modules/ModSecurity-test-Framework/ci/provisioning/runtime-components.manifest.json`.
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
- The selected native host probe sets Common integration mode to
  `native-traefik-middleware`, sends host outcomes only after ResponseWriter
  confirmation, and retains separate raw decision and host-outcome events.
- Connector-specific code remains responsible for the host profile, build glue, example configuration, and process entry point.
- Response mapping is linked for contract checking only; upstream response inspection is unsupported by `forwardAuth`.
- No production, CRS-complete, full-matrix, broad runtime, or RESPONSE_BODY verification is claimed.

## Compatibility and native Phase-4 boundary

The compatibility host model is Traefik `forwardAuth`. It executes before
upstream handling and cannot inspect the later upstream response body.
Consequently, for that compatibility path,
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are
`unsupported_by_host_model`, not merely absent from a local run.

The separate selected native UDS probe does observe the upstream response. It
has targeted evidence for a P3 pre-commit denial and a P4 post-commit
`log_only` outcome with original and visible status metadata. It cannot prove
a late abort; strict P4 is `NOT EXECUTED`. Neither path changes a capability
state without the separate canonical evidence/promotion process.

No response-body payload belongs in an event or report.
