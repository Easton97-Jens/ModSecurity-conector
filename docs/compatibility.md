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
| Apache connector | scaffolded | Local v3 connector analyzed, no code imported |
| NGINX connector | scaffolded | Local v3 connector analyzed, no code imported |
| HAProxy connector | unknown | SPOE/Lua/native options documented, implementation undecided |
| Envoy connector | unknown | HTTP filter/ext_authz/Wasm options documented, implementation undecided |
| Lighttpd connector | unknown | Native plugin and mod_magnet options documented, implementation undecided |
| Traefik connector | unknown | Yaegi/Wasm plugin options documented, implementation undecided |
| v2 regression reuse | planned | Only portable rule/engine semantics may enter `tests/common/` |

## Capability Rule

Tests and connector docs must name required capabilities. If a behavior depends
on hook timing, buffering, streaming, log artifacts, reload semantics, or server
configuration, it is connector-specific unless proven portable.
