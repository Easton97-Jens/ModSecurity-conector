# Envoy Build

Status: bridge-starter
Runtime status: not-verified

Envoy has a local sidecar/HTTP bridge starter:

```sh
make -C connectors/envoy build-starter
make -C connectors/envoy self-test
```

The target compiles repository-local Envoy metadata and bridge starter code
against connector-neutral `common/` headers and sources. It does not build an
Envoy HTTP filter, external processing service, proxy-wasm module, or
libmodsecurity adapter.

## Current Build Starter

| Item | Value |
| --- | --- |
| Build command | `make -C connectors/envoy build-starter` |
| Self-test command | `make -C connectors/envoy self-test` |
| Sources | `connectors/envoy/src/envoy_bridge.c`, `connectors/envoy/src/envoy_bridge_main.c`, `connectors/envoy/metadata.c` |
| Headers | `connectors/envoy/src/envoy_bridge.h`, `connectors/envoy/metadata.h` |
| Shared code | `common/src/origin.c`, `common/src/capabilities.c`, `common/src/intervention.c`, `common/src/status.c` |
| Include paths | repository root, `common/include`, and `connectors/envoy/src` |
| Artifact path | `${BUILD_ROOT}/envoy-bridge-starter/envoy_bridge` |
| Default build root | `${XDG_STATE_HOME:-$HOME/.local/state}/ModSecurity-conector-build` |

## Production Adapter Blockers

A productive Envoy adapter build is blocked until one integration path supplies
real dependencies and a harness contract, for example:

- Envoy C++ SDK/API headers and build integration for a native HTTP filter;
- generated ext_proc protobuf/gRPC bindings and service dependencies;
- proxy-wasm SDK headers and WASM toolchain;
- or a documented sidecar/bridge protocol, Envoy configuration, and runtime
  harness.

A libmodsecurity-backed bridge is also blocked in this workspace because
`/src/ModSecurity-conector-build` and `/src/ModSecurity_V3` do not currently
provide the required `modsecurity.h`, `transaction.h`, `rules_set.h`, or
`libmodsecurity*` artifacts.

No production adapter build command is claimed here.

## Last Bridge-Starter Check

`make -C connectors/envoy build-starter` and `make -C connectors/envoy self-test`
were executed in this workspace. The self-test reported
`envoy_bridge_self_test: pass` for the local bridge decision model.

This is bridge-starter evidence only. It is not Envoy runtime evidence and not
ModSecurity runtime evidence.
