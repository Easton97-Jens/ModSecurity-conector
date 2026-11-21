# Rust-Connector-Workspace

Dieser Workspace enthält die Rust-Grundlage der Connector-Neuentwicklung.

## Aktuelle Crates

- `msconnector-core`: hostneutrale Lifecycle-, Phasen-, Body- und Interventionsmodelle.
- `msconnector-ffi`: unsichere Grenze zur externen C++-Engine `libmodsecurity`.
- `msconnector-host-api`: panic-geschützte C-ABI für dünne native Hostadapter.
- `msconnector-proxy`: eigenständiger HTTP-Reverse-Proxy mit P1/P2/P3/P4-Transaktionen.

## Engine-Vertrag

Die Implementierung bindet `libmodsecurity v3.0.17` oder eine kompatible 3.x-ABI.
Regelladen, Entscheidungen und engine-eigene Bodylimits bleiben bei
`libmodsecurity`. Rust verwaltet Transportpuffer, exakt einmalige Body-Abschlüsse,
native Handle-Lebensdauer, Transaction-Cleanup und Panic-Eindämmung.

## Build

Setzen Sie `MODSECURITY_ROOT` und `LD_LIBRARY_PATH` auf einen installierten
`libmodsecurity`-Prefix, zum Beispiel:

```sh
MODSECURITY_ROOT=/var/tmp/codex/git/modsecurity-v3.0.17-prefix \
LD_LIBRARY_PATH=/var/tmp/codex/git/modsecurity-v3.0.17-prefix/lib \
cargo test --workspace --locked
```

## Status

Core, FFI und eigenständiger Proxy-Runtime sind implementiert. Apache, NGINX,
HAProxy HTX/SPOE, Envoy ext_proc/ext_authz, Traefik UDS/forwardAuth sowie
lighttpd patched/stock benötigen weitere Implementierung und echte Hostnachweise
vor einer Freigabe.
