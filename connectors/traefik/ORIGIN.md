# Traefik Connector Origin

Status: decision-service-starter
Runtime status: not-verified

No upstream Traefik connector source has been imported into this repository.
No Traefik API, Traefik plugin SDK, middleware SDK, or Traefik runtime source is
vendored under `connectors/traefik`.

## Current Source Inventory

| Path | Origin | Upstream version | License status | Notes |
| --- | --- | --- | --- | --- |
| `connectors/traefik/metadata.c` | repo-owned starter metadata | not selected | repository root license not documented | Compile-time metadata for the local starter |
| `connectors/traefik/metadata.h` | repo-owned starter metadata | not selected | repository root license not documented | Compile-time metadata declarations |
| `connectors/traefik/src/traefik_build_starter.c` | repo-owned build-starter source | not selected | repository root license not documented | Does not include Traefik or libmodsecurity APIs |
| `connectors/traefik/src/traefik_decision_service.h` | repo-owned decision-service starter | not selected | repository root license not documented | Local decision model declarations |
| `connectors/traefik/src/traefik_decision_service.c` | repo-owned decision-service starter | not selected | repository root license not documented | Local request decision logic only |
| `connectors/traefik/src/traefik_decision_service_main.c` | repo-owned decision-service starter | not selected | repository root license not documented | CLI/self-test entry point only |
| `connectors/traefik/build/build-starter.sh` | repo-owned build helper | not selected | repository root license not documented | Compiles metadata and decision-service starters |
| `connectors/traefik/Makefile` | repo-owned build helper | not selected | repository root license not documented | Connector-local build/self-test targets |

## Not Imported

- Traefik source: not selected.
- Traefik plugin or middleware SDK: not selected.
- Traefik Go module: not present.
- libmodsecurity runtime integration source: not present for Traefik.

## Runtime Claim

None. This origin file documents repo-owned compile-time and local decision-
service starter code only. It does not establish adapter ownership, Traefik
runtime compatibility, a tested `forwardAuth` deployment, CRS execution, or
ModSecurity request/response processing.
