# Envoy Source

**Language:** English | [Deutsch](README.de.md)

Status: ext_authz connector source; `minimal_runtime_smoke` / `connector-gap`
Runtime status: targeted request-header 200/403 path only

This directory contains repository-local source for the Envoy HTTP `ext_authz`
service and the older bridge self-test:

- `envoy_ext_authz_service_main.c`: connector-owned host profile and shared
  HTTP authorization service entry point.
- `envoy_modsecurity_mapper.h` / `.c`: thin C17 request, response, and config
  mapper functions over the Common generic mapper.
- `envoy_bridge.h`: bridge decision API over connector-neutral request data.
- `envoy_bridge.c`: deterministic allow/block decision model for local
  self-tests.
- `envoy_bridge_main.c`: CLI entry point for `--self-test`.

The service selects Envoy's external HTTP authorization model without importing
Envoy SDK types. It delegates configuration, libmodsecurity lifecycle, bounded
HTTP parsing, transaction handling, decisions, and event output to
`common/runtime/`. The response mapper is linked for contract completeness, but
`ext_authz` remains request-phase only.

The older bridge starter does not call Envoy or libmodsecurity APIs and remains
self-test-only. Neither source presence nor its self-test is runtime evidence.
