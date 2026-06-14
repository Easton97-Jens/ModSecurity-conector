# Envoy Source

Status: bridge-starter
Runtime status: not-verified

This directory contains repository-local source for the Envoy sidecar/HTTP
bridge starter:

- `envoy_bridge.h`: bridge decision API over connector-neutral request data.
- `envoy_bridge.c`: deterministic allow/block decision model for local
  self-tests.
- `envoy_bridge_main.c`: CLI entry point for `--self-test`.

The bridge starter uses `msconnector_request`, `msconnector_intervention`, and
`msconnector_status` shapes from `common/`. It does not call Envoy APIs and does
not call libmodsecurity APIs.

Production source may only be added with repository-backed ORIGIN, license,
metadata, build, and runtime evidence. Do not add Envoy API calls,
libmodsecurity adapter lifecycle code, or adapter logic without the required
headers, build paths, and harness evidence.
