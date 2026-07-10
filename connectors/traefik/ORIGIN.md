# Traefik Connector Origin

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: targeted local 200/403; broader verification remains open

No upstream Traefik connector source has been imported into this repository.
No Traefik plugin SDK, middleware SDK, Go module, cgo bridge, or Traefik runtime
source is vendored under `connectors/traefik`. The selected integration boundary
is Traefik's external HTTP `forwardAuth` protocol.

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
| `connectors/traefik/src/traefik_modsecurity_mapper.c` | repo-owned adapter source | not selected | repository root license not documented | Thin Common mapper callsites |
| `connectors/traefik/src/traefik_forwardauth_service_main.c` | repo-owned adapter source | not selected | repository root license not documented | Common HTTP authorization service host profile |
| `connectors/traefik/build/build-connector.sh` | repo-owned build helper | not selected | repository root license not documented | C17 compile/link-only service build |
| `connectors/traefik/scripts/check-config.sh` | repo-owned validation helper | not selected | repository root license not documented | Configuration check entry point |
| `connectors/traefik/scripts/start-smoke.sh` | repo-owned validation helper | not selected | repository root license not documented | Process-only start/stop smoke |
| `connectors/traefik/scripts/runtime-smoke.sh` | repo-owned validation helper | not selected | repository root license not documented | Runtime-smoke entry point |
| `connectors/traefik/scripts/runtime_smoke.py` | repo-owned validation helper | not selected | repository root license not documented | Traefik/forwardAuth/upstream orchestration and evidence |
| `connectors/traefik/config/traefik-forwardauth.conf` | repo-owned example config | not selected | repository root license not documented | Request-phase configuration; response processing disabled |
| `connectors/traefik/config/traefik-forwardauth-dynamic.yaml` | repo-owned example config | not selected | repository root license not documented | Start-smoke Traefik File Provider template |

## Not Imported

- Traefik source: not selected.
- Traefik plugin or middleware SDK: not selected.
- Traefik Go module: not present.
- Traefik plugin/cgo integration source: not present and not selected.

## Runtime Claim

None. This origin file documents repo-owned source and build boundaries only.
It does not establish Traefik runtime compatibility, a tested deployment on the
current commit, CRS completeness, response-phase processing, or production
readiness.
