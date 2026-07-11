# Envoy Connector Build

Status: C17 compile/link verified; targeted ext_authz request path is
`minimal_runtime_smoke` / `connector-gap`.

## Connector service

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

`MODSECURITY_PREFIX` or `MODSECURITY_LIB_FILE` may be used instead. The build
accepts Framework-resolved values through the same variables. It compiles with
`-std=c17 -Wall -Wextra -Werror`, links Common SDK/runtime, the Envoy profile and
thin mappers, and records a local rpath to the explicitly selected
libmodsecurity directory.

Output:

```text
${BUILD_ROOT}/envoy-connector/msconnector_envoy_ext_authz
```

`BUILD_ROOT` must be absolute and outside the checkout. The build target does
not execute the binary, validate config, start a process, or send a request.

## Separate gates

```sh
make -C connectors/envoy check-envoy-config RULES_FILE=/absolute/rules.conf
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
```

The older `build-starter` and `self-test` targets remain isolated compatibility
checks for the local bridge CLI and do not build or verify the connector service.

## Separate ext_proc source/build target

The unpromoted Go external-processing service is independently pinned and does
not link libmodsecurity yet:

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
```

`go.mod`/`go.sum` pin Envoy's official generated Go API and gRPC dependencies.
`config/envoy-ext-proc-versions.env` pins the intended Envoy release. The build
uses `go mod verify` and `go build -mod=readonly`; the config materializer only
writes to `BUILD_ROOT`. These commands do not start Envoy, call Common or
libmodsecurity, or validate runtime interoperability.
