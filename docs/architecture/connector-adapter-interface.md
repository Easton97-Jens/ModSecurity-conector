# Connector Adapter Interface

This document is the stable contract for future connector harnesses. It is not
a webserver implementation plan.

## Connector-Neutral Responsibilities

The shared runner owns YAML loading, capability/status validation, rule
materialization, request body/header generation, expected HTTP status checks,
stable audit-log checks, and summary JSON generation.

Connector code owns only server-specific build/runtime mechanics: module
loading, server configuration, request dispatch, log collection, and cleanup.

## Required Hooks

| Hook | Responsibility |
| --- | --- |
| `prepare()` | Validate prerequisites and create generated directories under `BUILD_ROOT` |
| `start()` | Start the real server process with the connector module loaded |
| `stop()` | Stop the server process without leaving stale listeners |
| `reload()` | Reload configuration where the connector supports it; otherwise document unsupported |
| `apply_rules()` | Install generated ModSecurity rules for one case |
| `materialize_case()` | Turn shared YAML artifacts into connector-specific config files |
| `send_request()` | Send the real HTTP request from the YAML case |
| `collect_logs()` | Copy or reference server, connector, audit, and access logs |
| `summarize_results()` | Write connector JSON/text results using shared schema |
| `cleanup()` | Remove or isolate runtime state under `BUILD_ROOT` |

## Shared Metadata Models

Future adapters should report the same append-only metadata used by the current
Apache and NGINX harnesses:

- `msconnector_status`: neutral operation result (`ok`, `error`, `blocked`,
  `unsupported`) mapped from runtime smoke status.
- `msconnector_origin`: source repository, revision/version, license, and
  imported path metadata for the connector module under test.
- `msconnector_intervention`: disruptive flag, HTTP intervention status when
  disruptive, and optional log message.

The current shell/Python harnesses serialize these shapes as JSON. They do not
instantiate the C structs through FFI.

Phase 3 adds small Common C helper implementations for those shapes. Existing
Apache and NGINX harnesses still use Python/Shell and mirror the schema through
`modules/ModSecurity-test-Framework/tests/runners/msconnector_models.py`.

## Boundary Rules

- `common/` and `docs/imports/common/` remain connector-neutral.
- `connectors/<name>/` contains server-specific build/runtime logic.
- Generated configs, logs, downloads, and binaries stay under `BUILD_ROOT`.
- Direct libmodsecurity API success never counts as connector success.

Future Envoy, Lighttpd, and Traefik adapters must prove the same
`real-world-connector-path` semantics before any common case is counted as PASS.
HAProxy already has an evidence-scoped SPOA/SPOP runtime path; broader HAProxy
capability gaps remain report-owned until runtime evidence supports promotion.
