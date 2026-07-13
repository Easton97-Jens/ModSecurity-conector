# Traefik Connector Origin

Status: forwardAuth compatibility smoke plus targeted native UDS host probe
Runtime status: targeted local P1--P4-safe evidence; broader verification remains open

No upstream Traefik connector source has been imported into this repository.
The repository owns a small standard-library Go module under
`native_middleware/`; it is not imported Traefik source, a Traefik SDK, or a
cgo bridge. The standard compatibility boundary remains Traefik's external
HTTP `forwardAuth` protocol; the full-lifecycle host probe separately selects
the native local plugin and its repo-owned persistent UDS Common/libmodsecurity
bridge without changing capability declarations.

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
| `connectors/traefik/src/traefik_engine_protocol.h` | repo-owned UDS protocol | selected by non-promoted full-lifecycle host probe | repository root license not documented | Bounded P1--P4 lifecycle and host-outcome contract |
| `connectors/traefik/src/traefik_engine_service.c` | repo-owned Common/libmodsecurity service | selected by non-promoted full-lifecycle host probe | repository root license not documented | Persistent private UDS engine service |
| `connectors/traefik/native_middleware/middleware.go` | repo-owned Go middleware source | selected by non-promoted full-lifecycle host probe | repository root license not documented | Bounded streaming wrapper with passthrough default and UDS selection |
| `connectors/traefik/native_middleware/engine_uds.go` | repo-owned Go UDS client | selected by non-promoted full-lifecycle host probe | repository root license not documented | One session per host request to the persistent engine service |
| `connectors/traefik/native_middleware/middleware_test.go` | repo-owned Go unit tests | selected by non-promoted full-lifecycle host probe | repository root license not documented | Focused source-level behavior tests |
| `connectors/traefik/native_middleware/engine_uds_test.go` | repo-owned Go UDS tests | selected by non-promoted full-lifecycle host probe | repository root license not documented | Lifecycle and host-outcome ordering tests |
| `connectors/traefik/native_middleware/go.mod` | repo-owned Go module metadata | selected only by non-promoted full-lifecycle host probe | repository root license not documented | No external dependencies |
| `connectors/traefik/native_middleware/.traefik.yml` | repo-owned plugin manifest | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Traefik plugin metadata/test data; pinned host load probe exists |
| `connectors/traefik/build/build-native-middleware.sh` | repo-owned build helper | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Go source build/test command, outside-checkout report only |
| `connectors/traefik/config/traefik-native-middleware-dynamic.yaml` | repo-owned example config | selected by non-promoted full-lifecycle host probe | repository root license not documented | Reference local-plugin File Provider shape |
| `connectors/traefik/config/traefik-native-middleware-static.yaml` | repo-owned example config | selected by non-promoted full-lifecycle host probe | repository root license not documented | Reference local-plugin registration shape |
| `connectors/traefik/scripts/runtime_native_smoke.py` | repo-owned host harness | selected by non-promoted full-lifecycle host probe | repository root license not documented | Isolated host, UDS engine, canonical-rule, and metadata-only outcome orchestration |

## Not Imported

- Traefik source: not selected.
- Traefik plugin or middleware SDK: not selected.
- Traefik Go module: not imported; the repo-owned standard-library module is
  a local-plugin source package, not upstream SDK source.
- Traefik plugin/cgo integration source: not present and not selected.

## Runtime Claim

This file does not make a capability claim. It documents repo-owned source and
build boundaries only; the targeted host probe does not establish CRS
completeness, full response-phase coverage, or production readiness.
