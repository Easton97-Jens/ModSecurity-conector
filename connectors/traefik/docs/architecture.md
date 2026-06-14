# Traefik Architecture

Status: decision-service-starter
Runtime status: not-verified

The repository now has a Traefik local decision-service starter, not a selected
runtime integration architecture. The implemented Traefik-specific code is
repo-owned C metadata/capability source plus a local in-memory allow/block
decision model that compiles against the connector-neutral `common/` layer.

Global scaffold gates remain in
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Repository Evidence

- `common/include/msconnector/` provides connector-neutral metadata,
  capability, origin, status, request, response, transaction, and intervention
  data shapes.
- `common/src/` provides connector-neutral helper implementations.
- Apache and NGINX keep server-specific lifecycle, hook, filter, build, and
  harness logic in adapter-owned connector trees.
- No Traefik API, Traefik plugin SDK, Traefik Go module, or Traefik runtime
  source is present in `connectors/traefik`.

## Integration Path Decision

Implemented path: local decision-service starter.

This path is selected because it can be built entirely from repository-local C
code and shared connector-neutral structures. It models the smallest next step
toward an external decision service: request data in, allow/block decision out.
It does not open a socket, implement Traefik `forwardAuth`, process Traefik
traffic, call libmodsecurity, or load CRS.

## Option Evaluation

| Option | Current decision | Reason |
| --- | --- | --- |
| Traefik plugin | deferred | No Go module, plugin SDK, or Traefik plugin API is present in the repo |
| Traefik middleware | deferred | No middleware API or Traefik Go dependency is present in the repo |
| `forwardAuth` / external HTTP decision service | starter only | Local decision model exists, but no HTTP server, Traefik config, or runtime harness exists |
| Sidecar / proxy bridge | deferred | No bridge runtime, proxy config, or harness exists |
| Custom module/build | deferred | No Traefik source/build contract exists |

A future runtime path must document the exact Traefik version/API, source or SDK
origin, license, build command, configuration, ModSecurity integration point,
request/response mapping, intervention mapping, logging behavior, and runtime
results.
