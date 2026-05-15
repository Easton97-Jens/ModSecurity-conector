# Compatibility

Status: scaffolded

## Version Position

The scaffold targets libmodsecurity v3 public APIs. v2 artifacts are not used as
architecture for new connectors.

## Current Compatibility Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Common headers | implemented | Connector-neutral C-compatible data shapes only |
| libmodsecurity v3 API mapping | planned | Public API sequence documented, not wrapped |
| Apache connector | scaffolded | Local source-built PoC observed expected HTTP behavior for all current shared minimal cases |
| NGINX connector | scaffolded | Local source-built PoC observed expected HTTP behavior for all current shared minimal cases |
| HAProxy connector | unknown | SPOE/Lua/native options documented, implementation undecided |
| Envoy connector | unknown | HTTP filter/ext_authz/Wasm options documented, implementation undecided |
| Lighttpd connector | unknown | Native plugin and mod_magnet options documented, implementation undecided |
| Traefik connector | unknown | Yaegi/Wasm plugin options documented, implementation undecided |
| v2 regression reuse | planned | Only portable rule/engine semantics may enter `tests/common/` |

## Capability Rule

Tests and connector docs must name required capabilities. If a behavior depends
on hook timing, buffering, streaming, log artifacts, reload semantics, or server
configuration, it is connector-specific unless proven portable.

## Shared Minimal Cases

The files under `tests/common/cases/minimal/` are portable rule/request models.
They are not proof that a connector supports the behavior until that
connector's runtime harness observes the expected HTTP response.

Observed locally on 2026-05-15 with `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Case | Capability area | Apache | NGINX |
| --- | --- | --- | --- |
| `audit_log_phase1_block.yaml` | query args, phase 1, audit log | pass, HTTP 403 plus audit fields | pass, HTTP 403 plus audit fields |
| `phase1_header_block.yaml` | request headers, phase 1 | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_block.yaml` | query args, phase 2 | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_pass.yaml` | query args, phase 2, pass-through | pass, HTTP 200 plus origin body | pass, HTTP 200 plus origin body |
| `request_body_json_block.yaml` | request body, JSON content type, raw body match | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_urlencoded_block.yaml` | form body, `ARGS_POST` | pass, HTTP 403 | pass, HTTP 403 |
| `response_header_basic.yaml` | response headers, phase 3 | pass, HTTP 403 | pass, HTTP 403 |

This proves only these PoC behaviors in this workspace, not full connector
compatibility, CRS support, multipart handling, streaming behavior, HTTP/2, or
complete response-body behavior.
