# Traefik Source

Status: decision-service-starter
Runtime status: not-verified

This directory contains:

- `traefik_build_starter.c`: compile-time metadata smoke source.
- `traefik_decision_service.h`: local decision-service starter declarations.
- `traefik_decision_service.c`: local in-memory allow/block decision logic.
- `traefik_decision_service_main.c`: CLI/self-test entry point.

These files are not a Traefik adapter. They do not include Traefik,
libmodsecurity, CRS, plugin, middleware, or `forwardAuth` runtime APIs.

Production source may be added only with repository-backed origin, license,
source-map, metadata, build, and validation evidence. Do not infer Traefik
adapter behavior from other connectors.
