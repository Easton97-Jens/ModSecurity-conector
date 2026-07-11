# Traefik Source

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: broader connector behavior not verified

This directory contains:

- `traefik_build_starter.c`: compile-time metadata smoke source.
- `traefik_decision_service.h`: local decision-service starter declarations.
- `traefik_decision_service.c`: local in-memory allow/block decision logic.
- `traefik_decision_service_main.c`: CLI/self-test entry point.
- `traefik_modsecurity_mapper.c`: thin C17 functions delegating to the Common
  generic request/response mapper contracts.
- `traefik_forwardauth_service_main.c`: connector host profile and entry point
  for the shared HTTP authorization service runtime.

The selected adapter path is an external `forwardAuth` service. The separate
`../native_middleware/` Go module is unselected source/build groundwork with a
pass-through engine seam, not a cgo bridge or runtime claim. Upstream response
inspection is explicitly unsupported by the selected request-phase protocol,
even though the response mapper is linked for Common contract checking.

Production source may be added only with repository-backed origin, license,
source-map, metadata, build, and validation evidence. Do not infer Traefik
adapter behavior from other connectors.
