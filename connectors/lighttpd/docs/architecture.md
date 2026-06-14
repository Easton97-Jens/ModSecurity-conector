# lighttpd Architecture

Status: bridge-starter
Runtime status: not-verified
Integration path: decision-service bridge starter; runtime integration deferred

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

This scope uses connector-neutral `common/` origin, status, intervention, and
capability helpers. It does not include lighttpd headers, call lighttpd APIs,
call ModSecurity APIs, implement FastCGI/SCGI protocol handling, map real
request/response hooks, or implement runtime intervention handling.

## Integration Path Decision

| Option | Decision | Reason |
| --- | --- | --- |
| Native lighttpd module | deferred/blocked | No selected lighttpd headers, SDK/source tree, or module build system is present in this repository. |
| FastCGI bridge | deferred/blocked | No FastCGI protocol adapter or lighttpd FastCGI runtime configuration is present. |
| SCGI bridge | deferred/blocked | No SCGI protocol adapter or lighttpd SCGI runtime configuration is present. |
| External HTTP service / sidecar | starter selected | A local decision-service starter is possible without fake lighttpd or ModSecurity API claims. It does not process real traffic. |

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

## Blockers Before Adapter Ownership

A real lighttpd adapter needs, at minimum:

- a selected production integration path;
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
