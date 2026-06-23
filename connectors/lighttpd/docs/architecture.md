# lighttpd Architecture

Status: bridge-starter plus sidecar_proxy runtime-smoke path
Runtime status: locally verifiable with a staged lighttpd binary
Integration path: sidecar_proxy for Phase 1; native module and FastCGI/SCGI deferred

The repository now contains a concrete lighttpd decision-service bridge starter.
It is a local CLI/self-test integration point only, not a production lighttpd
adapter.

## Current Implemented Scope

Implemented lighttpd-specific code is limited to:

- repo-owned metadata in `connectors/lighttpd/metadata.c` and
  `connectors/lighttpd/metadata.h`;
- a compile-time metadata/probe starter in
  `connectors/lighttpd/src/lighttpd_build_starter.c`;
- local bridge-starter data flow in `connectors/lighttpd/src/lighttpd_bridge.h`,
  `connectors/lighttpd/src/lighttpd_bridge.c`, and
  `connectors/lighttpd/src/lighttpd_bridge_main.c`;
- standalone compile scripts in `connectors/lighttpd/build/`;
- local `Makefile` targets for build/self-test starter checks.

This starter scope uses connector-neutral `common/` origin, status,
intervention, and capability helpers. It does not include lighttpd headers, call
lighttpd APIs, call ModSecurity APIs, implement FastCGI/SCGI protocol handling,
map native request/response hooks, or implement native-module intervention
handling. The separate Phase 1 runtime smoke uses lighttpd as a local HTTP
upstream behind a sidecar decision proxy.

## Integration Path Decision

| Option | Decision | Reason |
| --- | --- | --- |
| Native lighttpd module | deferred/blocked | No selected lighttpd headers, SDK/source tree, or module build system is present in this repository. |
| FastCGI bridge | deferred/blocked | No FastCGI protocol adapter or lighttpd FastCGI runtime configuration is present. |
| SCGI bridge | deferred/blocked | No SCGI protocol adapter or lighttpd SCGI runtime configuration is present. |
| External HTTP service / sidecar | selected Phase 1 mode | Lowest coupling to lighttpd internals and no dependency on native module ABI or FastCGI/SCGI protocol work. Runtime success requires real local lighttpd 200 and sidecar 200/403 evidence. |
| mod_magnet / Lua | spike only | Possible control-plane glue, but no selected Lua policy, request-body mapping, intervention semantics, or ModSecurity binding exists. |

Repository evidence for future lighttpd options exists in
`modules/ModSecurity-test-Framework/docs/imports/sources.md` and
`modules/ModSecurity-test-Framework/docs/future-connectors.md`, but those files
do not provide a local lighttpd SDK, module build, runtime harness, or
ModSecurity integration implementation.

## Bridge-Starter Semantics

The bridge starter can:

- compile a local decision-service starter binary;
- build local probe request data using shared request shapes;
- return an explicit blocked decision for the probe;
- self-test that no runtime capabilities are advertised.

The bridge starter cannot:

- run as a lighttpd module;
- implement FastCGI or SCGI;
- receive real lighttpd traffic;
- call libmodsecurity;
- load CRS;
- prove No-CRS, With-CRS, RESPONSE_BODY, audit/log, or negative/pass-through
  behavior.

## Selected Phase 1 Mode

The selected Phase 1 runtime direction is sidecar/proxy. It keeps the first
runtime boundary outside the lighttpd module ABI, avoids committing to
FastCGI/SCGI protocol ownership before the adapter contract is mature, and can
be validated with explicit HTTP allow/block evidence.

That mode can prove:

- a local common.sh-managed `lighttpd` binary can be resolved and started;
- allowed requests can pass through the selected sidecar/proxy path to lighttpd;
- blocked requests can return HTTP 403 before reaching the upstream path;
- evidence can be written with the shared smoke-result schema.

That mode cannot prove:

- native lighttpd module hook correctness;
- FastCGI/SCGI adapter semantics;
- request-body or response-body mapping inside lighttpd;
- CRS completeness, production readiness, or full matrix readiness.

The current harness may set `runtime_verified=true` only when a resolved local
lighttpd binary starts, direct lighttpd HTTP returns 200, the sidecar forwards an
allowed request with 200, and `X-Modsec-Smoke: block` returns 403. It also writes
`lighttpd_binary_verified`, `lighttpd_http_verified`,
`sidecar_proxy_verified`, `lighttpd_log_path`, `upstream_log_path`, and
`request_transcript_path` in the common result JSON.

With `DECISION_BACKEND=libmodsecurity`, the same sidecar path uses the shared
targeted libmodsecurity evaluator. The evaluator is built from
`common/scripts/modsecurity_targeted_eval.cc` against local common.sh-managed
headers and libraries, loads `common/rules/modsecurity_targeted_smoke.conf`, and
may set `modsecurity_backend_verified=true` only when rule `1000001` returns the
403 intervention for `X-Modsec-Smoke: block`.

## Blockers Before Adapter Ownership

A real lighttpd adapter needs, at minimum:

- production hardening for the selected sidecar_proxy path or a later selected
  native/FastCGI/SCGI path;
- lighttpd headers/SDK/source or documented bridge protocol/runtime
  dependencies;
- hook or bridge mapping for request headers, request body, response headers,
  response body, logging, and interventions;
- real ModSecurity API integration and rule loading;
- build output for the selected path;
- a framework-owned real-world runtime harness;
- No-CRS and With-CRS runtime evidence.

Until then, lighttpd remains bridge-starter only and must not be promoted to
adapter-owned or runtime-smoke-verified.

## Parallel Phase Target

The runtime-smoke target for the open-connector parallel phase is
`integration_mode=sidecar_proxy`. The architecture spike compared native module,
FastCGI/SCGI, sidecar/proxy, and mod_magnet/Lua; Phase 1 selects sidecar/proxy
while leaving the other paths deferred.

Shared data contracts remain in `common/include/msconnector/`:

- `request.h` / `response.h` for HTTP mapping;
- `intervention.h` for block decisions and future 403 responses;
- `status.h` for neutral pass/BLOCKED/error status values;
- `logging.h` for log records and callback shape;
- `capabilities.h` for capability claims;
- `origin.h` for source metadata;
- `transaction.h` for transaction/decision views.

Smoke evidence is generated by `common/scripts/write_smoke_result.py` via
`common/scripts/run_blocked_runtime_smoke.sh`. lighttpd must not add a separate
Result/Evidence JSON model. Current BLOCKED evidence records
`runtime_verified=false`, `production_ready=false`, `full_matrix_ready=false`,
and `crs_complete=false`.
