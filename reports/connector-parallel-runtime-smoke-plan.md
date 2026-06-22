# Connector Parallel Runtime Smoke Plan

Status: parallel phase started for Envoy, Traefik, and lighttpd.

## Why Common msconnector Contracts Are Used

`common/include/msconnector/` is the connector-neutral contract boundary for all
open connectors. Envoy, Traefik, and lighttpd must translate their own runtime
inputs into these shared shapes instead of creating connector-local copies of
request, response, intervention, status, logging, capability, origin,
transaction, or decision models.

The shared contracts currently used or reserved for the open connectors are:

| Area | Global component |
| --- | --- |
| Request mapping | `msconnector/request.h`, `msconnector/request.hpp` |
| Response mapping | `msconnector/response.h`, `msconnector/response.hpp` |
| Intervention/block decisions | `msconnector/intervention.h`, `msconnector/intervention.hpp` |
| Status values | `msconnector/status.h`, `msconnector/status.hpp` |
| Logging | `msconnector/logging.h`, `msconnector/logging.hpp` |
| Options/directives | `msconnector/options.h`, `msconnector/directives.h` |
| Capabilities | `msconnector/capabilities.h`, `msconnector/capabilities.hpp` |
| Origin/metadata | `msconnector/origin.h`, `msconnector/origin.hpp` |
| Transaction lifecycle and decision view | `msconnector/transaction.h`, `msconnector/transaction.hpp` |
| Rule-load stats | `msconnector/rule_load_stats.h` |

## Shared Logic

The parallel runtime-smoke entrypoints share result/evidence writing through:

- `common/scripts/write_smoke_result.py`
- `common/scripts/run_blocked_runtime_smoke.sh`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh`

These helpers centralize:

- `result.json`, `summary.json`, `summary.txt`, and `results.jsonl` writing;
- the common `runtime_verified=false` / `production_ready=false` /
  `full_matrix_ready=false` / `crs_complete=false` claim defaults;
- `claims_not_allowed`;
- `missing_dependencies`;
- Exit-77 BLOCKED result semantics;
- the `msconnector_decision` status/intervention/reason shape used by open C
  adapters;
- local runtime binary lookup without global `PATH` fallback;
- compatibility summary files under `$RESULTS_DIR`.

No connector-specific runtime terms are encoded in the common helpers. Each
connector passes its own connector name, integration mode, skipped reason,
missing dependency description, and architecture decision text.

## Runtime Dependency Policy

Runtime dependencies are never installed globally by connector smokes. The
smokes must not run `apt install`, `apt-get install`, `yum install`,
`dnf install`, `apk add`, `brew install`, `go install`, or `npm install -g`, and
they must not write runtime artifacts under `/usr/local`, `/usr/bin`, or `/opt`.

`modules/ModSecurity-test-Framework/ci/common.sh` is the source of truth for
runtime, build, log, cache, source, and component-cache paths. The open
connector smoke wrappers source `connector-smoke-common.sh`, which sources
`common.sh` and provides the connector-neutral lookup helpers.

Dependency lookup order:

1. explicit binary environment variable, such as `ENVOY_BIN`, `TRAEFIK_BIN`, or
   `LIGHTTPD_BIN`;
2. local common.sh-managed caches and runtime roots:
   `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
   `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
   `$SOURCE_ROOT`;
3. connector/project-defined local dependency directories under those roots;
4. Exit 77 with BLOCKED evidence if no local binary is found.

Examples:

```sh
ENVOY_BIN=/path/to/local/envoy make smoke-envoy
TRAEFIK_BIN=/path/to/local/traefik make smoke-traefik
LIGHTTPD_BIN=/path/to/local/lighttpd make smoke-lighttpd
```

## Connector-Specific Logic

Envoy keeps only Envoy-specific ext_authz design, configuration, smoke harness
entrypoint, and bridge-starter code. The Phase 1 runtime target is
`integration_mode=ext_authz`. `ext_proc` is deferred to a later phase.

Traefik keeps only Traefik-specific forwardAuth design, configuration, smoke
harness entrypoint, and local decision-service starter code. The Phase 1 runtime
target is `integration_mode=forwardAuth`. A Go plugin is out of scope for Phase
1.

lighttpd keeps only lighttpd-specific architecture-spike documentation,
configuration for the eventual path, smoke harness entrypoint, and bridge
starter code. The Phase 1 mode is
`integration_mode=architecture_spike_plus_runtime_smoke`. The spike must compare
native module, FastCGI/SCGI, sidecar/proxy, and mod_magnet/Lua before selecting
the runtime path.

## Claims Still Forbidden

The open connectors must not claim:

- `runtime_verified=true`
- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`

They also must not generate full-matrix reports, production-readiness reports,
or CRS-complete claims from starter/self-test evidence.

## Parallel Runtime-Smoke Artifacts

Each connector writes connector-specific artifacts:

| Connector | Evidence root | Fallback |
| --- | --- | --- |
| Envoy | `$VERIFIED_RUN_ROOT/envoy-smoke/` | `$BUILD_ROOT/results/envoy-smoke/` |
| Traefik | `$VERIFIED_RUN_ROOT/traefik-smoke/` | `$BUILD_ROOT/results/traefik-smoke/` |
| lighttpd | `$VERIFIED_RUN_ROOT/lighttpd-smoke/` | `$BUILD_ROOT/results/lighttpd-smoke/` |

Each `result.json` contains at least:

- `connector`
- `integration_mode`
- `runtime_verified`
- `full_matrix_ready`
- `production_ready`
- `crs_complete`
- `response_body_verified`
- `allowed_request_status`
- `blocked_request_status`
- `evidence_root`
- `timestamp`
- `skipped_reason`
- `missing_dependencies`
- `claims_not_allowed`

## Current Expected Outcomes

`make smoke-envoy`, `make smoke-traefik`, and `make smoke-lighttpd` are targeted
runtime-smoke entrypoints. In environments without the selected runtime binaries
and real libmodsecurity-backed adapters, they must exit 77 with BLOCKED evidence
rather than reporting success.

Current blockers:

- Envoy: local `envoy` binary is not available through `ENVOY_BIN` or
  common.sh-managed local paths.
- Traefik: local `traefik` binary is not available through `TRAEFIK_BIN` or
  common.sh-managed local paths.
- lighttpd: production integration path has not been selected; when no local
  binary is available, `missing_dependencies` includes `lighttpd`.

## Duplicate Avoidance

The previous connector-local inline JSON writers in the Envoy, Traefik, and
lighttpd harnesses have been replaced by common helpers. The connector harnesses
now provide adapter parameters only. The small connector-local decision result
structs have also been replaced with aliases to `msconnector_decision`, leaving
only connector-specific adapter function names. Request, response, status,
intervention, capability, origin, logging, transaction, and decision contracts
remain in `common/include/msconnector/`.

Apache, HAProxy, and Nginx are not modified by this parallel phase.
