# Rust Connector Workspace

This workspace contains the Rust foundation of the connector rewrite.

## Current crates

- `msconnector-core`: host-neutral lifecycle, phase, body and intervention types.
- `msconnector-ffi`: unsafe boundary for the external `libmodsecurity` C++ engine.
- `msconnector-host-api`: panic-contained C ABI for thin native host adapters.
- `msconnector-proxy`: standalone HTTP reverse proxy with P1/P2/P3/P4 transaction phases.

## Engine contract

The engine implementation targets `libmodsecurity v3.0.17` or a compatible 3.x ABI.
Rule loading, transaction decisions and engine-owned body limits remain owned by
`libmodsecurity`. Rust owns transport buffers, exactly-once body completion,
native handle lifetime, transaction cleanup and panic containment.

## Build

Set `MODSECURITY_ROOT` and `LD_LIBRARY_PATH` to an installed `libmodsecurity`
prefix, for example:

```sh
MODSECURITY_ROOT=/var/tmp/codex/git/modsecurity-v3.0.17-prefix \
LD_LIBRARY_PATH=/var/tmp/codex/git/modsecurity-v3.0.17-prefix/lib \
cargo test --workspace --locked
```

## Status

Core, FFI and standalone proxy runtime are implemented. Apache, NGINX,
HAProxy HTX/SPOE, Envoy ext_proc/ext_authz, Traefik UDS/forwardAuth and
lighttpd patched/stock host adapters require separate implemented and hosted
runtime evidence before promotion.
